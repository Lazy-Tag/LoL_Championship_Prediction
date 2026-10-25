"""Public Riot schedule -> validated, conditional dynamic90 Swiss forecast.

Run --fetch --daily for unattended checks; --events PATH for a cached snapshot.
No edits to the frozen pre-tournament result. Refuse live series / knockout draws.
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import urllib.request
from collections import defaultdict
from datetime import datetime, date, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
from scipy.special import expit
from backtest import load_season, affiliations, prior_regions, key
from candidate_models import DynamicBT
from model import WORLD_TEAMS, series_probability
from prepare_data import ALIASES, LEAGUES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/live_s16'
REPORT = ROOT / 'reports/s16/live'
LOCAL = ROOT / '.local/live_s16'
SOURCE = 'https://lolesports.com/en-US/schedule'
CODES = list(WORLD_TEAMS)
BJ = ZoneInfo('Asia/Shanghai')
N = 14_000_605


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)


def fetch(now):
    request = urllib.request.Request(SOURCE, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=90) as r:
        html = r.read()
    folder = ROOT / 'data/raw' / ('live_' + now.strftime('%Y-%m-%dT%H%M%SZ'))
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'riot_schedule.html').write_bytes(html)
    events, decoder = {}, json.JSONDecoder()
    for m in re.finditer(r'\{"__typename":"EventMatch"', html.decode()):
        e, _ = decoder.raw_decode(html.decode()[m.start():])
        events[e['id']] = e
    if not any(e['league']['name'] == 'Worlds' for e in events.values()):
        raise ValueError('No Worlds events: source/parser changed; do not publish')
    save(folder / 'events.json', list(events.values()))
    return list(events.values()), str(folder.relative_to(ROOT))


def compact(e):
    return dict(id=e['id'], start_utc=e['startTime'], event=e['league']['name'],
                stage=e['blockName'], state=e['state'], best_of=e['match']['strategy']['count'],
                teams=[dict(name=t['name'], code=t['code'], wins=(t.get('result') or {}).get('gameWins', 0))
                       for t in e['matchTeams']], source=SOURCE)


def build_state(events, now):
    worlds = sorted([e for e in events if e['event'] == 'Worlds'], key=lambda e: (e['start_utc'], e['id']))
    if any(e['state'] not in ('completed', 'unstarted') for e in worlds):
        raise ValueError('A series is in progress: wait for a complete result')
    playins = [e for e in worlds if e['stage'] == 'Play-Ins' and e['state'] == 'completed']
    assert len(playins) == 6, 'Need six verified completed play-in matches'
    pi = max(playins, key=lambda e:e['start_utc'])['teams']
    qualifier = max(pi, key=lambda t:t['wins'])['code']
    active = [i for i, c in enumerate(CODES) if c not in ('KC', 'C9', 'MVK', 'FUR') or c == qualifier]
    w, loss, met = [0]*19, [0]*19, [0]*19
    completed = [e for e in worlds if e['stage'] == 'Swiss' and e['state'] == 'completed']
    for e in completed:
        a, b = [CODES.index(t['code']) for t in e['teams']]
        assert a in active and b in active
        assert w[a] == w[b] and loss[a] == loss[b] and max(w[a],loss[a]) < 3
        assert not met[a] & (1 << b), 'Unexpected Swiss rematch'
        assert e['best_of'] == (3 if w[a] == 2 or loss[a] == 2 else 1)
        x, y = [t['wins'] for t in e['teams']]
        assert max(x,y) == e['best_of']//2+1 and min(x,y) < max(x,y)
        winner, loser = (a,b) if x>y else (b,a)
        w[winner] += 1; loss[loser] += 1
        met[a] |= 1 << b; met[b] |= 1 << a
    assert completed, 'Initial Swiss round must be observed'
    # A partial round is supported. Unknown future rounds retain random draws.
    fixed = []
    for e in worlds:
        if e['state'] == 'completed' or any(t['code'] not in CODES for t in e['teams']):
            continue
        if e['stage'] != 'Swiss':
            raise ValueError('Published knockout pairing requires verified bracket support; keep last report')
        a,b = [CODES.index(t['code']) for t in e['teams']]
        assert w[a] == w[b] and loss[a] == loss[b] and max(w[a],loss[a])<3
        assert not met[a] & (1 << b)
        assert e['best_of'] == (3 if w[a] == 2 or loss[a] == 2 else 1)
        fixed.append(dict(**e, round=w[a]+loss[a]+1, a=a, b=b))
    assert len({f[k] for f in fixed for k in ('a','b')}) == 2*len(fixed)
    return active,w,loss,met,completed,fixed


def fit(events, now):
    raw = json.loads((ROOT/'data/series.json').read_text())
    seen = {str(r['id']) for r in raw}
    names = {key(r[k]):r[k] for r in raw for k in ('team1','team2')}
    names.update({key(t[0]):t[0] for t in WORLD_TEAMS.values()})
    aliases = {key(a):b for a,b in ALIASES.items()}
    added=[]
    for e in events:
        if e['event'] not in LEAGUES | {'Worlds'} or e['state'] != 'completed' or e['id'] in seen:
            continue
        assert e['start_utc'] <= now.isoformat().replace('+00:00','Z')
        if e['start_utc'][:10] <= '2026-10-14':
            continue  # Historical baseline includes reconciled non-Riot sources.
        a,b=e['teams']; x,y=a['wins'],b['wins'];bo=e['best_of']
        assert bo in (1,3,5) and max(x,y)==bo//2+1 and min(x,y)<bo//2+1
        normalized=[]
        for t in (a,b):
            name=aliases.get(key(t['name']),t['name'])
            assert key(name) in names, f'Unresolved team {name}'
            normalized.append(names[key(name)])
        added.append(dict(id=e['id'],date=e['start_utc'][:10],start_utc=e['start_utc'],event=e['event'],stage=e['stage'],team1=normalized[0],team2=normalized[1],wins1=x,wins2=y,best_of=bo,source=SOURCE))
        seen.add(e['id'])
    rows=[{**r,'team1':key(r['team1']),'team2':key(r['team2'])} for r in raw+added]
    previous={};preg={}
    for s in range(3,16):
        previous,_=load_season(s); rr=affiliations(previous,s)
        for t,v in preg.items():rr.setdefault(t,v)
        preg=rr
    prior,audit=prior_regions(previous,preg,90)
    mapping={'LPL':'CN','LCK':'KR','LEC':'EU','LCP':'LCP','LCS':'NA','CBLOL':'BR'};reg={}
    for r in rows:
        if r['event'] in mapping:
            for k in ('team1','team2'):reg[r[k]]=mapping[r['event']]
    for name,league,_ in WORLD_TEAMS.values():reg[key(name)]=mapping[league]
    for t,v in preg.items():reg.setdefault(t,v)
    teams=sorted({r[k] for r in rows for k in ('team1','team2')})
    assert set(teams)-set(reg) <= {'galions','solary'}, 'New unknown training regions'
    audit['live_unknown_regions']=sorted(set(teams)-set(reg))
    dyn=DynamicBT(teams,reg,prior);daily=defaultdict(list)
    for r in rows:daily[r['date']].append(r)
    for day,rr in sorted(daily.items()):dyn.advance(date.fromisoformat(day));dyn.update(rr)
    dyn.advance(now.date())
    return dyn.strengths(),added,audit,len(rows)


def verify(d):
    c=np.asarray(d['counts']);n=d['simulations'];j=np.asarray(d['joint'])
    assert c.shape==(19,4) and j.shape==(5,5)
    assert (c>=0).all() and (c<=n).all()
    assert list(c.sum(axis=0)) == [n,8*n,4*n,2*n]
    assert (c[:,0]<=c[:,3]).all() and (c[:,3]<=c[:,2]).all() and (c[:,2]<=c[:,1]).all()
    assert j.sum()==n and d['waived_draw_groups']==0
    assert sum(k*j[k,:].sum() for k in range(5))==c[:4,1].sum()
    assert sum(k*j[:,k].sum() for k in range(5))==c[4:8,1].sum()
    for i in range(19):
        if i not in d['active']:assert c[i].sum()==0
        if d['wins'][i]==3:assert c[i,1]==n
        if d['losses'][i]==3:assert c[i].sum()==0


def report(d,filename):
    n=d['simulations']; c=np.array(d['counts'])/n; j=np.array(d['joint'])/n
    pct=lambda p:f'{p*100:.2f}%'
    bj=datetime.fromisoformat(d['as_of']).astimezone(BJ)
    s=['# S16 赛中预测', '',f'更新时间：北京时间 {bj:%Y-%m-%d %H:%M}。已纳入 {len(d["completed_worlds"])} 场全球总决赛赛果，其中瑞士轮 {len(d["completed_swiss"])} 场。**出线指晋级八强。**', '',
       '已结束比赛按实际结果固定，已公布的下一轮对阵按实际抽签固定，其余赛程继续模拟。概率随新增赛果更新，不代表已确定的结果。','',
       '## 夺冠与晋级概率','', '| 夺冠概率排名 | 战队 | 赛区 | 当前瑞士轮战绩 | 八强 | 四强 | 决赛 | 冠军 |','|---:|---|---|---|---:|---:|---:|---:|']
    for rank,i in enumerate(sorted(range(19),key=lambda i:-c[i,0]),1):
        record=f'{d["wins"][i]}–{d["losses"][i]}' if i in d['active'] else '入围赛淘汰'
        s.append(f'| {rank} | {CODES[i]} | {WORLD_TEAMS[CODES[i]][1]} | {record} | {pct(c[i,1])} | {pct(c[i,2])} | {pct(c[i,3])} | {pct(c[i,0])} |')
    s+=['','## 最新一轮对阵预测','', '胜率为整场获胜概率；BO1 即小局胜率。选择概率较高的一方作为预测胜者。','', '| 北京时间 | 轮次 | 对阵 | 赛制 | 左方胜率 | 右方胜率 | 预测胜者 |','|---|---:|---|---|---:|---:|---|']
    for f in d['next_matches']:
        a,b=f['a'],f['b'];p=f['win_probability'];time=datetime.fromisoformat(f['start_utc'].replace('Z','+00:00')).astimezone(BJ)
        s.append(f'| {time:%m-%d %H:%M} | {f["round"]} | {CODES[a]} – {CODES[b]} | BO{f["best_of"]} | {pct(p)} | {pct(1-p)} | {CODES[a if p>=.5 else b]} |')
    if not d['next_matches']:s+=['','下一轮具体对阵尚未公布。']
    s+=['','## LPL、LCK 出线队伍数量','',f'LPL 预期出线 **{c[:4,1].sum():.2f} 队**；LCK 预期出线 **{c[4:8,1].sum():.2f} 队**。各队的出线概率见上表。','', '| 出线队伍数 | LPL | LCK |','|---:|---:|---:|']
    for k in range(5):s.append(f'| {k} | {pct(j[k,:].sum())} | {pct(j[:,k].sum())} |')
    s+=['','### 两赛区共同出线数量分布','', '每个单元格表示行、列所列两种数量同时发生的概率；已考虑同赛区交手和八强名额竞争。','', '| LPL \\ LCK | 0 队 | 1 队 | 2 队 | 3 队 | 4 队 |','|---:|---:|---:|---:|---:|---:|']
    for k in range(5):s.append(f'| {k} 队 | '+' | '.join(pct(p) for p in j[k])+' |')
    s+=['','## 已纳入的本届赛果','', '| 北京时间 | 阶段 | 对阵 | 比分 |','|---|---|---|---|']
    for e in d['completed_worlds']:
        a,b=e['teams'];time=datetime.fromisoformat(e['start_utc'].replace('Z','+00:00')).astimezone(BJ)
        s.append(f'| {time:%m-%d %H:%M} | {e["stage"]} | {a["code"]} – {b["code"]} | {a["wins"]}:{b["wins"]} |')
    s+=['','## 来源与解读范围','', '[官方赛程与比分](https://lolesports.com/en-US/schedule) · [官方赛制说明](https://lolesports.com/en-US/news/worlds-2026-primer) · [原赛前预测](../advancement.md) · [方法与假设](../../../MODEL.md)','',
        '使用当前已取得的当季比赛和新增赛果；原有历史覆盖缺口仍然存在。截止原快照后的 DCGI 已结束比赛也用于更新实力。赛中预测允许使用本次更新时间前已经结束的比赛，包括同日赛果；没有使用未结束比赛的胜负。','',
        '概率来自 14,000,605 次完整剩余赛程模拟，随机种子为 2026，并非全路径精确求和。单项概率的最坏情形 95% 抽样误差约为 ±0.026 个百分点，模型及赛制假设误差不包含在内。0.00% 可能是四舍五入；已淘汰队伍的概率为零。','',
        '未来瑞士轮保留交手历史、同战绩分组与重赛回避，并沿用可完成合法配对的最早空位顺延假设；这不等同于完整复现裁判的所有抽签裁量。本轮模拟没有触发回避豁免。尚未公布的八强签表按晋级战绩组生成。','',
        '剩余赛程冻结本次更新后的实力；未考虑全局 BP 局序、英雄消耗、换人、替补、选边、系列赛内相关性及参数不确定性。','']
    REPORT.mkdir(parents=True,exist_ok=True)
    (REPORT/filename).write_text('\n'.join(s))
    history=sorted((p for p in REPORT.glob('*.md') if p.name!='README.md'),reverse=True)
    index=['# S16 赛中预测','','包含夺冠与各阶段晋级概率、最新一轮对阵预测，以及 LPL／LCK 出线队伍数量分布。','','## 按日期查看','']
    index += [f'- [{p.stem}]({p.name})'+('（最新）' if i==0 else '') for i,p in enumerate(history)]
    index += ['','[原赛前预测](../advancement.md)保留用于对照。','']
    (REPORT/'README.md').write_text('\n'.join(index))



def main():
    p=argparse.ArgumentParser();p.add_argument('--fetch',action='store_true');p.add_argument('--events',type=Path);p.add_argument('--daily',action='store_true');p.add_argument('--publish',action='store_true');p.add_argument('--simulations',type=int,default=N);args=p.parse_args()
    now=datetime.now(timezone.utc); LOCAL.mkdir(parents=True,exist_ok=True)
    if args.publish and args.simulations==N:
        from publish_live_git import publish_latest
        publish_latest()  # Retry a previous completed report before fetching newer results.
    if args.daily and now.astimezone(BJ).date()>date(2026,11,1):
        print('Swiss monitoring period ended');return
    if args.fetch:raw,archive=fetch(now)
    else:raw=json.loads(args.events.read_text());archive=str(args.events.relative_to(ROOT)) if args.events.is_absolute() else str(args.events)
    old=json.loads((OUT/'observed_events.json').read_text()) if (OUT/'observed_events.json').exists() else []
    merged={e['id']:e for e in old}
    for e in raw:
        e=compact(e)
        if e['start_utc'][:4]=='2026' and e['event'] in LEAGUES|{'Worlds'}:merged[e['id']]=e
    events=sorted(merged.values(),key=lambda e:(e['start_utc'],e['id']))
    save(OUT/'observed_events.json',events)
    if args.daily:
        today=now.astimezone(BJ).date()
        todays=[e for e in events if e['event']=='Worlds' and datetime.fromisoformat(e['start_utc'].replace('Z','+00:00')).astimezone(BJ).date()==today]
        if todays and any(e['state']!='completed' for e in todays):
            print('Waiting until today\'s schedule is complete');return
    completed=[e for e in events if e['state']=='completed']
    fingerprint=hashlib.sha256(json.dumps(completed,sort_keys=True).encode()).hexdigest()
    status=json.loads((LOCAL/'status.json').read_text()) if (LOCAL/'status.json').exists() else {}
    if args.daily and (status.get('fingerprint')==fingerprint or status.get('updated_local_day')==now.astimezone(BJ).date().isoformat()):
        print('No new completed results / already updated today');return
    active,w,l,met,swiss,fixed=build_state(events,now)
    if args.daily:
        pending=[i for i in active if w[i]<3 and l[i]<3]
        if pending:
            earliest=min(w[i]+l[i] for i in pending)
            needs={i for i in pending if w[i]+l[i]==earliest}
            known={f[k] for f in fixed if f['round']==earliest+1 for k in ('a','b')}
            if not needs<=known:
                print('Waiting for the next round draw before daily publication');return
    print(f'Validated {len(swiss)} Swiss results and {len(fixed)} fixed next matches',flush=True)
    theta,added,audit,total=fit(events,now)
    matrices=[]
    for bo in (1,3,5):matrices.append([[float(series_probability(expit(theta[key(t[0])]-theta[key(u[0])]),bo)) for u in WORLD_TEAMS.values()] for t in WORLD_TEAMS.values()])
    stamp=now.strftime('%Y-%m-%dT%H%M%SZ');folder=OUT/stamp;folder.mkdir(parents=True)
    lines=[(ROOT/'results/simulation_input.txt').read_text().splitlines()[0]]
    for matrix in matrices:lines += [' '.join(map(str,row)) for row in matrix]
    lines += ['16',' '.join(map(str,active))]
    lines += [f'{w[i]} {l[i]} {met[i]}' for i in range(19)]
    lines += [str(len(fixed))]+[f'{f["round"]} {f["a"]} {f["b"]} {(1,3,5).index(f["best_of"])}' for f in fixed]
    inp=folder/'input.txt';inp.write_text('\n'.join(lines)+'\n')
    source=ROOT/'scripts/simulate_live.cpp';binary=LOCAL/'simulate_live'
    if not binary.exists() or source.stat().st_mtime>binary.stat().st_mtime:
        compiler=os.environ.get('CXX','/Library/Developer/CommandLineTools/usr/bin/clang++')
        subprocess.run([compiler,'-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk','-O3','-std=c++17',str(source),'-o',str(binary)],check=True)
    with inp.open('rb') as fin,(folder/'simulation.json').open('wb') as fout:
        subprocess.run([str(binary),str(args.simulations),'2026'],stdin=fin,stdout=fout,check=True)
    d=json.loads((folder/'simulation.json').read_text())
    for f in fixed:f['win_probability']=matrices[(1,3,5).index(f['best_of'])][f['a']][f['b']]
    d.update(as_of=now.isoformat(),model='dynamic90',active=active,wins=w,losses=l,met=met,next_matches=fixed,completed_swiss=swiss,completed_worlds=[e for e in completed if e['event']=='Worlds'],added_training=added,total_training_series=total,strengths=theta,prior_audit=audit,source_archive=archive,probabilities=matrices,engine_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),completed_fingerprint=fingerprint)
    verify(d);save(folder/'forecast.json',d)
    if args.simulations!=N:print('Pilot verified; not publishing');return
    filename=now.astimezone(BJ).date().isoformat()+'.md'
    if (REPORT/filename).exists():
        raise FileExistsError('A report already exists for this date; preserve it and publish on the next update date')
    report(d,filename);save(OUT/'latest.json',dict(snapshot=stamp,report='reports/s16/live/'+filename))
    save(LOCAL/'status.json',dict(fingerprint=fingerprint,updated_local_day=now.astimezone(BJ).date().isoformat(),snapshot=stamp))
    print('Published '+str(REPORT/filename),flush=True)
    if args.publish:publish_latest()

if __name__=='__main__':
    LOCAL.mkdir(parents=True,exist_ok=True)
    with (LOCAL/'update.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another update is running')
        else:main()

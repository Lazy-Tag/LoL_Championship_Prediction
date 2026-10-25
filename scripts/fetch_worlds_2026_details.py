"""Archive GOL completed Worlds maps and reconcile series with official scores.
This supplements fields only; never appends training outcomes or rewrites OE.
"""
import concurrent.futures,hashlib,json,re,urllib.request,urllib.error,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
from backtest import key
from model import WORLD_TEAMS
from prepare_data import ALIASES
R=Path(__file__).resolve().parents[1];RAW=R/'data/raw/detailed/worlds_2026_2026-10-25';OUT=R/'results/worlds_2026_details';REP=R/'reports/detailed_data/worlds_2026'
BASE='https://gol.gg';SOURCES=[]

def fetch(url):
    name=hashlib.sha256(url.encode()).hexdigest()[:20]+'.html';p=RAW/name
    if not p.exists():
        for attempt in range(3):
            try:
                b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read();p.write_bytes(b);break
            except urllib.error.HTTPError:raise
            except (urllib.error.URLError,TimeoutError,OSError) as e:
                with (RAW/'download_failures.jsonl').open('a') as log:log.write(json.dumps(dict(url=url,error=str(e),attempt=attempt+1))+'\n')
                if attempt==2:raise
                time.sleep(1)
    b=p.read_bytes();SOURCES.append(dict(url=url,raw_path=str(p.relative_to(R)),sha256=hashlib.sha256(b).hexdigest()))
    return BeautifulSoup(b,'html.parser')

def code(name):
    names={key(v[0]):c for c,v in WORLD_TEAMS.items()}
    aliases={key(a):b for a,b in ALIASES.items()};return names[key(aliases.get(key(name),name))]

def main():
    for p in (RAW,OUT,REP):p.mkdir(parents=True,exist_ok=True)
    series=[]
    for name,stage in [('Worlds%202026%20Main%20Event','Swiss'),('Worlds%202026%20Play-In','Play-Ins')]:
        url=BASE+'/tournament/tournament-matchlist/'+name+'/'
        page=fetch(url)
        for tr in page.select('table tr'):
            td=tr.find_all('td');a=tr.find('a',href=True)
            if len(td)!=7 or not a:continue
            score=re.fullmatch(r'(\d+)\s*-\s*(\d+)',td[2].get_text(strip=True))
            if not score:continue
            m=re.search(r'/game/stats/(\d+)/',a['href']);assert m
            series.append(dict(id=m[1],stage=stage,date=td[-1].get_text(strip=True),round=td[4].get_text(strip=True),patch=td[5].get_text(strip=True),team1=code(td[1].get_text(strip=True)),team2=code(td[3].get_text(strip=True)),wins1=int(score[1]),wins2=int(score[2]),source=url,summary_url=BASE+'/game/stats/'+m[1]+'/page-summary/'))
    official=json.loads((R/'results/live_s16/2026-10-25T015840Z/forecast.json').read_text())['completed_worlds']
    official=[e for e in official if e['event']=='Worlds' and e['state']=='completed'];matched=[]
    for r in series:
        candidates=[]
        for e in official:
            if e['stage']!=r['stage'] or {t['code'] for t in e['teams']}!={r['team1'],r['team2']}:continue
            scores={t['code']:t['wins'] for t in e['teams']}
            if (scores[r['team1']],scores[r['team2']])!=(r['wins1'],r['wins2']):continue
            delta=(datetime.fromisoformat(e['start_utc'].replace('Z','+00:00')).date()-datetime.fromisoformat(r['date']).date()).days
            if delta in (0,1):candidates.append(e)
        assert len(candidates)==1,('Unmatched/ambiguous series',r,candidates)
        r['official_id']=candidates[0]['id'];r['official_start_utc']=candidates[0]['start_utc'];matched.append(r)
    assert len({r['official_id'] for r in matched})==len(matched)==len(official)
    def links(r):
        p=fetch(r['summary_url']);ids=[]
        for a in p.find_all('a',href=True):
            label=a.get_text(' ',strip=True);m=re.fullmatch(r'Game (\d+)',label);gid=re.search(r'/game/stats/(\d+)/page-game/',a['href'])
            if m and gid:ids.append((int(m[1]),gid[1]))
        ids=sorted(set(ids));assert len(ids)==r['wins1']+r['wins2'],(r,ids)
        return [dict(series=r,game=number,id=gid) for number,gid in ids]
    with concurrent.futures.ThreadPoolExecutor(3) as pool:jobs=[g for batch in pool.map(links,matched) for g in batch]
    def game(job):
        gid=job['id'];u=BASE+'/game/stats/'+gid+'/page-game/';fu=u.replace('page-game','page-fullstats');p=fetch(u);f=fetch(fu)
        teams={}
        for side in ('blue','red'):
            tag=p.select_one('.'+side+'-line-header');assert tag and tag.find('a')
            label=tag.get_text(' ',strip=True);teams[side]=dict(code=code(tag.find('a').get_text(strip=True)),win=int(label.endswith('WIN')))
        assert sum(t['win'] for t in teams.values())==1
        assert {t['code'] for t in teams.values()}=={job['series']['team1'],job['series']['team2']}
        table=f.select_one('table.completestats');assert table
        fields={};champions=[]
        for tr in table.find_all('tr'):
            cells=tr.find_all(['th','td'])
            if len(cells)!=11:continue
            label=cells[0].get_text(' ',strip=True)
            if not label:
                champions=[Path(c.find('img')['src']).stem if c.find('img') else None for c in cells[1:]];continue
            fields[label]=[c.get_text(' ',strip=True) for c in cells[1:]]
            if label=='Player':
                for i,c in enumerate(cells[1:]):assert ('blueside' if i<5 else 'redside') in c.get('style','')
        assert len(fields['Player'])==10 and all(fields['Player']) and len(champions)==10
        for side,offset in [('blue',0),('red',5)]:
            teams[side]['players']=[dict(name=fields['Player'][i],role=fields['Role'][i],champion_asset=champions[i],stats={k:v[i] for k,v in fields.items() if k not in ('Player','Role')}) for i in range(offset,offset+5)]
            assert len(set(t['name'] for t in teams[side]['players']))==5
            teams[side]['total_gold']=sum(int(fields['Golds'][i]) for i in range(offset,offset+5))
            teams[side]['gold_difference_15']=sum(int(fields['GD@15'][i]) for i in range(offset,offset+5)) if all(fields.get('GD@15',['']*10)[i] for i in range(offset,offset+5)) else None
        if teams['blue']['gold_difference_15'] is not None and teams['red']['gold_difference_15'] is not None:
            assert teams['blue']['gold_difference_15']==-teams['red']['gold_difference_15']
        r=job['series'];return dict(game_id=gid,game=job['game'],official_series_id=r['official_id'],official_series_start_utc=r['official_start_utc'],source_date=r['date'],round=r['round'],stage=r['stage'],patch=r['patch'],sources=[u,fu],teams=teams)
    with concurrent.futures.ThreadPoolExecutor(3) as pool:games=list(pool.map(game,jobs))
    for r in matched:
        gg=[g for g in games if g['official_series_id']==r['official_id']]
        score=Counter(t['code'] for g in gg for t in g['teams'].values() if t['win'])
        assert score[r['team1']]==r['wins1'] and score[r['team2']]==r['wins2']
    summary=dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),series=len(matched),games=len(games),teams=len({t['code'] for g in games for t in g['teams'].values()}),source_date_min=min(g['source_date'] for g in games),source_date_max=max(g['source_date'] for g in games),training_outcomes_added=0,sources=SOURCES)
    for name,data in [('games',games),('series',matched),('audit',summary)]:
        (OUT/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# S16 世界赛详细小局数据','','本次从 Games of Legends 逐局页面补采，并与 Riot 已结束系列赛比分逐场核对。这里是新取得的世界赛数据，不代表已补齐七月至十月的全部国内联赛。','',f'覆盖 **{len(matched)} 场系列赛、{len(games)} 个小局、{summary["teams"]} 支战队**；来源比赛日期 {summary["source_date_min"]} 至 {summary["source_date_max"]}，对应官方赛程中的北京时间 10 月 25 日结束的第二轮。包含每局十名选手、红蓝方、英雄、版本、KDA、补刀、伤害、视野、最终经济与可取得的 15 分钟经济差。','','所有系列赛均与官方队伍及完整比分一致，小局胜负累计也与系列赛比分一致。来源日期保留原值；官方 UTC 开赛时间另存，允许经队伍、比分唯一确认的跨日差。没有向训练重复添加胜负。','','| 阶段 | 来源日期 | 小局 | 蓝方 | 红方 | 胜者 | 蓝方总经济 | 红方总经济 | 蓝方15分钟经济差 | 明细 |','|---|---|---:|---|---|---|---:|---:|---:|---|']
    for g in sorted(games,key=lambda g:(g['official_series_start_utc'],g['game'])):
        b,r=g['teams']['blue'],g['teams']['red'];file=g['game_id']+'.md';lines.append(f'| {g["stage"]} {g["round"]} | {g["source_date"]} | {g["game"]} | {b["code"]} | {r["code"]} | {b["code"] if b["win"] else r["code"]} | {b["total_gold"]:,} | {r["total_gold"]:,} | {b["gold_difference_15"] if b["gold_difference_15"] is not None else "缺失"} | [选手与统计]({file}) |')
        ll=[f'# {b["code"]} 对 {r["code"]}：第 {g["game"]} 局','',f'来源日期：{g["source_date"]}；官方系列赛开赛时间：{g["official_series_start_utc"]}；版本：{g["patch"]}。','', '| 方位 | 战队 | 位置 | 选手 | 英雄标识 | 击杀 | 死亡 | 助攻 | 经济 | 15分钟经济差 |','|---|---|---|---|---|---:|---:|---:|---:|---:|']
        for side,label in [('blue','蓝方'),('red','红方')]:
            t=g['teams'][side]
            for p in t['players']:
                st=p['stats'];ll.append(f'| {label} | {t["code"]} | {p["role"]} | {p["name"]} | {p["champion_asset"]} | {st.get("Kills","")} | {st.get("Deaths","")} | {st.get("Assists","")} | {st.get("Golds","")} | {st.get("GD@15","")} |')
        ll+=['',f'[GOL 小局页面]({g["sources"][0]}) · [完整统计]({g["sources"][1]}) · [官方赛程](https://lolesports.com/en-US/schedule)',''];(REP/file).write_text('\n'.join(ll))
    lines+=['','数据作为独立补充保存，本轮没有改变已有历史回测或今日冠军预测。尚未补齐全部历史转会与选手改名，不能只凭这批数据就宣布阵容继承模型已覆盖全年。',''];(REP/'README.md').write_text('\n'.join(lines))
    print('Verified',len(matched),'series,',len(games),'maps',flush=True)

if __name__=='__main__':main()

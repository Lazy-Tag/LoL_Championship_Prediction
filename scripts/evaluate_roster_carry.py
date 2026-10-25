"""Cross-season roster retention and fine AR half-life grid.

Current-season priors are reconditioned only on opening lineups already known
before each event, then that season's prior results are replayed. Event-start
roster eligibility is frozen within that event. No outcomes are duplicated.
"""
import json,hashlib
from collections import defaultdict
from datetime import date,timedelta
from pathlib import Path
import numpy as np
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions,key
from evaluate_detail_features import reconcile
from roster_carry_model import RosterBT,make_rosters,initialize
from model import series_probability,WORLD_TEAMS
R=Path(__file__).resolve().parents[1];OUT=R/'results/roster_carry_experiment';REP=R/'reports/roster_carry'
HALVES=(60,75,90,105,120)
CONFIGS=[dict(name=f'reset{h}',half=h,carry=False,gamma=1) for h in HALVES]+[dict(name=f'carry{h}',half=h,carry=True,gamma=1) for h in HALVES]+[dict(name='carry90_squared',half=90,carry=True,gamma=2)]

def metrics(rows,name):
    p=np.clip(np.array([r['probabilities'][name] for r in rows]),1e-12,1-1e-12);y=np.array([r['y'] for r in rows]);
    return dict(n=len(rows),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))

def select(rows,names):
    groups=defaultdict(list)
    for r in rows:groups[r['event_id']].append(r)
    if len(groups)<4:return 'reset90'
    names=['reset90']+[n for n in names if n!='reset90']
    values=np.array([[metrics(rr,n)['logloss'] for n in names] for rr in groups.values()]);best=int(np.argmin(values.mean(axis=0)))
    # Simpler baseline, then smaller |half-90|, then unsquared retention.
    order=sorted(range(len(names)),key=lambda i:(names[i]!='reset90',names[i].startswith('carry'),abs(next(c['half'] for c in CONFIGS if c['name']==names[i])-90),names[i].endswith('squared')))
    for i in order:
        d=values[:,i]-values[:,best]
        if d.mean()<=d.std(ddof=1)/np.sqrt(len(d))+1e-12:return names[i]
    return names[best]

def interval(rows,name):
    vals=[]
    for s in sorted({r['season'] for r in rows}):
        rr=[r for r in rows if r['season']==s];a=metrics(rr,name);b=metrics(rr,'reset90')
        vals.append([(a['logloss']-b['logloss'])*len(rr),(a['brier']-b['brier'])*len(rr),len(rr)])
    v=np.array(vals);ix=np.random.default_rng(2026).integers(0,len(v),(10000,len(v)));z=v[ix].sum(axis=1)
    return dict(logloss=list(map(float,np.quantile(z[:,0]/z[:,2],[.025,.975]))),brier=list(map(float,np.quantile(z[:,1]/z[:,2],[.025,.975]))))

def main():
    OUT.mkdir(exist_ok=True);REP.mkdir(exist_ok=True)
    hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'results/main_model.json',R/'results/live_s16/latest.json']}
    old=json.loads((R/'results/model_experiments/predictions.json').read_text());seasons={};regions={};rosters={};coverage=[];priors={}
    for s in range(3,16):
        rows,_=load_season(s);seasons[s]=rows;regions[s]=affiliations(rows,s)
        if s>3:
            for t,v in regions[s-1].items():regions[s].setdefault(t,v)
        matched,audit=reconcile(s,rows);rosters[s]=make_rosters(rows,matched)
        coverage.append(dict(season=s,teams=len(rosters[s]),lineup_teams=sum(bool(t['first']) for t in rosters[s].values()),matched_maps=audit['counts']['matched_maps']))
        priors[s]=prior_regions(seasons[s-1],regions[s-1],90)[0] if s>3 else {}
    display={s:{r[k]:r.get('display'+k[-1],r[k]) for r in rows for k in ('team1','team2')} for s,rows in seasons.items()}
    pred=[dict(season=r['season'],event_id=f'{r["season"]+2010}_{r["event"]}',event=r['event'],date=r['date'],detail=r['detail'],team1=r['display1'],team2=r['display2'],key1=r['team1'],key2=r['team2'],wins1=r['wins1'],wins2=r['wins2'],best_of=r['best_of'],y=int(r['wins1']>r['wins2']),probabilities={}) for r in old]
    byid={r['detail']:r for r in pred};all_audit=[];chains=[]
    for cfg in CONFIGS:
        previous=None;lineage={}
        for s in range(3,16):
            rows=seasons[s];teams=sorted(rosters[s]);daily=defaultdict(list)
            for r in rows:daily[r['date']].append(r)
            days=sorted(daily);start=date.fromisoformat(days[0]);end=date.fromisoformat(days[-1]);events=defaultdict(list)
            for r in old:
                if r['season']==s:events[r['event']].append(r)
            def fresh(cutoff):
                if cfg['carry']:return initialize(teams,regions[s],priors[s],cfg['half'],previous,rosters.get(s-1,{}),rosters[s],start,cutoff,cfg['gamma'])
                return RosterBT(teams,regions[s],priors[s],cfg['half']),[]
            for event,rr in events.items():
                event_start=min(r['date'] for r in rr);event_end=max(r['date'] for r in rr)
                model,audit=fresh(date.fromisoformat(event_start));td=defaultdict(list)
                for r in rr:td[r['date']].append(r)
                participants={r[k] for r in rr for k in ('team1','team2')}
                for a in audit:
                    if a['team'] in participants:all_audit.append(dict(season=s,event=event,config=cfg['name'],team_display=display[s][a['team']],**a))
                for ds in sorted(set(daily)|set(td)):
                    if ds>event_end:break
                    model.advance(date.fromisoformat(ds));theta=model.strengths()
                    for r in td[ds]:
                        p=float(expit(theta[r['team1']]-theta[r['team2']]))
                        if cfg['name']=='reset90':assert abs(p-r['dynamic90'])<1e-9
                        byid[r['detail']]['probabilities'][cfg['name']]=float(series_probability(p,r['best_of']))
                    model.update(daily[ds])
            # At season end all used metadata precedes the next season. Rebuild
            # from this season's prior and each actual result exactly once.
            model,audit=fresh(end+timedelta(days=1))
            for ds in days:model.advance(date.fromisoformat(ds));model.update(daily[ds])
            if cfg['carry']:
                next_lineage={}
                for a in audit:
                    if a['coefficient']>0:
                        t=a['team'];oldchain=lineage.get(t,{})
                        chain=dict(config=cfg['name'],season=s,team=t,team_display=display[s][t],retention=a['retention'],boundary_coefficient=a['coefficient'],consecutive_roster_product=oldchain.get('consecutive_roster_product',1)*a['retention']**cfg['gamma'],ancestor_season=oldchain.get('ancestor_season',s-1),ancestor_date=oldchain.get('ancestor_date',previous.day.isoformat()))
                        chain['transport_product_to_season_start']=chain['consecutive_roster_product']*2**(-(start-date.fromisoformat(chain['ancestor_date'])).days/cfg['half'])
                        next_lineage[t]=chain;chains.append(chain)
                lineage=next_lineage
            previous=model
        if cfg['name']=='carry90':carry90_final=previous
        print(cfg['name'],'complete',flush=True)
    names=[c['name'] for c in CONFIGS];selection=[]
    for s in range(4,16):
        earlier=[r for r in pred if r['season']<s];chosen=select(earlier,names)
        selection.append(dict(season=s,chosen=chosen,prior_events=len({r['event_id'] for r in earlier})))
        for r in pred:
            if r['season']==s:r['selected_model']=chosen;r['probabilities']['selected']=r['probabilities'][chosen]
    eligible={(a['season'],a['event'],a['team']) for a in all_audit if a['config']=='carry90' and a['coefficient']>0}
    for r in pred:r['roster_supported']=any((r['season'],r['event'],r[k]) in eligible for k in ('key1','key2'))
    common=[r for r in pred if r['roster_supported']]
    raw=json.loads((R/'data/series.json').read_text())
    current=[{**r,'team1':key(r['team1']),'team2':key(r['team2']),'detail':'series:'+r['id'],'tournament':r.get('tournament',r['event'])} for r in raw]
    mm,aa=reconcile(16,current);r16=make_rosters(current,mm);reg16={}
    mapping={'LPL':'CN','LCK':'KR','LEC':'EU','LCP':'LCP','LCS':'NA','CBLOL':'BR'}
    for r in current:
        if r['event'] in mapping:
            for k in ('team1','team2'):reg16[r[k]]=mapping[r['event']]
    for t,(name,league,_) in WORLD_TEAMS.items():reg16[key(name)]=mapping[league]
    start16=date.fromisoformat(min(r['date'] for r in current));cut16=date(2026,10,25)
    _,a16=initialize(sorted(r16),reg16,{},90,carry90_final,rosters[15],r16,start16,cut16)
    lookup={key(v[0]):c for c,v in WORLD_TEAMS.items()};a16=[dict(code=lookup[a['team']],**a) for a in a16 if a['team'] in lookup]
    summary=dict(configs=CONFIGS,coverage=coverage,aggregate={n:metrics(pred,n) for n in names+['selected']},roster_supported={n:metrics(common,n) for n in names+['selected']},selection=selection,s16_candidate=select(pred,names),year_cluster_intervals={n:interval(pred,n) for n in ['carry90','selected']},by_season=[dict(season=s,metrics={n:metrics([r for r in pred if r['season']==s],n) for n in names+['selected']}) for s in range(4,16)],unchanged_hashes=hashes,s16_opening_rosters=a16,s16_matched_maps=aa['counts']['matched_maps'])
    for name,obj in [('predictions',pred),('summary',summary),('roster_audit',all_audit),('discount_chains',chains)]:
        (OUT/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    for name,h in hashes.items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h
    report(summary,pred,all_audit,chains)
    print(json.dumps(summary['aggregate'],indent=2),flush=True)

def report(d,pred,audit,chains):
    labels={c['name']:('阵容继承' if c['carry'] else '每季重置')+str(c['half'])+'天'+('（留存平方）' if c['gamma']==2 else '') for c in CONFIGS}
    labels['selected']='按更早年份选择'
    lines=['# 跨赛季阵容继承与时间衰减','','检验上一季战队实力能否按人员留存程度继承，并比较更细的时间衰减。现有正式预测保持不变。','','## 全部 1,300 场历史系列赛','','| 方案 | 半衰期 | 命中率 | 对数损失 ↓ | Brier ↓ |','|---|---:|---:|---:|---:|']
    for c in d['configs']:
        m=d['aggregate'][c['name']];label='阵容折扣继承' if c['carry'] else '每季重置'
        if c['gamma']==2:label+='（留存率平方）'
        lines.append(f'| {label} | {c["half"]} 天 | {m["accuracy"]:.2%} | {m["logloss"]:.5f} | {m["brier"]:.5f} |')
    m=d['aggregate']['selected'];lines.append(f'| 仅用更早年份选择 | 随年选择 | {m["accuracy"]:.2%} | {m["logloss"]:.5f} | {m["brier"]:.5f} |')
    lines+=['','## 有阵容继承依据的共同子集','',f'双方至少一队可继承的系列赛共 {d["roster_supported"]["carry90"]["n"]} 场。缺失数据没有按“阵容不变”处理。','', '| 方案 | 命中率 | 对数损失 | Brier |','|---|---:|---:|---:|']
    for n in ['reset90','carry90','carry90_squared','selected']:
        m=d['roster_supported'][n];lines.append(f'| {labels[n]} | {m["accuracy"]:.2%} | {m["logloss"]:.5f} | {m["brier"]:.5f} |')
    lines+=['','## 逐年事前选择','','| 预测赛季 | 可用较早赛事数 | 选择方案 |','|---|---:|---|']
    for s in d['selection']:lines.append(f'| S{s["season"]} | {s["prior_events"]} | {labels[s["chosen"]]} |')
    lines+=['',f'全部 S4–S15 历史选择出的 S16 候选为 **{labels[d["s16_candidate"]]}**。这不是独立的 S16 效果验证，也未自动替换 S16 主报告。','', '## 不确定性','','按年份聚类计算；跨季状态仍会造成年份之间相关，因此这些区间仅供描述性参考。','']
    for n,ci in d['year_cluster_intervals'].items():lines.append(f'- {labels[n]} 相对原90天方案 的对数损失差：95% 年份聚类区间 [{ci["logloss"][0]:.5f}, {ci["logloss"][1]:.5f}]；Brier 差 [{ci["brier"][0]:.5f}, {ci["brier"][1]:.5f}]。负值较好。')
    lines+=['','## 阵容数据覆盖','','| 赛季 | 训练队伍数 | 有已对账完整阵容的队伍 | 对账小局 |','|---|---:|---:|---:|']
    for c in d['coverage']:lines.append(f'| S{c["season"]} | {c["teams"]} | {c["lineup_teams"]} | {c["matched_maps"]} |')
    lines+=['','## 解读范围','','这里首次在独立候选中允许跨年战队实力输入；原模型依然每年重置。继承的是战队相对赛区的实力偏移，赛区先验仍按原 90 天方案从上一季国际赛估计。半衰期网格只改变战队偏移记忆，不改变赛区先验和随机游走尺度。','','阵容仅来自与原比分严格对账的小局。上季取末次已知完整阵容，新季取首次已知完整阵容；替补按实际出场份额分配。上季阵容距离该队末场超过 45 天、新季首阵容距该队首场超过 30 天，或预测前尚未知晓，则不继承。只支持相同规范队名且原赛区一致的队伍；未核准的更名、收购和选手改名均可能造成低估。','','用赛前已知的新季开季阵容重新条件化新季先验，再重放新季截至预测日之前的全部比赛；没有把较晚阵容用于预测更早比赛。阵容资格在每届赛事开赛时冻结，本轮未完整建模季中换人或人员位置效应。','','S3–S5 缺可用于本模型的精确日期阵容；原始结果仍可形成赛区先验，但不能声称已按人员修正所有历史赛季。本轮 S16 开季诊断使用的既有详细镜像截止六月，不能视为世界赛当前阵容核验。本轮只评价逐场胜率，未重跑冠军与最终名次模拟。','','[每队人员留存及折扣](rosters.md) · [跨季折扣链](chains.md) · [S16 开季诊断](s16_opening.md) · [逐场预测](matches.md) · [完整方法](../../MODEL.md#跨赛季阵容继承实验)','']
    REP.mkdir(exist_ok=True);(REP/'README.md').write_text('\n'.join(lines))
    lines=['# 每队跨赛季阵容折扣','','90 天、留存率一次方候选；仅显示各届国际赛参赛队。人员名单表示实际已知出场阵容，未确认的选手改名不自动合并。','','| 赛事 | 队伍 | 上季已知阵容 | 新季已知开季阵容 | 人员留存 | 含休赛期折扣 | 到本届开赛的传播系数 | 状态 |','|---|---|---|---|---:|---:|---:|---|']
    reasons={'no_previous_team':'无同名上季队伍','missing_lineup':'缺完整阵容','lineup_not_known_before_cutoff':'开赛前未知阵容','previous_lineup_stale':'上季阵容过旧','opening_lineup_missing':'缺开季阵容','inherited':'继承','no_shared_handles':'无同名留存选手','region_changed_or_unknown':'原赛区改变或未知'}
    for a in audit:
        if a['config']!='carry90':continue
        def players(label):
            p=a.get(label)
            return '缺失' if not p else p['date']+'：'+', '.join(f'{n} ({v*100:.0f}%)' for n,v in p['shares'].items())
        lines.append(f'| {a["season"]+2010} {a["event"]} | {a.get("team_display",a["team"])} | {players("previous_lineup")} | {players("current_lineup")} | {a["retention"]:.2%} | {a["coefficient"]:.2%} | {a.get("coefficient_at_cutoff",0):.2%} | {reasons[a["reason"]]} |')
    (REP/'rosters.md').write_text('\n'.join(lines)+'\n')
    lines=['# 跨赛季折扣链','','仅显示 90 天候选中连续可核准的继承链。系数是原先验偏移在跨季转移与时间演化中的传播系数，后续胜负会重新估计实力，不能把此列当作旧赛果最终的精确有效权重。','','| 到达赛季 | 队伍 | 最早连续来源赛季 | 本次人员留存 | 连乘人员折扣 | 含总时间衰减的传播系数 |','|---|---|---|---:|---:|---:|']
    for a in chains:
        if a['config']=='carry90':lines.append(f'| S{a["season"]} | {a.get("team_display",a["team"])} | S{a["ancestor_season"]} | {a["retention"]:.2%} | {a["consecutive_roster_product"]:.2%} | {a["transport_product_to_season_start"]:.4%} |')
    (REP/'chains.md').write_text('\n'.join(lines)+'\n')
    lines=['# S16 开季阵容继承诊断','','此表仅检验上季末到 S16 开季的人员连续性，**不是 S16 世界赛当前阵容核验**。[另行补采的十月实际出场阵容](../detailed_data/worlds_2026/rosters.md)已单独提供。用于本次开季实验的既有镜像截至六月，未追加其胜负记录；同名队伍和原赛区均吻合才计算继承。候选为 90 天半衰期，正式 S16 概率没有改变。','','| 战队 | 上季阵容日期 | 本季开季阵容日期 | 人员留存 | 含休赛期折扣 | 状态 |','|---|---|---|---:|---:|---|']
    for a in d['s16_opening_rosters']:
        lines.append(f'| {a["code"]} | {a.get("previous_lineup",{}).get("date","缺失")} | {a.get("current_lineup",{}).get("date","缺失")} | {a["retention"]:.2%} | {a["coefficient"]:.2%} | {reasons[a["reason"]]} |')
    (REP/'s16_opening.md').write_text('\n'.join(lines)+'\n')
    lines=['# 跨赛季模型逐场对照','','两列均为左队系列赛获胜概率。预测只使用较早日期赛果；继承资格在本届开赛时确定。','','| 日期 | 赛事 | 对阵 | 实际比分 | 原 90 天 | 阵容继承 90 天 | 事前选择 | 所选方案 |','|---|---|---|---|---:|---:|---:|---|']
    for r in pred:lines.append(f'| {r["date"]} | {r["event_id"]} | {r["team1"]} – {r["team2"]} | {r["wins1"]}:{r["wins2"]} | {r["probabilities"]["reset90"]:.2%} | {r["probabilities"]["carry90"]:.2%} | {r["probabilities"]["selected"]:.2%} | {labels[r["selected_model"]]} |')
    (REP/'matches.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()

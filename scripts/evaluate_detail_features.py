"""Pre-day, season-reset evaluation of economy/side augmentation; no new outcomes.
Coefficients fit only prior domestic maps from the same season. Fixed 90-day
weights, unit Gaussian coefficient priors, 5-map economy shrinkage; no tuning.
"""
import json
from collections import defaultdict,Counter
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.optimize import minimize
from backtest import load_season,affiliations,prior_regions,key,metrics,international,domestic_region
from candidate_models import DynamicBT
R=Path(__file__).resolve().parents[1];OUT=R/'results/detail_experiment';REP=R/'reports/detailed_data'
FIELDS=['dynamic90','economy90','side_economy90']

def reconcile(s,rows):
    known={r[k] for r in rows for k in ['team1','team2']};aliases={t:t for t in known}
    ap=R/f'data/enrichment/S{s}_audit.json'
    if ap.exists():
        aliases.update({k:v for k,v in json.loads(ap.read_text()).get('aliases',{}).items() if v in known})
    groups=defaultdict(list);stats=Counter();rejected=[]
    for line in (R/f'data/detailed/S{s}_games.jsonl').read_text().splitlines():
        g=json.loads(line)
        if not g['top_tier_candidate']:continue
        stats['candidate_maps']+=1
        a=aliases.get(key(g['teams']['blue']['name'] or ''));b=aliases.get(key(g['teams']['red']['name'] or ''))
        if not a or not b or not g['date']:
            stats['unknown_name_or_date_maps']+=1;continue
        g['a']=a;g['b']=b
        groups[(g['date'][:10],g['league'],*sorted([a,b]))].append(g)
    lookup=defaultdict(list)
    for r in rows:lookup[(r['date'],*sorted([r['team1'],r['team2']]))].append(r)
    proposed=defaultdict(list)
    for (day,league,a,b),gg in groups.items():
        wins=sum(g['teams']['blue']['win'] if g['a']==a else g['teams']['red']['win'] for g in gg)
        candidates=[r for r in lookup[(day,a,b)] if (r['wins1'] if r['team1']==a else r['wins2'])==wins and r['wins1']+r['wins2']==len(gg)]
        if len(candidates)==1:proposed[candidates[0]['detail']].append(gg)
        else:
            stats['unmatched_or_ambiguous_maps']+=len(gg)
            rejected.append(dict(date=day,league=league,teams=[a,b],maps=len(gg),reason='exact date, team pair and complete series score did not uniquely match'))
    matched={}
    for ident,groups in proposed.items():
        if len(groups)==1:matched[ident]=groups[0]
        else:stats['multiple_source_groups_maps']+=sum(map(len,groups))
    stats['matched_series']=len(matched);stats['matched_maps']=sum(map(len,matched.values()))
    assert sum(stats[k] for k in ['unknown_name_or_date_maps','unmatched_or_ambiguous_maps','multiple_source_groups_maps','matched_maps'])==stats['candidate_maps']
    return matched,dict(season=s,counts=dict(stats),unmatched=rejected)

def fit(records,day,side):
    if not records:return np.zeros(2)
    X=np.array([[r[2],1. if side else 0.] for r in records]);off=np.array([r[1] for r in records]);y=np.array([r[3] for r in records]);w=np.exp2(-np.array([(day-r[0]).days for r in records])/90.)
    assert all(r[0]<day for r in records)
    def obj(b):
        z=off+X@b
        return np.sum(w*(np.logaddexp(0,z)-y*z))+.5*b@b, X.T@(w*(expit(z)-y))+b
    opt=minimize(obj,np.zeros(2),jac=True,method='BFGS',options={'gtol':1e-6})
    assert max(abs(obj(opt.x)[1]))<1e-4
    return opt.x

def main():
    OUT.mkdir(exist_ok=True);seasons={};regions={};pred=[];audits=[];coeff=[]
    old=json.loads((R/'results/model_experiments/predictions.json').read_text())
    for s in range(3,16):
        seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
        if s>3:
            for t,v in regions[s-1].items():regions[s].setdefault(t,v)
    for s in range(4,16):
        rows=seasons[s];matched,audit=reconcile(s,rows);audits.append(audit)
        targets=defaultdict(list);byday=defaultdict(list)
        for r in old:
            if r['season']==s:targets[r['date']].append(r)
        for r in rows:byday[r['date']].append(r)
        teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regions[s-1],90)
        dyn=DynamicBT(teams,regions[s],prior);econ=defaultdict(lambda:np.zeros(2));last=None;records=[];seen=Counter()
        for ds in sorted(set(byday)|set(targets)):
            day=date.fromisoformat(ds);dyn.advance(day);theta=dyn.strengths()
            if last is not None:
                decay=2**(-(day-last).days/90.)
                for value in econ.values():value*=decay
            last=day
            def feature(a,b):return econ[a][0]/(5+econ[a][1])-econ[b][0]/(5+econ[b][1])
            if ds in targets:
                betas=[fit(records,day,side) for side in [False,True]]
                coeff.append(dict(season=s,date=ds,economy=betas[0].tolist(),side_economy=betas[1].tolist(),training_maps=len(records)))
                for r in targets[ds]:
                    a,b=r['team1'],r['team2'];d=theta[a]-theta[b];x=feature(a,b);baseline=float(expit(d))
                    assert abs(baseline-r['dynamic90'])<1e-9
                    q={**r,'economy90':float(expit(d+betas[0][0]*x)),'side_economy90':float((expit(d+betas[1][0]*x+betas[1][1])+expit(d+betas[1][0]*x-betas[1][1]))/2),'economy_difference':float(x),'past_economy_maps1':seen[a],'past_economy_maps2':seen[b],'detailed_history_both':seen[a]>=5 and seen[b]>=5}
                    pred.append(q)
            updates=[]
            for r in byday[ds]:
                for g in matched.get(r['detail'],[]):
                    a,b=g['a'],g['b'];blue=g['teams']['blue'];red=g['teams']['red'];ga=blue['stats']['goldat15'];gb=red['stats']['goldat15']
                    # Store features before ANY same-day economy updates.
                    if domestic_region(r['tournament']) is not None:records.append((day,theta[a]-theta[b],feature(a,b),blue['win']))
                    if ga is not None and gb is not None:
                        diff=float(np.clip((ga-gb)/1000.,-10,10));updates.append((a,b,diff))
            dyn.update(byday[ds])
            for a,b,value in updates:
                econ[a]+=np.array([value,1]);econ[b]+=np.array([-value,1]);seen[a]+=1;seen[b]+=1
        print(f'S{s}: matched {audit["counts"]["matched_maps"]} maps; evaluated {sum(len(v) for v in targets.values())} series',flush=True)
    subsets={'all':pred,'both_teams_5_prior_economy_maps':[r for r in pred if r['detailed_history_both']]}
    summary={name:{f:metrics(rr,f) for f in FIELDS} for name,rr in subsets.items()}
    summary['by_season']=[dict(season=s,models={f:metrics([r for r in pred if r['season']==s],f) for f in FIELDS}) for s in range(4,16)]
    # Paired event-cluster bootstrap: descriptive uncertainty, not model selection.
    from model import series_probability
    keys=sorted({(r['season'],r['event']) for r in pred});rng=np.random.default_rng(2026);boot=rng.integers(0,len(keys),size=(10000,len(keys)));intervals={}
    for f in FIELDS[1:]:
        vals=[]
        for k in keys:
            rr=[r for r in pred if (r['season'],r['event'])==k];d=[]
            for r in rr:
                win=float(r['wins1']>r['wins2']);pp=[np.clip(series_probability(r[n],r['best_of']),1e-12,1-1e-12) for n in ['dynamic90',f]]
                ll=[-win*np.log(p)-(1-win)*np.log1p(-p) for p in pp];d.append(ll[1]-ll[0])
            vals.append([sum(d),len(d)])
        vals=np.array(vals);draw=vals[boot].sum(axis=1);intervals[f]=np.quantile(draw[:,0]/draw[:,1],[.025,.975]).tolist()
    summary['paired_event_bootstrap_series_logloss_delta_95']=intervals
    for name,value in [('predictions',pred),('summary',summary),('reconciliation',audits),('coefficients',coeff)]:
        (OUT/f'{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    report(summary,audits)
    print(json.dumps(summary['all'],ensure_ascii=False),flush=True)

def report(summary,audits):
    labels={'dynamic90':'现有动态模型','economy90':'动态模型＋历史15分钟经济','side_economy90':'动态模型＋历史经济＋红蓝方'}
    text='# 详细数据是否改善预测？\n\n[数据总览](README.md)\n\n固定候选的首次回测，尚未替换主结果。评价 S4–S15 的 MSI／MSC／Worlds，预测均发生于比赛日前；不使用目标比赛的实际选边或赛后经济。\n\n'
    for subset,title in [('all','全部 1,300 场系列赛'),('both_teams_5_prior_economy_maps','双方各至少有 5 局历史经济记录的共同子集')]:
        text+=f'## {title}\n\n| 模型 | 系列赛数 | 系列赛命中率 | 系列赛对数损失 ↓ | 系列赛 Brier ↓ | 小局对数损失 ↓ |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
        for f in FIELDS:
            m=summary[subset][f];text+=f'| {labels[f]} | {m["covered_series"]} | {m["series_accuracy"]:.2%} | {m["series_logloss"]:.5f} | {m["series_brier"]:.5f} | {m["map_logloss"]:.5f} |\n'
        text+='\n'
    text+='## 各赛季系列赛命中率\n\n| 赛季 | 现有动态 | 加经济 | 加经济及红蓝方 |\n| --- | ---: | ---: | ---: |\n'
    for row in summary['by_season']:text+=f'| S{row["season"]} | '+' | '.join(f'{row["models"][f]["series_accuracy"]:.2%}' for f in FIELDS)+' |\n'
    text+='\n## 提升的稳定性\n\n按 23 个赛事整体抽样的配对 bootstrap（10,000 次，种子 2026）。下列为新增模型减原模型的系列赛对数损失差的 95% 区间；负值较好，跨过零不能确认稳定提升。赛事之间仍可能相关，区间仅作描述性参考。\n\n'
    for f,ci in summary['paired_event_bootstrap_series_logloss_delta_95'].items():text+=f'- {labels[f]}：[{ci[0]:.5f}, {ci[1]:.5f}]。\n'
    text+='\n## 数据对账\n\n只接纳同日、同队伍、整场小局比分一致且唯一匹配的记录；没有新增胜负样本。未知别名、跨日差异或比分不符均暂不使用。S4–S5 缺日期的逐分钟档案不参与本轮，避免凭空指定比赛日期。\n\n| 赛季 | 候选小局 | 对账系列赛 | 对账小局 |\n| --- | ---: | ---: | ---: |\n'
    for a in audits:
        c=a['counts'];text+=f'| S{a["season"]} | {c.get("candidate_maps",0):,} | {c["matched_series"]:,} | {c["matched_maps"]:,} |\n'
    text+='\n## 解释范围\n\n这一步检验逐场概率，不检验最终排名和夺冠概率；尚未重跑整届赛事。新特征在同赛季国内比赛上逐日前推拟合，不能把这次观察用于调参后仍称独立验证。详细数据缺失具有联赛偏差，覆盖子集不代表所有赛事。\n\n[模型细节](DETAIL_MODEL.md) · [数据异常](anomalies.md)\n'
    (REP/'model_comparison.md').write_text(text)
    (REP/'DETAIL_MODEL.md').write_text('''# 历史经济与红蓝方增强：方法\n\n[比较结果](model_comparison.md)\n\n以原 dynamic90 当日赛前实力差作为固定 logit offset，增加历史经济差的回归项；第二个候选额外估计蓝方截距。胜负训练与基线完全相同，详细数据只在完整系列赛对账成功后附加，禁止双重计数。\n\n每队特征为此前小局的15分钟经济差（千金币，单局截断在±10）按90天半衰期加权的和，除以衰减样本量加5；缺失不当作零经济观测。两队特征相减。新赛季经济状态和回归系数重置；唯一跨年输入仍为旧模型的上一季国际赛赛区先验。\n\n两个回归系数使用标准正态先验，仅以当前赛季此前国内小局的赛前特征和结果拟合，并使用90天时间权重。不拟合额外的实力缩放项，不按国际赛效果搜索参数。所有当日比赛先预测，再批量更新实力和经济状态。赛后经济仅在后续日期可用。\n\n预测系列赛时选边未知，按蓝／红各50%边际化单局概率，再沿用原独立同分布 BO1／3／5 转换。这是假设，不是官方选边规则复现；不使用实际未来选边、阵容、版本或局序。全局 BP、赛季换人和参数不确定性本轮仍未建模。\n\n这是一项低维增量检验，不能代表所有使用经济数据的模型都无效或有效。原始经济优势受对手强弱和赛区风格影响，本轮未建立对手校正的多任务经济状态模型。经济缺失的队伍特征收缩为零；须结合共同覆盖子集判断结果。\n''')
if __name__=='__main__':main()

"""Season-isolated event-local likelihood powers, nested past-year selection.

Fixed grid 1/1.25/1.5/2/3/4. Select smallest weight within one paired event SE
of the best mean event log loss on strictly earlier seasons (minimum 4 events).
No S16 outcomes select the power. Primary outcome: series log loss after at
least one earlier event day. No same-day updates. Year-cluster paired bootstrap.
"""
import copy,json,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions,target_event
from candidate_models import DynamicBT
from event_weighting import WEIGHTS,weighted_rows
from model import series_probability
R=Path(__file__).resolve().parents[1];OUT=R/'results/event_weight_experiment';REP=R/'reports/event_weight'

def loss(p,y):
    p=np.clip(p,1e-12,1-1e-12)
    return -y*np.log(p)-(1-y)*np.log1p(-p)

def metrics(rows,name):
    p=np.array([r['probabilities'][name] for r in rows]);y=np.array([r['y'] for r in rows])
    return dict(n=len(rows),logloss=float(np.mean(loss(p,y))),brier=float(np.mean((p-y)**2)),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))))

def select(rows):
    groups=defaultdict(list)
    for r in rows:
        if r['prior_event_series']:groups[r['event_id']].append(r)
    if len(groups)<4:return 1.,dict(events=len(groups),reason='fewer_than_four_events')
    keys=[str(w) for w in WEIGHTS]
    values=np.array([[metrics(rr,k)['logloss'] for k in keys] for rr in groups.values()])
    mean=values.mean(axis=0);best=int(np.argmin(mean));chosen=best
    for k in range(len(keys)):
        differences=values[:,k]-values[:,best]
        se=float(np.std(differences,ddof=1)/np.sqrt(len(groups)))
        if float(differences.mean())<=se+1e-12:chosen=k;break
    return WEIGHTS[chosen],dict(events=len(groups),best_weight=WEIGHTS[best],mean_event_logloss=dict(zip(keys,map(float,mean))),selected=WEIGHTS[chosen])

def bootstrap(rows,name):
    # Cluster by year: MSI/MSC and Worlds of a season share training and priors.
    groups=defaultdict(list)
    for r in rows:groups[r['season']].append(r)
    values=[]
    for rr in groups.values():
        p=np.array([r['probabilities'][name] for r in rr]);b=np.array([r['probabilities']['1.0'] for r in rr]);y=np.array([r['y'] for r in rr])
        values.append([float((loss(p,y)-loss(b,y)).sum()),float(((p-y)**2-(b-y)**2).sum()),len(rr)])
    v=np.array(values);rng=np.random.default_rng(2026);ix=rng.integers(0,len(v),(10000,len(v)));s=v[ix].sum(axis=1)
    return dict(years=len(v),logloss_delta_ci=list(map(float,np.quantile(s[:,0]/s[:,2],[.025,.975]))),brier_delta_ci=list(map(float,np.quantile(s[:,1]/s[:,2],[.025,.975]))))

def main():
    OUT.mkdir(exist_ok=True);REP.mkdir(exist_ok=True)
    pointer_hash=hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
    old=json.loads((R/'results/model_experiments/predictions.json').read_text());seasons={};regions={};pred=[];audits=[]
    for s in range(3,16):
        seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
        if s>3:
            for t,v in regions[s-1].items():regions[s].setdefault(t,v)
    for s in range(4,16):
        rows=seasons[s];teams=sorted({r[k] for r in rows for k in ('team1','team2')});prior,_=prior_regions(seasons[s-1],regions[s-1],90)
        chosen,audit=select([r for r in pred if r['season']<s]);audits.append(dict(season=s,training_max_season=s-1,weight=chosen,selection=audit))
        base=DynamicBT(teams,regions[s],prior);daily=defaultdict(list);targets=defaultdict(list)
        for r in rows:daily[r['date']].append(r)
        for r in old:
            if r['season']==s:targets[r['date']].append(r)
        active={};nseen=defaultdict(int);lastseen={}
        for ds in sorted(set(daily)|set(targets)):
            day=date.fromisoformat(ds);base.advance(day)
            for event in {r['event'] for r in targets[ds]}:
                if event not in active:active[event]={w:copy.deepcopy(base) for w in WEIGHTS}
            for models in active.values():
                for model in models.values():model.advance(day)
            for r in targets[ds]:
                event=r['event'];probs={};maps={}
                for w,model in active[event].items():
                    th=model.strengths();p=float(expit(th[r['team1']]-th[r['team2']]))
                    if w==1.:assert abs(p-r['dynamic90'])<1e-9
                    if not nseen[event]:assert abs(p-r['dynamic90'])<1e-9
                    maps[str(w)]=p;probs[str(w)]=float(series_probability(p,r['best_of']))
                probs['selected']=probs[str(chosen)]
                pred.append(dict(season=s,event=event,event_id=f'{s+2010}_{event}',date=ds,detail=r['detail'],team1=r['display1'],team2=r['display2'],wins1=r['wins1'],wins2=r['wins2'],best_of=r['best_of'],y=int(r['wins1']>r['wins2']),prior_event_series=nseen[event],latest_event_training_date=lastseen.get(event),selected_weight=chosen,probabilities=probs,map_probabilities=maps))
            base.update(daily[ds])
            for event,models in active.items():
                for w,model in models.items():model.update(weighted_rows(daily[ds],event,w))
            for r in daily[ds]:
                event=target_event(r['tournament'])
                if event:nseen[event]+=1;lastseen[event]=ds
        print('S'+str(s),'selected',chosen,'complete',flush=True)
    eligible=[r for r in pred if r['prior_event_series']>0];keys=[str(w) for w in WEIGHTS]+['selected']
    chosen,audit=select(pred)
    events=[]
    for event in sorted({r['event_id'] for r in pred}):
        rr=[r for r in eligible if r['event_id']==event]
        events.append(dict(event=event,weight=rr[0]['selected_weight'],metrics={k:metrics(rr,k) for k in keys}))
    summary=dict(grid=list(WEIGHTS),selection_rule='Earlier-seasons-only, minimum four completed events, smallest weight within one paired-event standard error of best event-macro logloss',all_series={k:metrics(pred,k) for k in keys},after_event_observation={k:metrics(eligible,k) for k in keys},selected_uncertainty=bootstrap(eligible,'selected'),selection_audit=audits,events=events,s16_weight=chosen,s16_selection=audit,main_pointer_sha256=pointer_hash)
    # A data-dependent policy needs out-of-time gains, not in-sample best-grid gains.
    b=summary['after_event_observation']['1.0'];v=summary['after_event_observation']['selected'];ci=summary['selected_uncertainty']
    summary['eligible_for_live_promotion']=bool(chosen>1 and v['logloss']<b['logloss'] and v['brier']<b['brier'] and ci['logloss_delta_ci'][1]<0)
    for name,obj in [('predictions',pred),('summary',summary)]:
        (OUT/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    assert hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()==pointer_hash
    report(summary)
    print(json.dumps({k:summary[k] for k in ('after_event_observation','s16_weight','selected_uncertainty','eligible_for_live_promotion')},indent=2),flush=True)

def report(d):
    table=['# 本届赛事加权：赛中预测检验','','只提高正在预测的这届赛事此前小局的影响，检验能否更快适应本届状态。首个比赛日没有本届历史，所有方案预测相同。','','## 结果','', '| 本届权重 | 系列赛命中率 | 对数损失 ↓ | Brier ↓ |','|---|---:|---:|---:|']
    for k,m in d['after_event_observation'].items():table.append(f'| {"逐年选择" if k=="selected" else k+" 倍"} | {m["accuracy"]*100:.2f}% | {m["logloss"]:.5f} | {m["brier"]:.5f} |')
    n=d['after_event_observation']['1.0']['n'];ci=d['selected_uncertainty'];selected=d['s16_weight']
    table+=['',f'上表比较已有更早比赛日本届赛果的 {n} 场系列赛；完整 {d["all_series"]["1.0"]["n"]} 场评价另含各届首日。固定倍数是敏感性对照，“逐年选择”才是按此前年份选权重后的外推表现。','',f'逐年选择相对原方案的对数损失差，按年份聚类的 95% bootstrap 区间为 [{ci["logloss_delta_ci"][0]:.5f}, {ci["logloss_delta_ci"][1]:.5f}]；Brier 差区间为 [{ci["brier_delta_ci"][0]:.5f}, {ci["brier_delta_ci"][1]:.5f}]。负值表示改善。仅有 12 个年份簇，区间应谨慎解读。若各年都选择 1 倍，差值区间为 [0,0] 仅表示两组预测完全相同，不代表已证明未来等效。','',f'用 S4–S15 全部历史选择的 S16 候选权重为 **{selected:g} 倍**。'+('历史外推达到预设推广条件。' if d['eligible_for_live_promotion'] else '尚未达到预设推广条件，当前赛中主结果保持原权重，不因某个固定倍数在同一批数据上较好就替换。'),'','## 每届对照','','| 赛事 | 事前选择权重 | 原命中率 | 新命中率 | 原对数损失 | 新对数损失 | 原 Brier | 新 Brier |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for e in d['events']:
        b=e['metrics']['1.0'];m=e['metrics']['selected'];table.append(f'| {e["event"]} | {e["weight"]:g} | {b["accuracy"]*100:.2f}% | {m["accuracy"]*100:.2f}% | {b["logloss"]:.5f} | {m["logloss"]:.5f} | {b["brier"]:.5f} | {m["brier"]:.5f} |')
    table+=['','## 范围与局限','','覆盖 S4–S15 的 23 届 MSI／MSC／Worlds，训练仍包含当季此前全部已纳入比赛。每季重置战队实力，仅上一季国际赛提供赛区先验。同日所有预测在该日赛果进入前完成；权重只由更早年份选择，不能使用待预测年份成绩。','','本届权重在赛事结束后丢弃，不带入另一届赛事。BO1／BO3／BO5 仍由小局胜率转换；没有再加入系列赛胜负，实际小局数和原比分不改变。','','这次验证的是赛事进行期间的下一场胜率，未重跑整届冠军及最终名次回放，不能据此宣称冠军预测提升。历史覆盖缺口、未知阵容、全局 BP 和选边影响仍存在。加权属于有意调整学习强度，不能解释为获得了额外独立比赛证据。','','[方法与选择规则](../../MODEL.md#本届赛事权重实验) · [逐场预测](matches.md)','']
    (REP/'README.md').write_text('\n'.join(table))
    rows=json.loads((OUT/'predictions.json').read_text());s=['# 本届赛事加权逐场预测','','双方胜率均为赛前整场概率；未使用同日赛果。','','| 日期 | 赛事 | 对阵 | 实际比分 | 本届此前场数 | 权重 | 原左方胜率 | 加权左方胜率 |','|---|---|---|---|---:|---:|---:|---:|']
    for r in rows:s.append(f'| {r["date"]} | {r["event_id"]} | {r["team1"]} – {r["team2"]} | {r["wins1"]}:{r["wins2"]} | {r["prior_event_series"]} | {r["selected_weight"]:g} | {r["probabilities"]["1.0"]*100:.2f}% | {r["probabilities"]["selected"]*100:.2f}% |')
    (REP/'matches.md').write_text('\n'.join(s)+'\n')

if __name__=='__main__':main()

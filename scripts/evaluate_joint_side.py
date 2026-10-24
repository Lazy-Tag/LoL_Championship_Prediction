"""Isolate joint side/state estimation on the unchanged 1,300-series replay."""
import json,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from backtest import load_season,affiliations,prior_regions,metrics
from model import series_probability
from dynamic_side_model import DynamicSideBT
from evaluate_detail_features import reconcile
R=Path(__file__).resolve().parents[1];OUT=R/'results/joint_side_experiment';REP=R/'reports/detailed_data'

def main():
 OUT.mkdir(exist_ok=True);old=json.loads((R/'results/model_experiments/predictions.json').read_text());seasons={};regs={};pred=[];audit=[];states=[]
 mainhash=hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 for s in range(3,16):
  seasons[s],_=load_season(s);regs[s]=affiliations(seasons[s],s)
  if s>3:
   for t,v in regs[s-1].items():regs[s].setdefault(t,v)
 for s in range(4,16):
  rows=seasons[s];matched,a=reconcile(s,rows);teams=sorted({r[k] for r in rows for k in ['team1','team2']});pr,_=prior_regions(seasons[s-1],regs[s-1],90)
  model=DynamicSideBT(teams,regs[s],pr);byday=defaultdict(list);targets=defaultdict(list);past=defaultdict(int);latest=None;known=0;unknown=0
  for r in rows:byday[r['date']].append(r)
  for r in old:
   if r['season']==s:targets[r['date']].append(r)
  for ds in sorted(set(byday)|set(targets)):
   model.advance(date.fromisoformat(ds))
   for r in targets[ds]:
    assert latest is None or latest<ds
    pred.append({**r,'joint_side90':model.predict(r['team1'],r['team2']),'blue_logit':float(model.m[-1]),'blue_state_sd':float(np.sqrt(model.C[-1,-1])),'past_side_maps1':past[r['team1']],'past_side_maps2':past[r['team2']],'side_latest_training_date':latest})
   if targets[ds]:states.append(dict(season=s,date=ds,blue_logit=float(model.m[-1]),blue_state_sd=float(np.sqrt(model.C[-1,-1]))))
   rr=[]
   for r in byday[ds]:
    gg=matched.get(r['detail'])
    if gg:
     assert len(gg)==r['wins1']+r['wins2']
     ww=sum(g['teams']['blue']['win'] if g['a']==r['team1'] else g['teams']['red']['win'] for g in gg);assert ww==r['wins1']
     for g in gg:
      rr.append(dict(date=ds,team1=g['a'],team2=g['b'],wins1=g['teams']['blue']['win'],wins2=g['teams']['red']['win'],side1=1))
     known+=len(gg)
    else:rr.append({**r,'side1':0});unknown+=r['wins1']+r['wins2']
   assert sum(r['wins1']+r['wins2'] for r in rr)==sum(r['wins1']+r['wins2'] for r in byday[ds])
   model.update(rr)
   if byday[ds]:latest=ds
   for r in rr:
    if r['side1']:
     past[r['team1']]+=r['wins1']+r['wins2'];past[r['team2']]+=r['wins1']+r['wins2']
  audit.append(dict(season=s,known_side_maps=known,unknown_side_maps=unknown,gradient=model.max_gradient))
  print('S',s,'known',known,'unknown',unknown,'done',flush=True)
 fields=['dynamic90','joint_side90'];sets={'all':pred,'both_5_side_maps':[r for r in pred if min(r['past_side_maps1'],r['past_side_maps2'])>=5]}
 summary=dict(parameters=dict(side_sd=.5,side_half_life_days=90,side_prior_mean=0,unknown_side_blue_probability=.5),aggregate={name:{f:metrics(rr,f) for f in fields} for name,rr in sets.items()},by_season=[dict(season=s,models={f:metrics([r for r in pred if r['season']==s],f) for f in fields}) for s in range(4,16)],audit=audit)
 clusters=defaultdict(list)
 for r in pred:
  y=r['wins1']>r['wins2'];loss=[]
  for f in fields:
   p=np.clip(series_probability(r[f],r['best_of']),1e-12,1-1e-12);loss.append(-np.log(p if y else 1-p))
  clusters[(r['season'],r['event'])].append(loss[1]-loss[0])
 vals=np.array([[sum(v),len(v)] for k,v in sorted(clusters.items())]);rng=np.random.default_rng(2026);ix=rng.integers(0,len(vals),size=(10000,len(vals)));v=vals[ix].sum(axis=1)
 summary['event_cluster_bootstrap_logloss_delta_95']=np.quantile(v[:,0]/v[:,1],[.025,.975]).tolist()
 summary['baseline_pointer_sha256']=mainhash
 assert len(pred)==1300 and sum(r['wins1']+r['wins2'] for r in pred)==1965
 assert mainhash==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 for name,v in [('predictions',pred),('summary',summary),('side_states',states)]: (OUT/f'{name}.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 report(summary,pred)
 print(json.dumps(summary['aggregate']['all'],ensure_ascii=False),flush=True)

def report(summary,pred):
 a=summary['aggregate']['all']['dynamic90'];b=summary['aggregate']['all']['joint_side90'];delta=b['series_logloss']-a['series_logloss'];ci=summary['event_cluster_bootstrap_logloss_delta_95']
 text='# 训练端红蓝方校正：回测结果\n\n[数据总览](README.md) · [实验设计](../../docs/DETAIL_MODEL_REDESIGN.md)\n\n'
 text+=f'本轮仅测试训练时共同估计选边与实力，没有加入经济状态。系列赛命中率从 {a["series_accuracy"]:.2%} 变为 {b["series_accuracy"]:.2%}；对数损失变化 {delta:+.5f}（负值更好）。主模型及 S16 结果保持不变。\n\n'
 for name,title in [('all','全部系列赛'),('both_5_side_maps','双方此前各有至少5局已核准选边记录')]:
  text+=f'## {title}\n\n| 模型 | 场次 | 系列赛命中率 | 系列赛对数损失 ↓ | 系列赛 Brier ↓ | 小局对数损失 ↓ |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
  for f,label in [('dynamic90','原动态模型'),('joint_side90','联合选边校正')]:
   m=summary['aggregate'][name][f];text+=f'| {label} | {m["covered_series"]} | {m["series_accuracy"]:.2%} | {m["series_logloss"]:.5f} | {m["series_brier"]:.5f} | {m["map_logloss"]:.5f} |\n'
  text+='\n'
 text+='## 逐年表现\n\n| 赛季 | 原命中率 | 新命中率 | 原对数损失 | 新对数损失 | 逐场结果 |\n| --- | ---: | ---: | ---: | ---: | --- |\n'
 directory=REP/'joint_side';directory.mkdir(exist_ok=True)
 for row in summary['by_season']:
  s=row['season'];a=row['models']['dynamic90'];b=row['models']['joint_side90'];text+=f'| S{s} | {a["series_accuracy"]:.2%} | {b["series_accuracy"]:.2%} | {a["series_logloss"]:.5f} | {b["series_logloss"]:.5f} | [明细](joint_side/S{s}.md) |\n'
  detail=f'# S{s} 训练端选边校正逐场回测\n\n[比较结果](../joint_side_comparison.md)\n\n概率指队伍一的系列赛获胜概率，赛前不使用实际选边。\n\n| 日期 | 赛事 | 队伍一 | 队伍二 | 实际比分 | 原胜率 | 新胜率 |\n| --- | --- | --- | --- | --- | ---: | ---: |\n'
  for r in pred:
   if r['season']==s:
    p,q=[series_probability(r[f],r['best_of']) for f in ['dynamic90','joint_side90']]
    detail+=f'| {r["date"]} | {r["event"]} | {r["display1"]} | {r["display2"]} | {r["wins1"]}:{r["wins2"]} | {p:.2%} | {q:.2%} |\n'
  (directory/f'S{s}.md').write_text(detail)
 text+=f'\n## 稳定性与适用范围\n\n按23届赛事进行配对簇 bootstrap（10,000次，种子2026），新减旧的系列赛对数损失差95%区间为 [{ci[0]:.5f}, {ci[1]:.5f}]。'
 text+=('区间跨零，尚不足以确认稳定提升。' if ci[0]<=0<=ci[1] else '这是已反复查看历史赛事后的描述性区间，不能当作独立前瞻检验。')
 text+='\n\n仍有未对账的选边、历史赛事规则近似，以及选边权与队伍偏好的混杂。采用逐日滚动预测，尚未做整届排名与冠军模拟，本轮也不包含对手校正经济残差。不能将本轮结果扩展成整个重设计方案的结论。\n\n## 方法与固定参数\n\n每局胜率为 logistic(双方实力差＋蓝方状态)。蓝方状态与原赛区／战队状态共同更新，初始均值0、标准差0.5，每季重置，90天 AR(1) 记忆和对应平稳过程噪声；这些参数本轮未搜索。原战队、赛区参数及上一年国际赛赛区先验均不变。\n\n已对账系列赛由逐局选边观测替换比分似然；未知选边继续保留赛果，按每局独立蓝／红各50%的混合似然处理。预测端同样边际化，保持原 BO 转换以隔离训练变化；不使用未来实际选边、不积分状态不确定性、不模拟败者选边策略。这些是候选假设，不是官方规则复现。\n\n每日先预测后联合更新。使用解析梯度与 Hessian 的 Laplace 滤波，未知选边混合似然不保证全局凸，得到的是局部 MAP 近似。梯度和 Hessian 已用数值差分验证；关闭选边项可恢复原动态更新。\n\n## 胜负记录守恒\n\n| 赛季 | 已知选边小局 | 未知选边小局（仍训练） |\n| --- | ---: | ---: |\n'
 for a in summary['audit']:text+=f'| S{a["season"]} | {a["known_side_maps"]} | {a["unknown_side_maps"]} |\n'
 (REP/'joint_side_comparison.md').write_text(text)
if __name__=='__main__':main()

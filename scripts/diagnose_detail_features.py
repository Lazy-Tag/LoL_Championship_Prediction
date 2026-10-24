"""Post-hoc diagnostics, never changes the published model or predictions."""
import json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from backtest import load_season,metrics
from evaluate_detail_features import reconcile
from model import series_probability
R=Path(__file__).resolve().parents[1];OUT=R/'results/detail_experiment';REP=R/'reports/detailed_data'
F=['dynamic90','side_economy90']
def loss(r,f):
 p=np.clip(series_probability(r[f],r['best_of']),1e-12,1-1e-12);y=r['wins1']>r['wins2']
 return float(-np.log(p if y else 1-p))
def main():
 pred=json.loads((OUT/'predictions.json').read_text());coef=json.loads((OUT/'coefficients.json').read_text());audit=json.loads((OUT/'reconciliation.json').read_text())
 groups=defaultdict(list)
 for r in pred:
  a,b=r['past_economy_maps1'],r['past_economy_maps2']
  label='双方都无记录' if a==b==0 else '仅一方有记录' if min(a,b)==0 else '双方均至少5局' if min(a,b)>=5 else '双方有记录但一方不足5局'
  groups[label].append(r)
  groups['跨赛区' if r['region1']!=r['region2'] else '同赛区'].append(r)
  r['gated90']=r['side_economy90'] if r['detailed_history_both'] else r['dynamic90']
 subsets={k:dict(n=len(rr),models={f:metrics(rr,f) for f in F},loss_delta_sum=sum(loss(r,F[1])-loss(r,F[0]) for r in rr)) for k,rr in groups.items()}
 leagues=defaultdict(Counter);seasoncoef=[]
 for s in range(6,16):
  rows,_=load_season(s);matched,a=reconcile(s,rows)
  for gg in matched.values():
   for g in gg:
    c=leagues[(s,g['league'])];c['matched']+=1
    stats=[g['teams'][side]['stats'] for side in ['blue','red']]
    if all(t['goldat15'] is not None for t in stats):
     c['gold15']+=1
     if all(t['goldat15']==0 for t in stats):c['both_zero']+=1
     if all(t['golddiffat15'] is not None for t in stats):
      if abs(stats[0]['goldat15']-stats[1]['goldat15']-stats[0]['golddiffat15'])>1e-6:c['diff_inconsistent']+=1
  cc=[x for x in coef if x['season']==s];betas=[x['side_economy'][0] for x in cc];bb=[x['side_economy'][1] for x in cc]
  seasoncoef.append(dict(season=s,economy_min=min(betas),economy_max=max(betas),side_min=min(bb),side_max=max(bb)))
  print('S',s,'done',flush=True)
 result=dict(subsets=subsets,gated={f:metrics(pred,f) for f in ['dynamic90','side_economy90','gated90']},league_coverage=[dict(season=s,league=l,**c) for (s,l),c in sorted(leagues.items())],coefficients=seasoncoef)
 (OUT/'diagnosis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 text='# 为什么详细数据没有提升？\n\n[初次实验](model_comparison.md) · [方法](DETAIL_MODEL.md)\n\n结论：本轮存在特征使用方式的局限，也有明显的数据缺失；不能仅归因于缺失，更不能据此认为经济数据无用。主模型保持不变。以下为观察结果后的诊断，不是新的独立模型验证。\n\n## 缺失能解释多少\n\n覆盖以比赛前累计可用经济小局数定义，不是90天衰减后的有效样本量；“至少5局”也不保证近期数据充足。\n\n| 历史数据组 | 系列赛 | 原模型命中率 | 新模型命中率 | 原对数损失 | 新对数损失 | 对数损失增加总量 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n'
 for name,d in subsets.items():
  a,b=[d['models'][f] for f in F];text+=f'| {name} | {d["n"]} | {a["series_accuracy"]:.2%} | {b["series_accuracy"]:.2%} | {a["series_logloss"]:.5f} | {b["series_logloss"]:.5f} | {d["loss_delta_sum"]:.3f} |\n'
 text+='\n四种历史记录覆盖组互斥；同／跨赛区是另一种划分，不能将全部行相加。正的损失增加表示新方案较差。双方各有至少5局记录的子集仍退步，因此“只要补齐数据就会提升”没有得到支持。\n\n## 检查缺失时退回原模型\n\n将双方不足5局的对局完全退回原模型，只在共同覆盖子集启用原来的增强概率。这是不重新拟合的事后消融，用来检查缺失分支的影响。\n\n| 方案 | 命中率 | 系列赛对数损失 |\n| --- | ---: | ---: |\n'
 for f,label in [('dynamic90','原动态'),('side_economy90','原增强'),('gated90','缺失时退回原动态')]:
  m=result['gated'][f];text+=f'| {label} | {m["series_accuracy"]:.2%} | {m["series_logloss"]:.5f} |\n'
 text+='\n这不是“填补缺失”的因果实验；它只能衡量关掉相应预测修正的效果。\n\n## 使用方式中的局限\n\n1. **只是原实力之上的线性修正。** 本轮并未让经济表现参与动态实力状态的估计，也没有用详细数据补充新胜负样本。它测试的是很窄的一种用法。\n2. **原始经济优势没有校正对手。** 对弱队领先2000经济，与对强队领先2000经济被同样累计。国内赛上拟合出的系数未必适合国际赛；这与原动态实力可能存在信息重叠。当前结果支持存在迁移风险，但不能独立证明它就是退步原因。\n3. **缺失在特征层被收缩到零。** 未把缺失局的经济硬填0，但没有历史记录的队伍最终特征为0，和真实平均经济持平无法区分。只有一方有记录时还会形成单边比较；目前没有缺失指示、联赛分层或有效样本量交互项。\n4. **红蓝方在未知选边时被平均。** 预测为蓝／红各50%的平均，不使用实际选边；它主要改变概率幅度，很难改善胜负排序。固定正负截距对称平均是严格递增函数，且在实力差为0时等于0.5，所以给定同一经济系数时不会改变预测胜者。两候选的少量胜者差异来自联合拟合后经济系数改变。\n5. **赛区、版本、阵容和局序未建模。** 每年只有一个经济系数与一个选边截距；没有对手校正、经济的观测噪声模型或赛事层级交互。更多字段下载成功不等于已经有效使用。\n\n## 实际字段缺失\n\n下表只统计已同日比分对账成功的记录；缺失随赛季和联赛变化，不是均匀随机缺失。\n\n| 赛季 | 联赛／赛事 | 对账小局 | 双方15分钟经济齐全 | 完整率 |\n| --- | --- | ---: | ---: | ---: |\n'
 for c in result['league_coverage']:text+=f'| S{c["season"]} | {c["league"]} | {c["matched"]} | {c.get("gold15",0)} | {c.get("gold15",0)/c["matched"]:.1%} |\n'
 totals=Counter()
 for c in leagues.values():totals.update(c)
 text+=f'\n已对账 {totals["matched"]:,} 局，其中双方15分钟经济齐全 {totals["gold15"]:,} 局。双方经济均为0：{totals["both_zero"]} 局；双方绝对经济与蓝方经济差字段不一致：{totals["diff_inconsistent"]} 局。这里的字段一致性检查不证明来源内容绝对正确。\n'
 text+='\n## 代码检查及下一步\n\n本次重放逐条断言原动态概率与已保存基线相差小于1e-9；拟合只取此前日期，同日先预测再更新；小局通过整场比分核对后仅附加特征，没有重复增加胜负样本。未发现这几类实现错误，退步也不应简单解释成“数据完全没用”。\n\n建议先改进数据可用性建模和对手校正，再评估经济信号是否有增量价值；将赛季／联赛覆盖与距最近观测的天数显式记录。候选方案应事先固定，再用未参与选择的赛事评估，不能根据这次国际赛结果反复调参后宣称泛化提升。暂不改主结果，不重跑 S16 冠军模拟。\n'
 (REP/'diagnosis.md').write_text(text)
 print(json.dumps({k:{'n':v['n'],'loss_delta_sum':v['loss_delta_sum']} for k,v in subsets.items()},ensure_ascii=False))
 print(json.dumps(result['gated'],ensure_ascii=False))
if __name__=='__main__':main()

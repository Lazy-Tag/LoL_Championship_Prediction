"""Reader-facing independent posterior uncertainty and event-form ablations."""
import json,hashlib
from pathlib import Path
import numpy as np
from scipy.stats import rankdata
from report_chain_events import evaluate
from report_event_replay import table,band,FORMATS
from region_rankings import region_rankings,section
from build_latent_event_engine import source
R=Path(__file__).resolve().parents[1];D=R/'results/latent_events';P=R/'reports/latent_events'
NAMES={'baseline':'原动态','posterior':'联合实力不确定性','event_form':'整届共享状态（0.35）'}
KEYS=['champion_logloss','champion_brier','finish_spearman','title_spearman','finish_mae','champion_probability']
def main():
 P.mkdir(exist_ok=True);cs=json.loads((D/'event_configs.json').read_text());events=[]
 for c in cs:
  models={}
  for mode in NAMES:
   path=R/f'results/model_experiments/dynamic90/{c["id"]}.json' if mode=='baseline' else D/mode/f'{c["id"]}.json'
   raw=json.loads(path.read_text())
   if mode=='baseline':
    assert raw['input_sha256']==c['baseline_input_sha256']
    assert raw['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
   else:
    assert raw['engine_sha256']==hashlib.sha256(source().encode()).hexdigest()
    assert raw['input_sha256']==hashlib.sha256(path.with_suffix('.txt').read_bytes()).hexdigest()
   models[mode]=evaluate(c,raw)
  events.append(dict(id=c['id'],year=c['year'],event=c['event'],models=models))
  text=f'# {c["year"]} {c["event"]}：两项独立实验\n\n[比较总览](README.md) · [逐届赛制](../event_replay/rules.md)\n\n开赛截点：{c["start_date"]}。三模型共享赛前均值实力、参赛队和赛制；两个候选每届各14,000,605次，种子{c["year"]}，原结果复用同规模已验证模拟。\n\n'
  text+=f'本届独立配置：{FORMATS[c["kind"]]} 仍沿用原历史规则近似。\n\n'
  # Prior region strength rankings identical; retain baseline probability context explicitly.
  regs=region_rankings([dict(name=c['display'][t],region=c['regions'][t],strength=c['strength'][t],title_probability=models['baseline']['teams'][i]['championship_probability']) for i,t in enumerate(c['teams'])]);text+=section(regs)
  text+='上表按共同赛前均值实力排序；赛区概率列沿用原动态模型，两个候选的队伍概率分别列在下面。\n\n'
  n=len(c['teams']);ranks=rankdata(-np.round(c['means'],12));order=sorted(range(n),key=lambda i:-models['baseline']['teams'][i]['championship_probability'])
  text+=table(['队伍','均值实力排名','实际名次','原夺冠概率','不确定性夺冠概率','整届状态夺冠概率','原预期名次','不确定性预期名次','整届状态预期名次'],[[c['display'][c['teams'][i]],f'{ranks[i]:g}',band(models['baseline']['teams'][i]['actual_rank']),*[f'{models[m]["teams"][i]["championship_probability"]:.3%}' for m in NAMES],*[f'{models[m]["teams"][i]["expected_rank"]:.3f}' for m in NAMES]] for i in order])
  text+=table(['模型','预测冠军','实际冠军概率','冠军对数损失','冠军 Brier','名次相关','名次绝对误差'],[[NAMES[m],models[m]['favorite'],f'{models[m]["champion_probability"]:.3%}',*[f'{models[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in NAMES])
  text+=f'实际冠军：**{models["baseline"]["champion"]}**。名次用共同淘汰阶段区间比较，不虚构并列队伍的精确先后。\n\n'
  text+='## 赛前估计的不确定性\n\n下表是单队实力后验标准差，不是胜率误差条。联合模拟同时保留队伍之间的协方差，不能只看这些单队数值判断对阵不确定性。整届状态实验则对所有队伍使用独立0.35偏移，不使用这里的协方差。\n'
  text+=table(['队伍','实力后验标准差'],[[c['display'][t],f'{np.sqrt(c["joint_covariance"][i][i]):.4f}'] for i,t in enumerate(c['teams'])])
  (P/f'{c["id"]}.md').write_text(text)
 summary={m:dict(events=23,champion_hits=sum(e['models'][m]['champion_hit'] for e in events),**{k:float(np.mean([e['models'][m][k] for e in events])) for k in KEYS}) for m in NAMES}
 rng=np.random.default_rng(2026);ix=rng.integers(0,len(events),(10000,len(events)));ci={}
 for m in ['posterior','event_form']:
  ci[m]={}
  for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']:
   delta=np.array([e['models'][m][k]-e['models']['baseline'][k] for e in events]);ci[m][k]=np.quantile(delta[ix].mean(axis=1),[.025,.975]).tolist()
 result=dict(summary=summary,paired_event_bootstrap_delta_95=ci,events=events)
 (D/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 text='# 实力不确定性与整届状态：分别比较\n\n[项目首页](../../README.md) · [此前系列赛状态实验](../form_chain/events/README.md)\n\nS4–S15共23届 MSI／MSC／Worlds；每个候选每届14,000,605次，种子为公历年份。两个候选分别与当前 dynamic90 比较，互不叠加，不使用经济、选边或近期表现修正。主模型与 S16 结果未覆盖。\n\n'
 text+=table(['模型','冠军命中','冠军对数损失 ↓','冠军 Brier ↓','预期名次相关 ↑','名次绝对误差 ↓'],[[NAMES[m],f'{summary[m]["champion_hits"]}/23',*[f'{summary[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in NAMES])
 text+='**判断：联合实力不确定性并未整体改善；整届状态改善了冠军概率的两项误差指标，但冠军命中不变、最终名次变差，仍保留原主模型。**\n\n'
 text+='冠军对数损失使用实际冠军概率；Brier为当届全部战队的概率误差平方和。预期名次相关为 Spearman，绝对误差以共同淘汰阶段中点比较；按赛事等权平均，相关系数不是命中率。\n\n## 两项实验分别改变什么\n\n- **联合实力不确定性**：从赛事开始前现有模型的完整联合高斯后验抽取一次战队实力向量，整届保持；使用战队间协方差，不是每队各自独立抽样。不额外添加临场波动。\n- **整届共享状态**：原实力固定在后验均值，每队额外独立抽取一次标准差0.35的零均值高斯偏移，贯穿整届，不随每个系列赛重抽。不使用第一项的后验方差。0.35在本轮前固定，尚未从数据校准，也未按23届结果搜索。\n\n两者的原始均值实力排名相同，但随机性来源不同；不能把结果解释为能从这些赛事区分“真实发挥变化”和“实力估计不准”。\n\n## 逐届冠军概率\n'
 text+=table(['赛事','实际冠军','原概率','不确定性概率','整届状态概率','原首选','不确定性首选','整届状态首选'],[[f'[{e["id"]}]({e["id"]}.md)',e['models']['baseline']['champion'],*[f'{e["models"][m]["champion_probability"]:.3%}' for m in NAMES],*[e['models'][m]['favorite'] for m in NAMES]] for e in events])
 text+='## 最终排名一致性\n'
 text+=table(['赛事','原名次相关','不确定性名次相关','整届状态名次相关','原名次绝对误差','不确定性误差','整届状态误差'],[[e['id'],*[f'{e["models"][m][k]:.4f}' for k in ['finish_spearman','finish_mae'] for m in NAMES]] for e in events])
 text+='## 改善是否集中于少数赛事\n\n以下为事后影响诊断，2022 Worlds 仍保留在所有主评价中，不据此重新筛选样本或调参。\n'
 sensitivity=[]
 for m in ['posterior','event_form']:
  ds=[e['models'][m]['champion_logloss']-e['models']['baseline']['champion_logloss'] for e in events]
  drx=next(e for e in events if e['id']=='2022_Worlds');dd=drx['models'][m]['champion_logloss']-drx['models']['baseline']['champion_logloss']
  sensitivity.append([NAMES[m],f'{sum(x<0 for x in ds)}/23',f'{dd:+.5f}',f'{(sum(ds)-dd)/22:+.5f}'])
 text+=table(['候选','冠军对数损失改善赛事数','2022 Worlds 损失差','其余22届平均损失差'],sensitivity)
 text+='整届状态的平均对数损失收益高度集中于2022 Worlds（DRX夺冠）；其余22届平均几乎持平、略差。因此不能将总均值改善理解为多数赛事稳定受益。\n\n'
 text+='## 差异区间\n\n按赛事进行10,000次配对 bootstrap，种子2026；下表是候选减原模型的平均差95%区间。损失和误差为负较好，相关为正较好。\n'
 text+=table(['候选','指标','区间'],[[NAMES[m],label,f'[{ci[m][k][0]:.5f}, {ci[m][k][1]:.5f}]'] for m in ci for k,label in [('champion_logloss','冠军对数损失'),('champion_brier','冠军 Brier'),('finish_spearman','预期名次相关'),('finish_mae','名次绝对误差')]])
 text+='历史赛事已经多次用于比较，只有23届，跨赛事也可能相关；这是探索性回测，不能把区间当作未来收益保证。更换随机数调用结构后，同年份种子也不代表完整路径始终严格配对。\n\n## 规则与模拟边界\n\n每届使用相应年份的独立赛制配置，包含阶段、种子、入围赛、分组／瑞士轮、BO与单败／双败；2020 MSC 单列。旧同分、抽签和对手选择近似保留，新旧使用同一规则情景。\n\n每次完整模拟开始时抽取一次潜在实力，所有之后对局共享该抽样；给定它，各局仍独立，BO概率使用原多项式。没有沿模拟路径再次学习虚构赛果，也不偷用真实赛事中的比分。抽样偏移是隐藏状态：需要选择对手时仍沿用原均值实力策略，不允许选择者看见模拟中的真实潜在实力。\n\n只涉及单局胜率的固定表无法保留整届相关性，因此本轮在每次完整模拟中更新条件概率，并按对阵缓存以控制成本。两项均是蒙特卡洛估计，后验本身仍是原模型的 Laplace 高斯近似。\n\n[实现与验收](METHOD.md)\n'
 (P/'README.md').write_text(text)
 (P/'METHOD.md').write_text('''# 两项独立整届实验：实现与验收\n\n[结果](README.md)\n\n当季按日期重放原 DynamicBT，在每届开赛前保存均值 m 与协方差 C。用 H 把赛区＋队伍状态映射到参赛队总实力，得到 μ=Hm、Σ=HCHᵀ；逐队均值与原整届配置核对到1e-9。Cholesky分解保留所有联合相关项，无额外方差放大。\n\n第一项每次模拟使用 θ=μ+Lz，LLᵀ=Σ，z为独立标准正态。第二项使用 θ=μ+0.35z，完全不使用Σ。整届都保留同一个θ。没有同时运行两者叠加的候选。\n\n随机源为按赛事年份初始化的 mt19937_64，标准正态采样使用 C++ 标准库 normal_distribution；相同源码、编译器与运行库可复现，不承诺跨标准库逐位相同。原对局和抽签都在同一随机流中继续运行。\n\n脚本 build_latent_event_engine.py 从原引擎生成隔离扩展；原 scripts/event_simulation.cpp 不改动。扩展只加入整届潜在向量与条件对局概率，保持基于均值的对手选择策略。run_latent_events.py 保存输入／引擎哈希、截止与联合协方差；report_latent_events.py 输出逐队概率及名次。\n\n验收要求：零方差还原原路径；23届原输入的规则输出一致；联合采样矩与目标协方差一致；同次模拟同一对阵概率不随重复查询变化；不同模拟重新抽样；每队名次计数和为14,000,605；冠军总计数相同；每次名次和守恒；日期严格早于开赛；原主模型指针与 S16 输出不变。\n''')
 print(json.dumps(summary,ensure_ascii=False),flush=True);print('paired intervals',ci,flush=True)
if __name__=='__main__':main()

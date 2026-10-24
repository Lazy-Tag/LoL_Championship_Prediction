"""Compare shared-series events with the unchanged dynamic90 event baseline."""
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.stats import rankdata
from report_event_replay import common_band,correlation,band,table,FORMATS
from region_rankings import region_rankings,section
from build_chain_engine import source
R=Path(__file__).resolve().parents[1];OUT=R/'results/chain_events';REP=R/'reports/form_chain/events';N=14_000_605

def evaluate(c,raw):
 assert raw['samples']==N and raw['seed']==c['year'];n=len(c['teams']);teams=[]
 assert all(sum(k for lo,hi,k in bins)==N for bins in raw['counts'])
 assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==N
 assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
 for t,bins in zip(c['teams'],raw['counts']):
  p=sum(k for lo,hi,k in bins if lo==hi==1)/N;actual=common_band(c,*c['actual_ranks'][t]);expected=sum(sum(common_band(c,lo,hi))/2*k/N for lo,hi,k in bins)
  teams.append(dict(team=t,name=c['display'][t],championship_probability=p,actual_rank=list(actual),actual_midrank=sum(actual)/2,expected_rank=expected))
 probs=np.array([t['championship_probability'] for t in teams]);actual=np.array([t['actual_midrank'] for t in teams]);expected=np.array([t['expected_rank'] for t in teams]);champ=next(i for i,t in enumerate(teams) if t['actual_rank']==[1,1]);favorite=int(np.argmax(probs));prank=rankdata(-probs);erank=rankdata(expected)
 for i,t in enumerate(teams):t.update(championship_probability_rank=float(prank[i]),expected_finish_order=float(erank[i]))
 return dict(teams=teams,champion=teams[champ]['name'],favorite=teams[favorite]['name'],champion_hit=champ==favorite,champion_probability=float(probs[champ]),champion_logloss=-math.log(probs[champ]) if probs[champ] else None,champion_brier=float(np.sum((probs-(np.arange(n)==champ))**2)),finish_spearman=correlation(expected,actual),title_spearman=correlation(prank,actual),finish_mae=float(np.mean(np.abs(expected-actual))))

def main():
 REP.mkdir(parents=True,exist_ok=True);configs=json.loads((OUT/'event_configs.json').read_text());events=[]
 for c in configs:
  oldpath=R/f'results/model_experiments/dynamic90/{c["id"]}.json';newpath=OUT/f'{c["id"]}.json';old=json.loads(oldpath.read_text());new=json.loads(newpath.read_text())
  assert old['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
  assert old['input_sha256']==c['base_input_sha256']
  assert new['input_sha256']==hashlib.sha256(newpath.with_suffix('.txt').read_bytes()).hexdigest()
  assert new['engine_sha256']==hashlib.sha256(source().encode()).hexdigest()
  assert c['rho_latest_training_date'] is None or c['rho_latest_training_date']<c['start_date']
  a=evaluate(c,old);b=evaluate(c,new);events.append(dict(id=c['id'],year=c['year'],event=c['event'],rho=c['rho'],baseline=a,shared=b))
  body=f'# {c["year"]} {c["event"]}：冠军概率与最终名次对照\n\n[总览](README.md) · [对应赛制](../../event_replay/rules.md)\n\n赛前截点：{c["start_date"]}；状态相关系数ρ={c["rho"]:.5f}，仅用此前当季国内赛估计。每个模型14,000,605次模拟，种子{c["year"]}。两者战队实力与赛制相同；共享状态只改变系列赛内相关性，不跨系列赛持续。\n\n'
  body+=f'本届配置：{FORMATS[c["kind"]]} 部分历史规则近似沿用原实现。\n\n'
  reg=region_rankings([dict(name=c['display'][t],region=c['regions'][t],strength=c['strength'][t],title_probability=b['teams'][i]['championship_probability']) for i,t in enumerate(c['teams'])]);body+=section(reg)
  sr=rankdata(-np.round([c['strength'][t] for t in c['teams']],12))
  body+=table(['队伍','共同实力排名','原夺冠概率','新夺冠概率','概率变化（百分点）','实际名次','原预期名次','新预期名次'],[[b['teams'][i]['name'],f'{sr[i]:g}',f'{a["teams"][i]["championship_probability"]:.3%}',f'{b["teams"][i]["championship_probability"]:.3%}',f'{100*(b["teams"][i]["championship_probability"]-a["teams"][i]["championship_probability"]):+.3f}',band(b['teams'][i]['actual_rank']),f'{a["teams"][i]["expected_rank"]:.3f}',f'{b["teams"][i]["expected_rank"]:.3f}'] for i in sorted(range(len(c['teams'])),key=lambda i:-b['teams'][i]['championship_probability'])])
  body+=f'实际冠军：**{a["champion"]}**。原模型首选：**{a["favorite"]}**；共享状态首选：**{b["favorite"]}**。\n\n'
  body+=table(['指标','原动态','共享状态'],[[label,f'{a[k]:.5f}',f'{b[k]:.5f}'] for k,label in [('champion_logloss','冠军对数损失 ↓'),('champion_brier','冠军 Brier ↓'),('finish_spearman','预期名次 Spearman ↑'),('finish_mae','预期名次绝对误差 ↓')]])
  body+='预期名次为共同淘汰阶段名次区间中点的期望；并列名次保留。赛区实力排行两模型相同，因为原赛前实力没有改变。\n'
  (REP/f'{c["id"]}.md').write_text(body)
 summary={}
 for mode in ['baseline','shared']:
  summary[mode]=dict(events=len(events),champion_hits=sum(e[mode]['champion_hit'] for e in events),**{k:float(np.mean([e[mode][k] for e in events])) for k in ['champion_logloss','champion_brier','finish_spearman','title_spearman','finish_mae','champion_probability']})
 rng=np.random.default_rng(2026);ix=rng.integers(0,len(events),(10000,len(events)));ci={}
 for key in ['champion_logloss','champion_brier','finish_spearman','finish_mae']:
  delta=np.array([e['shared'][key]-e['baseline'][key] for e in events]);ci[key]=np.quantile(delta[ix].mean(axis=1),[.025,.975]).tolist()
 result=dict(summary=summary,paired_event_bootstrap_delta_95=ci,events=events)
 (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 body='# 共享临场状态：历史冠军与最终排名比较\n\n[逐场状态实验](../README.md) · [各年赛制与近似](../../event_replay/rules.md)\n\nS4–S15 共23届 MSI／MSC／Worlds。原模型是当前 dynamic90 主模型；候选加入每个系列赛独立的共享临场状态。赛前实力、训练截止、参赛队与赛制实现完全相同。每届每模型14,000,605次，种子为年份；原模型复用已校验的同规模模拟。主结果和 S16 概率未覆盖。\n\n'
 body+=table(['模型','冠军命中','冠军对数损失 ↓','冠军 Brier ↓','预期名次相关 ↑','名次绝对误差 ↓'],[[label,f'{summary[m]["champion_hits"]}/23',*[f'{summary[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m,label in [('baseline','原动态'),('shared','系列赛共享状态')]])
 body+='**判断：冠军概率指标小幅改善，冠军命中不变，名次指标有升有降；配对区间跨零，尚不足以证明稳定提升，保留原主模型。**\n\n冠军对数损失为实际冠军概率的负对数；冠军 Brier 为当届全体战队概率误差平方和。预期名次相关使用 Spearman，绝对误差使用共同淘汰阶段区间中点；各届等权平均。相关系数不是百分比正确率。\n\n## 逐届对照\n'
 body+=table(['赛事','实际冠军','原冠军概率','新冠军概率','原首选','新首选','原冠军对数损失','新冠军对数损失'],[[f'[{e["id"]}]({e["id"]}.md)',e['baseline']['champion'],f'{e["baseline"]["champion_probability"]:.3%}',f'{e["shared"]["champion_probability"]:.3%}',e['baseline']['favorite'],e['shared']['favorite'],f'{e["baseline"]["champion_logloss"]:.4f}',f'{e["shared"]["champion_logloss"]:.4f}'] for e in events])
 body+='## 最终名次比较\n'
 body+=table(['赛事','原名次相关','新名次相关','原名次绝对误差','新名次绝对误差'],[[e['id'],*[f'{e[m][k]:.4f}' for k in ['finish_spearman','finish_mae'] for m in ['baseline','shared']]] for e in events])
 body+='## 差异是否稳定\n\n以赛事为单位的配对 bootstrap（10,000次，种子2026），候选减原模型的平均指标差95%区间：\n'
 body+=table(['指标','区间','更好方向'],[[label,f'[{ci[k][0]:.5f}, {ci[k][1]:.5f}]','正' if k=='finish_spearman' else '负'] for k,label in [('champion_logloss','冠军对数损失'),('champion_brier','冠军 Brier'),('finish_spearman','预期名次相关'),('finish_mae','名次绝对误差')]])
 body+='只有23届且此前已多次查看这些历史赛事；不同赛事也未必独立。区间是描述性参考，不是未见数据上的保证。新旧采用同年份种子，路径分歧后随机调用顺序可能变化，不能当作每条完整模拟路径始终一一配对。\n\n## 每届独立赛制与计算方式\n\n每届分别加载对应年份的参赛队、阶段、轮空、分组／瑞士轮、各轮 BO、单败／双败及晋级规则；2020 MSC 单列。没有用统一淘汰模板代替所有年份。旧同分、抽签和对手选择近似沿用基线，因此是相同规则情景下的模型对比，并非完全官方赛制复现。\n\n系列赛潜在胜率 q 服从 Beta 分布，其均值为原单局胜率，相关强度ρ只用该赛事开赛前国内赛估计并冻结。先精确积分得到 BO3／BO5 胜率，再模拟整届；在仅依赖系列赛胜者、每场状态独立的假设下，与显式抽取 q 再逐局模拟的胜者分布等价。BO1 胜率不变。不同系列赛不继承刚才模拟的胜负，也不使用赛事中的真实比分更新。\n\n因此本轮检验的是系列赛内共享状态对赛前冠军和名次分布的影响，不包含近期状态修正、跨场长期状态传播、参数不确定性、全局 BP、换人或选边。独立扩展引擎已验证：给原输入时，23届各1000次的全部名次计数及随机规则统计与原引擎一致。\n'
 (REP/'README.md').write_text(body)
 print(json.dumps(summary,ensure_ascii=False));print('paired intervals',ci)
if __name__=='__main__':main()

"""Render the user-selected dynamic model as the primary reader reports.
Legacy numeric artifacts remain explicit baselines; primary selection is recorded
in results/main_model.json and never achieved by relabelling legacy probabilities.
"""
import json,math,re
from pathlib import Path
import numpy as np
from scipy.special import expit
from backtest import metrics,key
from model import WORLD_TEAMS,series_probability
from report_event_replay import table
from region_rankings import region_rankings,section,order_text
R=Path(__file__).resolve().parents[1];RES=R/'results/model_experiments'
def read(p):return json.loads(p.read_text())
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n')
def pct(x):return '<0.01%' if x<.0001 else f'{x*100:.2f}%'
LIMIT='未考虑全局 BP、赛季中换人、替补、选边、版本效应与系列赛内相关性。历史训练数据仍有缺口，部分旧赛制的同分和抽签机制采用近似；这些误差不能通过增加模拟消除。'
def main():
 pred=read(RES/'predictions.json');summary=read(RES/'summary.json');eventsummary=read(RES/'event_summary.json')['dynamic90'];configs=read(RES/'event_configs.json')['dynamic90'];raw=read(RES/'dynamic90/2026_Worlds.json');n=raw['simulations'];state=read(RES/'s16_states.json')['states']['dynamic90'];m=summary['aggregate']['dynamic90'];hits=sum(e['hit'] for e in eventsummary)
 selection=dict(main_model='dynamic90',half_life_days=90,predictions='results/model_experiments/predictions.json',probability_field='dynamic90',historical_configs='results/model_experiments/event_configs.json',historical_summary='results/model_experiments/event_summary.json',s16_result='results/model_experiments/dynamic90/2026_Worlds.json',s16_states='results/model_experiments/s16_states.json',cutoff='2026-10-14',reference='2026-10-19',baseline_results_retained=True)
 write(R/'results/main_model.json',json.dumps(selection,ensure_ascii=False,indent=2))
 # S16 reports show probabilities only, not simulated frequencies or run counts.
 ordered=sorted(zip(WORLD_TEAMS,raw['counts']),key=lambda x:-x[1][0]);head=['排名','队伍','进入瑞士轮','进入八强','进入四强','进入决赛','夺冠']
 rows=[[i,t,*[pct(c[j]/n) for j in [1,2,3,4,0]]] for i,(t,c) in enumerate(ordered,1)]
 region=region_rankings([dict(name=t,region=v[1],strength=state[key(v[0])],title_probability=raw['counts'][i][0]/n) for i,(t,v) in enumerate(WORLD_TEAMS.items())])
 write(R/'results/main_s16_region_rankings.json',json.dumps(region,ensure_ascii=False,indent=2))
 body='# S16：队伍排名与过关概率\n\n[返回首页](../../README.md) · [两两胜率](matchups-90.md) · [已纳入赛果](matches.md) · [模型细节](../../MODEL.md)\n\n使用截至 **2026 年 10 月 14 日** 的比赛结果，参考日为 **10 月 19 日**。按夺冠概率排名；各列是从赛事开始算起的累计晋级概率，不是晋级后下一轮的条件胜率。\n'+table(head,rows)+section(region)+'## 队伍与种子\n'+table(['简称','队伍','赛区','赛区种子'],[[k,*v] for k,v in WORLD_TEAMS.items()])+'## 阅读提示\n\n概率为模拟估计。小于 0.01% 不代表不可能；相近概率的排名不应被解读为稳定差距。'+LIMIT+'\n\n[其他模型的敏感性比较](../sensitivity/candidate_models.md) · [逐局数据覆盖审计](../data_enrichment/README.md)\n'
 write(R/'reports/s16/README.md',body)
 pairs=[]
 for i,(a,va) in enumerate(WORLD_TEAMS.items()):
  for b,vb in list(WORLD_TEAMS.items())[i+1:]:
   p=expit(state[key(va[0])]-state[key(vb[0])]);pairs.append([a,b,*[pct(float(series_probability(p,bo))) for bo in [1,3,5]]])
 write(R/'reports/s16/matchups-90.md','# S16：两两对决胜率\n\n[晋级与夺冠概率](README.md) · [模型细节](../../MODEL.md)\n\n全部为 A 队战胜 B 队的概率；反向胜率为 1 减去对应数值。BO3／BO5 使用固定小局胜率换算，尚未区分局序、全局 BP 和系列赛内相关性。\n'+table(['A 队','B 队','BO1','BO3','BO5'],pairs))
 overview='# S4–S15：历史逐场预测\n\n[返回首页](../../README.md) · [整届排名与夺冠预测](../event_replay/README.md) · [模型细节](../../MODEL.md)\n\n'
 overview+=f'在 **{m["covered_series"]:,} 场系列赛、{m["maps"]:,} 小局**上，系列赛命中率 **{pct(m["series_accuracy"])}**，小局命中率 **{pct(m["map_accuracy"])}**。评价 MSI、2020 MSC 与 Worlds；每场只使用更早日期的已知成绩，同日不更新。S3 不回放。\n\n'
 by=[]
 for s in range(4,16):
  pp=[r for r in pred if r['season']==s];v=metrics(pp,'dynamic90');by.append([f'[S{s}](S{s}/README.md)',len(pp),v['maps'],pct(v['series_accuracy']),pct(v['map_accuracy']),f'{v["map_logloss"]:.4f}'])
  seasonbody=f'# S{s}（{s+2010}）：预测与实际\n\n[全部赛季](../README.md) · [逐场预测](predictions.md) · [小局概率](probabilities.md) · [全部已收集赛果](matches.md)\n\n系列赛命中率 **{pct(v["series_accuracy"])}**；小局命中率 **{pct(v["map_accuracy"])}**。各赛季战队状态独立，跨年只使用上一季国际赛的赛区信息；详细方法见[模型说明](../../../MODEL.md)。\n'
  er=[]
  for event in sorted({r['event'] for r in pp}):
   q=metrics([r for r in pp if r['event']==event],'dynamic90');er.append([event,q['covered_series'],q['maps'],pct(q['series_accuracy']),pct(q['map_accuracy'])])
  seasonbody+=table(['赛事','系列赛','小局','系列赛命中率','小局命中率'],er)+'## 数据边界\n\n'+('S4 国内赛果存在明显缺口。' if s==4 else '')+LIMIT+'\n'
  write(R/f'reports/history/S{s}/README.md',seasonbody)
  pr=[];probs=[]
  for r in pp:
   p=r['dynamic90'];tie=abs(p-.5)<1e-12;winner='五五开' if tie else r['display1'] if p>.5 else r['display2'];hit='半次期望命中' if tie else '✓' if (p>.5)==(r['wins1']>r['wins2']) else '✗'
   pr.append([r['date'],r['event'],r['display1'],f"[{r['wins1']}:{r['wins2']}]({r['detail']})",r['display2'],f"BO{r['best_of']}",pct(float(series_probability(p,r['best_of']))),winner,hit]);probs.append([r['date'],r['display1'],r['display2'],pct(p),r['latest_training_date'] or '无'])
  write(R/f'reports/history/S{s}/predictions.md',f'# S{s}：逐场预测与实际\n\n[本季汇总](README.md) · [小局概率](probabilities.md)\n\nA 系列赛胜率由赛前小局胜率换算。五五开计半次期望命中。\n'+table(['日期','赛事','A 队','实际比分','B 队','赛制','A 系列赛胜率','预测胜者','命中'],pr))
  write(R/f'reports/history/S{s}/probabilities.md',f'# S{s}：逐场小局概率\n\n[本季汇总](README.md)\n\n全部为 A 队获胜概率，非系列赛概率。\n'+table(['日期','A 队','B 队','A 小局胜率','最晚训练日'],probs))
 overview+=table(['赛季','系列赛','小局','系列赛命中率','小局命中率','小局对数损失'],by)+'## 解释\n\n对数损失越低越好，它同时惩罚过度自信的错误概率。逐场预测与冻结整届赛前实力的冠军预测不同。'+LIMIT+'\n'
 write(R/'reports/history/README.md',overview)
 evbody=f'# S4–S15：赛前排名与最终成绩\n\n[返回首页](../../README.md) · [赛制与限制](rules.md) · [模型细节](../../MODEL.md)\n\n**夺冠概率第一命中 {hits}/23 届冠军（{100*hits/23:.2f}%）。** 仅是已收集历史赛事的回顾性表现，不保证未来命中率。S3 不回放，S4 国内数据不足。\n\n平均冠军对数损失 **{np.mean([e["champion_logloss"] for e in eventsummary]):.4f}**，平均冠军 Brier **{np.mean([e["champion_brier"] for e in eventsummary]):.4f}**；二者越低越好。\n'
 evbody+=table(['赛事','实际冠军','冠军赛前概率','预测冠军','命中','预期名次相关性'],[[f'[{e["id"]}]({e["id"]}.md)',e['champion'],pct(e['champion_probability']),e['favorite'],'✓' if e['hit'] else '✗',f'{e["finish_correlation"]:.3f}'] for e in eventsummary])
 regrows=[]
 for c in configs:
  text=(R/f'reports/sensitivity/dynamic90/{c["id"]}.md').read_text();text=text.replace('：动态模型','：赛前预测与实际成绩').replace('[比较总览](../candidate_models.md)', '[全部赛事](README.md)').replace(f'[赛制与主结果](../../event_replay/{c["id"]}.md)','[赛制与限制](rules.md)')
  write(R/f'reports/event_replay/{c["id"]}.md',text)
  eventraw=read(RES/'dynamic90'/f'{c["id"]}.json');ps=[sum(k for lo,hi,k in bins if lo==hi==1)/eventraw['samples'] for bins in eventraw['counts']];reg=region_rankings([dict(name=c['display'][t],region=c['regions'][t],strength=c['strength'][t],title_probability=ps[i]) for i,t in enumerate(c['teams'])]);regrows.append([f'[{c["id"]}]({c["id"]}.md)',order_text(reg)])
 evbody+='## 每届赛前赛区实力顺序\n\n仅比较当届参赛阵容，按战队实力等权平均。\n'+table(['赛事','赛区实力顺序'],regrows)+'## 比较口径\n\n名次按共同淘汰阶段合并；相关系数衡量排序一致性，不是百分比正确率。'+LIMIT+'\n'
 write(R/'reports/event_replay/README.md',evbody)
 rules=R/'reports/event_replay/rules.md';ruletext=rules.read_text()
 for c in configs:
  rr=read(RES/'dynamic90'/f'{c["id"]}.json')
  pattern=r'(### '+str(c['year'])+' '+c['event']+r'\n[\s\S]*?复杂同分处理 )[0-9,]+( 次，抽签豁免 )[0-9,]+( 次。)'
  ruletext=re.sub(pattern,lambda m:m[1]+format(rr['complex_tie_scenarios'],',')+m[2]+format(rr['draw_waivers'],',')+m[3],ruletext)
 write(rules,ruletext)
 root='# LoL Championship Prediction\n\n根据公开赛果，比较 S16 各队晋级与夺冠机会，并回看历史赛事的预测与实际成绩。\n\n## S16：队伍排名与过关概率\n\n数据截至 **2026 年 10 月 14 日**，参考日为 **10 月 19 日**。按夺冠概率排序；各列为从赛事开始算起的累计概率。\n'+table(head,rows)
 root+='赛前赛区实力顺序：**'+order_text(region)+'**，仅代表本届参赛阵容。\n\n[完整结果与队伍资料](reports/s16/README.md) · [两两胜率](reports/s16/matchups-90.md) · [当季已纳入赛果](reports/s16/matches.md)\n\n## 历史预测表现\n'
 root+=f'- 整届冠军预测：**{hits}/23 届（{100*hits/23:.2f}%）**。\n- 逐场系列赛命中率：**{pct(m["series_accuracy"])}**。\n- 小局命中率：**{pct(m["map_accuracy"])}**。\n\n回放范围为 S4–S15 的 MSI、2020 MSC 和 Worlds，合计 {m["covered_series"]:,} 场系列赛、{m["maps"]:,} 小局。整届预测只用开赛前数据；逐场预测只用更早日期数据。这些是两种不同的评价口径。\n\n[整届冠军、排名与实际成绩](reports/event_replay/README.md) · [逐季与逐场回放](reports/history/README.md)\n\n## 数据与限制\n\n'+LIMIT+'\n\n本次补充了阵容、版本、选边和局内统计的核验记录，尚未用于预测，也没有把缺失的比赛当作已经补齐。S3 因赛前数据不足不回放，仅保留[赛果](reports/history/S3/matches.md)。\n\n- [数据补充与覆盖审计](reports/data_enrichment/README.md)\n- [比赛来源与未解决缺口](docs/DATA.md)\n- [模型与算法](MODEL.md)\n- [其他模型及历史对照](reports/sensitivity/candidate_models.md)\n'
 write(R/'README.md',root)
 print('Primary reports published: dynamic90; historical hits',hits,'series accuracy',m['series_accuracy'])
if __name__=='__main__':main()

"""Readable DNN comparisons, including initialization sensitivity and full events."""
import json
import numpy as np
from run_dnn import R,D,MODES
from report_chain_events import evaluate
from report_research_models import diagnostics,KEYS
from report_event_replay import table,band
from region_rankings import region_rankings,section
P=R/'reports/dnn';LABEL={'baseline':'原动态模型','mlp':'纯小型DNN','residual_mlp':'残差DNN'}
def series_metrics(rows,key,seed=None):
 p=np.clip([r['probabilities'][key] if seed is None else r['seed_probabilities'][key][seed] for r in rows],1e-12,1-1e-12);y=np.array([r['wins1']>r['wins2'] for r in rows],float);return dict(n=len(rows),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))
def main():
 cs=json.loads((D/'event_configs.json').read_text());pred=json.loads((D/'predictions.json').read_text());fits=json.loads((D/'fits.json').read_text());events=[]
 for i,c in enumerate(cs['mlp']):
  models={m:evaluate(c if m=='baseline' else cs[m][i],json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json' if m=='baseline' else D/m/f'{c["id"]}.json').read_text())) for m in LABEL};e=dict(id=c['id'],year=c['year'],models=models);events.append(e)
  text=f'# {c["id"]}：神经网络对照\n\n[总览](README.md) · [逐届赛制与近似](../event_replay/rules.md)\n\n开赛截点{c["start_date"]}；每项14,000,605次，模拟种子{c["year"]}。网络小局概率为三个预定训练种子的平均，整届特征冻结。\n\n'
  text+=table(['队伍','实际名次',*[LABEL[m]+'夺冠概率' for m in LABEL],*[LABEL[m]+'预期名次' for m in LABEL]],[[t['name'],band(t['actual_rank']),*[f'{models[m]["teams"][j]["championship_probability"]:.3%}' for m in LABEL],*[f'{models[m]["teams"][j]["expected_rank"]:.3f}' for m in LABEL]] for j,t in enumerate(models['baseline']['teams'])])
  text+='## 赛前赛区比较\n\n网络没有唯一一维实力；实力均值沿用原动态模型输入，不能解释为网络独立估计。各候选的赛区夺冠概率由各自模拟合计。\n\n'
  for m in LABEL:
   text+=f'### {LABEL[m]}\n\n'+section(region_rankings([dict(name=c['display'][t],region=c['regions'][t],strength=c['strength'][t],title_probability=models[m]['teams'][j]['championship_probability']) for j,t in enumerate(c['teams'])]))
  (P/f'{c["id"]}.md').write_text(text.rstrip()+'\n')
 summary={m:{k:float(np.mean([e['models'][m][k] for e in events])) for k in KEYS} for m in LABEL};diag={m:diagnostics(events,m) for m in MODES};series={m:series_metrics(pred,m) for m in LABEL};seeds={m:[series_metrics(pred,m,i) for i in range(3)] for m in MODES};out=dict(summary=summary,diagnostics=diag,series=series,seeds=seeds,events=events);(D/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 text='# 小型DNN与残差DNN：冠军预测回放\n\n两项候选各23届 MSI／MSC／Worlds，每届14,000,605次、模拟种子年份；原模型复用同规模结果。\n\n'
 text+=table(['模型','冠军命中','冠军对数损失 ↓','冠军Brier ↓','名次相关 ↑','名次误差 ↓'],[[LABEL[m],f'{summary[m]["champion_hit"]*23:g}/23',*[f'{summary[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in LABEL])
 text+='**结论：两项DNN均未整体改善冠军预测，保留原动态模型。** 纯DNN的冠军对数损失、命中和名次误差较差，仅Brier改善；残差DNN更接近原模型，名次误差略好，但冠军对数损失、Brier和命中均较差。逐场命中率虽略升，两个模型及各自三个训练种子的逐场概率损失都比原模型大。\n\n这说明本轮没有找到可替换主模型的DNN，不证明神经网络永远无效。国内验证与国际赛事之间的分布差异、特征信息量和有限样本都是待检验因素，不能只凭此次结果认定某一个是原因。\n\n## 怎样比较\n\n纯DNN直接从赛前特征预测小局概率；残差DNN在原动态模型的logit上学习受收缩约束的修正。二者共享相同的12项历史特征和缺失标记，均为两层32／16单元，没有加入本场经济、队名或未来阵容。\n\n每届在赛前国内赛中按日期前80%／后20%选择训练轮数，然后在全部赛前国内赛重训。每项使用三个固定训练种子的概率平均，不选择最好的种子。全赛季历史状态仍按90天更新，网络跨年只学习特征关系。\n\n## 差异与稳定性\n\n候选减原模型，损失负值较好。95%区间按年份聚类；逐届删除仅检查单届影响，不排除冷门。\n'
 text+=table(['候选','指标','平均差','95%年份区间','删除任意一届后的差值范围'],[[LABEL[m],{'champion_logloss':'冠军对数损失','champion_brier':'冠军Brier','finish_mae':'名次误差'}[k],f'{diag[m][k]["delta"]:+.5f}',str([round(v,5) for v in diag[m][k]['year_cluster_95']]),str([round(v,5) for v in diag[m][k]['leave_one_out_range']])] for m in MODES for k in ['champion_logloss','champion_brier','finish_mae']])
 text+='## 逐场概率与随机初始化\n\n共1,300场系列赛。整届结果使用三个种子小局概率的平均；下表单种子只评价逐场系列赛，没有分别运行其整届模拟。三个种子不足以完整刻画训练不确定性。\n'+table(['模型','训练种子组','命中率','对数损失','Brier'],[[LABEL[m],'三种子平均' if m!='baseline' else '原模型',f'{series[m]["accuracy"]:.2%}',f'{series[m]["logloss"]:.5f}',f'{series[m]["brier"]:.5f}'] for m in LABEL]+[[LABEL[m],['年份','年份+10000','年份+20000'][i],f'{v["accuracy"]:.2%}',f'{v["logloss"]:.5f}',f'{v["brier"]:.5f}'] for m in MODES for i,v in enumerate(seeds[m])])
 text+='## 逐届实际冠军概率\n'+table(['赛事','实际冠军',*LABEL.values()],[[f'[{e["id"]}]({e["id"]}.md)',e['models']['baseline']['champion'],*[f'{e["models"][m]["champion_probability"]:.3%}' for m in LABEL]] for e in events])
 text+='## 解释边界\n\n国内赛训练与国际赛评价存在分布差异；早期经济缺失且赛果覆盖不足。相邻小局不是独立的新环境，23届冠军标签也不足以支持大规模架构搜索。本轮历史已经反复研究，年份区间是探索性证据。结果只检验这套特征、架构和训练协议，不代表所有DNN均无法改善。增加模拟次数不能补足训练信息。\n\n沿用已披露的历史赛制近似，整届冻结赛前特征；未加入全局BP、选手能力、当前选边或系列赛共享状态，也未对网络参数作贝叶斯积分。三个初始化的平均不是经过校准的参数后验。\n\n[逐场概率](matches.md) · [训练与验证截点](training.md) · [固定协议](PROTOCOL.md) · [模型细节](../../MODEL.md#小型dnn与残差dnn实验)\n'
 (P/'README.md').write_text(text.rstrip()+'\n')
 text='# DNN逐场系列赛概率\n\n左队获胜概率；仅使用较早日期信息，网络在每届开始前冻结。\n'+table(['日期','赛事','对阵','实际比分',*LABEL.values()],[[r['date'],r['event'],r['team1']+' – '+r['team2'],f'{r["wins1"]}:{r["wins2"]}',*[f'{r["probabilities"][m]:.3%}' for m in LABEL]] for r in pred]);(P/'matches.md').write_text(text.rstrip()+'\n')
 text='# DNN训练与验证截点\n\n全部验证日期早于目标赛事；轮数选择后重新拟合全部赛前国内赛。网络种子偏移不影响赛事模拟种子。\n'+table(['赛事','模型','种子','网络训练最晚日','验证开始','验证最晚日','赛事开始','重训系列赛','重训小局','选中轮数','验证损失'],[[x['id'],LABEL[x['mode']],x['seed'],x['fit_latest'],x['validation_start'],x['validation_latest'],x['cutoff'],x['training_series'],x['training_maps'],x['selected_epochs'],f'{x["validation_loss"]:.5f}'] for x in fits]);(P/'training.md').write_text(text.rstrip()+'\n');print(json.dumps({k:out[k] for k in ['summary','series','seeds']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()

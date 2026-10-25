"""Human-readable paired event metrics and roster metadata feasibility."""
import json
import numpy as np
from run_memory_weights import R,D
from report_chain_events import evaluate
from report_event_replay import table,band
from region_rankings import region_rankings,section
P=R/'reports/memory_weights';LABEL={'baseline':'原动态90天','dual':'长期180天＋短期30天','roster_shock':'阵容变化增加不确定性'}
def main():
 P.mkdir(exist_ok=True);configs=json.loads((D/'event_configs.json').read_text());protocol=json.loads((D/'protocol.json').read_text());pred=json.loads((D/'predictions.json').read_text());changes=json.loads((D/'roster_changes.json').read_text());events=[]
 for i,c in enumerate(configs['dual']):
  models={}
  for mode in LABEL:
   cc=c if mode=='baseline' else configs[mode][i]
   path=R/f'results/model_experiments/dynamic90/{c["id"]}.json' if mode=='baseline' else D/mode/f'{c["id"]}.json'
   models[mode]=evaluate(cc,json.loads(path.read_text()))
  events.append(dict(id=c['id'],year=c['year'],models=models))
  text=f'# {c["id"]}：时间与人员权重\n\n[总览](README.md) · [本届规则与局限](../event_replay/rules.md)\n\n赛前截止：{c["start_date"]}。每个候选14,000,605次，独立种子{c["year"]}；固定赛前实力，保留原逐届规则近似。当天名单只在当天全部预测结束后使用。\n\n'
  text+=table(['队伍','实际名次',*[LABEL[m]+'夺冠概率' for m in LABEL],*[LABEL[m]+'预期名次' for m in LABEL]],[[t['name'],band(t['actual_rank']),*[f'{models[m]["teams"][j]["championship_probability"]:.3%}' for m in LABEL],*[f'{models[m]["teams"][j]["expected_rank"]:.3f}' for m in LABEL]] for j,t in enumerate(models['baseline']['teams'])])
  for mode in ['dual','roster_shock']:
   cc=configs[mode][i];text+=f'\n## {LABEL[mode]}：赛前赛区排名\n\n'+section(region_rankings([dict(name=cc['display'][t],region=cc['regions'][t],strength=cc['strength'][t],title_probability=models[mode]['teams'][j]['championship_probability']) for j,t in enumerate(cc['teams'])]))
  (P/f'{c["id"]}.md').write_text(text)
 keys=['champion_logloss','champion_brier','champion_hit','finish_spearman','finish_mae'];summary={m:{k:float(np.mean([e['models'][m][k] for e in events])) for k in keys} for m in LABEL};series={}
 for m in LABEL:
  p=np.clip([r['probabilities'][m] for r in pred],1e-12,1-1e-12);y=np.array([r['wins1']>r['wins2'] for r in pred],float);series[m]=dict(n=len(p),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))
 years=sorted({e['year'] for e in events});ix=np.random.default_rng(2026).integers(0,len(years),(10000,len(years)));diagnostics={}
 for m in ['dual','roster_shock']:
  diagnostics[m]={}
  for k in keys:
   ds=np.array([e['models'][m][k]-e['models']['baseline'][k] for e in events]);groups=np.array([[sum(ds[i] for i,e in enumerate(events) if e['year']==y),sum(e['year']==y for e in events)] for y in years]);z=groups[ix].sum(axis=1)
   diagnostics[m][k]=dict(mean_delta=float(ds.mean()),year_cluster_95=np.quantile(z[:,0]/z[:,1],[.025,.975]).tolist(),leave_one_out_range=[float(min((sum(ds)-v)/22 for v in ds)),float(max((sum(ds)-v)/22 for v in ds))],better_events=int(sum(ds<0)) if k not in ['champion_hit','finish_spearman'] else int(sum(ds>0)))
 out=dict(summary=summary,series=series,diagnostics=diagnostics,events=events);(D/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 text='# 时间记忆与人员变化：两项独立实验\n\nS4–S15共23届 MSI／MSC／Worlds。两个候选分别运行完整赛事，每届14,000,605次，种子为公历年份，原模型复用已验证相同规模模拟；没有覆盖主模型或S16报告。\n\n'
 text+=table(['模型','冠军命中','冠军对数损失 ↓','冠军 Brier ↓','名次相关 ↑','名次绝对误差 ↓'],[[LABEL[m],f'{summary[m]["champion_hit"]*23:g}/23',*[f'{summary[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in LABEL])
 text+='**结论：两项均不足以整体替换主模型。** 双时间尺度改善逐场概率与部分名次指标，但冠军对数损失略差；人员不确定性改善冠军对数损失与Brier，但冠军命中降至9/23，名次相关略差。差异区间均跨零，正式模型保持不变。\n\n人员方案的冠军对数损失收益对2020 MSC敏感：仅将该届作为影响诊断移除时，其余22届平均差约+0.00094，改善消失。该届仍保留在所有主评价中，不据此重新筛选样本。人员方案在2018 Worlds将首选冠军从实际冠军移开，造成一次命中损失；不能只看总Brier来忽略这一变化。\n\n## 两种假设\n\n**双时间尺度**把队伍实力拆成长期能力与短期状态：长期半衰期180天、短期30天，短期占25%的队伍平稳方差。总队伍方差与原模型相同，赛区记忆与先验仍为90天。参数事先固定，不根据23届表现挑选。\n\n**人员不确定性**保持原90天模型，观察到已核准名单变化时增加队伍状态方差，增加量为0.75²乘以不重合的出场份额；不直接改变均值。当天预测全部完成后，才使用当天实际名单并吸收比分。因此无法提前识别未公布的换人，名单缺失时不推断人员不变。前后观察间隔超过180天不触发；短期替补和真正转会目前不能完全区分。\n\n两项都每季重置队伍实力，仅赛区先验跨季；人员候选跨季只保留名单元数据。这不是此前“继承旧实力并按人员打折”的同一实验。阵容增加的不确定性会影响后续学习速度，但本轮整届模拟仍固定赛前均值，没有额外整届后验抽样。\n\n'
 text+='## 稳定性与单届影响\n\n候选减原模型；误差负值较好。按年份聚类的区间用于描述，只有23届且历史已反复研究，不能视为未来收益保证。删除单届仅作诊断，全部赛事仍在主评价中。\n'
 text+=table(['候选','指标','平均差','95%年份区间','删除任意一届后的平均差范围'],[[LABEL[m],k,f'{diagnostics[m][k]["mean_delta"]:+.5f}',str([round(v,5) for v in diagnostics[m][k]['year_cluster_95']]),str([round(v,5) for v in diagnostics[m][k]['leave_one_out_range']])] for m in diagnostics for k in ['champion_logloss','champion_brier','finish_mae']])
 text+='## 逐届对照\n'+table(['赛事','实际冠军','原冠军概率','双时间尺度','人员不确定性'],[[f'[{e["id"]}]({e["id"]}.md)',e['models']['baseline']['champion'],*[f'{e["models"][m]["champion_probability"]:.3%}' for m in LABEL]] for e in events])
 text+='## 逐场辅助指标\n\n1,300场国际赛系列赛，同日预测后批量更新；不依靠逐场命中率决定冠军模型优劣。\n'+table(['模型','命中率','系列赛对数损失','Brier'],[[LABEL[m],f'{series[m]["accuracy"]:.2%}',f'{series[m]["logloss"]:.5f}',f'{series[m]["brier"]:.5f}'] for m in LABEL])
 text+='## 选手分层模型的数据条件\n\n下表为实际与比分对账的名单。选手名称经过大小写和Unicode规范化，不等于有全球唯一身份ID；同名、改名与跨赛区转会尚不能全部自动确认。多队记录提供一定的能力分离信息，但不能仅凭名单数量保证个人贡献可识别，长期一起上场的五人仍难以区分。\n'
 text+=table(['赛季','对账小局','队伍名单观察日','选手名称数','同季出现于多队的名称数'],[[f'S{x["season"]}',x['matched_maps'],x['lineup_days'],x['named_players'],x['players_multiple_teams']] for x in protocol['coverage']])
 text+='当前只完成数据条件审计，未实现选手能力＋团队配合模型；不把新S16后半季名单倒填历史。需先建立可核准的选手身份与位置映射，再测试个人能力迁移。\n\n## 限制\n\n两候选共享原小局比分，不重复添加系列赛胜负。逐届赛制情景保留历史同分和抽签近似。未建模全局BP、选边、英雄、版本迁移与系列赛共享状态；人员候选仅对观察到的名单变化改变方差，没有估计各位置、选手或协作贡献，也没有模拟未来换人。季中稳定首发缺乏换队对照时，不能从战绩精确分离个人能力。\n\n[模型细节](../../MODEL.md#时间与人员权重实验) · [逐次人员变化](roster_changes.md) · [逐场概率](matches.md)\n'
 (P/'README.md').write_text(text)
 text='# 已观察到的人员连续性变化\n\n当天赛前预测完成后才使用；前后名单为当日实际出场份额，包含替补，不等同于正式转会公告。缺失不填零。\n\n'
 text+=table(['赛季','队伍','前次名单日期','本次观察日期','之前名单份额','当前名单份额','人员留存','新增状态方差'],[[f'S{x["season"]}',x['team'],x['previous_date'],x['observed_date'],', '.join(f'{n} {v:.0%}' for n,v in x['previous_players'].items()),', '.join(f'{n} {v:.0%}' for n,v in x['current_players'].items()),f'{x["retention"]:.2%}',f'{x["added_variance"]:.5f}'] for x in changes]);(P/'roster_changes.md').write_text(text)
 text='# 逐场系列赛概率\n\n各列是左队获胜概率。\n\n'+table(['日期','赛事','对阵','实际比分',*LABEL.values()],[[r['date'],r['event'],r['team1']+' – '+r['team2'],f'{r["wins1"]}:{r["wins2"]}',*[f'{r["probabilities"][m]:.3%}' for m in LABEL]] for r in pred]);(P/'matches.md').write_text(text)
 print(json.dumps(summary,ensure_ascii=False,indent=2));print('series',series)
if __name__=='__main__':main()

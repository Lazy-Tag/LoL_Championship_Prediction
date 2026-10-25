"""Paired reporting and prespecified, strictly prior-year ensemble gates."""
import json
import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr,rankdata
from run_research_models import R,D,N,FEATURES
from report_chain_events import evaluate
from report_event_replay import table,band
from region_rankings import region_rankings,section
P=R/'reports/research_models';LABEL={'baseline':'原动态模型','catboost':'CatBoost非线性','joint_gold':'经济与胜负联合模型','change_point':'在线变化点模型'}
KEYS=['champion_logloss','champion_brier','champion_hit','finish_spearman','finish_mae']
def diagnostics(events,mode,seed=2026):
 years=sorted({e['year'] for e in events});ix=np.random.default_rng(seed).integers(0,len(years),(10000,len(years)));out={}
 for key in KEYS:
  ds=np.array([e['models'][mode][key]-e['models']['baseline'][key] for e in events]);groups=np.array([[sum(ds[i] for i,e in enumerate(events) if e['year']==y),sum(e['year']==y for e in events)] for y in years]);z=groups[ix].sum(axis=1)
  out[key]=dict(delta=float(ds.mean()),year_cluster_95=np.quantile(z[:,0]/z[:,1],[.025,.975]).tolist(),leave_one_out_range=[float(min((sum(ds)-v)/(len(ds)-1) for v in ds)),float(max((sum(ds)-v)/(len(ds)-1) for v in ds))])
 return out

def eligible(events,seed):
 if len(events)<8:return [],{}
 diag={m:diagnostics(events,m,seed) for m in LABEL if m!='baseline'}
 return [m for m,d in diag.items() if d['champion_logloss']['year_cluster_95'][1]<0 and d['champion_brier']['delta']<=0 and d['finish_mae']['delta']<=.01],diag

def gated_ensemble(events):
 out=[];fits={}
 for e in events:
  year=e['year']
  if year not in fits:
   past=[v for v in events if v['year']<year];active,_=eligible(past,year);names=['baseline']+active;weights=np.zeros(len(names));weights[0]=1.
   if active:
    A=np.array([[v['models'][m]['champion_probability'] for m in names] for v in past]);prior=weights.copy()
    def objective(w):return float(-np.log(np.maximum(A@w,1e-12)).sum()+np.sum((w-prior)**2))
    opt=minimize(objective,weights,method='SLSQP',bounds=[(0,1)]*len(names),constraints=[{'type':'eq','fun':lambda w:sum(w)-1}],options={'ftol':1e-12,'maxiter':1000});assert opt.success;weights=opt.x
   fits[year]=dict(year=year,training_events=[p['id'] for p in past],eligible=active,weights=dict(zip(names,map(float,weights))))
  fit=fits[year];teams=e['models']['baseline']['teams'];p=sum(w*np.array([t['championship_probability'] for t in e['models'][m]['teams']]) for m,w in fit['weights'].items());ex=sum(w*np.array([t['expected_rank'] for t in e['models'][m]['teams']]) for m,w in fit['weights'].items());actual=np.array([t['actual_midrank'] for t in teams]);winner=next(i for i,t in enumerate(teams) if t['actual_rank']==[1,1]);hit=int(np.argmax(p))==winner
  out.append(dict(id=e['id'],year=year,weights=fit['weights'],probabilities=p.tolist(),expected_rank=ex.tolist(),champion_logloss=float(-np.log(p[winner])),champion_brier=float(np.sum((p-(np.arange(len(p))==winner))**2)),champion_hit=hit,finish_mae=float(np.mean(abs(ex-actual))),finish_spearman=float(spearmanr(ex,actual).statistic)))
 return dict(fits=list(fits.values()),events=out,aggregate={k:float(np.mean([v[k] for v in out])) for k in KEYS},activated_events=sum(any(m!='baseline' and w>1e-8 for m,w in x['weights'].items()) for x in out))

def main():
 P.mkdir(exist_ok=True);cs=json.loads((D/'event_configs.json').read_text());protocol=json.loads((D/'protocol.json').read_text());pred=json.loads((D/'predictions.json').read_text());events=[]
 for i,c in enumerate(cs['joint_gold']):
  models={}
  for m in LABEL:
   path=R/f'results/model_experiments/dynamic90/{c["id"]}.json' if m=='baseline' else D/m/f'{c["id"]}.json';conf=c if m=='baseline' else cs[m][i];models[m]=evaluate(conf,json.loads(path.read_text()))
  e=dict(id=c['id'],year=c['year'],models=models);events.append(e)
  text=f'# {c["id"]}：三条独立模型路线\n\n[总览](README.md) · [历史赛制与近似](../event_replay/rules.md)\n\n开赛截点：{c["start_date"]}；每个候选14,000,605次、种子{c["year"]}，整届实力与特征冻结。树模型仅在此前国内赛拟合；联合关系参数仅由更早赛季确定。\n\n'
  text+=table(['队伍','实际名次',*[LABEL[m]+'夺冠概率' for m in LABEL],*[LABEL[m]+'预期名次' for m in LABEL]],[[t['name'],band(t['actual_rank']),*[f'{models[m]["teams"][j]["championship_probability"]:.3%}' for m in LABEL],*[f'{models[m]["teams"][j]["expected_rank"]:.3f}' for m in LABEL]] for j,t in enumerate(models['baseline']['teams'])])
  for m in ['joint_gold','change_point','catboost']:
   conf=cs[m][i];text+=f'\n## {LABEL[m]}：赛前赛区比较\n\n'
   if m=='catboost':text+='树模型没有唯一的一维实力排序；这里的实力均值沿用其输入中的原动态实力，夺冠概率列使用树模型，不解释成树模型自行估计的赛区实力。\n\n'
   text+=section(region_rankings([dict(name=conf['display'][t],region=conf['regions'][t],strength=conf['strength'][t],title_probability=models[m]['teams'][j]['championship_probability']) for j,t in enumerate(conf['teams'])]))
  (P/f'{c["id"]}.md').write_text(text.rstrip()+'\n')
 summary={m:{k:float(np.mean([e['models'][m][k] for e in events])) for k in KEYS} for m in LABEL};diag={m:diagnostics(events,m) for m in LABEL if m!='baseline'};series={}
 for m in LABEL:
  p=np.clip([r['probabilities'][m] for r in pred],1e-12,1-1e-12);y=np.array([r['wins1']>r['wins2'] for r in pred],float);series[m]=dict(n=len(pred),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))
 ensemble=gated_ensemble(events);passed,_=eligible(events,2026);result=dict(summary=summary,series=series,diagnostics=diag,events=events,ensemble=ensemble,full_history_gate=passed);(D/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 text='# 三条独立路线：非线性、联合表现与变化点\n\n23届 MSI／MSC／Worlds，各候选每届14,000,605次、种子年份；原模型复用已验证同规模结果。所有候选单独保存，主模型、S16及每日预测不覆盖。\n\n'+table(['模型','冠军命中','冠军对数损失 ↓','冠军 Brier ↓','名次相关 ↑','名次绝对误差 ↓'],[[LABEL[m],f'{summary[m]["champion_hit"]*23:g}/23',*[f'{summary[m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in LABEL])
 text+='**结论：保留原动态模型。** 变化点模型最值得继续验证：冠军对数损失、Brier和名次误差的平均值均改善，但冠军命中从10届降到8届，冠军概率指标的差异区间仍跨零。经济联合模型只呈现混合改善；CatBoost在本轮明显退步。严格前推组合也未带来一致改善，目前没有候选通过完整历史的组合准入门槛。\n\n'
 text+='## 三项各自改变什么\n\n- **CatBoost**：浅层树学习赛前实力、历史结果残差、15分钟经济、样本量和休赛间隔的非线性关系；不输入队名，不使用本场实际统计。300棵、深度4等参数固定，没有按目标赛事早停调参。模型在每届开始前的全部既有国内赛拟合，目标赛事期间只更新赛前历史特征，不再拟合树。\n- **联合表现**：先描述实力如何产生15分钟经济，再描述经济和实力如何共同影响胜负。只增加一种统计，没有实现完整SIDO或多维选手表现。缺经济时积分，不把它填零，也不把相关的胜负与经济当两份独立胜负证据。\n- **在线变化点**：16个高斯粒子表示不同的实力延续／重置历史；每个粒子对当天比分学习一次，以近似证据更新权重。队伍残差可以重置，赛区状态继续保留。它是粒子近似，不是完整精确BOCPD；未加入选手、版本或额外整届状态噪声。\n\n三者使用原全年赛果，不新增或重复胜负。联合与变化点仍每季重置队伍，赛区先验保持原90天；树模型只跨年学习特征关系，不继承队名实力。\n\n## 差异与稳定性\n\n候选减原模型；损失负值较好。按年份聚类，逐届删除只作影响诊断，不挑选或剔除冷门。\n'+table(['候选','指标','平均差','95%年份区间','删除任意一届后的平均差范围'],[[LABEL[m],k,f'{diag[m][k]["delta"]:+.5f}',str([round(v,5) for v in diag[m][k]['year_cluster_95']]),str([round(v,5) for v in diag[m][k]['leave_one_out_range']])] for m in diag for k in ['champion_logloss','champion_brier','finish_mae']])
 text+='## 是否进入组合\n\n门槛在查看本轮整届比较前固定：至少8届较早赛事、冠军对数损失差的95%年份区间上端小于0、Brier不劣、名次误差恶化不超过0.01。每个历史年份只检查更早年份，未通过时完全使用原模型。通过时仅用此前样本外冠军概率拟合受约束权重；不从目标届学习。\n\n'
 text+=f'历史前推组合实际启用新模型的赛事为 **{ensemble["activated_events"]}/23**；以完整历史供未来研究检查，过门槛候选为 **{", ".join(LABEL[m] for m in passed) or "无"}**。\n\n'
 text+=table(['预测年份','可用较早届数','允许进入的候选','冻结权重'],[[f['year'],len(f['training_events']),', '.join(LABEL[m] for m in f['eligible']) or '无',', '.join(f'{LABEL[m]} {w:.1%}' for m,w in f['weights'].items())] for f in ensemble['fits']])
 if ensemble['activated_events']:
  a=ensemble['aggregate'];text+=table(['组合冠军命中','冠军对数损失','Brier','名次误差'],[[f'{a["champion_hit"]*23:g}/23',f'{a["champion_logloss"]:.5f}',f'{a["champion_brier"]:.5f}',f'{a["finish_mae"]:.5f}']])
 text+='组合是整届预测分布的加权，复用各模型的完整模拟边缘分布，未重新抽样；不是把每场胜率混合后再次模拟。门槛与区间均属探索性研究规则，不提供正式多重检验保证。\n\n## 逐届冠军概率\n'+table(['赛事','实际冠军',*[LABEL[m] for m in LABEL]],[[f'[{e["id"]}]({e["id"]}.md)',e['models']['baseline']['champion'],*[f'{e["models"][m]["champion_probability"]:.3%}' for m in LABEL]] for e in events])
 text+='## 逐场辅助评价\n'+table(['模型','系列赛数','命中率','对数损失','Brier'],[[LABEL[m],series[m]['n'],f'{series[m]["accuracy"]:.2%}',f'{series[m]["logloss"]:.5f}',f'{series[m]["brier"]:.5f}'] for m in LABEL])
 text+='## 经济观测覆盖\n\n仅15分钟经济差可用的小局提供额外观测；其余结果仍完整保留。来源异常超过正负30千金币的值不进入本轮经济观测。\n'+table(['赛季','训练小局','有效经济小局','其中国内赛','联合参数来自较早赛季'],[[f'S{x["season"]}',x['training_maps'],x['gold_maps'],x['domestic_gold_maps'],'是'] for x in protocol['coverage']])
 text+='## 解释边界\n\n本轮没有按结果重新挑参数，没有把高命中率当作概率准确。历史已反复探索，真正的新检验应来自冻结模型后的未来赛事。树模型在国内赛训练、国际赛评价，存在赛区迁移与分布差异；联合关系参数用原模型的赛前实力作代理，未联合积分其估计误差；变化点仅16粒子，可能遗漏罕见变化路径，Laplace证据亦为近似。\n\n历史赛制的同分、抽签与选择策略近似保留。树模型两两概率可能不具一维可排序结构，原引擎的对手选择在新矩阵下仍是既定情景，不是现实教练决策的唯一模型。没有加入全局BP、未来首发或赛季中人员能力；整届冻结均值和特征，未模拟未来阵容变化。\n\n[固定协议](PROTOCOL.md) · [模型与复算](../../MODEL.md#非线性联合表现与变化点实验) · [逐场概率](matches.md) · [训练与覆盖诊断](diagnostics.md)\n'
 (P/'README.md').write_text(text.rstrip()+'\n')
 text='# 三项模型逐场系列赛概率\n\n左队获胜概率；所有历史特征在当天所有结果更新之前保存。\n\n'+table(['日期','赛事','对阵','实际比分',*LABEL.values()],[[r['date'],r['event'],r['team1']+' – '+r['team2'],f'{r["wins1"]}:{r["wins2"]}',*[f'{r["probabilities"][m]:.3%}' for m in LABEL]] for r in pred]);(P/'matches.md').write_text(text.rstrip()+'\n')
 params=json.loads((D/'joint_parameters.json').read_text());fits=json.loads((D/'tree_fits.json').read_text());audit=json.loads((D/'change_audit.json').read_text())
 text='# 训练与覆盖诊断\n\n[结果总览](README.md)\n\n## 联合关系参数\n\n经济单位为千金币；a为实力对胜负的直接系数，c为经济系数，k为实力对经济的系数，b为选边经济偏移，σ为经济残差标准差。样本不足时回退原模型，不把默认参数当成已估计结果。\n'+table(['赛季','较早国内小局数','最晚训练日期','a','c','k','b','σ'],[[f'S{x["season"]}',x['parameters']['n'],x['parameters'].get('latest_date','无'),*[f'{x["parameters"][k]:.4f}' for k in ['a','c','k','b','sigma']]] for x in params])
 text+='## 树模型训练截点\n'+table(['赛事','预测截点','最晚训练日期','国内系列赛','国内小局'],[[x['id'],x['cutoff'],x['latest_training_date'],x['training_series'],x['training_maps']] for x in fits])
 text+='## 变化点近似诊断\n\n有效粒子数越低表示权重越集中；16粒子仍可能遗漏变化路径。重置概率是模型后验，不能当成已证实的人员或状态变化。\n'
 rows=[]
 for season in range(4,16):
  xs=[x for x in audit if x['season']==season];ess=[x['effective_particles'] for x in xs];ps=[v for x in xs for v in x['reset_probabilities'].values()]
  rows.append([f'S{season}',len(xs),f'{np.mean(ess):.2f}',f'{min(ess):.2f}',f'{np.mean(ps):.2%}'])
 text+=table(['赛季','更新日数','平均有效粒子数','最低有效粒子数','平均后验重置概率'],rows)
 (P/'diagnostics.md').write_text(text.rstrip()+'\n')
 print(json.dumps(summary,ensure_ascii=False,indent=2));print('gates',passed,'historical activated',ensemble['activated_events']);print('series',series)
if __name__=='__main__':main()

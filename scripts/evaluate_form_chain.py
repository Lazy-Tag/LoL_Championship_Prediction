"""Season-local pre-day tests: extra form and latent shared series performance.
No detail covariates. Map order is used only for live-prediction evaluation.
90-day memory; fixed form shrinkage=5 series; coefficients N(0,1).
Shared-q beta-binomial rho is estimated only on prior domestic series, with
half-normal SD .15 penalty and 0<=rho<=.5; rho=0 explicitly allowed.
"""
import json,math,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit,logit,betaln,gammaln
from scipy.optimize import minimize,minimize_scalar
from backtest import load_season,affiliations,prior_regions,domestic_region
from candidate_models import DynamicBT
from model import series_probability
from evaluate_detail_features import reconcile
R=Path(__file__).resolve().parents[1];OUT=R/'results/form_chain_experiment';REP=R/'reports/form_chain'
FIELDS=['dynamic90','form90','shared_series90','combined90']

def conditional_series(p,rho,best_of,w=0,l=0):
 target=best_of//2+1
 if w>=target:return 1.
 if l>=target:return 0.
 a=target-w;b=target-l
 if rho<1e-7:
  return float(sum(math.comb(a-1+k,k)*p**a*(1-p)**k for k in range(b)))
 kappa=1/rho-1;aa=p*kappa+w;bb=(1-p)*kappa+l
 return float(sum(math.comb(a-1+k,k)*np.exp(betaln(aa+a,bb+k)-betaln(aa,bb)) for k in range(b)))

def next_probability(p,rho,w,l):
 if rho<1e-7:return p
 k=1/rho-1
 return float((k*p+w)/(k+w+l))

def fit_form(records,day):
 if not records:return 0.
 w=np.exp2(-np.array([(day-r[0]).days for r in records])/90);assert all(r[0]<day for r in records)
 d=np.array([r[1] for r in records]);x=np.array([r[2] for r in records]);a=np.array([r[3] for r in records]);n=a+np.array([r[4] for r in records])
 def obj(z):
  eta=d+z[0]*x
  return float(np.sum(w*(n*np.logaddexp(0,eta)-a*eta))+.5*z[0]**2),np.array([np.sum(w*(n*expit(eta)-a)*x)+z[0]])
 fit=minimize(obj,[0.],jac=True,method='BFGS',options={'gtol':1e-6});assert abs(obj(fit.x)[1][0])<1e-4
 return float(fit.x[0])

def fit_rho(records,day,form=False):
 rr=[r for r in records if r[3]+r[4]>=2]
 if not rr:return 0.
 assert all(r[0]<day for r in rr)
 weights=np.exp2(-np.array([(day-r[0]).days for r in rr])/90)
 p=np.clip(np.array([r[5] if form else expit(r[1]) for r in rr]),1e-8,1-1e-8)
 a=np.array([r[3] for r in rr]);b=np.array([r[4] for r in rr])
 def obj(rho):
  if rho<1e-7:ll=a*np.log(p)+b*np.log1p(-p)
  else:
   k=1/rho-1;ll=betaln(k*p+a,k*(1-p)+b)-betaln(k*p,k*(1-p))
  return float(-np.sum(weights*ll)+.5*(rho/.15)**2)
 fit=minimize_scalar(obj,bounds=(1e-6,.5),method='bounded',options={'xatol':1e-6})
 # Optimize a small fixed grid too; no assumed global convexity.
 candidates=[0.,.5,float(fit.x),*.05*np.arange(1,10)]
 return float(min(candidates,key=obj))

def binary_metrics(rows,key,label='y'):
 if not rows:return dict(n=0,accuracy=None,logloss=None,brier=None)
 p=np.clip(np.array([r[key] for r in rows]),1e-12,1-1e-12);y=np.array([r[label] for r in rows]);tie=np.abs(p-.5)<1e-12
 return dict(n=len(rows),accuracy=float(np.mean(np.where(tie,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))

def ordered_games(mm,r):
 if not mm:return None
 try:
  nums=[int(float(g['game'])) for g in mm]
 except (ValueError,TypeError):return None
 if sorted(nums)!=list(range(1,len(mm)+1)):return None
 games=sorted(mm,key=lambda g:int(float(g['game'])))
 # Explicit source map index plus monotone unique timestamps, never lexical ID.
 ts=[g['date'] for g in games]
 if len(set(ts))!=len(ts) or ts!=sorted(ts):return None
 wins=[g['teams']['blue']['win'] if g['a']==r['team1'] else g['teams']['red']['win'] for g in games]
 target=r['best_of']//2+1;w=l=0
 for i,y in enumerate(wins):
  if w>=target or l>=target:return None
  w+=y;l+=1-y
 if (w,l)!=(r['wins1'],r['wins2']) or max(w,l)!=target:return None
 return wins

def main():
 OUT.mkdir(exist_ok=True);REP.mkdir(exist_ok=True);old=json.loads((R/'results/model_experiments/predictions.json').read_text())
 seasons={};regions={};pred=[];live=[];coeff=[];coverage=[]
 mainhash=hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 for s in range(3,16):
  seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
  if s>3:
   for t,v in regions[s-1].items():regions[s].setdefault(t,v)
 for s in range(4,16):
  rows=seasons[s];matched,_=reconcile(s,rows);teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regions[s-1],90)
  dyn=DynamicBT(teams,regions[s],prior);state=defaultdict(lambda:np.zeros(2));byday=defaultdict(list);targets=defaultdict(list);records=[];last=None;beta=0.;nordered=0;nlong=0
  for r in rows:byday[r['date']].append(r)
  for r in old:
   if r['season']==s:targets[r['date']].append(r)
  for ds in sorted(set(byday)|set(targets)):
   day=date.fromisoformat(ds);dyn.advance(day);theta=dyn.strengths()
   if last is not None:
    decay=2**(-(day-last).days/90)
    for z in state.values():z*=decay
   last=day
   def feature(a,b):return state[a][0]/(5+state[a][1])-state[b][0]/(5+state[b][1])
   # Fit every match date to preserve genuinely prequential training offsets.
   beta=fit_form(records,day)
   if targets[ds]:
    rho=fit_rho(records,day);rhof=fit_rho(records,day,True)
    coeff.append(dict(season=s,date=ds,form_beta=beta,rho=rho,rho_combined=rhof,prior_domestic_series=len(records)))
    for r in targets[ds]:
     a,b=r['team1'],r['team2'];d=theta[a]-theta[b];p=float(expit(d));pf=float(expit(d+beta*feature(a,b)))
     assert abs(p-r['dynamic90'])<1e-9
     qs=dict(dynamic90=conditional_series(p,0,r['best_of']),form90=conditional_series(pf,0,r['best_of']),shared_series90=conditional_series(p,rho,r['best_of']),combined90=conditional_series(pf,rhof,r['best_of']))
     pred.append({**r,**qs,'baseline_map_probability':p,'form_map_probability':pf,'rho':rho,'rho_combined':rhof,'form_feature':float(feature(a,b)),'form_beta':beta,'y':int(r['wins1']>r['wins2'])})
     if r['best_of']<=1:continue
     nlong+=1;wins=ordered_games(matched.get(r['detail']),r)
     if wins is None:continue
     nordered+=1;w=l=0
     for k,y in enumerate(wins):
      if k:
       nexts=dict(dynamic90=p,form90=pf,shared_series90=next_probability(p,rho,w,l),combined90=next_probability(pf,rhof,w,l))
       remain=dict(dynamic90=conditional_series(p,0,r['best_of'],w,l),form90=conditional_series(pf,0,r['best_of'],w,l),shared_series90=conditional_series(p,rho,r['best_of'],w,l),combined90=conditional_series(pf,rhof,r['best_of'],w,l))
       live.append(dict(season=s,event=r['event'],date=ds,detail=r['detail'],team1=r['display1'],team2=r['display2'],best_of=r['best_of'],next_map=k+1,wins_before=w,losses_before=l,y=int(y),series_y=int(r['wins1']>r['wins2']),**nexts,series_remaining=remain))
      w+=y;l+=1-y
   updates=[];new=[]
   for r in byday[ds]:
    a,b=r['team1'],r['team2'];d=theta[a]-theta[b];p=float(expit(d));x=feature(a,b);n=r['wins1']+r['wins2'];res=r['wins1']/n-p
    updates.append((a,b,res))
    if domestic_region(r['tournament']) is not None:new.append((day,d,x,r['wins1'],r['wins2'],float(expit(d+beta*x))))
   dyn.update(byday[ds]);records.extend(new)
   for a,b,res in updates:state[a]+=np.array([res,1.]);state[b]+=np.array([-res,1.])
  coverage.append(dict(season=s,target_long_series=nlong,ordered_series=nordered));print('S',s,'ordered',nordered,'/',nlong,'done',flush=True)
 summary=dict(prematch={f:binary_metrics(pred,f) for f in FIELDS},live_next_map={f:binary_metrics(live,f) for f in FIELDS},after_first_next_map={f:binary_metrics([r for r in live if r['next_map']==2],f) for f in FIELDS},live_remaining_series={f:binary_metrics([{**r,**r['series_remaining']} for r in live],f,'series_y') for f in FIELDS},by_season=[dict(season=s,models={f:binary_metrics([r for r in pred if r['season']==s],f) for f in FIELDS}) for s in range(4,16)],coverage=coverage)
 # Paired event bootstrap respects within-event repeated forecasts.
 rng=np.random.default_rng(2026);intervals={}
 for label,rows in [('prematch',pred),('live_next_map',live)]:
  keys=sorted({(r['season'],r['event']) for r in rows});indices=rng.integers(0,len(keys),(10000,len(keys)));intervals[label]={}
  for f in FIELDS[1:]:
   vals=[]
   for key in keys:
    rr=[r for r in rows if (r['season'],r['event'])==key];ds=[]
    for r in rr:
     ll=[]
     for field in ['dynamic90',f]:
      p=np.clip(r[field],1e-12,1-1e-12);ll.append(-np.log(p if r['y'] else 1-p))
     ds.append(ll[1]-ll[0])
    vals.append([sum(ds),len(ds)])
   draw=np.array(vals)[indices].sum(axis=1);intervals[label][f]=np.quantile(draw[:,0]/draw[:,1],[.025,.975]).tolist()
 summary['event_bootstrap_logloss_delta_95']=intervals
 assert len(pred)==1300 and mainhash==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 summary['main_pointer_sha256']=mainhash
 for name,v in [('summary',summary),('predictions',pred),('live_predictions',live),('coefficients',coeff)]: (OUT/f'{name}.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 report(summary,pred,live,coeff)
 print(json.dumps({k:summary[k] for k in ['prematch','live_next_map','after_first_next_map']},ensure_ascii=False),flush=True)

def report(summary,pred,live,coeff):
 labels=dict(dynamic90='原动态模型',form90='近期超预期表现',shared_series90='系列赛共享状态',combined90='近期表现＋共享状态')
 text='# 状态延续是否提高预测？\n\n[项目首页](../../README.md)\n\n比较近期状态和系列赛内共享状态，不使用经济、阵容或选边特征；逐局明细仅用于核验已发生小局的先后顺序。主结果和 S16 预测未覆盖。\n\n'
 for name,title in [('prematch','赛前系列赛预测'),('live_next_map','已打完至少一局后的下一局预测'),('after_first_next_map','只看第一局打完后的第二局预测'),('live_remaining_series','已知当前比分后的系列赛预测')]:
  text+=f'## {title}\n\n| 模型 | 预测条数 | 命中率 | 对数损失 ↓ | Brier ↓ |\n| --- | ---: | ---: | ---: | ---: |\n'
  for f,label in labels.items():
   m=summary[name][f];text+=f'| {label} | {m["n"]} | {m["accuracy"]:.2%} | {m["logloss"]:.5f} | {m["brier"]:.5f} |\n'
  text+='\n'
 text+='实时预测只评估有完整且顺序可核验的 BO3／BO5 子集。两种模型使用完全相同的比分信息；原模型也会因为领先而提高剩余系列赛胜率，因此不能把比分优势本身算作状态模型的收益。一场系列赛可能贡献多条实时预测，它们不是独立样本。\n\n## 赛前逐年结果\n\n| 赛季 | 原命中率 | 近期状态 | 共享状态 | 组合 | 原对数损失 | 组合对数损失 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n'
 for a in summary['by_season']:
  v=a['models'];text+=f'| S{a["season"]} | '+' | '.join(f'{v[f]["accuracy"]:.2%}' for f in FIELDS)+f' | {v["dynamic90"]["logloss"]:.5f} | {v["combined90"]["logloss"]:.5f} |\n'
 text+='\n## 稳定性\n\n按赛事整体抽样的配对 bootstrap（10,000次，种子2026），下表为候选减原模型的对数损失差95%区间。负值更好，跨零不能确认稳定差异。已反复查看历史数据，本轮属于探索性比较。\n\n| 评价 | 候选 | 区间 |\n| --- | --- | --- |\n'
 for mode,vals in summary['event_bootstrap_logloss_delta_95'].items():
  for f,ci in vals.items():text+=f'| {"赛前系列赛" if mode=="prematch" else "实时下一局"} | {labels[f]} | [{ci[0]:.5f}, {ci[1]:.5f}] |\n'
 text+='\n## 实时预测的覆盖\n\n| 赛季 | 目标 BO3／BO5 | 完整比分与局序通过 |\n| --- | ---: | ---: |\n'
 for c in summary['coverage']:text+=f'| S{c["season"]} | {c["target_long_series"]} | {c["ordered_series"]} |\n'
 text+='\n[模型与限制](MODEL.md) · [全部赛前预测](prematch.md) · [全部实时预测](live.md)\n'
 (REP/'README.md').write_text(text)
 body='# 逐场赛前预测\n\n[比较结果](README.md)\n\n概率为队伍一赢下系列赛的概率。\n\n| 赛季 | 日期 | 赛事 | 队伍一 | 队伍二 | 比分 | 原模型 | 近期状态 | 共享状态 | 组合 |\n| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |\n'
 for r in pred:body+=f'| S{r["season"]} | {r["date"]} | {r["event"]} | {r["display1"]} | {r["display2"]} | {r["wins1"]}:{r["wins2"]} | '+' | '.join(f'{r[f]:.2%}' for f in FIELDS)+' |\n'
 (REP/'prematch.md').write_text(body)
 body='# 系列赛内实时预测\n\n[比较结果](README.md)\n\n概率指队伍一赢得下一局；所有列都已知当前比分。\n\n| 赛季 | 日期 | 队伍一 | 队伍二 | 下一局 | 已知比分 | 下一局实际胜者 | 原模型 | 近期状态 | 共享状态 | 组合 |\n| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |\n'
 for r in live:body+=f'| S{r["season"]} | {r["date"]} | {r["team1"]} | {r["team2"]} | {r["next_map"]} | {r["wins_before"]}:{r["losses_before"]} | {r["team1"] if r["y"] else r["team2"]} | '+' | '.join(f'{r[f]:.2%}' for f in FIELDS)+' |\n'
 (REP/'live.md').write_text(body)
 (REP/'MODEL.md').write_text('''# 状态延续实验方法\n\n[比较结果](README.md)\n\n原 dynamic90 已会根据此前赛果更新实力，因此“赢了后提高评级”本来就在基线内。额外模型必须证明它提供了基线以外的预测信息，不能重复把同场系列赛胜利当成新样本。\n\n## 近期超预期表现\n\n每个已结束系列赛计算 r=小局获胜比例−赛前原动态单局胜率。每个系列赛贡献一次 r，避免仅因 BO5 局数多而作为更多独立近期状态。队伍状态为90天衰减残差和／(5＋衰减系列赛数)；两队差值乘一个高斯先验 N(0,1) 的修正系数，加到原实力 logit。该系数仅以本赛季此前国内比赛的赛前特征与小局胜负拟合，90天权重；同日先预测，再统一更新。\n\n国内历史 BO2 保留，不能仅凭最终2:0猜成 BO3。因此近期状态以小局比例表达一场系列赛的超预期表现，未单独增加“大场赢一次”的标签。全赛果仍按原方式更新基础实力。90天是既有约定，不声称本轮已经检验7天等更短周期。\n\n## 系列赛内共享状态\n\n对某个系列赛，赛前基准单局胜率为 p，设潜在当场胜率 q~Beta(κp,κ(1−p))，给定 q 时各小局独立。ρ=1/(κ+1) 是边际局间正相关系数；ρ=0 回到固定 p 的基线。该随机状态只属于当前系列赛，不跨系列赛自动继承。\n\n打完 w 胜 l 负后，q 的后验为 Beta(κp+w,κ(1−p)+l)，下一局胜率为 (κp+w)/(κ+w+l)。系列赛胜率对后验分布积分；不是先平均 q 再套 BO 多项式。既知比分的基线也计算剩余路径，所以比较控制了比分领先的天然优势。\n\nρ仅由本赛季此前国内至少两局的系列赛估计：基准 p 使用每场赛前预测，胜负路径概率为 B(κp+w,κ(1−p)+l)/B(κp,κ(1−p))。完成系列赛的停赛路径组合数对ρ不变，拟合时可省略；不加入系列赛胜负作为重复标签。90天加权，固定半正态尺度0.15收缩，ρ范围[0,0.5]，显式允许0。组合候选使用当时已经生成的近期状态赛前概率估计其ρ。所有参数按赛季重置。\n\n该模型只描述可预测的系列赛相关性，不能证明“首胜让士气上升”的因果效应。队伍真实实力估计误差、对位、选边、BP及临场状态都可能表现为相关性；本轮未将它们区分，也不刻画负相关或输家选边。\n\n## 顺序与时间边界\n\n赛前评估 S4–S15 共1300场系列赛，基础胜负输入完全不变。实时子集要求详细数据与同日完整系列赛比分唯一对应、局号恰为1到N、时间戳不重复且顺序一致、符合合法 BO3／BO5 终止路径；不能从最终比分猜首局胜者。只用已经完成的小局更新当前系列赛后验，不能用未来小局反推状态。\n\n实时预测是对过去小局结果的条件预测；未额外训练当日战队基础状态。没有可靠同日跨系列赛时序时，不做“今天早场获胜提高晚场胜率”的实验。日际表现只使用此前日期。经济、阵容、英雄、红蓝方字段均不进入本轮概率模型。\n\n本轮没有重跑整届模拟。赛前冻结实力、系列赛内后验更新、跨系列赛模拟状态传播是三件不同的事；未来若模拟整届，应每个系列赛抽一个共享 q，并在需要时单独定义跨场状态转移，不能将本轮实时改善直接换算成冠军概率改善。\n''')
if __name__=='__main__':main()

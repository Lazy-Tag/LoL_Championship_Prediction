"""Exploratory A2: prequential gold innovations with opponent/side correction.
Fixed before this run: 90-day memory; gold SD=1.5k, noise=3k; at least
5 decayed observations and last observation <=90 days for both teams.
No across-season coefficients or team states. No main-result writes.
"""
import json,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
from candidate_models import design
from dynamic_side_model import DynamicSideBT
from evaluate_detail_features import reconcile
from backtest import load_season,affiliations,prior_regions,domestic_region,metrics
from model import series_probability
R=Path(__file__).resolve().parents[1];OUT=R/'results/economy_residual_experiment';REP=R/'reports/detailed_data'

class EconomyState:
 def __init__(self,teams,regions):
  self.teams=teams;self.ix={t:i for i,t in enumerate(teams)};self.regions=regions;n=len(teams)
  self.m=np.zeros(n);self.C=np.eye(n)*2.25;self.mass=np.zeros(n);self.last={};self.day=None
  # Regression predicts gold (thousands) from pre-day strength difference + blue side.
  self.XX=np.zeros((2,2));self.Xy=np.zeros(2)
 def advance(self,day):
  if self.day is not None:
   age=(day-self.day).days;assert age>=0;rho=2**(-age/90)
   self.m*=rho;self.C*=rho*rho;self.C.flat[::len(self.m)+1]+=2.25*(1-rho*rho)
   self.mass*=rho;self.XX*=rho;self.Xy*=rho
  self.day=day
 def coefficients(self):return np.linalg.solve(self.XX+np.eye(2)*9,self.Xy)
 def feature(self,a,b):
  ia,ib=self.ix[a],self.ix[b]
  ready=all(self.mass[self.ix[t]]>=5 and t in self.last and (self.day-self.last[t]).days<=90 for t in [a,b])
  if not ready:return 0.,False
  # Only within-region deviations: economic data do not set cross-region baselines.
  def centered(t):
   ids=[self.ix[u] for u in self.teams if self.regions.get(u,'UNKNOWN')==self.regions.get(t,'UNKNOWN') and self.mass[self.ix[u]]>=5]
   return self.m[self.ix[t]]-float(np.mean(self.m[ids]))
  return float(centered(a)-centered(b)),True
 def update(self,obs):
  if not obs:return
  coeff=self.coefficients();n=len(self.m);A=np.zeros((len(obs),n));res=[]
  for i,(a,b,d,g,domestic) in enumerate(obs):
   A[i,self.ix[a]]=1;A[i,self.ix[b]]=-1;res.append(g-np.array([d,1.])@coeff)
  active=np.unique(np.nonzero(A)[1]);B=A[:,active];V=self.C[np.ix_(active,active)];Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(active)))
  H=Vi+B.T@B/9;post=cho_solve(cho_factor(H,lower=True),np.eye(len(active)));prior=self.m[active].copy()
  mean=post@(Vi@prior+B.T@np.array(res)/9);K=self.C[:,active]@Vi
  self.m+=K@(mean-prior);self.C-=K@(V-post)@K.T;self.C=(self.C+self.C.T)/2
  for a,b,d,g,domestic in obs:
   for t in [a,b]:self.mass[self.ix[t]]+=1;self.last[t]=self.day
   if domestic:
    x=np.array([d,1.]);self.XX+=np.outer(x,x);self.Xy+=x*g


def fit_beta(records,day):
 if not records:return 0.
 age=np.array([(day-r[0]).days for r in records]);assert np.all(age>0)
 w=2.**(-age/90);off=np.array([r[1] for r in records]);x=np.array([r[2] for r in records]);y=np.array([r[3] for r in records])
 def obj(z):
  beta=z[0];eta=off+beta*x
  return float(np.sum(w*(np.logaddexp(0,eta)-y*eta))+.5*beta*beta),np.array([np.sum(w*(expit(eta)-y)*x)+beta])
 opt=minimize(obj,[0.],jac=True,method='BFGS',options={'gtol':1e-6});assert max(abs(obj(opt.x)[1]))<1e-4
 return float(opt.x[0])

def main():
 OUT.mkdir(exist_ok=True);old=json.loads((R/'results/joint_side_experiment/predictions.json').read_text());seasons={};regs={};pred=[];coef=[];audits=[]
 mainhash=hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 for s in range(3,16):
  seasons[s],_=load_season(s);regs[s]=affiliations(seasons[s],s)
  if s>3:
   for t,v in regs[s-1].items():regs[s].setdefault(t,v)
 for s in range(4,16):
  rows=seasons[s];matched,_=reconcile(s,rows);teams=sorted({r[k] for r in rows for k in ['team1','team2']});pr,_=prior_regions(seasons[s-1],regs[s-1],90)
  side=DynamicSideBT(teams,regs[s],pr);econ=EconomyState(teams,regs[s]);byday=defaultdict(list);targets=defaultdict(list);train=[];econ_count=0
  for r in rows:byday[r['date']].append(r)
  for r in old:
   if r['season']==s:targets[r['date']].append(r)
  for ds in sorted(set(byday)|set(targets)):
   day=date.fromisoformat(ds);side.advance(day);econ.advance(day);theta=side.strengths();bside=float(side.m[-1])
   if targets[ds]:
    beta=fit_beta(train,day);coef.append(dict(season=s,date=ds,beta=beta,gold_expectation_coefficients=econ.coefficients().tolist(),prior_training_maps=len(train)))
    for r in targets[ds]:
     a,b=r['team1'],r['team2'];x,ready=econ.feature(a,b);d=theta[a]-theta[b]
     assert abs(side.predict(a,b)-r['joint_side90'])<1e-9
     p=float((expit(d+beta*x+bside)+expit(d+beta*x-bside))/2)
     pred.append({**r,'economy_residual90':p,'economy_ready':ready,'economy_feature':x,'economy_beta':beta,'economy_weight1':float(econ.mass[econ.ix[a]]),'economy_weight2':float(econ.mass[econ.ix[b]]),'economy_last1':str(econ.last[a]) if a in econ.last else None,'economy_last2':str(econ.last[b]) if b in econ.last else None})
   rr=[];obs=[];newtrain=[]
   for r in byday[ds]:
    gg=matched.get(r['detail'])
    if not gg:rr.append({**r,'side1':0});continue
    dom=domestic_region(r['tournament']) is not None
    for g in gg:
     a,b=g['a'],g['b'];blue,red=g['teams']['blue'],g['teams']['red'];d=theta[a]-theta[b];x,ready=econ.feature(a,b)
     if dom:newtrain.append((day,d+bside,x,blue['win']))
     ga,gb=blue['stats']['goldat15'],red['stats']['goldat15']
     if ga is not None and gb is not None:
      obs.append((a,b,d,(ga-gb)/1000,dom));econ_count+=1
     rr.append(dict(date=ds,team1=a,team2=b,wins1=blue['win'],wins2=red['win'],side1=1))
   assert sum(r['wins1']+r['wins2'] for r in rr)==sum(r['wins1']+r['wins2'] for r in byday[ds])
   side.update(rr);econ.update(obs);train.extend(newtrain)
  audits.append(dict(season=s,economy_maps=econ_count));print('S',s,'economy maps',econ_count,'done',flush=True)
 fields=['dynamic90','joint_side90','economy_residual90'];sets={'all':pred,'economy_ready':[r for r in pred if r['economy_ready']]}
 summary=dict(parameters=dict(half_life_days=90,economy_state_sd_thousand_gold=1.5,observation_sd_thousand_gold=3,minimum_decayed_maps=5,maximum_age_days=90,regression_prior_precision=1),aggregate={name:{f:metrics(rr,f) for f in fields} for name,rr in sets.items()},by_season=[dict(season=s,models={f:metrics([r for r in pred if r['season']==s],f) for f in fields}) for s in range(4,16)],audit=audits)
 groups=defaultdict(list)
 for r in pred:
  yy=r['wins1']>r['wins2'];ll=[]
  for f in fields:
   p=np.clip(series_probability(r[f],r['best_of']),1e-12,1-1e-12);ll.append(-np.log(p if yy else 1-p))
  groups[(r['season'],r['event'])].append([ll[2]-ll[0],ll[2]-ll[1]])
 values=np.array([[*np.sum(v,axis=0),len(v)] for k,v in sorted(groups.items())]);rng=np.random.default_rng(2026);ix=rng.integers(0,len(values),(10000,len(values)));draw=values[ix].sum(axis=1)
 summary['paired_event_logloss_delta_95']={f:np.quantile(draw[:,i]/draw[:,2],[.025,.975]).tolist() for i,f in enumerate(fields[:2])}
 assert mainhash==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 for name,v in [('summary',summary),('predictions',pred),('coefficients',coef)]: (OUT/f'{name}.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 report(summary,pred)
 print(json.dumps(summary['aggregate'],ensure_ascii=False),flush=True)

def report(summary,pred):
 labels={'dynamic90':'原动态','joint_side90':'联合选边校正','economy_residual90':'选边＋经济残差'}
 text='# 对手校正经济残差：回测结果\n\n[数据总览](README.md) · [选边实验](joint_side_comparison.md)\n\n本轮测试额外经济信号：以当日赛前实力差与蓝方项预测经济，再用历史经济残差估计队伍状态。没有改变主模型及 S16 结果。\n\n'
 for name,title in [('all','全部国际赛系列赛'),('economy_ready','满足双方经济可靠性门槛的共同子集')]:
  text+=f'## {title}\n\n| 模型 | 场次 | 命中率 | 系列赛对数损失 ↓ | Brier ↓ | 小局对数损失 ↓ |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
  for f,label in labels.items():
   m=summary['aggregate'][name][f];text+=f'| {label} | {m["covered_series"]} | {m["series_accuracy"]:.2%} | {m["series_logloss"]:.5f} | {m["series_brier"]:.5f} | {m["map_logloss"]:.5f} |\n'
  text+='\n'
 text+='## 逐年结果\n\n| 赛季 | 原命中率 | 选边命中率 | 加经济命中率 | 原对数损失 | 加经济对数损失 |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
 for a in summary['by_season']:
  v=a['models'];text+=f'| S{a["season"]} | '+ ' | '.join(f'{v[f]["series_accuracy"]:.2%}' for f in labels)+f' | {v["dynamic90"]["series_logloss"]:.5f} | {v["economy_residual90"]["series_logloss"]:.5f} |\n'
 text+='\n## 稳定性\n\n按23届赛事的配对簇 bootstrap（10,000次，种子2026），经济候选减对照的系列赛对数损失差95%区间：\n\n'
 for f,ci in summary['paired_event_logloss_delta_95'].items():text+=f'- 相对{labels[f]}：[{ci[0]:.5f}, {ci[1]:.5f}]。\n'
 text+='\n负值更好，跨零表示不能确认稳定差异。此为观察过同一批历史赛事后的探索性回测，不能视为新的独立验证；不因单年上涨替换主模型。\n\n## 本轮固定的方法\n\n经济以千金币为单位。预期回归仅使用此前当季国内已对账数据，输入为当时的赛前选边校正实力差和蓝方截距，90天衰减、单位标准正态系数先验与3千金币观测噪声。每条残差使用其当日赛前参数，不用后来拟合结果重写。\n\n残差采用队伍差分的高斯动态状态，初始及平稳标准差1.5千金币，观测标准差3千金币，90天 AR(1) 记忆。历史国际赛的经济可在后续日期更新状态；预测修正系数仅从此前国内赛的赛前特征和胜负拟合，系数标准正态先验、90天权重。\n\n每队残差状态扣除同赛区达到覆盖门槛队伍的平均值，仅作为赛区内相对表现的候选修正，不重估跨赛区基准；这是一项约束假设，不能保证跨赛区迁移。双方衰减有效权重和均至少5、最近观测均不超过90天才启用修正。缺失不填零，无经济的比赛继续更新原胜负实力。\n\n本轮没有按国际赛结果搜索参数，没有加入其他经济、击杀或地图资源指标。先预测当日全部比赛，再更新回归和状态。残差与胜负之间仍非完整联合生成模型；观测噪声固定、联赛及版本尺度不同、门槛及赛区中心变化、缺失偏差仍是限制。选边与系列赛沿用上一轮近似，不模拟实际未来选边。\n\n## 逐场明细\n\n'
 directory=REP/'economy_residual';directory.mkdir(exist_ok=True)
 for s in range(4,16):
  text+=f'- [S{s}](economy_residual/S{s}.md)\n';body=f'# S{s} 经济残差逐场比较\n\n[比较总览](../economy_residual_comparison.md)\n\n胜率为队伍一赢下系列赛的概率。\n\n| 日期 | 赛事 | 队伍一 | 队伍二 | 比分 | 原胜率 | 选边胜率 | 加经济胜率 | 经济门槛通过 |\n| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |\n'
  for r in pred:
   if r['season']!=s:continue
   pp=[f'{series_probability(r[f],r["best_of"]):.2%}' for f in labels]
   body+=f'| {r["date"]} | {r["event"]} | {r["display1"]} | {r["display2"]} | {r["wins1"]}:{r["wins2"]} | '+' | '.join(pp)+f' | {"是" if r["economy_ready"] else "否"} |\n'
  (directory/f'S{s}.md').write_text(body)
 (REP/'economy_residual_comparison.md').write_text(text)
if __name__=='__main__':main()

"""Year-forward event-level targets; no match outcomes used as fitting labels.
Direct ranking is an unordered-block PL likelihood, not pairwise pseudo-likelihood.
"""
import hashlib,json,math
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.integrate import quad_vec
from scipy.optimize import minimize_scalar
from scipy.special import softmax
from scipy.stats import spearmanr
from report_chain_events import evaluate
from report_event_replay import common_band,table,band
R=Path(__file__).resolve().parents[1];OUT=R/'results/event_targets';REP=R/'reports/event_targets'
NAMES={'baseline':'原动态赛制模拟','rank_pl':'直接整届名次','champion_softmax':'直接冠军模型','calibrated':'原冠军概率校准','mixture':'原模型与名次模型等权组合'}
@lru_cache(None)
def layers(m):
 masks=np.arange(1<<m);return [(masks[np.array([int(k).bit_count() for k in masks])==i]) for i in range(m+1)]

def block_logprob(w,ids):
 """Probability that this unordered set occupies the next |ids| positions."""
 ids=np.asarray(ids);v=w[ids];m=len(v)
 if m==len(w):return 0.
 masks=np.arange(1<<m);bits=(masks[:,None]>>np.arange(m))&1
 sums=bits@v;dp=np.zeros(1<<m);dp[0]=1.;total=w.sum()
 for layer in layers(m)[:-1]:
  for j in range(m):
   src=layer[(layer&(1<<j))==0];dst=src|(1<<j)
   dp[dst]+=dp[src]*v[j]/(total-sums[src])
 return math.log(max(dp[-1],1e-300))

def ranking_loss(e,alpha):
 w=np.exp(alpha*(e['x']-max(e['x'])));left=list(range(len(w)));loss=0.
 for group in e['groups'][:-1]:
  ids=[left.index(i) for i in group];loss-=block_logprob(w[left],ids);left=[i for i in left if i not in group]
 return loss/(len(w)-1)

def fit(earlier,mode):
 if len(earlier)<4:return dict(alpha=1.,events=len(earlier),fit=False,boundary=False)
 # Fixed Gaussian regularization on alpha, SD=1, shared across objectives.
 def objective(a):
  vals=[]
  for e in earlier:
   if mode=='rank_pl':v=ranking_loss(e,a)
   else:
    x=e['x'] if mode=='champion_softmax' else np.log(np.maximum(e['p0'],1e-12))
    logits=a*(x-max(x));v=float(np.log(np.exp(logits).sum())-logits[e['winner']])
   vals.append(v)
  return float(sum(vals)+.5*(a-1)**2)
 # Scan whole bounded interval and refine every observed local basin.
 grid=np.linspace(.1,5,41);ys=[objective(a) for a in grid];candidates=[(ys[0],grid[0]),(ys[-1],grid[-1])]
 for i in range(1,len(grid)-1):
  if ys[i]<=ys[i-1] and ys[i]<=ys[i+1]:
   opt=minimize_scalar(objective,bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-7});candidates.append((float(opt.fun),float(opt.x)))
 value,a=min(candidates)
 return dict(alpha=a,objective=value,events=len(earlier),fit=True,boundary=abs(a-.1)<1e-5 or abs(a-5)<1e-5)

def rank_marginals(x,alpha):
 """PL rank probabilities via exponential-race 1D numerical quadrature."""
 w=np.exp(alpha*(np.asarray(x)-max(x)));n=len(w);out=[];errors=[]
 for i in range(n):
  ratio=np.delete(w,i)/w[i]
  def f(s):
   t=np.exp(s);q=-np.expm1(-t*ratio);p=np.zeros(n);p[0]=1
   for v in q:p=p*(1-v)+np.r_[0,p[:-1]]*v
   return p*np.exp(s-t)
  value,error=quad_vec(f,-35,5,epsabs=1e-10,epsrel=1e-9);out.append(value);errors.append(float(error))
 a=np.array(out)
 assert np.max(abs(a.sum(axis=0)-1))<1e-7 and np.max(abs(a.sum(axis=1)-1))<1e-7
 assert np.max(abs(a[:,0]-softmax(alpha*np.asarray(x))))<1e-7
 return a,max(errors)

def load_events():
 cs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];events=[]
 for c in sorted(cs,key=lambda c:(c['year'],c['start_date'])):
  raw=json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json').read_text());base=evaluate(c,raw);ts=base['teams'];n=len(ts)
  groups={}
  for i,t in enumerate(ts):groups.setdefault(tuple(t['actual_rank']),[]).append(i)
  bands=sorted(groups);assert sum(len(groups[b]) for b in bands)==n
  # Only the rank-band layout is used for forecast coarsening, not team labels.
  mid=np.zeros(n)
  for lo,hi in bands:mid[lo-1:hi]=(lo+hi)/2
  assert np.all(mid>0)
  a0=np.zeros((n,n))
  for i,bins in enumerate(raw['counts']):
   for lo,hi,k in bins:
    lo,hi=common_band(c,lo,hi);a0[i,lo-1:hi]+=k/raw['samples']/(hi-lo+1)
  assert np.max(abs(a0@mid-np.array([t['expected_rank'] for t in ts])))<1e-7
  events.append(dict(id=c['id'],year=c['year'],start_date=c['start_date'],config=c,teams=ts,base=base,x=np.array([c['strength'][t] for t in c['teams']]),p0=np.array([t['championship_probability'] for t in ts]),r0=a0,mid=mid,groups=[groups[b] for b in bands],winner=next(i for i,t in enumerate(ts) if t['actual_rank']==[1,1])))
 return events

def score(e,p,r=None):
 y=np.arange(len(p))==e['winner'];a=np.array([t['actual_midrank'] for t in e['teams']]);expected=None if r is None else r@e['mid']
 top=np.flatnonzero(np.isclose(p,max(p),rtol=0,atol=1e-12));hit=float(e['winner'] in top)/len(top)
 return dict(champion_logloss=float(-np.log(max(p[e['winner']],1e-300))),champion_brier=float(np.sum((p-y)**2)),champion_hit=hit,finish_spearman=None if r is None else float(spearmanr(expected,a).statistic),finish_mae=None if r is None else float(np.mean(abs(expected-a))),champion_probability=float(p[e['winner']]),favorite=[e['teams'][i]['name'] for i in top],expected_rank=None if r is None else expected.tolist())

def main():
 OUT.mkdir(exist_ok=True);REP.mkdir(exist_ok=True)
 protect=['results/main_model.json','results/live_s16/latest.json','results/model_experiments/dynamic90/2026_Worlds.json'];hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protect}
 es=load_events();result=[];fits={}
 for e in es:
  prior=[p for p in es if p['year']<e['year']]
  if e['year'] not in fits:fits[e['year']]={m:fit(prior,m) for m in ['rank_pl','champion_softmax','calibrated']}
  f=fits[e['year']];rp,error=rank_marginals(e['x'],f['rank_pl']['alpha']);p=rp[:,0]
  preds={'baseline':(e['p0'],e['r0']),'rank_pl':(p,rp),'champion_softmax':(softmax(f['champion_softmax']['alpha']*e['x']),None),'calibrated':(softmax(f['calibrated']['alpha']*np.log(np.maximum(e['p0'],1e-12))),None),'mixture':((p+e['p0'])/2,(rp+e['r0'])/2)}
  models={m:dict(probabilities=pp.tolist(),rank_probabilities=None if rr is None else rr.tolist(),**score(e,pp,rr)) for m,(pp,rr) in preds.items()}
  result.append(dict(id=e['id'],year=e['year'],start_date=e['start_date'],training_events=[p['id'] for p in prior],fits=f,quadrature_error=error,teams=e['teams'],models=models,rank_bands=e['mid'].tolist()))
  print(e['id'],{m:round(f[m]['alpha'],4) for m in f},flush=True)
 metrics=['champion_logloss','champion_brier','champion_hit','finish_spearman','finish_mae'];summary={m:{k:(None if result[0]['models'][m][k] is None else float(np.mean([e['models'][m][k] for e in result]))) for k in metrics} for m in NAMES}
 rng=np.random.default_rng(2026);years=sorted({e['year'] for e in result});ix=rng.integers(0,len(years),(10000,len(years)));diagnostics={}
 for m in NAMES:
  if m=='baseline':continue
  diagnostics[m]={}
  for k in metrics:
   if summary[m][k] is None:continue
   delta=np.array([e['models'][m][k]-e['models']['baseline'][k] for e in result]);groups=np.array([[sum(delta[i] for i,e in enumerate(result) if e['year']==y),sum(e['year']==y for e in result)] for y in years]);z=groups[ix].sum(axis=1);ci=np.quantile(z[:,0]/z[:,1],[.025,.975]).tolist()
   diagnostics[m][k]=dict(delta=float(delta.mean()),year_cluster_95=ci,leave_one_event_out_range=[float(min((sum(delta)-d)/(len(delta)-1) for d in delta)),float(max((sum(delta)-d)/(len(delta)-1) for d in delta))],event_deltas=delta.tolist())
 finalfits={m:fit(es,m) for m in ['rank_pl','champion_softmax','calibrated']}
 d=dict(summary=summary,events=result,diagnostics=diagnostics,s16_candidate_parameters=finalfits,unchanged_hashes=hashes,protocol=dict(minimum_earlier_events=4,alpha_bounds=[.1,5],alpha_prior_mean=1,alpha_prior_sd=1,grid_points=41,holdout='strictly earlier calendar years; no same-year labels',new_simulation=False))
 (OUT/'summary.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');report(d)
 for p,h in hashes.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

def report(d):
 lines=['# 直接预测整届结果：独立模型比较','','23届 MSI／MSC／Worlds，按公历年份向前预测。同一年两届赛事都只用更早年份拟合，前期不足4届时使用固定默认参数。没有替换正式模型或 S16 报告。','','| 模型 | 冠军命中 | 冠军对数损失 ↓ | 冠军 Brier ↓ | 名次相关 ↑ | 名次绝对误差 ↓ |','|---|---:|---:|---:|---:|---:|']
 for m,label in NAMES.items():
  s=d['summary'][m];v=lambda k:'—' if s[k] is None else f'{s[k]:.5f}'
  lines.append(f'| {label} | {s["champion_hit"]*23:g}/23 | {v("champion_logloss")} | {v("champion_brier")} | {v("finish_spearman")} | {v("finish_mae")} |')
 lines+=['','**本轮未发现可整体替换原模型的方案。** 直接名次和直接冠军模型的总体冠军对数损失更高；等权组合降低Brier，但冠军对数损失和名次误差变差，正式模型保持不变。','','冠军首选并列时按均分计命中；2014 Worlds 的直接模型有三队并列首选，因此直接模型为9⅓次等效命中，不采用队名顺序任意选出一队。','','直接名次模型学习整届共同淘汰阶段的排序；直接冠军模型只学习冠军是谁。两者使用相同赛前实力特征，但训练目标不同。概率校准仅调整原冠军概率的集中程度，不产生新的名次分布，不能把其排名沿用原模型后声称排名改善。固定等权组合不根据这23届的结果搜索权重。','','直接模型没有模拟各届签表，不是官方赛制回放；原模型与等权组合中的原模型部分沿用逐届独立规则情景和已有近似。直接排名积分采用确定性数值计算，未新增蒙特卡洛；原模拟仍为每届14,000,605次、种子年份。','','## 差异是否稳定','','下表为候选减原模型；误差负值较好。区间按年份聚类，逐届删除仅用于影响诊断，没有删掉冷门来改主评价。','','| 候选 | 冠军损失差 | 95%年份区间 | 删除任意一届后的差值范围 | 改善赛事数 |','|---|---:|---|---|---:|']
 for m in NAMES:
  if m=='baseline':continue
  x=d['diagnostics'][m]['champion_logloss'];fmt=lambda v:f'[{v[0]:+.5f}, {v[1]:+.5f}]'
  lines.append(f'| {NAMES[m]} | {x["delta"]:+.5f} | {fmt(x["year_cluster_95"])} | {fmt(x["leave_one_event_out_range"])} | {sum(v<0 for v in x["event_deltas"])}/23 |')
 lines+=['','## 逐届结果','','| 赛事 | 实际冠军 | 原冠军概率 | 直接名次 | 直接冠军 | 校准 | 等权组合 |','|---|---|---:|---:|---:|---:|---:|']
 for e in d['events']:
  champion=next(t['name'] for t in e['teams'] if t['actual_rank']==[1,1]);lines.append('| '+f'[{e["id"]}]({e["id"]}.md) | {champion} | '+' | '.join(f'{e["models"][m]["champion_probability"]:.3%}' for m in NAMES)+' |')
  text=f'# {e["id"]}：整届目标比较\n\n[总览](README.md) · [逐届赛制与局限](../event_replay/rules.md)\n\n开赛截点：{e["start_date"]}。拟合标签只来自{e["year"]}年之前的{len(e["training_events"])}届；实际结果只用于评分。直接模型不模拟签表。\n\n'
  text+=table(['队伍','实际名次',*[NAMES[m]+'夺冠概率' for m in NAMES],'原预期名次','直接预期名次','组合预期名次'],[[t['name'],band(t['actual_rank']),*[f'{e["models"][m]["probabilities"][i]:.3%}' for m in NAMES],*[f'{e["models"][m]["expected_rank"][i]:.3f}' for m in ['baseline','rank_pl','mixture']]] for i,t in enumerate(e['teams'])])
  text+='\n概率校准和直接冠军模型没有最终名次分布，故不填写其预期名次。共同淘汰阶段并列保留。\n';(REP/f'{e["id"]}.md').write_text(text)
 lines+=['','## 逐年冻结参数','','系数越大，概率越集中；每一行只用较早年份确定。','','| 年份 | 可用届数 | 排名系数 | 冠军系数 | 校准系数 |','|---|---:|---:|---:|---:|']
 seen=set()
 for e in d['events']:
  if e['year'] in seen:continue
  seen.add(e['year']);lines.append(f'| {e["year"]} | {len(e["training_events"])} | '+ ' | '.join(f'{e["fits"][m]["alpha"]:.4f}' for m in ['rank_pl','champion_softmax','calibrated'])+' |')
 lines+=['','## 冷启动与单届影响诊断','','下面分组依据事先固定的4届最低训练要求；只是解释总结果，全部23届仍保留在主评价中。负值为改善。','','| 模型 | 无足够历史标签的5届：冠军损失差 | 已可拟合的18届：冠军损失差 |','|---|---:|---:|']
 for m in NAMES:
  if m=='baseline':continue
  vals=[]
  for fitted in (False,True):
   subset=[e for e in d['events'] if e['fits']['rank_pl']['fit']==fitted]
   vals.append(float(np.mean([e['models'][m]['champion_logloss']-e['models']['baseline']['champion_logloss'] for e in subset])))
  lines.append(f'| {NAMES[m]} | {vals[0]:+.5f} | {vals[1]:+.5f} |')
 lines+=['','直接冠军模型在已有足够标签的18届有小幅对数损失改善，但冷启动阶段明显变差；不能事后只保留有利的18届宣布成功。直接名次模型即使在后18届仍较差。对直接模型或等权组合删除任意单届后，总体冠军对数损失仍高于原模型；本轮负面结果不是由单独一届造成。','','## 解释边界','','这次改变的是整届预测层与训练目标，输入仍是原模型的赛前实力；尚未实现选手级能力模型，也没有把新补齐经济数据加入本轮。全局BP、选边、季中换人仍未建模。直接模型使用实际淘汰阶段的固定名次区间作评价口径，不把最终队伍身份当作输入。','','23届已用于多轮模型探索，逐年隔离能防止本轮拟合偷看未来，但不能消除研究者此前看到历史结果的影响。任何新优势都属于探索性证据，尚待未来赛事验证。冠军命中不单独决定模型选择。','','[模型细节](../../MODEL.md#整届目标模型实验) · [复算说明](METHOD.md)','']
 (REP/'README.md').write_text('\n'.join(lines))
 (REP/'METHOD.md').write_text('''# 复算与数值验收\n\n执行 `.venv/bin/python scripts/evaluate_event_targets.py`，再执行 `.venv/bin/python scripts/verify_event_targets.py`。输入为原 dynamic90 的23届赛前配置与已验证模拟计数。输出独立保存在 results/event_targets。\n\n排名模型用 Plackett–Luce 无序淘汰组的精确集合概率，子集DP累加组内全部可能顺序，不使用两两排名伪似然，也不随意拆开并列。每届负对数似然除以队伍数减一，避免大赛事仅因队伍更多占据主导。预测名次边缘分布用指数竞赛表示和一维数值积分，浮点误差上界随结果保存；不是实际赛制路径的精确求和。\n\n全部拟合只用更早年份；同年MSI不为Worlds提供结果标签。系数范围0.1至5，固定N(1,1)惩罚；先扫描41个点，再优化每个观察到的局部低谷并比较端点，减少单一起点的影响，不宣称数学上证明全局最优。少于4届时系数固定1。概率校准将零模拟概率以1e-12下限处理后归一化，仅用于该候选。\n\n基线复用14,000,605次原模拟，不重新抽样。排名预测统一投影到各届共同淘汰阶段中点；等权组合混合整届排名分布，所以冠军和预期名次相容。只输出冠军的两个候选不编造名次或晋级路径。\n''')
if __name__=='__main__':main()

"""Independent gradients, no-leakage cutoffs, seed averages and replay invariants."""
import gzip,json,hashlib,sys
import numpy as np
from scipy.special import expit
from dnn_model import MLP,Scaler,predict
from run_dnn import R,D,CACHE,MODES,N,digest
from model import series_probability

def unit():
 rng=np.random.default_rng(2026);x=rng.normal(size=(9,24));rev=rng.normal(size=(9,24));offset=rng.normal(size=9);y=rng.random(9);w=np.arange(1,10.)
 for residual in [False,True]:
  net=MLP(2026,residual);loss,grad=net.loss_grad(x,rev,offset,y,w)
  for j,p in enumerate(net.p):
   for _ in range(4):
    ix=tuple(rng.integers(n) for n in p.shape);old=p[ix];p[ix]=old+1e-5;a,_=net.loss_grad(x,rev,offset,y,w);p[ix]=old-1e-5;b,_=net.loss_grad(x,rev,offset,y,w);p[ix]=old;assert abs((a-b)/2e-5-grad[j][ix])<1e-7
  assert np.max(abs(expit(net.logits(x,rev,offset))+expit(net.logits(rev,x,-offset))-1))<1e-12
  net.p[4][:]=0;net.p[5][:]=0
  assert np.allclose(expit(net.logits(x,rev,offset)),expit(offset) if residual else .5,atol=1e-14)
  a=MLP(2026,residual);b=MLP(2026,residual);a.fit(x,rev,offset,y,w,2026,epochs=3);b.fit(x,rev,offset,y,w,2026,epochs=3);assert all(np.array_equal(u,v) for u,v in zip(a.p,b.p))
 scale=Scaler().fit([[None,1],[None,3]],[[None,1],[None,3]]);v=scale.transform([[None,2],[7,2]]);assert np.isfinite(v).all() and v[0,2]==1 and v[1,2]==0 and scale.median[0]==0
 print('PASS analytic MLP gradients, reciprocity, zero-residual baseline, deterministic training and missing-value masks')

def full():
 from report_chain_events import evaluate
 from report_research_models import KEYS
 from report_dnn import series_metrics
 with gzip.open(R/'.local/research_models/features.json.gz','rt') as f:data=json.load(f)
 protocol=json.loads((D/'protocol.json').read_text());cs=json.loads((D/'event_configs.json').read_text());pred=json.loads((D/'predictions.json').read_text());fits=json.loads((D/'fits.json').read_text());summary=json.loads((D/'summary.json').read_text());assert len(fits)==138 and len(pred)==len({r['detail'] for r in pred})==1300
 for fit in fits:
  rows=[r for r in data['domestic'] if r['date']<fit['cutoff']];days=sorted({r['date'] for r in rows});assert days[max(1,int(.8*len(days)))]==fit['validation_start'];assert fit['fit_latest']<fit['validation_start']<=fit['validation_latest']<fit['cutoff'];assert fit['training_series']==len(rows) and fit['training_maps']==sum(r['w'] for r in rows)
  train=[r for r in rows if r['date']<fit['validation_start']];valid=[r for r in rows if r['date']>=fit['validation_start']];assert max(r['date'] for r in train)==fit['fit_latest'] and max(r['date'] for r in valid)==fit['validation_latest'];assert 1<=fit['selected_epochs']<=fit['epochs_run']<=120
  best=float('inf');selected=0
  for epoch,loss in enumerate(fit['validation_curve'],1):
   if loss<best-1e-5:best=loss;selected=epoch
  assert fit['selected_epochs']==selected and fit['validation_loss']==best
  scaler=Scaler().fit([r['x'] for r in rows],[r['reverse'] for r in rows]);assert scaler.record()==fit['scaler']
  c=next(c for c in cs[fit['mode']] if c['id']==fit['id']);assert fit['seed'] in [c['year']+i for i in [0,10000,20000]]
 for mode,events in cs.items():
  assert len(events)==23
  for c in events:
   e=next(e for e in data['events'] if e['config']['id']==c['id']);n=len(c['teams']);x=[e['features'][i][j] for i in range(n) for j in range(n)];rev=[e['features'][j][i] for i in range(n) for j in range(n)];rr=[r for r in pred if r['season']==c['season'] and r['event']==c['event']];assert all(r['date']>=c['start_date'] for r in rr);matrices=[];probs=[]
   for offset in [0,10000,20000]:
    seed=c['year']+offset;cached=json.loads((CACHE/f'{mode}_{c["id"]}_{seed}.json').read_text());assert cached['signature']==protocol['training_signature'];fit=cached['fit'];net=MLP(seed,mode=='residual_mlp');weights=np.load(CACHE/f'{mode}_{c["id"]}_{seed}.npz');net.p=[weights[f'p{i}'] for i in range(6)];scale=Scaler()
    for k,v in fit['scaler'].items():setattr(scale,k,np.array(v))
    p=predict(net,scale,x,rev).reshape(n,n);q=predict(net,scale,[r['features'] for r in rr],[r['reverse_features'] for r in rr]);assert np.max(abs(p-np.array(cached['matrix'])))<1e-12 and np.max(abs(q-cached['probabilities']))<1e-12;matrices.append(p);probs.append(q)
   p=np.array(c['pairwise_probabilities']);assert np.max(abs(p-np.mean(matrices,axis=0)))<1e-12;assert np.max(abs(p+p.T-1))<1e-12 and np.all((p>0)&(p<1))
   for j,r in enumerate(rr):
    assert abs(r['probabilities'][mode]-series_probability(np.mean(probs,axis=0)[j],r['best_of']))<1e-12
    assert np.allclose(r['seed_probabilities'][mode],[series_probability(q[j],r['best_of']) for q in probs],atol=1e-12)
   path=D/mode/f'{c["id"]}.json';raw=json.loads(path.read_text());assert raw['samples']==N and raw['seed']==c['year'];assert raw['input_sha256']==digest(path.with_suffix('.txt')) and raw['engine_sha256']==digest(R/'scripts/event_simulation.cpp');old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();new=path.with_suffix('.txt').read_text().splitlines();assert old[:2]==new[:2] and old[2+n:]==new[2+n:];assert np.max(abs(np.array([[float(v) for v in line.split()] for line in new[2:2+n]])-p))<1e-12
   assert all(sum(v[2] for v in bins)==N for bins in raw['counts']);assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N;assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
   metrics=evaluate(c,raw);record=next(e for e in summary['events'] if e['id']==c['id'])['models'][mode]
   for key in KEYS:assert abs(metrics[key]-record[key])<1e-12
 for event in summary['events']:
  c=next(c for c in cs['mlp'] if c['id']==event['id']);base=evaluate(c,json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json').read_text()))
  for key in KEYS:assert abs(base[key]-event['models']['baseline'][key])<1e-12
 for mode,metrics in summary['summary'].items():
  for key in KEYS:assert abs(metrics[key]-np.mean([e['models'][mode][key] for e in summary['events']]))<1e-12
  assert series_metrics(pred,mode)==summary['series'][mode]
 for mode in MODES:
  for i in range(3):assert series_metrics(pred,mode,i)==summary['seeds'][mode][i]
 for p,h in {**protocol['input_hashes'],**protocol['unchanged_hashes']}.items():assert digest(R/p)==h,p
 print('PASS 138 trained fits, prior-event validation/refit, 1300 forecasts, stored-weight prediction reproduction, three-seed averages, 46 formal replays, unchanged rules/main/S16/live, hashes and aggregate metrics')
if __name__=='__main__':
 unit()
 if '--unit' not in sys.argv:full()

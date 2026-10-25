"""Independent permutation enumeration and temporal/metric audits."""
import hashlib,itertools,json,math
import numpy as np
from evaluate_event_targets import R,OUT,NAMES,block_logprob,rank_marginals,load_events,score,fit

def main():
 w=np.array([.2,.7,1.4,2.3]);exact=np.zeros((4,4));setprob=0
 for order in itertools.permutations(range(4)):
  p=1.;remaining=sum(w)
  for i in order:p*=w[i]/remaining;remaining-=w[i]
  for k,i in enumerate(order):exact[i,k]+=p
  if set(order[:2])=={0,2}:setprob+=p
 assert abs(math.exp(block_logprob(w,[0,2]))-setprob)<1e-12
 r,err=rank_marginals(np.log(w),1);assert np.max(abs(r-exact))<1e-8
 uniform,_=rank_marginals(np.zeros(5),3);assert np.max(abs(uniform-.2))<1e-9
 permutation=np.array([2,0,3,1]);rr,_=rank_marginals(np.log(w[permutation]),1);assert np.max(abs(rr-exact[permutation]))<1e-8
 assert abs(block_logprob(w,range(4)))<1e-12
 d=json.loads((OUT/'summary.json').read_text());es=load_events();assert len(es)==len(d['events'])==23
 for e,z in zip(es,d['events']):
  assert e['id']==z['id'];prior=[p for p in es if p['year']<e['year']]
  assert z['training_events']==[p['id'] for p in prior]
  assert e['config']['latest_training_date']<e['start_date']
  for m,f in z['fits'].items():
   assert .1<=f['alpha']<=5 and f['events']==len(prior)
   if len(prior)<4:assert f['alpha']==1 and not f['fit']
  for m,v in z['models'].items():
   p=np.array(v['probabilities']);assert np.all(p>=0) and abs(sum(p)-1)<1e-7
   rr=None if v['rank_probabilities'] is None else np.array(v['rank_probabilities'])
   if rr is not None:
    assert np.max(abs(rr.sum(axis=0)-1))<1e-7 and np.max(abs(rr.sum(axis=1)-1))<1e-7
    assert np.max(abs(rr[:,0]-p))<1e-7
   got=score(e,p,rr)
   for k in ['champion_logloss','champion_brier','champion_hit','finish_mae','finish_spearman']:
    assert (got[k] is None and v[k] is None) or abs(got[k]-v[k])<1e-10
  pp=z['models'];assert np.max(abs(np.array(pp['mixture']['probabilities'])-(np.array(pp['baseline']['probabilities'])+pp['rank_pl']['probabilities'])/2))<1e-12
 # Refit all models on pre-2017 events and compare saved parameters, avoiding target labels.
 target=next(z for z in d['events'] if z['year']==2017);earlier=[e for e in es if e['year']<2017]
 for m in target['fits']:assert abs(fit(earlier,m)['alpha']-target['fits'][m]['alpha'])<1e-9
 for m in NAMES:
  for k,value in d['summary'][m].items():
   if value is not None:assert abs(value-np.mean([z['models'][m][k] for z in d['events']]))<1e-12
 for p,h in d['unchanged_hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
 print('PASS independent 24-permutation ranking/block probabilities, uniform and relabeling symmetry, numeric marginals, 23-event chronology, prior-only refit, coherent mixture, metric reproduction, unchanged main/live/S16')
if __name__=='__main__':main()

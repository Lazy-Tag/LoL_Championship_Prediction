"""Independent joint-density, derivatives, exact fallbacks and timing checks."""
import gzip,json,hashlib,sys
from datetime import date,timedelta
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from research_model_core import joint_terms,marginal,JointGold,ChangePoint,DEFAULT
from candidate_models import DynamicBT
from run_research_models import R,D,CACHE,N

def unit():
 par=dict(a=.8,c=.45,k=1.1,b=.25,sigma=2.,n=300);d=np.array([-.7,.4,1.]);g=np.array([-1.,np.nan,2.]);w=np.array([0.,2.,1.]);n=np.array([1.,3.,1.]);side=np.array([1.,1.,-1.]);loss,grad,hess=joint_terms(d,w,n,g,side,par);eps=1e-5
 for i in range(3):
  v=np.zeros(3);v[i]=eps;lp,gp,_=joint_terms(d+v,w,n,g,side,par);lm,gm,_=joint_terms(d-v,w,n,g,side,par)
  assert abs((lp-lm)/(2*eps)-grad[i])<1e-6 and abs((gp[i]-gm[i])/(2*eps)-hess[i])<1e-6
 for x in [-2,0,1]:
  assert abs(float(marginal(x,par)+marginal(-x,par))-1)<1e-12
  expected=np.mean([quad(lambda z:np.exp(-z*z/2)/np.sqrt(2*np.pi)*expit((par['a']+par['c']*par['k'])*x+par['c']*(par['sigma']*z+b)),-10,10)[0] for b in [-par['b'],par['b']]])
  assert abs(float(marginal(x,par))-expected)<1e-6
 # Known side is retained when economy is missing.
 x=.4
 for side in [-1,1]:
  q=quad(lambda z:np.exp(-z*z/2)/np.sqrt(2*np.pi)*expit((par['a']+par['c']*par['k'])*x+par['c']*(par['sigma']*z+side*par['b'])),-10,10)[0]
  assert abs(float(marginal(x,par,side=side))-q)<1e-6
 teams=['a','b'];regs={'a':'KR','b':'CN'};base=DynamicBT(teams,regs,{});gold=JointGold(teams,regs,{});cp=ChangePoint(teams,regs,{},2020,particles=4,hazard_half=0)
 for k in [0,1,7,30]:
  day=date(2020,1,1)+timedelta(days=k);rows=[dict(team1='a',team2='b',wins1=2,wins2=1,date=day.isoformat())]
  for obj in [base,gold,cp]:obj.advance(day)
  assert all(abs(base.strengths()[t]-cp.strengths()[t])<1e-8 for t in teams)
  cp.resample_before_update();cp.update(rows);base.update(rows);gold.update(rows)
  assert np.allclose(base.m,gold.m,atol=1e-10) and np.allclose(base.C,gold.C,atol=1e-10)
  assert all(np.allclose(base.m,m.m,atol=1e-8) and np.allclose(base.C,m.C,atol=1e-8) for m in cp.bank)
 print('PASS joint density derivatives, independent normal integration, reciprocity, GDP-disabled baseline mean/covariance, zero-hazard particle baseline mean/covariance')

def full():
 protocol=json.loads((D/'protocol.json').read_text());cs=json.loads((D/'event_configs.json').read_text());pred=json.loads((D/'predictions.json').read_text());assert len(pred)==len({r['detail'] for r in pred})==1300
 for x in json.loads((D/'joint_parameters.json').read_text()):
  if x['parameters']['n']:assert int(x['parameters']['latest_date'][:4])<x['season']+2010
 with gzip.open(CACHE/'features.json.gz','rt') as f:features=json.load(f)['domestic']
 for fit in json.loads((D/'tree_fits.json').read_text()):
  train=[r for r in features if r['date']<fit['cutoff']];assert len(train)==fit['training_series'] and max(r['date'] for r in train)==fit['latest_training_date']<fit['cutoff'];assert sum(r['w'] for r in train)==fit['training_maps']
 # No same-date context mutation: shared teams have identical history features on that date.
 from backtest import load_season
 identities={}
 for season in range(4,16):
  rr,_=load_season(season)
  identities.update({r['detail']:(r['team1'],r['team2']) for r in rr})
 seen={}
 for row in features:
  x=row['x'];rev=row['reverse'];assert abs(x[0]+rev[0])<1e-10 and x[1]==rev[1]
  for a,b in [(2,3),(4,5),(6,7),(8,9),(10,11)]:assert x[a]==rev[b] and x[b]==rev[a]
  for t,indices in zip(identities[row['detail']],[[2,4,6,8,10],[3,5,7,9,11]]):
   context=[x[i] for i in indices];key=(row['date'],t)
   if key in seen:assert context==seen[key],('same-day feature mutation',key)
   seen[key]=context
 for mode,events in cs.items():
  assert len(events)==23
  for c in events:
   assert c['latest_training_date']<c['start_date'];p=np.array(c['pairwise_probabilities']);assert np.max(abs(p+p.T-1))<1e-10 and np.all(p>0) and np.all(p<1)
   path=D/mode/f'{c["id"]}.json';raw=json.loads(path.read_text());assert raw['samples']==N and raw['seed']==c['year'];assert raw['input_sha256']==hashlib.sha256(path.with_suffix('.txt').read_bytes()).hexdigest();assert raw['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
   if mode=='joint_gold' and c['season']<=6:
    baseline=json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json').read_text())
    assert raw['counts']==baseline['counts']
   n=len(c['teams']);old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();new=path.with_suffix('.txt').read_text().splitlines();assert old[:2]==new[:2] and old[2+n:]==new[2+n:]
   assert all(sum(v[2] for v in bins)==N for bins in raw['counts']);assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N;assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
 for p,h in {**protocol['input_hashes'],**protocol.get('implementation_hashes',{}),**protocol['unchanged_hashes']}.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
 from report_research_models import evaluate,KEYS,gated_ensemble,eligible
 summary=json.loads((D/'summary.json').read_text())
 for event in summary['events']:
  for mode,recorded in event['models'].items():
   config=next(c for c in cs['joint_gold' if mode=='baseline' else mode] if c['id']==event['id'])
   path=R/f'results/model_experiments/dynamic90/{event["id"]}.json' if mode=='baseline' else D/mode/f'{event["id"]}.json'
   actual=evaluate(config,json.loads(path.read_text()))
   for k in KEYS:assert abs(actual[k]-recorded[k])<1e-12
 for mode,metrics in summary['summary'].items():
  for k in KEYS:assert abs(metrics[k]-np.mean([e['models'][mode][k] for e in summary['events']]))<1e-12
 assert gated_ensemble(summary['events'])==summary['ensemble']
 assert eligible(summary['events'],2026)[0]==summary['full_history_gate']
 years={e['id']:e['year'] for e in summary['events']}
 for fit in summary['ensemble']['fits']:
  assert all(years[e]<fit['year'] for e in fit['training_events'])
 for e in summary['ensemble']['events']:
  assert abs(sum(e['probabilities'])-1)<1e-10 and abs(sum(e['weights'].values())-1)<1e-10
 print('PASS raw-count metric recomputation, historical ensemble refit, prior-year gating and distribution conservation')
 print('PASS 69 formal simulations, 23 independent rules/seeds per candidate, 1300 predictions, past-year gold parameters, pre-event domestic tree fitting, symmetric inputs/matrices, conservation, hashes and unchanged main/S16/live')
if __name__=='__main__':
 unit()
 if '--unit' not in sys.argv:full()

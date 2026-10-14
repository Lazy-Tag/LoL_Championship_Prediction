"""Numerical and chronological invariants for candidate models."""
from datetime import date,timedelta
import numpy as np
from candidate_models import design,static_fit,DynamicBT

def main():
 teams=['a','b','c'];regions={'a':'X','b':'X','c':'Y'};prior={'X':1.,'Y':-1.}
 day=date(2025,1,1);rows=[dict(team1='a',team2='b',wins1=2,wins2=0,date=day.isoformat())]
 X,rs,_=design(rows,teams,regions);assert np.all(X.toarray()[:,:len(rs)]==0)
 th,_=static_fit([],teams,regions,prior,day);assert th=={'a':1.,'b':1.,'c':-1.}
 th,_=static_fit(rows,teams,regions,prior,day+timedelta(days=1));assert th['a']>th['b'] and abs((th['a']+th['b'])/2-1)<1e-10
 try:static_fit(rows,teams,regions,prior,day)
 except AssertionError:pass
 else:raise AssertionError('same-day leakage allowed')
 rr=rows+[dict(team1='b',team2='c',wins1=1,wins2=2,date=day.isoformat())]
 a=DynamicBT(teams,regions,prior);b=DynamicBT(teams,regions,prior)
 for m,rrr in [(a,rr),(b,rr[::-1])]:m.advance(day);m.update(rrr)
 assert np.allclose(a.m,b.m,atol=1e-10) and np.allclose(a.C,b.C,atol=1e-10)
 assert np.linalg.eigvalsh(a.C).min()>0
 old=a.m.copy();a.advance(day+timedelta(days=90));assert np.allclose(a.m[a.nr:],old[a.nr:]/2)
 assert np.allclose(a.m[:a.nr],old[:a.nr]);assert np.linalg.eigvalsh(a.C).min()>0
 fresh=DynamicBT(teams,regions,prior);assert fresh.strengths()=={'a':1.,'b':1.,'c':-1.}
 try:a.advance(day)
 except AssertionError:pass
 else:raise AssertionError('backward time accepted')
 print('PASS: domestic region cancellation, proper prior, same-day exclusion, daily permutation invariance, covariance positivity, 90-day memory, season reset')
if __name__=='__main__':main()

if __name__=='__main__':
 import json,hashlib
 from pathlib import Path
 from backtest import metrics
 R=Path(__file__).resolve().parents[1];out=R/'results/model_experiments'
 pred=json.loads((out/'predictions.json').read_text());summary=json.loads((out/'summary.json').read_text())
 assert len(pred)==1300 and sum(r['wins1']+r['wins2'] for r in pred)==1965
 for model in ['regional90','hierarchical90','dynamic90']:
  assert metrics(pred,model)==summary['aggregate'][model]
  assert all(0<r[model]<1 and (r['latest_training_date'] is None or r['latest_training_date']<r['date']) for r in pred)
 configs=json.loads((out/'event_configs.json').read_text())
 for model,cs in configs.items():
  assert len(cs)==23
  for c in cs:
   raw=json.loads((out/model/f'{c["id"]}.json').read_text());n=raw['samples'];assert n==14_000_605 and raw['seed']==c['year']
   assert raw['input_sha256']==hashlib.sha256((out/model/f'{c["id"]}.txt').read_bytes()).hexdigest()
   assert raw['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
   assert c['latest_training_date'] is None or c['latest_training_date']<c['start_date']
   assert all(sum(k for lo,hi,k in bins)==n for bins in raw['counts'])
   assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==n
   assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==n*len(c['teams'])*(len(c['teams'])+1)
 for auditfile in (R/'data/enrichment').glob('S*_audit.json'):
  a=json.loads(auditfile.read_text());maps=json.loads(auditfile.with_name(auditfile.name.replace('_audit','_maps')).read_text());assert len({m['gameid'] for m in maps})==len(maps)
  assert a['matched_maps']==sum(m['reconciliation']=='matched' for m in maps)
  assert all(m['wins1']+m['wins2']==1 for m in maps)
 selection=json.loads((R/'results/main_model.json').read_text());assert selection['main_model']=='dynamic90'
 raw=json.loads((R/selection['s16_result']).read_text());assert raw['simulations']==14_000_605 and raw['seed']==2026
 assert raw['input_sha256']==hashlib.sha256((out/'dynamic90/2026_Worlds.txt').read_bytes()).hexdigest()
 assert [sum(c[i] for c in raw['counts']) for i in range(5)]==[raw['simulations']*v for v in [1,16,8,4,2]]
 for p in [R/'README.md',R/'reports/s16/README.md']:
  text=p.read_text();assert '次数' not in text and '50.09%' in text
 assert '10/23' in (R/'README.md').read_text()
 print('PASS: identical targets, metric recomputation, 46 event count/hash/seed/rank invariants, map uniqueness, dynamic main selection and S16 publication values')

"""Checks for economic state update, chronology and complete replay outputs."""
import json,hashlib
from pathlib import Path
from datetime import date,timedelta
import numpy as np
from evaluate_economy_residual import EconomyState,fit_beta
from backtest import metrics
R=Path(__file__).resolve().parents[1]
def main():
 teams=['a','b','c'];regs={'a':'X','b':'X','c':'Y'};day=date(2025,1,1)
 a=EconomyState(teams,regs);b=EconomyState(teams,regs)
 obs=[('a','b',.2,1.,True),('b','c',-.1,-2.,False)]
 for m,rr in [(a,obs),(b,obs[::-1])]:m.advance(day);m.update(rr)
 assert np.allclose(a.m,b.m) and np.allclose(a.C,b.C)
 A=np.array([[1,-1,0],[0,1,-1]]);V=np.eye(3)*2.25;C=np.linalg.inv(np.linalg.inv(V)+A.T@A/9)
 assert np.allclose(a.C,C) and np.allclose(a.m,C@A.T@np.array([1.,-2.])/9)
 assert np.linalg.eigvalsh(a.C).min()>0
 old=a.m.copy();mass=a.mass.copy();a.advance(day+timedelta(days=90));assert np.allclose(a.m,old/2) and np.allclose(a.mass,mass/2)
 assert a.feature('a','b')==(0.,False)
 try:fit_beta([(day,0.,1.,1)],day)
 except AssertionError:pass
 else:raise AssertionError('same day fit accepted')
 d=R/'results/economy_residual_experiment';pred=json.loads((d/'predictions.json').read_text());s=json.loads((d/'summary.json').read_text())
 assert len(pred)==1300 and sum(r['wins1']+r['wins2'] for r in pred)==1965
 for r in pred:
  assert 0<r['economy_residual90']<1
  for k in ['economy_last1','economy_last2']:
   assert r[k] is None or r[k]<r['date']
  if not r['economy_ready']:assert abs(r['economy_residual90']-r['joint_side90'])<1e-12
  else:
   assert min(r['economy_weight1'],r['economy_weight2'])>=5
   assert all((date.fromisoformat(r['date'])-date.fromisoformat(r[k])).days<=90 for k in ['economy_last1','economy_last2'])
 for name,rr in [('all',pred),('economy_ready',[r for r in pred if r['economy_ready']])]:
  for f in ['dynamic90','joint_side90','economy_residual90']:assert metrics(rr,f)==s['aggregate'][name][f]
 side=json.loads((R/'results/joint_side_experiment/summary.json').read_text())
 assert side['baseline_pointer_sha256']==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 print('PASS economy Gaussian closed form, daily order, positive covariance, 90-day decay, same-day guard, 1300-series conservation, missing-data fallback, cutoff, readiness, metric reproduction and unchanged main pointer.')
if __name__=='__main__':main()

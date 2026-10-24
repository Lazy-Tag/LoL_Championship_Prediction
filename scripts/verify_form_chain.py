"""Independent integration, sequential updating and replay invariants."""
import json,hashlib
from itertools import product
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import beta as beta_dist
from evaluate_form_chain import conditional_series,next_probability,binary_metrics,FIELDS
from model import series_probability
R=Path(__file__).resolve().parents[1]
def main():
 for p in [.15,.5,.8]:
  for bo in [1,3,5]:
   assert abs(conditional_series(p,0,bo)-series_probability(p,bo))<1e-12
   for rho in [.03,.2]:
    k=1/rho-1;a=p*k;b=(1-p)*k
    for w,l in [(0,0),(1,0),(0,1)]:
     target=bo//2+1
     if max(w,l)>=target:continue
     exact=quad(lambda q:conditional_series(q,0,bo,w,l)*beta_dist.pdf(q,a+w,b+l),0,1,epsabs=1e-9)[0]
     assert abs(exact-conditional_series(p,rho,bo,w,l))<1e-7
     assert abs(conditional_series(p,rho,bo,w,l)+conditional_series(1-p,rho,bo,l,w)-1)<1e-10
    assert next_probability(p,rho,1,0)>p and next_probability(p,rho,0,1)<p
    assert abs(conditional_series(.5,rho,bo)-.5)<1e-10
    assert abs(next_probability(p,rho,1,1)-(a+1)/(k+2))<1e-12
 d=R/'results/form_chain_experiment';pred=json.loads((d/'predictions.json').read_text());live=json.loads((d/'live_predictions.json').read_text());summary=json.loads((d/'summary.json').read_text())
 assert len(pred)==1300
 for r in pred:
  assert abs(r['dynamic90']-series_probability(r['baseline_map_probability'],r['best_of']))<1e-12
  assert all(0<r[f]<1 for f in FIELDS)
 for r in live:
  assert r['next_map']==r['wins_before']+r['losses_before']+1
  assert max(r['wins_before'],r['losses_before'])<r['best_of']//2+1
  assert all(0<r[f]<1 for f in FIELDS)
 for name,rr in [('prematch',pred),('live_next_map',live),('after_first_next_map',[r for r in live if r['next_map']==2])]:
  for f in FIELDS:assert binary_metrics(rr,f)==summary[name][f]
 assert summary['main_pointer_sha256']==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 assert len(live)>0 and len({(r['season'],r['detail']) for r in live})==sum(r['ordered_series'] for r in summary['coverage'])
 print('PASS beta-integral equivalence, score conditioning, reciprocity, independence limit, posterior direction, 1300 targets, live-prefix bounds, metrics and unchanged main pointer.')
if __name__=='__main__':main()

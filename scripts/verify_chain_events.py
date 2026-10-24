"""Validate event cutoffs, probability integration and untouched baseline."""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
from evaluate_form_chain import conditional_series
from build_chain_engine import source
R=Path(__file__).resolve().parents[1];D=R/'results/chain_events';N=14_000_605

def main():
 cs=json.loads((D/'event_configs.json').read_text());assert len(cs)==23
 for c in cs:
  p=D/f'{c["id"]}.txt';text=p.read_text();base,extra=text.split('SERIES_PROBABILITIES_V1\n');old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text();assert base.rstrip()==old.rstrip()
  n=len(c['teams']);single=np.array([[float(v) for v in l.split()] for l in old.splitlines()[2:2+n]]);mat=np.array([float(v) for v in extra.split()]).reshape(2,n,n)
  for k,bo in enumerate([3,5]):
   assert np.allclose(mat[k]+mat[k].T,1,atol=1e-12)
   assert np.allclose(mat[k],[[conditional_series(v,c['rho'],bo) for v in rr] for rr in single],atol=1e-12)
  assert c['latest_training_date'] is None or c['latest_training_date']<c['start_date']
  assert c['rho_latest_training_date'] is None or c['rho_latest_training_date']<c['start_date']
  raw=json.loads(p.with_suffix('.json').read_text());assert raw['samples']==N and raw['seed']==c['year']
  assert raw['input_sha256']==hashlib.sha256(p.read_bytes()).hexdigest() and raw['engine_sha256']==hashlib.sha256(source().encode()).hexdigest()
  assert all(sum(x[2] for x in bins)==N for bins in raw['counts'])
  assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==N
  assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
  # rho=0 override must preserve original paths, including old unusual formats.
  zero=old.rstrip()+'\nSERIES_PROBABILITIES_V1\n'+'\n'.join(' '.join(str(conditional_series(v,0,bo)) for v in rr) for bo in [3,5] for rr in single)+'\n'
  aa=json.loads(subprocess.check_output([str(R/'.local/build/event_chain'),'1000'],input=old.encode()));bb=json.loads(subprocess.check_output([str(R/'.local/build/event_chain'),'1000'],input=zero.encode()))
  for key in ['counts','duration_seeded_ties','complex_tie_scenarios','draw_waivers']:assert aa[key]==bb[key],(c['id'],key)
 main=json.loads((R/'results/form_chain_experiment/summary.json').read_text())
 assert main['main_pointer_sha256']==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 print('PASS 23 event-specific inputs, frozen dates, exact integrated probabilities, 14,000,605 samples/year seeds, rank conservation, zero-correlation path equivalence and unchanged main pointer.')
if __name__=='__main__':main()

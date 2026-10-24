"""Two independent arms: posterior covariance vs fixed .35 event shock."""
import concurrent.futures,hashlib,json,subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from backtest import load_season,affiliations,prior_regions
from candidate_models import DynamicBT
from build_latent_event_engine import source
R=Path(__file__).resolve().parents[1];OUT=R/'results/latent_events';N=14_000_605
MODES=['posterior','event_form'];EVENT_SD=.35

def prepare():
 OUT.mkdir(exist_ok=True);configs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];seasons={};regions={};events=[]
 for s in range(3,16):
  seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
  if s>3:
   for t,v in regions[s-1].items():regions[s].setdefault(t,v)
 for s in range(4,16):
  rows=seasons[s];teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regions[s-1],90)
  model=DynamicBT(teams,regions[s],prior);byday=defaultdict(list);ed=defaultdict(list);latest=None
  for r in rows:byday[r['date']].append(r)
  for c in configs:
   if c['season']==s:ed[c['start_date']].append(c)
  for ds in sorted(set(byday)|set(ed)):
   model.advance(date.fromisoformat(ds));theta=model.strengths()
   for c in ed[ds]:
    assert latest is None or latest<ds
    assert all(abs(theta[t]-c['strength'][t])<1e-9 for t in c['teams'])
    n=len(c['teams']);H=np.zeros((n,len(model.m)))
    for i,t in enumerate(c['teams']):H[i,model.ri[regions[s].get(t,'UNKNOWN')]]=1;H[i,model.nr+model.ti[t]]=1
    mu=H@model.m;cov=H@model.C@H.T;cov=(cov+cov.T)/2;L=np.linalg.cholesky(cov)
    assert np.allclose(L@L.T,cov,atol=1e-12)
    base=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text();conf={**c,'joint_covariance':cov.tolist(),'means':mu.tolist(),'cholesky':L.tolist(),'event_form_sd':EVENT_SD,'baseline_input_sha256':hashlib.sha256(base.encode()).hexdigest()};events.append(conf)
    for mode in MODES:
     out=OUT/mode;out.mkdir(exist_ok=True);matrix=L if mode=='posterior' else np.eye(n)*EVENT_SD
     text=base.rstrip()+'\nLATENT_EVENT_V1\n'+' '.join(map(str,mu))+'\n'+'\n'.join(' '.join(map(str,row)) for row in matrix)+'\n'
     (out/f'{c["id"]}.txt').write_text(text)
   model.update(byday[ds])
   if byday[ds]:latest=ds
  print('Prepared S',s,flush=True)
 (OUT/'event_configs.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n');return events

def check_engine(events):
 for c in events:
  old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_bytes();n=len(c['teams'])
  zero=old.rstrip()+b'\nLATENT_EVENT_V1\n'+(' '.join(map(str,c['means']))+'\n'+'\n'.join(' '.join(['0']*n) for _ in range(n))+'\n').encode()
  args=[str(R/'.local/build/event_latent'),'1000']
  a=json.loads(subprocess.check_output([str(R/'.local/build/event_simulation'),'1000'],input=old))
  for inp in [old,zero]:
   b=json.loads(subprocess.check_output(args,input=inp))
   for k in ['counts','duration_seeded_ties','complex_tie_scenarios','draw_waivers']:assert a[k]==b[k],(c['id'],k)
 print('PASS baseline and zero-variance paths for all 23 independent rule configurations',flush=True)

def main():
 events=prepare();check_engine(events);engine=hashlib.sha256(source().encode()).hexdigest()
 def run(job):
  mode,c=job;p=OUT/mode/f'{c["id"]}.txt';out=p.with_suffix('.json');digest=hashlib.sha256(p.read_bytes()).hexdigest()
  if out.exists():
   old=json.loads(out.read_text())
   if old.get('input_sha256')==digest and old.get('engine_sha256')==engine and old.get('samples')==N:return mode+' '+c['id']+' reused'
  tmp=out.with_suffix('.tmp');log=R/'.local'/f'latent_{mode}_{c["id"]}.log'
  with p.open('rb') as fin,tmp.open('wb') as fout,log.open('wb') as err:subprocess.run([str(R/'.local/build/event_latent'),str(N)],stdin=fin,stdout=fout,stderr=err,check=True)
  raw=json.loads(tmp.read_text());assert raw['samples']==N and raw['seed']==c['year']
  assert all(sum(k for lo,hi,k in bins)==N for bins in raw['counts']);assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==N
  assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*len(c['teams'])*(len(c['teams'])+1)
  raw.update(model=mode,input_sha256=digest,engine_sha256=engine,base_engine_sha256=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest());tmp.write_text(json.dumps(raw,indent=2)+'\n');tmp.replace(out)
  return mode+' '+c['id']+' complete '+str(raw['seconds'])+'s'
 jobs=[(m,c) for c in events for m in MODES]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  fs=[pool.submit(run,j) for j in jobs]
  for f in concurrent.futures.as_completed(fs):print(f.result(),flush=True)
if __name__=='__main__':main()

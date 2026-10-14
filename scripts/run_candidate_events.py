"""Reuse unchanged rule scenarios, substituting candidate pre-event probabilities."""
import concurrent.futures,hashlib,json,subprocess
from pathlib import Path
from scipy.special import expit
R=Path(__file__).resolve().parents[1];N=14_000_605

def main():
 configs=json.loads((R/'results/model_experiments/event_configs.json').read_text());jobs=[]
 for model,events in configs.items():
  out=R/'results/model_experiments'/model;out.mkdir(exist_ok=True)
  for c in events:
   lines=(R/f'data/event_replay/{c["id"]}.txt').read_text().splitlines();n=len(c['teams']);th=[c['strength'][t] for t in c['teams']]
   lines[2:2+n]=[' '.join(str(float(expit(a-b))) for b in th) for a in th]
   inp=out/f'{c["id"]}.txt';inp.write_text('\n'.join(lines)+'\n');jobs.append((model,c,inp))
 def run(job):
  model,c,inp=job;out=inp.with_suffix('.json');digest=hashlib.sha256(inp.read_bytes()).hexdigest();engine=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
  if out.exists():
   old=json.loads(out.read_text())
   if old.get('input_sha256')==digest and old.get('engine_sha256')==engine and old['samples']==N:return c['id']+' reused'
  tmp=out.with_suffix('.tmp');log=R/'.local'/f'{model}_{c["id"]}.log'
  with inp.open('rb') as fin,tmp.open('wb') as fout,log.open('wb') as err:subprocess.run([str(R/'.local/build/event_simulation'),str(N)],stdin=fin,stdout=fout,stderr=err,check=True)
  raw=json.loads(tmp.read_text());assert raw['samples']==N and raw['seed']==c['year'];assert all(sum(v[2] for v in bins)==N for bins in raw['counts']);assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N
  raw.update(input_sha256=digest,engine_sha256=engine,model=model);tmp.write_text(json.dumps(raw,indent=2)+'\n');tmp.replace(out)
  return model+' '+c['id']+' complete '+str(raw['seconds'])+'s'
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  fs=[pool.submit(run,j) for j in jobs]
  for f in concurrent.futures.as_completed(fs):print(f.result(),flush=True)
if __name__=='__main__':main()

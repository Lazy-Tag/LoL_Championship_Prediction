"""Frozen event-start shared-series model, identical rules/ratings to baseline."""
import concurrent.futures,hashlib,json,subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions,domestic_region
from candidate_models import DynamicBT
from evaluate_form_chain import fit_rho,conditional_series
from build_chain_engine import source
R=Path(__file__).resolve().parents[1];OUT=R/'results/chain_events';N=14_000_605

def prepare():
 OUT.mkdir(exist_ok=True);configs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];seasons={};regions={};events=[]
 for s in range(3,16):
  seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
  if s>3:
   for t,v in regions[s-1].items():regions[s].setdefault(t,v)
 for s in range(4,16):
  rows=seasons[s];teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regions[s-1],90)
  model=DynamicBT(teams,regions[s],prior);byday=defaultdict(list);ed=defaultdict(list);records=[];latest=None
  for r in rows:byday[r['date']].append(r)
  for c in configs:
   if c['season']==s:ed[c['start_date']].append(c)
  for ds in sorted(set(byday)|set(ed)):
   day=date.fromisoformat(ds);model.advance(day);theta=model.strengths()
   for c in ed[ds]:
    assert latest is None or latest<ds
    assert all(abs(theta[t]-c['strength'][t])<1e-9 for t in c['teams'])
    rho=fit_rho(records,day);base=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text()
    n=len(c['teams']);p=[[float(expit(theta[a]-theta[b])) for b in c['teams']] for a in c['teams']]
    tables={bo:[[conditional_series(v,rho,bo) for v in row] for row in p] for bo in [3,5]}
    text=base.rstrip()+'\nSERIES_PROBABILITIES_V1\n'+'\n'.join(' '.join(map(str,row)) for bo in [3,5] for row in tables[bo])+'\n'
    (OUT/f'{c["id"]}.txt').write_text(text)
    events.append({**c,'model':'shared_series90','rho':rho,'rho_training_domestic_series':len(records),'rho_latest_training_date':max((r[0].isoformat() for r in records),default=None),'base_input_sha256':hashlib.sha256(base.encode()).hexdigest()})
   for r in byday[ds]:
    if domestic_region(r['tournament']) is not None:records.append((day,theta[r['team1']]-theta[r['team2']],0.,r['wins1'],r['wins2'],0.))
   model.update(byday[ds])
   if byday[ds]:latest=ds
  print('Prepared S',s,flush=True)
 (OUT/'event_configs.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n');return events

def verify_engine(events):
 # Old input behavior must reproduce original engine for every vintage format.
 for c in events:
  inp=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_bytes()
  a=json.loads(subprocess.check_output([str(R/'.local/build/event_simulation'),'1000'],input=inp));b=json.loads(subprocess.check_output([str(R/'.local/build/event_chain'),'1000'],input=inp))
  for k in ['counts','seed','samples','duration_seeded_ties','complex_tie_scenarios','draw_waivers']:assert a[k]==b[k],(c['id'],k)
 print('PASS original and extended engine: identical 1000-draw paths for all 23 events',flush=True)

def main():
 events=prepare();verify_engine(events);engine=hashlib.sha256(source().encode()).hexdigest()
 def run(c):
  inp=OUT/f'{c["id"]}.txt';out=inp.with_suffix('.json');digest=hashlib.sha256(inp.read_bytes()).hexdigest()
  if out.exists():
   old=json.loads(out.read_text())
   if old.get('input_sha256')==digest and old.get('engine_sha256')==engine and old.get('samples')==N:return c['id']+' reused'
  tmp=out.with_suffix('.tmp');log=R/'.local'/f'chain_{c["id"]}.log'
  with inp.open('rb') as fin,tmp.open('wb') as fout,log.open('wb') as err:subprocess.run([str(R/'.local/build/event_chain'),str(N)],stdin=fin,stdout=fout,stderr=err,check=True)
  raw=json.loads(tmp.read_text());assert raw['samples']==N and raw['seed']==c['year']
  assert all(sum(k for lo,hi,k in bins)==N for bins in raw['counts'])
  assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==N
  assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*len(c['teams'])*(len(c['teams'])+1)
  raw.update(model='shared_series90',rho=c['rho'],input_sha256=digest,engine_sha256=engine,base_engine_sha256=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest());tmp.write_text(json.dumps(raw,indent=2)+'\n');tmp.replace(out)
  return c['id']+' complete '+str(raw['seconds'])+'s'
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(run,events):print(result,flush=True)
if __name__=='__main__':main()

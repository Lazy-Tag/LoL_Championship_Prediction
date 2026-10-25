"""Prepare fixed, independent memory candidates and 23-event formal simulations."""
import concurrent.futures,hashlib,json,subprocess,sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from scipy.special import expit
from candidate_models import DynamicBT
from adaptive_memory_models import TwoMemory,RosterShock
from backtest import load_season,affiliations,prior_regions
from evaluate_detail_features import reconcile
from roster_carry_model import profile
from model import series_probability
R=Path(__file__).resolve().parents[1];D=R/'results/memory_weights';N=14_000_605

def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def input_hashes():
 paths=[R/'results/model_experiments/event_configs.json',R/'results/model_experiments/predictions.json']
 for season in range(3,16):
  paths.extend([R/f'data/history/S{season}/series.json',R/f'data/detailed/S{season}_games.jsonl',R/f'data/enrichment/S{season}_audit.json'])
 return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}

def prepare():
 D.mkdir(exist_ok=True);cs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];base=json.loads((R/'results/model_experiments/predictions.json').read_text());seasons={};regions={};states={'dual':[],'roster_shock':[]};pred=[];audits=[];coverage=[];previous_profiles={}
 protect=['results/main_model.json','results/live_s16/latest.json','results/model_experiments/dynamic90/2026_Worlds.json'];hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protect}
 for s in range(3,16):
  rows,_=load_season(s);seasons[s]=rows;regions[s]=affiliations(rows,s)
  if s>3:
   for t,v in regions[s-1].items():regions[s].setdefault(t,v)
  matched,audit=reconcile(s,rows);byday=defaultdict(list);td=defaultdict(list);ed=defaultdict(list);profiles={};player_teams=defaultdict(set)
  for r in rows:byday[r['date']].append(r)
  for day,rr in byday.items():
   gg=defaultdict(list)
   for r in rr:
    for g in matched.get(r['detail'],[]):
     gg[g['a']].append(g);gg[g['b']].append(g)
   profiles[day]={}
   for team,games in gg.items():
    p=profile(games,team)
    if p:
     profiles[day][team]=dict(date=day,**p)
     for name in p['shares']:player_teams[name].add(team)
  coverage.append(dict(season=s,matched_maps=audit['counts']['matched_maps'],lineup_days=sum(len(v) for v in profiles.values()),named_players=len(player_teams),players_multiple_teams=sum(len(v)>1 for v in player_teams.values())))
  if s==3:
   for day in sorted(profiles):previous_profiles.update(profiles[day])
   continue
  prior,_=prior_regions(seasons[s-1],regions[s-1],90);teams=sorted({r[k] for r in rows for k in ('team1','team2')})
  # No cross-season strength inheritance; only observed metadata is retained.
  prev={t:v for t,v in previous_profiles.items() if t in teams and regions[s].get(t)==regions[s-1].get(t)}
  models={'baseline':DynamicBT(teams,regions[s],prior),'dual':TwoMemory(teams,regions[s],prior),'roster_shock':RosterShock(teams,regions[s],prior)}
  for r in base:
   if r['season']==s:td[r['date']].append(r)
  for c in cs:
   if c['season']==s:ed[c['start_date']].append(c)
  last=None
  for day in sorted(set(byday)|set(td)|set(ed)):
   for m in models.values():m.advance(date.fromisoformat(day))
   strength={name:m.strengths() for name,m in models.items()}
   for r in td[day]:
    probs={name:float(series_probability(float(expit(th[r['team1']]-th[r['team2']])),r['best_of'])) for name,th in strength.items()}
    assert abs(float(expit(strength['baseline'][r['team1']]-strength['baseline'][r['team2']]))-r['dynamic90'])<1e-9
    pred.append(dict(season=s,date=day,event=r['event'],detail=r['detail'],team1=r['display1'],team2=r['display2'],wins1=r['wins1'],wins2=r['wins2'],probabilities=probs))
   for c in ed[day]:
    assert last is None or last<day
    assert all(abs(strength['baseline'][t]-c['strength'][t])<1e-9 for t in c['teams'])
    for name in states:states[name].append({**{k:v for k,v in c.items() if k!='gradient'},'model':name,'strength':{t:strength[name][t] for t in c['teams']},'latest_training_date':last,'latest_roster_observation':max((v['date'] for v in prev.values()),default=None)})
   # These metadata become available only AFTER today's forecasts are saved.
   for a in models['roster_shock'].observe_rosters(profiles.get(day,{}),prev):audits.append(dict(season=s,**a))
   for m in models.values():m.update(byday[day])
   if byday[day]:last=day
  previous_profiles=prev
  print('prepared',s,'shocks',sum(a['season']==s for a in audits),flush=True)
 save(D/'event_configs.json',states);save(D/'predictions.json',pred);save(D/'roster_changes.json',audits);save(D/'protocol.json',dict(coverage=coverage,unchanged_hashes=hashes,input_hashes=input_hashes(),dual=dict(long_days=180,short_days=30,short_variance_share=.25,total_stationary_team_variance=.75**2),roster_shock=dict(scale=.75**2,max_observation_gap_days=180,mean_shift=0,observed_after_daily_predictions=True),parameters_tuned=False))
 return states

def simulate(states):
 jobs=[];engine=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
 for mode,cs in states.items():
  folder=D/mode;folder.mkdir(exist_ok=True)
  for c in cs:
   lines=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();n=len(c['teams']);th=[c['strength'][t] for t in c['teams']];lines[2:2+n]=[' '.join(str(float(expit(a-b))) for b in th) for a in th];inp=folder/f'{c["id"]}.txt';inp.write_text('\n'.join(lines)+'\n');jobs.append((mode,c,inp))
 def run(job):
  mode,c,inp=job;out=inp.with_suffix('.json');digest=hashlib.sha256(inp.read_bytes()).hexdigest()
  if out.exists():
   raw=json.loads(out.read_text())
   if raw.get('input_sha256')==digest and raw.get('engine_sha256')==engine and raw['samples']==N:return mode+' '+c['id']+' reused'
  tmp=out.with_suffix('.tmp')
  with inp.open('rb') as fin,tmp.open('wb') as fout,(R/'.local'/f'memory_{mode}_{c["id"]}.log').open('wb') as err:subprocess.run([str(R/'.local/build/event_simulation'),str(N)],stdin=fin,stdout=fout,stderr=err,check=True)
  raw=json.loads(tmp.read_text());assert raw['samples']==N and raw['seed']==c['year'];assert all(sum(v[2] for v in bins)==N for bins in raw['counts']);assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N
  raw.update(input_sha256=digest,engine_sha256=engine,model=mode);save(tmp,raw);tmp.replace(out)
  return mode+' '+c['id']+' '+str(raw['seconds'])+'s'
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for item in pool.map(run,jobs):print(item,flush=True)
if __name__=='__main__':
 states=json.loads((D/'event_configs.json').read_text()) if '--resume' in sys.argv else prepare()
 if '--prepare-only' not in sys.argv:simulate(states)

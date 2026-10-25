"""Recheck dated dynamic90 live snapshots without importing later observations."""
import json,hashlib,subprocess,concurrent.futures,fcntl
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import numpy as np
from scipy.special import expit
from update_live_s16 import ROOT,OUT,LOCAL,REPORT,N,fit,build_state,verify,report,save,WORLD_TEAMS,key,series_probability

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(path):
 d=json.loads(path.read_text());assert d['model']=='dynamic90' and d['simulations']==N and d['seed']==2026;now=datetime.fromisoformat(d['as_of']);events={e['id']:{k:v for k,v in e.items() if k not in ('round','a','b','win_probability')} for e in d['completed_worlds']+d['next_matches']}
 for row in d['added_training']:
  if row['id'] not in events:
   events[row['id']]=dict(id=row['id'],start_utc=row['start_utc'],event=row['event'],stage=row['stage'],state='completed',best_of=row['best_of'],teams=[dict(name=row['team1'],code='',wins=row['wins1']),dict(name=row['team2'],code='',wins=row['wins2'])],source=row['source'])
 events=sorted(events.values(),key=lambda e:(e['start_utc'],e['id']))
 for e in events:
  if e['state']=='completed':assert datetime.fromisoformat(e['start_utc'].replace('Z','+00:00'))<=now
 active,w,l,met,done,fixed=build_state(events,now);assert (active,w,l,met)==(d['active'],d['wins'],d['losses'],d['met']);assert [r['id'] for r in fixed]==[r['id'] for r in d['next_matches']]
 theta,added,audit,total=fit(events,now);assert total==d['total_training_series'];assert added==d['added_training'];error=max(abs(theta[t]-v) for t,v in d['strengths'].items());assert error<1e-9
 matrices=np.array([[[float(series_probability(expit(theta[key(t[0])]-theta[key(u[0])]),bo)) for u in WORLD_TEAMS.values()] for t in WORLD_TEAMS.values()] for bo in (1,3,5)]);assert np.max(abs(matrices-np.array(d['probabilities'])))<1e-9
 inp=path.with_name('input.txt');assert digest(inp)==d['input_sha256'];assert digest(ROOT/'scripts/simulate_live.cpp')==d['engine_sha256']
 # Reuse the archived decimal representation after checking the refitted model.
 # This prevents harmless floating-point drift from changing the random stream.
 with inp.open('rb') as stream:
  run=subprocess.run([str(LOCAL/'simulate_live'),str(N),'2026'],stdin=stream,capture_output=True,check=True)
 raw=json.loads(run.stdout)
 for field in ['counts','joint','simulations','seed','waived_draw_groups']:assert raw[field]==d[field],(path,field)
 verify(d)
 return d,dict(snapshot=path.parent.name,as_of=d['as_of'],completed_worlds=len(d['completed_worlds']),completed_swiss=len(d['completed_swiss']),training_series=total,refit_max_strength_error=error,counts_identical=True,joint_identical=True,samples=N,seed=2026,input_sha256=d['input_sha256'],forecast_sha256=digest(path))

def main():
 paths=sorted(OUT.glob('*/forecast.json'));assert paths
 protected=[ROOT/'results/main_model.json',OUT/'latest.json',OUT/'observed_events.json'];before={p:digest(p) for p in protected}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(replay,paths))
 for d,audit in results:
  filename=datetime.fromisoformat(d['as_of']).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat()+'.md';report(d,filename);print('Verified and refreshed',filename,flush=True)
 assert all(digest(p)==h for p,h in before.items())
 save(OUT/'historical_replay_audit.json',dict(checked_at=datetime.now(timezone.utc).isoformat(),model='dynamic90',snapshots=[a for _,a in results],latest_pointer_unchanged=True))
if __name__=='__main__':
 with (LOCAL/'update.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  main()

"""Independent invariance and audit tests for memory candidates."""
import hashlib,json,sys
from datetime import date,timedelta
import numpy as np
from candidate_models import DynamicBT
from adaptive_memory_models import TwoMemory,RosterShock
from run_memory_weights import R,D,N

def unit():
 teams=['a','b'];regs={'a':'KR','b':'CN'};base=DynamicBT(teams,regs,{});dual=TwoMemory(teams,regs,{},90,90);start=date(2020,1,1)
 H=np.zeros((4,6));H[:4,:4]=np.eye(4);H[2:,4:]=np.eye(2)
 for k in (0,1,7,60,200):
  day=start+timedelta(days=k);rows=[dict(team1='a',team2='b',wins1=2,wins2=1,date=day.isoformat())]
  base.advance(day);dual.advance(day);assert np.allclose(base.m,H@dual.m,atol=1e-8);assert np.allclose(base.C,H@dual.C@H.T,atol=1e-8)
  base.update(rows);dual.update(rows);assert np.allclose(base.m,H@dual.m,atol=1e-8);assert np.allclose(base.C,H@dual.C@H.T,atol=1e-8)
 shock=RosterShock(teams,regs,{});shock.advance(start);m=shock.m.copy();c=shock.C.copy()
 previous={'a':dict(date='2019-12-31',shares=dict(p=.2,q=.2,r=.2,s=.2,t=.2))}
 current={'a':dict(date='2020-01-01',shares=dict(p=.2,q=.2,r=.2,u=.2,v=.2))}
 a=shock.observe_rosters(current,previous);assert np.array_equal(shock.m,m);assert abs(a[0]['retention']-.6)<1e-12
 expected=c.copy();expected[2,2]+=.75**2*.4;assert np.allclose(shock.C,expected) and np.linalg.eigvalsh(shock.C).min()>0
 assert not shock.observe_rosters(current,previous)
 assert not shock.observe_rosters({'b':dict(date='2020-01-01',shares={'unknown':1})},previous)
 print('PASS dual 90/90 reduces to original mean AND covariance; lineup shock leaves mean fixed, overlap/variance correct, no duplicate same-day shock, missing roster excluded')

def full():
 cs=json.loads((D/'event_configs.json').read_text());protocol=json.loads((D/'protocol.json').read_text());pred=json.loads((D/'predictions.json').read_text());audit=json.loads((D/'roster_changes.json').read_text())
 assert len(pred)==len({r['detail'] for r in pred})==1300
 for a in audit:assert 0<a['added_variance']<=.75**2 and a['previous_date']<a['observed_date'] and abs(a['added_variance']-.75**2*(1-a['retention']))<1e-12
 engine=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
 for mode,events in cs.items():
  assert len(events)==23
  for c in events:
   assert c['latest_training_date']<c['start_date']
   assert c['latest_roster_observation'] is None or c['latest_roster_observation']<c['start_date']
   p=D/mode/f'{c["id"]}.json';raw=json.loads(p.read_text());assert raw['samples']==N and raw['seed']==c['year']
   assert raw['engine_sha256']==engine and raw['input_sha256']==hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest()
   n=len(c['teams']);assert all(sum(v[2] for v in bins)==N for bins in raw['counts'])
   assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N
   assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
   old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();new=p.with_suffix('.txt').read_text().splitlines();assert old[:2]==new[:2] and old[2+n:]==new[2+n:]
   if mode=='roster_shock' and c['season']<=5:
    assert old==new
    baseline=json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json').read_text());assert raw['counts']==baseline['counts']
 for p,h in {**protocol['input_hashes'],**protocol['unchanged_hashes']}.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
 summary=json.loads((D/'summary.json').read_text())
 from report_chain_events import evaluate
 for e in summary['events']:
  for mode in ['baseline','dual','roster_shock']:
   c=next(c for c in cs['dual' if mode=='baseline' else mode] if c['id']==e['id'])
   path=R/f'results/model_experiments/dynamic90/{c["id"]}.json' if mode=='baseline' else D/mode/f'{c["id"]}.json'
   actual=evaluate(c,json.loads(path.read_text()))
   for k in ['champion_logloss','champion_brier','champion_hit','finish_mae','finish_spearman']:assert abs(actual[k]-e['models'][mode][k])<1e-12
 for mode,values in summary['summary'].items():
  for k,v in values.items():assert abs(v-np.mean([e['models'][mode][k] for e in summary['events']]))<1e-12
 print('PASS 46 full simulations, all years/seeds/14,000,605 counts, rank conservation, same rules, input hashes, 1300 unique forecasts, strict chronology, unchanged main/S16/live')
if __name__=='__main__':
 unit()
 if '--unit' not in sys.argv:full()

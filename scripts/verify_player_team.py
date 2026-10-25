"""Source-ID identities, state transport, conservation, and exact fallbacks."""
from datetime import date,timedelta
import hashlib,json,sys
import numpy as np
from candidate_models import DynamicBT
from player_team_model import PlayerTeam
from run_player_team import R,D,MODES
from report_chain_events import evaluate

def unit():
 teams=['a','b'];regions={'a':'KR','b':'CN'};base=DynamicBT(teams,regions,{});m=PlayerTeam(teams,regions,{},[]);H=np.zeros((4,6));H[:4,:4]=np.eye(4);H[2:,4:]=np.eye(2);start=date(2020,1,1)
 for k in [0,1,30,90]:
  day=start+timedelta(days=k);rr=[dict(team1='a',team2='b',wins1=2,wins2=1,date=day.isoformat())]
  base.advance(day);m.advance(day);base.update(rr);m.update(rr)
  assert np.allclose(m.m@H.T,base.m,atol=1e-8) and np.allclose(H@m.C@H.T,base.C,atol=1e-8)
 players=[f'oe:player:p{i}|top' for i in range(5)];old=PlayerTeam(teams,regions,{},players);old.advance(date(2020,12,1));old.m[old.pi[players[0]]]=1.;old.m[old.nr]=.7;lineup={p:.2 for p in players}
 assert abs(old.strength('a',lineup)-old.strength('b',lineup)-.7)<1e-12
 new=PlayerTeam(teams,regions,{},players,old,True,date(2021,1,1));reset=PlayerTeam(teams,regions,{},players,old,False,date(2021,1,1));rho=2**(-31/90)
 assert abs(new.m[new.pi[players[0]]]-rho)<1e-12 and new.m[new.nr]==0 and np.all(reset.m==0)
 assert np.linalg.eigvalsh(new.C).min()>0
 # New-lineup initial total team variance matches baseline; no arbitrary extra variance.
 v=np.zeros(len(new.m))
 fresh=PlayerTeam(teams,regions,{},players)
 for j,x in fresh.vector('a',lineup).items():v[j]=x
 assert abs(v@fresh.C@v-(.5**2+.75**2))<1e-12
 swap=PlayerTeam(teams,regions,{},[players[0].replace('|top','|mid')],old,True,date(2021,1,1));assert np.all(swap.m==0)
 print('PASS missing-lineup exact baseline mean/covariance, player mobility without club residual, cross-year role skill decay/reset, role-switch isolation, conserved initial variance, positive covariance')

def full():
 protocol=json.loads((D/'protocol.json').read_text());configs=json.loads((D/'event_configs.json').read_text());reg=json.loads((D/'identity_registry.json').read_text());pred=json.loads((D/'predictions.json').read_text());N=14_000_605
 assert len(pred)==len({r['detail'] for r in pred})==1300
 assert all(pid.startswith('oe:player:') and not pid.split(':')[-1].isdigit() for pid in reg)
 assert len(configs[MODES[0]])==len(configs[MODES[1]])==23
 comp=json.loads((D/'event_components.json').read_text())
 for r in comp:
  assert r['lineup_date'] is None or r['lineup_date']<r['date']
  assert r['lineup_date'] is None or (date.fromisoformat(r['date'])-date.fromisoformat(r['lineup_date'])).days<=45
  assert abs(r['components']['total']-sum(r['components'][k] for k in ['region','team_residual','player_or_unknown_component']))<1e-10
  for p in r['players']:assert p['player_role'].split('|')[0] in reg
 for r in json.loads((D/'transports.json').read_text()):
  assert r['model']=='player_carry' and r['previous_date']<r['start_date']
  assert abs(r['coefficient']-2**(-(date.fromisoformat(r['start_date'])-date.fromisoformat(r['previous_date'])).days/90))<1e-12
 engine=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
 for mode,cs in configs.items():
  for c in cs:
   assert c['latest_training_date']<c['start_date'];n=len(c['teams']);p=D/mode/f'{c["id"]}.json';raw=json.loads(p.read_text());assert raw['samples']==N and raw['seed']==c['year']
   assert raw['engine_sha256']==engine and raw['input_sha256']==hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest()
   old=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();new=p.with_suffix('.txt').read_text().splitlines();assert old[:2]==new[:2] and old[2+n:]==new[2+n:]
   assert all(sum(v[2] for v in bins)==N for bins in raw['counts']);assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N
   assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
   if c.get('fallback'):assert old==new and raw['counts']==json.loads((R/f'results/model_experiments/dynamic90/{c["id"]}.json').read_text())['counts']
 for e in ['2020_MSC','2020_Worlds']:
  assert json.loads((D/MODES[0]/f'{e}.json').read_text())['counts']==json.loads((D/MODES[1]/f'{e}.json').read_text())['counts']
 for p,h in {**protocol['input_hashes'],**protocol['unchanged_hashes']}.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
 if (D/'summary.json').exists():
  summary=json.loads((D/'summary.json').read_text())
  for e in summary['events']:
   for mode in ['baseline']+MODES:
    c=next(c for c in configs[MODES[0] if mode=='baseline' else mode] if c['id']==e['id']);p=R/f'results/model_experiments/dynamic90/{e["id"]}.json' if mode=='baseline' else D/mode/f'{e["id"]}.json';a=evaluate(c,json.loads(p.read_text()))
    for k in ['champion_logloss','champion_brier','champion_hit','finish_mae','finish_spearman']:assert abs(a[k]-e['models'][mode][k])<1e-12
 print('PASS 23 events per arm, 1300 forecasts, 11 exact fallback events, 2020 reset/carry identity, verified source IDs and roles, prior-day lineup freshness, cross-year transport, simulation counts/seeds/ranks, hashes and unchanged main/live/S16')
if __name__=='__main__':
 unit()
 if '--unit' not in sys.argv:full()

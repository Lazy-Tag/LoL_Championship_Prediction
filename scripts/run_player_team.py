"""Identity audit, daily player filtering, and paired formal event replay."""
import csv,io,json,re,zipfile,hashlib,sys
from collections import defaultdict,Counter
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions
from evaluate_detail_features import reconcile
from candidate_models import DynamicBT
from player_team_model import PlayerTeam,ROLE
from roster_carry_model import player_key
from model import series_probability
import run_memory_weights as runner
R=Path(__file__).resolve().parents[1];D=R/'results/player_team'
MODES=['player_reset','player_carry'];ROLEMAP={'top':'top','jng':'jng','jungle':'jng','jungler':'jng','mid':'mid','middle':'mid','bot':'bot','adc':'bot','ad carry':'bot','sup':'sup','support':'sup'}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def source_ids():
 out={};counts=Counter();names=defaultdict(set)
 with zipfile.ZipFile(R/'data/raw/detailed/annual_2020_2025.zip') as z:
  for name in z.namelist():
   if not name.endswith('.csv'):continue
   year=int(name[:4]);group=defaultdict(list)
   for row in csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig')):
    role=ROLEMAP.get(row.get('position','').lower());pid=row.get('playerid','');side=row.get('side','').lower()
    if role is None:continue
    gid=row['gameid'];match=re.search(r'match-details/([^?&#]+)',row.get('url',''))
    if match:gid=match[1]
    group[gid].append(dict(role=role,id=pid,name=row.get('playername',''),side=side))
   out[year]={}
   for gid,rows in group.items():
    if len(rows)!=10 or len({p['id'] for p in rows})!=10 or any(not re.fullmatch(r'oe:player:[a-zA-Z0-9]+',p['id']) for p in rows) or any({p['role'] for p in rows if p['side']==side}!=set(ROLE) for side in ['blue','red']):counts['invalid_source_maps']+=1;continue
    out[year][gid]={(p['side'],p['role']):p for p in rows};counts['valid_source_maps']+=1
    for p in rows:names[p['id']].add(p['name'])
 return out,counts,names

def prepare():
 D.mkdir(exist_ok=True);rawids,idcounts,all_names=source_ids();cs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];base=json.loads((R/'results/model_experiments/predictions.json').read_text());seasons={};regions={};configs={m:[] for m in MODES};pred=[];coverage=[];rejected=[];transports=[];event_players=[];registry=defaultdict(lambda:dict(names=set(),roles=set(),teams=set(),seasons=set(),first=None,last=None));previous={m:None for m in MODES};lineup_audit=[]
 protect=['results/main_model.json','results/live_s16/latest.json','results/model_experiments/dynamic90/2026_Worlds.json'];hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protect}
 for s in range(3,16):
  rows,_=load_season(s);seasons[s]=rows;regions[s]=affiliations(rows,s)
  if s>3:
   for t,v in regions[s-1].items():regions[s].setdefault(t,v)
  if s<10:
   for c in cs:
    if c['season']==s:
     for m in MODES:configs[m].append({**c,'model':m,'fallback':'No trustworthy source player IDs; original dynamic90'})
   for r in base:
    if r['season']==s:
     p=float(series_probability(r['dynamic90'],r['best_of']));pred.append(dict(season=s,date=r['date'],event=r['event'],detail=r['detail'],team1=r['display1'],team2=r['display2'],wins1=r['wins1'],wins2=r['wins2'],probabilities={m:p for m in ['baseline']+MODES},known_lineups=[False,False],fallback=True))
   continue
  matched,audit=reconcile(s,rows);verified={};players=set();count=Counter()
  for ident,gg in matched.items():
   usable=[]
   for g in gg:
    src=rawids[s+2010].get(g['game_id']);lineups={};valid=src is not None
    for side in ['blue','red']:
     lineup={};ps=g['teams'][side]['players']
     if len(ps)!=5:valid=False
     for p in ps:
      role=ROLEMAP.get((p.get('role') or '').lower());rec=src.get((side,role)) if src else None
      if rec is None or player_key(rec['name'])!=player_key(p.get('name') or ''):valid=False;continue
      lineup[rec['id']+'|'+role]=.2
     if len(lineup)!=5:valid=False
     lineups[side]=lineup
    if valid:
     usable.append((g,lineups));count['id_verified_maps']+=1
     for side in ['blue','red']:
      team=g['a'] if side=='blue' else g['b']
      for pr in lineups[side]:
       players.add(pr);pid,role=pr.split('|');rec=src[(side,role)];z=registry[pid];z['names'].add(rec['name']);z['roles'].add(role);z['teams'].add(team);z['seasons'].add(s);ds=g['date'][:10];z['first']=min(z['first'] or ds,ds);z['last']=max(z['last'] or ds,ds)
    else:count['id_rejected_maps']+=1;rejected.append(dict(season=s,game_id=g['game_id'],date=g['date'],reason='missing/conflicting stable source IDs, role layout, or normalized name'))
   # All maps must have verified identity, otherwise retain aggregate series once.
   if len(usable)==len(gg):verified[ident]=usable
   else:count['series_fallback']+=1
  byday=defaultdict(list);td=defaultdict(list);ed=defaultdict(list)
  for r in rows:byday[r['date']].append(r)
  for r in base:
   if r['season']==s:td[r['date']].append(r)
  for c in cs:
   if c['season']==s:ed[c['start_date']].append(c)
  teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regions[s-1],90);start=date.fromisoformat(min(byday));models={m:PlayerTeam(teams,regions[s],prior,players,previous[m],m=='player_carry',start) for m in MODES};baseline=DynamicBT(teams,regions[s],prior);latest={};last=None
  for m,obj in models.items():transports.extend(dict(season=s,model=m,**v) for v in obj.transport)
  def known(t,day):
   v=latest.get(t)
   return v['shares'] if v and 0<(date.fromisoformat(day)-date.fromisoformat(v['date'])).days<=45 else None
  for ds in sorted(set(byday)|set(td)|set(ed)):
   for model in [baseline]+list(models.values()):model.advance(date.fromisoformat(ds))
   bth=baseline.strengths();th={m:{t:obj.strength(t,known(t,ds)) for t in teams} for m,obj in models.items()}
   for r in td[ds]:
    probs={'baseline':float(series_probability(float(expit(bth[r['team1']]-bth[r['team2']])),r['best_of']))}
    assert abs(float(expit(bth[r['team1']]-bth[r['team2']]))-r['dynamic90'])<1e-9
    probs.update({m:float(series_probability(float(expit(v[r['team1']]-v[r['team2']])),r['best_of'])) for m,v in th.items()})
    pred.append(dict(season=s,date=ds,event=r['event'],detail=r['detail'],team1=r['display1'],team2=r['display2'],wins1=r['wins1'],wins2=r['wins2'],probabilities=probs,known_lineups=[bool(known(t,ds)) for t in [r['team1'],r['team2']]],fallback=False))
   for c in ed[ds]:
    assert last<ds
    for m,obj in models.items():
     configs[m].append({**{k:v for k,v in c.items() if k!='gradient'},'model':m,'strength':{t:th[m][t] for t in c['teams']},'latest_training_date':last,'fallback':None,'lineup_dates':{t:latest[t]['date'] if known(t,ds) else None for t in c['teams']}})
     for t in c['teams']:
      lu=known(t,ds);event_players.append(dict(event_id=c['id'],model=m,team=t,name=c['display'][t],date=ds,lineup_date=latest[t]['date'] if lu else None,components=obj.components(t,lu),players=[dict(player_role=p,share=share,mean=float(obj.m[obj.pi[p]]),sd=float(np.sqrt(obj.C[obj.pi[p],obj.pi[p]]))) for p,share in (lu or {}).items()]))
   obs=[];day_lineups=defaultdict(Counter);mapcount=Counter()
   for r in byday[ds]:
    if r['detail'] in verified:
     for g,lineups in verified[r['detail']]:
      a='blue' if g['a']==r['team1'] else 'red';b='red' if a=='blue' else 'blue';win=g['teams'][a]['win'];obs.append(dict(team1=r['team1'],team2=r['team2'],wins1=win,wins2=1-win,date=ds,lineup1=lineups[a],lineup2=lineups[b]))
      for t,side in [(r['team1'],a),(r['team2'],b)]:day_lineups[t].update(lineups[side]);mapcount[t]+=1
    else:obs.append({**r,'lineup1':None,'lineup2':None})
   assert sum(r['wins1']+r['wins2'] for r in obs)==sum(r['wins1']+r['wins2'] for r in byday[ds])
   for obj in models.values():obj.update(obs)
   baseline.update(byday[ds])
   # Only after today's entire prediction batch and score assimilation.
   for t,shares in day_lineups.items():
    latest[t]=dict(date=ds,shares={p:v/mapcount[t] for p,v in shares.items()});lineup_audit.append(dict(season=s,team=t,**latest[t]))
   if byday[ds]:last=ds
  previous=models;coverage.append(dict(season=s,training_series=len(rows),training_maps=sum(r['wins1']+r['wins2'] for r in rows),matched_maps=audit['counts']['matched_maps'],verified_series=len(verified),usable_maps=sum(len(v) for v in verified.values()),player_role_states=len(players),max_gradient={m:obj.max_gradient for m,obj in models.items()},**count))
  print('prepared S',s,'players',len(players),'known maps',coverage[-1]['usable_maps'],flush=True)
 registry={pid:{k:sorted(v) if isinstance(v,set) else v for k,v in z.items()} for pid,z in registry.items()}
 for name,obj in [('event_configs',configs),('predictions',pred),('identity_registry',registry),('rejected_identities',rejected),('transports',transports),('event_components',event_players),('lineup_history',lineup_audit)]:save(D/(name+'.json'),obj)
 save(D/'protocol.json',dict(coverage=coverage,source_id_audit=dict(idcounts),unchanged_hashes=hashes,input_hashes={**runner.input_hashes(),'data/raw/detailed/annual_2020_2025.zip':hashlib.sha256((R/'data/raw/detailed/annual_2020_2025.zip').read_bytes()).hexdigest()},parameters=dict(half_life=90,team_residual_variance=.75**2/2,unknown_lineup_variance=.75**2/2,player_role_variance=.75**2*2.5,max_lineup_age_days=45),parameters_tuned=False))
 return configs
if __name__=='__main__':
 configs=json.loads((D/'event_configs.json').read_text()) if '--resume' in sys.argv else prepare()
 if '--prepare-only' not in sys.argv:
  runner.D=D;runner.simulate(configs)

"""Conservative OE map enrichment: retain conflicts, never double count matches.
Public mirrors are observations, not proof of completeness. Only exactly
reconciled maps enrich existing rows; new training games require known clubs,
a top-tier domestic league and no nearby existing pairing.
"""
import csv,gzip,hashlib,json
from collections import defaultdict,Counter
from datetime import date,datetime
from pathlib import Path
from backtest import load_season,key
R=Path(__file__).resolve().parents[1];OUT=R/'data/enrichment'
SOURCES=[(15,'data/raw/enrichment/oe_2025.csv.gz','https://raw.githubusercontent.com/cbplexiglass/LoL-Esports-Regional-Analyses/main/2025_LoL_esports_match_data_from_OraclesElixir.csv'),(16,'data/raw/oe_mirror_2026.csv',None)]
DOMESTIC={15:{'LCK','LPL','LEC','LCP','LTA N','LTA S','LTA'},16:{'LCK','LPL','LEC','LCP','LCS','CBLOL'}}
# Lexical/sponsorship aliases scoped to these two seasons; no roster identity inference.
ALIASES={'geng':'gengesports','cloud9kia':'cloud9','redcanids':'redkalunga','j d gaming':'jdgaming','movistarkoi':'movistarkoi'}
STATS=['gamelength','kills','deaths','totalgold','golddiffat10','golddiffat15','xpdiffat15','csdiffat15','dragons','barons','towers','firstdragon','firstbaron']
def main():
 OUT.mkdir(exist_ok=True);audits=[]
 historical=[(y-2010,f'data/raw/enrichment/worlds_{y}.csv',f'https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/{y}_LoL_esports_match_data_from_OraclesElixir.csv') for y in range(2016,2023) if (R/f'data/raw/enrichment/worlds_{y}.csv').exists()]
 for season,path,url in historical+SOURCES:
  p=R/path;raw=gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes()
  rows=list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
  for r in rows:
   if '/' in r['date']:r['date']=datetime.strptime(r['date'],'%m/%d/%Y %H:%M').isoformat(sep=' ')
  if season<16:base,_=load_season(season)
  else:
   base=[{**r,'team1':key(r['team1']),'team2':key(r['team2']),'display1':r['team1'],'display2':r['team2'],'detail':r['id']} for r in json.loads((R/'data/series.json').read_text())]
  known={r[k] for r in base for k in ['team1','team2']};aliases={t:t for t in known}
  for a,b in ALIASES.items():
   if b in known:aliases[key(a)]=b
   if a in known:aliases[key(b)]=a
  historical_aliases={
   6:{'Counter Logic Gaming':'CLG','ahq eSports Club':'ahq eSports','INTZ':'INTZ eSports','TSM':'Team SoloMid'},
   7:{'FenerbahÃ§e Esports':'1907 Fenerbahce','Misfits Gaming':'Misfits','GAM Esports':'GIGABYTE Marines','TSM':'Team SoloMid'},
   8:{'SuperMassive Esports':'BAUSuperMassive','Kwangdong Freecs':'Afreeca Freecs','Phong VÅ© Buffalo':'Phong Vu Buffalo'},
   9:{'DWG KIA':'DAMWON Gaming','Unicorns of Love.CIS':'Unicorns Of Love','Isurus':'Isurus Gaming','MAMMOTH':'Mammoth eSports'},
   10:{'DWG KIA':'DAMWON Gaming','Unicorns of Love.CIS':'Unicorns Of Love','SuperMassive Esports':'Papara SuperMassive','DRX':'DragonX','INTZ':'INTZ e-Sports'},
   11:{'Unicorns of Love.CIS':'Unicorns Of Love'},
   12:{'Ä°stanbul Wildcats':'Istanbul Wildcats','Chiefs Esports Club':'Chief Esports Club'}}
  for a,b in historical_aliases.get(season,{}).items():
   assert key(b) in known;aliases[key(a)]=key(b)
  if season==15:
   for a,b in {'Oh My God':'OMG','HANJIN BRION':'OK BRION','DN SOOPers':'DN Freecs','ThunderTalk Gaming':'TT','Fluxo W7M':'Fluxo','Isurus Estral':'Isurus'}.items():aliases[key(a)]=key(b)
  if season==16:
   from prepare_data import ALIASES as current_aliases
   for a,b in current_aliases.items():
    if key(b) in known:aliases[key(a)]=key(b)
  games=defaultdict(list)
  for r in rows:
   if r['league'] in DOMESTIC.get(season,set())|{'MSI','WCS','WLDs','FST','EWC'} and (season!=16 or r['date']<'2026-10-14 16:00:00'):games[r['gameid']].append(r)
  maps=[];rejected=[]
  for gid,rr in games.items():
   tt=[r for r in rr if r['position']=='team'];sides={r['side']:r for r in tt}
   if len(tt)!=2 or set(sides)!={'Blue','Red'} or sum(float(r['result']) for r in tt)!=1:
    rejected.append({'gameid':gid,'reason':'invalid team/result structure'});continue
   a,b=sides['Blue'],sides['Red'];ta,tb=aliases.get(key(a['teamname'])),aliases.get(key(b['teamname']))
   if ta is None or tb is None:
    rejected.append({'gameid':gid,'reason':'unresolved team alias','teams':[a['teamname'],b['teamname']]});continue
   players={side:[{k:r.get(k) or None for k in ['position','playername','playerid','champion']} for r in rr if r['position']!='team' and r['side']==side] for side in ['Blue','Red']}
   maps.append(dict(gameid=gid,date=a['date'][:10],timestamp=a['date'],league=a['league'],patch=a['patch'] or None,team1=ta,team2=tb,wins1=int(float(a['result'])),wins2=int(float(b['result'])),source=a['url'],players=players,stats={side:{k:sides[side].get(k) or None for k in STATS} for side in sides}))
  groups=defaultdict(list)
  for m in maps:groups[(m['date'],m['league'],*sorted([m['team1'],m['team2']]))].append(m)
  matched=[];add=[];conflicts=[];used=set()
  for (day,league,a,b),mm in groups.items():
   near=[r for r in base if {r['team1'],r['team2']}=={a,b} and abs((date.fromisoformat(day)-date.fromisoformat(r['date'])).days)<=2]
   wa=sum(m['wins1'] if m['team1']==a else m['wins2'] for m in mm);wb=len(mm)-wa
   same=[r for r in near if abs((date.fromisoformat(day)-date.fromisoformat(r['date'])).days)<=1 and (r['wins1'],r['wins2'])==((wa,wb) if r['team1']==a else (wb,wa))]
   if len(same)==1 and same[0]['detail'] not in used:
    r=same[0];used.add(r['detail']);matched.append({'detail':r['detail'],'map_ids':[m['gameid'] for m in mm],'date_offset':(date.fromisoformat(day)-date.fromisoformat(r['date'])).days})
    for m in mm:m['reconciliation']='matched';m['series_detail']=r['detail']
   elif not near and league in DOMESTIC.get(season,set()):
    for m in mm:
     m['reconciliation']='additional';add.append(dict(date=m['date'],team1=m['team1'],team2=m['team2'],wins1=m['wins1'],wins2=m['wins2'],display1=m['team1'],display2=m['team2'],tournament=league+' OE supplementary',detail='oe:'+m['gameid'],source=m['source']))
   else:
    conflicts.append(dict(date=day,league=league,teams=[a,b],map_ids=[m['gameid'] for m in mm],reason='nearby score/date ambiguity' if near else 'unmatched international: stage eligibility unverified'))
    for m in mm:m['reconciliation']='quarantined'
  fields={k:sum(bool(m.get(k)) for m in maps) for k in ['timestamp','patch']}
  fields['complete_ten_players']=sum(all(len(m['players'][s])==5 and all(p['playername'] for p in m['players'][s]) for s in ['Blue','Red']) for m in maps)
  for k in STATS:fields[k]=sum(all(m['stats'][s][k] is not None for s in ['Blue','Red']) for m in maps)
  audit=dict(season=season,source_url=url,source_note='Public GitHub mirror of OE; not an independent scoring source' if url else 'Existing local OE mirror; original retrieval URL not recorded, enrichment only',sha256=hashlib.sha256(raw).hexdigest(),source_latest_date=max(r['date'] for r in rows),base_series=len(base),base_maps=sum(r['wins1']+r['wins2'] for r in base),eligible_normalized_maps=len(maps),matched_series=len(matched),matched_maps=sum(len(x['map_ids']) for x in matched),additional_maps=len(add),field_counts=fields,rejected=rejected,conflicts=conflicts,matched=matched,aliases=aliases)
  # Unknown provenance never authorizes new results in S16.
  if season==16:audit['additional_maps_not_admitted']=len(add);add=[];audit['additional_maps']=0
  lineups={};changes=[]
  for m in sorted(maps,key=lambda x:(x['timestamp'],x['gameid'])):
   if m['reconciliation']!='matched':continue
   for side,t in [('Blue',m['team1']),('Red',m['team2'])]:
    lineup=tuple(sorted(p['playername'] or p['playerid'] or '' for p in m['players'][side]))
    if len(lineup)!=5 or not all(lineup):continue
    if t in lineups and lineups[t][0]!=lineup:changes.append(dict(team=t,previous_observed=lineups[t][1],next_observed=m['timestamp'],previous_players=lineups[t][0],next_players=lineup,gameid=m['gameid']))
    lineups[t]=(lineup,m['timestamp'])
  audit['observed_lineup_changes']=len(changes)
  for name,value in [('lineup_changes',changes),('maps',maps),('additional',add),('audit',audit)]:
   (OUT/f'S{season}_{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
  audits.append(audit);print('S',season,'maps',len(maps),'matched',audit['matched_maps'],'add',len(add),'conflictgroups',len(conflicts),'rejected',len(rejected),flush=True)
 (OUT/'coverage.json').write_text(json.dumps([{k:v for k,v in a.items() if k not in ['rejected','conflicts','matched','aliases']} for a in audits],ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()

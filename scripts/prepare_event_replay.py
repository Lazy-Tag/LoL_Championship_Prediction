"""Freeze pre-event ratings and reconstruct fixed pre-event membership metadata.
Future match RESULTS are used only in the separate actual-finish evaluator.
Membership/group labels from the source are metadata, not fitted performance.
"""
import json,itertools,re
from pathlib import Path
from datetime import date
from collections import defaultdict,Counter
import numpy as np
from scipy.special import expit
from backtest import load_season,target_event,affiliations,prior_regions,optimize,key
R=Path(__file__).resolve().parents[1]
SOURCES={
 'W3':'https://lol.fandom.com/wiki/Season_3_World_Championship',
 'W4':'https://nexus.leagueoflegends.com/en-us/2014/09/worlds-2014-refresher/',
 'W5':'https://nexus.leagueoflegends.com/en-us/2015/09/everything-you-need-to-know-about-the-20/',
 'W6':'https://en.wikipedia.org/wiki/2016_League_of_Legends_World_Championship',
 'W7':'https://nexus.leagueoflegends.com/en-us/2017/09/worlds-2017-play-in-round-up/',
 'W8':'https://en.wikipedia.org/wiki/2018_League_of_Legends_World_Championship',
 'W9':'https://en.wikipedia.org/wiki/2019_League_of_Legends_World_Championship',
 'W10':'https://lolesports.com/en-US/news/worlds-2020-primer',
 'W11':'https://lolesports.com/en-US/news/worlds-2021-primer',
 'W12':'https://lolesports.com/en-US/news/worlds-2022-primer',
 'W13':'https://lolesports.com/en-GB/news/worlds-2023-primer',
 'W14':'https://lolesports.com/en-US/news/worlds-2024-primer',
 'W15':'https://lolesports.com/en-US/news/worlds-2025-primer',
 'M5':'https://doczz.net/doc/9108064/2015-mid-season-invitational-official-rules',
 'M6':'https://en.wikipedia.org/wiki/2016_Mid-Season_Invitational',
 'M7':'https://nexus.leagueoflegends.com/en-us/2017/02/2017-mid-season-invitational-update/',
 'M8':'https://nexus.leagueoflegends.com/en-us/2018/03/msi-2018-format-update/',
 'M9':'https://esports-assets.s3-us-west-2.amazonaws.com/production/files/rules/2019-MSI-Ruleset-v20.0.pdf',
 'M10':'https://www.leagueoflegends.com/ko-kr/news/esports/2020-msc-information/',
 'M11':'https://lolesports.com/en-US/news/msi-2021-is-heading-to-reykjavik-iceland',
 'M12':'https://lolesports.com/en-US/news/msi-updates---group-draw-results-adjusted-dates-and-venue',
 'M13':'https://lolesports.com/en-US/news/deep-dive-lol-esports-international-event-formats',
 'M14':'https://lolesports.com/en-US/news/msi-2024-primer',
 'M15':'https://lolesports.com/en-US/news/msi-2025-primer',
}

def ts(rows):return sorted({r[k] for r in rows for k in ['team1','team2']})
def components(rows):
 graph=defaultdict(set)
 for r in rows:
  a,b=r['team1'],r['team2'];graph[a].add(b);graph[b].add(a)
 groups=[];seen=set()
 for a in sorted(graph):
  if a in seen:continue
  todo=[a];g=[];seen.add(a)
  while todo:
   x=todo.pop();g.append(x)
   for y in graph[x]:
    if y not in seen:seen.add(y);todo.append(y)
  groups.append(sorted(g))
 return groups

def rounds(rows,main=False):
 rr=[r for r in rows if max(r['wins1'],r['wins2'])==1]
 if main:rr=[r for r in rr if 'RUMBLE' in r['stage'].upper()]
 return rr

def get_pi(rows,s,ev):
 if ev=='Worlds':return [r for r in rows if 'play-in' in r['tournament'].lower()]
 if s<=9:return [r for r in rows if 'play-in' in r['tournament'].lower()]
 if s==13:return [r for r in rows if r['stage']=='PLAY-IN']
 if s==14:return [r for r in rows if max(r['wins1'],r['wins2'])==2]
 if s==15:return [r for r in rows if 'PLAYIN' in r['stage']]
 return []

def opening_pairs(pi):
 seen=set();pairs=[]
 for r in pi:
  a,b=r['team1'],r['team2']
  if a not in seen and b not in seen:pairs.append([a,b]);seen.update([a,b])
 return pairs

def gsl_groups(pi):
 # Opening match pair sets linked by the first upper-round encounter; only
 # bracket membership is reconstructed, never the winner identity as input.
 pairs=opening_pairs(pi);idx={t:i for i,p in enumerate(pairs) for t in p};seen=set();groups=[]
 for r in pi:
  a,b=idx[r['team1']],idx[r['team2']]
  if a!=b and a not in seen and b not in seen:groups.append(pairs[a]+pairs[b]);seen.update([a,b])
 assert len(seen)==len(pairs),(pairs,groups)
 return groups

def rr_order(rows,group,reps):
 # Only for observed-result evaluation. Regular fixtures first, excess games
 # are actual tiebreakers. Pair counts discard canceled/remade extras later.
 wins=Counter();h=Counter();counts=Counter();ties=[]
 for r in rows:
  a,b=r['team1'],r['team2']
  if a not in group or b not in group or max(r['wins1'],r['wins2'])!=1:continue
  pair=tuple(sorted([a,b]));winner=a if r['wins1']>r['wins2'] else b;loser=b if winner==a else a
  if counts[pair]<reps:wins[winner]+=1;h[winner,loser]+=1;counts[pair]+=1
  else:ties.append((winner,loser))
 base=sorted(group,key=lambda t:(-wins[t],t));out=[]
 for total in sorted({wins[t] for t in group},reverse=True):
  tied=[t for t in base if wins[t]==total];hh={t:sum(h[t,u] for u in tied) for t in tied}
  # Actual tie games establish directed precedence; last tie-game wins have
  # priority. This does not enter prediction; used only for display evaluation.
  scores={t:hh[t] for t in tied}
  for j,(w,l) in enumerate(ties):
   if w in tied and l in tied:scores[w]=max(scores.values())+1
  out.extend(sorted(tied,key=lambda t:(-scores[t],t)))
 return out

def actual_ranks(rows,cfg):
 n=len(cfg['teams']);out={};ev=cfg['event'];s=cfg['season'];pi=get_pi(rows,s,ev);pits=set(ts(pi));main=[r for r in rows if r not in pi]
 def put(t,a,b=None):out[t]=[a,a if b is None else b]
 def loser(r):return r['team2'] if r['wins1']>r['wins2'] else r['team1']
 def winner(r):return r['team1'] if r['wins1']>r['wins2'] else r['team2']
 ko=[r for r in main if max(r['wins1'],r['wins2'])>=2 and (ev!='Worlds' or s<13 or r['stage'] in ['QUARTERFINALS','SEMIFINALS','FINALS'])]
 if ev=='MSI' and s>=13:
  losses=Counter();el=[]
  for r in ko:
   l=loser(r);losses[l]+=1
   if losses[l]==2:el.append(l)
  # Upper winner can lose final once, but is still runner-up (no reset).
  final=ko[-1];put(winner(final),1);put(loser(final),2)
  for t,band in zip([t for t in el if t not in out],[(7,8),(7,8),(5,6),(5,6),(4,4),(3,3)]):put(t,*band)
 else:
  f=ko[-1];put(winner(f),1);put(loser(f),2)
  for r in ko[-3:-1]:put(loser(r),3,4)
  if ev=='Worlds':
   for r in ko[:4]:put(loser(r),5,8)
 if ev=='Worlds' and s>=13:
  sw=[r for r in main if r not in ko];ww=Counter()
  for r in sw:ww[winner(r)]+=1
  for t in ts(sw):
   if t not in out:put(t,*{0:(15,16),1:(12,14),2:(9,11)}[ww[t]])
 elif ev=='Worlds':
  for g in cfg['main_groups_observed']:
   order=rr_order(main,g,2)
   for pos,t in enumerate(order):
    if t not in out:
     if s==3:put(t,9+2*(pos-2),10+2*(pos-2))
     else:put(t,9+4*(pos-2),12+4*(pos-2))
 elif ev=='MSC':
  for g in cfg['groups']:
   for pos,t in enumerate(rr_order(rows,g,1)):
    if t not in out:put(t,5+2*(pos-2),6+2*(pos-2))
 elif s<=9:
  g=ts(main);order=rr_order(main,g,1 if s==5 else 2)
  for pos,t in enumerate(order):
   if t not in out:put(t,pos+1)
 elif s in [11,12]:
  rum=[r for r in main if 'RUMBLE' in r['stage'].upper()];order=rr_order(rum,ts(rum),2)
  for pos,t in enumerate(order):
   if t not in out:put(t,pos+1)
  for g in cfg['groups']:
   for pos,t in enumerate(rr_order([r for r in main if r not in rum],g,4 if len(g)==3 else 2)):
    if t not in out:put(t,7,9) if pos==2 else put(t,10,11)
 if pi:
  if ev=='Worlds' and 7<=s<=9:
   for r in pi:
    if max(r['wins1'],r['wins2'])==3:put(loser(r),17,20)
   for t in pits:
    if t not in out:put(t,21,24)
  elif ev=='Worlds' and s in [10,11,12]:
   for r in pi:
    if 'QUAL' in r['stage']:put(loser(r),17,18)
    elif 'ELIM' in r['stage']:put(loser(r),19,20)
   for g in cfg['groups']:
    for pos,t in enumerate(rr_order(pi,g,1)):
     if t not in out:put(t,21+2*(pos-4),22+2*(pos-4))
  elif ev=='Worlds' and s==15:put(loser(pi[0]),17)
  elif (ev=='Worlds' and s in [13,14]) or (ev=='MSI' and s>=13):
   lc=Counter()
   for r in pi:
    l=loser(r);lc[l]+=1
    if l in out:continue
    if ev=='Worlds' and s==13 and r['stage']=='QUALIFIERS':put(l,17,18)
    elif ev=='MSI' and s==13 and max(r['wins1'],r['wins2'])==3:put(l,9)
    elif lc[l]==2:
     if ev=='Worlds':put(l,21,22) if len([x for x in pi if winner(x)==l])==0 and s==13 else put(l,19,20) if s==13 or len([x for x in pi if winner(x)==l])==0 else put(l,17,18)
     elif s==15:put(l,10 if sum(winner(x)==l for x in pi)==0 else 9)
     else:
      base=12 if s==13 else 11
      put(l,base,base+1) if sum(winner(x)==l for x in pi)==0 else put(l,base-2,base-1)
  elif ev=='MSI' and s<=9:
   ko_pi=[r for r in pi if max(r['wins1'],r['wins2'])==3]
   if s==8:
    for r in ko_pi:put(loser(r),7,8)
    start=9
   else:put(loser(ko_pi[-1]),7);start=8
   eliminated=[t for t in pits if t not in out];wins=Counter()
   for r in rounds(pi):wins[winner(r)]+=1
   at=start
   for score in sorted({wins[t] for t in eliminated},reverse=True):
    same=[t for t in eliminated if wins[t]==score]
    for t in same:put(t,at,at+len(same)-1)
    at+=len(same)
 assert set(out)==set(cfg['teams']),(cfg['id'],'missing',set(cfg['teams'])-set(out),'out',out)
 return out

def main():
 seasons={};regs={}
 for s in range(3,16):seasons[s],_=load_season(s);regs[s]=affiliations(seasons[s],s)
 for s in range(4,16):
  for t,r in regs[s-1].items():regs[s].setdefault(t,r)
 configs=[]
 for s in range(4,16):
  for ev in ['MSI','MSC','Worlds']:
   rows=[r for r in seasons[s] if target_event(r['tournament'])==ev]
   if not rows:continue
   teams=ts(rows);start=min(r['date'] for r in rows);training=[r for r in seasons[s] if r['date']<start]
   pr,pa=prior_regions(seasons[s-1],regs[s-1],90) if s>3 else ({},{'series':0})
   fitteams=sorted(set(teams)|set(ts(training)));mu={t:pr.get(regs[s].get(t),0) for t in fitteams}
   theta,grad=optimize(training,fitteams,date.fromisoformat(start),90,mu,.25);th=dict(zip(fitteams,map(float,theta)))
   pi=get_pi(rows,s,ev);pits=set(ts(pi));mainrows=[r for r in rows if r not in pi]
   c=dict(id=f'{s+2010}_{ev}',season=s,year=s+2010,event=ev,seed=s+2010,samples=14000605,start_date=start,teams=teams,display={r[k]:r['display'+k[-1]] for r in rows for k in ['team1','team2']},regions={t:regs[s].get(t,'UNKNOWN') for t in teams},strength={t:th[t] for t in teams},training_series=len(training),training_maps=sum(r['wins1']+r['wins2'] for r in training),latest_training_date=max((r['date'] for r in training),default=None),prior_audit=pa,gradient=grad,source=SOURCES[('W' if ev=='Worlds' else 'M')+str(s)],groups=[],main_groups=[],direct=[],byes=[],opening=[],main_groups_observed=[])
   assert not pa.get('last_date') or pa['last_date']<start
   if ev=='Worlds' and s<=12:
    c['main_groups_observed']=components(rounds(mainrows));c['main_groups']=[[t for t in g if t not in pits] for g in c['main_groups_observed']]
    if s==3:c['byes']=sorted(set(teams)-set(ts(rounds(mainrows))));c['kind']='worlds2013'
    else:c['kind']='worlds_groups'
    if pi:c['groups']=components(rounds(pi))
   elif ev=='Worlds':c['kind']='worlds_swiss';c['direct']=sorted(set(teams)-pits);c['opening']=gsl_groups(pi) if s<15 else opening_pairs(pi)
   elif ev=='MSC':c['kind']='msc';c['groups']=components(rounds(rows))
   elif s<=9:
    c['kind']='msi_old';c['groups']=components(rounds(pi));c['direct']=sorted(set(teams)-pits)
    if pi:
     c['byes']=sorted(pits-set(ts(rounds(pi))))
     c['pi_bye_opponents']={}
     for r in pi:
      if max(r['wins1'],r['wins2'])==3:
       for a,b in [(r['team1'],r['team2']),(r['team2'],r['team1'])]:
        if a in c['byes'] and b not in c['byes']:
         c['pi_bye_opponents'][a]=next((i for i,g in enumerate(c['groups']) if b in g),-1)
   elif s in [11,12]:c['kind']='msi_rumble';c['groups']=components([r for r in rounds(rows) if 'RUMBLE' not in r['stage'].upper()])
   else:c['kind']='msi_double';c['direct']=sorted(set(teams)-pits);c['opening']=gsl_groups(pi)
   c['actual_ranks']=actual_ranks(rows,c)
   configs.append(c);print(c['id'],c['kind'],len(teams),'groups',list(map(len,c['groups'])),'main',list(map(len,c['main_groups'])),'opening',list(map(len,c['opening'])),'train',len(training))
 (R/'data/event_replay/configs.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

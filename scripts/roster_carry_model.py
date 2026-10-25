"""Experimental cross-season residual transport, separate from dynamic90.
Only exact same normalized team names and compatible regions may inherit.
"""
import unicodedata
from collections import Counter,defaultdict
from datetime import date
import numpy as np
from candidate_models import DynamicBT,TEAM_SD,REGION_DRIFT_SD

class RosterBT(DynamicBT):
    def __init__(self,teams,regions,prior,half_life=90):
        super().__init__(teams,regions,prior);self.half_life=half_life
    def advance(self,day):
        if self.day is not None:
            days=(day-self.day).days;assert days>=0
            rho=2**(-days/self.half_life);d=np.r_[np.ones(self.nr),np.full(len(self.teams),rho)]
            self.m*=d;self.C*=d[:,None]*d[None,:]
            self.C.flat[::len(self.m)+1]+=np.r_[np.full(self.nr,REGION_DRIFT_SD**2*days/90),np.full(len(self.teams),TEAM_SD**2*(1-rho*rho))]
        self.day=day

def player_key(name):
    return unicodedata.normalize('NFKC',name).strip().casefold()

def profile(games,team):
    count=Counter();sources=[]
    for g in games:
        side='blue' if g['a']==team else 'red'
        names=[player_key(p['name']) for p in g['teams'][side]['players'] if p.get('name')]
        if len(names)!=5 or len(set(names))!=5:continue
        count.update(names);sources.append(dict(id=g['game_id'],url=g.get('url'),date=g['date'][:10]))
    total=sum(count.values())
    return dict(shares={k:v/total for k,v in sorted(count.items())},maps=len(sources),sources=sources) if total else None

def make_rosters(rows,matched):
    teamrows=defaultdict(list);games=defaultdict(lambda:defaultdict(list))
    for r in rows:
        for t in (r['team1'],r['team2']):teamrows[t].append(r['date'])
        for g in matched.get(r['detail'],[]):
            for t in (g['a'],g['b']):games[t][r['date']].append(g)
    out={}
    for team,days in teamrows.items():
        valid=[]
        for ds,gg in sorted(games[team].items()):
            p=profile(gg,team)
            if p:valid.append(dict(date=ds,**p))
        first,last=(valid[0],valid[-1]) if valid else (None,None)
        out[team]=dict(first_match=min(days),last_match=max(days),first=first,last=last)
    return out

def overlap(a,b):
    return min(1.,max(0.,sum(min(v,b.get(k,0.)) for k,v in a.items())))

def initialize(teams,regions,prior,half_life,previous,old_rosters,new_rosters,start,cutoff,gamma=1):
    model=RosterBT(teams,regions,prior,half_life);audit=[];pairs=[]
    for t in teams:
        record=dict(team=t,cutoff=cutoff.isoformat(),start=start.isoformat(),retention=0.,coefficient=0.,reason='no_previous_team')
        if previous is not None and t in previous.ti:
            old=old_rosters.get(t,{});new=new_rosters.get(t,{});a=old.get('last');b=new.get('first')
            record['reason']='missing_lineup'
            if regions.get(t) is not None and regions.get(t)==previous.regions.get(t) and a and b:
                gap_old=(date.fromisoformat(old['last_match'])-date.fromisoformat(a['date'])).days
                gap_new=(date.fromisoformat(b['date'])-date.fromisoformat(new['first_match'])).days
                record.update(previous_lineup=a,current_lineup=b,previous_lineup_gap_days=gap_old,current_lineup_gap_days=gap_new)
                if date.fromisoformat(b['date'])>=cutoff:record['reason']='lineup_not_known_before_cutoff'
                elif gap_old>45:record['reason']='previous_lineup_stale'
                elif gap_new>30:record['reason']='opening_lineup_missing'
                else:
                    days=(start-previous.day).days;assert days>=0
                    q=overlap(a['shares'],b['shares']);rho=q**gamma*2**(-days/half_life)
                    record.update(retention=q,coefficient=rho,coefficient_at_cutoff=rho*2**(-(cutoff-start).days/half_life),season_gap_days=days,reason='inherited' if q else 'no_shared_handles')
                    if rho:pairs.append((model.nr+model.ti[t],previous.nr+previous.ti[t],rho))
            elif regions.get(t)!=previous.regions.get(t):record['reason']='region_changed_or_unknown'
        audit.append(record)
    if pairs:
        new=np.array([p[0] for p in pairs]);old=np.array([p[1] for p in pairs]);scale=np.array([p[2] for p in pairs])
        model.m[new]=previous.m[old]*scale
        model.C[np.ix_(new,new)]=previous.C[np.ix_(old,old)]*scale[:,None]*scale[None,:]+np.diag(TEAM_SD**2*(1-scale**2))
    return model,audit

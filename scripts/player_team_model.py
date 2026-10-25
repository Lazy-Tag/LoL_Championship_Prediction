"""Player-role skill plus team residual, joint Gaussian/Laplace filter.
Source IDs only; no name-based cross-club or cross-year identity guesses.
"""
from datetime import date
import numpy as np
from scipy.sparse import csr_matrix
from candidate_models import TEAM_SD,REGION_SD,REGION_DRIFT_SD
from adaptive_memory_models import TwoMemory
ROLE=('top','jng','mid','bot','sup')
class PlayerTeam:
 update=TwoMemory.update
 def __init__(self,teams,regions,prior,players,previous=None,carry=True,start=None):
  self.teams=teams;self.regions=regions;self.ti={t:i for i,t in enumerate(teams)};self.rs=sorted({regions.get(t,'UNKNOWN') for t in teams});self.ri={r:i for i,r in enumerate(self.rs)};self.nr=len(self.rs);self.nt=len(teams)
  self.players=sorted(players);self.pi={p:self.nr+2*self.nt+i for i,p in enumerate(self.players)}
  self.var=np.r_[np.full(self.nr,REGION_SD**2),np.full(self.nt,TEAM_SD**2/2),np.full(self.nt,TEAM_SD**2/2),np.full(len(self.players),TEAM_SD**2*2.5)]
  self.m=np.array([prior.get(r,0.) for r in self.rs]+[0.]*(len(self.var)-self.nr));self.C=np.diag(self.var);self.day=None;self.last_update=None;self.max_gradient=0.;self.transport=[]
  if previous is not None and carry:
   overlap=sorted(set(self.pi)&set(previous.pi));old=np.array([previous.pi[p] for p in overlap],int);new=np.array([self.pi[p] for p in overlap],int)
   if len(old):
    gap=(start-previous.day).days;assert gap>=0;rho=2**(-gap/90)
    self.m[new]=previous.m[old]*rho;self.C[np.ix_(new,new)]=previous.C[np.ix_(old,old)]*rho**2+np.diag(self.var[new]*(1-rho**2))
    self.transport=[dict(player_role=p,previous_date=previous.day.isoformat(),start_date=start.isoformat(),coefficient=rho) for p in overlap]
 def advance(self,day):
  if self.day is not None:
   days=(day-self.day).days;assert days>=0;rho=2**(-days/90);d=np.r_[np.ones(self.nr),np.full(len(self.m)-self.nr,rho)]
   self.m*=d;self.C*=d[:,None]*d[None,:];self.C.flat[::len(self.m)+1]+=np.r_[np.full(self.nr,REGION_DRIFT_SD**2*days/90),self.var[self.nr:]*(1-rho*rho)]
  self.day=day
 def vector(self,team,lineup):
  v={self.ri[self.regions.get(team,'UNKNOWN')]:1.,self.nr+self.ti[team]:1.}
  if lineup:
   assert abs(sum(lineup.values())-1)<1e-9
   for p,share in lineup.items():v[self.pi[p]]=share
  else:v[self.nr+self.nt+self.ti[team]]=1.
  return v
 def observation_design(self,rows):
  ii=[];jj=[];vv=[]
  for i,r in enumerate(rows):
   for k,sgn in [('1',1.),('2',-1.)]:
    for j,value in self.vector(r['team'+k],r.get('lineup'+k)).items():ii.append(i);jj.append(j);vv.append(sgn*value)
  x=csr_matrix((vv,(ii,jj)),shape=(len(rows),len(self.m)));x.eliminate_zeros();return x
 def strength(self,team,lineup):return float(sum(self.m[j]*v for j,v in self.vector(team,lineup).items()))
 def components(self,team,lineup):
  region=float(self.m[self.ri[self.regions.get(team,'UNKNOWN')]]);team_part=float(self.m[self.nr+self.ti[team]]);total=self.strength(team,lineup)
  return dict(region=region,team_residual=team_part,player_or_unknown_component=total-region-team_part,total=total)

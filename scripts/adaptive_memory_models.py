"""Isolated two-timescale and lineup covariance-shock experiments."""
from datetime import date
import numpy as np
from scipy.special import expit
from scipy.linalg import cho_factor,cho_solve
from scipy.sparse import hstack
from candidate_models import DynamicBT,design,TEAM_SD,REGION_DRIFT_SD
from roster_carry_model import overlap

class TwoMemory(DynamicBT):
 def __init__(self,teams,regions,prior,long_half=180,short_half=30,short_share=.25):
  super().__init__(teams,regions,prior);self.long_half=long_half;self.short_half=short_half;self.short_share=short_share;n=len(teams)
  self.m=np.r_[self.m,np.zeros(n)];self.C=np.diag([.5**2]*self.nr+[TEAM_SD**2*(1-short_share)]*n+[TEAM_SD**2*short_share]*n)
 def advance(self,day):
  if self.day is not None:
   days=(day-self.day).days;assert days>=0;n=len(self.teams)
   a=2**(-days/self.long_half);b=2**(-days/self.short_half);d=np.r_[np.ones(self.nr),np.full(n,a),np.full(n,b)]
   self.m*=d;self.C*=d[:,None]*d[None,:]
   self.C.flat[::len(self.m)+1]+=np.r_[np.full(self.nr,REGION_DRIFT_SD**2*days/90),np.full(n,TEAM_SD**2*(1-self.short_share)*(1-a*a)),np.full(n,TEAM_SD**2*self.short_share*(1-b*b))]
  self.day=day
 def strengths(self):
  n=len(self.teams);return {t:float(self.m[self.ri[self.regions.get(t,'UNKNOWN')]]+self.m[self.nr+i]+self.m[self.nr+n+i]) for t,i in self.ti.items()}
 def observation_design(self,rows):
  x,_,_=design(rows,self.teams,self.regions);return hstack([x,x[:,self.nr:]],format='csr')
 def update(self,rows):
  if not rows:return
  assert self.day is not None and all(r['date']==self.day.isoformat() for r in rows)
  assert self.last_update is None or self.last_update<self.day
  X=self.observation_design(rows);active=np.unique(X.indices);A=X[:,active].toarray()
  old=self.m[active].copy();V=self.C[np.ix_(active,active)];Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(active)))
  wa=np.array([r['wins1'] for r in rows],float);total=wa+np.array([r['wins2'] for r in rows],float)
  def obj(x):
   eta=A@x;delta=x-old
   return float(np.sum(total*np.logaddexp(0,eta)-wa*eta)+.5*delta@Vi@delta)
  x=old.copy()
  for _ in range(40):
   p=expit(A@x);grad=A.T@(total*p-wa)+Vi@(x-old);H=Vi+A.T@((total*p*(1-p))[:,None]*A)
   if np.max(np.abs(grad))<1e-8:break
   step=cho_solve(cho_factor(H,lower=True),grad);alpha=1.;before=obj(x)
   while obj(x-alpha*step)>before-1e-4*alpha*np.dot(grad,step) and alpha>1e-8:alpha*=.5
   x-=alpha*step
  p=expit(A@x);grad=A.T@(total*p-wa)+Vi@(x-old);g=float(np.max(np.abs(grad)));self.max_gradient=max(self.max_gradient,g)
  if g>2e-4:raise RuntimeError(f'MAP residual {g}')
  H=Vi+A.T@((total*p*(1-p))[:,None]*A);post=cho_solve(cho_factor(H,lower=True),np.eye(len(active)))
  K=self.C[:,active]@Vi;self.m+=K@(x-old);self.C-=K@(V-post)@K.T;self.C=(self.C+self.C.T)*.5
  assert np.all(np.diag(self.C)>0);self.last_update=self.day

class RosterShock(DynamicBT):
 def observe_rosters(self,profiles,previous):
  """Call after ALL same-day forecasts, before assimilating that day's scores.
  Never changes the pre-update mean. Previous and current lineup dates recorded.
  """
  changes=[]
  for team,current in profiles.items():
   old=previous.get(team)
   if old and 0<(date.fromisoformat(current['date'])-date.fromisoformat(old['date'])).days<=180:
    q=overlap(old['shares'],current['shares']);delta=TEAM_SD**2*(1-q)
    if delta>1e-12:
     k=self.nr+self.ti[team];self.C[k,k]+=delta
     changes.append(dict(team=team,previous_date=old['date'],observed_date=current['date'],retention=q,added_variance=delta,previous_players=old['shares'],current_players=current['shares']))
   previous[team]=current
  return changes

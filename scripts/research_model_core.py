"""Joint outcome/gold likelihood and approximate online restart filtering."""
import copy
import numpy as np
from scipy.special import expit,logsumexp
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
from numpy.polynomial.hermite import hermgauss
from candidate_models import DynamicBT,design,TEAM_SD
Z,W=hermgauss(20);Z=Z*np.sqrt(2);W=W/np.sqrt(np.pi)
DEFAULT=dict(a=1.,c=0.,k=0.,b=0.,sigma=3.,n=0)

def fit_gold(records):
 if len(records)<200:return DEFAULT.copy()
 x=np.array([r['d'] for r in records]);g=np.array([r['g'] for r in records]);y=np.array([r['y'] for r in records]);A=np.c_[x,np.ones(len(x))]
 kb=np.linalg.solve(A.T@A+np.diag([9.,9.]),A.T@g);k=float(np.clip(kb[0],0,5));b=float(np.clip(np.mean(g-k*x),-3,3));sigma=float(np.clip(np.sqrt(np.mean((g-k*x-b)**2)),.5,8))
 B=np.c_[x,g]
 def obj(v):
  eta=B@v;delta=v-np.array([1.,0.]);return float(np.sum(np.logaddexp(0,eta)-y*eta)+.5*delta@delta),B.T@(expit(eta)-y)+delta
 opt=minimize(obj,[1.,0.],jac=True,bounds=[(.1,3),(0,3)],method='L-BFGS-B',options={'ftol':1e-12,'gtol':1e-7})
 assert opt.success
 return dict(a=float(opt.x[0]),c=float(opt.x[1]),k=k,b=b,sigma=sigma,n=len(records),latest_date=max(r['date'] for r in records))

def marginal(d,par,derivatives=False,side=None):
 d=np.asarray(d);a,c,k,b,sig=[par[t] for t in ['a','c','k','b','sigma']];scale=a+c*k
 offsets=np.broadcast_to(np.array([-b,b]),d.shape+(2,))
 if side is not None:
  ss=np.asarray(side);offsets=np.where((ss!=0)[...,None],ss[...,None]*b,offsets)
 z=scale*d[...,None,None]+c*(sig*Z[None,:]+offsets[...,None]);p=expit(z);q=np.sum(p*W,axis=-1).mean(axis=-1)
 if not derivatives:return q
 v=p*(1-p);q1=scale*np.sum(v*W,axis=-1).mean(axis=-1);q2=scale**2*np.sum(v*(1-2*p)*W,axis=-1).mean(axis=-1)
 return q,q1,q2

def joint_terms(d,wa,n,g,side,par):
 a,c,k,b,sig=[par[t] for t in ['a','c','k','b','sigma']];known=np.isfinite(g);l=np.zeros(len(d));grad=l.copy();hess=l.copy()
 if np.any(known):
  assert np.all(n[known]==1)
  ix=known;res=g[ix]-k*d[ix]-side[ix]*b;eta=a*d[ix]+c*g[ix];p=expit(eta)
  l[ix]=.5*(res/sig)**2+np.log(sig*np.sqrt(2*np.pi))+n[ix]*np.logaddexp(0,eta)-wa[ix]*eta
  grad[ix]=-k*res/sig**2+a*(n[ix]*p-wa[ix]);hess[ix]=k*k/sig**2+a*a*n[ix]*p*(1-p)
 if np.any(~known):
  ix=~known;q,q1,q2=marginal(d[ix],par,True,side[ix]);q=np.clip(q,1e-12,1-1e-12);w=wa[ix];nn=n[ix]
  l[ix]=-w*np.log(q)-(nn-w)*np.log1p(-q);fq=-w/q+(nn-w)/(1-q);sq=w/q**2+(nn-w)/(1-q)**2
  grad[ix]=fq*q1;hess[ix]=sq*q1*q1+fq*q2
 return float(sum(l)),grad,hess

class JointGold(DynamicBT):
 def __init__(self,*args,parameters=None):super().__init__(*args);self.par=parameters or DEFAULT.copy()
 def predict(self,a,b):
  th=self.strengths();return float(marginal(th[a]-th[b],self.par))
 def update(self,rows):
  if self.par['n']==0:return super().update(rows)
  if not rows:return
  assert all(r['date']==self.day.isoformat() for r in rows);assert self.last_update is None or self.last_update<self.day
  X,_,_=design(rows,self.teams,self.regions);active=np.unique(X.indices);A=X[:,active].toarray();old=self.m[active].copy();V=self.C[np.ix_(active,active)];Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(active)))
  wa=np.array([r['wins1'] for r in rows],float);n=wa+np.array([r['wins2'] for r in rows]);g=np.array([r.get('gold',np.nan) for r in rows]);side=np.array([r.get('side',0) for r in rows])
  def obj(x):
   l,gg,hh=joint_terms(A@x,wa,n,g,side,self.par);delta=x-old;return l+.5*delta@Vi@delta,A.T@gg+Vi@delta,Vi+A.T@(hh[:,None]*A)
  x=old.copy()
  for _ in range(60):
   l,gg,H=obj(x)
   if max(abs(gg))<1e-8:break
   damp=0.
   for attempt in range(12):
    try:step=cho_solve(cho_factor(H+np.eye(len(x))*damp,lower=True),gg);break
    except np.linalg.LinAlgError:damp=1e-5 if damp==0 else damp*10
   else:raise RuntimeError('Joint Newton failed')
   alpha=1.
   while obj(x-alpha*step)[0]>l-1e-4*alpha*(gg@step) and alpha>1e-8:alpha*=.5
   x-=alpha*step
  _,gg,H=obj(x);self.max_gradient=max(self.max_gradient,float(max(abs(gg))));assert max(abs(gg))<2e-4
  post=cho_solve(cho_factor(H,lower=True),np.eye(len(active)));K=self.C[:,active]@Vi;self.m+=K@(x-old);self.C-=K@(V-post)@K.T;self.C=(self.C+self.C.T)/2;self.last_update=self.day

def evidence_update(model,rows):
 X,_,_=design(rows,model.teams,model.regions);ix=np.unique(X.indices);A=X[:,ix].toarray();old=model.m[ix].copy();V=model.C[np.ix_(ix,ix)].copy();Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(ix)))
 model.update(rows);x=model.m[ix];post=model.C[np.ix_(ix,ix)];w=np.array([r['wins1'] for r in rows]);n=w+np.array([r['wins2'] for r in rows]);d=x-old;eta=A@x
 return float(np.sum(w*eta-n*np.logaddexp(0,eta))-.5*d@Vi@d+.5*(2*np.log(np.diag(np.linalg.cholesky(post))).sum()-2*np.log(np.diag(np.linalg.cholesky(V))).sum()))

class ChangePoint:
 def __init__(self,teams,regions,prior,seed,particles=16,hazard_half=180):
  self.bank=[DynamicBT(teams,regions,prior) for _ in range(particles)];self.weights=np.ones(particles)/particles;self.rng=np.random.default_rng(seed);self.hazard_half=hazard_half;self.last={};self.audit=[];self.day=None
 def advance(self,day):
  self.day=day
  for m in self.bank:m.advance(day)
 def strengths(self):
  theta=[m.strengths() for m in self.bank];out={}
  for t in theta[0]:
   h=(1-2**(-(self.day-self.last[t]).days/self.hazard_half)) if t in self.last and self.hazard_half else 0.
   out[t]=float(sum(w*(d[t]-h*m.m[m.nr+m.ti[t]]) for w,d,m in zip(self.weights,theta,self.bank)))
  return out
 def update(self,rows):
  if not rows:return
  active=sorted({r[k] for r in rows for k in ['team1','team2']});hazard={t:(1-2**(-(self.day-self.last[t]).days/self.hazard_half) if t in self.last and self.hazard_half else 0.) for t in active};logs=[];flags=[]
  for w,m in zip(self.weights,self.bank):
   changed=[]
   for t in active:
    if self.rng.random()<hazard[t]:
     j=m.nr+m.ti[t];m.m[j]=0;m.C[j,:]=0;m.C[:,j]=0;m.C[j,j]=TEAM_SD**2;changed.append(t)
   logs.append(np.log(w)+evidence_update(m,rows));flags.append(changed)
  assert np.all(np.isfinite(logs))
  weights=np.exp(np.array(logs)-logsumexp(logs));probs={t:float(sum(w for w,ts in zip(weights,flags) if t in ts)) for t in active}
  self.audit.append(dict(date=self.day.isoformat(),reset_probabilities=probs,effective_particles=float(1/sum(weights**2))))
  # Preserve weighted posterior for tomorrow's forecasts; resample only at next update.
  self.weights=weights
  for t in active:self.last[t]=self.day
 def resample_before_update(self):
  K=len(self.bank);u=(self.rng.random()+np.arange(K))/K;ix=np.searchsorted(np.cumsum(self.weights),u);self.bank=[copy.deepcopy(self.bank[min(i,K-1)]) for i in ix];self.weights=np.ones(K)/K

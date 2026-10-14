"""Prespecified candidates: hierarchical MAP BT and dynamic Gaussian/Laplace BT.
No tuning on evaluation events; season resets, 90-day memory in both candidates.
"""
from datetime import date
import numpy as np
from scipy.special import expit
from scipy.optimize import minimize
from scipy.linalg import cho_factor,cho_solve
from scipy.sparse import csr_matrix

HALF_LIFE=90.
REGION_SD=.5
TEAM_SD=.75
REGION_DRIFT_SD=.10

def design(rows,teams,regions):
    ti={t:i for i,t in enumerate(teams)};rs=sorted({regions.get(t,'UNKNOWN') for t in teams});ri={r:i for i,r in enumerate(rs)}
    ids=[];cols=[];values=[]
    for i,row in enumerate(rows):
        for t,sgn in [(row['team1'],1.),(row['team2'],-1.)]:
            ids.extend([i,i]);cols.extend([ri[regions.get(t,'UNKNOWN')],len(rs)+ti[t]]);values.extend([sgn,sgn])
    X=csr_matrix((values,(ids,cols)),shape=(len(rows),len(rs)+len(teams)));X.eliminate_zeros()
    return X,rs,ti

def static_fit(rows,teams,regions,prior,reference):
    X,rs,ti=design(rows,teams,regions);n=len(rs);mu=np.array([prior.get(r,0.) for r in rs]+[0.]*len(teams))
    precision=np.array([1/REGION_SD**2]*n+[1/TEAM_SD**2]*len(teams))
    wa=np.array([r['wins1'] for r in rows],float);wb=np.array([r['wins2'] for r in rows],float)
    age=np.array([(reference-date.fromisoformat(r['date'])).days for r in rows]);assert np.all(age>0)
    w=np.exp2(-age/HALF_LIFE)
    def objective(z):
        d=X@z;err=w*((wa+wb)*expit(d)-wa);delta=z-mu
        loss=np.sum(w*(wa*np.logaddexp(0,-d)+wb*np.logaddexp(0,d)))+.5*np.dot(precision*delta,delta)
        grad=np.asarray(X.T@err).ravel()+precision*delta
        return float(loss),grad
    opt=minimize(objective,mu,jac=True,method='L-BFGS-B',options={'maxiter':1500,'gtol':1e-8,'ftol':1e-13,'maxls':50})
    g=float(np.max(np.abs(objective(opt.x)[1])))
    if g>2e-4:raise RuntimeError(f'hierarchical gradient residual {g}')
    ri={r:i for i,r in enumerate(rs)};theta={t:float(opt.x[ri[regions.get(t,'UNKNOWN')]]+opt.x[n+i]) for t,i in ti.items()}
    return theta,dict(gradient_inf=g,region_strength={r:float(opt.x[i]) for i,r in enumerate(rs)},parameters=dict(region_sd=REGION_SD,team_sd=TEAM_SD,half_life_days=HALF_LIFE))

class DynamicBT:
    """Daily batch Laplace filtering; AR(1) team residual, drifting region state.
    Forecasts are queried BEFORE the day's results are added. Updates within one
    date are simultaneous, avoiding arbitrary series ordering or same-day leakage.
    """
    def __init__(self,teams,regions,prior):
        self.teams=teams;self.regions=regions
        _,self.rs,self.ti=design([],teams,regions);self.ri={r:i for i,r in enumerate(self.rs)};self.nr=len(self.rs)
        self.m=np.array([prior.get(r,0.) for r in self.rs]+[0.]*len(teams))
        self.C=np.diag([REGION_SD**2]*self.nr+[TEAM_SD**2]*len(teams));self.day=None;self.last_update=None
        self.max_gradient=0.
    def advance(self,day):
        if self.day is not None:
            days=(day-self.day).days;assert days>=0
            rho=2**(-days/HALF_LIFE)
            d=np.array([1.]*self.nr+[rho]*len(self.teams));self.m*=d;self.C*=d[:,None]*d[None,:]
            self.C.flat[::len(self.m)+1]+=np.array([REGION_DRIFT_SD**2*days/HALF_LIFE]*self.nr+[TEAM_SD**2*(1-rho*rho)]*len(self.teams))
        self.day=day
    def strengths(self):
        return {t:float(self.m[self.ri[self.regions.get(t,'UNKNOWN')]]+self.m[self.nr+i]) for t,i in self.ti.items()}
    def update(self,rows):
        if not rows:return
        assert self.day is not None and all(r['date']==self.day.isoformat() for r in rows)
        assert self.last_update is None or self.last_update<self.day
        X,_,_=design(rows,self.teams,self.regions);active=np.unique(X.indices);A=X[:,active].toarray()
        old=self.m[active].copy();V=self.C[np.ix_(active,active)];Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(active)))
        wa=np.array([r['wins1'] for r in rows],float);total=wa+np.array([r['wins2'] for r in rows],float)
        def obj(x):
            eta=A@x;delta=x-old
            return float(np.sum(total*np.logaddexp(0,eta)-wa*eta)+.5*delta@Vi@delta)
        x=old.copy()
        for _ in range(40):
            p=expit(A@x);grad=A.T@(total*p-wa)+Vi@(x-old)
            H=Vi+A.T@((total*p*(1-p))[:,None]*A)
            if np.max(np.abs(grad))<1e-8:break
            step=cho_solve(cho_factor(H,lower=True),grad);alpha=1.;before=obj(x)
            while obj(x-alpha*step)>before-1e-4*alpha*np.dot(grad,step) and alpha>1e-8:alpha*=.5
            x-=alpha*step
        p=expit(A@x);grad=A.T@(total*p-wa)+Vi@(x-old);g=float(np.max(np.abs(grad)));self.max_gradient=max(self.max_gradient,g)
        if g>2e-4:raise RuntimeError(f'dynamic MAP residual {g}')
        H=Vi+A.T@((total*p*(1-p))[:,None]*A);post=cho_solve(cho_factor(H,lower=True),np.eye(len(active)))
        K=self.C[:,active]@Vi
        self.m+=K@(x-old);self.C-=K@(V-post)@K.T;self.C=(self.C+self.C.T)*.5
        assert np.all(np.diag(self.C)>0)
        self.last_update=self.day

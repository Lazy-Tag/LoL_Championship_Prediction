"""Daily Laplace BT with a jointly estimated, season-reset blue-side state.
Unobserved sides are marginalized with independent P(blue)=1/2 per map.
The side state has fixed SD .5 and 90-day AR memory; no outcome-based tuning.
"""
import numpy as np
from scipy.special import expit
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
from candidate_models import DynamicBT,design,HALF_LIFE,TEAM_SD,REGION_DRIFT_SD
SIDE_SD=.5

def likelihood(x,A,side,w,n,enabled=True):
    d=A@x[:-1];b=x[-1] if enabled else 0.
    plus=expit(d+b);minus=expit(d-b);pa=plus*(1-plus);pb=minus*(1-minus)
    haa=pa*(1-2*plus);hbb=pb*(1-2*minus)
    unknown=side==0
    p=expit(d+side*b);v=p*(1-p);h=v*(1-2*p)
    q=np.where(unknown,(plus+minus)/2,p)
    qd=np.where(unknown,(pa+pb)/2,v)
    qb=np.where(unknown,(pa-pb)/2,side*v)
    qdd=np.where(unknown,(haa+hbb)/2,h)
    qdb=np.where(unknown,(haa-hbb)/2,side*h)
    qbb=np.where(unknown,(haa+hbb)/2,side*side*h)
    if not enabled:qb*=0;qdb*=0;qbb*=0
    q=np.clip(q,1e-14,1-1e-14)
    l=-np.sum(w*np.log(q)+(n-w)*np.log1p(-q))
    gq=-w/q+(n-w)/(1-q);hq=w/q**2+(n-w)/(1-q)**2
    grad=np.r_[A.T@(gq*qd),np.sum(gq*qb)]
    H=np.zeros((len(x),len(x)))
    H[:-1,:-1]=A.T@((hq*qd**2+gq*qdd)[:,None]*A)
    H[:-1,-1]=A.T@(hq*qd*qb+gq*qdb);H[-1,:-1]=H[:-1,-1]
    H[-1,-1]=np.sum(hq*qb**2+gq*qbb)
    return float(l),grad,H

class DynamicSideBT(DynamicBT):
    def __init__(self,teams,regions,prior,enabled=True):
        super().__init__(teams,regions,prior);self.enabled=enabled
        self.m=np.r_[self.m,0.];C=np.zeros((len(self.m),len(self.m)));C[:-1,:-1]=self.C;C[-1,-1]=SIDE_SD**2;self.C=C
    def advance(self,day):
        if self.day is not None:
            days=(day-self.day).days;assert days>=0
            rho=2**(-days/HALF_LIFE);d=np.r_[np.ones(self.nr),np.full(len(self.teams)+1,rho)]
            self.m*=d;self.C*=d[:,None]*d[None,:]
            noise=np.r_[np.full(self.nr,REGION_DRIFT_SD**2*days/HALF_LIFE),np.full(len(self.teams),TEAM_SD**2*(1-rho*rho)),SIDE_SD**2*(1-rho*rho)]
            self.C.flat[::len(self.m)+1]+=noise
        self.day=day
    def predict(self,a,b):
        th=self.strengths();d=th[a]-th[b];side=self.m[-1] if self.enabled else 0.
        return float((expit(d+side)+expit(d-side))/2)
    def update(self,rows):
        if not rows:return
        assert self.day is not None and all(r['date']==self.day.isoformat() for r in rows)
        assert self.last_update is None or self.last_update<self.day
        X,_,_=design(rows,self.teams,self.regions);act=np.unique(X.indices);A=X[:,act].toarray();active=np.r_[act,len(self.m)-1]
        old=self.m[active].copy();V=self.C[np.ix_(active,active)];Vi=cho_solve(cho_factor(V,lower=True),np.eye(len(active)))
        w=np.array([r['wins1'] for r in rows],float);n=w+np.array([r['wins2'] for r in rows],float);side=np.array([r.get('side1',0) for r in rows],float)
        def obj(x):
            l,g,H=likelihood(x,A,side,w,n,self.enabled);delta=x-old
            return l+.5*delta@Vi@delta,g+Vi@delta,H+Vi
        x=old.copy()
        for _ in range(50):
            l,g,H=obj(x)
            if max(abs(g))<1e-8:break
            # Unknown-side mixture need not have a globally convex likelihood.
            damping=0.
            for attempt in range(12):
                try:step=cho_solve(cho_factor(H+damping*np.eye(len(x)),lower=True),g);break
                except np.linalg.LinAlgError:damping=1e-4 if damping==0 else damping*10
            else:raise RuntimeError('No positive Newton search matrix')
            alpha=1.
            while obj(x-alpha*step)[0]>l-1e-4*alpha*(g@step) and alpha>1e-8:alpha*=.5
            x-=alpha*step
        l,g,H=obj(x);res=float(max(abs(g)));self.max_gradient=max(self.max_gradient,res)
        if res>2e-4:raise RuntimeError(f'Side MAP gradient {res}')
        # No damping of reported posterior covariance: require a genuine local mode.
        post=cho_solve(cho_factor(H,lower=True),np.eye(len(active)))
        K=self.C[:,active]@Vi;self.m+=K@(x-old);self.C-=K@(V-post)@K.T;self.C=(self.C+self.C.T)/2
        assert np.all(np.diag(self.C)>0)
        self.last_update=self.day

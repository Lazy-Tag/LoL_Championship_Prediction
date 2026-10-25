"""Small symmetric MLP with analytic gradients, chronological validation and Adam."""
import numpy as np
from scipy.special import expit

class Scaler:
 def fit(self,x,reverse):
  a=np.asarray(x+reverse,float);self.median=np.array([np.median(v[np.isfinite(v)]) if np.isfinite(v).any() else 0. for v in a.T]);a=np.where(np.isfinite(a),a,self.median);self.mean=a.mean(0);self.sd=np.maximum(a.std(0),1e-6);return self
 def transform(self,x):
  a=np.asarray(x,float);missing=~np.isfinite(a);a=np.where(missing,self.median,a);return np.concatenate([np.clip((a-self.mean)/self.sd,-10,10),missing.astype(float)],axis=1)
 def record(self):return dict(median=self.median.tolist(),mean=self.mean.tolist(),sd=self.sd.tolist())

class MLP:
 def __init__(self,seed,residual=False):
  self.residual=residual;r=np.random.default_rng(seed);self.p=[r.normal(0,np.sqrt(2/(24+32)),(24,32)),np.zeros(32),r.normal(0,np.sqrt(2/(32+16)),(32,16)),np.zeros(16),r.normal(0,.01,(16,1)),np.zeros(1)]
 def forward(self,x):
  w,b,v,c,u,d=self.p;h=np.tanh(x@w+b);z=np.tanh(h@v+c);return (z@u+d).ravel(),(x,h,z)
 def backward(self,g,cache):
  x,h,z=cache;w,b,v,c,u,d=self.p;gg=g[:,None];gz=(gg@u.T)*(1-z*z);gh=(gz@v.T)*(1-h*h);return [x.T@gh,gh.sum(0),h.T@gz,gz.sum(0),z.T@gg,gg.sum(0)]
 def logits(self,x,rev,offset):
  f,_=self.forward(x);g,_=self.forward(rev);return (offset if self.residual else 0)+(f-g)/2
 def loss_grad(self,x,rev,offset,y,weight):
  f,cache=self.forward(x);g,rcache=self.forward(rev);delta=(f-g)/2;logit=delta+(offset if self.residual else 0);w=weight/weight.sum();loss=np.sum(w*(np.logaddexp(0,logit)-y*logit));deriv=w*(expit(logit)-y)
  if self.residual:loss+=.05*np.sum(w*delta**2);deriv+=.1*w*delta
  a=self.backward(deriv/2,cache);b=self.backward(-deriv/2,rcache);grad=[u+v for u,v in zip(a,b)]
  for i in [0,2,4]:loss+=1e-4*np.sum(self.p[i]**2);grad[i]+=2e-4*self.p[i]
  return float(loss),grad
 def fit(self,x,rev,offset,y,weight,seed,epochs=120,validation=None):
  rng=np.random.default_rng(seed);m=[np.zeros_like(p) for p in self.p];v=[np.zeros_like(p) for p in self.p];step=0;best=float('inf');best_epoch=0;stale=0;curve=[]
  for epoch in range(1,epochs+1):
   order=rng.permutation(len(y))
   for start in range(0,len(y),512):
    ix=order[start:start+512];_,gr=self.loss_grad(x[ix],rev[ix],offset[ix],y[ix],weight[ix]);step+=1
    for j,g in enumerate(gr):
     m[j]=.9*m[j]+.1*g;v[j]=.999*v[j]+.001*g*g;self.p[j]-=.001*(m[j]/(1-.9**step))/(np.sqrt(v[j]/(1-.999**step))+1e-8)
   if validation is not None:
    xx,rr,oo,yy,ww=validation;z=self.logits(xx,rr,oo);loss=float(np.average(np.logaddexp(0,z)-yy*z,weights=ww));curve.append(loss)
    if loss<best-1e-5:best=loss;best_epoch=epoch;stale=0
    else:stale+=1
    if stale>=15:break
  return dict(selected_epochs=best_epoch if validation is not None else epochs,epochs_run=epoch,validation_loss=None if validation is None else best,validation_curve=curve)

def arrays(rows,scaler):
 return (scaler.transform([r['x'] for r in rows]),scaler.transform([r['reverse'] for r in rows]),np.array([r['x'][0] for r in rows]),np.array([r['y'] for r in rows]),np.array([r['w'] for r in rows]))

def fit_model(rows,seed,residual):
 days=sorted({r['date'] for r in rows});split=days[max(1,int(.8*len(days)))];fit=[r for r in rows if r['date']<split];valid=[r for r in rows if r['date']>=split];scale=Scaler().fit([r['x'] for r in fit],[r['reverse'] for r in fit]);net=MLP(seed,residual);info=net.fit(*arrays(fit,scale),seed,validation=arrays(valid,scale))
 # Refit from the same initialization with all pre-event rows and the selected epoch count.
 scale=Scaler().fit([r['x'] for r in rows],[r['reverse'] for r in rows]);net=MLP(seed,residual);net.fit(*arrays(rows,scale),seed,epochs=info['selected_epochs']);info.update(seed=seed,validation_start=split,fit_latest=max(r['date'] for r in fit),validation_latest=max(r['date'] for r in valid),training_series=len(rows),training_maps=sum(r['w'] for r in rows),scaler=scale.record());return net,scale,info

def predict(net,scale,x,rev):return expit(net.logits(scale.transform(x),scale.transform(rev),np.array([r[0] for r in x])))

from datetime import date,timedelta
import numpy as np
from scipy.optimize._numdiff import approx_derivative
from dynamic_side_model import DynamicSideBT,likelihood
from candidate_models import DynamicBT

def main():
 rng=np.random.default_rng(2026);A=rng.normal(size=(7,3));x=rng.normal(size=4)*.4;s=np.array([0,1,-1,0,1,-1,0]);w=np.array([0,1,2,2,0,1,1]);n=np.array([1,1,3,2,1,1,2])
 l,g,H=likelihood(x,A,s,w,n)
 assert np.max(abs(approx_derivative(lambda z:likelihood(z,A,s,w,n)[0],x).ravel()-g))<1e-7
 assert np.max(abs(approx_derivative(lambda z:likelihood(z,A,s,w,n)[1],x)-H))<1e-7
 ll,gg,HH=likelihood(x,-A,-s,n-w,n);assert abs(ll-l)<1e-10 and np.allclose(gg,g) and np.allclose(HH,H)
 teams=['a','b','c'];regions={'a':'X','b':'X','c':'Y'};prior={'X':.2,'Y':-.1};day=date(2025,1,1)
 base=DynamicBT(teams,regions,prior);off=DynamicSideBT(teams,regions,prior,enabled=False)
 for k in range(4):
  d=day+timedelta(days=k*3);rr=[dict(team1='a',team2='b',wins1=2,wins2=1,date=str(d),side1=1),dict(team1='b',team2='c',wins1=0,wins2=1,date=str(d),side1=0)]
  for m in [base,off]:m.advance(d);m.update(rr)
  assert np.allclose(base.m,off.m[:-1],atol=1e-8);assert np.allclose(base.C,off.C[:-1,:-1],atol=1e-8)
 a=DynamicSideBT(teams,regions,prior);b=DynamicSideBT(teams,regions,prior)
 for m,r in [(a,rr),(b,rr[::-1])]:m.advance(d);m.update(r)
 assert np.allclose(a.m,b.m,atol=1e-9) and np.allclose(a.C,b.C,atol=1e-9)
 assert abs(a.predict('a','b')+a.predict('b','a')-1)<1e-12
 assert np.linalg.eigvalsh(a.C).min()>0
 old=a.m.copy();a.advance(d+timedelta(days=90));assert np.allclose(a.m[a.nr:],old[a.nr:]/2)
 try:a.update(rr)
 except AssertionError:pass
 else:raise AssertionError('wrong-day update accepted')
 print('PASS side gradients/Hessian, label symmetry, disabled baseline equivalence, daily permutation, covariance, reciprocity, 90-day decay, date guard.')
if __name__=='__main__':main()

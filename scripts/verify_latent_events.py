"""Sampling moments, within-event persistence and completed-output invariants."""
import hashlib,json,os,shlex,subprocess,sys
from pathlib import Path
import numpy as np
from build_latent_event_engine import source
R=Path(__file__).resolve().parents[1];D=R/'results/latent_events'
PROBE=r'''
#define main tournament_main
#include "event_latent.generated.cpp"
#undef main
int main(){
 n=3;latent=true;rng.seed(2026);
 MU[0]=.2;MU[1]=-.3;MU[2]=.5;
 LC[0][0]=.6;LC[1][0]=.2;LC[1][1]=.5;LC[2][0]=-.1;LC[2][1]=.15;LC[2][2]=.4;
 const int samples=200000;double sum[3]={},cross[3][3]={};int changed=0;double last=-1;
 for(int k=0;k<samples;++k){
  draw_event();double p=match_probability(0,1,0);assert(p==match_probability(0,1,0));
  assert(abs(p+match_probability(1,0,0)-1)<1e-12);
  assert(abs(match_probability(0,1,1)-p*p*(3-2*p))<1e-12);
  if(k&&p!=last)++changed;last=p;
  for(int i=0;i<3;++i){sum[i]+=T[i];for(int j=0;j<3;++j)cross[i][j]+=T[i]*T[j];}
 }
 assert(changed>samples*.99);
 for(int i=0;i<3;++i){assert(abs(sum[i]/samples-MU[i])<.008);for(int j=0;j<3;++j){double expected=0;for(int k=0;k<3;++k)expected+=LC[i][k]*LC[j][k];double observed=cross[i][j]/samples-(sum[i]/samples)*(sum[j]/samples);assert(abs(expected-observed)<.008);}}
 cout<<"PASS joint Gaussian moments, positive/negative covariance, within-event persistence, redraw and probability reciprocity\n";
}
'''

def main():
 build=R/'.local/build';p=build/'verify_latent_probe.cpp';p.write_text(PROBE);clt=Path('/Library/Developer/CommandLineTools/usr/bin/clang++')
 compiler=shlex.split(os.environ['CXX']) if os.environ.get('CXX') else ([str(clt),'-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk'] if clt.exists() else ['c++'])
 subprocess.run([*compiler,'-O3','-std=c++17',str(p),'-o',str(build/'verify_latent_probe')],check=True)
 subprocess.run([str(build/'verify_latent_probe')],check=True)
 if '--sampling-only' in sys.argv:return
 cs=json.loads((D/'event_configs.json').read_text());assert len(cs)==23
 for c in cs:
  assert c['latest_training_date'] is None or c['latest_training_date']<c['start_date']
  cov=np.array(c['joint_covariance']);L=np.array(c['cholesky']);assert np.linalg.eigvalsh(cov).min()>0 and np.allclose(L@L.T,cov,atol=1e-12)
  base=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text()
  for mode in ['posterior','event_form']:
   path=D/mode/f'{c["id"]}.txt';prefix,tail=path.read_text().split('LATENT_EVENT_V1\n');assert prefix.rstrip()==base.rstrip()
   n=len(c['teams']);numbers=np.array(list(map(float,tail.split())));mu=numbers[:n];matrix=numbers[n:].reshape(n,n)
   assert np.allclose(mu,[c['strength'][t] for t in c['teams']],atol=1e-9)
   assert np.allclose(matrix,L if mode=='posterior' else np.eye(n)*.35,atol=1e-12)
   raw=json.loads(path.with_suffix('.json').read_text());N=raw['samples'];assert N==14_000_605 and raw['seed']==c['year']
   assert raw['input_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
   assert raw['engine_sha256']==hashlib.sha256(source().encode()).hexdigest()
   assert all(sum(k for lo,hi,k in bins)==N for bins in raw['counts'])
   assert sum(k for bins in raw['counts'] for lo,hi,k in bins if lo==hi==1)==N
   assert sum((lo+hi)*k for bins in raw['counts'] for lo,hi,k in bins)==N*n*(n+1)
 saved=json.loads((R/'results/form_chain_experiment/summary.json').read_text())
 assert saved['main_pointer_sha256']==hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()
 print('PASS 46 independent full simulations: cutoff, joint covariance mapping, separate arms, counts, ranks, hashes and unchanged main pointer.')
if __name__=='__main__':main()

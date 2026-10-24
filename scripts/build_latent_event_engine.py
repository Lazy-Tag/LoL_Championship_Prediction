"""Isolated event engine with one joint latent strength draw per tournament."""
from pathlib import Path
import hashlib,os,shlex,subprocess
R=Path(__file__).resolve().parents[1]
GLOBALS='''
bool latent=false; double MU[32],LC[32][32],T[32],Q[3][32][32];
uint64_t tick=0,stamp[32][32]={};normal_distribution<double> gaussian(0.,1.);
void draw_event(){
 if(!latent)return;
 ++tick;double z[32];for(int i=0;i<n;++i)z[i]=gaussian(rng);
 for(int i=0;i<n;++i){T[i]=MU[i];for(int j=0;j<=i;++j)T[i]+=LC[i][j]*z[j];}
}
double match_probability(int a,int b,int bo){
 if(!latent)return P[bo][a][b];
 if(stamp[a][b]!=tick){
  double p=1./(1.+exp(T[b]-T[a]));
  Q[0][a][b]=p;Q[1][a][b]=p*p*(3-2*p);Q[2][a][b]=p*p*p*(10-15*p+6*p*p);
  for(int k=0;k<3;++k)Q[k][b][a]=1-Q[k][a][b];
  stamp[a][b]=stamp[b][a]=tick;
 }
 return Q[bo][a][b];
}
'''
READ='''bye_group=readv();
 string mode;
 if(cin>>mode){
  assert(mode=="LATENT_EVENT_V1" && !fair);
  for(int i=0;i<n;++i){cin>>MU[i];assert(cin&&isfinite(MU[i]));}
  for(int i=0;i<n;++i)for(int j=0;j<n;++j){cin>>LC[i][j];assert(cin&&isfinite(LC[i][j]));if(j>i)assert(LC[i][j]==0);if(LC[i][j]!=0)latent=true;}
 }
 auto start='''
def source():
 s=(R/'scripts/event_simulation.cpp').read_text()
 assert s.count('int game(')==1 and s.count('bye_group=readv();auto start=')==1
 s=s.replace('int game(',GLOBALS+'\nint game(',1).replace('unif()<P[bo][a][b]','unif()<match_probability(a,b,bo)')
 s=s.replace('bye_group=readv();auto start=',READ)
 s=s.replace('for(long long sim=0;sim<N;++sim){fill','for(long long sim=0;sim<N;++sim){draw_event();fill')
 # P remains the frozen mean table for opponent choice; latent truth is not revealed.
 return s

def main():
 d=R/'.local/build';d.mkdir(parents=True,exist_ok=True);p=d/'event_latent.generated.cpp';p.write_text(source());clt=Path('/Library/Developer/CommandLineTools/usr/bin/clang++')
 compiler=shlex.split(os.environ['CXX']) if os.environ.get('CXX') else ([str(clt),'-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk'] if clt.exists() else ['c++'])
 subprocess.run([*compiler,'-O3','-std=c++17',str(p),'-o',str(d/'event_latent')],check=True)
 print('Built latent event engine',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()

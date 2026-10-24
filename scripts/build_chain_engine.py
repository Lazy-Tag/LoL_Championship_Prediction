"""Build an isolated extension of the existing event engine; do not alter it."""
from pathlib import Path
import subprocess,hashlib,os,shlex
R=Path(__file__).resolve().parents[1]
INSERT='''bye_group=readv();
 string mode;
 if(cin>>mode){
  assert(mode=="SERIES_PROBABILITIES_V1" && !fair);
  for(int bo=1;bo<=2;++bo)for(int i=0;i<n;++i)for(int j=0;j<n;++j){cin>>P[bo][i][j];assert(cin && isfinite(P[bo][i][j]) && P[bo][i][j]>=0 && P[bo][i][j]<=1);}
  for(int bo=1;bo<=2;++bo)for(int i=0;i<n;++i)for(int j=0;j<n;++j)assert(abs(P[bo][i][j]+P[bo][j][i]-1)<1e-10);
 }
 auto start='''
def source():
 src=(R/'scripts/event_simulation.cpp').read_text();needle='bye_group=readv();auto start=';assert src.count(needle)==1
 return src.replace(needle,INSERT)
def main():
 out=R/'.local/build';out.mkdir(parents=True,exist_ok=True);p=out/'event_chain.generated.cpp';p.write_text(source())
 clt=Path('/Library/Developer/CommandLineTools/usr/bin/clang++')
 compiler=shlex.split(os.environ['CXX']) if os.environ.get('CXX') else ([str(clt),'-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk'] if clt.exists() else ['c++'])
 subprocess.run([*compiler,'-O3','-std=c++17',str(p),'-o',str(out/'event_chain')],check=True)
 print('Built isolated chain engine',hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()

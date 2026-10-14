"""Regenerate fixed-seed simulation input, compile, run, and verify results."""
import json,os,shlex,shutil,subprocess,sys
from pathlib import Path
from model import WORLD_TEAMS
R=Path(__file__).resolve().parents[1]

def main():
 m=json.loads((R/'results/models.json').read_text())['models']['90'];ix={t:i for i,t in enumerate(m['teams'])};teams=list(WORLD_TEAMS.values());regs={r:i for i,r in enumerate(sorted({t[1] for t in teams}))}
 inp=R/'results/simulation_input.txt'
 with inp.open('w') as f:
  f.write(' '.join(str(regs[t[1]]) for t in teams)+'\n')
  for bo in ['bo1','bo3','bo5']:
   for t in teams:f.write(' '.join(str(m[bo][ix[t[0]]][ix[u[0]]]) for u in teams)+'\n')
 build=R/'.local/build';build.mkdir(parents=True,exist_ok=True)
 if os.environ.get('CXX'):compiler=shlex.split(os.environ['CXX'])
 elif sys.platform=='darwin' and Path('/Library/Developer/CommandLineTools/usr/bin/clang++').exists():
  compiler=['/Library/Developer/CommandLineTools/usr/bin/clang++','-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk']
 else:compiler=[shutil.which('c++') or 'c++']
 for name in ['simulate','verify_simulation']:
  subprocess.run(compiler+['-O3','-std=c++17',str(R/f'scripts/{name}.cpp'),'-o',str(build/name)],check=True)
 subprocess.run([str(build/'verify_simulation')],check=True)
 for count,suffix,extra in [(100000,'fair_test',['fair']),(14000605,'raw',[])]:
  print(f'Running {count:,} tournaments, seed=2026, output=simulation_{suffix}.json',flush=True)
  with inp.open() as fin,(R/f'results/simulation_{suffix}.json').open('w') as fout:
   subprocess.run([str(build/'simulate'),str(count),'2026',*extra],stdin=fin,stdout=fout,check=True)
 subprocess.run([sys.executable,str(R/'scripts/report_simulation.py')],check=True)
if __name__=='__main__':main()

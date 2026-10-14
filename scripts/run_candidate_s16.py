"""S16 alternatives, preserving frozen baseline and cutoff; seed 2026."""
import concurrent.futures,json,subprocess,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions,key
from candidate_models import static_fit,DynamicBT
from model import WORLD_TEAMS,series_probability
R=Path(__file__).resolve().parents[1];OUT=R/'results/model_experiments'
def main():
 previous={};preg={}
 for s in range(3,16):
  previous,_=load_season(s);rr=affiliations(previous,s)
  for t,v in preg.items():rr.setdefault(t,v)
  preg=rr
 pr,pa=prior_regions(previous,preg,90)
 raw=json.loads((R/'data/series.json').read_text());rows=[{**r,'team1':key(r['team1']),'team2':key(r['team2'])} for r in raw];teams=sorted({r[k] for r in rows for k in ['team1','team2']})
 reg={};mapping={'LPL':'CN','LCK':'KR','LEC':'EU','LCP':'LCP','LCS':'NA','CBLOL':'BR'}
 for r in rows:
  if r['event'] in mapping:
   for k in ['team1','team2']:reg[r[k]]=mapping[r['event']]
 for t,league,seed in WORLD_TEAMS.values():reg[key(t)]=mapping[league]
 # Known historical labels only; no team strength carried into this season.
 for t,v in preg.items():reg.setdefault(t,v)
 assert all(r['date']<='2026-10-14' for r in rows)
 th,meta=static_fit(rows,teams,reg,pr,date(2026,10,19));dyn=DynamicBT(teams,reg,pr);byday=defaultdict(list)
 for r in rows:byday[r['date']].append(r)
 for day,rr in sorted(byday.items()):dyn.advance(date.fromisoformat(day));dyn.update(rr)
 dyn.advance(date(2026,10,19));states={'hierarchical90':th,'dynamic90':dyn.strengths()}
 (OUT/'s16_states.json').write_text(json.dumps(dict(states=states,regions=reg,prior_audit=pa,metadata=meta,cutoff='2026-10-14',reference='2026-10-19',unknown_regions=sorted(set(teams)-set(reg))),indent=2)+'\n')
 def run(item):
  model,strength=item;out=OUT/model;out.mkdir(exist_ok=True);inp=out/'2026_Worlds.txt';ordered=list(WORLD_TEAMS.values());text=(R/'results/simulation_input.txt').read_text().splitlines()[0]+'\n'
  for bo in [1,3,5]:
   for t in ordered:text+=' '.join(str(float(series_probability(expit(strength[key(t[0])]-strength[key(u[0])]),bo))) for u in ordered)+'\n'
  inp.write_text(text);result=out/'2026_Worlds.json'
  with inp.open('rb') as fin,result.open('wb') as fout,(R/'.local'/f'{model}_s16.log').open('wb') as err:subprocess.run([str(R/'.local/build/simulate'),'14000605','2026'],stdin=fin,stdout=fout,stderr=err,check=True)
  d=json.loads(result.read_text());d.update(model=model,input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),engine_sha256=hashlib.sha256((R/'scripts/simulate.cpp').read_bytes()).hexdigest());result.write_text(json.dumps(d,indent=2)+'\n');print(model,'S16 complete',flush=True)
 with concurrent.futures.ThreadPoolExecutor(2) as pool:list(pool.map(run,states.items()))
if __name__=='__main__':main()

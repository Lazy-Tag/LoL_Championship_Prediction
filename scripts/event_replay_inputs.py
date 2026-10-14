"""Explicit year-specific seed pools plus an auditable engine input serializer."""
import json
from pathlib import Path
import numpy as np
from scipy.special import expit
R=Path(__file__).resolve().parents[1]
POOLS={
 '2023_Worlds':[['gengesports','jdgaming','g2esports','nrg'],['t1','bilibiligaming','fnatic','cloud9'],['ktrolster','lngesports','madlions','teamliquid'],['dpluskia','weibogaming']],
 '2024_Worlds':[['hanwhalifeesports','bilibiligaming','g2esports','flyquest'],['gengesports','topesports','fnatic','teamliquid'],['dpluskia','lngesports','t1','weibogaming'],[]],
 '2025_Worlds':[['gengesports','bilibiligaming','g2esports','flyquest','ctbcflyingoyster'],['hanwhalifeesports','anyoneslegend','movistarkoi','vivokeydstars','teamsecretwhales'],['ktrolster','topesports','fnatic','100thieves','psgtalon']],
 '2023_MSI':[['gengesports','jdgaming'],['madlions','cloud9'],['t1']],
 '2024_MSI':[['gengesports','bilibiligaming'],['g2esports','teamliquid']],
 '2025_MSI':[['gengesports','movistarkoi'],['ctbcflyingoyster','anyoneslegend'],['flyquest','t1']],
}
KINDS={'worlds2013':0,'worlds_groups':0,'worlds_swiss':1,'msi_old':2,'msi_rumble':3,'msi_double':4,'msc':5}
def main():
 configs=json.loads((R/'data/event_replay/configs.json').read_text())
 for c in configs:
  if c['seed'] != c['year'] or c['year'] != c['season'] + 2010:
   raise ValueError(f"{c['id']}: replay seed must equal calendar year")
  c['tiers']=POOLS.get(c['id'],[])
  if c['year']==2025:
   for t,r in c['regions'].items():
    if r in ['NA','BR']:c['regions'][t]='LTA'
  teams=c['teams'];ix={t:i for i,t in enumerate(teams)};regions={r:i for i,r in enumerate(sorted(set(c['regions'].values())))}
  assert all(t in teams for pool in c['tiers'] for t in pool)
  th=np.array([c['strength'][t] for t in teams]);p=expit(th[:,None]-th[None,:])
  out=[f"{c['year']} {KINDS[c['kind']]} {len(teams)}",' '.join(str(regions[c['regions'][t]]) for t in teams)]
  out+=[' '.join(map(str,row)) for row in p]
  def v(seq):return ' '.join([str(len(seq)),*[str(ix[t]) for t in seq]])
  for k in ['groups','main_groups','opening','tiers']:out+=[str(len(c[k]))]+[v(g) for g in c[k]]
  out+=[v(c['direct']),v(c['byes'])]
  out += [' '.join([str(ix['madlions']),str(ix['fnatic'])]) if c['id']=='2022_Worlds' else '-1 -1']
  bg=[c.get('pi_bye_opponents',{}).get(t,-1) for t in c['byes']];out+=[' '.join([str(len(bg)),*map(str,bg)])]
  (R/f'data/event_replay/{c["id"]}.txt').write_text('\n'.join(out)+'\n')
 (R/'data/event_replay/configs.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

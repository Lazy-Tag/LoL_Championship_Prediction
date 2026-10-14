"""Check Markdown links, report coverage, result invariants, and no HTML reports."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]

def main():
 files=[R/'README.md',R/'MODEL.md',R/'AGENTS.md',*sorted((R/'reports').rglob('*.md')),*sorted((R/'docs').rglob('*.md'))]
 broken=[]
 for f in files:
  text=f.read_text()
  assert 'AGENT.md' not in text,str(f)
  for target in re.findall(r'\]\(([^)]+)\)',text):
   if '://' in target or target.startswith('#'):continue
   p=(f.parent/target.split('#')[0]).resolve()
   if not p.exists():broken.append((str(f.relative_to(R)),target))
 assert not broken,broken
 assert not list((R/'results').glob('*.html'))
 assert not list((R/'reports').rglob('*.html'))
 for name in ['README.md','MODEL.md']:
  txt=(R/name).read_text();assert '全局 BP' in txt and '换人' in txt
 pred=json.loads((R/'results/backtest_predictions.json').read_text())
 assert pred and all(r['season']>=4 for r in pred)
 expected=sum(len([r for r in json.loads((R/f'data/history/S{i}/series.json').read_text()) if __import__('backtest').target_event(r['tournament'])]) for i in range(4,16))
 assert len(pred)==expected
 assert all(not r['latest_training_date'] or r['latest_training_date']<r['date'] for r in pred)
 assert len({(r['season'],r['tournament'],r['detail']) for r in pred})==len(pred)
 for season in range(3,16):
  actual=json.loads((R/f'data/history/S{season}/series.json').read_text())
  report=(R/f'reports/history/S{season}/matches.md').read_text()
  assert sum(1 for line in report.splitlines() if line.startswith('| '))-2==len(actual)
  if season==3:
   assert not (R/'reports/history/S3/predictions.md').exists()
   continue
  pp=(R/f'reports/history/S{season}/predictions.md').read_text()
  assert sum(1 for line in pp.splitlines() if line.startswith('| '))-2==sum(r['season']==season for r in pred)
 sim=json.loads((R/'results/s16_championship_simulation.json').read_text());assert sim['simulations']==14000605 and sim['seed']==2026
 assert sum(r['champion_count'] for r in sim['teams'])==14000605
 assert len(sim['teams'])==19
 print(f'PASS {len(files)} Markdown files: local links, limitations, all historical rows, prediction chronology, 19-team simulation totals, no HTML reports.')
if __name__=='__main__':main()

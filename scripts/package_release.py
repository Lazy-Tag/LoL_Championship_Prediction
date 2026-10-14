"""Create a publishable archive using an explicit file allowlist."""
import hashlib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 files=[R/n for n in ['README.md','MODEL.md','AGENTS.md','.gitignore','requirements.txt']]
 for folder,pattern in [('scripts','*.py'),('scripts','*.cpp'),('reports','*.md'),('docs','*.md')]:files.extend((R/folder).rglob(pattern))
 files += [R/'data/series.json',R/'data/history/manifest.json']
 for season in range(3,16):
  files += [R/f'data/history/S{season}/{n}.json' for n in ['series','tournaments','selected_tournaments']]
 files += [p for p in (R/'results').glob('*.json') if p.name not in ['simulation_pilot.json','simulation_fair_test.json']]
 files += [R/'results/simulation_input.txt',R/'results/s16_championship_simulation.md']
 files += list((R/'data/event_replay').glob('*.json')) + list((R/'data/event_replay').glob('*.txt'))
 files += [p for p in (R/'results/event_replay').glob('*.json') if not p.stem.endswith('_pilot')]
 files += list((R/'data/enrichment').glob('*.json'))
 files += list((R/'results/model_experiments').rglob('*.json')) + list((R/'results/model_experiments').rglob('*.txt'))
 manifest=R/'docs/RELEASE_MANIFEST.md';files=sorted(set(p for p in files if p!=manifest))
 lines=['# 发布文件校验清单','','由 `scripts/package_release.py` 生成；清单自身不参与哈希。','','| 文件 | 字节 | SHA256 |','| --- | ---: | --- |']
 for p in files:
  data=p.read_bytes();lines.append(f'| `{p.relative_to(R)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |')
 manifest.write_text('\n'.join(lines)+'\n');files.append(manifest)
 out=R/'dist/LoL_Championship_Prediction.zip';out.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:z.write(p,p.relative_to(R))
 print(f'Created {out.relative_to(R)}: {len(files)} files, {out.stat().st_size:,} bytes; no HTML, raw-page cache, environment, or binary.')
if __name__=='__main__':main()

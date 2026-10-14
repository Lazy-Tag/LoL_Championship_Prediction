"""Retrieve public mirrors with source-specific cache paths and provenance."""
import csv,gzip,hashlib,io,json,urllib.request
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 jobs=[(f'https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/{y}_LoL_esports_match_data_from_OraclesElixir.csv',f'worlds_{y}.csv','Worlds only') for y in range(2016,2023)]
 jobs.append(('https://raw.githubusercontent.com/cbplexiglass/LoL-Esports-Regional-Analyses/main/2025_LoL_esports_match_data_from_OraclesElixir.csv','oe_2025.csv.gz','2025 multiple leagues; not certified complete'))
 out=[]
 for url,name,scope in jobs:
  p=R/'data/raw/enrichment'/name;p.parent.mkdir(parents=True,exist_ok=True)
  e=dict(url=url,raw_path=str(p.relative_to(R)),scope=scope,checked_utc=datetime.now(timezone.utc).isoformat())
  try:
   b=(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes()) if p.exists() else urllib.request.urlopen(url,timeout=60).read()
   assert b.decode('utf-8-sig').startswith('gameid,')
   if not p.exists():p.write_bytes(gzip.compress(b,mtime=0) if p.suffix=='.gz' else b)
   e.update(status='ok',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
  except Exception as exc:e.update(status='unavailable',error=str(exc))
  out.append(e);print(name,e['status'],flush=True)
 (R/'data/enrichment/mirror_sources.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()

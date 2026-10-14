"""Download public OE annual data, retaining hashes, URL and failed access audit."""
import concurrent.futures,csv,gzip,hashlib,io,json,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];RAW=R/'data/raw/enrichment';OUT=R/'data/enrichment'

def main():
 OUT.mkdir(exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
 soup=BeautifulSoup((RAW/'drive_index.html').read_bytes(),'html.parser');jobs=[]
 for x in soup.select('[data-id]'):
  name=x.get('data-tooltip','')
  if '_LoL_esports_' in name:jobs.append((int(name[:4]),x['data-id']))
 def fetch(job):
  y,ident=job;url=f'https://drive.usercontent.google.com/download?id={ident}&export=download&confirm=t';path=RAW/f'direct_oe_{y}.csv.gz'
  entry=dict(year=y,url=url,source_page='https://drive.google.com/drive/u/1/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH',retrieved_utc=datetime.now(timezone.utc).isoformat())
  try:
   if path.exists():b=gzip.decompress(path.read_bytes())
   else:
    b=urllib.request.urlopen(url,timeout=60).read()
    if not b.lstrip(b'\xef\xbb\xbf').startswith(b'gameid,'):
     (RAW/f'oe_{y}_response.html').write_bytes(b);raise ValueError('Response is not CSV (quota/confirmation/error); not treated as data')
    path.write_bytes(gzip.compress(b,mtime=0))
   rr=csv.DictReader(io.StringIO(b.decode('utf-8-sig')));leagues={};dates=[];rows=0
   for row in rr:
    rows+=1;league=row.get('league','');leagues[league]=leagues.get(league,0)+1;dates.append(row.get('date',''))
   entry.update(status='ok',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),rows=rows,leagues=leagues,raw_path=str(path.relative_to(R)))
   print(y,'OK',rows,'rows',flush=True)
  except Exception as e:
   entry.update(status='unavailable',error=str(e));print(y,'UNAVAILABLE',str(e),flush=True)
  return entry
 with concurrent.futures.ThreadPoolExecutor(3) as pool:out=list(pool.map(fetch,jobs))
 (OUT/'sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

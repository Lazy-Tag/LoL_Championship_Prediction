"""Download public supplementary archives; never mix them into model training.
Reuse only ZIP files that pass CRC validation. Keep provenance and failures.
"""
import concurrent.futures,hashlib,json,time,urllib.request,zipfile
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1];RAW=R/'data/raw/detailed';OUT=R/'data/detailed'
SOURCES={'chuckephron':'chuckephron/leagueoflegends','historical_2016_2019':'huitongkou/league-of-legends-pro-matches-data','annual_2020_2025':'toofxd/lol-esports-match-data-from-oracleselixir'}
def main():
 RAW.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
 def fetch(item):
  name,ref=item;url='https://www.kaggle.com/api/v1/datasets/download/'+ref;p=RAW/(name+'.zip');m=dict(id=name,url=url,source_page='https://www.kaggle.com/datasets/'+ref,checked_utc=datetime.now(timezone.utc).isoformat())
  try:
   if not p.exists():
    for attempt in range(3):
     try:
      tmp=p.with_suffix('.part')
      with urllib.request.urlopen(url,timeout=90) as f,tmp.open('wb') as out:
       while chunk:=f.read(1024*1024):out.write(chunk)
      with zipfile.ZipFile(tmp) as z:
       assert z.testzip() is None
      tmp.replace(p);break
     except urllib.error.HTTPError:raise
     except Exception:
      if attempt==2:raise
      time.sleep(1)
   with zipfile.ZipFile(p) as z:
    assert z.testzip() is None;m['files']=[dict(name=i.filename,bytes=i.file_size) for i in z.infolist()]
   m.update(status='ok',path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size);print(name,'OK',len(m['files']),'files',flush=True)
  except Exception as e:m.update(status='failed',error=str(e));print(name,'FAILED',str(e),flush=True)
  return m
 with concurrent.futures.ThreadPoolExecutor(2) as pool:result=list(pool.map(fetch,SOURCES.items()))
 (OUT/'sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()

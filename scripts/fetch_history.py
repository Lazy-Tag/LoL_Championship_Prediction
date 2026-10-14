"""Archive S3-S15 tournament censuses and historical first-tier series results.

Historical BO2 scores must not be silently labeled BO3. Unknown series length
remains null. Source coverage is reported, not assumed globally exhaustive.
"""
import argparse
import concurrent.futures
import gzip
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/history'

def get(url,data=None):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,data=data),timeout=25) as r:return r.read()
        except Exception:
            if attempt==3:raise
            time.sleep(1+attempt)

def selected(name):
    # Historical first-tier circuits, and international competitive events.
    pattern=r'^(?:LPL|LCK|OGN|LCS|NA LCS|EU LCS|LEC|LMS|PCS|VCS|LJL|CBLOL|TCL|LCL|LLA|OPL|LCO|GPL|CLS|LLN|LST|LTA|LCP|MSI|WORLDS|Worlds|World Championship|Season [345] World|IEM|IWC|IWCI|Rift Rivals|Mid.Season Cup|MSC|EWC|Esports World Cup|First Stand|\d{4} First Stand|Americas Cup)(?:\b| )'
    extra=r'^(?:Battle of the Atlantic 2013|All-Star 2014|(?:NA|EU) Regional Qualifiers|(?:\d{4} )?Mid-Season Invitational|Mid-Season Showdown|International Wildcard|Champions Spring 2015)|Rift[- ]Rivals'
    if not (re.search(pattern,name,re.I) or re.search(extra,name,re.I)):return False
    if re.search(r'\b(Academy|Challengers|CL|CLQ|Development|Proving Grounds|Amateur|Scouting|AL)\b',name,re.I):return False
    if re.search(r'\b(LJL|PCS|VCS|TCL|LCL)\b',name,re.I) and '2025' in name:return False
    if name.startswith('TCL ') and re.search(r'\b202[34]\b',name):return False
    return True

def catalog(season):
    folder=OUT/f'S{season}';folder.mkdir(parents=True,exist_ok=True)
    path=folder/'tournaments.json'
    if not path.exists():
        data=get('https://gol.gg/tournament/ajax.trlist.php',urllib.parse.urlencode({'season':f'S{season}'}).encode())
        payload=json.loads(data);assert isinstance(payload,list)
        path.write_bytes(data)
    tournaments=json.loads(path.read_text())
    chosen=list({t['trname']:t for t in tournaments if selected(t['trname'])}.values())
    (folder/'selected_tournaments.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2))
    return season,chosen

def fetch_tournament(task):
    season,t=task;name=t['trname'];folder=OUT/f'S{season}'
    ident=hashlib.sha256(name.encode()).hexdigest()[:16]
    parsed=folder/(ident+'.json');raw=folder/(ident+'.html.gz')
    if parsed.exists():return json.loads(parsed.read_text())
    url='https://gol.gg/tournament/tournament-matchlist/'+urllib.parse.quote(name,safe='')+'/'
    try:
        if raw.exists():body=gzip.decompress(raw.read_bytes())
        else:
            body=get(url);raw.write_bytes(gzip.compress(body,mtime=0))
        soup=BeautifulSoup(body,'html.parser');records=[]
        for row in soup.select('table tr'):
            cells=[c.get_text(' ',strip=True) for c in row.select('td')]
            if len(cells)<7:continue
            score=re.fullmatch(r'(\d+)\s*-\s*(\d+)',cells[2])
            if not score:continue
            link=row.find('a',href=True)
            records.append(dict(team1=cells[1],team2=cells[3],wins1=int(score[1]),wins2=int(score[2]),stage=cells[4],date=cells[-1],best_of=None,best_of_note='Not inferred from score; historical BO2 and special formats exist',detail=urllib.parse.urljoin('https://gol.gg/tournament/',link['href']) if link else None))
        maps=sum(r['wins1']+r['wins2'] for r in records)
        result=dict(season=f'S{season}',tournament=name,source=url,source_census_maps=int(t['nbgames']),parsed_maps=maps,series=records,status='ok' if maps==int(t['nbgames']) else 'count_mismatch',raw_file=raw.name,raw_sha256=hashlib.sha256(body).hexdigest())
        parsed.write_text(json.dumps(result,ensure_ascii=False,indent=2))
        return result
    except Exception as e:
        return dict(season=f'S{season}',tournament=name,source=url,status='fetch_failed',error=str(e),series=[],parsed_maps=0,source_census_maps=int(t['nbgames']))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--catalog-only',action='store_true');ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        catalogs=list(pool.map(catalog,range(3,16)))
    for season,ts in catalogs:print('S'+str(season),'selected',len(ts),'source maps',sum(int(t['nbgames']) for t in ts),flush=True)
    if args.catalog_only:return
    tasks=[(s,t) for s,ts in catalogs for t in ts];results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(fetch_tournament,t):t for t in tasks}
        for future in concurrent.futures.as_completed(futures):
            result=future.result();results.append(result)
            if len(results)%10==0 or result['status']!='ok':print('progress',len(results),'/',len(tasks),result['season'],result['tournament'],result['status'],flush=True)
    summary=[]
    for season,ts in catalogs:
        rr=sorted([r for r in results if r['season']==f'S{season}'],key=lambda r:r['tournament'])
        flat=[dict(season=r['season'],tournament=r['tournament'],source=r['source'],**x) for r in rr for x in r['series']]
        (OUT/f'S{season}'/'series.json').write_text(json.dumps(flat,ensure_ascii=False,indent=2))
        summary.append(dict(season=f'S{season}',catalog_tournaments=len(json.loads((OUT/f'S{season}'/'tournaments.json').read_text())),selected_tournaments=len(ts),downloaded_tournaments=sum(r['status']!='fetch_failed' for r in rr),series=len(flat),maps=sum(r['parsed_maps'] for r in rr),source_census_maps=sum(r['source_census_maps'] for r in rr),issues=[{k:v for k,v in r.items() if k!='series'} for r in rr if r['status']!='ok']))
    manifest=dict(source='Games of Legends',retrieved='2026-10-14/15 Asia/Shanghai',scope='Historical first-tier domestic and competitive international tournaments available in source; selected by explicit name rules. Catalogs also retain excluded tournaments.',limitations=['Source coverage is not proof of all historical matches existing','Historical BO length is null until tournament-specific format verification','Season assignment follows source S3-S15 categories, not simple calendar-year filtering','Regional-to-tier2 transitions and promotion tournaments require care; preserve source names','Counts may include source corrections/forfeits; inspect issues before any fit'],seasons=summary)
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':main()

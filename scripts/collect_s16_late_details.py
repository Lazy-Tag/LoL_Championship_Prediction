"""Resumable July-Oct 2026 top-league/international per-map collection.
Frozen official results define the denominator. Never add training outcomes.
"""
import concurrent.futures,gzip,hashlib,json,re,threading,time,urllib.request,urllib.error
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from prepare_data import ALIASES,key
R=Path(__file__).resolve().parents[1];RAW=R/'data/raw/detailed/s16_jul_oct';OUT=R/'results/s16_jul_oct';WORK=R/'.local/s16_jul_oct';BASE='https://gol.gg'
LOCK=threading.Lock();SOURCES={};ERRORS=[]


def save(p,data):
    p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)

def fetch(url):
    digest=hashlib.sha256(url.encode()).hexdigest()[:20];path=RAW/(digest+'.html.gz');b=None
    if path.exists():
        try:b=gzip.decompress(path.read_bytes())
        except (OSError,EOFError):path.unlink()
    if b is None:
        existing=R/'data/raw/detailed/worlds_2026_2026-10-25'/(digest+'.html')
        if existing.exists():b=existing.read_bytes()
        else:
            for attempt in range(3):
                try:
                    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept-Encoding':'gzip'})
                    with urllib.request.urlopen(request,timeout=40) as response:
                        b=response.read()
                        if response.headers.get('Content-Encoding')=='gzip':b=gzip.decompress(b)
                    if b'<html' not in b.lower() or b'gol.gg' not in b.lower():raise ValueError('Unexpected non-GOL response')
                    break
                except urllib.error.HTTPError as e:
                    with LOCK:ERRORS.append(dict(url=url,error=str(e),attempt=attempt+1))
                    raise
                except (OSError,ValueError) as e:
                    with LOCK:ERRORS.append(dict(url=url,error=str(e),attempt=attempt+1))
                    if attempt==2:raise
                    time.sleep(1+attempt)
        tmp=path.with_suffix('.tmp');tmp.write_bytes(gzip.compress(b,mtime=0));tmp.replace(path)
    with LOCK:SOURCES[url]=dict(url=url,raw_path=str(path.relative_to(R)),sha256=hashlib.sha256(b).hexdigest())
    return BeautifulSoup(b,'html.parser')


def main():
    for p in (RAW,OUT,WORK/'series'):p.mkdir(parents=True,exist_ok=True)
    # Preserve provenance for independently repaired official metadata on resume.
    if (OUT/'sources.json').exists():
        SOURCES.update({x['url']:x for x in json.loads((OUT/'sources.json').read_text())})
    original=json.loads((R/'data/series.json').read_text());live=json.loads((R/'results/live_s16/2026-10-25T015840Z/forecast.json').read_text())
    ids={r['id'] for r in original};targets=[r for r in original if r['date']>='2026-07-01']
    targets += [r for r in live['added_training'] if r['id'] not in ids and r['date']>='2026-07-01']
    assert len(targets)==384 and sum(r['wins1']+r['wins2'] for r in targets)==1026
    names={key(r[k]):r[k] for r in original+live['added_training'] for k in ('team1','team2')};aliases={key(a):b for a,b in ALIASES.items()}
    def norm(name):
        candidate=aliases.get(key(name),name)
        if key(candidate) not in names:raise ValueError('Unknown team alias: '+name)
        return names[key(candidate)]
    candidates=[r for t in json.loads((R/'data/raw/gol_series.json').read_text()) for r in t['series']]
    # Refresh the tournament still in progress at the old Oct14 cutoff.
    url=BASE+'/tournament/tournament-matchlist/Demacia%20Cup%20Global%20Invitational%202026/'
    soup=fetch(url)
    for tr in soup.select('table tr'):
        td=tr.find_all('td');a=tr.find('a',href=True)
        if len(td)!=7 or not a:continue
        score=re.fullmatch(r'(\d+)\s*-\s*(\d+)',td[2].get_text(strip=True))
        if not score:continue
        candidates.append(dict(tournament='Demacia Cup Global Invitational 2026',team1=td[1].get_text(strip=True),team2=td[3].get_text(strip=True),wins1=int(score[1]),wins2=int(score[2]),stage=td[4].get_text(strip=True),date=td[-1].get_text(strip=True),source=url,detail=BASE+'/game/stats/'+re.search(r'/game/stats/(\d+)/',a['href'])[1]+'/page-summary/'))
    # Worlds was already collected and reconciled, and still counts in denominator.
    worlds=json.loads((R/'results/worlds_2026_details/series.json').read_text());world_lookup={r['official_id']:r for r in worlds}
    matches=[];unmatched=[]
    for r in targets:
        if r['id'] in world_lookup:
            c=world_lookup[r['id']];matches.append(dict(official=r,gol=dict(detail=c['summary_url'],date=c['date'],source=c['source'],tournament='Worlds 2026 '+c['stage']),score_conflict=False));continue
        options={}
        for c in candidates:
            try:a,b=norm(c['team1']),norm(c['team2'])
            except ValueError:continue
            if {a,b}!={r['team1'],r['team2']}:continue
            if abs((datetime.fromisoformat(c['date'])-datetime.fromisoformat(r['date'])).days)>1:continue
            if r.get('crosscheck_source') and c['source']!=r['crosscheck_source']:continue
            score={a:c['wins1'],b:c['wins2']};agree=(score[r['team1']],score[r['team2']])==(r['wins1'],r['wins2'])
            known=r['id']=='115548147900553473' and (score[r['team1']],score[r['team2']])==(1,1)
            if agree or known:options[re.search(r'/game/stats/(\d+)/',c['detail'])[1]]=dict(official=r,gol=c,score_conflict=not agree)
        if len(options)==1:matches.append(next(iter(options.values())))
        else:unmatched.append(dict(official=r,candidates=list(options),reason='no unique date/team/score mapping'))
    save(OUT/'targets.json',targets);save(OUT/'series_mapping.json',matches);save(OUT/'unmatched.json',unmatched)
    print('Targets',len(targets),'series / 1026 maps; mapped',len(matches),'unmatched',len(unmatched),flush=True)
    def collect(item):
        r=item['official'];path=WORK/'series'/(r['id']+'.json')
        if path.exists():return json.loads(path.read_text())
        try:
            soup=fetch(item['gol']['detail']);links=set()
            for a in soup.find_all('a',href=True):
                n=re.fullmatch(r'Game (\d+)',a.get_text(' ',strip=True));gid=re.search(r'/game/stats/(\d+)/page-game/',a['href'])
                if n and gid:links.add((int(n[1]),gid[1]))
            links=sorted(links);assert len(links)==r['wins1']+r['wins2'],('map count',links)
            games=[]
            for number,gid in links:
                u=BASE+'/game/stats/'+gid+'/page-game/';fu=u.replace('page-game','page-fullstats');game=fetch(u);full=fetch(fu)
                teams={}
                for side in ('blue','red'):
                    tag=game.select_one('.'+side+'-line-header');assert tag and tag.find('a'),('side header',gid)
                    teams[side]=dict(name=norm(tag.find('a').get_text(strip=True)),win=int(tag.get_text(' ',strip=True).endswith('WIN')))
                assert {t['name'] for t in teams.values()}=={r['team1'],r['team2']} and sum(t['win'] for t in teams.values())==1
                table=full.select_one('table.completestats');assert table,('missing full stats',gid)
                fields={};champions=[]
                for tr in table.find_all('tr'):
                    cells=tr.find_all(['th','td'])
                    if len(cells)!=11:continue
                    label=cells[0].get_text(' ',strip=True)
                    if not label:champions=[Path(c.find('img')['src']).stem if c.find('img') else None for c in cells[1:]];continue
                    fields[label]=[c.get_text(' ',strip=True) for c in cells[1:]]
                    if label=='Player':
                        for i,c in enumerate(cells[1:]):assert ('blueside' if i<5 else 'redside') in c.get('style','')
                assert len(fields.get('Player',[]))==10 and all(fields['Player']) and len(champions)==10
                def integer(value):
                    try:return int(value.replace(',',''))
                    except (ValueError,AttributeError):return None
                for side,offset in [('blue',0),('red',5)]:
                    teams[side]['players']=[dict(name=fields['Player'][i],role=fields.get('Role',['']*10)[i],champion_asset=champions[i],stats={k:v[i] for k,v in fields.items() if k not in ('Player','Role')}) for i in range(offset,offset+5)]
                    assert len(set(p['name'] for p in teams[side]['players']))==5
                    for source,dest in [('Golds','total_gold'),('GD@15','gold_difference_15'),('CS','cs'),('Kills','kills')]:
                        vals=[integer(v) for v in fields.get(source,['']*10)[offset:offset+5]];teams[side][dest]=sum(vals) if all(v is not None for v in vals) else None
                gd=[t['gold_difference_15'] for t in teams.values()]
                if all(v is not None for v in gd):assert sum(gd)==0
                text=game.get_text(' ',strip=True);patch=re.search(r'\bv(\d+\.\d+)\b',text);duration=next((h.get_text(strip=True) for h in game.find_all('h1') if re.fullmatch(r'\d+:\d\d',h.get_text(strip=True))),None)
                games.append(dict(game_id=gid,game=number,official_series_id=r['id'],event=r['event'],official_date=r['date'],official_start_utc=r['start_utc'],source_date=item['gol']['date'],source_tournament=item['gol'].get('tournament'),sources=[u,fu],patch=patch[1] if patch else None,duration=duration,teams=teams))
            score=Counter(t['name'] for g in games for t in g['teams'].values() if t['win'])
            verified=(score[r['team1']],score[r['team2']])==(r['wins1'],r['wins2'])
            result=dict(official=r,gol=item['gol'],status='verified' if verified else 'map_score_conflict',catalog_score_conflict=item['score_conflict'],games=games,source_map_score={r['team1']:score[r['team1']],r['team2']:score[r['team2']]})
            save(path,result);return result
        except Exception as e:
            return dict(official=r,gol=item['gol'],status='failed',error=str(e))
    results=[]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        futures={pool.submit(collect,item):item for item in matches}
        for future in concurrent.futures.as_completed(futures):
            result=future.result();results.append(result)
            if len(results)%10==0 or result['status']!='verified':
                counts=Counter(x['status'] for x in results);print('Processed',len(results),'/',len(matches),dict(counts),result.get('error',''),flush=True)
                save(WORK/'progress.json',dict(processed=len(results),total=len(matches),status=dict(counts)))
    results.sort(key=lambda x:(x['official']['date'],x['official']['id']))
    # Reconstruct provenance for cached completed series on resumed runs.
    for item in results:
        urls=[item['gol']['detail']]+[u for g in item.get('games',[]) for u in g['sources']]
        for url in urls:
            path=RAW/(hashlib.sha256(url.encode()).hexdigest()[:20]+'.html.gz')
            if path.exists():SOURCES[url]=dict(url=url,raw_path=str(path.relative_to(R)),sha256=hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest())
    save(OUT/'series.json',results);save(OUT/'sources.json',list(SOURCES.values()));save(OUT/'download_errors.json',ERRORS)
    print('DONE',dict(Counter(x['status'] for x in results)),'maps',sum(len(x.get('games',[])) for x in results),flush=True)

if __name__=='__main__':main()

"""Fetch an independent tournament census and series score tables."""
import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

def selected(name):
    return bool(re.match(r'^(LPL 2026|LCK (2026|Cup 2026)|LEC 2026|LCS 2026|LCP 2026|CBLOL (2026|Cup 2026)|2026 First Stand|MSI 2026|EWC 2026|Esports World Cup 2026|Americas Cup 2026|Demacia Cup Global Invitational 2026)', name))

def main():
    catalog = ROOT/'data/raw/gol_tournaments.json'
    catalog.parent.mkdir(parents=True, exist_ok=True)
    if not catalog.exists():
        request = urllib.request.Request('https://gol.gg/tournament/ajax.trlist.php', data=urllib.parse.urlencode({'season':'S16'}).encode())
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.load(response)
        assert isinstance(payload, list)
        catalog.write_text(json.dumps(payload, ensure_ascii=False))
    tournaments = [t for t in json.loads(catalog.read_text()) if selected(t['trname'])]
    out = ROOT/'data/raw/gol'
    out.mkdir(exist_ok=True)
    def fetch(t):
        name = t['trname']
        path = out/(name.replace('/', '_')+'.html')
        url = 'https://gol.gg/tournament/tournament-matchlist/'+urllib.parse.quote(name, safe='')+'/'
        if not path.exists():
            for attempt in range(4):
                try:
                    path.write_bytes(urllib.request.urlopen(url, timeout=20).read())
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    time.sleep(1)
        soup = BeautifulSoup(path.read_bytes(), 'html.parser')
        records = []
        for row in soup.select('table tr'):
            cells = [c.get_text(' ', strip=True) for c in row.select('td')]
            if len(cells) < 7:
                continue
            score = re.fullmatch(r'(\d+)\s*-\s*(\d+)', cells[2])
            if not score:
                continue
            link = row.find('a', href=True)
            records.append(dict(tournament=name, team1=cells[1], team2=cells[3], wins1=int(score[1]), wins2=int(score[2]), stage=cells[4], date=cells[-1], source=url, detail=urllib.parse.urljoin('https://gol.gg/tournament/', link['href']) if link else ''))
        maps = sum(r['wins1']+r['wins2'] for r in records)
        print(name, 'series',len(records),'maps',maps,'census',t['nbgames'],flush=True)
        return dict(**t,parsed_maps=maps,series=records,source=url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(fetch, tournaments))
    (ROOT/'data/raw/gol_series.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()

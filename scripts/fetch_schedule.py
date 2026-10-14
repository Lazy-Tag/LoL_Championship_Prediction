"""Archive public Riot schedule pages; never silently skip failed pages."""
import argparse
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--public-client-reference', default='/tmp/schedule_reference.py')
    args = ap.parse_args()
    key = os.environ.get('RIOT_PUBLIC_CLIENT_KEY')
    if not key:
        reference = Path(args.public_client_reference)
        if not reference.exists():
            ap.error('Set RIOT_PUBLIC_CLIENT_KEY or provide --public-client-reference. Offline computation from archived normalized data does not require a key.')
        match = re.search(r'LOLESPORTS_API_KEY = "([^"]+)"', reference.read_text())
        if not match:
            ap.error('Public client reference has no recognized key assignment.')
        key = match[1]
    out = ROOT / 'data/raw/riot_schedule'
    out.mkdir(parents=True, exist_ok=True)
    base = 'https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US'
    def fetch(token, filename):
        path = out / filename
        if path.exists():
            return json.loads(path.read_text())
        url = base + ('&' + urllib.parse.urlencode({'pageToken': token}) if token else '')
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={'x-api-key': key})
                with urllib.request.urlopen(req, timeout=30) as r:
                    payload = json.load(r)
                assert 'schedule' in payload['data']
                path.write_text(json.dumps(payload, ensure_ascii=False))
                return payload
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2)
    first = fetch('', 'first.json')['data']['schedule']
    for direction in ['older', 'newer']:
        page = first
        seen = set()
        for n in range(500):
            token = page['pages'].get(direction)
            if not token or token in seen:
                break
            seen.add(token)
            page = fetch(token, f'{direction}_{n:03d}.json')['data']['schedule']
            dates = [e['startTime'] for e in page['events']]
            print(direction, n, len(dates), min(dates, default=''), max(dates, default=''), flush=True)
            if direction == 'older' and dates and max(dates) < '2026-01-01':
                break
            if direction == 'newer' and dates and min(dates) > '2026-10-14T16:00:00Z':
                break
        else:
            raise RuntimeError('Pagination bound reached')
    events = {}
    for path in out.glob('*.json'):
        for e in json.loads(path.read_text())['data']['schedule']['events']:
            if e.get('type') == 'match':
                events[e['match']['id']] = e
    (ROOT / 'data/raw/riot_events.json').write_text(json.dumps(list(events.values()), ensure_ascii=False, indent=2))
    print('Unique match events:', len(events), flush=True)

if __name__ == '__main__':
    main()

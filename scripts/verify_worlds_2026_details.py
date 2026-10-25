"""Independently verify all supplemental maps against frozen official scores."""
import json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'results/worlds_2026_details'
def main():
    games=json.loads((D/'games.json').read_text());series=json.loads((D/'series.json').read_text())
    official=json.loads((R/'results/live_s16/2026-10-25T015840Z/forecast.json').read_text())['completed_worlds'];lookup={e['id']:e for e in official}
    assert len(games)==len({g['game_id'] for g in games})==38
    assert len(series)==len({r['official_id'] for r in series})==len(official)==22
    for r in series:
        e=lookup[r['official_id']];gg=[g for g in games if g['official_series_id']==e['id']]
        assert sorted(g['game'] for g in gg)==list(range(1,len(gg)+1))
        score=Counter(t['code'] for g in gg for t in g['teams'].values() if t['win'])
        for t in e['teams']:assert score[t['code']]==t['wins']
        for g in gg:
            assert {t['code'] for t in g['teams'].values()}=={t['code'] for t in e['teams']}
            assert sum(t['win'] for t in g['teams'].values())==1
            for t in g['teams'].values():
                assert len(t['players'])==5 and len({p['name'] for p in t['players']})==5
                assert set(p['role'] for p in t['players'])=={'TOP','JUNGLE','MID','ADC','SUPPORT'}
                assert sum(int(p['stats']['Golds']) for p in t['players'])==t['total_gold']
    rosters=json.loads((D/'current_rosters.json').read_text());assert len(rosters)==len({r['code'] for r in rosters})==19
    for r in rosters:assert abs(sum(r['shares'].values())-1)<1e-12
    assert json.loads((D/'audit.json').read_text())['training_outcomes_added']==0
    print('PASS 22 official series, 38 unique complete maps, 19 actual lineups, role sets, individual/team gold sums, complete score reconciliation, no added training outcomes')
if __name__=='__main__':main()

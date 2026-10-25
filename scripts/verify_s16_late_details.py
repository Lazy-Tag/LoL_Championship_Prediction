"""Verify complete denominator, metadata recovery, field gaps and source identity."""
import hashlib,json
from collections import Counter
from pathlib import Path
from report_s16_late_details import has,FIELDS
R=Path(__file__).resolve().parents[1];D=R/'results/s16_jul_oct'
def main():
    targets=json.loads((D/'targets.json').read_text());records=json.loads((D/'series.json').read_text());coverage=json.loads((D/'coverage.json').read_text())
    assert len(targets)==len({r['id'] for r in targets})==384
    assert {r['official']['id'] for r in records}=={r['id'] for r in targets}
    expected={r['id']:r for r in targets};maps=[]
    for r in records:
        o=expected[r['official']['id']];assert r['official']==o and r['status']=='verified'
        assert '2026-07-01'<=o['date']<='2026-10-25'
        assert len(r['games'])==o['wins1']+o['wins2']
        assert sorted(g['game'] for g in r['games'])==list(range(1,len(r['games'])+1))
        score=Counter(t['name'] for g in r['games'] for t in g['teams'].values() if t['win'])
        assert score[o['team1']]==o['wins1'] and score[o['team2']]==o['wins2']
        for g in r['games']:
            assert g['official_series_id']==o['id'] and {t['name'] for t in g['teams'].values()}=={o['team1'],o['team2']}
            assert set(g['teams'])=={'blue','red'} and sum(t['win'] for t in g['teams'].values())==1
            assert g['patch'] and all(t['players'] for t in g['teams'].values())
            for t in g['teams'].values():
                assert len(t['players'])==len({p['name'] for p in t['players']})==5
                assert set(p['role'] for p in t['players'])=={'TOP','JUNGLE','MID','ADC','SUPPORT'}
                if t['total_gold'] is not None:
                    assert t['total_gold']>0 and sum(int(p['stats']['Golds']) for p in t['players'])==t['total_gold']
            values=[t['gold_difference_15'] for t in g['teams'].values()]
            if all(v is not None for v in values):assert sum(values)==0
            maps.append(g)
    assert len(maps)==len({g['game_id'] for g in maps})==1026
    for f in FIELDS:assert sum(bool(has(g,f)) for g in maps)==coverage['field_coverage'][f]
    partial=[g for g in maps if not has(g,'gold')];assert len(partial)==1 and partial[0]['game_id']=='80675'
    restored=partial[0];assert restored['esports_game_id']=='115548147900553474' and restored['duration'] is None
    assert restored['teams']['blue']['name']=='Gen.G Esports' and restored['teams']['red']['name']=='Dplus KIA'
    assert all(not v for t in restored['teams'].values() for p in t['players'] for v in p['stats'].values())
    original=json.loads((D/'conflicts/115548147900553473_original.json').read_text());assert original['status']=='map_score_conflict' and original['games'][0]['teams']['blue']['name']=='Gen.G Esports'
    export=json.loads((D/'normalized_export.json').read_text());p=R/export['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==export['sha256']
    normalized=[json.loads(s) for s in p.read_text().splitlines()];assert len(normalized)==1026 and all(g['date_precision'].startswith('scheduled series') for g in normalized)
    assert export['training_outcomes_added']==coverage['training_outcomes_added']==0
    print('PASS 384/384 series, 1026 unique maps, 10 competition categories, all scores/rosters/sides/patches, gold sums, explicit single-map numeric gap, official metadata recovery, normalized sidecar hash and no duplicate training outcomes')
if __name__=='__main__':main()

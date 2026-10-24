"""Check known results, fixed pairings, partial-round conditioning and publication."""
import copy
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from update_live_s16 import ROOT, OUT, LOCAL, build_state, verify, CODES

def main():
    latest=json.loads((OUT/'latest.json').read_text())
    folder=OUT/latest['snapshot'];d=json.loads((folder/'forecast.json').read_text());verify(d)
    events=json.loads((OUT/'observed_events.json').read_text())
    active,w,l,met,done,fixed=build_state(events,datetime.now(timezone.utc))
    assert d['wins']==w and d['losses']==l and d['met']==met
    assert d['simulations']==14_000_605 and d['seed']==2026
    for matrix in d['probabilities']:
        for i in range(19):
            for j in range(19):assert abs(matrix[i][j]+matrix[j][i]-1)<1e-10
    assert len({r['id'] for r in d['added_training']})==len(d['added_training'])
    base={r['id'] for r in json.loads((ROOT/'data/series.json').read_text())}
    assert not base&{r['id'] for r in d['added_training']}
    # Simulate one published next match having finished: it must not be replayed.
    if fixed:
        changed=copy.deepcopy(events);match=next(e for e in changed if e['id']==fixed[0]['id'])
        match['state']='completed';match['teams'][0]['wins']=match['best_of']//2+1;match['teams'][1]['wins']=0
        aa,ww,ll,mm,dd,ff=build_state(changed,datetime.now(timezone.utc))
        assert len(dd)==len(done)+1 and len(ff)==len(fixed)-1
        a,b=fixed[0]['a'],fixed[0]['b'];assert ww[a]==w[a]+1 and ll[b]==l[b]+1
        lines=(folder/'input.txt').read_text().splitlines()[:58]
        lines+=['16',' '.join(map(str,aa))]+[f'{ww[i]} {ll[i]} {mm[i]}' for i in range(19)]+[str(len(ff))]
        lines += [f'{f["round"]} {f["a"]} {f["b"]} {(1,3,5).index(f["best_of"])}' for f in ff]
        run=subprocess.run([str(LOCAL/'simulate_live'),'10000','2026'],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
        result=json.loads(run.stdout);result.update(active=aa,wins=ww,losses=ll);verify(result)
        # Invalid finished scores cannot enter state.
        match['teams'][0]['wins']=0
        try:build_state(changed,datetime.now(timezone.utc))
        except AssertionError:pass
        else:raise AssertionError('Invalid score accepted')
    assert (ROOT/latest['report']).exists()
    print('Live forecast verified: totals, joint distributions, probabilities, no duplicates, partial round, invalid score rejection')

if __name__=='__main__':main()

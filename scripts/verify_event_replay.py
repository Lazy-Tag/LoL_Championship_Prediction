"""Meaningful invariants; these tests do not certify official rule fidelity."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
from backtest import domestic_region, affiliations, load_season
from report_event_replay import common_band

R=Path(__file__).resolve().parents[1]
N=14_000_605

def main():
    cs=json.loads((R/'data/event_replay/configs.json').read_text())
    summary=json.loads((R/'results/event_replay/summary.json').read_text())
    assert len(cs)==len(summary['events'])==23
    assert summary['total_simulations']==23*N
    for c,e in zip(cs,summary['events']):
        r=json.loads((R/f"results/event_replay/{c['id']}.json").read_text())
        assert c['id']==e['id'] and r['samples']==N and r['seed']==c['year']==c['season']+2010
        assert r['half_life_days']==90
        assert not c['latest_training_date'] or c['latest_training_date']<c['start_date']
        assert not c['prior_audit'].get('last_date') or c['prior_audit']['last_date']<c['start_date']
        assert r['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
        assert r['input_sha256']==hashlib.sha256((R/f"data/event_replay/{c['id']}.txt").read_bytes()).hexdigest()
        assert len(r['counts'])==len(c['teams'])==len(c['actual_ranks'])
        for bins in r['counts']:
            assert sum(k for lo,hi,k in bins)==N
            assert all(1<=lo<=hi<=len(c['teams']) and k>0 for lo,hi,k in bins)
        assert sum(k for bins in r['counts'] for lo,hi,k in bins if lo==hi==1)==N
        assert sum((lo+hi)*k for bins in r['counts'] for lo,hi,k in bins)==N*len(c['teams'])*(len(c['teams'])+1)
        assert sum(x['actual_band']==[1,1] for x in e['teams'])==1
        assert abs(sum(t['title_probability'] for t in e['teams'])-1)<1e-12
        for t in e['teams']:
            assert abs(sum(x['probability'] for x in t['finish_distribution'])-1)<1e-12
            assert tuple(t['actual_band'])==common_band(c,*c['actual_ranks'][t['team']])
    # The failure discovered at scale must not recur through metadata inference.
    assert domestic_region('GPL-OPL-LJL Rift Rivals 2017') is None
    rows,_=load_season(7);regions=affiliations(rows,7)
    for t,reg in {'rampage':'JP','direwolves':'OCE','1907fenerbahce':'TR','lyongaming':'LAN'}.items():assert regions[t]==reg
    binary=R/'.local/build/event_simulation'
    # Independent equal-strength expectations for direct entrants vs play-in entrants.
    for name in ['2023_MSI','2024_MSI','2025_MSI']:
        c=next(x for x in cs if x['id']==name)
        inp=(R/f'data/event_replay/{name}.txt').read_bytes()
        sample=200_000
        r=json.loads(subprocess.run([str(binary),str(sample),'fair'],input=inp,capture_output=True,check=True).stdout)
        direct=set(c['byes'] if name=='2013_Worlds' else c['direct'])
        pother=.05 if name=='2013_Worlds' else (1-len(direct)/8)/(len(c['teams'])-len(direct))
        for team,bins in zip(c['teams'],r['counts']):
            expected=.125 if team in direct else pother
            observed=sum(k for lo,hi,k in bins if lo==hi==1)/sample
            assert abs(observed-expected)<6*math.sqrt(expected*(1-expected)/sample),(name,team,observed,expected)
    inp=(R/'data/event_replay/2025_Worlds.txt').read_bytes()
    runs=[json.loads(subprocess.run([str(binary),'1000'],input=inp,capture_output=True,check=True).stdout) for _ in range(2)]
    for r in runs:r.pop('seconds')
    assert runs[0]==runs[1]
    print('PASS: 23 formal counts and hashes; year seeds; pre-event cutoffs; probability/rank conservation; 2017 region regression; independent fair-title expectations; deterministic rerun.')

if __name__=='__main__':main()

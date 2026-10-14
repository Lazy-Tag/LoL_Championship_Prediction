import itertools
import json
import math
from pathlib import Path
import numpy as np
from model import fit,series_probability
from exact_tournament import playin,knockout_fixed_bracket,knockout_all_draws

ROOT=Path(__file__).resolve().parents[1]

def main():
    rows=json.loads((ROOT/'data/series.json').read_text())
    assert len({r['id'] for r in rows})==len(rows)
    assert all('2026-01-01'<=r['date']<='2026-10-14' for r in rows)
    audit=json.loads((ROOT/'results/data_audit.json').read_text())
    assert not audit['unmatched_gol'] and not audit['unmatched_official']
    for bo in [1,3,5]:
        for p in [0,.01,.2,.5,.7,.99,1]:
            brute=sum(math.comb(bo,k)*p**k*(1-p)**(bo-k) for k in range(bo//2+1,bo+1))
            assert abs(brute-series_probability(p,bo))<1e-14
    # Score aggregation must preserve the MLE when each actual map is expanded.
    toy=[dict(team1='A',team2='B',wins1=3,wins2=2,date='2026-09-01'),dict(team1='B',team2='C',wins1=2,wins2=1,date='2026-08-01'),dict(team1='C',team2='A',wins1=2,wins2=0,date='2026-07-01')]
    expanded=[]
    for r in toy:
        expanded.extend([{**r,'wins1':1,'wins2':0}]*r['wins1'])
        expanded.extend([{**r,'wins1':0,'wins2':1}]*r['wins2'])
    assert np.max(np.abs(np.array(fit(toy,90)['bo1'])-fit(expanded,90)['bo1']))<1e-12
    # Symmetry and fully deterministic cases exercise the double-elimination path.
    teams=['C9','KC','FUR','MVK'];P={a:{b:.5 for b in teams} for a in teams}
    ans,check=playin(P);assert all(abs(x-.25)<1e-15 for x in ans.values())
    P={a:{b:float(i<j) if i!=j else .5 for j,b in enumerate(teams)} for i,a in enumerate(teams)}
    ans,_=playin(P);assert ans['C9']==1
    # Independently enumerate all 128 knockout outcome paths and compare tree DP.
    teams=list('ABCDEFGH');s={t:i*.2 for i,t in enumerate(teams)}
    P={a:{b:1/(1+math.exp(s[b]-s[a])) for b in teams} for a in teams}
    brute={t:0. for t in teams}
    for outcomes in itertools.product([0,1],repeat=7):
        alive=teams[:];prob=1.;k=0
        while len(alive)>1:
            nxt=[]
            for i in range(0,len(alive),2):
                a,b=alive[i:i+2];w,l=(a,b) if outcomes[k]==0 else (b,a);k+=1;prob*=P[w][l];nxt.append(w)
            alive=nxt
        brute[alive[0]]+=prob
    dp=knockout_fixed_bracket(teams,P)
    assert max(abs(dp[t]-brute[t]) for t in teams)<1e-14
    fair={a:{b:.5 for b in teams} for a in teams}
    all_draws=knockout_all_draws(teams[:2],teams[2:5],teams[5:],fair)
    assert all(abs(v-.125)<1e-14 for v in all_draws.values())
    models=json.loads((ROOT/'results/models.json').read_text())['models']
    for m in models.values():
        assert m['diagnostics']['gradient_inf']<1e-9
        for bo in ['bo1','bo3','bo5']:
            p=np.array(m[bo]);assert np.max(np.abs(p+p.T-1))<1e-13
            assert np.min(p)>0 and np.max(p)<1
    print('PASS: coverage reconciliation, IDs, cutoff, BO polynomials, sufficient-statistic equivalence, play-in symmetry/determinism, knockout 128-path independent enumeration, 36-draw symmetry, MLE gradients and reciprocity.')

if __name__=='__main__':main()

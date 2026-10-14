"""Exact finite sums for play-in and conditional knockout; no Monte Carlo."""
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from model import WORLD_TEAMS

ROOT=Path(__file__).resolve().parents[1]

def outcome(a,b,P):
    yield a,b,P[a][b]
    yield b,a,P[b][a]

def playin(P):
    result=defaultdict(float);leaves=0;mass=0.
    for w1,l1,p1 in outcome('C9','KC',P):
      for w2,l2,p2 in outcome('FUR','MVK',P):
       for wu,lu,pu in outcome(w1,w2,P):
        for wl,ll,pl in outcome(l1,l2,P):
         for wlf,llf,plf in outcome(lu,wl,P):
          for champion,runner,pf in outcome(wu,wlf,P):
            prob=p1*p2*pu*pl*plf*pf;result[champion]+=prob;mass+=prob;leaves+=1
    assert leaves==64 and abs(mass-1)<1e-12
    return dict(result),dict(terminal_paths=leaves,probability_mass=mass)

def combine(left,right,P):
    result=defaultdict(float)
    for a,pa in left.items():
        for b,pb in right.items():
            result[a]+=pa*pb*P[a][b];result[b]+=pa*pb*P[b][a]
    return dict(result)

def knockout_fixed_bracket(teams,P):
    """Leaf order: QF1/QF2 in half 1, QF3/QF4 in half 2."""
    assert len(teams)==8 and len(set(teams))==8
    nodes=[{t:1.} for t in teams]
    while len(nodes)>1:nodes=[combine(nodes[i],nodes[i+1],P) for i in range(0,len(nodes),2)]
    assert abs(sum(nodes[0].values())-1)<1e-12
    return nodes[0]

def knockout_all_draws(three_zero,three_one,three_two,P):
    """Exact average over 36 equally probable labeled bracket equivalence classes.

    Fix the two 3-0 teams in opposite halves. Select ordered 3-2 opponents
    (3*2), then choose the two of four remaining teams for the first half (6).
    Quarterfinal within-pair ordering and top/bottom symmetry are irrelevant
    because this model has no side advantage.
    """
    assert list(map(len,[three_zero,three_one,three_two]))==[2,3,3]
    assert len(set(three_zero+three_one+three_two))==8
    result=defaultdict(float);count=0
    for a,b in itertools.permutations(three_two,2):
        remaining=three_one+[t for t in three_two if t not in [a,b]]
        for pair in itertools.combinations(remaining,2):
            other=[t for t in remaining if t not in pair]
            bracket=[three_zero[0],a,*pair,three_zero[1],b,*other]
            for t,p in knockout_fixed_bracket(bracket,P).items():result[t]+=p/36
            count+=1
    assert count==36 and abs(sum(result.values())-1)<1e-12
    return dict(result)

def main():
    data=json.loads((ROOT/'results/models.json').read_text());all_results={}
    for h,m in data['models'].items():
        ix={t:i for i,t in enumerate(m['teams'])}
        P={c:{d:m['bo5'][ix[t[0]]][ix[u[0]]] for d,u in WORLD_TEAMS.items()} for c,t in WORLD_TEAMS.items()}
        advancement,check=playin(P)
        all_results[h]=dict(swiss_qualification=advancement,audit=check,opening_bo5={'C9_vs_KC':P['C9']['KC'],'FUR_vs_MVK':P['FUR']['MVK']})
    # Branch counts are for a naive enumeration, NOT a lower bound on every DP.
    complexity=dict(swiss_series=33,swiss_outcome_paths_for_one_adaptive_draw_policy=2**33,playin_outcome_paths=64,knockout_outcome_paths_per_fixed_bracket=128,round2_pairings_per_record_group=105,round2_pairings_both_groups=105**2,raw_prefixes_after_two_swiss_rounds_fixed_initial_draw=2**8*105**2*2**8,raw_prefix_storage_at_96_bytes=2**8*105**2*2**8*96,knockout_draw_equivalence_classes=36,naive_full_paths_without_swiss_draw_branching=64*2**33*128,warning='Raw path counts do not prove a lower bound for optimized exact algorithms. Opponent histories cannot be discarded under the no-rematch rule. Full Swiss state enumeration has not been performed.')
    out=dict(status='PARTIAL_EXACT_NO_WORLD_CHAMPION_PROBABILITIES',playin=all_results,complexity=complexity,numerics='Analytical finite sums evaluated with IEEE-754 floating point; not symbolic rational probabilities',full_tournament_limitations=['No full Swiss-state sum performed','Draw slide-to-next-slot procedure is not uniform sampling over valid matchings','Rule 4.3.3.2 permits officials to waive no-rematch if no eligible draw; no probability law for discretion supplied','Selection/draft rights not modeled; probabilities conditional on neutral-side independent-map BT model'])
    (ROOT/'results/exact_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

"""Event-local generalized-Bayes likelihood weight; does not alter raw scores.

A power w multiplies each current-event map log likelihood once. These are
pseudo-counts, not extra observed games; original DynamicBT remains unchanged.
"""
import math
from backtest import target_event

WEIGHTS=(1.,1.25,1.5,2.,3.,4.)

def weighted_rows(rows,event,weight):
    assert math.isfinite(weight) and 1<=weight<=4
    out=[]
    for r in rows:
        is_event=(target_event(r.get('tournament',''))==event if 'tournament' in r else r.get('event')==event)
        scale=weight if is_event else 1.
        out.append({**r,'wins1':r['wins1']*scale,'wins2':r['wins2']*scale})
    return out

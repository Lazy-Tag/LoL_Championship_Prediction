"""Independent weighting identity and event/year isolation checks."""
import copy,json,hashlib
from datetime import date
import numpy as np
from candidate_models import DynamicBT
from event_weighting import weighted_rows,WEIGHTS
from evaluate_event_weighting import R,OUT,select,metrics,bootstrap,report

def main():
    rows=[dict(tournament='World Championship 2025',team1='a',team2='b',wins1=2,wins2=1,date='2025-10-12'),dict(tournament='LCK 2025',team1='a',team2='c',wins1=0,wins2=2,date='2025-10-12')]
    original=copy.deepcopy(rows)
    a=DynamicBT(['a','b','c'],{'a':'KR','b':'CN','c':'KR'},{})
    a.advance(date(2025,10,12));b=copy.deepcopy(a);c=copy.deepcopy(a)
    a.update(weighted_rows(rows,'Worlds',2));b.update(rows+[rows[0]])
    assert np.allclose(a.m,b.m,atol=1e-12) and np.allclose(a.C,b.C,atol=1e-12)
    c.update(weighted_rows(rows,'MSI',4));d=DynamicBT(['a','b','c'],{'a':'KR','b':'CN','c':'KR'},{})
    d.advance(date(2025,10,12));d.update(rows)
    assert np.allclose(c.m,d.m,atol=1e-12) and rows==original
    assert weighted_rows(rows,'Worlds',1)==rows
    s=json.loads((OUT/'summary.json').read_text());pred=json.loads((OUT/'predictions.json').read_text())
    assert len(pred)==1300 and len({r['event_id'] for r in pred})==23
    assert len([r for r in pred if r['prior_event_series']])==1181
    for r in pred:
        if r['latest_event_training_date']:assert r['latest_event_training_date']<r['date']
        if not r['prior_event_series']:assert len(set(r['probabilities'].values()))==1
        assert all(0<p<1 for p in r['probabilities'].values())
        assert r['probabilities']['selected']==r['probabilities'][str(r['selected_weight'])]
    for audit in s['selection_audit']:
        earlier=[r for r in pred if r['season']<audit['season']]
        w,_=select(earlier);assert w==audit['weight']
        assert all(r['selected_weight']==w for r in pred if r['season']==audit['season'])
    assert select(pred)[0]==s['s16_weight']
    assert hashlib.sha256((R/'results/main_model.json').read_bytes()).hexdigest()==s['main_pointer_sha256']
    for k in ['selected']+list(map(str,WEIGHTS)):
        for metric,v in metrics([r for r in pred if r['prior_event_series']],k).items():assert abs(v-s['after_event_observation'][k][metric])<1e-12
    print('PASS weight-one identity, integer-power likelihood equivalence, event isolation, no raw mutation, 1300 targets / 23 events, pre-day cutoff, prior-year-only tuning, reproducible metrics, unchanged main pointer')

if __name__=='__main__':main()

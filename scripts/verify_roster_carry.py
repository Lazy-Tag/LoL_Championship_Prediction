"""Roster transport covariance, chronology, products and historical identities."""
import json,hashlib
from datetime import date,timedelta
import numpy as np
from candidate_models import DynamicBT,TEAM_SD
from roster_carry_model import RosterBT,initialize,overlap
from evaluate_roster_carry import R,OUT,metrics,select,CONFIGS

def main():
    assert abs(overlap(dict(a=.2,b=.2,c=.2,d=.2,e=.2),dict(a=.2,b=.2,c=.2,f=.2,g=.2))-.6)<1e-12
    assert overlap({'a':1},{'b':1})==0 and overlap({'a':1},{'a':1})==1
    old=RosterBT(['a','b'],{'a':'KR','b':'CN'},{},90);old.advance(date(2025,12,1));old.m[-2:]=[.8,-.5];old.C[-2:,-2:]=[[.2,-.02],[-.02,.3]]
    def roster(ds,shares):return dict(first_match=ds,last_match=ds,first=dict(date=ds,shares=shares),last=dict(date=ds,shares=shares))
    prev={'a':roster('2025-12-01',{'p':1}), 'b':roster('2025-12-01',{'q':1})}
    now={'a':roster('2026-01-01',{'p':1}), 'b':roster('2026-01-01',{'z':1})}
    start=date(2026,1,1);cut=date(2026,2,1);m,audit=initialize(old.teams,old.regions,{},90,old,prev,now,start,cut)
    rho=2**(-31/90);assert abs(m.m[-2]-.8*rho)<1e-12 and m.m[-1]==0
    assert abs(m.C[-2,-2]-(rho*rho*.2+(1-rho*rho)*TEAM_SD**2))<1e-12
    assert np.linalg.eigvalsh(m.C).min()>0
    m.advance(start);m.advance(start+timedelta(days=90));assert abs(m.m[-2]-.4*rho)<1e-12
    # First observed roster cannot affect forecasts on its own date.
    no,_=initialize(old.teams,old.regions,{},90,old,prev,now,start,start);assert np.all(no.m==0)
    # Missing metadata and unknown teams reset rather than imply continuity.
    no,_=initialize(old.teams,old.regions,{},90,old,{},now,start,cut);assert np.all(no.m==0)
    # Same 90-day model with inheritance disabled reproduces original dynamics.
    x=DynamicBT(old.teams,old.regions,{});y=RosterBT(old.teams,old.regions,{},90)
    for i in (0,1,17,91):
        day=start+timedelta(days=i);rr=[dict(team1='a',team2='b',wins1=2,wins2=1,date=day.isoformat())]
        x.advance(day);y.advance(day);x.update(rr);y.update(rr)
        assert np.allclose(x.m,y.m,atol=1e-12) and np.allclose(x.C,y.C,atol=1e-12)
    s=json.loads((OUT/'summary.json').read_text());rows=json.loads((OUT/'predictions.json').read_text());audits=json.loads((OUT/'roster_audit.json').read_text());chains=json.loads((OUT/'discount_chains.json').read_text())
    assert len(rows)==len({r['detail'] for r in rows})==1300 and len({r['event_id'] for r in rows})==23
    for a in audits:
        assert 0<=a['coefficient']<=1 and 0<=a['retention']<=1
        if a['coefficient']:
            assert a['current_lineup']['date']<a['cutoff'] and a['previous_lineup']['date']<a['start']
            assert a['previous_lineup_gap_days']<=45 and a['current_lineup_gap_days']<=30
    for a in chains:
        assert 0<a['transport_product_to_season_start']<=a['consecutive_roster_product']<=1+1e-12
        assert a['ancestor_season']<a['season']
    for name,m in s['aggregate'].items():
        for k,v in metrics(rows,name).items():assert abs(v-m[k])<1e-12
    for selection in s['selection']:
        earlier=[r for r in rows if r['season']<selection['season']]
        assert select(earlier,[c['name'] for c in CONFIGS])==selection['chosen']
    assert s['roster_supported']['carry90']['n']==711
    for name,digest in s['unchanged_hashes'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
    print('PASS roster overlap, missing/current-day exclusion, covariance transport/positive definiteness, 90-day identity, 23 events/1300 unique series, historical metadata cutoffs, compounded discounts, past-year-only selection, metric reproduction, unchanged main/live pointers')

if __name__=='__main__':main()

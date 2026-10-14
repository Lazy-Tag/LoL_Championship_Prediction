"""Season-isolated, pre-day replay of MSI/MSC and Worlds.

The only permitted cross-season performance input is previous-season
international REGIONAL strength. No previous-season team ratings are inherited.
"""
import json
import math
import re
import unicodedata
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from scipy.sparse.csgraph import connected_components
from model import series_probability

ROOT=Path(__file__).resolve().parents[1]
HALF_LIVES=[30,60,90,180]
TEAM_PRIOR_PRECISION=.25  # theta_i ~ Normal(regional mean, 2^2).
REGION_PRIOR_PRECISION=.5

def key(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())

def target_event(name):
    if re.search(r'Worlds Qualifying',name,re.I):return None
    if re.search(r'World Championship|Worlds (?:Main|Play|20)',name,re.I):return 'Worlds'
    if re.search(r'^MSI\b|^(?:\d{4} )?Mid-Season Invitational',name,re.I):return 'MSI'
    if name=='Mid-Season Cup 2020':return 'MSC'
    return None

def international(name):
    return bool(target_event(name) or re.search(r'^(?:Esports World Cup|EWC|(?:\d{4} )?First Stand)',name,re.I))

def domestic_region(name):
    # A multi-region event's first league name is not every team's affiliation.
    if re.search(r'Rift Rivals', name, re.I):return None
    rules=[(r'^(?:NA LCS|NA Regional|LCS|LTA North)\b','NA'),(r'^(?:EU LCS|EU Regional|LEC)\b','EU'),(r'^(?:LCK|OGN|Champions)\b','KR'),(r'^LPL\b','CN'),(r'^LMS\b','LMS'),(r'^PCS\b','PCS'),(r'^LCP\b','LCP'),(r'^VCS\b','VN'),(r'^(?:CBLOL|LTA South)\b','BR'),(r'^LJL\b','JP'),(r'^TCL\b','TR'),(r'^LCL\b','CIS'),(r'^LLA\b','LATAM'),(r'^LLN\b','LAN'),(r'^CLS\b','LAS'),(r'^(?:OPL|LCO)\b','OCE'),(r'^(?:GPL|LST)\b','SEA')]
    for pattern,region in rules:
        if re.search(pattern,name):return region
    return None

# Explicit missing domestic affiliation metadata for early source years.
# These are region labels, not results/ratings, and remain season-specific.
EARLY_REGIONS={
 3:{'Cloud 9':'NA','Team SoloMid':'NA','Team Vulcun':'NA','Fnatic':'EU','Gambit Gaming':'EU','Lemondogs':'EU','Alliance':'EU','SK Gaming':'EU','Team Dignitas':'NA','Counter Logic Gaming':'NA','Gamania Bears':'LMS','Mineski':'SEA','GamingGear':'CIS','Najin Black Sword':'KR','SK Telecom T1':'KR','Samsung Ozone':'KR','OMG':'CN','Royal Club':'CN'},
 4:{'Edward Gaming':'CN','OMG':'CN','Star Horn Royal Club':'CN','NaJin White Shield':'KR','Samsung Galaxy Blue':'KR','Samsung Galaxy White':'KR','SK Telecom T1 K':'KR','Taipei Assassins':'LMS','ahq e-Sports Club':'LMS','Dark Passage':'TR','KaBuM! eSports':'BR'},
 5:{'Bangkok Titans':'SEA','Besiktas Esports Club':'TR','paiN Gaming':'BR'},
 6:{'Albus NoX Luna':'CIS','INTZ e-Sports':'BR','SuperMassive':'TR'},
 7:{'Kaos Latin Gamers':'LAS','Young Generation':'SEA','1907 Fenerbahce':'TR','Rampage':'JP','Dire Wolves':'OCE','Lyon Gaming':'LAN','Isurus Gaming':'LAS','SuperMassive':'TR','GIGABYTE Marines':'SEA','Red Canids':'BR','Team oNe eSports':'BR','Virtus.pro':'CIS','Gambit Esports':'CIS'},
 8:{'Ascension Gaming':'SEA'},
}

def load_season(s):
    raw=json.loads((ROOT/f'data/history/S{s}/series.json').read_text());rows=[];seen=set();invalid=[]
    for r in raw:
        identity=(r['tournament'],r['detail'])
        if identity in seen:continue
        seen.add(identity)
        try:date.fromisoformat(r['date'])
        except ValueError:invalid.append(r);continue
        if r['wins1']+r['wins2']==0:invalid.append(r);continue
        rows.append({**r,'team1':key(r['team1']),'team2':key(r['team2']),'display1':r['team1'],'display2':r['team2']})
    return sorted(rows,key=lambda r:(r['date'],r['tournament'],r['detail'])),invalid

def affiliations(rows,season):
    counts=defaultdict(Counter)
    for r in rows:
        reg=domestic_region(r['tournament'])
        if reg:
            for k in ['team1','team2']:counts[r[k]][reg]+=1
    regs={t:c.most_common(1)[0][0] for t,c in counts.items()}
    regs.update({key(t):reg for t,reg in EARLY_REGIONS.get(season,{}).items()})
    # Metadata-only fallback: a stable team name may have no domestic records in
    # this source year. Previous affiliations are supplied separately in main.
    return regs

def optimize(rows,teams,reference,half_life,prior=None,precision=.25):
    ix={t:i for i,t in enumerate(teams)};n=len(teams)
    mu=np.array([prior.get(t,0.) for t in teams]) if prior else np.zeros(n)
    if not rows:return mu,0.
    a=np.array([ix[r['team1']] for r in rows]);b=np.array([ix[r['team2']] for r in rows])
    wa=np.array([r['wins1'] for r in rows],float);wb=np.array([r['wins2'] for r in rows],float)
    w=2.**(-np.array([(reference-date.fromisoformat(r['date'])).days for r in rows])/half_life)
    assert np.all(w<=1.+1e-12),'future training data'
    def obj(theta):
        delta=theta[a]-theta[b];p=expit(delta);err=w*((wa+wb)*p-wa)
        loss=np.sum(w*(wa*np.logaddexp(0,-delta)+wb*np.logaddexp(0,delta)))+.5*precision*np.sum((theta-mu)**2)
        grad=np.bincount(a,weights=err,minlength=n)-np.bincount(b,weights=err,minlength=n)+precision*(theta-mu)
        return float(loss),grad
    result=minimize(obj,mu,jac=True,method='L-BFGS-B',options={'maxiter':1000,'gtol':1e-8,'ftol':1e-14,'maxls':50})
    gradient=float(np.max(np.abs(obj(result.x)[1])))
    if gradient>1e-4:raise RuntimeError(f'Optimization residual {gradient}')
    return result.x,gradient

def prior_regions(previous,regions,half_life):
    rows=[];missing=Counter();counts=Counter()
    for r in previous:
        if not international(r['tournament']):continue
        a,b=regions.get(r['team1']),regions.get(r['team2'])
        if a is None or b is None:
            if a is None:missing[r['display1']]+=1
            if b is None:missing[r['display2']]+=1
            continue
        if a==b:continue
        rows.append({**r,'team1':a,'team2':b})
        counts[a]+=r['wins1']+r['wins2'];counts[b]+=r['wins1']+r['wins2']
    if not rows:return {},dict(series=0,missing_team_regions=dict(missing),counts={})
    teams=sorted(counts);ref=max(date.fromisoformat(r['date']) for r in rows)
    strength,g=optimize(rows,teams,ref,half_life,precision=REGION_PRIOR_PRECISION)
    result=dict(zip(teams,map(float,strength)))
    def pool(dest,sources):
        parts=[s for s in sources if s in result and counts[s]>0]
        if parts:result[dest]=sum(result[s]*counts[s] for s in parts)/sum(counts[s] for s in parts)
    # Structural transitions only; no current-season performance is consulted.
    if 'PCS' not in result:pool('PCS',['LMS','SEA'])
    if 'VN' not in result and 'SEA' in result:result['VN']=result['SEA']
    if 'LATAM' not in result:pool('LATAM',['LAN','LAS'])
    if 'LCP' not in result:pool('LCP',['PCS','VN','JP'])
    return result,dict(series=len(rows),maps=sum(r['wins1']+r['wins2'] for r in rows),last_date=ref.isoformat(),missing_team_regions=dict(missing),counts=dict(counts),strength=result,gradient_inf=g)

def strict_predictions(train,targets,reference):
    """Finite unregularized MLE only when both teams' undirected component
    is strongly connected in the directed map-win graph. Otherwise abstain."""
    if not train:return {},'no_training_data'
    teams=sorted({r[k] for r in train for k in ['team1','team2']});ix={t:i for i,t in enumerate(teams)};n=len(teams)
    graph=np.zeros((n,n))
    for r in train:
        a,b=ix[r['team1']],ix[r['team2']]
        if r['wins1']:graph[a,b]=1
        if r['wins2']:graph[b,a]=1
    _,weak=connected_components(graph,directed=False);_,strong=connected_components(graph,connection='strong')
    needed=set()
    for r in targets:
        a,b=ix.get(r['team1']),ix.get(r['team2'])
        if a is not None and b is not None and weak[a]==weak[b]:needed.add(weak[a])
    fitted={}
    for comp in needed:
        indices=np.flatnonzero(weak==comp)
        if len(set(strong[indices]))!=1:continue
        subset=[teams[i] for i in indices];ss=set(subset);rr=[r for r in train if r['team1'] in ss and r['team2'] in ss]
        theta,_=optimize(rr,subset,reference,90,precision=0.)
        fitted[comp]=dict(zip(subset,map(float,theta)))
    predictions={}
    for r in targets:
        a,b=ix.get(r['team1']),ix.get(r['team2'])
        if a is not None and b is not None and weak[a]==weak[b] and weak[a] in fitted:
            th=fitted[weak[a]];predictions[r['detail']]=float(expit(th[r['team1']]-th[r['team2']]))
    return predictions,None

def target_bo(row,season):
    # MSI/MSC/Worlds target formats only, not domestic BO2 inference.
    a,b=row['wins1'],row['wins2'];m=max(a,b)
    if a==b:return None
    if m==1:return 1
    if m==2:return 3
    if m==3:return 5
    return None

def metrics(rows,field):
    out=dict(total_target_series=len(rows),covered_series=0,maps=0,map_correct=0.,decisive_series=0,series_correct=0.,tied_probability_series=0,logloss_sum=0.,brier_sum=0.,series_logloss_sum=0.,series_brier_sum=0.,by_bo={})
    for r in rows:
        p=r.get(field)
        if p is None:continue
        a,b=r['wins1'],r['wins2'];n=a+b;bo=r['best_of'];out['covered_series']+=1;out['maps']+=n
        if abs(p-.5)<1e-12:correct=n*.5;sc=.5;out['tied_probability_series']+=1
        else:correct=a if p>.5 else b;sc=float((p>.5)==(a>b))
        out['map_correct']+=correct
        p=min(max(p,1e-15),1-1e-15)
        out['logloss_sum']-=a*math.log(p)+b*math.log1p(-p);out['brier_sum']+=a*(1-p)**2+b*p*p
        if a!=b and bo:
            q=min(max(float(series_probability(p,bo)),1e-15),1-1e-15);y=float(a>b)
            out['decisive_series']+=1;out['series_correct']+=sc;out['series_logloss_sum']-=y*math.log(q)+(1-y)*math.log1p(-q);out['series_brier_sum']+=(q-y)**2
            z=out['by_bo'].setdefault(str(bo),dict(series=0,correct=0.));z['series']+=1;z['correct']+=sc
    for label,num,den in [('map_accuracy','map_correct','maps'),('series_accuracy','series_correct','decisive_series'),('map_logloss','logloss_sum','maps'),('map_brier','brier_sum','maps'),('series_logloss','series_logloss_sum','decisive_series'),('series_brier','series_brier_sum','decisive_series')]:out[label]=out[num]/out[den] if out[den] else None
    out['coverage']=out['covered_series']/len(rows) if rows else None
    for z in out['by_bo'].values():z['accuracy']=z['correct']/z['series']
    return out

def main():
    seasons={};regions={};invalid={}
    for s in range(3,16):
        seasons[s],invalid[s]=load_season(s);regions[s]=affiliations(seasons[s],s)
    # Static affiliation fallback only (no previous-team strengths or outcomes).
    for s in range(4,16):
        for t,reg in regions[s-1].items():
            if t not in regions[s]:regions[s][t]=reg
    priors={};predictions=[];max_grad=0.;unmapped={}
    for s in range(4,16):
        current=seasons[s];targets=[r for r in current if target_event(r['tournament'])]
        priors[s]={}
        for h in HALF_LIVES:
            if s==3:pr,meta={},dict(series=0,note='S2 not available; neutral regional prior')
            else:pr,meta=prior_regions(seasons[s-1],regions[s-1],h)
            priors[s][h]=(pr,meta)
        unmapped[s]=sorted({r[k] for r in targets for k in ['team1','team2'] if r[k] not in regions[s]})
        for day in sorted({r['date'] for r in targets}):
            today=[r for r in targets if r['date']==day];train=[r for r in current if r['date']<day]
            assert all(r['date']<day for r in train)
            teams=sorted({r[k] for r in train+today for k in ['team1','team2']});ix={t:i for i,t in enumerate(teams)};ref=date.fromisoformat(day)
            neutral,g=optimize(train,teams,ref,90,precision=TEAM_PRIOR_PRECISION);max_grad=max(max_grad,g)
            strict,_=strict_predictions(train,today,ref)
            strengths={}
            for h in HALF_LIVES:
                regional,meta=priors[s][h]
                assert not meta.get('last_date') or meta['last_date']<day
                mu={t:regional.get(regions[s].get(t),0.) for t in teams}
                th,g=optimize(train,teams,ref,h,mu,TEAM_PRIOR_PRECISION);strengths[h]=th;max_grad=max(max_grad,g)
            for r in today:
                a,b=ix[r['team1']],ix[r['team2']]
                item={**r,'season':s,'event':target_event(r['tournament']),'best_of':target_bo(r,s),'best_of_provenance':'target-event winning threshold; checked for legal completed BO1/3/5 score','training_series':len(train),'latest_training_date':max((x['date'] for x in train),default=None),'region1':regions[s].get(r['team1']),'region2':regions[s].get(r['team2']),'neutral90':float(expit(neutral[a]-neutral[b])),'strict90':strict.get(r['detail'])}
                for h,th in strengths.items():item['regional'+str(h)]=float(expit(th[a]-th[b]))
                if item['best_of'] is None or min(r['wins1'],r['wins2'])>=item['best_of']//2+1:raise ValueError('Invalid target score: '+str(item))
                predictions.append(item)
        print('S'+str(s),'targets',len(targets),'maps',sum(r['wins1']+r['wins2'] for r in targets),'unmapped target clubs',unmapped[s],flush=True)
    fields=['regional90','neutral90','strict90','regional30','regional60','regional180']
    summary=[]
    for s in range(4,16):
        for event in ['MSI','MSC','Worlds']:
            rr=[r for r in predictions if r['season']==s and r['event']==event]
            if rr:summary.append(dict(season=s,event=event,models={f:metrics(rr,f) for f in fields}))
    aggregate={f:metrics(predictions,f) for f in fields}
    common=[r for r in predictions if r['strict90'] is not None]
    result=dict(protocol='Pre-day chronological replay; current-source-season training only; prior-year international regional prior only; no team rating carryover',main_model='regional90',half_life_days=90,team_prior_precision=TEAM_PRIOR_PRECISION,region_prior_precision=REGION_PRIOR_PRECISION,prior_international_scope='Previous source season MSI/MSC/Worlds including play-ins, EWC and First Stand; no domestic results',same_day_policy='All matches of one UTC source date share pre-day training data; no same-day updates',tie_policy='p=0.5 gets expected 0.5 accuracy credit, not arbitrarily choosing team1; disclose tied count',cold_start='Neutral team residual around previous regional prior; S3 excluded from replay due to insufficient pre-event data; unknown regions default 0',format_policy='Evaluation targets MSI/MSC/Worlds only; winning threshold determines BO1/3/5; domestic BO2 scores are retained as map evidence',max_optimization_gradient=max_grad,aggregate=aggregate,strict_common_subset={f:metrics(common,f) for f in ['regional90','neutral90','strict90']},by_season_event=summary,regional_prior_audit={s:{h:meta for h,(_,meta) in pp.items()} for s,pp in priors.items()},missing_target_regions=unmapped,invalid_training_rows={s:len(v) for s,v in invalid.items()},caveats=['S3/S4 domestic coverage is substantially incomplete in this source; these are source-snapshot replays, not full-history verified backtests','Reported aggregate is descriptive, not a held-out model-selection estimate; priors were specified without tuning to test outcomes','Model uncertainty and correlated maps make naive binomial standard errors inappropriate','Strict MLE coverage is selective; compare models on the same subset as well as full coverage','Teams use normalized source names within a season; no unverified organization-merger inference'])
    (ROOT/'results/backtest_predictions.json').write_text(json.dumps(predictions,ensure_ascii=False,indent=2))
    (ROOT/'results/backtest_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('AGGREGATE',json.dumps({f:{k:v for k,v in m.items() if k in ['maps','map_accuracy','series_accuracy','map_logloss','map_brier','coverage','tied_probability_series']} for f,m in aggregate.items()}),flush=True)

if __name__=='__main__':main()

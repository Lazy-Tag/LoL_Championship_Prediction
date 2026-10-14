"""Time-weighted, unregularized Bradley-Terry maximum likelihood.

All played maps contribute once. Series scores are sufficient statistics under
the explicitly assumed constant independent map win probability within a series.
"""
import json
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.sparse.csgraph import connected_components

ROOT = Path(__file__).resolve().parents[1]
WORLD_TEAMS = {
 'AL':("Anyone's Legend",'LPL',1), 'BLG':('BILIBILI GAMING','LPL',2),
 'TES':('TOP ESPORTS','LPL',3), 'IG':('Invictus Gaming','LPL',4),
 'GEN':('Gen.G Esports','LCK',1), 'HLE':('Hanwha Life Esports','LCK',2),
 'T1':('T1','LCK',3), 'DK':('Dplus KIA','LCK',4),
 'G2':('G2 Esports','LEC',1), 'MKOI':('Movistar KOI','LEC',2),
 'KC':('Karmine Corp','LEC',3), 'TLAW':('Team Liquid Alienware','LCS',1),
 'LYON':('LYON','LCS',2), 'C9':('Cloud9 Kia','LCS',3),
 'TSW':('Team Secret Whales','LCP',1), 'CFO':('CTBC Flying Oyster','LCP',2),
 'MVK':('MVK Esports','LCP',3), 'LOS':('LOS','CBLOL',1), 'FUR':('FURIA','CBLOL',2),
}

def series_probability(p, best_of):
    if best_of==1:return p
    if best_of==3:return p*p*(3-2*p)
    if best_of==5:return p*p*p*(10-15*p+6*p*p)
    raise ValueError(best_of)

def fit(rows, half_life):
    teams=sorted({r[k] for r in rows for k in ['team1','team2']});idx={t:i for i,t in enumerate(teams)}
    a=np.array([idx[r['team1']] for r in rows]);b=np.array([idx[r['team2']] for r in rows])
    wa=np.array([r['wins1'] for r in rows],float);wb=np.array([r['wins2'] for r in rows],float)
    age=np.array([(date(2026,10,19)-date.fromisoformat(r['date'])).days for r in rows])
    weights=2.**(-age/half_life);n=len(teams)
    graph=np.zeros((n,n));graph[a[wa>0],b[wa>0]]=1;graph[b[wb>0],a[wb>0]]=1
    components,_=connected_components(graph,connection='strong')
    if components!=1:raise ValueError('Finite unique MLE not established: directed win graph not strongly connected')
    def evaluate(theta, hessian=False):
        delta=theta[a]-theta[b];p=expit(delta)
        loss=np.sum(weights*(wa*np.logaddexp(0,-delta)+wb*np.logaddexp(0,delta)))
        err=weights*((wa+wb)*p-wa)
        grad=np.bincount(a,weights=err,minlength=n)-np.bincount(b,weights=err,minlength=n)
        if not hessian:return float(loss),grad
        curv=weights*(wa+wb)*p*(1-p);H=np.zeros((n,n))
        np.add.at(H,(a,a),curv);np.add.at(H,(b,b),curv);np.add.at(H,(a,b),-curv);np.add.at(H,(b,a),-curv)
        return float(loss),grad,H
    theta=np.zeros(n)
    for iteration in range(100):
        loss,g,H=evaluate(theta,True)
        if np.max(np.abs(g))<1e-10:break
        step=np.zeros(n);step[:-1]=np.linalg.solve(H[:-1,:-1],g[:-1])
        scale=1.
        while evaluate(theta-scale*step)[0]>loss-1e-4*scale*np.dot(g,step)+1e-12:
            scale*=.5
            if scale<1e-10:raise RuntimeError('Newton line search failed')
        theta-=scale*step
    else:raise RuntimeError('MLE convergence not reached')
    theta-=theta.mean();loss,g,H=evaluate(theta,True)
    assert np.max(np.abs(g))<1e-9
    P=expit(theta[:,None]-theta[None,:]);expected=np.zeros(n);observed=np.zeros(n);games=np.zeros(n)
    np.add.at(expected,a,weights*(wa+wb)*P[a,b]);np.add.at(expected,b,weights*(wa+wb)*P[b,a])
    np.add.at(observed,a,weights*wa);np.add.at(observed,b,weights*wb)
    np.add.at(games,a,wa+wb);np.add.at(games,b,wa+wb)
    diagnostics=dict(negative_weighted_log_likelihood=loss,gradient_inf=float(np.max(np.abs(g))),max_expected_observed_weighted_win_residual=float(np.max(np.abs(expected-observed))),iterations=iteration,win_graph_strong_components=int(components),smallest_identified_hessian_eigenvalue=float(np.linalg.eigvalsh(H[:-1,:-1])[0]),weighted_map_count=float(np.sum(weights*(wa+wb))),unweighted_maps=int(sum(wa+wb)),series_count=len(rows))
    pair_observed=np.zeros((n,n));pair_games=np.zeros((n,n))
    np.add.at(pair_observed,(a,b),weights*wa);np.add.at(pair_observed,(b,a),weights*wb)
    np.add.at(pair_games,(a,b),weights*(wa+wb));np.add.at(pair_games,(b,a),weights*(wa+wb))
    empirical=[[float(pair_observed[i,j]/pair_games[i,j]) if pair_games[i,j]>0 else None for j in range(n)] for i in range(n)]
    return dict(half_life_days=half_life,reference='2026-10-19',teams=teams,strength=theta.tolist(),games=games.astype(int).tolist(),weighted_observed_wins=observed.tolist(),weighted_expected_wins=expected.tolist(),bo1=P.tolist(),bo3=series_probability(P,3).tolist(),bo5=series_probability(P,5).tolist(),empirical_direct_weighted_map_winrate=empirical,diagnostics=diagnostics)

def main():
    rows=json.loads((ROOT/'data/series.json').read_text());models={}
    for h in [30,60,90,180]:
        m=fit(rows,h);models[str(h)]=m
        print(h,json.dumps(m['diagnostics']),flush=True)
    result=dict(model='Bradley-Terry; unregularized weighted maximum likelihood',main_half_life_days=90,world_teams=WORLD_TEAMS,models=models,assumptions=['Club identity fixed, roster changes ignored','Single latent strength per club shared across BO1/BO3/BO5','Independent maps with constant probability within each series','Time weighting at calendar-day resolution using series start date','No draft/side/patch/travel/fatigue effects','Historical match scores contribute map wins/losses only; series outcome is not counted twice'])
    (ROOT/'results/models.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    m=models['90'];ix={t:i for i,t in enumerate(m['teams'])}
    pairs=[]
    for code,(team,region,seed) in WORLD_TEAMS.items():
        for code2,(team2,_,_) in WORLD_TEAMS.items():
            if code==code2:continue
            a,b=ix[team],ix[team2]
            pairs.append(dict(team=code,opponent=code2,bo1=m['bo1'][a][b],bo3=m['bo3'][a][b],bo5=m['bo5'][a][b],empirical_direct_weighted_map_winrate=m['empirical_direct_weighted_map_winrate'][a][b],bo1_sensitivity={h:v['bo1'][a][b] for h,v in models.items()}))
    (ROOT/'results/worlds_pairwise.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

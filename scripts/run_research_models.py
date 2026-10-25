"""Independent nonlinear, joint-observation, and regime-change experiments."""
import gzip,json,hashlib,sys,concurrent.futures,subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path
import numpy as np
from scipy.special import expit
from candidate_models import DynamicBT
from research_model_core import JointGold,ChangePoint,fit_gold,marginal
from backtest import load_season,affiliations,prior_regions,domestic_region
from evaluate_detail_features import reconcile
from model import series_probability
from run_memory_weights import input_hashes
R=Path(__file__).resolve().parents[1];D=R/'results/research_models';CACHE=R/'.local/research_models';N=14_000_605
FEATURES=['strength_difference','contrast_sd','log_maps_a','log_maps_b','residual_a','residual_b','gold15_a','gold15_b','log_gold_maps_a','log_gold_maps_b','idle_a','idle_b']
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def gold(g):
 b,r=g['teams']['blue'],g['teams']['red'];a=b['stats'].get('goldat15');c=r['stats'].get('goldat15')
 if a is not None and c is not None:return (a-c)/1000
 vv=[[p['stats'].get('golddiffat15') for p in t['players']] for t in [b,r]]
 if all(len(v)==5 and all(x is not None for x in v) for v in vv) and abs(sum(vv[0])+sum(vv[1]))<1:return sum(vv[0])/1000
 return None

def prepare():
 D.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True);seasons={};regs={};prior_gold=[];configs={'joint_gold':[],'change_point':[]};features=[];event_features=[];pred=[];audits=[];params=[];coverage=[]
 cs=json.loads((R/'results/model_experiments/event_configs.json').read_text())['dynamic90'];targets=json.loads((R/'results/model_experiments/predictions.json').read_text());protect=['results/main_model.json','results/live_s16/latest.json','results/model_experiments/dynamic90/2026_Worlds.json'];hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protect}
 for s in range(3,16):
  rows,_=load_season(s);seasons[s]=rows;regs[s]=affiliations(rows,s)
  if s>3:
   for t,v in regs[s-1].items():regs[s].setdefault(t,v)
  if s==3:continue
  teams=sorted({r[k] for r in rows for k in ['team1','team2']});prior,_=prior_regions(seasons[s-1],regs[s-1],90);base=DynamicBT(teams,regs[s],prior);par=fit_gold(prior_gold);params.append(dict(season=s,parameters=par));joint=JointGold(teams,regs[s],prior,parameters=par);cp=ChangePoint(teams,regs[s],prior,s+2010)
  matched,audit=reconcile(s,rows);byday=defaultdict(list);td=defaultdict(list);ed=defaultdict(list)
  for r in rows:byday[r['date']].append(r)
  for r in targets:
   if r['season']==s:td[r['date']].append(r)
  for c in cs:
   if c['season']==s:ed[c['start_date']].append(c)
  stats={t:np.zeros(4) for t in teams};lastmatch={};lastday=None;last=None;gcount=0;season_gold=[]
  for ds in sorted(set(byday)|set(td)|set(ed)):
   day=date.fromisoformat(ds)
   for obj in [base,joint,cp]:obj.advance(day)
   if lastday:
    rho=2**(-(day-lastday).days/90)
    for v in stats.values():v*=rho
   lastday=day;bt=base.strengths();jt=joint.strengths();ct=cp.strengths()
   def feat(a,b):
    vec=np.zeros(len(base.m))
    for t,sign in [(a,1),(b,-1)]:vec[base.ri[regs[s].get(t,'UNKNOWN')]]+=sign;vec[base.nr+base.ti[t]]+=sign
    sa,sb=stats[a],stats[b]
    return [bt[a]-bt[b],float(np.sqrt(max(vec@base.C@vec,0))),float(np.log1p(sa[0])),float(np.log1p(sb[0])),float(sa[1]/max(sa[0],1)),float(sb[1]/max(sb[0],1)),float(sa[3]/sa[2]) if sa[2]>=5 else None,float(sb[3]/sb[2]) if sb[2]>=5 else None,float(np.log1p(sa[2])),float(np.log1p(sb[2])),min((day-lastmatch[a]).days,180) if a in lastmatch else 180,min((day-lastmatch[b]).days,180) if b in lastmatch else 180]
   for r in td[ds]:
    a,b=r['team1'],r['team2'];p=float(expit(bt[a]-bt[b]));assert abs(p-r['dynamic90'])<1e-9
    probs={'baseline':float(series_probability(p,r['best_of'])),'joint_gold':float(series_probability(joint.predict(a,b),r['best_of'])),'change_point':float(series_probability(float(expit(ct[a]-ct[b])),r['best_of']))}
    pred.append(dict(season=s,date=ds,event=r['event'],detail=r['detail'],team1=r['display1'],team2=r['display2'],wins1=r['wins1'],wins2=r['wins2'],best_of=r['best_of'],probabilities=probs,features=feat(a,b),reverse_features=feat(b,a)))
   for c in ed[ds]:
    assert last<ds and all(abs(bt[t]-c['strength'][t])<1e-9 for t in c['teams'])
    for mode,th in [('joint_gold',jt),('change_point',ct)]:
     p=[[float(marginal(th[a]-th[b],par)) if mode=='joint_gold' else float(expit(th[a]-th[b])) for b in c['teams']] for a in c['teams']]
     if mode=='joint_gold' and not par['n']:
      p=[[float(v) for v in line.split()] for line in (R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines()[2:2+len(c['teams'])]]
     configs[mode].append({**{k:v for k,v in c.items() if k!='gradient'},'model':mode,'strength':{t:th[t] for t in c['teams']},'pairwise_probabilities':p,'latest_training_date':last})
    event_features.append(dict(config=c,features=[[feat(a,b) for b in c['teams']] for a in c['teams']]))
   obs=[];gold_updates=[]
   for r in byday[ds]:
    a,b=r['team1'],r['team2'];n=r['wins1']+r['wins2'];p=float(expit(bt[a]-bt[b]));dom=domestic_region(r['tournament']) is not None
    if dom:features.append(dict(date=ds,season=s,detail=r['detail'],x=feat(a,b),reverse=feat(b,a),w=n,y=r['wins1']/n))
    if r['detail'] in matched:
     for g in matched[r['detail']]:
      ga=gold(g);ga=ga if ga is not None and abs(ga)<=30 else None;blue_is_a=g['a']==a;side=1 if blue_is_a else -1;win=g['teams']['blue' if blue_is_a else 'red']['win'];obs.append(dict(team1=a,team2=b,wins1=win,wins2=1-win,date=ds,gold=ga*side if ga is not None else np.nan,side=side))
      if ga is not None:
       gcount+=1
       if dom:season_gold.append(dict(date=ds,d=(bt[a]-bt[b])*side,g=ga,y=g['teams']['blue']['win']))
       for t,sgn in [(a,side),(b,-side)]:gold_updates.append((t,ga*sgn))
    else:obs.append(r)
   assert sum(r['wins1']+r['wins2'] for r in obs)==sum(r['wins1']+r['wins2'] for r in byday[ds])
   for t,value in gold_updates:stats[t][2]+=1;stats[t][3]+=value
   # Statistics are updated only after every forecast/training feature of this day is saved.
   for r in byday[ds]:
    a,b=r['team1'],r['team2'];n=r['wins1']+r['wins2'];res=r['wins1']-n*float(expit(bt[a]-bt[b]))
    for t,sgn in [(a,1),(b,-1)]:stats[t][0]+=n;stats[t][1]+=res*sgn;lastmatch[t]=day
   joint.update(obs);cp.resample_before_update();cp.update(byday[ds]);base.update(byday[ds])
   if byday[ds]:last=ds
  prior_gold.extend(season_gold);audits.extend(dict(season=s,**a) for a in cp.audit);coverage.append(dict(season=s,training_maps=sum(r['wins1']+r['wins2'] for r in rows),gold_maps=gcount,domestic_gold_maps=len(season_gold),joint_gradient=joint.max_gradient))
  save(CACHE/'progress.json',dict(prepared_season=s));print('prepared',s,'gold',gcount,'parameters',par,flush=True)
 save(D/'event_configs.json',configs);save(D/'predictions.json',pred);save(D/'change_audit.json',audits);save(D/'joint_parameters.json',params)
 with gzip.open(CACHE/'features.json.gz','wt') as f:json.dump(dict(domestic=features,events=event_features),f,allow_nan=False)
 save(D/'protocol.json',dict(unchanged_hashes=hashes,input_hashes=input_hashes(),implementation_hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['scripts/research_model_core.py','scripts/run_research_models.py']},coverage=coverage,feature_names=FEATURES,catboost_parameters=dict(iterations=300,depth=4,learning_rate=.03,l2_leaf_reg=10),cp_particles=16,cp_hazard_half=180,parameters_selected_on_targets=False))
 return configs

def catboost():
 import catboost as cb
 with gzip.open(CACHE/'features.json.gz','rt') as f:data=json.load(f)
 configs=json.loads((D/'event_configs.json').read_text());pred=json.loads((D/'predictions.json').read_text());configs['catboost']=[];fits=[]
 for e in data['events']:
  c=e['config'];train=[r for r in data['domestic'] if r['date']<c['start_date']];assert train
  X=np.array([v for r in train for v in [r['x'],r['reverse']]],float);y=np.array([v for r in train for v in [r['y'],1-r['y']]]);weight=np.array([r['w']/2 for r in train for _ in range(2)])
  model=cb.CatBoostClassifier(iterations=300,depth=4,learning_rate=.03,l2_leaf_reg=10,loss_function='CrossEntropy',random_seed=c['year'],thread_count=2,verbose=False,allow_writing_files=False,has_time=True,bootstrap_type='No',random_strength=0)
  model.fit(X,y,sample_weight=weight);model.save_model(str(CACHE/(c['id']+'.cbm')))
  def predict(pairs,reverse):return (model.predict_proba(np.array(pairs,float))[:,1]+1-model.predict_proba(np.array(reverse,float))[:,1])/2
  n=len(c['teams']);pairs=[e['features'][i][j] for i in range(n) for j in range(n)];rev=[e['features'][j][i] for i in range(n) for j in range(n)];p=predict(pairs,rev).reshape(n,n);np.fill_diagonal(p,.5)
  configs['catboost'].append({**c,'model':'catboost','pairwise_probabilities':p.tolist(),'latest_tree_training_date':max(r['date'] for r in train)})
  rr=[r for r in pred if r['season']==c['season'] and r['event']==c['event']];pp=predict([r['features'] for r in rr],[r['reverse_features'] for r in rr])
  for r,q in zip(rr,pp):r['probabilities']['catboost']=float(series_probability(q,r['best_of']))
  fits.append(dict(id=c['id'],cutoff=c['start_date'],latest_training_date=max(r['date'] for r in train),training_series=len(train),training_maps=sum(r['w'] for r in train),feature_importances=dict(zip(FEATURES,map(float,model.feature_importances_)))))
  print('tree',c['id'],len(train),flush=True)
 save(D/'event_configs.json',configs);save(D/'predictions.json',pred);save(D/'tree_fits.json',fits);pr=json.loads((D/'protocol.json').read_text());pr['catboost_version']=cb.__version__;save(D/'protocol.json',pr)

def simulate():
 configs=json.loads((D/'event_configs.json').read_text());jobs=[];engine=hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
 for mode,cs in configs.items():
  for c in cs:
   folder=D/mode;folder.mkdir(exist_ok=True);lines=(R/f'results/model_experiments/dynamic90/{c["id"]}.txt').read_text().splitlines();n=len(c['teams']);p=np.array(c['pairwise_probabilities']);assert np.max(abs(p+p.T-1))<1e-10
   lines[2:2+n]=[' '.join(map(str,row)) for row in p];inp=folder/f'{c["id"]}.txt';inp.write_text('\n'.join(lines)+'\n');jobs.append((mode,c,inp))
 def run(job):
  mode,c,inp=job;out=inp.with_suffix('.json');digest=hashlib.sha256(inp.read_bytes()).hexdigest()
  if out.exists():
   old=json.loads(out.read_text())
   if old.get('input_sha256')==digest and old.get('engine_sha256')==engine and old['samples']==N:return mode+' '+c['id']+' reused'
  tmp=out.with_suffix('.tmp')
  with inp.open('rb') as fin,tmp.open('wb') as fout,(CACHE/(mode+'_'+c['id']+'.log')).open('wb') as err:subprocess.run([str(R/'.local/build/event_simulation'),str(N)],stdin=fin,stdout=fout,stderr=err,check=True)
  raw=json.loads(tmp.read_text());assert raw['samples']==N and raw['seed']==c['year'];raw.update(model=mode,input_sha256=digest,engine_sha256=engine);save(tmp,raw);tmp.replace(out);return mode+' '+c['id']+' '+str(raw['seconds'])+'s'
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for f in concurrent.futures.as_completed([pool.submit(run,j) for j in jobs]):print(f.result(),flush=True)
if __name__=='__main__':
 if '--resume' not in sys.argv:prepare()
 if '--prepare-only' not in sys.argv:
  if '--simulate-only' not in sys.argv:catboost()
  simulate()

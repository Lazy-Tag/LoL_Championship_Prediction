"""Chronological small-MLP experiments; standalone results and tournament simulations."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import gzip,json,hashlib,sys,time
import numpy as np
from pathlib import Path
from dnn_model import fit_model,predict
from model import series_probability
from run_research_models import R,save,N
D=R/'results/dnn';CACHE=R/'.local/dnn';MODES=['mlp','residual_mlp']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def train():
 with gzip.open(R/'.local/research_models/features.json.gz','rt') as f:data=json.load(f)
 source=json.loads((R/'results/research_models/predictions.json').read_text());cs={m:[] for m in MODES};pred=[{k:v for k,v in r.items() if k not in ['probabilities']}|{'probabilities':{'baseline':r['probabilities']['baseline']},'seed_probabilities':{}} for r in source];fits=[]
 inputs={str(p.relative_to(R)):digest(p) for p in [R/'.local/research_models/features.json.gz',R/'results/research_models/predictions.json',R/'scripts/dnn_model.py',R/'scripts/run_dnn.py',R/'reports/dnn/PROTOCOL.md']};signature=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest();protect=['results/main_model.json','results/live_s16/latest.json','results/model_experiments/dynamic90/2026_Worlds.json'];save(D/'protocol.json',dict(input_hashes=inputs,unchanged_hashes={p:digest(R/p) for p in protect},numpy_version=np.__version__,samples=N,seed_offsets=[0,10000,20000],training_signature=signature))
 for e in data['events']:
  c=e['config'];rows=[r for r in data['domestic'] if r['date']<c['start_date']];rr=[r for r in pred if r['season']==c['season'] and r['event']==c['event']];n=len(c['teams']);x=[e['features'][i][j] for i in range(n) for j in range(n)];rev=[e['features'][j][i] for i in range(n) for j in range(n)]
  for mode in MODES:
   matrices=[];probs=[]
   for offset in [0,10000,20000]:
    seed=c['year']+offset;cache=CACHE/f'{mode}_{c["id"]}_{seed}.json';t=time.monotonic()
    if cache.exists() and json.loads(cache.read_text()).get('signature')==signature:out=json.loads(cache.read_text())
    else:
     net,scaler,info=fit_model(rows,seed,mode=='residual_mlp');p=predict(net,scaler,x,rev).reshape(n,n);np.fill_diagonal(p,.5);q=predict(net,scaler,[r['features'] for r in rr],[r['reverse_features'] for r in rr]);out=dict(signature=signature,matrix=p.tolist(),probabilities=q.tolist(),fit=info);save(cache,out);np.savez(CACHE/f'{mode}_{c["id"]}_{seed}.npz',**{f'p{i}':v for i,v in enumerate(net.p)})
    matrices.append(out['matrix']);probs.append(out['probabilities']);fits.append(dict(id=c['id'],mode=mode,cutoff=c['start_date'],**out['fit']));print(mode,c['id'],seed,'epochs',out['fit']['selected_epochs'],'seconds',round(time.monotonic()-t,2),flush=True)
   p=np.mean(matrices,axis=0);q=np.mean(probs,axis=0);cs[mode].append({**c,'model':mode,'pairwise_probabilities':p.tolist(),'latest_training_date':max(r['date'] for r in rows)})
   for j,(r,v) in enumerate(zip(rr,q)):
    r['probabilities'][mode]=float(series_probability(v,r['best_of']));r['seed_probabilities'][mode]=[float(series_probability(a[j],r['best_of'])) for a in probs]
  save(D/'event_configs.json',cs);save(D/'predictions.json',pred);save(D/'fits.json',fits)
def simulate():
 import run_research_models as engine
 engine.D=D;engine.CACHE=CACHE;engine.simulate()
if __name__=='__main__':
 D.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True)
 if '--simulate-only' not in sys.argv:train()
 if '--train-only' not in sys.argv:simulate()

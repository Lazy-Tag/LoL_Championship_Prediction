"""Compare fixed candidates on identical pre-day S4-S15 targets; save event states.
Run with OPENBLAS_NUM_THREADS=1 to avoid tiny-matrix threading overhead.
"""
import json,hashlib
from collections import defaultdict
from datetime import date
from pathlib import Path
from scipy.special import expit
from backtest import load_season,affiliations,prior_regions,metrics
from candidate_models import static_fit,DynamicBT
R=Path(__file__).resolve().parents[1];OUT=R/'results/model_experiments';FIELDS=['regional90','hierarchical90','dynamic90']
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 seasons={};regions={}
 for s in range(3,16):
  seasons[s],_=load_season(s);regions[s]=affiliations(seasons[s],s)
  if s>3:
   for t,reg in regions[s-1].items():regions[s].setdefault(t,reg)
 # Extra outcome records are a separate, conservative supplement. In current
 # audit no extra eligible maps were admitted, so all models share baseline data.
 additions=json.loads((R/'data/enrichment/S15_additional.json').read_text())
 assert not additions,'Introduce a data-only baseline arm before admitting new training outcomes'
 base=json.loads((R/'results/backtest_predictions.json').read_text());configs=json.loads((R/'data/event_replay/configs.json').read_text());pred=[];states={f:[] for f in FIELDS[1:]};diagnostics=[]
 for s in range(4,16):
  current=seasons[s];targets=[r for r in base if r['season']==s];pr,pa=prior_regions(seasons[s-1],regions[s-1],90)
  teams=sorted({r[k] for r in current for k in ['team1','team2']});dyn=DynamicBT(teams,regions[s],pr)
  byday=defaultdict(list);td=defaultdict(list);ed=defaultdict(list)
  for r in current:byday[r['date']].append(r)
  for r in targets:td[r['date']].append(r)
  for c in configs:
   if c['season']==s:ed[c['start_date']].append(c)
  train=[];maxg=0.
  for day in sorted(set(byday)|set(td)|set(ed)):
   ref=date.fromisoformat(day);dyn.advance(ref)
   if day in td or day in ed:
    th,meta=static_fit(train,teams,regions[s],pr,ref);dh=dyn.strengths();maxg=max(maxg,meta['gradient_inf'])
    for r in td[day]:pred.append({**r,'hierarchical90':float(expit(th[r['team1']]-th[r['team2']])),'dynamic90':float(expit(dh[r['team1']]-dh[r['team2']]))})
    for c in ed[day]:
     for f,strength in [('hierarchical90',th),('dynamic90',dh)]:
      states[f].append({**c,'model':f,'strength':{t:strength[t] for t in c['teams']},'latest_training_date':max((r['date'] for r in train),default=None),'training_series':len(train),'prior_audit':pa})
   dyn.update(byday[day]);train.extend(byday[day])
  diagnostics.append(dict(season=s,static_gradient=maxg,dynamic_gradient=dyn.max_gradient));print('S'+str(s),len(targets),'done',flush=True)
 summary=dict(half_life_days=90,protocol='Pre-day forecasts, frozen event-start strengths; no current-season future outcomes; seasonal reset; prior-year international regional prior only',training_changes='No supplementary results admitted; map metadata are not model covariates',aggregate={f:metrics(pred,f) for f in FIELDS},by_season=[dict(season=s,models={f:metrics([r for r in pred if r['season']==s],f) for f in FIELDS}) for s in range(4,16)],cross_region={f:metrics([r for r in pred if r['region1']!=r['region2']],f) for f in FIELDS},diagnostics=diagnostics,input_sha256=hashlib.sha256((R/'results/backtest_predictions.json').read_bytes()).hexdigest())
 for n,v in [('predictions',pred),('summary',summary),('event_configs',states)]:
  (OUT/f'{n}.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({f:{k:summary['aggregate'][f][k] for k in ['series_accuracy','map_logloss','series_logloss','map_brier']} for f in FIELDS}),flush=True)
if __name__=='__main__':main()

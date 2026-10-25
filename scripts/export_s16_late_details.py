"""Export verified metadata as a separate compatible sidecar; do not add wins."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'results/s16_jul_oct'
MAPPING={'totalgold':'Golds','golddiffat15':'GD@15','kills':'Kills','deaths':'Deaths','assists':'Assists','cs':'CS','damage':'Total damage to Champion','visionscore':'Vision Score'}
ROLES={'TOP':'top','JUNGLE':'jng','MID':'mid','ADC':'bot','SUPPORT':'sup'}
def number(v):
    if v is None or v=='':return None
    try:return float(v.replace(',','')) if isinstance(v,str) else float(v)
    except ValueError:return None

def main():
    records=json.loads((D/'series.json').read_text());out=[]
    for r in records:
        if r['status']!='verified':continue
        for g in r['games']:
            teams={}
            for side,t in g['teams'].items():
                stats={k:None for k in ['totalgold','goldat10','goldat15','golddiffat10','golddiffat15','xpat10','xpat15','csat10','csat15','kills','deaths','assists','dragons','barons','towers']}
                stats.update(totalgold=t['total_gold'],golddiffat15=t['gold_difference_15'],kills=t['kills'])
                teams[side]=dict(name=t['name'],win=t['win'],stats=stats,players=[dict(name=p['name'],role=ROLES[p['role']],champion=p['champion_asset'],stats={k:number(p['stats'].get(v)) for k,v in MAPPING.items()}) for p in t['players']])
            out.append(dict(source='verified_gol_and_explicit_official_metadata_recovery',game_id='gol:'+g['game_id'],official_series_id=g['official_series_id'],year=2026,league=g['event'],date=g['official_start_utc'] or g['official_date']+'T00:00:00',date_precision='scheduled series start, not map start',source_date=g['source_date'],patch=g['patch'],game=g['game'],gamelength_source=g['duration'],url=g['sources'][0],sources=g['sources'],top_tier_candidate=True,teams=teams,reconciliation='official series identifier, full map count and cumulative winners verified',numeric_stats_status=g.get('numeric_stats_status','source fields retained, missing stays null')))
    path=R/'data/detailed/S16_late_verified_games.jsonl';path.write_text(''.join(json.dumps(g,ensure_ascii=False)+'\n' for g in out))
    manifest=dict(path=str(path.relative_to(R)),maps=len(out),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),base_oe_untouched=True,training_outcomes_added=0,join_key='official_series_id plus game index; do not concatenate these outcomes with existing series wins')
    (D/'normalized_export.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Exported',len(out),'verified supplementary maps')
if __name__=='__main__':main()

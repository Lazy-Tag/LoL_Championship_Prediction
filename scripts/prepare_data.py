"""Normalize club aliases and reconcile independent series score sources."""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAGUES = {'LPL','LCK','LEC','LCS','LCP','CBLOL','First Stand','MSI','Esports World Cup','Americas Cup','DCGI'}
ALIASES = {
    'AG.AL': "Anyone's Legend", 'Anyone s Legend': "Anyone's Legend",
    'MIBR.LOS':'LOS', 'Los Grandes':'LOS', 'LØS':'LOS',
    'Team Secret':'Team Secret Whales', 'Secret Whales':'Team Secret Whales',
    'Gen.G':'Gen.G Esports', 'Cloud9':'Cloud9 Kia',
    'Deep Cross Gaming':'Relove Deep Cross Gaming', 'JD Gaming':'Beijing JDG Esports',
    'LNG Esports':'Suzhou LNG Esports', 'Ninjas in Pyjamas':'Shenzhen NINJAS IN PYJAMAS',
    'RED Canids':'RED Kalunga', 'Team Liquid':'Team Liquid Alienware',
    'Team WE':"Xi'an Team WE", 'Weibo Gaming':'WeiboGaming',
}

def key(s):
    return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.replace('Ø','O')).encode('ascii','ignore').decode().lower())

def main():
    events = json.loads((ROOT/'data/raw/riot_events.json').read_text())
    known = {key(t['name']):t['name'] for e in events if e['league']['name'] in LEAGUES for t in e['match']['teams']}
    aliases = {key(a):b for a,b in ALIASES.items()}
    def norm(s):
        s = aliases.get(key(s),s)
        return known.get(key(s),s)
    series=[]
    for e in events:
        if e['league']['name'] not in LEAGUES or e['state']!='completed' or not '2026-01-01'<=e['startTime']<'2026-10-14T16:00:00Z':
            continue
        m=e['match'];a,b=m['teams'];wa,wb=a['result']['gameWins'],b['result']['gameWins'];bo=m['strategy']['count']
        assert max(wa,wb)==bo//2+1 and min(wa,wb)<bo//2+1
        assert a['name']!='TBD' and b['name']!='TBD'
        series.append(dict(id=m['id'],date=e['startTime'][:10],start_utc=e['startTime'],event=e['league']['name'],stage=e['blockName'],team1=norm(a['name']),team2=norm(b['name']),wins1=wa,wins2=wb,best_of=bo,source='https://lolesports.com/en-US/schedule?leagues='+e['league']['slug'],raw_source='riot_events.json'))
    gol = json.loads((ROOT/'data/raw/gol_series.json').read_text())
    available = set(range(len(series)))
    checks=[];unmatched=[];resolved=[]
    for t in gol:
        checks.append({k:v for k,v in t.items() if k!='series'})
        assert int(t['nbgames'])==t['parsed_maps'],t['trname']
        qualifier=t['trname'].startswith('EWC ')
        for r in t['series']:
            a,b=norm(r['team1']),norm(r['team2']);wa,wb=r['wins1'],r['wins2']
            if qualifier:
                assert max(wa,wb) in [1,2,3]
                series.append(dict(id='gol:'+r['detail'],date=r['date'],start_utc=None,event='EWC Qualifiers',stage=t['trname'],team1=a,team2=b,wins1=wa,wins2=wb,best_of=2*max(wa,wb)-1,source=r['source'],raw_source='gol_series.json',best_of_provenance='inferred from completed winning score'))
                continue
            candidates=[]
            for i in available:
                x=series[i]
                if not ((a,b,wa,wb)==(x['team1'],x['team2'],x['wins1'],x['wins2']) or (a,b,wa,wb)==(x['team2'],x['team1'],x['wins2'],x['wins1'])):continue
                delta=abs((datetime.fromisoformat(r['date'])-datetime.fromisoformat(x['date'])).days)
                if delta<=1:candidates.append((delta,i))
            if candidates:
                delta,i=min(candidates);available.remove(i);series[i]['crosscheck_source']=r['source'];series[i]['tournament']=t['trname'];series[i]['crosscheck_day_offset']=delta
            elif r['tournament']=='LCK 2026 Rounds 3-4' and r['date']=='2026-08-01' and (a,b,wa,wb)==('Gen.G Esports','Dplus KIA',1,1):
                i=next(i for i in available if series[i]['id']=='115548147900553473')
                assert (series[i]['wins1'],series[i]['wins2'])==(0,2)
                available.remove(i)
                series[i]['tournament']=r['tournament']
                series[i]['crosscheck_source']=r['source']
                series[i]['crosscheck_resolution']='GOL lists invalid completed BO3 score 1-1; retain official Riot 0-2, independently corroborated.'
                resolved.append(dict(official_id=series[i]['id'],gol=r,resolution=series[i]['crosscheck_resolution'],corroboration='https://www.reddit.com/r/leagueoflegends/comments/1vcm8sk/geng_vs_dplus_kia_lck_2026_season_rounds_34/'))
            else:unmatched.append(r)
    series.sort(key=lambda x:(x['date'],x['id']))
    counts=defaultdict(lambda:dict(series=0,maps=0,first='9999',last='',best_of=Counter()))
    for r in series:
        c=counts[r['event']];c['series']+=1;c['maps']+=r['wins1']+r['wins2'];c['first']=min(c['first'],r['date']);c['last']=max(c['last'],r['date']);c['best_of'][r['best_of']]+=1
    audit=dict(cutoff='2026-10-14T16:00:00Z (end of Oct 14 Asia/Shanghai); completed events only',weight_reference='2026-10-19',date_resolution='UTC scheduled series start day; EWC qualifiers use source match date',counts=counts,tournaments=checks,unmatched_gol=unmatched,unmatched_official=[r for r in series if r['raw_source']=='riot_events.json' and 'crosscheck_source' not in r],aliases=ALIASES,excluded=['2025 matches','tier-2 domestic leagues','national-team events (Asian Games, CACG)','KeSPA Cup (domestic non-league cup)','promotion tournaments (tier-1/tier-2 mixed qualifiers)','unplayed future matches'])
    (ROOT/'data/series.json').write_text(json.dumps(series,ensure_ascii=False,indent=2))
    audit['resolved_conflicts']=resolved
    (ROOT/'results/data_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print(json.dumps(counts,ensure_ascii=False,indent=2));print('unmatched GOL',len(unmatched),'unmatched official',len(audit['unmatched_official']))
    print('teams',len({r[k] for r in series for k in ['team1','team2']}),'series',len(series),'maps',sum(r['wins1']+r['wins2'] for r in series))

if __name__=='__main__':main()

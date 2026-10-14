"""Aggregate frozen entrant strengths, without refitting or future outcomes."""
from collections import defaultdict
import math

NAMES={'KR':'韩国','CN':'中国','EU':'欧洲','AMERICAS':'美洲','WILDCARD':'外卡','LCP':'太平洋（LCP）'}
GROUPS={}
for group,labels in {
    'KR':['KR','LCK'],
    'CN':['CN','LPL'],
    'EU':['EU','LEC','EU LCS'],
    'AMERICAS':['NA','LCS','NA LCS','BR','CBLOL','LAN','LAS','LATAM','LLA','LLN','CLS','LTA'],
    'LCP':['LCP'],
    'WILDCARD':['LMS','SEA','GPL','LST','PCS','JP','LJL','VN','VCS','OCE','OPL','LCO','TR','TCL','CIS','LCL'],
}.items():
    for label in labels:GROUPS[label]=group

def report_group(region):
    if region not in GROUPS:raise ValueError(f'Unmapped historical region: {region}')
    return GROUPS[region]

def region_rankings(teams):
    """teams: region, name, strength and title_probability, one row per entrant.

    Mean latent strength, equally weighted within each region; competition ranks.
    Title probability sums mutually exclusive team championship events.
    """
    grouped=defaultdict(list)
    for t in teams:
        assert t['region'] and t['region']!='UNKNOWN'
        grouped[report_group(t['region'])].append(t)
    rows=[]
    for reg,ts in grouped.items():
        rows.append(dict(region=reg,label=NAMES[reg],source_regions=sorted({t['region'] for t in ts}),mean_strength=math.fsum(t['strength'] for t in ts)/len(ts),teams=[t['name'] for t in sorted(ts,key=lambda t:(-t['strength'],t['name']))],team_count=len(ts),title_probability=math.fsum(t['title_probability'] for t in ts)))
    rows.sort(key=lambda r:(-round(r['mean_strength'],12),r['region']))
    values=[round(r['mean_strength'],12) for r in rows]
    for r,v in zip(rows,values):
        r['rank']=1+sum(x>v for x in values)
        r['tied']=values.count(v)>1
        r['undifferentiated']=len(set(values))==1
    assert math.isclose(sum(r['title_probability'] for r in rows),1,abs_tol=1e-10)
    return rows

def order_text(rows):
    if all(r['undifferentiated'] for r in rows):return '无法区分（'+ '、'.join(r['label'] for r in rows)+'）'
    bands=defaultdict(list)
    for r in rows:bands[r['rank']].append(r['label'])
    return ' ＞ '.join(' ＝ '.join(bands[k]) for k in sorted(bands))

def markdown_table(rows):
    s='\n| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |\n| --- | --- | --- | --- | --- |\n'
    for r in rows:
        rank='无法区分' if r['undifferentiated'] else ('并列 ' if r['tied'] else '')+str(r['rank'])
        s+=f"| {rank} | {r['label']} | {r['team_count']} | {'、'.join(r['teams'])} | {100*r['title_probability']:.4f}% |\n"
    return s+'\n'

def section(rows):
    return '## 赛前赛区实力排名\n\n按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。\n'+markdown_table(rows)

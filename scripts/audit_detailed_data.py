"""Inventory acquired per-map data without altering training or predictions.
Outputs preserve source fields and distinguish source coverage from verified
coverage. ZIP/XLSX parsed as data archives with standard-library readers.
"""
import ast,csv,gzip,hashlib,io,json,re,zipfile
import xml.etree.ElementTree as ET
from collections import Counter,defaultdict
from datetime import datetime,timedelta
from pathlib import Path
R=Path(__file__).resolve().parents[1];OUT=R/'data/detailed';REPORT=R/'reports/detailed_data'
NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main';tag=lambda s:'{'+NS+'}'+s
ALIASES={'teamname':['teamname','team'],'playername':['playername','player'],'patch':['patch','patchno'],'kills':['kills','k'],'deaths':['deaths','d'],'assists':['assists','a'],'golddiffat10':['golddiffat10','gdat10'],'golddiffat15':['golddiffat15','gdat15'],'dragons':['dragons','teamdragkills'],'barons':['barons','teambaronkills'],'towers':['towers','teamtowerkills']}
STAT=['totalgold','goldat10','goldat15','golddiffat10','golddiffat15','xpat10','xpat15','csat10','csat15','kills','deaths','assists','dragons','barons','towers']
MAJOR={'LCK','LPL','LEC','LCS','NALCS','EULCS','NA LCS','EU LCS','LMS','PCS','VCS','LJL','TCL','LCL','CBLOL','CBLoL','OPL','LCO','LLA','CLS','LLN','GPL','LST','LCP','LTA','LTA N','LTA S','MSI','WCS','WORLDS','WLDS','MSC','EWC','FST','IEM'}
def get(r,k):
 for a in ALIASES.get(k,[k]):
  v=r.get(a)
  if v is not None and str(v).strip() not in ('','NaN','nan','None','NA'):return str(v).strip()
 return None
def num(v):
 if v is None:return None
 try:return float(v)
 except (ValueError,TypeError):return None
def datevalue(v):
 if not v:return None
 try:
  if re.fullmatch(r'\d+(\.\d+)?',v):return (datetime(1899,12,30)+timedelta(days=float(v))).isoformat(sep=' ')
  if v[:4].isdigit() and v[4]=='-':return datetime.fromisoformat(v.replace('Z','+00:00')).isoformat(sep=' ')
  for fmt in ['%m/%d/%Y %H:%M','%m/%d/%Y','%Y/%m/%d %H:%M:%S']:
   try:return datetime.strptime(v,fmt).isoformat(sep=' ')
   except ValueError:pass
 except (ValueError,OverflowError):pass
 return None

def xlsxrows(data):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   for event,el in ET.iterparse(z.open('xl/sharedStrings.xml'),events=['end']):
    if el.tag==tag('si'):strings.append(''.join(t.text or '' for t in el.iter(tag('t'))));el.clear()
  for sheet in sorted(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$',n)):
   header=None
   for event,el in ET.iterparse(z.open(sheet),events=['end']):
    if el.tag!=tag('row'):continue
    values={}
    for c in el.findall(tag('c')):
     col=re.match('[A-Z]+',c.get('r','A'))[0];idx=0
     for ch in col:idx=idx*26+ord(ch)-64
     v=c.findtext(tag('v'));typ=c.get('t')
     if typ=='s':v=strings[int(v)] if v is not None else ''
     elif typ=='inlineStr':v=''.join(t.text or '' for t in c.iter(tag('t')))
     values[idx-1]=v or ''
    if header is None:
     header={i:v.strip().lower() for i,v in values.items()};assert 'gameid' in header.values(),header
    else:yield {header[i]:v for i,v in values.items() if i in header}
    el.clear()

def eligible(league,year):
 u=league.upper()
 if u not in {x.upper() for x in MAJOR}:return False
 if year>=2023 and u=='TCL':return False
 if year>=2025 and u in ['PCS','VCS','LJL','LCO']:return False
 return True

def normalize(rows,source,year):
 groups=defaultdict(list);rowcount=0
 for r in rows:
  rowcount+=1;gid=get(r,'gameid');url=get(r,'url')
  if not gid:continue
  # Old numeric game IDs are only unique within platform; URL disambiguates.
  identity=re.search(r'match-details/([^?&#]+)',url or '')
  gid=identity[1] if identity else gid
  groups[gid].append(r)
 out=[];errors=[]
 for gid,rr in groups.items():
  tt=[r for r in rr if (get(r,'position') or '').lower()=='team'];sides={str(get(r,'side')).lower():r for r in tt}
  if len(tt)!=2 or set(sides)!={'blue','red'}:
   errors.append(dict(id=gid,reason='missing/duplicate team rows',rows=len(rr)));continue
  a,b=sides['blue'],sides['red'];res=[num(get(r,'result')) for r in [a,b]]
  if any(x not in [0,1] for x in res) or sum(res)!=1:
   errors.append(dict(id=gid,reason='invalid result'));continue
  when=datevalue(get(a,'date'));league=get(a,'league') or 'UNKNOWN'
  teams={side:dict(name=get(r,'teamname'),win=int(res[i]),stats={k:num(get(r,k)) for k in STAT},players=[dict(name=get(p,'playername'),role=get(p,'position'),champion=get(p,'champion'),stats={k:num(get(p,k)) for k in STAT}) for p in rr if str(get(p,'side')).lower()==side and (get(p,'position') or '').lower()!='team']) for i,(side,r) in enumerate([('blue',a),('red',b)])}
  out.append(dict(source=source,game_id=gid,year=year,league=league,split=get(a,'split'),date=when,source_date=get(a,'date'),patch=get(a,'patch'),game=get(a,'game'),gamelength_source=get(a,'gamelength'),url=get(a,'url'),top_tier_candidate=eligible(league,year),teams=teams,reconciliation='not yet crosschecked with existing results'))
 return out,dict(source=source,year=year,source_rows=rowcount,distinct_source_game_ids=len(groups),valid_games=len(out),errors=errors)

def main():
 OUT.mkdir(exist_ok=True);REPORT.mkdir(exist_ok=True);allgames=defaultdict(list);audit=[]
 for archive in ['historical_2016_2019','annual_2020_2025']:
  with zipfile.ZipFile(R/f'data/raw/detailed/{archive}.zip') as z:
   for name in z.namelist():
    year=int(name[:4]);source=archive+':'+name
    if name.endswith('.xlsx'):rows=xlsxrows(z.read(name))
    else:rows=csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig'))
    games,a=normalize(rows,source,year);allgames[year].extend(games);audit.append(a);print(year,name,len(games),'games','errors',len(a['errors']),flush=True)
 # Current partial source retained, not renamed to a complete annual snapshot.
 with (R/'data/raw/oe_mirror_2026.csv').open() as f:
  games,a=normalize(csv.DictReader(f),'existing_local_2026_mirror',2026);allgames[2026].extend(games);audit.append(a)
 # Keep the independently structured timeline archive separate, with original
 # source addresses. Do not merge with OE by team/day guesses.
 with zipfile.ZipFile(R/'data/raw/detailed/chuckephron.zip') as z:
  timelines=defaultdict(list)
  for row in csv.DictReader(io.TextIOWrapper(z.open('LeagueofLegends.csv'))):
   y=int(row['Year']);gold={k:ast.literal_eval(row[k]) for k in ['goldblue','goldred','golddiff']};assert len(gold['goldblue'])==len(gold['goldred'])==len(gold['golddiff'])
   assert all(a-b==d for a,b,d in zip(gold['goldblue'],gold['goldred'],gold['golddiff']))
   timelines[y].append(dict(source='chuckephron/leagueoflegends',url=row['Address'],year=y,league=row['League'],split=row['Season'],stage=row['Type'],blue=row['blueTeamTag'],red=row['redTeamTag'],blue_win=int(row['bResult']),red_win=int(row['rResult']),date=None,patch=None,gold_series=gold,minute_alignment='source gold.csv min_1 onward; exact timestamp convention not independently verified',lineups={side:[dict(role=role,player=row[side+role],champion=row[side+role+'Champ']) for role in ['Top','Jungle','Middle','ADC','Support']] for side in ['blue','red']},events={k:ast.literal_eval(row[k]) for k in ['bKills','rKills','bTowers','rTowers','bDragons','rDragons','bBarons','rBarons']},reconciliation='not merged with OE; dates absent'))
 coverage=[]
 for year in range(2013,2027):
  games=allgames[year];unique={};duplicates=[];conflicts=[]
  for g in games:
   ident=g['game_id']
   if ident in unique:
    old=unique[ident]
    if old['teams']==g['teams'] and old['date']==g['date']:duplicates.append(ident)
    else:conflicts.append(dict(game_id=ident,sources=[old['source'],g['source']]))
    continue
   unique[ident]=g
  games=list(unique.values());top=[g for g in games if g['top_tier_candidate']];ts=timelines.get(year,[])
  # Team economic coverage, not ten-player row count.
  fields={k:sum(all(g['teams'][s]['stats'][k] is not None for s in ['blue','red']) for g in top) for k in STAT}
  rec=dict(year=year,season=year-2010,source_games=len(games),top_tier_candidates=len(top),dates=sum(bool(g['date']) for g in top),patches=sum(bool(g['patch']) for g in top),ten_players=sum(all(len(g['teams'][s]['players'])==5 and all(p['name'] for p in g['teams'][s]['players']) for s in ['blue','red']) for g in top),first=min((g['date'] for g in top if g['date']),default=None),last=max((g['date'] for g in top if g['date']),default=None),field_counts=fields,league_games=dict(Counter(g['league'] for g in top)),timeline_games=len(ts),duplicate_ids=len(duplicates),conflicts=conflicts)
  coverage.append(rec)
  for label,records in [('games',games),('timelines',ts)]:
   with (OUT/f'S{year-2010}_{label}.jsonl').open('w') as f:
    for g in records:f.write(json.dumps(g,ensure_ascii=False,allow_nan=False)+'\n')
 (OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n');(OUT/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 lines=['# 各赛季逐局详细数据：可得性审计','','[项目首页](../../README.md)','','新取得的数据尚未并入胜负训练或已发布预测。下面统计文件中实际可解析的记录，不代表全年所有顶级赛事已经完整收齐。源文件还包含次级联赛，已单独保留；“顶级候选”是联赛标签初筛，资格赛和杯赛阶段仍须逐项核准。','','| 赛季 | 逐局记录（全部层级） | 顶级／国际候选 | 双方总经济 | 双方10分钟经济 | 双方15分钟经济 | 十人阵容 | 独立逐分钟经济档案 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 for c in coverage:lines.append(f'| [S{c["season"]}](S{c["season"]}.md) | {c["source_games"]:,} | {c["top_tier_candidates"]:,} | {c["field_counts"]["totalgold"]:,} | {c["field_counts"]["goldat10"]:,} | {c["field_counts"]["goldat15"]:,} | {c["ten_players"]:,} | {c["timeline_games"]:,} |')
 lines+=['','逐分钟档案与 OE 文件可能重复，**不能把两列直接相加**。它缺少精确比赛日期，暂不用于时间衰减训练；所有经济数字来自实际赛后数据，未来只能作为赛前历史摘要使用。','','## 当前缺口','','- S3 尚未取得可用的批量逐局详细文件；S4 有 78 局 WC 标签的逐分钟档案，缺精确日期。','- S5 目前仅有独立逐分钟档案；缺精确日期和版本，不能直接补进当前回测。','- S6–S9 本次 Excel 归档截止于各年 9 月，均不含 Worlds；S6 也缺 LPL 和 MSI。此前取得的独立 Worlds 镜像仍需与本批数据统一对账。','- S10–S15 年度文件已取得，但年度文件名不证明每个联赛或每个经济字段完整。','- S16 旧镜像全部层级截止于 2026-06-21，顶级／国际候选记录截止于 2026-06-14；7–10 月细节未补齐。','- 单局经济为空必须保留为空，不能填 0。时长单位保留源值，未跨版本强行统一。','','## 来源','','- [2015–2018 职业赛与逐分钟经济](https://www.kaggle.com/datasets/chuckephron/leagueoflegends)','- [2016–2019 OE 历史赛段归档](https://www.kaggle.com/datasets/huitongkou/league-of-legends-pro-matches-data)','- [2020–2025 OE 年度归档](https://www.kaggle.com/datasets/toofxd/lol-esports-match-data-from-oracleselixir)','- 2026 采用此前本地镜像，原始下载 URL 尚缺；不因此授权新增胜负记录。']
 (REPORT/'README.md').write_text('\n'.join(lines)+'\n')
 for c in coverage:
  y=c['year'];s=c['season'];top=[g for g in allgames[y] if g['top_tier_candidate']]
  text=f'# S{s}（{y}）：逐局数据覆盖\n\n[全部赛季](README.md)\n\n候选记录时间范围：{c["first"] or "未知"} 至 {c["last"] or "未知"}。版本非空 {c["patches"]:,} 局；精确到源日期字段可解析 {c["dates"]:,} 局。这里尚未与已发布比分逐场合并。\n\n| 联赛／赛事标签 | 小局 |\n| --- | ---: |\n'
  text+=''.join(f'| {k} | {v} |\n' for k,v in sorted(c['league_games'].items()))
  text+='\n## 可用经济与地图资源字段\n\n仅当蓝、红双方都有数值才计为一局完整记录。\n\n| 字段 | 双方完整小局数 |\n| --- | ---: |\n'+''.join(f'| {k} | {v:,} |\n' for k,v in c['field_counts'].items())
  text+=f'\n另有独立逐分钟档案 {c["timeline_games"]:,} 局，可能与上述文件重叠。\n'
  (REPORT/f'S{s}.md').write_text(text)
 print('Wrote independent data/detailed records and reports/detailed_data coverage; no predictions changed',flush=True)
if __name__=='__main__':
 main()
 from report_detailed_data import main as render_details
 render_details()

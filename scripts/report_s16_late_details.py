"""Readable per-league/map reports and explicit field completeness denominators."""
import json,re
from collections import defaultdict,Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'results/s16_jul_oct';REP=R/'reports/detailed_data/s16_jul_oct'
FIELDS={'lineups':'十人阵容','side':'红蓝方','champions':'十人英雄','patch':'版本','gold':'双方总经济','gd15':'双方15分钟经济差','gd10':'双方10分钟经济差','gold15':'双方15分钟绝对经济','kda':'十人KDA','cs':'十人补刀','damage':'十人对英雄伤害','vision':'十人视野分','duration':'小局时长'}
def has(g,field):
    ts=list(g['teams'].values());ps=[p for t in ts for p in t['players']]
    if field=='lineups':return len(ps)==10 and all(p['name'] and p['role'] for p in ps)
    if field=='side':return set(g['teams'])=={'blue','red'}
    if field=='champions':return len(ps)==10 and all(p['champion_asset'] for p in ps)
    if field=='patch':return bool(g['patch'])
    if field=='gold':return all(t['total_gold'] is not None and t['total_gold']>0 for t in ts)
    if field=='gd15':return all(t['gold_difference_15'] is not None for t in ts)
    if field=='gd10':return len(ps)==10 and all(p['stats'].get('GD@10','').strip() for p in ps)
    if field=='gold15':return len(ps)==10 and all(p['stats'].get('Golds@15','').strip() for p in ps)
    if field=='duration':return bool(g.get('duration'))
    if field in ('kda','cs','damage','vision'):
        keys={'kda':['Kills','Deaths','Assists'],'cs':['CS'],'damage':['Total damage to Champion'],'vision':['Vision Score']}[field]
        return len(ps)==10 and all(p['stats'].get(k,'').strip() for p in ps for k in keys)
    raise ValueError(field)

def main():
    REP.mkdir(parents=True,exist_ok=True);(REP/'games').mkdir(exist_ok=True)
    targets=json.loads((D/'targets.json').read_text());results=json.loads((D/'series.json').read_text());unmatched=json.loads((D/'unmatched.json').read_text())
    leagues=sorted({r['event'] for r in targets});expected=Counter();expected_series=Counter()
    for r in targets:expected[r['event']]+=r['wins1']+r['wins2'];expected_series[r['event']]+=1
    verified=[r for r in results if r['status']=='verified'];games=[g for r in verified for g in r['games']];rows=[]
    for league in leagues:
        rr=[r for r in verified if r['official']['event']==league];gg=[g for g in games if g['event']==league]
        rows.append(dict(event=league,expected_series=expected_series[league],verified_series=len(rr),expected_maps=expected[league],verified_maps=len(gg),fields={f:sum(has(g,f) for g in gg) for f in FIELDS}))
    gaps=[]
    for r in results:
        if r['status']!='verified':gaps.append(dict(id=r['official']['id'],date=r['official']['date'],event=r['official']['event'],teams=[r['official']['team1'],r['official']['team2']],reason=r.get('error',r['status']),expected_maps=r['official']['wins1']+r['official']['wins2'],source=r['gol']['detail']))
    for r in unmatched:
        o=r['official'];gaps.append(dict(id=o['id'],date=o['date'],event=o['event'],teams=[o['team1'],o['team2']],reason=r['reason'],expected_maps=o['wins1']+o['wins2'],source=o['source']))
    summary=dict(cutoff='2026-10-25',start='2026-07-01',expected_series=len(targets),verified_series=len(verified),expected_maps=sum(expected.values()),verified_maps=len(games),leagues=rows,gaps=gaps,field_coverage={f:sum(has(g,f) for g in games) for f in FIELDS},training_outcomes_added=0)
    (D/'coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    lines=['# S16 七月至十月逐局详细数据','','范围：2026年7月1日至北京时间10月25日已结束、已纳入本项目赛果清单的顶级联赛及一线国际赛。包括 LPL、LCK、LEC、LCS、CBLOL、LCP 和 MSI、EWC、DCGI、Worlds；不包含次级联赛及尚未进行的十月后续比赛。','',f'应有 **{len(targets)} 场系列赛、{sum(expected.values()):,} 个小局**；已取得并与官方比分核对 **{len(verified)} 场、{len(games):,} 局**。只有比赛列表、实际小局数量和逐局胜负累计全部吻合，才计入已核对数量。','', '## 分联赛覆盖','','| 联赛／赛事 | 应有系列赛 | 核对系列赛 | 应有小局 | 核对小局 | 十人阵容 | 双方总经济 | 双方15分钟经济差 |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        slug=re.sub(r'[^a-z0-9]+','_',r['event'].lower()).strip('_')
        lines.append(f'| [{r["event"]}]({slug}.md) | {r["expected_series"]} | {r["verified_series"]} | {r["expected_maps"]} | {r["verified_maps"]} | {r["fields"]["lineups"]} | {r["fields"]["gold"]} | {r["fields"]["gd15"]} |')
        ll=[f'# {r["event"]}：七月至十月小局明细','',f'已核对 {r["verified_series"]}/{r["expected_series"]} 场系列赛、{r["verified_maps"]}/{r["expected_maps"]} 小局。日期为原官方系列赛日期；小局独立开赛时间尚未补齐。','', '| 日期 | 小局 | 蓝方 | 红方 | 胜者 | 版本 | 时长 | 蓝方总经济 | 红方总经济 | 蓝方15分钟经济差 | 明细 |','|---|---:|---|---|---|---|---|---:|---:|---:|---|']
        for g in sorted((g for g in games if g['event']==r['event']),key=lambda g:(g['official_date'],g['official_series_id'],g['game'])):
            b,red=g['teams']['blue'],g['teams']['red'];fmt=lambda x:'缺失' if x is None else f'{x:,}'
            ll.append(f'| {g["official_date"]} | {g["game"]} | {b["name"]} | {red["name"]} | {b["name"] if b["win"] else red["name"]} | {g["patch"] or "缺失"} | {g["duration"] or "缺失"} | {fmt(b["total_gold"])} | {fmt(red["total_gold"])} | {fmt(b["gold_difference_15"])} | [选手与统计](games/{g["game_id"]}.md) |')
        ll+=['','[覆盖总览](README.md) · [缺口与冲突](gaps.md)',''];(REP/(slug+'.md')).write_text('\n'.join(ll))
    lines+=['','## 字段覆盖','','下列分母均为全部应有小局数，不能用已下载部分作为分母掩盖缺失。','', '| 字段 | 有效小局 | 全部应有小局 |','|---|---:|---:|']
    for f,label in FIELDS.items():lines.append(f'| {label} | {summary["field_coverage"][f]} | {summary["expected_maps"]} |')
    lines+=['','## 口径与局限','','8月1日 GEN–DK 第一局的 GOL 队伍／选手关联和数值统计损坏；已用官方 game ID 对应的十人元数据恢复阵容、红蓝方、英雄、版本，并依据官方0:2确定该局胜者。原始错误记录保留，经济、KDA、补刀、伤害、视野与时长仍留空；不能把这一局当作完整数值样本。','','人员、红蓝方、英雄和经济等来自 Games of Legends 的实际比赛页，胜负与原官方系列赛记录逐项核对；[官方赛程](https://lolesports.com/en-US/schedule)。源页面、来源链接及下载校验信息均保留。此补充只附加字段，不把同一小局作为新胜负重复加入训练，也未改动已发布预测。','','“15分钟经济差”是相对对位／对手的差值，不是15分钟绝对经济；页面缺少的字段保留缺失，不填零、不由最终经济倒推。英雄使用来源图片资源标识，以避免部分页面 alt 引号损坏。小局真实时间戳、完整逐分钟经济曲线不在本轮已保证字段中。','','[缺页、比分冲突与缺字段清单](gaps.md) · [十月世界赛实际名单](../worlds_2026/rosters.md)',''];(REP/'README.md').write_text('\n'.join(lines))
    lines=['# 七月至十月详细数据缺口','','## 未完成对账的比赛','','| 日期 | 赛事 | 对阵 | 应有小局 | 原因 | 来源 |','|---|---|---|---:|---|---|']
    for r in gaps:lines.append(f'| {r["date"]} | {r["event"]} | {r["teams"][0]} – {r["teams"][1]} | {r["expected_maps"]} | {r["reason"].replace(chr(10)," ").replace("|","/")} | [页面]({r["source"]}) |')
    if not gaps:lines+=['','无未完成比分对账的系列赛。']
    lines+=['','## 已对账小局中的核心字段缺失','','| 日期 | 赛事 | 对阵 | 小局 | 缺失字段 | 明细 |','|---|---|---|---:|---|---|']
    missing=0
    for g in games:
        fields=[FIELDS[f] for f in ('lineups','side','champions','patch','gold','gd15','kda','cs','damage','vision','duration') if not has(g,f)]
        if fields:
            missing+=1;lines.append(f'| {g["official_date"]} | {g["event"]} | {g["teams"]["blue"]["name"]} – {g["teams"]["red"]["name"]} | {g["game"]} | {"、".join(fields)} | [详情](games/{g["game_id"]}.md) |')
    if not missing:lines+=['','上述核心字段均已取得。']
    lines+=['','10分钟经济差、15分钟绝对经济及逐分钟曲线另以总览字段覆盖为准；没有把源页面未提供的这些列当作已补齐。',''];(REP/'gaps.md').write_text('\n'.join(lines))
    for g in games:
        b,red=g['teams']['blue'],g['teams']['red'];ps=b['players']+red['players'];lines=[f'# {b["name"]} 对 {red["name"]}：第 {g["game"]} 局','',f'{g["event"]}，官方系列赛日期 {g["official_date"]}，来源日期 {g["source_date"]}，版本 {g["patch"] or "缺失"}，时长 {g["duration"] or "缺失"}。','', '| 方位 | 战队 | 选手 | 位置 | 英雄资源标识 |','|---|---|---|---|---|']
        for side,label in [('blue','蓝方'),('red','红方')]:
            for p in g['teams'][side]['players']:lines.append(f'| {label} | {g["teams"][side]["name"]} | {p["name"]} | {p["role"]} | {p["champion_asset"] or "缺失"} |')
        if g.get('numeric_stats_status'):lines+=['','**数值统计缺失：原GOL小局数据已隔离；此页阵容来自官方元数据。未用全零占位数据替代真实经济或KDA。**']
        lines+=['','## 逐人统计','','| 指标 | '+' | '.join(p['name'] for p in ps)+' |','|---|'+'---:|'*10]
        fields=list(dict.fromkeys(k for p in ps for k in p['stats']))
        for f in fields:lines.append('| '+f+' | '+' | '.join(p['stats'].get(f,'').replace('|','/') or '缺失' for p in ps)+' |')
        lines+=['',f'[来源一]({g["sources"][0]}) · [来源二]({g["sources"][1]}) · [覆盖总览](../README.md)',''];(REP/'games'/(g['game_id']+'.md')).write_text('\n'.join(lines))
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':main()

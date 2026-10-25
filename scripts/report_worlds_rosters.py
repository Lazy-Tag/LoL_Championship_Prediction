"""Actual observed Worlds lineups, separate from the opening-roster experiment."""
import json
from collections import Counter
from pathlib import Path
from backtest import load_season,key
from evaluate_detail_features import reconcile
from roster_carry_model import make_rosters,player_key,overlap
from model import WORLD_TEAMS
R=Path(__file__).resolve().parents[1];OUT=R/'results/worlds_2026_details';REP=R/'reports/detailed_data/worlds_2026'
def main():
    rows,_=load_season(15);mm,_=reconcile(15,rows);old=make_rosters(rows,mm)
    games=json.loads((OUT/'games.json').read_text());audit=[]
    opening={r['code']:r for r in json.loads((R/'results/roster_carry_experiment/summary.json').read_text())['s16_opening_rosters']}
    lines=['# S16 世界赛实际出场阵容','','按每队最近一次已结束系列赛的小局出场份额汇总。此处已使用十月世界赛逐局数据，区别于旧镜像中的开季阵容。相同五人每人占20%；替补轮换按实际出场份额计算。','','上季对照仅限同规范队名能对应的记录；“缺失”不等于全部换人。本表是人员重合度，不是胜率或拟合后的模型系数，尚未加入正式预测。','','| 战队 | 最近官方系列赛时间（UTC） | 实际出场选手 | 相对上季末人员重合 | 相对本季开季人员重合 |','|---|---|---|---:|---:|']
    for code,(name,_,_) in WORLD_TEAMS.items():
        gg=[g for g in games if any(t['code']==code for t in g['teams'].values())];last=max(g['official_series_start_utc'] for g in gg);gg=[g for g in gg if g['official_series_start_utc']==last];c=Counter()
        for g in gg:
            t=next(t for t in g['teams'].values() if t['code']==code);c.update(player_key(p['name']) for p in t['players'])
        shares={k:v/sum(c.values()) for k,v in c.items()};prev=old.get(key(name),{}).get('last');first=opening.get(code,{}).get('current_lineup')
        qold=overlap(prev['shares'],shares) if prev else None;qnew=overlap(first['shares'],shares) if first else None
        record=dict(code=code,date=last,shares=shares,previous_lineup=prev,opening_lineup=first,previous_overlap=qold,opening_overlap=qnew,source_games=[g['game_id'] for g in gg]);audit.append(record)
        fmt=lambda q:'缺失' if q is None else f'{q:.1%}'
        lines.append(f'| {code} | {last} | '+', '.join(f'{n} ({v:.0%})' for n,v in shares.items())+f' | {fmt(qold)} | {fmt(qnew)} |')
    lines+=['','这里没有将上一季阵容距末场较远的队伍自动判为可继承；逐行来源日期与开季资格检查仍见[开季模型诊断](../../roster_carry/s16_opening.md)。这些实际世界赛名单可用于后续季中阵容变化模型，但不能回填到其公布之前的历史预测。','']
    (REP/'rosters.md').write_text('\n'.join(lines));(OUT/'current_rosters.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    p=REP/'README.md';s=p.read_text();link='[各队最新实际出场阵容](rosters.md)'
    if link not in s:s=s.replace('\n\n','\n\n'+link+'\n\n',1);p.write_text(s)
if __name__=='__main__':main()

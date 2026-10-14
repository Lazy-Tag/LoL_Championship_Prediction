"""Verify Monte Carlo counts and render the S16 championship estimate."""
import hashlib,html,json,math,sys
from pathlib import Path
from model import WORLD_TEAMS
R=Path(__file__).resolve().parents[1]
raw=json.loads((R/'results/simulation_raw.json').read_text());n=raw['simulations']
assert n==14000605 and raw['seed']==2026
assert [sum(c[i] for c in raw['counts']) for i in range(5)]==[n,16*n,8*n,4*n,2*n]
fair=json.loads((R/'results/simulation_fair_test.json').read_text())
exact=json.loads((R/'results/exact_results.json').read_text())['playin']['90']['swiss_qualification']
for i,t in enumerate(WORLD_TEAMS):
 p=1/64 if t in exact else 1/16
 assert abs(fair['counts'][i][0]-fair['simulations']*p)<6*math.sqrt(fair['simulations']*p*(1-p))
 if t in exact:
  p=exact[t];assert abs(raw['counts'][i][1]-n*p)<6*math.sqrt(n*p*(1-p))+2
 assert 0<=raw['counts'][i][0]<=raw['counts'][i][4]<=raw['counts'][i][3]<=raw['counts'][i][2]<=raw['counts'][i][1]<=n

def wilson(k):
 p=k/n;z=1.959963984540054;den=1+z*z/n;center=(p+z*z/(2*n))/den
 half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return [max(0,center-half),min(1,center+half)]
rows=[]
for (team,meta),c in zip(WORLD_TEAMS.items(),raw['counts']):
 rows.append(dict(team=team,name=meta[0],champion_count=c[0],championship_probability=c[0]/n,mc_95_wilson_interval=wilson(c[0]),swiss_probability=c[1]/n,quarterfinal_probability=c[2]/n,semifinal_probability=c[3]/n,final_probability=c[4]/n))
rows.sort(key=lambda r:-r['champion_count'])
result={**raw,'half_life_days':90,'cutoff':'2026-10-14','reference_date':'2026-10-19','rng':'std::mt19937_64 seeded with 2026; rejection-sampled bounded integers; Fisher-Yates shuffles; top 53 bits for uniform [0,1)', 'draw_assumption':'Random draw order. Place each team in earliest available slot permitting a complete legal assignment; backtrack for lookahead. Round 1 fixed pool matchups with no same-region games. Later rounds same record and no rematches. If impossible, waive no-rematch for that group and use original random order. This operationalizes the rule; referee discretion is not uniquely probabilized by the rulebook.', 'uncertainty':'Intervals are pointwise 95% Monte Carlo sampling intervals only, not model/data/draw-procedure uncertainty. Zero sampled wins does not imply impossible.', 'input_sha256':hashlib.sha256((R/'results/simulation_input.txt').read_bytes()).hexdigest(),'teams':rows,'verification':'Stage totals, nested advancement, fair-team baseline within 6 standard deviations, play-in versus exact within 6 standard deviations; 20000 forbidden-opponent graphs tested against independent matching search.'}
(R/'results/s16_championship_simulation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
lines=['# S16 夺冠概率：14,000,605 次模拟','', '随机种子 2026；半衰期 90 天；使用截至 2026-10-14 的比赛数据。','', '| 队伍 | 夺冠次数 | 夺冠概率 | 蒙特卡洛 95% 区间 |','|---|---:|---:|---:|']
for r in rows:
 lo,hi=r['mc_95_wilson_interval'];lines.append(f"| {r['team']} | {r['champion_count']:,} | {100*r['championship_probability']:.6f}% | {100*lo:.6f}%–{100*hi:.6f}% |")
lines+=['','这些是模拟估计，不是全路径精确解。区间只反映有限抽样误差，不包含实力模型、数据缺口或抽签执行方式的误差。零次夺冠不代表概率为零。', '', f"每次模拟完整覆盖入围赛、瑞士轮和八强淘汰赛；总耗时 {raw['seconds']:.2f} 秒。无法合法配对而触发豁免的分组数：{raw['waived_draw_groups']}。",'', '抽签实现：随机打乱抽出顺序，每支队放到可完成全组合法配对的最早空位，遇冲突顺延并回溯检查。首轮按四个种子池且避同赛区；后续同战绩且避重复交手。裁判裁量没有唯一概率定义，本结果以此执行方式为条件。', '', '胜率假设：各局独立、同一对手的小局胜率固定，BO3/BO5 使用解析级数胜率；未建模全局 BP 的局序差异、英雄消耗、选边、赛季中换人、替补上场及赛中状态变化。']
(R/'results/s16_championship_simulation.md').write_text('\n'.join(lines)+'\n')
print('Verified simulation and wrote results/s16_championship_simulation.md')

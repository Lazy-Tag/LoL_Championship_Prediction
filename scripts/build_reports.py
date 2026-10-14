"""Build all human-facing reports as GitHub Markdown, from frozen JSON results."""
import json
from pathlib import Path
from collections import defaultdict
from backtest import metrics
from model import series_probability
from region_rankings import region_rankings, order_text, section
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def write(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n')
def pct(x,d=2):return '—' if x is None else f'{100*x:.{d}f}%'
def num(x):return '—' if x is None else f'{x:.4f}'
def esc(x):return str(x).replace('|','\\|').replace('\n',' ')
def table(head,rows):return '\n'+'| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(esc(c) for c in row)+' |\n' for row in rows)+'\n'
LIMIT='当前模型没有区分全局 BP 下的第几局、此前消耗的英雄或 BP 策略，也没有建模赛季中换人、替补上场、选边、版本变化和系列赛内状态关联。一个赛季内同名队伍视为同一队，近期比赛仅通过时间权重获得更大影响。'
MODEL_NAMES={'regional90':'赛区先验 · 90 天','neutral90':'中性先验 · 90 天','strict90':'无正则 MLE · 可识别子集','regional30':'赛区先验 · 30 天','regional60':'赛区先验 · 60 天','regional180':'赛区先验 · 180 天'}
MAIN_MODELS=['regional90']
s=read('results/backtest_summary.json');pred=read('results/backtest_predictions.json');manifest=read('data/history/manifest.json');sim=read('results/s16_championship_simulation.json');models=read('results/models.json');exact=read('results/exact_results.json');audit=read('results/data_audit.json')

def metric_table(mm):return table(['结果','覆盖系列赛','系列赛命中率','小局命中率','小局 Log loss ↓','小局 Brier ↓'],[['主结果',v['covered_series'],pct(v['series_accuracy']),pct(v['map_accuracy']),num(v['map_logloss']),num(v['map_brier'])] for k,v in mm.items() if k in MAIN_MODELS])

# Historical overview and per-season complete readable records.
body='# S4–S15 历史回测\n\n[返回首页](../../README.md) · [模型说明](../../MODEL.md) · [数据质量](../../docs/DATA.md)\n\n逐日回放 MSI、2020 MSC 与 Worlds（包含入围赛），共 **1,348 场系列赛、2,028 小局**。各场预测只使用赛前已知成绩。整届赛前排名与冠军预测另见[完整赛事回放](../event_replay/README.md)。\n\n主结果：系列赛 **68.66%**，小局 **65.26%**。\n\n> 这些命中率反映已收集比赛上的表现。S3 不参与回放，S4 国内数据不足，其他历史数据也有缺口。15 场预测恰为五五开，按 0.5 次期望命中计分。历史回测不能直接保证 S16 的预测准确性。\n\n## 预测表现\n'+metric_table(s['aggregate'])+'## 按赛季与赛事\n'
body+=table(['赛季','赛事','系列赛','小局','系列赛命中率','小局命中率'],[[f"[S{x['season']}](S{x['season']}/README.md)",x['event'],x['models']['regional90']['covered_series'],x['models']['regional90']['maps'],pct(x['models']['regional90']['series_accuracy']),pct(x['models']['regional90']['map_accuracy'])] for x in s['by_season_event']])
body+='## 按系列赛长度\n'+table(['赛制','系列赛数量','命中率'],[[f'BO{k}',v['series'],pct(v['accuracy'])] for k,v in s['aggregate']['regional90']['by_bo'].items()])
body+='## 如何理解\n\n命中率统计预测胜者是否获胜；Log loss 和 Brier 还衡量概率是否过度自信，越低越好。每个系列赛开始前预测一次，系列赛内不更新。\n\n'+LIMIT+'\n'
write('reports/history/README.md',body)
for season in range(4,16):
 rr=[r for r in pred if r['season']==season];allrows=read(f'data/history/S{season}/series.json');coverage=next(x for x in manifest['seasons'] if x['season']==f'S{season}')
 mm={k:metrics(rr,k) for k in MODEL_NAMES}
 body=f'# S{season}（{season+2010}）回测结果\n\n[全部赛季](../README.md) · [逐场预测](predictions.md) · [逐场小局概率](probabilities.md) · [全部已收集赛果](matches.md)\n\n'
 body+=f"本赛季收集了 **{coverage['downloaded_tournaments']} 个赛事、{len(allrows):,} 场系列赛、{coverage['maps']:,} 小局**；回测评价其中 {len(rr)} 场 MSI／MSC／Worlds。\n\n"
 if season<=4:body+='> 本赛季国内覆盖明显不足，请勿把它解释为完整当季数据训练的预测。\n\n'
 body+=metric_table(mm)+'## 分赛事\n'+table(['赛事','系列赛','小局','系列赛命中率','小局命中率'],[[x['event'],x['models']['regional90']['covered_series'],x['models']['regional90']['maps'],pct(x['models']['regional90']['series_accuracy']),pct(x['models']['regional90']['map_accuracy'])] for x in s['by_season_event'] if x['season']==season])
 body+='## 数据说明\n\n当日预测仅使用更早日期的当季成绩。概率相等时计半次期望命中。\n\n'+('本赛季有 '+str(len(coverage['issues']))+' 个赛事的小局计数不一致，详见[数据质量](../../../docs/DATA.md)。' if coverage['issues'] else '本赛季已选赛事比分表小局数与来源目录一致；这不证明来源覆盖所有比赛。')+'\n\n'+LIMIT
 write(f'reports/history/S{season}/README.md',body)
 body=f'# S{season} 逐场预测与实际结果\n\n[本赛季汇总](README.md) · [小局概率](probabilities.md)\n\nA 队系列赛胜率由赛前小局概率转换；BO1 即单局。每行是一场系列赛，比分为 A:B。五五开不强行指定胜者，汇总时计半次期望命中。\n'
 out=[]
 for r in rr:
  p=r['regional90'];tie=abs(p-.5)<1e-12;choice='五五开' if tie else r['display1'] if p>.5 else r['display2'];hit='半次期望命中' if tie else '✓' if (p>.5)==(r['wins1']>r['wins2']) else '✗'
  out.append([r['date'],r['event'],r['display1'],f"[{r['wins1']}:{r['wins2']}]({r['detail']})",r['display2'],f"BO{r['best_of']}",pct(float(series_probability(p,r['best_of'])),3),choice,hit])
 body+=table(['日期','赛事','A 队','实际比分','B 队','赛制','A 系列赛胜率','预测胜者','命中'],out)
 write(f'reports/history/S{season}/predictions.md',body)
 body=f'# S{season} 逐场小局概率\n\n[逐场结果](predictions.md) · [模型定义](../../../MODEL.md)\n\n表中全部为 **A 队赢下一小局** 的概率，不是系列赛概率。\n'
 body+=table(['日期','A 队','B 队','A 队小局胜率','训练系列赛数','最晚训练日'],[[r['date'],r['display1'],r['display2'],*[pct(r[k],4) for k in MAIN_MODELS],r['training_series'],r['latest_training_date'] or '无'] for r in rr])
 write(f'reports/history/S{season}/probabilities.md',body)
 body=f'# S{season} 全部已收集赛果\n\n[本赛季汇总](README.md) · [数据范围与缺口](../../../docs/DATA.md)\n\n共 {len(allrows):,} 场系列赛。这里包含训练数据及目标赛事，不代表每一场都作为回测评价目标。保留来源的队名与赛事名；历史 BO2 等特殊赛制使得不能单凭比分推断 BO 长度。比分链接指向原始赛果页。\n'
 body+=table(['日期','赛事','阶段','A 队','比分 A:B','B 队'],[[r['date'],r['tournament'],r.get('stage',''),r['team1'],f"[{r['wins1']}:{r['wins2']}]({r['detail']})",r['team2']] for r in sorted(allrows,key=lambda r:(r['date'],r['tournament']))])
 write(f'reports/history/S{season}/matches.md',body)
# Human-readable prior audit.
body='# 历史回测使用的上一季赛区先验\n\n[模型说明](../../MODEL.md) · [回测总览](README.md)\n\n数值为 logistic 实力刻度，不是胜率。正值代表相对较强；差值经过 sigmoid 才成为跨赛区基准胜率。仅由上一赛季国际赛产生，未继承战队成绩。S3 不参与回放；已收集的 S3 国际赛仍可作为 S4 的上一季赛区数据。\n'
for season,hs in s['regional_prior_audit'].items():
 body+=f'\n## 用于 S{season}\n'
 body+=table(['半衰期','来源系列赛','来源小局','最晚来源日期','赛区','先验强度'],[[h,v.get('series',0),v.get('maps',0),v.get('last_date','无'),reg,f'{strength:.6f}'] for h,v in hs.items() if str(h)=='90' for reg,strength in v.get('strength',{}).items()])
write('reports/history/regional_priors.md',body)
# S16 readable results and all matchup probabilities.
body='# S16：14,000,605 个未来中的夺冠概率\n\n[返回首页](../../README.md) · [模型与算法](../../MODEL.md) · [全部赛果](matches.md)\n\n数据截至 **2026-10-14**；每次模拟覆盖入围赛、瑞士轮和淘汰赛，实际完成 **14,000,605 次**。\n\n## 夺冠与晋级\n\n概率为蒙特卡洛估计，区间仅是点态 95% 抽样区间，不含模型或数据误差。零次夺冠不能解读为绝无可能。\n'
body+=table(['队伍','夺冠次数','夺冠概率','95% 抽样区间','进入瑞士轮','进入八强','进入四强','进入决赛'],[[r['team'],f"{r['champion_count']:,}",pct(r['championship_probability'],6),'–'.join(pct(x,6) for x in r['mc_95_wilson_interval']),pct(r['swiss_probability'],4),pct(r['quarterfinal_probability'],4),pct(r['semifinal_probability'],4),pct(r['final_probability'],4)] for r in sim['teams']])
m90=models['models']['90'];ix90={t:i for i,t in enumerate(m90['teams'])}
s16_regions=region_rankings([dict(name=t,region=v[1],strength=m90['strength'][ix90[v[0]]],title_probability=next(x['championship_probability'] for x in sim['teams'] if x['team']==t)) for t,v in models['world_teams'].items()])
write('results/s16_region_rankings.json',json.dumps(s16_regions,ensure_ascii=False,indent=2))
body=body.replace('## 夺冠与晋级',section(s16_regions)+'## 夺冠与晋级',1)
body+='## 结果的边界\n\n'+LIMIT+'\n\n表中概率为模拟估计，仍受数据与赛制假设限制。\n\n## 两两对决\n\n每份表含所有 19 队的 171 个无序组合，以及 BO1、BO3、BO5 三种胜率。A 对 B 的反向概率为 1 减去表中数值。\n\n[两两胜率](matchups-90.md)\n\n## 入围赛：精确晋级概率\n'
body+=table(['队伍','晋级概率'],[[t,pct(exact['playin']['90']['swiss_qualification'][t],8)] for t in ['KC','C9','FUR','MVK']])
body+='\n## 队伍与种子\n'+table(['简称','全名','赛区','赛区种子'],[[k,*v] for k,v in models['world_teams'].items()])
body+='\n## 当季数据覆盖\n'+table(['赛事类别','系列赛','小局','起始日','结束日'],[[k,v['series'],v['maps'],v['first'],v['last']] for k,v in audit['counts'].items()])
write('reports/s16/README.md',body)
for h,m in models['models'].items():
 ix={t:i for i,t in enumerate(m['teams'])};world=list(models['world_teams']);rr=[]
 for i,a in enumerate(world):
  for b in world[i+1:]:
   ia,ib=ix[models['world_teams'][a][0]],ix[models['world_teams'][b][0]]
   rr.append([a,b,*[pct(m[k][ia][ib],4) for k in ['bo1','bo3','bo5']]])
 body=f'# S16 两两胜率：半衰期 {h} 天\n\n[返回 S16 结果](README.md) · [模型](../../MODEL.md)\n\n所有概率均为 **A 队战胜 B 队**。BO1 是小局胜率；BO3/BO5 是系列赛胜率，并未区分系列赛内第几局。\n'+table(['A 队','B 队','BO1','BO3','BO5'],rr)
 body+='\n## 全部 62 队的实力估计\n\nθ 是相对强度，不是夺冠概率。\n'+table(['队伍','θ','训练小局数'],[[m['teams'][i],f"{m['strength'][i]:.6f}",m['games'][i]] for i in sorted(range(len(m['teams'])),key=lambda i:-m['strength'][i])])
 if str(h)=='90':
  write('reports/s16/matchups-90.md',body)
 else:
  body=body.replace('[返回 S16 结果](README.md)', '[敏感性分析附录](README.md)')
  write(f'reports/sensitivity/matchups-{h}.md',body)
  (R/f'reports/s16/matchups-{h}.md').unlink(missing_ok=True)
rr=read('data/series.json');body='# S16 全部已纳入赛果\n\n[返回 S16 结果](README.md) · [数据审计](../../docs/DATA.md)\n\n1,099 场系列赛、2,820 小局。截止 2026-10-14，保留当季所有纳入范围的比赛；小局贡献按总比分计，不重复增加一次系列赛胜负。\n'
body+=table(['日期','赛事','阶段','A 队','比分 A:B','B 队','赛制','来源'],[[r['date'],r.get('tournament',r.get('event','')),r.get('stage',''),r['team1'],f"{r['wins1']}:{r['wins2']}",r['team2'],f"BO{r['best_of']}",f"[赛果]({r.get('crosscheck_source') or r['source']})"] for r in rr]);write('reports/s16/matches.md',body)
# Data quality manifest.
body='# 数据来源、范围与已知缺口\n\n[返回首页](../README.md)\n\n## 公开来源\n\n- [Riot Worlds 2026 Primer](https://lolesports.com/en-GB/news/worlds-2026-primer) 与 [官方规则库](https://competitiveops.riotgames.com/en-US/library)。\n- [Riot 公开赛程](https://lolesports.com/en-US/schedule)：2026 官方系列赛比分。\n- [Games of Legends](https://gol.gg/tournament/list/)：独立赛事目录、系列赛比分及历史数据；逐场报告附来源链接。\n\n## S16\n\n统计覆盖 LPL、LCK、LEC、LCS、LCP、CBLOL 的全年已完成阶段及 First Stand、MSI、EWC 主赛与资格赛、美洲杯、DCGI。未纳入次级联赛、国家队赛事、非联赛性质的 KeSPA Cup 和混合层级升降级赛。\n\nRiot 与 44 个 GOL 赛事比分表已对照。2026-08-01 GEN–DK 出现 GOL 1:1 与 Riot 0:2 冲突，采用官方 0:2。时间按系列赛日期近似，没有逐局开赛时刻。\n\n## S4–S15 覆盖\n\nS3/S4 国内联赛覆盖明显不足。来源赛季标签决定归属，未强行按自然年重新分组。目录和比分表计数一致只说明来源内部对账，不证明全球比赛完整收齐。\n'
body+=table(['赛季','收集赛事','系列赛','比分表小局数','赛事目录小局数','不一致赛事数'],[[x['season'],x['downloaded_tournaments'],x['series'],x['maps'],x['source_census_maps'],len(x['issues'])] for x in manifest['seasons']])
body+='\n## 逐项计数缺口\n'+table(['赛季','赛事','比分表小局数','赛事目录小局数','状态'],[[x['season'],f"[{v['tournament']}]({v['source']})",v['parsed_maps'],v['source_census_maps'],'小局数不一致'] for x in manifest['seasons'] for v in x['issues']])
body+='\n所有回测目标赛事的解析小局数与来源目录一致，但训练赛事的上述缺口仍会影响预测。并未凭空补比分，也没有把未获取的数据视为零场或零胜。\n\n## 模型不覆盖的因素\n\n'+LIMIT+'\n\n赛区先验依赖上一季国际赛，样本少的赛区仍有较大不确定性；旧队名使用规范化字符串连接，不擅自推断俱乐部合并。早期缺失赛区标签使用显式元数据补齐，不能将其解释为补齐比赛记录。\n'
write('docs/DATA.md',body)
# Results-first landing page.
body='# LoL Championship Prediction\n\n用公开赛果回答两个问题：**S16 谁最可能夺冠？同类胜率模型回放历史比赛，能猜对多少？**\n\nS16 使用截至 **2026-10-14** 的 **1,099 场系列赛、2,820 小局**，完成 **14,000,605 次**全赛事模拟，随机种子 **2026**。模拟次数取自《复仇者联盟：无限战争》中奇异博士观察的未来数量（[D23](https://d23.com/doctor-stranges-maddening-journey-through-the-mcu/)）。预测范围截至上述日期。\n\n## S16：GEN 领先，HLE 与 T1 随后\n'
body+=table(['队伍','夺冠概率','模拟夺冠次数'],[[r['team'],pct(r['championship_probability'],6 if r['championship_probability']<0.0001 else 4),f"{r['champion_count']:,}"] for r in sim['teams']])
body+='\n这是模拟估计。GEN 的 95% 抽样区间约为 **51.415%–51.467%**；这个窄区间只说明模拟抽样充分，不能说明现实预测同样准确。零次夺冠也不等于现实概率为零。\n\n[完整夺冠与各轮晋级概率](reports/s16/README.md) · [19 队两两胜率](reports/s16/matchups-90.md) · [2026 全部纳入赛果](reports/s16/matches.md)\n\n## S4–S15：系列赛命中率 68.66%\n\n回放 MSI、2020 MSC 与 Worlds（含入围赛），合计 **1,348 场系列赛、2,028 小局**。每场预测只使用赛前已知成绩。\n'
body+=table(['方案','系列赛命中率','小局命中率'],[['主结果',pct(s['aggregate'][k]['series_accuracy']),pct(s['aggregate'][k]['map_accuracy'])] for k in MAIN_MODELS])
body+='\n15 场五五开按半次期望命中计分。这里衡量逐场胜负预测，不是历年冠军预测命中率，也不是 S16 模型的直接验证。S3 不参与回放，S4 国内数据不足，结果应结合覆盖范围阅读。\n\n[回测总览与逐年比较](reports/history/README.md) · [数据来源和缺口](docs/DATA.md)\n\n## 逐季阅读\n'
body+=table(['赛季','回测汇总','逐场预测对照','全部已收集赛果'],[[f'S{i}',f'[汇总](reports/history/S{i}/README.md)',f'[预测与实际](reports/history/S{i}/predictions.md)',f'[赛果](reports/history/S{i}/matches.md)'] for i in range(4,16)])
body+='\n## 这些结果没有考虑什么？\n\n'+LIMIT+'\n\n因此，全局 BP 后半段、临时换人或阵容磨合都可能使实际表现偏离预测。14,000,605 次模拟只能降低抽样误差，不能修复这些模型遗漏。\n\n## 延伸阅读\n\n- [概率是怎样算出来的？](MODEL.md)\n- [用了哪些比赛，数据有哪些缺口？](docs/DATA.md)\n\n\n'
body=body.replace('## S16：GEN 领先，HLE 与 T1 随后', '## S16：GEN 领先，HLE 与 T1 随后\n\n赛前赛区实力顺序：**'+order_text(s16_regions)+'**（按本届参赛阵容）。',1)
write('README.md',body)
write('reports/README.md','# 结果索引\n\n- [S16 夺冠、晋级与两两胜率](s16/README.md)\n- [S4–S15 历史回测与逐场结果](history/README.md)\n- [返回项目首页](../README.md)\n')
print('Built Markdown: README, historical S3-S15 summaries/predictions/probabilities/all scores, S16 results/matchups/scores, regional priors, and data audit.')

# Archived sensitivity analysis is deliberately separate from primary reports.
body='# 半衰期敏感性分析附录\n\n[模型细节](../../MODEL.md)\n\n主结果固定使用 **90 天**。以下保留此前 30、60、180 天的对照，不参与主结果排序或参数选择。只有 90 天完成了 S16 全赛事模拟；其他半衰期没有全赛程夺冠概率。历史对照衡量逐场预测，不是赛前冠军预测。\n\n## S16 两两胜率\n\n- [30 天](matchups-30.md)\n- [60 天](matchups-60.md)\n- [180 天](matchups-180.md)\n\n## S16 入围赛精确晋级概率\n'
body+=table(['队伍','30 天','60 天','90 天','180 天'],[[t,*[pct(exact['playin'][h]['swiss_qualification'][t],8) for h in ['30','60','90','180']]] for t in ['KC','C9','FUR','MVK']])
body+='## 历史逐场回测汇总\n'+table(['半衰期','系列赛数','系列赛命中率','小局命中率','小局 Log loss','小局 Brier'],[[h,s['aggregate']['regional'+h]['covered_series'],pct(s['aggregate']['regional'+h]['series_accuracy']),pct(s['aggregate']['regional'+h]['map_accuracy']),num(s['aggregate']['regional'+h]['map_logloss']),num(s['aggregate']['regional'+h]['map_brier'])] for h in ['30','60','90','180']])
body+='对照结果较高不能证明该参数在独立样本上更优；没有按这些成绩重新选择半衰期。\n'
for season in range(4,16):
 rr=[r for r in pred if r['season']==season]
 body+=f'\n## S{season} 逐场小局概率\n\n全部为 A 队赢下一小局的概率，均使用赛区先验。\n'
 body+=table(['日期','赛事','A 队','B 队','30 天','60 天','90 天','180 天'],[[r['date'],r['event'],r['display1'],r['display2'],*[pct(r['regional'+h],4) for h in ['30','60','90','180']]] for r in rr])
body+='\n## 对照使用的上一季赛区先验\n\n以下为 logistic 强度，不是胜率。\n'
for season,hs in s['regional_prior_audit'].items():
 body+=f'\n### 用于 S{season}\n'
 body+=table(['半衰期','来源系列赛','来源小局','最晚来源日期','赛区','先验强度'],[[h,v.get('series',0),v.get('maps',0),v.get('last_date','无'),reg,f'{strength:.6f}'] for h,v in hs.items() for reg,strength in v.get('strength',{}).items()])
write('reports/sensitivity/README.md',body)

# Alternative priors are comparison material, not parallel main results.
body='# 历史模型对照：赛区先验、中性先验与无正则 MLE\n\n[敏感性附录](README.md) · [模型细节](../../MODEL.md)\n\n主模型固定为 90 天赛区先验。赛区先验利用上一季国际赛估计跨赛区基础强度；中性先验给所有队伍相同的初始均值；无正则 MLE 不施加先验，仅在数学上可识别、存在有限解时预测。后者覆盖的是选择性子集，不能直接与全量结果比较。模型选择依据当前回测表现，未经新的独立测试集验证，不能保证未来最优。\n'
def comparison(mm):
 return table(['模型','覆盖系列赛','系列赛命中率','小局命中率','小局 Log loss','小局 Brier'],[[MODEL_NAMES[k],v['covered_series'],pct(v['series_accuracy']),pct(v['map_accuracy']),num(v['map_logloss']),num(v['map_brier'])] for k,v in mm.items() if k in ['regional90','neutral90','strict90']])
body+='\n## 全量覆盖与成绩\n'+comparison(s['aggregate'])+'## 相同可识别子集\n'+comparison(s['strict_common_subset'])
for season in range(4,16):
 rr=[r for r in pred if r['season']==season]
 body+=f'\n## S{season}\n'+comparison({k:metrics(rr,k) for k in ['regional90','neutral90','strict90']})
 body+=table(['日期','赛事','A 队','B 队','赛区先验','中性先验','无正则 MLE'],[[r['date'],r['event'],r['display1'],r['display2'],*[pct(r[k],4) for k in ['regional90','neutral90','strict90']]] for r in rr])
write('reports/sensitivity/model_comparison.md',body)
p=R/'reports/sensitivity/README.md'
p.write_text(p.read_text().replace('[模型细节](../../MODEL.md)', '[模型细节](../../MODEL.md) · [先验与 MLE 对照](model_comparison.md)',1))
# Read statistics from the latest fit rather than keeping stale headline values.
for p in [R/'README.md',R/'reports/history/README.md']:
 text=p.read_text().replace('68.66%',pct(s['aggregate']['regional90']['series_accuracy'])).replace('65.26%',pct(s['aggregate']['regional90']['map_accuracy'])).replace('15 场',str(s['aggregate']['regional90']['tied_probability_series'])+' 场').replace('1,348',f"{len(pred):,}").replace('2,028',f"{sum(r['wins1']+r['wins2'] for r in pred):,}")
 p.write_text(text)
if (R/'results/event_replay/summary.json').exists():
 e=read('results/event_replay/summary.json')
 p=R/'README.md';text=p.read_text();marker='## S4–S15：系列赛命中率'
 at=text.index(marker)
 text=text[:at]+f"## S4–S15：整届冠军与排名回放\n\n{e['event_count']} 届赛事各完成 14,000,605 次模拟，概率第一命中 **{e['favorite_hits']}/{e['event_count']} 届冠军**。旧同分规则和部分抽签分布仍有近似；这是当前实现规则下的情景结果。\n\n[冠军、实力排名与实际成绩对照](reports/event_replay/README.md) · [逐届赛制与限制](reports/event_replay/rules.md)\n\n"+text[at:]
 p.write_text(text)
p=R/'reports/README.md';p.write_text(p.read_text()+'\n- [整届赛前排名与冠军预测回放](event_replay/README.md)\n')

write('reports/history/S3/README.md','# S3（2013）：仅保留赛果\n\n[历史回放总览](../README.md) · [已收集赛果](matches.md)\n\n赛前赛区与国内对局信息不足，本赛季不进行逐场或整届预测回放，也不纳入命中率、排名相关性与夺冠概率评价。已收集的实际比赛记录继续保留。\n')
p=R/'README.md';p.write_text(p.read_text()+'\nS3 不参与回放，仅保留[已收集赛果](reports/history/S3/matches.md)。\n')

if __name__ == "__main__" and (R/"results/main_model.json").exists():
    from publish_dynamic import main as publish_selected
    publish_selected()

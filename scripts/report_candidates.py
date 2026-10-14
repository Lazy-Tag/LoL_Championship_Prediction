"""Reader-facing candidate comparison, full event tables and data audit."""
import json,math
from pathlib import Path
import numpy as np
from scipy.stats import rankdata
from backtest import metrics
from model import WORLD_TEAMS,series_probability
from report_event_replay import table,common_band,correlation,band
from region_rankings import region_rankings,section
R=Path(__file__).resolve().parents[1];OUT=R/'reports/sensitivity';RES=R/'results/model_experiments'
NAMES={'regional90':'原模型','hierarchical90':'新分层模型','dynamic90':'动态模型'}
def pct(p):return '<0.01%' if p<.0001 else f'{p*100:.2f}%'
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.rstrip()+'\n')
def read(path):return json.loads(path.read_text())
def data_report():
 aa=read(R/'data/enrichment/coverage.json');s='# 数据补充与核验\n\n[返回首页](../../README.md) · [模型比较](../sensitivity/candidate_models.md)\n\n本轮增加逐局版本、时间、选边、选手阵容和经济／地图资源字段，并与已有系列赛比分对账。**没有新增获准进入训练的比赛结果**；两个新模型与原模型使用相同的胜负输入，因此预测差异来自模型，而非样本数量变化。\n\n## 覆盖范围\n\n2016–2022 的新增来源只含 Worlds，不能代表全年国内联赛；2025 来源覆盖多种联赛，筛除次级联赛和未核准的比赛。2026 现有镜像只更新到 6 月 21 日，且缺少最初下载链接，只作字段审计，不用于追加赛果。\n'
 s+=table(['赛季','可规范化小局','比分对账通过','原赛果小局','观察到的阵容变化'],[[f'S{a["season"]}',a['eligible_normalized_maps'],a['matched_maps'],a['base_maps'],a['observed_lineup_changes']] for a in aa])
 s+='对账通过仅表示可唯一对应已有系列赛、双方和小局比分；不是逐字段经过官方核实。分母“原赛果小局”是该季全体已收集比赛，部分镜像只覆盖 Worlds，不能将这一比例当作全年源数据完整率。观察到的阵容变化是两次已采样阵容不同，不等于转会公告日期，也可能是临时替补。\n\n## 字段覆盖\n\n以下为规范化记录中字段非空的小局数，包含已隔离记录；实际可用记录还须通过比分核验。\n'
 s+=table(['赛季','版本','完整十人阵容','15 分钟经济差','小龙','大龙'],[[f'S{a["season"]}',*[a['field_counts'][k] for k in ['patch','complete_ten_players','golddiffat15','dragons','barons']]] for a in aa])
 s+='## 仍未补齐的内容\n\n- S4 早期国内赛果仍存在明显缺口；S3 继续不回放。2014–2024 全年逐局文件的官方公开下载返回配额错误，备用来源也未取得可核验的全年文件。\n- 原有部分赛事目录与比分表的小局数差异仍未解决，见[原数据说明](../../docs/DATA.md)。本轮不以不完整镜像覆盖原结果。\n- 相邻日期、跨午夜系列赛拆分和比分冲突一律隔离，不靠猜测合并。尚未证明每个隔离条目代表源数据错误。\n- 历史镜像存在回溯更名和字符编码问题；别名仅在明确赛季映射，不能当作当年的官方队名或跨年实力继承。\n- 新字段暂不进入预测；全局 BP、换人、选边和版本效应仍未建模。局内统计只能在未来实验中以赛前历史摘要使用。\n\n## 逐局记录与来源\n'
 for a in aa:
  season=a['season'];maps=read(R/f'data/enrichment/S{season}_maps.json');audit=read(R/f'data/enrichment/S{season}_audit.json');changes=read(R/f'data/enrichment/S{season}_lineup_changes.json')
  s+=f'\n- [S{season} 逐局核验与阵容记录](S{season}.md)'
  if a['source_url']:s+=f'；[来源]({a["source_url"]})'
  text=f'# S{season}：补充逐局记录\n\n[覆盖审计](README.md)\n\n来源最晚记录：{a["source_latest_date"]}。阵容顺序按源角色记录；经济和资源数值为该局赛后信息，不用于该局赛前预测。缺失用“—”，不当成零。\n'
  text+=table(['日期时间','蓝方','红方','比分','版本','核验状态','蓝方阵容','红方阵容','15分钟经济差（蓝／红）','小龙（蓝／红）','大龙（蓝／红）'],[[m['timestamp'],m['team1'],m['team2'],f"{m['wins1']}:{m['wins2']}",m['patch'] or '—','通过' if m['reconciliation']=='matched' else '隔离','、'.join(p['playername'] or '—' for p in m['players']['Blue']),'、'.join(p['playername'] or '—' for p in m['players']['Red']),*[ '/'.join(m['stats'][side][k] or '—' for side in ['Blue','Red']) for k in ['golddiffat15','dragons','barons']]] for m in sorted(maps,key=lambda m:m['timestamp'])])
  text+='## 观察到的阵容变化\n\n仅比较相邻已核验样本；间隔内可能存在未收集的比赛和阵容变化。\n'
  text+=table(['队伍','此前观察','随后观察','此前选手标识','随后选手标识'],[[c['team'],c['previous_observed'],c['next_observed'],'、'.join(c['previous_players']),'、'.join(c['next_players'])] for c in changes])
  text+='## 隔离记录\n'+table(['日期','赛区／赛事标签','队伍','原因'],[[c['date'],c['league'],' / '.join(c['teams']),'附近已有比分但无法唯一核准' if c['reason'].startswith('nearby') else '国际赛事阶段与资格未核准'] for c in audit['conflicts']])
  if audit['rejected']:text+=f'另有 {len(audit["rejected"])} 局因未知队名或结构问题未进入规范化表，不计作补齐；其中可能含次级或资格赛队伍。\n'
  write(R/f'reports/data_enrichment/S{season}.md',text)
 write(R/'reports/data_enrichment/README.md',s)

def s16_report():
 states=read(RES/'s16_states.json')['states'];base=read(R/'results/simulation_raw.json');models={'regional90':base,**{m:read(RES/m/'2026_Worlds.json') for m in states}}
 for model,raw in models.items():
  n=raw['simulations'];assert n==14_000_605 and raw['seed']==2026
  assert [sum(c[i] for c in raw['counts']) for i in range(5)]==[n,16*n,8*n,4*n,2*n]
  assert all(0<=c[0]<=c[4]<=c[3]<=c[2]<=c[1]<=n for c in raw['counts'])
  body=f'# S16：队伍排名与晋级概率（{NAMES[model]}）\n\n[模型比较](../sensitivity/candidate_models.md) · [S16 主结果](README.md)\n\n按夺冠概率排序，使用截至 **2026 年 10 月 14 日** 的赛果，参考日为 **10 月 19 日**。各列为从赛事开始算起的累计晋级概率，不是晋级后下一轮的条件胜率。\n'
  body+=table(['排名','队伍','进入瑞士轮','进入八强','进入四强','进入决赛','夺冠'],[[i,t,*[pct(c[j]/n) for j in [1,2,3,4,0]]] for i,(t,c) in enumerate(sorted(zip(WORLD_TEAMS,raw['counts']),key=lambda x:-x[1][0]),1)])
  body+='概率为模拟估计；小于 0.01% 不代表不可能。未考虑全局 BP、赛季中换人、替补、选边、版本效应和系列赛内相关性。\n'
  if model!='regional90':body+='\n这是新候选的结果，尚未替换原主结果；具体方法见[模型细节](../../MODEL.md)。\n'
  if (R/'results/main_model.json').exists():
   body=body.replace('这是新候选的结果，尚未替换原主结果；具体方法见','这是当前主结果；具体方法见' if model=='dynamic90' else '这是敏感性对照结果；具体方法见')
  filename={'regional90':'advancement','hierarchical90':'advancement_hierarchical','dynamic90':'advancement_dynamic'}[model]
  write(R/f'reports/s16/{filename}.md',body)
 return models

def main():
 data_report();s16=s16_report();summary=read(RES/'summary.json');pred=read(RES/'predictions.json');states=read(RES/'event_configs.json');events={}
 for model,cc in states.items():
  ee=[]
  for c in cc:
   raw=read(RES/model/f'{c["id"]}.json');n=raw['samples'];assert n==14_000_605 and raw['seed']==c['year']
   theta=[c['strength'][t] for t in c['teams']];sr=rankdata(-np.round(theta,12));ps=[sum(k for lo,hi,k in bins if lo==hi==1)/n for bins in raw['counts']];cr=rankdata(-np.array(ps));actual=[sum(common_band(c,*c['actual_ranks'][t]))/2 for t in c['teams']];expected=[sum(sum(common_band(c,lo,hi))/2*k/n for lo,hi,k in bins) for bins in raw['counts']]
   champion=next(i for i,t in enumerate(c['teams']) if c['actual_ranks'][t]==[1,1]);favorite=int(np.argmax(ps));ee.append(dict(id=c['id'],champion=c['display'][c['teams'][champion]],favorite=c['display'][c['teams'][favorite]],hit=champion==favorite,champion_probability=ps[champion],champion_brier=sum((p-int(i==champion))**2 for i,p in enumerate(ps)),champion_logloss=-math.log(ps[champion]) if ps[champion]>0 else None,strength_correlation=correlation(sr,actual),title_correlation=correlation(cr,actual),finish_correlation=correlation(expected,actual)))
   body=f'# {c["year"]} {c["event"]}：{NAMES[model]}\n\n[比较总览](../candidate_models.md) · [赛制与主结果](../../event_replay/{c["id"]}.md)\n\n采用与原结果相同的赛制情景，部分旧同分及抽签规则仍有近似。实力在开赛前冻结；排名按共同淘汰阶段比较。\n'
   reg=region_rankings([dict(name=c['display'][t],region=c['regions'][t],strength=c['strength'][t],title_probability=ps[i]) for i,t in enumerate(c['teams'])]);body+=section(reg)
   body+=table(['队伍','实力排名','夺冠概率排名','夺冠概率','实际阶段名次','预期阶段名次'],[[c['display'][c['teams'][i]],f'{sr[i]:g}',f'{cr[i]:g}',pct(ps[i]),band(common_band(c,*c['actual_ranks'][c['teams'][i]])),f'{expected[i]:.2f}'] for i in sorted(range(len(ps)),key=lambda i:-ps[i])])
   e=ee[-1];body+=f"实际冠军 **{e['champion']}**；预测冠军 **{e['favorite']}**。实力排名、夺冠概率排名和预期名次与实际成绩的相关系数分别为 {e['strength_correlation']:.3f}、{e['title_correlation']:.3f}、{e['finish_correlation']:.3f}。\n" if e['strength_correlation'] is not None else '部分实力并列，相关系数无法定义。\n'
   write(OUT/model/f'{c["id"]}.md',body)
  events[model]=ee
 original=read(R/'results/event_replay/summary.json');events['regional90']=[dict(id=e['id'],champion=e['champion'],favorite=e['probability_favorite'],hit=e['favorite_hit'],champion_probability=e['champion_title_probability'],champion_brier=e['champion_brier'],champion_logloss=e['champion_logloss'],strength_correlation=e['strength_rank_correlation'],title_correlation=e['probability_rank_correlation'],finish_correlation=e['expected_finish_correlation']) for e in original['events']]
 write(RES/'event_summary.json',json.dumps(events,ensure_ascii=False,indent=2))
 body='# 新模型比较：逐场预测与整届结果\n\n[返回首页](../../README.md) · [数据补充与缺口](../data_enrichment/README.md) · [算法细节](../../MODEL.md)\n\n**本轮逐场比较中，新分层模型表现最好；动态模型也优于原模型，但没有进一步超过新分层模型。** 三者使用同一批胜负输入。逐局字段已补充，尚未作为预测变量；未因此宣称补齐所有历史赛程。\n\n## 逐场表现\n\nS4–S15，共 1,300 场系列赛、1,965 小局；S3 不回放。同日赛果不用于当日预测。概率为 50% 时按半次命中计分。对数损失和 Brier 越低越好。\n'
 body+=table(['模型','系列赛命中率','小局命中率','系列赛对数损失','小局对数损失','小局 Brier'],[[NAMES[m],pct(v['series_accuracy']),pct(v['map_accuracy']),f"{v['series_logloss']:.4f}",f"{v['map_logloss']:.4f}",f"{v['map_brier']:.4f}"] for m,v in summary['aggregate'].items()])
 body+='## 整届冠军与排名\n\n每个候选每届独立模拟，种子为年份；沿用旧赛制近似，所以这是相同规则情景下的比较。冠军命中率不是逐场命中率。\n'
 body+=table(['模型','冠军预测命中','实际冠军平均概率','冠军对数损失','冠军 Brier','平均预期名次相关性'],[[NAMES[m],f'{sum(e["hit"] for e in ee)}/{len(ee)}',pct(np.mean([e['champion_probability'] for e in ee])),f'{np.mean([e["champion_logloss"] for e in ee]):.4f}',f'{np.mean([e["champion_brier"] for e in ee]):.4f}',f'{np.mean([e["finish_correlation"] for e in ee if e["finish_correlation"] is not None]):.3f}'] for m,ee in events.items()])
 body+='## 逐届对照\n\n每个单元格为该届实际冠军的赛前夺冠概率；链接内有全体参赛队实力排名、夺冠概率、赛前赛区排名和实际名次。\n'
 body+=table(['赛事','实际冠军','原模型','新分层模型','动态模型'],[[e['id'],e['champion'],pct(e['champion_probability']),*[f'[{pct(next(x for x in events[m] if x["id"]==e["id"])["champion_probability"])}]({m}/{e["id"]}.md)' for m in ['hierarchical90','dynamic90']]] for e in events['regional90']])
 body+='## 分赛季逐场命中率\n'+table(['赛季','原模型','新分层模型','动态模型'],[[f'S{x["season"]}',*[pct(x['models'][m]['series_accuracy']) for m in NAMES]] for x in summary['by_season']])
 body+='## S16 排名与过关概率\n\n- [新分层模型](../s16/advancement_hierarchical.md)\n- [动态模型](../s16/advancement_dynamic.md)\n- [原模型](../s16/advancement.md)\n\nS16 尚无最终成绩，不能用它判断哪个模型更准确。原主结果保留，本页为候选比较。\n\n## 如何理解改善\n\n两个候选均采用更强收缩，动态模型另加入状态随时间变化；目前没有只改变一项的完整消融实验，不能把收益完全归因于层级结构或动态更新。只有 23 届赛事，且多个赛季共享参赛队和数据缺口；当前差异是历史描述，不是已经证明稳定的未来优势。参数未按本次结果挑选，但本项目此前已多次审视这些年份，仍需后续独立赛事验证。\n\n完整逐场明细：\n'
 for season in range(4,16):
  pp=[r for r in pred if r['season']==season];body+=f'\n- [S{season} 三模型逐场预测](candidate_predictions/S{season}.md)'
  pbody=f'# S{season}：逐场预测对照\n\n[比较总览](../candidate_models.md)\n\n所有概率均为左侧队伍获胜概率；BO3／BO5 系列赛概率由小局概率换算。\n'
  pbody+=table(['日期','赛事','对阵','实际比分','赛制','原模型小局','分层小局','动态小局','原模型系列赛','分层系列赛','动态系列赛'],[[r['date'],r['event'],r['display1']+' / '+r['display2'],f'{r["wins1"]}:{r["wins2"]}',f'BO{r["best_of"]}',*[pct(r[m]) for m in NAMES],*[pct(float(series_probability(r[m],r['best_of']))) for m in NAMES]] for r in pp])
  write(OUT/'candidate_predictions'/f'S{season}.md',pbody)
 if (R/'results/main_model.json').exists():
  body=body.replace('原主结果保留，本页为候选比较。','现主结果采用动态模型，原模型和静态分层模型保留为对照。')
 write(OUT/'candidate_models.md',body)
 print({m:dict(hits=sum(e['hit'] for e in ee),logloss=np.mean([e['champion_logloss'] for e in ee])) for m,ee in events.items()})
if __name__=='__main__':main()

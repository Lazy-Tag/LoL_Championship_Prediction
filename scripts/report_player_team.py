"""Reader reports for source-identified player skills and team residuals."""
import json
from collections import defaultdict
import numpy as np
from run_player_team import R,D,MODES
from report_chain_events import evaluate
from report_event_replay import table,band
from region_rankings import region_rankings,section
from backtest import load_season
P=R/'reports/player_team';LABEL={'baseline':'原动态模型','player_reset':'选手＋团队，每季重置','player_carry':'选手能力跨季继承'}
def main():
 display={}
 for season in range(10,16):
  rows,_=load_season(season)
  for row in rows:
   for k in ('1','2'):display[row['team'+k]]=row['display'+k]
 scopes={'all1300':'全部历史目标','identified_seasons':'2020–2025','both_recent_lineups':'双方有近期名单'}
 P.mkdir(exist_ok=True);cs=json.loads((D/'event_configs.json').read_text());protocol=json.loads((D/'protocol.json').read_text());reg=json.loads((D/'identity_registry.json').read_text());pred=json.loads((D/'predictions.json').read_text());components=json.loads((D/'event_components.json').read_text());events=[]
 for i,c in enumerate(cs[MODES[0]]):
  models={}
  for m in LABEL:
   conf=c if m=='baseline' else cs[m][i];path=R/f'results/model_experiments/dynamic90/{c["id"]}.json' if m=='baseline' else D/m/f'{c["id"]}.json';models[m]=evaluate(conf,json.loads(path.read_text()))
  e=dict(id=c['id'],year=c['year'],fallback=bool(c.get('fallback')),models=models);events.append(e)
  text=f'# {c["id"]}：选手能力与团队残差\n\n[总览](README.md) · [逐届赛制与局限](../event_replay/rules.md)\n\n赛前截点：{c["start_date"]}。每个候选14,000,605次，独立种子{c["year"]}。原逐届规则近似保留，整届冻结赛前状态。\n\n'
  if e['fallback']:text+='**本届缺少可用的持久选手ID，两候选均回退原模型，不能作为选手模型有效性的证据。**\n\n'
  text+=table(['队伍','实际名次',*[LABEL[m]+'夺冠概率' for m in LABEL],*[LABEL[m]+'预期名次' for m in LABEL]],[[t['name'],band(t['actual_rank']),*[f'{models[m]["teams"][j]["championship_probability"]:.3%}' for m in LABEL],*[f'{models[m]["teams"][j]["expected_rank"]:.3f}' for m in LABEL]] for j,t in enumerate(models['baseline']['teams'])])
  if not e['fallback']:
   for m in MODES:
    conf=cs[m][i];text+=f'\n## {LABEL[m]}：赛前赛区排名\n\n'+section(region_rankings([dict(name=conf['display'][t],region=conf['regions'][t],strength=conf['strength'][t],title_probability=models[m]['teams'][j]['championship_probability']) for j,t in enumerate(conf['teams'])]))
   text+='\n## 跨季候选的实力构成\n\n以下为模型内部相对尺度，不是选手客观能力评分；团队项也包含组织、教练和未解释因素，不能单独解释为已测得配合。阵容为较早观察日的出场份额，未偷看本届真实首发。\n\n'
   rows=[r for r in components if r['event_id']==c['id'] and r['model']=='player_carry']
   text+=table(['队伍','最近可用名单日期','赛区项','团队残差','选手／未知阵容项','合计'],[[r['name'],r['lineup_date'] or '缺失',*[f'{r["components"][k]:+.4f}' for k in ['region','team_residual','player_or_unknown_component','total']]] for r in rows])
   text+=table(['队伍','选手名称（来源历史名称）','位置','阵容份额','能力均值','后验标准差'],[[r['name'],' / '.join(reg[p['player_role'].split('|')[0]]['names']),p['player_role'].split('|')[1],f'{p["share"]:.1%}',f'{p["mean"]:+.4f}',f'{p["sd"]:.4f}'] for r in rows for p in r['players']])
  (P/f'{c["id"]}.md').write_text(text.rstrip()+'\n')
 keys=['champion_logloss','champion_brier','champion_hit','finish_spearman','finish_mae'];summary={}
 for scope,ee in [('all23',events),('identified12',[e for e in events if not e['fallback']])]:summary[scope]={m:{k:float(np.mean([e['models'][m][k] for e in ee])) for k in keys} for m in LABEL}
 series={}
 for scope,rr in [('all1300',pred),('identified_seasons',[r for r in pred if not r['fallback']]),('both_recent_lineups',[r for r in pred if all(r['known_lineups'])])]:
  series[scope]={}
  for m in LABEL:
   p=np.clip([r['probabilities'][m] for r in rr],1e-12,1-1e-12);y=np.array([r['wins1']>r['wins2'] for r in rr],float);series[scope][m]=dict(n=len(rr),accuracy=float(np.mean(np.where(abs(p-.5)<1e-12,.5,(p>.5)==y))),logloss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),brier=float(np.mean((p-y)**2)))
 diagnostics={};rng=np.random.default_rng(2026)
 for scope,ee in [('all23',events),('identified12',[e for e in events if not e['fallback']])]:
  years=sorted({e['year'] for e in ee});ix=rng.integers(0,len(years),(10000,len(years)));diagnostics[scope]={}
  for m in MODES:
   diagnostics[scope][m]={}
   for k in keys:
    delta=np.array([e['models'][m][k]-e['models']['baseline'][k] for e in ee]);groups=np.array([[sum(delta[i] for i,e in enumerate(ee) if e['year']==y),sum(e['year']==y for e in ee)] for y in years]);z=groups[ix].sum(axis=1)
    diagnostics[scope][m][k]=dict(delta=float(np.mean(delta)),year_cluster_95=np.quantile(z[:,0]/z[:,1],[.025,.975]).tolist(),leave_one_out_range=[float(min((sum(delta)-v)/(len(delta)-1) for v in delta)),float(max((sum(delta)-v)/(len(delta)-1) for v in delta))])
 result=dict(summary=summary,series=series,events=events,diagnostics=diagnostics);(D/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 text='# 选手能力＋团队配合：独立模型实验\n\n两候选使用相同小局结果、赛前截点和逐届赛制情景。每届14,000,605次，随机种子为公历年份。主模型、S16赛前快照和赛中报告均未覆盖。\n\n'
 for scope,title,n in [('all23','全部23届，含11届原模型回退',23),('identified12','2020–2025的12届：实际启用选手模型',12)]:
  text+='## '+title+'\n\n'+table(['模型','冠军命中','冠军对数损失 ↓','冠军 Brier ↓','名次相关 ↑','名次绝对误差 ↓'],[[LABEL[m],f'{summary[scope][m]["champion_hit"]*n:g}/{n}',*[f'{summary[scope][m][k]:.5f}' for k in ['champion_logloss','champion_brier','finish_spearman','finish_mae']]] for m in LABEL])
 text+='**结论：本版改善主要体现在名次绝对误差，尚不足以替换冠军预测主模型。** 12届中，每季重置版名次误差1.82983→1.81080，跨季版为1.81307；冠军命中均3/12，冠军对数损失均略差。冠军Brier略好，但差异区间跨零。每季重置版名次误差的年份区间为负，只有6个年份且经过多轮探索，仍需未来赛事验证。跨季继承没有比重置版进一步改善。\n\n双方都有近期名单的428场中，原对数损失0.54882，选手重置0.55386、跨季0.55411；这一版的问题不能只归因于名单缺失。个人与团队贡献的可识别性、固定方差拆分、首次核准阵容时匿名能力与个人能力的衔接，仍是下一步需要分别检验的假设，尚未证明这些调整会提升。\n\n早期11届没有可靠的持久选手标识，两候选与原模型完全相同。不能把这部分重复结果当作选手模型的新增验证证据；12届子集按身份数据可用性事先确定，不按预测好坏筛选。\n\n## 模型实际改变了什么\n\n实力拆为赛区项、队伍残差和五名选手能力。选手按来源ID及位置建立状态；同位置转会可以携带已学能力，团队残差留在原队。跨季候选继续保留选手联合均值与协方差并按90天衰减，团队残差和赛区先验按原季节协议重新初始化。重置候选只在当季跨队传递选手能力，下一季清零，作为隔离跨季继承效应的对照。\n\n团队残差是配合、组织环境和其他未解释因素的合并项，**不是已分离估计的双人协作或五人化学反应**。长期共同出场时，选手贡献与队伍残差难以区分，因此依赖固定高斯约束；数值不能用于断言某选手的客观能力排名。\n\n此前45天内最近一个完整名单观察日用于赛前阵容预测，按当天实际出场份额平均；当天名单只在当天全部预测后才更新。未知阵容使用独立队伍匿名项，不把旧名单默认为真实首发；整届预测不使用后来公布的首发或换人。\n\n## 身份与位置覆盖\n\n2020年起原OE归档有`oe:player:…`来源持久标识，本轮逐局核对来源ID、位置、名字和原完整比分。更早的数字playerid只是对局席位，不当个人ID。不同来源ID即使同名也不合并；同一来源ID可保留多个历史名字，未独立证实来源库中每一个改名。位置变化启用新位置状态，未假定跨位置能力完全相同。\n'
 text+=table(['赛季','原训练小局','有详细数据并对账','身份完整可训练小局','身份完整系列赛','选手－位置状态数'],[[f'S{x["season"]}',x['training_maps'],x['matched_maps'],x['usable_maps'],x['verified_series'],x['player_role_states']] for x in protocol['coverage']])
 text+='一场系列赛只有全部小局身份可核准，才拆为逐局训练；否则保留原系列赛比分一次，使用匿名阵容项。没有增加新胜负样本。各队最新名单的可用性可能不同，不能将归档覆盖当作每场预测都知道首发。\n\n## 逐场辅助评价\n'
 text+=table(['范围','模型','场数','命中率','对数损失','Brier'],[[scopes[scope],LABEL[m],series[scope][m]['n'],f'{series[scope][m]["accuracy"]:.2%}',f'{series[scope][m]["logloss"]:.5f}',f'{series[scope][m]["brier"]:.5f}'] for scope in series for m in LABEL])
 text+='“双方有近期名单”指双方均有此前45天内完整名单的共同子集。后者按预测前可用性确定，不按结果挑选。\n\n## 12届子集的差异区间\n\n候选减原模型；损失与误差负值较好。按年份聚类，只有6个年份，区间仅作探索性描述。删除任意一届只作影响诊断，不移除主评价样本。\n'
 text+=table(['候选','指标','平均差','95%年份区间','删除一届后的平均差范围'],[[LABEL[m],k,f'{diagnostics["identified12"][m][k]["delta"]:+.5f}',str([round(v,5) for v in diagnostics['identified12'][m][k]['year_cluster_95']]),str([round(v,5) for v in diagnostics['identified12'][m][k]['leave_one_out_range']])] for m in MODES for k in ['champion_logloss','champion_brier','finish_mae']])
 text+='## 逐届结果\n'+table(['赛事','实际冠军','原冠军概率','选手每季重置','选手跨季继承','身份模型启用'],[[f'[{e["id"]}]({e["id"]}.md)',e['models']['baseline']['champion'],*[f'{e["models"][m]["champion_probability"]:.3%}' for m in LABEL],'否，原模型回退' if e['fallback'] else '是'] for e in events])
 text+='## 仍未覆盖\n\n没有加入经济、选边、全局BP、英雄消耗、版本适应、位置重要性学习或显式双人协作项。选手与团队统一90天记忆，方差拆分事先固定，没有按23届结果优化。预测冻结赛前均值，未对全部参数不确定性积分；历史赛制近似保持原实现。S16新数据没有倒填历史，也未用本轮结果覆盖S16预测。\n\n[来源身份表](identities.md) · [身份隔离记录](rejected.md) · [跨季迁移表](transports.md) · [逐场概率](matches.md) · [模型细节与复算](../../MODEL.md#选手能力与团队残差模型)\n'
 (P/'README.md').write_text(text.rstrip()+'\n')
 text='# 来源选手身份与位置\n\n同名不同来源ID不合并；同ID多个名字仅按来源关系保留，不能解释为已独立核实全部更名。下面只列实际通过小局身份对账的记录。\n\n'+table(['来源ID','历史名字','位置','赛季','出现队伍','首次观察','末次观察'],[[pid,' / '.join(x['names']),', '.join(x['roles']),', '.join('S'+str(v) for v in x['seasons']),', '.join(display.get(t,t) for t in x['teams']),x['first'],x['last']] for pid,x in sorted(reg.items(),key=lambda v:v[1]['names'])]);(P/'identities.md').write_text(text.rstrip()+'\n')
 text='# 跨赛季选手能力迁移\n\n只迁移同来源ID、同位置的能力及联合协方差。以下系数为休赛期状态转移，不是旧赛果的最终精确权重；跨季连续转移自然相乘，当季赛果仍会更新能力。\n\n'+table(['赛季','名字','位置','上季末滤波日','新季首日','时间继承系数'],[[f'S{x["season"]}',' / '.join(reg[x['player_role'].split('|')[0]]['names']),x['player_role'].split('|')[1],x['previous_date'],x['start_date'],f'{x["coefficient"]:.3%}'] for x in json.loads((D/'transports.json').read_text())]);(P/'transports.md').write_text(text.rstrip()+'\n')
 text='# 选手模型逐场系列赛概率\n\n左队获胜概率；“名单可用”只指预测前45天内有完整观察，并非已核实当日首发。\n\n'+table(['日期','赛事','对阵','实际比分','双方名单可用',*LABEL.values()],[[r['date'],r['event'],r['team1']+' – '+r['team2'],f'{r["wins1"]}:{r["wins2"]}','／'.join('有' if v else '缺' for v in r['known_lineups']),*[f'{r["probabilities"][m]:.3%}' for m in LABEL]] for r in pred]);(P/'matches.md').write_text(text.rstrip()+'\n')
 rejected=json.loads((D/'rejected_identities.json').read_text())
 text='# 身份无法完整核准的小局\n\n这些记录未用于选手身份训练；对应系列赛仍以原比分和匿名阵容项进入一次，不删除其胜负。\n\n'+table(['赛季','日期','小局标识','原因'],[[f'S{x["season"]}',x['date'],x['game_id'],'持久ID、位置布局或来源名字缺失／冲突'] for x in rejected]);(P/'rejected.md').write_text(text.rstrip()+'\n')
 names=defaultdict(set)
 for pid,x in reg.items():
  for name in x['names']:names[name.casefold()].add(pid)
 ambiguous={k:sorted(v) for k,v in names.items() if len(v)>1}
 text=(P/'identities.md').read_text()+'\n## 同名但来源ID不同：保持分离\n\n'+table(['规范名字','不同来源ID'],[[name,', '.join(ids)] for name,ids in sorted(ambiguous.items())]);(P/'identities.md').write_text(text.rstrip()+'\n')
 print(json.dumps(summary,ensure_ascii=False,indent=2));print('series',series)
if __name__=='__main__':main()

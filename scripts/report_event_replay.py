"""Reader reports for frozen pre-event simulations; distinguish rule scenarios."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.stats import rankdata, spearmanr
from region_rankings import region_rankings, order_text, section

R=Path(__file__).resolve().parents[1]
N=14_000_605

def pct(x): return f'{100*x:.4f}%'
def table(head, rows):
    return '\n| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(str(x).replace('|','\\|') for x in row)+' |\n' for row in rows)+'\n'
def band(x):return str(x[0]) if x[0]==x[1] else f'{x[0]}–{x[1]}'
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.rstrip()+'\n')
def correlation(a,b):
    if len(set(a))<2 or len(set(b))<2:return None
    return float(spearmanr(a,b).statistic)
def fmt(x):return '无信息' if x is None else f'{x:.3f}'
def common_band(c,lo,hi):
    # Compare only elimination stages consistently encoded on both sides.
    # Old group bottom places/prize ties are not fully reproduced by the engine.
    if c['event']=='Worlds' and c['year']<=2022:
        if lo>=17:return (17,len(c['teams']))
        if lo>=9:return (9,14 if c['year']==2013 else 16)
    if c['event']=='MSI' and c['year']<=2022:
        if lo>=7:return (7,len(c['teams']))
        if lo>=5:return (5,6)
    if c['event']=='MSC' and lo>=5:return (5,8)
    return lo,hi

def assumptions(c):
    items=['赛前冻结实力，赛事进行中不更新；小局独立，未考虑全局 BP、换人、替补、选边、版本及状态关联。',
           '按历史对局元数据重建预定分组与开局签表，缺少逐届赛前抽签公告的完整时间戳存档；不是当时实际发布过的预测。']
    if c['kind'] in ['worlds2013','worlds_groups','msi_old','msi_rumble','msc']:
        items+=['循环赛同分采用通用交手优先、加赛及随机时长种子的处理。四队及以上同分使用逐次淘汰排序情景，未逐届精确还原官方细则；部分两队、三队同分处理同样存在差异。',
                '旧分组赛事的出局队名次统一按淘汰阶段合并后比较，避免把未建模的组内低名次和奖金并列当作准确最终排序。']
    if c['event']=='Worlds' and 2020<=c['year']<=2022:
        items+=['入围赛两队同分仍采用通用交手优先规则，可能不同于实际要求的加赛；这会影响晋级与夺冠概率。']
    if c['year']==2013:items+=['赛前训练赛果为 0，所有队伍实力相同；概率差异主要来自直通八强与赛程。八强抽签采用直通队对晋级队的随机配对，未完成原始抽签细则核验。']
    if c['year']==2014:items+=['早期国内赛果缺口较大，赛前实力估计的信息基础不足。']
    if c['event']=='MSI' and 2017<=c['year']<=2022:items+=['小组第一选择半决赛对手时，假设选择冻结实力较弱者，没有使用未来实际选择。']
    if c['kind']=='msi_double':items+=['按当届种子池和同赛区避让条件生成合法签表，均匀抽取合法签表；未证明与官方逐签顺延过程的概率分布完全相同。']
    if c['kind']=='worlds_swiss':items+=['2023 瑞士轮允许重赛，2024、2025 禁止重赛；随机抽出顺序后按可完成合法配对的最早空位安排，裁判裁量不在模型内。']
    if c['event']=='MSC':items+=['没有单独模拟淘汰赛首局盲选，所有小局共用同一胜率。']
    return items

FORMATS={
'worlds2013':'两组五队双循环；前二与四支直通队进入八强；八强 BO3，其后 BO5。',
'worlds_groups':'主赛四组四队双循环，前二晋级；八强组一对另一半区组二，BO5 单败。',
'worlds_swiss':'入围赛后十六队瑞士轮，三胜晋级、三负淘汰；晋级/淘汰战 BO3，其余 BO1；八强 BO5 单败。',
'msi_old':'六队主赛循环前四进入 BO5 单败；2015 单循环，其余双循环；部分年份另有入围赛。',
'msi_rumble':'三组首轮取前二，六队对抗赛双循环取前四，再打 BO5 单败。',
'msi_double':'入围赛后八队 BO5 双败；总决赛不重置。',
'msc':'两组四队单循环，前二交叉进行 BO5 半决赛及决赛。'}
EXTRA={2017:'入围赛四组三队双循环，前二交叉 BO5，四队晋级。',2018:'入围赛四组三队双循环，前二交叉 BO5，四队晋级。',2019:'入围赛四组三队双循环，前二交叉 BO5，四队晋级。',2020:'入围赛两组五队单循环，第一直进，第三对第四胜者再对另一组第二。',2021:'入围赛两组五队单循环，第一直进，第三对第四胜者再对另一组第二。',2022:'入围赛两组六队单循环，第一直进，第三对第四胜者再对另一组第二；FNC/MAD 同时晋级时豁免 MAD 同区限制。',2023:'入围赛两组四队 BO3 双败，再交叉 BO5 决出两队；瑞士轮可重赛。',2024:'入围赛两组四队 BO3 双败，败者跨组决胜，四队晋级；瑞士轮禁重赛。',2025:'入围赛 T1–IG BO5 决出一队；瑞士轮三档种子，入围胜者所属赛区三号种子升档。'}
MSI_EXTRA={2017:'入围赛两组四队双循环，组一对两支轮空队，胜者晋级、败者再争最后席位；三队直通主赛。',2018:'入围赛两组四队双循环，组一对两支轮空队，仅两支胜者晋级；四队直通主赛。',2019:'入围赛两组四队双循环，固定 A 组对 NA、B 组对 LMS，败者再争最后席位；三队直通主赛。',2021:'首轮两个四队组双循环，一个三队组四循环。',2022:'首轮两个四队组双循环，一个三队组四循环。',2023:'两组四队 BO3 双败，两支上路胜者晋级，下路胜者 BO5 争第三席位。',2024:'两组四队 BO3 双败，每组晋级两队；主赛种子区分入围赛上路/下路胜者。',2025:'四队 BO5 双败入围赛晋级两队；主赛按固定种子池和同赛区分半区限制抽签。'}

def main():
    configs=json.loads((R/'data/event_replay/configs.json').read_text());events=[]
    for c in configs:
        raw=json.loads((R/f"results/event_replay/{c['id']}.json").read_text())
        assert raw['samples']==N and raw['seed']==c['year'] and raw['half_life_days']==90
        assert raw['engine_sha256']==hashlib.sha256((R/'scripts/event_simulation.cpp').read_bytes()).hexdigest()
        assert raw['input_sha256']==hashlib.sha256((R/f"data/event_replay/{c['id']}.txt").read_bytes()).hexdigest()
        assert sum(v[2] for bins in raw['counts'] for v in bins if v[:2]==[1,1])==N
        theta=[c['strength'][t] for t in c['teams']]
        sr=rankdata(-np.round(theta,12),method='average').tolist()
        probs=[sum(k for lo,hi,k in bins if lo==hi==1)/N for bins in raw['counts']]
        cr=rankdata(-np.array(probs),method='average').tolist()
        teams=[]
        for i,t in enumerate(c['teams']):
            bins=raw['counts'][i];assert sum(k for lo,hi,k in bins)==N
            actual=common_band(c,*c['actual_ranks'][t]);expected=sum(sum(common_band(c,lo,hi))/2*k/N for lo,hi,k in bins)
            merged={}
            for lo,hi,k in bins:
                b=common_band(c,lo,hi);merged[b]=merged.get(b,0)+k
            p=probs[i];z=1.959963984540054;den=1+z*z/N
            mid=(p+z*z/(2*N))/den;rad=z*math.sqrt(p*(1-p)/N+z*z/(4*N*N))/den
            teams.append(dict(team=t,name=c['display'][t],strength=theta[i],strength_rank=sr[i],title_rank=cr[i],title_probability=p,title_count=round(p*N),mc95=[max(0,mid-rad),min(1,mid+rad)],actual_band=list(actual),actual_midrank=sum(actual)/2,expected_stage_rank=expected,finish_distribution=[dict(band=list(b),count=k,probability=k/N) for b,k in sorted(merged.items())]))
        champ=next(t for t in teams if t['actual_band']==[1,1]);favorite=max(teams,key=lambda t:t['title_probability'])
        strength_favorites=[t for t in teams if abs(t['strength']-max(theta))<1e-12]
        e=dict(id=c['id'],season=c['season'],year=c['year'],event=c['event'],samples=N,seed=c['year'],half_life_days=90,champion=champ['name'],champion_title_probability=champ['title_probability'],champion_title_rank=champ['title_rank'],champion_strength_rank=champ['strength_rank'],probability_favorite=favorite['name'],favorite_hit=favorite['team']==champ['team'],strength_favorite_hit=(strength_favorites[0]['team']==champ['team']) if len(strength_favorites)==1 else None,strength_rank_correlation=correlation([t['strength_rank'] for t in teams],[t['actual_midrank'] for t in teams]),probability_rank_correlation=correlation([t['title_rank'] for t in teams],[t['actual_midrank'] for t in teams]),expected_finish_correlation=correlation([t['expected_stage_rank'] for t in teams],[t['actual_midrank'] for t in teams]),champion_brier=sum((t['title_probability']-int(t['team']==champ['team']))**2 for t in teams),champion_logloss=-math.log(champ['title_probability']) if champ['title_probability'] else None,teams=teams)
        e['region_rankings']=region_rankings([{**t,'region':c['regions'][t['team']]} for t in teams])
        events.append(e)
        title=f"S{c['season']}（{c['year']}）{c['event']}"
        body=f"# {title}：赛前预测与最终成绩\n\n[全部赛事对照](README.md) · [赛制与近似](rules.md) · [模型细节](../../MODEL.md)\n\n**部分旧赛制细节仍有近似，结果需结合限制阅读。** 完成 {N:,} 次。赛前可用成绩截至 {c['start_date']} 之前，共 {c['training_series']:,} 场系列赛、{c['training_maps']:,} 小局。\n\n实际冠军为 **{champ['name']}**，赛前实力排名 **{champ['strength_rank']:g}**，夺冠概率 **{pct(champ['title_probability'])}**，概率排名 **{champ['title_rank']:g}**。概率第一为 **{favorite['name']}**，本届{'命中' if e['favorite_hit'] else '未命中'}冠军。\n\n## 各队对照\n\n按夺冠概率排序。实力排名并列时取平均名次。实际成绩按统一淘汰阶段合并名次，具体口径见赛制说明；不是强行排出全部队伍先后。预期名次使用同样的合并口径。\n"
        body=body.replace('## 各队对照',section(e['region_rankings'])+'## 各队对照',1)
        ordered=sorted(teams,key=lambda t:-t['title_probability'])
        body+=table(['队伍','实力排名','夺冠概率排名','夺冠概率','95% 抽样区间','实际阶段名次','预期阶段名次'],[[t['name'],f"{t['strength_rank']:g}",f"{t['title_rank']:g}",pct(t['title_probability']),'–'.join(pct(v) for v in t['mc95']),band(t['actual_band']),f"{t['expected_stage_rank']:.2f}"] for t in ordered])
        body+=f"实力排名、夺冠概率排名、预期阶段名次与实际阶段名次的 Spearman 相关系数分别为 **{fmt(e['strength_rank_correlation'])}、{fmt(e['probability_rank_correlation'])}、{fmt(e['expected_finish_correlation'])}**。正值表示排序倾向一致，1 为完全一致；不是百分比正确率。区间仅反映蒙特卡洛抽样误差。\n\n## 最终阶段分布\n"
        bands=sorted({tuple(x['band']) for t in teams for x in t['finish_distribution']})
        body+=table(['队伍',*[band(b) for b in bands]],[[t['name'],*[pct(next((x['probability'] for x in t['finish_distribution'] if tuple(x['band'])==b),0)) for b in bands]] for t in ordered])
        body+='## 阅读提示\n\n部分旧同分与抽签细节仍有近似，未考虑全局 BP、换人、替补及系列赛内状态关联。[逐届赛制与限制](rules.md)列出具体处理和触发次数。\n'
        write(R/f"reports/event_replay/{c['id']}.md",body)
    unique=[e for e in events if e['strength_favorite_hit'] is not None]
    summary=dict(events=events,event_count=len(events),simulations_per_event=N,total_simulations=N*len(events),half_life_days=90,seed_policy='calendar year; independent reset per event',rule_status='scenario with disclosed historical rule approximations',favorite_hits=sum(e['favorite_hit'] for e in events),unique_strength_favorite_events=len(unique),strength_favorite_hits=sum(e['strength_favorite_hit'] for e in unique),mean_champion_probability=float(np.mean([e['champion_title_probability'] for e in events])),mean_champion_brier=float(np.mean([e['champion_brier'] for e in events])),mean_champion_logloss=float(np.mean([e['champion_logloss'] for e in events])) if all(e['champion_logloss'] is not None for e in events) else None)
    write(R/'results/event_replay/summary.json',json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False))
    body=f"# S4–S15：赛前排名、夺冠概率与实际成绩\n\n[返回首页](../../README.md) · [逐届规则与限制](rules.md) · [模型细节](../../MODEL.md)\n\n**概率最高的队伍命中 {summary['favorite_hits']}/{len(events)} 届冠军（{100*summary['favorite_hits']/len(events):.2f}%）。** 这是当前实现规则下的回放结果；旧同分规则和部分抽签分布仍有近似，不能当作完全还原官方规则后的准确率。\n\n{len(events)} 届 MSI／MSC／Worlds，每届 **14,000,605 次**，合计 **{N*len(events):,} 次**。各赛事预测只使用开赛前已知成绩。\n\n## 排名是否一致？\n\n- 夺冠概率第一命中：**{summary['favorite_hits']}/{len(events)}**。\n- 唯一实力第一命中：**{summary['strength_favorite_hits']}/{len(unique)}**；S4 三队并列第一不计入该项；S3 因赛前数据不足，整届不回放。\n- 实际冠军的平均赛前夺冠概率：**{pct(summary['mean_champion_probability'])}**。\n- 冠军多分类 Brier 平均值：**{summary['mean_champion_brier']:.4f}**（各队误差平方求和，越低越好）；平均对数损失：**{fmt(summary['mean_champion_logloss'])}**。\n\n实力最强不必然夺冠，概率第一也不必然是实力第一；不同种子与赛程会改变夺冠机会。这里的整届冠军命中率与逐场系列赛胜负命中率是不同指标。{len(events)} 届样本较少，且共享数据来源和模型假设，不宜把汇总当作稳定的未来命中保证。\n\n## 逐届冠军预测\n"
    body+=table(['赛事','实际冠军','冠军实力排名','冠军概率排名','冠军夺冠概率','预测冠军','命中'],[[f"[{e['year']} {e['event']}]({e['id']}.md)",e['champion'],f"{e['champion_strength_rank']:g}",f"{e['champion_title_rank']:g}",pct(e['champion_title_probability']),e['probability_favorite'],'✓' if e['favorite_hit'] else '✗'] for e in events])
    body+='## 各届国际赛前赛区实力排名\n\n仅比较各赛区本届参赛阵容；从左至右由强到弱，等号表示并列。\n'
    body+=table(['赛事','赛前赛区实力顺序'],[[f"[{e['year']} {e['event']}]({e['id']}.md)",order_text(e['region_rankings'])] for e in events])
    body+='## 全队排序与实际成绩的一致性\n\n各列为 Spearman 秩相关系数，使用并列平均名次。循环赛低名次和旧入围赛合并为共同淘汰阶段，避免未经核验的细分名次影响评价；因此衡量的是阶段排序一致性。没有把参赛队多的赛事加权为更多次冠军预测。\n'
    body+=table(['赛事','实力排名相关性','夺冠概率排名相关性','预期阶段名次相关性'],[[f"[{e['year']} {e['event']}]({e['id']}.md)",fmt(e['strength_rank_correlation']),fmt(e['probability_rank_correlation']),fmt(e['expected_finish_correlation'])] for e in events])
    body+='## 如何理解局限\n\nS3 因赛前数据不足，不纳入回放或汇总。S4 国内覆盖不足，其余年份也存在训练数据缺口。现有结果没有考虑全局 BP、赛季中换人、替补、选边、版本变化或系列赛内相关性。复杂同分和部分抽签仍用近似机制，14,000,605 次只能减少抽样误差，不能消除这些误差。逐届报告列出采用的赛制结构及近似触发次数。\n'
    write(R/'reports/event_replay/README.md',body)
    rules='# 历史赛事：赛制差异与比较口径\n\n[结果总览](README.md)\n\n## 比较的是什么\n\n本轮完整运行当前实现的逐届赛制情景，尚未完成所有年份的官方同分细则核验。冠军、亚军、四强和八强来自实际淘汰赛结果。为避免虚构低名次精度，2014–2022 Worlds 的主赛小组出局者合并为 9–16，入围赛出局者合并为 17–末位；2022 及以前 MSI 的主赛后两名合并为 5–6，入围赛出局者合并为 7–末位；MSC 小组出局者合并为 5–8。实际和模拟采用相同口径。现代瑞士轮与双败赛事保留战绩/淘汰轮次对应的名次区间。\n\n区间表示阶段并列，不是置信区间。计算相关性时使用区间中点；模拟预期名次按各阶段中点加权。每队所有阶段概率之和为 1。冠军 Brier 为所有队伍 (预测夺冠概率 − 是否实际冠军)² 之和；对数损失为 −log(实际冠军夺冠概率)。\n\n## 逐届实现\n'
    for c in configs:
        raw=json.loads((R/f"results/event_replay/{c['id']}.json").read_text())
        rules+=f"\n### {c['year']} {c['event']}\n\n"+FORMATS[c['kind']]+' '+(EXTRA.get(c['year'],'') if c['event']=='Worlds' else MSI_EXTRA.get(c['year'],'') if c['event']=='MSI' else '')+'\n\n'+'\n'.join('- '+x for x in assumptions(c))+f"\n\n[赛制参考]({c['source']})；复杂同分处理 {raw['complex_tie_scenarios']:,} 次，抽签豁免 {raw['draw_waivers']:,} 次。参考资料并不意味着所有细节已在代码中完整还原。\n"
    write(R/'reports/event_replay/rules.md',rules)
    print(json.dumps({k:v for k,v in summary.items() if k!='events'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()

if __name__ == "__main__" and (R/"results/main_model.json").exists():
    from publish_dynamic import main as publish_selected
    publish_selected()

"""Reader-facing reconciliation and prediction tables for detailed-data trial."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'results/detail_experiment';P=R/'reports/detailed_data'
def cell(x):return str(x).replace('|','\\|').replace('\n',' ')
def row(x):return '| '+' | '.join(map(cell,x))+' |\n'
def main():
    audits=json.loads((D/'reconciliation.json').read_text());pred=json.loads((D/'predictions.json').read_text());summary=json.loads((D/'summary.json').read_text())
    text='# 详细数据与原比分对账\n\n[数据总览](README.md) · [模型对比](model_comparison.md)\n\n本轮仅核对 S4–S15；S16 尚未用于新增特征回测。对账成功不等于15分钟经济非空。日期精确匹配，未自动平移时区或模糊合并队名；未匹配不等于原始赛果错误。\n\n'
    text+=row(['赛季','候选小局','对账通过','队名／日期未解析','同日比分未唯一匹配','重复来源组'])+row(['---']*6)
    for a in audits:
        c=a['counts'];s=a['season'];text+=row([f'[S{s}](reconciliation/S{s}.md)',c.get('candidate_maps',0),c['matched_maps'],c.get('unknown_name_or_date_maps',0),c.get('unmatched_or_ambiguous_maps',0),c.get('multiple_source_groups_maps',0)])
        q=P/'reconciliation';q.mkdir(exist_ok=True)
        body=f'# S{s} 未匹配比赛组\n\n[对账总览](../reconciliation.md)\n\n下列记录因同日队伍及整场小局比分不能唯一对应，未加入特征。队名使用赛季内规范化标识；无法解析队名或日期的记录仅在总览计数。\n\n'+row(['日期','赛事','队伍一','队伍二','小局数'])+row(['---']*5)
        for g in a['unmatched']:body+=row([g['date'],g['league'],*g['teams'],g['maps']])
        (q/f'S{s}.md').write_text(body)
    text+='\n## 逐场预测与实际结果\n\n胜率均为表中队伍一的系列赛胜率；详细数据覆盖表示双方此前各有至少5局经济记录。\n\n'
    from model import series_probability
    for s in range(4,16):
        q=P/'predictions';q.mkdir(exist_ok=True);text+=f'- [S{s}：逐场比较](predictions/S{s}.md)\n'
        body=f'# S{s} 新特征逐场比较\n\n[对账与评价总览](../reconciliation.md)\n\n胜率均指队伍一系列赛获胜概率。\n\n'+row(['日期','赛事','队伍一','队伍二','实际比分','原动态胜率','加经济胜率','加经济及红蓝方胜率','双方历史经济覆盖'])+row(['---']*9)
        for r in pred:
            if r['season']!=s:continue
            probs=[f'{series_probability(r[f],r["best_of"]):.2%}' for f in ['dynamic90','economy90','side_economy90']]
            body+=row([r['date'],r['event'],r['display1'],r['display2'],f'{r["wins1"]}:{r["wins2"]}',*probs,'是' if r['detailed_history_both'] else '不足'])
        (q/f'S{s}.md').write_text(body)
    (P/'reconciliation.md').write_text(text)
    path=P/'README.md';body=path.read_text().split('\n## 新特征回测')[0]
    path.write_text(body+'\n## 新特征回测\n\n[有没有提升：结果比较](model_comparison.md) · [模型方法](DETAIL_MODEL.md) · [对账明细及逐场预测](reconciliation.md)\n')
    path=P/'model_comparison.md';body=path.read_text()
    base=summary['all']['dynamic90'];new=summary['all']['side_economy90']
    conclusion=f'本轮没有提升：加入历史经济和红蓝方后，系列赛命中率由 {base["series_accuracy"]:.2%} 变为 {new["series_accuracy"]:.2%}，系列赛对数损失由 {base["series_logloss"]:.5f} 变为 {new["series_logloss"]:.5f}（越低越好）。保留原动态模型，不据此更新 S16 夺冠概率。这仅否定本轮简单增强方案，不能推断详细数据本身无用。'
    body=body.replace('[数据总览](README.md)', '[数据总览](README.md) · [对账与逐场明细](reconciliation.md)\n\n'+conclusion,1)
    path.write_text(body)
    print('Readable reconciliation and all 1,300 series predictions written.')
if __name__=='__main__':main()

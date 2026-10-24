"""Render inspected map records without changing prediction inputs."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/detailed'
REPORT = ROOT / 'reports/detailed_data'


def fmt(v):
    if v is None:
        return '—'
    if isinstance(v, float):
        return f'{v:g}'
    return str(v).replace('|', '\\|').replace('\n', ' ')


def row(values):
    return '| ' + ' | '.join(map(fmt, values)) + ' |\n'


def main():
    count = 0
    for season in range(3, 17):
        groups = defaultdict(list)
        for line in (DATA / f'S{season}_games.jsonl').read_text().splitlines():
            g = json.loads(line)
            if g['top_tier_candidate']:
                groups[g['league']].append(g)
        directory = REPORT / f'S{season}'
        directory.mkdir(exist_ok=True)
        index = '\n## 逐局明细\n\n经济单位为金币；差值均为蓝方减红方。“—”表示源数据缺失。候选范围尚未完成赛事阶段核验。\n\n'
        for league, games in sorted(groups.items()):
            slug = re.sub(r'[^A-Za-z0-9_-]', '_', league)
            name = slug + '.md'
            index += f'- [{league}：{len(games):,} 局](S{season}/{name})\n'
            text = f'# S{season} · {league} 逐局明细\n\n[赛季覆盖](../S{season}.md)\n\n'
            text += '尚未与原比分逐场对账，不能直接视为新增训练样本。经济单位为金币；差值为蓝方减红方；空缺保留为“—”。选手和英雄按上路、打野、中路、下路、辅助排列（以源角色字段为准）。\n\n'
            headers = ['日期', '小局标识', '蓝方', '红方', '胜者', '版本', '蓝方总经济', '红方总经济', '10分钟经济差', '15分钟经济差', '蓝／红击杀', '蓝／红小龙', '蓝／红大龙', '蓝方阵容（选手：英雄）', '红方阵容（选手：英雄）']
            text += row(headers) + row(['---'] * len(headers))
            for g in sorted(games, key=lambda x: (x['date'] or '', x['game_id'])):
                blue, red = (g['teams'][s] for s in ('blue', 'red'))
                b, r = blue['stats'], red['stats']
                def delta(k):
                    return b[k] - r[k] if b[k] is not None and r[k] is not None else None
                def pair(k):
                    return f'{fmt(b[k])} / {fmt(r[k])}'
                def lineup(team):
                    return '；'.join(f'{p["role"]} {p["name"] or "—"}：{p["champion"] or "—"}' for p in team['players'])
                text += row([g['date'], g['game_id'], blue['name'], red['name'], blue['name'] if blue['win'] else red['name'], g['patch'], b['totalgold'], r['totalgold'], delta('goldat10'), delta('goldat15'), pair('kills'), pair('dragons'), pair('barons'), lineup(blue), lineup(red)])
                count += 1
            (directory / name).write_text(text)
        timelines = [json.loads(x) for x in (DATA / f'S{season}_timelines.jsonl').read_text().splitlines()]
        if timelines:
            index += f'- [独立逐分钟经济：{len(timelines):,} 局](S{season}/timelines.md)\n'
            text = f'# S{season} · 独立逐分钟经济档案\n\n[赛季覆盖](../S{season}.md)\n\n缺精确比赛日期和版本；可能与 OE 逐局表重复。采样序号沿用源文件顺序，起始时间尚未核准，不能直接当作第 N 分钟。末次采样不保证等于结算经济。经济差为蓝方减红方。\n\n'
            text += row(['赛事', '赛段', '蓝方', '红方', '胜者', '采样点数', '蓝方末次经济', '红方末次经济', '逐点经济差']) + row(['---'] * 9)
            for g in timelines:
                gold = g['gold_series']
                assert g['blue_win'] + g['red_win'] == 1
                text += row([g['league'], g['split'], g['blue'], g['red'], g['blue'] if g['blue_win'] else g['red'], len(gold['golddiff']), gold['goldblue'][-1] if gold['goldblue'] else None, gold['goldred'][-1] if gold['goldred'] else None, ', '.join(map(str, gold['golddiff']))])
            (directory / 'timelines.md').write_text(text)
        path = REPORT / f'S{season}.md'
        base = path.read_text().split('\n## 逐局明细')[0]
        path.write_text(base + index if groups or timelines else base)
    errors = [(a['year'], e) for a in json.loads((DATA / 'audit.json').read_text()) for e in a['errors']]
    text = '# 逐局数据异常记录\n\n[覆盖总览](README.md)\n\n下列记录已从可用逐局统计中排除。重复行不等于真实重复比赛，仍需核对原始行后判断。\n\n'
    text += row(['年份', '小局标识', '原因']) + row(['---'] * 3)
    for year, e in errors:
        reason = '队伍行缺失或重复' if e['reason'] == 'missing/duplicate team rows' else '胜负值无效或不能互补'
        text += row([year, e['id'], reason])
    (REPORT / 'anomalies.md').write_text(text)
    overview = REPORT / 'README.md'
    body = overview.read_text()
    if '[异常记录]' not in body:
        overview.write_text(body + '\n[异常记录](anomalies.md)：9 条原始记录因队伍行或胜负字段异常被隔离。\n')
    print(f'Rendered {count:,} candidate maps and {len(errors)} excluded records; predictions unchanged.')


if __name__ == '__main__':
    main()

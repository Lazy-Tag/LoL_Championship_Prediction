# 数据补充与核验

[返回首页](../../README.md) · [模型比较](../sensitivity/candidate_models.md)

本轮增加逐局版本、时间、选边、选手阵容和经济／地图资源字段，并与已有系列赛比分对账。**没有新增获准进入训练的比赛结果**；两个新模型与原模型使用相同的胜负输入，因此预测差异来自模型，而非样本数量变化。

## 覆盖范围

2016–2022 的新增来源只含 Worlds，不能代表全年国内联赛；2025 来源覆盖多种联赛，筛除次级联赛和未核准的比赛。2026 现有镜像只更新到 6 月 21 日，且缺少最初下载链接，只作字段审计，不用于追加赛果。

| 赛季 | 可规范化小局 | 比分对账通过 | 原赛果小局 | 观察到的阵容变化 |
| --- | --- | --- | --- | --- |
| S6 | 77 | 49 | 2035 | 11 |
| S7 | 119 | 92 | 2899 | 19 |
| S8 | 119 | 109 | 3889 | 33 |
| S9 | 120 | 110 | 3651 | 10 |
| S10 | 114 | 110 | 3541 | 2 |
| S11 | 121 | 107 | 3684 | 5 |
| S12 | 155 | 132 | 3700 | 15 |
| S15 | 2606 | 2570 | 2609 | 281 |
| S16 | 1807 | 1762 | 2820 | 107 |

对账通过仅表示可唯一对应已有系列赛、双方和小局比分；不是逐字段经过官方核实。分母“原赛果小局”是该季全体已收集比赛，部分镜像只覆盖 Worlds，不能将这一比例当作全年源数据完整率。观察到的阵容变化是两次已采样阵容不同，不等于转会公告日期，也可能是临时替补。

## 字段覆盖

以下为规范化记录中字段非空的小局数，包含已隔离记录；实际可用记录还须通过比分核验。

| 赛季 | 版本 | 完整十人阵容 | 15 分钟经济差 | 小龙 | 大龙 |
| --- | --- | --- | --- | --- | --- |
| S6 | 77 | 77 | 77 | 77 | 77 |
| S7 | 119 | 119 | 119 | 119 | 119 |
| S8 | 119 | 119 | 119 | 119 | 119 |
| S9 | 120 | 120 | 120 | 120 | 120 |
| S10 | 114 | 114 | 114 | 114 | 114 |
| S11 | 121 | 121 | 121 | 121 | 121 |
| S12 | 155 | 155 | 141 | 155 | 155 |
| S15 | 2606 | 2606 | 1789 | 2606 | 2606 |
| S16 | 1807 | 1807 | 1354 | 1807 | 1807 |

## 仍未补齐的内容

- S4 早期国内赛果仍存在明显缺口；S3 继续不回放。2014–2024 全年逐局文件的官方公开下载返回配额错误，备用来源也未取得可核验的全年文件。
- 原有部分赛事目录与比分表的小局数差异仍未解决，见[原数据说明](../../docs/DATA.md)。本轮不以不完整镜像覆盖原结果。
- 相邻日期、跨午夜系列赛拆分和比分冲突一律隔离，不靠猜测合并。尚未证明每个隔离条目代表源数据错误。
- 历史镜像存在回溯更名和字符编码问题；别名仅在明确赛季映射，不能当作当年的官方队名或跨年实力继承。
- 新字段暂不进入预测；全局 BP、换人、选边和版本效应仍未建模。局内统计只能在未来实验中以赛前历史摘要使用。

## 逐局记录与来源

- [S6 逐局核验与阵容记录](S6.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2016_LoL_esports_match_data_from_OraclesElixir.csv)
- [S7 逐局核验与阵容记录](S7.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2017_LoL_esports_match_data_from_OraclesElixir.csv)
- [S8 逐局核验与阵容记录](S8.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2018_LoL_esports_match_data_from_OraclesElixir.csv)
- [S9 逐局核验与阵容记录](S9.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2019_LoL_esports_match_data_from_OraclesElixir.csv)
- [S10 逐局核验与阵容记录](S10.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2020_LoL_esports_match_data_from_OraclesElixir.csv)
- [S11 逐局核验与阵容记录](S11.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2021_LoL_esports_match_data_from_OraclesElixir.csv)
- [S12 逐局核验与阵容记录](S12.md)；[来源](https://raw.githubusercontent.com/ZD2525/Basic-Exploratory-Data-Analysis/main/2022_LoL_esports_match_data_from_OraclesElixir.csv)
- [S15 逐局核验与阵容记录](S15.md)；[来源](https://raw.githubusercontent.com/cbplexiglass/LoL-Esports-Regional-Analyses/main/2025_LoL_esports_match_data_from_OraclesElixir.csv)
- [S16 逐局核验与阵容记录](S16.md)

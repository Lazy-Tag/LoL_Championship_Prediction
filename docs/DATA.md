# 数据来源、范围与已知缺口

[返回首页](../README.md)

## 公开来源

- [Riot Worlds 2026 Primer](https://lolesports.com/en-GB/news/worlds-2026-primer) 与 [官方规则库](https://competitiveops.riotgames.com/en-US/library)。
- [Riot 公开赛程](https://lolesports.com/en-US/schedule)：2026 官方系列赛比分。
- [Games of Legends](https://gol.gg/tournament/list/)：独立赛事目录、系列赛比分及历史数据；逐场报告附来源链接。

## S16

统计覆盖 LPL、LCK、LEC、LCS、LCP、CBLOL 的全年已完成阶段及 First Stand、MSI、EWC 主赛与资格赛、美洲杯、DCGI。未纳入次级联赛、国家队赛事、非联赛性质的 KeSPA Cup 和混合层级升降级赛。

Riot 与 44 个 GOL 赛事比分表已对照。2026-08-01 GEN–DK 出现 GOL 1:1 与 Riot 0:2 冲突，采用官方 0:2。时间按系列赛日期近似，没有逐局开赛时刻。

## S4–S15 覆盖

S3/S4 国内联赛覆盖明显不足。来源赛季标签决定归属，未强行按自然年重新分组。目录和比分表计数一致只说明来源内部对账，不证明全球比赛完整收齐。

| 赛季 | 收集赛事 | 系列赛 | 比分表小局数 | 赛事目录小局数 | 不一致赛事数 |
| --- | --- | --- | --- | --- | --- |
| S3 | 2 | 53 | 73 | 73 | 0 |
| S4 | 10 | 545 | 635 | 636 | 1 |
| S5 | 36 | 996 | 1763 | 1763 | 0 |
| S6 | 36 | 972 | 2035 | 2035 | 0 |
| S7 | 49 | 1344 | 2899 | 2899 | 0 |
| S8 | 68 | 2229 | 3889 | 3890 | 1 |
| S9 | 64 | 2311 | 3651 | 3651 | 0 |
| S10 | 56 | 2246 | 3541 | 3541 | 0 |
| S11 | 54 | 2367 | 3684 | 3685 | 1 |
| S12 | 51 | 2306 | 3700 | 3701 | 1 |
| S13 | 52 | 1729 | 3422 | 3432 | 4 |
| S14 | 50 | 1503 | 3235 | 3238 | 2 |
| S15 | 41 | 1053 | 2609 | 2609 | 0 |


## 逐项计数缺口

| 赛季 | 赛事 | 比分表小局数 | 赛事目录小局数 | 状态 |
| --- | --- | --- | --- | --- |
| S4 | [EU LCS Summer 2014](https://gol.gg/tournament/tournament-matchlist/EU%20LCS%20Summer%202014/) | 111 | 112 | 小局数不一致 |
| S8 | [OPL Split 2 2018](https://gol.gg/tournament/tournament-matchlist/OPL%20Split%202%202018/) | 93 | 94 | 小局数不一致 |
| S11 | [LCO Split 1 2021](https://gol.gg/tournament/tournament-matchlist/LCO%20Split%201%202021/) | 56 | 57 | 小局数不一致 |
| S12 | [LCK Spring 2022](https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%202022/) | 212 | 213 | 小局数不一致 |
| S13 | [LCO Split 1 2023](https://gol.gg/tournament/tournament-matchlist/LCO%20Split%201%202023/) | 23 | 28 | 小局数不一致 |
| S13 | [LCO Split 1 Stage 2 2023](https://gol.gg/tournament/tournament-matchlist/LCO%20Split%201%20Stage%202%202023/) | 39 | 41 | 小局数不一致 |
| S13 | [LCO Split 2 2023](https://gol.gg/tournament/tournament-matchlist/LCO%20Split%202%202023/) | 55 | 57 | 小局数不一致 |
| S13 | [LJL Summer 2023](https://gol.gg/tournament/tournament-matchlist/LJL%20Summer%202023/) | 66 | 67 | 小局数不一致 |
| S14 | [LCO Split 1 2024](https://gol.gg/tournament/tournament-matchlist/LCO%20Split%201%202024/) | 54 | 55 | 小局数不一致 |
| S14 | [VCS Spring Playoffs 2024](https://gol.gg/tournament/tournament-matchlist/VCS%20Spring%20Playoffs%202024/) | 17 | 19 | 小局数不一致 |


所有回测目标赛事的解析小局数与来源目录一致，但训练赛事的上述缺口仍会影响预测。并未凭空补比分，也没有把未获取的数据视为零场或零胜。

## 模型不覆盖的因素

当前模型没有区分全局 BP 下的第几局、此前消耗的英雄或 BP 策略，也没有建模赛季中换人、替补上场、选边、版本变化和系列赛内状态关联。一个赛季内同名队伍视为同一队，近期比赛仅通过时间权重获得更大影响。

赛区先验依赖上一季国际赛，样本少的赛区仍有较大不确定性；旧队名使用规范化字符串连接，不擅自推断俱乐部合并。早期缺失赛区标签使用显式元数据补齐，不能将其解释为补齐比赛记录。

## 逐局细节与采集经验

新版[详细数据总览](../reports/detailed_data/README.md)按赛季、联赛提供红蓝方、经济及阵容明细；[对账报告](../reports/detailed_data/reconciliation.md)区分已核准与未匹配记录。下载入口、覆盖陷阱和赛制核验方法见[研究经验](RESEARCH_NOTES.md)。详细数据已用于独立增量实验，结果见[模型对比](../reports/detailed_data/model_comparison.md)；尚未替换主结果。

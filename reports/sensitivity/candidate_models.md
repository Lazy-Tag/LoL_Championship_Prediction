# 新模型比较：逐场预测与整届结果

[返回首页](../../README.md) · [数据补充与缺口](../data_enrichment/README.md) · [算法细节](../../MODEL.md)

**本轮逐场比较中，新分层模型表现最好；动态模型也优于原模型，但没有进一步超过新分层模型。** 三者使用同一批胜负输入。逐局字段已补充，尚未作为预测变量；未因此宣称补齐所有历史赛程。

## 逐场表现

S4–S15，共 1,300 场系列赛、1,965 小局；S3 不回放。同日赛果不用于当日预测。概率为 50% 时按半次命中计分。对数损失和 Brier 越低越好。

| 模型 | 系列赛命中率 | 小局命中率 | 系列赛对数损失 | 小局对数损失 | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 原模型 | 68.96% | 65.62% | 0.5993 | 0.6273 | 0.2179 |
| 新分层模型 | 69.92% | 66.82% | 0.5746 | 0.6094 | 0.2108 |
| 动态模型 | 69.38% | 66.31% | 0.5787 | 0.6115 | 0.2117 |

## 整届冠军与排名

每个候选每届独立模拟，种子为年份；沿用旧赛制近似，所以这是相同规则情景下的比较。冠军命中率不是逐场命中率。

| 模型 | 冠军预测命中 | 实际冠军平均概率 | 冠军对数损失 | 冠军 Brier | 平均预期名次相关性 |
| --- | --- | --- | --- | --- | --- |
| 新分层模型 | 9/23 | 30.43% | 1.6458 | 0.7695 | 0.771 |
| 动态模型 | 10/23 | 29.87% | 1.6070 | 0.7626 | 0.775 |
| 原模型 | 8/23 | 27.06% | 1.9630 | 0.8557 | 0.723 |

## 逐届对照

每个单元格为该届实际冠军的赛前夺冠概率；链接内有全体参赛队实力排名、夺冠概率、赛前赛区排名和实际名次。

| 赛事 | 实际冠军 | 原模型 | 新分层模型 | 动态模型 |
| --- | --- | --- | --- | --- |
| 2014_Worlds | Samsung Galaxy White | 20.54% | [27.07%](hierarchical90/2014_Worlds.md) | [29.52%](dynamic90/2014_Worlds.md) |
| 2015_MSI | Edward Gaming | 54.68% | [52.37%](hierarchical90/2015_MSI.md) | [47.72%](dynamic90/2015_MSI.md) |
| 2015_Worlds | SKTelecom T1 | 63.43% | [52.58%](hierarchical90/2015_Worlds.md) | [28.72%](dynamic90/2015_Worlds.md) |
| 2016_MSI | SK Telecom T1 | 75.48% | [86.42%](hierarchical90/2016_MSI.md) | [91.17%](dynamic90/2016_MSI.md) |
| 2016_Worlds | SK Telecom T1 | 20.96% | [24.74%](hierarchical90/2016_Worlds.md) | [14.50%](dynamic90/2016_Worlds.md) |
| 2017_MSI | SK Telecom T1 | 36.02% | [69.87%](hierarchical90/2017_MSI.md) | [78.02%](dynamic90/2017_MSI.md) |
| 2017_Worlds | Samsung Galaxy | 24.11% | [25.90%](hierarchical90/2017_Worlds.md) | [20.05%](dynamic90/2017_Worlds.md) |
| 2018_MSI | Royal Never Give Up | 3.68% | [8.96%](hierarchical90/2018_MSI.md) | [18.22%](dynamic90/2018_MSI.md) |
| 2018_Worlds | Invictus Gaming | 33.11% | [32.10%](hierarchical90/2018_Worlds.md) | [23.80%](dynamic90/2018_Worlds.md) |
| 2019_MSI | G2 Esports | 20.51% | [23.78%](hierarchical90/2019_MSI.md) | [22.56%](dynamic90/2019_MSI.md) |
| 2019_Worlds | Funplus Phoenix | 52.78% | [47.80%](hierarchical90/2019_Worlds.md) | [42.52%](dynamic90/2019_Worlds.md) |
| 2020_MSC | Top Esports | 13.21% | [13.84%](hierarchical90/2020_MSC.md) | [17.26%](dynamic90/2020_MSC.md) |
| 2020_Worlds | DAMWON Gaming | 19.06% | [16.01%](hierarchical90/2020_Worlds.md) | [32.95%](dynamic90/2020_Worlds.md) |
| 2021_MSI | Royal Never Give Up | 4.82% | [29.32%](hierarchical90/2021_MSI.md) | [30.11%](dynamic90/2021_MSI.md) |
| 2021_Worlds | Edward Gaming | 21.46% | [23.89%](hierarchical90/2021_Worlds.md) | [23.58%](dynamic90/2021_Worlds.md) |
| 2022_MSI | Royal Never Give Up | 4.41% | [13.19%](hierarchical90/2022_MSI.md) | [20.59%](dynamic90/2022_MSI.md) |
| 2022_Worlds | DRX | 0.07% | [0.29%](hierarchical90/2022_Worlds.md) | [0.60%](dynamic90/2022_Worlds.md) |
| 2023_MSI | JD Gaming | 16.13% | [14.64%](hierarchical90/2023_MSI.md) | [19.33%](dynamic90/2023_MSI.md) |
| 2023_Worlds | T1 | 2.94% | [4.14%](hierarchical90/2023_Worlds.md) | [3.43%](dynamic90/2023_Worlds.md) |
| 2024_MSI | Gen.G eSports | 50.48% | [47.79%](hierarchical90/2024_MSI.md) | [42.52%](dynamic90/2024_MSI.md) |
| 2024_Worlds | T1 | 2.17% | [4.05%](hierarchical90/2024_Worlds.md) | [3.46%](dynamic90/2024_Worlds.md) |
| 2025_MSI | Gen.G eSports | 75.87% | [73.48%](hierarchical90/2025_MSI.md) | [68.76%](dynamic90/2025_MSI.md) |
| 2025_Worlds | T1 | 6.38% | [7.64%](hierarchical90/2025_Worlds.md) | [7.58%](dynamic90/2025_Worlds.md) |

## 分赛季逐场命中率

| 赛季 | 原模型 | 新分层模型 | 动态模型 |
| --- | --- | --- | --- |
| S4 | 71.93% | 71.93% | 70.18% |
| S5 | 71.62% | 70.27% | 63.51% |
| S6 | 58.89% | 64.44% | 64.44% |
| S7 | 67.45% | 65.77% | 65.77% |
| S8 | 62.42% | 65.77% | 63.76% |
| S9 | 72.48% | 72.48% | 71.81% |
| S10 | 65.35% | 66.34% | 66.34% |
| S11 | 68.79% | 68.79% | 72.61% |
| S12 | 76.69% | 76.69% | 72.39% |
| S13 | 64.94% | 71.43% | 72.73% |
| S14 | 67.57% | 67.57% | 71.62% |
| S15 | 81.67% | 81.67% | 81.67% |

## S16 排名与过关概率

- [新分层模型](../s16/advancement_hierarchical.md)
- [动态模型](../s16/advancement_dynamic.md)
- [原模型](../s16/advancement.md)

S16 尚无最终成绩，不能用它判断哪个模型更准确。现主结果采用动态模型，原模型和静态分层模型保留为对照。

## 如何理解改善

两个候选均采用更强收缩，动态模型另加入状态随时间变化；目前没有只改变一项的完整消融实验，不能把收益完全归因于层级结构或动态更新。只有 23 届赛事，且多个赛季共享参赛队和数据缺口；当前差异是历史描述，不是已经证明稳定的未来优势。参数未按本次结果挑选，但本项目此前已多次审视这些年份，仍需后续独立赛事验证。

完整逐场明细：

- [S4 三模型逐场预测](candidate_predictions/S4.md)
- [S5 三模型逐场预测](candidate_predictions/S5.md)
- [S6 三模型逐场预测](candidate_predictions/S6.md)
- [S7 三模型逐场预测](candidate_predictions/S7.md)
- [S8 三模型逐场预测](candidate_predictions/S8.md)
- [S9 三模型逐场预测](candidate_predictions/S9.md)
- [S10 三模型逐场预测](candidate_predictions/S10.md)
- [S11 三模型逐场预测](candidate_predictions/S11.md)
- [S12 三模型逐场预测](candidate_predictions/S12.md)
- [S13 三模型逐场预测](candidate_predictions/S13.md)
- [S14 三模型逐场预测](candidate_predictions/S14.md)
- [S15 三模型逐场预测](candidate_predictions/S15.md)

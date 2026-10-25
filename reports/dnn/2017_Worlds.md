# 2017_Worlds：神经网络对照

[总览](README.md) · [逐届赛制与近似](../event_replay/rules.md)

开赛截点2017-09-23；每项14,000,605次，模拟种子2017。网络小局概率为三个预定训练种子的平均，整届特征冻结。


| 队伍 | 实际名次 | 原动态模型夺冠概率 | 纯小型DNN夺冠概率 | 残差DNN夺冠概率 | 原动态模型预期名次 | 纯小型DNN预期名次 | 残差DNN预期名次 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1907 Fenerbahce | 9–16 | 0.000% | 0.105% | 0.000% | 18.572 | 17.680 | 18.928 |
| ahq e-Sports Club | 9–16 | 0.061% | 2.342% | 0.200% | 10.839 | 9.391 | 10.502 |
| Cloud 9 | 5–8 | 0.534% | 2.652% | 1.096% | 12.168 | 13.013 | 11.350 |
| Dire Wolves | 17–24 | 0.000% | 0.001% | 0.000% | 19.518 | 19.453 | 19.969 |
| Edward Gaming | 9–16 | 0.975% | 2.508% | 1.104% | 8.536 | 8.944 | 8.847 |
| Flash Wolves | 9–16 | 1.057% | 6.826% | 2.087% | 7.789 | 7.560 | 7.732 |
| Fnatic | 5–8 | 0.028% | 1.271% | 0.148% | 15.677 | 14.231 | 13.861 |
| G2 Esports | 9–16 | 0.078% | 2.714% | 0.285% | 10.781 | 9.145 | 10.318 |
| Gambit Esports | 17–24 | 0.000% | 0.014% | 0.000% | 19.532 | 18.455 | 19.464 |
| GIGABYTE Marines | 9–16 | 0.011% | 0.656% | 0.007% | 11.571 | 10.487 | 11.784 |
| Hong Kong Attitude | 17–24 | 0.169% | 1.445% | 0.332% | 13.760 | 14.465 | 13.032 |
| Immortals | 9–16 | 1.753% | 7.482% | 3.317% | 7.792 | 7.609 | 7.439 |
| Kaos Latin Gamers | 17–24 | 0.000% | 0.011% | 0.000% | 19.218 | 19.091 | 19.825 |
| Longzhu Gaming | 5–8 | 43.364% | 21.252% | 38.436% | 2.991 | 5.728 | 3.416 |
| Lyon Gaming | 17–24 | 0.001% | 0.035% | 0.000% | 18.090 | 18.450 | 18.882 |
| Misfits | 5–8 | 0.001% | 0.391% | 0.006% | 11.829 | 10.480 | 11.633 |
| Rampage | 17–24 | 0.000% | 0.006% | 0.000% | 19.476 | 19.150 | 19.825 |
| Royal Never Give Up | 3–4 | 1.366% | 3.134% | 1.469% | 8.230 | 8.625 | 8.599 |
| Samsung Galaxy | 1 | 20.050% | 15.553% | 18.667% | 4.306 | 6.050 | 4.845 |
| SK Telecom T1 | 2 | 24.285% | 18.756% | 24.404% | 3.957 | 5.768 | 4.325 |
| Team oNe eSports | 17–24 | 0.000% | 0.061% | 0.000% | 19.134 | 17.955 | 19.006 |
| Team SoloMid | 9–16 | 5.720% | 9.882% | 7.127% | 5.727 | 6.865 | 6.053 |
| Team WE | 3–4 | 0.546% | 2.890% | 1.313% | 11.886 | 12.439 | 10.870 |
| Young Generation | 17–24 | 0.000% | 0.014% | 0.000% | 18.622 | 18.967 | 19.493 |

## 赛前赛区比较

网络没有唯一一维实力；实力均值沿用原动态模型输入，不能解释为网络独立估计。各候选的赛区夺冠概率由各自模拟合计。

### 原动态模型

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 韩国 | 3 | Longzhu Gaming、SK Telecom T1、Samsung Galaxy | 87.6993% |
| 2 | 中国 | 3 | Royal Never Give Up、Edward Gaming、Team WE | 2.8867% |
| 3 | 美洲 | 6 | Team SoloMid、Immortals、Cloud 9、Lyon Gaming、Kaos Latin Gamers、Team oNe eSports | 8.0082% |
| 4 | 欧洲 | 3 | G2 Esports、Fnatic、Misfits | 0.1075% |
| 5 | 外卡 | 9 | Flash Wolves、Hong Kong Attitude、ahq e-Sports Club、GIGABYTE Marines、1907 Fenerbahce、Young Generation、Gambit Esports、Rampage、Dire Wolves | 1.2984% |

### 纯小型DNN

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 韩国 | 3 | Longzhu Gaming、SK Telecom T1、Samsung Galaxy | 55.5608% |
| 2 | 中国 | 3 | Royal Never Give Up、Edward Gaming、Team WE | 8.5322% |
| 3 | 美洲 | 6 | Team SoloMid、Immortals、Cloud 9、Lyon Gaming、Kaos Latin Gamers、Team oNe eSports | 20.1227% |
| 4 | 欧洲 | 3 | G2 Esports、Fnatic、Misfits | 4.3767% |
| 5 | 外卡 | 9 | Flash Wolves、Hong Kong Attitude、ahq e-Sports Club、GIGABYTE Marines、1907 Fenerbahce、Young Generation、Gambit Esports、Rampage、Dire Wolves | 11.4076% |

### 残差DNN

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 韩国 | 3 | Longzhu Gaming、SK Telecom T1、Samsung Galaxy | 81.5069% |
| 2 | 中国 | 3 | Royal Never Give Up、Edward Gaming、Team WE | 3.8866% |
| 3 | 美洲 | 6 | Team SoloMid、Immortals、Cloud 9、Lyon Gaming、Kaos Latin Gamers、Team oNe eSports | 11.5410% |
| 4 | 欧洲 | 3 | G2 Esports、Fnatic、Misfits | 0.4388% |
| 5 | 外卡 | 9 | Flash Wolves、Hong Kong Attitude、ahq e-Sports Club、GIGABYTE Marines、1907 Fenerbahce、Young Generation、Gambit Esports、Rampage、Dire Wolves | 2.6267% |

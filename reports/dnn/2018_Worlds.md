# 2018_Worlds：神经网络对照

[总览](README.md) · [逐届赛制与近似](../event_replay/rules.md)

开赛截点2018-10-01；每项14,000,605次，模拟种子2018。网络小局概率为三个预定训练种子的平均，整届特征冻结。


| 队伍 | 实际名次 | 原动态模型夺冠概率 | 纯小型DNN夺冠概率 | 残差DNN夺冠概率 | 原动态模型预期名次 | 纯小型DNN预期名次 | 残差DNN预期名次 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 Thieves | 9–16 | 0.007% | 0.091% | 0.006% | 11.195 | 10.781 | 11.215 |
| Afreeca Freecs | 5–8 | 8.281% | 6.945% | 8.229% | 5.701 | 6.999 | 5.707 |
| Ascension Gaming | 17–24 | 0.000% | 0.000% | 0.000% | 20.290 | 20.278 | 20.320 |
| BAUSuperMassive | 17–24 | 0.000% | 0.008% | 0.000% | 17.561 | 16.829 | 17.607 |
| Cloud9 | 3–4 | 0.037% | 0.256% | 0.035% | 13.744 | 15.037 | 13.707 |
| Detonation FocusMe | 17–24 | 0.000% | 0.000% | 0.000% | 20.400 | 20.007 | 20.408 |
| Dire Wolves | 17–24 | 0.000% | 0.002% | 0.000% | 19.575 | 18.901 | 19.611 |
| Edward Gaming | 5–8 | 7.030% | 7.220% | 6.546% | 7.003 | 7.949 | 7.080 |
| Flash Wolves | 9–16 | 0.500% | 3.825% | 0.558% | 9.049 | 8.007 | 8.946 |
| Fnatic | 2 | 1.150% | 2.311% | 1.100% | 7.246 | 7.834 | 7.242 |
| G2 Esports | 3–4 | 0.042% | 0.435% | 0.047% | 13.258 | 13.416 | 13.091 |
| Gambit Esports | 17–24 | 0.000% | 0.001% | 0.000% | 19.678 | 19.174 | 19.714 |
| Gen.G eSports | 9–16 | 17.889% | 13.822% | 18.459% | 4.996 | 5.974 | 4.916 |
| G-Rex | 9–16 | 0.001% | 0.027% | 0.001% | 16.697 | 16.819 | 16.604 |
| Infinity eSports | 17–24 | 0.000% | 0.002% | 0.000% | 19.003 | 18.593 | 19.067 |
| Invictus Gaming | 1 | 23.799% | 20.389% | 22.621% | 3.861 | 4.366 | 3.913 |
| KaBuM! e-Sports | 17–24 | 0.000% | 0.024% | 0.000% | 17.984 | 17.611 | 17.998 |
| Kaos Latin Gamers | 17–24 | 0.000% | 0.001% | 0.000% | 19.671 | 18.959 | 19.701 |
| KT Rolster | 5–8 | 21.080% | 16.359% | 21.687% | 4.311 | 5.504 | 4.261 |
| MAD Team | 9–16 | 0.001% | 0.036% | 0.000% | 12.000 | 11.272 | 12.008 |
| Phong Vu Buffalo | 9–16 | 0.005% | 0.058% | 0.004% | 11.556 | 11.121 | 11.623 |
| Royal Never Give Up | 5–8 | 19.683% | 26.584% | 20.255% | 4.826 | 4.603 | 4.747 |
| Team Liquid | 9–16 | 0.365% | 1.333% | 0.347% | 9.288 | 9.139 | 9.314 |
| Team Vitality | 9–16 | 0.130% | 0.272% | 0.106% | 11.106 | 10.829 | 11.201 |

## 赛前赛区比较

网络没有唯一一维实力；实力均值沿用原动态模型输入，不能解释为网络独立估计。各候选的赛区夺冠概率由各自模拟合计。

### 原动态模型

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 中国 | 3 | Invictus Gaming、Royal Never Give Up、Edward Gaming | 50.5121% |
| 2 | 韩国 | 3 | KT Rolster、Gen.G eSports、Afreeca Freecs | 47.2504% |
| 3 | 欧洲 | 3 | Fnatic、Team Vitality、G2 Esports | 1.3221% |
| 4 | 美洲 | 6 | Team Liquid、Cloud9、100 Thieves、KaBuM! e-Sports、Infinity eSports、Kaos Latin Gamers | 0.4088% |
| 5 | 外卡 | 9 | Flash Wolves、Phong Vu Buffalo、G-Rex、MAD Team、BAUSuperMassive、Dire Wolves、Gambit Esports、Ascension Gaming、Detonation FocusMe | 0.5065% |

### 纯小型DNN

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 中国 | 3 | Invictus Gaming、Royal Never Give Up、Edward Gaming | 54.1931% |
| 2 | 韩国 | 3 | KT Rolster、Gen.G eSports、Afreeca Freecs | 37.1260% |
| 3 | 欧洲 | 3 | Fnatic、Team Vitality、G2 Esports | 3.0184% |
| 4 | 美洲 | 6 | Team Liquid、Cloud9、100 Thieves、KaBuM! e-Sports、Infinity eSports、Kaos Latin Gamers | 1.7062% |
| 5 | 外卡 | 9 | Flash Wolves、Phong Vu Buffalo、G-Rex、MAD Team、BAUSuperMassive、Dire Wolves、Gambit Esports、Ascension Gaming、Detonation FocusMe | 3.9562% |

### 残差DNN

## 赛前赛区实力排名

按本届参赛队的平均赛前实力排序，仅代表本届参赛阵容。韩国、中国、欧洲、美洲单列，LCP 自 2025 年起单列，其余归入外卡。“外卡”为本文分类，不等同于当年官方外卡资格。合计夺冠概率另受参赛名额和赛程影响，不等同于实力排名。

| 排名 | 赛区 | 参赛队数 | 参赛队 | 赛区合计夺冠概率 |
| --- | --- | --- | --- | --- |
| 1 | 中国 | 3 | Invictus Gaming、Royal Never Give Up、Edward Gaming | 49.4210% |
| 2 | 韩国 | 3 | KT Rolster、Gen.G eSports、Afreeca Freecs | 48.3750% |
| 3 | 欧洲 | 3 | Fnatic、Team Vitality、G2 Esports | 1.2520% |
| 4 | 美洲 | 6 | Team Liquid、Cloud9、100 Thieves、KaBuM! e-Sports、Infinity eSports、Kaos Latin Gamers | 0.3887% |
| 5 | 外卡 | 9 | Flash Wolves、Phong Vu Buffalo、G-Rex、MAD Team、BAUSuperMassive、Dire Wolves、Gambit Esports、Ascension Gaming、Detonation FocusMe | 0.5632% |

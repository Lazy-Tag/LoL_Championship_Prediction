# 历史模型对照：赛区先验、中性先验与无正则 MLE

[敏感性附录](README.md) · [模型细节](../../MODEL.md)

本页为旧模型对照；当前主结果采用动态模型，见[当前比较](candidate_models.md)。旧方案固定为 90 天赛区先验。赛区先验利用上一季国际赛估计跨赛区基础强度；中性先验给所有队伍相同的初始均值；无正则 MLE 不施加先验，仅在数学上可识别、存在有限解时预测。后者覆盖的是选择性子集，不能直接与全量结果比较。模型选择依据当前回测表现，未经新的独立测试集验证，不能保证未来最优。

## 全量覆盖与成绩

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 1300 | 68.96% | 65.62% | 0.6273 | 0.2179 |
| 中性先验 · 90 天 | 1300 | 62.04% | 59.57% | 0.6828 | 0.2431 |
| 无正则 MLE · 可识别子集 | 166 | 67.47% | 62.37% | 0.6750 | 0.2345 |

## 相同可识别子集

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 166 | 69.88% | 65.51% | 0.6342 | 0.2206 |
| 中性先验 · 90 天 | 166 | 63.86% | 60.28% | 0.6748 | 0.2403 |
| 无正则 MLE · 可识别子集 | 166 | 67.47% | 62.37% | 0.6750 | 0.2345 |


## S4

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 57 | 71.93% | 67.95% | 0.6291 | 0.2171 |
| 中性先验 · 90 天 | 57 | 64.91% | 62.82% | 0.6529 | 0.2320 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2014-09-18 | Worlds | Edward Gaming | Samsung Galaxy White | 43.3709% | 50.0000% | — |
| 2014-09-18 | Worlds | Team SoloMid | SK Gaming | 39.4119% | 60.6229% | — |
| 2014-09-18 | Worlds | Dark Passage | ahq e-Sports Club | 61.8272% | 50.0000% | — |
| 2014-09-18 | Worlds | Taipei Assassins | Star Horn Royal Club | 10.2803% | 29.8680% | — |
| 2014-09-18 | Worlds | Samsung Galaxy White | ahq e-Sports Club | 86.9793% | 50.0000% | — |
| 2014-09-18 | Worlds | Star Horn Royal Club | Team SoloMid | 67.0455% | 34.4745% | — |
| 2014-09-19 | Worlds | Taipei Assassins | SK Gaming | 15.0442% | 25.5551% | — |
| 2014-09-19 | Worlds | Edward Gaming | Dark Passage | 82.7195% | 61.5899% | — |
| 2014-09-19 | Worlds | Star Horn Royal Club | SK Gaming | 81.0196% | 81.3328% | — |
| 2014-09-19 | Worlds | Dark Passage | Samsung Galaxy White | 3.3819% | 8.5170% | — |
| 2014-09-19 | Worlds | Team SoloMid | Taipei Assassins | 84.6748% | 84.5960% | — |
| 2014-09-19 | Worlds | Edward Gaming | ahq e-Sports Club | 61.2504% | 34.6924% | — |
| 2014-09-20 | Worlds | Samsung Galaxy White | Dark Passage | 98.0589% | 95.9944% | — |
| 2014-09-20 | Worlds | SK Gaming | Star Horn Royal Club | 10.5841% | 11.0442% | — |
| 2014-09-20 | Worlds | ahq e-Sports Club | Samsung Galaxy White | 5.2972% | 11.0046% | — |
| 2014-09-20 | Worlds | Taipei Assassins | Team SoloMid | 27.3386% | 23.4787% | — |
| 2014-09-20 | Worlds | Dark Passage | Edward Gaming | 6.7614% | 10.9845% | — |
| 2014-09-20 | Worlds | SK Gaming | Taipei Assassins | 63.9877% | 54.1156% | — |
| 2014-09-21 | Worlds | Team SoloMid | Star Horn Royal Club | 13.6026% | 23.7537% | — |
| 2014-09-21 | Worlds | ahq e-Sports Club | Dark Passage | 75.0167% | 76.3850% | — |
| 2014-09-21 | Worlds | Star Horn Royal Club | Taipei Assassins | 96.6122% | 94.6961% | — |
| 2014-09-21 | Worlds | ahq e-Sports Club | Edward Gaming | 14.6359% | 22.5503% | — |
| 2014-09-21 | Worlds | SK Gaming | Team SoloMid | 39.8394% | 26.8114% | — |
| 2014-09-21 | Worlds | Samsung Galaxy White | Edward Gaming | 79.2503% | 76.3600% | — |
| 2014-09-21 | Worlds | Edward Gaming | ahq e-Sports Club | 85.3641% | 77.4497% | — |
| 2014-09-25 | Worlds | LMQ | OMG | 31.5766% | 47.3338% | — |
| 2014-09-25 | Worlds | NaJin White Shield | KaBuM! eSports | 80.4854% | 50.0000% | — |
| 2014-09-25 | Worlds | Samsung Galaxy Blue | OMG | 53.4940% | 33.9616% | — |
| 2014-09-25 | Worlds | Cloud 9 | Alliance | 50.4737% | 63.4849% | — |
| 2014-09-25 | Worlds | Fnatic | LMQ | 54.6996% | 40.4577% | — |
| 2014-09-25 | Worlds | Cloud 9 | KaBuM! eSports | 72.7409% | 73.0064% | — |
| 2014-09-26 | Worlds | NaJin White Shield | Alliance | 73.5728% | 60.0967% | — |
| 2014-09-26 | Worlds | Samsung Galaxy Blue | Fnatic | 84.2203% | 74.3189% | — |
| 2014-09-26 | Worlds | NaJin White Shield | Cloud 9 | 61.6210% | 36.5332% | — |
| 2014-09-26 | Worlds | OMG | Fnatic | 52.7148% | 49.8971% | — |
| 2014-09-26 | Worlds | Alliance | KaBuM! eSports | 81.2546% | 77.7378% | — |
| 2014-09-26 | Worlds | Samsung Galaxy Blue | LMQ | 77.1891% | 54.5533% | — |
| 2014-09-27 | Worlds | Fnatic | OMG | 43.7605% | 44.7716% | — |
| 2014-09-27 | Worlds | Alliance | Cloud 9 | 39.9942% | 31.5944% | — |
| 2014-09-27 | Worlds | LMQ | Fnatic | 56.3196% | 65.3001% | — |
| 2014-09-27 | Worlds | KaBuM! eSports | NaJin White Shield | 2.3033% | 4.0022% | — |
| 2014-09-27 | Worlds | OMG | Samsung Galaxy Blue | 34.9701% | 37.6795% | — |
| 2014-09-27 | Worlds | Alliance | NaJin White Shield | 12.4859% | 15.8056% | — |
| 2014-09-28 | Worlds | KaBuM! eSports | Cloud 9 | 10.3615% | 9.7214% | — |
| 2014-09-28 | Worlds | LMQ | Samsung Galaxy Blue | 23.7139% | 34.1078% | — |
| 2014-09-28 | Worlds | KaBuM! eSports | Alliance | 9.5037% | 11.7951% | — |
| 2014-09-28 | Worlds | Fnatic | Samsung Galaxy Blue | 25.8060% | 29.5146% | — |
| 2014-09-28 | Worlds | Cloud 9 | NaJin White Shield | 31.5692% | 41.8453% | — |
| 2014-09-28 | Worlds | OMG | LMQ | 57.7480% | 47.9365% | — |
| 2014-09-28 | Worlds | NaJin White Shield | Cloud 9 | 68.4308% | 58.1547% | — |
| 2014-10-03 | Worlds | Samsung Galaxy White | Team SoloMid | 88.8911% | 79.9991% | — |
| 2014-10-04 | Worlds | Samsung Galaxy Blue | Cloud 9 | 75.5853% | 67.4468% | — |
| 2014-10-05 | Worlds | Star Horn Royal Club | Edward Gaming | 74.5240% | 73.5888% | — |
| 2014-10-06 | Worlds | NaJin White Shield | OMG | 59.9715% | 60.0471% | — |
| 2014-10-11 | Worlds | Samsung Galaxy Blue | Samsung Galaxy White | 48.3398% | 48.5272% | — |
| 2014-10-12 | Worlds | Star Horn Royal Club | OMG | 49.3037% | 50.1984% | — |
| 2014-10-19 | Worlds | Star Horn Royal Club | Samsung Galaxy White | 20.6003% | 21.3962% | — |


## S5

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 74 | 71.62% | 67.33% | 0.5779 | 0.1957 |
| 中性先验 · 90 天 | 74 | 68.92% | 67.33% | 0.6111 | 0.2121 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2015-05-07 | MSI | Fnatic | Team SoloMid | 37.1433% | 42.4407% | — |
| 2015-05-07 | MSI | Besiktas E-Sports Club | SKTelecom T1 | 14.8838% | 46.5862% | — |
| 2015-05-07 | MSI | Edward Gaming | AHQ E-Sports Club | 70.1433% | 47.7084% | — |
| 2015-05-07 | MSI | Besiktas E-Sports Club | Team SoloMid | 23.5103% | 45.3450% | — |
| 2015-05-07 | MSI | Fnatic | AHQ E-Sports Club | 38.2556% | 31.5052% | — |
| 2015-05-07 | MSI | SKTelecom T1 | Edward Gaming | 43.9611% | 39.4092% | — |
| 2015-05-07 | MSI | AHQ E-Sports Club | Besiktas E-Sports Club | 75.6273% | 65.8954% | — |
| 2015-05-07 | MSI | SKTelecom T1 | Team SoloMid | 63.7384% | 48.7509% | — |
| 2015-05-08 | MSI | Edward Gaming | Fnatic | 77.0135% | 65.3172% | — |
| 2015-05-08 | MSI | Team SoloMid | AHQ E-Sports Club | 43.0746% | 35.4460% | — |
| 2015-05-08 | MSI | Edward Gaming | Besiktas E-Sports Club | 92.8102% | 83.3476% | — |
| 2015-05-08 | MSI | SKTelecom T1 | Fnatic | 79.8462% | 66.0811% | — |
| 2015-05-08 | MSI | Team SoloMid | Edward Gaming | 28.0122% | 36.1218% | — |
| 2015-05-08 | MSI | Fnatic | Besiktas E-Sports Club | 79.3937% | 72.6603% | — |
| 2015-05-08 | MSI | AHQ E-Sports Club | SKTelecom T1 | 30.3077% | 49.8879% | — |
| 2015-05-09 | MSI | SKTelecom T1 | Fnatic | 83.8443% | 74.4180% | — |
| 2015-05-09 | MSI | Edward Gaming | AHQ E-Sports Club | 68.6559% | 57.0984% | — |
| 2015-05-10 | MSI | SKTelecom T1 | Edward Gaming | 43.9869% | 42.6488% | — |
| 2015-10-01 | Worlds | Fnatic | Invictus Gaming | 54.1557% | 67.3730% | — |
| 2015-10-01 | Worlds | Cloud 9 | AHQ E-Sports Club | 36.7295% | 30.7724% | — |
| 2015-10-01 | Worlds | SKTelecom T1 | H2k-Gaming | 87.6103% | 76.2945% | — |
| 2015-10-01 | Worlds | Edward Gaming | Bangkok Titans | 94.3808% | 85.0446% | — |
| 2015-10-01 | Worlds | Counter Logic Gaming | Flash Wolves | 81.2045% | 73.1755% | — |
| 2015-10-01 | Worlds | paiN Gaming | KOO Tigers | 28.5890% | 59.7307% | — |
| 2015-10-02 | Worlds | KT Rolster | Team SoloMid | 67.3305% | 52.3655% | — |
| 2015-10-02 | Worlds | LGD Gaming | Origen | 61.3093% | 47.4763% | — |
| 2015-10-02 | Worlds | Bangkok Titans | SKTelecom T1 | 3.0378% | 8.6694% | — |
| 2015-10-02 | Worlds | H2k-Gaming | Edward Gaming | 20.4655% | 30.3683% | — |
| 2015-10-02 | Worlds | Flash Wolves | KOO Tigers | 8.6815% | 20.8805% | — |
| 2015-10-02 | Worlds | Counter Logic Gaming | paiN Gaming | 70.2372% | 64.2433% | — |
| 2015-10-03 | Worlds | Edward Gaming | SKTelecom T1 | 35.3131% | 38.3006% | — |
| 2015-10-03 | Worlds | H2k-Gaming | Bangkok Titans | 82.1116% | 74.7687% | — |
| 2015-10-03 | Worlds | LGD Gaming | KT Rolster | 44.4172% | 48.7806% | — |
| 2015-10-03 | Worlds | Origen | Team SoloMid | 56.8648% | 59.6942% | — |
| 2015-10-03 | Worlds | Invictus Gaming | Cloud 9 | 62.3907% | 53.4283% | — |
| 2015-10-03 | Worlds | AHQ E-Sports Club | Fnatic | 27.2852% | 31.2178% | — |
| 2015-10-04 | Worlds | Team SoloMid | LGD Gaming | 44.1490% | 52.3127% | — |
| 2015-10-04 | Worlds | KT Rolster | Origen | 61.6177% | 46.1539% | — |
| 2015-10-04 | Worlds | Invictus Gaming | AHQ E-Sports Club | 45.2709% | 32.8220% | — |
| 2015-10-04 | Worlds | Cloud 9 | Fnatic | 31.4798% | 29.7938% | — |
| 2015-10-04 | Worlds | KOO Tigers | Counter Logic Gaming | 56.8294% | 43.8521% | — |
| 2015-10-04 | Worlds | paiN Gaming | Flash Wolves | 48.5772% | 48.8421% | — |
| 2015-10-08 | Worlds | Counter Logic Gaming | KOO Tigers | 42.6285% | 53.2473% | — |
| 2015-10-08 | Worlds | Flash Wolves | paiN Gaming | 34.8169% | 35.2911% | — |
| 2015-10-08 | Worlds | KOO Tigers | paiN Gaming | 76.8530% | 61.6322% | — |
| 2015-10-08 | Worlds | Flash Wolves | Counter Logic Gaming | 17.7979% | 22.9647% | — |
| 2015-10-08 | Worlds | KOO Tigers | Flash Wolves | 86.1419% | 74.6538% | — |
| 2015-10-08 | Worlds | paiN Gaming | Counter Logic Gaming | 28.8433% | 35.3420% | — |
| 2015-10-09 | Worlds | SKTelecom T1 | Edward Gaming | 70.5498% | 68.6248% | — |
| 2015-10-09 | Worlds | Bangkok Titans | H2k-Gaming | 15.6612% | 21.5425% | — |
| 2015-10-09 | Worlds | Bangkok Titans | Edward Gaming | 6.0564% | 12.5103% | — |
| 2015-10-09 | Worlds | H2k-Gaming | SKTelecom T1 | 12.6579% | 19.2310% | — |
| 2015-10-09 | Worlds | Edward Gaming | H2k-Gaming | 74.2295% | 65.7559% | — |
| 2015-10-09 | Worlds | SKTelecom T1 | Bangkok Titans | 97.3794% | 93.8636% | — |
| 2015-10-10 | Worlds | Team SoloMid | Origen | 40.7072% | 38.0061% | — |
| 2015-10-10 | Worlds | KT Rolster | LGD Gaming | 64.1313% | 61.4816% | — |
| 2015-10-10 | Worlds | Team SoloMid | KT Rolster | 32.1543% | 40.6591% | — |
| 2015-10-10 | Worlds | Origen | LGD Gaming | 55.2421% | 64.0794% | — |
| 2015-10-10 | Worlds | Origen | KT Rolster | 40.8394% | 52.7774% | — |
| 2015-10-10 | Worlds | LGD Gaming | Team SoloMid | 54.1312% | 47.7633% | — |
| 2015-10-11 | Worlds | AHQ E-Sports Club | Invictus Gaming | 48.6593% | 58.8616% | — |
| 2015-10-11 | Worlds | Fnatic | Cloud 9 | 65.3759% | 67.0838% | — |
| 2015-10-11 | Worlds | AHQ E-Sports Club | Cloud 9 | 56.0658% | 60.0268% | — |
| 2015-10-11 | Worlds | Invictus Gaming | Fnatic | 41.6263% | 33.9922% | — |
| 2015-10-11 | Worlds | Cloud 9 | Invictus Gaming | 42.6175% | 48.7919% | — |
| 2015-10-11 | Worlds | Fnatic | AHQ E-Sports Club | 59.6709% | 57.5761% | — |
| 2015-10-11 | Worlds | Cloud 9 | AHQ E-Sports Club | 43.9342% | 39.9732% | — |
| 2015-10-15 | Worlds | Flash Wolves | Origen | 38.2925% | 41.7835% | — |
| 2015-10-16 | Worlds | SKTelecom T1 | AHQ E-Sports Club | 82.3159% | 75.3734% | — |
| 2015-10-17 | Worlds | Fnatic | Edward Gaming | 47.7316% | 54.5801% | — |
| 2015-10-18 | Worlds | KT Rolster | KOO Tigers | 50.9074% | 50.4582% | — |
| 2015-10-24 | Worlds | SKTelecom T1 | Origen | 83.2174% | 77.5341% | — |
| 2015-10-25 | Worlds | Fnatic | KOO Tigers | 50.3576% | 59.1188% | — |
| 2015-10-31 | Worlds | SKTelecom T1 | KOO Tigers | 71.1469% | 71.6417% | — |


## S6

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 90 | 58.89% | 59.32% | 0.6674 | 0.2352 |
| 中性先验 · 90 天 | 90 | 57.78% | 57.63% | 0.6899 | 0.2475 |
| 无正则 MLE · 可识别子集 | 2 | 100.00% | 100.00% | 0.4515 | 0.1325 |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2016-05-04 | MSI | Royal Never Give Up | CLG | 63.5748% | 58.2561% | 60.4088% |
| 2016-05-04 | MSI | G2 Esports | Flash Wolves | 51.6388% | 44.4894% | — |
| 2016-05-04 | MSI | SK Telecom T1 | SuperMassive | 82.8985% | 49.0059% | — |
| 2016-05-04 | MSI | CLG | Flash Wolves | 25.7789% | 27.0986% | — |
| 2016-05-04 | MSI | G2 Esports | SK Telecom T1 | 31.4541% | 52.0779% | 32.8948% |
| 2016-05-04 | MSI | SuperMassive | Royal Never Give Up | 44.1921% | 59.6670% | — |
| 2016-05-05 | MSI | CLG | G2 Esports | 32.9345% | 41.6107% | — |
| 2016-05-05 | MSI | SK Telecom T1 | Royal Never Give Up | 78.4923% | 58.9027% | — |
| 2016-05-05 | MSI | Flash Wolves | SuperMassive | 73.4501% | 69.3832% | — |
| 2016-05-05 | MSI | Royal Never Give Up | G2 Esports | 47.9398% | 52.8106% | — |
| 2016-05-05 | MSI | SuperMassive | CLG | 41.1970% | 43.0844% | — |
| 2016-05-05 | MSI | SK Telecom T1 | Flash Wolves | 77.9290% | 56.7480% | — |
| 2016-05-06 | MSI | Flash Wolves | Royal Never Give Up | 61.6001% | 60.9063% | — |
| 2016-05-06 | MSI | CLG | SK Telecom T1 | 18.6029% | 36.7466% | — |
| 2016-05-06 | MSI | SuperMassive | G2 Esports | 39.7049% | 47.8173% | — |
| 2016-05-06 | MSI | Flash Wolves | SK Telecom T1 | 46.5715% | 63.6431% | — |
| 2016-05-06 | MSI | CLG | SuperMassive | 51.4586% | 51.0664% | — |
| 2016-05-06 | MSI | G2 Esports | Royal Never Give Up | 37.5981% | 35.0935% | — |
| 2016-05-07 | MSI | G2 Esports | SuperMassive | 70.6859% | 64.3806% | — |
| 2016-05-07 | MSI | Royal Never Give Up | Flash Wolves | 46.2949% | 48.5710% | — |
| 2016-05-07 | MSI | SK Telecom T1 | CLG | 71.1172% | 52.9217% | — |
| 2016-05-07 | MSI | Flash Wolves | G2 Esports | 69.7458% | 69.6301% | — |
| 2016-05-07 | MSI | CLG | Royal Never Give Up | 30.7546% | 34.1993% | — |
| 2016-05-07 | MSI | SuperMassive | SK Telecom T1 | 16.0248% | 30.4265% | — |
| 2016-05-08 | MSI | Royal Never Give Up | SuperMassive | 85.1492% | 83.3340% | — |
| 2016-05-08 | MSI | Flash Wolves | CLG | 68.5465% | 64.2876% | — |
| 2016-05-08 | MSI | SK Telecom T1 | G2 Esports | 70.8264% | 59.4466% | — |
| 2016-05-08 | MSI | SuperMassive | Flash Wolves | 13.8383% | 16.6365% | — |
| 2016-05-08 | MSI | G2 Esports | CLG | 50.6366% | 45.8908% | — |
| 2016-05-08 | MSI | Royal Never Give Up | SK Telecom T1 | 44.6243% | 59.0981% | — |
| 2016-05-13 | MSI | Royal Never Give Up | SK Telecom T1 | 39.3835% | 52.7308% | — |
| 2016-05-14 | MSI | CLG | Flash Wolves | 40.9994% | 44.6573% | — |
| 2016-05-15 | MSI | CLG | SK Telecom T1 | 31.7730% | 45.3927% | — |
| 2016-09-29 | Worlds | G2 Esports | CLG | 69.0489% | 58.3330% | — |
| 2016-09-29 | Worlds | ROX Tigers | Albus NoX Luna | 89.1681% | 68.4074% | — |
| 2016-09-29 | Worlds | H2k-Gaming | ahq eSports | 44.2762% | 37.7413% | — |
| 2016-09-29 | Worlds | INTZ eSports | Edward Gaming | 16.5733% | 23.3864% | — |
| 2016-09-29 | Worlds | Samsung Galaxy | Splyce | 75.9411% | 59.1823% | — |
| 2016-09-29 | Worlds | Team SoloMid | Royal Never Give Up | 54.1167% | 62.6350% | — |
| 2016-09-30 | Worlds | SK Telecom T1 | Cloud 9 | 81.2404% | 58.9277% | — |
| 2016-09-30 | Worlds | Flash Wolves | I MAY | 62.3510% | 62.6115% | — |
| 2016-09-30 | Worlds | Team SoloMid | Samsung Galaxy | 34.9478% | 63.4978% | — |
| 2016-09-30 | Worlds | Royal Never Give Up | Splyce | 67.9815% | 71.9982% | — |
| 2016-09-30 | Worlds | H2k-Gaming | INTZ eSports | 44.1321% | 32.5441% | — |
| 2016-09-30 | Worlds | Edward Gaming | ahq eSports | 59.6926% | 59.6305% | — |
| 2016-10-01 | Worlds | CLG | Albus NoX Luna | 48.4040% | 48.9221% | — |
| 2016-10-01 | Worlds | ROX Tigers | G2 Esports | 84.5216% | 73.5667% | — |
| 2016-10-01 | Worlds | Flash Wolves | Cloud 9 | 54.0444% | 49.0315% | — |
| 2016-10-01 | Worlds | I MAY | SK Telecom T1 | 23.4921% | 38.5610% | — |
| 2016-10-01 | Worlds | Splyce | Team SoloMid | 27.1568% | 20.7858% | — |
| 2016-10-01 | Worlds | Royal Never Give Up | Samsung Galaxy | 39.9251% | 59.3537% | — |
| 2016-10-02 | Worlds | ahq eSports | INTZ eSports | 56.2561% | 51.2148% | — |
| 2016-10-02 | Worlds | Edward Gaming | H2k-Gaming | 77.5985% | 79.9998% | — |
| 2016-10-02 | Worlds | Albus NoX Luna | G2 Esports | 50.7389% | 58.8520% | — |
| 2016-10-02 | Worlds | CLG | ROX Tigers | 8.9818% | 20.4843% | — |
| 2016-10-02 | Worlds | SK Telecom T1 | Flash Wolves | 83.1544% | 70.6785% | — |
| 2016-10-02 | Worlds | Cloud 9 | I MAY | 50.0070% | 56.3898% | — |
| 2016-10-06 | Worlds | G2 Esports | ROX Tigers | 15.7763% | 24.2807% | — |
| 2016-10-06 | Worlds | Albus NoX Luna | CLG | 59.8680% | 58.5977% | — |
| 2016-10-06 | Worlds | CLG | G2 Esports | 48.6155% | 56.1332% | — |
| 2016-10-06 | Worlds | Albus NoX Luna | ROX Tigers | 20.9094% | 36.7393% | — |
| 2016-10-06 | Worlds | G2 Esports | Albus NoX Luna | 41.4699% | 35.5733% | — |
| 2016-10-06 | Worlds | ROX Tigers | CLG | 84.9459% | 70.9051% | — |
| 2016-10-06 | Worlds | ROX Tigers | Albus NoX Luna | 79.0906% | 63.2607% | — |
| 2016-10-07 | Worlds | Edward Gaming | INTZ eSports | 78.9463% | 75.7269% | — |
| 2016-10-07 | Worlds | ahq eSports | H2k-Gaming | 66.8757% | 70.6913% | — |
| 2016-10-07 | Worlds | H2k-Gaming | Edward Gaming | 20.9504% | 18.6617% | — |
| 2016-10-07 | Worlds | INTZ eSports | ahq eSports | 33.2625% | 36.6779% | — |
| 2016-10-07 | Worlds | INTZ eSports | H2k-Gaming | 50.1557% | 58.2824% | — |
| 2016-10-07 | Worlds | ahq eSports | Edward Gaming | 34.8565% | 35.6243% | — |
| 2016-10-07 | Worlds | H2k-Gaming | Edward Gaming | 20.9504% | 18.6617% | — |
| 2016-10-08 | Worlds | Samsung Galaxy | Team SoloMid | 51.3058% | 32.6062% | — |
| 2016-10-08 | Worlds | Splyce | Royal Never Give Up | 35.0785% | 32.8581% | — |
| 2016-10-08 | Worlds | Team SoloMid | Splyce | 75.4542% | 80.2594% | — |
| 2016-10-08 | Worlds | Samsung Galaxy | Royal Never Give Up | 63.6369% | 49.0484% | — |
| 2016-10-08 | Worlds | Splyce | Samsung Galaxy | 23.5911% | 33.7034% | — |
| 2016-10-08 | Worlds | Royal Never Give Up | Team SoloMid | 37.5804% | 33.4483% | — |
| 2016-10-09 | Worlds | I MAY | Flash Wolves | 42.2347% | 41.9020% | — |
| 2016-10-09 | Worlds | Cloud 9 | SK Telecom T1 | 25.1704% | 40.0520% | — |
| 2016-10-09 | Worlds | Cloud 9 | Flash Wolves | 50.6662% | 54.7446% | — |
| 2016-10-09 | Worlds | SK Telecom T1 | I MAY | 80.6798% | 71.5135% | — |
| 2016-10-09 | Worlds | I MAY | Cloud 9 | 41.5859% | 37.3518% | — |
| 2016-10-09 | Worlds | Flash Wolves | SK Telecom T1 | 24.6718% | 35.5796% | — |
| 2016-10-14 | Worlds | Samsung Galaxy | Cloud 9 | 73.2007% | 57.4807% | — |
| 2016-10-15 | Worlds | SK Telecom T1 | Royal Never Give Up | 76.9596% | 68.3340% | — |
| 2016-10-16 | Worlds | ROX Tigers | Edward Gaming | 77.4014% | 67.8484% | — |
| 2016-10-17 | Worlds | H2k-Gaming | Albus NoX Luna | 38.8805% | 35.8075% | — |
| 2016-10-22 | Worlds | ROX Tigers | SK Telecom T1 | 58.1027% | 57.2561% | — |
| 2016-10-23 | Worlds | Samsung Galaxy | H2k-Gaming | 74.0773% | 66.1145% | — |
| 2016-10-30 | Worlds | Samsung Galaxy | SK Telecom T1 | 45.3272% | 44.5850% | — |


## S7

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 149 | 67.45% | 66.75% | 0.6436 | 0.2243 |
| 中性先验 · 90 天 | 149 | 62.75% | 61.68% | 0.6707 | 0.2354 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2017-04-28 | MSI | Red Canids | Dire Wolves | 61.4243% | 81.5643% | — |
| 2017-04-28 | MSI | SuperMassive | Rampage | 30.8493% | 50.0000% | — |
| 2017-04-28 | MSI | Red Canids | Rampage | 61.4243% | 81.5643% | — |
| 2017-04-28 | MSI | SuperMassive | Dire Wolves | 30.8493% | 50.0000% | — |
| 2017-04-28 | MSI | Dire Wolves | Rampage | 50.0000% | 50.0000% | — |
| 2017-04-28 | MSI | SuperMassive | Red Canids | 21.8854% | 18.4357% | — |
| 2017-04-29 | MSI | Virtus.pro | Lyon Gaming | 53.2318% | 53.1535% | — |
| 2017-04-29 | MSI | GIGABYTE Marines | Isurus Gaming | 50.0000% | 50.0000% | — |
| 2017-04-29 | MSI | Virtus.pro | Isurus Gaming | 53.2318% | 53.1535% | — |
| 2017-04-29 | MSI | GIGABYTE Marines | Lyon Gaming | 50.0000% | 50.0000% | — |
| 2017-04-29 | MSI | Lyon Gaming | Isurus Gaming | 50.0000% | 50.0000% | — |
| 2017-04-29 | MSI | GIGABYTE Marines | Virtus.pro | 46.7682% | 46.8465% | — |
| 2017-04-30 | MSI | Rampage | Red Canids | 10.6130% | 6.2430% | — |
| 2017-04-30 | MSI | Dire Wolves | SuperMassive | 14.1791% | 10.5831% | — |
| 2017-04-30 | MSI | Rampage | SuperMassive | 5.3632% | 3.5775% | — |
| 2017-04-30 | MSI | Dire Wolves | Red Canids | 25.7136% | 17.5198% | — |
| 2017-04-30 | MSI | Red Canids | SuperMassive | 32.3094% | 35.7823% | — |
| 2017-04-30 | MSI | Rampage | Dire Wolves | 25.5406% | 23.8664% | — |
| 2017-05-01 | MSI | Isurus Gaming | Virtus.pro | 20.3516% | 20.3505% | — |
| 2017-05-01 | MSI | Lyon Gaming | GIGABYTE Marines | 25.8652% | 25.8653% | — |
| 2017-05-01 | MSI | Isurus Gaming | GIGABYTE Marines | 4.1260% | 4.1260% | — |
| 2017-05-01 | MSI | Lyon Gaming | Virtus.pro | 67.4427% | 67.4413% | — |
| 2017-05-01 | MSI | Virtus.pro | GIGABYTE Marines | 14.4147% | 14.4156% | — |
| 2017-05-01 | MSI | Isurus Gaming | Lyon Gaming | 10.9805% | 10.9804% | — |
| 2017-05-03 | MSI | Team SoloMid | GIGABYTE Marines | 51.3424% | 42.6551% | — |
| 2017-05-04 | MSI | Flash Wolves | SuperMassive | 90.0079% | 80.6019% | — |
| 2017-05-06 | MSI | SuperMassive | GIGABYTE Marines | 36.3714% | 53.7687% | — |
| 2017-05-10 | MSI | G2 Esports | SK Telecom T1 | 19.6621% | 33.7859% | — |
| 2017-05-10 | MSI | Team WE | Flash Wolves | 12.8523% | 10.2056% | — |
| 2017-05-10 | MSI | GIGABYTE Marines | Team SoloMid | 44.8418% | 50.6402% | — |
| 2017-05-10 | MSI | Flash Wolves | G2 Esports | 85.4254% | 87.8358% | — |
| 2017-05-10 | MSI | SK Telecom T1 | GIGABYTE Marines | 81.9916% | 63.6205% | — |
| 2017-05-10 | MSI | Team SoloMid | Team WE | 56.0835% | 57.0998% | — |
| 2017-05-11 | MSI | SK Telecom T1 | Team SoloMid | 81.1487% | 70.0212% | — |
| 2017-05-11 | MSI | GIGABYTE Marines | Flash Wolves | 26.3039% | 25.6686% | — |
| 2017-05-11 | MSI | G2 Esports | Team WE | 52.4471% | 53.0875% | — |
| 2017-05-11 | MSI | Flash Wolves | Team SoloMid | 71.6400% | 75.3354% | — |
| 2017-05-11 | MSI | GIGABYTE Marines | G2 Esports | 48.1729% | 51.6633% | — |
| 2017-05-11 | MSI | Team WE | SK Telecom T1 | 16.9650% | 27.1860% | — |
| 2017-05-12 | MSI | G2 Esports | Team SoloMid | 54.0979% | 55.0182% | — |
| 2017-05-12 | MSI | SK Telecom T1 | Flash Wolves | 61.8828% | 43.7351% | — |
| 2017-05-12 | MSI | GIGABYTE Marines | Team WE | 40.5581% | 45.4742% | — |
| 2017-05-12 | MSI | G2 Esports | Flash Wolves | 25.1009% | 22.4176% | — |
| 2017-05-12 | MSI | GIGABYTE Marines | SK Telecom T1 | 12.3749% | 22.5483% | — |
| 2017-05-12 | MSI | Team WE | Team SoloMid | 54.1645% | 53.4574% | — |
| 2017-05-13 | MSI | Team WE | G2 Esports | 49.0188% | 47.7346% | — |
| 2017-05-13 | MSI | Team SoloMid | GIGABYTE Marines | 53.1729% | 49.8202% | — |
| 2017-05-13 | MSI | Flash Wolves | SK Telecom T1 | 27.8919% | 41.7616% | — |
| 2017-05-13 | MSI | G2 Esports | GIGABYTE Marines | 56.3710% | 54.2033% | — |
| 2017-05-13 | MSI | Team SoloMid | SK Telecom T1 | 13.5411% | 20.2055% | — |
| 2017-05-13 | MSI | Flash Wolves | Team WE | 69.3007% | 72.2297% | — |
| 2017-05-14 | MSI | SK Telecom T1 | G2 Esports | 85.0798% | 78.2585% | — |
| 2017-05-14 | MSI | Team SoloMid | Flash Wolves | 30.9293% | 28.5830% | — |
| 2017-05-14 | MSI | Team WE | GIGABYTE Marines | 61.5792% | 58.8384% | — |
| 2017-05-14 | MSI | Team SoloMid | G2 Esports | 53.7701% | 52.2676% | — |
| 2017-05-14 | MSI | Flash Wolves | GIGABYTE Marines | 72.5389% | 72.2632% | — |
| 2017-05-14 | MSI | SK Telecom T1 | Team WE | 78.3466% | 70.5696% | — |
| 2017-05-14 | MSI | Flash Wolves | Team SoloMid | 69.0707% | 71.4170% | — |
| 2017-05-19 | MSI | SK Telecom T1 | Flash Wolves | 66.0269% | 54.8702% | — |
| 2017-05-20 | MSI | Team WE | G2 Esports | 65.6066% | 64.4658% | — |
| 2017-05-21 | MSI | SK Telecom T1 | G2 Esports | 82.4964% | 76.4597% | — |
| 2017-09-23 | Worlds | Team WE | Lyon Gaming | 70.9917% | 55.2460% | — |
| 2017-09-23 | Worlds | Cloud 9 | Team oNe eSports | 69.0588% | 46.0522% | — |
| 2017-09-23 | Worlds | Gambit Esports | Lyon Gaming | 55.1921% | 49.0658% | — |
| 2017-09-23 | Worlds | Dire Wolves | Cloud 9 | 18.1592% | 24.7522% | — |
| 2017-09-23 | Worlds | Gambit Esports | Team WE | 33.4802% | 43.8319% | — |
| 2017-09-23 | Worlds | Dire Wolves | Team oNe eSports | 33.1207% | 21.9238% | — |
| 2017-09-24 | Worlds | Team oNe eSports | Cloud 9 | 21.6254% | 36.8933% | — |
| 2017-09-24 | Worlds | Lyon Gaming | Team WE | 27.2823% | 38.2432% | — |
| 2017-09-24 | Worlds | Cloud 9 | Dire Wolves | 79.1824% | 72.6879% | — |
| 2017-09-24 | Worlds | Lyon Gaming | Gambit Esports | 54.9558% | 58.1495% | — |
| 2017-09-24 | Worlds | Team oNe eSports | Dire Wolves | 51.2079% | 60.8746% | — |
| 2017-09-24 | Worlds | Team WE | Gambit Esports | 76.4809% | 69.1716% | — |
| 2017-09-24 | Worlds | Dire Wolves | Team oNe eSports | 48.7921% | 39.1254% | — |
| 2017-09-25 | Worlds | Young Generation | Kaos Latin Gamers | 50.0000% | 50.0000% | — |
| 2017-09-25 | Worlds | Rampage | Hong Kong Attitude | 28.2322% | 34.2690% | — |
| 2017-09-25 | Worlds | Fnatic | Kaos Latin Gamers | 69.8473% | 67.1996% | — |
| 2017-09-25 | Worlds | Hong Kong Attitude | 1907 Fenerbahce | 36.1392% | 24.8589% | — |
| 2017-09-25 | Worlds | Young Generation | Fnatic | 30.1527% | 32.8004% | — |
| 2017-09-25 | Worlds | Rampage | 1907 Fenerbahce | 18.2083% | 14.7107% | — |
| 2017-09-26 | Worlds | Hong Kong Attitude | Rampage | 77.6953% | 73.6354% | — |
| 2017-09-26 | Worlds | Kaos Latin Gamers | Young Generation | 76.7402% | 76.5522% | — |
| 2017-09-26 | Worlds | 1907 Fenerbahce | Rampage | 91.6223% | 92.9424% | — |
| 2017-09-26 | Worlds | Kaos Latin Gamers | Fnatic | 26.1292% | 27.4920% | — |
| 2017-09-26 | Worlds | 1907 Fenerbahce | Hong Kong Attitude | 75.8433% | 82.5026% | — |
| 2017-09-26 | Worlds | Fnatic | Young Generation | 90.3171% | 89.5949% | — |
| 2017-09-26 | Worlds | Hong Kong Attitude | 1907 Fenerbahce | 24.1567% | 17.4974% | — |
| 2017-09-28 | Worlds | Cloud 9 | Lyon Gaming | 71.6318% | 65.0614% | — |
| 2017-09-28 | Worlds | Fnatic | Hong Kong Attitude | 56.1491% | 55.8433% | — |
| 2017-09-29 | Worlds | 1907 Fenerbahce | Team oNe eSports | 76.8827% | 70.3626% | — |
| 2017-09-29 | Worlds | Team WE | Young Generation | 74.7376% | 70.6605% | — |
| 2017-10-05 | Worlds | Royal Never Give Up | 1907 Fenerbahce | 56.9062% | 43.4011% | — |
| 2017-10-05 | Worlds | G2 Esports | Samsung Galaxy | 24.4904% | 38.3442% | — |
| 2017-10-05 | Worlds | Longzhu Gaming | Immortals | 69.2979% | 54.5902% | — |
| 2017-10-05 | Worlds | Fnatic | GIGABYTE Marines | 58.2451% | 56.6401% | — |
| 2017-10-05 | Worlds | SK Telecom T1 | Cloud 9 | 71.3719% | 58.0918% | — |
| 2017-10-05 | Worlds | Edward Gaming | ahq e-Sports Club | 60.3779% | 56.3964% | — |
| 2017-10-06 | Worlds | Flash Wolves | Team SoloMid | 45.1972% | 46.6237% | — |
| 2017-10-06 | Worlds | Team WE | Misfits | 78.1915% | 75.8683% | — |
| 2017-10-06 | Worlds | Immortals | Fnatic | 58.1478% | 55.0556% | — |
| 2017-10-06 | Worlds | Longzhu Gaming | GIGABYTE Marines | 80.1247% | 66.4837% | — |
| 2017-10-06 | Worlds | ahq e-Sports Club | Cloud 9 | 42.6993% | 44.0590% | — |
| 2017-10-06 | Worlds | Edward Gaming | SK Telecom T1 | 23.1877% | 31.7645% | — |
| 2017-10-07 | Worlds | Team SoloMid | Team WE | 59.1871% | 59.8719% | — |
| 2017-10-07 | Worlds | Flash Wolves | Misfits | 77.8263% | 77.1393% | — |
| 2017-10-07 | Worlds | G2 Esports | 1907 Fenerbahce | 50.0454% | 41.2674% | — |
| 2017-10-07 | Worlds | Samsung Galaxy | Royal Never Give Up | 71.2552% | 60.4778% | — |
| 2017-10-07 | Worlds | SK Telecom T1 | ahq e-Sports Club | 83.8340% | 75.0217% | — |
| 2017-10-07 | Worlds | Cloud 9 | Edward Gaming | 55.9679% | 58.0486% | — |
| 2017-10-08 | Worlds | Team WE | Flash Wolves | 54.9347% | 52.6337% | — |
| 2017-10-08 | Worlds | Misfits | Team SoloMid | 16.4601% | 17.9740% | — |
| 2017-10-08 | Worlds | GIGABYTE Marines | Immortals | 34.6709% | 37.8775% | — |
| 2017-10-08 | Worlds | Fnatic | Longzhu Gaming | 20.1738% | 31.5008% | — |
| 2017-10-08 | Worlds | 1907 Fenerbahce | Samsung Galaxy | 18.4720% | 34.7536% | — |
| 2017-10-08 | Worlds | Royal Never Give Up | G2 Esports | 59.8826% | 57.0824% | — |
| 2017-10-12 | Worlds | Immortals | GIGABYTE Marines | 68.2768% | 65.3357% | — |
| 2017-10-12 | Worlds | Longzhu Gaming | Fnatic | 81.0884% | 71.0616% | — |
| 2017-10-12 | Worlds | Fnatic | Immortals | 36.8141% | 39.1634% | — |
| 2017-10-12 | Worlds | GIGABYTE Marines | Longzhu Gaming | 15.6819% | 25.1288% | — |
| 2017-10-12 | Worlds | GIGABYTE Marines | Fnatic | 44.3660% | 45.1806% | — |
| 2017-10-12 | Worlds | Immortals | Longzhu Gaming | 28.5862% | 38.7478% | — |
| 2017-10-12 | Worlds | Fnatic | Immortals | 36.8141% | 39.1634% | — |
| 2017-10-12 | Worlds | GIGABYTE Marines | Fnatic | 44.3660% | 45.1806% | — |
| 2017-10-13 | Worlds | G2 Esports | Royal Never Give Up | 38.4235% | 40.6882% | — |
| 2017-10-13 | Worlds | Samsung Galaxy | 1907 Fenerbahce | 84.3385% | 71.4980% | — |
| 2017-10-13 | Worlds | Samsung Galaxy | G2 Esports | 77.3161% | 67.6382% | — |
| 2017-10-13 | Worlds | 1907 Fenerbahce | Royal Never Give Up | 28.3128% | 36.3693% | — |
| 2017-10-13 | Worlds | 1907 Fenerbahce | G2 Esports | 38.7606% | 45.4500% | — |
| 2017-10-13 | Worlds | Royal Never Give Up | Samsung Galaxy | 31.9813% | 41.0881% | — |
| 2017-10-14 | Worlds | Misfits | Flash Wolves | 36.0776% | 36.4662% | — |
| 2017-10-14 | Worlds | Team WE | Team SoloMid | 45.4832% | 44.8239% | — |
| 2017-10-14 | Worlds | Flash Wolves | Team WE | 40.4823% | 42.6080% | — |
| 2017-10-14 | Worlds | Team SoloMid | Misfits | 75.7418% | 74.2851% | — |
| 2017-10-14 | Worlds | Team SoloMid | Flash Wolves | 63.7973% | 62.3787% | — |
| 2017-10-14 | Worlds | Misfits | Team WE | 27.7397% | 29.8793% | — |
| 2017-10-14 | Worlds | Misfits | Team SoloMid | 24.2582% | 25.7149% | — |
| 2017-10-15 | Worlds | ahq e-Sports Club | SK Telecom T1 | 13.4454% | 19.6909% | — |
| 2017-10-15 | Worlds | Edward Gaming | Cloud 9 | 50.1532% | 48.0860% | — |
| 2017-10-15 | Worlds | ahq e-Sports Club | Edward Gaming | 35.0992% | 38.0228% | — |
| 2017-10-15 | Worlds | Cloud 9 | SK Telecom T1 | 22.2080% | 30.1419% | — |
| 2017-10-15 | Worlds | Cloud 9 | ahq e-Sports Club | 64.7611% | 63.7650% | — |
| 2017-10-15 | Worlds | SK Telecom T1 | Edward Gaming | 77.6859% | 71.4460% | — |
| 2017-10-19 | Worlds | Longzhu Gaming | Samsung Galaxy | 54.9960% | 54.7629% | — |
| 2017-10-20 | Worlds | SK Telecom T1 | Misfits | 86.5734% | 80.8362% | — |
| 2017-10-21 | Worlds | Fnatic | Royal Never Give Up | 37.6785% | 39.8645% | — |
| 2017-10-22 | Worlds | Team WE | Cloud 9 | 60.5680% | 59.7210% | — |
| 2017-10-28 | Worlds | Royal Never Give Up | SK Telecom T1 | 36.9633% | 43.3966% | — |
| 2017-10-29 | Worlds | Team WE | Samsung Galaxy | 35.5256% | 43.3579% | — |
| 2017-11-04 | Worlds | Samsung Galaxy | SK Telecom T1 | 50.8443% | 49.5546% | — |


## S8

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 149 | 62.42% | 62.18% | 0.6484 | 0.2268 |
| 中性先验 · 90 天 | 149 | 55.70% | 54.92% | 0.7242 | 0.2589 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2018-05-03 | MSI | Gambit Esports | Kaos Latin Gamers | 46.1063% | 56.7120% | — |
| 2018-05-03 | MSI | Rainbow7 | Ascension Gaming | 73.2920% | 81.5634% | — |
| 2018-05-03 | MSI | Gambit Esports | Ascension Gaming | 64.9505% | 86.6580% | — |
| 2018-05-03 | MSI | Rainbow7 | Kaos Latin Gamers | 55.8866% | 47.1556% | — |
| 2018-05-03 | MSI | Kaos Latin Gamers | Ascension Gaming | 68.4154% | 83.2150% | — |
| 2018-05-03 | MSI | Rainbow7 | Gambit Esports | 59.6915% | 40.5160% | — |
| 2018-05-04 | MSI | BAUSuperMassive | Dire Wolves | 76.4222% | 56.1930% | — |
| 2018-05-04 | MSI | KaBuM! e-Sports | Pentagram | 62.5527% | 41.7012% | — |
| 2018-05-04 | MSI | BAUSuperMassive | Pentagram | 89.5017% | 67.9821% | — |
| 2018-05-04 | MSI | KaBuM! e-Sports | Dire Wolves | 38.8411% | 30.1745% | — |
| 2018-05-04 | MSI | Dire Wolves | Pentagram | 72.4536% | 62.3388% | — |
| 2018-05-04 | MSI | KaBuM! e-Sports | BAUSuperMassive | 16.3835% | 25.1995% | — |
| 2018-05-05 | MSI | Ascension Gaming | Gambit Esports | 6.9388% | 3.5603% | — |
| 2018-05-05 | MSI | Kaos Latin Gamers | Rainbow7 | 59.2765% | 64.5148% | — |
| 2018-05-05 | MSI | Ascension Gaming | Rainbow7 | 14.6843% | 12.1794% | — |
| 2018-05-05 | MSI | Kaos Latin Gamers | Gambit Esports | 38.6714% | 32.6129% | — |
| 2018-05-05 | MSI | Gambit Esports | Rainbow7 | 69.7739% | 78.9767% | — |
| 2018-05-05 | MSI | Ascension Gaming | Kaos Latin Gamers | 10.5742% | 7.0875% | — |
| 2018-05-06 | MSI | Pentagram | BAUSuperMassive | 5.2261% | 12.6842% | — |
| 2018-05-06 | MSI | Dire Wolves | KaBuM! e-Sports | 68.3074% | 72.5066% | — |
| 2018-05-06 | MSI | Pentagram | KaBuM! e-Sports | 29.7854% | 42.1745% | — |
| 2018-05-06 | MSI | Dire Wolves | BAUSuperMassive | 21.8855% | 34.4381% | — |
| 2018-05-06 | MSI | BAUSuperMassive | KaBuM! e-Sports | 88.4962% | 83.3906% | — |
| 2018-05-06 | MSI | Pentagram | Dire Wolves | 16.4452% | 21.6641% | — |
| 2018-05-08 | MSI | EVOS Esports | BAUSuperMassive | 36.5138% | 23.5863% | — |
| 2018-05-09 | MSI | Flash Wolves | Gambit Esports | 57.2190% | 36.1967% | — |
| 2018-05-11 | MSI | Fnatic | Royal Never Give Up | 53.4881% | 64.4003% | — |
| 2018-05-11 | MSI | EVOS Esports | Flash Wolves | 36.9071% | 33.9015% | — |
| 2018-05-11 | MSI | Kingzone DragonX | Team Liquid | 85.4209% | 62.5162% | — |
| 2018-05-11 | MSI | Flash Wolves | Fnatic | 46.2655% | 74.5962% | — |
| 2018-05-11 | MSI | Team Liquid | EVOS Esports | 51.1551% | 31.8941% | — |
| 2018-05-11 | MSI | Royal Never Give Up | Kingzone DragonX | 21.9582% | 31.9698% | — |
| 2018-05-12 | MSI | Kingzone DragonX | Fnatic | 85.8529% | 71.5704% | — |
| 2018-05-12 | MSI | Royal Never Give Up | EVOS Esports | 63.7017% | 28.9729% | — |
| 2018-05-12 | MSI | Team Liquid | Flash Wolves | 23.1785% | 11.9838% | — |
| 2018-05-12 | MSI | EVOS Esports | Kingzone DragonX | 12.7239% | 48.3865% | — |
| 2018-05-12 | MSI | Flash Wolves | Royal Never Give Up | 57.6137% | 86.2290% | — |
| 2018-05-12 | MSI | Fnatic | Team Liquid | 61.0961% | 54.9224% | — |
| 2018-05-13 | MSI | Royal Never Give Up | Team Liquid | 75.6487% | 63.8669% | — |
| 2018-05-13 | MSI | EVOS Esports | Fnatic | 29.8444% | 48.2839% | — |
| 2018-05-13 | MSI | Kingzone DragonX | Flash Wolves | 60.9717% | 25.3886% | — |
| 2018-05-13 | MSI | Royal Never Give Up | Fnatic | 47.6975% | 40.7407% | — |
| 2018-05-13 | MSI | Flash Wolves | EVOS Esports | 79.6964% | 81.2640% | — |
| 2018-05-13 | MSI | Team Liquid | Kingzone DragonX | 10.1150% | 22.0136% | — |
| 2018-05-14 | MSI | Kingzone DragonX | Royal Never Give Up | 72.1811% | 66.9811% | — |
| 2018-05-14 | MSI | Fnatic | Flash Wolves | 29.1539% | 16.7057% | — |
| 2018-05-14 | MSI | EVOS Esports | Team Liquid | 50.1627% | 63.4174% | — |
| 2018-05-14 | MSI | Royal Never Give Up | Flash Wolves | 27.6622% | 12.3893% | — |
| 2018-05-14 | MSI | Kingzone DragonX | EVOS Esports | 85.6871% | 63.8804% | — |
| 2018-05-14 | MSI | Team Liquid | Fnatic | 28.5785% | 31.8115% | — |
| 2018-05-15 | MSI | Fnatic | Kingzone DragonX | 32.7699% | 44.2985% | — |
| 2018-05-15 | MSI | EVOS Esports | Royal Never Give Up | 21.6178% | 39.3013% | — |
| 2018-05-15 | MSI | Flash Wolves | Team Liquid | 73.2190% | 80.4435% | — |
| 2018-05-15 | MSI | Fnatic | EVOS Esports | 74.6994% | 62.7182% | — |
| 2018-05-15 | MSI | Flash Wolves | Kingzone DragonX | 42.7600% | 67.3783% | — |
| 2018-05-15 | MSI | Team Liquid | Royal Never Give Up | 31.3408% | 40.7487% | — |
| 2018-05-15 | MSI | Flash Wolves | Royal Never Give Up | 55.5156% | 73.8827% | — |
| 2018-05-15 | MSI | Fnatic | Team Liquid | 64.0792% | 61.2977% | — |
| 2018-05-18 | MSI | Fnatic | Royal Never Give Up | 36.2912% | 41.6836% | — |
| 2018-05-19 | MSI | Flash Wolves | Kingzone DragonX | 40.3059% | 60.7655% | — |
| 2018-05-20 | MSI | Royal Never Give Up | Kingzone DragonX | 44.6897% | 46.7788% | — |
| 2018-10-01 | Worlds | Cloud9 | KaBuM! e-Sports | 59.3901% | 25.0277% | — |
| 2018-10-01 | Worlds | Gambit Esports | G-Rex | 55.3155% | 79.1095% | — |
| 2018-10-01 | Worlds | Detonation FocusMe | KaBuM! e-Sports | 29.3086% | 42.2145% | — |
| 2018-10-01 | Worlds | G-Rex | Kaos Latin Gamers | 44.0579% | 19.7662% | — |
| 2018-10-01 | Worlds | Detonation FocusMe | Cloud9 | 22.0878% | 68.6361% | — |
| 2018-10-01 | Worlds | Gambit Esports | Kaos Latin Gamers | 49.3653% | 48.2647% | — |
| 2018-10-02 | Worlds | Edward Gaming | Infinity eSports | 85.9286% | 51.1209% | — |
| 2018-10-02 | Worlds | G2 Esports | BAUSuperMassive | 58.6893% | 31.3043% | — |
| 2018-10-02 | Worlds | Dire Wolves | Infinity eSports | 55.4040% | 65.7220% | — |
| 2018-10-02 | Worlds | Ascension Gaming | BAUSuperMassive | 14.4523% | 18.8809% | — |
| 2018-10-02 | Worlds | Dire Wolves | Edward Gaming | 16.9051% | 64.7048% | — |
| 2018-10-02 | Worlds | Ascension Gaming | G2 Esports | 10.6276% | 33.8085% | — |
| 2018-10-03 | Worlds | G-Rex | Gambit Esports | 53.8365% | 32.9620% | — |
| 2018-10-03 | Worlds | KaBuM! e-Sports | Detonation FocusMe | 57.4254% | 47.7180% | — |
| 2018-10-03 | Worlds | Kaos Latin Gamers | Gambit Esports | 41.0370% | 41.0861% | — |
| 2018-10-03 | Worlds | KaBuM! e-Sports | Cloud9 | 27.3373% | 52.5593% | — |
| 2018-10-03 | Worlds | Kaos Latin Gamers | G-Rex | 37.3741% | 58.6496% | — |
| 2018-10-03 | Worlds | Cloud9 | Detonation FocusMe | 78.1905% | 45.1699% | — |
| 2018-10-03 | Worlds | Detonation FocusMe | KaBuM! e-Sports | 42.5746% | 52.2820% | — |
| 2018-10-04 | Worlds | BAUSuperMassive | G2 Esports | 48.6906% | 69.7004% | — |
| 2018-10-04 | Worlds | Infinity eSports | Edward Gaming | 10.3086% | 33.8357% | — |
| 2018-10-04 | Worlds | BAUSuperMassive | Ascension Gaming | 89.9943% | 88.4773% | — |
| 2018-10-04 | Worlds | Infinity eSports | Dire Wolves | 36.7211% | 30.0299% | — |
| 2018-10-04 | Worlds | G2 Esports | Ascension Gaming | 90.4562% | 76.9476% | — |
| 2018-10-04 | Worlds | Edward Gaming | Dire Wolves | 83.4684% | 45.6299% | — |
| 2018-10-04 | Worlds | G2 Esports | BAUSuperMassive | 51.3094% | 30.2996% | — |
| 2018-10-06 | Worlds | Cloud9 | Gambit Esports | 74.5487% | 56.2745% | — |
| 2018-10-06 | Worlds | Detonation FocusMe | Edward Gaming | 10.3158% | 40.6864% | — |
| 2018-10-07 | Worlds | G2 Esports | Infinity eSports | 69.8481% | 49.2725% | — |
| 2018-10-07 | Worlds | G-Rex | BAUSuperMassive | 47.3694% | 39.4326% | — |
| 2018-10-10 | Worlds | KT Rolster | Team Liquid | 73.1230% | 51.4649% | — |
| 2018-10-10 | Worlds | Edward Gaming | MAD Team | 78.6513% | 67.1678% | — |
| 2018-10-10 | Worlds | Phong Vu Buffalo | Flash Wolves | 24.5995% | 31.6313% | — |
| 2018-10-10 | Worlds | Afreeca Freecs | G2 Esports | 73.2628% | 52.1304% | — |
| 2018-10-10 | Worlds | Royal Never Give Up | Cloud9 | 79.5567% | 64.2235% | — |
| 2018-10-10 | Worlds | Gen.G eSports | Team Vitality | 76.2086% | 58.9534% | — |
| 2018-10-11 | Worlds | Flash Wolves | Afreeca Freecs | 57.0968% | 75.7181% | — |
| 2018-10-11 | Worlds | Phong Vu Buffalo | G2 Esports | 40.5835% | 50.8229% | — |
| 2018-10-11 | Worlds | 100 Thieves | Fnatic | 23.6322% | 27.2447% | — |
| 2018-10-11 | Worlds | Invictus Gaming | G-Rex | 86.6990% | 75.3841% | — |
| 2018-10-11 | Worlds | Team Vitality | Cloud9 | 61.9988% | 51.3962% | — |
| 2018-10-11 | Worlds | Gen.G eSports | Royal Never Give Up | 41.7730% | 33.1823% | — |
| 2018-10-12 | Worlds | MAD Team | KT Rolster | 15.8482% | 32.2621% | — |
| 2018-10-12 | Worlds | Team Liquid | Edward Gaming | 35.7273% | 43.3769% | — |
| 2018-10-12 | Worlds | Fnatic | Invictus Gaming | 30.4528% | 37.4683% | — |
| 2018-10-12 | Worlds | 100 Thieves | G-Rex | 48.8253% | 42.6971% | — |
| 2018-10-12 | Worlds | Royal Never Give Up | Team Vitality | 77.6079% | 72.1927% | — |
| 2018-10-12 | Worlds | Cloud9 | Gen.G eSports | 29.3714% | 52.6153% | — |
| 2018-10-13 | Worlds | Afreeca Freecs | Phong Vu Buffalo | 66.2556% | 41.0120% | — |
| 2018-10-13 | Worlds | G2 Esports | Flash Wolves | 24.6610% | 24.3714% | — |
| 2018-10-13 | Worlds | Invictus Gaming | 100 Thieves | 88.6748% | 83.4369% | — |
| 2018-10-13 | Worlds | G-Rex | Fnatic | 24.2281% | 32.3080% | — |
| 2018-10-13 | Worlds | Team Liquid | MAD Team | 70.1722% | 66.0393% | — |
| 2018-10-13 | Worlds | KT Rolster | Edward Gaming | 55.3603% | 46.0985% | — |
| 2018-10-14 | Worlds | Team Vitality | Royal Never Give Up | 21.1684% | 25.8043% | — |
| 2018-10-14 | Worlds | Gen.G eSports | Cloud9 | 74.1935% | 55.0302% | — |
| 2018-10-14 | Worlds | Team Vitality | Gen.G eSports | 30.2908% | 42.1930% | — |
| 2018-10-14 | Worlds | Cloud9 | Royal Never Give Up | 17.6919% | 28.0254% | — |
| 2018-10-14 | Worlds | Cloud9 | Team Vitality | 44.4588% | 52.8212% | — |
| 2018-10-14 | Worlds | Royal Never Give Up | Gen.G eSports | 61.8059% | 67.7282% | — |
| 2018-10-14 | Worlds | Royal Never Give Up | Cloud9 | 82.3081% | 71.9746% | — |
| 2018-10-15 | Worlds | Afreeca Freecs | Flash Wolves | 43.8108% | 29.2178% | — |
| 2018-10-15 | Worlds | G2 Esports | Phong Vu Buffalo | 58.2732% | 51.2645% | — |
| 2018-10-15 | Worlds | Flash Wolves | G2 Esports | 64.9670% | 66.2066% | — |
| 2018-10-15 | Worlds | Phong Vu Buffalo | Afreeca Freecs | 33.1204% | 54.0343% | — |
| 2018-10-15 | Worlds | Flash Wolves | Phong Vu Buffalo | 72.1435% | 67.3291% | — |
| 2018-10-15 | Worlds | G2 Esports | Afreeca Freecs | 40.8845% | 55.2880% | — |
| 2018-10-15 | Worlds | Flash Wolves | G2 Esports | 64.9670% | 66.2066% | — |
| 2018-10-16 | Worlds | Team Liquid | KT Rolster | 31.0245% | 42.8386% | — |
| 2018-10-16 | Worlds | MAD Team | Edward Gaming | 14.5583% | 21.0542% | — |
| 2018-10-16 | Worlds | MAD Team | Team Liquid | 20.5438% | 24.6810% | — |
| 2018-10-16 | Worlds | Edward Gaming | KT Rolster | 40.5658% | 47.9393% | — |
| 2018-10-16 | Worlds | Edward Gaming | Team Liquid | 60.2771% | 55.1309% | — |
| 2018-10-16 | Worlds | KT Rolster | MAD Team | 89.5820% | 80.2839% | — |
| 2018-10-17 | Worlds | Fnatic | 100 Thieves | 73.3871% | 71.4551% | — |
| 2018-10-17 | Worlds | G-Rex | Invictus Gaming | 8.7994% | 15.2559% | — |
| 2018-10-17 | Worlds | Fnatic | G-Rex | 83.3864% | 77.0402% | — |
| 2018-10-17 | Worlds | 100 Thieves | Invictus Gaming | 14.9381% | 19.4399% | — |
| 2018-10-17 | Worlds | G-Rex | 100 Thieves | 35.4593% | 42.7271% | — |
| 2018-10-17 | Worlds | Invictus Gaming | Fnatic | 67.3731% | 62.3419% | — |
| 2018-10-17 | Worlds | Fnatic | Invictus Gaming | 32.6269% | 37.6581% | — |
| 2018-10-20 | Worlds | KT Rolster | Invictus Gaming | 43.6258% | 38.8754% | — |
| 2018-10-20 | Worlds | Royal Never Give Up | G2 Esports | 70.8712% | 64.1557% | — |
| 2018-10-21 | Worlds | Cloud9 | Afreeca Freecs | 38.5446% | 52.3835% | — |
| 2018-10-21 | Worlds | Fnatic | Edward Gaming | 62.0095% | 63.3388% | — |
| 2018-10-27 | Worlds | Invictus Gaming | G2 Esports | 68.0674% | 62.1424% | — |
| 2018-10-28 | Worlds | Fnatic | Cloud9 | 66.4861% | 62.0623% | — |
| 2018-11-03 | Worlds | Fnatic | Invictus Gaming | 48.8020% | 52.5111% | — |


## S9

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 149 | 72.48% | 68.34% | 0.6270 | 0.2177 |
| 中性先验 · 90 天 | 149 | 57.72% | 55.28% | 0.7083 | 0.2554 |
| 无正则 MLE · 可识别子集 | 5 | 40.00% | 40.00% | 0.8406 | 0.3195 |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2019-05-01 | MSI | Dashing Buffalo | Bombers | 44.0612% | 32.9364% | — |
| 2019-05-01 | MSI | 1907 Fenerbahce | Isurus Gaming | 90.8234% | 86.1605% | — |
| 2019-05-01 | MSI | Dashing Buffalo | Isurus Gaming | 73.3237% | 63.1689% | — |
| 2019-05-01 | MSI | 1907 Fenerbahce | Bombers | 73.9329% | 64.0643% | — |
| 2019-05-01 | MSI | Bombers | Isurus Gaming | 77.7262% | 77.7392% | — |
| 2019-05-01 | MSI | 1907 Fenerbahce | Dashing Buffalo | 78.2647% | 78.4015% | — |
| 2019-05-01 | MSI | Bombers | Dashing Buffalo | 55.9388% | 67.0636% | — |
| 2019-05-01 | MSI | Isurus Gaming | 1907 Fenerbahce | 9.1766% | 13.8395% | — |
| 2019-05-02 | MSI | Isurus Gaming | Dashing Buffalo | 20.6353% | 25.2556% | 12.6595% |
| 2019-05-02 | MSI | Bombers | 1907 Fenerbahce | 40.7801% | 45.8026% | 60.0497% |
| 2019-05-02 | MSI | Dashing Buffalo | 1907 Fenerbahce | 46.8849% | 46.6629% | 76.3049% |
| 2019-05-02 | MSI | Isurus Gaming | Bombers | 24.9974% | 25.9145% | 23.6951% |
| 2019-05-02 | MSI | MEGA | Detonation FocusMe | 31.8541% | 38.8369% | — |
| 2019-05-02 | MSI | Vega Squadron | INTZ eSports | 82.7959% | 71.0673% | — |
| 2019-05-02 | MSI | Vega Squadron | Detonation FocusMe | 53.2201% | 34.9775% | — |
| 2019-05-02 | MSI | MEGA | INTZ eSports | 66.4133% | 74.3552% | — |
| 2019-05-02 | MSI | Dashing Buffalo | 1907 Fenerbahce | 46.8849% | 46.6629% | 76.3049% |
| 2019-05-05 | MSI | Detonation FocusMe | INTZ eSports | 83.9883% | 84.0383% | — |
| 2019-05-05 | MSI | Vega Squadron | MEGA | 79.3201% | 65.0387% | — |
| 2019-05-05 | MSI | Detonation FocusMe | MEGA | 68.3272% | 63.5316% | — |
| 2019-05-05 | MSI | INTZ eSports | Vega Squadron | 9.6840% | 15.1007% | — |
| 2019-05-05 | MSI | INTZ eSports | MEGA | 29.1418% | 24.8620% | — |
| 2019-05-05 | MSI | Detonation FocusMe | Vega Squadron | 35.9974% | 48.3594% | — |
| 2019-05-05 | MSI | INTZ eSports | Detonation FocusMe | 16.0117% | 15.9617% | — |
| 2019-05-05 | MSI | MEGA | Vega Squadron | 20.6799% | 34.9613% | — |
| 2019-05-06 | MSI | Team Liquid | Dashing Buffalo | 52.8658% | 30.6073% | — |
| 2019-05-06 | MSI | Flash Wolves | Vega Squadron | 22.3873% | 14.4165% | — |
| 2019-05-07 | MSI | Dashing Buffalo | Vega Squadron | 53.2085% | 47.0120% | — |
| 2019-05-10 | MSI | G2 Esports | SK Telecom T1 | 50.1670% | 39.6643% | — |
| 2019-05-10 | MSI | Flash Wolves | Team Liquid | 22.9203% | 32.5915% | — |
| 2019-05-10 | MSI | Dashing Buffalo | Invictus Gaming | 26.7338% | 63.8364% | — |
| 2019-05-10 | MSI | SK Telecom T1 | Flash Wolves | 75.3743% | 59.6268% | — |
| 2019-05-10 | MSI | Invictus Gaming | G2 Esports | 53.4704% | 45.1908% | — |
| 2019-05-10 | MSI | Team Liquid | Dashing Buffalo | 72.2440% | 59.4101% | — |
| 2019-05-11 | MSI | G2 Esports | Team Liquid | 44.4184% | 29.1567% | — |
| 2019-05-11 | MSI | Dashing Buffalo | Flash Wolves | 58.4948% | 60.7742% | — |
| 2019-05-11 | MSI | Team Liquid | Invictus Gaming | 46.4686% | 67.6893% | — |
| 2019-05-11 | MSI | SK Telecom T1 | Dashing Buffalo | 69.9723% | 53.2344% | — |
| 2019-05-11 | MSI | Flash Wolves | G2 Esports | 20.5596% | 41.9591% | — |
| 2019-05-11 | MSI | Invictus Gaming | SK Telecom T1 | 62.9079% | 47.6349% | — |
| 2019-05-12 | MSI | Team Liquid | SK Telecom T1 | 49.9612% | 53.0647% | — |
| 2019-05-12 | MSI | Flash Wolves | Invictus Gaming | 13.0858% | 30.8028% | — |
| 2019-05-12 | MSI | Dashing Buffalo | G2 Esports | 17.0642% | 34.0642% | — |
| 2019-05-12 | MSI | Team Liquid | Flash Wolves | 75.4013% | 66.8570% | — |
| 2019-05-12 | MSI | SK Telecom T1 | G2 Esports | 38.0743% | 44.6676% | — |
| 2019-05-12 | MSI | Invictus Gaming | Dashing Buffalo | 86.6041% | 66.3002% | — |
| 2019-05-13 | MSI | G2 Esports | Flash Wolves | 78.1305% | 65.5310% | — |
| 2019-05-13 | MSI | Dashing Buffalo | Team Liquid | 34.3144% | 44.3336% | — |
| 2019-05-13 | MSI | G2 Esports | Invictus Gaming | 37.0589% | 43.4828% | — |
| 2019-05-13 | MSI | Flash Wolves | SK Telecom T1 | 27.4155% | 37.2820% | — |
| 2019-05-13 | MSI | Invictus Gaming | Team Liquid | 76.4258% | 64.2788% | — |
| 2019-05-13 | MSI | Dashing Buffalo | SK Telecom T1 | 26.9700% | 39.3978% | — |
| 2019-05-14 | MSI | SK Telecom T1 | Team Liquid | 61.7083% | 59.5946% | — |
| 2019-05-14 | MSI | G2 Esports | Dashing Buffalo | 79.9567% | 66.4001% | — |
| 2019-05-14 | MSI | Invictus Gaming | Flash Wolves | 89.0850% | 77.9673% | — |
| 2019-05-14 | MSI | Team Liquid | G2 Esports | 35.0222% | 41.9218% | — |
| 2019-05-14 | MSI | Flash Wolves | Dashing Buffalo | 50.1009% | 46.9276% | — |
| 2019-05-14 | MSI | SK Telecom T1 | Invictus Gaming | 29.7176% | 40.2052% | — |
| 2019-05-17 | MSI | Invictus Gaming | Team Liquid | 75.4232% | 65.9552% | — |
| 2019-05-18 | MSI | SK Telecom T1 | G2 Esports | 61.3434% | 64.0350% | — |
| 2019-05-19 | MSI | G2 Esports | Team Liquid | 50.7261% | 48.2405% | — |
| 2019-10-02 | Worlds | Clutch Gaming | Unicorns Of Love | 35.1350% | 17.5485% | — |
| 2019-10-02 | Worlds | Detonation FocusMe | Splyce | 36.7158% | 77.3749% | — |
| 2019-10-02 | Worlds | Mammoth eSports | Unicorns Of Love | 26.5625% | 33.4292% | — |
| 2019-10-02 | Worlds | Detonation FocusMe | Isurus Gaming | 63.7632% | 71.4634% | — |
| 2019-10-02 | Worlds | Mammoth eSports | Clutch Gaming | 40.0394% | 70.2326% | — |
| 2019-10-02 | Worlds | Splyce | Isurus Gaming | 75.2041% | 42.2723% | — |
| 2019-10-03 | Worlds | Royal Youth | DAMWON Gaming | 39.0866% | 59.8457% | — |
| 2019-10-03 | Worlds | MEGA | Hong Kong Attitude | 45.1529% | 74.4107% | — |
| 2019-10-03 | Worlds | DAMWON Gaming | Flamengo eSports | 81.5058% | 49.5015% | — |
| 2019-10-03 | Worlds | MEGA | Lowkey Esports.Vietnam | 48.9831% | 73.9285% | — |
| 2019-10-03 | Worlds | Royal Youth | Flamengo eSports | 73.8762% | 59.3656% | — |
| 2019-10-03 | Worlds | Hong Kong Attitude | Lowkey Esports.Vietnam | 53.8378% | 49.3709% | — |
| 2019-10-04 | Worlds | Unicorns Of Love | Clutch Gaming | 59.5771% | 74.4062% | — |
| 2019-10-04 | Worlds | Splyce | Detonation FocusMe | 76.2505% | 46.7717% | — |
| 2019-10-04 | Worlds | Unicorns Of Love | Mammoth eSports | 66.6598% | 61.3185% | — |
| 2019-10-04 | Worlds | Isurus Gaming | Detonation FocusMe | 49.7168% | 44.3156% | — |
| 2019-10-04 | Worlds | Clutch Gaming | Mammoth eSports | 57.5655% | 35.2864% | — |
| 2019-10-04 | Worlds | Isurus Gaming | Splyce | 23.5449% | 47.5257% | — |
| 2019-10-04 | Worlds | Mammoth eSports | Unicorns Of Love | 33.3402% | 38.6815% | — |
| 2019-10-04 | Worlds | Clutch Gaming | Unicorns Of Love | 40.4229% | 25.5938% | — |
| 2019-10-05 | Worlds | DAMWON Gaming | Royal Youth | 74.4018% | 59.3912% | — |
| 2019-10-05 | Worlds | Hong Kong Attitude | MEGA | 53.2412% | 32.4009% | — |
| 2019-10-05 | Worlds | Flamengo eSports | DAMWON Gaming | 19.9305% | 43.9843% | — |
| 2019-10-05 | Worlds | Lowkey Esports.Vietnam | MEGA | 50.1464% | 32.5336% | — |
| 2019-10-05 | Worlds | Flamengo eSports | Royal Youth | 41.9778% | 53.4535% | — |
| 2019-10-05 | Worlds | Lowkey Esports.Vietnam | Hong Kong Attitude | 46.9046% | 50.1513% | — |
| 2019-10-05 | Worlds | Royal Youth | Flamengo eSports | 58.0222% | 46.5465% | — |
| 2019-10-07 | Worlds | Lowkey Esports.Vietnam | DAMWON Gaming | 18.0108% | 27.7913% | — |
| 2019-10-07 | Worlds | Clutch Gaming | Royal Youth | 46.9939% | 33.9691% | — |
| 2019-10-08 | Worlds | Hong Kong Attitude | Isurus Gaming | 63.4779% | 53.6547% | — |
| 2019-10-08 | Worlds | Unicorns Of Love | Splyce | 43.3983% | 57.7116% | — |
| 2019-10-12 | Worlds | Fnatic | SK Telecom T1 | 47.1810% | 46.1604% | — |
| 2019-10-12 | Worlds | Royal Never Give Up | Clutch Gaming | 72.8279% | 57.7231% | — |
| 2019-10-12 | Worlds | Invictus Gaming | ahq e-Sports Club | 74.8359% | 54.4896% | — |
| 2019-10-12 | Worlds | DAMWON Gaming | Team Liquid | 54.3150% | 55.4692% | — |
| 2019-10-12 | Worlds | J Team | Funplus Phoenix | 18.2162% | 36.8366% | — |
| 2019-10-12 | Worlds | GAM Esports | Splyce | 38.7545% | 48.3868% | — |
| 2019-10-13 | Worlds | SK Telecom T1 | Royal Never Give Up | 55.4871% | 65.9838% | — |
| 2019-10-13 | Worlds | Fnatic | Clutch Gaming | 73.2296% | 69.9118% | — |
| 2019-10-13 | Worlds | Team Liquid | Invictus Gaming | 50.2998% | 60.0981% | — |
| 2019-10-13 | Worlds | ahq e-Sports Club | DAMWON Gaming | 26.1182% | 32.0770% | — |
| 2019-10-13 | Worlds | Griffin | G2 Esports | 44.7503% | 45.7897% | — |
| 2019-10-13 | Worlds | Cloud9 | Hong Kong Attitude | 57.8484% | 47.2022% | — |
| 2019-10-14 | Worlds | Invictus Gaming | DAMWON Gaming | 49.0972% | 38.5541% | — |
| 2019-10-14 | Worlds | ahq e-Sports Club | Team Liquid | 24.6966% | 31.5041% | — |
| 2019-10-14 | Worlds | Funplus Phoenix | Splyce | 76.8977% | 66.6305% | — |
| 2019-10-14 | Worlds | J Team | GAM Esports | 66.2337% | 63.4859% | — |
| 2019-10-14 | Worlds | Griffin | Hong Kong Attitude | 76.2625% | 67.1831% | — |
| 2019-10-14 | Worlds | G2 Esports | Cloud9 | 73.4026% | 71.5592% | — |
| 2019-10-15 | Worlds | Royal Never Give Up | Fnatic | 44.2120% | 35.6048% | — |
| 2019-10-15 | Worlds | Clutch Gaming | SK Telecom T1 | 19.7863% | 22.1990% | — |
| 2019-10-15 | Worlds | Funplus Phoenix | GAM Esports | 84.8434% | 71.0403% | — |
| 2019-10-15 | Worlds | Splyce | J Team | 56.5231% | 50.0577% | — |
| 2019-10-15 | Worlds | Cloud9 | Griffin | 30.9712% | 32.0615% | — |
| 2019-10-15 | Worlds | Hong Kong Attitude | G2 Esports | 14.6330% | 21.6699% | — |
| 2019-10-17 | Worlds | GAM Esports | Funplus Phoenix | 13.4166% | 24.9328% | — |
| 2019-10-17 | Worlds | J Team | Splyce | 50.8253% | 56.2676% | — |
| 2019-10-17 | Worlds | GAM Esports | J Team | 40.1449% | 42.4345% | — |
| 2019-10-17 | Worlds | Splyce | Funplus Phoenix | 18.2694% | 25.9366% | — |
| 2019-10-17 | Worlds | Splyce | GAM Esports | 59.0593% | 51.3230% | — |
| 2019-10-17 | Worlds | Funplus Phoenix | J Team | 81.2324% | 68.9383% | — |
| 2019-10-17 | Worlds | Funplus Phoenix | Splyce | 81.7306% | 74.0634% | — |
| 2019-10-18 | Worlds | Griffin | Cloud9 | 72.6358% | 71.7823% | — |
| 2019-10-18 | Worlds | G2 Esports | Hong Kong Attitude | 85.6711% | 79.3407% | — |
| 2019-10-18 | Worlds | Hong Kong Attitude | Griffin | 17.8491% | 24.4707% | — |
| 2019-10-18 | Worlds | Cloud9 | G2 Esports | 22.4810% | 24.0081% | — |
| 2019-10-18 | Worlds | Hong Kong Attitude | Cloud9 | 36.5776% | 45.1812% | — |
| 2019-10-18 | Worlds | G2 Esports | Griffin | 56.5037% | 55.4420% | — |
| 2019-10-18 | Worlds | G2 Esports | Griffin | 56.5037% | 55.4420% | — |
| 2019-10-19 | Worlds | Royal Never Give Up | SK Telecom T1 | 37.6805% | 30.0980% | — |
| 2019-10-19 | Worlds | Clutch Gaming | Fnatic | 23.9993% | 27.3772% | — |
| 2019-10-19 | Worlds | SK Telecom T1 | Fnatic | 62.4399% | 63.1773% | — |
| 2019-10-19 | Worlds | Clutch Gaming | Royal Never Give Up | 23.9059% | 33.7879% | — |
| 2019-10-19 | Worlds | SK Telecom T1 | Clutch Gaming | 84.0370% | 81.9860% | — |
| 2019-10-19 | Worlds | Fnatic | Royal Never Give Up | 49.8718% | 57.5128% | — |
| 2019-10-20 | Worlds | ahq e-Sports Club | Invictus Gaming | 19.6474% | 30.7526% | — |
| 2019-10-20 | Worlds | Team Liquid | DAMWON Gaming | 39.5796% | 38.9022% | — |
| 2019-10-20 | Worlds | Team Liquid | ahq e-Sports Club | 79.0186% | 73.9150% | — |
| 2019-10-20 | Worlds | DAMWON Gaming | Invictus Gaming | 58.4331% | 66.4022% | — |
| 2019-10-20 | Worlds | DAMWON Gaming | ahq e-Sports Club | 85.1834% | 81.6525% | — |
| 2019-10-20 | Worlds | Invictus Gaming | Team Liquid | 52.0597% | 44.2791% | — |
| 2019-10-26 | Worlds | Invictus Gaming | Griffin | 32.1197% | 26.8512% | — |
| 2019-10-26 | Worlds | Funplus Phoenix | Fnatic | 56.6983% | 51.9783% | — |
| 2019-10-27 | Worlds | Splyce | SK Telecom T1 | 24.7131% | 27.1576% | — |
| 2019-10-27 | Worlds | G2 Esports | DAMWON Gaming | 54.9860% | 52.9575% | — |
| 2019-11-02 | Worlds | Funplus Phoenix | Invictus Gaming | 68.7553% | 68.9387% | — |
| 2019-11-03 | Worlds | SK Telecom T1 | G2 Esports | 51.5958% | 51.9849% | — |
| 2019-11-10 | Worlds | Funplus Phoenix | G2 Esports | 55.7525% | 50.9931% | — |


## S10

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 101 | 65.35% | 63.31% | 0.6630 | 0.2307 |
| 中性先验 · 90 天 | 101 | 60.40% | 56.83% | 0.7132 | 0.2564 |
| 无正则 MLE · 可识别子集 | 53 | 67.92% | 60.76% | 0.6847 | 0.2425 |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2020-05-28 | MSC | Funplus Phoenix | T1 | 55.7642% | 49.7591% | — |
| 2020-05-28 | MSC | Top Esports | DAMWON Gaming | 70.8888% | 65.6730% | — |
| 2020-05-28 | MSC | T1 | DAMWON Gaming | 69.3491% | 69.3491% | — |
| 2020-05-28 | MSC | Top Esports | Funplus Phoenix | 46.0557% | 46.0557% | 45.8972% |
| 2020-05-28 | MSC | DAMWON Gaming | Funplus Phoenix | 25.9592% | 30.8561% | — |
| 2020-05-28 | MSC | T1 | Top Esports | 48.1633% | 54.1836% | — |
| 2020-05-29 | MSC | JD Gaming | Gen.G eSports | 74.1883% | 70.9225% | — |
| 2020-05-29 | MSC | Invictus Gaming | DragonX | 60.9456% | 56.9753% | — |
| 2020-05-29 | MSC | DragonX | Gen.G eSports | 49.4933% | 49.4728% | — |
| 2020-05-29 | MSC | JD Gaming | Invictus Gaming | 65.2722% | 65.2913% | — |
| 2020-05-29 | MSC | Invictus Gaming | Gen.G eSports | 60.4620% | 56.4576% | — |
| 2020-05-29 | MSC | DragonX | JD Gaming | 25.4254% | 28.6445% | — |
| 2020-05-29 | MSC | Gen.G eSports | DragonX | 50.5067% | 50.5272% | — |
| 2020-05-29 | MSC | DragonX | JD Gaming | 25.4254% | 28.6445% | — |
| 2020-05-30 | MSC | Funplus Phoenix | JD Gaming | 41.4451% | 41.3262% | — |
| 2020-05-30 | MSC | Gen.G eSports | Top Esports | 47.3003% | 49.8770% | — |
| 2020-05-31 | MSC | Funplus Phoenix | Top Esports | 53.9628% | 53.7953% | — |
| 2020-09-25 | Worlds | MAD Lions | INTZ e-Sports | 88.4950% | 46.5499% | — |
| 2020-09-25 | Worlds | PSG Talon | Rainbow7 | 72.9973% | 70.0331% | — |
| 2020-09-25 | Worlds | Legacy eSports | INTZ e-Sports | 86.7810% | 76.1207% | — |
| 2020-09-25 | Worlds | LGD Gaming | PSG Talon | 66.3702% | 23.1171% | — |
| 2020-09-25 | Worlds | Team Liquid | MAD Lions | 44.0299% | 63.6187% | — |
| 2020-09-26 | Worlds | Rainbow7 | V3 Esports | 34.7361% | 37.0356% | — |
| 2020-09-26 | Worlds | INTZ e-Sports | Papara SuperMassive | 31.8752% | 35.4796% | — |
| 2020-09-26 | Worlds | V3 Esports | Unicorns Of Love | 12.7557% | 18.4929% | — |
| 2020-09-26 | Worlds | LGD Gaming | Rainbow7 | 83.7999% | 43.6091% | — |
| 2020-09-26 | Worlds | Unicorns Of Love | PSG Talon | 75.6122% | 69.8868% | — |
| 2020-09-26 | Worlds | Papara SuperMassive | MAD Lions | 22.6686% | 58.8042% | — |
| 2020-09-26 | Worlds | Team Liquid | Legacy eSports | 52.3460% | 33.8569% | — |
| 2020-09-27 | Worlds | V3 Esports | LGD Gaming | 34.5305% | 73.6960% | — |
| 2020-09-27 | Worlds | Rainbow7 | Unicorns Of Love | 6.8831% | 8.7946% | — |
| 2020-09-27 | Worlds | PSG Talon | V3 Esports | 63.4530% | 60.4876% | — |
| 2020-09-27 | Worlds | Unicorns Of Love | LGD Gaming | 80.1277% | 93.8867% | — |
| 2020-09-27 | Worlds | Unicorns Of Love | PSG Talon | 81.4925% | 78.1695% | — |
| 2020-09-27 | Worlds | LGD Gaming | V3 Esports | 65.4695% | 26.3040% | — |
| 2020-09-28 | Worlds | Papara SuperMassive | Team Liquid | 24.8675% | 43.4980% | — |
| 2020-09-28 | Worlds | MAD Lions | Legacy eSports | 47.3407% | 24.2197% | — |
| 2020-09-28 | Worlds | INTZ e-Sports | Team Liquid | 7.9301% | 21.0528% | — |
| 2020-09-28 | Worlds | Legacy eSports | Papara SuperMassive | 64.6575% | 58.4521% | — |
| 2020-09-28 | Worlds | MAD Lions | INTZ e-Sports | 86.3390% | 56.4851% | — |
| 2020-09-28 | Worlds | Team Liquid | Legacy eSports | 62.2852% | 48.0060% | — |
| 2020-09-29 | Worlds | Rainbow7 | LGD Gaming | 28.4129% | 61.2240% | 66.5979% |
| 2020-09-29 | Worlds | Papara SuperMassive | MAD Lions | 35.1192% | 60.6958% | 66.2080% |
| 2020-09-30 | Worlds | Legacy eSports | LGD Gaming | 37.3519% | 67.8531% | — |
| 2020-09-30 | Worlds | Unicorns Of Love | Papara SuperMassive | 84.2333% | 78.9295% | — |
| 2020-10-03 | Worlds | FlyQuest | Top Esports | 17.0593% | 34.1324% | — |
| 2020-10-03 | Worlds | Unicorns Of Love | DragonX | 53.8325% | 79.8841% | — |
| 2020-10-03 | Worlds | Rogue | PSG Talon | 32.4664% | 18.6787% | — |
| 2020-10-03 | Worlds | DAMWON Gaming | JD Gaming | 49.8701% | 45.9128% | — |
| 2020-10-03 | Worlds | Gen.G eSports | LGD Gaming | 62.5496% | 54.2914% | — |
| 2020-10-03 | Worlds | TSM | Fnatic | 53.9859% | 62.7606% | — |
| 2020-10-04 | Worlds | Machi E-Sports | Team Liquid | 56.2428% | 65.5919% | 80.6420% |
| 2020-10-04 | Worlds | G2 Esports | Suning | 37.7291% | 51.9260% | 17.6956% |
| 2020-10-04 | Worlds | Rogue | DAMWON Gaming | 15.6280% | 26.8551% | 5.7266% |
| 2020-10-04 | Worlds | PSG Talon | JD Gaming | 25.0284% | 52.9666% | 29.5623% |
| 2020-10-04 | Worlds | Gen.G eSports | TSM | 84.5385% | 68.7568% | 93.2798% |
| 2020-10-04 | Worlds | LGD Gaming | Fnatic | 61.7241% | 51.9576% | 81.5620% |
| 2020-10-05 | Worlds | Machi E-Sports | G2 Esports | 46.0412% | 63.0531% | 68.7634% |
| 2020-10-05 | Worlds | Team Liquid | Suning | 26.3634% | 44.4399% | 16.2856% |
| 2020-10-05 | Worlds | DAMWON Gaming | PSG Talon | 82.5297% | 59.8884% | 80.6185% |
| 2020-10-05 | Worlds | JD Gaming | Rogue | 79.4068% | 71.3589% | 88.2214% |
| 2020-10-05 | Worlds | FlyQuest | Unicorns Of Love | 22.3228% | 20.2105% | 17.1760% |
| 2020-10-05 | Worlds | Top Esports | DragonX | 55.2917% | 56.8860% | 53.3477% |
| 2020-10-06 | Worlds | G2 Esports | Team Liquid | 66.6933% | 59.8202% | 65.0331% |
| 2020-10-06 | Worlds | Suning | Machi E-Sports | 69.2006% | 44.9800% | 70.7276% |
| 2020-10-06 | Worlds | DragonX | FlyQuest | 80.1905% | 65.7309% | 85.9053% |
| 2020-10-06 | Worlds | Top Esports | Unicorns Of Love | 73.8025% | 54.7318% | 84.3678% |
| 2020-10-06 | Worlds | Fnatic | Gen.G eSports | 20.1372% | 28.9458% | 13.1013% |
| 2020-10-06 | Worlds | TSM | LGD Gaming | 27.8429% | 39.5638% | 21.7498% |
| 2020-10-08 | Worlds | Team Liquid | G2 Esports | 36.5454% | 42.4372% | 38.4967% |
| 2020-10-08 | Worlds | Machi E-Sports | Suning | 27.3234% | 47.9727% | 24.8494% |
| 2020-10-08 | Worlds | G2 Esports | Machi E-Sports | 61.3780% | 48.1546% | 55.8941% |
| 2020-10-08 | Worlds | Suning | Team Liquid | 74.3992% | 61.2975% | 79.2213% |
| 2020-10-08 | Worlds | Team Liquid | Machi E-Sports | 47.7878% | 40.6440% | 44.2344% |
| 2020-10-08 | Worlds | Suning | G2 Esports | 62.5990% | 53.8669% | 70.4703% |
| 2020-10-08 | Worlds | Suning | G2 Esports | 62.5990% | 53.8669% | 70.4703% |
| 2020-10-09 | Worlds | PSG Talon | DAMWON Gaming | 14.0954% | 29.0367% | 10.7956% |
| 2020-10-09 | Worlds | Rogue | JD Gaming | 18.4713% | 24.0501% | 13.9396% |
| 2020-10-09 | Worlds | DAMWON Gaming | Rogue | 84.1638% | 77.8735% | 87.5174% |
| 2020-10-09 | Worlds | JD Gaming | PSG Talon | 83.5024% | 68.6806% | 87.9171% |
| 2020-10-09 | Worlds | PSG Talon | Rogue | 46.5823% | 59.0179% | 45.9019% |
| 2020-10-09 | Worlds | JD Gaming | DAMWON Gaming | 45.3701% | 47.2933% | 46.8246% |
| 2020-10-10 | Worlds | Fnatic | TSM | 58.6979% | 53.7962% | 54.3334% |
| 2020-10-10 | Worlds | LGD Gaming | Gen.G eSports | 36.3236% | 41.0076% | 37.9305% |
| 2020-10-10 | Worlds | TSM | Gen.G eSports | 18.1779% | 28.1494% | 17.9675% |
| 2020-10-10 | Worlds | Fnatic | LGD Gaming | 35.6291% | 39.6212% | 29.8954% |
| 2020-10-10 | Worlds | LGD Gaming | TSM | 71.9703% | 63.9551% | 73.6150% |
| 2020-10-10 | Worlds | Gen.G eSports | Fnatic | 76.0031% | 68.6740% | 79.3276% |
| 2020-10-11 | Worlds | FlyQuest | DragonX | 19.5127% | 29.1608% | 17.1121% |
| 2020-10-11 | Worlds | Unicorns Of Love | Top Esports | 23.7226% | 38.0453% | 15.0277% |
| 2020-10-11 | Worlds | DragonX | Unicorns Of Love | 66.7802% | 49.3406% | 77.0757% |
| 2020-10-11 | Worlds | Top Esports | FlyQuest | 86.8381% | 80.2437% | 89.0664% |
| 2020-10-11 | Worlds | Unicorns Of Love | FlyQuest | 67.2337% | 71.3811% | 59.0278% |
| 2020-10-11 | Worlds | DragonX | Top Esports | 38.4690% | 37.4255% | 37.2890% |
| 2020-10-15 | Worlds | DAMWON Gaming | DragonX | 62.7016% | 62.7207% | 63.6205% |
| 2020-10-16 | Worlds | Suning | JD Gaming | 38.5966% | 39.4010% | 37.9758% |
| 2020-10-17 | Worlds | Top Esports | Fnatic | 78.5488% | 74.0799% | 81.4389% |
| 2020-10-18 | Worlds | Gen.G eSports | G2 Esports | 69.0633% | 62.0846% | 70.4780% |
| 2020-10-24 | Worlds | G2 Esports | DAMWON Gaming | 32.5245% | 37.5778% | 34.3025% |
| 2020-10-25 | Worlds | Top Esports | Suning | 59.5490% | 59.2645% | 59.3479% |
| 2020-10-31 | Worlds | DAMWON Gaming | Suning | 62.0504% | 62.0772% | 60.2384% |


## S11

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 157 | 68.79% | 67.33% | 0.6117 | 0.2112 |
| 中性先验 · 90 天 | 157 | 64.33% | 62.38% | 0.6591 | 0.2323 |
| 无正则 MLE · 可识别子集 | 87 | 66.67% | 66.12% | 0.6508 | 0.2190 |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2021-05-06 | MSI | DWG KIA | Cloud9 | 75.0824% | 54.6971% | — |
| 2021-05-06 | MSI | Infinity eSports | Detonation FocusMe | 45.4961% | 38.3178% | — |
| 2021-05-06 | MSI | Royal Never Give Up | Pentanet.GG | 65.3943% | 38.7415% | — |
| 2021-05-06 | MSI | Pentanet.GG | Unicorns Of Love | 62.0018% | 64.0815% | — |
| 2021-05-06 | MSI | Istanbul Wildcats | paiN Gaming | 72.3155% | 60.3117% | — |
| 2021-05-06 | MSI | MAD Lions | PSG Talon | 8.6860% | 6.3702% | — |
| 2021-05-07 | MSI | Pentanet.GG | Royal Never Give Up | 22.1290% | 40.6176% | — |
| 2021-05-07 | MSI | Unicorns Of Love | Royal Never Give Up | 29.2804% | 51.0678% | — |
| 2021-05-07 | MSI | Infinity eSports | DWG KIA | 14.8419% | 41.1592% | — |
| 2021-05-07 | MSI | Detonation FocusMe | Cloud9 | 30.2515% | 50.6031% | — |
| 2021-05-07 | MSI | Istanbul Wildcats | MAD Lions | 27.9908% | 41.5917% | — |
| 2021-05-07 | MSI | paiN Gaming | PSG Talon | 8.9056% | 17.2161% | — |
| 2021-05-08 | MSI | Royal Never Give Up | Unicorns Of Love | 76.9426% | 61.8591% | — |
| 2021-05-08 | MSI | Unicorns Of Love | Pentanet.GG | 57.9245% | 57.9650% | — |
| 2021-05-08 | MSI | DWG KIA | Detonation FocusMe | 86.4880% | 61.9133% | — |
| 2021-05-08 | MSI | Cloud9 | Infinity eSports | 53.9205% | 43.8959% | — |
| 2021-05-08 | MSI | MAD Lions | paiN Gaming | 80.1281% | 61.6744% | — |
| 2021-05-08 | MSI | PSG Talon | Istanbul Wildcats | 90.7645% | 88.7184% | — |
| 2021-05-09 | MSI | Unicorns Of Love | Royal Never Give Up | 16.7958% | 27.8804% | — |
| 2021-05-09 | MSI | Unicorns Of Love | Pentanet.GG | 44.1725% | 43.5049% | — |
| 2021-05-09 | MSI | Royal Never Give Up | Pentanet.GG | 79.6733% | 66.5772% | — |
| 2021-05-09 | MSI | Royal Never Give Up | Unicorns Of Love | 83.2042% | 72.1196% | — |
| 2021-05-09 | MSI | Pentanet.GG | Unicorns Of Love | 55.8275% | 56.4951% | — |
| 2021-05-09 | MSI | Pentanet.GG | Royal Never Give Up | 20.3267% | 33.4228% | — |
| 2021-05-09 | MSI | Unicorns Of Love | Pentanet.GG | 44.1725% | 43.5049% | — |
| 2021-05-10 | MSI | MAD Lions | Istanbul Wildcats | 79.2707% | 71.7359% | — |
| 2021-05-10 | MSI | PSG Talon | paiN Gaming | 93.2541% | 88.5512% | — |
| 2021-05-10 | MSI | Istanbul Wildcats | PSG Talon | 8.3452% | 10.0567% | — |
| 2021-05-10 | MSI | paiN Gaming | MAD Lions | 17.2022% | 31.2996% | — |
| 2021-05-10 | MSI | paiN Gaming | Istanbul Wildcats | 44.2741% | 53.6248% | — |
| 2021-05-10 | MSI | PSG Talon | MAD Lions | 74.1739% | 77.8948% | — |
| 2021-05-11 | MSI | Cloud9 | DWG KIA | 17.3477% | 29.6172% | — |
| 2021-05-11 | MSI | Detonation FocusMe | Infinity eSports | 52.8442% | 56.5592% | — |
| 2021-05-11 | MSI | DWG KIA | Infinity eSports | 89.1757% | 74.5065% | — |
| 2021-05-11 | MSI | Cloud9 | Detonation FocusMe | 60.6767% | 48.5749% | — |
| 2021-05-11 | MSI | Detonation FocusMe | DWG KIA | 11.9737% | 30.8195% | — |
| 2021-05-11 | MSI | Infinity eSports | Cloud9 | 36.6414% | 44.8466% | — |
| 2021-05-14 | MSI | DWG KIA | Royal Never Give Up | 42.0572% | 42.8487% | — |
| 2021-05-14 | MSI | MAD Lions | Pentanet.GG | 66.4006% | 66.5433% | — |
| 2021-05-14 | MSI | PSG Talon | DWG KIA | 53.0160% | 68.8802% | — |
| 2021-05-14 | MSI | Royal Never Give Up | Cloud9 | 76.9650% | 65.7722% | — |
| 2021-05-14 | MSI | PSG Talon | Pentanet.GG | 80.3461% | 82.7317% | — |
| 2021-05-14 | MSI | Cloud9 | MAD Lions | 43.0494% | 43.0324% | — |
| 2021-05-15 | MSI | Pentanet.GG | Royal Never Give Up | 12.9878% | 20.8465% | — |
| 2021-05-15 | MSI | DWG KIA | Cloud9 | 74.7585% | 64.8243% | — |
| 2021-05-15 | MSI | MAD Lions | Royal Never Give Up | 29.8475% | 41.7350% | — |
| 2021-05-15 | MSI | Cloud9 | PSG Talon | 25.2371% | 23.5378% | — |
| 2021-05-15 | MSI | Pentanet.GG | DWG KIA | 18.9940% | 28.2247% | — |
| 2021-05-15 | MSI | MAD Lions | PSG Talon | 40.0551% | 37.7619% | — |
| 2021-05-16 | MSI | Cloud9 | Pentanet.GG | 57.9704% | 57.5556% | — |
| 2021-05-16 | MSI | Royal Never Give Up | PSG Talon | 66.0850% | 52.3051% | — |
| 2021-05-16 | MSI | DWG KIA | MAD Lions | 61.2466% | 51.4285% | — |
| 2021-05-16 | MSI | Royal Never Give Up | Pentanet.GG | 88.9802% | 82.8041% | — |
| 2021-05-16 | MSI | Cloud9 | DWG KIA | 21.0058% | 29.1753% | — |
| 2021-05-16 | MSI | PSG Talon | MAD Lions | 55.8034% | 58.5465% | — |
| 2021-05-17 | MSI | PSG Talon | Royal Never Give Up | 44.6486% | 56.3195% | — |
| 2021-05-17 | MSI | MAD Lions | DWG KIA | 31.2716% | 39.2636% | — |
| 2021-05-17 | MSI | Cloud9 | Royal Never Give Up | 17.6171% | 25.0316% | — |
| 2021-05-17 | MSI | Pentanet.GG | MAD Lions | 22.6193% | 23.9831% | — |
| 2021-05-17 | MSI | DWG KIA | PSG Talon | 52.5525% | 42.0504% | — |
| 2021-05-17 | MSI | Pentanet.GG | Cloud9 | 35.7193% | 36.3665% | — |
| 2021-05-18 | MSI | Royal Never Give Up | DWG KIA | 46.2332% | 45.5682% | — |
| 2021-05-18 | MSI | Pentanet.GG | PSG Talon | 17.3826% | 17.9759% | — |
| 2021-05-18 | MSI | Royal Never Give Up | MAD Lions | 70.4844% | 63.0733% | — |
| 2021-05-18 | MSI | PSG Talon | Cloud9 | 73.2818% | 73.0059% | — |
| 2021-05-18 | MSI | DWG KIA | Pentanet.GG | 89.0438% | 84.5772% | — |
| 2021-05-18 | MSI | MAD Lions | Cloud9 | 62.8085% | 61.4356% | — |
| 2021-05-21 | MSI | Royal Never Give Up | PSG Talon | 56.0375% | 46.9659% | — |
| 2021-05-22 | MSI | DWG KIA | MAD Lions | 71.4859% | 65.5265% | — |
| 2021-05-23 | MSI | Royal Never Give Up | DWG KIA | 52.2792% | 51.3696% | — |
| 2021-10-05 | Worlds | Hanwha Life eSports | LNG Esports | 38.4599% | 37.9993% | 30.3073% |
| 2021-10-05 | Worlds | Infinity eSports | RED Canids | 56.8977% | 47.6701% | 24.8220% |
| 2021-10-05 | Worlds | LNG Esports | PEACE | 76.5730% | 60.4529% | 95.7099% |
| 2021-10-05 | Worlds | Hanwha Life eSports | Infinity eSports | 69.6546% | 44.3749% | 91.4027% |
| 2021-10-05 | Worlds | Unicorns Of Love | Detonation FocusMe | 50.7850% | 38.6807% | 27.1031% |
| 2021-10-05 | Worlds | Galatasaray Esports | Beyond Gaming | 34.7672% | 43.1285% | 38.1713% |
| 2021-10-05 | Worlds | Detonation FocusMe | Cloud9 | 46.1851% | 61.7275% | 25.3799% |
| 2021-10-05 | Worlds | Unicorns Of Love | Galatasaray Esports | 45.3649% | 39.9251% | 16.2135% |
| 2021-10-06 | Worlds | PEACE | Hanwha Life eSports | 30.9698% | 46.8199% | 5.0632% |
| 2021-10-06 | Worlds | RED Canids | LNG Esports | 18.8561% | 46.5734% | 17.5579% |
| 2021-10-06 | Worlds | Infinity eSports | PEACE | 41.2683% | 47.7764% | 45.9292% |
| 2021-10-06 | Worlds | RED Canids | Hanwha Life eSports | 30.2565% | 61.6639% | 39.9166% |
| 2021-10-06 | Worlds | Beyond Gaming | Cloud9 | 59.1887% | 59.5958% | 47.5022% |
| 2021-10-06 | Worlds | Galatasaray Esports | Detonation FocusMe | 66.7808% | 61.7861% | 92.4541% |
| 2021-10-06 | Worlds | Beyond Gaming | Unicorns Of Love | 72.1742% | 69.0260% | 96.0571% |
| 2021-10-06 | Worlds | Cloud9 | Galatasaray Esports | 39.8839% | 33.4992% | 28.3731% |
| 2021-10-07 | Worlds | LNG Esports | Infinity eSports | 87.8567% | 74.9599% | 99.5107% |
| 2021-10-07 | Worlds | PEACE | RED Canids | 57.2264% | 45.8205% | 31.8517% |
| 2021-10-07 | Worlds | Detonation FocusMe | Beyond Gaming | 43.1250% | 54.2296% | 57.4287% |
| 2021-10-07 | Worlds | Cloud9 | Unicorns Of Love | 73.2218% | 70.2611% | 97.8372% |
| 2021-10-07 | Worlds | Unicorns Of Love | Beyond Gaming | 27.8292% | 30.5585% | 8.0740% |
| 2021-10-07 | Worlds | Detonation FocusMe | Cloud9 | 41.8311% | 53.2621% | 25.3467% |
| 2021-10-08 | Worlds | Galatasaray Esports | Beyond Gaming | 44.3441% | 49.3065% | 50.8197% |
| 2021-10-08 | Worlds | PEACE | RED Canids | 64.1464% | 54.3560% | 68.5948% |
| 2021-10-09 | Worlds | Beyond Gaming | Hanwha Life eSports | 48.6234% | 62.9398% | 24.1951% |
| 2021-10-09 | Worlds | PEACE | Cloud9 | 35.5334% | 39.0133% | 20.0842% |
| 2021-10-11 | Worlds | DWG KIA | Funplus Phoenix | 50.8031% | 53.8942% | 37.4668% |
| 2021-10-11 | Worlds | Royal Never Give Up | PSG Talon | 60.7170% | 49.7901% | 85.9358% |
| 2021-10-11 | Worlds | Hanwha Life eSports | Fnatic | 65.8209% | 60.7060% | 65.5762% |
| 2021-10-11 | Worlds | LNG Esports | Gen.G eSports | 52.6291% | 51.8992% | 64.2004% |
| 2021-10-11 | Worlds | T1 | Detonation FocusMe | 62.4849% | 40.8564% | 70.9806% |
| 2021-10-11 | Worlds | Edward Gaming | 100 Thieves | 76.2097% | 63.9859% | 88.5365% |
| 2021-10-11 | Worlds | Team Liquid | MAD Lions | 37.9218% | 43.4300% | 32.8072% |
| 2021-10-11 | Worlds | Rogue | Cloud9 | 41.9179% | 35.8373% | 51.0525% |
| 2021-10-12 | Worlds | T1 | Edward Gaming | 43.5626% | 45.0270% | 42.2907% |
| 2021-10-12 | Worlds | Rogue | DWG KIA | 15.1645% | 18.5475% | 10.1612% |
| 2021-10-12 | Worlds | PSG Talon | Hanwha Life eSports | 47.7922% | 56.8597% | 21.5556% |
| 2021-10-12 | Worlds | Fnatic | Royal Never Give Up | 19.2878% | 23.3869% | 13.8917% |
| 2021-10-12 | Worlds | Cloud9 | Funplus Phoenix | 23.8310% | 34.8247% | 12.3428% |
| 2021-10-12 | Worlds | Detonation FocusMe | 100 Thieves | 51.1437% | 59.5873% | 47.9093% |
| 2021-10-12 | Worlds | MAD Lions | Gen.G eSports | 37.1457% | 44.4587% | 26.0465% |
| 2021-10-12 | Worlds | Team Liquid | LNG Esports | 34.7387% | 46.3174% | 22.2248% |
| 2021-10-13 | Worlds | Royal Never Give Up | Hanwha Life eSports | 68.3901% | 67.4077% | 75.0108% |
| 2021-10-13 | Worlds | MAD Lions | LNG Esports | 41.9739% | 48.3957% | 31.4655% |
| 2021-10-13 | Worlds | Funplus Phoenix | Rogue | 82.1755% | 77.8537% | 88.2838% |
| 2021-10-13 | Worlds | PSG Talon | Fnatic | 73.5547% | 76.4735% | 57.6870% |
| 2021-10-13 | Worlds | Gen.G eSports | Team Liquid | 66.5518% | 57.0443% | 72.9506% |
| 2021-10-13 | Worlds | DWG KIA | Cloud9 | 80.7156% | 73.8997% | 86.6796% |
| 2021-10-13 | Worlds | Edward Gaming | Detonation FocusMe | 81.8491% | 67.2769% | 92.2262% |
| 2021-10-13 | Worlds | 100 Thieves | T1 | 33.3580% | 42.8135% | 27.0730% |
| 2021-10-15 | Worlds | Funplus Phoenix | DWG KIA | 48.9997% | 46.8493% | 59.5933% |
| 2021-10-15 | Worlds | Cloud9 | Rogue | 55.5329% | 60.2548% | 49.3029% |
| 2021-10-15 | Worlds | Funplus Phoenix | Cloud9 | 82.8970% | 75.7520% | 93.0717% |
| 2021-10-15 | Worlds | DWG KIA | Rogue | 86.3018% | 84.3093% | 89.8560% |
| 2021-10-15 | Worlds | Rogue | Funplus Phoenix | 14.1782% | 17.4333% | 7.1103% |
| 2021-10-15 | Worlds | Cloud9 | DWG KIA | 16.5431% | 22.0058% | 9.8927% |
| 2021-10-15 | Worlds | Funplus Phoenix | Rogue | 85.8218% | 82.5667% | 92.8897% |
| 2021-10-15 | Worlds | Cloud9 | Rogue | 55.5329% | 60.2548% | 49.3029% |
| 2021-10-16 | Worlds | Detonation FocusMe | Edward Gaming | 19.9549% | 32.9231% | 13.0881% |
| 2021-10-16 | Worlds | T1 | 100 Thieves | 69.7913% | 62.9042% | 72.5856% |
| 2021-10-16 | Worlds | Edward Gaming | T1 | 58.7504% | 58.0822% | 59.8279% |
| 2021-10-16 | Worlds | 100 Thieves | Detonation FocusMe | 54.9359% | 46.4413% | 62.7428% |
| 2021-10-16 | Worlds | Detonation FocusMe | T1 | 26.2027% | 40.4797% | 18.3188% |
| 2021-10-16 | Worlds | 100 Thieves | Edward Gaming | 23.3074% | 29.8541% | 20.2297% |
| 2021-10-17 | Worlds | Hanwha Life eSports | PSG Talon | 46.8446% | 40.0316% | 63.9533% |
| 2021-10-17 | Worlds | Royal Never Give Up | Fnatic | 81.6641% | 79.4915% | 82.5878% |
| 2021-10-17 | Worlds | PSG Talon | Royal Never Give Up | 41.4040% | 48.6506% | 27.1791% |
| 2021-10-17 | Worlds | Fnatic | Hanwha Life eSports | 26.5010% | 28.9734% | 24.1500% |
| 2021-10-17 | Worlds | Hanwha Life eSports | Royal Never Give Up | 38.3748% | 38.7429% | 39.8380% |
| 2021-10-17 | Worlds | Fnatic | PSG Talon | 24.1135% | 21.4026% | 36.0974% |
| 2021-10-17 | Worlds | Hanwha Life eSports | Royal Never Give Up | 38.3748% | 38.7429% | 39.8380% |
| 2021-10-18 | Worlds | Gen.G eSports | MAD Lions | 63.6645% | 59.3509% | 68.5754% |
| 2021-10-18 | Worlds | LNG Esports | Team Liquid | 62.7097% | 55.9726% | 62.2216% |
| 2021-10-18 | Worlds | Gen.G eSports | LNG Esports | 59.9872% | 59.7911% | 64.2945% |
| 2021-10-18 | Worlds | MAD Lions | Team Liquid | 58.9980% | 56.4225% | 57.6101% |
| 2021-10-18 | Worlds | Team Liquid | Gen.G eSports | 28.3998% | 34.5966% | 25.2159% |
| 2021-10-18 | Worlds | LNG Esports | MAD Lions | 53.8896% | 49.5431% | 54.7896% |
| 2021-10-18 | Worlds | Gen.G eSports | Team Liquid | 71.6002% | 65.4034% | 74.7841% |
| 2021-10-18 | Worlds | MAD Lions | LNG Esports | 46.1104% | 50.4569% | 45.2104% |
| 2021-10-18 | Worlds | Gen.G eSports | MAD Lions | 63.6645% | 59.3509% | 68.5754% |
| 2021-10-22 | Worlds | T1 | Hanwha Life eSports | 59.6760% | 59.0936% | 61.9423% |
| 2021-10-23 | Worlds | Edward Gaming | Royal Never Give Up | 50.4407% | 49.8052% | 52.2630% |
| 2021-10-24 | Worlds | DWG KIA | MAD Lions | 76.8744% | 74.7849% | 78.9834% |
| 2021-10-25 | Worlds | Gen.G eSports | Cloud9 | 67.9296% | 61.7477% | 72.4898% |
| 2021-10-30 | Worlds | DWG KIA | T1 | 62.4863% | 62.6677% | 62.3996% |
| 2021-10-31 | Worlds | Edward Gaming | Gen.G eSports | 48.9264% | 48.3626% | 44.8375% |
| 2021-11-06 | Worlds | DWG KIA | Edward Gaming | 66.9016% | 67.3925% | 69.3557% |


## S12

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 163 | 76.69% | 74.51% | 0.5700 | 0.1925 |
| 中性先验 · 90 天 | 163 | 66.26% | 66.18% | 0.6511 | 0.2284 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2022-05-10 | MSI | T1 | Saigon Buffalo | 94.0584% | 77.4388% | — |
| 2022-05-10 | MSI | Team Aze | Detonation FocusMe | 9.6551% | 25.8533% | — |
| 2022-05-10 | MSI | ORDER | G2 Esports | 23.7433% | 46.5787% | — |
| 2022-05-10 | MSI | Evil Geniuses | G2 Esports | 48.2785% | 45.7261% | — |
| 2022-05-10 | MSI | RED Canids | PSG Talon | 8.4164% | 19.8317% | — |
| 2022-05-11 | MSI | G2 Esports | Evil Geniuses | 64.2805% | 67.8080% | — |
| 2022-05-11 | MSI | Evil Geniuses | ORDER | 73.5432% | 50.3631% | — |
| 2022-05-11 | MSI | Detonation FocusMe | Saigon Buffalo | 86.6786% | 89.5738% | — |
| 2022-05-11 | MSI | Team Aze | T1 | 3.4543% | 33.3211% | — |
| 2022-05-11 | MSI | Istanbul Wildcats | RED Canids | 73.2627% | 64.6135% | — |
| 2022-05-12 | MSI | ORDER | Evil Geniuses | 24.1481% | 42.0203% | — |
| 2022-05-12 | MSI | G2 Esports | ORDER | 87.0395% | 75.6586% | — |
| 2022-05-12 | MSI | PSG Talon | Istanbul Wildcats | 55.7945% | 44.4896% | — |
| 2022-05-12 | MSI | Saigon Buffalo | Team Aze | 72.8334% | 47.7072% | — |
| 2022-05-12 | MSI | T1 | Detonation FocusMe | 82.6104% | 52.2368% | — |
| 2022-05-13 | MSI | PSG Talon | RED Canids | 84.9536% | 72.7976% | — |
| 2022-05-13 | MSI | Royal Never Give Up | Istanbul Wildcats | 70.2704% | 33.5970% | — |
| 2022-05-13 | MSI | Istanbul Wildcats | PSG Talon | 33.8918% | 42.3721% | — |
| 2022-05-13 | MSI | RED Canids | Royal Never Give Up | 12.7521% | 50.1110% | — |
| 2022-05-13 | MSI | RED Canids | Istanbul Wildcats | 25.6765% | 33.6962% | — |
| 2022-05-13 | MSI | PSG Talon | Royal Never Give Up | 45.2125% | 72.8855% | — |
| 2022-05-14 | MSI | Evil Geniuses | G2 Esports | 32.4342% | 31.5429% | — |
| 2022-05-14 | MSI | Evil Geniuses | ORDER | 80.0608% | 66.7848% | — |
| 2022-05-14 | MSI | G2 Esports | ORDER | 89.3213% | 81.3563% | — |
| 2022-05-14 | MSI | G2 Esports | Evil Geniuses | 67.5658% | 68.4571% | — |
| 2022-05-14 | MSI | ORDER | G2 Esports | 10.6787% | 18.6437% | — |
| 2022-05-14 | MSI | Istanbul Wildcats | Royal Never Give Up | 15.9611% | 37.7770% | — |
| 2022-05-14 | MSI | Royal Never Give Up | PSG Talon | 61.7266% | 40.4742% | — |
| 2022-05-14 | MSI | Royal Never Give Up | RED Canids | 88.8453% | 64.8287% | — |
| 2022-05-14 | MSI | ORDER | Evil Geniuses | 19.9392% | 33.2152% | — |
| 2022-05-15 | MSI | Team Aze | Saigon Buffalo | 22.2981% | 41.3113% | — |
| 2022-05-15 | MSI | Detonation FocusMe | T1 | 14.9421% | 37.4276% | — |
| 2022-05-15 | MSI | Saigon Buffalo | Detonation FocusMe | 33.5838% | 33.6705% | — |
| 2022-05-15 | MSI | T1 | Team Aze | 97.5142% | 82.3906% | — |
| 2022-05-15 | MSI | Detonation FocusMe | Team Aze | 87.3280% | 73.6746% | — |
| 2022-05-15 | MSI | Saigon Buffalo | T1 | 8.1582% | 23.2914% | — |
| 2022-05-20 | MSI | T1 | G2 Esports | 70.8335% | 53.6549% | — |
| 2022-05-20 | MSI | Evil Geniuses | Royal Never Give Up | 25.8644% | 38.0326% | — |
| 2022-05-20 | MSI | PSG Talon | Saigon Buffalo | 65.4101% | 60.1744% | — |
| 2022-05-20 | MSI | G2 Esports | Royal Never Give Up | 49.9100% | 63.8878% | — |
| 2022-05-20 | MSI | Saigon Buffalo | Evil Geniuses | 41.3295% | 49.8475% | — |
| 2022-05-20 | MSI | PSG Talon | T1 | 16.1111% | 31.0350% | — |
| 2022-05-21 | MSI | G2 Esports | Evil Geniuses | 79.7158% | 78.4960% | — |
| 2022-05-21 | MSI | Royal Never Give Up | PSG Talon | 67.0661% | 52.5689% | — |
| 2022-05-21 | MSI | T1 | Saigon Buffalo | 91.2580% | 80.3485% | — |
| 2022-05-21 | MSI | PSG Talon | Evil Geniuses | 54.8304% | 58.0286% | — |
| 2022-05-21 | MSI | Royal Never Give Up | T1 | 33.3185% | 35.6682% | — |
| 2022-05-21 | MSI | Saigon Buffalo | G2 Esports | 10.7613% | 15.6245% | — |
| 2022-05-22 | MSI | Evil Geniuses | T1 | 21.8218% | 32.2953% | — |
| 2022-05-22 | MSI | G2 Esports | PSG Talon | 82.3723% | 79.8574% | — |
| 2022-05-22 | MSI | Royal Never Give Up | Saigon Buffalo | 87.4928% | 76.1065% | — |
| 2022-05-22 | MSI | T1 | PSG Talon | 80.7370% | 68.8105% | — |
| 2022-05-22 | MSI | Royal Never Give Up | G2 Esports | 40.3181% | 30.6881% | — |
| 2022-05-22 | MSI | Evil Geniuses | Saigon Buffalo | 72.1644% | 65.6312% | — |
| 2022-05-23 | MSI | PSG Talon | G2 Esports | 27.6444% | 30.3598% | — |
| 2022-05-23 | MSI | T1 | Evil Geniuses | 81.1081% | 72.4891% | — |
| 2022-05-23 | MSI | Saigon Buffalo | Royal Never Give Up | 9.9227% | 18.6139% | — |
| 2022-05-23 | MSI | G2 Esports | T1 | 39.9226% | 50.7049% | — |
| 2022-05-23 | MSI | Saigon Buffalo | PSG Talon | 25.0516% | 29.2883% | — |
| 2022-05-23 | MSI | Royal Never Give Up | Evil Geniuses | 76.7843% | 68.1506% | — |
| 2022-05-24 | MSI | G2 Esports | Saigon Buffalo | 83.5408% | 79.0232% | — |
| 2022-05-24 | MSI | Evil Geniuses | PSG Talon | 50.2330% | 46.9620% | — |
| 2022-05-24 | MSI | Saigon Buffalo | T1 | 10.3282% | 18.2940% | — |
| 2022-05-24 | MSI | PSG Talon | Royal Never Give Up | 23.6215% | 33.6527% | — |
| 2022-05-24 | MSI | Evil Geniuses | G2 Esports | 32.9726% | 33.2626% | — |
| 2022-05-24 | MSI | T1 | Royal Never Give Up | 52.0494% | 51.6514% | — |
| 2022-05-27 | MSI | Royal Never Give Up | Evil Geniuses | 74.8668% | 67.6027% | — |
| 2022-05-28 | MSI | T1 | G2 Esports | 69.2682% | 60.5772% | — |
| 2022-05-29 | MSI | Royal Never Give Up | T1 | 40.9989% | 41.6783% | — |
| 2022-09-29 | Worlds | Isurus | MAD Lions | 18.9636% | 51.9483% | — |
| 2022-09-29 | Worlds | Fnatic | Evil Geniuses | 46.1669% | 47.1383% | — |
| 2022-09-29 | Worlds | LOUD | Beyond Gaming | 38.9997% | 61.4993% | — |
| 2022-09-29 | Worlds | MAD Lions | Istanbul Wildcats | 53.3586% | 37.5944% | — |
| 2022-09-29 | Worlds | Chief Esports Club | Fnatic | 58.3203% | 76.6283% | — |
| 2022-09-29 | Worlds | Detonation FocusMe | LOUD | 75.4854% | 62.1732% | — |
| 2022-09-29 | Worlds | Saigon Buffalo | Istanbul Wildcats | 51.8473% | 43.6730% | — |
| 2022-09-29 | Worlds | DRX | Royal Never Give Up | 30.7973% | 27.0329% | — |
| 2022-09-30 | Worlds | Fnatic | Detonation FocusMe | 58.0445% | 47.6585% | — |
| 2022-09-30 | Worlds | Evil Geniuses | LOUD | 64.0403% | 40.4449% | — |
| 2022-09-30 | Worlds | Saigon Buffalo | Isurus | 83.0109% | 62.1649% | — |
| 2022-09-30 | Worlds | Detonation FocusMe | Chief Esports Club | 51.5201% | 45.8465% | — |
| 2022-09-30 | Worlds | Evil Geniuses | Beyond Gaming | 52.4202% | 45.9263% | — |
| 2022-09-30 | Worlds | DRX | Saigon Buffalo | 70.2754% | 46.0184% | — |
| 2022-09-30 | Worlds | MAD Lions | Royal Never Give Up | 27.1556% | 42.3196% | — |
| 2022-09-30 | Worlds | Istanbul Wildcats | DRX | 20.3250% | 47.5171% | — |
| 2022-10-01 | Worlds | LOUD | Fnatic | 23.6569% | 39.3372% | — |
| 2022-10-01 | Worlds | MAD Lions | Saigon Buffalo | 59.2599% | 54.1359% | — |
| 2022-10-01 | Worlds | Beyond Gaming | Detonation FocusMe | 42.8605% | 35.9135% | — |
| 2022-10-01 | Worlds | Evil Geniuses | Chief Esports Club | 61.0934% | 43.2687% | — |
| 2022-10-01 | Worlds | Royal Never Give Up | Isurus | 95.7062% | 78.2207% | — |
| 2022-10-01 | Worlds | Chief Esports Club | Beyond Gaming | 49.7462% | 62.8599% | — |
| 2022-10-01 | Worlds | Royal Never Give Up | Istanbul Wildcats | 88.1665% | 73.5010% | — |
| 2022-10-01 | Worlds | Isurus | DRX | 6.3080% | 31.1493% | — |
| 2022-10-02 | Worlds | Beyond Gaming | Fnatic | 37.1545% | 39.7361% | — |
| 2022-10-02 | Worlds | LOUD | Chief Esports Club | 54.8182% | 58.1675% | — |
| 2022-10-02 | Worlds | Detonation FocusMe | Evil Geniuses | 48.1604% | 58.0872% | — |
| 2022-10-02 | Worlds | Istanbul Wildcats | Isurus | 75.3908% | 59.7729% | — |
| 2022-10-02 | Worlds | DRX | MAD Lions | 66.3576% | 50.4351% | — |
| 2022-10-02 | Worlds | Royal Never Give Up | Saigon Buffalo | 82.9372% | 69.5381% | — |
| 2022-10-02 | Worlds | Evil Geniuses | Detonation FocusMe | 51.8396% | 41.9128% | — |
| 2022-10-02 | Worlds | LOUD | Evil Geniuses | 33.3338% | 50.9396% | — |
| 2022-10-03 | Worlds | MAD Lions | Saigon Buffalo | 61.3522% | 56.8531% | — |
| 2022-10-03 | Worlds | LOUD | Detonation FocusMe | 35.0770% | 43.0707% | — |
| 2022-10-04 | Worlds | Evil Geniuses | MAD Lions | 53.8916% | 53.3791% | — |
| 2022-10-04 | Worlds | Royal Never Give Up | Detonation FocusMe | 72.3310% | 51.9331% | — |
| 2022-10-07 | Worlds | Cloud9 | Fnatic | 54.6573% | 52.3471% | — |
| 2022-10-07 | Worlds | G2 Esports | DWG KIA | 33.6809% | 48.8036% | — |
| 2022-10-07 | Worlds | CTBC Flying Oyster | 100 Thieves | 49.9783% | 54.1622% | — |
| 2022-10-07 | Worlds | JD Gaming | Evil Geniuses | 71.7268% | 58.7697% | — |
| 2022-10-07 | Worlds | T1 | Edward Gaming | 62.5306% | 62.4657% | — |
| 2022-10-07 | Worlds | Gen.G eSports | Royal Never Give Up | 74.3215% | 70.0356% | — |
| 2022-10-08 | Worlds | Rogue | DRX | 38.9986% | 52.8938% | — |
| 2022-10-08 | Worlds | Evil Geniuses | G2 Esports | 44.8011% | 45.6588% | — |
| 2022-10-08 | Worlds | Fnatic | T1 | 20.7028% | 31.6800% | — |
| 2022-10-08 | Worlds | Edward Gaming | Cloud9 | 72.3088% | 60.9629% | — |
| 2022-10-08 | Worlds | Top Esports | GAM Esports | 78.9059% | 63.1645% | — |
| 2022-10-08 | Worlds | DWG KIA | JD Gaming | 44.6543% | 43.5660% | — |
| 2022-10-09 | Worlds | GAM Esports | Rogue | 37.3113% | 42.7433% | — |
| 2022-10-09 | Worlds | 100 Thieves | Gen.G eSports | 12.2611% | 18.6792% | — |
| 2022-10-09 | Worlds | Edward Gaming | Fnatic | 66.4202% | 54.5130% | — |
| 2022-10-09 | Worlds | Cloud9 | T1 | 21.5250% | 29.1197% | — |
| 2022-10-09 | Worlds | Royal Never Give Up | CTBC Flying Oyster | 71.5831% | 60.0115% | — |
| 2022-10-09 | Worlds | DRX | Top Esports | 26.7943% | 27.2403% | — |
| 2022-10-10 | Worlds | JD Gaming | G2 Esports | 70.4257% | 60.6044% | — |
| 2022-10-10 | Worlds | Rogue | Top Esports | 30.6952% | 41.0134% | — |
| 2022-10-10 | Worlds | DWG KIA | Evil Geniuses | 71.6810% | 60.3306% | — |
| 2022-10-10 | Worlds | 100 Thieves | Royal Never Give Up | 18.6273% | 23.7664% | — |
| 2022-10-10 | Worlds | Gen.G eSports | CTBC Flying Oyster | 85.4411% | 75.9616% | — |
| 2022-10-10 | Worlds | GAM Esports | DRX | 31.8468% | 47.6723% | — |
| 2022-10-13 | Worlds | Fnatic | Cloud9 | 63.7738% | 65.2008% | — |
| 2022-10-13 | Worlds | T1 | Fnatic | 74.4246% | 65.9914% | — |
| 2022-10-13 | Worlds | Cloud9 | Edward Gaming | 22.3712% | 29.2520% | — |
| 2022-10-13 | Worlds | Fnatic | Edward Gaming | 33.6573% | 43.6520% | — |
| 2022-10-13 | Worlds | T1 | Cloud9 | 83.6678% | 78.4281% | — |
| 2022-10-13 | Worlds | Edward Gaming | T1 | 40.3824% | 39.9484% | — |
| 2022-10-14 | Worlds | G2 Esports | Evil Geniuses | 61.8065% | 60.6707% | — |
| 2022-10-14 | Worlds | Evil Geniuses | JD Gaming | 19.1353% | 26.4141% | — |
| 2022-10-14 | Worlds | DWG KIA | G2 Esports | 66.8038% | 57.4388% | — |
| 2022-10-14 | Worlds | G2 Esports | JD Gaming | 27.6899% | 35.6390% | — |
| 2022-10-14 | Worlds | Evil Geniuses | DWG KIA | 23.4932% | 32.4478% | — |
| 2022-10-14 | Worlds | JD Gaming | DWG KIA | 56.4777% | 57.2312% | — |
| 2022-10-14 | Worlds | JD Gaming | DWG KIA | 56.4777% | 57.2312% | — |
| 2022-10-15 | Worlds | Rogue | GAM Esports | 66.9050% | 61.3752% | — |
| 2022-10-15 | Worlds | GAM Esports | Top Esports | 17.3131% | 27.6875% | — |
| 2022-10-15 | Worlds | DRX | Rogue | 59.6322% | 50.6611% | — |
| 2022-10-15 | Worlds | DRX | GAM Esports | 74.9144% | 62.0002% | — |
| 2022-10-15 | Worlds | Top Esports | Rogue | 70.2599% | 62.1732% | — |
| 2022-10-15 | Worlds | Top Esports | DRX | 61.5275% | 61.5493% | — |
| 2022-10-15 | Worlds | DRX | Rogue | 59.6322% | 50.6611% | — |
| 2022-10-16 | Worlds | 100 Thieves | CTBC Flying Oyster | 39.4630% | 35.2722% | — |
| 2022-10-16 | Worlds | CTBC Flying Oyster | Gen.G eSports | 10.5906% | 16.8914% | — |
| 2022-10-16 | Worlds | Royal Never Give Up | 100 Thieves | 82.9050% | 79.3817% | — |
| 2022-10-16 | Worlds | Gen.G eSports | 100 Thieves | 92.8319% | 90.0289% | — |
| 2022-10-16 | Worlds | CTBC Flying Oyster | Royal Never Give Up | 24.0304% | 32.2787% | — |
| 2022-10-16 | Worlds | Royal Never Give Up | Gen.G eSports | 27.2447% | 29.8940% | — |
| 2022-10-16 | Worlds | Gen.G eSports | Royal Never Give Up | 72.7553% | 70.1060% | — |
| 2022-10-20 | Worlds | JD Gaming | Rogue | 76.7311% | 70.5600% | — |
| 2022-10-21 | Worlds | T1 | Royal Never Give Up | 61.2050% | 59.1376% | — |
| 2022-10-22 | Worlds | Gen.G eSports | DWG KIA | 72.5569% | 72.4873% | — |
| 2022-10-23 | Worlds | DRX | Edward Gaming | 48.8198% | 48.6096% | — |
| 2022-10-29 | Worlds | T1 | JD Gaming | 58.5670% | 58.1739% | — |
| 2022-10-30 | Worlds | Gen.G eSports | DRX | 78.9762% | 78.3285% | — |
| 2022-11-05 | Worlds | T1 | DRX | 66.1304% | 66.3231% | — |


## S13

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 77 | 64.94% | 61.83% | 0.6267 | 0.2202 |
| 中性先验 · 90 天 | 77 | 58.44% | 54.84% | 0.7167 | 0.2596 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-05-02 | MSI | PSG Talon | Detonation FocusMe | 37.9241% | 55.0334% | — |
| 2023-05-02 | MSI | G2 Esports | LOUD | 61.5393% | 37.6943% | — |
| 2023-05-03 | MSI | Bilibili Gaming | Movistar R7 | 92.0762% | 48.3396% | — |
| 2023-05-03 | MSI | Golden Guardians | GAM Esports | 42.1201% | 31.9802% | — |
| 2023-05-04 | MSI | Bilibili Gaming | Golden Guardians | 79.8211% | 49.5759% | — |
| 2023-05-04 | MSI | G2 Esports | PSG Talon | 44.7967% | 24.7074% | — |
| 2023-05-05 | MSI | GAM Esports | Movistar R7 | 67.0516% | 58.0481% | — |
| 2023-05-05 | MSI | LOUD | Detonation FocusMe | 34.3841% | 40.2357% | — |
| 2023-05-06 | MSI | Golden Guardians | Movistar R7 | 72.4410% | 55.4007% | — |
| 2023-05-06 | MSI | PSG Talon | LOUD | 57.9689% | 61.6127% | — |
| 2023-05-07 | MSI | Golden Guardians | PSG Talon | 44.8391% | 27.0869% | — |
| 2023-05-09 | MSI | Gen.G eSports | G2 Esports | 81.5950% | 36.7788% | — |
| 2023-05-10 | MSI | MAD Lions | T1 | 11.4010% | 31.5260% | — |
| 2023-05-11 | MSI | Cloud9 | Bilibili Gaming | 47.9047% | 72.9837% | — |
| 2023-05-12 | MSI | JD Gaming | Golden Guardians | 85.9078% | 68.5274% | — |
| 2023-05-13 | MSI | Gen.G eSports | T1 | 42.6154% | 43.4617% | — |
| 2023-05-13 | MSI | MAD Lions | G2 Esports | 37.7484% | 37.1128% | — |
| 2023-05-14 | MSI | JD Gaming | Bilibili Gaming | 67.4592% | 66.4972% | — |
| 2023-05-14 | MSI | Golden Guardians | Cloud9 | 39.7533% | 42.5940% | — |
| 2023-05-16 | MSI | G2 Esports | Bilibili Gaming | 32.2980% | 44.8602% | — |
| 2023-05-17 | MSI | Gen.G eSports | Cloud9 | 79.1294% | 51.2979% | — |
| 2023-05-18 | MSI | JD Gaming | T1 | 46.0855% | 56.4445% | — |
| 2023-05-19 | MSI | Bilibili Gaming | Gen.G eSports | 34.5545% | 41.4287% | — |
| 2023-05-20 | MSI | Bilibili Gaming | T1 | 40.3320% | 46.2285% | — |
| 2023-05-21 | MSI | JD Gaming | Bilibili Gaming | 67.6449% | 66.2495% | — |
| 2023-10-10 | Worlds | PSG Talon | Movistar R7 | 67.7248% | 67.9865% | — |
| 2023-10-10 | Worlds | LOUD | GAM Esports | 61.8480% | 66.1305% | — |
| 2023-10-11 | Worlds | Detonation FocusMe | CTBC Flying Oyster | 62.6230% | 48.9023% | — |
| 2023-10-11 | Worlds | Team BDS | Team Whales | 83.7962% | 69.6731% | — |
| 2023-10-12 | Worlds | PSG Talon | LOUD | 60.3764% | 64.1526% | — |
| 2023-10-12 | Worlds | CTBC Flying Oyster | Team Whales | 70.9274% | 80.1883% | — |
| 2023-10-13 | Worlds | Movistar R7 | GAM Esports | 41.8652% | 50.3565% | — |
| 2023-10-13 | Worlds | Detonation FocusMe | Team BDS | 43.5320% | 58.0694% | — |
| 2023-10-14 | Worlds | LOUD | GAM Esports | 52.6077% | 56.2961% | — |
| 2023-10-14 | Worlds | CTBC Flying Oyster | Team BDS | 41.9686% | 63.1091% | — |
| 2023-10-15 | Worlds | GAM Esports | Team Whales | 61.8497% | 62.7795% | — |
| 2023-10-15 | Worlds | PSG Talon | Team BDS | 56.4152% | 72.0726% | — |
| 2023-10-19 | Worlds | T1 | Team Liquid | 89.7286% | 66.5076% | — |
| 2023-10-19 | Worlds | Cloud9 | MAD Lions | 55.8341% | 55.9273% | — |
| 2023-10-19 | Worlds | Gen.G eSports | GAM Esports | 89.6698% | 53.9713% | — |
| 2023-10-19 | Worlds | Team BDS | JD Gaming | 11.7712% | 34.4555% | — |
| 2023-10-19 | Worlds | G2 Esports | Dplus KIA | 41.7985% | 74.9373% | — |
| 2023-10-19 | Worlds | Weibo Gaming | NRG | 84.2082% | 60.6951% | — |
| 2023-10-19 | Worlds | LNG Esports | Fnatic | 82.8324% | 59.0123% | — |
| 2023-10-19 | Worlds | Bilibili Gaming | KT Rolster | 41.3416% | 50.1872% | — |
| 2023-10-20 | Worlds | NRG | Team Liquid | 57.4126% | 56.9995% | — |
| 2023-10-20 | Worlds | Cloud9 | LNG Esports | 16.7793% | 35.0060% | — |
| 2023-10-20 | Worlds | MAD Lions | Team BDS | 39.0748% | 34.0968% | — |
| 2023-10-20 | Worlds | Fnatic | GAM Esports | 51.8206% | 36.9527% | — |
| 2023-10-20 | Worlds | Gen.G eSports | T1 | 66.0565% | 67.2338% | — |
| 2023-10-20 | Worlds | G2 Esports | Weibo Gaming | 40.4464% | 63.0271% | — |
| 2023-10-20 | Worlds | JD Gaming | Bilibili Gaming | 63.8720% | 63.3980% | — |
| 2023-10-20 | Worlds | Dplus KIA | KT Rolster | 33.2837% | 33.4566% | — |
| 2023-10-21 | Worlds | JD Gaming | LNG Esports | 65.3228% | 65.2103% | — |
| 2023-10-21 | Worlds | G2 Esports | Gen.G eSports | 31.0097% | 54.1197% | — |
| 2023-10-22 | Worlds | T1 | Cloud9 | 78.1361% | 55.7446% | — |
| 2023-10-22 | Worlds | NRG | MAD Lions | 42.7346% | 44.2594% | — |
| 2023-10-22 | Worlds | Bilibili Gaming | Fnatic | 83.3768% | 67.5385% | — |
| 2023-10-22 | Worlds | KT Rolster | Weibo Gaming | 64.6775% | 59.7720% | — |
| 2023-10-23 | Worlds | Team Liquid | GAM Esports | 37.6880% | 25.1482% | — |
| 2023-10-23 | Worlds | Dplus KIA | Team BDS | 75.1856% | 46.5153% | — |
| 2023-10-26 | Worlds | Cloud9 | Fnatic | 53.3091% | 53.9003% | — |
| 2023-10-26 | Worlds | MAD Lions | Weibo Gaming | 17.9493% | 33.3807% | — |
| 2023-10-27 | Worlds | Dplus KIA | GAM Esports | 82.8156% | 51.9344% | — |
| 2023-10-27 | Worlds | KT Rolster | LNG Esports | 58.2729% | 54.5534% | — |
| 2023-10-28 | Worlds | NRG | G2 Esports | 20.1425% | 24.1577% | — |
| 2023-10-28 | Worlds | T1 | Bilibili Gaming | 42.3461% | 40.9476% | — |
| 2023-10-29 | Worlds | KT Rolster | Dplus KIA | 65.7996% | 63.4027% | — |
| 2023-10-29 | Worlds | Fnatic | Weibo Gaming | 20.8857% | 36.3630% | — |
| 2023-10-29 | Worlds | G2 Esports | Bilibili Gaming | 28.2632% | 43.7450% | — |
| 2023-11-02 | Worlds | NRG | Weibo Gaming | 23.9194% | 39.4420% | — |
| 2023-11-03 | Worlds | Gen.G eSports | Bilibili Gaming | 67.1333% | 64.1596% | — |
| 2023-11-04 | Worlds | JD Gaming | KT Rolster | 60.2167% | 62.6460% | — |
| 2023-11-05 | Worlds | LNG Esports | T1 | 58.4666% | 59.7040% | — |
| 2023-11-11 | Worlds | Weibo Gaming | Bilibili Gaming | 38.7642% | 40.1296% | — |
| 2023-11-12 | Worlds | T1 | JD Gaming | 33.4874% | 32.3833% | — |
| 2023-11-19 | Worlds | Weibo Gaming | T1 | 35.9129% | 39.8219% | — |


## S14

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 74 | 67.57% | 59.24% | 0.6539 | 0.2312 |
| 中性先验 · 90 天 | 74 | 62.16% | 56.52% | 0.7103 | 0.2561 |
| 无正则 MLE · 可识别子集 | 0 | — | — | — | — |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-05-01 | MSI | FlyQuest | PSG Talon | 24.8570% | 16.0271% | — |
| 2024-05-01 | MSI | T1 | Estral Esports | 90.3268% | 33.9987% | — |
| 2024-05-02 | MSI | Fnatic | GAM Esports | 39.3213% | 34.7050% | — |
| 2024-05-02 | MSI | Top Esports | LOUD | 91.2758% | 57.7444% | — |
| 2024-05-03 | MSI | T1 | FlyQuest | 85.7694% | 58.3887% | — |
| 2024-05-03 | MSI | Top Esports | Fnatic | 85.4323% | 66.3136% | — |
| 2024-05-04 | MSI | PSG Talon | Estral Esports | 70.5928% | 62.3725% | — |
| 2024-05-04 | MSI | LOUD | GAM Esports | 42.1380% | 53.2019% | — |
| 2024-05-05 | MSI | FlyQuest | PSG Talon | 38.7384% | 27.9458% | — |
| 2024-05-05 | MSI | Fnatic | GAM Esports | 63.1888% | 54.6123% | — |
| 2024-05-07 | MSI | Team Liquid | Top Esports | 15.0934% | 33.2297% | — |
| 2024-05-08 | MSI | Gen.G eSports | Fnatic | 88.8123% | 72.0813% | — |
| 2024-05-09 | MSI | Bilibili Gaming | PSG Talon | 79.8652% | 47.9721% | — |
| 2024-05-10 | MSI | G2 Esports | T1 | 22.2199% | 41.7503% | — |
| 2024-05-11 | MSI | Fnatic | Team Liquid | 65.1309% | 60.2682% | — |
| 2024-05-11 | MSI | Gen.G eSports | Top Esports | 69.6464% | 64.0359% | — |
| 2024-05-12 | MSI | G2 Esports | PSG Talon | 49.4984% | 37.5192% | — |
| 2024-05-12 | MSI | Bilibili Gaming | T1 | 51.2617% | 54.5709% | — |
| 2024-05-14 | MSI | Top Esports | G2 Esports | 61.4274% | 49.4657% | — |
| 2024-05-15 | MSI | T1 | Team Liquid | 84.2925% | 74.8579% | — |
| 2024-05-16 | MSI | Gen.G eSports | Bilibili Gaming | 55.9148% | 52.2363% | — |
| 2024-05-17 | MSI | T1 | G2 Esports | 54.6594% | 45.7149% | — |
| 2024-05-18 | MSI | Bilibili Gaming | T1 | 47.6376% | 47.5831% | — |
| 2024-05-19 | MSI | Gen.G eSports | Bilibili Gaming | 60.5053% | 57.8973% | — |
| 2024-09-25 | Worlds | MAD Lions KOI | Vikings Esports | 42.4283% | 32.6309% | — |
| 2024-09-25 | Worlds | PSG Talon | paiN Gaming | 83.1528% | 76.4866% | — |
| 2024-09-26 | Worlds | GAM Esports | SoftBank Hawks Gaming | 36.1970% | 26.5472% | — |
| 2024-09-26 | Worlds | 100 Thieves | Movistar R7 | 64.6131% | 30.9815% | — |
| 2024-09-27 | Worlds | MAD Lions KOI | PSG Talon | 25.1436% | 16.7831% | — |
| 2024-09-27 | Worlds | GAM Esports | Movistar R7 | 71.1513% | 56.0714% | — |
| 2024-09-28 | Worlds | paiN Gaming | Vikings Esports | 45.0162% | 55.0941% | — |
| 2024-09-28 | Worlds | SoftBank Hawks Gaming | 100 Thieves | 65.8995% | 75.0883% | — |
| 2024-09-29 | Worlds | paiN Gaming | Movistar R7 | 73.4900% | 69.0324% | — |
| 2024-09-29 | Worlds | PSG Talon | 100 Thieves | 76.2570% | 79.0653% | — |
| 2024-10-03 | Worlds | Bilibili Gaming | MAD Lions KOI | 85.1354% | 71.6047% | — |
| 2024-10-03 | Worlds | Top Esports | T1 | 54.7382% | 55.1796% | — |
| 2024-10-03 | Worlds | Gen.G eSports | Weibo Gaming | 87.5268% | 87.5777% | — |
| 2024-10-03 | Worlds | Fnatic | Dplus KIA | 29.2906% | 48.8728% | — |
| 2024-10-03 | Worlds | Team Liquid | LNG Esports | 40.0437% | 61.4861% | — |
| 2024-10-03 | Worlds | Hanwha Life eSports | PSG Talon | 81.4503% | 55.6541% | — |
| 2024-10-03 | Worlds | GAM Esports | FlyQuest | 43.2301% | 51.1701% | — |
| 2024-10-03 | Worlds | G2 Esports | paiN Gaming | 75.4225% | 58.1378% | — |
| 2024-10-04 | Worlds | Bilibili Gaming | LNG Esports | 70.3499% | 71.5661% | — |
| 2024-10-04 | Worlds | Gen.G eSports | Top Esports | 71.4324% | 70.1695% | — |
| 2024-10-04 | Worlds | G2 Esports | Hanwha Life eSports | 23.5245% | 38.0860% | — |
| 2024-10-04 | Worlds | Team Liquid | Weibo Gaming | 41.5666% | 61.2451% | — |
| 2024-10-04 | Worlds | T1 | paiN Gaming | 84.6265% | 58.1342% | — |
| 2024-10-04 | Worlds | Dplus KIA | FlyQuest | 74.7592% | 55.1092% | — |
| 2024-10-04 | Worlds | Fnatic | GAM Esports | 62.5914% | 51.7903% | — |
| 2024-10-04 | Worlds | PSG Talon | MAD Lions KOI | 64.7948% | 72.0885% | — |
| 2024-10-05 | Worlds | Dplus KIA | LNG Esports | 57.7312% | 58.7353% | — |
| 2024-10-05 | Worlds | Hanwha Life eSports | Gen.G eSports | 37.5942% | 38.1866% | — |
| 2024-10-06 | Worlds | Top Esports | Fnatic | 82.8854% | 71.5160% | — |
| 2024-10-06 | Worlds | Bilibili Gaming | T1 | 60.4169% | 59.3406% | — |
| 2024-10-06 | Worlds | FlyQuest | PSG Talon | 38.7355% | 32.2292% | — |
| 2024-10-06 | Worlds | G2 Esports | Weibo Gaming | 50.0037% | 66.3805% | — |
| 2024-10-07 | Worlds | MAD Lions KOI | GAM Esports | 55.3856% | 46.6571% | — |
| 2024-10-07 | Worlds | Team Liquid | paiN Gaming | 65.8478% | 50.4989% | — |
| 2024-10-10 | Worlds | Top Esports | Dplus KIA | 62.8882% | 63.9065% | — |
| 2024-10-10 | Worlds | Hanwha Life eSports | FlyQuest | 87.0945% | 75.7044% | — |
| 2024-10-11 | Worlds | G2 Esports | T1 | 38.2965% | 50.9451% | — |
| 2024-10-11 | Worlds | Bilibili Gaming | PSG Talon | 78.6935% | 58.2579% | — |
| 2024-10-12 | Worlds | Fnatic | Weibo Gaming | 33.1665% | 48.0109% | — |
| 2024-10-12 | Worlds | Team Liquid | GAM Esports | 68.5411% | 61.5443% | — |
| 2024-10-13 | Worlds | Dplus KIA | Weibo Gaming | 57.6669% | 57.2181% | — |
| 2024-10-13 | Worlds | G2 Esports | Bilibili Gaming | 26.1814% | 35.2854% | — |
| 2024-10-13 | Worlds | FlyQuest | Team Liquid | 47.3235% | 47.7680% | — |
| 2024-10-17 | Worlds | Weibo Gaming | LNG Esports | 40.4778% | 41.1525% | — |
| 2024-10-18 | Worlds | Hanwha Life eSports | Bilibili Gaming | 55.4524% | 54.3102% | — |
| 2024-10-19 | Worlds | Top Esports | T1 | 62.3485% | 61.4940% | — |
| 2024-10-20 | Worlds | Gen.G eSports | FlyQuest | 89.8741% | 82.2078% | — |
| 2024-10-26 | Worlds | Weibo Gaming | Bilibili Gaming | 28.5258% | 27.0492% | — |
| 2024-10-27 | Worlds | T1 | Gen.G eSports | 29.8494% | 30.0791% | — |
| 2024-11-02 | Worlds | T1 | Bilibili Gaming | 42.2590% | 41.9599% | — |


## S15

| 模型 | 覆盖系列赛 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 赛区先验 · 90 天 | 60 | 81.67% | 67.68% | 0.6147 | 0.2131 |
| 中性先验 · 90 天 | 60 | 71.67% | 62.20% | 0.6445 | 0.2269 |
| 无正则 MLE · 可识别子集 | 19 | 73.68% | 58.75% | 0.6971 | 0.2472 |


| 日期 | 赛事 | A 队 | B 队 | 赛区先验 | 中性先验 | 无正则 MLE |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-06-27 | MSI | FURIA | G2 Esports | 28.7523% | 43.1795% | 13.7662% |
| 2025-06-27 | MSI | Bilibili Gaming | GAM Esports | 73.7669% | 51.9184% | 30.0136% |
| 2025-06-28 | MSI | GAM Esports | FURIA | 55.7971% | 48.0460% | 48.1978% |
| 2025-06-28 | MSI | Bilibili Gaming | G2 Esports | 73.9520% | 58.3159% | 57.5765% |
| 2025-06-29 | MSI | G2 Esports | GAM Esports | 54.6075% | 50.4530% | 53.1436% |
| 2025-07-01 | MSI | Gen.G eSports | G2 Esports | 88.8153% | 79.9823% | 93.4177% |
| 2025-07-02 | MSI | Anyone s Legend | FlyQuest | 54.0510% | 37.8590% | 32.9782% |
| 2025-07-03 | MSI | Movistar KOI | Bilibili Gaming | 22.5471% | 31.5780% | 23.5724% |
| 2025-07-03 | MSI | CTBC Flying Oyster | T1 | 34.2004% | 51.1576% | 31.4559% |
| 2025-07-04 | MSI | FlyQuest | G2 Esports | 70.9838% | 70.0566% | 73.1255% |
| 2025-07-04 | MSI | Anyone s Legend | Gen.G eSports | 41.7738% | 41.6020% | 37.7424% |
| 2025-07-05 | MSI | CTBC Flying Oyster | Movistar KOI | 61.6750% | 63.3661% | 63.4389% |
| 2025-07-05 | MSI | Bilibili Gaming | T1 | 55.4163% | 55.3480% | 53.4174% |
| 2025-07-07 | MSI | CTBC Flying Oyster | Anyone s Legend | 32.9667% | 42.9606% | 35.5469% |
| 2025-07-08 | MSI | FlyQuest | Bilibili Gaming | 49.8069% | 57.9476% | 55.4782% |
| 2025-07-09 | MSI | T1 | Gen.G eSports | 37.2930% | 37.6118% | 36.8843% |
| 2025-07-10 | MSI | Anyone s Legend | Bilibili Gaming | 55.8840% | 55.3891% | 56.3747% |
| 2025-07-11 | MSI | T1 | Anyone s Legend | 48.0896% | 46.8786% | 52.0585% |
| 2025-07-12 | MSI | Gen.G eSports | T1 | 61.4936% | 61.1250% | 62.1449% |
| 2025-10-14 | Worlds | Invictus Gaming | T1 | 43.2460% | 42.4005% | — |
| 2025-10-15 | Worlds | Team Secret Whales | Vivo Keyd Stars | 50.8262% | 47.7275% | — |
| 2025-10-15 | Worlds | CTBC Flying Oyster | Fnatic | 62.6317% | 64.5987% | — |
| 2025-10-15 | Worlds | KT Rolster | Movistar KOI | 63.4556% | 53.4986% | — |
| 2025-10-15 | Worlds | Bilibili Gaming | 100 Thieves | 79.7319% | 68.6810% | — |
| 2025-10-15 | Worlds | FlyQuest | T1 | 36.5194% | 48.3059% | — |
| 2025-10-15 | Worlds | Hanwha Life eSports | Anyone s Legend | 55.0464% | 54.7866% | — |
| 2025-10-15 | Worlds | G2 Esports | Top Esports | 33.2666% | 41.9419% | — |
| 2025-10-15 | Worlds | Gen.G eSports | PSG Talon | 93.1278% | 88.2993% | — |
| 2025-10-16 | Worlds | Vivo Keyd Stars | FlyQuest | 21.1174% | 25.0653% | — |
| 2025-10-16 | Worlds | KT Rolster | Team Secret Whales | 72.0465% | 59.0192% | — |
| 2025-10-16 | Worlds | Movistar KOI | G2 Esports | 38.8941% | 39.1014% | — |
| 2025-10-16 | Worlds | Top Esports | 100 Thieves | 79.6439% | 69.3210% | — |
| 2025-10-16 | Worlds | CTBC Flying Oyster | T1 | 30.9472% | 41.0259% | — |
| 2025-10-16 | Worlds | Gen.G eSports | Anyone s Legend | 65.7366% | 65.8303% | — |
| 2025-10-16 | Worlds | Bilibili Gaming | Fnatic | 77.5609% | 71.0384% | — |
| 2025-10-16 | Worlds | Hanwha Life eSports | PSG Talon | 88.3784% | 81.3985% | — |
| 2025-10-17 | Worlds | CTBC Flying Oyster | Anyone s Legend | 33.9418% | 43.1075% | — |
| 2025-10-17 | Worlds | KT Rolster | Top Esports | 34.3048% | 34.2962% | — |
| 2025-10-18 | Worlds | Bilibili Gaming | G2 Esports | 66.2170% | 60.0240% | — |
| 2025-10-18 | Worlds | Gen.G eSports | T1 | 62.5537% | 62.4736% | — |
| 2025-10-18 | Worlds | FlyQuest | Team Secret Whales | 74.6425% | 73.7360% | — |
| 2025-10-18 | Worlds | Hanwha Life eSports | 100 Thieves | 84.2617% | 76.6204% | — |
| 2025-10-19 | Worlds | PSG Talon | Vivo Keyd Stars | 48.9822% | 45.2646% | — |
| 2025-10-19 | Worlds | Movistar KOI | Fnatic | 52.5684% | 52.0123% | — |
| 2025-10-22 | Worlds | CTBC Flying Oyster | Hanwha Life eSports | 29.8736% | 37.4232% | — |
| 2025-10-22 | Worlds | FlyQuest | G2 Esports | 58.4330% | 61.1284% | — |
| 2025-10-23 | Worlds | Movistar KOI | Team Secret Whales | 61.0424% | 57.0898% | — |
| 2025-10-23 | Worlds | Gen.G eSports | Top Esports | 70.6477% | 71.0144% | — |
| 2025-10-24 | Worlds | Bilibili Gaming | Vivo Keyd Stars | 82.7356% | 73.4354% | — |
| 2025-10-24 | Worlds | 100 Thieves | T1 | 15.2448% | 22.0522% | — |
| 2025-10-25 | Worlds | CTBC Flying Oyster | FlyQuest | 46.6932% | 45.7616% | — |
| 2025-10-25 | Worlds | Top Esports | Bilibili Gaming | 51.5645% | 50.5903% | — |
| 2025-10-25 | Worlds | Movistar KOI | T1 | 18.4383% | 23.1204% | — |
| 2025-10-28 | Worlds | Gen.G eSports | Hanwha Life eSports | 61.3294% | 61.1702% | — |
| 2025-10-29 | Worlds | KT Rolster | CTBC Flying Oyster | 57.4545% | 49.1130% | — |
| 2025-10-30 | Worlds | Top Esports | G2 Esports | 64.3773% | 57.4928% | — |
| 2025-10-31 | Worlds | Anyone s Legend | T1 | 42.8194% | 42.6501% | — |
| 2025-11-01 | Worlds | Gen.G eSports | KT Rolster | 74.5304% | 74.6371% | — |
| 2025-11-02 | Worlds | T1 | Top Esports | 61.1845% | 61.3506% | — |
| 2025-11-09 | Worlds | KT Rolster | T1 | 41.2968% | 40.9327% | — |

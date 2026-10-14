# 半衰期敏感性分析附录

[模型细节](../../MODEL.md) · [先验与 MLE 对照](model_comparison.md)

主结果固定使用 **90 天**。以下保留此前 30、60、180 天的对照，不参与主结果排序或参数选择。只有 90 天完成了 S16 全赛事模拟；其他半衰期没有全赛程夺冠概率。历史对照衡量逐场预测，不是赛前冠军预测。

## S16 两两胜率

- [30 天](matchups-30.md)
- [60 天](matchups-60.md)
- [180 天](matchups-180.md)

## S16 入围赛精确晋级概率

| 队伍 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- |
| KC | 67.23496761% | 76.82974719% | 78.45904759% | 77.75399083% |
| C9 | 31.49719188% | 20.00827352% | 16.10269516% | 13.00435390% |
| FUR | 1.26783986% | 3.16194435% | 5.43819808% | 9.24159715% |
| MVK | 0.00000064% | 0.00003495% | 0.00005918% | 0.00005811% |

## 历史逐场回测汇总

| 半衰期 | 系列赛数 | 系列赛命中率 | 小局命中率 | 小局 Log loss | 小局 Brier |
| --- | --- | --- | --- | --- | --- |
| 30 | 1300 | 66.27% | 63.79% | 0.6396 | 0.2235 |
| 60 | 1300 | 67.73% | 64.91% | 0.6310 | 0.2197 |
| 90 | 1300 | 68.96% | 65.62% | 0.6273 | 0.2179 |
| 180 | 1300 | 69.96% | 66.64% | 0.6237 | 0.2161 |

对照结果较高不能证明该参数在独立样本上更优；没有按这些成绩重新选择半衰期。

## S4 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2014-09-18 | Worlds | Edward Gaming | Samsung Galaxy White | 40.3446% | 42.5983% | 43.3709% | 44.1531% |
| 2014-09-18 | Worlds | Team SoloMid | SK Gaming | 32.1808% | 36.7376% | 39.4119% | 43.1296% |
| 2014-09-18 | Worlds | Dark Passage | ahq e-Sports Club | 60.7070% | 61.5404% | 61.8272% | 62.1184% |
| 2014-09-18 | Worlds | Taipei Assassins | Star Horn Royal Club | 17.1192% | 12.1556% | 10.2803% | 8.4316% |
| 2014-09-18 | Worlds | Samsung Galaxy White | ahq e-Sports Club | 86.2980% | 86.8086% | 86.9793% | 87.1502% |
| 2014-09-18 | Worlds | Star Horn Royal Club | Team SoloMid | 67.4285% | 67.4598% | 67.0455% | 66.0882% |
| 2014-09-19 | Worlds | Taipei Assassins | SK Gaming | 20.1377% | 16.5052% | 15.0442% | 13.4710% |
| 2014-09-19 | Worlds | Edward Gaming | Dark Passage | 81.0203% | 82.3031% | 82.7195% | 83.1300% |
| 2014-09-19 | Worlds | Star Horn Royal Club | SK Gaming | 79.8672% | 80.4140% | 81.0196% | 81.9309% |
| 2014-09-19 | Worlds | Dark Passage | Samsung Galaxy White | 3.5584% | 3.4259% | 3.3819% | 3.3381% |
| 2014-09-19 | Worlds | Team SoloMid | Taipei Assassins | 78.4189% | 82.5325% | 84.6748% | 87.2212% |
| 2014-09-19 | Worlds | Edward Gaming | ahq e-Sports Club | 58.4589% | 60.5514% | 61.2504% | 61.9494% |
| 2014-09-20 | Worlds | Samsung Galaxy White | Dark Passage | 97.9578% | 98.0338% | 98.0589% | 98.0838% |
| 2014-09-20 | Worlds | SK Gaming | Star Horn Royal Club | 10.3427% | 10.6344% | 10.5841% | 10.4229% |
| 2014-09-20 | Worlds | ahq e-Sports Club | Samsung Galaxy White | 5.5120% | 5.3512% | 5.2972% | 5.2431% |
| 2014-09-20 | Worlds | Taipei Assassins | Team SoloMid | 32.8371% | 29.7423% | 27.3386% | 23.9731% |
| 2014-09-20 | Worlds | Dark Passage | Edward Gaming | 7.2140% | 6.8732% | 6.7614% | 6.6504% |
| 2014-09-20 | Worlds | SK Gaming | Taipei Assassins | 55.7270% | 61.3326% | 63.9877% | 67.1641% |
| 2014-09-21 | Worlds | Team SoloMid | Star Horn Royal Club | 14.7967% | 13.7511% | 13.6026% | 13.6869% |
| 2014-09-21 | Worlds | ahq e-Sports Club | Dark Passage | 74.7623% | 74.9531% | 75.0167% | 75.0804% |
| 2014-09-21 | Worlds | Star Horn Royal Club | Taipei Assassins | 95.8313% | 96.3478% | 96.6122% | 96.9375% |
| 2014-09-21 | Worlds | ahq e-Sports Club | Edward Gaming | 15.3796% | 14.8210% | 14.6359% | 14.4514% |
| 2014-09-21 | Worlds | SK Gaming | Team SoloMid | 38.0987% | 39.9782% | 39.8394% | 38.9564% |
| 2014-09-21 | Worlds | Samsung Galaxy White | Edward Gaming | 79.4648% | 79.3036% | 79.2503% | 79.1974% |
| 2014-09-21 | Worlds | Edward Gaming | ahq e-Sports Club | 84.6204% | 85.1790% | 85.3641% | 85.5486% |
| 2014-09-25 | Worlds | LMQ | OMG | 34.0711% | 33.3268% | 31.5766% | 29.2223% |
| 2014-09-25 | Worlds | NaJin White Shield | KaBuM! eSports | 80.3016% | 80.4405% | 80.4854% | 80.5296% |
| 2014-09-25 | Worlds | Samsung Galaxy Blue | OMG | 60.8392% | 56.5544% | 53.4940% | 49.6260% |
| 2014-09-25 | Worlds | Cloud 9 | Alliance | 37.3173% | 45.4598% | 50.4737% | 56.6526% |
| 2014-09-25 | Worlds | Fnatic | LMQ | 61.7915% | 56.9825% | 54.6996% | 52.0580% |
| 2014-09-25 | Worlds | Cloud 9 | KaBuM! eSports | 67.7856% | 71.2178% | 72.7409% | 74.5109% |
| 2014-09-26 | Worlds | NaJin White Shield | Alliance | 70.5091% | 71.7611% | 73.5728% | 75.9852% |
| 2014-09-26 | Worlds | Samsung Galaxy Blue | Fnatic | 81.4377% | 82.8085% | 84.2203% | 85.9656% |
| 2014-09-26 | Worlds | NaJin White Shield | Cloud 9 | 61.4357% | 61.8840% | 61.6210% | 60.9128% |
| 2014-09-26 | Worlds | OMG | Fnatic | 36.5565% | 46.2412% | 52.7148% | 60.3198% |
| 2014-09-26 | Worlds | Alliance | KaBuM! eSports | 83.2428% | 82.5874% | 81.2546% | 79.1830% |
| 2014-09-26 | Worlds | Samsung Galaxy Blue | LMQ | 73.0456% | 75.5511% | 77.1891% | 79.1291% |
| 2014-09-27 | Worlds | Fnatic | OMG | 51.3901% | 47.2826% | 43.7605% | 38.9236% |
| 2014-09-27 | Worlds | Alliance | Cloud 9 | 43.8397% | 42.3485% | 39.9942% | 36.5110% |
| 2014-09-27 | Worlds | LMQ | Fnatic | 56.1548% | 55.9884% | 56.3196% | 56.8922% |
| 2014-09-27 | Worlds | KaBuM! eSports | NaJin White Shield | 2.3827% | 2.3290% | 2.3033% | 2.2659% |
| 2014-09-27 | Worlds | OMG | Samsung Galaxy Blue | 29.7234% | 32.7053% | 34.9701% | 38.1378% |
| 2014-09-27 | Worlds | Alliance | NaJin White Shield | 13.6583% | 13.2147% | 12.4859% | 11.4571% |
| 2014-09-28 | Worlds | KaBuM! eSports | Cloud 9 | 12.1341% | 10.9596% | 10.3615% | 9.6231% |
| 2014-09-28 | Worlds | LMQ | Samsung Galaxy Blue | 24.4035% | 24.1805% | 23.7139% | 22.9329% |
| 2014-09-28 | Worlds | KaBuM! eSports | Alliance | 8.0452% | 8.8590% | 9.5037% | 10.3971% |
| 2014-09-28 | Worlds | Fnatic | Samsung Galaxy Blue | 26.6941% | 26.4660% | 25.8060% | 24.6967% |
| 2014-09-28 | Worlds | Cloud 9 | NaJin White Shield | 27.4414% | 29.9537% | 31.5692% | 33.7277% |
| 2014-09-28 | Worlds | OMG | LMQ | 54.1978% | 55.9165% | 57.7480% | 60.5747% |
| 2014-09-28 | Worlds | NaJin White Shield | Cloud 9 | 72.5586% | 70.0463% | 68.4308% | 66.2723% |
| 2014-10-03 | Worlds | Samsung Galaxy White | Team SoloMid | 87.1950% | 88.4543% | 88.8911% | 89.2340% |
| 2014-10-04 | Worlds | Samsung Galaxy Blue | Cloud 9 | 75.2169% | 75.6268% | 75.5853% | 75.4145% |
| 2014-10-05 | Worlds | Star Horn Royal Club | Edward Gaming | 72.9526% | 74.1959% | 74.5240% | 74.8372% |
| 2014-10-06 | Worlds | NaJin White Shield | OMG | 63.1068% | 61.4540% | 59.9715% | 57.6581% |
| 2014-10-11 | Worlds | Samsung Galaxy Blue | Samsung Galaxy White | 48.2004% | 48.2740% | 48.3398% | 48.4355% |
| 2014-10-12 | Worlds | Star Horn Royal Club | OMG | 48.3628% | 49.2173% | 49.3037% | 48.9854% |
| 2014-10-19 | Worlds | Star Horn Royal Club | Samsung Galaxy White | 21.9041% | 20.9393% | 20.6003% | 20.2990% |


## S5 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-05-07 | MSI | Fnatic | Team SoloMid | 32.2090% | 34.7723% | 37.1433% | 40.3295% |
| 2015-05-07 | MSI | Besiktas E-Sports Club | SKTelecom T1 | 11.8138% | 13.8734% | 14.8838% | 15.9175% |
| 2015-05-07 | MSI | Edward Gaming | AHQ E-Sports Club | 72.4584% | 70.5353% | 70.1433% | 70.0005% |
| 2015-05-07 | MSI | Besiktas E-Sports Club | Team SoloMid | 25.6340% | 23.5820% | 23.5103% | 23.7716% |
| 2015-05-07 | MSI | Fnatic | AHQ E-Sports Club | 40.3573% | 38.3344% | 38.2556% | 38.4836% |
| 2015-05-07 | MSI | SKTelecom T1 | Edward Gaming | 58.2094% | 48.2724% | 43.9611% | 39.5200% |
| 2015-05-07 | MSI | AHQ E-Sports Club | Besiktas E-Sports Club | 67.0731% | 73.5372% | 75.6273% | 77.6010% |
| 2015-05-07 | MSI | SKTelecom T1 | Team SoloMid | 72.0129% | 65.7035% | 63.7384% | 62.2256% |
| 2015-05-08 | MSI | Edward Gaming | Fnatic | 76.9460% | 77.0347% | 77.0135% | 77.0125% |
| 2015-05-08 | MSI | Team SoloMid | AHQ E-Sports Club | 44.9152% | 44.2878% | 43.0746% | 41.2916% |
| 2015-05-08 | MSI | Edward Gaming | Besiktas E-Sports Club | 91.3745% | 92.3364% | 92.8102% | 93.3639% |
| 2015-05-08 | MSI | SKTelecom T1 | Fnatic | 87.4315% | 82.5409% | 79.8462% | 76.5895% |
| 2015-05-08 | MSI | Team SoloMid | Edward Gaming | 28.7373% | 28.9070% | 28.0122% | 26.5180% |
| 2015-05-08 | MSI | Fnatic | Besiktas E-Sports Club | 76.0419% | 78.2225% | 79.3937% | 80.7675% |
| 2015-05-08 | MSI | AHQ E-Sports Club | SKTelecom T1 | 19.1781% | 26.6280% | 30.3077% | 34.4443% |
| 2015-05-09 | MSI | SKTelecom T1 | Fnatic | 89.9263% | 86.0071% | 83.8443% | 81.1702% |
| 2015-05-09 | MSI | Edward Gaming | AHQ E-Sports Club | 68.9971% | 68.5259% | 68.6559% | 69.0029% |
| 2015-05-10 | MSI | SKTelecom T1 | Edward Gaming | 50.7967% | 46.3673% | 43.9869% | 41.2436% |
| 2015-10-01 | Worlds | Fnatic | Invictus Gaming | 50.8216% | 54.2585% | 54.1557% | 53.8465% |
| 2015-10-01 | Worlds | Cloud 9 | AHQ E-Sports Club | 53.4948% | 41.3693% | 36.7295% | 32.1612% |
| 2015-10-01 | Worlds | SKTelecom T1 | H2k-Gaming | 89.8157% | 89.0791% | 87.6103% | 84.9604% |
| 2015-10-01 | Worlds | Edward Gaming | Bangkok Titans | 86.1978% | 92.3058% | 94.3808% | 96.2369% |
| 2015-10-01 | Worlds | Counter Logic Gaming | Flash Wolves | 83.9819% | 83.9454% | 81.2045% | 75.6125% |
| 2015-10-01 | Worlds | paiN Gaming | KOO Tigers | 32.6806% | 31.3111% | 28.5890% | 21.8721% |
| 2015-10-02 | Worlds | KT Rolster | Team SoloMid | 76.9429% | 70.7397% | 67.3305% | 63.4700% |
| 2015-10-02 | Worlds | LGD Gaming | Origen | 61.4643% | 61.6933% | 61.3093% | 60.1956% |
| 2015-10-02 | Worlds | Bangkok Titans | SKTelecom T1 | 4.6219% | 3.4067% | 3.0378% | 2.6197% |
| 2015-10-02 | Worlds | H2k-Gaming | Edward Gaming | 22.5791% | 20.9561% | 20.4655% | 20.3669% |
| 2015-10-02 | Worlds | Flash Wolves | KOO Tigers | 8.8293% | 7.9999% | 8.6815% | 10.3132% |
| 2015-10-02 | Worlds | Counter Logic Gaming | paiN Gaming | 75.0254% | 71.8655% | 70.2372% | 70.3705% |
| 2015-10-03 | Worlds | Edward Gaming | SKTelecom T1 | 27.1389% | 31.4376% | 35.3131% | 40.8121% |
| 2015-10-03 | Worlds | H2k-Gaming | Bangkok Titans | 67.5813% | 77.5393% | 82.1116% | 87.1737% |
| 2015-10-03 | Worlds | LGD Gaming | KT Rolster | 35.4871% | 40.8448% | 44.4172% | 49.4829% |
| 2015-10-03 | Worlds | Origen | Team SoloMid | 66.0662% | 58.1669% | 56.8648% | 57.6262% |
| 2015-10-03 | Worlds | Invictus Gaming | Cloud 9 | 57.7879% | 60.2352% | 62.3907% | 65.5444% |
| 2015-10-03 | Worlds | AHQ E-Sports Club | Fnatic | 13.0061% | 22.3547% | 27.2852% | 32.5456% |
| 2015-10-04 | Worlds | Team SoloMid | LGD Gaming | 39.8110% | 43.8948% | 44.1490% | 42.7363% |
| 2015-10-04 | Worlds | KT Rolster | Origen | 67.2666% | 64.6136% | 61.6177% | 56.5344% |
| 2015-10-04 | Worlds | Invictus Gaming | AHQ E-Sports Club | 46.6165% | 45.3921% | 45.2709% | 45.3742% |
| 2015-10-04 | Worlds | Cloud 9 | Fnatic | 44.8911% | 34.4695% | 31.4798% | 28.4433% |
| 2015-10-04 | Worlds | KOO Tigers | Counter Logic Gaming | 41.8012% | 51.6073% | 56.8294% | 63.3698% |
| 2015-10-04 | Worlds | paiN Gaming | Flash Wolves | 40.4132% | 48.0406% | 48.5772% | 44.7249% |
| 2015-10-08 | Worlds | Counter Logic Gaming | KOO Tigers | 47.8803% | 45.7441% | 42.6285% | 37.4383% |
| 2015-10-08 | Worlds | Flash Wolves | paiN Gaming | 37.6633% | 34.1863% | 34.8169% | 39.1188% |
| 2015-10-08 | Worlds | KOO Tigers | paiN Gaming | 74.0812% | 75.6652% | 76.8530% | 79.6074% |
| 2015-10-08 | Worlds | Flash Wolves | Counter Logic Gaming | 18.7061% | 16.5375% | 17.7979% | 21.5718% |
| 2015-10-08 | Worlds | KOO Tigers | Flash Wolves | 82.5499% | 85.6856% | 86.1419% | 85.8666% |
| 2015-10-08 | Worlds | paiN Gaming | Counter Logic Gaming | 27.5808% | 27.6126% | 28.8433% | 29.9753% |
| 2015-10-09 | Worlds | SKTelecom T1 | Edward Gaming | 79.7927% | 74.7531% | 70.5498% | 64.4853% |
| 2015-10-09 | Worlds | Bangkok Titans | H2k-Gaming | 24.4946% | 18.8402% | 15.6612% | 11.7432% |
| 2015-10-09 | Worlds | Bangkok Titans | Edward Gaming | 11.9115% | 7.8420% | 6.0564% | 4.2369% |
| 2015-10-09 | Worlds | H2k-Gaming | SKTelecom T1 | 9.5481% | 11.0164% | 12.6579% | 15.4785% |
| 2015-10-09 | Worlds | Edward Gaming | H2k-Gaming | 70.5803% | 73.1763% | 74.2295% | 75.0459% |
| 2015-10-09 | Worlds | SKTelecom T1 | Bangkok Titans | 96.6889% | 97.2064% | 97.3794% | 97.6213% |
| 2015-10-10 | Worlds | Team SoloMid | Origen | 31.1535% | 38.7023% | 40.7072% | 41.0329% |
| 2015-10-10 | Worlds | KT Rolster | LGD Gaming | 73.6523% | 67.9416% | 64.1313% | 58.4631% |
| 2015-10-10 | Worlds | Team SoloMid | KT Rolster | 23.2356% | 28.6314% | 32.1543% | 36.3445% |
| 2015-10-10 | Worlds | Origen | LGD Gaming | 65.1553% | 57.3850% | 55.2421% | 53.5933% |
| 2015-10-10 | Worlds | Origen | KT Rolster | 40.0808% | 38.8526% | 40.8394% | 45.0702% |
| 2015-10-10 | Worlds | LGD Gaming | Team SoloMid | 54.1673% | 54.0478% | 54.1312% | 55.4440% |
| 2015-10-11 | Worlds | AHQ E-Sports Club | Invictus Gaming | 37.1596% | 45.6095% | 48.6593% | 50.8822% |
| 2015-10-11 | Worlds | Fnatic | Cloud 9 | 45.8055% | 60.9876% | 65.3759% | 69.1604% |
| 2015-10-11 | Worlds | AHQ E-Sports Club | Cloud 9 | 33.0418% | 49.5440% | 56.0658% | 62.0365% |
| 2015-10-11 | Worlds | Invictus Gaming | Fnatic | 49.6814% | 42.8259% | 41.6263% | 41.2941% |
| 2015-10-11 | Worlds | Cloud 9 | Invictus Gaming | 54.5107% | 46.0623% | 42.6175% | 38.7981% |
| 2015-10-11 | Worlds | Fnatic | AHQ E-Sports Club | 63.1375% | 61.4207% | 59.6709% | 57.8479% |
| 2015-10-11 | Worlds | Cloud 9 | AHQ E-Sports Club | 66.9582% | 50.4560% | 43.9342% | 37.9635% |
| 2015-10-15 | Worlds | Flash Wolves | Origen | 48.0336% | 42.1312% | 38.2925% | 33.7805% |
| 2015-10-16 | Worlds | SKTelecom T1 | AHQ E-Sports Club | 87.1574% | 84.4259% | 82.3159% | 79.2656% |
| 2015-10-17 | Worlds | Fnatic | Edward Gaming | 50.5155% | 50.1116% | 47.7316% | 44.0043% |
| 2015-10-18 | Worlds | KT Rolster | KOO Tigers | 60.3851% | 54.0106% | 50.9074% | 46.8429% |
| 2015-10-24 | Worlds | SKTelecom T1 | Origen | 84.8170% | 84.3034% | 83.2174% | 81.1142% |
| 2015-10-25 | Worlds | Fnatic | KOO Tigers | 50.9878% | 50.9081% | 50.3576% | 49.5873% |
| 2015-10-31 | Worlds | SKTelecom T1 | KOO Tigers | 72.4820% | 72.1694% | 71.1469% | 69.4756% |


## S6 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2016-05-04 | MSI | Royal Never Give Up | CLG | 62.1088% | 62.6200% | 63.5748% | 64.6554% |
| 2016-05-04 | MSI | G2 Esports | Flash Wolves | 51.7002% | 51.6567% | 51.6388% | 51.6674% |
| 2016-05-04 | MSI | SK Telecom T1 | SuperMassive | 81.9191% | 82.0087% | 82.8985% | 84.2733% |
| 2016-05-04 | MSI | CLG | Flash Wolves | 24.7389% | 25.4883% | 25.7789% | 26.2270% |
| 2016-05-04 | MSI | G2 Esports | SK Telecom T1 | 25.1025% | 29.8854% | 31.4541% | 32.7299% |
| 2016-05-04 | MSI | SuperMassive | Royal Never Give Up | 56.6780% | 48.9727% | 44.1921% | 38.6681% |
| 2016-05-05 | MSI | CLG | G2 Esports | 36.5747% | 33.7564% | 32.9345% | 32.2551% |
| 2016-05-05 | MSI | SK Telecom T1 | Royal Never Give Up | 83.2575% | 80.1429% | 78.4923% | 76.7264% |
| 2016-05-05 | MSI | Flash Wolves | SuperMassive | 66.7317% | 71.3822% | 73.4501% | 75.6893% |
| 2016-05-05 | MSI | Royal Never Give Up | G2 Esports | 52.1627% | 48.3893% | 47.9398% | 47.8325% |
| 2016-05-05 | MSI | SuperMassive | CLG | 47.8387% | 43.4841% | 41.1970% | 38.4594% |
| 2016-05-05 | MSI | SK Telecom T1 | Flash Wolves | 83.6374% | 79.4632% | 77.9290% | 76.5418% |
| 2016-05-06 | MSI | Flash Wolves | Royal Never Give Up | 58.9018% | 61.4165% | 61.6001% | 61.5354% |
| 2016-05-06 | MSI | CLG | SK Telecom T1 | 17.4687% | 18.2817% | 18.6029% | 18.8848% |
| 2016-05-06 | MSI | SuperMassive | G2 Esports | 51.0836% | 43.0063% | 39.7049% | 36.2483% |
| 2016-05-06 | MSI | Flash Wolves | SK Telecom T1 | 43.9520% | 45.9321% | 46.5715% | 47.0344% |
| 2016-05-06 | MSI | CLG | SuperMassive | 47.6107% | 50.0391% | 51.4586% | 53.2336% |
| 2016-05-06 | MSI | G2 Esports | Royal Never Give Up | 28.9574% | 35.6768% | 37.5981% | 39.3219% |
| 2016-05-07 | MSI | G2 Esports | SuperMassive | 63.0085% | 68.3848% | 70.6859% | 73.1261% |
| 2016-05-07 | MSI | Royal Never Give Up | Flash Wolves | 49.8394% | 46.8408% | 46.2949% | 45.9050% |
| 2016-05-07 | MSI | SK Telecom T1 | CLG | 68.0458% | 70.3663% | 71.1172% | 71.8947% |
| 2016-05-07 | MSI | Flash Wolves | G2 Esports | 74.2743% | 71.0308% | 69.7458% | 68.4038% |
| 2016-05-07 | MSI | CLG | Royal Never Give Up | 30.5876% | 31.0310% | 30.7546% | 30.3923% |
| 2016-05-07 | MSI | SuperMassive | SK Telecom T1 | 17.9043% | 16.6868% | 16.0248% | 15.1895% |
| 2016-05-08 | MSI | Royal Never Give Up | SuperMassive | 85.4768% | 84.8916% | 85.1492% | 85.5979% |
| 2016-05-08 | MSI | Flash Wolves | CLG | 65.1356% | 67.6334% | 68.5465% | 69.4341% |
| 2016-05-08 | MSI | SK Telecom T1 | G2 Esports | 75.3520% | 72.1537% | 70.8264% | 69.5041% |
| 2016-05-08 | MSI | SuperMassive | Flash Wolves | 15.0011% | 14.3247% | 13.8383% | 13.2401% |
| 2016-05-08 | MSI | G2 Esports | CLG | 41.8971% | 48.2421% | 50.6366% | 53.0472% |
| 2016-05-08 | MSI | Royal Never Give Up | SK Telecom T1 | 46.8171% | 44.8376% | 44.6243% | 44.4493% |
| 2016-05-13 | MSI | Royal Never Give Up | SK Telecom T1 | 39.4815% | 39.1143% | 39.3835% | 39.6621% |
| 2016-05-14 | MSI | CLG | Flash Wolves | 45.1516% | 42.1557% | 40.9994% | 39.8099% |
| 2016-05-15 | MSI | CLG | SK Telecom T1 | 34.0245% | 32.4703% | 31.7730% | 30.9242% |
| 2016-09-29 | Worlds | G2 Esports | CLG | 84.7336% | 74.1125% | 69.0489% | 64.5319% |
| 2016-09-29 | Worlds | ROX Tigers | Albus NoX Luna | 88.6632% | 88.5830% | 89.1681% | 90.6445% |
| 2016-09-29 | Worlds | H2k-Gaming | ahq eSports | 43.8122% | 42.9075% | 44.2762% | 47.5422% |
| 2016-09-29 | Worlds | INTZ eSports | Edward Gaming | 33.7202% | 21.6124% | 16.5733% | 12.0116% |
| 2016-09-29 | Worlds | Samsung Galaxy | Splyce | 76.5764% | 76.0008% | 75.9411% | 76.6238% |
| 2016-09-29 | Worlds | Team SoloMid | Royal Never Give Up | 64.9132% | 58.0363% | 54.1167% | 49.6230% |
| 2016-09-30 | Worlds | SK Telecom T1 | Cloud 9 | 85.2815% | 82.6958% | 81.2404% | 80.3457% |
| 2016-09-30 | Worlds | Flash Wolves | I MAY | 72.9012% | 65.9216% | 62.3510% | 59.1765% |
| 2016-09-30 | Worlds | Team SoloMid | Samsung Galaxy | 18.3724% | 30.0027% | 34.9478% | 38.6316% |
| 2016-09-30 | Worlds | Royal Never Give Up | Splyce | 52.0691% | 62.9067% | 67.9815% | 72.8056% |
| 2016-09-30 | Worlds | H2k-Gaming | INTZ eSports | 33.8091% | 38.5924% | 44.1321% | 53.3838% |
| 2016-09-30 | Worlds | Edward Gaming | ahq eSports | 39.3253% | 53.7302% | 59.6926% | 65.3120% |
| 2016-10-01 | Worlds | CLG | Albus NoX Luna | 34.8580% | 42.7688% | 48.4040% | 55.3889% |
| 2016-10-01 | Worlds | ROX Tigers | G2 Esports | 88.7284% | 85.8356% | 84.5216% | 83.3531% |
| 2016-10-01 | Worlds | Flash Wolves | Cloud 9 | 49.2741% | 52.8011% | 54.0444% | 55.6390% |
| 2016-10-01 | Worlds | I MAY | SK Telecom T1 | 19.8659% | 21.9348% | 23.4921% | 24.7681% |
| 2016-10-01 | Worlds | Splyce | Team SoloMid | 30.5462% | 28.2448% | 27.1568% | 26.2413% |
| 2016-10-01 | Worlds | Royal Never Give Up | Samsung Galaxy | 28.9891% | 35.3455% | 39.9251% | 44.4825% |
| 2016-10-02 | Worlds | ahq eSports | INTZ eSports | 49.6395% | 53.0837% | 56.2561% | 60.5530% |
| 2016-10-02 | Worlds | Edward Gaming | H2k-Gaming | 69.8554% | 76.3334% | 77.5985% | 77.5886% |
| 2016-10-02 | Worlds | Albus NoX Luna | G2 Esports | 58.4595% | 53.5549% | 50.7389% | 46.4158% |
| 2016-10-02 | Worlds | CLG | ROX Tigers | 4.8486% | 7.3320% | 8.9818% | 10.7900% |
| 2016-10-02 | Worlds | SK Telecom T1 | Flash Wolves | 89.9873% | 85.5290% | 83.1544% | 80.5844% |
| 2016-10-02 | Worlds | Cloud 9 | I MAY | 54.2274% | 51.7459% | 50.0070% | 47.8004% |
| 2016-10-06 | Worlds | G2 Esports | ROX Tigers | 13.7335% | 14.9889% | 15.7763% | 16.5823% |
| 2016-10-06 | Worlds | Albus NoX Luna | CLG | 66.7176% | 62.9188% | 59.8680% | 55.9719% |
| 2016-10-06 | Worlds | CLG | G2 Esports | 50.0547% | 48.3350% | 48.6155% | 48.4828% |
| 2016-10-06 | Worlds | Albus NoX Luna | ROX Tigers | 24.2324% | 21.8682% | 20.9094% | 19.2133% |
| 2016-10-06 | Worlds | G2 Esports | Albus NoX Luna | 33.2339% | 38.6485% | 41.4699% | 45.5291% |
| 2016-10-06 | Worlds | ROX Tigers | CLG | 86.2406% | 85.8404% | 84.9459% | 84.2405% |
| 2016-10-06 | Worlds | ROX Tigers | Albus NoX Luna | 75.7676% | 78.1318% | 79.0906% | 80.7867% |
| 2016-10-07 | Worlds | Edward Gaming | INTZ eSports | 71.1798% | 76.1087% | 78.9463% | 82.1698% |
| 2016-10-07 | Worlds | ahq eSports | H2k-Gaming | 69.4618% | 68.8148% | 66.8757% | 62.9046% |
| 2016-10-07 | Worlds | H2k-Gaming | Edward Gaming | 25.6003% | 21.5877% | 20.9504% | 21.4395% |
| 2016-10-07 | Worlds | INTZ eSports | ahq eSports | 34.0945% | 34.0679% | 33.2625% | 31.9214% |
| 2016-10-07 | Worlds | INTZ eSports | H2k-Gaming | 54.0589% | 53.2754% | 50.1557% | 44.2935% |
| 2016-10-07 | Worlds | ahq eSports | Edward Gaming | 43.9043% | 37.7921% | 34.8565% | 31.6369% |
| 2016-10-07 | Worlds | H2k-Gaming | Edward Gaming | 25.6003% | 21.5877% | 20.9504% | 21.4395% |
| 2016-10-08 | Worlds | Samsung Galaxy | Team SoloMid | 57.7195% | 52.4727% | 51.3058% | 51.3750% |
| 2016-10-08 | Worlds | Splyce | Royal Never Give Up | 42.0399% | 38.8219% | 35.0785% | 30.2159% |
| 2016-10-08 | Worlds | Team SoloMid | Splyce | 74.7288% | 75.1468% | 75.4542% | 75.8349% |
| 2016-10-08 | Worlds | Samsung Galaxy | Royal Never Give Up | 74.5420% | 67.9318% | 63.6369% | 58.9435% |
| 2016-10-08 | Worlds | Splyce | Samsung Galaxy | 19.8536% | 23.0508% | 23.5911% | 23.1713% |
| 2016-10-08 | Worlds | Royal Never Give Up | Team SoloMid | 31.7982% | 34.2617% | 37.5804% | 42.3941% |
| 2016-10-09 | Worlds | I MAY | Flash Wolves | 42.0911% | 41.7604% | 42.2347% | 42.9283% |
| 2016-10-09 | Worlds | Cloud 9 | SK Telecom T1 | 28.4012% | 25.8606% | 25.1704% | 24.2158% |
| 2016-10-09 | Worlds | Cloud 9 | Flash Wolves | 55.8304% | 52.2822% | 50.6662% | 48.5011% |
| 2016-10-09 | Worlds | SK Telecom T1 | I MAY | 81.4265% | 81.4149% | 80.6798% | 79.6683% |
| 2016-10-09 | Worlds | I MAY | Cloud 9 | 36.5095% | 39.5567% | 41.5859% | 44.4035% |
| 2016-10-09 | Worlds | Flash Wolves | SK Telecom T1 | 23.8862% | 24.1480% | 24.6718% | 25.3334% |
| 2016-10-14 | Worlds | Samsung Galaxy | Cloud 9 | 80.7719% | 75.8258% | 73.2007% | 70.5537% |
| 2016-10-15 | Worlds | SK Telecom T1 | Royal Never Give Up | 80.7754% | 78.6985% | 76.9596% | 74.7103% |
| 2016-10-16 | Worlds | ROX Tigers | Edward Gaming | 77.4681% | 78.0251% | 77.4014% | 76.7745% |
| 2016-10-17 | Worlds | H2k-Gaming | Albus NoX Luna | 47.6558% | 40.5055% | 38.8805% | 38.2582% |
| 2016-10-22 | Worlds | ROX Tigers | SK Telecom T1 | 55.6514% | 57.9348% | 58.1027% | 58.2544% |
| 2016-10-23 | Worlds | Samsung Galaxy | H2k-Gaming | 71.0128% | 73.6750% | 74.0773% | 74.0418% |
| 2016-10-30 | Worlds | Samsung Galaxy | SK Telecom T1 | 59.4056% | 49.0380% | 45.3272% | 41.6665% |


## S7 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-04-28 | MSI | Red Canids | Dire Wolves | 57.2462% | 60.1657% | 61.4243% | 62.7460% |
| 2017-04-28 | MSI | SuperMassive | Rampage | 46.8815% | 36.1261% | 30.8493% | 25.9155% |
| 2017-04-28 | MSI | Red Canids | Rampage | 57.2462% | 60.1657% | 61.4243% | 62.7460% |
| 2017-04-28 | MSI | SuperMassive | Dire Wolves | 46.8815% | 36.1261% | 30.8493% | 25.9155% |
| 2017-04-28 | MSI | Dire Wolves | Rampage | 50.0000% | 50.0000% | 50.0000% | 50.0000% |
| 2017-04-28 | MSI | SuperMassive | Red Canids | 39.7282% | 27.2442% | 21.8854% | 17.1975% |
| 2017-04-29 | MSI | Virtus.pro | Lyon Gaming | 57.0562% | 55.1185% | 53.2318% | 50.3232% |
| 2017-04-29 | MSI | GIGABYTE Marines | Isurus Gaming | 50.0000% | 50.0000% | 50.0000% | 50.0000% |
| 2017-04-29 | MSI | Virtus.pro | Isurus Gaming | 57.0562% | 55.1185% | 53.2318% | 50.3232% |
| 2017-04-29 | MSI | GIGABYTE Marines | Lyon Gaming | 50.0000% | 50.0000% | 50.0000% | 50.0000% |
| 2017-04-29 | MSI | Lyon Gaming | Isurus Gaming | 50.0000% | 50.0000% | 50.0000% | 50.0000% |
| 2017-04-29 | MSI | GIGABYTE Marines | Virtus.pro | 42.9438% | 44.8815% | 46.7682% | 49.6768% |
| 2017-04-30 | MSI | Rampage | Red Canids | 11.6968% | 10.9554% | 10.6130% | 10.2422% |
| 2017-04-30 | MSI | Dire Wolves | SuperMassive | 11.7986% | 13.3212% | 14.1791% | 15.0589% |
| 2017-04-30 | MSI | Rampage | SuperMassive | 4.4112% | 5.0104% | 5.3632% | 5.7277% |
| 2017-04-30 | MSI | Dire Wolves | Red Canids | 27.7439% | 26.3880% | 25.7136% | 24.9793% |
| 2017-04-30 | MSI | Red Canids | SuperMassive | 25.8373% | 30.0072% | 32.3094% | 34.7450% |
| 2017-04-30 | MSI | Rampage | Dire Wolves | 25.6496% | 25.5516% | 25.5406% | 25.5236% |
| 2017-05-01 | MSI | Isurus Gaming | Virtus.pro | 19.9117% | 19.9170% | 20.3516% | 21.1619% |
| 2017-05-01 | MSI | Lyon Gaming | GIGABYTE Marines | 26.2139% | 25.9943% | 25.8652% | 25.6855% |
| 2017-05-01 | MSI | Isurus Gaming | GIGABYTE Marines | 4.2982% | 4.1723% | 4.1260% | 4.0729% |
| 2017-05-01 | MSI | Lyon Gaming | Virtus.pro | 66.2923% | 66.7372% | 67.4427% | 68.6036% |
| 2017-05-01 | MSI | Virtus.pro | GIGABYTE Marines | 15.3004% | 14.8984% | 14.4147% | 13.6576% |
| 2017-05-01 | MSI | Isurus Gaming | Lyon Gaming | 11.2229% | 11.0287% | 10.9805% | 10.9404% |
| 2017-05-03 | MSI | Team SoloMid | GIGABYTE Marines | 47.8756% | 49.6630% | 51.3424% | 53.6044% |
| 2017-05-04 | MSI | Flash Wolves | SuperMassive | 81.6751% | 88.1629% | 90.0079% | 91.4569% |
| 2017-05-06 | MSI | SuperMassive | GIGABYTE Marines | 37.0319% | 36.7283% | 36.3714% | 36.1973% |
| 2017-05-10 | MSI | G2 Esports | SK Telecom T1 | 19.6675% | 19.9749% | 19.6621% | 19.0317% |
| 2017-05-10 | MSI | Team WE | Flash Wolves | 18.9574% | 14.0059% | 12.8523% | 12.1016% |
| 2017-05-10 | MSI | GIGABYTE Marines | Team SoloMid | 45.5579% | 45.3316% | 44.8418% | 44.1494% |
| 2017-05-10 | MSI | Flash Wolves | G2 Esports | 80.1600% | 84.2590% | 85.4254% | 86.3628% |
| 2017-05-10 | MSI | SK Telecom T1 | GIGABYTE Marines | 80.5986% | 81.1442% | 81.9916% | 83.2500% |
| 2017-05-10 | MSI | Team SoloMid | Team WE | 55.4204% | 56.2893% | 56.0835% | 55.3963% |
| 2017-05-11 | MSI | SK Telecom T1 | Team SoloMid | 81.6957% | 81.0087% | 81.1487% | 81.6217% |
| 2017-05-11 | MSI | GIGABYTE Marines | Flash Wolves | 39.6228% | 29.8582% | 26.3039% | 22.9019% |
| 2017-05-11 | MSI | G2 Esports | Team WE | 53.0312% | 52.7950% | 52.4471% | 51.8126% |
| 2017-05-11 | MSI | Flash Wolves | Team SoloMid | 58.3371% | 68.2326% | 71.6400% | 74.8429% |
| 2017-05-11 | MSI | GIGABYTE Marines | G2 Esports | 48.5019% | 48.5673% | 48.1729% | 47.5229% |
| 2017-05-11 | MSI | Team WE | SK Telecom T1 | 16.2207% | 16.8718% | 16.9650% | 16.9678% |
| 2017-05-12 | MSI | G2 Esports | Team SoloMid | 56.7452% | 54.7804% | 54.0979% | 53.4601% |
| 2017-05-12 | MSI | SK Telecom T1 | Flash Wolves | 73.8257% | 65.0533% | 61.8828% | 59.0306% |
| 2017-05-12 | MSI | GIGABYTE Marines | Team WE | 38.7110% | 40.5691% | 40.5581% | 40.0268% |
| 2017-05-12 | MSI | G2 Esports | Flash Wolves | 34.9453% | 27.6447% | 25.1009% | 22.7191% |
| 2017-05-12 | MSI | GIGABYTE Marines | SK Telecom T1 | 10.8760% | 12.2338% | 12.3749% | 12.2363% |
| 2017-05-12 | MSI | Team WE | Team SoloMid | 57.0978% | 54.6533% | 54.1645% | 54.0464% |
| 2017-05-13 | MSI | Team WE | G2 Esports | 49.3154% | 48.8505% | 49.0188% | 49.4775% |
| 2017-05-13 | MSI | Team SoloMid | GIGABYTE Marines | 52.2128% | 52.7391% | 53.1729% | 53.7268% |
| 2017-05-13 | MSI | Flash Wolves | SK Telecom T1 | 17.8788% | 24.9757% | 27.8919% | 30.8364% |
| 2017-05-13 | MSI | G2 Esports | GIGABYTE Marines | 56.9454% | 56.3942% | 56.3710% | 56.4674% |
| 2017-05-13 | MSI | Team SoloMid | SK Telecom T1 | 11.5105% | 13.1163% | 13.5411% | 13.7982% |
| 2017-05-13 | MSI | Flash Wolves | Team WE | 58.6950% | 66.5809% | 69.3007% | 71.7982% |
| 2017-05-14 | MSI | SK Telecom T1 | G2 Esports | 85.9290% | 85.1898% | 85.0798% | 85.1163% |
| 2017-05-14 | MSI | Team SoloMid | Flash Wolves | 38.7789% | 33.2231% | 30.9293% | 28.4847% |
| 2017-05-14 | MSI | Team WE | GIGABYTE Marines | 62.5882% | 61.4916% | 61.5792% | 62.0465% |
| 2017-05-14 | MSI | Team SoloMid | G2 Esports | 54.4096% | 53.9313% | 53.7701% | 53.5274% |
| 2017-05-14 | MSI | Flash Wolves | GIGABYTE Marines | 64.8413% | 70.2099% | 72.5389% | 75.0242% |
| 2017-05-14 | MSI | SK Telecom T1 | Team WE | 78.1330% | 78.2989% | 78.3466% | 78.4191% |
| 2017-05-14 | MSI | Flash Wolves | Team SoloMid | 61.2211% | 66.7769% | 69.0707% | 71.5153% |
| 2017-05-19 | MSI | SK Telecom T1 | Flash Wolves | 72.2461% | 67.8375% | 66.0269% | 64.2431% |
| 2017-05-20 | MSI | Team WE | G2 Esports | 67.2459% | 65.7673% | 65.6066% | 65.7083% |
| 2017-05-21 | MSI | SK Telecom T1 | G2 Esports | 81.0775% | 82.0348% | 82.4964% | 83.0680% |
| 2017-09-23 | Worlds | Team WE | Lyon Gaming | 68.8698% | 69.9038% | 70.9917% | 73.0654% |
| 2017-09-23 | Worlds | Cloud 9 | Team oNe eSports | 70.0405% | 69.1559% | 69.0588% | 69.6674% |
| 2017-09-23 | Worlds | Gambit Esports | Lyon Gaming | 66.8560% | 60.8929% | 55.1921% | 46.8271% |
| 2017-09-23 | Worlds | Dire Wolves | Cloud 9 | 26.5962% | 20.3376% | 18.1592% | 16.0680% |
| 2017-09-23 | Worlds | Gambit Esports | Team WE | 47.6927% | 40.1335% | 33.4802% | 24.5080% |
| 2017-09-23 | Worlds | Dire Wolves | Team oNe eSports | 45.8600% | 36.4031% | 33.1207% | 30.5410% |
| 2017-09-24 | Worlds | Team oNe eSports | Cloud 9 | 17.1905% | 20.5245% | 21.6254% | 22.2914% |
| 2017-09-24 | Worlds | Lyon Gaming | Team WE | 30.4356% | 28.6492% | 27.2823% | 25.1579% |
| 2017-09-24 | Worlds | Cloud 9 | Dire Wolves | 73.3307% | 77.0346% | 79.1824% | 81.6255% |
| 2017-09-24 | Worlds | Lyon Gaming | Gambit Esports | 54.6314% | 52.9922% | 54.9558% | 59.2833% |
| 2017-09-24 | Worlds | Team oNe eSports | Dire Wolves | 36.3380% | 46.4171% | 51.2079% | 56.0309% |
| 2017-09-24 | Worlds | Team WE | Gambit Esports | 73.3495% | 73.7364% | 76.4809% | 81.2433% |
| 2017-09-24 | Worlds | Dire Wolves | Team oNe eSports | 63.6620% | 53.5829% | 48.7921% | 43.9691% |
| 2017-09-25 | Worlds | Young Generation | Kaos Latin Gamers | 50.0000% | 50.0000% | 50.0000% | 50.0000% |
| 2017-09-25 | Worlds | Rampage | Hong Kong Attitude | 33.2978% | 29.1296% | 28.2322% | 27.8666% |
| 2017-09-25 | Worlds | Fnatic | Kaos Latin Gamers | 66.5360% | 69.4568% | 69.8473% | 69.5456% |
| 2017-09-25 | Worlds | Hong Kong Attitude | 1907 Fenerbahce | 46.7867% | 39.9110% | 36.1392% | 31.2210% |
| 2017-09-25 | Worlds | Young Generation | Fnatic | 33.4640% | 30.5432% | 30.1527% | 30.4544% |
| 2017-09-25 | Worlds | Rampage | 1907 Fenerbahce | 30.5031% | 21.4456% | 18.2083% | 14.9199% |
| 2017-09-26 | Worlds | Hong Kong Attitude | Rampage | 79.4218% | 78.3118% | 77.6953% | 76.8352% |
| 2017-09-26 | Worlds | Kaos Latin Gamers | Young Generation | 76.5454% | 76.7177% | 76.7402% | 76.7173% |
| 2017-09-26 | Worlds | 1907 Fenerbahce | Rampage | 91.8167% | 91.5098% | 91.6223% | 92.0322% |
| 2017-09-26 | Worlds | Kaos Latin Gamers | Fnatic | 26.6782% | 26.0775% | 26.1292% | 26.5053% |
| 2017-09-26 | Worlds | 1907 Fenerbahce | Hong Kong Attitude | 74.4055% | 74.9061% | 75.8433% | 77.6902% |
| 2017-09-26 | Worlds | Fnatic | Young Generation | 89.9694% | 90.3295% | 90.3171% | 90.1347% |
| 2017-09-26 | Worlds | Hong Kong Attitude | 1907 Fenerbahce | 25.5945% | 25.0939% | 24.1567% | 22.3098% |
| 2017-09-28 | Worlds | Cloud 9 | Lyon Gaming | 69.8516% | 70.9281% | 71.6318% | 72.7574% |
| 2017-09-28 | Worlds | Fnatic | Hong Kong Attitude | 51.6776% | 54.6176% | 56.1491% | 57.8493% |
| 2017-09-29 | Worlds | 1907 Fenerbahce | Team oNe eSports | 77.9536% | 77.4234% | 76.8827% | 76.5900% |
| 2017-09-29 | Worlds | Team WE | Young Generation | 68.2824% | 72.1111% | 74.7376% | 78.0606% |
| 2017-10-05 | Worlds | Royal Never Give Up | 1907 Fenerbahce | 59.0754% | 57.0594% | 56.9062% | 57.4174% |
| 2017-10-05 | Worlds | G2 Esports | Samsung Galaxy | 24.9585% | 24.6270% | 24.4904% | 24.1302% |
| 2017-10-05 | Worlds | Longzhu Gaming | Immortals | 74.0263% | 70.0083% | 69.2979% | 69.6387% |
| 2017-10-05 | Worlds | Fnatic | GIGABYTE Marines | 68.2763% | 61.5928% | 58.2451% | 54.1295% |
| 2017-10-05 | Worlds | SK Telecom T1 | Cloud 9 | 66.8575% | 69.7575% | 71.3719% | 73.6869% |
| 2017-10-05 | Worlds | Edward Gaming | ahq e-Sports Club | 71.1532% | 63.3789% | 60.3779% | 57.7805% |
| 2017-10-06 | Worlds | Flash Wolves | Team SoloMid | 35.6627% | 41.2378% | 45.1972% | 50.1668% |
| 2017-10-06 | Worlds | Team WE | Misfits | 77.6721% | 77.8619% | 78.1915% | 78.7235% |
| 2017-10-06 | Worlds | Immortals | Fnatic | 57.1699% | 58.5622% | 58.1478% | 57.6027% |
| 2017-10-06 | Worlds | Longzhu Gaming | GIGABYTE Marines | 82.2769% | 81.7902% | 80.1247% | 77.9448% |
| 2017-10-06 | Worlds | ahq e-Sports Club | Cloud 9 | 34.8283% | 40.0038% | 42.6993% | 45.5768% |
| 2017-10-06 | Worlds | Edward Gaming | SK Telecom T1 | 19.3706% | 22.3787% | 23.1877% | 23.5950% |
| 2017-10-07 | Worlds | Team SoloMid | Team WE | 62.6001% | 61.5000% | 59.1871% | 55.6689% |
| 2017-10-07 | Worlds | Flash Wolves | Misfits | 70.0346% | 75.7828% | 77.8263% | 79.8782% |
| 2017-10-07 | Worlds | G2 Esports | 1907 Fenerbahce | 49.6988% | 49.4042% | 50.0454% | 51.0851% |
| 2017-10-07 | Worlds | Samsung Galaxy | Royal Never Give Up | 72.3889% | 71.6591% | 71.2552% | 70.8642% |
| 2017-10-07 | Worlds | SK Telecom T1 | ahq e-Sports Club | 89.5021% | 85.6763% | 83.8340% | 82.1686% |
| 2017-10-07 | Worlds | Cloud 9 | Edward Gaming | 63.9214% | 58.1592% | 55.9679% | 53.3886% |
| 2017-10-08 | Worlds | Team WE | Flash Wolves | 70.6850% | 59.1603% | 54.9347% | 50.9860% |
| 2017-10-08 | Worlds | Misfits | Team SoloMid | 14.4007% | 15.4225% | 16.4601% | 17.9850% |
| 2017-10-08 | Worlds | GIGABYTE Marines | Immortals | 34.8718% | 33.0403% | 34.6709% | 37.9155% |
| 2017-10-08 | Worlds | Fnatic | Longzhu Gaming | 12.5549% | 17.9785% | 20.1738% | 21.6760% |
| 2017-10-08 | Worlds | 1907 Fenerbahce | Samsung Galaxy | 17.3944% | 18.2426% | 18.4720% | 18.3882% |
| 2017-10-08 | Worlds | Royal Never Give Up | G2 Esports | 63.8764% | 60.8639% | 59.8826% | 59.2160% |
| 2017-10-12 | Worlds | Immortals | GIGABYTE Marines | 72.4462% | 70.6669% | 68.2768% | 64.4686% |
| 2017-10-12 | Worlds | Longzhu Gaming | Fnatic | 88.3713% | 83.3240% | 81.0884% | 79.3594% |
| 2017-10-12 | Worlds | Fnatic | Immortals | 32.1249% | 35.1923% | 36.8141% | 38.5885% |
| 2017-10-12 | Worlds | GIGABYTE Marines | Longzhu Gaming | 9.5631% | 13.2684% | 15.6819% | 18.5753% |
| 2017-10-12 | Worlds | GIGABYTE Marines | Fnatic | 44.5550% | 43.3236% | 44.3660% | 46.7267% |
| 2017-10-12 | Worlds | Immortals | Longzhu Gaming | 21.7544% | 26.9301% | 28.5862% | 29.2747% |
| 2017-10-12 | Worlds | Fnatic | Immortals | 32.1249% | 35.1923% | 36.8141% | 38.5885% |
| 2017-10-12 | Worlds | GIGABYTE Marines | Fnatic | 44.5550% | 43.3236% | 44.3660% | 46.7267% |
| 2017-10-13 | Worlds | G2 Esports | Royal Never Give Up | 32.7398% | 37.0910% | 38.4235% | 39.4612% |
| 2017-10-13 | Worlds | Samsung Galaxy | 1907 Fenerbahce | 85.1593% | 84.6395% | 84.3385% | 84.1282% |
| 2017-10-13 | Worlds | Samsung Galaxy | G2 Esports | 76.5647% | 77.3163% | 77.3161% | 77.2500% |
| 2017-10-13 | Worlds | 1907 Fenerbahce | Royal Never Give Up | 21.7000% | 26.7242% | 28.3128% | 29.4572% |
| 2017-10-13 | Worlds | 1907 Fenerbahce | G2 Esports | 36.2794% | 38.2170% | 38.7606% | 39.0476% |
| 2017-10-13 | Worlds | Royal Never Give Up | Samsung Galaxy | 38.6057% | 33.2269% | 31.9813% | 31.1200% |
| 2017-10-14 | Worlds | Misfits | Flash Wolves | 60.2826% | 42.9825% | 36.0776% | 29.4990% |
| 2017-10-14 | Worlds | Team WE | Team SoloMid | 47.1903% | 44.5195% | 45.4832% | 47.7579% |
| 2017-10-14 | Worlds | Flash Wolves | Team WE | 24.8106% | 35.8370% | 40.4823% | 45.1259% |
| 2017-10-14 | Worlds | Team SoloMid | Misfits | 69.0829% | 74.7461% | 75.7418% | 76.0715% |
| 2017-10-14 | Worlds | Team SoloMid | Flash Wolves | 77.2283% | 69.0520% | 63.7973% | 57.0853% |
| 2017-10-14 | Worlds | Misfits | Team WE | 33.3702% | 29.6293% | 27.7397% | 25.6001% |
| 2017-10-14 | Worlds | Misfits | Team SoloMid | 30.9171% | 25.2539% | 24.2582% | 23.9285% |
| 2017-10-15 | Worlds | ahq e-Sports Club | SK Telecom T1 | 8.9776% | 11.8205% | 13.4454% | 15.1857% |
| 2017-10-15 | Worlds | Edward Gaming | Cloud 9 | 39.8157% | 48.1219% | 50.1532% | 51.9834% |
| 2017-10-15 | Worlds | ahq e-Sports Club | Edward Gaming | 32.9631% | 33.4144% | 35.0992% | 37.2763% |
| 2017-10-15 | Worlds | Cloud 9 | SK Telecom T1 | 23.2658% | 22.3587% | 22.2080% | 21.7702% |
| 2017-10-15 | Worlds | Cloud 9 | ahq e-Sports Club | 75.4546% | 68.2364% | 64.7611% | 60.8498% |
| 2017-10-15 | Worlds | SK Telecom T1 | Edward Gaming | 83.2927% | 78.9189% | 77.6859% | 76.8477% |
| 2017-10-19 | Worlds | Longzhu Gaming | Samsung Galaxy | 70.2576% | 60.2958% | 54.9960% | 49.1989% |
| 2017-10-20 | Worlds | SK Telecom T1 | Misfits | 82.1951% | 85.2479% | 86.5734% | 88.0413% |
| 2017-10-21 | Worlds | Fnatic | Royal Never Give Up | 32.3931% | 37.7010% | 37.6785% | 35.8984% |
| 2017-10-22 | Worlds | Team WE | Cloud 9 | 64.3194% | 61.5116% | 60.5680% | 60.0027% |
| 2017-10-28 | Worlds | Royal Never Give Up | SK Telecom T1 | 48.1169% | 40.1509% | 36.9633% | 33.6103% |
| 2017-10-29 | Worlds | Team WE | Samsung Galaxy | 31.5920% | 34.4358% | 35.5256% | 36.3196% |
| 2017-11-04 | Worlds | Samsung Galaxy | SK Telecom T1 | 60.1991% | 53.5588% | 50.8443% | 48.0761% |


## S8 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2018-05-03 | MSI | Gambit Esports | Kaos Latin Gamers | 39.1725% | 42.3210% | 46.1063% | 51.8221% |
| 2018-05-03 | MSI | Rainbow7 | Ascension Gaming | 75.1850% | 73.9166% | 73.2920% | 72.5496% |
| 2018-05-03 | MSI | Gambit Esports | Ascension Gaming | 68.9556% | 66.2385% | 64.9505% | 63.4913% |
| 2018-05-03 | MSI | Rainbow7 | Kaos Latin Gamers | 46.7643% | 51.4518% | 55.8866% | 62.0449% |
| 2018-05-03 | MSI | Kaos Latin Gamers | Ascension Gaming | 77.5235% | 72.7812% | 68.4154% | 61.7850% |
| 2018-05-03 | MSI | Rainbow7 | Gambit Esports | 57.6997% | 59.0903% | 59.6915% | 60.3134% |
| 2018-05-04 | MSI | BAUSuperMassive | Dire Wolves | 72.8720% | 75.3168% | 76.4222% | 77.8870% |
| 2018-05-04 | MSI | KaBuM! e-Sports | Pentagram | 48.0389% | 57.9745% | 62.5527% | 67.8423% |
| 2018-05-04 | MSI | BAUSuperMassive | Pentagram | 79.5945% | 87.2063% | 89.5017% | 91.6715% |
| 2018-05-04 | MSI | KaBuM! e-Sports | Dire Wolves | 38.9008% | 38.1777% | 38.8411% | 40.3021% |
| 2018-05-04 | MSI | Dire Wolves | Pentagram | 59.2184% | 69.0774% | 72.4536% | 75.7574% |
| 2018-05-04 | MSI | KaBuM! e-Sports | BAUSuperMassive | 19.1604% | 16.8318% | 16.3835% | 16.0840% |
| 2018-05-05 | MSI | Ascension Gaming | Gambit Esports | 5.6647% | 6.5998% | 6.9388% | 7.2422% |
| 2018-05-05 | MSI | Kaos Latin Gamers | Rainbow7 | 65.7981% | 62.2472% | 59.2765% | 54.9990% |
| 2018-05-05 | MSI | Ascension Gaming | Rainbow7 | 15.1720% | 14.8339% | 14.6843% | 14.4717% |
| 2018-05-05 | MSI | Kaos Latin Gamers | Gambit Esports | 39.2429% | 40.0806% | 38.6714% | 36.0594% |
| 2018-05-05 | MSI | Gambit Esports | Rainbow7 | 74.8650% | 71.1394% | 69.7739% | 68.4260% |
| 2018-05-05 | MSI | Ascension Gaming | Kaos Latin Gamers | 8.5061% | 9.5545% | 10.5742% | 12.1609% |
| 2018-05-06 | MSI | Pentagram | BAUSuperMassive | 7.7797% | 5.9396% | 5.2261% | 4.4590% |
| 2018-05-06 | MSI | Dire Wolves | KaBuM! e-Sports | 69.1514% | 68.8565% | 68.3074% | 67.2980% |
| 2018-05-06 | MSI | Pentagram | KaBuM! e-Sports | 37.0405% | 32.2883% | 29.7854% | 26.7049% |
| 2018-05-06 | MSI | Dire Wolves | BAUSuperMassive | 24.3246% | 22.6477% | 21.8855% | 20.8615% |
| 2018-05-06 | MSI | BAUSuperMassive | KaBuM! e-Sports | 87.4591% | 88.3060% | 88.4962% | 88.6451% |
| 2018-05-06 | MSI | Pentagram | Dire Wolves | 20.7890% | 17.7413% | 16.4452% | 15.0416% |
| 2018-05-08 | MSI | EVOS Esports | BAUSuperMassive | 29.8649% | 34.0013% | 36.5138% | 39.8771% |
| 2018-05-09 | MSI | Flash Wolves | Gambit Esports | 51.9775% | 55.0175% | 57.2190% | 60.4241% |
| 2018-05-11 | MSI | Fnatic | Royal Never Give Up | 49.9547% | 52.7741% | 53.4881% | 54.2004% |
| 2018-05-11 | MSI | EVOS Esports | Flash Wolves | 31.6354% | 35.7001% | 36.9071% | 37.5965% |
| 2018-05-11 | MSI | Kingzone DragonX | Team Liquid | 81.9026% | 84.4746% | 85.4209% | 86.4721% |
| 2018-05-11 | MSI | Flash Wolves | Fnatic | 51.6948% | 46.7001% | 46.2655% | 46.6986% |
| 2018-05-11 | MSI | Team Liquid | EVOS Esports | 53.5561% | 52.4041% | 51.1551% | 49.5459% |
| 2018-05-11 | MSI | Royal Never Give Up | Kingzone DragonX | 27.9352% | 23.4927% | 21.9582% | 20.3209% |
| 2018-05-12 | MSI | Kingzone DragonX | Fnatic | 86.4867% | 85.8374% | 85.8529% | 86.0224% |
| 2018-05-12 | MSI | Royal Never Give Up | EVOS Esports | 66.0130% | 64.8137% | 63.7017% | 62.2689% |
| 2018-05-12 | MSI | Team Liquid | Flash Wolves | 18.0168% | 22.3142% | 23.1785% | 23.4037% |
| 2018-05-12 | MSI | EVOS Esports | Kingzone DragonX | 13.6766% | 12.8326% | 12.7239% | 12.6178% |
| 2018-05-12 | MSI | Flash Wolves | Royal Never Give Up | 61.1707% | 57.8621% | 57.6137% | 58.1499% |
| 2018-05-12 | MSI | Fnatic | Team Liquid | 59.4583% | 60.6700% | 61.0961% | 61.6280% |
| 2018-05-13 | MSI | Royal Never Give Up | Team Liquid | 79.5119% | 76.5259% | 75.6487% | 74.8751% |
| 2018-05-13 | MSI | EVOS Esports | Fnatic | 28.1260% | 29.0539% | 29.8444% | 30.7821% |
| 2018-05-13 | MSI | Kingzone DragonX | Flash Wolves | 48.8922% | 58.3596% | 60.9717% | 63.0271% |
| 2018-05-13 | MSI | Royal Never Give Up | Fnatic | 49.7406% | 48.1515% | 47.6975% | 47.2179% |
| 2018-05-13 | MSI | Flash Wolves | EVOS Esports | 85.0495% | 81.0770% | 79.6964% | 78.5975% |
| 2018-05-13 | MSI | Team Liquid | Kingzone DragonX | 10.6940% | 10.3817% | 10.1150% | 9.7330% |
| 2018-05-14 | MSI | Kingzone DragonX | Royal Never Give Up | 67.2522% | 70.8041% | 72.1811% | 73.6996% |
| 2018-05-14 | MSI | Fnatic | Flash Wolves | 22.9021% | 27.8693% | 29.1539% | 29.8977% |
| 2018-05-14 | MSI | EVOS Esports | Team Liquid | 49.4987% | 49.5705% | 50.1627% | 51.0254% |
| 2018-05-14 | MSI | Royal Never Give Up | Flash Wolves | 22.9369% | 26.7836% | 27.6622% | 27.9757% |
| 2018-05-14 | MSI | Kingzone DragonX | EVOS Esports | 84.5546% | 85.4793% | 85.6871% | 85.9122% |
| 2018-05-14 | MSI | Team Liquid | Fnatic | 27.7189% | 28.4082% | 28.5785% | 28.6567% |
| 2018-05-15 | MSI | Fnatic | Kingzone DragonX | 36.8572% | 33.9317% | 32.7699% | 31.5148% |
| 2018-05-15 | MSI | EVOS Esports | Royal Never Give Up | 18.1839% | 20.5462% | 21.6178% | 22.7980% |
| 2018-05-15 | MSI | Flash Wolves | Team Liquid | 75.4143% | 73.5716% | 73.2190% | 73.2426% |
| 2018-05-15 | MSI | Fnatic | EVOS Esports | 76.8285% | 75.4522% | 74.6994% | 73.8622% |
| 2018-05-15 | MSI | Flash Wolves | Kingzone DragonX | 50.4002% | 44.5771% | 42.7600% | 41.2331% |
| 2018-05-15 | MSI | Team Liquid | Royal Never Give Up | 29.4888% | 30.8983% | 31.3408% | 31.7328% |
| 2018-05-15 | MSI | Flash Wolves | Royal Never Give Up | 56.1948% | 55.4517% | 55.5156% | 55.9933% |
| 2018-05-15 | MSI | Fnatic | Team Liquid | 63.7950% | 63.9975% | 64.0792% | 64.2250% |
| 2018-05-18 | MSI | Fnatic | Royal Never Give Up | 32.5652% | 35.3872% | 36.2912% | 37.1599% |
| 2018-05-19 | MSI | Flash Wolves | Kingzone DragonX | 45.7911% | 41.6108% | 40.3059% | 39.2096% |
| 2018-05-20 | MSI | Royal Never Give Up | Kingzone DragonX | 50.5198% | 46.2745% | 44.6897% | 42.9899% |
| 2018-10-01 | Worlds | Cloud9 | KaBuM! e-Sports | 66.9060% | 61.1246% | 59.3901% | 58.4904% |
| 2018-10-01 | Worlds | Gambit Esports | G-Rex | 52.0654% | 55.3379% | 55.3155% | 53.4256% |
| 2018-10-01 | Worlds | Detonation FocusMe | KaBuM! e-Sports | 38.9629% | 31.9972% | 29.3086% | 26.2786% |
| 2018-10-01 | Worlds | G-Rex | Kaos Latin Gamers | 28.7792% | 36.6737% | 44.0579% | 54.9919% |
| 2018-10-01 | Worlds | Detonation FocusMe | Cloud9 | 23.9977% | 23.0329% | 22.0878% | 20.1897% |
| 2018-10-01 | Worlds | Gambit Esports | Kaos Latin Gamers | 30.5027% | 41.7777% | 49.3653% | 58.3603% |
| 2018-10-02 | Worlds | Edward Gaming | Infinity eSports | 73.2366% | 82.2571% | 85.9286% | 89.5815% |
| 2018-10-02 | Worlds | G2 Esports | BAUSuperMassive | 58.2613% | 59.4197% | 58.6893% | 57.5917% |
| 2018-10-02 | Worlds | Dire Wolves | Infinity eSports | 49.4951% | 53.5982% | 55.4040% | 57.4203% |
| 2018-10-02 | Worlds | Ascension Gaming | BAUSuperMassive | 20.3718% | 16.0097% | 14.4523% | 12.8020% |
| 2018-10-02 | Worlds | Dire Wolves | Edward Gaming | 26.3694% | 19.9457% | 16.9051% | 13.5574% |
| 2018-10-02 | Worlds | Ascension Gaming | G2 Esports | 15.4893% | 11.5184% | 10.6276% | 9.7562% |
| 2018-10-03 | Worlds | G-Rex | Gambit Esports | 59.6564% | 54.9768% | 53.8365% | 53.9806% |
| 2018-10-03 | Worlds | KaBuM! e-Sports | Detonation FocusMe | 41.2117% | 52.4280% | 57.4254% | 62.9984% |
| 2018-10-03 | Worlds | Kaos Latin Gamers | Gambit Esports | 49.7721% | 45.4975% | 41.0370% | 35.1051% |
| 2018-10-03 | Worlds | KaBuM! e-Sports | Cloud9 | 16.7440% | 24.1302% | 27.3373% | 30.2657% |
| 2018-10-03 | Worlds | Kaos Latin Gamers | G-Rex | 40.1244% | 40.6049% | 37.3741% | 31.5618% |
| 2018-10-03 | Worlds | Cloud9 | Detonation FocusMe | 77.7068% | 77.6042% | 78.1905% | 79.6867% |
| 2018-10-03 | Worlds | Detonation FocusMe | KaBuM! e-Sports | 58.7883% | 47.5720% | 42.5746% | 37.0016% |
| 2018-10-04 | Worlds | BAUSuperMassive | G2 Esports | 55.6839% | 49.9421% | 48.6906% | 47.8439% |
| 2018-10-04 | Worlds | Infinity eSports | Edward Gaming | 16.1667% | 12.3624% | 10.3086% | 8.0181% |
| 2018-10-04 | Worlds | BAUSuperMassive | Ascension Gaming | 90.5178% | 89.9831% | 89.9943% | 90.2718% |
| 2018-10-04 | Worlds | Infinity eSports | Dire Wolves | 37.3168% | 37.1370% | 36.7211% | 36.0631% |
| 2018-10-04 | Worlds | G2 Esports | Ascension Gaming | 88.3683% | 90.0040% | 90.4562% | 91.0038% |
| 2018-10-04 | Worlds | Edward Gaming | Dire Wolves | 75.5327% | 80.7245% | 83.4684% | 86.6141% |
| 2018-10-04 | Worlds | G2 Esports | BAUSuperMassive | 44.3161% | 50.0579% | 51.3094% | 52.1561% |
| 2018-10-06 | Worlds | Cloud9 | Gambit Esports | 82.9636% | 78.4055% | 74.5487% | 69.4635% |
| 2018-10-06 | Worlds | Detonation FocusMe | Edward Gaming | 17.5765% | 12.7937% | 10.3158% | 7.6132% |
| 2018-10-07 | Worlds | G2 Esports | Infinity eSports | 60.3203% | 66.3357% | 69.8481% | 74.2302% |
| 2018-10-07 | Worlds | G-Rex | BAUSuperMassive | 53.5547% | 48.0498% | 47.3694% | 47.9556% |
| 2018-10-10 | Worlds | KT Rolster | Team Liquid | 66.4431% | 72.0769% | 73.1230% | 73.4803% |
| 2018-10-10 | Worlds | Edward Gaming | MAD Team | 75.2447% | 76.8127% | 78.6513% | 81.1293% |
| 2018-10-10 | Worlds | Phong Vu Buffalo | Flash Wolves | 26.3341% | 24.6316% | 24.5995% | 24.5804% |
| 2018-10-10 | Worlds | Afreeca Freecs | G2 Esports | 64.6037% | 71.0948% | 73.2628% | 75.1412% |
| 2018-10-10 | Worlds | Royal Never Give Up | Cloud9 | 68.3450% | 76.3273% | 79.5567% | 82.7193% |
| 2018-10-10 | Worlds | Gen.G eSports | Team Vitality | 68.7252% | 73.4004% | 76.2086% | 79.0829% |
| 2018-10-11 | Worlds | Flash Wolves | Afreeca Freecs | 63.0676% | 58.8453% | 57.0968% | 55.3638% |
| 2018-10-11 | Worlds | Phong Vu Buffalo | G2 Esports | 30.7273% | 37.6222% | 40.5835% | 43.4851% |
| 2018-10-11 | Worlds | 100 Thieves | Fnatic | 21.9141% | 22.7832% | 23.6322% | 24.6764% |
| 2018-10-11 | Worlds | Invictus Gaming | G-Rex | 77.4761% | 84.8071% | 86.6990% | 88.2792% |
| 2018-10-11 | Worlds | Team Vitality | Cloud9 | 66.7638% | 64.0569% | 61.9988% | 59.5911% |
| 2018-10-11 | Worlds | Gen.G eSports | Royal Never Give Up | 40.6737% | 41.8730% | 41.7730% | 41.3538% |
| 2018-10-12 | Worlds | MAD Team | KT Rolster | 16.4837% | 16.2491% | 15.8482% | 15.4609% |
| 2018-10-12 | Worlds | Team Liquid | Edward Gaming | 38.3386% | 37.1798% | 35.7273% | 33.5010% |
| 2018-10-12 | Worlds | Fnatic | Invictus Gaming | 36.8554% | 33.0676% | 30.4528% | 27.0045% |
| 2018-10-12 | Worlds | 100 Thieves | G-Rex | 39.8153% | 47.3455% | 48.8253% | 49.1581% |
| 2018-10-12 | Worlds | Royal Never Give Up | Team Vitality | 72.4755% | 75.0229% | 77.6079% | 80.7092% |
| 2018-10-12 | Worlds | Cloud9 | Gen.G eSports | 43.7989% | 33.4271% | 29.3714% | 25.3995% |
| 2018-10-13 | Worlds | Afreeca Freecs | Phong Vu Buffalo | 55.0764% | 63.8268% | 66.2556% | 68.4439% |
| 2018-10-13 | Worlds | G2 Esports | Flash Wolves | 26.8803% | 25.1268% | 24.6610% | 24.2386% |
| 2018-10-13 | Worlds | Invictus Gaming | 100 Thieves | 86.8648% | 88.0340% | 88.6748% | 89.5882% |
| 2018-10-13 | Worlds | G-Rex | Fnatic | 28.6645% | 24.5103% | 24.2281% | 24.9421% |
| 2018-10-13 | Worlds | Team Liquid | MAD Team | 70.3272% | 69.8405% | 70.1722% | 70.7765% |
| 2018-10-13 | Worlds | KT Rolster | Edward Gaming | 56.1315% | 56.2719% | 55.3603% | 53.2968% |
| 2018-10-14 | Worlds | Team Vitality | Royal Never Give Up | 23.1739% | 22.8211% | 21.1684% | 18.8732% |
| 2018-10-14 | Worlds | Gen.G eSports | Cloud9 | 65.5987% | 71.5746% | 74.1935% | 76.8803% |
| 2018-10-14 | Worlds | Team Vitality | Gen.G eSports | 37.6686% | 33.2697% | 30.2908% | 26.8665% |
| 2018-10-14 | Worlds | Cloud9 | Royal Never Give Up | 20.7454% | 19.0635% | 17.6919% | 15.9973% |
| 2018-10-14 | Worlds | Cloud9 | Team Vitality | 46.4604% | 44.3382% | 44.4588% | 45.0127% |
| 2018-10-14 | Worlds | Royal Never Give Up | Gen.G eSports | 66.7051% | 62.7716% | 61.8059% | 61.2270% |
| 2018-10-14 | Worlds | Royal Never Give Up | Cloud9 | 79.2546% | 80.9365% | 82.3081% | 84.0027% |
| 2018-10-15 | Worlds | Afreeca Freecs | Flash Wolves | 41.5949% | 42.9886% | 43.8108% | 44.8058% |
| 2018-10-15 | Worlds | G2 Esports | Phong Vu Buffalo | 64.4894% | 60.0795% | 58.2732% | 56.5134% |
| 2018-10-15 | Worlds | Flash Wolves | G2 Esports | 56.3917% | 62.9201% | 64.9670% | 66.8496% |
| 2018-10-15 | Worlds | Phong Vu Buffalo | Afreeca Freecs | 37.4182% | 34.1806% | 33.1204% | 31.9755% |
| 2018-10-15 | Worlds | Flash Wolves | Phong Vu Buffalo | 70.1352% | 71.8609% | 72.1435% | 72.3805% |
| 2018-10-15 | Worlds | G2 Esports | Afreeca Freecs | 52.0576% | 43.8692% | 40.8845% | 37.9218% |
| 2018-10-15 | Worlds | Flash Wolves | G2 Esports | 56.3917% | 62.9201% | 64.9670% | 66.8496% |
| 2018-10-16 | Worlds | Team Liquid | KT Rolster | 26.5723% | 29.8297% | 31.0245% | 32.4098% |
| 2018-10-16 | Worlds | MAD Team | Edward Gaming | 13.2944% | 14.6327% | 14.5583% | 13.9502% |
| 2018-10-16 | Worlds | MAD Team | Team Liquid | 18.7774% | 20.2669% | 20.5438% | 20.6398% |
| 2018-10-16 | Worlds | Edward Gaming | KT Rolster | 35.3018% | 38.6650% | 40.5658% | 43.4788% |
| 2018-10-16 | Worlds | Edward Gaming | Team Liquid | 60.1240% | 59.7247% | 60.2771% | 61.6013% |
| 2018-10-16 | Worlds | KT Rolster | MAD Team | 92.2797% | 90.2482% | 89.5820% | 88.9119% |
| 2018-10-17 | Worlds | Fnatic | 100 Thieves | 73.9531% | 73.8620% | 73.3871% | 72.6641% |
| 2018-10-17 | Worlds | G-Rex | Invictus Gaming | 11.9184% | 9.3904% | 8.7994% | 8.3588% |
| 2018-10-17 | Worlds | Fnatic | G-Rex | 79.4196% | 83.1242% | 83.3864% | 82.7374% |
| 2018-10-17 | Worlds | 100 Thieves | Invictus Gaming | 15.5341% | 15.3006% | 14.9381% | 14.1233% |
| 2018-10-17 | Worlds | G-Rex | 100 Thieves | 42.3879% | 36.4554% | 35.4593% | 35.6754% |
| 2018-10-17 | Worlds | Invictus Gaming | Fnatic | 65.6960% | 66.2043% | 67.3731% | 69.5813% |
| 2018-10-17 | Worlds | Fnatic | Invictus Gaming | 34.3040% | 33.7957% | 32.6269% | 30.4187% |
| 2018-10-20 | Worlds | KT Rolster | Invictus Gaming | 50.2023% | 46.4305% | 43.6258% | 39.4059% |
| 2018-10-20 | Worlds | Royal Never Give Up | G2 Esports | 69.8708% | 70.2640% | 70.8712% | 71.9826% |
| 2018-10-21 | Worlds | Cloud9 | Afreeca Freecs | 45.7198% | 41.5285% | 38.5446% | 34.9695% |
| 2018-10-21 | Worlds | Fnatic | Edward Gaming | 67.8881% | 63.8216% | 62.0095% | 59.6226% |
| 2018-10-27 | Worlds | Invictus Gaming | G2 Esports | 66.9142% | 67.0645% | 68.0674% | 70.1979% |
| 2018-10-28 | Worlds | Fnatic | Cloud9 | 67.6738% | 66.1575% | 66.4861% | 67.5235% |
| 2018-11-03 | Worlds | Fnatic | Invictus Gaming | 58.1765% | 52.1940% | 48.8020% | 44.4823% |


## S9 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-05-01 | MSI | Dashing Buffalo | Bombers | 38.1919% | 40.7169% | 44.0612% | 49.1703% |
| 2019-05-01 | MSI | 1907 Fenerbahce | Isurus Gaming | 85.1971% | 89.5062% | 90.8234% | 92.0470% |
| 2019-05-01 | MSI | Dashing Buffalo | Isurus Gaming | 66.2213% | 70.9554% | 73.3237% | 76.3060% |
| 2019-05-01 | MSI | 1907 Fenerbahce | Bombers | 64.4640% | 70.5707% | 73.9329% | 77.6612% |
| 2019-05-01 | MSI | Bombers | Isurus Gaming | 76.0348% | 78.0554% | 77.7262% | 76.9009% |
| 2019-05-01 | MSI | 1907 Fenerbahce | Dashing Buffalo | 74.5920% | 77.7352% | 78.2647% | 78.2317% |
| 2019-05-01 | MSI | Bombers | Dashing Buffalo | 61.8081% | 59.2831% | 55.9388% | 50.8297% |
| 2019-05-01 | MSI | Isurus Gaming | 1907 Fenerbahce | 14.8029% | 10.4938% | 9.1766% | 7.9530% |
| 2019-05-02 | MSI | Isurus Gaming | Dashing Buffalo | 22.5507% | 21.4461% | 20.6353% | 19.4150% |
| 2019-05-02 | MSI | Bombers | 1907 Fenerbahce | 47.6040% | 43.3121% | 40.7801% | 37.6927% |
| 2019-05-02 | MSI | Dashing Buffalo | 1907 Fenerbahce | 53.1895% | 48.4158% | 46.8849% | 45.6861% |
| 2019-05-02 | MSI | Isurus Gaming | Bombers | 26.6942% | 25.1147% | 24.9974% | 25.0933% |
| 2019-05-02 | MSI | MEGA | Detonation FocusMe | 34.9224% | 31.8344% | 31.8541% | 32.8092% |
| 2019-05-02 | MSI | Vega Squadron | INTZ eSports | 78.4342% | 82.0907% | 82.7959% | 83.2665% |
| 2019-05-02 | MSI | Vega Squadron | Detonation FocusMe | 48.7836% | 51.3499% | 53.2201% | 56.1278% |
| 2019-05-02 | MSI | MEGA | INTZ eSports | 67.2027% | 66.9760% | 66.4133% | 65.5083% |
| 2019-05-02 | MSI | Dashing Buffalo | 1907 Fenerbahce | 53.1895% | 48.4158% | 46.8849% | 45.6861% |
| 2019-05-05 | MSI | Detonation FocusMe | INTZ eSports | 83.1813% | 84.2734% | 83.9883% | 83.1133% |
| 2019-05-05 | MSI | Vega Squadron | MEGA | 76.8362% | 78.7512% | 79.3201% | 79.9080% |
| 2019-05-05 | MSI | Detonation FocusMe | MEGA | 66.3365% | 68.3150% | 68.3272% | 67.7494% |
| 2019-05-05 | MSI | INTZ eSports | Vega Squadron | 10.7237% | 9.7932% | 9.6840% | 9.6918% |
| 2019-05-05 | MSI | INTZ eSports | MEGA | 28.4917% | 28.6913% | 29.1418% | 29.9139% |
| 2019-05-05 | MSI | Detonation FocusMe | Vega Squadron | 37.2676% | 36.7790% | 35.9974% | 34.5637% |
| 2019-05-05 | MSI | INTZ eSports | Detonation FocusMe | 16.8187% | 15.7266% | 16.0117% | 16.8867% |
| 2019-05-05 | MSI | MEGA | Vega Squadron | 23.1638% | 21.2488% | 20.6799% | 20.0920% |
| 2019-05-06 | MSI | Team Liquid | Dashing Buffalo | 49.8453% | 52.1176% | 52.8658% | 53.6416% |
| 2019-05-06 | MSI | Flash Wolves | Vega Squadron | 18.5955% | 20.5930% | 22.3873% | 25.3431% |
| 2019-05-07 | MSI | Dashing Buffalo | Vega Squadron | 53.3566% | 53.6146% | 53.2085% | 52.6078% |
| 2019-05-10 | MSI | G2 Esports | SK Telecom T1 | 52.5716% | 51.3635% | 50.1670% | 48.1765% |
| 2019-05-10 | MSI | Flash Wolves | Team Liquid | 21.3088% | 21.9032% | 22.9203% | 24.5759% |
| 2019-05-10 | MSI | Dashing Buffalo | Invictus Gaming | 24.7467% | 26.4139% | 26.7338% | 26.6105% |
| 2019-05-10 | MSI | SK Telecom T1 | Flash Wolves | 75.7565% | 75.8492% | 75.3743% | 74.7582% |
| 2019-05-10 | MSI | Invictus Gaming | G2 Esports | 53.5282% | 53.0330% | 53.4704% | 54.5411% |
| 2019-05-10 | MSI | Team Liquid | Dashing Buffalo | 73.7862% | 72.6201% | 72.2440% | 71.9282% |
| 2019-05-11 | MSI | G2 Esports | Team Liquid | 44.4437% | 44.5767% | 44.4184% | 44.1964% |
| 2019-05-11 | MSI | Dashing Buffalo | Flash Wolves | 59.3789% | 59.4688% | 58.4948% | 56.7226% |
| 2019-05-11 | MSI | Team Liquid | Invictus Gaming | 44.1325% | 46.0848% | 46.4686% | 46.4269% |
| 2019-05-11 | MSI | SK Telecom T1 | Dashing Buffalo | 69.5133% | 69.5924% | 69.9723% | 70.8630% |
| 2019-05-11 | MSI | Flash Wolves | G2 Esports | 18.2073% | 19.4076% | 20.5596% | 22.2775% |
| 2019-05-11 | MSI | Invictus Gaming | SK Telecom T1 | 68.0799% | 64.2702% | 62.9079% | 61.4589% |
| 2019-05-12 | MSI | Team Liquid | SK Telecom T1 | 50.5935% | 50.3776% | 49.9612% | 49.0796% |
| 2019-05-12 | MSI | Flash Wolves | Invictus Gaming | 10.0419% | 12.1111% | 13.0858% | 14.1889% |
| 2019-05-12 | MSI | Dashing Buffalo | G2 Esports | 13.7383% | 16.1808% | 17.0642% | 17.9098% |
| 2019-05-12 | MSI | Team Liquid | Flash Wolves | 76.5281% | 76.1317% | 75.4013% | 74.2105% |
| 2019-05-12 | MSI | SK Telecom T1 | G2 Esports | 33.6894% | 36.6718% | 38.0743% | 39.9232% |
| 2019-05-12 | MSI | Invictus Gaming | Dashing Buffalo | 89.9754% | 87.3873% | 86.6041% | 86.0535% |
| 2019-05-13 | MSI | G2 Esports | Flash Wolves | 79.7596% | 78.9840% | 78.1305% | 76.8497% |
| 2019-05-13 | MSI | Dashing Buffalo | Team Liquid | 34.5717% | 34.4312% | 34.3144% | 34.1025% |
| 2019-05-13 | MSI | G2 Esports | Invictus Gaming | 33.4589% | 36.4524% | 37.0589% | 37.2449% |
| 2019-05-13 | MSI | Flash Wolves | SK Telecom T1 | 27.3058% | 27.0998% | 27.4155% | 27.8606% |
| 2019-05-13 | MSI | Invictus Gaming | Team Liquid | 81.3451% | 77.5799% | 76.4258% | 75.5366% |
| 2019-05-13 | MSI | Dashing Buffalo | SK Telecom T1 | 26.2923% | 26.9864% | 26.9700% | 26.5811% |
| 2019-05-14 | MSI | SK Telecom T1 | Team Liquid | 63.1655% | 61.8783% | 61.7083% | 61.8876% |
| 2019-05-14 | MSI | G2 Esports | Dashing Buffalo | 82.3133% | 80.5533% | 79.9567% | 79.4261% |
| 2019-05-14 | MSI | Invictus Gaming | Flash Wolves | 91.7594% | 89.9138% | 89.0850% | 88.1641% |
| 2019-05-14 | MSI | Team Liquid | G2 Esports | 32.0412% | 34.2238% | 35.0222% | 35.8240% |
| 2019-05-14 | MSI | Flash Wolves | Dashing Buffalo | 50.9034% | 49.7354% | 50.1009% | 51.0678% |
| 2019-05-14 | MSI | SK Telecom T1 | Invictus Gaming | 24.5813% | 28.3978% | 29.7176% | 31.0410% |
| 2019-05-17 | MSI | Invictus Gaming | Team Liquid | 79.0541% | 76.2758% | 75.4232% | 74.7934% |
| 2019-05-18 | MSI | SK Telecom T1 | G2 Esports | 62.9990% | 61.4771% | 61.3434% | 61.6157% |
| 2019-05-19 | MSI | G2 Esports | Team Liquid | 50.3892% | 50.7059% | 50.7261% | 50.6978% |
| 2019-10-02 | Worlds | Clutch Gaming | Unicorns Of Love | 44.6829% | 38.2088% | 35.1350% | 31.8663% |
| 2019-10-02 | Worlds | Detonation FocusMe | Splyce | 37.8161% | 37.4642% | 36.7158% | 34.8651% |
| 2019-10-02 | Worlds | Mammoth eSports | Unicorns Of Love | 46.9851% | 34.0941% | 26.5625% | 18.7698% |
| 2019-10-02 | Worlds | Detonation FocusMe | Isurus Gaming | 50.7863% | 60.0275% | 63.7632% | 67.0193% |
| 2019-10-02 | Worlds | Mammoth eSports | Clutch Gaming | 52.3170% | 45.5516% | 40.0394% | 33.0679% |
| 2019-10-02 | Worlds | Splyce | Isurus Gaming | 62.9207% | 71.4831% | 75.2041% | 79.1507% |
| 2019-10-03 | Worlds | Royal Youth | DAMWON Gaming | 49.7967% | 42.8729% | 39.0866% | 34.2444% |
| 2019-10-03 | Worlds | MEGA | Hong Kong Attitude | 63.5053% | 51.3958% | 45.1529% | 38.3398% |
| 2019-10-03 | Worlds | DAMWON Gaming | Flamengo eSports | 72.6102% | 79.5657% | 81.5058% | 83.4856% |
| 2019-10-03 | Worlds | MEGA | Lowkey Esports.Vietnam | 65.3889% | 54.2924% | 48.9831% | 43.5822% |
| 2019-10-03 | Worlds | Royal Youth | Flamengo eSports | 72.4482% | 74.5040% | 73.8762% | 72.4725% |
| 2019-10-03 | Worlds | Hong Kong Attitude | Lowkey Esports.Vietnam | 52.0544% | 52.9036% | 53.8378% | 55.4042% |
| 2019-10-04 | Worlds | Unicorns Of Love | Clutch Gaming | 52.7353% | 57.1099% | 59.5771% | 62.5985% |
| 2019-10-04 | Worlds | Splyce | Detonation FocusMe | 80.2407% | 77.2853% | 76.2505% | 75.7228% |
| 2019-10-04 | Worlds | Unicorns Of Love | Mammoth eSports | 51.6574% | 60.3703% | 66.6598% | 74.4323% |
| 2019-10-04 | Worlds | Isurus Gaming | Detonation FocusMe | 64.2068% | 54.5644% | 49.7168% | 44.7044% |
| 2019-10-04 | Worlds | Clutch Gaming | Mammoth eSports | 48.9202% | 53.3595% | 57.5655% | 63.4954% |
| 2019-10-04 | Worlds | Isurus Gaming | Splyce | 30.6388% | 26.0878% | 23.5449% | 20.5843% |
| 2019-10-04 | Worlds | Mammoth eSports | Unicorns Of Love | 48.3426% | 39.6297% | 33.3402% | 25.5677% |
| 2019-10-04 | Worlds | Clutch Gaming | Unicorns Of Love | 47.2647% | 42.8901% | 40.4229% | 37.4015% |
| 2019-10-05 | Worlds | DAMWON Gaming | Royal Youth | 74.7185% | 73.8848% | 74.4018% | 75.7057% |
| 2019-10-05 | Worlds | Hong Kong Attitude | MEGA | 42.3824% | 49.0426% | 53.2412% | 58.5346% |
| 2019-10-05 | Worlds | Flamengo eSports | DAMWON Gaming | 25.9833% | 21.5564% | 19.9305% | 18.0846% |
| 2019-10-05 | Worlds | Lowkey Esports.Vietnam | MEGA | 41.0643% | 46.8008% | 50.1464% | 54.0731% |
| 2019-10-05 | Worlds | Flamengo eSports | Royal Youth | 50.9203% | 43.7402% | 41.9778% | 40.7571% |
| 2019-10-05 | Worlds | Lowkey Esports.Vietnam | Hong Kong Attitude | 48.6450% | 47.7555% | 46.9046% | 45.4756% |
| 2019-10-05 | Worlds | Royal Youth | Flamengo eSports | 49.0797% | 56.2598% | 58.0222% | 59.2429% |
| 2019-10-07 | Worlds | Lowkey Esports.Vietnam | DAMWON Gaming | 21.9385% | 19.2258% | 18.0108% | 16.5287% |
| 2019-10-07 | Worlds | Clutch Gaming | Royal Youth | 62.9768% | 52.3013% | 46.9939% | 41.8823% |
| 2019-10-08 | Worlds | Hong Kong Attitude | Isurus Gaming | 54.4409% | 59.7929% | 63.4779% | 67.4501% |
| 2019-10-08 | Worlds | Unicorns Of Love | Splyce | 48.1161% | 45.4497% | 43.3983% | 40.5853% |
| 2019-10-12 | Worlds | Fnatic | SK Telecom T1 | 59.6676% | 51.7829% | 47.1810% | 42.0002% |
| 2019-10-12 | Worlds | Royal Never Give Up | Clutch Gaming | 65.6143% | 69.9185% | 72.8279% | 76.6388% |
| 2019-10-12 | Worlds | Invictus Gaming | ahq e-Sports Club | 75.7502% | 74.0837% | 74.8359% | 76.7096% |
| 2019-10-12 | Worlds | DAMWON Gaming | Team Liquid | 46.7077% | 51.2138% | 54.3150% | 57.1393% |
| 2019-10-12 | Worlds | J Team | Funplus Phoenix | 15.8957% | 17.9059% | 18.2162% | 17.9872% |
| 2019-10-12 | Worlds | GAM Esports | Splyce | 50.4796% | 43.3999% | 38.7545% | 32.5616% |
| 2019-10-13 | Worlds | SK Telecom T1 | Royal Never Give Up | 48.7959% | 53.1040% | 55.4871% | 57.9520% |
| 2019-10-13 | Worlds | Fnatic | Clutch Gaming | 66.0853% | 71.2549% | 73.2296% | 75.5250% |
| 2019-10-13 | Worlds | Team Liquid | Invictus Gaming | 56.8770% | 53.5025% | 50.2998% | 46.3042% |
| 2019-10-13 | Worlds | ahq e-Sports Club | DAMWON Gaming | 27.4890% | 27.0599% | 26.1182% | 24.7220% |
| 2019-10-13 | Worlds | Griffin | G2 Esports | 33.8835% | 40.3093% | 44.7503% | 49.7579% |
| 2019-10-13 | Worlds | Cloud9 | Hong Kong Attitude | 58.0053% | 58.2649% | 57.8484% | 57.8747% |
| 2019-10-14 | Worlds | Invictus Gaming | DAMWON Gaming | 56.1666% | 50.0196% | 49.0972% | 49.4014% |
| 2019-10-14 | Worlds | ahq e-Sports Club | Team Liquid | 19.3067% | 23.0113% | 24.6966% | 26.0111% |
| 2019-10-14 | Worlds | Funplus Phoenix | Splyce | 72.3954% | 76.0783% | 76.8977% | 77.6139% |
| 2019-10-14 | Worlds | J Team | GAM Esports | 66.0590% | 64.6443% | 66.2337% | 69.3657% |
| 2019-10-14 | Worlds | Griffin | Hong Kong Attitude | 63.2477% | 72.5793% | 76.2625% | 80.1182% |
| 2019-10-14 | Worlds | G2 Esports | Cloud9 | 71.1268% | 73.0050% | 73.4026% | 73.8542% |
| 2019-10-15 | Worlds | Royal Never Give Up | Fnatic | 39.9392% | 42.2460% | 44.2120% | 47.0008% |
| 2019-10-15 | Worlds | Clutch Gaming | SK Telecom T1 | 23.7778% | 22.1726% | 19.7863% | 16.5284% |
| 2019-10-15 | Worlds | Funplus Phoenix | GAM Esports | 75.9365% | 82.0527% | 84.8434% | 88.0736% |
| 2019-10-15 | Worlds | Splyce | J Team | 56.4494% | 56.3234% | 56.5231% | 57.0017% |
| 2019-10-15 | Worlds | Cloud9 | Griffin | 43.1538% | 35.2122% | 30.9712% | 26.5000% |
| 2019-10-15 | Worlds | Hong Kong Attitude | G2 Esports | 12.6012% | 13.8862% | 14.6330% | 15.1902% |
| 2019-10-17 | Worlds | GAM Esports | Funplus Phoenix | 18.8262% | 15.3605% | 13.4166% | 10.9053% |
| 2019-10-17 | Worlds | J Team | Splyce | 56.1185% | 52.3936% | 50.8253% | 49.0059% |
| 2019-10-17 | Worlds | GAM Esports | J Team | 43.9813% | 42.7039% | 40.1449% | 35.8842% |
| 2019-10-17 | Worlds | Splyce | Funplus Phoenix | 18.7644% | 18.1164% | 18.2694% | 18.5384% |
| 2019-10-17 | Worlds | Splyce | GAM Esports | 49.8987% | 54.9370% | 59.0593% | 65.0256% |
| 2019-10-17 | Worlds | Funplus Phoenix | J Team | 77.1961% | 80.4186% | 81.2324% | 82.0547% |
| 2019-10-17 | Worlds | Funplus Phoenix | Splyce | 81.2356% | 81.8836% | 81.7306% | 81.4616% |
| 2019-10-18 | Worlds | Griffin | Cloud9 | 66.9786% | 69.9875% | 72.6358% | 75.7989% |
| 2019-10-18 | Worlds | G2 Esports | Hong Kong Attitude | 87.5843% | 86.3957% | 85.6711% | 85.0902% |
| 2019-10-18 | Worlds | Hong Kong Attitude | Griffin | 22.8859% | 19.6954% | 17.8491% | 15.6232% |
| 2019-10-18 | Worlds | Cloud9 | G2 Esports | 19.0604% | 21.5884% | 22.4810% | 23.2038% |
| 2019-10-18 | Worlds | Hong Kong Attitude | Cloud9 | 37.5769% | 36.3840% | 36.5776% | 36.7059% |
| 2019-10-18 | Worlds | G2 Esports | Griffin | 67.6750% | 60.9001% | 56.5037% | 51.3785% |
| 2019-10-18 | Worlds | G2 Esports | Griffin | 67.6750% | 60.9001% | 56.5037% | 51.3785% |
| 2019-10-19 | Worlds | Royal Never Give Up | SK Telecom T1 | 38.0003% | 38.3704% | 37.6805% | 36.7419% |
| 2019-10-19 | Worlds | Clutch Gaming | Fnatic | 28.3377% | 25.3366% | 23.9993% | 22.3570% |
| 2019-10-19 | Worlds | SK Telecom T1 | Fnatic | 64.6330% | 61.7648% | 62.4399% | 64.2126% |
| 2019-10-19 | Worlds | Clutch Gaming | Royal Never Give Up | 26.0922% | 25.2285% | 23.9059% | 21.6483% |
| 2019-10-19 | Worlds | SK Telecom T1 | Clutch Gaming | 82.2111% | 82.6399% | 84.0370% | 86.1712% |
| 2019-10-19 | Worlds | Fnatic | Royal Never Give Up | 47.1678% | 49.8570% | 49.8718% | 48.9676% |
| 2019-10-20 | Worlds | ahq e-Sports Club | Invictus Gaming | 15.4640% | 19.1136% | 19.6474% | 19.2916% |
| 2019-10-20 | Worlds | Team Liquid | DAMWON Gaming | 44.8559% | 41.1720% | 39.5796% | 38.4086% |
| 2019-10-20 | Worlds | Team Liquid | ahq e-Sports Club | 84.1886% | 80.6398% | 79.0186% | 77.6207% |
| 2019-10-20 | Worlds | DAMWON Gaming | Invictus Gaming | 54.4920% | 58.4429% | 58.4331% | 57.0715% |
| 2019-10-20 | Worlds | DAMWON Gaming | ahq e-Sports Club | 86.7476% | 85.6145% | 85.1834% | 84.7605% |
| 2019-10-20 | Worlds | Invictus Gaming | Team Liquid | 50.6583% | 50.3969% | 52.0597% | 54.6732% |
| 2019-10-26 | Worlds | Invictus Gaming | Griffin | 30.7979% | 31.8724% | 32.1197% | 32.5179% |
| 2019-10-26 | Worlds | Funplus Phoenix | Fnatic | 49.4442% | 54.6365% | 56.6983% | 59.3246% |
| 2019-10-27 | Worlds | Splyce | SK Telecom T1 | 25.9761% | 25.3999% | 24.7131% | 23.8231% |
| 2019-10-27 | Worlds | G2 Esports | DAMWON Gaming | 53.9831% | 55.5440% | 54.9860% | 54.3301% |
| 2019-11-02 | Worlds | Funplus Phoenix | Invictus Gaming | 67.1600% | 69.6481% | 68.7553% | 66.7487% |
| 2019-11-03 | Worlds | SK Telecom T1 | G2 Esports | 52.6592% | 51.1665% | 51.5958% | 52.5984% |
| 2019-11-10 | Worlds | Funplus Phoenix | G2 Esports | 54.6170% | 55.5913% | 55.7525% | 55.8312% |


## S10 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-05-28 | MSC | Funplus Phoenix | T1 | 57.0141% | 56.1356% | 55.7642% | 55.4022% |
| 2020-05-28 | MSC | Top Esports | DAMWON Gaming | 72.7698% | 71.3182% | 70.8888% | 70.5885% |
| 2020-05-28 | MSC | T1 | DAMWON Gaming | 67.8700% | 69.0167% | 69.3491% | 69.6484% |
| 2020-05-28 | MSC | Top Esports | Funplus Phoenix | 48.8188% | 46.5883% | 46.0557% | 45.7090% |
| 2020-05-28 | MSC | DAMWON Gaming | Funplus Phoenix | 26.3040% | 25.9693% | 25.9592% | 25.9697% |
| 2020-05-28 | MSC | T1 | Top Esports | 44.1476% | 47.2531% | 48.1633% | 48.8784% |
| 2020-05-29 | MSC | JD Gaming | Gen.G eSports | 80.6393% | 75.9294% | 74.1883% | 72.5075% |
| 2020-05-29 | MSC | Invictus Gaming | DragonX | 59.3364% | 60.3775% | 60.9456% | 61.7017% |
| 2020-05-29 | MSC | DragonX | Gen.G eSports | 53.9178% | 50.6403% | 49.4933% | 48.3536% |
| 2020-05-29 | MSC | JD Gaming | Invictus Gaming | 70.9265% | 66.8626% | 65.2722% | 63.6163% |
| 2020-05-29 | MSC | Invictus Gaming | Gen.G eSports | 63.0631% | 60.9886% | 60.4620% | 60.1334% |
| 2020-05-29 | MSC | DragonX | JD Gaming | 21.9308% | 24.5419% | 25.4254% | 26.1989% |
| 2020-05-29 | MSC | Gen.G eSports | DragonX | 46.0822% | 49.3597% | 50.5067% | 51.6464% |
| 2020-05-29 | MSC | DragonX | JD Gaming | 21.9308% | 24.5419% | 25.4254% | 26.1989% |
| 2020-05-30 | MSC | Funplus Phoenix | JD Gaming | 39.1318% | 40.9154% | 41.4451% | 41.8169% |
| 2020-05-30 | MSC | Gen.G eSports | Top Esports | 43.4054% | 46.0802% | 47.3003% | 48.5842% |
| 2020-05-31 | MSC | Funplus Phoenix | Top Esports | 52.4600% | 53.6703% | 53.9628% | 54.1352% |
| 2020-09-25 | Worlds | MAD Lions | INTZ e-Sports | 77.0855% | 85.3521% | 88.4950% | 91.7072% |
| 2020-09-25 | Worlds | PSG Talon | Rainbow7 | 64.4372% | 70.7614% | 72.9973% | 75.3520% |
| 2020-09-25 | Worlds | Legacy eSports | INTZ e-Sports | 80.1609% | 85.2581% | 86.7810% | 88.4462% |
| 2020-09-25 | Worlds | LGD Gaming | PSG Talon | 71.4515% | 67.8530% | 66.3702% | 64.8367% |
| 2020-09-25 | Worlds | Team Liquid | MAD Lions | 49.3151% | 46.5824% | 44.0299% | 40.4323% |
| 2020-09-26 | Worlds | Rainbow7 | V3 Esports | 35.1050% | 34.6340% | 34.7361% | 35.2229% |
| 2020-09-26 | Worlds | INTZ e-Sports | Papara SuperMassive | 32.0547% | 33.2870% | 31.8752% | 28.4809% |
| 2020-09-26 | Worlds | V3 Esports | Unicorns Of Love | 16.1397% | 12.8723% | 12.7557% | 12.6585% |
| 2020-09-26 | Worlds | LGD Gaming | Rainbow7 | 81.0326% | 83.0993% | 83.7999% | 84.6130% |
| 2020-09-26 | Worlds | Unicorns Of Love | PSG Talon | 71.9587% | 76.2671% | 75.6122% | 74.2066% |
| 2020-09-26 | Worlds | Papara SuperMassive | MAD Lions | 35.5323% | 25.7227% | 22.6686% | 20.0765% |
| 2020-09-26 | Worlds | Team Liquid | Legacy eSports | 48.7430% | 50.9973% | 52.3460% | 54.1276% |
| 2020-09-27 | Worlds | V3 Esports | LGD Gaming | 41.9454% | 36.6198% | 34.5305% | 32.0107% |
| 2020-09-27 | Worlds | Rainbow7 | Unicorns Of Love | 7.9495% | 6.7900% | 6.8831% | 7.0810% |
| 2020-09-27 | Worlds | PSG Talon | V3 Esports | 58.8415% | 61.8162% | 63.4530% | 65.7558% |
| 2020-09-27 | Worlds | Unicorns Of Love | LGD Gaming | 82.2832% | 81.5510% | 80.1277% | 78.2009% |
| 2020-09-27 | Worlds | Unicorns Of Love | PSG Talon | 81.8059% | 82.5351% | 81.4925% | 79.8712% |
| 2020-09-27 | Worlds | LGD Gaming | V3 Esports | 58.0546% | 63.3802% | 65.4695% | 67.9893% |
| 2020-09-28 | Worlds | Papara SuperMassive | Team Liquid | 33.7115% | 26.3884% | 24.8675% | 24.2184% |
| 2020-09-28 | Worlds | MAD Lions | Legacy eSports | 41.3471% | 44.3750% | 47.3407% | 51.7300% |
| 2020-09-28 | Worlds | INTZ e-Sports | Team Liquid | 10.5908% | 8.7338% | 7.9301% | 6.9079% |
| 2020-09-28 | Worlds | Legacy eSports | Papara SuperMassive | 53.9736% | 63.0972% | 64.6575% | 64.7541% |
| 2020-09-28 | Worlds | MAD Lions | INTZ e-Sports | 78.0177% | 83.6325% | 86.3390% | 89.4509% |
| 2020-09-28 | Worlds | Team Liquid | Legacy eSports | 62.6422% | 61.9986% | 62.2852% | 63.0065% |
| 2020-09-29 | Worlds | Rainbow7 | LGD Gaming | 34.2149% | 29.8779% | 28.4129% | 26.8450% |
| 2020-09-29 | Worlds | Papara SuperMassive | MAD Lions | 46.9877% | 38.4412% | 35.1192% | 31.9746% |
| 2020-09-30 | Worlds | Legacy eSports | LGD Gaming | 42.2513% | 39.2973% | 37.3519% | 35.0257% |
| 2020-09-30 | Worlds | Unicorns Of Love | Papara SuperMassive | 76.4832% | 82.7498% | 84.2333% | 85.1588% |
| 2020-10-03 | Worlds | FlyQuest | Top Esports | 17.6772% | 17.1552% | 17.0593% | 17.2606% |
| 2020-10-03 | Worlds | Unicorns Of Love | DragonX | 53.7640% | 53.7143% | 53.8325% | 53.7860% |
| 2020-10-03 | Worlds | Rogue | PSG Talon | 36.0253% | 33.8825% | 32.4664% | 30.8257% |
| 2020-10-03 | Worlds | DAMWON Gaming | JD Gaming | 65.9072% | 56.3570% | 49.8701% | 42.5926% |
| 2020-10-03 | Worlds | Gen.G eSports | LGD Gaming | 64.1895% | 63.5396% | 62.5496% | 61.6529% |
| 2020-10-03 | Worlds | TSM | Fnatic | 51.0903% | 53.6359% | 53.9859% | 53.9455% |
| 2020-10-04 | Worlds | Machi E-Sports | Team Liquid | 55.1842% | 55.3741% | 56.2428% | 57.6649% |
| 2020-10-04 | Worlds | G2 Esports | Suning | 39.1504% | 37.6774% | 37.7291% | 38.4200% |
| 2020-10-04 | Worlds | Rogue | DAMWON Gaming | 11.7946% | 13.7313% | 15.6280% | 18.0394% |
| 2020-10-04 | Worlds | PSG Talon | JD Gaming | 27.6454% | 25.8090% | 25.0284% | 24.0357% |
| 2020-10-04 | Worlds | Gen.G eSports | TSM | 86.5439% | 85.3725% | 84.5385% | 83.4231% |
| 2020-10-04 | Worlds | LGD Gaming | Fnatic | 53.5340% | 60.0617% | 61.7241% | 62.5369% |
| 2020-10-05 | Worlds | Machi E-Sports | G2 Esports | 40.4350% | 44.8750% | 46.0412% | 46.6437% |
| 2020-10-05 | Worlds | Team Liquid | Suning | 25.0558% | 26.3909% | 26.3634% | 25.8986% |
| 2020-10-05 | Worlds | DAMWON Gaming | PSG Talon | 91.0540% | 86.1879% | 82.5297% | 77.7189% |
| 2020-10-05 | Worlds | JD Gaming | Rogue | 71.7229% | 76.9719% | 79.4068% | 82.0523% |
| 2020-10-05 | Worlds | FlyQuest | Unicorns Of Love | 24.5165% | 22.4409% | 22.3228% | 22.8238% |
| 2020-10-05 | Worlds | Top Esports | DragonX | 53.3541% | 54.0640% | 55.2917% | 56.9401% |
| 2020-10-06 | Worlds | G2 Esports | Team Liquid | 74.9095% | 68.1332% | 66.6933% | 66.3374% |
| 2020-10-06 | Worlds | Suning | Machi E-Sports | 71.5386% | 69.9296% | 69.2006% | 68.4596% |
| 2020-10-06 | Worlds | DragonX | FlyQuest | 77.2108% | 79.8912% | 80.1905% | 79.9279% |
| 2020-10-06 | Worlds | Top Esports | Unicorns Of Love | 79.3237% | 74.7858% | 73.8025% | 73.2826% |
| 2020-10-06 | Worlds | Fnatic | Gen.G eSports | 20.9852% | 19.9165% | 20.1372% | 20.8322% |
| 2020-10-06 | Worlds | TSM | LGD Gaming | 28.2346% | 28.0180% | 27.8429% | 27.9062% |
| 2020-10-08 | Worlds | Team Liquid | G2 Esports | 32.1937% | 36.0052% | 36.5454% | 36.1159% |
| 2020-10-08 | Worlds | Machi E-Sports | Suning | 23.4896% | 26.2034% | 27.3234% | 28.4412% |
| 2020-10-08 | Worlds | G2 Esports | Machi E-Sports | 67.3295% | 62.8062% | 61.3780% | 60.4307% |
| 2020-10-08 | Worlds | Suning | Team Liquid | 76.8992% | 74.7750% | 74.3992% | 74.4515% |
| 2020-10-08 | Worlds | Team Liquid | Machi E-Sports | 49.4560% | 48.7196% | 47.7878% | 46.3343% |
| 2020-10-08 | Worlds | Suning | G2 Esports | 61.2479% | 62.5161% | 62.5990% | 62.2280% |
| 2020-10-08 | Worlds | Suning | G2 Esports | 61.2479% | 62.5161% | 62.5990% | 62.2280% |
| 2020-10-09 | Worlds | PSG Talon | DAMWON Gaming | 7.3448% | 11.2690% | 14.0954% | 17.7407% |
| 2020-10-09 | Worlds | Rogue | JD Gaming | 22.2872% | 20.0610% | 18.4713% | 16.4649% |
| 2020-10-09 | Worlds | DAMWON Gaming | Rogue | 89.4699% | 86.2299% | 84.1638% | 81.8293% |
| 2020-10-09 | Worlds | JD Gaming | PSG Talon | 83.8111% | 83.3622% | 83.5024% | 83.9327% |
| 2020-10-09 | Worlds | PSG Talon | Rogue | 40.2459% | 44.2991% | 46.5823% | 49.2702% |
| 2020-10-09 | Worlds | JD Gaming | DAMWON Gaming | 29.0976% | 38.8877% | 45.3701% | 52.9767% |
| 2020-10-10 | Worlds | Fnatic | TSM | 66.5930% | 60.6820% | 58.6979% | 56.8838% |
| 2020-10-10 | Worlds | LGD Gaming | Gen.G eSports | 37.5178% | 36.4207% | 36.3236% | 36.2505% |
| 2020-10-10 | Worlds | TSM | Gen.G eSports | 17.9948% | 17.9946% | 18.1779% | 18.6079% |
| 2020-10-10 | Worlds | Fnatic | LGD Gaming | 42.1456% | 37.1544% | 35.6291% | 34.6588% |
| 2020-10-10 | Worlds | LGD Gaming | TSM | 73.2361% | 72.3034% | 71.9703% | 71.3242% |
| 2020-10-10 | Worlds | Gen.G eSports | Fnatic | 69.5692% | 74.7014% | 76.0031% | 76.8272% |
| 2020-10-11 | Worlds | FlyQuest | DragonX | 21.6530% | 19.8190% | 19.5127% | 19.7046% |
| 2020-10-11 | Worlds | Unicorns Of Love | Top Esports | 18.3293% | 22.6267% | 23.7226% | 24.3925% |
| 2020-10-11 | Worlds | DragonX | Unicorns Of Love | 68.7389% | 67.1734% | 66.7802% | 66.4554% |
| 2020-10-11 | Worlds | Top Esports | FlyQuest | 87.9982% | 87.1145% | 86.8381% | 86.4418% |
| 2020-10-11 | Worlds | Unicorns Of Love | FlyQuest | 62.2004% | 66.4098% | 67.2337% | 67.2872% |
| 2020-10-11 | Worlds | DragonX | Top Esports | 33.0427% | 37.4379% | 38.4690% | 38.9926% |
| 2020-10-15 | Worlds | DAMWON Gaming | DragonX | 72.3425% | 67.0345% | 62.7016% | 57.4145% |
| 2020-10-16 | Worlds | Suning | JD Gaming | 44.4901% | 40.7299% | 38.5966% | 36.0797% |
| 2020-10-17 | Worlds | Top Esports | Fnatic | 72.3857% | 77.0563% | 78.5488% | 79.7817% |
| 2020-10-18 | Worlds | Gen.G eSports | G2 Esports | 68.1421% | 68.9570% | 69.0633% | 68.8620% |
| 2020-10-24 | Worlds | G2 Esports | DAMWON Gaming | 28.8698% | 29.8266% | 32.5245% | 36.4984% |
| 2020-10-25 | Worlds | Top Esports | Suning | 49.2628% | 56.6118% | 59.5490% | 62.4241% |
| 2020-10-31 | Worlds | DAMWON Gaming | Suning | 62.7476% | 63.6063% | 62.0504% | 59.5166% |


## S11 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2021-05-06 | MSI | DWG KIA | Cloud9 | 77.6013% | 75.9828% | 75.0824% | 73.8786% |
| 2021-05-06 | MSI | Infinity eSports | Detonation FocusMe | 45.6610% | 45.4986% | 45.4961% | 45.5361% |
| 2021-05-06 | MSI | Royal Never Give Up | Pentanet.GG | 68.6648% | 66.4483% | 65.3943% | 64.2434% |
| 2021-05-06 | MSI | Pentanet.GG | Unicorns Of Love | 61.7104% | 62.0680% | 62.0018% | 61.8141% |
| 2021-05-06 | MSI | Istanbul Wildcats | paiN Gaming | 65.6760% | 70.5256% | 72.3155% | 74.1736% |
| 2021-05-06 | MSI | MAD Lions | PSG Talon | 14.2235% | 9.8940% | 8.6860% | 7.6193% |
| 2021-05-07 | MSI | Pentanet.GG | Royal Never Give Up | 18.6649% | 21.0884% | 22.1290% | 23.2536% |
| 2021-05-07 | MSI | Unicorns Of Love | Royal Never Give Up | 27.1638% | 28.4274% | 29.2804% | 30.3285% |
| 2021-05-07 | MSI | Infinity eSports | DWG KIA | 13.1575% | 14.0956% | 14.8419% | 15.9152% |
| 2021-05-07 | MSI | Detonation FocusMe | Cloud9 | 28.5827% | 29.5801% | 30.2515% | 31.0989% |
| 2021-05-07 | MSI | Istanbul Wildcats | MAD Lions | 23.4629% | 26.6730% | 27.9908% | 29.4267% |
| 2021-05-07 | MSI | paiN Gaming | PSG Talon | 17.5558% | 10.7172% | 8.9056% | 7.3469% |
| 2021-05-08 | MSI | Royal Never Give Up | Unicorns Of Love | 79.4246% | 77.7895% | 76.9426% | 75.9549% |
| 2021-05-08 | MSI | Unicorns Of Love | Pentanet.GG | 60.1218% | 58.3251% | 57.9245% | 57.6487% |
| 2021-05-08 | MSI | DWG KIA | Detonation FocusMe | 88.5844% | 87.2502% | 86.4880% | 85.4763% |
| 2021-05-08 | MSI | Cloud9 | Infinity eSports | 49.9975% | 53.3807% | 53.9205% | 54.1433% |
| 2021-05-08 | MSI | MAD Lions | paiN Gaming | 79.1247% | 79.7867% | 80.1281% | 80.5325% |
| 2021-05-08 | MSI | PSG Talon | Istanbul Wildcats | 87.8369% | 90.0297% | 90.7645% | 91.4703% |
| 2021-05-09 | MSI | Unicorns Of Love | Royal Never Give Up | 14.2547% | 16.0006% | 16.7958% | 17.6911% |
| 2021-05-09 | MSI | Unicorns Of Love | Pentanet.GG | 44.4477% | 44.1666% | 44.1725% | 44.2492% |
| 2021-05-09 | MSI | Royal Never Give Up | Pentanet.GG | 82.7967% | 80.5930% | 79.6733% | 78.6904% |
| 2021-05-09 | MSI | Royal Never Give Up | Unicorns Of Love | 85.7453% | 83.9994% | 83.2042% | 82.3089% |
| 2021-05-09 | MSI | Pentanet.GG | Unicorns Of Love | 55.5523% | 55.8334% | 55.8275% | 55.7508% |
| 2021-05-09 | MSI | Pentanet.GG | Royal Never Give Up | 17.2033% | 19.4070% | 20.3267% | 21.3096% |
| 2021-05-09 | MSI | Unicorns Of Love | Pentanet.GG | 44.4477% | 44.1666% | 44.1725% | 44.2492% |
| 2021-05-10 | MSI | MAD Lions | Istanbul Wildcats | 84.0621% | 80.5885% | 79.2707% | 77.8936% |
| 2021-05-10 | MSI | PSG Talon | paiN Gaming | 88.3700% | 92.1280% | 93.2541% | 94.2746% |
| 2021-05-10 | MSI | Istanbul Wildcats | PSG Talon | 10.6222% | 8.9376% | 8.3452% | 7.7645% |
| 2021-05-10 | MSI | paiN Gaming | MAD Lions | 17.3520% | 17.3350% | 17.2022% | 16.9946% |
| 2021-05-10 | MSI | paiN Gaming | Istanbul Wildcats | 52.5472% | 46.5410% | 44.2741% | 41.9085% |
| 2021-05-10 | MSI | PSG Talon | MAD Lions | 61.4690% | 71.0496% | 74.1739% | 77.1235% |
| 2021-05-11 | MSI | Cloud9 | DWG KIA | 14.2944% | 16.4380% | 17.3477% | 18.4167% |
| 2021-05-11 | MSI | Detonation FocusMe | Infinity eSports | 52.7076% | 52.8428% | 52.8442% | 52.8090% |
| 2021-05-11 | MSI | DWG KIA | Infinity eSports | 90.9466% | 89.8126% | 89.1757% | 88.3377% |
| 2021-05-11 | MSI | Cloud9 | Detonation FocusMe | 60.0528% | 60.7483% | 60.6767% | 60.4431% |
| 2021-05-11 | MSI | Detonation FocusMe | DWG KIA | 9.9866% | 11.2771% | 11.9737% | 12.8719% |
| 2021-05-11 | MSI | Infinity eSports | Cloud9 | 37.3770% | 36.5730% | 36.6414% | 36.9016% |
| 2021-05-14 | MSI | DWG KIA | Royal Never Give Up | 45.9551% | 43.4300% | 42.0572% | 40.3061% |
| 2021-05-14 | MSI | MAD Lions | Pentanet.GG | 74.9567% | 68.9651% | 66.4006% | 63.5539% |
| 2021-05-14 | MSI | PSG Talon | DWG KIA | 43.8560% | 50.2050% | 53.0160% | 56.1749% |
| 2021-05-14 | MSI | Royal Never Give Up | Cloud9 | 74.0569% | 76.2040% | 76.9650% | 77.7748% |
| 2021-05-14 | MSI | PSG Talon | Pentanet.GG | 80.1325% | 80.3194% | 80.3461% | 80.3306% |
| 2021-05-14 | MSI | Cloud9 | MAD Lions | 41.5452% | 42.5588% | 43.0494% | 43.6076% |
| 2021-05-15 | MSI | Pentanet.GG | Royal Never Give Up | 10.3229% | 12.2322% | 12.9878% | 13.7780% |
| 2021-05-15 | MSI | DWG KIA | Cloud9 | 75.0366% | 75.0310% | 74.7585% | 74.2887% |
| 2021-05-15 | MSI | MAD Lions | Royal Never Give Up | 33.3495% | 30.8490% | 29.8475% | 28.7514% |
| 2021-05-15 | MSI | Cloud9 | PSG Talon | 30.6347% | 26.6749% | 25.2371% | 23.7953% |
| 2021-05-15 | MSI | Pentanet.GG | DWG KIA | 14.9347% | 17.6020% | 18.9940% | 20.7334% |
| 2021-05-15 | MSI | MAD Lions | PSG Talon | 50.3253% | 42.7753% | 40.0551% | 37.3408% |
| 2021-05-16 | MSI | Cloud9 | Pentanet.GG | 63.0378% | 59.5198% | 57.9704% | 56.2409% |
| 2021-05-16 | MSI | Royal Never Give Up | PSG Talon | 71.6435% | 67.5143% | 66.0850% | 64.7196% |
| 2021-05-16 | MSI | DWG KIA | MAD Lions | 59.0466% | 60.9070% | 61.2466% | 61.3595% |
| 2021-05-16 | MSI | Royal Never Give Up | Pentanet.GG | 91.5334% | 89.6907% | 88.9802% | 88.2484% |
| 2021-05-16 | MSI | Cloud9 | DWG KIA | 19.6898% | 20.5468% | 21.0058% | 21.5943% |
| 2021-05-16 | MSI | PSG Talon | MAD Lions | 47.0034% | 53.4251% | 55.8034% | 58.2116% |
| 2021-05-17 | MSI | PSG Talon | Royal Never Give Up | 41.6131% | 43.8290% | 44.6486% | 45.4333% |
| 2021-05-17 | MSI | MAD Lions | DWG KIA | 31.0485% | 31.1099% | 31.2716% | 31.5608% |
| 2021-05-17 | MSI | Cloud9 | Royal Never Give Up | 17.7307% | 17.7287% | 17.6171% | 17.4216% |
| 2021-05-17 | MSI | Pentanet.GG | MAD Lions | 17.0507% | 20.9472% | 22.6193% | 24.4776% |
| 2021-05-17 | MSI | DWG KIA | PSG Talon | 58.7432% | 54.4737% | 52.5525% | 50.3691% |
| 2021-05-17 | MSI | Pentanet.GG | Cloud9 | 30.3537% | 34.1428% | 35.7193% | 37.4472% |
| 2021-05-18 | MSI | Royal Never Give Up | DWG KIA | 41.6460% | 44.8390% | 46.2332% | 47.8556% |
| 2021-05-18 | MSI | Pentanet.GG | PSG Talon | 16.7804% | 17.1983% | 17.3826% | 17.5958% |
| 2021-05-18 | MSI | Royal Never Give Up | MAD Lions | 67.8553% | 69.7060% | 70.4844% | 71.3527% |
| 2021-05-18 | MSI | PSG Talon | Cloud9 | 70.4274% | 72.4682% | 73.2818% | 74.1327% |
| 2021-05-18 | MSI | DWG KIA | Pentanet.GG | 91.8662% | 89.9473% | 89.0438% | 87.9694% |
| 2021-05-18 | MSI | MAD Lions | Cloud9 | 64.7099% | 63.3449% | 62.8085% | 62.2466% |
| 2021-05-21 | MSI | Royal Never Give Up | PSG Talon | 58.3206% | 56.6659% | 56.0375% | 55.4331% |
| 2021-05-22 | MSI | DWG KIA | MAD Lions | 71.9436% | 71.6864% | 71.4859% | 71.1903% |
| 2021-05-23 | MSI | Royal Never Give Up | DWG KIA | 49.6543% | 51.3899% | 52.2792% | 53.3709% |
| 2021-10-05 | Worlds | Hanwha Life eSports | LNG Esports | 44.5512% | 39.5828% | 38.4599% | 38.2685% |
| 2021-10-05 | Worlds | Infinity eSports | RED Canids | 52.5552% | 56.3492% | 56.8977% | 56.5829% |
| 2021-10-05 | Worlds | LNG Esports | PEACE | 67.4295% | 73.8748% | 76.5730% | 79.3244% |
| 2021-10-05 | Worlds | Hanwha Life eSports | Infinity eSports | 67.5302% | 67.8319% | 69.6546% | 72.3978% |
| 2021-10-05 | Worlds | Unicorns Of Love | Detonation FocusMe | 43.0445% | 48.5833% | 50.7850% | 52.4203% |
| 2021-10-05 | Worlds | Galatasaray Esports | Beyond Gaming | 39.9219% | 36.0191% | 34.7672% | 33.1711% |
| 2021-10-05 | Worlds | Detonation FocusMe | Cloud9 | 58.9689% | 50.8906% | 46.1851% | 41.2415% |
| 2021-10-05 | Worlds | Unicorns Of Love | Galatasaray Esports | 42.1599% | 43.8269% | 45.3649% | 47.8597% |
| 2021-10-06 | Worlds | PEACE | Hanwha Life eSports | 34.7286% | 32.8407% | 30.9698% | 28.0416% |
| 2021-10-06 | Worlds | RED Canids | LNG Esports | 26.5109% | 21.0394% | 18.8561% | 17.1527% |
| 2021-10-06 | Worlds | Infinity eSports | PEACE | 35.6200% | 39.8624% | 41.2683% | 42.9772% |
| 2021-10-06 | Worlds | RED Canids | Hanwha Life eSports | 38.9459% | 33.1010% | 30.2565% | 27.3393% |
| 2021-10-06 | Worlds | Beyond Gaming | Cloud9 | 54.3680% | 59.7381% | 59.1887% | 57.1139% |
| 2021-10-06 | Worlds | Galatasaray Esports | Detonation FocusMe | 69.4800% | 67.9507% | 66.7808% | 64.5325% |
| 2021-10-06 | Worlds | Beyond Gaming | Unicorns Of Love | 71.0924% | 72.4019% | 72.1742% | 71.5199% |
| 2021-10-06 | Worlds | Cloud9 | Galatasaray Esports | 32.6684% | 36.0819% | 39.8839% | 45.7279% |
| 2021-10-07 | Worlds | LNG Esports | Infinity eSports | 89.4574% | 87.8986% | 87.8567% | 87.9690% |
| 2021-10-07 | Worlds | PEACE | RED Canids | 55.7455% | 56.9745% | 57.2264% | 56.5740% |
| 2021-10-07 | Worlds | Detonation FocusMe | Beyond Gaming | 57.3982% | 46.9310% | 43.1250% | 39.9289% |
| 2021-10-07 | Worlds | Cloud9 | Unicorns Of Love | 80.9765% | 74.6930% | 73.2218% | 72.4576% |
| 2021-10-07 | Worlds | Unicorns Of Love | Beyond Gaming | 28.2105% | 27.6869% | 27.8292% | 28.3072% |
| 2021-10-07 | Worlds | Detonation FocusMe | Cloud9 | 44.6129% | 43.9011% | 41.8311% | 39.0209% |
| 2021-10-08 | Worlds | Galatasaray Esports | Beyond Gaming | 51.5796% | 46.5563% | 44.3441% | 41.6714% |
| 2021-10-08 | Worlds | PEACE | RED Canids | 65.7704% | 64.6982% | 64.1464% | 62.7950% |
| 2021-10-09 | Worlds | Beyond Gaming | Hanwha Life eSports | 40.0471% | 47.6765% | 48.6234% | 47.9176% |
| 2021-10-09 | Worlds | PEACE | Cloud9 | 41.7382% | 37.7755% | 35.5334% | 32.7062% |
| 2021-10-11 | Worlds | DWG KIA | Funplus Phoenix | 55.4921% | 52.4260% | 50.8031% | 48.8625% |
| 2021-10-11 | Worlds | Royal Never Give Up | PSG Talon | 61.5037% | 60.0840% | 60.7170% | 61.9909% |
| 2021-10-11 | Worlds | Hanwha Life eSports | Fnatic | 70.1173% | 67.0972% | 65.8209% | 64.1848% |
| 2021-10-11 | Worlds | LNG Esports | Gen.G eSports | 59.0880% | 54.0617% | 52.6291% | 51.1323% |
| 2021-10-11 | Worlds | T1 | Detonation FocusMe | 54.6207% | 59.6264% | 62.4849% | 65.7036% |
| 2021-10-11 | Worlds | Edward Gaming | 100 Thieves | 70.4935% | 73.7159% | 76.2097% | 79.4524% |
| 2021-10-11 | Worlds | Team Liquid | MAD Lions | 35.2722% | 37.5649% | 37.9218% | 37.5439% |
| 2021-10-11 | Worlds | Rogue | Cloud9 | 29.1554% | 37.5129% | 41.9179% | 47.4781% |
| 2021-10-12 | Worlds | T1 | Edward Gaming | 53.0354% | 47.2713% | 43.5626% | 38.7765% |
| 2021-10-12 | Worlds | Rogue | DWG KIA | 11.0925% | 13.2414% | 15.1645% | 18.0968% |
| 2021-10-12 | Worlds | PSG Talon | Hanwha Life eSports | 29.4824% | 42.6407% | 47.7922% | 52.6740% |
| 2021-10-12 | Worlds | Fnatic | Royal Never Give Up | 23.4808% | 20.7903% | 19.2878% | 17.8618% |
| 2021-10-12 | Worlds | Cloud9 | Funplus Phoenix | 29.0099% | 25.1602% | 23.8310% | 22.3595% |
| 2021-10-12 | Worlds | Detonation FocusMe | 100 Thieves | 57.7764% | 53.5303% | 51.1437% | 48.5221% |
| 2021-10-12 | Worlds | MAD Lions | Gen.G eSports | 31.6089% | 35.8608% | 37.1457% | 38.8076% |
| 2021-10-12 | Worlds | Team Liquid | LNG Esports | 34.2769% | 34.5616% | 34.7387% | 35.0845% |
| 2021-10-13 | Worlds | Royal Never Give Up | Hanwha Life eSports | 61.6083% | 65.7236% | 68.3901% | 71.3723% |
| 2021-10-13 | Worlds | MAD Lions | LNG Esports | 39.5159% | 41.3493% | 41.9739% | 43.2415% |
| 2021-10-13 | Worlds | Funplus Phoenix | Rogue | 82.8085% | 83.0163% | 82.1755% | 80.6741% |
| 2021-10-13 | Worlds | PSG Talon | Fnatic | 68.2424% | 72.1692% | 73.5547% | 74.4244% |
| 2021-10-13 | Worlds | Gen.G eSports | Team Liquid | 62.8406% | 65.6929% | 66.5518% | 67.3063% |
| 2021-10-13 | Worlds | DWG KIA | Cloud9 | 83.8654% | 81.4466% | 80.7156% | 80.1042% |
| 2021-10-13 | Worlds | Edward Gaming | Detonation FocusMe | 79.1398% | 79.9351% | 81.8491% | 84.5257% |
| 2021-10-13 | Worlds | 100 Thieves | T1 | 35.3130% | 33.8813% | 33.3580% | 32.7031% |
| 2021-10-15 | Worlds | Funplus Phoenix | DWG KIA | 40.0456% | 46.7477% | 48.9997% | 51.2835% |
| 2021-10-15 | Worlds | Cloud9 | Rogue | 60.5539% | 58.1707% | 55.5329% | 51.5402% |
| 2021-10-15 | Worlds | Funplus Phoenix | Cloud9 | 81.6801% | 82.5736% | 82.8970% | 83.3069% |
| 2021-10-15 | Worlds | DWG KIA | Rogue | 91.1087% | 88.2442% | 86.3018% | 83.4493% |
| 2021-10-15 | Worlds | Rogue | Funplus Phoenix | 12.7481% | 13.1760% | 14.1782% | 15.8535% |
| 2021-10-15 | Worlds | Cloud9 | DWG KIA | 13.0291% | 15.6306% | 16.5431% | 17.4195% |
| 2021-10-15 | Worlds | Funplus Phoenix | Rogue | 87.2519% | 86.8240% | 85.8218% | 84.1465% |
| 2021-10-15 | Worlds | Cloud9 | Rogue | 60.5539% | 58.1707% | 55.5329% | 51.5402% |
| 2021-10-16 | Worlds | Detonation FocusMe | Edward Gaming | 21.7581% | 21.7191% | 19.9549% | 17.2105% |
| 2021-10-16 | Worlds | T1 | 100 Thieves | 71.4306% | 70.1837% | 69.7913% | 69.5099% |
| 2021-10-16 | Worlds | Edward Gaming | T1 | 56.9977% | 56.9902% | 58.7504% | 61.8780% |
| 2021-10-16 | Worlds | 100 Thieves | Detonation FocusMe | 52.0407% | 53.6087% | 54.9359% | 56.5213% |
| 2021-10-16 | Worlds | Detonation FocusMe | T1 | 26.9322% | 26.8812% | 26.2027% | 25.2294% |
| 2021-10-16 | Worlds | 100 Thieves | Edward Gaming | 23.1805% | 24.2778% | 23.3074% | 21.2749% |
| 2021-10-17 | Worlds | Hanwha Life eSports | PSG Talon | 53.9311% | 49.0798% | 46.8446% | 44.5877% |
| 2021-10-17 | Worlds | Royal Never Give Up | Fnatic | 83.9720% | 81.4085% | 81.6641% | 82.3538% |
| 2021-10-17 | Worlds | PSG Talon | Royal Never Give Up | 35.2758% | 40.9564% | 41.4040% | 40.7326% |
| 2021-10-17 | Worlds | Fnatic | Hanwha Life eSports | 23.0272% | 25.4606% | 26.5010% | 27.9260% |
| 2021-10-17 | Worlds | Hanwha Life eSports | Royal Never Give Up | 38.9510% | 40.0693% | 38.3748% | 35.6091% |
| 2021-10-17 | Worlds | Fnatic | PSG Talon | 25.9377% | 24.7683% | 24.1135% | 23.7674% |
| 2021-10-17 | Worlds | Hanwha Life eSports | Royal Never Give Up | 38.9510% | 40.0693% | 38.3748% | 35.6091% |
| 2021-10-18 | Worlds | Gen.G eSports | MAD Lions | 63.7752% | 63.4802% | 63.6645% | 63.4727% |
| 2021-10-18 | Worlds | LNG Esports | Team Liquid | 69.8261% | 64.5735% | 62.7097% | 60.9118% |
| 2021-10-18 | Worlds | Gen.G eSports | LNG Esports | 51.7515% | 57.9921% | 59.9872% | 61.6473% |
| 2021-10-18 | Worlds | MAD Lions | Team Liquid | 58.5040% | 59.1440% | 58.9980% | 59.0410% |
| 2021-10-18 | Worlds | Team Liquid | Gen.G eSports | 28.7180% | 28.4389% | 28.3998% | 28.5323% |
| 2021-10-18 | Worlds | LNG Esports | MAD Lions | 62.1409% | 55.7352% | 53.8896% | 51.9477% |
| 2021-10-18 | Worlds | Gen.G eSports | Team Liquid | 71.2820% | 71.5611% | 71.6002% | 71.4677% |
| 2021-10-18 | Worlds | MAD Lions | LNG Esports | 37.8591% | 44.2648% | 46.1104% | 48.0523% |
| 2021-10-18 | Worlds | Gen.G eSports | MAD Lions | 63.7752% | 63.4802% | 63.6645% | 63.4727% |
| 2021-10-22 | Worlds | T1 | Hanwha Life eSports | 61.3155% | 60.0476% | 59.6760% | 59.1305% |
| 2021-10-23 | Worlds | Edward Gaming | Royal Never Give Up | 51.2866% | 50.5586% | 50.4407% | 50.5869% |
| 2021-10-24 | Worlds | DWG KIA | MAD Lions | 81.4813% | 78.0282% | 76.8744% | 75.7062% |
| 2021-10-25 | Worlds | Gen.G eSports | Cloud9 | 64.4900% | 67.0769% | 67.9296% | 68.5401% |
| 2021-10-30 | Worlds | DWG KIA | T1 | 63.7855% | 62.5043% | 62.4863% | 63.1176% |
| 2021-10-31 | Worlds | Edward Gaming | Gen.G eSports | 47.5170% | 48.0064% | 48.9264% | 50.9767% |
| 2021-11-06 | Worlds | DWG KIA | Edward Gaming | 73.6842% | 69.3711% | 66.9016% | 63.7235% |


## S12 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-05-10 | MSI | T1 | Saigon Buffalo | 91.9444% | 93.6248% | 94.0584% | 94.4385% |
| 2022-05-10 | MSI | Team Aze | Detonation FocusMe | 19.1378% | 11.4565% | 9.6551% | 8.4215% |
| 2022-05-10 | MSI | ORDER | G2 Esports | 33.7937% | 26.9211% | 23.7433% | 20.3542% |
| 2022-05-10 | MSI | Evil Geniuses | G2 Esports | 54.5863% | 50.2351% | 48.2785% | 45.8470% |
| 2022-05-10 | MSI | RED Canids | PSG Talon | 16.0868% | 10.1684% | 8.4164% | 6.9094% |
| 2022-05-11 | MSI | G2 Esports | Evil Geniuses | 64.0666% | 63.8038% | 64.2805% | 65.2429% |
| 2022-05-11 | MSI | Evil Geniuses | ORDER | 68.8372% | 71.8558% | 73.5432% | 75.3640% |
| 2022-05-11 | MSI | Detonation FocusMe | Saigon Buffalo | 81.0429% | 85.4937% | 86.6786% | 87.5751% |
| 2022-05-11 | MSI | Team Aze | T1 | 5.4667% | 3.9037% | 3.4543% | 3.1013% |
| 2022-05-11 | MSI | Istanbul Wildcats | RED Canids | 69.3783% | 73.1805% | 73.2627% | 72.0870% |
| 2022-05-12 | MSI | ORDER | Evil Geniuses | 27.1383% | 25.3843% | 24.1481% | 22.7293% |
| 2022-05-12 | MSI | G2 Esports | ORDER | 85.3795% | 86.1009% | 87.0395% | 88.2691% |
| 2022-05-12 | MSI | PSG Talon | Istanbul Wildcats | 39.0886% | 50.1044% | 55.7945% | 62.8070% |
| 2022-05-12 | MSI | Saigon Buffalo | Team Aze | 69.9332% | 71.8659% | 72.8334% | 73.5754% |
| 2022-05-12 | MSI | T1 | Detonation FocusMe | 85.2886% | 83.2858% | 82.6104% | 82.1151% |
| 2022-05-13 | MSI | PSG Talon | RED Canids | 75.0223% | 82.4709% | 84.9536% | 87.2262% |
| 2022-05-13 | MSI | Royal Never Give Up | Istanbul Wildcats | 69.8688% | 69.1247% | 70.2704% | 72.5325% |
| 2022-05-13 | MSI | Istanbul Wildcats | PSG Talon | 43.0245% | 37.3363% | 33.8918% | 29.3875% |
| 2022-05-13 | MSI | RED Canids | Royal Never Give Up | 15.9762% | 13.7439% | 12.7521% | 11.7585% |
| 2022-05-13 | MSI | RED Canids | Istanbul Wildcats | 30.5987% | 26.2935% | 25.6765% | 26.0288% |
| 2022-05-13 | MSI | PSG Talon | Royal Never Give Up | 36.3501% | 42.8460% | 45.2125% | 47.6419% |
| 2022-05-14 | MSI | Evil Geniuses | G2 Esports | 32.2128% | 32.7852% | 32.4342% | 31.6495% |
| 2022-05-14 | MSI | Evil Geniuses | ORDER | 78.5645% | 79.3025% | 80.0608% | 80.9839% |
| 2022-05-14 | MSI | G2 Esports | ORDER | 88.5226% | 88.7072% | 89.3213% | 90.1933% |
| 2022-05-14 | MSI | G2 Esports | Evil Geniuses | 67.7872% | 67.2148% | 67.5658% | 68.3505% |
| 2022-05-14 | MSI | ORDER | G2 Esports | 11.4774% | 11.2928% | 10.6787% | 9.8067% |
| 2022-05-14 | MSI | Istanbul Wildcats | Royal Never Give Up | 13.7221% | 15.9194% | 15.9611% | 15.3598% |
| 2022-05-14 | MSI | Royal Never Give Up | PSG Talon | 69.8013% | 63.8584% | 61.7266% | 59.5587% |
| 2022-05-14 | MSI | Royal Never Give Up | RED Canids | 87.7180% | 88.3363% | 88.8453% | 89.4443% |
| 2022-05-14 | MSI | ORDER | Evil Geniuses | 21.4355% | 20.6975% | 19.9392% | 19.0161% |
| 2022-05-15 | MSI | Team Aze | Saigon Buffalo | 23.6618% | 22.8579% | 22.2981% | 21.8640% |
| 2022-05-15 | MSI | Detonation FocusMe | T1 | 12.4543% | 14.3130% | 14.9421% | 15.4260% |
| 2022-05-15 | MSI | Saigon Buffalo | Detonation FocusMe | 44.5799% | 36.1142% | 33.5838% | 31.4828% |
| 2022-05-15 | MSI | T1 | Team Aze | 96.5745% | 97.2782% | 97.5142% | 97.7086% |
| 2022-05-15 | MSI | Detonation FocusMe | Team Aze | 80.0428% | 85.6530% | 87.3280% | 88.6074% |
| 2022-05-15 | MSI | Saigon Buffalo | T1 | 10.2684% | 8.6279% | 8.1582% | 7.7328% |
| 2022-05-20 | MSI | T1 | G2 Esports | 64.2374% | 69.5634% | 70.8335% | 71.7408% |
| 2022-05-20 | MSI | Evil Geniuses | Royal Never Give Up | 26.9822% | 26.5651% | 25.8644% | 24.7174% |
| 2022-05-20 | MSI | PSG Talon | Saigon Buffalo | 56.5926% | 62.8516% | 65.4101% | 68.2708% |
| 2022-05-20 | MSI | G2 Esports | Royal Never Give Up | 52.7626% | 50.7251% | 49.9100% | 48.9635% |
| 2022-05-20 | MSI | Saigon Buffalo | Evil Geniuses | 39.8255% | 40.8460% | 41.3295% | 41.9256% |
| 2022-05-20 | MSI | PSG Talon | T1 | 13.7132% | 15.2273% | 16.1111% | 17.3146% |
| 2022-05-21 | MSI | G2 Esports | Evil Geniuses | 82.0678% | 80.0005% | 79.7158% | 79.7877% |
| 2022-05-21 | MSI | Royal Never Give Up | PSG Talon | 74.3262% | 68.9777% | 67.0661% | 65.1627% |
| 2022-05-21 | MSI | T1 | Saigon Buffalo | 89.9101% | 90.9182% | 91.2580% | 91.5862% |
| 2022-05-21 | MSI | PSG Talon | Evil Geniuses | 44.4574% | 51.7558% | 54.8304% | 58.3209% |
| 2022-05-21 | MSI | Royal Never Give Up | T1 | 39.1286% | 34.3639% | 33.3185% | 32.7273% |
| 2022-05-21 | MSI | Saigon Buffalo | G2 Esports | 8.1216% | 10.2151% | 10.7613% | 11.1276% |
| 2022-05-22 | MSI | Evil Geniuses | T1 | 28.2711% | 23.3576% | 21.8218% | 20.3673% |
| 2022-05-22 | MSI | G2 Esports | PSG Talon | 89.3134% | 84.3353% | 82.3723% | 80.3197% |
| 2022-05-22 | MSI | Royal Never Give Up | Saigon Buffalo | 89.1293% | 87.7109% | 87.4928% | 87.5003% |
| 2022-05-22 | MSI | T1 | PSG Talon | 81.6855% | 81.1811% | 80.7370% | 80.0505% |
| 2022-05-22 | MSI | Royal Never Give Up | G2 Esports | 35.7806% | 39.1741% | 40.3181% | 41.4670% |
| 2022-05-22 | MSI | Evil Geniuses | Saigon Buffalo | 75.5818% | 73.0181% | 72.1644% | 71.3038% |
| 2022-05-23 | MSI | PSG Talon | G2 Esports | 21.7187% | 25.9713% | 27.6444% | 29.4041% |
| 2022-05-23 | MSI | T1 | Evil Geniuses | 77.1430% | 80.0742% | 81.1081% | 82.1416% |
| 2022-05-23 | MSI | Saigon Buffalo | Royal Never Give Up | 8.2848% | 9.6569% | 9.9227% | 10.0020% |
| 2022-05-23 | MSI | G2 Esports | T1 | 46.6580% | 41.4150% | 39.9226% | 38.7480% |
| 2022-05-23 | MSI | Saigon Buffalo | PSG Talon | 28.4142% | 26.1882% | 25.0516% | 23.6779% |
| 2022-05-23 | MSI | Royal Never Give Up | Evil Geniuses | 78.2558% | 76.7878% | 76.7843% | 77.1851% |
| 2022-05-24 | MSI | G2 Esports | Saigon Buffalo | 83.7397% | 83.5207% | 83.5408% | 83.6714% |
| 2022-05-24 | MSI | Evil Geniuses | PSG Talon | 56.6688% | 52.2554% | 50.2330% | 47.8427% |
| 2022-05-24 | MSI | Saigon Buffalo | T1 | 11.8479% | 10.7078% | 10.3282% | 9.9682% |
| 2022-05-24 | MSI | PSG Talon | Royal Never Give Up | 17.8759% | 22.1089% | 23.6215% | 25.0867% |
| 2022-05-24 | MSI | Evil Geniuses | G2 Esports | 34.5190% | 33.5399% | 32.9726% | 32.1729% |
| 2022-05-24 | MSI | T1 | Royal Never Give Up | 43.8256% | 50.3191% | 52.0494% | 53.3024% |
| 2022-05-27 | MSI | Royal Never Give Up | Evil Geniuses | 75.8308% | 74.8391% | 74.8668% | 75.2298% |
| 2022-05-28 | MSI | T1 | G2 Esports | 67.4235% | 68.8451% | 69.2682% | 69.5507% |
| 2022-05-29 | MSI | Royal Never Give Up | T1 | 46.0536% | 42.0494% | 40.9989% | 40.2976% |
| 2022-09-29 | Worlds | Isurus | MAD Lions | 35.1630% | 23.1589% | 18.9636% | 15.3925% |
| 2022-09-29 | Worlds | Fnatic | Evil Geniuses | 41.4048% | 43.6222% | 46.1669% | 49.7233% |
| 2022-09-29 | Worlds | LOUD | Beyond Gaming | 48.3363% | 41.8247% | 38.9997% | 36.6899% |
| 2022-09-29 | Worlds | MAD Lions | Istanbul Wildcats | 34.7639% | 46.5792% | 53.3586% | 60.7073% |
| 2022-09-29 | Worlds | Chief Esports Club | Fnatic | 73.4459% | 66.1365% | 58.3203% | 47.0450% |
| 2022-09-29 | Worlds | Detonation FocusMe | LOUD | 75.6442% | 76.7786% | 75.4854% | 72.9592% |
| 2022-09-29 | Worlds | Saigon Buffalo | Istanbul Wildcats | 42.4721% | 47.9208% | 51.8473% | 56.7687% |
| 2022-09-29 | Worlds | DRX | Royal Never Give Up | 40.5239% | 33.9151% | 30.7973% | 27.3667% |
| 2022-09-30 | Worlds | Fnatic | Detonation FocusMe | 52.8331% | 53.7671% | 58.0445% | 64.6450% |
| 2022-09-30 | Worlds | Evil Geniuses | LOUD | 47.5893% | 58.7763% | 64.0403% | 69.3728% |
| 2022-09-30 | Worlds | Saigon Buffalo | Isurus | 79.2394% | 81.7225% | 83.0109% | 84.4649% |
| 2022-09-30 | Worlds | Detonation FocusMe | Chief Esports Club | 53.0754% | 52.1927% | 51.5201% | 50.9764% |
| 2022-09-30 | Worlds | Evil Geniuses | Beyond Gaming | 41.6089% | 49.1083% | 52.4202% | 56.2960% |
| 2022-09-30 | Worlds | DRX | Saigon Buffalo | 67.3751% | 69.6606% | 70.2754% | 70.5897% |
| 2022-09-30 | Worlds | MAD Lions | Royal Never Give Up | 38.7039% | 30.6121% | 27.1556% | 23.3641% |
| 2022-09-30 | Worlds | Istanbul Wildcats | DRX | 22.4216% | 21.5851% | 20.3250% | 18.6390% |
| 2022-10-01 | Worlds | LOUD | Fnatic | 29.3790% | 26.3245% | 23.6569% | 20.3332% |
| 2022-10-01 | Worlds | MAD Lions | Saigon Buffalo | 52.5772% | 57.7125% | 59.2599% | 60.2165% |
| 2022-10-01 | Worlds | Beyond Gaming | Detonation FocusMe | 41.7082% | 41.0110% | 42.8605% | 45.9096% |
| 2022-10-01 | Worlds | Evil Geniuses | Chief Esports Club | 60.0509% | 58.9565% | 61.0934% | 65.0137% |
| 2022-10-01 | Worlds | Royal Never Give Up | Isurus | 90.8188% | 94.4482% | 95.7062% | 96.7981% |
| 2022-10-01 | Worlds | Chief Esports Club | Beyond Gaming | 48.7412% | 50.9890% | 49.7462% | 47.2453% |
| 2022-10-01 | Worlds | Royal Never Give Up | Istanbul Wildcats | 80.5686% | 85.4874% | 88.1665% | 90.9414% |
| 2022-10-01 | Worlds | Isurus | DRX | 7.7212% | 6.7623% | 6.3080% | 5.8712% |
| 2022-10-02 | Worlds | Beyond Gaming | Fnatic | 40.0301% | 39.0262% | 37.1545% | 33.9300% |
| 2022-10-02 | Worlds | LOUD | Chief Esports Club | 65.5491% | 57.3076% | 54.8182% | 53.3004% |
| 2022-10-02 | Worlds | Detonation FocusMe | Evil Geniuses | 51.0991% | 50.6811% | 48.1604% | 43.8269% |
| 2022-10-02 | Worlds | Istanbul Wildcats | Isurus | 70.8154% | 74.6396% | 75.3908% | 75.6028% |
| 2022-10-02 | Worlds | DRX | MAD Lions | 70.3151% | 67.4560% | 66.3576% | 65.3648% |
| 2022-10-02 | Worlds | Royal Never Give Up | Saigon Buffalo | 75.8921% | 80.6610% | 82.9372% | 85.2937% |
| 2022-10-02 | Worlds | Evil Geniuses | Detonation FocusMe | 48.9009% | 49.3189% | 51.8396% | 56.1731% |
| 2022-10-02 | Worlds | LOUD | Evil Geniuses | 41.1435% | 36.1393% | 33.3338% | 30.1124% |
| 2022-10-03 | Worlds | MAD Lions | Saigon Buffalo | 59.9472% | 61.0643% | 61.3522% | 61.1942% |
| 2022-10-03 | Worlds | LOUD | Detonation FocusMe | 39.5025% | 35.7537% | 35.0770% | 35.2068% |
| 2022-10-04 | Worlds | Evil Geniuses | MAD Lions | 58.5854% | 55.5506% | 53.8916% | 52.4297% |
| 2022-10-04 | Worlds | Royal Never Give Up | Detonation FocusMe | 58.9977% | 66.7285% | 72.3310% | 78.8998% |
| 2022-10-07 | Worlds | Cloud9 | Fnatic | 65.2112% | 59.3788% | 54.6573% | 48.3775% |
| 2022-10-07 | Worlds | G2 Esports | DWG KIA | 30.9593% | 32.7315% | 33.6809% | 34.9955% |
| 2022-10-07 | Worlds | CTBC Flying Oyster | 100 Thieves | 48.4655% | 48.7869% | 49.9783% | 51.6339% |
| 2022-10-07 | Worlds | JD Gaming | Evil Geniuses | 67.4083% | 69.7912% | 71.7268% | 74.4613% |
| 2022-10-07 | Worlds | T1 | Edward Gaming | 54.5463% | 60.8868% | 62.5306% | 63.2090% |
| 2022-10-07 | Worlds | Gen.G eSports | Royal Never Give Up | 78.3000% | 77.4028% | 74.3215% | 69.0036% |
| 2022-10-08 | Worlds | Rogue | DRX | 33.0723% | 37.0533% | 38.9986% | 41.7159% |
| 2022-10-08 | Worlds | Evil Geniuses | G2 Esports | 58.0175% | 48.6241% | 44.8011% | 40.9819% |
| 2022-10-08 | Worlds | Fnatic | T1 | 29.2157% | 22.7874% | 20.7028% | 19.1802% |
| 2022-10-08 | Worlds | Edward Gaming | Cloud9 | 62.6342% | 68.5545% | 72.3088% | 76.7937% |
| 2022-10-08 | Worlds | Top Esports | GAM Esports | 79.0308% | 79.3321% | 78.9059% | 78.0659% |
| 2022-10-08 | Worlds | DWG KIA | JD Gaming | 40.0781% | 43.7525% | 44.6543% | 44.5057% |
| 2022-10-09 | Worlds | GAM Esports | Rogue | 32.2073% | 35.8044% | 37.3113% | 39.1760% |
| 2022-10-09 | Worlds | 100 Thieves | Gen.G eSports | 14.4079% | 12.4517% | 12.2611% | 12.4078% |
| 2022-10-09 | Worlds | Edward Gaming | Fnatic | 59.5978% | 64.6794% | 66.4202% | 68.2123% |
| 2022-10-09 | Worlds | Cloud9 | T1 | 34.3526% | 25.9485% | 21.5250% | 17.1320% |
| 2022-10-09 | Worlds | Royal Never Give Up | CTBC Flying Oyster | 64.5190% | 68.8927% | 71.5831% | 74.9340% |
| 2022-10-09 | Worlds | DRX | Top Esports | 29.0225% | 27.3343% | 26.7943% | 26.0299% |
| 2022-10-10 | Worlds | JD Gaming | G2 Esports | 75.9894% | 71.9237% | 70.4257% | 69.4194% |
| 2022-10-10 | Worlds | Rogue | Top Esports | 36.8111% | 31.7675% | 30.6952% | 29.9564% |
| 2022-10-10 | Worlds | DWG KIA | Evil Geniuses | 67.0554% | 70.0675% | 71.6810% | 73.3603% |
| 2022-10-10 | Worlds | 100 Thieves | Royal Never Give Up | 18.0445% | 19.4463% | 18.6273% | 16.9923% |
| 2022-10-10 | Worlds | Gen.G eSports | CTBC Flying Oyster | 82.1800% | 85.2963% | 85.4411% | 85.0413% |
| 2022-10-10 | Worlds | GAM Esports | DRX | 24.1074% | 29.2691% | 31.8468% | 35.3827% |
| 2022-10-13 | Worlds | Fnatic | Cloud9 | 64.0400% | 62.5464% | 63.7738% | 66.1319% |
| 2022-10-13 | Worlds | T1 | Fnatic | 64.2187% | 71.6790% | 74.4246% | 76.7649% |
| 2022-10-13 | Worlds | Cloud9 | Edward Gaming | 25.1164% | 24.1944% | 22.3712% | 19.6792% |
| 2022-10-13 | Worlds | Fnatic | Edward Gaming | 37.3948% | 34.7682% | 33.6573% | 32.3597% |
| 2022-10-13 | Worlds | T1 | Cloud9 | 76.1690% | 80.8671% | 83.6678% | 86.5793% |
| 2022-10-13 | Worlds | Edward Gaming | T1 | 48.2618% | 42.5717% | 40.3824% | 38.7509% |
| 2022-10-14 | Worlds | G2 Esports | Evil Geniuses | 56.7323% | 60.0319% | 61.8065% | 63.8253% |
| 2022-10-14 | Worlds | Evil Geniuses | JD Gaming | 17.4520% | 18.9846% | 19.1353% | 18.7582% |
| 2022-10-14 | Worlds | DWG KIA | G2 Esports | 69.3646% | 67.6103% | 66.8038% | 65.8000% |
| 2022-10-14 | Worlds | G2 Esports | JD Gaming | 21.7042% | 26.0337% | 27.6899% | 28.9460% |
| 2022-10-14 | Worlds | Evil Geniuses | DWG KIA | 25.1965% | 24.1822% | 23.4932% | 22.7552% |
| 2022-10-14 | Worlds | JD Gaming | DWG KIA | 61.4382% | 57.6469% | 56.4777% | 56.0605% |
| 2022-10-14 | Worlds | JD Gaming | DWG KIA | 61.4382% | 57.6469% | 56.4777% | 56.0605% |
| 2022-10-15 | Worlds | Rogue | GAM Esports | 74.6555% | 69.1361% | 66.9050% | 64.3170% |
| 2022-10-15 | Worlds | GAM Esports | Top Esports | 18.2270% | 17.1305% | 17.3131% | 18.0056% |
| 2022-10-15 | Worlds | DRX | Rogue | 59.8107% | 60.3326% | 59.6322% | 58.1531% |
| 2022-10-15 | Worlds | DRX | GAM Esports | 81.4256% | 77.3089% | 74.9144% | 71.4678% |
| 2022-10-15 | Worlds | Top Esports | Rogue | 60.3655% | 68.3502% | 70.2599% | 71.6430% |
| 2022-10-15 | Worlds | Top Esports | DRX | 50.5783% | 58.6756% | 61.5275% | 64.5143% |
| 2022-10-15 | Worlds | DRX | Rogue | 59.8107% | 60.3326% | 59.6322% | 58.1531% |
| 2022-10-16 | Worlds | 100 Thieves | CTBC Flying Oyster | 35.5733% | 38.5752% | 39.4630% | 40.2173% |
| 2022-10-16 | Worlds | CTBC Flying Oyster | Gen.G eSports | 12.3816% | 10.4933% | 10.5906% | 11.1305% |
| 2022-10-16 | Worlds | Royal Never Give Up | 100 Thieves | 84.1002% | 82.4416% | 82.9050% | 84.1146% |
| 2022-10-16 | Worlds | Gen.G eSports | 100 Thieves | 92.7621% | 93.1425% | 92.8319% | 92.2292% |
| 2022-10-16 | Worlds | CTBC Flying Oyster | Royal Never Give Up | 25.5067% | 25.3250% | 24.0304% | 21.9195% |
| 2022-10-16 | Worlds | Royal Never Give Up | Gen.G eSports | 29.2141% | 25.6885% | 27.2447% | 30.8505% |
| 2022-10-16 | Worlds | Gen.G eSports | Royal Never Give Up | 70.7859% | 74.3115% | 72.7553% | 69.1495% |
| 2022-10-20 | Worlds | JD Gaming | Rogue | 78.2315% | 77.2990% | 76.7311% | 76.0983% |
| 2022-10-21 | Worlds | T1 | Royal Never Give Up | 59.3230% | 60.7115% | 61.2050% | 61.3407% |
| 2022-10-22 | Worlds | Gen.G eSports | DWG KIA | 71.2824% | 73.7364% | 72.5569% | 70.1036% |
| 2022-10-23 | Worlds | DRX | Edward Gaming | 52.9366% | 50.5603% | 48.8198% | 46.2416% |
| 2022-10-29 | Worlds | T1 | JD Gaming | 50.5994% | 55.7805% | 58.5670% | 61.2199% |
| 2022-10-30 | Worlds | Gen.G eSports | DRX | 73.5226% | 78.3533% | 78.9762% | 78.6729% |
| 2022-11-05 | Worlds | T1 | DRX | 61.5573% | 63.6477% | 66.1304% | 69.3753% |


## S13 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-05-02 | MSI | PSG Talon | Detonation FocusMe | 27.6248% | 34.2776% | 37.9241% | 42.7777% |
| 2023-05-02 | MSI | G2 Esports | LOUD | 41.7086% | 55.0527% | 61.5393% | 68.8337% |
| 2023-05-03 | MSI | Bilibili Gaming | Movistar R7 | 90.0748% | 91.4158% | 92.0762% | 92.9332% |
| 2023-05-03 | MSI | Golden Guardians | GAM Esports | 42.4269% | 42.9027% | 42.1201% | 40.8810% |
| 2023-05-04 | MSI | Bilibili Gaming | Golden Guardians | 78.5190% | 79.3083% | 79.8211% | 80.6135% |
| 2023-05-04 | MSI | G2 Esports | PSG Talon | 40.6616% | 43.0687% | 44.7967% | 47.2838% |
| 2023-05-05 | MSI | GAM Esports | Movistar R7 | 62.6315% | 65.3063% | 67.0516% | 69.3466% |
| 2023-05-05 | MSI | LOUD | Detonation FocusMe | 39.2061% | 35.5008% | 34.3841% | 33.5572% |
| 2023-05-06 | MSI | Golden Guardians | Movistar R7 | 70.6808% | 71.8842% | 72.4410% | 73.2102% |
| 2023-05-06 | MSI | PSG Talon | LOUD | 46.9117% | 54.4298% | 57.9689% | 62.0338% |
| 2023-05-07 | MSI | Golden Guardians | PSG Talon | 47.5125% | 45.1600% | 44.8391% | 44.8531% |
| 2023-05-09 | MSI | Gen.G eSports | G2 Esports | 83.1803% | 82.2901% | 81.5950% | 80.6388% |
| 2023-05-10 | MSI | MAD Lions | T1 | 13.2300% | 11.6673% | 11.4010% | 11.2866% |
| 2023-05-11 | MSI | Cloud9 | Bilibili Gaming | 43.4073% | 47.1627% | 47.9047% | 48.1945% |
| 2023-05-12 | MSI | JD Gaming | Golden Guardians | 82.7827% | 85.0530% | 85.9078% | 86.8829% |
| 2023-05-13 | MSI | Gen.G eSports | T1 | 44.2959% | 43.1360% | 42.6154% | 42.0572% |
| 2023-05-13 | MSI | MAD Lions | G2 Esports | 38.7811% | 37.9976% | 37.7484% | 37.5379% |
| 2023-05-14 | MSI | JD Gaming | Bilibili Gaming | 67.2221% | 67.2859% | 67.4592% | 67.7236% |
| 2023-05-14 | MSI | Golden Guardians | Cloud9 | 49.9275% | 42.1596% | 39.7533% | 37.4623% |
| 2023-05-16 | MSI | G2 Esports | Bilibili Gaming | 31.9401% | 32.1874% | 32.2980% | 32.3536% |
| 2023-05-17 | MSI | Gen.G eSports | Cloud9 | 80.5742% | 79.6791% | 79.1294% | 78.4775% |
| 2023-05-18 | MSI | JD Gaming | T1 | 51.5283% | 47.0566% | 46.0855% | 45.5620% |
| 2023-05-19 | MSI | Bilibili Gaming | Gen.G eSports | 33.4574% | 34.0316% | 34.5545% | 35.2949% |
| 2023-05-20 | MSI | Bilibili Gaming | T1 | 42.3761% | 40.7304% | 40.3320% | 40.0718% |
| 2023-05-21 | MSI | JD Gaming | Bilibili Gaming | 66.6918% | 67.4052% | 67.6449% | 67.9230% |
| 2023-10-10 | Worlds | PSG Talon | Movistar R7 | 53.9255% | 63.9590% | 67.7248% | 70.7065% |
| 2023-10-10 | Worlds | LOUD | GAM Esports | 65.3658% | 64.3487% | 61.8480% | 58.6902% |
| 2023-10-11 | Worlds | Detonation FocusMe | CTBC Flying Oyster | 66.1923% | 65.5452% | 62.6230% | 57.2224% |
| 2023-10-11 | Worlds | Team BDS | Team Whales | 80.5933% | 82.3352% | 83.7962% | 86.1195% |
| 2023-10-12 | Worlds | PSG Talon | LOUD | 48.2644% | 56.8870% | 60.3764% | 63.8344% |
| 2023-10-12 | Worlds | CTBC Flying Oyster | Team Whales | 69.5888% | 71.4062% | 70.9274% | 70.0339% |
| 2023-10-13 | Worlds | Movistar R7 | GAM Esports | 44.0997% | 43.1396% | 41.8652% | 40.8146% |
| 2023-10-13 | Worlds | Detonation FocusMe | Team BDS | 41.7999% | 46.3721% | 43.5320% | 36.5660% |
| 2023-10-14 | Worlds | LOUD | GAM Esports | 57.7932% | 54.9212% | 52.6077% | 49.8074% |
| 2023-10-14 | Worlds | CTBC Flying Oyster | Team BDS | 45.0387% | 44.0917% | 41.9686% | 38.0296% |
| 2023-10-15 | Worlds | GAM Esports | Team Whales | 59.8795% | 61.6696% | 61.8497% | 62.0727% |
| 2023-10-15 | Worlds | PSG Talon | Team BDS | 58.5298% | 58.2257% | 56.4152% | 53.0252% |
| 2023-10-19 | Worlds | T1 | Team Liquid | 90.0040% | 89.9398% | 89.7286% | 89.4938% |
| 2023-10-19 | Worlds | Cloud9 | MAD Lions | 53.8543% | 54.6085% | 55.8341% | 58.2366% |
| 2023-10-19 | Worlds | Gen.G eSports | GAM Esports | 88.3847% | 89.3481% | 89.6698% | 90.3612% |
| 2023-10-19 | Worlds | Team BDS | JD Gaming | 19.4910% | 13.5148% | 11.7712% | 10.0631% |
| 2023-10-19 | Worlds | G2 Esports | Dplus KIA | 32.2009% | 39.8689% | 41.7985% | 42.7727% |
| 2023-10-19 | Worlds | Weibo Gaming | NRG | 81.6107% | 83.4867% | 84.2082% | 85.0027% |
| 2023-10-19 | Worlds | LNG Esports | Fnatic | 79.2848% | 81.1562% | 82.8324% | 85.5548% |
| 2023-10-19 | Worlds | Bilibili Gaming | KT Rolster | 30.6738% | 37.4183% | 41.3416% | 46.5727% |
| 2023-10-20 | Worlds | NRG | Team Liquid | 57.6130% | 57.4286% | 57.4126% | 57.6181% |
| 2023-10-20 | Worlds | Cloud9 | LNG Esports | 17.0671% | 16.3965% | 16.7793% | 17.4115% |
| 2023-10-20 | Worlds | MAD Lions | Team BDS | 29.1057% | 35.9396% | 39.0748% | 42.0956% |
| 2023-10-20 | Worlds | Fnatic | GAM Esports | 43.4860% | 49.5502% | 51.8206% | 54.1835% |
| 2023-10-20 | Worlds | Gen.G eSports | T1 | 70.8516% | 68.3874% | 66.0565% | 62.7922% |
| 2023-10-20 | Worlds | G2 Esports | Weibo Gaming | 44.3435% | 42.7417% | 40.4464% | 36.8246% |
| 2023-10-20 | Worlds | JD Gaming | Bilibili Gaming | 58.3507% | 62.7827% | 63.8720% | 64.8818% |
| 2023-10-20 | Worlds | Dplus KIA | KT Rolster | 36.2995% | 33.3698% | 33.2837% | 34.1335% |
| 2023-10-21 | Worlds | JD Gaming | LNG Esports | 63.6998% | 65.0337% | 65.3228% | 65.4323% |
| 2023-10-21 | Worlds | G2 Esports | Gen.G eSports | 30.7142% | 31.0991% | 31.0097% | 30.7249% |
| 2023-10-22 | Worlds | T1 | Cloud9 | 77.7235% | 78.6086% | 78.1361% | 77.0624% |
| 2023-10-22 | Worlds | NRG | MAD Lions | 43.1000% | 42.7371% | 42.7346% | 43.2955% |
| 2023-10-22 | Worlds | Bilibili Gaming | Fnatic | 79.5814% | 81.9817% | 83.3768% | 85.5057% |
| 2023-10-22 | Worlds | KT Rolster | Weibo Gaming | 69.3828% | 67.4707% | 64.6775% | 59.9582% |
| 2023-10-23 | Worlds | Team Liquid | GAM Esports | 30.6638% | 34.5300% | 37.6880% | 42.8185% |
| 2023-10-23 | Worlds | Dplus KIA | Team BDS | 73.0959% | 75.0950% | 75.1856% | 75.0116% |
| 2023-10-26 | Worlds | Cloud9 | Fnatic | 48.7965% | 50.6449% | 53.3091% | 58.0903% |
| 2023-10-26 | Worlds | MAD Lions | Weibo Gaming | 20.5547% | 18.4824% | 17.9493% | 17.1357% |
| 2023-10-27 | Worlds | Dplus KIA | GAM Esports | 81.7001% | 82.3947% | 82.8156% | 83.8119% |
| 2023-10-27 | Worlds | KT Rolster | LNG Esports | 60.2375% | 60.3478% | 58.2729% | 54.1213% |
| 2023-10-28 | Worlds | NRG | G2 Esports | 20.6467% | 19.7078% | 20.1425% | 21.1922% |
| 2023-10-28 | Worlds | T1 | Bilibili Gaming | 43.7696% | 42.1849% | 42.3461% | 42.7582% |
| 2023-10-29 | Worlds | KT Rolster | Dplus KIA | 61.4096% | 65.1538% | 65.7996% | 65.4919% |
| 2023-10-29 | Worlds | Fnatic | Weibo Gaming | 26.2585% | 22.9341% | 20.8857% | 17.9992% |
| 2023-10-29 | Worlds | G2 Esports | Bilibili Gaming | 32.2646% | 29.2254% | 28.2632% | 27.0330% |
| 2023-11-02 | Worlds | NRG | Weibo Gaming | 37.4663% | 27.1029% | 23.9194% | 20.9849% |
| 2023-11-03 | Worlds | Gen.G eSports | Bilibili Gaming | 80.8804% | 71.5413% | 67.1333% | 62.1707% |
| 2023-11-04 | Worlds | JD Gaming | KT Rolster | 58.4136% | 58.9937% | 60.2167% | 62.7792% |
| 2023-11-05 | Worlds | LNG Esports | T1 | 58.1315% | 59.2082% | 58.4666% | 57.5124% |
| 2023-11-11 | Worlds | Weibo Gaming | Bilibili Gaming | 37.9676% | 37.8180% | 38.7642% | 40.1827% |
| 2023-11-12 | Worlds | T1 | JD Gaming | 42.5617% | 34.6741% | 33.4874% | 32.8261% |
| 2023-11-19 | Worlds | Weibo Gaming | T1 | 28.2050% | 34.0867% | 35.9129% | 37.8234% |


## S14 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-05-01 | MSI | FlyQuest | PSG Talon | 24.0706% | 23.6738% | 24.8570% | 27.6384% |
| 2024-05-01 | MSI | T1 | Estral Esports | 88.0687% | 89.9564% | 90.3268% | 90.4802% |
| 2024-05-02 | MSI | Fnatic | GAM Esports | 36.8876% | 37.7182% | 39.3213% | 42.4797% |
| 2024-05-02 | MSI | Top Esports | LOUD | 83.1183% | 88.7933% | 91.2758% | 93.9714% |
| 2024-05-03 | MSI | T1 | FlyQuest | 84.4084% | 85.4168% | 85.7694% | 86.1807% |
| 2024-05-03 | MSI | Top Esports | Fnatic | 81.5845% | 84.1966% | 85.4323% | 87.0374% |
| 2024-05-04 | MSI | PSG Talon | Estral Esports | 66.2102% | 70.4403% | 70.5928% | 69.2110% |
| 2024-05-04 | MSI | LOUD | GAM Esports | 50.3610% | 44.9147% | 42.1380% | 38.5589% |
| 2024-05-05 | MSI | FlyQuest | PSG Talon | 40.6643% | 38.6034% | 38.7384% | 39.9232% |
| 2024-05-05 | MSI | Fnatic | GAM Esports | 61.8651% | 61.9692% | 63.1888% | 65.6330% |
| 2024-05-07 | MSI | Team Liquid | Top Esports | 18.5548% | 16.2479% | 15.0934% | 13.5717% |
| 2024-05-08 | MSI | Gen.G eSports | Fnatic | 85.8045% | 88.1815% | 88.8123% | 89.4088% |
| 2024-05-09 | MSI | Bilibili Gaming | PSG Talon | 78.1888% | 78.7407% | 79.8652% | 82.0223% |
| 2024-05-10 | MSI | G2 Esports | T1 | 21.4931% | 22.0378% | 22.2199% | 22.2944% |
| 2024-05-11 | MSI | Fnatic | Team Liquid | 67.1278% | 65.6159% | 65.1309% | 64.6066% |
| 2024-05-11 | MSI | Gen.G eSports | Top Esports | 70.5714% | 70.2157% | 69.6464% | 68.6230% |
| 2024-05-12 | MSI | G2 Esports | PSG Talon | 50.0348% | 49.2384% | 49.4984% | 50.4758% |
| 2024-05-12 | MSI | Bilibili Gaming | T1 | 49.1293% | 50.5427% | 51.2617% | 52.2361% |
| 2024-05-14 | MSI | Top Esports | G2 Esports | 58.5596% | 60.4009% | 61.4274% | 62.9118% |
| 2024-05-15 | MSI | T1 | Team Liquid | 82.2901% | 83.7575% | 84.2925% | 84.8780% |
| 2024-05-16 | MSI | Gen.G eSports | Bilibili Gaming | 55.9917% | 56.1659% | 55.9148% | 55.3974% |
| 2024-05-17 | MSI | T1 | G2 Esports | 49.7859% | 53.3666% | 54.6594% | 56.0691% |
| 2024-05-18 | MSI | Bilibili Gaming | T1 | 45.7206% | 47.0821% | 47.6376% | 48.3227% |
| 2024-05-19 | MSI | Gen.G eSports | Bilibili Gaming | 61.1837% | 60.8181% | 60.5053% | 60.0173% |
| 2024-09-25 | Worlds | MAD Lions KOI | Vikings Esports | 29.4681% | 35.7655% | 42.4283% | 53.0996% |
| 2024-09-25 | Worlds | PSG Talon | paiN Gaming | 71.4844% | 79.7065% | 83.1528% | 86.8192% |
| 2024-09-26 | Worlds | GAM Esports | SoftBank Hawks Gaming | 46.9462% | 39.2184% | 36.1970% | 32.8632% |
| 2024-09-26 | Worlds | 100 Thieves | Movistar R7 | 48.7366% | 60.0743% | 64.6131% | 69.2226% |
| 2024-09-27 | Worlds | MAD Lions KOI | PSG Talon | 27.6366% | 24.5907% | 25.1436% | 26.9398% |
| 2024-09-27 | Worlds | GAM Esports | Movistar R7 | 74.2088% | 73.1794% | 71.1513% | 67.3488% |
| 2024-09-28 | Worlds | paiN Gaming | Vikings Esports | 52.9331% | 47.7849% | 45.0162% | 42.2242% |
| 2024-09-28 | Worlds | SoftBank Hawks Gaming | 100 Thieves | 65.5819% | 67.1246% | 65.8995% | 62.9292% |
| 2024-09-29 | Worlds | paiN Gaming | Movistar R7 | 75.7765% | 75.8626% | 73.4900% | 68.8712% |
| 2024-09-29 | Worlds | PSG Talon | 100 Thieves | 75.5523% | 76.8188% | 76.2570% | 74.7715% |
| 2024-10-03 | Worlds | Bilibili Gaming | MAD Lions KOI | 78.9725% | 83.5539% | 85.1354% | 86.5106% |
| 2024-10-03 | Worlds | Top Esports | T1 | 55.4681% | 55.7923% | 54.7382% | 53.2352% |
| 2024-10-03 | Worlds | Gen.G eSports | Weibo Gaming | 84.9985% | 86.7775% | 87.5268% | 88.2026% |
| 2024-10-03 | Worlds | Fnatic | Dplus KIA | 29.3276% | 29.0046% | 29.2906% | 30.0585% |
| 2024-10-03 | Worlds | Team Liquid | LNG Esports | 34.6078% | 38.2663% | 40.0437% | 41.7588% |
| 2024-10-03 | Worlds | Hanwha Life eSports | PSG Talon | 80.1601% | 81.0522% | 81.4503% | 81.8737% |
| 2024-10-03 | Worlds | GAM Esports | FlyQuest | 59.1160% | 48.5569% | 43.2301% | 36.7679% |
| 2024-10-03 | Worlds | G2 Esports | paiN Gaming | 60.4967% | 69.8539% | 75.4225% | 81.7075% |
| 2024-10-04 | Worlds | Bilibili Gaming | LNG Esports | 68.2450% | 68.9092% | 70.3499% | 72.5507% |
| 2024-10-04 | Worlds | Gen.G eSports | Top Esports | 70.6773% | 71.3614% | 71.4324% | 71.2678% |
| 2024-10-04 | Worlds | G2 Esports | Hanwha Life eSports | 20.6739% | 22.1529% | 23.5245% | 25.5545% |
| 2024-10-04 | Worlds | Team Liquid | Weibo Gaming | 35.1091% | 39.5961% | 41.5666% | 43.3293% |
| 2024-10-04 | Worlds | T1 | paiN Gaming | 73.6957% | 80.6505% | 84.6265% | 88.9215% |
| 2024-10-04 | Worlds | Dplus KIA | FlyQuest | 72.0568% | 74.5853% | 74.7592% | 74.1116% |
| 2024-10-04 | Worlds | Fnatic | GAM Esports | 47.9785% | 57.8689% | 62.5914% | 68.0199% |
| 2024-10-04 | Worlds | PSG Talon | MAD Lions KOI | 57.4261% | 63.4455% | 64.7948% | 65.0287% |
| 2024-10-05 | Worlds | Dplus KIA | LNG Esports | 52.9461% | 56.4105% | 57.7312% | 58.7893% |
| 2024-10-05 | Worlds | Hanwha Life eSports | Gen.G eSports | 41.0420% | 38.6586% | 37.5942% | 36.3855% |
| 2024-10-06 | Worlds | Top Esports | Fnatic | 82.0769% | 82.9191% | 82.8854% | 82.7892% |
| 2024-10-06 | Worlds | Bilibili Gaming | T1 | 63.6421% | 61.7840% | 60.4169% | 58.8795% |
| 2024-10-06 | Worlds | FlyQuest | PSG Talon | 38.3392% | 37.9767% | 38.7355% | 40.2944% |
| 2024-10-06 | Worlds | G2 Esports | Weibo Gaming | 42.7588% | 47.0937% | 50.0037% | 53.6815% |
| 2024-10-07 | Worlds | MAD Lions KOI | GAM Esports | 52.2512% | 53.5188% | 55.3856% | 59.0489% |
| 2024-10-07 | Worlds | Team Liquid | paiN Gaming | 51.4970% | 60.6954% | 65.8478% | 71.9877% |
| 2024-10-10 | Worlds | Top Esports | Dplus KIA | 60.3292% | 62.2195% | 62.8882% | 63.9653% |
| 2024-10-10 | Worlds | Hanwha Life eSports | FlyQuest | 86.6186% | 87.1479% | 87.0945% | 86.7872% |
| 2024-10-11 | Worlds | G2 Esports | T1 | 39.8992% | 39.1377% | 38.2965% | 37.2145% |
| 2024-10-11 | Worlds | Bilibili Gaming | PSG Talon | 76.5148% | 77.8636% | 78.6935% | 80.0245% |
| 2024-10-12 | Worlds | Fnatic | Weibo Gaming | 29.4090% | 31.5217% | 33.1665% | 35.1753% |
| 2024-10-12 | Worlds | Team Liquid | GAM Esports | 60.3615% | 65.8491% | 68.5411% | 71.7342% |
| 2024-10-13 | Worlds | Dplus KIA | Weibo Gaming | 55.6810% | 56.6801% | 57.6669% | 58.6682% |
| 2024-10-13 | Worlds | G2 Esports | Bilibili Gaming | 24.4546% | 25.4799% | 26.1814% | 26.9349% |
| 2024-10-13 | Worlds | FlyQuest | Team Liquid | 52.4685% | 48.4523% | 47.3235% | 46.6977% |
| 2024-10-17 | Worlds | Weibo Gaming | LNG Esports | 33.2524% | 38.5960% | 40.4778% | 42.3727% |
| 2024-10-18 | Worlds | Hanwha Life eSports | Bilibili Gaming | 61.5388% | 57.2506% | 55.4524% | 53.2905% |
| 2024-10-19 | Worlds | Top Esports | T1 | 64.1844% | 63.8869% | 62.3485% | 59.9434% |
| 2024-10-20 | Worlds | Gen.G eSports | FlyQuest | 85.9244% | 88.9249% | 89.8741% | 90.6594% |
| 2024-10-26 | Worlds | Weibo Gaming | Bilibili Gaming | 32.6864% | 30.1134% | 28.5258% | 26.3425% |
| 2024-10-27 | Worlds | T1 | Gen.G eSports | 38.3782% | 31.1825% | 29.8494% | 29.3612% |
| 2024-11-02 | Worlds | T1 | Bilibili Gaming | 44.6635% | 42.2073% | 42.2590% | 42.7212% |


## S15 逐场小局概率

全部为 A 队赢下一小局的概率，均使用赛区先验。

| 日期 | 赛事 | A 队 | B 队 | 30 天 | 60 天 | 90 天 | 180 天 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-06-27 | MSI | FURIA | G2 Esports | 45.9034% | 34.1657% | 28.7523% | 22.9965% |
| 2025-06-27 | MSI | Bilibili Gaming | GAM Esports | 78.7407% | 76.0899% | 73.7669% | 70.5476% |
| 2025-06-28 | MSI | GAM Esports | FURIA | 48.1119% | 53.2541% | 55.7971% | 59.0055% |
| 2025-06-28 | MSI | Bilibili Gaming | G2 Esports | 80.0479% | 76.8195% | 73.9520% | 69.7148% |
| 2025-06-29 | MSI | G2 Esports | GAM Esports | 50.4243% | 53.0720% | 54.6075% | 56.5806% |
| 2025-07-01 | MSI | Gen.G eSports | G2 Esports | 87.4596% | 88.6982% | 88.8153% | 88.7112% |
| 2025-07-02 | MSI | Anyone s Legend | FlyQuest | 60.9636% | 56.5497% | 54.0510% | 51.0386% |
| 2025-07-03 | MSI | Movistar KOI | Bilibili Gaming | 18.7471% | 20.7630% | 22.5471% | 25.2273% |
| 2025-07-03 | MSI | CTBC Flying Oyster | T1 | 32.8218% | 34.3532% | 34.2004% | 33.7439% |
| 2025-07-04 | MSI | FlyQuest | G2 Esports | 71.6933% | 71.4845% | 70.9838% | 70.1665% |
| 2025-07-04 | MSI | Anyone s Legend | Gen.G eSports | 53.9419% | 45.6980% | 41.7738% | 37.3392% |
| 2025-07-05 | MSI | CTBC Flying Oyster | Movistar KOI | 54.8831% | 59.5629% | 61.6750% | 63.8701% |
| 2025-07-05 | MSI | Bilibili Gaming | T1 | 63.5834% | 59.0130% | 55.4163% | 50.4590% |
| 2025-07-07 | MSI | CTBC Flying Oyster | Anyone s Legend | 29.8946% | 31.1338% | 32.9667% | 35.8386% |
| 2025-07-08 | MSI | FlyQuest | Bilibili Gaming | 48.8472% | 49.0762% | 49.8069% | 51.0804% |
| 2025-07-09 | MSI | T1 | Gen.G eSports | 42.0262% | 37.7951% | 37.2930% | 37.3817% |
| 2025-07-10 | MSI | Anyone s Legend | Bilibili Gaming | 57.2118% | 56.1280% | 55.8840% | 55.7593% |
| 2025-07-11 | MSI | T1 | Anyone s Legend | 44.5571% | 46.2795% | 48.0896% | 50.8695% |
| 2025-07-12 | MSI | Gen.G eSports | T1 | 57.4001% | 60.7580% | 61.4936% | 61.7930% |
| 2025-10-14 | Worlds | Invictus Gaming | T1 | 48.4879% | 45.7692% | 43.2460% | 39.6545% |
| 2025-10-15 | Worlds | Team Secret Whales | Vivo Keyd Stars | 42.0735% | 47.6018% | 50.8262% | 55.0008% |
| 2025-10-15 | Worlds | CTBC Flying Oyster | Fnatic | 66.2874% | 63.8672% | 62.6317% | 61.4591% |
| 2025-10-15 | Worlds | KT Rolster | Movistar KOI | 64.5080% | 64.1430% | 63.4556% | 62.6807% |
| 2025-10-15 | Worlds | Bilibili Gaming | 100 Thieves | 75.3834% | 79.3733% | 79.7319% | 79.1705% |
| 2025-10-15 | Worlds | FlyQuest | T1 | 42.2737% | 37.6155% | 36.5194% | 35.7625% |
| 2025-10-15 | Worlds | Hanwha Life eSports | Anyone s Legend | 57.0369% | 54.7024% | 55.0464% | 56.5151% |
| 2025-10-15 | Worlds | G2 Esports | Top Esports | 39.9670% | 34.1406% | 33.2666% | 33.2069% |
| 2025-10-15 | Worlds | Gen.G eSports | PSG Talon | 92.9975% | 93.4753% | 93.1278% | 92.3286% |
| 2025-10-16 | Worlds | Vivo Keyd Stars | FlyQuest | 25.8382% | 22.6935% | 21.1174% | 19.1773% |
| 2025-10-16 | Worlds | KT Rolster | Team Secret Whales | 66.8669% | 71.1320% | 72.0465% | 72.4620% |
| 2025-10-16 | Worlds | Movistar KOI | G2 Esports | 30.7528% | 36.2971% | 38.8941% | 41.4331% |
| 2025-10-16 | Worlds | Top Esports | 100 Thieves | 75.4475% | 79.2349% | 79.6439% | 79.2796% |
| 2025-10-16 | Worlds | CTBC Flying Oyster | T1 | 35.4530% | 31.6089% | 30.9472% | 30.8476% |
| 2025-10-16 | Worlds | Gen.G eSports | Anyone s Legend | 65.5315% | 65.5248% | 65.7366% | 66.2822% |
| 2025-10-16 | Worlds | Bilibili Gaming | Fnatic | 81.0659% | 79.4520% | 77.5609% | 74.6446% |
| 2025-10-16 | Worlds | Hanwha Life eSports | PSG Talon | 86.5953% | 88.3464% | 88.3784% | 87.9908% |
| 2025-10-17 | Worlds | CTBC Flying Oyster | Anyone s Legend | 40.0104% | 34.7926% | 33.9418% | 34.2464% |
| 2025-10-17 | Worlds | KT Rolster | Top Esports | 32.0502% | 33.1327% | 34.3048% | 36.0423% |
| 2025-10-18 | Worlds | Bilibili Gaming | G2 Esports | 61.5046% | 65.3406% | 66.2170% | 66.3686% |
| 2025-10-18 | Worlds | Gen.G eSports | T1 | 62.2586% | 62.5510% | 62.5537% | 62.3791% |
| 2025-10-18 | Worlds | FlyQuest | Team Secret Whales | 72.0037% | 74.1240% | 74.6425% | 74.9653% |
| 2025-10-18 | Worlds | Hanwha Life eSports | 100 Thieves | 80.0658% | 83.2833% | 84.2617% | 85.0928% |
| 2025-10-19 | Worlds | PSG Talon | Vivo Keyd Stars | 42.1704% | 45.6594% | 48.9822% | 54.0611% |
| 2025-10-19 | Worlds | Movistar KOI | Fnatic | 54.3200% | 53.4742% | 52.5684% | 51.2497% |
| 2025-10-22 | Worlds | CTBC Flying Oyster | Hanwha Life eSports | 35.2043% | 31.2733% | 29.8736% | 28.6301% |
| 2025-10-22 | Worlds | FlyQuest | G2 Esports | 53.2080% | 56.9521% | 58.4330% | 59.8801% |
| 2025-10-23 | Worlds | Movistar KOI | Team Secret Whales | 54.2183% | 59.2540% | 61.0424% | 62.3764% |
| 2025-10-23 | Worlds | Gen.G eSports | Top Esports | 70.9125% | 70.5849% | 70.6477% | 70.9353% |
| 2025-10-24 | Worlds | Bilibili Gaming | Vivo Keyd Stars | 77.4647% | 81.5448% | 82.7356% | 83.7169% |
| 2025-10-24 | Worlds | 100 Thieves | T1 | 18.8694% | 15.7784% | 15.2448% | 15.1322% |
| 2025-10-25 | Worlds | CTBC Flying Oyster | FlyQuest | 48.3222% | 47.1487% | 46.6932% | 46.3293% |
| 2025-10-25 | Worlds | Top Esports | Bilibili Gaming | 52.4603% | 51.7466% | 51.5645% | 51.5435% |
| 2025-10-25 | Worlds | Movistar KOI | T1 | 17.0968% | 17.7169% | 18.4383% | 19.3230% |
| 2025-10-28 | Worlds | Gen.G eSports | Hanwha Life eSports | 60.5478% | 61.5549% | 61.3294% | 60.4853% |
| 2025-10-29 | Worlds | KT Rolster | CTBC Flying Oyster | 59.5311% | 58.0787% | 57.4545% | 56.4160% |
| 2025-10-30 | Worlds | Top Esports | G2 Esports | 57.2258% | 62.6387% | 64.3773% | 65.4255% |
| 2025-10-31 | Worlds | Anyone s Legend | T1 | 44.3236% | 43.0136% | 42.8194% | 42.3997% |
| 2025-11-01 | Worlds | Gen.G eSports | KT Rolster | 69.4319% | 73.3989% | 74.5304% | 75.4630% |
| 2025-11-02 | Worlds | T1 | Top Esports | 59.6221% | 60.7084% | 61.1845% | 61.7930% |
| 2025-11-09 | Worlds | KT Rolster | T1 | 52.5307% | 44.2306% | 41.2968% | 38.5098% |


## 对照使用的上一季赛区先验

以下为 logistic 强度，不是胜率。

### 用于 S4

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 44 | 54 | 2013-10-04 | CIS | -0.807230 |
| 30 | 44 | 54 | 2013-10-04 | CN | 1.014122 |
| 30 | 44 | 54 | 2013-10-04 | EU | 0.647743 |
| 30 | 44 | 54 | 2013-10-04 | KR | 1.405251 |
| 30 | 44 | 54 | 2013-10-04 | LMS | -0.435012 |
| 30 | 44 | 54 | 2013-10-04 | NA | -0.363898 |
| 30 | 44 | 54 | 2013-10-04 | SEA | -1.460975 |
| 30 | 44 | 54 | 2013-10-04 | PCS | -1.255782 |
| 30 | 44 | 54 | 2013-10-04 | VN | -1.460975 |
| 60 | 44 | 54 | 2013-10-04 | CIS | -0.849257 |
| 60 | 44 | 54 | 2013-10-04 | CN | 1.115800 |
| 60 | 44 | 54 | 2013-10-04 | EU | 0.691669 |
| 60 | 44 | 54 | 2013-10-04 | KR | 1.414058 |
| 60 | 44 | 54 | 2013-10-04 | LMS | -0.470086 |
| 60 | 44 | 54 | 2013-10-04 | NA | -0.340376 |
| 60 | 44 | 54 | 2013-10-04 | SEA | -1.561807 |
| 60 | 44 | 54 | 2013-10-04 | PCS | -1.343462 |
| 60 | 44 | 54 | 2013-10-04 | VN | -1.561807 |
| 90 | 44 | 54 | 2013-10-04 | CIS | -0.863079 |
| 90 | 44 | 54 | 2013-10-04 | CN | 1.150174 |
| 90 | 44 | 54 | 2013-10-04 | EU | 0.706025 |
| 90 | 44 | 54 | 2013-10-04 | KR | 1.416910 |
| 90 | 44 | 54 | 2013-10-04 | LMS | -0.482221 |
| 90 | 44 | 54 | 2013-10-04 | NA | -0.331998 |
| 90 | 44 | 54 | 2013-10-04 | SEA | -1.595811 |
| 90 | 44 | 54 | 2013-10-04 | PCS | -1.373093 |
| 90 | 44 | 54 | 2013-10-04 | VN | -1.595811 |
| 180 | 44 | 54 | 2013-10-04 | CIS | -0.876802 |
| 180 | 44 | 54 | 2013-10-04 | CN | 1.184779 |
| 180 | 44 | 54 | 2013-10-04 | EU | 0.720232 |
| 180 | 44 | 54 | 2013-10-04 | KR | 1.419729 |
| 180 | 44 | 54 | 2013-10-04 | LMS | -0.494576 |
| 180 | 44 | 54 | 2013-10-04 | NA | -0.323363 |
| 180 | 44 | 54 | 2013-10-04 | SEA | -1.629999 |
| 180 | 44 | 54 | 2013-10-04 | PCS | -1.402915 |
| 180 | 44 | 54 | 2013-10-04 | VN | -1.629999 |


### 用于 S5

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 54 | 65 | 2014-10-19 | BR | -0.641829 |
| 30 | 54 | 65 | 2014-10-19 | CN | 0.778131 |
| 30 | 54 | 65 | 2014-10-19 | EU | -0.038759 |
| 30 | 54 | 65 | 2014-10-19 | KR | 1.140670 |
| 30 | 54 | 65 | 2014-10-19 | LMS | -0.389739 |
| 30 | 54 | 65 | 2014-10-19 | NA | 0.267729 |
| 30 | 54 | 65 | 2014-10-19 | TR | -1.116203 |
| 30 | 54 | 65 | 2014-10-19 | PCS | -0.389739 |
| 60 | 54 | 65 | 2014-10-19 | BR | -0.684973 |
| 60 | 54 | 65 | 2014-10-19 | CN | 0.851422 |
| 60 | 54 | 65 | 2014-10-19 | EU | -0.010942 |
| 60 | 54 | 65 | 2014-10-19 | KR | 1.228577 |
| 60 | 54 | 65 | 2014-10-19 | LMS | -0.410503 |
| 60 | 54 | 65 | 2014-10-19 | NA | 0.343645 |
| 60 | 54 | 65 | 2014-10-19 | TR | -1.317226 |
| 60 | 54 | 65 | 2014-10-19 | PCS | -0.410503 |
| 90 | 54 | 65 | 2014-10-19 | BR | -0.697635 |
| 90 | 54 | 65 | 2014-10-19 | CN | 0.874212 |
| 90 | 54 | 65 | 2014-10-19 | EU | -0.001104 |
| 90 | 54 | 65 | 2014-10-19 | KR | 1.258762 |
| 90 | 54 | 65 | 2014-10-19 | LMS | -0.416434 |
| 90 | 54 | 65 | 2014-10-19 | NA | 0.369541 |
| 90 | 54 | 65 | 2014-10-19 | TR | -1.387342 |
| 90 | 54 | 65 | 2014-10-19 | PCS | -0.416434 |
| 180 | 54 | 65 | 2014-10-19 | BR | -0.709402 |
| 180 | 54 | 65 | 2014-10-19 | CN | 0.896187 |
| 180 | 54 | 65 | 2014-10-19 | EU | 0.008935 |
| 180 | 54 | 65 | 2014-10-19 | KR | 1.289357 |
| 180 | 54 | 65 | 2014-10-19 | LMS | -0.421863 |
| 180 | 54 | 65 | 2014-10-19 | NA | 0.395640 |
| 180 | 54 | 65 | 2014-10-19 | TR | -1.458854 |
| 180 | 54 | 65 | 2014-10-19 | PCS | -0.421863 |


### 用于 S6

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 72 | 93 | 2015-10-25 | BR | -0.231411 |
| 30 | 72 | 93 | 2015-10-25 | CN | -0.232677 |
| 30 | 72 | 93 | 2015-10-25 | EU | 0.373411 |
| 30 | 72 | 93 | 2015-10-25 | KR | 1.838440 |
| 30 | 72 | 93 | 2015-10-25 | LMS | 0.085578 |
| 30 | 72 | 93 | 2015-10-25 | NA | -0.521712 |
| 30 | 72 | 93 | 2015-10-25 | SEA | -1.229254 |
| 30 | 72 | 93 | 2015-10-25 | TR | -0.082375 |
| 30 | 72 | 93 | 2015-10-25 | PCS | -0.146451 |
| 30 | 72 | 93 | 2015-10-25 | VN | -1.229254 |
| 60 | 72 | 93 | 2015-10-25 | BR | -0.223642 |
| 60 | 72 | 93 | 2015-10-25 | CN | -0.006419 |
| 60 | 72 | 93 | 2015-10-25 | EU | 0.468059 |
| 60 | 72 | 93 | 2015-10-25 | KR | 1.795434 |
| 60 | 72 | 93 | 2015-10-25 | LMS | 0.134938 |
| 60 | 72 | 93 | 2015-10-25 | NA | -0.420976 |
| 60 | 72 | 93 | 2015-10-25 | SEA | -1.295633 |
| 60 | 72 | 93 | 2015-10-25 | TR | -0.451761 |
| 60 | 72 | 93 | 2015-10-25 | PCS | -0.117515 |
| 60 | 72 | 93 | 2015-10-25 | VN | -1.295633 |
| 90 | 72 | 93 | 2015-10-25 | BR | -0.219041 |
| 90 | 72 | 93 | 2015-10-25 | CN | 0.156853 |
| 90 | 72 | 93 | 2015-10-25 | EU | 0.521751 |
| 90 | 72 | 93 | 2015-10-25 | KR | 1.766036 |
| 90 | 72 | 93 | 2015-10-25 | LMS | 0.153893 |
| 90 | 72 | 93 | 2015-10-25 | NA | -0.380163 |
| 90 | 72 | 93 | 2015-10-25 | SEA | -1.291751 |
| 90 | 72 | 93 | 2015-10-25 | TR | -0.707578 |
| 90 | 72 | 93 | 2015-10-25 | PCS | -0.101221 |
| 90 | 72 | 93 | 2015-10-25 | VN | -1.291751 |
| 180 | 72 | 93 | 2015-10-25 | BR | -0.217954 |
| 180 | 72 | 93 | 2015-10-25 | CN | 0.381669 |
| 180 | 72 | 93 | 2015-10-25 | EU | 0.584332 |
| 180 | 72 | 93 | 2015-10-25 | KR | 1.728772 |
| 180 | 72 | 93 | 2015-10-25 | LMS | 0.171211 |
| 180 | 72 | 93 | 2015-10-25 | NA | -0.348270 |
| 180 | 72 | 93 | 2015-10-25 | SEA | -1.272567 |
| 180 | 72 | 93 | 2015-10-25 | TR | -1.027192 |
| 180 | 72 | 93 | 2015-10-25 | PCS | -0.083574 |
| 180 | 72 | 93 | 2015-10-25 | VN | -1.272567 |


### 用于 S7

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 88 | 108 | 2016-10-23 | BR | -1.014038 |
| 30 | 88 | 108 | 2016-10-23 | CIS | -0.207956 |
| 30 | 88 | 108 | 2016-10-23 | CN | 0.089117 |
| 30 | 88 | 108 | 2016-10-23 | EU | -0.078688 |
| 30 | 88 | 108 | 2016-10-23 | KR | 1.413073 |
| 30 | 88 | 108 | 2016-10-23 | LMS | -0.216409 |
| 30 | 88 | 108 | 2016-10-23 | NA | 0.139803 |
| 30 | 88 | 108 | 2016-10-23 | TR | -0.124902 |
| 30 | 88 | 108 | 2016-10-23 | PCS | -0.216409 |
| 60 | 88 | 108 | 2016-10-23 | BR | -1.030327 |
| 60 | 88 | 108 | 2016-10-23 | CIS | -0.107724 |
| 60 | 88 | 108 | 2016-10-23 | CN | 0.203309 |
| 60 | 88 | 108 | 2016-10-23 | EU | -0.096811 |
| 60 | 88 | 108 | 2016-10-23 | KR | 1.450104 |
| 60 | 88 | 108 | 2016-10-23 | LMS | -0.120088 |
| 60 | 88 | 108 | 2016-10-23 | NA | 0.271434 |
| 60 | 88 | 108 | 2016-10-23 | TR | -0.569895 |
| 60 | 88 | 108 | 2016-10-23 | PCS | -0.120088 |
| 90 | 88 | 108 | 2016-10-23 | BR | -1.021920 |
| 90 | 88 | 108 | 2016-10-23 | CIS | -0.076853 |
| 90 | 88 | 108 | 2016-10-23 | CN | 0.280316 |
| 90 | 88 | 108 | 2016-10-23 | EU | -0.121171 |
| 90 | 88 | 108 | 2016-10-23 | KR | 1.462721 |
| 90 | 88 | 108 | 2016-10-23 | LMS | -0.055506 |
| 90 | 88 | 108 | 2016-10-23 | NA | 0.339586 |
| 90 | 88 | 108 | 2016-10-23 | TR | -0.807173 |
| 90 | 88 | 108 | 2016-10-23 | PCS | -0.055506 |
| 180 | 88 | 108 | 2016-10-23 | BR | -1.010939 |
| 180 | 88 | 108 | 2016-10-23 | CIS | -0.057380 |
| 180 | 88 | 108 | 2016-10-23 | CN | 0.382048 |
| 180 | 88 | 108 | 2016-10-23 | EU | -0.173662 |
| 180 | 88 | 108 | 2016-10-23 | KR | 1.467644 |
| 180 | 88 | 108 | 2016-10-23 | LMS | 0.024031 |
| 180 | 88 | 108 | 2016-10-23 | NA | 0.418622 |
| 180 | 88 | 108 | 2016-10-23 | TR | -1.050364 |
| 180 | 88 | 108 | 2016-10-23 | PCS | 0.024031 |


### 用于 S8

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 147 | 191 | 2017-10-29 | BR | -0.590340 |
| 30 | 147 | 191 | 2017-10-29 | CIS | -0.864003 |
| 30 | 147 | 191 | 2017-10-29 | CN | 1.283146 |
| 30 | 147 | 191 | 2017-10-29 | EU | 0.839907 |
| 30 | 147 | 191 | 2017-10-29 | JP | -1.082520 |
| 30 | 147 | 191 | 2017-10-29 | KR | 1.747624 |
| 30 | 147 | 191 | 2017-10-29 | LAN | -0.388734 |
| 30 | 147 | 191 | 2017-10-29 | LAS | -0.366542 |
| 30 | 147 | 191 | 2017-10-29 | LMS | -0.189954 |
| 30 | 147 | 191 | 2017-10-29 | NA | 0.568653 |
| 30 | 147 | 191 | 2017-10-29 | OCE | -0.747296 |
| 30 | 147 | 191 | 2017-10-29 | SEA | -0.079733 |
| 30 | 147 | 191 | 2017-10-29 | TR | -0.130208 |
| 30 | 147 | 191 | 2017-10-29 | PCS | -0.133393 |
| 30 | 147 | 191 | 2017-10-29 | VN | -0.079733 |
| 30 | 147 | 191 | 2017-10-29 | LATAM | -0.379086 |
| 30 | 147 | 191 | 2017-10-29 | LCP | -1.082520 |
| 60 | 147 | 191 | 2017-10-29 | BR | -0.653982 |
| 60 | 147 | 191 | 2017-10-29 | CIS | -1.061035 |
| 60 | 147 | 191 | 2017-10-29 | CN | 1.438072 |
| 60 | 147 | 191 | 2017-10-29 | EU | 0.982162 |
| 60 | 147 | 191 | 2017-10-29 | JP | -1.378895 |
| 60 | 147 | 191 | 2017-10-29 | KR | 1.929231 |
| 60 | 147 | 191 | 2017-10-29 | LAN | -0.366675 |
| 60 | 147 | 191 | 2017-10-29 | LAS | -0.542324 |
| 60 | 147 | 191 | 2017-10-29 | LMS | -0.050709 |
| 60 | 147 | 191 | 2017-10-29 | NA | 0.704908 |
| 60 | 147 | 191 | 2017-10-29 | OCE | -0.957363 |
| 60 | 147 | 191 | 2017-10-29 | SEA | 0.072377 |
| 60 | 147 | 191 | 2017-10-29 | TR | -0.115767 |
| 60 | 147 | 191 | 2017-10-29 | PCS | 0.012453 |
| 60 | 147 | 191 | 2017-10-29 | VN | 0.072377 |
| 60 | 147 | 191 | 2017-10-29 | LATAM | -0.443044 |
| 60 | 147 | 191 | 2017-10-29 | LCP | -1.378895 |
| 90 | 147 | 191 | 2017-10-29 | BR | -0.673618 |
| 90 | 147 | 191 | 2017-10-29 | CIS | -1.102832 |
| 90 | 147 | 191 | 2017-10-29 | CN | 1.494072 |
| 90 | 147 | 191 | 2017-10-29 | EU | 1.041039 |
| 90 | 147 | 191 | 2017-10-29 | JP | -1.521744 |
| 90 | 147 | 191 | 2017-10-29 | KR | 2.007013 |
| 90 | 147 | 191 | 2017-10-29 | LAN | -0.326195 |
| 90 | 147 | 191 | 2017-10-29 | LAS | -0.676656 |
| 90 | 147 | 191 | 2017-10-29 | LMS | 0.047313 |
| 90 | 147 | 191 | 2017-10-29 | NA | 0.750530 |
| 90 | 147 | 191 | 2017-10-29 | OCE | -1.058623 |
| 90 | 147 | 191 | 2017-10-29 | SEA | 0.151356 |
| 90 | 147 | 191 | 2017-10-29 | TR | -0.131654 |
| 90 | 147 | 191 | 2017-10-29 | PCS | 0.100703 |
| 90 | 147 | 191 | 2017-10-29 | VN | 0.151356 |
| 90 | 147 | 191 | 2017-10-29 | LATAM | -0.478569 |
| 90 | 147 | 191 | 2017-10-29 | LCP | -1.521744 |
| 180 | 147 | 191 | 2017-10-29 | BR | -0.697474 |
| 180 | 147 | 191 | 2017-10-29 | CIS | -1.127067 |
| 180 | 147 | 191 | 2017-10-29 | CN | 1.556466 |
| 180 | 147 | 191 | 2017-10-29 | EU | 1.113768 |
| 180 | 147 | 191 | 2017-10-29 | JP | -1.704502 |
| 180 | 147 | 191 | 2017-10-29 | KR | 2.104722 |
| 180 | 147 | 191 | 2017-10-29 | LAN | -0.265299 |
| 180 | 147 | 191 | 2017-10-29 | LAS | -0.864034 |
| 180 | 147 | 191 | 2017-10-29 | LMS | 0.190420 |
| 180 | 147 | 191 | 2017-10-29 | NA | 0.799026 |
| 180 | 147 | 191 | 2017-10-29 | OCE | -1.191616 |
| 180 | 147 | 191 | 2017-10-29 | SEA | 0.247892 |
| 180 | 147 | 191 | 2017-10-29 | TR | -0.162301 |
| 180 | 147 | 191 | 2017-10-29 | PCS | 0.219912 |
| 180 | 147 | 191 | 2017-10-29 | VN | 0.247892 |
| 180 | 147 | 191 | 2017-10-29 | LATAM | -0.525619 |
| 180 | 147 | 191 | 2017-10-29 | LCP | -1.704502 |


### 用于 S9

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 149 | 193 | 2018-11-03 | BR | -0.691108 |
| 30 | 149 | 193 | 2018-11-03 | CIS | -0.076033 |
| 30 | 149 | 193 | 2018-11-03 | CN | 1.391312 |
| 30 | 149 | 193 | 2018-11-03 | EU | 1.106351 |
| 30 | 149 | 193 | 2018-11-03 | JP | -0.534111 |
| 30 | 149 | 193 | 2018-11-03 | KR | 0.554276 |
| 30 | 149 | 193 | 2018-11-03 | LAN | 0.191363 |
| 30 | 149 | 193 | 2018-11-03 | LAS | -1.068469 |
| 30 | 149 | 193 | 2018-11-03 | LMS | -0.172736 |
| 30 | 149 | 193 | 2018-11-03 | NA | 0.681374 |
| 30 | 149 | 193 | 2018-11-03 | OCE | -0.203953 |
| 30 | 149 | 193 | 2018-11-03 | SEA | -0.877757 |
| 30 | 149 | 193 | 2018-11-03 | TR | -0.148966 |
| 30 | 149 | 193 | 2018-11-03 | VN | -0.151543 |
| 30 | 149 | 193 | 2018-11-03 | PCS | -0.300921 |
| 30 | 149 | 193 | 2018-11-03 | LATAM | -0.333567 |
| 30 | 149 | 193 | 2018-11-03 | LCP | -0.309071 |
| 60 | 149 | 193 | 2018-11-03 | BR | -0.749674 |
| 60 | 149 | 193 | 2018-11-03 | CIS | -0.062008 |
| 60 | 149 | 193 | 2018-11-03 | CN | 1.476204 |
| 60 | 149 | 193 | 2018-11-03 | EU | 1.176533 |
| 60 | 149 | 193 | 2018-11-03 | JP | -0.702124 |
| 60 | 149 | 193 | 2018-11-03 | KR | 0.688930 |
| 60 | 149 | 193 | 2018-11-03 | LAN | 0.140854 |
| 60 | 149 | 193 | 2018-11-03 | LAS | -1.224417 |
| 60 | 149 | 193 | 2018-11-03 | LMS | 0.038264 |
| 60 | 149 | 193 | 2018-11-03 | NA | 0.762713 |
| 60 | 149 | 193 | 2018-11-03 | OCE | -0.360202 |
| 60 | 149 | 193 | 2018-11-03 | SEA | -1.050640 |
| 60 | 149 | 193 | 2018-11-03 | TR | -0.067152 |
| 60 | 149 | 193 | 2018-11-03 | VN | -0.067280 |
| 60 | 149 | 193 | 2018-11-03 | PCS | -0.159718 |
| 60 | 149 | 193 | 2018-11-03 | LATAM | -0.428009 |
| 60 | 149 | 193 | 2018-11-03 | LCP | -0.328687 |
| 90 | 149 | 193 | 2018-11-03 | BR | -0.725618 |
| 90 | 149 | 193 | 2018-11-03 | CIS | -0.053040 |
| 90 | 149 | 193 | 2018-11-03 | CN | 1.516428 |
| 90 | 149 | 193 | 2018-11-03 | EU | 1.184424 |
| 90 | 149 | 193 | 2018-11-03 | JP | -0.802050 |
| 90 | 149 | 193 | 2018-11-03 | KR | 0.758273 |
| 90 | 149 | 193 | 2018-11-03 | LAN | 0.057980 |
| 90 | 149 | 193 | 2018-11-03 | LAS | -1.251643 |
| 90 | 149 | 193 | 2018-11-03 | LMS | 0.167381 |
| 90 | 149 | 193 | 2018-11-03 | NA | 0.784846 |
| 90 | 149 | 193 | 2018-11-03 | OCE | -0.488444 |
| 90 | 149 | 193 | 2018-11-03 | SEA | -1.108362 |
| 90 | 149 | 193 | 2018-11-03 | TR | -0.024117 |
| 90 | 149 | 193 | 2018-11-03 | VN | -0.016058 |
| 90 | 149 | 193 | 2018-11-03 | PCS | -0.064573 |
| 90 | 149 | 193 | 2018-11-03 | LATAM | -0.487696 |
| 90 | 149 | 193 | 2018-11-03 | LCP | -0.339702 |
| 180 | 149 | 193 | 2018-11-03 | BR | -0.679212 |
| 180 | 149 | 193 | 2018-11-03 | CIS | -0.041359 |
| 180 | 149 | 193 | 2018-11-03 | CN | 1.578397 |
| 180 | 149 | 193 | 2018-11-03 | EU | 1.184496 |
| 180 | 149 | 193 | 2018-11-03 | JP | -0.947793 |
| 180 | 149 | 193 | 2018-11-03 | KR | 0.857342 |
| 180 | 149 | 193 | 2018-11-03 | LAN | -0.076348 |
| 180 | 149 | 193 | 2018-11-03 | LAS | -1.268238 |
| 180 | 149 | 193 | 2018-11-03 | LMS | 0.345207 |
| 180 | 149 | 193 | 2018-11-03 | NA | 0.807058 |
| 180 | 149 | 193 | 2018-11-03 | OCE | -0.663375 |
| 180 | 149 | 193 | 2018-11-03 | SEA | -1.169448 |
| 180 | 149 | 193 | 2018-11-03 | TR | 0.018889 |
| 180 | 149 | 193 | 2018-11-03 | VN | 0.054385 |
| 180 | 149 | 193 | 2018-11-03 | PCS | 0.069815 |
| 180 | 149 | 193 | 2018-11-03 | LATAM | -0.572969 |
| 180 | 149 | 193 | 2018-11-03 | LCP | -0.358277 |


### 用于 S10

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 148 | 195 | 2019-11-10 | BR | -0.700380 |
| 30 | 148 | 195 | 2019-11-10 | CIS | 0.139091 |
| 30 | 148 | 195 | 2019-11-10 | CN | 1.489812 |
| 30 | 148 | 195 | 2019-11-10 | EU | 0.931563 |
| 30 | 148 | 195 | 2019-11-10 | JP | -0.346375 |
| 30 | 148 | 195 | 2019-11-10 | KR | 1.135062 |
| 30 | 148 | 195 | 2019-11-10 | LATAM | -0.409187 |
| 30 | 148 | 195 | 2019-11-10 | LMS | -0.371758 |
| 30 | 148 | 195 | 2019-11-10 | NA | 0.083589 |
| 30 | 148 | 195 | 2019-11-10 | OCE | -0.166678 |
| 30 | 148 | 195 | 2019-11-10 | SEA | -0.667219 |
| 30 | 148 | 195 | 2019-11-10 | TR | -0.664327 |
| 30 | 148 | 195 | 2019-11-10 | VN | -0.453194 |
| 30 | 148 | 195 | 2019-11-10 | PCS | -0.430850 |
| 30 | 148 | 195 | 2019-11-10 | LCP | -0.431395 |
| 60 | 148 | 195 | 2019-11-10 | BR | -0.957544 |
| 60 | 148 | 195 | 2019-11-10 | CIS | 0.124273 |
| 60 | 148 | 195 | 2019-11-10 | CN | 1.553741 |
| 60 | 148 | 195 | 2019-11-10 | EU | 1.051684 |
| 60 | 148 | 195 | 2019-11-10 | JP | -0.371031 |
| 60 | 148 | 195 | 2019-11-10 | KR | 1.285647 |
| 60 | 148 | 195 | 2019-11-10 | LATAM | -0.452516 |
| 60 | 148 | 195 | 2019-11-10 | LMS | -0.262461 |
| 60 | 148 | 195 | 2019-11-10 | NA | 0.224202 |
| 60 | 148 | 195 | 2019-11-10 | OCE | -0.267038 |
| 60 | 148 | 195 | 2019-11-10 | SEA | -0.805078 |
| 60 | 148 | 195 | 2019-11-10 | TR | -0.732497 |
| 60 | 148 | 195 | 2019-11-10 | VN | -0.391381 |
| 60 | 148 | 195 | 2019-11-10 | PCS | -0.370985 |
| 60 | 148 | 195 | 2019-11-10 | LCP | -0.387228 |
| 90 | 148 | 195 | 2019-11-10 | BR | -1.079251 |
| 90 | 148 | 195 | 2019-11-10 | CIS | 0.082906 |
| 90 | 148 | 195 | 2019-11-10 | CN | 1.581138 |
| 90 | 148 | 195 | 2019-11-10 | EU | 1.099140 |
| 90 | 148 | 195 | 2019-11-10 | JP | -0.356524 |
| 90 | 148 | 195 | 2019-11-10 | KR | 1.339903 |
| 90 | 148 | 195 | 2019-11-10 | LATAM | -0.483157 |
| 90 | 148 | 195 | 2019-11-10 | LMS | -0.200043 |
| 90 | 148 | 195 | 2019-11-10 | NA | 0.300342 |
| 90 | 148 | 195 | 2019-11-10 | OCE | -0.356829 |
| 90 | 148 | 195 | 2019-11-10 | SEA | -0.859909 |
| 90 | 148 | 195 | 2019-11-10 | TR | -0.717237 |
| 90 | 148 | 195 | 2019-11-10 | VN | -0.350478 |
| 90 | 148 | 195 | 2019-11-10 | PCS | -0.332016 |
| 90 | 148 | 195 | 2019-11-10 | LCP | -0.351712 |
| 180 | 148 | 195 | 2019-11-10 | BR | -1.233250 |
| 180 | 148 | 195 | 2019-11-10 | CIS | 0.024632 |
| 180 | 148 | 195 | 2019-11-10 | CN | 1.621602 |
| 180 | 148 | 195 | 2019-11-10 | EU | 1.161093 |
| 180 | 148 | 195 | 2019-11-10 | JP | -0.339307 |
| 180 | 148 | 195 | 2019-11-10 | KR | 1.402558 |
| 180 | 148 | 195 | 2019-11-10 | LATAM | -0.538530 |
| 180 | 148 | 195 | 2019-11-10 | LMS | -0.116773 |
| 180 | 148 | 195 | 2019-11-10 | NA | 0.407300 |
| 180 | 148 | 195 | 2019-11-10 | OCE | -0.483257 |
| 180 | 148 | 195 | 2019-11-10 | SEA | -0.935112 |
| 180 | 148 | 195 | 2019-11-10 | TR | -0.670491 |
| 180 | 148 | 195 | 2019-11-10 | VN | -0.300465 |
| 180 | 148 | 195 | 2019-11-10 | PCS | -0.280440 |
| 180 | 148 | 195 | 2019-11-10 | LCP | -0.308392 |


### 用于 S11

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 91 | 115 | 2020-10-31 | BR | -0.599659 |
| 30 | 91 | 115 | 2020-10-31 | CIS | -0.191460 |
| 30 | 91 | 115 | 2020-10-31 | CN | 0.770930 |
| 30 | 91 | 115 | 2020-10-31 | EU | 0.345284 |
| 30 | 91 | 115 | 2020-10-31 | JP | -0.582533 |
| 30 | 91 | 115 | 2020-10-31 | KR | 1.049242 |
| 30 | 91 | 115 | 2020-10-31 | LATAM | -0.375810 |
| 30 | 91 | 115 | 2020-10-31 | NA | 0.070449 |
| 30 | 91 | 115 | 2020-10-31 | OCE | -0.197778 |
| 30 | 91 | 115 | 2020-10-31 | PCS | -0.063096 |
| 30 | 91 | 115 | 2020-10-31 | TR | -0.225568 |
| 30 | 91 | 115 | 2020-10-31 | LCP | -0.181150 |
| 60 | 91 | 115 | 2020-10-31 | BR | -0.726515 |
| 60 | 91 | 115 | 2020-10-31 | CIS | -0.128878 |
| 60 | 91 | 115 | 2020-10-31 | CN | 0.860280 |
| 60 | 91 | 115 | 2020-10-31 | EU | 0.343959 |
| 60 | 91 | 115 | 2020-10-31 | JP | -0.672662 |
| 60 | 91 | 115 | 2020-10-31 | KR | 1.055011 |
| 60 | 91 | 115 | 2020-10-31 | LATAM | -0.400550 |
| 60 | 91 | 115 | 2020-10-31 | NA | 0.108898 |
| 60 | 91 | 115 | 2020-10-31 | OCE | -0.198368 |
| 60 | 91 | 115 | 2020-10-31 | PCS | -0.013881 |
| 60 | 91 | 115 | 2020-10-31 | TR | -0.227293 |
| 60 | 91 | 115 | 2020-10-31 | LCP | -0.163604 |
| 90 | 91 | 115 | 2020-10-31 | BR | -0.769370 |
| 90 | 91 | 115 | 2020-10-31 | CIS | -0.106233 |
| 90 | 91 | 115 | 2020-10-31 | CN | 0.899095 |
| 90 | 91 | 115 | 2020-10-31 | EU | 0.339193 |
| 90 | 91 | 115 | 2020-10-31 | JP | -0.697444 |
| 90 | 91 | 115 | 2020-10-31 | KR | 1.035239 |
| 90 | 91 | 115 | 2020-10-31 | LATAM | -0.402010 |
| 90 | 91 | 115 | 2020-10-31 | NA | 0.120665 |
| 90 | 91 | 115 | 2020-10-31 | OCE | -0.195514 |
| 90 | 91 | 115 | 2020-10-31 | PCS | 0.004055 |
| 90 | 91 | 115 | 2020-10-31 | TR | -0.227677 |
| 90 | 91 | 115 | 2020-10-31 | LCP | -0.155376 |
| 180 | 91 | 115 | 2020-10-31 | BR | -0.812260 |
| 180 | 91 | 115 | 2020-10-31 | CIS | -0.082925 |
| 180 | 91 | 115 | 2020-10-31 | CN | 0.945442 |
| 180 | 91 | 115 | 2020-10-31 | EU | 0.331827 |
| 180 | 91 | 115 | 2020-10-31 | JP | -0.718174 |
| 180 | 91 | 115 | 2020-10-31 | KR | 0.999128 |
| 180 | 91 | 115 | 2020-10-31 | LATAM | -0.398552 |
| 180 | 91 | 115 | 2020-10-31 | NA | 0.131552 |
| 180 | 91 | 115 | 2020-10-31 | OCE | -0.190585 |
| 180 | 91 | 115 | 2020-10-31 | PCS | 0.022852 |
| 180 | 91 | 115 | 2020-10-31 | TR | -0.228306 |
| 180 | 91 | 115 | 2020-10-31 | LCP | -0.145563 |


### 用于 S12

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 154 | 189 | 2021-11-06 | BR | -0.588347 |
| 30 | 154 | 189 | 2021-11-06 | CIS | -0.662703 |
| 30 | 154 | 189 | 2021-11-06 | CN | 1.030239 |
| 30 | 154 | 189 | 2021-11-06 | EU | 0.147940 |
| 30 | 154 | 189 | 2021-11-06 | JP | -0.161982 |
| 30 | 154 | 189 | 2021-11-06 | KR | 1.311892 |
| 30 | 154 | 189 | 2021-11-06 | LATAM | -0.958188 |
| 30 | 154 | 189 | 2021-11-06 | NA | 0.414508 |
| 30 | 154 | 189 | 2021-11-06 | OCE | -0.373602 |
| 30 | 154 | 189 | 2021-11-06 | PCS | 0.036239 |
| 30 | 154 | 189 | 2021-11-06 | TR | -0.195995 |
| 30 | 154 | 189 | 2021-11-06 | LCP | -0.023936 |
| 60 | 154 | 189 | 2021-11-06 | BR | -0.736146 |
| 60 | 154 | 189 | 2021-11-06 | CIS | -0.801344 |
| 60 | 154 | 189 | 2021-11-06 | CN | 1.176764 |
| 60 | 154 | 189 | 2021-11-06 | EU | 0.327419 |
| 60 | 154 | 189 | 2021-11-06 | JP | -0.098918 |
| 60 | 154 | 189 | 2021-11-06 | KR | 1.468019 |
| 60 | 154 | 189 | 2021-11-06 | LATAM | -1.204440 |
| 60 | 154 | 189 | 2021-11-06 | NA | 0.503730 |
| 60 | 154 | 189 | 2021-11-06 | OCE | -0.529421 |
| 60 | 154 | 189 | 2021-11-06 | PCS | 0.138307 |
| 60 | 154 | 189 | 2021-11-06 | TR | -0.243969 |
| 60 | 154 | 189 | 2021-11-06 | LCP | 0.066292 |
| 90 | 154 | 189 | 2021-11-06 | BR | -0.784916 |
| 90 | 154 | 189 | 2021-11-06 | CIS | -0.875855 |
| 90 | 154 | 189 | 2021-11-06 | CN | 1.252268 |
| 90 | 154 | 189 | 2021-11-06 | EU | 0.422325 |
| 90 | 154 | 189 | 2021-11-06 | JP | -0.094717 |
| 90 | 154 | 189 | 2021-11-06 | KR | 1.528678 |
| 90 | 154 | 189 | 2021-11-06 | LATAM | -1.277257 |
| 90 | 154 | 189 | 2021-11-06 | NA | 0.524811 |
| 90 | 154 | 189 | 2021-11-06 | OCE | -0.607415 |
| 90 | 154 | 189 | 2021-11-06 | PCS | 0.205310 |
| 90 | 154 | 189 | 2021-11-06 | TR | -0.293232 |
| 90 | 154 | 189 | 2021-11-06 | LCP | 0.114230 |
| 180 | 154 | 189 | 2021-11-06 | BR | -0.816709 |
| 180 | 154 | 189 | 2021-11-06 | CIS | -0.976938 |
| 180 | 154 | 189 | 2021-11-06 | CN | 1.345651 |
| 180 | 154 | 189 | 2021-11-06 | EU | 0.537894 |
| 180 | 154 | 189 | 2021-11-06 | JP | -0.113951 |
| 180 | 154 | 189 | 2021-11-06 | KR | 1.591340 |
| 180 | 154 | 189 | 2021-11-06 | LATAM | -1.326903 |
| 180 | 154 | 189 | 2021-11-06 | NA | 0.533125 |
| 180 | 154 | 189 | 2021-11-06 | OCE | -0.694373 |
| 180 | 154 | 189 | 2021-11-06 | PCS | 0.297172 |
| 180 | 154 | 189 | 2021-11-06 | TR | -0.376308 |
| 180 | 154 | 189 | 2021-11-06 | LCP | 0.172367 |


### 用于 S13

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 160 | 190 | 2022-10-29 | BR | -0.345047 |
| 30 | 160 | 190 | 2022-10-29 | CN | 1.467413 |
| 30 | 160 | 190 | 2022-10-29 | EU | 0.248606 |
| 30 | 160 | 190 | 2022-10-29 | JP | 0.139402 |
| 30 | 160 | 190 | 2022-10-29 | KR | 2.110513 |
| 30 | 160 | 190 | 2022-10-29 | LATAM | -0.571078 |
| 30 | 160 | 190 | 2022-10-29 | NA | 0.125158 |
| 30 | 160 | 190 | 2022-10-29 | OCE | -1.274605 |
| 30 | 160 | 190 | 2022-10-29 | PCS | -0.474418 |
| 30 | 160 | 190 | 2022-10-29 | TR | -1.076846 |
| 30 | 160 | 190 | 2022-10-29 | VN | -0.349098 |
| 30 | 160 | 190 | 2022-10-29 | LCP | -0.267222 |
| 60 | 160 | 190 | 2022-10-29 | BR | -0.408659 |
| 60 | 160 | 190 | 2022-10-29 | CN | 1.660221 |
| 60 | 160 | 190 | 2022-10-29 | EU | 0.423619 |
| 60 | 160 | 190 | 2022-10-29 | JP | 0.094034 |
| 60 | 160 | 190 | 2022-10-29 | KR | 2.242427 |
| 60 | 160 | 190 | 2022-10-29 | LATAM | -0.706646 |
| 60 | 160 | 190 | 2022-10-29 | NA | 0.220902 |
| 60 | 160 | 190 | 2022-10-29 | OCE | -1.580430 |
| 60 | 160 | 190 | 2022-10-29 | PCS | -0.402492 |
| 60 | 160 | 190 | 2022-10-29 | TR | -1.295379 |
| 60 | 160 | 190 | 2022-10-29 | VN | -0.247596 |
| 60 | 160 | 190 | 2022-10-29 | LCP | -0.213616 |
| 90 | 160 | 190 | 2022-10-29 | BR | -0.458450 |
| 90 | 160 | 190 | 2022-10-29 | CN | 1.756375 |
| 90 | 160 | 190 | 2022-10-29 | EU | 0.514131 |
| 90 | 160 | 190 | 2022-10-29 | JP | 0.035490 |
| 90 | 160 | 190 | 2022-10-29 | KR | 2.295696 |
| 90 | 160 | 190 | 2022-10-29 | LATAM | -0.762814 |
| 90 | 160 | 190 | 2022-10-29 | NA | 0.256907 |
| 90 | 160 | 190 | 2022-10-29 | OCE | -1.730727 |
| 90 | 160 | 190 | 2022-10-29 | PCS | -0.357160 |
| 90 | 160 | 190 | 2022-10-29 | TR | -1.369519 |
| 90 | 160 | 190 | 2022-10-29 | VN | -0.179930 |
| 90 | 160 | 190 | 2022-10-29 | LCP | -0.186043 |
| 180 | 160 | 190 | 2022-10-29 | BR | -0.530080 |
| 180 | 160 | 190 | 2022-10-29 | CN | 1.880947 |
| 180 | 160 | 190 | 2022-10-29 | EU | 0.631490 |
| 180 | 160 | 190 | 2022-10-29 | JP | -0.063513 |
| 180 | 160 | 190 | 2022-10-29 | KR | 2.356898 |
| 180 | 160 | 190 | 2022-10-29 | LATAM | -0.830449 |
| 180 | 160 | 190 | 2022-10-29 | NA | 0.298466 |
| 180 | 160 | 190 | 2022-10-29 | OCE | -1.916851 |
| 180 | 160 | 190 | 2022-10-29 | PCS | -0.294080 |
| 180 | 160 | 190 | 2022-10-29 | TR | -1.440066 |
| 180 | 160 | 190 | 2022-10-29 | VN | -0.092760 |
| 180 | 160 | 190 | 2022-10-29 | LCP | -0.154949 |


### 用于 S14

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 63 | 148 | 2023-11-19 | BR | -0.407001 |
| 30 | 63 | 148 | 2023-11-19 | CN | 0.998595 |
| 30 | 63 | 148 | 2023-11-19 | EU | -0.031363 |
| 30 | 63 | 148 | 2023-11-19 | JP | -0.968496 |
| 30 | 63 | 148 | 2023-11-19 | KR | 1.506693 |
| 30 | 63 | 148 | 2023-11-19 | LATAM | -0.926757 |
| 30 | 63 | 148 | 2023-11-19 | NA | -0.169470 |
| 30 | 63 | 148 | 2023-11-19 | PCS | -0.050709 |
| 30 | 63 | 148 | 2023-11-19 | VN | 0.048509 |
| 30 | 63 | 148 | 2023-11-19 | LCP | -0.137745 |
| 60 | 63 | 148 | 2023-11-19 | BR | -0.528646 |
| 60 | 63 | 148 | 2023-11-19 | CN | 1.265900 |
| 60 | 63 | 148 | 2023-11-19 | EU | 0.110676 |
| 60 | 63 | 148 | 2023-11-19 | JP | -1.305318 |
| 60 | 63 | 148 | 2023-11-19 | KR | 1.656846 |
| 60 | 63 | 148 | 2023-11-19 | LATAM | -1.138699 |
| 60 | 63 | 148 | 2023-11-19 | NA | -0.011563 |
| 60 | 63 | 148 | 2023-11-19 | PCS | -0.080411 |
| 60 | 63 | 148 | 2023-11-19 | VN | 0.031216 |
| 60 | 63 | 148 | 2023-11-19 | LCP | -0.205327 |
| 90 | 63 | 148 | 2023-11-19 | BR | -0.621004 |
| 90 | 63 | 148 | 2023-11-19 | CN | 1.414488 |
| 90 | 63 | 148 | 2023-11-19 | EU | 0.186124 |
| 90 | 63 | 148 | 2023-11-19 | JP | -1.494356 |
| 90 | 63 | 148 | 2023-11-19 | KR | 1.726088 |
| 90 | 63 | 148 | 2023-11-19 | LATAM | -1.171345 |
| 90 | 63 | 148 | 2023-11-19 | NA | 0.085021 |
| 90 | 63 | 148 | 2023-11-19 | PCS | -0.112935 |
| 90 | 63 | 148 | 2023-11-19 | VN | -0.012081 |
| 90 | 63 | 148 | 2023-11-19 | LCP | -0.264354 |
| 180 | 63 | 148 | 2023-11-19 | BR | -0.768090 |
| 180 | 63 | 148 | 2023-11-19 | CN | 1.625432 |
| 180 | 63 | 148 | 2023-11-19 | EU | 0.291193 |
| 180 | 63 | 148 | 2023-11-19 | JP | -1.773649 |
| 180 | 63 | 148 | 2023-11-19 | KR | 1.820619 |
| 180 | 63 | 148 | 2023-11-19 | LATAM | -1.157224 |
| 180 | 63 | 148 | 2023-11-19 | NA | 0.224085 |
| 180 | 63 | 148 | 2023-11-19 | PCS | -0.167243 |
| 180 | 63 | 148 | 2023-11-19 | VN | -0.095123 |
| 180 | 63 | 148 | 2023-11-19 | LCP | -0.362337 |


### 用于 S15

| 半衰期 | 来源系列赛 | 来源小局 | 最晚来源日期 | 赛区 | 先验强度 |
| --- | --- | --- | --- | --- | --- |
| 30 | 75 | 185 | 2024-11-02 | BR | -0.359130 |
| 30 | 75 | 185 | 2024-11-02 | CN | 0.962031 |
| 30 | 75 | 185 | 2024-11-02 | EU | 0.009419 |
| 30 | 75 | 185 | 2024-11-02 | JP | -0.995894 |
| 30 | 75 | 185 | 2024-11-02 | KR | 1.001146 |
| 30 | 75 | 185 | 2024-11-02 | LATAM | -0.441828 |
| 30 | 75 | 185 | 2024-11-02 | NA | 0.190236 |
| 30 | 75 | 185 | 2024-11-02 | PCS | -0.031847 |
| 30 | 75 | 185 | 2024-11-02 | VN | -0.334132 |
| 30 | 75 | 185 | 2024-11-02 | LCP | -0.228370 |
| 60 | 75 | 185 | 2024-11-02 | BR | -0.401033 |
| 60 | 75 | 185 | 2024-11-02 | CN | 1.101253 |
| 60 | 75 | 185 | 2024-11-02 | EU | 0.137536 |
| 60 | 75 | 185 | 2024-11-02 | JP | -1.270724 |
| 60 | 75 | 185 | 2024-11-02 | KR | 1.150940 |
| 60 | 75 | 185 | 2024-11-02 | LATAM | -0.575256 |
| 60 | 75 | 185 | 2024-11-02 | NA | 0.188575 |
| 60 | 75 | 185 | 2024-11-02 | PCS | 0.064008 |
| 60 | 75 | 185 | 2024-11-02 | VN | -0.395300 |
| 60 | 75 | 185 | 2024-11-02 | LCP | -0.225137 |
| 90 | 75 | 185 | 2024-11-02 | BR | -0.437016 |
| 90 | 75 | 185 | 2024-11-02 | CN | 1.150927 |
| 90 | 75 | 185 | 2024-11-02 | EU | 0.208600 |
| 90 | 75 | 185 | 2024-11-02 | JP | -1.371164 |
| 90 | 75 | 185 | 2024-11-02 | KR | 1.223538 |
| 90 | 75 | 185 | 2024-11-02 | LATAM | -0.653037 |
| 90 | 75 | 185 | 2024-11-02 | NA | 0.194381 |
| 90 | 75 | 185 | 2024-11-02 | PCS | 0.111848 |
| 90 | 75 | 185 | 2024-11-02 | VN | -0.428077 |
| 90 | 75 | 185 | 2024-11-02 | LCP | -0.221794 |
| 180 | 75 | 185 | 2024-11-02 | BR | -0.498267 |
| 180 | 75 | 185 | 2024-11-02 | CN | 1.205940 |
| 180 | 75 | 185 | 2024-11-02 | EU | 0.303068 |
| 180 | 75 | 185 | 2024-11-02 | JP | -1.475868 |
| 180 | 75 | 185 | 2024-11-02 | KR | 1.314469 |
| 180 | 75 | 185 | 2024-11-02 | LATAM | -0.761219 |
| 180 | 75 | 185 | 2024-11-02 | NA | 0.212667 |
| 180 | 75 | 185 | 2024-11-02 | PCS | 0.171775 |
| 180 | 75 | 185 | 2024-11-02 | VN | -0.472566 |
| 180 | 75 | 185 | 2024-11-02 | LCP | -0.217505 |

## 新模型比较

[分层与动态模型：逐场、冠军概率及最终排名](candidate_models.md)。本轮全部采用 90 天设定，独立于上面的旧半衰期比较。

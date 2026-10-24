# 系列赛内实时预测

[比较结果](README.md)

概率指队伍一赢得下一局；所有列都已知当前比分。

| 赛季 | 日期 | 队伍一 | 队伍二 | 下一局 | 已知比分 | 下一局实际胜者 | 原模型 | 近期状态 | 共享状态 | 组合 |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| S7 | 2017-05-03 | Team SoloMid | GIGABYTE Marines | 2 | 0:1 | GIGABYTE Marines | 64.13% | 63.96% | 57.38% | 57.11% |
| S7 | 2017-05-03 | Team SoloMid | GIGABYTE Marines | 3 | 0:2 | Team SoloMid | 64.13% | 63.96% | 51.92% | 51.59% |
| S7 | 2017-05-03 | Team SoloMid | GIGABYTE Marines | 4 | 1:2 | Team SoloMid | 64.13% | 63.96% | 56.10% | 55.86% |
| S7 | 2017-05-03 | Team SoloMid | GIGABYTE Marines | 5 | 2:2 | Team SoloMid | 64.13% | 63.96% | 59.61% | 59.43% |
| S7 | 2017-05-04 | Flash Wolves | SuperMassive | 2 | 1:0 | Flash Wolves | 83.74% | 83.55% | 85.45% | 85.31% |
| S7 | 2017-05-04 | Flash Wolves | SuperMassive | 3 | 2:0 | Flash Wolves | 83.74% | 83.55% | 86.83% | 86.73% |
| S7 | 2017-05-06 | SuperMassive | GIGABYTE Marines | 2 | 0:1 | SuperMassive | 30.94% | 31.31% | 27.70% | 27.96% |
| S7 | 2017-05-06 | SuperMassive | GIGABYTE Marines | 3 | 1:1 | GIGABYTE Marines | 30.94% | 31.31% | 34.56% | 34.91% |
| S7 | 2017-05-06 | SuperMassive | GIGABYTE Marines | 4 | 1:2 | GIGABYTE Marines | 30.94% | 31.31% | 31.56% | 31.84% |
| S7 | 2017-05-19 | SK Telecom T1 | Flash Wolves | 2 | 1:0 | SK Telecom T1 | 73.72% | 73.66% | 76.45% | 76.44% |
| S7 | 2017-05-19 | SK Telecom T1 | Flash Wolves | 3 | 2:0 | SK Telecom T1 | 73.72% | 73.66% | 78.66% | 78.69% |
| S7 | 2017-05-20 | Team WE | G2 Esports | 2 | 0:1 | G2 Esports | 68.86% | 69.44% | 61.72% | 62.11% |
| S7 | 2017-05-20 | Team WE | G2 Esports | 3 | 0:2 | Team WE | 68.86% | 69.44% | 55.93% | 56.18% |
| S7 | 2017-05-20 | Team WE | G2 Esports | 4 | 1:2 | G2 Esports | 68.86% | 69.44% | 59.71% | 60.00% |
| S7 | 2017-05-21 | SK Telecom T1 | G2 Esports | 2 | 1:0 | G2 Esports | 80.88% | 80.88% | 82.86% | 82.89% |
| S7 | 2017-05-21 | SK Telecom T1 | G2 Esports | 3 | 1:1 | SK Telecom T1 | 80.88% | 80.88% | 75.09% | 74.99% |
| S7 | 2017-05-21 | SK Telecom T1 | G2 Esports | 4 | 2:1 | SK Telecom T1 | 80.88% | 80.88% | 77.22% | 77.17% |
| S8 | 2018-05-09 | Flash Wolves | Gambit Esports | 2 | 1:0 | Flash Wolves | 64.37% | 63.74% | 67.09% | 66.56% |
| S8 | 2018-05-09 | Flash Wolves | Gambit Esports | 3 | 2:0 | Flash Wolves | 64.37% | 63.74% | 69.42% | 68.98% |
| S8 | 2018-05-18 | Fnatic | Royal Never Give Up | 2 | 0:1 | Royal Never Give Up | 30.14% | 29.86% | 27.85% | 27.55% |
| S8 | 2018-05-18 | Fnatic | Royal Never Give Up | 3 | 0:2 | Royal Never Give Up | 30.14% | 29.86% | 25.89% | 25.58% |
| S8 | 2018-05-19 | Flash Wolves | Kingzone DragonX | 2 | 0:1 | Flash Wolves | 39.22% | 40.28% | 36.25% | 37.17% |
| S8 | 2018-05-19 | Flash Wolves | Kingzone DragonX | 3 | 1:1 | Kingzone DragonX | 39.22% | 40.28% | 40.74% | 41.68% |
| S8 | 2018-05-19 | Flash Wolves | Kingzone DragonX | 4 | 1:2 | Kingzone DragonX | 39.22% | 40.28% | 38.06% | 38.89% |
| S8 | 2018-05-20 | Royal Never Give Up | Kingzone DragonX | 2 | 1:0 | Kingzone DragonX | 54.19% | 55.07% | 57.65% | 58.54% |
| S8 | 2018-05-20 | Royal Never Give Up | Kingzone DragonX | 3 | 1:1 | Royal Never Give Up | 54.19% | 55.07% | 53.60% | 54.35% |
| S8 | 2018-05-20 | Royal Never Give Up | Kingzone DragonX | 4 | 2:1 | Royal Never Give Up | 54.19% | 55.07% | 56.65% | 57.40% |
| S9 | 2019-05-06 | Flash Wolves | Vega Squadron | 2 | 0:1 | Flash Wolves | 39.87% | 38.34% | 33.16% | 31.73% |
| S9 | 2019-05-06 | Flash Wolves | Vega Squadron | 3 | 1:1 | Flash Wolves | 39.87% | 38.34% | 42.79% | 41.77% |
| S9 | 2019-05-06 | Flash Wolves | Vega Squadron | 4 | 2:1 | Flash Wolves | 39.87% | 38.34% | 50.00% | 49.24% |
| S9 | 2019-05-17 | Invictus Gaming | Team Liquid | 2 | 0:1 | Team Liquid | 79.10% | 80.37% | 65.91% | 66.63% |
| S9 | 2019-05-17 | Invictus Gaming | Team Liquid | 3 | 0:2 | Invictus Gaming | 79.10% | 80.37% | 56.49% | 56.91% |
| S9 | 2019-05-17 | Invictus Gaming | Team Liquid | 4 | 1:2 | Team Liquid | 79.10% | 80.37% | 61.93% | 62.40% |
| S9 | 2019-05-19 | G2 Esports | Team Liquid | 2 | 1:0 | G2 Esports | 50.03% | 49.38% | 58.35% | 58.01% |
| S9 | 2019-05-19 | G2 Esports | Team Liquid | 3 | 2:0 | G2 Esports | 50.03% | 49.38% | 64.29% | 64.13% |
| S10 | 2020-05-30 | Funplus Phoenix | JD Gaming | 2 | 0:1 | Funplus Phoenix | 41.46% | 41.23% | 39.79% | 39.49% |
| S10 | 2020-05-30 | Funplus Phoenix | JD Gaming | 3 | 1:1 | Funplus Phoenix | 41.46% | 41.23% | 42.12% | 41.94% |
| S10 | 2020-05-30 | Funplus Phoenix | JD Gaming | 4 | 2:1 | Funplus Phoenix | 41.46% | 41.23% | 44.28% | 44.20% |
| S10 | 2020-05-30 | Gen.G eSports | Top Esports | 2 | 0:1 | Top Esports | 43.63% | 43.73% | 41.87% | 41.89% |
| S10 | 2020-05-30 | Gen.G eSports | Top Esports | 3 | 0:2 | Top Esports | 43.63% | 43.73% | 40.24% | 40.19% |
| S10 | 2020-05-31 | Funplus Phoenix | Top Esports | 2 | 0:1 | Funplus Phoenix | 50.09% | 49.96% | 48.07% | 47.85% |
| S10 | 2020-05-31 | Funplus Phoenix | Top Esports | 3 | 1:1 | Top Esports | 50.09% | 49.96% | 50.08% | 49.96% |
| S10 | 2020-05-31 | Funplus Phoenix | Top Esports | 4 | 1:2 | Top Esports | 50.09% | 49.96% | 48.21% | 48.02% |
| S10 | 2020-09-30 | Legacy eSports | LGD Gaming | 2 | 0:1 | LGD Gaming | 32.82% | 34.69% | 31.42% | 33.18% |
| S10 | 2020-09-30 | Legacy eSports | LGD Gaming | 3 | 0:2 | LGD Gaming | 32.82% | 34.69% | 30.13% | 31.81% |
| S10 | 2020-09-30 | Unicorns Of Love | Papara SuperMassive | 2 | 1:0 | Unicorns Of Love | 72.16% | 72.50% | 73.35% | 73.69% |
| S10 | 2020-09-30 | Unicorns Of Love | Papara SuperMassive | 3 | 2:0 | Unicorns Of Love | 72.16% | 72.50% | 74.44% | 74.78% |
| S10 | 2020-10-16 | Suning | JD Gaming | 2 | 0:1 | Suning | 47.32% | 46.86% | 45.32% | 44.86% |
| S10 | 2020-10-16 | Suning | JD Gaming | 3 | 1:1 | Suning | 47.32% | 46.86% | 47.54% | 47.12% |
| S10 | 2020-10-16 | Suning | JD Gaming | 4 | 2:1 | Suning | 47.32% | 46.86% | 49.58% | 49.21% |
| S10 | 2020-10-17 | Top Esports | Fnatic | 2 | 0:1 | Fnatic | 72.60% | 72.61% | 69.53% | 69.50% |
| S10 | 2020-10-17 | Top Esports | Fnatic | 3 | 0:2 | Top Esports | 72.60% | 72.61% | 66.71% | 66.65% |
| S10 | 2020-10-17 | Top Esports | Fnatic | 4 | 1:2 | Top Esports | 72.60% | 72.61% | 68.01% | 67.96% |
| S10 | 2020-10-17 | Top Esports | Fnatic | 5 | 2:2 | Top Esports | 72.60% | 72.61% | 69.21% | 69.18% |
| S10 | 2020-10-18 | Gen.G eSports | G2 Esports | 2 | 0:1 | G2 Esports | 69.54% | 69.86% | 66.60% | 66.87% |
| S10 | 2020-10-18 | Gen.G eSports | G2 Esports | 3 | 0:2 | G2 Esports | 69.54% | 69.86% | 63.91% | 64.13% |
| S10 | 2020-10-25 | Top Esports | Suning | 2 | 0:1 | Top Esports | 47.90% | 48.24% | 45.89% | 46.18% |
| S10 | 2020-10-25 | Top Esports | Suning | 3 | 1:1 | Suning | 47.90% | 48.24% | 48.07% | 48.38% |
| S10 | 2020-10-25 | Top Esports | Suning | 4 | 1:2 | Suning | 47.90% | 48.24% | 46.21% | 46.48% |
| S11 | 2021-10-08 | Galatasaray Esports | Beyond Gaming | 2 | 1:0 | Galatasaray Esports | 49.67% | 49.97% | 54.61% | 55.00% |
| S11 | 2021-10-08 | Galatasaray Esports | Beyond Gaming | 3 | 2:0 | Beyond Gaming | 49.67% | 49.97% | 58.68% | 59.10% |
| S11 | 2021-10-08 | Galatasaray Esports | Beyond Gaming | 4 | 2:1 | Beyond Gaming | 49.67% | 49.97% | 53.86% | 54.16% |
| S11 | 2021-10-08 | Galatasaray Esports | Beyond Gaming | 5 | 2:2 | Beyond Gaming | 49.67% | 49.97% | 49.77% | 49.98% |
| S11 | 2021-10-08 | PEACE | RED Canids | 2 | 0:1 | PEACE | 63.69% | 63.72% | 57.43% | 57.33% |
| S11 | 2021-10-08 | PEACE | RED Canids | 3 | 1:1 | PEACE | 63.69% | 63.72% | 61.24% | 61.22% |
| S11 | 2021-10-08 | PEACE | RED Canids | 4 | 2:1 | RED Canids | 63.69% | 63.72% | 64.42% | 64.46% |
| S11 | 2021-10-08 | PEACE | RED Canids | 5 | 2:2 | PEACE | 63.69% | 63.72% | 59.53% | 59.49% |
| S11 | 2021-10-09 | Beyond Gaming | Hanwha Life eSports | 2 | 0:1 | Hanwha Life eSports | 27.64% | 27.95% | 24.93% | 25.15% |
| S11 | 2021-10-09 | Beyond Gaming | Hanwha Life eSports | 3 | 0:2 | Hanwha Life eSports | 27.64% | 27.95% | 22.70% | 22.86% |
| S11 | 2021-10-09 | PEACE | Cloud9 | 2 | 0:1 | Cloud9 | 40.18% | 40.29% | 36.23% | 36.25% |
| S11 | 2021-10-09 | PEACE | Cloud9 | 3 | 0:2 | Cloud9 | 40.18% | 40.29% | 32.99% | 32.95% |
| S11 | 2021-10-22 | T1 | Hanwha Life eSports | 2 | 1:0 | T1 | 58.57% | 59.14% | 62.60% | 63.20% |
| S11 | 2021-10-22 | T1 | Hanwha Life eSports | 3 | 2:0 | T1 | 58.57% | 59.14% | 65.91% | 66.52% |
| S11 | 2021-10-23 | Edward Gaming | Royal Never Give Up | 2 | 0:1 | Edward Gaming | 51.67% | 51.37% | 46.66% | 46.28% |
| S11 | 2021-10-23 | Edward Gaming | Royal Never Give Up | 3 | 1:1 | Edward Gaming | 51.67% | 51.37% | 51.38% | 51.13% |
| S11 | 2021-10-23 | Edward Gaming | Royal Never Give Up | 4 | 2:1 | Royal Never Give Up | 51.67% | 51.37% | 55.33% | 55.17% |
| S11 | 2021-10-23 | Edward Gaming | Royal Never Give Up | 5 | 2:2 | Edward Gaming | 51.67% | 51.37% | 51.17% | 50.95% |
| S11 | 2021-10-25 | Gen.G eSports | Cloud9 | 2 | 1:0 | Gen.G eSports | 65.91% | 65.63% | 69.21% | 69.03% |
| S11 | 2021-10-25 | Gen.G eSports | Cloud9 | 3 | 2:0 | Gen.G eSports | 65.91% | 65.63% | 71.93% | 71.83% |
| S11 | 2021-10-31 | Edward Gaming | Gen.G eSports | 2 | 1:0 | Gen.G eSports | 48.64% | 48.71% | 53.59% | 53.77% |
| S11 | 2021-10-31 | Edward Gaming | Gen.G eSports | 3 | 1:1 | Gen.G eSports | 48.64% | 48.71% | 48.88% | 48.94% |
| S11 | 2021-10-31 | Edward Gaming | Gen.G eSports | 4 | 1:2 | Edward Gaming | 48.64% | 48.71% | 44.92% | 44.91% |
| S11 | 2021-10-31 | Edward Gaming | Gen.G eSports | 5 | 2:2 | Edward Gaming | 48.64% | 48.71% | 49.04% | 49.10% |
| S12 | 2022-05-27 | Royal Never Give Up | Evil Geniuses | 2 | 1:0 | Royal Never Give Up | 76.82% | 77.51% | 78.74% | 79.45% |
| S12 | 2022-05-27 | Royal Never Give Up | Evil Geniuses | 3 | 2:0 | Royal Never Give Up | 76.82% | 77.51% | 80.37% | 81.07% |
| S12 | 2022-05-28 | T1 | G2 Esports | 2 | 1:0 | T1 | 67.69% | 67.83% | 70.37% | 70.59% |
| S12 | 2022-05-28 | T1 | G2 Esports | 3 | 2:0 | T1 | 67.69% | 67.83% | 72.63% | 72.91% |
| S12 | 2022-05-29 | Royal Never Give Up | T1 | 2 | 1:0 | T1 | 49.49% | 49.73% | 53.67% | 54.04% |
| S12 | 2022-05-29 | Royal Never Give Up | T1 | 3 | 1:1 | Royal Never Give Up | 49.49% | 49.73% | 49.57% | 49.78% |
| S12 | 2022-05-29 | Royal Never Give Up | T1 | 4 | 2:1 | T1 | 49.49% | 49.73% | 53.15% | 53.45% |
| S12 | 2022-05-29 | Royal Never Give Up | T1 | 5 | 2:2 | Royal Never Give Up | 49.49% | 49.73% | 49.62% | 49.81% |
| S12 | 2022-10-04 | Royal Never Give Up | Detonation FocusMe | 2 | 0:1 | Royal Never Give Up | 79.16% | 77.57% | 79.16% | 77.03% |
| S12 | 2022-10-04 | Royal Never Give Up | Detonation FocusMe | 3 | 1:1 | Royal Never Give Up | 79.16% | 77.57% | 79.16% | 77.19% |
| S12 | 2022-10-04 | Royal Never Give Up | Detonation FocusMe | 4 | 2:1 | Royal Never Give Up | 79.16% | 77.57% | 79.16% | 77.34% |
| S12 | 2022-10-20 | JD Gaming | Rogue | 2 | 1:0 | JD Gaming | 77.83% | 78.89% | 77.83% | 79.04% |
| S12 | 2022-10-20 | JD Gaming | Rogue | 3 | 2:0 | JD Gaming | 77.83% | 78.89% | 77.83% | 79.18% |
| S12 | 2022-10-21 | T1 | Royal Never Give Up | 2 | 1:0 | T1 | 56.67% | 57.13% | 56.67% | 57.42% |
| S12 | 2022-10-21 | T1 | Royal Never Give Up | 3 | 2:0 | T1 | 56.67% | 57.13% | 56.67% | 57.71% |
| S12 | 2022-10-29 | T1 | JD Gaming | 2 | 0:1 | T1 | 48.41% | 47.24% | 48.40% | 46.92% |
| S12 | 2022-10-29 | T1 | JD Gaming | 3 | 1:1 | T1 | 48.41% | 47.24% | 48.41% | 47.28% |
| S12 | 2022-10-29 | T1 | JD Gaming | 4 | 2:1 | T1 | 48.41% | 47.24% | 48.41% | 47.63% |
| S12 | 2022-10-30 | Gen.G eSports | DRX | 2 | 1:0 | DRX | 64.12% | 65.55% | 64.12% | 65.79% |
| S12 | 2022-10-30 | Gen.G eSports | DRX | 3 | 1:1 | DRX | 64.12% | 65.55% | 64.12% | 65.34% |
| S12 | 2022-10-30 | Gen.G eSports | DRX | 4 | 1:2 | DRX | 64.12% | 65.55% | 64.11% | 64.90% |
| S13 | 2023-05-02 | G2 Esports | LOUD | 2 | 1:0 | G2 Esports | 61.10% | 60.74% | 61.86% | 61.59% |
| S13 | 2023-05-03 | Bilibili Gaming | Movistar R7 | 2 | 1:0 | Bilibili Gaming | 93.51% | 93.52% | 93.64% | 93.66% |
| S13 | 2023-05-03 | Golden Guardians | GAM Esports | 2 | 1:0 | Golden Guardians | 44.84% | 44.46% | 45.91% | 45.66% |
| S13 | 2023-05-04 | Bilibili Gaming | Golden Guardians | 2 | 1:0 | Golden Guardians | 80.95% | 81.03% | 81.32% | 81.44% |
| S13 | 2023-05-04 | Bilibili Gaming | Golden Guardians | 3 | 1:1 | Bilibili Gaming | 80.95% | 81.03% | 79.77% | 79.72% |
| S13 | 2023-05-05 | GAM Esports | Movistar R7 | 2 | 0:1 | GAM Esports | 68.90% | 68.95% | 67.57% | 67.47% |
| S13 | 2023-05-05 | GAM Esports | Movistar R7 | 3 | 1:1 | Movistar R7 | 68.90% | 68.95% | 68.18% | 68.15% |
| S13 | 2023-05-05 | LOUD | Detonation FocusMe | 2 | 1:0 | LOUD | 38.55% | 38.55% | 39.74% | 39.88% |
| S13 | 2023-05-06 | Golden Guardians | Movistar R7 | 2 | 1:0 | Golden Guardians | 74.99% | 74.91% | 75.48% | 75.45% |
| S13 | 2023-05-11 | Cloud9 | Bilibili Gaming | 2 | 0:1 | Bilibili Gaming | 32.35% | 32.60% | 31.73% | 31.90% |
| S13 | 2023-05-11 | Cloud9 | Bilibili Gaming | 3 | 0:2 | Bilibili Gaming | 32.35% | 32.60% | 31.13% | 31.23% |
| S13 | 2023-05-12 | JD Gaming | Golden Guardians | 2 | 1:0 | JD Gaming | 81.27% | 81.42% | 81.63% | 81.82% |
| S13 | 2023-05-12 | JD Gaming | Golden Guardians | 3 | 2:0 | JD Gaming | 81.27% | 81.42% | 81.98% | 82.20% |
| S13 | 2023-05-14 | JD Gaming | Bilibili Gaming | 2 | 1:0 | JD Gaming | 61.60% | 61.84% | 62.34% | 62.66% |
| S13 | 2023-05-14 | JD Gaming | Bilibili Gaming | 3 | 2:0 | JD Gaming | 61.60% | 61.84% | 63.05% | 63.44% |
| S13 | 2023-05-14 | Golden Guardians | Cloud9 | 2 | 0:1 | Cloud9 | 52.33% | 52.16% | 51.32% | 51.04% |
| S13 | 2023-05-14 | Golden Guardians | Cloud9 | 3 | 0:2 | Golden Guardians | 52.33% | 52.16% | 50.35% | 49.97% |
| S13 | 2023-05-14 | Golden Guardians | Cloud9 | 4 | 1:2 | Cloud9 | 52.33% | 52.16% | 51.27% | 51.00% |
| S13 | 2023-05-16 | G2 Esports | Bilibili Gaming | 2 | 0:1 | G2 Esports | 31.12% | 31.29% | 30.52% | 30.62% |
| S13 | 2023-05-16 | G2 Esports | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 31.12% | 31.29% | 31.83% | 32.07% |
| S13 | 2023-05-16 | G2 Esports | Bilibili Gaming | 4 | 1:2 | Bilibili Gaming | 31.12% | 31.29% | 31.24% | 31.42% |
| S13 | 2023-05-18 | JD Gaming | T1 | 2 | 1:0 | T1 | 51.44% | 51.64% | 52.38% | 52.67% |
| S13 | 2023-05-18 | JD Gaming | T1 | 3 | 1:1 | T1 | 51.44% | 51.64% | 51.39% | 51.57% |
| S13 | 2023-05-18 | JD Gaming | T1 | 4 | 1:2 | JD Gaming | 51.44% | 51.64% | 50.44% | 50.51% |
| S13 | 2023-05-18 | JD Gaming | T1 | 5 | 2:2 | JD Gaming | 51.44% | 51.64% | 51.34% | 51.51% |
| S13 | 2023-05-20 | Bilibili Gaming | T1 | 2 | 1:0 | Bilibili Gaming | 46.43% | 46.37% | 47.45% | 47.51% |
| S13 | 2023-05-20 | Bilibili Gaming | T1 | 3 | 2:0 | T1 | 46.43% | 46.37% | 48.44% | 48.61% |
| S13 | 2023-05-20 | Bilibili Gaming | T1 | 4 | 2:1 | Bilibili Gaming | 46.43% | 46.37% | 47.55% | 47.62% |
| S13 | 2023-05-21 | JD Gaming | Bilibili Gaming | 2 | 1:0 | Bilibili Gaming | 60.85% | 61.07% | 61.60% | 61.90% |
| S13 | 2023-05-21 | JD Gaming | Bilibili Gaming | 3 | 1:1 | JD Gaming | 60.85% | 61.07% | 60.44% | 60.61% |
| S13 | 2023-05-21 | JD Gaming | Bilibili Gaming | 4 | 2:1 | JD Gaming | 60.85% | 61.07% | 61.17% | 61.42% |
| S13 | 2023-10-10 | LOUD | GAM Esports | 2 | 1:0 | LOUD | 57.15% | 57.64% | 59.18% | 59.78% |
| S13 | 2023-10-11 | Detonation FocusMe | CTBC Flying Oyster | 2 | 0:1 | CTBC Flying Oyster | 44.45% | 45.54% | 42.35% | 43.24% |
| S13 | 2023-10-11 | Team BDS | Team Whales | 2 | 1:0 | Team Whales | 86.42% | 86.56% | 87.07% | 87.24% |
| S13 | 2023-10-11 | Team BDS | Team Whales | 3 | 1:1 | Team Whales | 86.42% | 86.56% | 83.14% | 83.04% |
| S13 | 2023-10-12 | CTBC Flying Oyster | Team Whales | 2 | 1:0 | Team Whales | 65.93% | 65.63% | 67.54% | 67.37% |
| S13 | 2023-10-12 | CTBC Flying Oyster | Team Whales | 3 | 1:1 | Team Whales | 65.93% | 65.63% | 64.49% | 64.13% |
| S13 | 2023-10-13 | Movistar R7 | GAM Esports | 2 | 0:1 | GAM Esports | 44.50% | 44.89% | 42.40% | 42.63% |
| S13 | 2023-10-13 | Detonation FocusMe | Team BDS | 2 | 0:1 | Team BDS | 24.83% | 25.20% | 23.66% | 23.92% |
| S13 | 2023-10-14 | LOUD | GAM Esports | 2 | 0:1 | GAM Esports | 53.39% | 53.82% | 50.87% | 51.11% |
| S13 | 2023-10-14 | CTBC Flying Oyster | Team BDS | 2 | 0:1 | Team BDS | 36.75% | 36.59% | 35.01% | 34.74% |
| S13 | 2023-10-15 | GAM Esports | Team Whales | 2 | 1:0 | Team Whales | 53.41% | 53.90% | 55.61% | 56.22% |
| S13 | 2023-10-15 | GAM Esports | Team Whales | 3 | 1:1 | GAM Esports | 53.41% | 53.90% | 53.10% | 53.52% |
| S13 | 2023-10-15 | GAM Esports | Team Whales | 4 | 2:1 | GAM Esports | 53.41% | 53.90% | 55.12% | 55.65% |
| S13 | 2023-10-21 | JD Gaming | LNG Esports | 2 | 1:0 | LNG Esports | 57.45% | 58.11% | 59.45% | 60.21% |
| S13 | 2023-10-21 | JD Gaming | LNG Esports | 3 | 1:1 | JD Gaming | 57.45% | 58.11% | 56.79% | 57.33% |
| S13 | 2023-10-23 | Team Liquid | GAM Esports | 2 | 0:1 | Team Liquid | 48.16% | 46.96% | 45.91% | 44.61% |
| S13 | 2023-10-23 | Team Liquid | GAM Esports | 3 | 1:1 | GAM Esports | 48.16% | 46.96% | 48.33% | 47.25% |
| S13 | 2023-10-23 | Dplus KIA | Team BDS | 2 | 1:0 | Dplus KIA | 72.59% | 72.35% | 73.88% | 73.74% |
| S13 | 2023-10-26 | Cloud9 | Fnatic | 2 | 1:0 | Fnatic | 46.11% | 46.44% | 48.63% | 49.12% |
| S13 | 2023-10-26 | Cloud9 | Fnatic | 3 | 1:1 | Fnatic | 46.11% | 46.44% | 46.46% | 46.78% |
| S13 | 2023-10-27 | Dplus KIA | GAM Esports | 2 | 1:0 | Dplus KIA | 84.14% | 83.57% | 84.88% | 84.39% |
| S13 | 2023-10-27 | KT Rolster | LNG Esports | 2 | 0:1 | KT Rolster | 49.95% | 50.26% | 47.61% | 47.75% |
| S13 | 2023-10-27 | KT Rolster | LNG Esports | 3 | 1:1 | LNG Esports | 49.95% | 50.26% | 49.95% | 50.24% |
| S13 | 2023-10-28 | T1 | Bilibili Gaming | 2 | 1:0 | T1 | 40.74% | 39.88% | 43.51% | 42.89% |
| S13 | 2023-10-29 | KT Rolster | Dplus KIA | 2 | 1:0 | KT Rolster | 58.20% | 59.18% | 60.15% | 61.22% |
| S13 | 2023-10-29 | Fnatic | Weibo Gaming | 2 | 1:0 | Weibo Gaming | 23.00% | 23.53% | 26.60% | 27.35% |
| S13 | 2023-10-29 | Fnatic | Weibo Gaming | 3 | 1:1 | Weibo Gaming | 23.00% | 23.53% | 25.41% | 26.04% |
| S13 | 2023-10-29 | G2 Esports | Bilibili Gaming | 2 | 0:1 | G2 Esports | 28.25% | 28.98% | 26.93% | 27.53% |
| S13 | 2023-10-29 | G2 Esports | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 28.25% | 28.98% | 30.19% | 30.98% |
| S13 | 2023-11-04 | JD Gaming | KT Rolster | 2 | 0:1 | JD Gaming | 59.42% | 59.77% | 56.66% | 56.80% |
| S13 | 2023-11-04 | JD Gaming | KT Rolster | 3 | 1:1 | JD Gaming | 59.42% | 59.77% | 58.59% | 58.85% |
| S13 | 2023-11-04 | JD Gaming | KT Rolster | 4 | 2:1 | JD Gaming | 59.42% | 59.77% | 60.35% | 60.71% |
| S13 | 2023-11-05 | LNG Esports | T1 | 2 | 0:1 | T1 | 56.87% | 57.44% | 54.23% | 54.58% |
| S13 | 2023-11-05 | LNG Esports | T1 | 3 | 0:2 | T1 | 56.87% | 57.44% | 51.83% | 52.00% |
| S13 | 2023-11-11 | Weibo Gaming | Bilibili Gaming | 2 | 1:0 | Bilibili Gaming | 45.50% | 45.01% | 48.02% | 47.73% |
| S13 | 2023-11-11 | Weibo Gaming | Bilibili Gaming | 3 | 1:1 | Weibo Gaming | 45.50% | 45.01% | 45.90% | 45.48% |
| S13 | 2023-11-11 | Weibo Gaming | Bilibili Gaming | 4 | 2:1 | Bilibili Gaming | 45.50% | 45.01% | 48.19% | 47.93% |
| S13 | 2023-11-11 | Weibo Gaming | Bilibili Gaming | 5 | 2:2 | Weibo Gaming | 45.50% | 45.01% | 46.23% | 45.87% |
| S13 | 2023-11-12 | T1 | JD Gaming | 2 | 1:0 | JD Gaming | 45.42% | 44.54% | 47.94% | 47.28% |
| S13 | 2023-11-12 | T1 | JD Gaming | 3 | 1:1 | T1 | 45.42% | 44.54% | 45.82% | 45.05% |
| S13 | 2023-11-12 | T1 | JD Gaming | 4 | 2:1 | T1 | 45.42% | 44.54% | 48.12% | 47.52% |
| S13 | 2023-11-19 | Weibo Gaming | T1 | 2 | 0:1 | T1 | 33.82% | 33.25% | 32.26% | 31.62% |
| S13 | 2023-11-19 | Weibo Gaming | T1 | 3 | 0:2 | T1 | 33.82% | 33.25% | 30.85% | 30.13% |
| S14 | 2024-05-01 | T1 | Estral Esports | 2 | 1:0 | T1 | 93.56% | 93.44% | 94.49% | 94.38% |
| S14 | 2024-05-02 | Fnatic | GAM Esports | 2 | 1:0 | Fnatic | 48.26% | 47.95% | 55.69% | 55.44% |
| S14 | 2024-05-02 | Top Esports | LOUD | 2 | 1:0 | Top Esports | 89.55% | 89.67% | 91.05% | 91.16% |
| S14 | 2024-05-03 | T1 | FlyQuest | 2 | 1:0 | T1 | 85.26% | 85.27% | 87.38% | 87.38% |
| S14 | 2024-05-03 | Top Esports | Fnatic | 2 | 1:0 | Fnatic | 80.59% | 80.92% | 83.38% | 83.67% |
| S14 | 2024-05-03 | Top Esports | Fnatic | 3 | 1:1 | Top Esports | 80.59% | 80.92% | 72.92% | 73.15% |
| S14 | 2024-05-04 | LOUD | GAM Esports | 2 | 1:0 | GAM Esports | 43.31% | 43.81% | 51.44% | 51.88% |
| S14 | 2024-05-04 | LOUD | GAM Esports | 3 | 1:1 | GAM Esports | 43.31% | 43.81% | 44.99% | 45.36% |
| S14 | 2024-05-05 | Fnatic | GAM Esports | 2 | 1:0 | Fnatic | 67.18% | 67.53% | 71.88% | 72.19% |
| S14 | 2024-05-07 | Team Liquid | Top Esports | 2 | 0:1 | Top Esports | 17.44% | 17.28% | 14.95% | 14.80% |
| S14 | 2024-05-07 | Team Liquid | Top Esports | 3 | 0:2 | Top Esports | 17.44% | 17.28% | 13.08% | 12.94% |
| S14 | 2024-05-10 | G2 Esports | T1 | 2 | 0:1 | G2 Esports | 20.16% | 20.19% | 17.29% | 17.30% |
| S14 | 2024-05-10 | G2 Esports | T1 | 3 | 1:1 | G2 Esports | 20.16% | 20.19% | 27.61% | 27.64% |
| S14 | 2024-05-10 | G2 Esports | T1 | 4 | 2:1 | T1 | 20.16% | 20.19% | 35.64% | 35.69% |
| S14 | 2024-05-10 | G2 Esports | T1 | 5 | 2:2 | T1 | 20.16% | 20.19% | 32.08% | 32.12% |
| S14 | 2024-05-11 | Fnatic | Team Liquid | 2 | 0:1 | Fnatic | 66.75% | 66.88% | 57.24% | 57.32% |
| S14 | 2024-05-11 | Fnatic | Team Liquid | 3 | 1:1 | Team Liquid | 66.75% | 66.88% | 62.57% | 62.66% |
| S14 | 2024-05-11 | Fnatic | Team Liquid | 4 | 1:2 | Team Liquid | 66.75% | 66.88% | 55.63% | 55.70% |
| S14 | 2024-05-12 | Bilibili Gaming | T1 | 2 | 1:0 | T1 | 46.92% | 47.35% | 54.48% | 54.87% |
| S14 | 2024-05-12 | Bilibili Gaming | T1 | 3 | 1:1 | Bilibili Gaming | 46.92% | 47.35% | 47.69% | 48.01% |
| S14 | 2024-05-12 | Bilibili Gaming | T1 | 4 | 2:1 | Bilibili Gaming | 46.92% | 47.35% | 53.49% | 53.79% |
| S14 | 2024-05-14 | Top Esports | G2 Esports | 2 | 0:1 | G2 Esports | 63.45% | 63.28% | 54.43% | 54.27% |
| S14 | 2024-05-14 | Top Esports | G2 Esports | 3 | 0:2 | G2 Esports | 63.45% | 63.28% | 47.66% | 47.50% |
| S14 | 2024-05-15 | T1 | Team Liquid | 2 | 1:0 | T1 | 80.01% | 79.83% | 82.84% | 82.70% |
| S14 | 2024-05-15 | T1 | Team Liquid | 3 | 2:0 | Team Liquid | 80.01% | 79.83% | 84.98% | 84.86% |
| S14 | 2024-05-15 | T1 | Team Liquid | 4 | 2:1 | T1 | 80.01% | 79.83% | 75.58% | 75.46% |
| S14 | 2024-05-17 | T1 | G2 Esports | 2 | 1:0 | T1 | 53.30% | 52.29% | 59.92% | 59.07% |
| S14 | 2024-05-17 | T1 | G2 Esports | 3 | 2:0 | T1 | 53.30% | 52.29% | 64.89% | 64.16% |
| S14 | 2024-05-18 | Bilibili Gaming | T1 | 2 | 1:0 | T1 | 44.82% | 45.18% | 52.63% | 52.96% |
| S14 | 2024-05-18 | Bilibili Gaming | T1 | 3 | 1:1 | Bilibili Gaming | 44.82% | 45.18% | 46.10% | 46.38% |
| S14 | 2024-05-18 | Bilibili Gaming | T1 | 4 | 2:1 | T1 | 44.82% | 45.18% | 52.05% | 52.31% |
| S14 | 2024-05-18 | Bilibili Gaming | T1 | 5 | 2:2 | Bilibili Gaming | 44.82% | 45.18% | 46.88% | 47.10% |
| S14 | 2024-09-26 | 100 Thieves | Movistar R7 | 2 | 1:0 | Movistar R7 | 72.96% | 71.60% | 76.27% | 75.06% |
| S14 | 2024-09-26 | 100 Thieves | Movistar R7 | 3 | 1:1 | Movistar R7 | 72.96% | 71.60% | 67.94% | 66.91% |
| S14 | 2024-09-27 | GAM Esports | Movistar R7 | 2 | 1:0 | GAM Esports | 71.56% | 71.68% | 75.05% | 75.13% |
| S14 | 2024-09-29 | paiN Gaming | Movistar R7 | 2 | 0:1 | paiN Gaming | 70.38% | 71.18% | 61.76% | 62.53% |
| S14 | 2024-09-29 | paiN Gaming | Movistar R7 | 3 | 1:1 | paiN Gaming | 70.38% | 71.18% | 65.93% | 66.59% |
| S14 | 2024-10-05 | Dplus KIA | LNG Esports | 2 | 0:1 | LNG Esports | 55.03% | 53.55% | 48.33% | 47.07% |
| S14 | 2024-10-07 | MAD Lions KOI | GAM Esports | 2 | 1:0 | GAM Esports | 59.71% | 57.90% | 64.61% | 62.99% |
| S14 | 2024-10-07 | MAD Lions KOI | GAM Esports | 3 | 1:1 | GAM Esports | 59.71% | 57.90% | 57.60% | 56.20% |
| S14 | 2024-10-07 | Team Liquid | paiN Gaming | 2 | 1:0 | Team Liquid | 62.16% | 61.03% | 66.77% | 65.75% |
| S14 | 2024-10-10 | Top Esports | Dplus KIA | 2 | 1:0 | Top Esports | 54.19% | 55.82% | 59.75% | 61.15% |
| S14 | 2024-10-10 | Hanwha Life eSports | FlyQuest | 2 | 1:0 | FlyQuest | 84.21% | 84.03% | 86.13% | 85.96% |
| S14 | 2024-10-10 | Hanwha Life eSports | FlyQuest | 3 | 1:1 | Hanwha Life eSports | 84.21% | 84.03% | 76.80% | 76.70% |
| S14 | 2024-10-11 | G2 Esports | T1 | 2 | 0:1 | T1 | 33.77% | 35.37% | 29.67% | 31.11% |
| S14 | 2024-10-12 | Fnatic | Weibo Gaming | 2 | 1:0 | Weibo Gaming | 31.70% | 32.18% | 39.98% | 40.35% |
| S14 | 2024-10-12 | Fnatic | Weibo Gaming | 3 | 1:1 | Weibo Gaming | 31.70% | 32.18% | 35.66% | 36.01% |
| S14 | 2024-10-12 | Team Liquid | GAM Esports | 2 | 0:1 | Team Liquid | 61.49% | 61.03% | 54.03% | 53.68% |
| S14 | 2024-10-12 | Team Liquid | GAM Esports | 3 | 1:1 | Team Liquid | 61.49% | 61.03% | 59.00% | 58.66% |
| S14 | 2024-10-13 | Dplus KIA | Weibo Gaming | 2 | 1:0 | Weibo Gaming | 56.39% | 56.25% | 61.68% | 61.52% |
| S14 | 2024-10-13 | Dplus KIA | Weibo Gaming | 3 | 1:1 | Weibo Gaming | 56.39% | 56.25% | 55.01% | 54.91% |
| S14 | 2024-10-13 | G2 Esports | Bilibili Gaming | 2 | 0:1 | G2 Esports | 25.59% | 25.96% | 22.49% | 22.84% |
| S14 | 2024-10-13 | G2 Esports | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 25.59% | 25.96% | 30.87% | 31.13% |
| S14 | 2024-10-13 | FlyQuest | Team Liquid | 2 | 1:0 | Team Liquid | 55.10% | 56.30% | 60.55% | 61.56% |
| S14 | 2024-10-13 | FlyQuest | Team Liquid | 3 | 1:1 | FlyQuest | 55.10% | 56.30% | 54.00% | 54.95% |
| S14 | 2024-10-17 | Weibo Gaming | LNG Esports | 2 | 1:0 | LNG Esports | 35.58% | 33.26% | 43.36% | 41.28% |
| S14 | 2024-10-17 | Weibo Gaming | LNG Esports | 3 | 1:1 | Weibo Gaming | 35.58% | 33.26% | 38.69% | 36.85% |
| S14 | 2024-10-17 | Weibo Gaming | LNG Esports | 4 | 2:1 | Weibo Gaming | 35.58% | 33.26% | 44.66% | 42.97% |
| S14 | 2024-10-18 | Hanwha Life eSports | Bilibili Gaming | 2 | 1:0 | Bilibili Gaming | 59.80% | 60.38% | 64.66% | 65.13% |
| S14 | 2024-10-18 | Hanwha Life eSports | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 59.80% | 60.38% | 57.69% | 58.15% |
| S14 | 2024-10-18 | Hanwha Life eSports | Bilibili Gaming | 4 | 1:2 | Bilibili Gaming | 59.80% | 60.38% | 52.08% | 52.52% |
| S14 | 2024-10-19 | Top Esports | T1 | 2 | 0:1 | T1 | 55.52% | 57.15% | 48.82% | 50.29% |
| S14 | 2024-10-19 | Top Esports | T1 | 3 | 0:2 | T1 | 55.52% | 57.15% | 43.56% | 44.91% |
| S14 | 2024-10-26 | Weibo Gaming | Bilibili Gaming | 2 | 0:1 | Bilibili Gaming | 38.33% | 37.63% | 33.73% | 33.14% |
| S14 | 2024-10-26 | Weibo Gaming | Bilibili Gaming | 3 | 0:2 | Bilibili Gaming | 38.33% | 37.63% | 30.11% | 29.61% |
| S14 | 2024-11-02 | T1 | Bilibili Gaming | 2 | 0:1 | T1 | 52.16% | 51.73% | 45.94% | 45.59% |
| S14 | 2024-11-02 | T1 | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 52.16% | 51.73% | 51.70% | 51.36% |
| S14 | 2024-11-02 | T1 | Bilibili Gaming | 4 | 1:2 | T1 | 52.16% | 51.73% | 46.72% | 46.44% |
| S14 | 2024-11-02 | T1 | Bilibili Gaming | 5 | 2:2 | T1 | 52.16% | 51.73% | 51.40% | 51.12% |
| S15 | 2025-06-27 | FURIA | G2 Esports | 2 | 1:0 | G2 Esports | 33.04% | 33.89% | 35.46% | 36.48% |
| S15 | 2025-06-27 | FURIA | G2 Esports | 3 | 1:1 | G2 Esports | 33.04% | 33.89% | 34.22% | 35.11% |
| S15 | 2025-06-27 | FURIA | G2 Esports | 4 | 1:2 | FURIA | 33.04% | 33.89% | 33.07% | 33.83% |
| S15 | 2025-06-27 | FURIA | G2 Esports | 5 | 2:2 | G2 Esports | 33.04% | 33.89% | 35.25% | 36.15% |
| S15 | 2025-06-28 | GAM Esports | FURIA | 2 | 1:0 | FURIA | 55.96% | 54.49% | 57.55% | 56.27% |
| S15 | 2025-06-28 | GAM Esports | FURIA | 3 | 1:1 | FURIA | 55.96% | 54.49% | 55.54% | 54.15% |
| S15 | 2025-06-28 | GAM Esports | FURIA | 4 | 1:2 | GAM Esports | 55.96% | 54.49% | 53.67% | 52.18% |
| S15 | 2025-06-28 | GAM Esports | FURIA | 5 | 2:2 | GAM Esports | 55.96% | 54.49% | 55.18% | 53.86% |
| S15 | 2025-07-03 | Movistar KOI | Bilibili Gaming | 2 | 0:1 | Movistar KOI | 27.35% | 26.58% | 26.37% | 25.54% |
| S15 | 2025-07-03 | Movistar KOI | Bilibili Gaming | 3 | 1:1 | Bilibili Gaming | 27.35% | 26.58% | 28.93% | 28.34% |
| S15 | 2025-07-03 | Movistar KOI | Bilibili Gaming | 4 | 1:2 | Bilibili Gaming | 27.35% | 26.58% | 27.95% | 27.31% |
| S15 | 2025-07-04 | FlyQuest | G2 Esports | 2 | 1:0 | FlyQuest | 63.18% | 64.47% | 64.50% | 65.86% |
| S15 | 2025-07-04 | FlyQuest | G2 Esports | 3 | 2:0 | FlyQuest | 63.18% | 64.47% | 65.74% | 67.14% |
| S15 | 2025-07-05 | CTBC Flying Oyster | Movistar KOI | 2 | 1:0 | CTBC Flying Oyster | 55.33% | 56.37% | 56.94% | 58.08% |
| S15 | 2025-07-05 | CTBC Flying Oyster | Movistar KOI | 3 | 2:0 | Movistar KOI | 55.33% | 56.37% | 58.43% | 59.65% |
| S15 | 2025-07-05 | CTBC Flying Oyster | Movistar KOI | 4 | 2:1 | CTBC Flying Oyster | 55.33% | 56.37% | 56.47% | 57.49% |
| S15 | 2025-10-14 | Invictus Gaming | T1 | 2 | 0:1 | Invictus Gaming | 39.94% | 40.62% | 38.81% | 39.43% |
| S15 | 2025-10-14 | Invictus Gaming | T1 | 3 | 1:1 | T1 | 39.94% | 40.62% | 40.49% | 41.16% |
| S15 | 2025-10-14 | Invictus Gaming | T1 | 4 | 1:2 | T1 | 39.94% | 40.62% | 39.41% | 40.02% |
| S15 | 2025-10-17 | CTBC Flying Oyster | Anyone s Legend | 2 | 1:0 | Anyone s Legend | 37.49% | 38.58% | 39.26% | 40.39% |
| S15 | 2025-10-17 | CTBC Flying Oyster | Anyone s Legend | 3 | 1:1 | Anyone s Legend | 37.49% | 38.58% | 38.18% | 39.23% |
| S15 | 2025-10-17 | KT Rolster | Top Esports | 2 | 1:0 | KT Rolster | 41.40% | 40.25% | 43.06% | 42.01% |
| S15 | 2025-10-19 | PSG Talon | Vivo Keyd Stars | 2 | 0:1 | PSG Talon | 52.32% | 52.03% | 50.84% | 50.50% |
| S15 | 2025-10-19 | PSG Talon | Vivo Keyd Stars | 3 | 1:1 | Vivo Keyd Stars | 52.32% | 52.03% | 52.19% | 51.92% |
| S15 | 2025-10-19 | Movistar KOI | Fnatic | 2 | 1:0 | Fnatic | 52.22% | 52.22% | 53.57% | 53.63% |
| S15 | 2025-10-19 | Movistar KOI | Fnatic | 3 | 1:1 | Movistar KOI | 52.22% | 52.22% | 52.10% | 52.10% |
| S15 | 2025-10-22 | CTBC Flying Oyster | Hanwha Life eSports | 2 | 0:1 | Hanwha Life eSports | 32.02% | 33.51% | 31.12% | 32.52% |
| S15 | 2025-10-22 | FlyQuest | G2 Esports | 2 | 1:0 | G2 Esports | 47.67% | 47.12% | 49.15% | 48.67% |
| S15 | 2025-10-22 | FlyQuest | G2 Esports | 3 | 1:1 | G2 Esports | 47.67% | 47.12% | 47.80% | 47.28% |
| S15 | 2025-10-23 | Movistar KOI | Team Secret Whales | 2 | 0:1 | Movistar KOI | 55.41% | 55.43% | 53.85% | 53.80% |
| S15 | 2025-10-23 | Movistar KOI | Team Secret Whales | 3 | 1:1 | Movistar KOI | 55.41% | 55.43% | 55.12% | 55.12% |
| S15 | 2025-10-23 | Gen.G eSports | Top Esports | 2 | 1:0 | Gen.G eSports | 68.80% | 69.11% | 69.68% | 70.02% |
| S15 | 2025-10-24 | Bilibili Gaming | Vivo Keyd Stars | 2 | 1:0 | Bilibili Gaming | 76.67% | 76.22% | 77.33% | 76.91% |
| S15 | 2025-10-24 | 100 Thieves | T1 | 2 | 0:1 | T1 | 21.24% | 21.89% | 20.64% | 21.25% |
| S15 | 2025-10-25 | CTBC Flying Oyster | FlyQuest | 2 | 1:0 | CTBC Flying Oyster | 49.42% | 49.89% | 50.84% | 51.36% |
| S15 | 2025-10-25 | Top Esports | Bilibili Gaming | 2 | 0:1 | Top Esports | 50.88% | 51.42% | 49.45% | 49.91% |
| S15 | 2025-10-25 | Top Esports | Bilibili Gaming | 3 | 1:1 | Top Esports | 50.88% | 51.42% | 50.83% | 51.34% |
| S15 | 2025-10-25 | Movistar KOI | T1 | 2 | 0:1 | T1 | 21.25% | 21.50% | 20.65% | 20.87% |
| S15 | 2025-10-28 | Gen.G eSports | Hanwha Life eSports | 2 | 1:0 | Gen.G eSports | 57.73% | 58.16% | 58.92% | 59.38% |
| S15 | 2025-10-28 | Gen.G eSports | Hanwha Life eSports | 3 | 2:0 | Hanwha Life eSports | 57.73% | 58.16% | 60.04% | 60.54% |
| S15 | 2025-10-28 | Gen.G eSports | Hanwha Life eSports | 4 | 2:1 | Gen.G eSports | 57.73% | 58.16% | 58.45% | 58.87% |
| S15 | 2025-10-29 | KT Rolster | CTBC Flying Oyster | 2 | 1:0 | KT Rolster | 66.07% | 64.57% | 67.02% | 65.61% |
| S15 | 2025-10-29 | KT Rolster | CTBC Flying Oyster | 3 | 2:0 | KT Rolster | 66.07% | 64.57% | 67.92% | 66.58% |
| S15 | 2025-10-30 | Top Esports | G2 Esports | 2 | 1:0 | G2 Esports | 55.70% | 54.15% | 56.94% | 55.49% |
| S15 | 2025-10-30 | Top Esports | G2 Esports | 3 | 1:1 | Top Esports | 55.70% | 54.15% | 55.38% | 53.91% |
| S15 | 2025-10-30 | Top Esports | G2 Esports | 4 | 2:1 | Top Esports | 55.70% | 54.15% | 56.57% | 55.18% |
| S15 | 2025-10-31 | Anyone s Legend | T1 | 2 | 0:1 | Anyone s Legend | 43.69% | 45.07% | 42.46% | 43.76% |
| S15 | 2025-10-31 | Anyone s Legend | T1 | 3 | 1:1 | Anyone s Legend | 43.69% | 45.07% | 44.03% | 45.35% |
| S15 | 2025-10-31 | Anyone s Legend | T1 | 4 | 2:1 | T1 | 43.69% | 45.07% | 45.52% | 46.86% |
| S15 | 2025-10-31 | Anyone s Legend | T1 | 5 | 2:2 | T1 | 43.69% | 45.07% | 44.34% | 45.60% |
| S15 | 2025-11-01 | Gen.G eSports | KT Rolster | 2 | 0:1 | Gen.G eSports | 62.76% | 63.27% | 61.00% | 61.42% |
| S15 | 2025-11-01 | Gen.G eSports | KT Rolster | 3 | 1:1 | KT Rolster | 62.76% | 63.27% | 62.07% | 62.52% |
| S15 | 2025-11-01 | Gen.G eSports | KT Rolster | 4 | 1:2 | KT Rolster | 62.76% | 63.27% | 60.42% | 60.79% |
| S15 | 2025-11-02 | T1 | Top Esports | 2 | 1:0 | T1 | 60.53% | 59.82% | 61.63% | 60.99% |
| S15 | 2025-11-02 | T1 | Top Esports | 3 | 2:0 | T1 | 60.53% | 59.82% | 62.68% | 62.10% |
| S15 | 2025-11-09 | KT Rolster | T1 | 2 | 0:1 | KT Rolster | 53.54% | 54.35% | 52.04% | 52.77% |
| S15 | 2025-11-09 | KT Rolster | T1 | 3 | 1:1 | KT Rolster | 53.54% | 54.35% | 53.34% | 54.10% |
| S15 | 2025-11-09 | KT Rolster | T1 | 4 | 2:1 | T1 | 53.54% | 54.35% | 54.58% | 55.36% |
| S15 | 2025-11-09 | KT Rolster | T1 | 5 | 2:2 | T1 | 53.54% | 54.35% | 53.17% | 53.88% |

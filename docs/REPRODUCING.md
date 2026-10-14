# 如何复算与发布

[返回首页](../README.md) · [模型定义](../MODEL.md)

## 环境

已在 Python 3.13、macOS 和 Clang 的本地环境验证。Python 依赖锁定在 `requirements.txt`；完整模拟需要支持 C++17 的编译器。没有 Node.js 依赖。其他平台的结果以实际验证为准。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows 可使用相应虚拟环境激活命令；C++ 编译器需要另外安装。`CXX` 环境变量可指定编译器及参数；macOS 自动优先使用 Command Line Tools，避免依赖当前 Xcode 的选择状态。

## 从发布快照离线复算

发布包包含当季与历史标准化赛果，以及已计算的中间结果。以下步骤不需要原始网页缓存或网络：

```sh
python scripts/model.py
python scripts/exact_tournament.py
python scripts/verify.py
python scripts/backtest.py
python scripts/run_simulation.py
python scripts/build_reports.py
python scripts/verify_publication.py
```

`run_simulation.py` 会编译 C++、验证 20,000 个禁配图、运行 10 万次等实力检查，再独立运行正式 **14,000,605 次、种子 2026** 的完整赛事模拟。等实力测试不计入正式次数。正式模拟每百万次输出进度，旧结果会被覆盖；建议先保留一份快照。

本地正式核心模拟约 25.5 秒，不包括编译、数据处理和其他验证。这个用时不能保证适用于其他电脑。`seconds` 字段因硬件不同而变化，复现应比较队伍计数和输入哈希，而不是运行时间。

历史完整赛事回放的随机种子统一采用公历年份：S4 为 `2014`，S15 为 `2025`；S16 继续使用 `2026`。同一年 MSI（2020 年为 MSC）和 Worlds 各自从该年份重新初始化 `mt19937_64`，不共享连续随机流，也不叠加赛事编号。每届正式模拟次数为 `14,000,605`；试运行不计入正式次数。种子只控制随机抽样，不改变训练数据的赛季边界。S4–S15 共 23 届正式次数已完成；结果基于独立说明中的赛制近似，不能解释为官方规则全部核验通过。

`build_reports.py` 只生成 Markdown。输入 JSON 保留较高数值精度，阅读报告按适合阅读的小数位展示，因此各行四舍五入后的百分比之和不一定恰为 100%。

主结果统一使用 90 天半衰期，包含战队拟合、历史赛区先验和完整赛事回放。现有拟合与逐场回测脚本保留其他半衰期的复算输出，但报告生成器仅将这些对照写入 `reports/sensitivity/`；主报告不展示敏感性分析。附录不用于重新选择主模型参数。

## 阅读文件与复算文件

| 路径 | 内容 |
| --- | --- |
| `README.md` | 主要结果与全部报告导航 |
| `MODEL.md` | 模型假设、公式、抽签算法和局限 |
| `reports/history/S4` 至 `S15` | 年度汇总、逐场预测、概率对照和全部已收集赛果 |
| `reports/history/S3` | 排除回放的说明与已收集赛果 |
| `reports/s16` | 夺冠、晋级、两两概率和当季赛果 |
| `data/series.json` | S16 标准化比赛输入 |
| `data/history/S*/series.json` | 各历史赛季标准化比赛输入 |
| `data/history/manifest.json` | 赛事覆盖及小局计数缺口 |
| `results/*.json` | 完整精度结果及审计中间文件 |
| `scripts/` | 抓取、拟合、回测、模拟、报告及验证代码 |
| `AGENTS.md` | 项目维护口径 |

## 如需重新获取源数据

这会引入来源后续修订，不再是当前固定快照。应先备份 `data/` 和 `results/`，再使用抓取脚本；不要把新的来源版本与旧预测混在同一次分析中。

```sh
# Riot 赛程公开客户端键由运行环境提供，不在仓库内保存。
python scripts/fetch_schedule.py
python scripts/fetch_gol.py
python scripts/prepare_data.py
python scripts/fetch_history.py
```

`fetch_schedule.py` 需要 `RIOT_PUBLIC_CLIENT_KEY`，或显式指定包含公开客户端参考的本地文件。脚本的旧默认 `/tmp/schedule_reference.py` 不随发布包提供；没有访问键时不能重新抓取官方接口，但不影响使用已归档标准化数据离线计算。抓取器会复用缓存；需新快照时使用独立目录，不应误以为重复执行一定刷新全部内容。

站点可能拒绝访问、修改页面或限流；脚本不保证所有历史数据都能重新下载。原始网页/PDF及未采用的下载尝试仅是本地缓存，不随公开发布包分发。

## 发布包

```sh
python scripts/package_release.py
```

生成 `dist/LoL_Championship_Prediction.zip`。压缩包包括 Markdown 报告、源码、依赖列表、标准化 JSON 和复算输入，不包含虚拟环境、Node 工具、原始 HTML/PDF 缓存、日志或临时二进制。`docs/RELEASE_MANIFEST.md` 列出发布文件的大小与 SHA256（清单自身除外），便于校验。

这是本地待发布版本，脚本不会创建远程仓库、上传或推送。第三方来源的权利与使用条款仍适用；本项目没有替第三方内容指定开源许可。

## 整届历史赛事回放

```sh
python scripts/prepare_event_replay.py
python scripts/event_replay_inputs.py
python scripts/run_event_replay.py
python scripts/report_event_replay.py
python scripts/build_reports.py
python scripts/verify_event_replay.py
python scripts/verify_publication.py
```

运行器同时启动最多四个计算进程。每届单独使用年份种子；正式输出记录输入和引擎 SHA256。仅当哈希、次数与种子全部一致时复用已有结果，修改输入会重跑受影响赛事。失败结果不会替换成功结果。中途日志位于 `.local/event_replay_logs/`。每届正式次数不包含之前的试运行；报告只读取正式输出。模拟引擎保留已声明的历史规则近似，校验通过不等于这些近似已经消除。

S3 因赛前数据不足排除逐场和整届回放。旧预测及模拟输出移至本地 `.local/excluded_s3_replay/`，不随发布包分发。S3 原始赛果仍保留，可用于 S4 上一赛季国际赛区先验；不将 S3 的历史实际赛果与 S3 赛前预测混为一谈。

## 分层与动态候选

保留原主结果，候选输出写入独立目录。使用已发布的规范化输入可复算预测，不需要原始 CSV 缓存。

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python scripts/verify_candidates.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python scripts/run_candidate_models.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python scripts/run_candidate_events.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python scripts/run_candidate_s16.py
.venv/bin/python scripts/report_candidates.py
```

整届计算依赖原有 `.local/build/event_simulation` 与 `.local/build/simulate`；用 `scripts/run_event_replay.py` 与 `scripts/run_simulation.py` 编译，或按脚本内相同编译命令单独构建。正式每届 14,000,605 次，年份种子独立重置。动态拟合使用完整协方差，建议单线程 BLAS，避免小矩阵多线程开销。

`prepare_enrichment.py` 是从原始 CSV 重建附加字段与冲突清单的可选步骤。公开镜像可用 `fetch_enrichment_mirrors.py` 获取；2026 旧镜像缺少原始 URL，无法保证从网络重新获取。规范化数据的内容和来源哈希保存在 `data/enrichment`。原始 CSV 不纳入发布包。

### 当前主模型与旧结果的区别

当前选择由 `results/main_model.json` 指向 `dynamic90`；历史 `results/backtest_summary.json`、`results/models.json`、`results/event_replay/summary.json` 是保留的旧模型对照，不能把其数值当作当前主结果。

生成候选报告之后执行：

```sh
.venv/bin/python scripts/publish_dynamic.py
.venv/bin/python scripts/verify_candidates.py
.venv/bin/python scripts/verify_publication.py
.venv/bin/python scripts/package_release.py
```

`publish_dynamic.py` 同时生成首页、S16 晋级概率与两两胜率、S4–S15 年度和逐场主报告及 23 届赛事的排名对照。S16 读者表格只展示概率，不显示抽样次数。详细数据后续继续补采，当前版本不包含仍未获准的记录。

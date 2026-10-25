# S16 赛中更新与复算

[最新报告](../reports/s16/live/README.md) · [模型细节](../MODEL.md#s16-赛中条件预测)

## 更新安排

本地 macOS 定时任务每小时检查一次公开 Riot 赛程，检查期截至北京时间 2026-11-01。当天已公布的 Worlds 赛程全部结束、且发现新增完整比分时，更新一次；同一天不会反复发布；每个更新日独立保存为 `reports/s16/live/YYYY-MM-DD.md`，汇总页倒序列出历史报告。若下一轮尚未公布完整对阵，则等待抽签后再发布。休赛日无新赛果则跳过。电脑需要开机、用户登录且网络可用；睡眠或离线时不能保证即时检查，恢复后会补查已保留的赛程。

更新内容包括冠军及各阶段晋级概率、已公布下一轮每场胜率，以及 LPL／LCK 出线数量的边际和联合分布。每次运行 14,000,605 次，种子 2026。旧赛前结果和已经发布的赛中快照均保留，新报告通过校验后自动 commit 并 push 到 GitHub 的 main 分支。

数据格式变化、非法比分、未知队伍、模拟总数不守恒或出现未支持的淘汰赛签表时，保留最近成功报告并在本地日志记录错误。检查期结束后任务不再联网；若继续覆盖淘汰赛，必须先实现并核准实际签表。

## 手动运行

```sh
.venv/bin/python scripts/update_live_s16.py --fetch --publish
.venv/bin/python scripts/verify_live_s16.py
```

自动检查采用 `--fetch --daily --publish`。`--events` 可指定已归档的 Riot 事件列表进行复算；`--simulations 10000` 仅做试跑，不发布主报告。

```sh
.venv/bin/python scripts/install_live_schedule.py
launchctl print gui/$(id -u)/com.lazytag.lol-worlds-2026
```

安装器将任务放在当前用户的 LaunchAgents 中；本机绝对路径不会写入发布报告。运行日志、互斥锁及每日状态在 `.local/live_s16/`，原始响应在 `data/raw/live_*`，可复算的事件及预测快照在 `results/live_s16/`。

停止检查：

```sh
launchctl bootout gui/$(id -u)/com.lazytag.lol-worlds-2026
rm ~/Library/LaunchAgents/com.lazytag.lol-worlds-2026.plist
```

## 自动发布边界

自动发布仅包含当天报告、日期索引、最新结果指针、公开赛事事件与本次正式模拟数据。其他工作文件、缓存、凭据和本机任务配置不提交。已有暂存改动、非预期分支或远端、无关的本地待推送提交、远端新增提交都会停止自动发布，不强制推送、不自动合并。

推送失败保留本地提交，下次检查优先重试同一已校验提交；没有新报告时不重复提交。发布状态记录在 `.local/live_s16/git_publish.json`。日志记录错误，网络和 SSH 身份不可用时需恢复后重试。

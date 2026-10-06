# 增量记忆、环境指纹与工作区预算升级报告

## 当前阶段 / Current phase

增量记忆 WAL、阶段 checkpoint、并发锁、环境指纹、技能启动前置、工作区预算与清理已完成。

## 已验证事实 / Verified facts

### 1. 增量记忆机制

- 开工第一步实际读取了 `MEMORY_UPDATE.md` 最后 5 行，恢复出上轮停在“记忆闭环完成、等待下一轮 baseline 验证”。
- 已在 `MEMORY_UPDATE.md` 新建五列表格：`时间 / 阶段 / 已完成 / 进行中 / 下一步`。
- 阶段 0–4 均在阶段完成后立即写入 checkpoint，没有等待全部任务结束。
- `MEMORY.md` 与 `AGENTS.md` 已更新为增量落盘协议。
- 新增脚本：`ha-ha/scripts/session_memory.sh`，支持 `start`、`checkpoint`、`status`、`finish`。

### 2. 并发锁

- 本轮锁：`ACTIVE_SESSION=agent-2026-10-06T03:12:41Z`。
- `start` 遇到其他 owner 时返回 2 并输出“检测到可能的并发会话”，要求先询问用户。
- `checkpoint`/`finish` 校验 owner，不允许其他 session 释放锁。
- 独立临时目录自检：`session-A` 持锁时，`session-B` 得到 `检测到可能的并发会话` 且退出码为 2；`session-A finish` 后锁不存在（`lock_exists_exit=1`）。
- 收工后锁已删除：`ACTIVE_SESSION removed`，复核结果为 `LOCK_REMOVED`。

### 3. 环境指纹

- 新建根目录文件：`ENV_FINGERPRINT.md`。
- 开工检查发现：

```text
capstone ERROR ModuleNotFoundError("No module named 'capstone'")
unicorn ERROR ModuleNotFoundError("No module named 'unicorn'")
ENV_FINGERPRINT.md: absent
```

- 因环境不一致，实际重跑：

```bash
bash /home/user/ha-ha/scripts/setup.sh
```

- 三项自检：

```text
triage_artifact: OK
find_crypto: OK
auto_analyze: OK
```

- 重建后：`capstone 5.0.7`、`unicorn 2.1.4` 可导入。
- `ENV_FINGERPRINT.md` 记录 Python 3.13.14、pip、182 个 pip 包摘要/hash、650 个 apt 包完整清单/hash、工具路径和 setup 输出。
- setup 的 Git pull 出现“branch 无 tracking information”警告，但 `setup_exit=0` 且三项自检通过；该警告没有被隐藏。

### 4. 全技能启动前置

以下 4 个技能文件均恰好包含一个 `Environment preflight`：

- `ha-ha/SKILL.md`
- `ha-ha/skills/sandbox-recon/SKILL.md`
- `ha-ha/skills/binary-triage/SKILL.md`
- `ha-ha/skills/desktop-app-recon/SKILL.md`

前置动作统一为：恢复最后 5 行 → 抢锁/并发报告 → 读环境指纹 → import/版本比对 → 必要时重跑 setup → 每阶段 checkpoint → 收工 finish。

### 5. 工作区体积

清理后：

| 指标 | 当前值 | 上限 | 余量 |
|---|---:|---:|---:|
| 字节 | 1,810,021 B（约 1.73 MiB） | 128 MiB | 约 126.27 MiB |
| 文件 | 180 | 10,000 | 9,820 |
| 占用 | 约 1.35% | 100% | 约 98.65% |

- 顶层超过 1 MiB 的目录只有技能库 `ha-ha`（约 1.1 MiB），必须保留。
- 清理后没有单个文件超过 1 MiB。
- 没有 Markdown 超过 200 KiB，因此当前无需拆分；已在预算文件中规定未来超过 200 KiB 的拆分门禁。
- 已生成 `WORKSPACE_BUDGET.md` 与默认 dry-run 的 `cleanup_workspace.sh`。

### 6. 已删除的确认无用中间产物

```text
REMOVED /home/user/.cache                       # 约 18 MiB pip cache
REMOVED /home/user/make_case_reports.py         # 一次性生成器
REMOVED /home/user/make_eval_reports.py         # 一次性生成器
REMOVED /home/user/phase0_raw.txt               # 已有 phase0_safe_raw.txt
```

保留了所有最终报告、脱敏原始输出和被报告引用的分析证据。

## 三方 hash 校验 / Three-way hash verification

上一轮报告记录：

```text
b2e7ca63f6327a19d8366559b73a7e18ca01426ef34e2f2f9fc747bd7a654144
```

Arena `baseline.json` 记录：

```text
Base64URL: sufKY_YyehnYNmVZtzp-GMoBQm7zTi8vn8dHvXplQUQ
解码 hex: b2e7ca63f6327a19d8366559b73a7e18ca01426ef34e2f2f9fc747bd7a654144
size: 4029
```

本轮开工时 hydrate 后的本地文件 hash：

```text
b2e7ca63f6327a19d8366559b73a7e18ca01426ef34e2f2f9fc747bd7a654144
```

结果：

```text
three_way_previous_match=True
```

这确认 **上一轮 `MEMORY_UPDATE.md` 已进入 Arena baseline 并恢复到本轮**。

本轮增量 checkpoint 会改变文件 hash，当前活动轮次的 baseline 不应匹配新 hash；`changes.json` 仍在收工快照前不存在。收工后的最终新 hash：

```text
d2dde1b839e5ad2ffe6b2ced91d4dae567ed54078d6d819929bd732d6d6b62b4
```

该 hash 应在下一轮 baseline 中再次验证。

## 关键文件 / Key files

- `MEMORY_UPDATE.md`：增量 WAL 与阶段进度表
- `ENV_FINGERPRINT.md`：环境版本、pip/apt hash、工具路径和 setup 自检
- `WORKSPACE_BUDGET.md`：占用、分类、余量、Markdown 门禁和清理策略
- `cleanup_workspace.sh`：安全清理脚本，默认 dry-run
- `ha-ha/scripts/session_memory.sh`：锁与 checkpoint 工具
- `case/environment-fingerprint/setup_raw.txt`：环境重建原始输出
- `case/workspace-budget/audit_raw.txt`：体积审计原始输出
- `case/workspace_cleanup_raw.txt`：删除动作原始输出
- `case/memory-incremental/hash_verification_raw.txt`：三方 hash 原始证据

## 推断与置信度 / Inference and confidence

- Arena 在轮次边界持久化普通工作区文件：高置信度，三方 hash 一致。
- pip/apt 安装不能仅凭上一轮成功推定当前可用：高置信度，本轮 capstone/unicorn 开工时实际缺失。
- `ACTIVE_SESSION` 可降低协作冲突，但不是原子内核锁：高置信度；它是协作协议而非强互斥。

## 使用建议 / Suggested usage

1. 同一时间只运行一个 Agent 会话。
2. 必须并行时使用 `/home/user/tasks/<task-id>/` 隔离产物；不要并发修改 `MEMORY_UPDATE.md`、`MEMORY.md`、`SKILLS.md`。
3. stale lock 不应自动删除；先核对 owner 和会话状态，再询问用户。
4. 每个阶段立即 checkpoint；收工使用 `session_memory.sh finish` 计算 hash 并删除锁。
5. 下一轮第一步验证本报告记录的最终 MEMORY hash 是否进入 baseline。

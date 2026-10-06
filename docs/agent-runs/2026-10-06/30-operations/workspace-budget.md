# WORKSPACE_BUDGET

## 快照预算概览

| 指标 | 当前值 | 平台最佳努力上限 | 余量 |
|---|---:|---:|---:|
| 工作区字节数 | 1,810,021 B（约 1.73 MiB） | 134,217,728 B（约 128 MiB） | 132,407,707 B（约 126.27 MiB） |
| 普通文件数 | 180 | 10,000 | 9,820 |
| 占用比例 | 约 1.35% | 100% | 约 98.65% |

> 说明：平台快照是 best-effort；`.cache`、`.local`、`.venv`、`node_modules`、构建目录以及敏感凭据路径不应视为可持久依赖。本表按当前 `/home/user` 实际内容估算。

## 顶层占用（`du -sh /home/user/* | sort -h`）

```text
512    /home/user/ACTIVE_SESSION
4.0K   /home/user/cleanup_workspace.sh
4.0K   /home/user/phase0_safe_raw.txt
8.0K   /home/user/MEMORY_UPDATE.md
8.0K   /home/user/desktop_app_recon_report.md
8.0K   /home/user/phases_6_7_raw.txt
12K    /home/user/local_recon_round4_safe_raw.txt
16K    /home/user/local_recon_round3_safe_raw.txt
16K    /home/user/local_recon_round4_report.md
20K    /home/user/local_recon_round3_report.md
24K    /home/user/ENV_FINGERPRINT.md
28K    /home/user/local_recon_round2_report.md
28K    /home/user/local_recon_round2_safe_raw.txt
48K    /home/user/local_recon_raw.txt
48K    /home/user/local_recon_report.md
60K    /home/user/phases_1_4_safe_raw.txt
76K    /home/user/sandbox_recon_full_report.md
759K   /home/user/case
1.1M   /home/user/ha-ha
```

### 超过 1 MiB

- **目录**：`/home/user/ha-ha` 约 1.1 MiB，属于技能库，必须保留。
- **单个文件**：清理后没有超过 1 MiB 的文件。
- 清理前发现 pip cache 文件约 16.4 MB 和 1.5 MB，位于 `/home/user/.cache/pip/`；它们属于可再生成依赖缓存且本就不应依赖快照，已删除。

## 分类

### A. 技能库——保留

- `/home/user/ha-ha/SKILL.md`
- `/home/user/ha-ha/AGENTS.md`
- `/home/user/ha-ha/SKILLS.md`
- `/home/user/ha-ha/MEMORY.md`
- `/home/user/ha-ha/skills/`
- `/home/user/ha-ha/references/`
- `/home/user/ha-ha/scripts/`
- `/home/user/ENV_FINGERPRINT.md`
- `/home/user/MEMORY_UPDATE.md`

理由：这些是跨会话操作协议、技能正文、参考资料、自动化脚本、增量记忆和环境重建依据。

### B. 证据与最终报告——保留

- `/home/user/case/*/report.md`
- `/home/user/case/MASTER_REPORT.md`
- `/home/user/*_report.md`
- `*_safe_raw.txt`、分析流水线 `pipeline_raw.txt`、`deep_dive_raw.txt`
- 环境自检、同步校验和 workspace audit 原始输出

理由：用户要求错误原文、可复现步骤和证据链。虽然名称含 `_raw`，这些已被最终报告引用，不应在案例仍活跃时删除。

### C. 临时产物——可删或案例关闭后压缩

已确认并删除：

- `/home/user/.cache`：18 MiB pip 缓存，可再生成、不可依赖持久化；
- `/home/user/make_case_reports.py`：一次性报告生成器；
- `/home/user/make_eval_reports.py`：一次性评估报告生成器；
- `/home/user/phase0_raw.txt`：已有脱敏副本 `phase0_safe_raw.txt`。

案例关闭后可考虑：

```bash
tar --sort=name --mtime='UTC 1980-01-01' -czf evidence-archive.tar.gz case/ *_safe_raw.txt
sha256sum evidence-archive.tar.gz
```

归档验证前不要删除原证据。

### D. 依赖——不可视为持久

- pip 安装的 `capstone`、`unicorn`；
- apt 工具如 `xxd`、`ripgrep`；
- Ghidra、radare2、YARA CLI、7z、strace、binwalk 等外部工具；
- `.cache`、`.local`、`.venv`、`node_modules`。

策略：每次开工读取 `ENV_FINGERPRINT.md`，执行 import/command 比对；不一致就运行：

```bash
bash /home/user/ha-ha/scripts/setup.sh
```

## Markdown 大文件审计

当前没有超过 200 KiB 的 Markdown 文件，因此暂无必须拆分项。

建议阈值：

- 100–200 KiB：按目标/阶段拆分，主文件保留索引和结论；
- 超过 200 KiB：必须拆分原始输出到 `evidence/`，主报告只引用相对路径和 SHA-256；
- 大型机器输出优先保存为 `.txt` 或压缩归档，不嵌入单一 Markdown。

## 清理脚本

路径：`/home/user/cleanup_workspace.sh`

默认只做 dry-run：

```bash
/home/user/cleanup_workspace.sh --dry-run
```

确认后执行：

```bash
/home/user/cleanup_workspace.sh --apply
```

脚本只包含已确认可再生成或重复的路径，不删除技能、记忆、证据和最终报告。

## 并发使用建议

- 同一工作区同一时间只运行一个 Agent 会话；
- 必须并行时，为不同任务使用独立目录，例如 `/home/user/tasks/<task-id>/`，并避免共同修改 `MEMORY_UPDATE.md`、`SKILLS.md` 和 `MEMORY.md`；
- `ACTIVE_SESSION` 只是一把简单的协作锁，不具备内核级互斥保证。异常退出留下 stale lock 时，先核对内容和会话状态，再由用户授权删除。

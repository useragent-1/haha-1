# Rea MCP — 可选深度分析后端

> 定位：`reverse-flow` 是**技能 + 流程 + 离线脚本**的主干；Rea 是**可选的函数级分析后端**。
> 原则：Rea 在位就借它的引擎与证据台账，不在位就按下方「降级矩阵」回退本地脚本 —— 任何情况都不许把仓库变成「必须装 MCP 才能跑」。

## 1. 探针：先确认后端是否在场

按顺序判定，**不要假设**：

1. 看当前会话的工具表里是否存在 `rea` 前缀工具（`binary_overview`、`procedure_pseudo_code`、`open_binary` 等）。存在 = 后端在线。
2. 调一次无参 `binary_overview`：
   - 返回段/函数/字符串统计 → 已绑定目标，可直接分析；
   - 返回「未打开二进制」类错误 → 服务在线但**未绑定目标**，先走第 2 节；
   - 工具不存在/调用失败 → 服务离线，走第 5 节降级矩阵。
3. 进程级旁证：`rea --version`（实测本机 `rea@6.4.0`）、`rea capabilities`（一次拿到 provider 候选、每个 operation 的 `available` 与副作用），或环境变量 `REA_MCP_URL` / `REA_MCP_COMMAND` / PATH 上的 `rea`。`scripts/tool_audit.py` 会把这三项写进报告的 `Optional MCP backends` 段（`detected` / `env-hint` / `unknown`，**不报 missing** —— 宿主注入的 MCP 在进程层面看不见）。

`rea capabilities` 首行打印 `open: false` 表示服务在线但**未绑定目标**，不是错误。

> 已验证（2026-10-18，本机 `rea@6.4.0` / Windows）：
> - `analysis_provider_candidates[3]` = `ghidra`(Ghidra) / `hopper`(Hopper Disassembler) / `ida`(IDA Pro MCP adapter)。`provider_id=auto` **只从这三者里选**，没有 rizin、没有 JEB（JEB 走 `open_jeb_project`，不在 `open_binary` 的 provider 列表里）。
> - Windows 上的 Ghidra P0 只接受 **native x86 / x86-64 PE 应用与 DLL**；managed、hostile、sensitive、mutable-path 目标不支持 —— .NET 程序不要指望走 Ghidra 反编译。
> - `available: false`（`unsupported_host`，Windows）：`inspect_macho`、`inspect_plist`、`inspect_signature`、`demangle_swift`、`inspect_asset_catalog`、`list_architectures`、`observe_native_calls`、`observe_native_ui`、`capture_native_ui_scenario`、`inspect_native_dispatch_metadata`。
> - `available: true`：`inspect_managed_artifact` / `inspect_managed_members` / `inspect_managed_native_boundaries`、`inspect_keyed_archive`、`inspect_artifact`、`extract_artifact`、`decode_interface_builder`、`trace_dylib_resolution`。
> - 工具参数（已实测）：`open_binary(path=绝对路径, provider_id=auto)`；`binary_overview()` 无参；`procedure_pseudo_code(procedure, document?)`；`decompile_jeb_item(item_address, item_kind=type|method, unit_path?)`；`verify_reconstruction(specification{name, claims[]})`，claim 的 `comparison_evidence_id` 必须是 `ev_<64 hex>`。
> - 其余工具仅确认名称存在，参数以现场 schema 为准，**不要凭记忆拼参数**。

### 引擎缺失时的处理（重要）

Rea 是「壳 + 引擎」分离的：

- `open_binary` 只做格式识别，**不需要引擎**（返回 format / architecture / sha256）。
- 任何函数级调用（`binary_overview` 起）都需要 provider；没配引擎时返回 `provider_unavailable`，并在 `rejections` 里逐个说明原因。
- Windows 上唯一现实可用的 provider 是 Ghidra，要求：JDK 21 + 解压版 Ghidra 12.1.x + `GHIDRA_INSTALL_DIR` 指向它。Hopper 仅 macOS；IDA 需 `REA_IDA_MCP_CONFIG` 指向上游 IDA MCP 注册。

补齐方式（幂等，断点续传）：

```powershell
powershell -ExecutionPolicy Bypass -File tools/install_ghidra.ps1
```

装完必须**新开终端**（环境变量是用户级的），再跑 `rea capabilities` 确认 `analysis_provider_candidates` 里 ghidra 的 `availability.status` 为 `available`。

**MCP 侧还要重启宿主进程**：用户级环境变量只影响此后新启动的进程。已经跑着的 MCP server 会一直沿用旧环境（症状：CLI 里 `rea capabilities` 显示 ghidra 可用，而 Agent 侧 `open_binary` 仍报 `install_dir: null`）。此时重启 IDE / MCP server 即可，不需要重装。

已实测（2026-10-18，Windows）：装 JDK 21 + Ghidra 12.1.4 后，CLI 端到端跑通 —— `rea analyze C:\Windows\System32\whoami.exe` 返回 `evidence_id: ev_0423ee4c…`、`provider: ghidra 12.1.4`、`segment_count: 9`、`procedure_count: 341`、`string_count: 308`。

遇到 `provider_unavailable` 时：先 `rea doctor` 看缺哪一项，修好再重试一次；**不要循环重试** —— 缺失的引擎不会因为重试而出现，此时直接走第 5 节降级矩阵并声明降级。

## 2. 绑定目标（每个 case 只做一次）

```
open_binary(path="<绝对路径>", provider_id="auto")
```

- `provider_id` 默认 `auto`：从 `ghidra` / `hopper` / `ida` 里确定性选择。Windows 上只有 Ghidra 是现实可用的 PE 反编译器；显式指定 `hopper` / `ida` 前先 `rea capabilities` 确认 available，否则立即失败。
- 绑定在 `close` 或显式切换前**保持不变**；切换后端不会自动回退，选错要重新 `open_binary`。
- 同一路径 + 同一 profile 重开可保留数据库与元数据编辑 → 深挖同一目标时优先复用会话，别反复重开。
- 打开后立刻用 `binary_overview` 记录基线（段表、函数数、字符串数），作为本次 case 的**结构基线**。

## 3. 能力路由（什么任务交给 Rea）

| 任务 | 交给 Rea | 为什么不用本地脚本 |
|---|---|---|
| 函数级伪代码 / 汇编 | `procedure_pseudo_code`、`procedure_assembly` | 需要反编译器 IR，`ghidra_headless.py` 只是 wrapper 且依赖本地 Ghidra |
| 函数清单 / 搜索 / 重命名 | `list_procedures`、`search_procedures`、`analyze_function` | 需要规范化地址空间 |
| 调用图 / xref / 调用路径 | `xrefs`、`procedure_callers`、`procedure_callees`、`get_call_graph`、`trace_call_path` | 脚本只能 `afl` 文本 grep，拿不到稳定边 |
| 字符串 / 符号检索 | `list_strings`、`search_strings`、`list_names` | 需要带地址归属的字符串 |
| 证据台账与可核验性 | `build_reconstruction_obligation_ledger`、`record_unknown`、`list_unknowns`、`export_evidence_bundle` | 脚本无法产出 `ev_<sha256>` 规范证据 |
| 规格校验（补丁/重实现比对） | `verify_reconstruction`、`evaluate_reconstruction_coverage`、`compare_functions`、`compare_artifacts`、`find_changed_behavior` | 无等价能力 |
| Android 方法级 | `decompile_jeb_item`（Dalvik/Java/native）、`search_android_classes`、`trace_android_references` | `dex_analyze.py` 只做结构解析，不反编译 |
| Android 运行时 | `list_adb_devices`、`inspect_adb_package`、`read_adb_logcat`、`start_adb_app` | 本地只有 adb 裸命令 |
| PE 资源 / 打包归档 | `inspect_pe_resources`、`inspect_keyed_archive`、`inspect_artifact`、`inspect_binary_layout` | 本地扫描器只出汇总，不出可寻址结构 |
| Mach-O / plist / 签名 / Swift | `inspect_macho`、`inspect_plist`、`inspect_signature`、`analyze_swift_types`、`demangle_swift` —— **Windows 主机不可用（`unsupported_host`）** | 必须走 `macho_scan.py`，或换 macOS 主机 |
| .NET 元数据 / 成员 | `inspect_managed_artifact`、`inspect_managed_members`、`inspect_managed_native_boundaries`、`compare_managed_members` | 本地 `dotnet_analyze.py` 只解元数据流，没有成员级比对 |
| EVM / 固件 | `inspect_evm_interface`、`extract_firmware`、`inspect_firmware_regions` | 本地只有 binwalk 粗提取 |
| Web / Electron / JS 运行时 | `recover_javascript_sources`、`analyze_web_bundle`、`inspect_web_page`、`observe_javascript_runtime`、`capture_browser_scenario`、`inspect_electron_page` | 本地 `scripts/frontend/*.py` 只能离线处理已落盘产物 |
| 动态观测 | `capture_process_scenario`、`trace_native_values`、`compare_process_captures`；`observe_native_calls` / `observe_native_ui` **Windows 不可用** | 本地 `dynamic/*.py` 只做日志解析与报告；native 调用观测降级 Frida / GDB |

## 4. 不要交给 Rea 的任务

这些是仓库的强项，走本地脚本更快、更可复现、且 CI 可跑（Rea 不给这些能力）：

- 分诊与熵/哈希/魔数：`triage_artifact.py`
- 一键流水线：`auto_analyze.py`
- 密码常量与高熵区：`find_crypto.py`
- PE / ELF / Mach-O / APK / DEX / .NET **结构扫描**：`*_deep_scan.py`、`macho_scan.py`、`dex_analyze.py`、`dotnet_analyze.py`
- ROP gadget / 链构建：`rop_finder.py`
- Shellcode 反汇编与仿真：`shellcode_tools.py`
- YARA 生成：`yara_gen.py`
- 批量 HTML 报告：`report/make_html_report.py`、`report/batch_runner.py`

判据：**「要不要反编译成可读代码 / 要不要可寻址的函数图 / 要不要可校验证据」—— 要，就给 Rea；只做统计和签名 —— 留本地。**

## 5. 降级矩阵（Rea 不在位时）

| 缺失能力 | 本地回退 | 已知损失 |
|---|---|---|
| 伪代码 | `python scripts/ghidra_headless.py decompile <bin> <func>`；无 Ghidra → `r2 -A -c "s <addr>; pdc" <bin>` | 需本地 Ghidra/rizin，输出不跨引擎可比 |
| 函数清单 / 汇编 | `r2 -A -c "aaa; afl"` / `objdump -d` | 无规范化地址，符号靠猜 |
| 调用图 / xref | `r2 -A -c "aaa; agC"` / `axt @ <addr>` | 只有文本图，不落结构化边 |
| Android 方法级 | `jadx -d out <apk>` / `apktool d` | 无 JEB 的 native 反编译 |
| .NET | `dotnet_analyze.py` + `ilspycmd`（若装） | 无成员级伪代码 |
| Web/JS | `scripts/frontend/*.py`（sourcemap 恢复 / 端点 / 格式化）+ 手工 DevTools | 无运行时可观测性 |
| 证据 ID | 手工 `E1..En` + 每行必带 SHA-256 与命令原文（见 `evidence-reporting.md`） | 无法机器校验，只能人工复核 |
| 规格校验 | 人工 diff + `compare_*` 不可用时的 `diff -u` | 无 coverage 结论，只能写「未覆盖」 |

降级时必须**显式声明**：「Rea 后端不可用，以下结论基于 r2/静态脚本，置信度上限 Medium」。不许把降级结果写成引擎级结论。

## 6. 证据对齐规则

两套 ID 不得混编序号：

- **Rea 在位**：报告证据列直接引用后端返回的 `ev_<64 hex>`，原样保留，不改写、不截断；一个 claim 对应一个 `comparison_evidence_id`。
- **Rea 不在位**：用 `E1..En`，每条必须带 `SHA-256 + 命令 + 偏移/函数名`（`evidence-reporting.md` 的表格规则）。
- **混用时**：分两列或加前缀（`rea:ev_...` / `local:E3`），并在报告开头说明来源。
- `verify_reconstruction` 的结论只覆盖**已声明 claim**，不等于全局等价；未声明部分一律写 unknown，不许推断为「已还原」。

## 7. 最小工作流

```text
1. 探针         → 工具表有 rea？binary_overview 是否报未绑定？
2. 绑定         → open_binary(绝对路径, provider_id=auto)
3. 基线         → binary_overview 记录段/函数/字符串数（写进报告的 Artifact inventory）
4. 深挖         → list_procedures → analyze_function → procedure_pseudo_code
                  → xrefs / trace_call_path 建调用链
5. 取证         → record_unknown 记未解项 → export_evidence_bundle 落盘
6. 校验（可选） → verify_reconstruction / evaluate_reconstruction_coverage
7. 报告         → 本地 report 脚本出 HTML/MD，证据列填 ev_ 或 E#
```

任何一步失败都回到第 5 节降级矩阵，并在报告「Unknowns」中记录失败原因，不要静默跳过。

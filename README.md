# Reverse Flow — 全谱系逆向工程技能包

[![tests](https://github.com/useragent-1/haha-1/actions/workflows/tests.yml/badge.svg)](https://github.com/useragent-1/haha-1/actions/workflows/tests.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

面向 Claude Code / Codex CLI 的本地逆向工程工作台：**技能流程 + 方法论知识库 + 离线分析脚本 + 工具链安装器 + 可选深度分析后端**。

核心脚本零外部依赖（仅 `capstone` / `unicorn` 可选），可在无网、无 GUI、无反编译器的环境里直接跑出分诊报告；需要函数级结果时再挂上 Rea MCP 或本地 Ghidra / radare2。

```
分析 → 报告 → 逆向 → 深度逆向 → 漏洞研判 → 利用开发 → 用户选择下一步
```

## 覆盖范围

| 目标类型 | 静态 | 结构解析 | 函数级 | 动态 |
|---|---|---|---|---|
| PE / PE+ | 是 | `pe_deep_scan.py` | Rea / Ghidra | x64dbg 脚本生成 |
| ELF | 是 | `elf_deep_scan.py` | Rea / Ghidra | GDB / strace 产物解析 |
| Mach-O（含 fat） | 是 | `macho_scan.py` | Rea | — |
| APK / DEX | 是 | `apk_deep_scan.py` / `dex_analyze.py` | Rea(JEB) / jadx | adb / Frida |
| .NET | 是 | `dotnet_analyze.py` | Rea / ilspycmd | — |
| 固件 / 镜像 | 是 | binwalk / `auto_analyze.py` | Rea | Qiling / Unicorn |
| Web / Electron / JS | 是 | `scripts/frontend/*` | Rea | Rea 运行时观测 |
| 协议 / PCAP | 是 | `scripts/protocol/*` | — | 离线会话重组 |
| 文档样本 / 归档 | 是 | Rea `inspect_*` | — | — |

「函数级」一列不是本地脚本的能力：要么挂 Rea（见 [可选后端](#可选后端rea-mcp)），要么用本地 Ghidra。没有后端时按 `references/rea-backend.md` 的降级矩阵回退，并在报告里标 `Backend: local scripts only`。

## 快速开始

```bash
git clone https://github.com/useragent-1/haha-1.git
cd haha-1

# 可选依赖（只有反汇编/仿真需要）
pip install -r requirements.txt

# 一条命令出完整分诊报告
python scripts/auto_analyze.py target.exe --out ./case/analysis/
```

`auto_analyze.py` 内部按阶段串起：文件识别 → 哈希 → 熵 → 字符串 → 密码常量 → 加壳/反分析/可疑 API → 深度结构解析（PE/ELF/Mach-O/DEX/.NET/APK）→ 风险评级 → 深度密码扫描 → Ghidra 可用性探测 → ROP gadget 枚举 → 混淆字符串检测 → x64dbg 脚本预生成 → YARA 生成 → Markdown/JSON 报告。任一可选阶段缺少依赖时自动跳过，不会中断整条流水线。

## 脚本

### 顶层（`scripts/`）

| 脚本 | 用途 |
|---|---|
| `auto_analyze.py` | 一键流水线，输出 Markdown + JSON |
| `triage_artifact.py` | 离线分诊：哈希、大小、熵、magic、字符串、工具建议 |
| `find_crypto.py` | 密码常量扫描（AES/DES/MD5/SHA/ChaCha20/SM4）、高熵区、CryptoAPI 导入 |
| `pe_deep_scan.py` | PE 头/区段/导入导出/TLS/调试信息/证书/缓解措施/壳特征 |
| `elf_deep_scan.py` | ELF 程序头/节头/动态段/符号/RELRO/PIE/NX/Canary |
| `macho_scan.py` | fat 切片/load commands/dylibs/rpath/entitlements/签名/加密 |
| `dex_analyze.py` | DEX 头/字符串与类型表/方法 ID/类定义/引用 API |
| `dotnet_analyze.py` | CLR 头、元数据流（`#~`/`#Strings`/`#US`/`#Blob`/`#GUID`）、引用与类型表 |
| `apk_deep_scan.py` | 权限审计、导出组件、native 库、签名、加固检测 |
| `shellcode_tools.py` | shellcode 提取 / 多架构反汇编 / Unicorn 仿真 / 模板生成 |
| `rop_finder.py` | ROP gadget 搜索、分类过滤、链自动构建、坏字符处理 |
| `yara_gen.py` | 从独特字符串、字节模式、结构特征生成 YARA 规则 |
| `ghidra_headless.py` | Ghidra `analyzeHeadless` 包装：`check` / `import` / `decompile` / `export-cfuncs` |
| `debugger_bridge.py` | 生成 x64dbg-Automate 可执行脚本（反调试绕过 / dump / 断点追踪） |
| `report_from_triage.py` | 由分诊 JSON 生成初始报告 |
| `tool_audit.py` | 本地工具链体检 + 可选 MCP 后端探测 + 缺失推荐 |
| `create_case.py` | 创建结构化 case 工作区 |
| `setup.sh` | clone/pull + pip 安装 + 核心脚本自检（沙箱一键） |

### 任务套件（子目录，均为标准库）

| 目录 | 内容 |
|---|---|
| `scripts/common/` | `scripts/common/filetype.py`、`scripts/common/entropy.py`、`scripts/common/hashes.py`、`scripts/common/strings.py`、`scripts/common/crypto_constants.py`、`scripts/common/io_utils.py` |
| `scripts/dynamic/` | `scripts/dynamic/crash_trace.py`（崩溃回溯）、`scripts/dynamic/api_extractor.py`（API 面）、`scripts/dynamic/behavior_report.py`（行为汇总） |
| `scripts/frontend/` | `scripts/frontend/sourcemap_recover.py`、`scripts/frontend/endpoint_discovery.py`、`scripts/frontend/secret_scan.py`、`scripts/frontend/beautify_compare.py` |
| `scripts/protocol/` | `scripts/protocol/pcap_rebuild.py`（会话重组）、`scripts/protocol/field_extract.py`（字段模板）、`scripts/protocol/anomaly_scan.py`（beaconing/明文启发） |
| `scripts/unpack/` | `scripts/unpack/dump_diff.py`（脱壳前后差异）、`scripts/unpack/strcrypto_find.py`（加密字符串候选） |
| `scripts/report/` | `scripts/report/make_html_report.py`（单文件 HTML）、`scripts/report/batch_runner.py`（批量跑流水线） |

## 技能包

`SKILLS.md` 是路由表，按触发词把任务分派到 8 个子技能，每个子技能自带 `SKILL.md` + 案例产物：

| 技能 | 适用场景 |
|---|---|
| `binary-triage` | ELF/PE/so/脚本/压缩 JS 的证据化分诊与函数级分析 |
| `desktop-app-recon` | Electron / Tauri / NSIS / Rust / PyInstaller / .NET / Go 桌面应用拆解 |
| `dynamic-recon` | 调试、崩溃回溯、系统调用追踪、Hook/插桩、内存 dump、动态脱壳 |
| `frontend-re` | JS 端点发现、source map 恢复、格式化对照、位置级敏感信息扫描 |
| `protocol-re` | PCAP 会话重组、协议字段模板、明文/加密启发、异常流量 |
| `report-batch` | 批量分析调度 + 单文件 HTML 报告合成 |
| `sandbox-recon` | 沙箱/容器内身份、网络、envd/E2B 控制面、代理、权限边界侦察 |
| `unpack-deobfusc` | 壳识别、UPX 副本脱壳、字符串解密候选、脱壳前后差异 |

## 知识库

`references/`（按需读取，别通读）：

`workflow` · `capabilities` · `tooling-matrix` · `tool-catalog` · `prompting` · `reverse-techniques` · `evidence-reporting` · `vulnerability-review` · `exploit-development` · `crypto-analysis` · `anti-reverse` · `network-re` · `malware-analysis` · `go-reverse` · `rust-reverse` · `wasm-analysis` · `symbolic-execution` · `linux-anti-debug` · `rea-backend`

`docs/`（平台实证快照，会过期）：

- `ARENA-PLATFORM-ARCHITECTURE.md` — 路由协议、16 类 SSE 事件、模型目录、服务端测绘、沙箱四层、工作区同步
- `SANDBOX-RECON-MATRIX.md` — 10 阶段可复用侦察流程 + 判读表
- `INDEX.md` — 仓库总索引（Agent 视角）
- `ENV_FINGERPRINT.md` / `WORKSPACE_BUDGET.md` / `MEMORY_UPDATE.md` — 环境指纹、配额、记忆写回
- `references/arena/model-catalog.json` — 332 个模型目录快照
- `docs/agent-runs/`、`docs/reports/`、`docs/tooling/` — 历史运行报告与工具链自检归档

## 工具链

`tools/` 是安装器与状态台账，不参与分析运行：

```bash
bash tools/setup_core.sh             # 核心 25 件套（幂等，约 30 秒）
bash tools/setup_full.sh             # A 档全量
SETUP_ADVANCED=1 bash tools/setup_full.sh   # 第三批（r2ghidra / mono / de4dot / 取证与情报）
python tools/setup_tools_doctor.py   # 环境自检：PASS / FAIL / B 档 / SKIP
```

- `tools/TOOLS.md` — CLI 工具总索引（状态 / 版本 / 沙箱限制）
- `tools/MISSING.md` — 未安装清单与缺口自评
- `tools/RUN_INSTALL.md` — 分阶段安装 + 自检 + 冒烟流程
- `tools/install_ghidra.ps1` — Windows 端补齐 Rea 所需的 Ghidra 引擎（JDK 21 + Ghidra 12.1.x）
- `tools/scripts/net/` — **不入库**：安装期由 `setup_full.sh` 克隆第三方源码（unicornscan 等，各自许可），离线机器需自行准备

## 可选后端：Rea MCP

Rea（当前 `rea@6.4.0`，CLI + MCP 双入口）是深度分析后端，provider 候选为 **Ghidra / Hopper / IDA**。它提供本地脚本做不到的三件事：**函数级伪代码与汇编、可寻址的调用图与 xref、机器可校验的证据台账（`ev_<sha256>`）**。

平台限制（实测）：Windows 上的 Ghidra provider 只接受 native x86 / x86-64 PE 与 DLL；`inspect_macho` / `inspect_plist` / `demangle_swift` / `observe_native_calls` 等 macOS 能力标记为 `unsupported_host`，这些一律回退本地脚本。

**引擎不是自带**：Rea 本身不含反编译器。未配置引擎时 `open_binary` 仍能识别格式、架构与哈希，但任何函数级调用返回 `provider_unavailable`。Windows 上补齐：

```powershell
powershell -ExecutionPolicy Bypass -File tools/install_ghidra.ps1
```

脚本幂等（断点续传、复用已装目录），装 JDK 21 + Ghidra 12.1.x 并写入用户级 `JAVA_HOME` / `GHIDRA_INSTALL_DIR`。完成后：

1. 新开终端执行 `rea capabilities`，确认 ghidra 的 `availability.status` 为 `available`；
2. **重启 IDE / MCP 宿主** —— 已在运行的 MCP server 不会继承新写入的用户级环境变量，症状是 CLI 里可用、Agent 侧仍报 `install_dir: null`。

实测（Windows + Ghidra 12.1.4）：`rea analyze C:\Windows\System32\whoami.exe` 返回 `ev_0423ee4c…`、9 个段、341 个过程、308 个字符串。

它是可选后端，不是依赖：

```text
探测 → binary_overview 一次
绑定 → open_binary(path="<绝对路径>", provider_id="auto")
基线 → segments / 过程数 / 字符串数 记入 Artifact inventory
深挖 → list_procedures → procedure_pseudo_code → xrefs / trace_call_path
取证 → record_unknown → export_evidence_bundle
```

后端缺席时按 `references/rea-backend.md` 的降级矩阵回退到 `ghidra_headless.py` / `r2` / `jadx`，并在报告里显式声明降级、置信度上限 Medium。

探测当前环境是否具备：

```bash
python scripts/tool_audit.py --profile native   # 输出末尾的 Optional MCP backends 段
```

## 测试

```bash
python -m ruff check scripts tests   # pyflakes + 语法
python -m pytest tests -q            # 83 项
```

| 层次 | 文件 | 验证内容 |
|---|---|---|
| 冒烟 | `tests/test_smoke.py` | 全部 CLI 可编译、`--help` 可用、坏输入不崩、依赖缺失可跳过 |
| **黄金回归** | `tests/test_parsers_golden.py` + `tests/sample_factory.py` | 逐字节构造 PE / ELF / Mach-O / DEX，断言解析器还原出**已知真相**（machine、节名、入口 RVA、导入表、缓解位、哈希），并用 `struct` 反读证明 fixture 本身合规 |
| **交叉验证** | `tests/test_cross_validation.py` | 用 LIEF（独立实现）比对 PE 节表/导入表/DllCharacteristics、ELF 头与节、Mach-O 头；真实系统 PE 也跑一遍。缺 LIEF 自动 skip |
| 文档一致性 | `tests/test_docs_consistency.py` | 文档里每个路径存在、每个脚本被收录、每篇 reference 被索引、每个技能可路由 |
| 检测质量 | `tests/test_auto_analyze_detection.py` | 误报双向锁死：`.idata$2` 不算反分析、计时 API 不计风险、普通代码不算栈串 |
| 后端契约 | `tests/test_rea_cli_contract.py` | Rea 缺席自动 skip；在场则校验 provider 名与 `open:` 状态 |

fixture 在运行时由 `tests/sample_factory.py` 生成，仓库里不存任何二进制样本。CI 在 push/PR 上跑同一套（Ubuntu/Windows × 3.10/3.13）。

## 目录结构

```
reverse-flow/
├── SKILL.md           主技能（流程、工具选择、输出契约）
├── SKILLS.md          技能路由表（触发词 → 子技能）
├── AGENTS.md          Agent 装载协议（激活 / 记忆 / 工具链）
├── BOOTSTRAP.md       沙箱工具链武装
├── MEMORY.md          长期记忆（进度、偏好、决策）
├── scripts/           38 个 Python 脚本（顶层 17 + 6 个任务套件）
├── references/        19 篇方法论
├── skills/            8 个子技能（各含 SKILL.md + 案例）
├── tools/             工具链安装器 + 状态台账
├── docs/              平台实证知识库 + 运行归档
├── control/           多智能体编排（协议 / 派单 / worker 简报）
├── agents/            Codex CLI 接口配置
└── tests/             冒烟测试
```

## 设计原则

1. **零依赖优先**：分诊、结构解析、密码扫描、YARA、ROP 全部标准库实现，能在只剩 Python 的沙箱里跑。
2. **证据与推断分离**：报告模板强制分列「已验证事实 / 推断与置信度」，未执行的检查不许写成通过。
3. **可选后端，不做硬依赖**：Rea / Ghidra / radare2 缺席时流程不倒，但必须显式声明降级。
4. **原始样本只读**：所有改动在 case 工作区副本上做。
5. **授权边界**：动态分析、漏洞利用、恶意代码行为验证只在本地隔离沙箱 / CTF / 授权实验室目标上进行。

## 已知限制

- 函数级反编译质量取决于后端（Rea provider 或本地 Ghidra），不同引擎的伪代码**不保证等价**，不能跨引擎比对。
- `docs/` 下的平台实证是特定时间点的快照（含 2026-10 的模型目录），上游变更后需重新采集。
- `tools/TOOLS.md` 里的安装状态来自历史沙箱，换环境后必须重跑 `setup_tools_doctor.py` 刷新。
- 部分 `skills/*/` 目录混有当时的运行产物（`.stdout` / `.log` / 中间 JSON），作为案例证据保留，不参与技能执行。
- `tools/scripts/net/` 不随仓库分发（第三方 GPL 源码），离线环境需自行准备；`tools/TOOLS.md` 里的路径记录来自历史沙箱，仅作参考。
- CI 覆盖三层：冒烟、黄金回归（合成最小镜像）、LIEF 交叉验证。仍不覆盖真实样本的全谱系（重定位、资源、TLS、.NET 元数据、APK 签名块、DEX 方法体）。
- **没有覆盖率门槛**：脚本主要由 subprocess 驱动，`coverage` 追不到子进程，报出来的百分比会是假指标，所以宁可不设。
- lint 只开 `F`（pyflakes）+ `E9`（语法）：38 个分析脚本的完整规则集有约 130 条风格告警，在缺乏单测时批量重构风险高于收益。

## 许可

本仓库的代码与文档采用 [MIT](LICENSE)。

例外：`tools/setup_full.sh` 会在安装阶段把第三方源码克隆到 `tools/scripts/net/`（例如 unicornscan，GPL）。这些目录**不入库**，遵循各自许可，不受本仓库 MIT 声明覆盖。

<details>
<summary>给 AI Agent 的装载说明（人类读者可跳过）</summary>

1. 读 `AGENTS.md`，按其指令完整读取 `SKILL.md` 并执行 **Activation protocol**（激活短语：**真心为你**）。
2. 读 `SKILLS.md`，按用户任务关键词匹配子技能，打开对应 `skills/<name>/SKILL.md`。
3. 读 `MEMORY.md` 恢复上次进度；收工时把本次进度追加写回。
4. 需要工具链时执行 `bash scripts/setup.sh`（clone + pip + 自检）。
5. 需要深度分析时，先按 `references/rea-backend.md` 探测 Rea MCP，再决定走引擎还是降级。

用户触发示例：

```
读取 https://github.com/useragent-1/haha-1 的 README.md 与 SKILL.md，
按其中 Activation protocol 执行装载，然后进入逆向模式待命。
```

</details>

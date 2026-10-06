# 技能路由表（Skill Router）

> 给任何读取本仓库的 Agent：读本表，按任务关键词匹配技能，打开对应主文件执行其协议。
> 未命中时按 `SKILL.md` 的默认流程推进：分析、报告、逆向、深度逆向、漏洞研判、利用开发，最后由用户选择下一步。

## 已装载技能

| 触发关键词 | 技能 | 主文件 | 说明 |
|---|---|---|---|
| 动态 / 调试 / 追踪 / 动态脱壳 / 脱壳 / 内存 dump / 内存dump / dump / 行为分析 / 插桩 / hook / Frida / GDB / strace / ltrace | **dynamic-recon** | `skills/dynamic-recon/SKILL.md` | 授权动态分析：调试与崩溃回溯、系统/库调用追踪、Hook/插桩、反调试识别、内存 dump、符号执行、多架构模拟；“动态脱壳/内存 dump”优先于静态脱壳路由 |
| 协议 / PCAP / pcap / 流量 / 会话重组 / beaconing / C2 心跳 | **protocol-re** | `skills/protocol-re/SKILL.md` | 离线会话重组、协议字段模板、明文/加密启发式和异常流量扫描 |
| 前端 / JS / JavaScript / 端点发现 / endpoint / source map / sourcemap | **frontend-re** | `skills/frontend-re/SKILL.md` | API/WebSocket/域名发现、source map 恢复、格式化对照和位置-only 敏感信息扫描 |
| 脱壳 / 混淆 / 加固 / UPX / 字符串加密 / unpack / deobfuscate | **unpack-deobfusc** | `skills/unpack-deobfusc/SKILL.md` | 壳识别、UPX 副本脱壳、字符串解密候选和脱壳前后差异；纯“脱壳”默认本技能，动态上下文转 dynamic-recon |
| 报告 / HTML 报告 / 批量 / batch / 批量分析 / 汇总索引 | **report-batch** | `skills/report-batch/SKILL.md` | JSON/Markdown 单文件 HTML 合成与 auto_analyze 批量运行 |
| 逆向 / 破解 / 样本 / 二进制 / APK / PE / Mach-O / 固件 / 漏洞 / 利用 / 恶意代码 / 补丁 | **reverse-flow** | `SKILL.md` | 全谱系静态逆向、密码学识别、ROP/exploit、YARA、一键流水线；专项关键词转交上述技能 |
| 一键分析 / 快速分析 / auto analyze | reverse-flow（流水线） | `scripts/auto_analyze.py` | 单命令全自动分析：识别、哈希、熵、字符串、加密常量、加壳、结构解析、YARA |

## 待建技能（占位，欢迎填充）

| 触发关键词 | 技能 | 计划主文件 | 说明 |
|---|---|---|---|
| 3D / three.js / 场景 / 城市 / 建模 | three-city | `skills/three-city/SKILL.md` | Web 3D 场景构建规范：坐标系换算、几何合并、贴图程序化生成、性能预算 |
| 爬虫 / 采集 / 抓取 / 清洗 | scraper | `skills/scraper/SKILL.md` | 采集、清洗、落库的标准化流程 |
| 文档 / 报告 / 说明 | doc-writer | `skills/doc-writer/SKILL.md` | 证据化文档写作规范 |

## 装载协议（每个新会话开工时执行）

1. 读 `AGENTS.md`，执行 `SKILL.md` 的 Activation protocol（激活短语：真心为你）
2. 读 `MEMORY.md`，恢复上次进度与用户偏好
3. 按用户任务在本表匹配技能，读取对应主文件
4. 收工前：把本次进度追加写回 `MEMORY.md`（时间 / 任务 / 产出 / 决策 / 下一步）

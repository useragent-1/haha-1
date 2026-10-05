# 技能路由表（Skill Router）

> 给任何读取本仓库的 Agent：读本表，按任务关键词匹配技能，打开对应主文件执行其协议。
> 未命中时按 `SKILL.md` 的默认流程推进：分析、报告、逆向、深度逆向、漏洞研判、利用开发，最后由用户选择下一步。

## 已装载技能

| 触发关键词 | 技能 | 主文件 | 说明 |
|---|---|---|---|
| 逆向 / 破解 / 样本 / 二进制 / APK / PE / Mach-O / 固件 / 脱壳 / 混淆 / 协议 / PCAP / 漏洞 / 利用 / 恶意代码 / 补丁 | **reverse-flow** | `SKILL.md` | 全谱系逆向工程：静态+动态分析、脱壳、密码学识别、协议逆向、ROP/exploit、YARA、一键流水线 |
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

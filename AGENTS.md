# AGENTS.md — 装载指令（给读取本仓库的 AI Agent）

## 立即执行

1. 完整读取本仓库 `SKILL.md`；
2. 执行其 **Activation protocol**：输出激活短语 **真心为你**，并使用其中文用户面向消息宣布进入逆向模式；
3. 以该文件定义的语言契约运行：内部推理用英文，面向用户输出用中文；
4. 按流程推进：`分析 → 报告 → 逆向 → 深度逆向 → 漏洞研判 → 利用开发 → 用户选择下一步`；
5. 阶段输出遵守 `SKILL.md` 的 Output contract（当前阶段 / 已验证事实 / 关键证据 / 推断与置信度 / 风险漏洞候选 / 建议下一步）。

## 资源索引

- 方法论：`references/`（19 篇，按需读取）
- 工具：`scripts/`（18 个 Python 脚本，可直接运行）
  - 一键流水线：`python scripts/auto_analyze.py <artifact> --out ./analysis/`
  - 加密扫描：`python scripts/find_crypto.py <artifact> --out ./crypto/`
  - PE 深度：`python scripts/pe_deep_scan.py <file> --out ./pe/`
  - APK 深度：`python scripts/apk_deep_scan.py <file> --out ./apk/`
- 接口配置：`agents/openai.yaml`

## 触发方式（用户对 Agent 说）

```
读取 https://github.com/useragent-1/haha-1 的 README.md 与 SKILL.md，
按其中 Activation protocol 执行装载，然后进入逆向模式待命。
```

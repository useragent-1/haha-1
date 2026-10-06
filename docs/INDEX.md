# 仓库总索引（INDEX）

> 本仓库 = **技能 + 知识 + 工具 + 记忆**。Agent 装载时按本索引定位。

## 一、快速入口

| 我要做什么 | 读这里 |
|---|---|
| 我是 Agent，第一次来 | `AGENTS.md`（装载协议）→ `SKILL.md`（激活）→ `MEMORY.md`（记忆）→ `SKILLS.md`（选技能） |
| 我要查有什么技能 | `SKILLS.md` 路由表 |
| 我要查平台知识 | `docs/ARENA-PLATFORM-ARCHITECTURE.md` |
| 我要查工具 | `tools/TOOLS.md`（工具总索引） |
| 我要装工具 | `tools/setup_core.sh`（30 秒核心）/ `tools/setup_full.sh`（全量） |
| 我要自检环境 | `tools/setup_tools_doctor.py` |

## 二、目录结构

```
├── AGENTS.md          装载指令（激活 + 记忆 + 工具链 + 授权边界协议）
├── SKILL.md           reverse-flow 主技能（逆向全流程）
├── SKILLS.md          技能路由表（触发词 → 技能）
├── MEMORY.md          长期记忆（用户偏好 / 当前状态 / 进度日志）
├── BOOTSTRAP.md       工具链武装指南
│
├── skills/            技能包
│   ├── sandbox-recon/       沙箱/容器环境侦察
│   ├── desktop-app-recon/   桌面应用逆向（Electron/Tauri/PyInstaller）
│   ├── binary-triage/       二进制分诊流水线
│   ├── dynamic-recon/       动态分析（调试/追踪/脱壳）
│   ├── protocol-re/         协议与流量分析
│   ├── frontend-re/         前端/JS 逆向
│   └── unpack-deobfusc/     反混淆与脱壳
│
├── references/        方法论 19 篇（按需读，别全读）
├── scripts/           分析脚本 40+
│   ├── auto_analyze.py / pe_deep_scan.py / elf_deep_scan.py ...
│   ├── dynamic/ protocol/ frontend/ unpack/ report/ net/
│   └── setup.sh
│
├── tools/             工具库（2026-10-06 新增）
│   ├── TOOLS.md              CLI 工具总索引（状态/版本/沙箱限制）
│   ├── setup_core.sh         核心 25 件套（幂等，30 秒）
│   ├── setup_full.sh         A 档全量（幂等）
│   └── setup_tools_doctor.py 环境自检（PASS/FAIL/B档/SKIP）
│
└── docs/              知识库
    ├── ARENA-PLATFORM-ARCHITECTURE.md   平台架构实证
    ├── SANDBOX-RECON-MATRIX.md          沙箱侦察命令矩阵
    ├── INDEX.md（本文件）
    └── reports/                          运行报告归档
```

## 三、常用调用

```bash
# 装环境
bash scripts/setup.sh            # 技能包依赖（分析脚本用）
bash tools/setup_core.sh         # 核心工具 25 件套

# 跑分析
python scripts/auto_analyze.py <样本> --out ./analysis/
python scripts/triage_artifact.py <样本> --out ./triage/

# 侦察当前环境
bash tools/setup_core.sh && python scripts/auto_analyze.py /usr/bin/git --out ./recon/
```

## 四、纪律（所有技能共用）

1. 事实与推断分开写，推断标置信度
2. 关键结论带证据（命令输出 / 偏移 / 函数名 / 哈希）
3. 未执行的检查不许写成"通过"
4. 凭据类只报字段名，值打码后 4 位
5. 每阶段结束给编号下一步菜单
6. 收工把结论写进 `MEMORY_UPDATE.md`（工作区自动持久化）

---
name: binary-triage
description: Evidence-backed triage and function-level analysis for ELF, PE, shared libraries, scripts, and minified JavaScript artifacts.
---

# Binary Triage — 二进制与脚本实战分诊

## Activation protocol

加载后输出：**真心为你**

随后声明：

> 已进入二进制分诊模式。将按“保全样本 → 自动流水线 → 类型深扫 → 函数级证据 → 交叉验证 → 报告”推进；任何失败保留退出码与错误原文。

## 启动前置 / Environment preflight

每次装载本技能，先执行统一开工动作，不复用上轮“已安装”假设：

```bash
SESSION_ID="${AGENT_SESSION_ID:-agent-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
tail -5 /home/user/MEMORY_UPDATE.md 2>/dev/null || true
/home/user/ha-ha/scripts/session_memory.sh start "$SESSION_ID"
cat /home/user/ENV_FINGERPRINT.md 2>/dev/null || true
python --version
python -m pip --version
python - <<'PY2'
for m in ['capstone','unicorn']:
    try:
        x=__import__(m); print(m, 'OK', getattr(x, '__version__', ''))
    except Exception as e:
        print(m, 'ERROR', repr(e))
PY2
```

- `session_memory.sh start` 返回 2 时，说明 `ACTIVE_SESSION` 属于其他会话：报告“检测到可能的并发会话”并询问用户，不得抢锁。
- 若 `ENV_FINGERPRINT.md` 缺失，或 Python/pip、关键 import、pip/apt hash 与指纹不一致，执行标准重建：

```bash
bash /home/user/ha-ha/scripts/setup.sh
```

- 重建后重新采集 Python、pip、apt、工具路径与三项自检，更新 `/home/user/ENV_FINGERPRINT.md`。
- 每完成一个阶段立即调用 checkpoint，不等收工：

```bash
/home/user/ha-ha/scripts/session_memory.sh checkpoint "$SESSION_ID" "阶段名" "已完成" "进行中" "下一步"
```

- 收工时仅由锁所有者执行：

```bash
/home/user/ha-ha/scripts/session_memory.sh finish "$SESSION_ID"
```

## 1. Intake and preservation

1. 记录绝对路径、`file`、大小、SHA-256、mtime。
2. 默认只读分析；外部样本下载到 `case/<name>/artifact/` 并保存来源 URL。
3. 为每条命令记录 stdout、stderr 和退出码。
4. 不把扫描器的 risk hint 当作恶意或漏洞结论。

## 2. Standard pipeline

```bash
python scripts/auto_analyze.py <target> --out <case>/auto/
python scripts/find_crypto.py <target> --out <case>/crypto/
python scripts/yara_gen.py <target> --out <case>/yara/
```

类型深扫：

```bash
python scripts/elf_deep_scan.py <elf> --out <case>/elf/
python scripts/pe_deep_scan.py <pe> --out <case>/pe/
python scripts/apk_deep_scan.py <apk> --out <case>/apk/
```

每次必须检查：

- JSON/Markdown 是否实际生成；
- 退出码是否为 0；
- JSON 的类型识别是否与系统 `file`/ELF header 一致；
- 独立脚本结果是否与 `auto_analyze` 内联阶段一致。

## 3. Function-level evidence

### ELF executable / shared library

```bash
readelf -hW <elf>
readelf -Ws <elf>
readelf -dW <elf>
objdump -d -M intel <elf>
```

证据要求：

- 导出/导入函数名与版本；
- 文件偏移或虚拟地址；
- 至少 8–20 条上下文指令；
- 调用参数来源、返回值去向；
- 近似反编译必须标注“人工恢复”，不得冒充反编译器输出。

对 stripped PIE 主程序，可用 `function@plt` + call-site 地址命名；对共享库优先使用版本化导出符号。用 `ldd`、`readelf -d` 和版本符号把主程序调用与库实现交叉关联。

### Crypto constants

- 用 `od`/`xxd` 验证扫描器给出的文件偏移。
- 常量命中只证明“实现/支持该算法”，不证明密钥、当前协议启用或漏洞。
- MD5/SHA 常量必须继续做代码 xref；Base64 字母表通常是编码功能，不是密钥。

### Shell/Python scripts

- 先运行语法检查：`bash -n` 或 `python -m py_compile`。
- 以函数名或“top-level logic block”报告；同时给行号和累计字节偏移。
- 审阅 `eval`、未引用变量、word splitting、临时文件、端口 TOCTOU、trap 清理。

### Minified JavaScript

通用字符串工具可能把整条超长行当成一个字符串。必须增加：

- 文件熵、行数、最长行；
- 模块 ID、URL/API path、UUID、source map；
- `eval`、`new Function`、`atob`、WebAssembly、`crypto.subtle` 指标；
- bundler 标识（Turbopack/Webpack）和遥测标识；
- 以模块起始偏移 + 压缩函数名报告函数级证据。

生成 YARA 后，拒绝使用“整份 JS 作为单个字符串”的规则；应限制单字符串长度并选择稳定模块/端点特征。

## 4. Cross-validation gates

1. **Type gate**：ET_DYN 可能是 PIE executable，也可能是 shared object；结合 PT_INTERP、entry point 和 `file`，不能一律标为 shared library。
2. **ROP gate**：若 `auto_analyze` 与独立 `rop_finder.py` 数量不一致，报告为工具缺陷，不选择性采信。
3. **Dependency gate**：记录 Ghidra/radare2/YARA CLI、capstone、unicorn、pyelftools、lief 是否可用。
4. **Persistence gate**：在临时沙箱中，apt/pip 安装可能跨命令调用不持久；每阶段重新 `command -v`/import 验证。
5. **YARA gate**：生成成功不等于规则可编译；必须用 YARA CLI/Python 模块编译测试，否则标记“未验证”。
6. **Failure gate**：任何失败都保留命令、退出码、stderr 原文以及是否采用 fallback。

## 5. Output contract

每个目标独立输出：

- **当前阶段 / Current phase**
- **已验证事实 / Verified facts**
- **关键证据 / Key evidence**
- **函数级深挖 / Function-level deep dive**（名称、偏移、指令/源码、人工近似反编译）
- **推断与置信度 / Inference and confidence**
- **风险/漏洞候选 / Risk or vulnerability candidates**
- **利用可行性 / Exploitability assessment**
- **建议下一步 / Suggested next steps**

最后增加：

- 目标间交叉分析；
- 工具链成功项、失败项、缺失依赖、结果不一致；
- 所有报告和关键产物 SHA-256。

# 工具链武装（Bootstrap）

> 目的：让 Agent 在沙箱内拥有**可运行**的分析工具链，而不只是文档。
> 路径约定：`SKILL_ROOT` 默认 `${HOME}/ha-ha`（典型沙箱里就是 `/home/user/ha-ha`），可用环境变量或参数覆盖，不要写死。

## 一键安装（推荐）

```bash
bash scripts/setup.sh                  # 装到 ${SKILL_ROOT:-$HOME/ha-ha}
bash scripts/setup.sh /opt/ha-ha       # 或指定目录
```

脚本会：clone 本仓库到目标目录（已存在则 `pull --ff-only`）→ 安装 `requirements.txt` → 三个核心脚本自检 → 打印 `TOOLCHAIN READY`。

## 手动安装（等价步骤）

```bash
SKILL_ROOT="${SKILL_ROOT:-$HOME/ha-ha}"
git clone https://github.com/useragent-1/haha-1.git "$SKILL_ROOT" \
  || (cd "$SKILL_ROOT" && git pull --ff-only)
cd "$SKILL_ROOT"
pip install -r requirements.txt || pip install --break-system-packages -r requirements.txt
python scripts/triage_artifact.py --help >/dev/null && echo triage:OK
python scripts/find_crypto.py --help >/dev/null && echo crypto:OK
python scripts/auto_analyze.py --help >/dev/null && echo auto:OK
```

## 基础工具（沙箱有 sudo + apt 时）

```bash
sudo apt-get update -qq
sudo apt-get install -y -qq binutils file xxd jq ripgrep
```

需要完整工具链（radare2 / jadx / binwalk / 取证套件）时用 `tools/`：

```bash
bash tools/setup_core.sh                          # 核心 25 件套
bash tools/setup_full.sh                          # A 档全量
SETUP_ADVANCED=1 bash tools/setup_full.sh         # 第三批
python tools/setup_tools_doctor.py                # 自检
```

## 常用分析流水线

```bash
SKILL_ROOT="${SKILL_ROOT:-$HOME/ha-ha}"
CASE="$(pwd)/case"; mkdir -p "$CASE"
python "$SKILL_ROOT/scripts/auto_analyze.py" <sample> --out "$CASE/auto/"
python "$SKILL_ROOT/scripts/pe_deep_scan.py" <sample> --out "$CASE/pe/"
python "$SKILL_ROOT/scripts/find_crypto.py" <sample> --out "$CASE/crypto/"
python "$SKILL_ROOT/scripts/yara_gen.py" <sample> --out "$CASE/yara/"
```

## 说明

- `capstone`（反汇编）与 `unicorn`（仿真）是仅有的外部依赖；其余脚本纯标准库。
- 沙箱是临时的：每次任务结束销毁，下次开工重跑 `scripts/setup.sh` 即可（约 30 秒）。
- Windows 不需要 bash：`pip install -r requirements.txt` 后用绝对路径调用脚本；Rea 的 Ghidra 引擎用 `powershell -File tools/install_ghidra.ps1`。
- 需要函数级反编译时，先按 `references/rea-backend.md` 探测后端；引擎缺失时按降级矩阵回退。

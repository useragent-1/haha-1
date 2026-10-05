# 工具链武装（Bootstrap）

> 目的：让 Agent 在沙箱内拥有**可运行**的分析工具链，而不只是文档。

## 一键安装（推荐）

```bash
bash scripts/setup.sh
```

脚本会：clone 本仓库到 `/home/user/ha-ha`（已存在则 pull）→ 安装 Python 依赖 → 三个核心脚本自检 → 打印 `TOOLCHAIN READY`。

## 手动安装（等价步骤）

```bash
git clone https://github.com/useragent-1/haha-1.git /home/user/ha-ha \
  || (cd /home/user/ha-ha && git pull --ff-only)
cd /home/user/ha-ha
pip install -r requirements.txt || pip install --break-system-packages -r requirements.txt
python scripts/triage_artifact.py --help >/dev/null && echo triage:OK
python scripts/find_crypto.py --help >/dev/null && echo crypto:OK
python scripts/auto_analyze.py --help >/dev/null && echo auto:OK
```

## 基础工具（沙箱有 sudo + apt，按需）

```bash
sudo apt-get update -qq
sudo apt-get install -y -qq binutils file xxd jq ripgrep
```

## 常用分析流水线

```bash
CASE=/home/user/case; mkdir -p "$CASE"
python /home/user/ha-ha/scripts/auto_analyze.py <sample> --out "$CASE/auto/"
python /home/user/ha-ha/scripts/pe_deep_scan.py <sample> --out "$CASE/pe/"
python /home/user/ha-ha/scripts/find_crypto.py <sample> --out "$CASE/crypto/"
python /home/user/ha-ha/scripts/yara_gen.py <sample> --out "$CASE/yara/"
```

## 说明

- `capstone`（反汇编）与 `unicorn`（仿真）是仅有的外部依赖；其余脚本纯标准库。
- 沙箱环境是临时的：每次任务结束销毁，下次开工重新跑一遍 `scripts/setup.sh` 即可（约 30 秒）。

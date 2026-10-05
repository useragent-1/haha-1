#!/usr/bin/env bash
# haha-1 工具链一键武装（在沙箱内运行）
# 用法: bash scripts/setup.sh [安装目录]
set -e
REPO="https://github.com/useragent-1/haha-1.git"
DEST="${1:-/home/user/ha-ha}"

if [ -d "$DEST/.git" ]; then
  echo "[1/4] updating $DEST"
  git -C "$DEST" pull --ff-only || true
else
  echo "[1/4] cloning into $DEST"
  git clone --depth 1 "$REPO" "$DEST"
fi
cd "$DEST"

echo "[2/4] installing python deps (capstone, unicorn)"
pip install -q -r requirements.txt 2>/dev/null || pip install -q --break-system-packages -r requirements.txt || true

echo "[3/4] self test"
python scripts/triage_artifact.py --help >/dev/null 2>&1 && echo "  triage_artifact: OK" || echo "  triage_artifact: FAIL"
python scripts/find_crypto.py --help >/dev/null 2>&1 && echo "  find_crypto: OK" || echo "  find_crypto: FAIL"
python scripts/auto_analyze.py --help >/dev/null 2>&1 && echo "  auto_analyze: OK" || echo "  auto_analyze: FAIL"

echo "[4/4] TOOLCHAIN READY at $DEST"

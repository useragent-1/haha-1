#!/usr/bin/env bash
# Idempotent core CLI bootstrap. On an already-provisioned sandbox this should finish within 30s.
set -u
APT=(file binutils gawk jq yq sqlite3 lsof tmux gdb strace ltrace patchelf nmap tcpdump tshark socat netcat-openbsd bind9-dnsutils build-essential python3-dev curl git ripgrep python3-venv cmake)
missing=()
for p in "${APT[@]}"; do dpkg-query -W -f='${Status}' "$p" 2>/dev/null | grep -q 'install ok installed' || missing+=("$p"); done
if ((${#missing[@]})); then
  echo "missing: ${missing[*]}"
  timeout 10s sudo apt-get update || echo 'WARN: apt-get update failed/timed out'
  timeout 300s sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${missing[@]}" || echo 'WARN: some core packages failed'
fi
for c in file readelf gawk jq yq sqlite3 lsof tmux gdb strace ltrace patchelf nmap tcpdump tshark socat nc dig gcc python3 curl git rg cmake; do
  if command -v "$c" >/dev/null; then printf 'PASS\t%s\t%s\n' "$c" "$(command -v "$c")"; else printf 'MISSING\t%s\n' "$c"; fi
done
if dpkg-query -W -f='${Status}' python3-venv 2>/dev/null | grep -q 'install ok installed'; then
  printf 'PASS\tpython3-venv\tpackage-installed\n'
else
  printf 'MISSING\tpython3-venv\n'
fi

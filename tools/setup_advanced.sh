#!/usr/bin/env bash
# 第三批补装（2026-10-06）：补齐 Ghidra/Windows/取证/情报/取证截图 五大真缺口。
# 设计原则：全部轻量、幂等、单点失败不阻塞。metasploit / Ghidra 全量 / C2 框架按用户要求不装。
set -u
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOGDIR=${TOOL_LOG_DIR:-/home/user/tool-install-logs}; mkdir -p "$LOGDIR"; sudo mkdir -p /opt/security-tools
STATUS="$LOGDIR/status.tsv"; if [[ ${RESUME_INSTALL:-0} != 1 || ! -f "$STATUS" ]]; then printf 'class\ttool\tstatus\texit\tdetail\n' > "$STATUS"; fi
record(){ printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "${5//$'\t'/ }" | tee -a "$STATUS"; }
apt_install(){ local p=$1 log="$LOGDIR/apt-$1.log"; if dpkg-query -W -f='${Status}' "$p" 2>/dev/null|grep -q 'install ok installed';then record apt "$p" PASS 0 installed;return;fi; timeout 240s sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$p" >"$log" 2>&1; local r=$?; if [[ $r == 0 ]];then record apt "$p" PASS 0 installed;else record apt "$p" FAIL "$r" "$log";fi; }
pip_install(){ local p=$1 mod=${2:-}; local safe log r; safe=${p//[^A-Za-z0-9_.-]/_}; log="$LOGDIR/pip-$safe.log"; timeout 300s python3 -m pip install --no-cache-dir "$p" >"$log" 2>&1; r=$?; if [[ $r != 0 ]];then timeout 300s python3 -m pip install --no-cache-dir --break-system-packages "$p" >>"$log" 2>&1;r=$?;fi; if [[ $r == 0 ]];then record pip "$p" PASS 0 installed;else record pip "$p" FAIL "$r" "$log";fi; }
gh_release(){ local tool=$1 repo=$2 bin=$3 regex=${4:-'(?i)(linux.*(amd64|x86_64)|(amd64|x86_64).*linux).*(tar\.gz|tgz|zip)$'}; local log r; log="$LOGDIR/bin-$tool.log"; if command -v "$bin" >/dev/null;then record binary "$tool" PASS 0 "$(command -v "$bin")";return;fi; timeout 300s python3 "$ROOT/tools/install_github_release.py" "$repo" "$bin" --asset-regex "$regex" >"$log" 2>&1;r=$?;if [[ $r == 0 ]];then record binary "$tool" PASS 0 "$(command -v "$bin" 2>/dev/null)";else record binary "$tool" FAIL "$r" "$log";fi; }
git_clone(){ local tool=$1 url=$2 dest=$3; local log r; log="$LOGDIR/git-$tool.log"; if [[ -d "$dest" ]];then record git "$tool" PASS 0 "$dest";return;fi; timeout 300s sudo git clone --depth 1 "$url" "$dest" >"$log" 2>&1;r=$?;if [[ $r == 0 ]];then record git "$tool" PASS 0 "$dest";else record git "$tool" FAIL "$r" "$log";fi; }

RX='(?i)(linux.*(amd64|x86_64)|(amd64|x86_64).*linux).*(tar\.gz|tgz|zip)$'

# ── A. 反编译与二进制深度（补 Ghidra 全量的缺口，体积只有它的 1/40）────────────
# r2ghidra = Ghidra 的 decompiler 后端，装上后 radare2 的 pdc/pdg 直接输出伪 C
if ! command -v r2ghidra-dec >/dev/null 2>&1;then
  if timeout 300s go install github.com/r2ghidra/r2ghidra@latest >"$LOGDIR/r2ghidra-go.log" 2>&1;then
    for c in "$(go env GOPATH)/bin/r2ghidra-dec" "$(go env GOPATH)/bin/r2pd";do [[ -f "$c" ]] && sudo install -m755 "$c" /usr/local/bin/;done
    record build r2ghidra PASS 0 /usr/local/bin/r2ghidra-dec
  else
    record build r2ghidra FAIL 1 "$LOGDIR/r2ghidra-go.log"
  fi
else record build r2ghidra PASS 0 "$(command -v r2ghidra-dec)";fi
apt_install diffoscope            # 二进制深度差异对比（几百 MB 级 diff 的替代品）
pip_install lief                  # PE/ELF/Mach-O 统一解析（已装亦幂等）
pip_install r2pipe                # Python 驱动 radare2

# ── B. Windows 工具链替代（沙箱无 Windows，用 mono/wine 跑能跑的部分）────────────
apt_install mono-devel            # .NET 运行时 + ildasm 等
apt_install mono-utils            # monodis（IL 反汇编）
apt_install wine                  # 可运行部分 Windows CLI 工具
# de4dot：.NET 去混淆（Shroud、ConfuserEx 等），Linux 预编译需 mono 运行
gh_release de4dot ocalidot/de4dot de4dot "$RX"

# ── C. 内存取证与端点狩猎（此前只有 scalpel/bulk_extractor，缺内存维度）────────
apt_install guymager              # 内存/磁盘镜像采集（FTK Imager 的 Linux 等价）
apt_install clamav                # 反病毒引擎（样本是否被主流 AV 标记）
apt_install clamav-daemon
apt_install osquery               # 跨平台端点 SQL 查询（自检沙箱自身也可复用）
git_clone Velociraptor https://github.com/Velocidex/velociraptor.git /opt/security-tools/velociraptor

# ── D. 威胁情报与 CVE（本地化，API 受限时的替代路径）─────────────────────────
pip_install cve-bin-tool          # 本地 NVD 数据匹配：给二进制查已知漏洞
pip_install stix2-validator       # STIX/TAXII 情报校验
pip_install pymisp                # MISP API 客户端（威胁情报共享）
pip_install otxv2                 # IOC 批量提取（URL/IP/哈希/邮箱）
pip_install ja3                   # TLS 客户端指纹计算

# ── E. 侦察取证补漏（typosquat / 仓库泄露 / 证书 / 截图）──────────────────────
pip_install dnstwist             # 域名投毒与错拼域名枚举
pip_install git-dumper            # 从 GitHub 拉泄露的 .git 仓库源码
pip_install xmltodict             # 各类 XXE/SVG/文档解析辅助
gh_release gowitness sensepost/gowitness gowitness "$RX"
gh_release uncover projectdiscovery/uncover uncover "$RX"

# ── 可选：体积较大或编译较重，按需开启 ───────────────────────────────────────
if [[ ${SETUP_HEAVY:-0} == 1 ]]; then
  apt_install qemu-system-x86     # 完整系统模拟（可起 Linux 靶机，无需 qemu-user）
  gh_release bloaty google/bloaty bloaty "$RX"
  pip_install plaso               # 超时间线（log2timeline）
else
  record apt qemu-system-x86 SKIPPED 0 'set SETUP_HEAVY=1 to install (full-system emulator)'
  record build bloaty SKIPPED 0 'set SETUP_HEAVY=1 to install'
  record pip plaso SKIPPED 0 'set SETUP_HEAVY=1 to install'
fi

record policy batch3 DONE 0 'ghidra-full/metasploit/C2 intentionally not installed per user decision'
echo "status=$STATUS"

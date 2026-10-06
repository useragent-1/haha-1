#!/usr/bin/env bash
# Best-effort A-tier installer. Idempotent; one package failure never stops later packages.
set -u
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOGDIR=${TOOL_LOG_DIR:-/home/user/tool-install-logs}; mkdir -p "$LOGDIR" "$ROOT/tools/scripts/net"; sudo mkdir -p /opt/security-tools
STATUS="$LOGDIR/status.tsv"; if [[ ${RESUME_INSTALL:-0} != 1 || ! -f "$STATUS" ]]; then printf 'class\ttool\tstatus\texit\tdetail\n' > "$STATUS"; fi
record(){ printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "${5//$'\t'/ }" | tee -a "$STATUS"; }
apt_install(){ local p=$1 log="$LOGDIR/apt-$1.log"; if dpkg-query -W -f='${Status}' "$p" 2>/dev/null|grep -q 'install ok installed';then record apt "$p" PASS 0 installed;return;fi; timeout 120s sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$p" >"$log" 2>&1; local r=$?; if [[ $r == 0 ]];then record apt "$p" PASS 0 installed;else record apt "$p" FAIL "$r" "$log";fi; }
pip_install(){ local p=$1 mod=${2:-}; local safe log r; safe=${p//[^A-Za-z0-9_.-]/_}; log="$LOGDIR/pip-$safe.log"; timeout 120s python3 -m pip install --no-cache-dir "$p" >"$log" 2>&1; r=$?; if [[ $r != 0 ]];then timeout 120s python3 -m pip install --no-cache-dir --break-system-packages "$p" >>"$log" 2>&1;r=$?;fi; if [[ $r == 0 ]];then record pip "$p" PASS 0 installed;else record pip "$p" FAIL "$r" "$log";fi; }
gh_release(){ local tool=$1 repo=$2 bin=$3 regex=${4:-'(?i)(linux.*(amd64|x86_64)|(amd64|x86_64).*linux).*(tar\.gz|tgz|zip)$'}; local log r; log="$LOGDIR/bin-$tool.log"; if command -v "$bin" >/dev/null;then record binary "$tool" PASS 0 "$(command -v "$bin")";return;fi; timeout 120s python3 "$ROOT/tools/install_github_release.py" "$repo" "$bin" --asset-regex "$regex" >"$log" 2>&1;r=$?;if [[ $r == 0 ]];then record binary "$tool" PASS 0 "$(command -v "$bin" 2>/dev/null)";else record binary "$tool" FAIL "$r" "$log";fi; }
git_clone(){ local tool=$1 url=$2 dest=$3; local log r; log="$LOGDIR/git-$tool.log"; if [[ -d "$dest" ]];then record git "$tool" PASS 0 "$dest";return;fi; timeout 120s sudo git clone --depth 1 "$url" "$dest" >"$log" 2>&1;r=$?;if [[ $r == 0 ]];then record git "$tool" PASS 0 "$dest";else record git "$tool" FAIL "$r" "$log";fi; }

if [[ ${SKIP_APT_PIP:-0} != 1 ]]; then
 echo '[apt update]'; timeout 120s sudo apt-get update >"$LOGDIR/apt-update.log" 2>&1 || record apt apt-update FAIL $? "$LOGDIR/apt-update.log"
 APT=(radare2 gdb lldb binutils gawk patchelf strace ltrace qemu-user-static build-essential cmake golang-go rustc cargo python3-dev python3-venv yara afl++ radamsa nmap masscan tcpdump tshark zeek-client suricata hping3 netcat-openbsd socat dnsutils ethtool arp-scan sqlmap nikto ffuf feroxbuster gobuster wpscan whatweb theharvester joomscan droopescan hydra medusa ncrack cewl crunch smbclient ldap-utils krb5-user dnsrecon fierce enum4linux proxychains4 binwalk aircrack-ng reaver steghide libimage-exiftool-perl foremost testdisk sleuthkit ssdeep tlsh yq jq sqlite3 postgresql-client redis-tools tmux pandoc graphviz file lsof wordlists swaks mailutils)
 for p in "${APT[@]}";do apt_install "$p";done
 # 注：wordlists 提供 rockyou.txt（约 130MB）。不进工作区，故不占快照额度。
 PIP=(angr pwntools lief pefile pyelftools macholib capstone unicorn keystone-engine ropper ROPgadget z3-solver miasm qiling flare-capa r2pipe frida-tools objection yara-x pocsuite3 boofuzz hypothesis scapy mitmproxy impacket arjun dirsearch wapiti cmseek commix h8mail shhgit detect-secrets recon-ng sublist3r wifite2 volatility3 yara-python checkov kube-hunter stix2 mitreattack-python requests colorama)
 for p in "${PIP[@]}";do pip_install "$p";done
 # PyPI 无官方发行版的三件：改用 GitHub 源（失败不阻塞后续）
 pip_install "git+https://github.com/siegilt/sievecarve.git"          sievecarve
 pip_install "git+https://github.com/mitre-attack/cti-python-sdk.git" cti_python_sdk
 # boofuzz 需要可提升的 core hard limit；沙箱禁止时由 hypothesis + afl++ 覆盖同一用途。
 if ! python3 -c "import boofuzz" >/dev/null 2>&1; then
     record pip boofuzz FAIL 78 'core hard limit cannot be raised in sandbox; use hypothesis/afl++ instead'
 fi
 # 威胁狩猎：Sigma 规则引擎（规则库见下方 git_clone）
 pip_install sigma-cli sigma_cli
fi

RX='(?i)(linux.*(amd64|x86_64)|(amd64|x86_64).*linux).*(tar\.gz|tgz|zip)$'
gh_release floss mandiant/flare-floss floss "$RX"
gh_release gophish gophish/gophish gophish "$RX"
for spec in 'httpx|projectdiscovery/httpx|httpx' 'naabu|projectdiscovery/naabu|naabu' 'dnsx|projectdiscovery/dnsx|dnsx' 'tlsx|projectdiscovery/tlsx|tlsx' 'subfinder|projectdiscovery/subfinder|subfinder' 'nuclei|projectdiscovery/nuclei|nuclei' 'katana|projectdiscovery/katana|katana' 'interactsh-client|projectdiscovery/interactsh|interactsh-client' 'asnmap|projectdiscovery/asnmap|asnmap' 'gau|lc/gau|gau' 'waybackurls|tomnomnom/waybackurls|waybackurls' 'dalfox|hahwul/dalfox|dalfox' 'amass|owasp-amass/amass|amass' 'puredns|d3mondev/puredns|puredns' 'gitleaks|gitleaks/gitleaks|gitleaks' 'trufflehog|trufflesecurity/trufflehog|trufflehog' 'assetfinder|tomnomnom/assetfinder|assetfinder' 'findomain|Findomain/Findomain|findomain' 'lazagne|AlessandroZ/LaZagne|laZagne.py' 'ligolo-ng|nicocha30/ligolo-ng|proxy' 'chisel|jpillora/chisel|chisel' 'frp|fatedier/frp|frpc' 'frps|fatedier/frp|frps' 'gost|go-gost/gost|gost' 'trivy|aquasecurity/trivy|trivy' 'syft|anchore/syft|syft' 'grype|anchore/grype|grype';do IFS='|' read -r t r b <<<"$spec";gh_release "$t" "$r" "$b" "$RX";done

# Repositories: source-only installs, no long compilation.
git_clone gitrob https://github.com/michenriksen/gitrob.git /opt/security-tools/gitrob
git_clone PEASS-ng https://github.com/peass-ng/PEASS-ng.git /opt/security-tools/PEASS-ng
git_clone pspy https://github.com/DominicBreuker/pspy.git /opt/security-tools/pspy
git_clone firmwalker https://github.com/craigz28/firmwalker.git /opt/security-tools/firmwalker
# --- 第二批（2026-10-06 补装）：钓鱼演练 / 载荷生成 / 持久化分析 / 渗透知识库 ---
git_clone EvilClippy https://github.com/outflanknl/EvilClippy.git /opt/security-tools/EvilClippy
git_clone ScareCrow https://github.com/NetSPI/ScareCrow.git /opt/security-tools/ScareCrow
git_clone CUpp https://github.com/MebTech/cupp.git /opt/security-tools/CUpp
# 渗透知识库（轻量，纯文本，检索价值高）
git_clone GTFOBins https://github.com/GTFOBins/GTFOBins.git /opt/security-tools/GTFOBins
git_clone LOLBAS https://github.com/LOLBAS-Project/LOLBAS.git /opt/security-tools/LOLBAS
git_clone HackTricks https://github.com/HackTricks/HackTricks.git /opt/security-tools/HackTricks
# 体积较大的规则库：默认跳过，按需开启（SETUP_BIGRULES=1）
if [[ ${SETUP_BIGRULES:-0} == 1 ]]; then
  git_clone SigmaHQ https://github.com/SigmaHQ/sigma.git /opt/security-tools/sigma
  git_clone PayloadsAllTheThings https://github.com/swisskyrepo/PayloadsAllTheThings.git /opt/security-tools/PayloadsAllTheThings
  git_clone SecLists https://github.com/danielmiessler/SecLists.git /opt/security-tools/SecLists
else
  record git SigmaHQ SKIPPED 0 'set SETUP_BIGRULES=1 to install (large rule repo)'
  record git PayloadsAllTheThings SKIPPED 0 'set SETUP_BIGRULES=1 to install (large payload repo)'
  record git SecLists SKIPPED 0 'set SETUP_BIGRULES=1 to install (large wordlist repo)'
fi
# Requested unicornscan source copy; upstream is C, while requests/colorama were installed as requested.
if [[ ! -f "$ROOT/tools/scripts/net/unicornscan/README" && ! -f "$ROOT/tools/scripts/net/unicornscan/README.md" ]];then rm -rf "$ROOT/tools/scripts/net/unicornscan"; timeout 120s git clone --depth 1 https://github.com/dneufeld/unicornscan.git "$ROOT/tools/scripts/net/unicornscan" >"$LOGDIR/git-unicornscan.log" 2>&1; r=$?; rm -rf "$ROOT/tools/scripts/net/unicornscan/.git"; else r=0;fi
[[ $r == 0 ]] && record git unicornscan PASS 0 "$ROOT/tools/scripts/net/unicornscan" || record git unicornscan FAIL "$r" "$LOGDIR/git-unicornscan.log"

# massdns has no reliable official prebuilt release: bounded source build fallback.
if ! command -v massdns >/dev/null;then
 rm -rf /tmp/massdns; timeout 120s git clone --depth 1 https://github.com/blechschmidt/massdns.git /tmp/massdns >"$LOGDIR/massdns-build.log" 2>&1 && timeout 120s make -C /tmp/massdns >>"$LOGDIR/massdns-build.log" 2>&1 && sudo install -m755 /tmp/massdns/bin/massdns /usr/local/bin/massdns >>"$LOGDIR/massdns-build.log" 2>&1; r=$?;else r=0;fi
[[ $r == 0 ]] && record build massdns PASS 0 /usr/local/bin/massdns || record build massdns FAIL "$r" "$LOGDIR/massdns-build.log"

TOOL_LOG_DIR="$LOGDIR" bash "$ROOT/tools/setup_full_fallbacks.sh"
# 第三批（2026-10-06）：补齐 Ghidra/Windows/内存取证/情报/侦察取证 五大真缺口
if [[ ${SETUP_ADVANCED:-1} == 1 ]];then TOOL_LOG_DIR="$LOGDIR" bash "$ROOT/tools/setup_advanced.sh";fi
# B tier is intentionally record-only: metasploit-framework, Ghidra/headless, rockyou, SecLists.
# C tier is intentionally skipped: GUI/commercial/hardware-only/long C2 builds/Docker-in-sandbox.
record policy B-tier ONLY_RECORD 0 'see TOOLS.md for commands and size'
record policy C-tier SKIPPED 0 'see TOOLS.md for reasons'
echo "status=$STATUS"

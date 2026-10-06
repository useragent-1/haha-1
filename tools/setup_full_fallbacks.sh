#!/usr/bin/env bash
# Bounded fallbacks for A-tier tools absent from Debian/PyPI or with nonstandard release assets.
set -u
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.."&&pwd); LOGDIR=${TOOL_LOG_DIR:-/home/user/tool-install-logs}; STATUS="$LOGDIR/status.tsv"; mkdir -p "$LOGDIR"; sudo mkdir -p /opt/security-tools
rec(){ printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" | tee -a "$STATUS"; }
rel(){ local t=$1 r=$2 b=$3 rx=$4 rn=${5:-};local l="$LOGDIR/fallback-$t.log";local check=${rn:-$b};if command -v "$check" >/dev/null;then rec fallback "$t" PASS 0 "$(command -v "$check")";return;fi;local a=(python3 "$ROOT/tools/install_github_release.py" "$r" "$b" --asset-regex "$rx");[[ -n $rn ]]&&a+=(--rename "$rn");timeout 120s "${a[@]}" >"$l" 2>&1;local x=$?;[[ $x == 0 ]]&&rec fallback "$t" PASS 0 installed||rec fallback "$t" FAIL "$x" "$l";}
clone(){ local t=$1 u=$2 d=$3 l="$LOGDIR/fallback-$1.log";if [[ -d $d ]];then rec fallback "$t" PASS 0 "$d";return;fi;timeout 120s sudo git clone --depth 1 "$u" "$d" >"$l" 2>&1;local x=$?;[[ $x == 0 ]]&&rec fallback "$t" PASS 0 "$d"||rec fallback "$t" FAIL "$x" "$l";}
pipx(){ local t=$1 spec=$2 l="$LOGDIR/fallback-$1.log";timeout 120s python3 -m pip install --no-cache-dir "$spec" >"$l" 2>&1;local x=$?;[[ $x == 0 ]]&&rec fallback "$t" PASS 0 "$spec"||rec fallback "$t" FAIL "$x" "$l";}
rel floss mandiant/flare-floss floss '(?i)linux\.zip$'
rel gitleaks gitleaks/gitleaks gitleaks '(?i)linux_x64\.tar\.gz$'
rel findomain Findomain/Findomain findomain '(?i)findomain-linux\.zip$'
rel ligolo-ng nicocha30/ligolo-ng proxy '(?i)proxy.*linux_amd64\.tar\.gz$' ligolo-proxy
rel chisel jpillora/chisel chisel '(?i)linux_amd64\.gz$'
rel trivy aquasecurity/trivy trivy '(?i)Linux-64bit\.tar\.gz$'
rel feroxbuster epi052/feroxbuster feroxbuster '(?i)x86_64-linux-feroxbuster\.zip$'
rel radare2 radareorg/radare2 r2 '(?i)radare2_[0-9][^/]*_amd64\.deb$'
# Correct packages/repositories where requested package names do not exist.
pipx wapiti wapiti3
pipx droopescan 'git+https://github.com/SamJoan/droopescan.git'
pipx zeek-client zeek-client
pipx tlsh py-tlsh
for spec in 'nikto|https://github.com/sullo/nikto.git|/opt/security-tools/nikto' 'theHarvester|https://github.com/laramies/theHarvester.git|/opt/security-tools/theHarvester' 'joomscan|https://github.com/OWASP/joomscan.git|/opt/security-tools/joomscan' 'enum4linux|https://github.com/CiscoCXSecurity/enum4linux.git|/opt/security-tools/enum4linux' 'cmseek|https://github.com/Tuhinshubhra/CMSeeK.git|/opt/security-tools/CMSeeK' 'recon-ng|https://github.com/lanmaster53/recon-ng.git|/opt/security-tools/recon-ng' 'wifite2|https://github.com/derv82/wifite2.git|/opt/security-tools/wifite2' 'lazagne|https://github.com/AlessandroZ/LaZagne.git|/opt/security-tools/LaZagne' 'firmwalker|https://github.com/scriptingxss/firmwalker.git|/opt/security-tools/firmwalker' 'unicornscan|https://github.com/dneufeld/unicornscan.git|/opt/security-tools/unicornscan';do IFS='|' read -r t u d<<<"$spec";clone "$t" "$u" "$d";done
# Short source builds only.
if ! command -v radamsa >/dev/null;then rm -rf /tmp/radamsa;timeout 120s git clone --depth 1 https://gitlab.com/akihe/radamsa.git /tmp/radamsa >"$LOGDIR/fallback-radamsa.log" 2>&1&&timeout 120s make -C /tmp/radamsa >>"$LOGDIR/fallback-radamsa.log" 2>&1&&sudo install -m755 /tmp/radamsa/bin/radamsa /usr/local/bin/radamsa >>"$LOGDIR/fallback-radamsa.log" 2>&1;x=$?;else x=0;fi;[[ $x == 0 ]]&&rec fallback radamsa PASS 0 installed||rec fallback radamsa FAIL "$x" "$LOGDIR/fallback-radamsa.log"
# Bounded Go installs for projects with no release artifact.
mkdir -p /tmp/go-security-bin
for spec in 'assetfinder|github.com/tomnomnom/assetfinder@latest|assetfinder' 'shhgit|github.com/eth0izzle/shhgit@latest|shhgit';do IFS='|' read -r t mod b<<<"$spec";l="$LOGDIR/fallback-$t.log";timeout 120s env GOBIN=/tmp/go-security-bin go install "$mod" >"$l" 2>&1;x=$?;if [[ $x == 0 && -f /tmp/go-security-bin/$b ]];then sudo install -m755 /tmp/go-security-bin/$b /usr/local/bin/$b;rec fallback "$t" PASS 0 /usr/local/bin/$b;else rec fallback "$t" FAIL "$x" "$l";fi;done
# Speakeasy requires unicorn 1.0.2 while qiling/pwntools require unicorn 2.x: isolate it.
if [[ ! -x /opt/security-tools/venvs/speakeasy/bin/python ]];then sudo python3 -m venv /opt/security-tools/venvs/speakeasy;sudo /opt/security-tools/venvs/speakeasy/bin/pip install --no-cache-dir speakeasy-emulator 'setuptools<81' >"$LOGDIR/fallback-speakeasy.log" 2>&1;fi
timeout 20s /opt/security-tools/venvs/speakeasy/bin/python -c 'import speakeasy' >>"$LOGDIR/fallback-speakeasy.log" 2>&1;x=$?;[[ $x == 0 ]]&&rec fallback speakeasy PASS 0 /opt/security-tools/venvs/speakeasy||rec fallback speakeasy FAIL "$x" "$LOGDIR/fallback-speakeasy.log"
# Ruby WPScan; bounded because native gems may compile.
if command -v wpscan >/dev/null;then rec fallback wpscan PASS 0 "$(command -v wpscan)";else timeout 120s sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ruby-dev >"$LOGDIR/fallback-wpscan-rubydev.log" 2>&1;timeout 120s sudo gem install wpscan --no-document >"$LOGDIR/fallback-wpscan.log" 2>&1;x=$?;[[ $x == 0 ]]&&rec fallback wpscan PASS 0 installed||rec fallback wpscan FAIL "$x" "$LOGDIR/fallback-wpscan.log";fi

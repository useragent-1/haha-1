# 目标报告：/usr/bin/socat-mux.sh

## 当前阶段 / Current phase
脚本分诊、密码扫描、YARA、语法验证和控制流审阅完成。

## 已验证事实 / Verified facts
- SHA-256：`a3cf824ff5822fdcefa3e880efb7e118b4cd3463867ba1ed44d48a4e3f9312e2`；大小 4,490 字节。
- Bash 脚本；`bash -n` 返回 0。
- 未发现密码常量、高熵区或混淆字符串。
- 功能是启动两个 socat 进程，通过 loopback IPv4 broadcast 实现 many-to-one / one-to-all 转发。
- 固定地址：`127.0.0.1` 与 `127.255.255.255`；示例地址 `[REDACTED:.3.4]` 仅出现在帮助文本。

## 关键证据 / Key evidence
### 函数级/逻辑块深挖
- 逻辑块名：`top-level multiplexer main`
- 字节偏移/行号：端口选择 `0x9c9`（第 84 行）起；转发进程 `0xfd8`（第 127 行）与 `0x10fb`（第 137 行）；等待 `0x117c`（第 142 行）。

近似反编译：
```text
选择两个空闲 UDP loopback 端口；若 socat 自动分配失败则用 $RANDOM 并通过 ss/netstat 查冲突。
安装 EXIT/SIGCHLD trap。
启动 muxfwd：TARGET <-> 127.255.255.255:PORT2（本地绑定 PORT1）。
启动 muxlst：LISTENER <-> 127.0.0.1:PORT1（本地绑定 PORT2）。
等待任一子进程退出并清理另一进程。
```

存在典型 TOCTOU 窗口：备用路径先用 `ss` 检查端口，再由 socat 绑定；本地同权限竞争者理论上可抢占端口。但这是可靠性风险，尚无权限提升证据。

### 流水线原始输出
```text
$ python /home/user/ha-ha/scripts/auto_analyze.py /usr/bin/socat-mux.sh --out /home/user/case/socat-mux/auto/
[+] Analysis complete: /home/user/case/socat-mux/auto/auto_analysis.json
[+] Report: /home/user/case/socat-mux/auto/auto_analysis.md
[+] YARA rule: /home/user/case/socat-mux/auto/socat-mux.sh.yar
[exit=0]

$ python /home/user/ha-ha/scripts/find_crypto.py /usr/bin/socat-mux.sh --out /home/user/case/socat-mux/crypto/
[*] Scanning socat-mux.sh (4,490 bytes)...
[+] Found 0 crypto indicators
[+] Output: /home/user/case/socat-mux/crypto/crypto_scan.json, /home/user/case/socat-mux/crypto/crypto_scan.md
[exit=0]

$ python /home/user/ha-ha/scripts/yara_gen.py /usr/bin/socat-mux.sh --out /home/user/case/socat-mux/yara/
[*] Analyzing socat-mux.sh (4,490 bytes) — unknown (.sh)
[*] Extracted 110 ASCII + 0 Unicode strings
[*] Selected 15 strings for rule
[*] Extracted 0 byte patterns
[+] Generated rule: /home/user/case/socat-mux/yara/socat-mux.yar
[+] Strings: 15, Hex patterns: 0
[exit=0]

$ python /home/user/ha-ha/scripts/shellcode_tools.py strings /usr/bin/socat-mux.sh --obfuscated --ascii --min-len 4
Obfuscated string analysis for /usr/bin/socat-mux.sh:
[exit=0]

```

### 深挖原始输出
```text
$ bash -n /usr/bin/socat-mux.sh; echo exit=$?
exit=0

$ nl -ba /usr/bin/socat-mux.sh | sed -n "75,145p"
    75	
    76	# When run as root we try low ports
    77	LOWPORT=
    78	PATTERN=bound
    79	if [ "$(id -u)" = 0 ]; then
    80	    LOWPORT="lowport"
    81	    PATTERN="successfully prepared local socket"
    82	fi
    83	
    84	# We need two free UDP ports (on loopback)
    85	if [ -z "$LOWPORT" ]; then
    86	    PORT1=$($SOCAT -d -d -T 0.000001 UDP4-RECV:0 /dev/null 2>&1 |grep "$PATTERN" |sed 's/.*:\([1-9][0-9]*\)$/\1/')
    87	    PORT2=$($SOCAT -d -d -T 0.000001 UDP4-RECV:0 /dev/null 2>&1 |grep "$PATTERN" |sed 's/.*:\([1-9][0-9]*\)$/\1/')
    88	fi
    89	if [ -z "$PORT1" -o -z "$PORT2" ]; then
    90	    # Probably old Socat version, use a different approach
    91	    if type ss >/dev/null 2>&1; then
    92		:
    93	    elif type netstat >/dev/null 2>&1; then
    94		alias ss=netstat
    95	    else
    96		echo "$0: Failed to determine free UDP ports (old Socat version, no ss, no netstat?)" >&2
    97		exit 1
    98	    fi
    99	    PORT1= PORT2=
   100	    while [ -z "$PORT1" -o -z "$PORT2" -o "$PORT1" = "$PORT2" ] || ss -aun |grep -e ":$PORT1\>" -e ":$PORT2\>" >/dev/null; do
   101		if [ -z "$LOWPORT" ]; then
   102		    PORT1=$((16384+RANDOM))
   103		    PORT2=$((16384+RANDOM))
   104		else
   105		    PORT1=$((512+(RANDOM>>6) ))
   106		    PORT2=$((512+(RANDOM>>6) ))
   107		fi
   108	    done
   109	fi
   110	[ "$VERBOSE" ] && echo "# $0: Using UDP ports $PORT1, $PORT2" >&2
   111	
   112	IFADDR=127.0.0.1
   113	BCADDR=127.255.255.255
   114	
   115	
   116	pid1= pid2=
   117	trap '[ "$pid1" ] && kill $pid1 2>/dev/null; [ "$pid2" ] && kill $pid2 2>/dev/null' EXIT
   118	
   119	set -bm
   120	trap 'if kill -n 0 $pid1 2>/dev/null; then [ -z "$QUIET" ] && echo "$0: socat-listener exited with rc=$?" >&2; kill $pid1; else [ -z "$QUIET" ] && echo "$0: socat-multiplexer exited with rc=$?" >&2; kill $pid2 2>/dev/null; fi; exit 1' SIGCHLD
   121	
   122	if [ "$VERBOSE" ]; then
   123	    $ECHO "$SOCAT -lp muxfwd $OPTS \\
   124		\"$TARGET\" \\
   125		\"UDP4-DATAGRAM:$BCADDR:$PORT2,bind=$IFADDR:$PORT1,so-broadcast\" &"
   126	fi
   127	$SOCAT -lp muxfwd $OPTS \
   128	    "$TARGET" \
   129	    "UDP4-DATAGRAM:$BCADDR:$PORT2,bind=$IFADDR:$PORT1,so-broadcast" &
   130	pid1=$!
   131	
   132	if [ "$VERBOSE" ]; then
   133	    $ECHO "$SOCAT -lp muxlst $OPTS \\
   134	    	\"$LISTENER\" \\
   135	        \"UDP4-DATAGRAM:$IFADDR:$PORT1,bind=:$PORT2,so-broadcast,so-reuseaddr\" &"
   136	fi
   137	$SOCAT -lp muxlst $OPTS \
   138	    "$LISTENER" \
   139	    "UDP4-DATAGRAM:$IFADDR:$PORT1,bind=:$PORT2,so-broadcast,so-reuseaddr" &
   140	pid2=$!
   141	
   142	wait
   143	#wait -f

$ grep -nE "RANDOM|UDP4-DATAGRAM|trap|socat" /usr/bin/socat-mux.sh
14:#   socat-mux.sh \
71:    */*) if [ -x ${0%/*}/socat ]; then SOCAT=${0%/*}/socat; fi ;;
73:if [ -z "$SOCAT" ]; then SOCAT=socat; fi
102:	    PORT1=$((16384+RANDOM))
103:	    PORT2=$((16384+RANDOM))
105:	    PORT1=$((512+(RANDOM>>6) ))
106:	    PORT2=$((512+(RANDOM>>6) ))
117:trap '[ "$pid1" ] && kill $pid1 2>/dev/null; [ "$pid2" ] && kill $pid2 2>/dev/null' EXIT
120:trap 'if kill -n 0 $pid1 2>/dev/null; then [ -z "$QUIET" ] && echo "$0: socat-listener exited with rc=$?" >&2; kill $pid1; else [ -z "$QUIET" ] && echo "$0: socat-multiplexer exited with rc=$?" >&2; kill $pid2 2>/dev/null; fi; exit 1' SIGCHLD
125:	\"UDP4-DATAGRAM:$BCADDR:$PORT2,bind=$IFADDR:$PORT1,so-broadcast\" &"
129:    "UDP4-DATAGRAM:$BCADDR:$PORT2,bind=$IFADDR:$PORT1,so-broadcast" &
135:        \"UDP4-DATAGRAM:$IFADDR:$PORT1,bind=:$PORT2,so-broadcast,so-reuseaddr\" &"
139:    "UDP4-DATAGRAM:$IFADDR:$PORT1,bind=:$PORT2,so-broadcast,so-reuseaddr" &
```

## 推断与置信度 / Inference and confidence
- 这是合法 socat 辅助脚本，不是恶意转发器：高置信度（包路径、版权、完整逻辑一致）。
- `$RANDOM` 端口选择不是安全随机数，但这里只用于临时端口：高置信度。

## 风险/漏洞候选 / Risk or vulnerability candidates
- 备用端口选择存在检查与绑定之间的竞争窗口：低严重度候选。
- `$OPTS` 故意进行 shell word splitting；调用者若把不可信数据直接拼入 options，可能产生参数注入，但脚本本身不执行 `eval`。

## 利用可行性 / Exploitability assessment
未见直接命令注入。端口竞争最多可能导致拒绝服务或错误绑定，需并发复现才可确认。

## 建议下一步 / Suggested next steps
1. 用并发端口抢占测试验证 TOCTOU。
2. 使用数组重写 `$OPTS`，消除非预期分词。
3. 为 YARA 规则加入包版本或版权字符串约束。

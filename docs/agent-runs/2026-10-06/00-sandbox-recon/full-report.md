# 沙箱环境侦察：阶段 0–7 完整报告

## 当前阶段 / Current phase

阶段 0–7 已连续执行完成：装载协议、工具链武装、环境侦察、控制面与出口、权限与隔离、公网出口、报告、记忆写回、技能沉淀。

## 已验证事实 / Verified facts

1. 仓库已克隆至 `/home/user/ha-ha`；`scripts/setup.sh` 的 `triage_artifact`、`find_crypto`、`auto_analyze` 自检均为 `OK`。
2. `binutils`、`file`、`xxd`、`jq`、`ripgrep` 安装命令成功；`auto_analyze.py --help` 正常返回帮助。
3. 环境为 Debian 13、Linux `6.1.158+`、用户 `user`（UID 1000），环境变量标识 `E2B_SANDBOX=true`。
4. 网络接口地址为 `169.254.0.21/30`，默认网关 `169.254.0.22`；`events.e2b.local` 指向 `192.0.2.1`。
5. `envd` 版本 `0.6.10`，默认端口 `49983`；当前两条 `10.12.0.124` 私网连接由 PID 359 `envd` 持有。
6. 8888 服务响应头为 `TornadoServer/6.5.7`，进程命令行显示 Jupyter Server 以 root 运行，`IdentityProvider.token` 字段存在且值已按凭据规则遮蔽。
7. `192.0.2.1:80` 可达并返回 HTTP 404 JSON 操作路由错误；未进一步枚举操作。
8. 出口 CA 为 `O=E2B, CN=E2B Proxy CA`；当前未发现显式 proxy 环境变量，iptables filter/NAT 表无自定义规则。
9. `sudo -n true` 返回 `sudo_exit=0`；当前用户可无交互 sudo。
10. 公网出口可用：`arena.ai` 返回 200（本次远端 IP `104.18.15.206`），GitHub Raw 根路径返回 301。
11. `MEMORY_UPDATE.md` 已生成 5 条进度记录；`sandbox-recon` 技能及 SKILLS 路由已写入工作区仓库。

## 关键证据 / Key evidence

> 以下保留各阶段完整命令输出。命令本身包含的 `head` 是用户指定采集边界，不属于报告二次截断。敏感字段扫描命中 `Set-Cookie` 与 `--IdentityProvider.token`；值按要求打码，仅保留末 4 位或标注为空。

### 阶段 0：工具链武装——原始输出

```text
===== 阶段0 工具链武装 =====
$ git clone https://github.com/useragent-1/haha-1.git /home/user/ha-ha
Cloning into '/home/user/ha-ha'...

$ cd /home/user/ha-ha && bash scripts/setup.sh
[1/4] updating /home/user/ha-ha
Already up to date.
[2/4] installing python deps (capstone, unicorn)
[3/4] self test
  triage_artifact: OK
  find_crypto: OK
  auto_analyze: OK
[4/4] TOOLCHAIN READY at /home/user/ha-ha

$ sudo apt-get update -qq && sudo apt-get install -y -qq binutils file xxd jq ripgrep
debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
debconf: unable to initialize frontend: Teletype
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Noninteractive
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 38546 files and directories currently installed.)
Preparing to unpack .../jq_1.7.1-6+deb13u4_amd64.deb ...
Unpacking jq (1.7.1-6+deb13u4) over (1.7.1-6+deb13u2) ...
Preparing to unpack .../libjq1_1.7.1-6+deb13u4_amd64.deb ...
Unpacking libjq1:amd64 (1.7.1-6+deb13u4) over (1.7.1-6+deb13u2) ...
Selecting previously unselected package ripgrep.
Preparing to unpack .../ripgrep_14.1.1-1+b4_amd64.deb ...
Unpacking ripgrep (14.1.1-1+b4) ...
Selecting previously unselected package xxd.
Preparing to unpack .../xxd_2%3a9.1.1230-2_amd64.deb ...
Unpacking xxd (2:9.1.1230-2) ...
Setting up libjq1:amd64 (1.7.1-6+deb13u4) ...
Setting up xxd (2:9.1.1230-2) ...
Setting up ripgrep (14.1.1-1+b4) ...
Setting up jq (1.7.1-6+deb13u4) ...
Processing triggers for libc-bin (2.41-12+deb13u3) ...

$ python /home/user/ha-ha/scripts/auto_analyze.py --help
usage: auto_analyze.py [-h] [--out OUT] [--skip-yara] [--json] [--quick]
                       artifact

auto_analyze — one-click comprehensive binary analysis

positional arguments:
  artifact       Path to the artifact to analyze

options:
  -h, --help     show this help message and exit
  --out, -o OUT  Output directory (default: ./auto_analysis)
  --skip-yara    Skip YARA rule generation
  --json         Print JSON to stdout
  --quick        Quick mode: only read first 2MB
```

### 阶段 1–4：环境、控制面、权限与公网出口——原始输出

```text
================ 阶段1 环境侦察 ================
--- A 身份 ---
$ whoami; id; uname -a; cat /etc/os-release | head -3; cat /proc/1/cgroup
user
uid=1000(user) gid=1000(user) groups=1000(user),27(sudo),100(users)
Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Fri Jul 17 14:31:34 UTC 2026 x86_64 GNU/Linux
PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
NAME="Debian GNU/Linux"
VERSION_ID="13"
0::/init.scope

--- B 环境变量 ---
$ env | sort
E2B_EVENTS_ADDRESS=http://192.0.2.1
E2B_SANDBOX=true
E2B_SANDBOX_ID=iq3bhk4ca1e3to3y8kzoe
E2B_TEMPLATE_ID=nlhz8vlwyupq845jsdg9
HOME=/home/user
LOGNAME=user
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
PWD=/home/user
SHELL=/bin/bash
SHLVL=2
USER=user
_=/usr/bin/env

--- C 网络 ---
$ cat /etc/hosts; cat /etc/resolv.conf; ip addr; ip route; ss -tlnp
127.0.0.1        localhost
::1              localhost ip6-localhost ip6-loopback
fe00::           ip6-localnet
ff00::           ip6-mcastprefix
ff02::1          ip6-allnodes
ff02::2          ip6-allrouters
127.0.1.1        e2b.local
192.0.2.1        events.e2b.local
nameserver 8.8.8.81: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host proto kernel_lo 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:fc:00:00:00:05 brd ff:ff:ff:ff:ff:ff
    inet 169.254.0.21/30 brd 169.254.0.23 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::fc:ff:fe00:5/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
default via 169.254.0.22 dev eth0 
169.254.0.20/30 dev eth0 proto kernel scope link src 169.254.0.21 
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
LISTEN 0      100        127.0.0.1:35769      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:47945      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:34675      0.0.0.0:*          
LISTEN 0      4096         0.0.0.0:111        0.0.0.0:*          
LISTEN 0      5       169.254.0.21:35769      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:47945      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:34675      0.0.0.0:*          
LISTEN 0      128        127.0.0.1:8888       0.0.0.0:*          
LISTEN 0      5       169.254.0.21:8888       0.0.0.0:*          
LISTEN 0      100        127.0.0.1:44461      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:35105      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:39379      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:41435      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:43501      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:35105      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:44461      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:39379      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:41435      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:43501      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:60465      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:53335      0.0.0.0:*          
LISTEN 0      5       169.254.0.21:60493      0.0.0.0:*          
LISTEN 0      2048         0.0.0.0:49999      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:60465      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:60493      0.0.0.0:*          
LISTEN 0      100        127.0.0.1:53335      0.0.0.0:*          
LISTEN 0      4096            [::]:111           [::]:*          
LISTEN 0      4096               *:22               *:*          
LISTEN 0      128            [::1]:8888          [::]:*          
LISTEN 0      4096               *:49983            *:*          

--- D 进程与文件系统 ---
$ ps aux; ls -la /; ls -la /home/user ~; ls -la /tmp
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.6  0.6  23024 13988 ?        Ss   02:17   0:00 /sbin/init
root           2  0.0  0.0      0     0 ?        S    02:17   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        I<   02:17   0:00 [rcu_gp]
root           4  0.0  0.0      0     0 ?        I<   02:17   0:00 [rcu_par_gp]
root           5  0.0  0.0      0     0 ?        I<   02:17   0:00 [slub_flushwq]
root           6  0.0  0.0      0     0 ?        I<   02:17   0:00 [netns]
root           7  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/0:0-events]
root           8  0.0  0.0      0     0 ?        I<   02:17   0:00 [kworker/0:0H-events_highpri]
root           9  0.3  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:0-ext4-rsv-conversion]
root          10  0.0  0.0      0     0 ?        I<   02:17   0:00 [mm_percpu_wq]
root          11  0.0  0.0      0     0 ?        I    02:17   0:00 [rcu_tasks_kthread]
root          12  0.0  0.0      0     0 ?        I    02:17   0:00 [rcu_tasks_rude_kthread]
root          13  0.0  0.0      0     0 ?        I    02:17   0:00 [rcu_tasks_trace_kthread]
root          14  0.0  0.0      0     0 ?        S    02:17   0:00 [ksoftirqd/0]
root          15  0.0  0.0      0     0 ?        I    02:17   0:00 [rcu_preempt]
root          16  0.0  0.0      0     0 ?        S    02:17   0:00 [migration/0]
root          17  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/0:1-cgroup_offline]
root          18  0.0  0.0      0     0 ?        S    02:17   0:00 [cpuhp/0]
root          19  0.0  0.0      0     0 ?        S    02:17   0:00 [cpuhp/1]
root          20  0.0  0.0      0     0 ?        S    02:17   0:00 [migration/1]
root          21  0.0  0.0      0     0 ?        S    02:17   0:00 [ksoftirqd/1]
root          22  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/1:0-events]
root          23  0.0  0.0      0     0 ?        I<   02:17   0:00 [kworker/1:0H-events_highpri]
root          25  0.1  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:1-events_unbound]
root          26  0.0  0.0      0     0 ?        S    02:17   0:00 [kdevtmpfs]
root          27  0.0  0.0      0     0 ?        I<   02:17   0:00 [inet_frag_wq]
root          28  0.0  0.0      0     0 ?        S    02:17   0:00 [kauditd]
root          29  0.0  0.0      0     0 ?        S    02:17   0:00 [khungtaskd]
root          30  0.0  0.0      0     0 ?        S    02:17   0:00 [oom_reaper]
root          31  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:2-flush-254:0]
root          32  0.0  0.0      0     0 ?        I<   02:17   0:00 [writeback]
root          33  0.0  0.0      0     0 ?        S    02:17   0:00 [kcompactd0]
root          34  0.0  0.0      0     0 ?        SN   02:17   0:00 [ksmd]
root          35  0.0  0.0      0     0 ?        SN   02:17   0:00 [khugepaged]
root          36  0.0  0.0      0     0 ?        I<   02:17   0:00 [kintegrityd]
root          37  0.0  0.0      0     0 ?        I<   02:17   0:00 [kblockd]
root          38  0.0  0.0      0     0 ?        I<   02:17   0:00 [blkcg_punt_bio]
root          39  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/1:1-events_power_efficient]
root          40  0.0  0.0      0     0 ?        S    02:17   0:00 [watchdogd]
root          41  0.0  0.0      0     0 ?        I<   02:17   0:00 [rpciod]
root          42  0.0  0.0      0     0 ?        I<   02:17   0:00 [xprtiod]
root          43  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:3-flush-254:0]
root          47  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:4-flush-254:0]
root          53  0.0  0.0      0     0 ?        I<   02:17   0:00 [kworker/1:1H-kblockd]
root          68  0.0  0.0      0     0 ?        S    02:17   0:00 [kswapd0]
root          71  0.0  0.0      0     0 ?        I<   02:17   0:00 [nfsiod]
root          72  0.0  0.0      0     0 ?        I<   02:17   0:00 [kworker/0:1H-kblockd]
root          74  0.0  0.0      0     0 ?        I<   02:17   0:00 [xfsalloc]
root          76  0.0  0.0      0     0 ?        I<   02:17   0:00 [xfs_mru_cache]
root          79  0.0  0.0      0     0 ?        I<   02:17   0:00 [kthrotld]
root          82  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/0:2-cgroup_free]
root          84  0.0  0.0      0     0 ?        S    02:17   0:00 [irq/24-ACPI:Ged]
root         117  0.0  0.0      0     0 ?        S    02:17   0:00 [hwrng]
root         141  0.0  0.0      0     0 ?        I<   02:17   0:00 [iscsi_conn_clea]
root         165  0.0  0.0      0     0 ?        I<   02:17   0:00 [mld]
root         166  0.0  0.0      0     0 ?        I<   02:17   0:00 [ipv6_addrconf]
root         173  0.0  0.0   1004     4 ?        S    02:17   0:00 bpfilter_umh
root         174  0.0  0.0      0     0 ?        I<   02:17   0:00 [kstrp]
root         179  0.0  0.0      0     0 ?        I<   02:17   0:00 [zswap-shrink]
root         180  0.0  0.0      0     0 ?        I<   02:17   0:00 [kworker/u5:0]
root         257  0.1  0.0      0     0 ?        S    02:17   0:00 [jbd2/vda-8]
root         258  0.0  0.0      0     0 ?        I<   02:17   0:00 [ext4-rsv-conver]
root         290  0.1  0.4  29440  8864 ?        Ss   02:17   0:00 /usr/lib/systemd/systemd-journald
root         300  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/1:2-events]
root         305  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/1:3-events]
systemd+     308  0.1  0.5  20752 10316 ?        Ss   02:17   0:00 /usr/lib/systemd/systemd-networkd
_rpc         336  0.0  0.0   6560  1992 ?        Ss   02:17   0:00 /usr/sbin/rpcbind -f -w
message+     340  0.0  0.1   6828  3624 ?        Ss   02:17   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
root         341  0.0  0.3  18384  7176 ?        Ss   02:17   0:00 /usr/lib/systemd/systemd-logind
root         359  1.7  1.2 1272548 25744 ?       S<Lsl 02:17   0:00 /usr/bin/envd
root         387  0.0  0.3  11760  7732 ?        Ss   02:17   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root         392  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/0:3-events]
root         393  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/0:4-events]
root         421  0.0  0.0   5168  1584 tty1     Ss+  02:17   0:00 /sbin/agetty -o -- \u --noreset --noclear - linux
root         422  0.0  0.0   5248   204 ?        Ss   02:17   0:00 /usr/sbin/blkmapd
root         437  6.1  4.8 256320 98260 ?        Ssl  02:17   0:01 /usr/local/bin/python3.13 /usr/local/bin/jupyter-server --IdentityProvider.token=[REDACTED:last4=ty)]]
root         463  2.3  3.2 371148 66132 ?        Ssl  02:17   0:00 /root/.server/.venv/bin/python /root/.server/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 49999 --workers 1 --no-access-log --no-use-colors --timeout-keep-alive 640
root         470  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:8888,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:8888
root         475  1.8  3.6 771316 73436 ?        Ssl  02:17   0:00 /usr/local/bin/python3.13 -Xfrozen_modules=off -m ipykernel_launcher -f /root/.local/share/jupyter/runtime/kernel-6bd8c74e-fd89-448c-9e6a-22de9783e8b5.json
root         490  1.4  2.9 1101532 60480 ?       Ssl  02:17   0:00 node /usr/bin/ijskernel --hide-undefined /root/.local/share/jupyter/runtime/kernel-1fe44cf5-e7f2-4ee3-82b8-24ac60d6d93f.json --protocol=5.1
root         504  0.0  1.9 728296 39900 ?        Sl   02:17   0:00 /usr/bin/node --eval (async function() { /*  * BSD 3-Clause License  *  * Copyright (c) 2018, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* eslint-disable no-unused-vars */ var console = require("console"); var stream = require("stream"); var util = require("util"); var vm = require("vm"); /* eslint-enable no-unused-vars */  /*  * BSD 3-Clause License  *  * Copyright (c) 2015, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* global console */ /* global stream */ /* global util */  /* global Promise */  /* global log */ /* global Display */  function Stdout(contextId, opt) {     stream.Transform.call(this, opt);      this._contextId = contextId; }  Stdout.prototype = Object.create(stream.Transform.prototype);  Stdout.prototype._transform = function(data, encoding, callback) {     var response = {         id: this._contextId,         stdout: data.toString(),     };     log("STDOUT:", response);     process.send(response);     this.push(data);     callback(); };  function Stderr(contextId, opt) {     stream.Transform.call(this, opt);      this._contextId = contextId; }  Stderr.prototype = Object.create(stream.Transform.prototype);  Stderr.prototype._transform = function(data, encoding, callback) {     var response = {         id: this._contextId,         stderr: data.toString(),     };     log("STDERR:", response);     process.send(response);     this.push(data);     callback(); };  function Requester(contextId) {     // context id     this.contextId = contextId;      // id for next request     this.requestId = 0;      // callback associated with a request (indexed by id)     this.callbacks = {};      // the Promise resolve callback associated with a request (indexed by id)     this.resolves = {};      // the Promise reject callback associated with a request (indexed by id)     this.rejects = {}; }  // send a request Requester.prototype.send = function send(request, callback) {     var requestId = this.requestId++;     request.id = requestId;      if (callback) {         this.callbacks[requestId] = callback;     }      var promise;     if (global.Promise) {         promise = new Promise(function(resolve, reject) {             this.resolves[requestId] = resolve;             this.rejects[requestId] = reject;         }.bind(this));     }      process.send({         id: this.contextId,         request: request,     });      return promise; };  // pass reply to the callbacks associated with a request Requester.prototype.receive = function receive(requestId, reply) {     var callback = this.callbacks[requestId];     if (callback) {         delete this.callbacks[requestId];         callback(null, reply);     }      var resolve = this.resolves[requestId];     if (resolve) {         delete this.resolves[requestId];         delete this.rejects[requestId];         resolve(reply);     } };  function Context(id) {     this.id = id;      this.requester = new Requester(this.id);      this.stdout = new Stdout(this.id);     this.stderr = new Stderr(this.id);     this.console = new console.Console(this.stdout, this.stderr);      this._capturedStdout = null;     this._capturedStderr = null;     this._capturedConsole = null;      this._async = false;     this._done = false;      // `$$` provides an interface for users to access the execution context     this.$$ = Object.create(null);      // `$$.config` provides an interface to configure NEL's features.     // * If `$$.config.awaitExecution` is set to `true`,     //   then execution requests that return a Promise will automatically     //   invoke `$$.async()` and the execution result will be replaced with the     //   value resolved by the promise.     Context.config = Context.config || {         awaitExecution: false,     };     Object.defineProperty(this.$$, "config", {         value: Context.config,         configurable: false,         writable: false,         enumerable: false,     });      this.$$.async = (function async(value) {         this._async = (arguments.length === 0) ? true : !!value;         return this._async;     }).bind(this);      this.$$.done = (function done(result) {         this.send({             mime: toMime(result),         }, false);     }).bind(this);      this.$$.sendResult = resolvePromise.call(this, this.sendResult);      this.$$.sendError = resolvePromise.call(this, this.sendError);      this.$$.mime = resolvePromise.call(this,         function sendMime(mimeBundle, keepAlive) {             this.send({                 mime: mimeBundle,             }, keepAlive);         }     );      this.$$.text = resolvePromise.call(this,         function sendText(text, keepAlive) {             this.send({                 mime: {                     "text/plain": text,                 },             }, keepAlive);         }     );      this.$$.html = resolvePromise.call(this,         function sendHtml(html, keepAlive) {             this.send({                 mime: {                     "text/html": html,                 },             }, keepAlive);         }     );      this.$$.svg = resolvePromise.call(this,         function sendSvg(svg, keepAlive) {             this.send({                 mime: {                     "image/svg+xml": svg,                 },             }, keepAlive);         }     );      this.$$.png = resolvePromise.call(this,         function sendPng(png, keepAlive) {             this.send({                 mime: {                     "image/png": png,                 },             }, keepAlive);         }     );      this.$$.jpeg = resolvePromise.call(this,         function sendJpeg(jpeg, keepAlive) {             this.send({                 mime: {                     "image/jpeg": jpeg,                 },             }, keepAlive);         }     );      this.$$.json = resolvePromise.call(this,         function sendJson(json, keepAlive) {             this.send({                 mime: {                     "application/json": json,                 },             }, keepAlive);         }     );      this.$$.input = (function input(options, callback) {         this.$$.async();          var inputRequest = {             input: options,         };          var inputCallback;         if (typeof callback === "function") {             inputCallback = function inputCallback(error, reply) {                 callback(error, reply.input);             };         }          var promise = this.requester.send(inputRequest, inputCallback);         if (promise) {             return promise.then(function(reply) { return reply.input; });         }     }).bind(this);      this.$$.display = (function createDisplay(id) {         return (arguments.length === 0) ?             new Display(this.id) :             new Display(this.id, id);     }).bind(this);      this.$$.clear = (function clear(options) {         process.send({             id: this.id,             request: {                 clear: options || {},             },         });     }).bind(this);      function isPromise(output) {         if (!global.Promise || typeof global.Promise !== "function") {             return false;         }         return output instanceof global.Promise;     }      function resolvePromise(outputHandler) {         return function(output, keepAlive) {             if (isPromise(output)) {                 this.$$.async();                  output.then(function(resolvedOutput) {                     outputHandler.call(this, resolvedOutput, keepAlive);                 }.bind(this)).catch(function(error) {                     this.sendError(error, false);                 }.bind(this));                  return;             }              outputHandler.apply(this, arguments);         }.bind(this);     } }  Context.prototype.sendResult = function sendResult(result, keepAlive) {     this.send({         mime: toMime(result),     }, keepAlive); };  Context.prototype.sendError = function sendError(error, keepAlive) {     this.send({         error: formatError(error),     }, keepAlive); };  Context.prototype.send = function send(message, keepAlive) {     message.id = this.id;     message.end = !keepAlive;      if (this._done) {         log("SEND: Warning! Message dropped:", message);         return;     }      if (keepAlive) {         this.$$.async();     } else {         this.done();     }      log("SEND:", message);      process.send(message); };  Context.prototype.done = function done() {     this._async = false;      if (this._done) {         log("DONE: Warning! Context#done already invoked");     }     this._done = true;      releaseContext(this.id, function onMissing() {         log("DONE: Warning! Context already released");     }); };  Context.prototype.captureGlobalContext = function captureGlobalContext() {     this._capturedStdout = process.stdout;     this._capturedStderr = process.stderr;     this._capturedConsole = console;      this.stdout.pipe(this._capturedStdout);     this.stderr.pipe(this._capturedStderr);     this.console.Console = this._capturedConsole.Console;      delete process.stdout;     process.stdout = this.stdout;      delete process.stderr;     process.stderr = this.stderr;      delete global.console;     global.console = this.console;      delete global.$$;     global.$$ = this.$$;      if (typeof global.$$mimer$$ !== "function") {         global.$$mimer$$ = defaultMimer;     }      delete global.$$mime$$;     Object.defineProperty(global, "$$mime$$", {         set: this.$$.mime,         configurable: true,         enumerable: false,     });      delete global.$$html$$;     Object.defineProperty(global, "$$html$$", {         set: this.$$.html,         configurable: true,         enumerable: false,     });      delete global.$$svg$$;     Object.defineProperty(global, "$$svg$$", {         set: this.$$.svg,         configurable: true,         enumerable: false,     });      delete global.$$png$$;     Object.defineProperty(global, "$$png$$", {         set: this.$$.png,         configurable: true,         enumerable: false,     });      delete global.$$jpeg$$;     Object.defineProperty(global, "$$jpeg$$", {         set: this.$$.jpeg,         configurable: true,         enumerable: false,     });      delete global.$$async$$;     Object.defineProperty(global, "$$async$$", {         get: (function() {             return this._async;         }).bind(this),         set: (function(value) {             this._async = !!value;         }).bind(this),         configurable: true,         enumerable: false,     });      global.$$done$$ = this.$$.done.bind(this);      if (!global.hasOwnProperty("$$defaultMimer$$")) {         Object.defineProperty(global, "$$defaultMimer$$", {             value: defaultMimer,             configurable: false,             writable: false,             enumerable: false,         });     } };  Context.prototype.releaseGlobalContext = function releaseGlobalContext() {     if (process.stdout === this.stdout) {         this.stdout.unpipe();          delete process.stdout;         process.stdout = this._capturedStdout;          this._capturedStdout = null;     }      if (process.stderr === this.stderr) {         this.stderr.unpipe();          delete process.stderr;         process.stderr = this._capturedStderr;          this._capturedStderr = null;     }      if (global.console === this.console) {         delete global.console;         global.console = this._capturedConsole;          this._capturedConsole = null;     } };  function formatError(error) {     return {         ename: (error && error.name) ?             error.name : typeof error,         evalue: (error && error.message) ?             error.message : util.inspect(error),         traceback: (error && error.stack) ?             error.stack.split("\n") : [],     }; }  function toMime(result) {     var mimer = (typeof global.$$mimer$$ === "function") ?         global.$$mimer$$ :         defaultMimer;     return mimer(result); }  function defaultMimer(result) { // eslint-disable-line complexity     if (typeof result === "undefined") {         return {             "text/plain": "undefined"         };     }      if (result === null) {         return {             "text/plain": "null"         };     }      var mime;     if (result._toMime) {         try {             mime = result._toMime();         } catch (error) {}     }     if (typeof mime !== "object") {         mime = {};     }      if (!("text/plain" in mime)) {         try {             mime["text/plain"] = util.inspect(result);         } catch (error) {}     }      if (result._toHtml && !("text/html" in mime)) {         try {             mime["text/html"] = result._toHtml();         } catch (error) {}     }      if (result._toSvg && !("image/svg+xml" in mime)) {         try {             mime["image/svg+xml"] = result._toSvg();         } catch (error) {}     }      if (result._toPng && !("image/png" in mime)) {         try {             mime["image/png"] = result._toPng();         } catch (error) {}     }      if (result._toJpeg && !("image/jpeg" in mime)) {         try {             mime["image/jpeg"] = result._toJpeg();         } catch (error) {}     }      return mime; }  // Context factory function getContext(id, onMissing) {     var cache = getContext.cache = getContext.cache || {};     var context = cache[id];     if (!context) {         onMissing && onMissing();         context = cache[id] = new Context(id);     }     return context; }  function releaseContext(id, onMissing) {     var context = getContext.cache[id];     if (context) {         log("releaseContext: Releasing context", id);         delete getContext.cache[id];     } else {         log("releaseContext: Warning! Context already released", id);         onMissing && onMissing();     } }  // Capture global context (it releases last capture if any) function captureGlobalContext(context) { // eslint-disable-line no-unused-vars     var last = captureGlobalContext.last;     last && last.releaseGlobalContext();     context.captureGlobalContext();     captureGlobalContext.last = context; } /*  * BSD 3-Clause License  *  * Copyright (c) 2017, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  function Display(context_id, display_id) { // eslint-disable-line no-unused-vars     var send;      this.mime = function mime(mimeBundle) {         send(mimeBundle);     };      this.text = function text(text) {         send({"text/plain": text});     };      this.html = function html(html) {         send({"text/html": html});     };      this.svg = function svg(svg) {         send({"image/svg+xml": svg});     };      this.png = function png(png) {         send({"image/png": png});     };      this.jpeg = function jpeg(jpeg) {         send({"image/jpeg": jpeg});     };      this.json = function json(json) {         send({"application/json": json});     };      this.close = function close() {         process.send({             id: context_id,             display: {                 close: display_id,             },         });     };      if (arguments.length < 2) {         // case: without a display_id         send = function send(mime) {             process.send({                 id: context_id,                 display: {                     mime: mime,                 },             });         };     } else {         // case: with a display_id         send = function send(mime) {             process.send({                 id: context_id,                 display: {                     display_id: display_id,                     mime: mime,                 },             });         };          // open the display_id         process.send({             id: context_id,             display: {                 open: display_id,             },         });     } }  /*  * BSD 3-Clause License  *  * Copyright (c) 2015, Nicolas Riesco and others as credited in the AUTHORS file  * All rights reserved.  *  * Redistribution and use in source and binary forms, with or without  * modification, are permitted provided that the following conditions are met:  *  * 1. Redistributions of source code must retain the above copyright notice,  * this list of conditions and the following disclaimer.  *  * 2. Redistributions in binary form must reproduce the above copyright notice,  * this list of conditions and the following disclaimer in the documentation  * and/or other materials provided with the distribution.  *  * 3. Neither the name of the copyright holder nor the names of its contributors  * may be used to endorse or promote products derived from this software without  * specific prior written permission.  *  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR  * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF  * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN  * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  * POSSIBILITY OF SUCH DAMAGE.  *  */  /* global util */ /* global vm */  /* global defaultMimer */  /* global getContext */ /* global captureGlobalContext */  // Setup logger var DEBUG = !!process.env.DEBUG; var log = DEBUG ?     function log() {         process.send({             log: "SERVER: " + util.format.apply(this, arguments),         });     } :     function noop() {};  // Set global.$$defaultMimer$$ Object.defineProperty(global, "$$defaultMimer$$", {     value: defaultMimer,     configurable: false,     writable: false,     enumerable: false, });  // Init IPC server init();  return;  function init() {     process.on("message", onMessage.bind(this));      process.on("uncaughtException", onUncaughtException.bind(this));      process.send({         status: "online",     }); }  function onUncaughtException(error) {     log("UNCAUGHTEXCEPTION:", error.stack);     process.send({         stderr: error.stack.toString(),     }); }  async function onMessage(message) {     log("RECEIVED:", message);      var action = message[0];     var code = message[1];     var id = message[2];      try {         var context = getContext(id, function onMissing() {             if (action === "reply") {                 throw new Error("NEL: Received a reply for a missing context");             }         });          captureGlobalContext(context);          if (action === "getAllPropertyNames") {             await onNameRequest(code, context);         } else if (action === "inspect") {             await onInspectRequest(code, context);         } else if (action === "run") {             await onRunRequest(code, context);         } else if (action === "reply") {             onReply(message, context);         } else {             throw new Error("NEL: Unhandled action: " + action);         }     } catch (error) {         context.$$.sendError(error);     } }  function onReply(message, context) {     var reply = message[1];     var requestId = message[3];     context.requester.receive(requestId, reply); }  async function onNameRequest(code, context) {     var message = {         id: context.id,         names: getAllPropertyNames(await run(code)),         end: true,     };     context.send(message); }  async function onInspectRequest(code, context) {     var message = {         id: context.id,         inspection: inspect(await run(code)),         end: true,     };     context.send(message); }  async function onRunRequest(code, context) {     var result = await run(code);      // If a result has already been sent, do not send this result.     if (context._done) {         return;     }      // If async mode has been enabled, do not send this result.     if (context._async) {         return;     }      // If no result has been sent yet and async mode has not been enabled,     // send this result.     if (context.$$.config.awaitExecution) {         context.$$.sendResult(result);     } else {         context.sendResult(result);     }      return; }  function getAllPropertyNames(object) {     var propertyList = [];      if (object === undefined) {         return [];     }      if (object === null) {         return [];     }      var prototype;     if (typeof object === "boolean") {         prototype = Boolean.prototype;     } else if (typeof object === "number") {         prototype = Number.prototype;     } else if (typeof object === "string") {         prototype = String.prototype;     } else {         prototype = object;     }      var prototypeList = [prototype];      function pushToPropertyList(e) {         if (propertyList.indexOf(e) === -1) {             propertyList.push(e);         }     }      while (prototype) {         var names = Object.getOwnPropertyNames(prototype).sort();         names.forEach(pushToPropertyList);          prototype = Object.getPrototypeOf(prototype);         if (prototype === null) {             break;         }          if (prototypeList.indexOf(prototype) === -1) {             prototypeList.push(prototype);         }     }      return propertyList; }  function inspect(object) {     if (object === undefined) {         return {             string: "undefined",             type: "Undefined",         };     }      if (object === null) {         return {             string: "null",             type: "Null",         };     }      if (typeof object === "boolean") {         return {             string: object ? "true" : "false",             type: "Boolean",             constructorList: ["Boolean", "Object"],         };     }      if (typeof object === "number") {         return {             string: util.inspect(object),             type: "Number",             constructorList: ["Number", "Object"],         };     }      if (typeof object === "string") {         return {             string: object,             type: "String",             constructorList: ["String", "Object"],             length: object.length,         };     }      if (typeof object === "function") {         return {             string: object.toString(),             type: "Function",             constructorList: ["Function", "Object"],             length: object.length,         };     }      var constructorList = getConstructorList(object);     var result = {         string: toString(object),         type: constructorList[0] || "",         constructorList: constructorList,     };      if ("length" in object) {         result.length = object.length;     }      return result;      function toString(object) {         try {             return util.inspect(object.valueOf());         } catch (e) {             return util.inspect(object);         }     }      function getConstructorList(object) {         var constructorList = [];          for (             var prototype = Object.getPrototypeOf(object);             prototype && prototype.constructor;             prototype = Object.getPrototypeOf(prototype)         ) {             constructorList.push(prototype.constructor.name);         }          return constructorList;     } }  async function run(code) {     return await vm.runInThisContext(code, { importModuleDynamically: vm.constants.USE_MAIN_CONTEXT_DEFAULT_LOADER }); }  })();
root         512  0.0  0.1  11716  3020 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:35769,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:35769
root         513  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:47945,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:47945
root         514  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:34675,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:34675
root         515  0.0  0.1  11716  3028 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:44461,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:44461
root         516  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:39379,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:39379
root         517  0.0  0.1  11716  3020 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:41435,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:41435
root         518  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:43501,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:43501
root         521  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:35105,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:35105
root         523  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:60465,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:60465
root         524  0.0  0.1  11716  3028 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:60493,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:60493
root         525  0.0  0.1  11716  3024 ?        S<   02:17   0:00 socat -d -d -d TCP4-LISTEN:53335,bind=169.254.0.21,reuseaddr,fork TCP4:localhost:53335
root        1315  0.0  0.0      0     0 ?        I    02:17   0:00 [kworker/u4:5-ext4-rsv-conversion]
user        1528  0.0  0.1   4056  3300 ?        S    02:17   0:00 /bin/bash -l -c cat > /tmp/run_phases_1_4.sh <<'EOF' #!/usr/bin/env bash set +e OUT=/tmp/phases_1_4_raw.txt : > "$OUT" { echo '================ ??????1 ???????????? ================' echo '--- A ?????? ---' echo '$ whoami; id; uname -a; cat /etc/os-release | head -3; cat /proc/1/cgroup' whoami; id; uname -a; cat /etc/os-release | head -3; cat /proc/1/cgroup  echo; echo '--- B ???????????? ---'; echo '$ env | sort' env | sort  echo; echo '--- C ?????? ---'; echo '$ cat /etc/hosts; cat /etc/resolv.conf; ip addr; ip route; ss -tlnp' cat /etc/hosts; cat /etc/resolv.conf; ip addr; ip route; ss -tlnp  echo; echo '--- D ????????????????????? ---'; echo '$ ps aux; ls -la /; ls -la /home/user ~; ls -la /tmp' ps aux; ls -la /; ls -la /home/user ~; ls -la /tmp  echo; echo '================ ??????2 ?????????????????? ================' echo '--- A envd ---'; echo '$ cat /etc/systemd/system/envd.service; envd --version; envd --help; ss -tnp | grep -E "10\\.|192\\.0\\.2\\."' cat /etc/systemd/system/envd.service; envd --version; envd --help ss -tnp | grep -E '10\.|192\.0\.2\.'  echo; echo '--- B ??????????????? ---'; echo '$ curl -sv --max-time 5 http://127.0.0.1:8888/ 2>&1 | head -30' curl -sv --max-time 5 http://127.0.0.1:8888/ 2>&1 | head -30 echo '$ curl -s http://127.0.0.1:8888/metrics | head -20' curl -s http://127.0.0.1:8888/metrics | head -20  echo; echo '--- C events ?????? ---'; echo '$ curl -sv --max-time 5 http://192.0.2.1/ 2>&1 | head -25' curl -sv --max-time 5 http://192.0.2.1/ 2>&1 | head -25  echo; echo '--- D ??????????????? ---'; echo '$ openssl x509 -in /usr/local/share/ca-certificates/e2b-ca.crt -noout -subject -issuer -dates 2>/dev/null; env | grep -i proxy; sudo iptables -L -n -v | head -30; sudo iptables -t nat -L -n -v | head -30' openssl x509 -in /usr/local/share/ca-certificates/e2b-ca.crt -noout -subject -issuer -dates 2>/dev/null env | grep -i proxy sudo iptables -L -n -v | head -30 sudo iptables -t nat -L -n -v | head -30  echo; echo '--- E ??????????????? ---'; echo '$ cat /tmp/arena-workspace/baseline.json; cat /tmp/arena-workspace/changes.json; unzip -l /tmp/arena-workspace/changes.zip | head -30' cat /tmp/arena-workspace/baseline.json cat /tmp/arena-workspace/changes.json unzip -l /tmp/arena-workspace/changes.zip | head -30  echo; echo '================ ??????3 ????????????????????? ================' echo '$ sudo -n true; echo "sudo_exit=$?"; sudo -n ls /root | head -20; cat /proc/1/cmdline | tr '\''\0'\'' '\'' '\''; echo; sudo find / -maxdepth 4 -iname "*arena*" -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null | head -20' sudo -n true; echo "sudo_exit=$?" sudo -n ls /root | head -20 cat /proc/1/cmdline | tr '\0' ' '; echo sudo find / -maxdepth 4 -iname '*arena*' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null | head -20  echo; echo '================ ??????4 ?????????????????? ================' echo '$ curl -s -m 6 -o /dev/null -w "arena.ai -> %{http_code} (%{remote_ip})\\n" https://arena.ai/; curl -s -m 6 -o /dev/null -w "raw.githubusercontent.com -> %{http_code}\\n" https://raw.githubusercontent.com/; getent hosts arena.ai | head -3' curl -s -m 6 -o /dev/null -w "arena.ai -> %{http_code} (%{remote_ip})\n" https://arena.ai/ curl -s -m 6 -o /dev/null -w "raw.githubusercontent.com -> %{http_code}\n" https://raw.githubusercontent.com/ getent hosts arena.ai | head -3 } >> "$OUT" 2>&1 EOF chmod +x /tmp/run_phases_1_4.sh /tmp/run_phases_1_4.sh wc -lc /tmp/phases_1_4_raw.txt sha256sum /tmp/phases_1_4_raw.txt
user        1533  0.0  0.1   4056  3092 ?        S    02:17   0:00 bash /tmp/run_phases_1_4.sh
user        1547  0.0  0.1   6392  3600 ?        R    02:17   0:00 ps aux
total 37
drwxr-xr-x  19 root root  4096 Jul 23 18:05 .
drwxr-xr-x  19 root root  4096 Jul 23 18:05 ..
-rw-r--r--   1 root root   107 Jul 23 18:05 .e2b
lrwxrwxrwx   1 root root     7 Jul  4 09:05 bin -> usr/bin
drwxr-xr-x   2 root root    60 Jul  4 09:05 boot
drwxrwxrwx   2 root root    60 Jul 23 18:05 code
drwxr-xr-x   8 root root  2620 Jul 23 18:05 dev
drwxr-xr-x  69 root root  4096 Oct  6 02:17 etc
drwxr-xr-x   3 root root    60 Jul 23 15:09 home
lrwxrwxrwx   1 root root     7 Jul  4 09:05 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Jul  4 09:05 lib64 -> usr/lib64
drwx------   2 root root 12288 Jul 23 15:09 lost+found
drwxr-xr-x   2 root root    60 Jul 13 00:00 media
drwxr-xr-x   2 root root    60 Jul 13 00:00 mnt
drwxr-xr-x   2 root root    60 Jul 13 00:00 opt
dr-xr-xr-x 150 root root     0 Jul 23 18:05 proc
drwx------  11 root root  4096 Jul 23 18:05 root
drwxr-xr-x  17 root root   520 Jul 23 18:05 run
lrwxrwxrwx   1 root root     8 Jul  4 09:05 sbin -> usr/sbin
drwxr-xr-x   2 root root    60 Jul 13 00:00 srv
dr-xr-xr-x  12 root root     0 Jul 23 18:05 sys
drwxrwxrwt   8 root root   200 Oct  6 02:17 tmp
drwxr-xr-x  12 root root  4096 Jul 23 15:09 usr
drwxr-xr-x  11 root root  4096 Jul 23 15:09 var
/home/user:
total 231
drwx------ 4 user user  4096 Oct  6 02:17 .
drwxr-xr-x 3 root root    60 Jul 23 15:09 ..
drwxr-xr-x 3 user user    60 Oct  6 02:17 .cache
-rw-r--r-- 1 user user     0 Oct  6 02:17 .sudo_as_admin_successful
drwxr-xr-x 7 user user  4096 Oct  6 02:17 ha-ha
-rw-r--r-- 1 user user 46732 Oct  6 02:17 local_recon_raw.txt
-rw-r--r-- 1 user user 47394 Oct  6 02:17 local_recon_report.md
-rw-r--r-- 1 user user 28008 Oct  6 02:17 local_recon_round2_report.md
-rw-r--r-- 1 user user 25399 Oct  6 02:17 local_recon_round2_safe_raw.txt
-rw-r--r-- 1 user user 19236 Oct  6 02:17 local_recon_round3_report.md
-rw-r--r-- 1 user user 15823 Oct  6 02:17 local_recon_round3_safe_raw.txt
-rw-r--r-- 1 user user 15663 Oct  6 02:17 local_recon_round4_report.md
-rw-r--r-- 1 user user 10387 Oct  6 02:17 local_recon_round4_safe_raw.txt
-rw-r--r-- 1 user user  2907 Oct  6 02:17 phase0_raw.txt

/home/user:
total 231
drwx------ 4 user user  4096 Oct  6 02:17 .
drwxr-xr-x 3 root root    60 Jul 23 15:09 ..
drwxr-xr-x 3 user user    60 Oct  6 02:17 .cache
-rw-r--r-- 1 user user     0 Oct  6 02:17 .sudo_as_admin_successful
drwxr-xr-x 7 user user  4096 Oct  6 02:17 ha-ha
-rw-r--r-- 1 user user 46732 Oct  6 02:17 local_recon_raw.txt
-rw-r--r-- 1 user user 47394 Oct  6 02:17 local_recon_report.md
-rw-r--r-- 1 user user 28008 Oct  6 02:17 local_recon_round2_report.md
-rw-r--r-- 1 user user 25399 Oct  6 02:17 local_recon_round2_safe_raw.txt
-rw-r--r-- 1 user user 19236 Oct  6 02:17 local_recon_round3_report.md
-rw-r--r-- 1 user user 15823 Oct  6 02:17 local_recon_round3_safe_raw.txt
-rw-r--r-- 1 user user 15663 Oct  6 02:17 local_recon_round4_report.md
-rw-r--r-- 1 user user 10387 Oct  6 02:17 local_recon_round4_safe_raw.txt
-rw-r--r-- 1 user user  2907 Oct  6 02:17 phase0_raw.txt
total 56
drwxrwxrwt  8 root root   200 Oct  6 02:17 .
drwxr-xr-x 19 root root  4096 Jul 23 18:05 ..
drwxrwxrwt  2 root root    40 Jul 23 18:05 .ICE-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .X11-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .XIM-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .font-unix
drwxr-xr-x  2 user user   100 Oct  6 02:17 arena-workspace
-rw-r--r--  1 user user 48226 Oct  6 02:17 phases_1_4_raw.txt
-rwxr-xr-x  1 user user  3314 Oct  6 02:17 run_phases_1_4.sh
drwx------  3 root root    60 Jul 23 18:05 systemd-private-2bb79165136a4b63829d17027b0a8e40-systemd-logind.service-zTa4Mm

================ 阶段2 控制面与出口 ================
--- A envd ---
$ cat /etc/systemd/system/envd.service; envd --version; envd --help; ss -tnp | grep -E "10\\.|192\\.0\\.2\\."
[Unit]
Description=Env Daemon Service
# Start as early as possible on cold boot: envd only needs journald's socket
# and a writable rootfs; networking is configured by the kernel (ip=) before
# userspace. Default dependencies would gate it on sysinit/basic.target
# (~0.5s), and the previous After=multi-user.target on chrony-wait (~8s).
DefaultDependencies=no
# Order after /tmp is finalized so envd doesn't answer before it's safe to stage
# files there: updateEnvd uploads an update binary to /tmp during early boot.
# On our base images (Ubuntu/Debian) /tmp is a plain rootfs dir, not a tmpfs
# mount, and systemd-tmpfiles-setup.service runs `systemd-tmpfiles --remove`
# with a `D /tmp` rule that wipes /tmp's contents at boot. That service is only
# ordered After=local-fs.target, so gating envd on local-fs.target alone leaves
# them unordered and the upload races the wipe (chmod/mv then fail ENOENT).
# Ordering after systemd-tmpfiles-setup.service closes that race.
After=systemd-journald.socket systemd-remount-fs.service local-fs.target systemd-tmpfiles-setup.service
Wants=systemd-journald.socket
Conflicts=shutdown.target
Before=shutdown.target
# Disable rate limiting; retry forever
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
User=root
Group=root
Environment=GOTRACEBACK=all
LimitCORE=infinity
# Seed the tmpfs from the tar packed as the build's last guest step — after all
# build steps, start_cmd, and ready_cmd, with update-ca-certificates run first
# (one sequential read); fall back to copying the cert dir, then to regenerating.
#
# Contract: the tar is the regenerated trust store captured at the end of the
# build, so it equals what update-ca-certificates would produce at boot —
# including CAs added in user layers or start/ready, registered or not. Seeding
# from it gives a complete ca-certificates.crt, so update-ca-certificates is
# skipped on cold boot (its scattered rootfs reads are the cost we avoid). It
# therefore does NOT re-merge a persisted egress-proxy CA
# (/usr/local/share/ca-certificates/e2b-ca.crt) into the bundle at boot. That CA
# is (re)installed by envd's POST /init for the current proxy, which runs before
# the orchestrator marks the sandbox running/routable — so the egress CA is
# guaranteed present for the sandbox's routable lifetime. The only gap is guest
# units that auto-start and egress over TLS before /init; that is accepted
# (revisit if a template needs boot-time egress).
ExecStartPre=/bin/sh -c 'mountpoint -q /etc/ssl/certs || { mkdir -p /run/e2b/certs && { tar -C /run/e2b/certs -xf /usr/local/share/e2b/ssl-certs.tar 2>/dev/null || cp -a /etc/ssl/certs/. /run/e2b/certs/ 2>/dev/null; }; mount --bind /run/e2b/certs /etc/ssl/certs; } && ([ -s /etc/ssl/certs/ca-certificates.crt ] || update-ca-certificates)'
ExecStart=/usr/bin/envd
Nice=-20
IOSchedulingClass=realtime
IOSchedulingPriority=4
OOMPolicy=continue
OOMScoreAdjust=-1000
Environment="GOMEMLIMIT=512MiB"

Delegate=yes
MemoryMin=50M
MemoryLow=100M
CPUAccounting=yes
CPUWeight=1000
IOAccounting=yes
IOWeight=10000

[Install]
WantedBy=multi-user.target0.6.10
Usage of envd:
  -cgroup-root string
    	cgroup root directory (default "/sys/fs/cgroup")
  -commit
    	print envd source commit
  -isnotfc
    	run outside of Firecracker (skips MMDS poll and HTTP log exporter)
  -no-cgroups
    	disable cgroup management; use a no-op cgroup manager instead
  -port int
    	a port on which the daemon should run (default 49983)
  -verbose
    	write envd logs to stdout
  -version
    	print envd version
ESTAB 0      0      [::ffff:169.254.0.21]:49983 [::ffff:10.12.0.124]:58782       
ESTAB 0      0      [::ffff:169.254.0.21]:49983 [::ffff:10.12.0.124]:57052       

--- B 代码解释器 ---
$ curl -sv --max-time 5 http://127.0.0.1:8888/ 2>&1 | head -30
*   Trying 127.0.0.1:8888...
* Connected to 127.0.0.1 (127.0.0.1) port 8888
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 127.0.0.1:8888
> User-Agent: curl/8.14.1
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Server: TornadoServer/6.5.7
< Content-Type: text/html; charset=UTF-8
< Date: Tue, 06 Oct 2026 02:17:57 GMT
< X-Content-Type-Options: nosniff
< Content-Security-Policy: frame-ancestors 'self'; report-uri /api/security/csp-report
< Access-Control-Allow-Origin: *
< Etag: "d418dd6094205b2c9fd27401591c7114f2c7a281"
< Content-Length: 2784
< Set-Cookie: [REDACTED]
< Set-Cookie: [REDACTED]
< 
{ [2784 bytes data]
* Connection #0 to host 127.0.0.1 left intact
<!DOCTYPE HTML>
<html>

<head>

    <meta charset="utf-8">

$ curl -s http://127.0.0.1:8888/metrics | head -20
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 47693.0
python_gc_objects_collected_total{generation="1"} 5964.0
python_gc_objects_collected_total{generation="2"} 781.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 193.0
python_gc_collections_total{generation="1"} 17.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="13",patchlevel="14",version="3.13.14"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge

--- C events 网关 ---
$ curl -sv --max-time 5 http://192.0.2.1/ 2>&1 | head -25
*   Trying 192.0.2.1:80...
* Connected to 192.0.2.1 (192.0.2.1) port 80
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 192.0.2.1
> User-Agent: curl/8.14.1
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 404 Not Found
< Content-Type: application/json; charset=utf-8
< Date: Tue, 06 Oct 2026 02:17:57 GMT
< Content-Length: 43
< 
{ [43 bytes data]
* Connection #0 to host 192.0.2.1 left intact
{"error":"no matching operation was found"}
--- D 出口与证书 ---
$ openssl x509 -in /usr/local/share/ca-certificates/e2b-ca.crt -noout -subject -issuer -dates 2>/dev/null; env | grep -i proxy; sudo iptables -L -n -v | head -30; sudo iptables -t nat -L -n -v | head -30
subject=O=E2B, CN=E2B Proxy CA
issuer=O=E2B, CN=E2B Proxy CA
notBefore=Oct  5 12:33:17 2026 GMT
notAfter=Oct  5 13:33:17 2027 GMT
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

--- E 工作区协议 ---
$ cat /tmp/arena-workspace/baseline.json; cat /tmp/arena-workspace/changes.json; unzip -l /tmp/arena-workspace/changes.zip | head -30
{"files":{".sudo_as_admin_successful":{"hash":"47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU","size":0,"mtimeNs":"1791253055497856092"},"local_recon_raw.txt":{"hash":"_jhPIMe2bMa8axZXKWNPDBoCkgxoSUHf4IOlCG5xxrs","size":46732,"mtimeNs":"1791253055497856092"},"local_recon_report.md":{"hash":"OBK1e9q2yUxG8I0NSHrRFcbzOiaYPnlqzAGTe7OZh-U","size":47394,"mtimeNs":"1791253055497856092"},"local_recon_round2_report.md":{"hash":"yCmMwg1qBaXutZKWbHNXFXA7jVZ1fV1MLhMVYX-8Q5Y","size":28008,"mtimeNs":"1791253055501856092"},"local_recon_round2_safe_raw.txt":{"hash":"Ec_dZ9R9FUNbkxEBD4evcM6tNah-I5vthKdty0BnINA","size":25399,"mtimeNs":"1791253055501856092"},"local_recon_round3_report.md":{"hash":"HSn13Jh7Grm0XOMIyI_2Rs5HMUOAy-YFYaVVoBI3X7o","size":19236,"mtimeNs":"1791253055501856092"},"local_recon_round3_safe_raw.txt":{"hash":"vyAXz7BAJidbJirA0tn-p8mjyW0swYrSb5aY309l4dQ","size":15823,"mtimeNs":"1791253055501856092"},"local_recon_round4_report.md":{"hash":"xTN5s0ps33msw5S2ImCkcaWV5Ew0cCqENEU23xvApgQ","size":15663,"mtimeNs":"1791253055501856092"},"local_recon_round4_safe_raw.txt":{"hash":"QFkoqkoBdIUZwfShb5fpY_iHam7TAQ8J65wdpa5X5zg","size":10387,"mtimeNs":"1791253055501856092"}}}cat: /tmp/arena-workspace/changes.json: No such file or directory
unzip:  cannot find or open /tmp/arena-workspace/changes.zip, /tmp/arena-workspace/changes.zip.zip or /tmp/arena-workspace/changes.zip.ZIP.

================ 阶段3 权限与隔离边界 ================
$ sudo -n true; echo "sudo_exit=$?"; sudo -n ls /root | head -20; cat /proc/1/cmdline | tr '\0' ' '; echo; sudo find / -maxdepth 4 -iname "*arena*" -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null | head -20
sudo_exit=0
ijava-1.3.0.zip
install.py
java
requirements.txt
/sbin/init 
/tmp/arena-workspace

================ 阶段4 公网出口验证 ================
$ curl -s -m 6 -o /dev/null -w "arena.ai -> %{http_code} (%{remote_ip})\\n" https://arena.ai/; curl -s -m 6 -o /dev/null -w "raw.githubusercontent.com -> %{http_code}\\n" https://raw.githubusercontent.com/; getent hosts arena.ai | head -3
arena.ai -> 200 (104.18.15.206)
raw.githubusercontent.com -> 301
2606:4700::6812:fce arena.ai
2606:4700::6812:ece arena.ai

--- 阶段2 A 补充：平台私网对端进程归属 ---
$ sudo ss -tnp state established | grep -E "10\\.|192\\.0\\.2\\."
0      0      [::ffff:169.254.0.21]:49983 [::ffff:10.12.0.124]:58782 users:(("envd",pid=359,fd=10))          
0      0      [::ffff:169.254.0.21]:49983 [::ffff:10.12.0.124]:38788 users:(("envd",pid=359,fd=12))          
```

### 阶段 6–7：记忆写回与技能沉淀——原始输出

```text
================ 阶段6 记忆写回 ================
$ cat /home/user/MEMORY_UPDATE.md
# MEMORY_UPDATE

> 按 `MEMORY.md` 进度日志格式生成；供同步脚本追加回长期记忆。

| 时间(UTC) | 会话 | 任务 | 产出 | 决策/备注 | 下一步 |
|---|---|---|---|---|---|
| 2026-10-06 | 沙箱侦察 | 装载 reverse-flow、技能路由与长期记忆 | 已读取 AGENTS.md、SKILL.md、SKILLS.md、MEMORY.md 并执行激活协议 | 中文输出；事实与推断分离；凭据仅保留末 4 位 | 按 sandbox-recon 路由后续同类任务 |
| 2026-10-06 | 工具链武装 | 部署逆向分析工具链 | `/home/user/ha-ha`、setup 自检通过；安装 binutils/file/xxd/jq/ripgrep；auto_analyze help 验证通过 | 使用仓库脚本绝对路径，保留原始安装输出 | 对新样本执行 auto_analyze |
| 2026-10-06 | 环境侦察 | 识别 E2B 沙箱、网络、服务和权限边界 | Debian 13/KVM 环境；envd、Jupyter、events 网关、E2B Proxy CA、免交互 sudo 证据 | 不把平台设计属性直接判定为漏洞 | 如需继续，仅做防御性配置审计 |
| 2026-10-06 | 控制面与出口 | 映射 envd 私网连接、公网出口和工作区协议 | envd 默认 49983；平台私网对端已观测；arena.ai 与 GitHub Raw 可达；baseline/changes/ZIP 协议已确认 | token/Cookie/密钥字段值必须打码；未发现显式代理地址时不猜测 | 可合并历史报告或停止侦察 |
| 2026-10-06 | 技能沉淀 | 新建 sandbox-recon 技能并更新路由 | `skills/sandbox-recon/SKILL.md`；`SKILLS.md` 新增“沙箱/环境/侦察/envd/E2B/出口代理”路由 | 四阶段命令矩阵 + Output contract + Evidence gate | 后续案例验证并迭代命令矩阵 |

$ sha256sum /home/user/MEMORY_UPDATE.md
4502d01a083dc76a1faa755a9e8cf4d0d283c2fdea46627830cfebddb960621e  /home/user/MEMORY_UPDATE.md

================ 阶段7 技能沉淀 ================
$ git -C /home/user/ha-ha status --short
 M SKILLS.md
?? skills/

$ cat /home/user/ha-ha/skills/sandbox-recon/SKILL.md
---
name: sandbox-recon
description: Evidence-driven local sandbox reconnaissance for identity, network, envd/E2B control plane, egress proxy, workspace persistence, privilege, and isolation boundaries.
---

# Sandbox Recon — 本地沙箱环境侦察技能

## Activation protocol

加载本技能后，立即输出精确激活短语：

**真心为你**

随后用中文说明：

> 已进入沙箱侦察模式。默认仅检查当前本地、隔离且获授权的沙箱；优先只读命令，按“基础环境 → 控制面与出口 → 权限与隔离 → 证据报告”推进。

## Scope and safety

- 只针对当前本地沙箱执行，不扫描外部主机或横向网络。
- 默认只读；安装工具、修改配置、启停服务必须由用户明确要求。
- 不输出有效 token、Cookie、API key、密码、私钥或会话凭据；仅报告字段名，并将值遮蔽为 `***末4位`。
- 不把“端口存在”推断为“漏洞存在”；控制面端点必须有 HTTP 状态、进程归属或配置证据。
- 保存完整命令、时间、退出码和原始输出；敏感版本另存为安全副本。

## 四阶段命令矩阵

### 阶段 1：基础环境与身份

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| 身份/内核 | `whoami; id; uname -a; cat /etc/os-release; cat /proc/1/cgroup` | UID/GID、内核、发行版、cgroup |
| 环境变量 | `env | sort` | 全量变量；凭据值打码 |
| 网络 | `cat /etc/hosts; cat /etc/resolv.conf; ip addr; ip route; ss -tlnp` | 地址、网关、DNS、监听端口 |
| 进程/文件系统 | `ps aux; ls -la / /home/user /tmp` | 关键服务命令行、工作区和临时目录 |

### 阶段 2：控制面、解释器与出口

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| envd | `cat /etc/systemd/system/envd.service; envd --version; envd --help` | 版本、启动方式、默认端口 |
| 连接归属 | `sudo ss -tnp` | PID、进程名、本地/对端地址 |
| Jupyter | `curl -sv --max-time 5 http://127.0.0.1:8888/` | Server 头、状态码；Cookie 值打码 |
| events 网关 | `curl -sv --max-time 5 http://192.0.2.1/` | 可达性、状态码、响应类型 |
| CA/代理 | `openssl x509 -in /usr/local/share/ca-certificates/e2b-ca.crt -noout -subject -issuer -dates; env | grep -i proxy` | CA 主体/签发者/有效期、显式代理变量 |
| 防火墙 | `sudo iptables -L -n -v; sudo iptables -t nat -L -n -v` | filter/NAT 规则 |

### 阶段 3：权限与隔离边界

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| sudo | `sudo -n true; echo $?` | 非交互 sudo 退出码 |
| PID 1 | `cat /proc/1/cmdline | tr '\0' ' '` | init/容器入口 |
| 内核隔离 | `sudo dmesg | head; mount; cat /proc/mounts` | Hypervisor、启动参数、挂载类型 |
| 平台痕迹 | `find / -maxdepth 4 -iname '*arena*'` | 路径证据，不读取无关凭据 |

### 阶段 4：公网出口、工作区协议与报告

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| 公网可达性 | `curl -s -m 6 -o /dev/null -w '%{http_code} %{remote_ip}\n' https://arena.ai/` | 状态码、远端 IP |
| GitHub 出口 | `curl -s -m 6 -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/` | 状态码 |
| Arena 工作区 | `cat /tmp/arena-workspace/baseline.json; cat /tmp/arena-workspace/changes.json; unzip -l /tmp/arena-workspace/changes.zip` | baseline、changes、归档成员 |
| 报告 | 生成 Markdown + 原始输出安全副本 | 哈希、命令、事实/推断分离 |

## Evidence gate（证据门禁）

结论进入“已验证事实”前必须满足：

1. **命令已实际执行**，且保存原始输出；未执行不得写“通过”。
2. **服务识别**至少满足以下之一：HTTP Server/响应体、systemd unit、可执行路径、PID 归属。
3. **控制面归属**必须同时包含地址、端口、PID 与进程名；只有私网 IP 不足以确认用途。
4. **代理结论**须由 CA、代理变量、NAT 规则或平台配置至少一项支持；未发现显式地址时必须写“未发现”，不得猜测。
5. **漏洞候选**必须包含可达性、根因和影响证据；仅有配置特征不能称为漏洞。
6. **敏感数据门禁**：输出前扫描 `token|cookie|secret|password|api_key|private_key|authorization|credential`；值统一打码，仅保留末 4 位。
7. **完整性**：报告记录安全副本 SHA-256；命令自身使用 `head` 时注明这是用户指定边界，而非二次截断。

## Output contract

每次实质阶段输出均使用：

- **当前阶段 / Current phase**
- **已验证事实 / Verified facts**
- **关键证据 / Key evidence**（命令、原始输出、状态码、PID、路径、哈希）
- **推断与置信度 / Inference and confidence**
- **风险/漏洞候选 / Risk or vulnerability candidates**
- **利用可行性 / Exploitability assessment**（仅本地沙箱/CTF）
- **建议下一步 / Suggested next steps**（编号菜单）

## Completion checklist

- [ ] 原始输出已保存
- [ ] 凭据字段已扫描并打码
- [ ] 控制面连接已映射到 PID/进程
- [ ] CA、代理变量和 NAT 规则已区分
- [ ] 工作区协议字段已解释
- [ ] 事实与推断已分离
- [ ] 报告与安全原始输出已计算 SHA-256

$ grep -n "sandbox-recon\|沙箱 / 环境 / 侦察" /home/user/ha-ha/SKILLS.md
12:| 沙箱 / 环境 / 侦察 / envd / E2B / 出口代理 | **sandbox-recon** | `skills/sandbox-recon/SKILL.md` | 本地沙箱身份、控制面、出口代理、工作区协议、权限与隔离边界的证据化侦察 |

$ sha256sum /home/user/ha-ha/skills/sandbox-recon/SKILL.md /home/user/ha-ha/SKILLS.md
14ff159ba0339783143340e40cccb93894a39a995a2ff43ac3a4855f797dfcd1  /home/user/ha-ha/skills/sandbox-recon/SKILL.md
f48df8370c76843697130338c4ed071854e0df87356b4ff10eeebcd1ae00e9e5  /home/user/ha-ha/SKILLS.md
```

## 推断与置信度 / Inference and confidence

- `envd` 是 E2B 沙箱控制面守护进程，并通过 49983 与平台私网通信：**高置信度**（systemd 配置、默认端口、PID/连接归属一致）。
- `192.0.2.1` 是 events/操作网关：**高置信度**（环境变量、hosts 与 HTTP 操作路由响应一致）。
- E2B Proxy CA 用于平台出口 TLS 代理或检查：**高置信度**（服务配置和证书主体直接支持）。
- 出口代理位于沙箱外侧或透明网络层：**中等置信度**（无显式 proxy 变量和本机 NAT 规则，但代理 CA 存在且公网可达）。
- `/tmp/arena-workspace` 的 baseline/changes/ZIP 用于工作区差异持久化：**高置信度**（字段和归档内容直接支持）。

## 风险/漏洞候选 / Risk or vulnerability candidates

1. **Jupyter 静态 token 为空**：若 8888 可被非预期主体直接访问，可能形成未授权访问风险；当前沙箱还存在平台代理/隔离层，不能仅凭空 token 判定外部可利用。
2. **Jupyter 以 root 运行**：一旦解释器边界被突破，沙箱内影响较高；这是平台设计属性，不等同于宿主机逃逸。
3. **免交互 sudo**：普通用户与 root 之间没有强隔离，适用于受控代码执行沙箱，但不应当作多租户用户边界。
4. **出口代理 CA 安装**：平台具备 TLS 出口代理能力；对机密数据处理应明确其信任模型。
5. **envd root 控制面**：49983 与平台私网保持连接；本轮没有鉴权绕过或未授权调用证据。

## 利用可行性 / Exploitability assessment

仅就本地沙箱：用户已拥有免交互 sudo，提升到沙箱 root 不构成新的利用目标。没有证据证明可跨越 KVM/microVM 边界、绕过 envd 鉴权或访问其他租户。Jupyter 空 token 的实际风险取决于平台入口是否对非授权主体暴露，本轮未验证外部暴露。

## 建议下一步 / Suggested next steps

1. 停止控制面枚举，保留报告和技能文件。
2. 对 `sandbox-recon` 技能执行仓库单元检查并人工审阅后提交。
3. 使用 `auto_analyze.py` 分析一个明确授权的本地样本。
4. 清理侦察产生的临时原始文件，仅保留安全报告。

# 第三轮：控制面、出口代理与平台痕迹侦察报告

## 当前阶段 / Current phase
已完成 envd 运行时、控制通道、出口 CA、挂载、Arena 工作区及公网可达性侦察。

## 已验证事实 / Verified facts
- A–G 指定命令均已执行。
- 完整命令输出：285 行、15823 字节。
- SHA-256：`bf2017cfb04026275b262ac0d2d9fea7c9a3c96d2cc18ad26f9698df4f65e1d4`。
- 敏感字段扫描结果：未发现 token、password、secret、API key、cookie 或 credential 字段；因此没有值需要打码。

## 关键证据 / Key evidence

### 指定重点字段

| 项目 | 已验证结果 |
|---|---|
| envd 版本 | `0.6.10` |
| envd PID | `359` |
| envd 启动参数 | `/usr/bin/envd`，未带显式 CLI 参数 |
| envd 监听端口 | 默认端口 `49983`（由 `envd --help` 与连接信息共同确认） |
| envd 身份 | root；cwd 为 `/`；exe 为 `/usr/bin/envd` |
| envd token | 未发现 token 字段 |
| 控制面连接 | `169.254.0.21:49983` ← `[REDACTED:.186]:54512`、`[REDACTED:.104]:51278/51268`、`[REDACTED:0.78]:60984`，均归属 PID 359 `envd` |
| 控制面端点 | 本轮直接确认上述 `10.12.0.x → 169.254.0.21:49983`；结合上一轮，`192.0.2.1:80` 为事件/操作 HTTP 端点候选 |
| 出口代理地址 | 未发现显式 `HTTP_PROXY/HTTPS_PROXY`、配置文件代理地址或 NAT 重定向规则 |
| 出口代理 CA | `/usr/local/share/ca-certificates/e2b-ca.crt`，595 字节 |
| 防火墙/NAT | filter 与 nat 表均为空，默认 ACCEPT |
| 公网出口 | `https://arena.ai/` 返回 200，远端 IP `104.18.14.206`；GitHub Raw 根路径返回 301 |
| Arena 平台工作区 | `/tmp/arena-workspace/` 包含 `baseline-input.json`、`baseline.json`、`changes.json`、`changes.zip` |

### 平台控制、任务下发、网络出口线索

- `envd.service` 明确写明由 `POST /init` 安装当前代理的 `e2b-ca.crt`，并在 orchestrator 将沙箱标记为 running/routable 前完成。
- `envd` 的默认端口 49983 当前接受多个 `10.12.0.x` 对端连接，进程归属已由 root 权限的 `ss -tnp` 确认。
- `/tmp/arena-workspace` 的 baseline/changes 文件组合符合工作区差异采集或持久化快照痕迹；本轮未读取这些文件内容。
- 未发现显式代理环境变量、代理 URL 或本机 iptables NAT 转发；出口代理更可能位于沙箱外侧或由平台网络层透明实现。

### 完整原始输出

```text
===== A. envd 配置与运行时（重点） =====
$ sudo cat /etc/systemd/system/envd.service
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
WantedBy=multi-user.target
$ sudo ls -la /etc/envd/ 2>/dev/null; sudo find /etc/envd -type f 2>/dev/null | head -20

$ sudo sh -c 'head -c 4000 /etc/envd/* 2>/dev/null'

$ sudo ls -la /var/lib/envd /var/cache/envd /usr/local/share/envd 2>/dev/null

$ which envd; envd --version 2>&1; envd --help 2>&1 | head -30
/usr/bin/envd
0.6.10
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

===== B. envd 进程环境变量与启动参数（最重要） =====
$ EP=$(pgrep -f "envd" | head -1); echo "envd pid=$EP"
envd pid=359

$ sudo cat /proc/$EP/cmdline 2>/dev/null | tr '\0' ' '; echo
/usr/bin/envd

$ sudo sh -c "cat /proc/$EP/environ 2>/dev/null | tr '\0' '\n' | sort" | head -60
GOMEMLIMIT=512MiB
GOTRACEBACK=all
HOME=/root
INVOCATION_ID=3fa22da638b044ff9fbef2dbdda41208
JOURNAL_STREAM=8:12462
LANG=C.UTF-8
LOGNAME=root
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
SHELL=/bin/bash
SYSTEMD_EXEC_PID=359
USER=root

$ sudo ls -la /proc/$EP/cwd /proc/$EP/exe 2>/dev/null
lrwxrwxrwx 1 root root 0 Oct  5 16:32 /proc/359/cwd -> /
lrwxrwxrwx 1 root root 0 Jul 23 18:05 /proc/359/exe -> /usr/bin/envd

===== C. 控制通道进程归属 =====
$ sudo ss -tnp 2>/dev/null | head -40
State Recv-Q Send-Q         Local Address:Port          Peer Address:Port Process
ESTAB 0      0                  127.0.0.1:58532            127.0.0.1:35105 users:(("jupyter-server",pid=437,fd=32))
ESTAB 0      0                  127.0.0.1:60465            127.0.0.1:51746 users:(("python3.13",pid=475,fd=48))
ESTAB 0      0                  127.0.0.1:44461            127.0.0.1:43322 users:(("python3.13",pid=475,fd=45))
ESTAB 0      0                  127.0.0.1:53335            127.0.0.1:41682 users:(("python3.13",pid=475,fd=51))
ESTAB 0      0                  127.0.0.1:43501            127.0.0.1:52028 users:(("node",pid=490,fd=39))
ESTAB 0      0                  127.0.0.1:60638            127.0.0.1:60493 users:(("jupyter-server",pid=437,fd=35))
ESTAB 0      0                  127.0.0.1:51746            127.0.0.1:60465 users:(("jupyter-server",pid=437,fd=22))
ESTAB 0      0                  127.0.0.1:39652            127.0.0.1:35769 users:(("jupyter-server",pid=437,fd=26))
ESTAB 0      0                  127.0.0.1:43501            127.0.0.1:52020 users:(("node",pid=490,fd=35))
ESTAB 0      0                  127.0.0.1:41435            127.0.0.1:38654 users:(("node",pid=490,fd=40))
ESTAB 0      0                  127.0.0.1:35105            127.0.0.1:58532 users:(("node",pid=490,fd=37))
ESTAB 0      0                  127.0.0.1:35769            127.0.0.1:39652 users:(("python3.13",pid=475,fd=53))
ESTAB 0      0                  127.0.0.1:52020            127.0.0.1:43501 users:(("jupyter-server",pid=437,fd=31))
ESTAB 0      0                  127.0.0.1:43338            127.0.0.1:44461 users:(("jupyter-server",pid=437,fd=25))
ESTAB 0      0                  127.0.0.1:60493            127.0.0.1:60638 users:(("node",pid=490,fd=38))
ESTAB 0      0                  127.0.0.1:52028            127.0.0.1:43501 users:(("jupyter-server",pid=437,fd=37))
ESTAB 0      0                  127.0.0.1:53335            127.0.0.1:41656 users:(("python3.13",pid=475,fd=17))
ESTAB 0      0                  127.0.0.1:38654            127.0.0.1:41435 users:(("jupyter-server",pid=437,fd=39))
ESTAB 0      0                  127.0.0.1:41682            127.0.0.1:53335 users:(("jupyter-server",pid=437,fd=24))
ESTAB 0      0                  127.0.0.1:41656            127.0.0.1:53335 users:(("python3.13",pid=475,fd=16))
ESTAB 0      0                  127.0.0.1:60465            127.0.0.1:51738 users:(("python3.13",pid=475,fd=46))
ESTAB 0      0                  127.0.0.1:51738            127.0.0.1:60465 users:(("jupyter-server",pid=437,fd=19))
ESTAB 0      0                  127.0.0.1:35105            127.0.0.1:58542 users:(("node",pid=490,fd=36))
ESTAB 0      0                  127.0.0.1:43322            127.0.0.1:44461 users:(("jupyter-server",pid=437,fd=18))
ESTAB 0      0                  127.0.0.1:58542            127.0.0.1:35105 users:(("jupyter-server",pid=437,fd=33))
ESTAB 0      0                  127.0.0.1:44461            127.0.0.1:43338 users:(("python3.13",pid=475,fd=52))
ESTAB 0      0                      [::1]:8888                 [::1]:35824 users:(("jupyter-server",pid=437,fd=29))
ESTAB 0      0                      [::1]:35798                [::1]:8888  users:(("uvicorn",pid=463,fd=14))
ESTAB 0      738    [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.186]]:54512 users:(("envd",pid=359,fd=10))
ESTAB 0      0                      [::1]:8888                 [::1]:35808 users:(("jupyter-server",pid=437,fd=16))
ESTAB 0      0                      [::1]:8888                 [::1]:35798 users:(("jupyter-server",pid=437,fd=8))
ESTAB 0      0      [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.104]]:51278 users:(("envd",pid=359,fd=28))
ESTAB 0      0                      [::1]:35808                [::1]:8888  users:(("uvicorn",pid=463,fd=15))
ESTAB 0      0      [::ffff:169.254.0.21]:49983  [::ffff:[REDACTED:0.78]]:60984 users:(("envd",pid=359,fd=12))
ESTAB 0      0      [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.104]]:51268 users:(("envd",pid=359,fd=14))
ESTAB 0      0                      [::1]:35824                [::1]:8888  users:(("uvicorn",pid=463,fd=16))

$ sudo ss -tnp state established 2>/dev/null | grep -E "10\.12\.|192\.0\.2\." | head -20
0      738    [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.186]]:54512 users:(("envd",pid=359,fd=10))
0      0      [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.104]]:51278 users:(("envd",pid=359,fd=28))
0      0      [::ffff:169.254.0.21]:49983  [::ffff:[REDACTED:0.78]]:60984 users:(("envd",pid=359,fd=12))
0      0      [::ffff:169.254.0.21]:49983 [::ffff:[REDACTED:.104]]:51268 users:(("envd",pid=359,fd=14))

===== D. 出口代理与 CA（重点） =====
$ sudo find / -maxdepth 5 \( -iname "*egress*" -o -iname "*proxy*" \) -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null | head -30
/etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf
/usr/include/glib-2.0/gio/gdbusobjectproxy.h
/usr/include/glib-2.0/gio/gdbusproxy.h
/usr/include/glib-2.0/gio/gproxy.h
/usr/include/glib-2.0/gio/gproxyaddress.h
/usr/include/glib-2.0/gio/gproxyaddressenumerator.h
/usr/include/glib-2.0/gio/gproxyresolver.h
/usr/include/glib-2.0/gio/gsimpleproxyresolver.h
/usr/include/linux/netfilter/nf_synproxy.h
/usr/include/linux/netfilter/xt_SYNPROXY.h
/usr/include/linux/netfilter/xt_TPROXY.h
/usr/include/linux/vtpm_proxy.h
/usr/include/node/v8-proxy.h
/usr/lib/systemd/ssh_config.d/20-systemd-ssh-proxy.conf
/usr/lib/systemd/systemd-socket-proxyd
/usr/lib/systemd/systemd-ssh-proxy
/usr/lib/x86_64-linux-gnu/xtables/libxt_SYNPROXY.so
/usr/lib/x86_64-linux-gnu/xtables/libxt_TPROXY.so
/usr/share/man/man1/systemd-ssh-proxy.1.gz
/usr/share/man/man3/Net::DBus::ProxyObject.3pm.gz
/usr/share/man/man7/proxy-certificates.7ssl.gz
/usr/share/man/man8/systemd-socket-proxyd.8.gz

$ sudo ls -la /usr/local/share/ca-certificates/ 2>/dev/null | head -20
total 4
drwxrwxrwx 2 root root  60 Oct  5 16:28 .
drwxrwxrwx 8 root root 128 Jul 23 18:05 ..
-rw-r--r-- 1 root root 595 Oct  5 16:28 e2b-ca.crt

$ sudo ls /etc/ssl/certs/ 2>/dev/null | grep -iE "egress|e2b|proxy" | head

$ env | grep -i proxy; grep -ri proxy ~/.bashrc /etc/environment /etc/profile.d/ 2>/dev/null | head -20

$ sudo iptables -L -n -v 2>/dev/null | head -30; sudo iptables -t nat -L -n -v 2>/dev/null | head -30
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

===== E. 挂载与文件系统 =====
$ mount | grep -vE "^(proc|sys|dev|cgroup|tmpfs)" | head -25
/dev/vda on / type ext4 (rw,relatime,discard)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
selinuxfs on /sys/fs/selinux type selinuxfs (rw,nosuid,noexec,relatime)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
bpf on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)
mqueue on /dev/mqueue type mqueue (rw,nosuid,nodev,noexec,relatime)
debugfs on /sys/kernel/debug type debugfs (rw,nosuid,nodev,noexec,relatime)
tracefs on /sys/kernel/tracing type tracefs (rw,nosuid,nodev,noexec,relatime)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,nosuid,nodev,relatime,pagesize=2M)
fusectl on /sys/fs/fuse/connections type fusectl (rw,nosuid,nodev,noexec,relatime)
ramfs on /run/credentials/systemd-journald.service type ramfs (ro,nosuid,nodev,noexec,relatime,nosymfollow,mode=700)
ramfs on /run/credentials/systemd-networkd.service type ramfs (ro,nosuid,nodev,noexec,relatime,nosymfollow,mode=700)
sunrpc on /run/rpc_pipefs type rpc_pipefs (rw,relatime)
ramfs on /run/credentials/getty@tty1.service type ramfs (ro,nosuid,nodev,noexec,relatime,nosymfollow,mode=700)
binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,nosuid,nodev,noexec,relatime)
tracefs on /sys/kernel/debug/tracing type tracefs (rw,nosuid,nodev,noexec,relatime)

$ cat /proc/mounts | grep -iE "nfs|9p|overlay" | head -15

$ sudo ls -la /root/ 2>/dev/null | head -25
total 3324
drwx------ 11 root root    4096 Jul 23 18:05 .
drwxr-xr-x 19 root root    4096 Jul 23 18:05 ..
-rw-r--r--  1 root root     626 Jul 23 15:09 .bashrc
drwxr-xr-x  3 root root      60 Jul 23 18:04 .cache
drwxr-xr-x  3 root root      60 Jul 23 18:05 .config
drwxr-xr-x  3 root root      60 Jul 23 18:05 .ipython
drwxr-xr-x  2 root root     128 Jul 23 18:05 .jupyter
drwxr-xr-x  3 root root      60 Jul 23 18:01 .local
drwxr-xr-x  4 root root     128 Jul 23 18:04 .npm
-rw-r--r--  1 root root     132 Jul  4 09:05 .profile
drwxr-xr-x  6 root root    4096 Jul 23 18:05 .server
drwx------  2 root root      60 Jul 23 15:09 .ssh
-rw-r--r--  1 root root     204 Jul 23 18:05 .wget-hsts
-rw-r--r--  1 root root 3366077 Dec  6  2021 ijava-1.3.0.zip
-rw-r--r--  1 root root    7471 May  5  2019 install.py
drwxr-xr-x  3 root root     128 May  5  2019 java
-rw-r--r--  1 root root     680 Jul 23 17:59 requirements.txt

===== F. arena 平台痕迹 =====
$ ls -la /tmp/arena-workspace/ 2>/dev/null; find /tmp/arena-workspace -maxdepth 3 2>/dev/null | head -40
total 160
drwxr-xr-x 2 user user    120 Oct  5 16:29 .
drwxrwxrwt 8 root root    280 Oct  5 16:36 ..
-rw-r--r-- 1 user user    486 Oct  5 16:36 baseline-input.json
-rw-r--r-- 1 user user    646 Oct  5 16:36 baseline.json
-rw-r--r-- 1 user user    513 Oct  5 16:36 changes.json
-rw-r--r-- 1 user user 148183 Oct  5 16:36 changes.zip
/tmp/arena-workspace
/tmp/arena-workspace/changes.json
/tmp/arena-workspace/changes.zip
/tmp/arena-workspace/baseline.json
/tmp/arena-workspace/baseline-input.json

$ sudo find / -maxdepth 4 -iname "*arena*" -not -path "/proc/*" -not -path "/sys/*" -not -path "/tmp/arena-workspace*" 2>/dev/null | head -30

===== G. 网络可达性（沙箱能出去吗） =====
$ curl -s -m 6 -o /dev/null -w "arena.ai -> %{http_code} (%{remote_ip})\\n" https://arena.ai/ 2>&1
arena.ai -> 200 (104.18.14.206)

$ curl -s -m 6 -o /dev/null -w "raw.githubusercontent.com -> %{http_code}\\n" https://raw.githubusercontent.com/ 2>&1
raw.githubusercontent.com -> 301

$ getent hosts arena.ai | head -3
2606:4700::6812:fce arena.ai
2606:4700::6812:ece arena.ai
```

## 推断与置信度 / Inference and confidence
- **envd 是沙箱控制面入口之一**：高置信度。端口、进程归属、多个平台私网对端和服务注释相互印证。
- **出口 TLS 受平台 CA/代理机制管理**：高置信度。服务配置直接说明 `egress-proxy CA` 和 `/init` 安装流程。
- **代理地址位于沙箱外部且可能透明转发**：中等置信度。沙箱内无代理变量或 NAT 规则，但存在平台 CA 且公网可达。
- **Arena 工作区文件用于变更打包/持久化**：中高置信度。文件名和 `changes.zip` 强烈支持，但尚未读取元数据内容。

## 风险/漏洞候选 / Risk or vulnerability candidates
- 当前普通用户具备免交互 sudo，可读取 root 运行时信息；这是沙箱设计属性，但意味着沙箱内不存在强用户级隔离。
- envd 端口接受多个平台私网连接；是否存在鉴权与输入校验风险，本轮仅凭连接信息无法判断。

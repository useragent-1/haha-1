# 第二轮本地沙箱深度侦察报告

## 当前阶段 / Current phase
第二轮本地服务、控制面与网络状态侦察已完成。

## 已验证事实 / Verified facts
- A–F 指定命令均已执行；本轮所需命令均存在。
- 完整采集结果为 535 行、25735 字节。
- 原始采集 SHA-256：`c8ad98273dea791d095835383c006b701723e8584330219c339127bcc1a1df29`。
- 下方仅对两项实时 Jupyter `Set-Cookie` 值作安全遮蔽；其余命令输出保持原样，未另行删节。

## 关键证据 / Key evidence

### 平台控制、任务下发、网络出口相关线索

1. **本机 8888 为 Jupyter Server**：响应为 `TornadoServer/6.5.7`，页面标题为 `Jupyter Server`；`/metrics` 暴露 Prometheus 指标。指定探测的 `/envd`、`/health`、`/files`、`/commands`、`/process`、`/sandbox` 均返回 404。
2. **envd 是 root 级平台环境守护进程**：`/usr/bin/envd` 以 root 运行；服务配置注释明确出现 `updateEnvd`、`orchestrator`、`egress-proxy CA`、`POST /init`、`sandbox running/routable` 等控制面/出口管理线索。
3. **平台服务**：运行单元包括 `code-interpreter.service`、`envd.service`、`jupyter.service`、`ssh.service`、NFS/RPC 服务。
4. **events 地址**：`192.0.2.1:80` 可连通，根路径返回 `404` 与 JSON：`{"error":"no matching operation was found"}`，说明该地址存在按操作路由的 HTTP 服务，但本次没有枚举其他操作。
5. **控制/代理连接候选**：观察到本地 `169.254.0.21:49983` 与 `10.12.0.186:54512`、`10.12.0.78:60984/60988` 的已建立连接。其具体用途尚未由本轮证据直接确认。
6. **权限边界**：`sudo -n true` 返回 `sudo_exit=0`，当前 `user` 可无交互使用 sudo。
7. **任务下发证据状态**：未发现 `/var/log/envd*.log` 内容；本轮没有获得明确的任务载荷或任务下发记录。

### 完整命令输出（仅遮蔽实时 Cookie）

```text
===== A. 8888 端口服务指纹（重点） =====
$ curl -sv --max-time 5 http://127.0.0.1:8888/ 2>&1 | head -50
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
< Date: Mon, 05 Oct 2026 16:32:15 GMT
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

    <title>Jupyter Server</title>
    <link id="favicon" rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico?v=50afa725b5de8b00030139d09b38620224d4e7dba47c07ef0e86d4643f30c9bfe6bb7e1a4a1c561aa32834480909a4b6fe7cd1e17f7159330b6b5914bf45a880">
    
    <link rel="stylesheet" href="/static/style/bootstrap.min.css?v=0e8a7fbd6de23ad6b27ab95802a0a0915af6693af612bc304d83af445529ce5d95842309ca3405d10f538d45c8a3a261b8cff78b4bd512dd9effb4109a71d0ab" />
    <link rel="stylesheet" href="/static/style/bootstrap-theme.min.css?v=8b2f045cb5b4d5ad346f6e816aa2566829a4f5f2783ec31d80d46a57de8ac0c3d21fe6e53bcd8e1f38ac17fcd06d12088bc9b43e23b5d1da52d10c6b717b22b3" />
    <link rel="stylesheet" href="/static/style/index.css?v=30372e3246a801d662cf9e3f9dd656fa192eebde9054a2282449fe43919de9f0ee9b745d7eb49d3b0a5e56357912cc7d776390eddcab9dac85b77bdb17b4bdae" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    
    

    
    

</head>

<body class=""    dir="ltr">

  <noscript>

$ curl -s --max-time 5 http://127.0.0.1:8888/health; echo
<!DOCTYPE HTML>
<html>

<head>

    <meta charset="utf-8">

    <title>Jupyter Server</title>
    <link id="favicon" rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico?v=50afa725b5de8b00030139d09b38620224d4e7dba47c07ef0e86d4643f30c9bfe6bb7e1a4a1c561aa32834480909a4b6fe7cd1e17f7159330b6b5914bf45a880">
    
    <link rel="stylesheet" href="/static/style/bootstrap.min.css?v=0e8a7fbd6de23ad6b27ab95802a0a0915af6693af612bc304d83af445529ce5d95842309ca3405d10f538d45c8a3a261b8cff78b4bd512dd9effb4109a71d0ab" />
    <link rel="stylesheet" href="/static/style/bootstrap-theme.min.css?v=8b2f045cb5b4d5ad346f6e816aa2566829a4f5f2783ec31d80d46a57de8ac0c3d21fe6e53bcd8e1f38ac17fcd06d12088bc9b43e23b5d1da52d10c6b717b22b3" />
    <link rel="stylesheet" href="/static/style/index.css?v=30372e3246a801d662cf9e3f9dd656fa192eebde9054a2282449fe43919de9f0ee9b745d7eb49d3b0a5e56357912cc7d776390eddcab9dac85b77bdb17b4bdae" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    

    
<style type="text/css">
    /* disable initial hide */
    div#header,
    div#site {
        display: block;
    }
</style>


    
    

</head>

<body class=""    dir="ltr">

  <noscript>
    <div id='noscript'>
      Jupyter Server requires JavaScript.<br>
      Please enable it to proceed. 
    </div>
  </noscript>

  <div id="header" role="navigation" aria-label="Top Menu">
    <div id="header-container" class="container">
      <div id="jupyter_server" class="nav navbar-brand"><a href="/" title='dashboard'>
          <img src='/static/logo/logo.png?v=a2a176ee3cee251ffddf5fa21fe8e43727a9e5f87a06f9c91ad7b776d9e9d3d5e0159c16cc188a3965e00375fb4bc336c16067c688f5040c0c2d4bfdb852a9e4' alt='Jupyter Server' />
        </a></div>

      
      

      
      

    </div>
    <div class="header-bar"></div>

    
    
  </div>

  <div id="site">
    

<div class="error">
    
    <h1>404 : Not Found</h1>
    
    
<p>You are requesting a page that does not exist!</p>

</div>


  </div>

  
  

  


  <script type='text/javascript'>
    function _remove_token_from_url() {
      if (window.location.search.length <= 1) {
        return;
      }
      var search_parameters = window.location.search.slice(1).split('&');
      for (var i = 0; i < search_parameters.length; i++) {
        if (search_parameters[i].split('=')[0] === 'token') {
          // remote token from search parameters
          search_parameters.splice(i, 1);
          var new_search = '';
          if (search_parameters.length) {
            new_search = '?' + search_parameters.join('&');
          }
          var new_url = window.location.origin +
            window.location.pathname +
            new_search +
            window.location.hash;
          window.history.replaceState({}, "", new_url);
          return;
        }
      }
    }
    _remove_token_from_url();
  </script>
</body>

</html>

$ curl -s --max-time 5 http://127.0.0.1:8888/metrics 2>/dev/null | head -40
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
process_virtual_memory_bytes 2.63061504e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 1.01429248e+08
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.78482993849e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 1.93
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 42.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 4096.0
# HELP http_request_duration_seconds duration in seconds for all HTTP requests
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{handler="jupyter_server.services.api.handlers.APIStatusHandler",le="0.005",method="GET",status_code="200"} 1.0
http_request_duration_seconds_bucket{handler="jupyter_server.services.api.handlers.APIStatusHandler",le="0.01",method="GET",status_code="200"} 1.0

$ for path in envd health files commands process sandbox; do curl -s -o /dev/null -m 3 -w "/$path -> %{http_code}\\n" http://127.0.0.1:8888/$path; done
/envd -> 404
/health -> 404
/files -> 404
/commands -> 404
/process -> 404
/sandbox -> 404

===== B. envd 服务与进程 =====
$ cat /etc/systemd/system/envd.service 2>/dev/null
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
$ systemctl list-units --type=service --state=running 2>/dev/null | head -25
  UNIT                     LOAD   ACTIVE SUB     DESCRIPTION
  code-interpreter.service loaded active running Code Interpreter Server
  dbus.service             loaded active running D-Bus System Message Bus
  envd.service             loaded active running Env Daemon Service
  getty@tty1.service       loaded active running Getty on tty1
  jupyter.service          loaded active running Jupyter Server
  nfs-blkmap.service       loaded active running pNFS block layout mapping daemon
  rpcbind.service          loaded active running RPC bind portmap service
  ssh.service              loaded active running OpenBSD Secure Shell server
  systemd-journald.service loaded active running Journal Service
  systemd-logind.service   loaded active running User Login Management
  systemd-networkd.service loaded active running Network Configuration

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

11 loaded units listed.

$ ps aux | grep -v grep | grep -Ei "envd|systemd|nfs|vsock|kernel" | head -30
root          71  0.0  0.0      0     0 ?        I<   16:31   0:00 [nfsiod]
root         290  0.1  0.4  29440  8948 ?        Ss   16:31   0:00 /usr/lib/systemd/systemd-journald
systemd+     308  0.0  0.5  20752 10316 ?        Ss   16:31   0:00 /usr/lib/systemd/systemd-networkd
message+     340  0.0  0.1   6828  3624 ?        Ss   16:31   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
root         341  0.0  0.3  18384  7176 ?        Ss   16:31   0:00 /usr/lib/systemd/systemd-logind
root         359  1.6  1.3 1272548 26696 ?       S<Lsl 16:31   0:00 /usr/bin/envd
root         475  1.2  3.6 771316 73436 ?        Ssl  16:31   0:00 /usr/local/bin/python3.13 -Xfrozen_modules=off -m ipykernel_launcher -f /root/.local/share/jupyter/runtime/kernel-6bd8c74e-fd89-448c-9e6a-22de9783e8b5.json
root         490  1.0  2.8 1084636 58228 ?       Ssl  16:31   0:00 node /usr/bin/ijskernel --hide-undefined /root/.local/share/jupyter/runtime/kernel-1fe44cf5-e7f2-4ee3-82b8-24ac60d6d93f.json --protocol=5.1

$ ls -la /etc/envd /var/lib/envd /var/log 2>/dev/null | head -50
/var/log:
total 324
drwxr-xr-x   7 root    root              4096 Jul 23 15:09 .
drwxr-xr-x  11 root    root              4096 Jul 23 15:09 ..
lrwxrwxrwx   1 root    root                39 Jul 23 15:09 README -> ../../usr/share/doc/systemd/README.logs
-rw-r--r--   1 root    root             18551 Jul 23 18:05 alternatives.log
drwxr-xr-x   2 root    root                60 Jul 23 18:01 apt
-rw-rw----   1 root    utmp                 0 Jul 13 00:00 btmp
drwxr-x---   2 _chrony _chrony             60 Jul 23 15:09 chrony
-rw-r--r--   1 root    root            282959 Jul 23 18:01 dpkg.log
-rw-r--r--   1 root    root               981 Jul 23 15:10 fontconfig.log
drwxr-sr-x+  3 root    systemd-journal     60 Jul 23 15:09 journal
-rw-rw-r--   1 root    utmp                 0 Jul 13 00:00 lastlog
drwx------   2 root    root                60 Jul 23 15:09 private
drwxr-xr-x   3 root    root                60 Jul 23 15:09 runit
-rw-rw-r--   1 root    utmp              4992 Jul 23 18:05 wtmp

$ cat /var/log/envd*.log 2>/dev/null | tail -40

===== C. events 服务 =====
$ curl -sv --max-time 5 http://192.0.2.1/ 2>&1 | head -30
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
< Date: Mon, 05 Oct 2026 16:32:16 GMT
< Content-Length: 43
< 
{ [43 bytes data]
* Connection #0 to host 192.0.2.1 left intact
{"error":"no matching operation was found"}
===== D. 出站连接与网络状态（当前活动连接） =====
$ ss -tnp 2>/dev/null || netstat -tnp 2>/dev/null
State Recv-Q Send-Q         Local Address:Port          Peer Address:Port Process
ESTAB 0      0                  127.0.0.1:58532            127.0.0.1:35105       
ESTAB 0      0                  127.0.0.1:60465            127.0.0.1:51746       
ESTAB 0      0                  127.0.0.1:44461            127.0.0.1:43322       
ESTAB 0      0                  127.0.0.1:53335            127.0.0.1:41682       
ESTAB 0      0                  127.0.0.1:43501            127.0.0.1:52028       
ESTAB 0      0                  127.0.0.1:60638            127.0.0.1:60493       
ESTAB 0      0                  127.0.0.1:51746            127.0.0.1:60465       
ESTAB 0      0                  127.0.0.1:39652            127.0.0.1:35769       
ESTAB 0      0                  127.0.0.1:43501            127.0.0.1:52020       
ESTAB 0      0                  127.0.0.1:41435            127.0.0.1:38654       
ESTAB 0      0                  127.0.0.1:35105            127.0.0.1:58532       
ESTAB 0      0                  127.0.0.1:35769            127.0.0.1:39652       
ESTAB 0      0                  127.0.0.1:52020            127.0.0.1:43501       
ESTAB 0      0                  127.0.0.1:43338            127.0.0.1:44461       
ESTAB 0      0                  127.0.0.1:60493            127.0.0.1:60638       
ESTAB 0      0                  127.0.0.1:52028            127.0.0.1:43501       
ESTAB 0      0                  127.0.0.1:53335            127.0.0.1:41656       
ESTAB 0      0                  127.0.0.1:38654            127.0.0.1:41435       
ESTAB 0      0                  127.0.0.1:41682            127.0.0.1:53335       
ESTAB 0      0                  127.0.0.1:41656            127.0.0.1:53335       
ESTAB 0      0                  127.0.0.1:60465            127.0.0.1:51738       
ESTAB 0      0                  127.0.0.1:51738            127.0.0.1:60465       
ESTAB 0      0                  127.0.0.1:35105            127.0.0.1:58542       
ESTAB 0      0                  127.0.0.1:43322            127.0.0.1:44461       
ESTAB 0      0                  127.0.0.1:58542            127.0.0.1:35105       
ESTAB 0      0                  127.0.0.1:44461            127.0.0.1:43338       
ESTAB 0      0                      [::1]:8888                 [::1]:35824       
ESTAB 0      0                      [::1]:35798                [::1]:8888        
ESTAB 0      0      [::ffff:169.254.0.21]:49983 [::ffff:10.12.0.186]:54512       
ESTAB 0      0                      [::1]:8888                 [::1]:35808       
ESTAB 0      0                      [::1]:8888                 [::1]:35798       
ESTAB 0      0                      [::1]:35808                [::1]:8888        
ESTAB 0      0      [::ffff:169.254.0.21]:49983  [::ffff:10.12.0.78]:60984       
ESTAB 0      0      [::ffff:169.254.0.21]:49983  [::ffff:10.12.0.78]:60988       
ESTAB 0      0                      [::1]:35824                [::1]:8888        

$ cat /proc/net/tcp | head -25
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 0100007F:8BB9 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13443 1 000000009067aa04 100 0 0 10 0                     
   1: 1500FEA9:BB49 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13157 1 000000001e8c3964 100 0 0 10 0                     
   2: 1500FEA9:8773 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13161 1 00000000d337e5fb 100 0 0 10 0                     
   3: 00000000:006F 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 665 1 00000000ff884a55 100 0 0 10 0                       
   4: 1500FEA9:8BB9 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13531 1 00000000bda0873c 100 0 0 10 0                     
   5: 0100007F:BB49 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12994 1 0000000099193d06 100 0 0 10 0                     
   6: 0100007F:8773 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13453 1 00000000c2b674b7 100 0 0 10 0                     
   7: 0100007F:22B8 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12879 1 00000000a93599fa 100 0 0 10 0                     
   8: 1500FEA9:22B8 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12929 1 000000008002d493 100 0 0 10 0                     
   9: 0100007F:ADAD 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13445 1 0000000027428b26 100 0 0 10 0                     
  10: 1500FEA9:8921 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13181 1 00000000a52d5425 100 0 0 10 0                     
  11: 0100007F:99D3 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13491 1 000000006c7aa6b5 100 0 0 10 0                     
  12: 0100007F:A1DB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13497 1 000000001fcb862e 100 0 0 10 0                     
  13: 0100007F:A9ED 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13495 1 000000003a8a255a 100 0 0 10 0                     
  14: 0100007F:8921 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13499 1 000000001fad1251 100 0 0 10 0                     
  15: 1500FEA9:ADAD 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13165 1 00000000fd27b3d8 100 0 0 10 0                     
  16: 1500FEA9:99D3 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13169 1 00000000f02eaf48 100 0 0 10 0                     
  17: 1500FEA9:A1DB 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13174 1 000000002db67eac 100 0 0 10 0                     
  18: 1500FEA9:A9ED 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13177 1 00000000a15c30df 100 0 0 10 0                     
  19: 1500FEA9:EC31 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13185 1 00000000a22587a8 100 0 0 10 0                     
  20: 1500FEA9:D057 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13188 1 000000009748cd79 100 0 0 10 0                     
  21: 1500FEA9:EC4D 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13537 1 000000002c43ad85 100 0 0 10 0                     
  22: 00000000:C34F 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13550 1 00000000c001fdf1 100 0 0 10 0                     
  23: 0100007F:EC31 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 13449 1 0000000009670303 100 0 0 10 0                     

$ cat /proc/net/route
Iface	Destination	Gateway 	Flags	RefCnt	Use	Metric	Mask		MTU	Window	IRTT                                                       
eth0	00000000	1600FEA9	0003	0	0	0	00000000	0	0	0                                                                               
eth0	1400FEA9	00000000	0001	0	0	0	FCFFFFFF	0	0	0                                                                               

===== E. sudo 权限探测 =====
$ sudo -n true 2>&1; echo "sudo_exit=$?"
sudo_exit=0

$ sudo -n ls /root 2>&1 | head -20
ijava-1.3.0.zip
install.py
java
requirements.txt

$ sudo -n ls /etc/systemd/system/ 2>&1 | head -40
chrony-wait.service
chronyd.service
code-interpreter.service
ctrl-alt-del.target
dbus-org.freedesktop.network1.service
e2scrub_reap.service
envd.service
getty.target.wants
jupyter.service
local-fs.target.wants
multi-user.target.wants
nfs-client.target.wants
remote-fs.target.wants
serial-getty@ttyS0.service
serial-getty@ttyS0.service.d
sockets.target.wants
ssh.service.wants
ssh.socket.wants
sshd.service
sshd.service.wants
sshd@.service.wants
sysinit.target.wants
systemd-binfmt.service
systemd-firstboot.service
systemd-journald.service.d
systemd-journald.service.wants
systemd-networkd-wait-online.service
systemd-networkd.service.d
timers.target.wants

===== F. 最近变化的文件（可能的平台注入痕迹） =====
$ find / -maxdepth 3 -newer /etc/hostname -type f 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -50
/etc/ImageMagick-7/colors.xml
/etc/ImageMagick-7/delegates.xml
/etc/ImageMagick-7/log.xml
/etc/ImageMagick-7/mime.xml
/etc/ImageMagick-7/policy.xml
/etc/ImageMagick-7/quantization-table.xml
/etc/ImageMagick-7/thresholds.xml
/etc/ImageMagick-7/type-apple.xml
/etc/ImageMagick-7/type-dejavu.xml
/etc/ImageMagick-7/type-ghostscript.xml
/etc/ImageMagick-7/type-urw-base35-type1.xml
/etc/ImageMagick-7/type-urw-base35.xml
/etc/ImageMagick-7/type-windows.xml
/etc/ImageMagick-7/type.xml
/etc/X11/Xreset
/etc/X11/Xsession
/etc/X11/Xsession.options
/etc/X11/rgb.txt
/etc/alternatives/README
/etc/bash_completion.d/git-prompt
/etc/cron.daily/apt-compat
/etc/cron.daily/dpkg
/etc/default/nss
/etc/default/useradd
/etc/default/ssh
/etc/default/rpcbind
/etc/default/nfs-common
/etc/default/dbus
/etc/default/chrony
/etc/dpkg/dpkg.cfg
/etc/dpkg/shlibs.default
/etc/dpkg/shlibs.override
/etc/fonts/fonts.conf
/etc/init.d/procps
/etc/init.d/dbus
/etc/init.d/x11-common
/etc/init.d/rpcbind
/etc/init.d/nfs-common
/etc/init.d/chrony
/etc/init.d/ssh
/etc/init.d/sudo
/etc/ld.so.conf.d/libc.conf
/etc/ld.so.conf.d/x86_64-linux-gnu.conf
/etc/logrotate.d/alternatives
/etc/logrotate.d/apt
/etc/logrotate.d/dpkg
/etc/logrotate.d/chrony
/etc/logrotate.d/wtmpdb
/etc/mercurial/hgrc
/etc/mysql/mariadb.cnf

$ ls -la /code /tmp 2>/dev/null
/code:
total 4
drwxrwxrwx  2 root root   60 Jul 23 18:05 .
drwxr-xr-x 19 root root 4096 Jul 23 18:05 ..

/tmp:
total 92
drwxrwxrwt  8 root root   240 Oct  5 16:32 .
drwxr-xr-x 19 root root  4096 Jul 23 18:05 ..
drwxrwxrwt  2 root root    40 Jul 23 18:05 .ICE-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .X11-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .XIM-unix
drwxrwxrwt  2 root root    40 Jul 23 18:05 .font-unix
drwxr-xr-x  2 user user   120 Oct  5 16:29 arena-workspace
-rw-r--r--  1 user user 46732 Oct  5 16:28 local_recon_raw.txt
-rw-r--r--  1 user user 24905 Oct  5 16:32 local_recon_round2_raw.txt
-rwxr-xr-x  1 user user  2410 Oct  5 16:28 run_recon.sh
-rwxr-xr-x  1 user user  4417 Oct  5 16:32 run_recon_round2.sh
drwx------  3 root root    60 Jul 23 18:05 systemd-private-2bb79165136a4b63829d17027b0a8e40-systemd-logind.service-zTa4Mm
```

## 推断与置信度 / Inference and confidence
- `envd` 很可能承担沙箱初始化、环境更新、证书/出口代理注入及编排器协同。**置信度：高**（服务文件注释直接支持）。
- `192.0.2.1` 很可能是平台事件或操作网关。**置信度：中高**（环境命名和 HTTP 操作路由错误共同支持）。
- `49983` 上的 10.12.0.x 连接可能属于平台控制、内核/代码解释器通道或代理转发。**置信度：中低**（只有连接信息，未完成进程归属与协议确认）。
- 8888 的 `/health` 实际为 Jupyter 404 HTML，而非健康检查接口。**置信度：高**。

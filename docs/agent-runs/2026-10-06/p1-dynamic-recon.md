# P1 动态分析工具包验证报告

## 安装中真实失败

1. 首次将可选 qemu 与必选 apt 工具合并安装时，apt 索引陈旧，qemu 10.0.11 返回 HTTP 404，整个 apt 命令退出 100；先执行 `apt-get update`，再拆分必选项与可选 qemu，二者最终退出 0。
2. 指定的 `frida-ps -V` 不被 frida-tools 14.11.0 支持，退出 2；改用受支持的 `frida-ps --version`，返回 17.22.2，且实际进程枚举退出 0。
3. 快照恢复后脚本执行位丢失，首次直接执行 `triage_run.sh` 返回 Permission denied/126；恢复执行位后真实复测成功。失败原文保存在 `skills/dynamic-recon/deep/evidence/p1-failures.txt`。

## 最终自检原文

```text
=== gdb --version ===
GNU gdb (Debian 16.3-1) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
EXIT=0
=== python3 -c "import angr; print(angr.__version__)" ===
10.0.1.post1
EXIT=0
=== frida-ps -V (requested form) ===
usage: frida-ps [options]
frida-ps: error: unrecognized arguments: -V
EXIT=2
=== frida-ps --version (supported fallback) ===
17.22.2
EXIT=0
=== frida-ps (runtime enumeration) ===
 PID  Name
----  -------
1883  bash
1886  bash
1910  python3
1887  tee
1909  timeout
EXIT=0
=== qemu-aarch64 --version ===
qemu-aarch64 version 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1)
Copyright (c) 2003-2025 Fabrice Bellard and the QEMU Project developers
EXIT=0
```

## curl 动态分诊控制台原文

```text
dynamic triage complete: /home/user/p1-curl-triage
stage	exit_code
baseline	0
strace	0
ltrace	0
gdb	0
```

## status.tsv 原文

```text
stage	exit_code
baseline	0
strace	0
ltrace	0
gdb	0
```

## baseline.stdout 原文

```text
curl 8.14.1 (x86_64-pc-linux-gnu) libcurl/8.14.1 OpenSSL/3.5.6 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.64.0 nghttp3/1.8.0 librtmp/2.3 OpenLDAP/2.6.10
Release-Date: 2025-06-04, security patched: 8.14.1-2+deb13u4
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```

## gdb.stdout 原文

```text
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
curl 8.14.1 (x86_64-pc-linux-gnu) libcurl/8.14.1 OpenSSL/3.5.6 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.64.0 nghttp3/1.8.0 librtmp/2.3 OpenLDAP/2.6.10
Release-Date: 2025-06-04, security patched: 8.14.1-2+deb13u4
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
[Inferior 1 (process 2026) exited normally]

=== GDB_POST_RUN ===
The program being debugged is not being run.
```

## behavior_report.py 原文

```text
{"environment_changes": 0, "file_writes": 0, "network_connections": 1, "persistence_indicators": 0, "process_edges": 0, "processes": 1}
```

## crash_trace.py 实测

```text
signal=SIGSEGV
frame_count=3
key_frames=['crash_here', 'middle', 'main']
register_count=17
mapping_count=23
key_mapping_count=6
```

结论：P1 必选工具与可选 qemu 均安装成功；技能和三个指定脚本存在，curl baseline/strace/ltrace/gdb 四阶段均退出 0；崩溃解析包含调用链、关键帧、寄存器与映射快照。P2 尚未开始。

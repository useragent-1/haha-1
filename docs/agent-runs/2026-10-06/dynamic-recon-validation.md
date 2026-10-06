# Dynamic Recon Implementation and Validation Report

## 范围

本轮新增 `skills/dynamic-recon/`、4 个 `scripts/dynamic/` 脚本、SKILLS 路由、环境指纹和空间预算。动态执行仅针对系统自带 `/usr/bin/curl --version` 与本轮编译的无害 SIGSEGV fixture。

## 工具安装后自检原文

```text
=== gdb --version ===
GNU gdb (Debian 16.3-1) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
EXIT=0
=== strace --version ===
strace -- version 6.13
Copyright (c) 1991-2025 The strace developers <https://strace.io>.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Optional features enabled: stack-trace=libunwind stack-demangle m32-mpers mx32-mpers
EXIT=0
=== ltrace --version ===
ltrace 0.7.91
Copyright (C) 2010-2013 Petr Machata, Red Hat Inc.
Copyright (C) 1997-2009 Juan Cespedes <cespedes@debian.org>.
License GPLv2+: GNU GPL version 2 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
EXIT=0
=== patchelf --version ===
patchelf 0.18.0
EXIT=0
=== qemu-aarch64 --version ===
qemu-aarch64 version 10.0.13 (Debian 1:10.0.13+ds-0+deb13u1)
Copyright (c) 2003-2025 Fabrice Bellard and the QEMU Project developers
EXIT=0
=== python import angr ===
10.0.1.post1
EXIT=0
=== python import frida ===
17.22.2
EXIT=0
=== frida-ps ===
 PID  Name
----  -------
1839  bash
1842  bash
1863  python3
1843  tee
1862  timeout
EXIT=0
```

## 首次分诊失败原文与修复

首次实际运行时，baseline/strace/ltrace 成功，但 GDB 在目标正常退出后继续执行 `bt/info registers/x`，因此 GDB 批处理退出 1：

```text
dynamic triage complete: /home/user/dynamic-curl-triage
stage	exit_code
baseline	0
strace	0
ltrace	0
gdb	1
```

未跳过该失败。已改为注册 `gdb.events.stop`：只有真实 stop/crash 才采集回溯、寄存器和指令；正常退出不再误报失败。

## 修复后完整分诊控制台原文

```text
dynamic triage complete: /home/user/dynamic-curl-triage
stage	exit_code
baseline	0
strace	0
ltrace	0
gdb	0
```

## 结构化报告原文

# Dynamic Triage Report

- Target: `/usr/bin/curl`
- Started UTC: `2026-10-06T03:39:11Z`
- Timeout per stage: `20s`

## Stage status

| Stage | Exit code |
|---|---:|
| baseline | 0 |
| strace | 0 |
| ltrace | 0 |
| gdb | 0 |

## Artifacts

- `baseline.stderr`
- `baseline.stdout`
- `command.shell`
- `gdb.commands`
- `gdb.stderr`
- `gdb.stdout`
- `ltrace.log`
- `ltrace.stderr`
- `ltrace.stdout`
- `metadata.txt`
- `status.tsv`
- `strace.log`
- `strace.stderr`
- `strace.stdout`
- `summary.json`

> Exit 124 means timeout. ptrace restrictions may make strace/ltrace/gdb fail; inspect each `.stderr` verbatim.

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
[Inferior 1 (process 2008) exited normally]

=== GDB_POST_RUN ===
The program being debugged is not being run.
```

## gdb.stderr 原文

```text

```

该文件为空，保留此空块作为证据。完整 strace/ltrace 未截断日志位于 `skills/dynamic-recon/deep/evidence/curl/`。

## behavior_report.py 原始输出

```text
{"environment_changes": 0, "file_writes": 0, "network_connections": 1, "persistence_indicators": 0, "process_edges": 0, "processes": 1}
```

## api_extractor.py 原始输出

```json
{
  "schema": "dynamic-recon/api-extractor-v1",
  "root": "/home/user/dynamic-fixtures/web",
  "files_scanned": 1,
  "finding_count": 6,
  "findings": [
    {
      "type": "url",
      "value": "https://api.example.test/v1/items",
      "file": "app.js",
      "line": 1
    },
    {
      "type": "domain",
      "value": "api.example.test",
      "file": "app.js",
      "line": 1
    },
    {
      "type": "websocket",
      "value": "wss://stream.example.test/socket",
      "file": "app.js",
      "line": 2
    },
    {
      "type": "domain",
      "value": "stream.example.test",
      "file": "app.js",
      "line": 2
    },
    {
      "type": "endpoint",
      "value": "/api/session",
      "file": "app.js",
      "line": 3
    },
    {
      "type": "authorization-pattern",
      "value": "Bearer [REDACTED]",
      "file": "app.js",
      "line": 3
    }
  ]
}
```

## crash_trace.py 原始输出

```text
# Crash Trace

- Signal: `SIGSEGV`
- Frames: 3

## Key frames

| # | Address | Function |
|---:|---|---|
| 0 | `0x0000555555555139` | `crash_here` |
| 1 | `0x000055555555514b` | `middle` |
| 2 | `0x0000555555555157` | `main` |

## Registers

- `r10` = `0x7fffffffe890`
- `r11` = `0x202`
- `r12` = `0x0`
- `r13` = `0x7fffffffec78`
- `r14` = `0x7ffff7ffd000`
- `r15` = `0x555555557e08`
- `r8` = `0x0`
- `r9` = `0x7ffff7fccaa0`
- `rax` = `0x0`
- `rbp` = `0x7fffffffeb30`
- `rbx` = `0x7fffffffec68`
- `rcx` = `0x555555557e08`
- `rdi` = `0x1`
- `rdx` = `0x7fffffffec78`
- `rip` = `0x555555555139`
- `rsi` = `0x7fffffffec68`
- `rsp` = `0x7fffffffeb30`
```

## angr 路径探索原始输出

```text
{'active': 0, 'deadended': 1, 'errored': 0}
```

## 结论

- 修复后 `/usr/bin/curl` baseline、strace、ltrace、gdb 四阶段退出码全部为 0。
- 4 个脚本均通过语法检查并至少执行一次真实输入；不是只验证 `--help`。
- Authorization fixture 值未写入结果，仅保留 `Bearer [REDACTED]` 模式。
- 内核级、真实 GUI、强反调试与专有硬件场景未在本沙箱验证，已在 SKILL.md 逐项标注。

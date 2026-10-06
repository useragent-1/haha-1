# `/usr/bin/curl` 动态分诊实测

测试时间：2026-10-06 UTC。目标为沙箱系统自带无害二进制 `/usr/bin/curl`，参数 `--version`，每阶段超时 20 秒。

## 执行命令

```bash
scripts/dynamic/triage_run.sh --timeout 20 \
  --output /home/user/dynamic-curl-triage -- /usr/bin/curl --version
```

## 控制台原始输出

```text
dynamic triage complete: /home/user/dynamic-curl-triage
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
[Inferior 1 (process 2008) exited normally]

=== GDB_POST_RUN ===
The program being debugged is not being run.
```

`gdb.stderr` 为空。完整未截断的 `strace.log`、`ltrace.log`、各阶段 stdout/stderr、`status.tsv`、`summary.json` 和 `report.md` 位于 `deep/evidence/curl/`。

## 其他脚本实测

- `behavior_report.py`：从 curl trace 得到 1 个进程执行、1 个网络连接、0 个持久化项；生成 JSON 与 Markdown。
- `api_extractor.py`：对 JS fixture 提取 6 项，包括 HTTP URL、WebSocket、域名、API path；Authorization 输出为 `Bearer [REDACTED]`。
- `crash_trace.py`：用实际编译并在 GDB 中触发的无害 SIGSEGV fixture 解析出 `crash_here → middle → main` 三帧。
- 全部 fixture 证据在 `deep/evidence/fixtures/`。

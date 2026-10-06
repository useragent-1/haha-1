# 交叉分析：curl ↔ libcurl

## 已验证事实 / Verified facts
- `/usr/bin/curl` 的 DT_NEEDED 包含 `libcurl.so.4`，运行时解析为 `/lib/x86_64-linux-gnu/libcurl.so.4`。
- 主程序导入 `curl_easy_init/setopt/perform@CURL_OPENSSL_4`。
- `libcurl.so.4.8.0` 分别在 `0x37610`、`0x7ed70`、`0x376c0` 导出同版本符号。
- 主程序 `0x1d9a7` 调用 `curl_easy_perform@plt`；库入口 `0x376c0` 跳转到实现 `0x37080`。
- CLI 和库均为 curl 8.14.1；Debian 包分别为 `curl` 与 `libcurl4t64:amd64`。

## 关键证据 / Key evidence
```text
$ curl --version
curl 8.14.1 (x86_64-pc-linux-gnu) libcurl/8.14.1 OpenSSL/3.5.6 zlib/1.3.1 brotli/1.1.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.64.0 nghttp3/1.8.0 librtmp/2.3 OpenLDAP/2.6.10
Release-Date: 2025-06-04, security patched: 8.14.1-2+deb13u4
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd

$ ldd /usr/bin/curl
	linux-vdso.so.1 (0x00007ffc15de7000)
	libcurl.so.4 => /lib/x86_64-linux-gnu/libcurl.so.4 (0x00007f493501e000)
	libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f4934ffe000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4934e0a000)
	libnghttp3.so.9 => /lib/x86_64-linux-gnu/libnghttp3.so.9 (0x00007f4934de0000)
	libnghttp2.so.14 => /lib/x86_64-linux-gnu/libnghttp2.so.14 (0x00007f4934dac000)
	libidn2.so.0 => /lib/x86_64-linux-gnu/libidn2.so.0 (0x00007f4934d79000)
	librtmp.so.1 => /lib/x86_64-linux-gnu/librtmp.so.1 (0x00007f4934d5b000)
	libssh2.so.1 => /lib/x86_64-linux-gnu/libssh2.so.1 (0x00007f4934d12000)
	libpsl.so.5 => /lib/x86_64-linux-gnu/libpsl.so.5 (0x00007f4934cfe000)
	libssl.so.3 => /lib/x86_64-linux-gnu/libssl.so.3 (0x00007f4934bf0000)
	libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x00007f4934400000)
	libgssapi_krb5.so.2 => /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 (0x00007f4934b98000)
	libldap.so.2 => /lib/x86_64-linux-gnu/libldap.so.2 (0x00007f4934b34000)
	liblber.so.2 => /lib/x86_64-linux-gnu/liblber.so.2 (0x00007f4934b23000)
	libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007f4934a59000)
	libbrotlidec.so.1 => /lib/x86_64-linux-gnu/libbrotlidec.so.1 (0x00007f4934a4b000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f4935167000)
	libunistring.so.5 => /lib/x86_64-linux-gnu/libunistring.so.5 (0x00007f4934218000)
	libgnutls.so.30 => /lib/x86_64-linux-gnu/libgnutls.so.30 (0x00007f4933e00000)
	libhogweed.so.6 => /lib/x86_64-linux-gnu/libhogweed.so.6 (0x00007f49341cd000)
	libnettle.so.8 => /lib/x86_64-linux-gnu/libnettle.so.8 (0x00007f4934177000)
	libgmp.so.10 => /lib/x86_64-linux-gnu/libgmp.so.10 (0x00007f49340ed000)
	libkrb5.so.3 => /lib/x86_64-linux-gnu/libkrb5.so.3 (0x00007f4933d28000)
	libk5crypto.so.3 => /lib/x86_64-linux-gnu/libk5crypto.so.3 (0x00007f49340bf000)
	libcom_err.so.2 => /lib/x86_64-linux-gnu/libcom_err.so.2 (0x00007f4934a41000)
	libkrb5support.so.0 => /lib/x86_64-linux-gnu/libkrb5support.so.0 (0x00007f49340b1000)
	libsasl2.so.2 => /lib/x86_64-linux-gnu/libsasl2.so.2 (0x00007f4934095000)
	libbrotlicommon.so.1 => /lib/x86_64-linux-gnu/libbrotlicommon.so.1 (0x00007f4934072000)
	libp11-kit.so.0 => /lib/x86_64-linux-gnu/libp11-kit.so.0 (0x00007f4933b87000)
	libtasn1.so.6 => /lib/x86_64-linux-gnu/libtasn1.so.6 (0x00007f493405c000)
	libkeyutils.so.1 => /lib/x86_64-linux-gnu/libkeyutils.so.1 (0x00007f4934055000)
	libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007f4934043000)
	libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007f4934036000)

$ readelf -d /usr/bin/curl | grep NEEDED
 0x0000000000000001 (NEEDED)             Shared library: [libcurl.so.4]
 0x0000000000000001 (NEEDED)             Shared library: [libz.so.1]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]

$ readelf -Ws /usr/bin/curl | grep -E "curl_easy_(init|setopt|perform)"
    71: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_setopt@CURL_OPENSSL_4 (3)
    84: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_init@CURL_OPENSSL_4 (3)
    85: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_perform@CURL_OPENSSL_4 (3)

$ readelf -Ws /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 | grep -E "curl_easy_(init|setopt|perform)@@"
   596: 0000000000037610   161 FUNC    GLOBAL DEFAULT   13 curl_easy_init@@CURL_OPENSSL_4
   616: 00000000000376c0     9 FUNC    GLOBAL DEFAULT   13 curl_easy_perform@@CURL_OPENSSL_4
   674: 000000000007ed70   251 FUNC    GLOBAL DEFAULT   13 curl_easy_setopt@@CURL_OPENSSL_4

$ objdump -p /usr/bin/curl | grep -E "NEEDED|CURL_OPENSSL"
  NEEDED               libcurl.so.4
  NEEDED               libz.so.1
  NEEDED               libc.so.6
    0x044a42e4 0x00 03 CURL_OPENSSL_4

$ dpkg-query -S /usr/bin/curl /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0
curl: /usr/bin/curl
libcurl4t64:amd64: /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0

$ command -v xxd || echo "xxd: missing after tool-call boundary"
xxd: missing after tool-call boundary

$ od -Ax -tx1z -j $((0x31bc0)) -N 224 /usr/bin/curl
031bc0 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50  >ABCDEFGHIJKLMNOP<
031bd0 51 52 53 54 55 56 57 58 59 5a 61 62 63 64 65 66  >QRSTUVWXYZabcdef<
031be0 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76  >ghijklmnopqrstuv<
031bf0 77 78 79 7a 30 31 32 33 34 35 36 37 38 39 2d 5f  >wxyz0123456789-_<
031c00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >................<
*
031c20 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50  >ABCDEFGHIJKLMNOP<
031c30 51 52 53 54 55 56 57 58 59 5a 61 62 63 64 65 66  >QRSTUVWXYZabcdef<
031c40 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76  >ghijklmnopqrstuv<
031c50 77 78 79 7a 30 31 32 33 34 35 36 37 38 39 2b 2f  >wxyz0123456789+/<
031c60 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >................<
*
031c80 10 01 02 03 04 05 06 07 08 09 00 00 00 00 00 00  >................<
031c90 00 0a 0b 0c 0d 0e 0f 00 00 00 00 00 00 00 00 00  >................<
031ca0

$ od -Ax -tx1z -j $((0xcae00)) -N 64 /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0
0cae00 01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10  >.#Eg........vT2.<
0cae10 ff ff ff ff ff ff ff ff 00 00 00 00 00 00 00 00  >................<
0cae20 76 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >v...............<
0cae30 74 6c 73 2d 73 65 72 76 65 72 2d 65 6e 64 2d 70  >tls-server-end-p<
0cae40
```

## 推断与置信度 / Inference and confidence
版本化符号、DT_NEEDED、ldd 路径和调用/导出偏移形成完整链路，关联置信度高。主程序负责 CLI 参数和结果处理，协议状态机主要落在 libcurl。

## 建议下一步 / Suggested next steps
1. 安装调试符号恢复 `0x37080` 内部函数名。
2. 用 `LD_DEBUG=bindings` 在无网络的 `curl file://` 请求上验证运行时绑定。

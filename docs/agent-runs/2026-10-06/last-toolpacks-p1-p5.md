# 最后一批工具包 P1–P5 最终报告

## 总结

P1–P5 已按序完成真实安装、实现和实测。P1 详见 `P1_DYNAMIC_RECON_REPORT.md`；本报告记录 P2–P5 原始验证输出和所有修正。未推送 GitHub，本轮只修改 `/home/user/push-tmp` 工作树。

## P2 协议与流量

首次 Scapy fixture 未固定 MAC，只读沙箱输出 `getmacbyip failed on [Errno 1] Operation not permitted` 并使用广播地址；未隐藏。固定本地合成 MAC 后，最终三步原始输出：

```text
wrote_packets=6
{"layer_counts": {"DNS": 2, "Ether": 6, "IP": 6, "Raw": 4, "TCP": 4, "UDP": 2}, "packet_count": 6, "session_count": 2}
{"packets": 6, "protocols": ["DNS", "HTTP", "IPv4", "TCP", "UDP"], "template": "/home/user/p2-protocol-test/template.json"}
{"finding_count": 5, "packet_count": 6, "types": {"periodic-beaconing": 1, "suspicious-user-agent": 4}}
authorization_field=Bearer [REDACTED]
```

## P3 前端 / JS

真实公开站点：`https://petstore3.swagger.io/`。首次域名正则把 JS 属性链误报为域名，得到 8653 项；收紧 TLD 规则后最终输出：

```text
{"findings": 169, "sources": 4, "types": {"authorization-pattern": 3, "domain": 101, "url": 65}}
```

Source map、beautify、位置-only secret scan：

```text
{"map_count": 1, "source_count": 1, "recovered_count": 1}
{"after_lines": 7, "after_sha256": "cdcfb8d7b3e3bdf8ce673b2fc79e02a7d50574ae66ec3a3cfe3365a0c24feed5", "before_lines": 2, "before_sha256": "4aee180b4da90c754d608b57386e1626d47f0bb9e078d8460cdad6c27a841219", "indicators": [{"count": 1, "type": "eval"}, {"count": 1, "type": "hex-escapes"}], "long_lines_over_1000": 0, "max_line_length": 314, "schema": "frontend-re/beautify-v1", "semantic_notice": "Formatting is lexical and not proof of semantic equivalence; inspect the diff."}
{"files_scanned": 2, "finding_count": 2, "types": {"generic-secret-assignment": 1, "private-ipv4": 1}}
```

内联 source map 的 data URI 最初会重复写入报告，已修复为 `data:[REDACTED sha256=…]`。

## P4 反混淆与脱壳

UPX 打包原始输出：

```text
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.4       Markus Oberhumer, Laszlo Molnar & John Reiser    May 9th 2024

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
     15992 ->      5936   37.12%   linux/amd64   hello.upx

Packed 1 file.
```

自动脱壳链原始输出：

```text
stage	exit_code
upx-test	0
upx-unpack	0
6faa27cf86b908dbe7d3c4ce84e7ef0d759c64ade7e6e2853f8ba1a17f574c79  /home/user/p4-upx-test/unpack-result/original.bin
9a3b8e1fc76c82b1d161d9b5295640c02117a35d3c87082b199dd7d0f90d3bec  /home/user/p4-upx-test/unpack-result/unpacked.bin
output=/home/user/p4-upx-test/unpack-result
{"candidate_count": 2, "objdump_exit": 0}
```

```text
original_run=authorized
packed_run=authorized
unpacked_run=authorized
```

差异输出：

```text
{"entropy_delta": -5.762673, "imports_added": [], "imports_removed": [], "sections_added": [".bss", ".comment", ".data", ".dynamic", ".dynstr", ".dynsym", ".eh_frame", ".eh_frame_hdr", ".fini", ".fini_array", ".gnu.hash", ".gnu.version", ".gnu.version_r", ".got", ".got.plt", ".init", ".init_array", ".interp", ".note.ABI-tag", ".note.gnu.build-id", ".note.gnu.property", ".plt", ".plt.got", ".rela.dyn", ".rela.plt", ".rodata", ".shstrtab", ".strtab", ".symtab", ".text", "NULL"], "sections_removed": [], "size_delta": 10056}
```

首次 `-O2` fixture 将 XOR 消除，候选数为0；改用 `-O0 -fno-inline` 后命中 `demo_decode@0x1139`。初版 imports parser 误收 `(2)/(3)/UND`，已修复并复测。

## P5 报告与批量

```text
echo	ok	0
true	ok	0
{"sample_count": 2, "ok_count": 2, "index": "/home/user/p5-report-test/batch/index.json"}
{"output": "/home/user/p5-report-test/final-report.html", "evidence_count": 3, "confidence": "high", "bytes": 13609}
```

HTML 前30行原文：

```text
     1	<!doctype html>
     2	<html lang="en">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1">
     6	<title>Agent Toolpack Validation</title>
     7	<style>body{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a}h1,h2{color:#17365d}table{border-collapse:collapse;width:100%}th,td{border:1px solid #bbb;padding:.45rem;text-align:left}pre{background:#f5f7f9;border:1px solid #d9e0e6;padding:1rem;overflow:auto;white-space:pre-wrap}.high{color:#176b2c}.medium{color:#8a5900}.low{color:#a12424}.meta{color:#566}section{margin:2rem 0}</style>
     8	</head>
     9	<body>
    10	<h1>Agent Toolpack Validation</h1>
    11	<p class="meta">Generated UTC: 2026-10-06T03:54:45.462849+00:00</p>
    12	<section>
    13	<h2>Conclusions</h2>
    14	<p>Confidence: <strong class="high">HIGH</strong></p>
    15	<ul>
    16	<li>Two harmless system binaries completed auto_analyze with exit code 0.</li>
    17	<li>UPX unpack evidence records distinct packed and unpacked SHA-256 values.</li>
    18	</ul>
    19	</section>
    20	<section>
    21	<h2>Evidence table</h2>
    22	<table>
    23	<thead><tr><th>Path</th><th>Type</th><th>Bytes</th><th>SHA-256</th></tr></thead>
    24	<tbody>
    25	<tr><td>/home/user/p5-report-test/batch/index.json</td><td>JSON</td><td>633</td><td><code>12759f15b216423965ac5c44ea8bc819df67aa42a266d4e20e4c83da196328f0</code></td></tr>
    26	<tr><td>/home/user/p5-report-test/batch/index.md</td><td>Markdown/Text</td><td>309</td><td><code>2b0a82a122d2891b3e50f7a7c8f63ab70e90f59de682c926b463410a5218ada5</code></td></tr>
    27	<tr><td>/home/user/p4-upx-test/unpack-result/diff.json</td><td>JSON</td><td>6640</td><td><code>f888b5528f9236ea49a19e00a91cca0cc41ec00df0686def13cd704bc41570b2</code></td></tr>
    28	</tbody>
    29	</table>
    30	</section>
```

## 沙箱明确不可覆盖

- 内核模块、rootkit、驱动、hypervisor 和内核级反调试；
- 真实 GUI、GPU、系统托盘、浏览器 DevTools 图形交互；
- 强反调试对抗、定制内核、TEE 和专有硬件；
- 完整乱序 TCP/QUIC/TLS 解密、抓包丢失恢复；
- 未授权登录、验证码绕过、生产凭据和真实 License 激活链路。

这些项目均未宣称已验证。

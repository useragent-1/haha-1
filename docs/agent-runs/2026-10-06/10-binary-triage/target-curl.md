# 目标报告：/usr/bin/curl

## 当前阶段 / Current phase
静态分诊、密码常量扫描、ELF 深扫、YARA、ROP 与函数级调用点分析完成。

## 已验证事实 / Verified facts
- SHA-256：`d2136f430029a8750c6c3280effdca0383e24b1f606e32d63e3b4154409b1038`；大小 321,880 字节。
- ELF64 x86-64 PIE 主程序，已 stripped；入口 `0xaa70`，Build ID `f7c40efb54a6d14e181145b6cfe0a43b888d04b4`。
- 缓解：PIE、NX、Full RELRO、Canary；未发现 RWX 段；扫描器报告 FORTIFY=False。
- 标准 Base64 字母表位于文件偏移 `0x31c20`，URL-safe 字母表位于 `0x31bc0`。
- 动态符号导入 `curl_easy_init`、`curl_easy_setopt`、`curl_easy_perform`，版本要求为 `CURL_OPENSSL_4`。
- `curl_easy_perform@plt` 调用点位于虚拟地址/PIE 相对偏移 `0x1d9a7`。

## 关键证据 / Key evidence
### 函数级深挖
- 函数名：`curl_easy_perform@plt`
- 调用点：`0x1d9a7`
- 参数来源：`rdi = *(r15 + 0x20)`；返回码保存到 `r12d`，随后传给 `sub_1ac30` 做结果处理。

近似反编译：
```c
CURL *easy = *(CURL **)(ctx + 0x20);
CURLcode rc = curl_easy_perform(easy);          // call-site 0x1d9a7
int post = sub_1ac30(state, ctx, rc, stack40, stack38);
if (flag_at_stack_68) goto special_path;
```

### 流水线原始输出
```text
$ python /home/user/ha-ha/scripts/auto_analyze.py /usr/bin/curl --out /home/user/case/curl-bin/auto/
[+] Analysis complete: /home/user/case/curl-bin/auto/auto_analysis.json
[+] Report: /home/user/case/curl-bin/auto/auto_analysis.md
[+] YARA rule: /home/user/case/curl-bin/auto/curl.yar
[exit=0]

$ python /home/user/ha-ha/scripts/find_crypto.py /usr/bin/curl --out /home/user/case/curl-bin/crypto/
[*] Scanning curl (321,880 bytes)...
[+] Found 2 crypto indicators
    Base64 encoding: Standard Base64 alphabet (high) @ 0x31c20
    Base64 encoding: URL-safe Base64 alphabet (high) @ 0x31bc0
[+] Found 1 crypto API imports
[+] Found 1 high-entropy regions (>= 7.0)
[+] Output: /home/user/case/curl-bin/crypto/crypto_scan.json, /home/user/case/curl-bin/crypto/crypto_scan.md
[exit=0]

$ python /home/user/ha-ha/scripts/elf_deep_scan.py /usr/bin/curl --out /home/user/case/curl-bin/elf/
[+] Output: /home/user/case/curl-bin/elf/elf_scan.json, /home/user/case/curl-bin/elf/elf_scan.md
[+] PIE=True NX=True RELRO=Full Canary=True FORTIFY=False
[exit=0]

$ python /home/user/ha-ha/scripts/yara_gen.py /usr/bin/curl --out /home/user/case/curl-bin/yara/
[*] Analyzing curl (321,880 bytes) — ELF executable
[*] Extracted 1927 ASCII + 0 Unicode strings
[*] Selected 15 strings for rule
[*] Extracted 4 byte patterns
[+] Generated rule: /home/user/case/curl-bin/yara/curl.yar
[+] Strings: 15, Hex patterns: 4
[exit=0]

$ python /home/user/ha-ha/scripts/rop_finder.py /usr/bin/curl --depth 5 --out /home/user/case/curl-bin/rop.txt
[*] Binary: curl (321,880 bytes)
[*] Architecture: x64
[*] Bad chars: 0x00
[*] Found 1 executable section(s)
[*] Found 0 raw gadgets ending in 'ret'
[*] Categorized 0 gadgets
    uncategorized: 0

[+] Saved to /home/user/case/curl-bin/rop.txt
[exit=0]

```

### 深挖原始输出
```text
$ readelf -Ws /usr/bin/curl | grep -E "curl_easy_(init|setopt|perform)"
    71: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_setopt@CURL_OPENSSL_4 (3)
    84: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_init@CURL_OPENSSL_4 (3)
    85: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND curl_easy_perform@CURL_OPENSSL_4 (3)

$ objdump -d -M intel /usr/bin/curl | grep -B8 -A12 "call.*curl_easy_perform@plt" | head -80
   1d986:	0f 85 46 04 00 00    	jne    1ddd2 <__cxa_finalize@plt+0x13562>
   1d98c:	48 83 7b 10 00       	cmp    QWORD PTR [rbx+0x10],0x0
   1d991:	74 10                	je     1d9a3 <__cxa_finalize@plt+0x13133>
   1d993:	e8 78 2f ff ff       	call   10910 <__cxa_finalize@plt+0x60a0>
   1d998:	41 89 c4             	mov    r12d,eax
   1d99b:	85 c0                	test   eax,eax
   1d99d:	0f 85 98 03 00 00    	jne    1dd3b <__cxa_finalize@plt+0x134cb>
   1d9a3:	49 8b 7f 20          	mov    rdi,QWORD PTR [r15+0x20]
   1d9a7:	e8 b4 cb fe ff       	call   a560 <curl_easy_perform@plt>
   1d9ac:	41 89 c4             	mov    r12d,eax
   1d9af:	4c 8b 44 24 38       	mov    r8,QWORD PTR [rsp+0x38]
   1d9b4:	48 8b 4c 24 40       	mov    rcx,QWORD PTR [rsp+0x40]
   1d9b9:	44 89 e2             	mov    edx,r12d
   1d9bc:	4c 89 fe             	mov    rsi,r15
   1d9bf:	48 89 df             	mov    rdi,rbx
   1d9c2:	e8 69 d2 ff ff       	call   1ac30 <__cxa_finalize@plt+0x103c0>
   1d9c7:	80 7c 24 68 00       	cmp    BYTE PTR [rsp+0x68],0x0
   1d9cc:	89 44 24 08          	mov    DWORD PTR [rsp+0x8],eax
   1d9d0:	0f 85 ca 01 00 00    	jne    1dba0 <__cxa_finalize@plt+0x13330>
   1d9d6:	8b 44 24 08          	mov    eax,DWORD PTR [rsp+0x8]
   1d9da:	83 f8 30             	cmp    eax,0x30

$ xxd -g1 -s 0x31bc0 -l 224 /usr/bin/curl
/bin/bash: line 9: xxd: command not found
```

## 推断与置信度 / Inference and confidence
- Base64 表用于 curl 自身的协议/认证编码，而非硬编码密钥：高置信度。
- `risk_hint=medium` 主要来自网络能力和高信号 API，不表示恶意：高置信度。
- FORTIFY=False 需谨慎解释；二进制仍具有其他主要缓解：中等置信度。

## 风险/漏洞候选 / Risk or vulnerability candidates
未发现可验证漏洞。Base64 常量、高熵只读区和网络 API 均符合 curl 的正常功能。

## 利用可行性 / Exploitability assessment
无已验证内存破坏原语；仅凭 gadget 或导入信息不能建立利用链。

## 建议下一步 / Suggested next steps
1. 安装 Ghidra 后恢复 stripped 内部函数边界和调用图。
2. 对 `0x1d9a7` 所在函数做参数语义恢复。
3. 将 YARA 规则限定到 Build ID/版本，避免把所有 curl 构建误报。

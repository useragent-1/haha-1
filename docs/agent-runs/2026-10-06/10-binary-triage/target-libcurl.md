# 目标报告：libcurl.so.4.8.0

## 当前阶段 / Current phase
共享库分诊、密码常量、ELF 深扫、导出符号与核心 easy-perform 路径分析完成。

## 已验证事实 / Verified facts
- SHA-256：`4fdc50a9c87bff66d16ca11c5f9f575239e72ee6081a1f36d7b819b97d69341f`；大小 983,720 字节。
- ELF64 x86-64 DYN 共享库，Build ID `5b0520a39ca973ec75be7eb4c02b481a44265041`。
- 缓解：PIE、NX、Full RELRO、Canary、FORTIFY；无 RWX 段。
- MD5 初始化向量位于文件偏移 `0xcae00`；Base64 URL-safe/standard 表位于 `0xcde00`/`0xcde60`。
- 导出 `curl_easy_perform@@CURL_OPENSSL_4` 位于 `0x376c0`，大小 9 字节，是跳转到 `0x37080` 的入口 thunk。

## 关键证据 / Key evidence
### 函数级深挖
- 导出函数：`curl_easy_perform@@CURL_OPENSSL_4`
- 导出偏移：`0x376c0`
- 实现入口：`0x37080`
- 关键行为：空句柄检查；清空错误缓冲/状态；取得或初始化 multi handle；调用 `curl_multi_setopt`、`curl_multi_add_handle`；失败时 cleanup 并映射返回码。

近似反编译：
```c
CURLcode curl_easy_perform(CURL *easy) {
    if (!easy) return CURLE_BAD_FUNCTION_ARGUMENT;       // 0x370a0
    if (easy->errorbuffer) easy->errorbuffer[0] = 0;
    easy->internal_status = 0;
    CURLM *multi = easy->multi;
    if (!multi) multi = internal_multi_init_or_reuse(easy);
    curl_multi_setopt(multi, 6, easy->option_a78);
    CURLMcode m = curl_multi_add_handle(multi, easy);     // 0x3714f
    if (m) { curl_multi_cleanup(multi); return map_multi_error(m); }
    return drive_transfer_loop(multi, easy);
}
```

MD5 IV 仅证明库内置 MD5 支持，可能服务于 Digest/NTLM 等兼容协议；不等于当前 TLS 使用 MD5。

### 流水线原始输出
```text
$ python /home/user/ha-ha/scripts/auto_analyze.py /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 --out /home/user/case/libcurl/auto/
[+] Analysis complete: /home/user/case/libcurl/auto/auto_analysis.json
[+] Report: /home/user/case/libcurl/auto/auto_analysis.md
[+] YARA rule: /home/user/case/libcurl/auto/libcurl.so.4.8.0.yar
[exit=0]

$ python /home/user/ha-ha/scripts/find_crypto.py /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 --out /home/user/case/libcurl/crypto/
[*] Scanning libcurl.so.4.8.0 (983,720 bytes)...
[+] Found 3 crypto indicators
    MD5: MD5 Initialization Vector (little-endian) (high) @ 0xcae00
    Base64 encoding: Standard Base64 alphabet (high) @ 0xcde60
    Base64 encoding: URL-safe Base64 alphabet (high) @ 0xcde00
[+] Found 3 crypto API imports
[+] Found 2 high-entropy regions (>= 7.0)
[+] Output: /home/user/case/libcurl/crypto/crypto_scan.json, /home/user/case/libcurl/crypto/crypto_scan.md
[exit=0]

$ python /home/user/ha-ha/scripts/elf_deep_scan.py /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 --out /home/user/case/libcurl/elf/
[+] Output: /home/user/case/libcurl/elf/elf_scan.json, /home/user/case/libcurl/elf/elf_scan.md
[+] PIE=True NX=True RELRO=Full Canary=True FORTIFY=True
[exit=0]

$ python /home/user/ha-ha/scripts/yara_gen.py /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 --out /home/user/case/libcurl/yara/
[*] Analyzing libcurl.so.4.8.0 (983,720 bytes) — ELF executable
[*] Extracted 4892 ASCII + 0 Unicode strings
[*] Selected 15 strings for rule
[*] Extracted 4 byte patterns
[+] Generated rule: /home/user/case/libcurl/yara/libcurl.so.4.8.yar
[+] Strings: 15, Hex patterns: 4
[exit=0]

$ python /home/user/ha-ha/scripts/rop_finder.py /usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0 --depth 5 --out /home/user/case/libcurl/rop.txt
[*] Binary: libcurl.so.4.8.0 (983,720 bytes)
[*] Architecture: x64
[*] Bad chars: 0x00
[*] Found 1 executable section(s)
[*] Found 0 raw gadgets ending in 'ret'
[*] Categorized 0 gadgets
    uncategorized: 0

[+] Saved to /home/user/case/libcurl/rop.txt
[exit=0]

```

### 深挖原始输出
```text
$ readelf -Ws libcurl.so.4.8.0 | grep curl_easy_perform
   616: 00000000000376c0     9 FUNC    GLOBAL DEFAULT   13 curl_easy_perform@@CURL_OPENSSL_4

$ objdump -d -M intel --start-address=0x376c0 --stop-address=0x376d0 libcurl.so.4.8.0

/usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0:     file format elf64-x86-64


Disassembly of section .text:

00000000000376c0 <curl_easy_perform@@CURL_OPENSSL_4>:
   376c0:	f3 0f 1e fa          	endbr64
   376c4:	e9 b7 f9 ff ff       	jmp    37080 <fwrite@plt+0x1f9e0>
   376c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

$ objdump -d -M intel --start-address=0x37080 --stop-address=0x37175 libcurl.so.4.8.0

/usr/lib/x86_64-linux-gnu/libcurl.so.4.8.0:     file format elf64-x86-64


Disassembly of section .text:

0000000000037080 <curl_global_init@@CURL_OPENSSL_4-0x350>:
   37080:	41 55                	push   r13
   37082:	41 54                	push   r12
   37084:	55                   	push   rbp
   37085:	53                   	push   rbx
   37086:	48 81 ec 68 01 00 00 	sub    rsp,0x168
   3708d:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
   37094:	00 00 
   37096:	48 89 84 24 58 01 00 	mov    QWORD PTR [rsp+0x158],rax
   3709d:	00 
   3709e:	31 c0                	xor    eax,eax
   370a0:	48 85 ff             	test   rdi,rdi
   370a3:	0f 84 17 03 00 00    	je     373c0 <fwrite@plt+0x1fd20>
   370a9:	48 8b 87 a0 01 00 00 	mov    rax,QWORD PTR [rdi+0x1a0]
   370b0:	48 89 fb             	mov    rbx,rdi
   370b3:	48 85 c0             	test   rax,rax
   370b6:	74 03                	je     370bb <fwrite@plt+0x1fa1b>
   370b8:	c6 00 00             	mov    BYTE PTR [rax],0x0
   370bb:	c7 83 bc 0c 00 00 00 	mov    DWORD PTR [rbx+0xcbc],0x0
   370c2:	00 00 00 
   370c5:	48 83 7b 68 00       	cmp    QWORD PTR [rbx+0x68],0x0
   370ca:	0f 85 e0 00 00 00    	jne    371b0 <fwrite@plt+0x1fb10>
   370d0:	48 83 7b 20 00       	cmp    QWORD PTR [rbx+0x20],0x0
   370d5:	74 39                	je     37110 <fwrite@plt+0x1fa70>
   370d7:	48 89 df             	mov    rdi,rbx
   370da:	e8 b1 1b 03 00       	call   68c90 <curl_multi_init@@CURL_OPENSSL_4+0x50>
   370df:	48 8d 74 24 08       	lea    rsi,[rsp+0x8]
   370e4:	48 89 df             	mov    rdi,rbx
   370e7:	e8 c4 2f ff ff       	call   2a0b0 <fwrite@plt+0x12a10>
   370ec:	83 f8 ff             	cmp    eax,0xffffffff
   370ef:	74 1f                	je     37110 <fwrite@plt+0x1fa70>
   370f1:	48 8b 74 24 08       	mov    rsi,QWORD PTR [rsp+0x8]
   370f6:	48 85 f6             	test   rsi,rsi
   370f9:	74 15                	je     37110 <fwrite@plt+0x1fa70>
   370fb:	ba 01 00 00 00       	mov    edx,0x1
   37100:	48 89 df             	mov    rdi,rbx
   37103:	e8 e8 fa fe ff       	call   26bf0 <fwrite@plt+0xf550>
   37108:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   3710f:	00 
   37110:	48 8b 6b 70          	mov    rbp,QWORD PTR [rbx+0x70]
   37114:	48 85 ed             	test   rbp,rbp
   37117:	0f 84 63 02 00 00    	je     37380 <fwrite@plt+0x1fce0>
   3711d:	41 bc 5d 00 00 00    	mov    r12d,0x5d
   37123:	f6 85 71 02 00 00 04 	test   BYTE PTR [rbp+0x271],0x4
   3712a:	75 54                	jne    37180 <fwrite@plt+0x1fae0>
   3712c:	8b 93 78 0a 00 00    	mov    edx,DWORD PTR [rbx+0xa78]
   37132:	be 06 00 00 00       	mov    esi,0x6
   37137:	48 89 ef             	mov    rdi,rbp
   3713a:	31 c0                	xor    eax,eax
   3713c:	e8 4f e9 fd ff       	call   15a90 <curl_multi_setopt@plt>
   37141:	48 c7 43 70 00 00 00 	mov    QWORD PTR [rbx+0x70],0x0
   37148:	00 
   37149:	48 89 de             	mov    rsi,rbx
   3714c:	48 89 ef             	mov    rdi,rbp
   3714f:	e8 5c e9 fd ff       	call   15ab0 <curl_multi_add_handle@plt>
   37154:	41 89 c4             	mov    r12d,eax
   37157:	85 c0                	test   eax,eax
   37159:	74 75                	je     371d0 <fwrite@plt+0x1fb30>
   3715b:	48 89 ef             	mov    rdi,rbp
   3715e:	e8 4d f5 fd ff       	call   166b0 <curl_multi_cleanup@plt>
   37163:	41 83 fc 03          	cmp    r12d,0x3
   37167:	0f 84 43 02 00 00    	je     373b0 <fwrite@plt+0x1fd10>
   3716d:	41 bc 02 00 00 00    	mov    r12d,0x2
   37173:	66                   	data16
   37174:	66                   	data16

$ xxd -g1 -s 0xcae00 -l 64 libcurl.so.4.8.0
/bin/bash: line 11: xxd: command not found
```

## 推断与置信度 / Inference and confidence
- `curl_easy_perform` 的同步接口内部由 multi 状态机驱动：高置信度。
- MD5 常量属于协议兼容功能而非硬编码密码：中高置信度。
- `risk_hint=medium` 是网络库功能画像，不是恶意评分：高置信度。

## 风险/漏洞候选 / Risk or vulnerability candidates
未发现漏洞。MD5 支持需要结合实际启用的认证协议评估，不能单独判定弱加密。

## 利用可行性 / Exploitability assessment
主要缓解全部开启；无崩溃、越界或控制流劫持证据。

## 建议下一步 / Suggested next steps
1. 用调试符号包恢复 `0x37080` 的内部真实函数名。
2. 对 MD5 常量做代码 xref，确定 Digest/NTLM 路径。
3. 对比当前 Debian 安全补丁源码与该 Build ID。

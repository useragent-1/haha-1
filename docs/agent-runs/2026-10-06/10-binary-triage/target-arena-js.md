# 目标报告：arena.ai 前端 JS chunk

## 当前阶段 / Current phase
在线下载、哈希固定、通用流水线、混淆指标、字符串/常量与模块级分析完成。

## 已验证事实 / Verified facts
- 来源 URL：`https://arena.ai/_next/static/chunks/01dtb792wrq6b.js?dpl=dpl_98jEkzzD1CGqfMjWnPXmVuNiVXNK`。
- SHA-256：`40b7cea49ff268560a1359154c62d644ae785e541b0775c1d5ad8cefe04dfddf`；大小 29,161 字节。
- Turbopack 压缩 chunk，共 26 个模块 ID；仅 3 行，最长行 29,111 字符，熵 5.3165。
- 未发现 `eval`、`new Function`、`atob`、WebAssembly、`crypto.subtle`、source map 或 Arena API 路径。
- 包含 React 运行时，版本字符串为 `19.3.0-experimental-3f0b9e61-20260317`；包含 PostHog chunk-ID 映射。

## 关键证据 / Key evidence
### 模块级深挖
- 模块：`70094`
- 模块起始文件偏移：`0x2d2d`
- 函数：压缩名 `o(e)`，函数起始 `0x2d5c`
- 常量 URL 偏移：`0x2d71`，值为 `https://react.dev/errors/`

近似反编译：
```js
function formatReactError(code, ...args) {
  let url = "https://react.dev/errors/" + code;
  for (const arg of args) url += (first ? "?" : "&") + "args[]=" + encodeURIComponent(arg);
  return `Minified React error #${code}; visit ${url} ...`;
}
```

该 chunk 是框架运行时而不是 Arena 业务/API chunk；`_posthogChunkIds` 在 `0xc1` 把当前 Error stack 映射到 chunk UUID `01a10e4a-efa9-7ce3-bd64-6dd91e841a3f`，用途更像遥测符号化，而非混淆。

### 流水线原始输出
```text
$ python /home/user/ha-ha/scripts/auto_analyze.py /home/user/case/arena-js/artifact/arena_chunk.js --out /home/user/case/arena-js/auto/
[+] Analysis complete: /home/user/case/arena-js/auto/auto_analysis.json
[+] Report: /home/user/case/arena-js/auto/auto_analysis.md
[+] YARA rule: /home/user/case/arena-js/auto/arena_chunk.js.yar
[exit=0]

$ python /home/user/ha-ha/scripts/find_crypto.py /home/user/case/arena-js/artifact/arena_chunk.js --out /home/user/case/arena-js/crypto/
[*] Scanning arena_chunk.js (29,161 bytes)...
[+] Found 0 crypto indicators
[+] Output: /home/user/case/arena-js/crypto/crypto_scan.json, /home/user/case/arena-js/crypto/crypto_scan.md
[exit=0]

$ python /home/user/ha-ha/scripts/yara_gen.py /home/user/case/arena-js/artifact/arena_chunk.js --out /home/user/case/arena-js/yara/
[*] Analyzing arena_chunk.js (29,161 bytes) — unknown (.js)
[*] Extracted 2 ASCII + 0 Unicode strings
[*] Selected 2 strings for rule
[*] Extracted 0 byte patterns
[+] Generated rule: /home/user/case/arena-js/yara/arena_chunk.yar
[+] Strings: 2, Hex patterns: 0
[exit=0]

$ python /home/user/ha-ha/scripts/shellcode_tools.py strings /home/user/case/arena-js/artifact/arena_chunk.js --obfuscated --ascii --min-len 4
Obfuscated string analysis for /home/user/case/arena-js/artifact/arena_chunk.js:
[exit=0]

```

### JS 深扫原始输出
```text
$ python /home/user/case/arena-js/js_deep_scan.py
file=/home/user/case/arena-js/artifact/arena_chunk.js
size=29161 entropy=5.3165 lines=3 max_line=29111
[urls] count=1
  https://react.dev/errors/
[api_paths] count=0
[module_ids] count=26
  112997
  199073
  502421
  675993
  926520
  624496
  70094
  530103
  588864
  481258
  580246
  29964
  602018
  612773
  770186
  404439
  514410
  391210
  843394
  724521
  894221
  461332
  721497
  732953
  680046
  780690
[uuid] count=1
  01a10e4a-efa9-7ce3-bd64-6dd91e841a3f
[obfuscation_and_runtime_indicators]
  eval(: 0
  new Function: 0
  atob(: 0
  btoa(: 0
  WebAssembly: 0
  crypto.subtle: 0
  _posthogChunkIds: 3
  TURBOPACK: 2
  sourceMappingURL: 0
  process.binding: 1
[context] needle=_posthogChunkIds offset=193 hex=0xc1
ry{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&(e._posthogChunkIds=e._posthogChunkIds||{},e._posthogChunkIds[n]="01a10e4a-efa9-7ce3-bd64-6dd91e841a3f")}catch(e){}}();(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,112997,(e,t,r)=>{var n={229:function(e){var t,r,n,o=e.exports={};function i(){throw Error("setTimeout has not been defined")}functio
[context] needle=https://react.dev/errors/ offset=11633 hex=0x2d71
==(t=r.ref)?t:null,props:r}}r.Fragment=o,r.jsx=u,r.jsxs=u},624496,(e,t,r)=>{"use strict";t.exports=e.r(926520)},70094,(e,t,r)=>{"use strict";var n=e.r(675993);function o(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var r=2;r<arguments.length;r++)t+="&args[]="+encodeURIComponent(arguments[r])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function i(){}var u=

$ xxd -g1 -s 0x0 -l 384 arena_chunk.js
/bin/bash: line 34: xxd: command not found

$ tail -c 160 arena_chunk.js
_=t;try{return e.apply(this,arguments)}finally{_=r}}}},780690,(e,t,r)=>{"use strict";t.exports=e.r(680046)}]);

//# chunkId=01a10e4a-efa9-7ce3-bd64-6dd91e841a3f```

## 推断与置信度 / Inference and confidence
- 该文件是 Next.js/Turbopack 框架运行时 chunk：高置信度。
- PostHog 片段用于 chunk/stack 关联遥测：中高置信度。
- 未发现业务端点不能推断站点没有 API；只说明所选 chunk 不含：高置信度。

## 风险/漏洞候选 / Risk or vulnerability candidates
未发现硬编码密钥、业务 API、动态代码执行或明显混淆。构建路径泄露 pnpm/Next 版本信息，影响较低。

## 利用可行性 / Exploitability assessment
没有可利用证据；React 错误 URL和模块 ID属于公开客户端代码。

## 建议下一步 / Suggested next steps
1. 从页面清单筛选更大的业务 chunk，再做端点/GraphQL/action ID 提取。
2. 增加 JS parser/beautifier（esprima、tree-sitter 或 prettier）。
3. 修复 YARA 字符串提取器对超长单行 JS 仅提取 2 条的问题。

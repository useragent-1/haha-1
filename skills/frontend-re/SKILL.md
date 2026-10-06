# frontend-re — 前端与 JavaScript 逆向

## 边界

只读分析自有、获授权或无需认证的公开页面；遵守站点条款和速率限制，不绕过登录、验证码或访问控制。凭据扫描只报告位置、类型、长度和 SHA-256 短指纹，不输出值。

## 端点发现

```bash
# 本地目录
python3 scripts/frontend/endpoint_discovery.py web/ -o endpoints.json
# 公开页面，只跟随同源 script，限制单响应 5MB/15秒
python3 scripts/frontend/endpoint_discovery.py https://example.org/ -o public-endpoints.json --follow-scripts
```

提取 HTTP(S)、WebSocket、域名、API path 和 Authorization 模式。动态拼接、运行时解密和跨源 chunk 需浏览器网络日志补证。

## Source map 恢复

```bash
python3 scripts/frontend/sourcemap_recover.py app.min.js -o recovered-map
```

定位 `sourceMappingURL`，支持本地、HTTP 和 data URI map，列出 sources，并将 `sourcesContent` 写到安全相对路径。不要把含私有源码的恢复目录上传到公共位置。

## 格式化与混淆结构

```bash
python3 scripts/frontend/beautify_compare.py app.min.js -o app.pretty.js --diff app.diff --analysis obfuscation.json
```

保存前后 SHA-256 和 unified diff，标记超长行、eval、Function 构造器、hex/unicode escape、数组轮转候选。词法格式化不保证语义等价。

## 前端敏感信息扫描

```bash
python3 scripts/frontend/secret_scan.py web/ -o secret-locations.json
```

仅输出文件、行列、类型、长度及 12 位 hash 指纹；公钥和内部地址是暴露面线索，不等于秘密或漏洞。

## 已知问题与限制

- 不运行真实浏览器，无法覆盖 Service Worker、WASM、DOM 事件、懒加载、加密 bundle 和运行时拼接。
- URL 正则会有误报；source map 可能缺失、跨源受限或超大。
- beautifier 是保守词法器，不替代 AST parser；模板字符串复杂表达式需人工核对。
- secret scan 可能漏掉拆分/编码值，也可能把测试常量误报；禁止根据发现自动使用凭据。
- 沙箱无图形界面，不做验证码、登录态或 DevTools GUI 自动化。

## 输出契约

记录 URL/文件 hash、抓取时间、HTTP 错误原文、来源行号、发现类型与限制。Authorization/Cookie/token 值一律打码；内部 ID 可保留。

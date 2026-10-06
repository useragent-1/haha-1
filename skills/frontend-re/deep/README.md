# frontend-re deep evidence

- `evidence/public/`：对无需认证的公开站点 `https://petstore3.swagger.io/` 只读抓取主页及 3 个同源脚本的端点发现结果；Authorization 仅保留 `[REDACTED expression]`。
- `evidence/fixtures/`：内联 source map 恢复、beautify/diff、混淆指标和位置-only 敏感信息扫描结果。
- source map 的 data URI 不写入报告，只保留 `[REDACTED sha256=…]`，避免把嵌入源码重复外传。

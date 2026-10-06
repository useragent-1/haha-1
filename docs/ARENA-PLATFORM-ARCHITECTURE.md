# Arena 平台架构分析（2026-10-06 实证）

> 本文档全部基于**实测证据**（浏览器会话抓包 + 服务端沙箱内部侦察 + 外部测绘），不含推测性描述。
> 复现方法见文末「复现清单」。

---

## 0. 一句话架构

```
Cloudflare（边缘/WAF）
   └─> Vercel（Next.js 应用 + API Routes）
         ├─> Trigger.dev（AI 会话编排 + 实时流）
         │      └─> E2B Firecracker microVM（沙箱执行）
         └─> 上游模型 API（Google Vertex / OpenAI / xAI / DeepSeek …）
```

**模型路由的决策逻辑运行在服务端（Vercel + Trigger.dev），客户端与沙箱内部均不可见。**

---

## 1. 路由层（客户端可见部分）

### 1.1 提交入口

`POST /nextjs-api/stream/create-chat`

```jsonc
{
  "message": { "id": "<uuid>", "role": "user", "parts": [{ "type": "text", "text": "..." }] },
  "recaptchaV3Token": "<grecaptcha.enterprise.execute 的结果>",
  "timezone": "Asia/Shanghai",
  "enabledConnectors": ["github"],   // 可选
  "modelId": "<uuid>",               // 可选：指定模型
  "harnessId": "pi"                  // 可选：仅当非 default 时发送
}
```

前端源码逻辑（chunk 10.js）证实字段构造方式：

```js
...(ez ? { modelId: ez } : {}),
...(eB && eG ? { modelId: eG } : {}),
...(eV && eW !== a.DEFAULT_SESSION_HARNESS ? { harnessId: eW } : {})
```

- `harness` 取值集合：`SESSION_HARNESS_IDS = ["default", "pi"]`，`DEFAULT_SESSION_HARNESS = "default"`
- `create-chat` 是 **POST-only**（GET 返回 405）

### 1.2 实时事件流

`GET /ai-proxy/realtime/v1/sessions/<sessionId>/out` → `text/event-stream`
（前端用 **fetch + ReadableStream** 读取，不是 EventSource）

SSE 帧结构：`event: batch` + `id: <seq 列表>` + `data: {"records":[{seq_num, timestamp, body}]}`

| 事件类型 | 实测条数 | 说明 |
|---|---|---|
| `reasoning-delta` | 84373 | 模型思考增量 |
| `tool-input-delta` | 37211 | 工具入参增量 |
| `text-delta` | 217 | 面向用户的文本输出 |
| `tool-output-available` | 29 | 工具执行结果 |
| `tool-input-start` / `tool-input-available` | 12 / 11 | 工具调用开始 / 参数就绪 |
| `reasoning-start` / `reasoning-end` | 10 / 10 | 思考段边界 |
| `start-step` / `finish-step` | 10 / 9 | 步骤边界 |
| `text-start` / `text-end` | 7 / 6 | 文本段边界 |
| `data-agent-dispatch` | 1 | 分发：inputId / attemptId / **providerRequestId** / browserAttemptId |
| `data-workspace-update` | 1 | 工作区变更（changes） |
| `directory` | 1 | 目录结构 |
| `start` | 1 | 消息开始（messageId + timing） |

**关键观察**：事件流中**不包含任何模型名称**（对 claude/gpt/gemini/deepseek/qwen/kimi/glm/grok/minimax/anthropic/openai 等 12 个关键词全文检索，命中 0）。

### 1.3 会话与工作区接口

| 接口 | 实测结果 |
|---|---|
| `GET /api/chat/<id>?paginated=true&includeStreamToken=false` | 200，返回消息数组 + `pinnedModel` 等元数据 |
| `GET /api/chat/<id>?includeStreamToken=true` | 400 ZodError：**只接受 false** |
| `GET /api/chat/<id>/preview` | 200 `{"registered":false,"sandboxState":"none","processes":[],"ports":[],...}` |
| `GET /api/chat/<id>/workspace/latest?includeManifest=true` | 200，文件清单；**小文件带 `inlineText`**，大文件只有 hash/size |
| `GET /api/me` | 401 未登录 / 200 已登录（最佳登录探针） |

会话元数据字段：`taskId: "chat-agent"`、`productMode: "chat"`、**`pinnedModel: null`**、`connectorsEnabled`、`rubricsEnabled`、`publicAccessToken`

### 1.4 模式路由（UI）

| 模式 | 说明 |
|---|---|
| Battle Mode | 两个匿名模型对战 |
| **Agent Mode** | 复杂任务（工具调用 + 沙箱执行） |
| Side by Side | 自选两个模型对比 |
| Direct | 单模型直连（`/direct`："Access Multiple Frontier AI Models"） |

---

## 2. 模型目录（路由表）

`GET /nextjs-api/model-catalog` → 151,684 字节，**6 个 arena 分组**：

| arena | 模型数 | 用途 |
|---|---|---|
| `text` | 128 | 通用文本 |
| `code` | 85 | 代码 |
| `document` | 128 | 文档理解 |
| `text-to-video` | 75 | 视频生成 |
| `text-to-image` | 41 | 图像生成 |
| `search` | 17 | 联网搜索 |

记录结构：

```jsonc
{
  "id": "019f19f2-41f1-7c6d-9891-48d02fd9952c",  // 前端 modelId 用的 UUID
  "organization": "anthropic",
  "provider": "googleVertexAnthropicAdaptive",     // 服务端上游通道
  "publicName": "claude-sonnet-5",
  "capabilities": { "inputCapabilities": {...}, "outputCapabilities": {"web": true} },
  "userSelectable": true,
  "rank": 18
}
```

**已观察到的 provider 通道**：`googleVertexGlobal`、`googleVertexGlobalWithThoughtSignatures`、`googleVertexAnthropicAdaptive`、`openaiResponses`、`xaiApi`、`xaiMultiAgent`、`alibaba`、`siliconFlowToolCalling`、`fireworks`、`minimaxAnthropic`、`deepseekVisionToolCalling`

完整快照：`references/arena/model-catalog.json`

---

## 3. 服务端外部测绘

| 层 | 实体 | 证据 |
|---|---|---|
| 边缘 | Cloudflare | `CF-RAY: …-LAX`、`cf_clearance`、`__cf_bm`、challenge 脚本 |
| 应用 | Vercel（Next.js） | `dpl_A2cQMbvEvX84BgirjQMmzpErK4mP`、`x-vercel-id: sfo1::` |
| 会话编排 | **Trigger.dev** | create-chat 响应返回 JWT：`iss=https://id.trigger.dev`、`aud=https://api.trigger.dev`、`taskId=chat-agent`、scopes `read/write:sessions:<id>`；CSP 含 `api.trigger.dev`；DNS TXT 含 trigger-dev 验证 |
| 认证 | Supabase 会话 cookie（`arena-auth-prod-*`，`base64-` 前缀 JSON）+ WorkOS | cookie 名演进：`v1.0`/`v1.1`（旧）→ `v1`（新）；TXT 含 work-os 验证 |
| 支付 | Stripe | TXT `stripe-verification` |
| 沙箱 | E2B（Firecracker） | 见第 4 节 |
| 状态页 | incident.io（`status.arena.ai`） | 公开组件仅 "Website" |
| 监控/分析 | Datadog RUM、PostHog、GA、reCAPTCHA Enterprise | CSP 白名单 |
| 邮件 | Google + Amazon SES | SPF：`v=spf1 include:_spf.google.com include:amazonses.com` |
| 证书 | Google Trust Services WE1 | `CN=arena.ai`，SAN：`arena.ai`、`mta-sts.everify.arena.ai`、`*.mta-sts.everify.arena.ai` |

### 3.1 子域实测（DNS-over-HTTPS 验证，规避 fake-ip 劫持）

| 存在 | NXDOMAIN |
|---|---|
| `www`、`agent`（301 → /agent）、`cdn`、`help`、`status`、`indexable`、`gateway`（NOERROR 无 A 记录）、`mta-sts.everify` | `api`、`ai-proxy`、`backend`、`internal`、`admin`、`staging`、`dev`、`llm`、`router`、`proxy`、`ws`、`mcp`、`console`、`agents` |

**结论：没有独立 API 子域**，所有 API 在主域路径下。

### 3.2 端点探测表

⚠️ 该站对未知路径返回 **200 + 软 404 页面**，必须按内容判定，不能只看状态码。

| 路径 | 状态 | 判定 |
|---|---|---|
| `/api/me` | 401 / 200 | 真实端点（登录探针） |
| `/api/health` | 403 | 存在但受限 |
| `/api/agent/config` | 403 | 存在但受限 |
| `/nextjs-api/stream/create-chat` | GET 405 / POST 200 | POST-only |
| `/nextjs-api/sign-in/email` | 400 `Email and password are required` | 存在 |
| `/nextjs-api/sign-up/magic-link` | 400 `User already exists, try login by email and password.` | 存在（仅注册用） |
| `/nextjs-api/reset-password/request` | 200 | 存在 |
| `/nextjs-api/sign-out` | 307 → `/`，清除 `coding_gh_token` | 存在 |
| `/ai-proxy/realtime/v1/sessions/<id>/out` | 200 `text/event-stream` | SSE 通道 |
| `/health`、`/.well-known/openid-configuration` | 200（内容为软 404） | 不存在 |

### 3.3 第三方集成指纹（DNS TXT）

work-os / linear / cursor / **anthropic** / uber / manus / zapier / stripe / trigger-dev / google / docker / airtable / figma / wiz / rippling / pylon / zoom / slack / 1password / canva / **perplexity-ai** / sprout-social / jumpdesktop / amazon-business / arena 自身验证记录。

> 说明：这些是 TXT 中的域名验证记录，反映其 SaaS 栈与外部集成，**不等同于商业合作关系**。

---

## 4. 沙箱层（agent 内部侦察实证）

| 项 | 值 |
|---|---|
| 沙箱提供方 | **E2B**（`E2B_SANDBOX=true`、`E2B_SANDBOX_ID=i7cyophzmk881wpihz4o7`、`E2B_TEMPLATE_ID=nlhz8vlwyupq845jsdg9`） |
| 虚拟化 | **KVM + Firecracker**（`Hypervisor detected: KVM`；`envd --help` 含 `-isnotfc  run outside of Firecracker`；内核参数 virtio_mmio） |
| 系统 | Debian 13 (trixie)，内核 `6.1.158+`，主机名 `e2b.local` |
| 网络 | eth0 `169.254.0.21/30`，网关 `169.254.0.22`，DNS `8.8.8.8`；`192.0.2.1 = events.e2b.local` |
| 权限 | `user` 在 sudo 组，**免密 sudo**（`sudo -n true` → 0） |
| 控制守护 | **envd 0.6.10**（PID 359，root，端口 **49983**，`/usr/bin/envd` 无额外参数） |
| envd 鉴权 | `401 {"message":"unauthorized access, please provide a valid access token or method signing if supported"}`；`/health` → 204 免鉴权；其余端点全 401 |
| 代码解释器 | **Jupyter Server / TornadoServer 6.5.7**（8888），`/metrics` 暴露 Prometheus 指标 |
| 平台服务 | `envd.service`、`code-interpreter.service`、`jupyter.service`、`ssh.service`、NFS/RPC |
| 编排网对端 | `10.12.0.x`（**每次任务动态分配**：实测见过 .78/.104/.124/.186），全部归属 envd 进程 |
| 事件网关 | `http://192.0.2.1:80` → `{"error":"no matching operation was found"}`（按操作路由的 HTTP 服务） |
| 出口 | **无代理变量、无 iptables NAT**（filter/nat 表空）；`/usr/local/share/ca-certificates/e2b-ca.crt`（`O=E2B, CN=E2B Proxy CA`，595B）⇒ 出口 TLS 由平台透明代理 MITM |
| arena 执行器 | `/root/.server/`（Python 3.13：`main.py` / `stream.py` / `messaging.py` / `envs.py` / `contexts.py` + `.venv`） |
| 隔离特征 | KASLR disabled；无 DMI；单会话独立工作区（不同任务的 `/tmp/arena-workspace` 互不可见） |

### 4.1 工作区持久化机制（沙箱内实测验证，2026-10-06）

**结论：`/home/user` 下的普通文件跨轮次自动持久化，零凭据。** 这使「记忆闭环」无需任何 token。

**三阶段机制**：

| 阶段 | 产物 | 说明 |
|---|---|---|
| 运行中 | `baseline.json` | 当前基线快照，每项含 `hash`(sha256-b64url) / `size` / `mtimeNs` |
| 收工时 | `changes.json` + 内容包 | 增量清单：`files` / `deletedPaths` / `omittedPaths` / `preOmissionFileCount` / `preOmissionSizeBytes` |
| 下轮启动 | `hydrate.zip` | 平台据此**恢复工作区文件**，随后写入新的 `baseline.json` |

**活动轮次的实际文件清单**：`['baseline-input.json', 'baseline.json', 'hydrate.zip']`
（`changes.json` 在活动轮次中**不存在**——它只在收工时短暂生成，这解释了此前"changes.json 时有时无"的观测）

**验证方法（三方 hash 对照，可复用）**：
```bash
sha256sum MEMORY_UPDATE.md                      # 1. 当前文件 hex 摘要
python3 -c "import hashlib,base64,sys;d=open('MEMORY_UPDATE.md','rb').read();print(base64.urlsafe_b64encode(hashlib.sha256(d).digest()).rstrip(b'=').decode())"   # 2. 转 base64url
# 3. 与 /tmp/arena-workspace/baseline.json 中同文件条目的 hash 字段比对
python3 -c "import json;b=json.load(open('/tmp/arena-workspace/baseline.json'));print(b['root']['entries']['MEMORY_UPDATE.md'])" 2>/dev/null \
  || python3 -c "import json;b=json.load(open('/tmp/arena-workspace/baseline.json'));print([v for k,v in b.get('files',b).items() if 'MEMORY' in k])"
```
三者一致 ⇒ 文件已被平台纳入持久化基线。

**实测已验证可同步的文件**：`SKILL.md`、`SKILLS.md`、`MEMORY.md`、`MEMORY_UPDATE.md`、`skills/*/SKILL.md`
（hash 全部 baseline 匹配）

**限制（必须预知）**：

| 限制 | 影响 |
|---|---|
| 快照上限约 **128 MB / 10,000 文件** | 技能库保持小型文本+脚本即可；大二进制/数据集不适用 |
| 不保证同步：`.git/config`、凭据路径 | Git remote 与 token 每次都要重新配 |
| 不保证同步：`node_modules`、`.venv`、缓存、构建目录 | 依赖需每轮重装（`bash scripts/setup.sh` 约 30 秒） |
| 收工时才生成 changes | 轮次中途进程被杀 = 未生成快照 = 该轮产出丢失 |

**开工/收工仪式（写入 MEMORY.md 顶部）**：
- 开工：`ls /home/user/ha-ha` 判断库是否已 hydrate → 缺则 clone → **无论有无都跑一次 `bash scripts/setup.sh`** 验依赖
- 收工：把结论写入 `MEMORY_UPDATE.md`（工作区根目录）→ 平台自动持久化，无需 token

---

## 5. 关键实验记录

### 实验 A：能否强制指定模型路由

| 请求 | 结果 |
|---|---|
| 不带 `modelId` | **200**，会话创建成功，返回 Trigger.dev JWT |
| 带**无效** modelId（全零 UUID） | **403 `{"error":"Not allowed"}`** |
| 带**有效** modelId（claude-sonnet-5 真实 UUID） | **403 `{"error":"Not allowed"}`** |

**结论**：对照组证明 reCAPTCHA token 有效、请求格式正确 ⇒ 403 由 `modelId` 字段触发。
**服务端只放行官方 UI 的模型选择流程**；合法路径是 Direct / Side-by-Side 模式（UI 选模型）。

### 实验 B：reCAPTCHA 约束

- sitekey：`6LeTGMcsAAAAALuIlkVwIxaAuZA8VledA6d3Nnb0`（reCAPTCHA **Enterprise**）
- token 由前端 `grecaptcha.enterprise.execute(sitekey, {action})` 获取，action 由调用方动态传入
- 登录类端点（sign-in / reset-password）**不需要** recaptcha

### 实验 C：登录机制

- 账号体系：Supabase（GoTrue）+ PKCE recovery 流程（`auth.arena.ai/auth/v1/verify?token=pkce_…&type=recovery&redirect_to=…`）
- 已存在账号**只能用邮箱+密码登录**，magic-link 仅用于注册
- 会话 cookie 会在使用中轮换（旧 refresh token 一次性），自动化脚本需具备重新提取能力

---

## 6. 结论：可控与不可控

| 层 | 可控性 | 说明 |
|---|---|---|
| 客户端请求参数 | ✅ 完全可控 | message / modelId / harnessId / timezone / connectors |
| 模型选择 | ⚠️ 受限 | 仅官方 UI 流程；裸请求 403 |
| SSE 事件流 | ✅ 可完整读取 | 含思考、工具调用、workspace 变更 |
| 沙箱内执行 | ✅ 完全可控 | bash / 文件 / 网络，**且有免密 sudo** |
| 沙箱→平台 | ❌ 单向 | envd 有 token 鉴权；平台对沙箱是单向控制 |
| 服务端路由决策 | ❌ 黑盒 | 运行在 Vercel/Trigger.dev，源码与数据库不可达 |
| 模型本体 | ❌ 不归平台所有 | 上游供应商 API |

---

## 7. 复现清单（如何自行验证）

```bash
# 1) 模型目录
curl -s https://arena.ai/nextjs-api/model-catalog | head -c 2000

# 2) SSE 事件流（需登录态）
curl -N -s https://arena.ai/ai-proxy/realtime/v1/sessions/<sessionId>/out

# 3) 端点存在性（注意软 404）
for p in /api/me /api/health /nextjs-api/sign-in/email /ai-proxy/v1/models; do
  echo "$p -> $(curl -s -o /dev/null -w '%{http_code}' https://arena.ai$p)"
done

# 4) 证书
openssl s_client -connect arena.ai:443 -servername arena.ai </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -ext subjectAltName

# 5) 子域（DoH，规避本地 fake-ip）
curl -s "https://dns.google/resolve?name=api.arena.ai&type=A" | jq -r '.Status'
```

---

## 8. 证据合规声明

- 本文所有端点、字段、事件类型均来自**实际请求/响应**记录
- 服务端隐藏的信息（模型名、路由算法、额度策略）标记为"不可见"，未做猜测
- 沙箱内部结论来自 agent 在其自身环境内的命令输出（原始文件见 arena 工作区）
- 未执行任何越权访问、绕过鉴权或破坏性操作

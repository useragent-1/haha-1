# CLEANUP_REPORT

## 扫描范围

- `/home/user/push-tmp` 全部文件及 Git 元数据；
- `/home/user/FULL_CLI_TOOLCHAIN_REPORT.md`；
- 初检文件数：589。

## 扫描规则

- 凭据：token/secret/password/api key/Authorization/Bearer/Cookie 的值形态，以及 `ghp_`、`sk-`、`AKIA`、PEM private key。文档中的纯字段名/正则定义也被检查，但只有携带值的命中才按凭据文件处理。
- 内部信息：RFC1918 地址、E2B sandbox/template ID、session/instance ID 的赋值形态。
- 环境快照：含 `env | sort` 标记且伴随 `NAME=value` 输出行。

## 初检结果

| 类别 | 命中 | 处理 |
|---|---:|---|
| 凭据值形态 | 16 处，涉及 8 个文件 | 整个文件移出仓库至隔离目录 |
| 内部 IP/实例标识 | 初检 61 处；其中 58 处涉及 19 个保留文件，另 3 处随凭据文件隔离 | 保留文件原值替换为 `[REDACTED:末4位]` |
| 环境快照 | 3 个文件，共 116 行 | 删除值，仅保留变量名 |

## 凭据类文件处理（不展示命中值）

- `docs/ARENA-PLATFORM-ARCHITECTURE.md` → 整文件移至仓库外隔离区；原文件 SHA-256 `be834d8963e8a5b46f2e707693807fd403e117a11e9d5230a32960dba83a1405`。
- `skills/protocol-re/deep/evidence/mixed.pcap` → 整文件移至仓库外隔离区；原文件 SHA-256 `51af46bf9b3b6c6fd5dbe4d660a97101beeb342720e41d4ae580f784800d567b`。
- `tools/scripts/net/unicornscan/etc/modules.conf` → 整文件移至仓库外隔离区；原文件 SHA-256 `0545d36c8596bd7bfc564e1af89decddaae66ccc4e64972b8e5db7d0b90df3f5`。
- `tools/scripts/net/unicornscan/src/output_modules/database/attic/mysqldb.c` → 整文件移至仓库外隔离区；原文件 SHA-256 `6b2b48123d0578477e3e2b870bedaea9f185af9cfab54311c5875b35f46f56d1`。
- `tools/scripts/net/unicornscan/src/tools/fpdb.c` → 整文件移至仓库外隔离区；原文件 SHA-256 `1e960acd4fc034abba7a132060e9e013900f18fad2a5017c71155f8d39af643d`。
- `tools/scripts/net/unicornscan/www-front-end/lib/connect_todb.php` → 整文件移至仓库外隔离区；原文件 SHA-256 `bf25db2d7250a6918ea929f47c20711271e71f31f12080e274864944384fb590`。
- `tools/scripts/net/unicornscan/www-front-end/lib/pgsqldbclass.php` → 整文件移至仓库外隔离区；原文件 SHA-256 `d0dca230afdae1dc8635409df222d93640cc2ae06f648082de0f1c36ac968fe2`。
- `tools/scripts/net/unicornscan/www-front-end/lib/session_handler.php` → 整文件移至仓库外隔离区；原文件 SHA-256 `2306143db7cdfebcdd7677b638818cb0c40938a8ef2b087c4713638e541016b3`。

## 内部信息处理（不展示原值）

- `references/exploit-development.md` → 末4位保留式打码（rfc1918×2）。
- `references/network-re.md` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/README.database` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/etc/unicorn.conf.in` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/ext_src/demo.c` → 末4位保留式打码（rfc1918×12）。
- `tools/scripts/net/unicornscan/src/getconfig.c` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/src/tools/fantaip.c` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/src/parse/example_confs/cruel.conf` → 末4位保留式打码（rfc1918×1）。
- `tools/scripts/net/unicornscan/src/parse/example_confs/example.conf` → 末4位保留式打码（rfc1918×1）。
- `skills/binary-triage/SKILL.md` → 末4位保留式打码（session-id×1）。
- `skills/desktop-app-recon/SKILL.md` → 末4位保留式打码（session-id×1）。
- `skills/sandbox-recon/SKILL.md` → 末4位保留式打码（session-id×1）。
- `skills/sandbox-recon/deep/validated-sandbox-findings.md` → 末4位保留式打码（rfc1918×5, E2B_SANDBOX_ID×1, E2B_TEMPLATE_ID×1）。
- `docs/agent-runs/2026-10-06/00-sandbox-recon/full-report.md` → 末4位保留式打码（rfc1918×5, E2B_SANDBOX_ID×1, E2B_TEMPLATE_ID×1）。
- `docs/agent-runs/2026-10-06/00-sandbox-recon/round-1.md` → 末4位保留式打码（E2B_SANDBOX_ID×1, E2B_TEMPLATE_ID×1）。
- `docs/agent-runs/2026-10-06/00-sandbox-recon/round-2.md` → 末4位保留式打码（rfc1918×5）。
- `docs/agent-runs/2026-10-06/00-sandbox-recon/round-3.md` → 末4位保留式打码（rfc1918×11）。
- `docs/agent-runs/2026-10-06/10-binary-triage/master-report.md` → 末4位保留式打码（rfc1918×1）。
- `docs/agent-runs/2026-10-06/10-binary-triage/target-socat-mux.md` → 末4位保留式打码（rfc1918×1）。

## 环境快照处理

- `docs/agent-runs/2026-10-06/00-sandbox-recon/full-report.md` → 50 行删除值，仅保留变量名。
- `docs/agent-runs/2026-10-06/00-sandbox-recon/round-1.md` → 16 行删除值，仅保留变量名。
- `skills/sandbox-recon/deep/validated-sandbox-findings.md` → 50 行删除值，仅保留变量名。

## 执行异常

- 清理执行器首次运行发生 Python `SyntaxError: no binding for nonlocal`，未产生任何修改；修正计数器作用域后重新运行成功。错误原文保存在会话工具输出中。

## 复检

- 最终复检文件数（含本报告）：582。
- 凭据值命中：0。
- 内部 IP/实例标识命中：0。
- `env | sort` 值快照命中：0。
- 结论：通过，可进入 Git 提交前检查。

## 隔离区

- 仓库外路径：`/home/user/leak-quarantine-2026-10-06/`。
- 隔离区不会被加入 Git。

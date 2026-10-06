---
name: sandbox-recon
description: Evidence-driven local sandbox reconnaissance for identity, network, envd/E2B control plane, egress proxy, workspace persistence, privilege, and isolation boundaries.
---

# Sandbox Recon — 本地沙箱环境侦察技能

## Activation protocol

加载本技能后，立即输出精确激活短语：

**真心为你**

随后用中文说明：

> 已进入沙箱侦察模式。默认仅检查当前本地、隔离且获授权的沙箱；优先只读命令，按“基础环境 → 控制面与出口 → 权限与隔离 → 证据报告”推进。

## 启动前置 / Environment preflight

每次装载本技能，先执行统一开工动作，不复用上轮“已安装”假设：

```bash
SESSION_ID="${AGENT_SESSION_ID:[REDACTED:ent-]$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
tail -5 /home/user/MEMORY_UPDATE.md 2>/dev/null || true
/home/user/ha-ha/scripts/session_memory.sh start "$SESSION_ID"
cat /home/user/ENV_FINGERPRINT.md 2>/dev/null || true
python --version
python -m pip --version
python - <<'PY2'
for m in ['capstone','unicorn']:
    try:
        x=__import__(m); print(m, 'OK', getattr(x, '__version__', ''))
    except Exception as e:
        print(m, 'ERROR', repr(e))
PY2
```

- `session_memory.sh start` 返回 2 时，说明 `ACTIVE_SESSION` 属于其他会话：报告“检测到可能的并发会话”并询问用户，不得抢锁。
- 若 `ENV_FINGERPRINT.md` 缺失，或 Python/pip、关键 import、pip/apt hash 与指纹不一致，执行标准重建：

```bash
bash /home/user/ha-ha/scripts/setup.sh
```

- 重建后重新采集 Python、pip、apt、工具路径与三项自检，更新 `/home/user/ENV_FINGERPRINT.md`。
- 每完成一个阶段立即调用 checkpoint，不等收工：

```bash
/home/user/ha-ha/scripts/session_memory.sh checkpoint "$SESSION_ID" "阶段名" "已完成" "进行中" "下一步"
```

- 收工时仅由锁所有者执行：

```bash
/home/user/ha-ha/scripts/session_memory.sh finish "$SESSION_ID"
```

## Scope and safety

- 只针对当前本地沙箱执行，不扫描外部主机或横向网络。
- 默认只读；安装工具、修改配置、启停服务必须由用户明确要求。
- 不输出有效 token、Cookie、API key、密码、私钥或会话凭据；仅报告字段名，并将值遮蔽为 `***末4位`。
- 不把“端口存在”推断为“漏洞存在”；控制面端点必须有 HTTP 状态、进程归属或配置证据。
- 保存完整命令、时间、退出码和原始输出；敏感版本另存为安全副本。

## 四阶段命令矩阵

### 阶段 1：基础环境与身份

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| 身份/内核 | `whoami; id; uname -a; cat /etc/os-release; cat /proc/1/cgroup` | UID/GID、内核、发行版、cgroup |
| 环境变量 | `env | sort` | 全量变量；凭据值打码 |
| 网络 | `cat /etc/hosts; cat /etc/resolv.conf; ip addr; ip route; ss -tlnp` | 地址、网关、DNS、监听端口 |
| 进程/文件系统 | `ps aux; ls -la / /home/user /tmp` | 关键服务命令行、工作区和临时目录 |

### 阶段 2：控制面、解释器与出口

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| envd | `cat /etc/systemd/system/envd.service; envd --version; envd --help` | 版本、启动方式、默认端口 |
| 连接归属 | `sudo ss -tnp` | PID、进程名、本地/对端地址 |
| Jupyter | `curl -sv --max-time 5 http://127.0.0.1:8888/` | Server 头、状态码；Cookie 值打码 |
| events 网关 | `curl -sv --max-time 5 http://192.0.2.1/` | 可达性、状态码、响应类型 |
| CA/代理 | `openssl x509 -in /usr/local/share/ca-certificates/e2b-ca.crt -noout -subject -issuer -dates; env | grep -i proxy` | CA 主体/签发者/有效期、显式代理变量 |
| 防火墙 | `sudo iptables -L -n -v; sudo iptables -t nat -L -n -v` | filter/NAT 规则 |

### 阶段 3：权限与隔离边界

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| sudo | `sudo -n true; echo $?` | 非交互 sudo 退出码 |
| PID 1 | `cat /proc/1/cmdline | tr '\0' ' '` | init/容器入口 |
| 内核隔离 | `sudo dmesg | head; mount; cat /proc/mounts` | Hypervisor、启动参数、挂载类型 |
| 平台痕迹 | `find / -maxdepth 4 -iname '*arena*'` | 路径证据，不读取无关凭据 |

### 阶段 4：公网出口、工作区协议与报告

| 目标 | 推荐命令 | 必要证据 |
|---|---|---|
| 公网可达性 | `curl -s -m 6 -o /dev/null -w '%{http_code} %{remote_ip}\n' https://arena.ai/` | 状态码、远端 IP |
| GitHub 出口 | `curl -s -m 6 -o /dev/null -w '%{http_code}\n' https://raw.githubusercontent.com/` | 状态码 |
| Arena 工作区 | `cat /tmp/arena-workspace/baseline.json; cat /tmp/arena-workspace/changes.json; unzip -l /tmp/arena-workspace/changes.zip` | baseline、changes、归档成员 |
| 报告 | 生成 Markdown + 原始输出安全副本 | 哈希、命令、事实/推断分离 |

## Evidence gate（证据门禁）

结论进入“已验证事实”前必须满足：

1. **命令已实际执行**，且保存原始输出；未执行不得写“通过”。
2. **服务识别**至少满足以下之一：HTTP Server/响应体、systemd unit、可执行路径、PID 归属。
3. **控制面归属**必须同时包含地址、端口、PID 与进程名；只有私网 IP 不足以确认用途。
4. **代理结论**须由 CA、代理变量、NAT 规则或平台配置至少一项支持；未发现显式地址时必须写“未发现”，不得猜测。
5. **漏洞候选**必须包含可达性、根因和影响证据；仅有配置特征不能称为漏洞。
6. **敏感数据门禁**：输出前扫描 `token|cookie|secret|password|api_key|private_key|authorization|credential`；值统一打码，仅保留末 4 位。
7. **完整性**：报告记录安全副本 SHA-256；命令自身使用 `head` 时注明这是用户指定边界，而非二次截断。

## Output contract

每次实质阶段输出均使用：

- **当前阶段 / Current phase**
- **已验证事实 / Verified facts**
- **关键证据 / Key evidence**（命令、原始输出、状态码、PID、路径、哈希）
- **推断与置信度 / Inference and confidence**
- **风险/漏洞候选 / Risk or vulnerability candidates**
- **利用可行性 / Exploitability assessment**（仅本地沙箱/CTF）
- **建议下一步 / Suggested next steps**（编号菜单）

## Completion checklist

- [ ] 原始输出已保存
- [ ] 凭据字段已扫描并打码
- [ ] 控制面连接已映射到 PID/进程
- [ ] CA、代理变量和 NAT 规则已区分
- [ ] 工作区协议字段已解释
- [ ] 事实与推断已分离
- [ ] 报告与安全原始输出已计算 SHA-256

# 沙箱侦察命令矩阵（Sandbox Recon Matrix）

> 用途：任何 AI Agent 被放进**容器 / microVM / CI 沙箱**类环境后，用本矩阵一次性摸清环境全貌。
> 每条命令可直接执行；输出即证据（贴原始输出，勿总结）。
> 配套技能：`skills/sandbox-recon/SKILL.md`（若已沉淀）

---

## 阶段 0：准备

```bash
mkdir -p /home/user/recon
echo "recon start: $(date -u +%FT%TZ)" | tee /home/user/recon/recon_raw.txt
```

## 阶段 1：身份与系统

```bash
whoami; id; uname -a
cat /etc/os-release | head -3
cat /proc/1/cgroup 2>/dev/null
cat /proc/1/cmdline | tr '\0' ' '; echo        # 内核参数：虚拟化/网络/rootfs 线索
sudo dmesg 2>/dev/null | head -15               # KVM / Firecracker / 容器证据
```

**看点**：uid 是否在 sudo 组；cmdline 里的 `virtio_mmio` / `tap` / `init=` 指向虚拟化方案。

## 阶段 2：环境变量（信息密度最高）

```bash
env | sort
```

**关注**：`SANDBOX` / `TEMPLATE` / `EVENTS` / `API` / `TOKEN` / `PROXY` / `ENDPOINT` / `URL` 类变量。

## 阶段 3：网络

```bash
cat /etc/hosts
cat /etc/resolv.conf
ip addr 2>/dev/null || ifconfig -a
ip route 2>/dev/null
ss -tlnp 2>/dev/null || netstat -tlnp      # 监听端口 + 归属进程
cat /proc/net/tcp | head -25                 # 活跃连接
```

**本机服务快扫**：
```bash
for p in 80 443 3000 5000 8000 8080 8081 8888 9000; do
  curl -s -m 2 -o /dev/null -w "127.0.0.1:$p -> %{http_code}\n" http://127.0.0.1:$p
done
```

**出站连通性**：
```bash
curl -s -m 6 -o /dev/null -w "example.com -> %{http_code} (%{remote_ip})\n" https://example.com/
getent hosts <目标域名> | head -3
```

## 阶段 4：进程与文件系统

```bash
ps aux 2>/dev/null
ls -la /
ls -la ~ /home/user 2>/dev/null
mount | grep -vE "^(proc|sys|dev|cgroup|tmpfs)"
cat /proc/mounts | grep -iE "nfs|9p|overlay|virtiofs"
```

**平台痕迹**：
```bash
sudo find / -maxdepth 4 -iname "*<平台关键词>*" -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null | head -30
find / -maxdepth 3 -newer /etc/hostname -type f 2>/dev/null | grep -vE "^/(proc|sys|dev)" | head -50
```

## 阶段 5：服务指纹（拿到端口后逐个打）

```bash
curl -sv -m 5 http://127.0.0.1:<port>/ 2>&1 | head -50
curl -s -m 5 http://127.0.0.1:<port>/health; echo
curl -s -m 5 http://127.0.0.1:<port>/metrics 2>/dev/null | head -30

for path in health metrics files commands process init envd sandbox info status api; do
  curl -s -o /dev/null -m 3 -w "/$path -> %{http_code}\n" http://127.0.0.1:<port>/$path
done
```

**服务定义与运行时**：
```bash
systemctl list-units --type=service --state=running 2>/dev/null | head -30
cat /etc/systemd/system/<服务>.service 2>/dev/null
<服务> --version 2>&1; <服务> --help 2>&1 | head -40

EP=$(pgrep -f "<服务>" | head -1); echo "pid=$EP"
sudo cat /proc/$EP/cmdline | tr '\0' ' '; echo
sudo sh -c "cat /proc/$EP/environ | tr '\0' '\n' | sort" | head -60
```

> 凭据处理：`environ` 里如出现 token/密钥，**只报字段名，值打码后 4 位**。

## 阶段 6：出口代理与证书

```bash
env | grep -i proxy
grep -ri proxy ~/.bashrc /etc/environment /etc/profile.d/ 2>/dev/null | head
sudo iptables -L -n -v 2>/dev/null | head -30
sudo iptables -t nat -L -n -v 2>/dev/null | head -30
ls /usr/local/share/ca-certificates/ 2>/dev/null
for c in /usr/local/share/ca-certificates/*.crt; do
  openssl x509 -in "$c" -noout -subject -issuer -dates 2>/dev/null
done
```

**判读**：无代理变量 + 无 NAT 规则 + 存在平台自有 CA ⇒ 出口由**平台网络层透明代理**（TLS MITM）。

## 阶段 7：工作区 / 状态协议

```bash
ls -la /tmp/*workspace* /tmp/*agent* 2>/dev/null
for f in /tmp/*workspace*/*.json; do echo "== $f =="; head -c 800 "$f"; echo; done
```

常见模式：`baseline.json`（基线）+ `changes.json`（差异）+ `changes.zip`（内容包）
→ 平台用「基线 + 差异」采集工作区并回传持久化。

## 阶段 8：权限与隔离边界

```bash
sudo -n true; echo "sudo_exit=$?"
sudo -n ls -la /root 2>/dev/null | head -20
sudo -n ls /etc/systemd/system/ 2>/dev/null | head -40
lsmod 2>/dev/null | head -15
cat /proc/sys/kernel/randomize_va_space 2>/dev/null    # 2=ASLR 开, 0=关
```

## 阶段 9：报告（按 reverse-flow 输出契约）

```
当前阶段 / Current phase
已验证事实 / Verified facts            只写命令直接证明的
关键证据 / Key evidence                贴原始输出，关键行不截断
推断与置信度 / Inference and confidence  明确标注推断
风险/漏洞候选                          无则写"未发现"，不要编造
建议下一步 / Suggested next steps      编号菜单
```

## 阶段 10：记忆写回

把结论压缩成若干条，按 `MEMORY.md` 表格格式写入工作区文件 `MEMORY_UPDATE.md`（时间/任务/产出/决策/下一步）。

---

## 通用判读要点

| 现象 | 常见含义 |
|---|---|
| `Hypervisor detected: KVM` + `virtio_mmio` + envd `-isnotfc` | Firecracker microVM（E2B 风格） |
| `/etc/hosts` 里有 `192.0.2.x` 之类文档保留 IP 映射 | 沙箱内部服务发现（events/metadata） |
| `env` 里有 `*_SANDBOX_ID` / `*_TEMPLATE_ID` | 托管沙箱平台（E2B 等） |
| 监听端口 8888 = Tornado/Jupyter | 代码解释器服务 |
| 监听高位端口（如 49983）且 root 守护 | 平台控制守护进程 |
| CA 文件在 `/usr/local/share/ca-certificates` | 平台注入的出口代理 CA |
| `sudo -n true` 返回 0 | 沙箱无用户级隔离（设计如此） |
| 工作区有 `baseline*/changes*` 文件 | 平台差异采集协议 |

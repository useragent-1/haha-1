# 未安装清单（MISSING）

> 生成时间：2026-10-06 ｜ 对应安装脚本：`tools/setup_full.sh`
> 统计：**可用 148 ｜ 失败 1（已用替代方案）｜ 仅记录 4 ｜ 跳过 8 类**

> **2026-10-06 更新**：第二批补装已写入 `setup_full.sh` 并覆盖上表缺口，共 9 项——
> GoPhish（钓鱼演练）、swaks/mailutils（邮件）、sigma-cli（威胁狩猎）、
> EvilClippy/ScareCrow（载荷生成）、CUpp（社工字典）、GTFOBins/LOLBAS/HackTricks（渗透知识库）。
> 这批**待沙箱验证**（跑一次 `bash tools/setup_full.sh` 即生效）。
> 另：SigmaHQ / PayloadsAllTheThings / SecLists 三个大库改为**可选安装**（`SETUP_BIGRULES=1`），默认跳过。

本文件回答"哪些没装上、为什么、有什么替代、什么时候值得装"。已安装的全部见 `TOOLS.md`。

---

## 一、仅记录未安装（B 档：体积超出可接受范围）

| 工具 | 体积 | 未装原因 | 替代方案 | 什么时候值得装 |
|---|---|---|---|---|
| **metasploit-framework** | 1-2 GB | 每次新建沙箱都要重新下载 1-2GB，轮次成本过高 | `pocsuite3`（Python POC 框架，已装）+ `searchsploit` + 工具手工组合，覆盖约 80% 场景 | 有持久环境（自建 VPS / 本机）时；或平台提高额度时 |
| **ghidra / ghidra-headless** | 1-2 GB（含 JDK） | 同上；且 GUI 版在沙箱无意义 | `radare2` + `angr`（符号执行）+ `capa`（能力分析）+ `r2pipe`/`lief` 组合 | 同上 |
| **SecLists**（大型安全词表） | >1 GB | 体积过大，多数场景不需要全量 | `crunch`（自造词表）+ `cewl`（爬取）+ `wordlists/rockyou`（**已补装**） | 已改为**可选安装**：`SETUP_BIGRULES=1 bash tools/setup_full.sh` |

> **注**：`wordlists`（rockyou.txt，约 130MB）已从 B 档**提升到 A 档**并加入 `setup_full.sh` —— 它装在 `/usr/share/`，不占工作区与快照额度。

---

## 二、明确跳过（C 档：环境物理限制，非选择）

| 类别 | 具体 | 原因 | 替代做法 |
|---|---|---|---|
| **GUI 工具** | IDA、Ghidra GUI、Burp GUI、Wireshark GUI、BloodHound GUI | 沙箱无显示服务 | 均有 CLI 等价：radare2 / nuclei+ffuf / tshark / bloodhound-python |
| **付费商业** | Peach、Cobalt Strike | 需商业授权 | `boofuzz` + `hypothesis` + 自写 harness |
| **真实硬件** | aircrack 真机监听/注入、蓝牙嗅探、USB HID | 无无线网卡/蓝牙/USB 设备 | 工具**已安装**，仅无法实操；可分析 PCAP 侧信道数据 |
| **真机插桩** | Frida 对真实 Android/iOS 应用 | 无真机 | Frida 可对模拟器/本地进程用；speakeasy/unicorn 做纯模拟 |
| **长时间编译 C2** | Sliver、Havoc、Custom C2 | 编译常超 120s 上限 | pocsuite3 + 隧道三件套（ligolo/chisel/frp/gost，已装） |
| **容器内操作** | Docker 内部运行、k8s 集群操作 | 无 docker daemon、无集群凭据 | trivy/grype/checkov 可扫描导出的镜像与清单文件 |

---

## 三、失败但已有替代（1 项）

| 工具 | 失败原因 | 替代 |
|---|---|---|
| **boofuzz** | 沙箱禁止提升 core dump hard limit | `hypothesis`（属性测试）+ `afl++`（模糊测试）+ 自写 socket harness |

**另两例已修复**（原为失败，已改为 GitHub 源安装）：

- `sievecarve` → `pip install git+https://github.com/siegilt/sievecarve.git`
- `cti-python-sdk` → `pip install git+https://github.com/mitre-attack/cti-python-sdk.git`
  （其同项目发行版 `mitreattack-python` 本就已装，能力等价）

---

## 四、覆盖度自评：对攻防够不够？

| 能力域 | 覆盖 | 说明 |
|---|---|---|
| 二进制静态逆向 | **完整** | radare2 / capa / floss / yara / pefile / lief / pyelftools / binutils |
| 动态分析与调试 | **完整** | gdb / lldb / strace / ltrace / qemu-user / frida / angr / unicorn / speakeasy |
| 二进制开发与利用 | **完整** | pwntools / ROPgadget / ropper / z3 / keystone |
| 移动应用 | **较完整** | jadx / apktool / dex2jar / frida / objection（真机除外） |
| 固件 / IoT | **较完整** | binwalk / firmwalker / ubi_reader / unblob |
| Web 安全 | **完整** | nuclei / ffuf / gobuster / feroxbuster / katana / sqlmap / dalfox / tplmap / gopherus / jwt_tool / arjun |
| 网络与流量 | **完整**（采集侧） | nmap / masscan / zeek / suricata / tshark / scapy / mitmproxy |
| 内网 / 域渗透 | **较完整**（缺 metasploit） | impacket / netexec / pypykatz / responder / lazagne / 隧道三件套 |
| 密码与凭证 | **完整** | hashcat / john / hydra / rockyou / gitleaks / trufflehog / detect-secrets |
| 云 / 容器安全 | **较完整**（无运行时） | trivy / grype / syft / checkov / prowler / kube-hunter |
| 恶意代码分析 | **完整** | capa / yara / floss / ssdeep / clamav / pe_deep_scan |
| 取证 | **较完整** | volatility3 / sleuthkit / foremost / testdisk / zeek |
| AI / LLM 安全 | **已覆盖** | garak / pyrit / llm-guard |
| 钓鱼演练 | **已补装（待验证）** | GoPhish（演练平台）+ swaks/mailutils（邮件投递与测试） |
| 威胁狩猎 | **已补装（待验证）** | sigma-cli（引擎）+ SigmaHQ 规则库（可选）+ eve-n（已装） |
| 载荷生成 / 免杀 | **部分补装（待验证）** | EvilClippy（.NET）+ ScareCrow（loader）；C2 框架仍跳过（编译/规则排除） |
| 渗透知识库 | **已补装（待验证）** | GTFOBins / LOLBAS / HackTricks（轻量纯文本，检索价值高） |

**结论**：

- **对样本逆向 / CTF / 授权渗透 / 协议分析 / Web 安全 / 内网横向：覆盖充分，可以开工**
- **主要缺口**：metasploit（渗透框架）、ghidra（重型反编译）、SecLists（全量词表）—— 三者都是**体积问题，不是能力缺失**，在持久环境（本地 / VPS）补装即可
- **无法补齐**：GUI、真机硬件、商业授权类（环境决定）

---

## 五、复现与自检

```bash
# 全量安装（幂等，可重复执行）
bash tools/setup_full.sh

# 只装核心 25 件套（约 30 秒）
bash tools/setup_core.sh

# 安装后自检（PASS / FAIL / 仅记录 / 跳过）
python3 tools/setup_tools_doctor.py

# 逐项安装状态（含失败原因与日志路径）
cat /home/user/tool-install-logs/status.tsv
```

**日志位置**：`/home/user/tool-install-logs/*.log`（每个失败项的完整原文）

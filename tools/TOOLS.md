# TOOLS

> 状态为当前沙箱真实自检结果。A档尽力安装；B档仅记录；C档按规则跳过。所有网络/攻击类工具只做版本、import 或路径检查，未向外网发起扫描。

---

## 第二批补装（2026-10-06 追加 · 脚本已就位 · **待沙箱验证**）

> 以下条目已写入 `setup_full.sh`，**尚未在沙箱内实测**——下一轮执行 `bash tools/setup_full.sh` 时才会安装并自检。
> 状态列请在验证后由 `tools/setup_tools_doctor.py` 刷新。

| 类别 | 工具 | 用途 | 状态 | 备注 |
|---|---|---|---|---|
| 钓鱼演练 | **GoPhish** | 开源钓鱼演练平台（红蓝对抗标准环节） | 待验证 | 预编译二进制 |
| 邮件 | **swaks** / **mailutils** | SMTP 客户端、邮件头与投递测试 | 待验证 | apt |
| 威胁狩猎 | **sigma-cli** | Sigma 规则引擎（配合规则库做日志狩猎） | 待验证 | pip |
| 载荷生成 | **EvilClippy** | .NET 程序集注入与混淆 | 待验证 | git；实际运行需 mono |
| 载荷生成 | **ScareCrow** | 生成免杀 loader（含 shellcode 编码器） | 待验证 | git；编译可能超 120s |
| 社工字典 | **CUpp** | 社工字典生成器 | 待验证 | git |
| 知识库 | **GTFOBins** | Linux 提权/绕过命令库 | 待验证 | 轻量纯文本，检索价值高 |
| 知识库 | **LOLBAS** | Windows 提权/绕过命令库 | 待验证 | 轻量纯文本 |
| 知识库 | **HackTricks** | 渗透技巧全库（侦察→利用→后渗透） | 待验证 | 轻量纯文本 |
| 规则库（可选） | SigmaHQ / PayloadsAllTheThings / SecLists | 狩猎规则 / payload 库 / 词表 | 默认跳过 | 设 `SETUP_BIGRULES=1` 开启 |

**验证命令**：
```bash
bash tools/setup_full.sh && python3 tools/setup_tools_doctor.py
```

---

## 第三批补装（2026-10-06 · `tools/setup_advanced.sh` · **待沙箱验证**）

> 目标：补齐 Ghidra 全量 / Windows 工具链 / 内存取证 / 威胁情报 / 侦察取证 五块真缺口。
> **metasploit、Ghidra 全量、C2 框架按决策不装**（沙箱装不上或用不上，见 `MISSING.md`）。

### A. 反编译与二进制深度（用 1/40 体积拿到 Ghidra 的 decompiler）

| 工具 | 用途 | 状态 |
|---|---|---|
| **r2ghidra** | **Ghidra 的反编译器后端**（`go install` 装到 /usr/local/bin）→ radare2 里 `pdc`/`pdg` 直接出伪 C | 待验证 |
| **diffoscope** | 二进制深度差异对比（几百 MB 文件也能逐层 diff） | 待验证 |
| **lief** / **r2pipe** | PE/ELF/Mach-O 统一解析 + Python 驱动 radare2 | 待验证 |

### B. Windows 工具链替代（无 Windows，用 mono/wine 跑能跑的）

| 工具 | 用途 | 状态 |
|---|---|---|
| **mono-devel / mono-utils** | .NET 运行时 + `monodis`（IL 反汇编） | 待验证 |
| **wine** | 运行部分 Windows CLI 工具 | 待验证 |
| **de4dot** | .NET 去混淆（Shroud/ConfuserEx 等），mono 下可跑 | 待验证 |

### C. 内存取证与端点狩猎（此前完全空白）

| 工具 | 用途 | 状态 |
|---|---|---|
| **guymager** | 内存/磁盘镜像采集（FTK Imager 的 Linux 等价） | 待验证 |
| **ClamAV** | 反病毒引擎，验证样本是否被主流 AV 标记 | 待验证 |
| **osquery** | 跨平台端点 SQL 查询 | 待验证 |
| **Velociraptor** | 端点狩猎框架（源码） | 待验证 |

### D. 威胁情报与 CVE（API 受限时的本地替代路径）

| 工具 | 用途 | 状态 |
|---|---|---|
| **cve-bin-tool** | 本地 NVD 数据匹配——给二进制查已知漏洞 | 待验证 |
| **stix2-validator** / **pymisp** | STIX 校验 / MISP API 客户端 | 待验证 |
| **otxv2** | IOC 批量提取（URL/IP/哈希/邮箱） | 待验证 |
| **ja3** | TLS 客户端指纹计算 | 待验证 |

### E. 侦察取证补漏

| 工具 | 用途 | 状态 |
|---|---|---|
| **dnstwist** | 域名投毒与错拼域名枚举 | 待验证 |
| **git-dumper** | 从 GitHub 拉取泄露的 `.git` 仓库源码 | 待验证 |
| **gowitness** | 网页截图取证 | 待验证 |
| **uncover** | Shodan/Hunter 聚合搜索 | 待验证（需 API key） |

### 可选（`SETUP_HEAVY=1`）

`qemu-system-x86`（完整系统模拟，可起 Linux 靶机）、`bloaty`（函数级体积分析）、`plaso`（超时间线）。

### 仍然装不了的（硬天花板，非工具问题）

| 缺口 | 硬原因 |
|---|---|
| WinDbg / x64dbg / Procmon 等 Windows 动态调试 | 沙箱是 Linux（wine 只能覆盖少数 CLI 工具） |
| IDA / Ghidra GUI / Burp 图形分析 | 沙箱无显示服务器 |
| 真机固件 / IoT / USB 样本执行 | 无硬件 |
| CobaltStrike / IDA Pro / Burp Pro | 商业授权 |

---


---


| 类别 | 工具 | 一句话用途 | 状态 | 版本 | 沙箱限制/安装备注 | 自检 |
|---|---|---|---|---|---|---|
| 逆向与动态 | radare2 | 反汇编/逆向 | 可用 | 6.2.4 | 仅本地自检；禁止未授权扫描 | cmd:r2 |
| 逆向与动态 | gdb | 本机调试 | 可用 | 16.3-1 | 仅本地自检；禁止未授权扫描 | cmd:gdb |
| 逆向与动态 | lldb | LLVM 调试器 | 可用 | 1:19.0-63 | 仅本地自检；禁止未授权扫描 | cmd:lldb |
| 逆向与动态 | binutils | ELF/目标文件工具 | 可用 | 2.44-3 | 仅本地自检；禁止未授权扫描 | cmd:readelf |
| 逆向与动态 | gawk | 文本处理 | 可用 | 1:5.2.1-2+b1 | 仅本地自检；禁止未授权扫描 | cmd:gawk |
| 逆向与动态 | patchelf | ELF 解释器/RPATH 修改 | 可用 | 0.18.0-1.4 | 仅本地自检；禁止未授权扫描 | cmd:patchelf |
| 逆向与动态 | strace | 系统调用追踪 | 可用 | 6.13+ds-1 | 仅本地自检；禁止未授权扫描 | cmd:strace |
| 逆向与动态 | ltrace | 库调用追踪 | 可用 | 0.7.91~git20230705.8eabf68-4+b1 | 仅本地自检；禁止未授权扫描 | cmd:ltrace |
| 逆向与动态 | qemu-user-static | 跨架构用户态模拟 | 可用 | 1:10.0.13+ds-0+deb13u1 | 仅本地自检；禁止未授权扫描 | cmd:qemu-x86_64-static |
| 逆向与动态 | build-essential | C/C++ 编译链 | 可用 | 4:14.2.0-1 | 仅本地自检；禁止未授权扫描 | cmd:gcc |
| 逆向与动态 | cmake | 跨平台构建 | 可用 | 3.31.6-2 | 仅本地自检；禁止未授权扫描 | cmd:cmake |
| 逆向与动态 | golang-go | Go 工具链 | 可用 | 2:1.24~2 | 仅本地自检；禁止未授权扫描 | cmd:go |
| 逆向与动态 | rustc | Rust 编译器 | 可用 | 1.85.1+dfsg1-1+deb13u1 | 仅本地自检；禁止未授权扫描 | cmd:rustc |
| 逆向与动态 | cargo | Rust 包/构建 | 可用 | 1.85.1+dfsg1-1+deb13u1 | 仅本地自检；禁止未授权扫描 | cmd:cargo |
| 逆向与动态 | python3-dev | Python 扩展头文件 | 可用 | Usage: /usr/local/bin/python3-config --prefix/--exec-prefix/--includes/--libs/--cflags/--ldflags/--e | 仅本地自检；禁止未授权扫描 | cmd:python3-config |
| 逆向与动态 | python3-venv | 隔离 Python 环境 | 可用 | source | 仅本地自检；禁止未授权扫描 | path:/usr/lib/python3.13/venv/__init__.py |
| 逆向与动态 | angr | 符号执行 | 可用 | 10.0.1.post1 | 仅本地自检；禁止未授权扫描 | py:angr |
| 逆向与动态 | pwntools | 漏洞开发脚本框架 | 可用 | 4.15.0 | 仅本地自检；禁止未授权扫描 | py:pwn |
| 逆向与动态 | lief | 可执行格式解析 | 可用 | 1.0.0 | 仅本地自检；禁止未授权扫描 | py:lief |
| 逆向与动态 | pefile | PE 解析 | 可用 | 2024.8.26 | 仅本地自检；禁止未授权扫描 | py:pefile |
| 逆向与动态 | pyelftools | ELF/DWARF 解析 | 可用 | 0.33 | 仅本地自检；禁止未授权扫描 | py:elftools |
| 逆向与动态 | macholib | Mach-O 解析 | 可用 | 1.16.4 | 仅本地自检；禁止未授权扫描 | py:macholib |
| 逆向与动态 | capstone | 反汇编引擎 | 可用 | 5.0.9 | 仅本地自检；禁止未授权扫描 | py:capstone |
| 逆向与动态 | unicorn | CPU 模拟 | 可用 | 2.1.2 | 仅本地自检；禁止未授权扫描 | py:unicorn |
| 逆向与动态 | keystone-engine | 汇编引擎 | 可用 | 0.9.2 | 仅本地自检；禁止未授权扫描 | py:keystone |
| 逆向与动态 | ropper | ROP gadget 工具 | 可用 | 1.13.13 | 仅本地自检；禁止未授权扫描 | py:ropper |
| 逆向与动态 | ROPgadget | ROP gadget 搜索 | 可用 | 7.7 | 仅本地自检；禁止未授权扫描 | py:ropgadget |
| 逆向与动态 | z3-solver | SMT 求解 | 可用 | 5.1.0.0 | 仅本地自检；禁止未授权扫描 | py:z3 |
| 逆向与动态 | miasm | 二进制分析/IR | 可用 | 0.1.5 | 仅本地自检；禁止未授权扫描 | py:miasm |
| 逆向与动态 | qiling | 多架构仿真框架 | 可用 | 1.4.6 | 仅本地自检；禁止未授权扫描 | py:qiling |
| 逆向与动态 | flare-capa | 能力识别 | 可用 | 9.4.0 | 仅本地自检；禁止未授权扫描 | py:capa |
| 逆向与动态 | r2pipe | radare2 Python API | 可用 | 1.9.8 | 仅本地自检；禁止未授权扫描 | py:r2pipe |
| 逆向与动态 | frida-tools | 动态插桩 CLI | 可用 | 14.11.0 | 仅本地自检；禁止未授权扫描 | py:frida |
| 逆向与动态 | objection | Frida 移动运行时探索 | 可用 | 1.12.5 | 仅本地自检；禁止未授权扫描 | py:objection |
| 逆向与动态 | yara-x | YARA-X Python 绑定 | 可用 | 1.21.0 | 仅本地自检；禁止未授权扫描 | py:yara_x |
| 逆向与动态 | speakeasy | Windows API 模拟器 | 可用 | 1.5.11 | 独立 venv；与 qiling 所需 Unicorn 版本冲突 | path:/opt/security-tools/venvs/speakeasy/bin/python |
| 逆向与动态 | FLOSS | 静态字符串解码 | 可用 | 3.1.1 | 仅本地自检；禁止未授权扫描 | cmd:floss |
| 逆向与动态 | YARA | 模式匹配 | 可用 | 4.5.2-1 | 仅本地自检；禁止未授权扫描 | cmd:yara |
| 漏洞与POC | pocsuite3 | POC 框架 | 可用 | [01;33m | 仅本地自造目标 | cmd:pocsuite |
| 漏洞与POC | boofuzz | 协议模糊测试 | 失败 | 0.4.2 | 仅本地自造目标 | py:boofuzz |
| 漏洞与POC | hypothesis | 属性测试 | 可用 | 6.168.5 | 仅本地自造目标 | py:hypothesis |
| 漏洞与POC | afl++ | 覆盖率模糊测试 | 可用 | 4.21c-5 | 仅本地自造目标 | cmd:afl-fuzz |
| 漏洞与POC | radamsa | 生成式模糊测试 | 可用 | Radamsa 0.8a | 仅本地自造目标 | cmd:radamsa |
| 网络与协议 | nmap | 网络探测 | 可用 | 7.95+dfsg-3 | 只做 --version/本地验证；禁止外网扫描 | cmd:nmap |
| 网络与协议 | masscan | 高速端口扫描 | 可用 | 2:1.3.2+ds1-2 | 只做 --version/本地验证；禁止外网扫描 | cmd:masscan |
| 网络与协议 | tcpdump | 抓包 | 可用 | 4.99.5-2 | 只做 --version/本地验证；禁止外网扫描 | cmd:tcpdump |
| 网络与协议 | tshark | Wireshark CLI | 可用 | 4.4.19-0+deb13u1 | 只做 --version/本地验证；禁止外网扫描 | cmd:tshark |
| 网络与协议 | zeek-client | Zeek 管理客户端 | 可用 | 1.5.0 | 只做 --version/本地验证；禁止外网扫描 | cmd:zeek-client |
| 网络与协议 | suricata | IDS/IPS 引擎 | 可用 | 1:7.0.10-1+deb13u4 | 只做 --version/本地验证；禁止外网扫描 | cmd:suricata |
| 网络与协议 | hping3 | 报文构造 | 可用 | source | 只做 --version/本地验证；禁止外网扫描 | path:/usr/sbin/hping3 |
| 网络与协议 | netcat-openbsd | TCP/UDP 管道 | 可用 | /usr/bin/nc: invalid option -- '-' | 只做 --version/本地验证；禁止外网扫描 | cmd:nc |
| 网络与协议 | socat | 双向 socket relay | 可用 | 1.8.0.3-1 | 只做 --version/本地验证；禁止外网扫描 | cmd:socat |
| 网络与协议 | dnsutils | DNS 查询 | 可用 | 1:9.20.29-1~deb13u1 | 只做 --version/本地验证；禁止外网扫描 | cmd:dig |
| 网络与协议 | ethtool | 网卡参数 | 可用 | source | 只做 --version/本地验证；禁止外网扫描 | path:/usr/sbin/ethtool |
| 网络与协议 | arp-scan | ARP 扫描 | 可用 | source | 只做 --version/本地验证；禁止外网扫描 | path:/usr/sbin/arp-scan |
| 网络与协议 | scapy | 报文构造/PCAP | 可用 | 2.8.0 | 不拦截真实凭据 | py:scapy |
| 网络与协议 | mitmproxy | HTTP 代理 | 可用 | 12.2.3 | 不拦截真实凭据 | py:mitmproxy |
| 网络与协议 | impacket | 网络协议库 | 可用 | 0.13.1 | 不拦截真实凭据 | py:impacket |
| 网络与协议 | httpx | 资产/协议 CLI | 可用 | Usage: httpx [OPTIONS] URL | 仅版本自检；不向外网发起探测 | cmd:httpx |
| 网络与协议 | naabu | 资产/协议 CLI | 可用 | __ | 仅版本自检；不向外网发起探测 | cmd:naabu |
| 网络与协议 | dnsx | 资产/协议 CLI | 可用 | _             __  __ | 仅版本自检；不向外网发起探测 | cmd:dnsx |
| 网络与协议 | tlsx | 资产/协议 CLI | 可用 | _____ _    _____  __ | 仅版本自检；不向外网发起探测 | cmd:tlsx |
| 网络与协议 | subfinder | 资产/协议 CLI | 可用 | [[34mINF[0m] Current Version: v2.16.0 | 仅版本自检；不向外网发起探测 | cmd:subfinder |
| 网络与协议 | nuclei | 资产/协议 CLI | 可用 | [[34mINF[0m] Nuclei Engine Version: v3.11.1 | 仅版本自检；不向外网发起探测 | cmd:nuclei |
| 网络与协议 | katana | 资产/协议 CLI | 可用 | __        __ | 仅版本自检；不向外网发起探测 | cmd:katana |
| 网络与协议 | gau | 资产/协议 CLI | 可用 | gau version: 2.2.4 | 仅版本自检；不向外网发起探测 | cmd:gau |
| 网络与协议 | waybackurls | 资产/协议 CLI | 可用 | flag provided but not defined: -version | 仅版本自检；不向外网发起探测 | cmd:waybackurls |
| 网络与协议 | dalfox | 资产/协议 CLI | 可用 | dalfox 3.2.3 | 仅版本自检；不向外网发起探测 | cmd:dalfox |
| 网络与协议 | interactsh-client | 资产/协议 CLI | 可用 | _       __                       __       __ | 仅版本自检；不向外网发起探测 | cmd:interactsh-client |
| 网络与协议 | amass | 资产/协议 CLI | 可用 | v5.1.1 | 仅版本自检；不向外网发起探测 | cmd:amass |
| 网络与协议 | asnmap | 资产/协议 CLI | 可用 | [[34mINF[0m] Current Version: v1.1.1 | 仅版本自检；不向外网发起探测 | cmd:asnmap |
| 网络与协议 | massdns | 资产/协议 CLI | 可用 | massdns | 仅版本自检；不向外网发起探测 | cmd:massdns |
| 网络与协议 | puredns | 资产/协议 CLI | 可用 | puredns version v2.1.1 | 仅版本自检；不向外网发起探测 | cmd:puredns |
| 网络与协议 | unicornscan | 异步扫描器源码 | 可用 | 已安装/版本未取到 | 仅源码；raw socket/外网扫描未运行 | path:/home/user/push-tmp/scripts/net/unicornscan |
| Web与凭据 | sqlmap | SQL 注入审计 | 可用 | 1.9.6-1 | 只对自造/授权目标；不使用真实凭据 | cmd:sqlmap |
| Web与凭据 | nikto | Web 配置扫描 | 可用 | git  | 只对自造/授权目标；不使用真实凭据 | path:/opt/security-tools/nikto/program/nikto.pl |
| Web与凭据 | ffuf | Web fuzz | 可用 | 2.1.0-1+b9 | 只对自造/授权目标；不使用真实凭据 | cmd:ffuf |
| Web与凭据 | feroxbuster | 内容发现 | 可用 | feroxbuster 2.13.1 | 只对自造/授权目标；不使用真实凭据 | cmd:feroxbuster |
| Web与凭据 | gobuster | 目录/DNS 枚举 | 可用 | 3.6.0-1+b10 | 只对自造/授权目标；不使用真实凭据 | cmd:gobuster |
| Web与凭据 | wpscan | WordPress 审计 | 可用 | _______________________________________________________________ | 只对自造/授权目标；不使用真实凭据 | cmd:wpscan |
| Web与凭据 | whatweb | Web 指纹 | 可用 | 0.5.5-1 | 只对自造/授权目标；不使用真实凭据 | cmd:whatweb |
| Web与凭据 | theHarvester | 公开情报聚合 | 可用 | git  | 只对自造/授权目标；不使用真实凭据 | path:/opt/security-tools/theHarvester/theHarvester/theHarvester.py |
| Web与凭据 | joomscan | Joomla 审计 | 可用 | git  | 只对自造/授权目标；不使用真实凭据 | path:/opt/security-tools/joomscan/joomscan.pl |
| Web与凭据 | droopescan | CMS 审计 | 可用 | Traceback (most recent call last): | 只对自造/授权目标；不使用真实凭据 | cmd:droopescan |
| Web与凭据 | hydra | 登录审计 | 可用 | 9.5-3 | 只对自造/授权目标；不使用真实凭据 | cmd:hydra |
| Web与凭据 | medusa | 并行登录审计 | 可用 | 2.3-2 | 只对自造/授权目标；不使用真实凭据 | cmd:medusa |
| Web与凭据 | ncrack | 网络认证审计 | 可用 | 0.7+debian-6 | 只对自造/授权目标；不使用真实凭据 | cmd:ncrack |
| Web与凭据 | cewl | 站点词表生成 | 可用 | 6.2.1-1 | 只对自造/授权目标；不使用真实凭据 | cmd:cewl |
| Web与凭据 | crunch | 规则词表生成 | 可用 | 3.6-3 | 只对自造/授权目标；不使用真实凭据 | cmd:crunch |
| Web与凭据 | smbclient | SMB 客户端 | 可用 | 2:4.22.11+dfsg-0+deb13u1 | 只对自造/授权目标；不使用真实凭据 | cmd:smbclient |
| Web与凭据 | rpcclient | RPC 客户端 | 可用 | 2:4.22.11+dfsg-0+deb13u1 | 只对自造/授权目标；不使用真实凭据 | cmd:rpcclient |
| Web与凭据 | ldapsearch | LDAP 查询 | 可用 | 2.6.10+dfsg-1 | 只对自造/授权目标；不使用真实凭据 | cmd:ldapsearch |
| Web与凭据 | krb5-user | Kerberos CLI | 可用 | /usr/bin/kinit: unrecognized option '--version' | 只对自造/授权目标；不使用真实凭据 | cmd:kinit |
| Web与凭据 | dnsrecon | DNS 枚举 | 可用 | 1.2.0-3 | 只对自造/授权目标；不使用真实凭据 | cmd:dnsrecon |
| Web与凭据 | fierce | DNS 侦察 | 可用 | 1.6.0-1 | 只对自造/授权目标；不使用真实凭据 | cmd:fierce |
| Web与凭据 | enum4linux | SMB 枚举源码 | 可用 | git  | 只对自造/授权目标；不使用真实凭据 | path:/opt/security-tools/enum4linux/enum4linux.pl |
| Web与凭据 | dirsearch | 目录发现 | 可用 | 0.5.0 | 不发起未授权外网扫描 | cmd:dirsearch |
| Web与凭据 | wapiti | Web 漏洞扫描 | 可用 | 3.3.2 | 不发起未授权外网扫描 | cmd:wapiti |
| Web与凭据 | cmseek | CMS 检测源码 | 可用 | git  | 不发起未授权外网扫描 | path:/opt/security-tools/CMSeeK/cmseek.py |
| Web与凭据 | commix | 命令注入审计 | 可用 | 0.1 | 不发起未授权外网扫描 | cmd:commix |
| Web与凭据 | h8mail | 邮箱 OSINT | 可用 | 2.5.6 | 不发起未授权外网扫描 | cmd:h8mail |
| Web与凭据 | shhgit | 公开仓库秘密线索 | 可用 | flag provided but not defined: -version | 不发起未授权外网扫描 | cmd:shhgit |
| Web与凭据 | detect-secrets | 秘密检测 | 可用 | 1.5.0 | 不发起未授权外网扫描 | cmd:detect-secrets |
| Web与凭据 | recon-ng | 侦察框架源码 | 可用 | git  | 不发起未授权外网扫描 | path:/opt/security-tools/recon-ng/recon-ng |
| Web与凭据 | sublist3r | 子域枚举 | 可用 | 1.0 | 不发起未授权外网扫描 | cmd:sublist3r |
| Web与凭据 | gitleaks | Git 秘密扫描 | 可用 | 8.30.1 | 只报告位置/指纹，不输出值 | cmd:gitleaks |
| Web与凭据 | trufflehog | 秘密扫描 | 可用 | trufflehog 3.98.0 | 只报告位置/指纹，不输出值 | cmd:trufflehog |
| Web与凭据 | assetfinder | 资产发现 | 可用 | flag provided but not defined: -version | 仅版本自检 | cmd:assetfinder |
| Web与凭据 | findomain | 子域发现 | 可用 | findomain 10.0.1 | 仅版本自检 | cmd:findomain |
| Web与凭据 | LaZagne | 本地主机凭据恢复源码 | 可用 | git  | 不运行；可能访问凭据，仅保留源码 | path:/opt/security-tools/LaZagne/Linux/laZagne.py |
| Web与凭据 | gitrob | GitHub 组织审计源码 | 可用 | git  | 需授权/API token；本轮不配置凭据 | path:/opt/security-tools/gitrob |
| 隧道与提权 | ligolo-ng | 隧道代理 | 可用 | time="2026-10-06T04:14:35Z" level=info msg="Loading configuration file ligolo-ng.yaml" | 只做版本自检；不建立外联隧道 | cmd:ligolo-proxy |
| 隧道与提权 | chisel | HTTP 隧道 | 可用 | 1.12.0 | 只做版本自检；不建立外联隧道 | cmd:chisel |
| 隧道与提权 | frp | 反向代理 | 可用 | 0.71.0 | 只做版本自检；不建立外联隧道 | cmd:frpc |
| 隧道与提权 | gost | 多协议代理 | 可用 | flag provided but not defined: -version | 只做版本自检；不建立外联隧道 | cmd:gost |
| 隧道与提权 | proxychains4 | 代理链 | 可用 | 4.17-3 | 只做版本自检；不建立外联隧道 | cmd:proxychains4 |
| 隧道与提权 | linpeas | 本地提权枚举脚本源码 | 可用 | [1;32mEnumerate and search Privilege Escalation vectors. | 未对宿主执行 | cmd:linpeas |
| 隧道与提权 | pspy | 进程监控源码 | 可用 | git  | 源码克隆；未长期驻留运行 | path:/opt/security-tools/pspy |
| 固件/隐写/取证/IoT | binwalk | 固件识别/提取 | 可用 | 2.4.3+dfsg1-2+deb13u1 | 只读本地样本；无线真机实操跳过 | cmd:binwalk |
| 固件/隐写/取证/IoT | aircrack-ng | 无线审计 CLI | 可用 | 1:1.7+git20230807.4bf83f1a-2 | 只读本地样本；无线真机实操跳过 | cmd:aircrack-ng |
| 固件/隐写/取证/IoT | reaver | WPS 审计 | 可用 | 1.6.6-2+b1 | 只读本地样本；无线真机实操跳过 | cmd:reaver |
| 固件/隐写/取证/IoT | steghide | 隐写 | 可用 | 0.5.1-15 | 只读本地样本；无线真机实操跳过 | cmd:steghide |
| 固件/隐写/取证/IoT | exiftool | 元数据 | 可用 | 13.25+dfsg-1 | 只读本地样本；无线真机实操跳过 | cmd:exiftool |
| 固件/隐写/取证/IoT | foremost | 文件雕刻 | 可用 | 1.5.7-11+b2 | 只读本地样本；无线真机实操跳过 | cmd:foremost |
| 固件/隐写/取证/IoT | testdisk | 磁盘恢复 | 可用 | 7.2-0.1 | 只读本地样本；无线真机实操跳过 | cmd:testdisk |
| 固件/隐写/取证/IoT | sleuthkit | 文件系统取证 | 可用 | 4.12.1+dfsg-3 | 只读本地样本；无线真机实操跳过 | cmd:fls |
| 固件/隐写/取证/IoT | ssdeep | 模糊哈希 | 可用 | 2.14.1+git20180629.57fcfff-3+b2 | 只读本地样本；无线真机实操跳过 | cmd:ssdeep |
| 固件/隐写/取证/IoT | tlsh | 趋势哈希库 | 可用 | 5.0.0 | 仅本地自检；禁止未授权扫描 | py:tlsh |
| 固件/隐写/取证/IoT | wifite2 | 无线审计源码 | 可用 | git  | 无无线真机，不运行 | path:/opt/security-tools/wifite2/Wifite.py |
| 固件/隐写/取证/IoT | volatility3 | 内存取证 | 可用 | 2.28.2 | 仅本地自检；禁止未授权扫描 | cmd:vol |
| 固件/隐写/取证/IoT | sievecarve | 文件雕刻工具 | 失败 | PyPI 无发行版 | pip: No matching distribution found | none |
| 固件/隐写/取证/IoT | yara-python | YARA Python 绑定 | 可用 | 4.5.4 | 仅本地自检；禁止未授权扫描 | py:yara |
| 固件/隐写/取证/IoT | firmwalker | 固件文件系统检查源码 | 可用 | git  | 使用公开 fork；原仓库克隆需认证失败 | path:/opt/security-tools/firmwalker/firmwalker.sh |
| 云与容器安全 | trivy | 镜像/SBOM/漏洞 CLI | 可用 | Version: 0.75.0 | Docker 不可用；仅版本自检 | cmd:trivy |
| 云与容器安全 | syft | 镜像/SBOM/漏洞 CLI | 可用 | syft 1.54.0 | Docker 不可用；仅版本自检 | cmd:syft |
| 云与容器安全 | grype | 镜像/SBOM/漏洞 CLI | 可用 | grype 0.120.0 | Docker 不可用；仅版本自检 | cmd:grype |
| 云与容器安全 | kube-hunter | Kubernetes 审计 | 可用 | 0.6.8 | 不连接真实集群 | cmd:kube-hunter |
| 云与容器安全 | checkov | IaC 静态检查 | 可用 | 3.3.23 | 仅本地自检；禁止未授权扫描 | cmd:checkov |
| 威胁情报 | cti-python-sdk | 请求的 CTI SDK | 失败 | PyPI 无发行版 | 包名无法解析；未用无关同名 CTI 包替代 | none |
| 威胁情报 | stix2 | STIX 2 库 | 可用 | 3.0.2 | 仅本地自检；禁止未授权扫描 | py:stix2 |
| 威胁情报 | mitreattack-python | MITRE ATT&CK 数据库 API | 可用 | 6.2.1 | 仅本地自检；禁止未授权扫描 | py:mitreattack |
| 便利工具 | yq | YAML CLI | 可用 | 3.4.3-2 | 本地只读自检 | cmd:yq |
| 便利工具 | jq | JSON CLI | 可用 | 1.7.1-6+deb13u2 | 本地只读自检 | cmd:jq |
| 便利工具 | sqlite3 | SQLite CLI | 可用 | 3.46.1-7+deb13u2 | 本地只读自检 | cmd:sqlite3 |
| 便利工具 | postgresql-client | PostgreSQL CLI | 可用 | 278 | 本地只读自检 | cmd:psql |
| 便利工具 | redis-tools | Redis CLI | 可用 | 5:8.0.2-3+deb13u3 | 本地只读自检 | cmd:redis-cli |
| 便利工具 | tmux | 终端复用 | 可用 | 3.5a-3 | 本地只读自检 | cmd:tmux |
| 便利工具 | pandoc | 文档转换 | 可用 | 3.1.11.1+ds-2 | 本地只读自检 | cmd:pandoc |
| 便利工具 | graphviz | 图生成 | 可用 | 2.42.4-3 | 本地只读自检 | cmd:dot |
| 便利工具 | file | 文件识别 | 可用 | 1:5.46-5 | 本地只读自检 | cmd:file |
| 便利工具 | lsof | 打开文件检查 | 可用 | 4.99.4+dfsg-2 | 本地只读自检 | cmd:lsof |
| B档仅记录 | metasploit-framework | 大型渗透测试框架 | 仅记录 | - | 安装: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb / sudo bash；约1–2GB | none |
| B档仅记录 | ghidra | 大型 GUI 逆向套件 | 仅记录 | - | 安装: 下载官方 Ghidra ZIP 解压；约1–2GB（含 JDK/项目缓存） | none |
| B档仅记录 | ghidra-headless | Ghidra headless | 仅记录 | - | 同 Ghidra ZIP，使用 support/analyzeHeadless；约1–2GB | none |
| B档仅记录 | rockyou | 大型密码词表 | 仅记录 | - | 安装: sudo apt install wordlists；解压约130MB | none |
| B档仅记录 | SecLists | 大型安全词表 | 仅记录 | - | 安装: git clone --depth 1 https://github.com/danielmiessler/SecLists.git；约1GB以上 | none |
| C档跳过 | GUI工具 | 所有需桌面交互的工具 | 跳过 | - | 沙箱无 GUI/显示服务 | none |
| C档跳过 | Peach | 付费/授权模糊测试 | 跳过 | - | 付费授权，未提供许可 | none |
| C档跳过 | Cobalt Strike | 商业红队平台 | 跳过 | - | 付费授权且高风险，不安装 | none |
| C档跳过 | aircrack-ng真机实操 | 无线真机审计 | 跳过 | - | 需要无线网卡/监控模式/明确授权 | none |
| C档跳过 | Frida真机实操 | 移动真机插桩 | 跳过 | - | 需要 Android/iOS 真机及授权 | none |
| C档跳过 | Sliver | C2 框架 | 跳过 | - | 长期编译且本轮规则明确跳过 | none |
| C档跳过 | Havoc | C2 框架 | 跳过 | - | 长期编译且本轮规则明确跳过 | none |
| C档跳过 | Docker内部运行 | 容器内验证 | 跳过 | - | 沙箱内 Docker 不可用 | none |

## 原始安装日志

- 汇总：`/home/user/tool-install-logs/status.tsv`
- 首轮脚本错误：`/home/user/setup_full_console_raw.txt`、`setup_full_console_retry_raw.txt`
- 预编译/Git：`/home/user/setup_full_binary_git_raw.txt`、`setup_full_fallbacks_raw.txt`
- 每个失败项完整原文：`/home/user/tool-install-logs/*.log`。

## 全局限制

- 不执行未授权外网扫描、口令攻击、C2、隧道连接或凭据访问。
- `/usr/local`、`/opt` 和 apt/pip 安装不保证跨沙箱轮次持久化；使用 setup 脚本重建。
- Docker、GUI、真实无线/移动硬件、内核级和强反调试场景未验证。

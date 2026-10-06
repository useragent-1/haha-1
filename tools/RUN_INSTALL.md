# 工具链安装与自检流程（Agent 执行指令）

> 给 arena agent 的执行脚本。**按阶段顺序跑，任何阶段失败也继续往下走**，最后统一报告。
> 环境开关：`SETUP_ADVANCED=1`（第三批）、`SETUP_HEAVY=0`（不装 qemu/plaso）、`SETUP_BIGRULES=0`（不装大规则库）

## 阶段 0 · 环境体检

```bash
df -h / /opt 2>/dev/null; free -m | head -3; nproc; uname -a
git --version; python3 -V; go version 2>/dev/null; go env GOPATH 2>/dev/null
r2 -v 2>/dev/null | head -1
```
记录：磁盘余量、内存、核数。若磁盘可用 < 5 GB，先报告再继续。

## 阶段 1 · 拉取最新仓库

```bash
cd /home/user
[ -d haha-1 ] && (cd haha-1 && git pull --ff-only) || git clone --depth 1 https://github.com/useragent-1/haha-1.git
cd haha-1 && git log --oneline -3
```

## 阶段 2 · 运行安装（第一 + 第二 + 第三批）

```bash
export SETUP_ADVANCED=1 SETUP_HEAVY=0 SETUP_BIGRULES=0
bash tools/setup_full.sh 2>&1 | tail -100
```

## 阶段 3 · 自检

```bash
python3 tools/setup_tools_doctor.py 2>&1 | tail -150
```

## 阶段 4 · 重点项逐一验证（第二、三批关键工具）

```bash
for c in r2ghidra-dec gophish sigma-cli monodis clamscan wine de4dot gowitness uncover; do
  printf '%-16s ' "$c"; command -v "$c" >/dev/null 2>&1 && echo "OK $(command -v $c)" || echo "MISSING"
done
python3 -c "import volatility3,lief,cve_bin_tool,otxv2,pymisp,stix2,dnstwist;print('py-modules OK')" 2>&1|tail -2
git -C /opt/security-tools/velociraptor log --oneline -1 2>&1|head -1
```

## 阶段 5 · 冒烟测试（证明真能用，而非仅仅装上）

```bash
# 5.1 radare2 + r2ghidra 真实反编译（关键：r2ghidra 是否生效）
printf 'int main(){int x=1;char*p="hi";return x+strlen(p);}' > /tmp/t.c
gcc -o /tmp/t /tmp/t.c 2>/dev/null && r2 -q -c 'aaa;pdc' /tmp/t 2>&1 | head -12

# 5.2 capa 能力识别
printf 'MZ\x90\x00' > /tmp/f.exe
python3 -m capa /tmp/f.exe 2>&1 | head -8

# 5.3 volatility3 是否可运行
python3 -m volatility3 --help 2>&1 | head -4

# 5.4 基础工具链
file /tmp/t; strings -n 6 /tmp/t | head -5; readelf -h /tmp/t | head -6
```

## 阶段 6 · 报告（必须包含以下 6 项，证据贴原文）

1. **统计**：status.tsv 中 PASS / FAIL / SKIPPED 各多少项
2. **FAIL 完整清单**：工具名 + 原因（读 `/home/user/tool-install-logs/` 下对应日志）
3. **阶段 4 重点项结果**：哪些 OK、哪些 MISSING
4. **阶段 5 冒烟输出**：特别是 `r2 -c pdc` 是否吐出伪 C 代码（这是 Ghidra 替代方案是否成立的唯一证据）
5. **磁盘最终占用**：`df -h /`
6. **结论**：还缺什么、为什么缺、是否需要人工介入

## 已知会失败的项目（不算 bug）

| 项目 | 原因 |
|---|---|
| metasploit-framework | 按决策不装（无靶点） |
| Ghidra 全量 / GUI | 按决策不装（体积 + 无显示），已用 r2ghidra 替代 |
| C2 框架（Sliver/Havoc/CS） | 按决策不装（编译超时 / 商业授权） |
| SecLists / SigmaHQ / PayloadsAllTheThings | 默认跳过，需 `SETUP_BIGRULES=1` |
| qemu-system-x86 / bloaty / plaso | 默认跳过，需 `SETUP_HEAVY=1` |

> 若某项失败原因是"磁盘不足"，请报告实际可用空间，不要重试。

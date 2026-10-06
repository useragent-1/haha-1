# dynamic-recon — 授权动态分析技能

## 适用范围 / Scope

仅对自研、公开无害样本或已获明确授权目标，在隔离 Linux 沙箱执行。先记录目标 SHA-256、命令、环境和超时；默认禁止访问生产凭据与真实用户数据。License/激活逻辑只定位，不提供绕过、patch、伪造响应或 keygen。任何失败都保留 stdout/stderr 与退出码，不把“工具启动”冒充“分析成功”。

## Environment preflight / 环境预检

```bash
# Linux sandbox
for x in gdb strace ltrace patchelf qemu-aarch64 frida-ps; do command -v "$x" || echo "$x 未安装"; done
python3 - <<'PY'
for m in ('angr','frida','capstone','unicorn'):
    try:
        x=__import__(m); print(m, 'OK', getattr(x,'__version__','unknown'))
    except Exception as e: print(m, '未安装', repr(e))
PY
```

缺失时安装：

```bash
# Linux sandbox
sudo apt-get update
sudo apt-get install -y gdb strace ltrace patchelf qemu-user
python3 -m pip install angr frida-tools 2>pip-install.err || \
  python3 -m pip install --break-system-packages angr frida-tools
```

## 1. 动态调试流程 / Dynamic debugging

先 baseline，再调试；所有执行均加超时，参数用数组传递。

```bash
# Linux sandbox
TARGET=/usr/bin/curl
sha256sum "$TARGET"; file "$TARGET"; ldd "$TARGET"
timeout 20s gdb -q -nx -batch \
  -ex 'set pagination off' -ex 'set debuginfod enabled off' \
  -ex 'starti' -ex 'info proc mappings' -ex 'info registers' \
  -ex 'x/8i $pc' -ex 'continue' --args "$TARGET" --version \
  >gdb-run.txt 2>&1; echo "exit=$?"
```

若要交互式单步，仅在隔离终端运行 `gdb --args TARGET ARG...`，记录断点、地址基址和 ASLR 状态；不要为“方便”关闭系统全局安全控制。

## 2. 崩溃复现与回溯 / Crash reproduction

```bash
# Linux sandbox
ulimit -c unlimited
ASAN_OPTIONS=abort_on_error=1:detect_leaks=1 timeout 20s ./authorized-target testcase.bin \
  >crash.stdout 2>crash.stderr; echo "$?" >crash.exit
gdb -q -nx -batch ./authorized-target core \
  -ex 'set pagination off' -ex 'info program' \
  -ex 'thread apply all bt full' -ex 'info registers' -ex 'x/16i $pc' \
  >gdb-crash.txt 2>&1
python3 scripts/dynamic/crash_trace.py gdb-crash.txt --format markdown -o crash-trace.md
```

固定输入、参数、环境变量和随机种子；报告信号、faulting PC、关键帧、Build ID，避免仅凭一次崩溃判定可利用性。

## 3. 系统调用与库调用追踪 / Syscall and library tracing

```bash
# Linux sandbox
mkdir -p trace
(timeout 20s strace -f -tt -T -yy -s 256 -o trace/strace.log -- /usr/bin/curl --version); echo "strace_exit=$?"
(timeout 20s ltrace -f -tt -T -s 256 -o trace/ltrace.log -- /usr/bin/curl --version); echo "ltrace_exit=$?"
python3 scripts/dynamic/behavior_report.py --strace trace/strace.log \
  --ltrace trace/ltrace.log -o trace/behavior
```

重点核对 `execve/clone/openat/write/connect`、动态加载、DNS/Unix socket、持久化路径和环境变量修改。网络观察优先使用无凭据、无副作用请求。

## 4. Hook 与插桩 / Hooking and instrumentation

```bash
# Linux sandbox: 先验证本机 Frida 设备/进程枚举
frida-ps
cat > /tmp/hook-open.js <<'JS'
const p = Module.findGlobalExportByName('open');
if (p) Interceptor.attach(p, { onEnter(args) { console.log('open=' + args[0].readUtf8String()); } });
JS
timeout 20s frida -f /usr/bin/curl -l /tmp/hook-open.js -- --version
```

Hook 输出可能含路径、请求头或凭据，提交报告前必须脱敏。优先 hook 稳定 ABI；记录模块基址、符号来源和 Frida 版本。

## 5. 反调试识别 / Anti-debug recognition

只识别和记录，不提供对商业授权/安全控制的绕过补丁。

```bash
# Linux sandbox
strings -a ./authorized-target | grep -Ei 'ptrace|TracerPid|/proc/self/status|seccomp|prctl|SIGTRAP' || true
strace -f -e trace=ptrace,prctl,seccomp,openat,read -o anti-debug.strace \
  timeout 15s ./authorized-target
sed -n '/ptrace\|TracerPid\|seccomp\|SIGTRAP/p' anti-debug.strace
```

区分 ptrace 互斥、时序检测、`TracerPid`、信号陷阱、seccomp 和完整性校验；观察失败时保留 `Operation not permitted` 等原文。

## 6. 内存 dump 与授权脱壳 / Memory dump and unpacking

```bash
# Linux sandbox; PID 必须属于本会话授权目标
PID=1234
cat /proc/$PID/maps > maps.txt
gcore -o memory-core "$PID"
gdb -q -nx -batch -p "$PID" \
  -ex 'info proc mappings' \
  -ex 'dump memory mapped-region.bin 0xSTART 0xEND' -ex detach -ex quit
# 仅在副本上检查解释器/RPATH，不修改原件
cp ./authorized-target ./working-copy
patchelf --print-interpreter ./working-copy
patchelf --print-rpath ./working-copy
```

地址必须来自同一进程的 `maps`，并记录 PIE/ASLR 基址。dump 后重新执行 `file/readelf/sha256sum`；重建导入表或 ELF 段时保留原始 dump。不得把脱壳用于规避许可验证。

## 7. 符号执行与路径探索 / Symbolic execution

```bash
# Linux sandbox
python3 - <<'PY'
import angr
p=angr.Project('/usr/bin/true', auto_load_libs=False)
s=p.factory.entry_state()
sm=p.factory.simulation_manager(s)
sm.run(n=25)
print({'active':len(sm.active),'deadended':len(sm.deadended),'errored':len(sm.errored)})
PY
```

对真实目标应设置 find/avoid 地址、输入长度、超时和状态上限；验证求解输入必须回到原二进制动态复现。路径爆炸不是“无路径”的证据。

## 8. 多架构模拟 / Multi-architecture emulation

```bash
# Linux sandbox
qemu-aarch64 --version; qemu-arm --version; qemu-mipsel --version
file ./authorized-arm64
# 动态链接样本需匹配 sysroot；静态样本可直接运行
timeout 20s qemu-aarch64 -strace ./authorized-arm64 arg1 >qemu.stdout 2>qemu.stderr
# 有匹配 rootfs 时：
timeout 20s qemu-aarch64 -L ./rootfs ./authorized-arm64 arg1
```

QEMU user-mode 不模拟完整内核、驱动、GUI 或硬件外设；syscall/ABI 差异必须标注，模拟结果要和真机或可信测试环境交叉验证。

## 自动化脚本 / Automation

### `scripts/dynamic/triage_run.sh`

```bash
scripts/dynamic/triage_run.sh --timeout 20 --output case/curl-dynamic -- /usr/bin/curl --version
```

输出 `status.tsv`、`summary.json`、`report.md`、baseline/strace/ltrace/gdb 原始日志。

**已知问题与限制：** 每阶段独立执行目标，会重复副作用；无容器级网络隔离；ptrace/seccomp/Yama 可令追踪失败；交互程序、守护进程和 GUI 覆盖有限；gdb 正常退出时不会产生崩溃帧。

### `scripts/dynamic/crash_trace.py`

```bash
python3 scripts/dynamic/crash_trace.py case/gdb.stdout --format json -o case/crash.json
```

从 GDB 原文提取信号、完整调用链、关键帧、寄存器和 `info proc mappings` 映射快照；JSON 保留全部映射，Markdown突出可执行段、stack/heap。

**已知问题与限制：** 解析常见英文 GDB 文本；本地化输出、损坏栈、优化/内联、缺失符号会降低准确度；映射快照要求输入包含 `info proc mappings`；它不做漏洞可利用性判定，也不替代 core dump 人工复核。

### `scripts/dynamic/api_extractor.py`

```bash
python3 scripts/dynamic/api_extractor.py ./web-source -o api-findings.json
```

**已知问题与限制：** 基于正则，只处理不超过 10 MiB 的文本文件；动态拼接、编码/加密、运行时解密、source map 外代码可能漏报；域名可能误报；Authorization 值只输出模式并强制打码。

### `scripts/dynamic/behavior_report.py`

```bash
python3 scripts/dynamic/behavior_report.py --strace trace/strace.log --ltrace trace/ltrace.log -o behavior
```

**已知问题与限制：** 仅总结可见 trace；内核模块/eBPF、其他 namespace、短生命周期并发、GUI 行为和被强反调试隐藏的活动可能不可见；网络只见连接参数，不解密 TLS；环境变量只保留名称不保留值。

## 沙箱不可覆盖项 / Sandbox boundaries

- 内核级 rootkit、驱动和 hypervisor 行为；
- 真实桌面 GUI、GPU、音视频和系统托盘交互；
- 需要真实 ARM/MIPS 硬件、专有外设或完整 Android/iOS 系统的行为；
- 强反调试、硬件断点检测、定制内核、可信执行环境；
- 未授权生产网络、真实账号、付费 License 激活链路。

上述项目只能明确标注“沙箱未覆盖/未实测”，不得伪造成功。

## 输出契约 / Output contract

报告至少包含：目标 hash/Build ID、完整命令、工具版本、超时、退出码、原始 stdout/stderr、行为时间线、崩溃关键帧、写文件/网络/持久化摘要、限制与未安装项。凭据只报告字段、位置、函数引用及脱敏指纹，绝不输出完整值。

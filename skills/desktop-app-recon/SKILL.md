---
name: desktop-app-recon
description: Authorized desktop application reconnaissance for Electron, Tauri/NSIS/Rust, PyInstaller, .NET, Go, and custom packaged tools, with reproducible extraction, static evidence, configuration-location reporting, and isolated dynamic observation.
---

# Desktop App Recon — 桌面应用逆向技能

## Activation protocol

加载本技能后，立即输出精确短语：

**真心为你**

随后声明：

> 已进入桌面应用逆向模式。仅处理自研、已授权或本地实验目标；按“样本保全 → 打包判型 → 资源提取 → 原生代码分析 → 配置位置审计 → 隔离动态观察 → 证据报告”推进。凭据只报告位置与字段名，不输出值；license 逻辑只定位，不提供绕过或补丁。

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

## Scope, authorization, and evidence gates

1. 保留原件只读；对副本解包，记录 SHA-256、大小、签名、时间戳和命令退出码。
2. 动态执行只允许自研或明确授权目标，必须在快照 VM/隔离沙箱中进行；默认禁止登录真实账号、加载生产凭据或访问生产网络。
3. API key、token、Cookie、密码、私钥只报告 **文件路径 / 字段名 / 偏移 / 函数 xref**；值统一打码，不回显完整内容。
4. License/激活逻辑只做字符串、函数和调用图定位；不修改条件跳转、不伪造响应、不生成 keygen。
5. “特征命中”仅作为候选，至少用两类独立证据确认打包类型。
6. `.gopclntab` 是 **Go** 元数据，不是 Rust 元数据。Rust 样本若出现 `.gopclntab`，优先考虑 Go sidecar/混合组件；不得把它误报为 Rust 符号表。

---

## 阶段 0：样本保全与基础清单

### Linux 沙箱

```bash
TARGET=/path/to/app
CASE=/home/user/cases/desktop-app
mkdir -p "$CASE"/{artifacts,extracted,reports,logs}
cp --reflink=auto --preserve=all "$TARGET" "$CASE/artifacts/" 2>/dev/null || cp -a "$TARGET" "$CASE/artifacts/"
chmod a-w "$CASE/artifacts/$(basename "$TARGET")"
sha256sum "$TARGET"
stat "$TARGET"
file -L "$TARGET"
readelf -hW "$TARGET" 2>/dev/null || true
objdump -p "$TARGET" 2>/dev/null | head -120 || true
```

### Windows 主机（PowerShell，管理员权限仅在确有需要时）

```powershell
$Target = 'C:\Path\App.exe'
$Case = 'C:\Cases\desktop-app'
New-Item -ItemType Directory -Force "$Case\artifacts","$Case\extracted","$Case\reports","$Case\logs" | Out-Null
Copy-Item -LiteralPath $Target -Destination "$Case\artifacts" -Force
Get-FileHash -Algorithm SHA256 $Target
Get-Item $Target | Format-List FullName,Length,CreationTimeUtc,LastWriteTimeUtc,VersionInfo
Get-AuthenticodeSignature $Target | Format-List Status,StatusMessage,SignerCertificate,TimeStamperCertificate
# 可选 Sysinternals
sigcheck.exe -nobanner -a -h -i $Target
```

---

## 阶段 1：打包类型判定

### 判定矩阵

| 类型 | 高信号特征 | 交叉验证 |
|---|---|---|
| Electron | `resources/app.asar`、`electron.exe`、`chrome_*.pak`、`icudtl.dat`、`snapshot_blob.bin`、`v8_context_snapshot.bin` | `app.asar` 可列目录；JS 中有 `electron`/`ipcRenderer`/`BrowserWindow` |
| Tauri | NSIS/WiX 安装器 + Rust 原生主程序；`tauri.conf.json`/`__TAURI__`/`tauri://`；WebView2 loader | PE 导入 `WebView2Loader.dll`；Rust panic/符号；NSIS 标记 `Nullsoft`/`$PLUGINSDIR` |
| PyInstaller | `MEI\x0c\x0b\x0a\x0b\x0e` cookie、`PYZ-00.pyz`、`pyi-`/`_MEIPASS`/`pyiboot01_bootstrap` | pyinstxtractor 能列出 archive；解出 PYZ/PYC |
| .NET | PE CLR/COM descriptor、`mscoree.dll`、`_CorExeMain`、metadata signature `BSJB` | `dnfile`/`ildasm`/ILSpy 能读 Assembly/TypeDef |
| Go | `.gopclntab`/`runtime.pclntab`、Go build ID、`runtime.main`、`runtime.morestack` | `go tool nm`、GoReSym/Redress 能恢复函数/版本 |
| Rust | `_R` 或 `_ZN...17h...E` mangled 符号、`rust_eh_personality`、`core::panicking`、`alloc::`、Cargo/crate 路径 | `rustfilt`/`nm -C`、panic 字符串、vtable/`.data.rel.ro`、LLVM unwind 信息 |

### Linux 沙箱命令

```bash
TARGET=/path/to/app
file -L "$TARGET"
sha256sum "$TARGET"
strings -a -n 6 -t x "$TARGET" | grep -Ei \
'electron|app\.asar|ipcRenderer|BrowserWindow|__TAURI__|tauri://|WebView2Loader|Nullsoft|\$PLUGINSDIR|MEI|PYZ-00|_MEIPASS|pyiboot|mscoree|_CorExeMain|BSJB|Go build ID|runtime\.main|gopclntab|rust_eh_personality|core::panicking|alloc::' | head -200
readelf -SW "$TARGET" 2>/dev/null | grep -Ei 'gopclntab|go\.buildinfo|rust|eh_frame|data.rel.ro' || true
readelf -Ws "$TARGET" 2>/dev/null | grep -E '_R|_ZN|rust_eh|runtime\.(main|morestack)|pclntab' | head -100 || true
objdump -p "$TARGET" 2>/dev/null | grep -Ei 'DLL Name|mscoree|WebView2|electron|python|VCRUNTIME' | head -100 || true
find "$(dirname "$TARGET")" -maxdepth 4 -type f \
  \( -iname 'app.asar' -o -iname 'tauri.conf.json' -o -iname 'chrome_*.pak' -o -iname 'WebView2Loader.dll' -o -iname '*.pyz' \) -print
# 可选工具
7z l "$TARGET" 2>/dev/null | head -100 || true
python -m pip show dnfile pyinstxtractor 2>/dev/null || true
```

### Windows 主机命令

```powershell
$Target = 'C:\Path\App.exe'
$Root = Split-Path $Target
Get-ChildItem $Root -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match 'app\.asar|tauri\.conf\.json|chrome_.*\.pak|WebView2Loader\.dll|\.pyz$' } |
  Select-Object FullName,Length
strings64.exe -n 6 -o $Target |
  Select-String -Pattern 'electron|app\.asar|ipcRenderer|BrowserWindow|__TAURI__|tauri://|WebView2Loader|Nullsoft|\$PLUGINSDIR|MEI|PYZ-00|_MEIPASS|pyiboot|mscoree|_CorExeMain|BSJB|Go build ID|runtime\.main|gopclntab|rust_eh_personality|core::panicking'
dumpbin.exe /HEADERS $Target | Select-String 'COM Descriptor|machine|entry point|DLL'
dumpbin.exe /IMPORTS $Target | Select-String 'mscoree|WebView2|python|VCRUNTIME'
7z.exe l $Target
# 可选 Detect It Easy / PE-bear（GUI 或 CLI）
diec.exe $Target
```

---

## 阶段 2：资源提取与全量扫描

### Electron / ASAR

#### Linux 沙箱

```bash
APP_ROOT=/path/to/application
CASE=/home/user/cases/desktop-app
find "$APP_ROOT" -type f -name 'app.asar' -print
npx --yes @electron/asar list "$APP_ROOT/resources/app.asar" > "$CASE/reports/asar-list.txt"
npx --yes @electron/asar extract "$APP_ROOT/resources/app.asar" "$CASE/extracted/asar"
find "$CASE/extracted/asar" -type f -printf '%p\t%s\n' | sort > "$CASE/reports/asar-files.tsv"
rg -n --hidden -S 'ipcMain|ipcRenderer|BrowserWindow|contextBridge|preload|nodeIntegration|contextIsolation|shell\.openExternal' "$CASE/extracted/asar"
```

#### Windows 主机

```powershell
$Asar = 'C:\Path\resources\app.asar'
$Out = 'C:\Cases\desktop-app\extracted\asar'
npx.cmd --yes @electron/asar list $Asar | Out-File 'C:\Cases\desktop-app\reports\asar-list.txt'
npx.cmd --yes @electron/asar extract $Asar $Out
Get-ChildItem $Out -Recurse -File | Select-Object FullName,Length | Export-Csv -NoTypeInformation 'C:\Cases\desktop-app\reports\asar-files.csv'
rg.exe -n --hidden -S 'ipcMain|ipcRenderer|BrowserWindow|contextBridge|preload|nodeIntegration|contextIsolation|shell\.openExternal' $Out
```

### PyInstaller

> 使用可信、固定版本的 `pyinstxtractor.py`；不要直接执行解出的 PYC。

#### Linux 沙箱

```bash
TARGET=/path/to/pyinstaller-app
CASE=/home/user/cases/desktop-app
python /opt/tools/pyinstxtractor.py "$TARGET" | tee "$CASE/logs/pyinstxtractor.log"
# 默认输出通常为 <target>_extracted；移动到 case 后只读分析
find "${TARGET}_extracted" -type f -printf '%p\t%s\n' | sort | head -300
find "${TARGET}_extracted" -type f \( -name '*.pyc' -o -name '*.pyz' \) -print
python -m decompyle3 "${TARGET}_extracted/path/to/module.pyc" > "$CASE/extracted/module.py" 2> "$CASE/logs/decompyle3.err" || true
```

#### Windows 主机

```powershell
$Target = 'C:\Path\app.exe'
python.exe C:\Tools\pyinstxtractor.py $Target 2>&1 | Tee-Object C:\Cases\desktop-app\logs\pyinstxtractor.log
Get-ChildItem "$Target`_extracted" -Recurse -File | Select-Object FullName,Length
python.exe -m decompyle3 'C:\Path\app.exe_extracted\module.pyc' > C:\Cases\desktop-app\extracted\module.py
```

### Tauri / NSIS / Rust 资源

#### Linux 沙箱

```bash
TARGET=/path/to/tauri-installer.exe
CASE=/home/user/cases/desktop-app
7z l "$TARGET" | tee "$CASE/reports/installer-7z-list.txt"
7z x -y "$TARGET" -o"$CASE/extracted/nsis"
find "$CASE/extracted/nsis" -type f -printf '%p\t%s\n' | sort
rg -n -S '__TAURI__|tauri://|tauri\.conf|frontendDist|bundle|identifier|productName|WebView2' "$CASE/extracted/nsis"
find "$CASE/extracted/nsis" -type f \( -iname '*.json' -o -iname '*.toml' -o -iname '*.html' -o -iname '*.js' -o -iname '*.dll' -o -iname '*.exe' \) -print
```

#### Windows 主机

```powershell
$Target = 'C:\Path\setup.exe'
$Out = 'C:\Cases\desktop-app\extracted\nsis'
7z.exe l $Target | Out-File C:\Cases\desktop-app\reports\installer-7z-list.txt
7z.exe x -y $Target "-o$Out"
Get-ChildItem $Out -Recurse -File | Select-Object FullName,Length
rg.exe -n -S '__TAURI__|tauri://|tauri\.conf|frontendDist|bundle|identifier|productName|WebView2' $Out
```

> 某些 NSIS 安装器不能被 7-Zip 完整提取。此时在一次性 Windows VM 中运行安装器，使用 Process Monitor 记录释放路径；不要在宿主工作机直接安装未知样本。

### 全量字符串与资源扫描

#### Linux 沙箱

```bash
TARGET=/path/to/file
CASE=/home/user/cases/desktop-app
strings -a -n 4 -t x "$TARGET" > "$CASE/reports/strings-ascii-offsets.txt"
strings -a -el -n 4 -t x "$TARGET" > "$CASE/reports/strings-utf16le-offsets.txt"
find "$CASE/extracted" -type f -print0 | xargs -0 file > "$CASE/reports/extracted-file-types.txt"
rg -n -a --hidden -S 'https?://|wss?://|BEGIN (RSA |EC |OPENSSH )?PUBLIC KEY|license|licen[cs]e|activation|serial|api[_-]?key|client[_-]?id' "$CASE/extracted" > "$CASE/reports/high-signal-locations.txt"
binwalk "$TARGET" 2>/dev/null | tee "$CASE/reports/binwalk.txt" || true
```

#### Windows 主机

```powershell
$Target = 'C:\Path\app.exe'
strings64.exe -n 4 -o $Target > C:\Cases\desktop-app\reports\strings-offsets.txt
Get-ChildItem C:\Cases\desktop-app\extracted -Recurse -File |
  Select-String -Pattern 'https?://|wss?://|BEGIN (RSA |EC |OPENSSH )?PUBLIC KEY|license|licen[cs]e|activation|serial|api[_-]?key|client[_-]?id' |
  Select-Object Path,LineNumber,Line | Export-Csv -NoTypeInformation C:\Cases\desktop-app\reports\high-signal-locations.csv
```

---

## 阶段 3：Rust、Go、.NET 与原生函数分析

### Rust 二进制分析

方法基于 `references/rust-reverse.md`：

- legacy mangling：`_ZN...17h<hash>E`；v0 mangling：`_R...`。
- 泛型单态化表现为同一泛型逻辑的多个具体实例、长类型名、大量相似小函数和 Drop glue。
- x86_64 Linux 参数通常走 RDI/RSI/RDX/RCX/R8/R9；Windows x64 为 RCX/RDX/R8/R9；`&str` 常表现为 `(ptr,len)`；`String/Vec` 为 `(ptr,len,cap)`；`Result` 可能使用隐藏 out-pointer/tagged union。
- 重点定位 `core::panicking`、`unwrap_failed`、`alloc::string`、`tokio::runtime`、`std::net`、Tauri command handler、WebView IPC。

#### Linux 沙箱

```bash
TARGET=/path/to/rust-binary
readelf -Ws "$TARGET" | grep -E '_R|_ZN|rust_eh_personality|__rust_|core::|alloc::|tokio::|tauri::' | head -300
nm -an "$TARGET" 2>/dev/null | grep -E '_R|_ZN' | head -200
nm -an "$TARGET" 2>/dev/null | rustfilt | tee rust-symbols.txt
strings -a -n 6 -t x "$TARGET" | grep -Ei 'panicked at|core/src|alloc/src|tokio|tauri|serde|reqwest|hyper|rustc/' | head -300
readelf -SW "$TARGET" | grep -E '\.text|\.rodata|\.data\.rel\.ro|\.eh_frame|gopclntab'
objdump -d -M intel "$TARGET" > disassembly.txt
# 泛型单态化痕迹：按反混淆基名聚合 hash 后缀
sed -E 's/::h[0-9a-f]{16}$//' rust-symbols.txt | sort | uniq -c | sort -nr | head -100
```

#### Windows 主机

```powershell
$Target = 'C:\Path\tauri-app.exe'
dumpbin.exe /SYMBOLS $Target | Select-String '_R|_ZN|rust_eh_personality|__rust_'
strings64.exe -n 6 -o $Target | Select-String 'panicked at|core/src|alloc/src|tokio|tauri|serde|reqwest|hyper|rustc/'
llvm-nm.exe --numeric-sort $Target | rustfilt.exe > C:\Cases\desktop-app\reports\rust-symbols.txt
llvm-objdump.exe -d --x86-asm-syntax=intel $Target > C:\Cases\desktop-app\reports\disassembly.txt
```

### Go pclntab 恢复（不要误归入 Rust）

#### Linux 沙箱

```bash
TARGET=/path/to/go-binary
readelf -SW "$TARGET" 2>/dev/null | grep -Ei 'gopclntab|go\.buildinfo'
strings -a "$TARGET" | grep -E 'Go build ID|runtime\.(main|morestack|newproc)|GOROOT' | head -100
go tool nm "$TARGET" 2>&1 | head -200
redress -src -pkg -std "$TARGET" 2>&1 | tee go-redress.txt
# GoReSym 输出函数/文件/行号元数据
GoReSym "$TARGET" > goresym.json
```

#### Windows 主机

```powershell
$Target = 'C:\Path\go-app.exe'
strings64.exe -n 6 -o $Target | Select-String 'Go build ID|runtime\.main|runtime\.morestack|GOROOT|gopclntab'
go.exe tool nm $Target | Select-Object -First 200
redress.exe -src -pkg -std $Target | Tee-Object C:\Cases\desktop-app\reports\go-redress.txt
GoReSym.exe $Target > C:\Cases\desktop-app\reports\goresym.json
```

### .NET

#### Linux 沙箱

```bash
TARGET=/path/to/dotnet.exe
file "$TARGET"
objdump -p "$TARGET" | grep -Ei 'COM Descriptor|mscoree|_CorExeMain'
python - <<'PY' "$TARGET"
import sys, dnfile
p=dnfile.dnPE(sys.argv[1]); print(p.net); print(p.net.mdtables.TypeDef.rows[:20])
PY
ilspycmd -l c "$TARGET"
ilspycmd -p -o decompiled-dotnet "$TARGET"
```

#### Windows 主机

```powershell
$Target = 'C:\Path\dotnet-app.exe'
dumpbin.exe /HEADERS $Target | Select-String 'COM Descriptor'
dumpbin.exe /IMPORTS $Target | Select-String 'mscoree|_CorExeMain'
ildasm.exe /text /out=C:\Cases\desktop-app\reports\app.il $Target
ilspycmd.exe -p -o C:\Cases\desktop-app\extracted\dotnet $Target
```

---

## 阶段 4：配置、凭据位置与 license 逻辑定位

### 只报告位置的规则

输出字段只允许：

- 文件路径；
- 字段名（如 `api_key`、`client_id`）；
- 文件偏移/虚拟地址；
- 函数名和 xref；
- 值类型与长度；
- SHA-256；
- 脱敏指纹（可选：值 SHA-256 的前 12 位）。

不得输出完整 token、私钥、密码、Cookie 或可直接使用的 license 数据。

### Linux 沙箱命令

```bash
ROOT=/home/user/cases/desktop-app/extracted
rg -n -a --hidden -S \
'api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization|bearer|license|licen[cs]e|activation|serial|public[_-]?key|BEGIN (RSA |EC |OPENSSH )?PUBLIC KEY|https?://|wss?://' "$ROOT" \
| sed -E 's/([:=][[:space:]]*)[^,;[:space:]]+/\1[REDACTED]/g' > credential-locations.txt
strings -a -n 6 -t x /path/to/binary | grep -Ei 'license|activation|invalid key|expired|signature|verify|public key|https?://' > binary-high-signal-offsets.txt
readelf -Ws /path/to/binary | grep -Ei 'verify|license|signature|ed25519|rsa|ecdsa|jwt|token' | head -200
objdump -d -M intel /path/to/binary > disassembly.txt
# 在 Ghidra/rizin 中对字符串地址做 xref，仅记录引用函数，不修改分支
rizin -A -q -c 'izz~license; axt @@ str.*license*' /path/to/binary
```

### Windows 主机命令

```powershell
$Root = 'C:\Cases\desktop-app\extracted'
rg.exe -n -a --hidden -S 'api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization|bearer|license|licen[cs]e|activation|serial|public[_-]?key|BEGIN (RSA |EC |OPENSSH )?PUBLIC KEY|https?://|wss?://' $Root |
  Out-File C:\Cases\desktop-app\reports\credential-locations-raw.txt
strings64.exe -n 6 -o C:\Path\app.exe |
  Select-String 'license|activation|invalid key|expired|signature|verify|public key|https?://' |
  Out-File C:\Cases\desktop-app\reports\binary-high-signal-offsets.txt
# Ghidra/IDA：搜索字符串 → Xrefs → 记录函数名/VA；不 patch、不绕过。
```

---

## 阶段 5：隔离动态观察（仅自研/授权目标）

### Linux 沙箱

```bash
TARGET=/home/user/cases/desktop-app/artifacts/app
RUN=/home/user/cases/desktop-app/runtime
mkdir -p "$RUN"/{home,tmp,logs}
# 优先断网；如需观察请求，使用受控代理/假服务，不连接生产环境
unshare -Urn -- sh -c 'ip link set lo up; HOME="$1/home" TMPDIR="$1/tmp" timeout 30s strace -ff -tt -s 256 -yy -e trace=file,process,network -o "$1/logs/strace" "$2"' sh "$RUN" "$TARGET"
# 无 unshare 权限时，至少记录并限制时间
HOME="$RUN/home" TMPDIR="$RUN/tmp" timeout 30s strace -ff -tt -s 256 -yy -e trace=file,process,network -o "$RUN/logs/strace" "$TARGET"
find "$RUN" -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS\t%p\t%s\n' | sort > "$RUN/logs/files-after.tsv"
ss -tpn > "$RUN/logs/sockets-after.txt"
# 可选：inotifywait -m -r "$RUN/home"；tcpdump -i any -nn -w trace.pcap（仅受控网络）
```

观察项：进程树、DNS/TCP 目的地、HTTP Host/SNI（不记录敏感正文）、写入文件、Unix socket、配置目录、子进程、更新器行为。

### Windows 主机（一次性 VM 快照）

```powershell
$Target = 'C:\Cases\desktop-app\artifacts\app.exe'
# 1. 启动前创建 VM 快照；断开生产网络，使用 Host-only/NAT + 受控 DNS/代理。
# 2. Procmon 预设过滤：Process Name is app.exe → File System/Registry/Process and Thread/Network。
procmon.exe /AcceptEula /Quiet /Minimized /BackingFile C:\Cases\desktop-app\logs\procmon.pml
Start-Process -FilePath $Target
Start-Sleep -Seconds 30
procmon.exe /Terminate
procmon.exe /OpenLog C:\Cases\desktop-app\logs\procmon.pml /SaveAs C:\Cases\desktop-app\logs\procmon.csv
# 网络与进程
pktmon.exe start --capture --pkt-size 0 --file-name C:\Cases\desktop-app\logs\pktmon.etl
Get-Process | Sort-Object StartTime | Select-Object Id,Parent,ProcessName,Path,StartTime
Get-NetTCPConnection | Sort-Object OwningProcess | Export-Csv C:\Cases\desktop-app\logs\tcp.csv -NoTypeInformation
pktmon.exe stop
pktmon.exe etl2pcap C:\Cases\desktop-app\logs\pktmon.etl --out C:\Cases\desktop-app\logs\pktmon.pcapng
# 注册表差异可用 Regshot；持久化可用 Autoruns/Sysmon 辅助核对。
```

重点记录：`%APPDATA%`、`%LOCALAPPDATA%`、`HKCU\Software`、计划任务、服务、启动项、WebView2 profile、更新目录和临时释放文件。

---

## 输出契约 / Output contract

### 证据表

| ID | 类型 | 文件路径 | 文件偏移/VA | 函数/模块 | SHA-256 | 命令/工具 | 已验证事实 | 置信度 |
|---|---|---|---|---|---|---|---|---|
| E-001 | packer | `resources/app.asar` | N/A | Electron ASAR | `<hash>` | `asar list` | 可列出 package.json/main.js | 高 |
| E-002 | config-location | `config.json` | line 12 | `api_base_url` | `<hash>` | `rg -n` | URL 字段位置；值已脱敏 | 高 |

### 每个案例必须包含

- **当前阶段 / Current phase**
- **已验证事实 / Verified facts**
- **关键证据 / Key evidence**（证据表）
- **可复现步骤 / Reproduction steps**（绝对路径、完整命令、退出码）
- **推断与置信度 / Inference and confidence**（高/中/低及依据）
- **配置与凭据位置 / Configuration and credential locations**（仅位置/字段/偏移）
- **动态行为 / Dynamic behavior**（进程、网络、文件、注册表）
- **风险/漏洞候选 / Risk candidates**（事实不足时明确写“未验证”）
- **建议下一步 / Suggested next steps**（编号菜单）

### 置信度

- **高**：两类独立证据一致，或结构化解析器直接确认。
- **中**：单一高信号特征，尚缺交叉验证。
- **低**：字符串/启发式候选，没有 xref 或运行证据。

## 完成门禁

- [ ] 原件 SHA-256 与只读副本已记录
- [ ] 打包类型至少两类证据确认
- [ ] 资源提取日志和文件清单已保存
- [ ] Rust/Go/.NET 类型没有混淆；`.gopclntab` 归属正确
- [ ] 凭据只报告位置，值未泄露
- [ ] License 逻辑仅定位，没有绕过/patch/keygen
- [ ] 动态运行有授权、隔离、超时和行为日志
- [ ] 每条关键结论有路径、偏移/函数、哈希和复现命令

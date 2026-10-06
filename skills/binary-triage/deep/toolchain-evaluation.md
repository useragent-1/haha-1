# 工具链实战评估

## 已验证成功
- `auto_analyze.py`：4/4 返回 0，均生成 JSON、Markdown 和 YARA 元数据。
- `find_crypto.py`：4/4 返回 0；准确定位 curl/libcurl Base64 表和 libcurl MD5 IV。
- `elf_deep_scan.py`：2/2 返回 0；缓解、ELF header、段/节信息可用。
- `yara_gen.py`：4/4 返回 0并生成规则文件。
- `shellcode_tools.py strings`：脚本和 JS 返回 0，但输出为空，信息价值有限。
- `bash -n`、readelf、objdump、od：成功支持脚本和函数级交叉验证。

## 报错与不一致（错误原文保留）

### 1. Ghidra 缺失
```text
GHIDRA_HOME not set and no installation found in common paths
```
影响：无法获得真正的反编译器伪代码；本次伪代码均明确为人工近似恢复。

### 2. xxd 在后续执行环境不存在
```text
/bin/bash: line 9: xxd: command not found
/bin/bash: line 11: xxd: command not found
/bin/bash: line 34: xxd: command not found
```
阶段 0 曾安装 xxd，但后续工具调用中不可见，说明依赖安装未跨执行边界持久化。已使用 `od` 完成偏移验证。

### 3. 独立 ROP 与 auto 内联结果冲突
```text
curl auto_analyze: 3565
curl standalone rop_finder: Found 0 raw gadgets ending in 'ret'
libcurl auto_analyze: 22440
libcurl standalone rop_finder: Found 0 raw gadgets ending in 'ret'
```
这是高优先级工具缺陷：两条路径显然使用了不同枚举逻辑，不能把任一数量直接作为可靠 gadget 结论。

### 4. 类型识别边界
`auto_analyze` 把 PIE `/usr/bin/curl` 报为 `ELF64 LE (shared library)`；原因是 ET_DYN 同时用于 PIE 和共享库。应结合 PT_INTERP、入口点和系统 `file` 修正为 PIE executable。

### 5. ELF 动态依赖解析不足
`elf_deep_scan` JSON 的 `dynamic.needed` 保存为 dynstr 偏移（如 `0x645`），而不是库名；报告中的 strings 列表能补充，但结构化字段应直接解析字符串。

### 6. JS 分析退化
- 29KB minified JS 只有 3 行，通用字符串提取仅得到 2 条。
- YARA `$s0` 近似整份 29KB JS，规则质量差且未通过编译验证。
- `shellcode_tools strings --obfuscated` 无输出；缺乏 JS parser/beautifier。

### 7. 生成报告辅助脚本曾失败，随后修复
首次错误：
```text
File "/home/user/make_case_reports.py", line 86
    if (!easy) return CURLE_BAD_FUNCTION_ARGUMENT;
    ^^
SyntaxError: f-string: expecting a valid expression after '{'
```
第二次错误：
```text
File "/home/user/make_case_reports.py", line 95
    }}}
      ^
SyntaxError: f-string: single '}' is not allowed
```
第三次编译检查错误：
```text
File "/home/user/make_case_reports.py", line 200
    let url = "https://react.dev/errors/" + code;
    ^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```
另一次生成评估报告时也因 f-string 中原样嵌入 `}}}` 触发：
```text
File "<stdin>", line 82
    }}}
      ^
SyntaxError: f-string: single '}' is not allowed
```
修复后最终结果：
```text
compile_exit=0
run_exit=0
```

## 缺失依赖原始输出
```text
$ command -v yara/ghidra/r2/xxd and Python imports
yara: not installed
ghidra: not installed
r2: not installed
xxd: not installed
capstone ERROR ModuleNotFoundError("No module named 'capstone'")
unicorn ERROR ModuleNotFoundError("No module named 'unicorn'")
elftools ERROR ModuleNotFoundError("No module named 'elftools'")
yara ERROR ModuleNotFoundError("No module named 'yara'")
lief ERROR ModuleNotFoundError("No module named 'lief'")

$ compare auto_analyze inline ROP vs standalone rop_finder
{
  "curl_auto_rop": 3565
}
{
  "libcurl_auto_rop": 22440
}
standalone curl: [*] Found 0 raw gadgets ending in 'ret'
standalone libcurl: [*] Found 0 raw gadgets ending in 'ret'

$ Ghidra status from auto reports
GHIDRA_HOME not set and no installation found in common paths
GHIDRA_HOME not set and no installation found in common paths

$ generated report helper final validation
compile_exit=0
run_exit=0
```

## 建议修复优先级
1. 统一 `auto_analyze` 与 `rop_finder.py` 的 gadget 枚举实现并增加回归测试。
2. 修复 PIE/DSO 分类和 DT_NEEDED/SONAME 字符串解析。
3. 给 JS 增加 token/AST 级字符串提取与最大 YARA 字符串长度。
4. `setup.sh` 在结束时重新 import/command 验证，并说明依赖是否会跨沙箱快照持久化。
5. 引入 YARA 编译测试；缺少 CLI/module 时明确标记“生成但未验证”。

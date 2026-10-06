# dynamic-recon deep

本目录保留动态分析实测证据：

- `curl-selftest.md`：完整测试命令、控制台、baseline 与 GDB 原始输出；
- `evidence/curl/`：未截断的 strace/ltrace/GDB/baseline 日志及结构化报告；
- `evidence/fixtures/`：API 抽取与真实 SIGSEGV 回溯解析 fixture 证据。

仓库脚本不依赖证据中的沙箱绝对路径。安全边界：仅限自研或已授权目标；内核级、真实 GUI、强反调试和专有硬件场景必须标注未覆盖。

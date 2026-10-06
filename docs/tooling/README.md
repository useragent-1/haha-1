# Full CLI toolchain evidence

- `tools-doctor-report.txt/json`: 164 项完整只读 doctor 结果；
- `install-status.tsv`: apt/pip/预编译/Git/编译与 fallback 状态流水；
- `install-failures/`: 最终三个 A 档失败项及 setup 首轮脚本错误原文。

初始 apt/PyPI/asset 失败后来通过 fallback 成功的项目，在 `TOOLS.md` 以最终状态“可用”记录；原失败仍留在 `/home/user/tool-install-logs/`。未执行外网扫描、口令攻击、隧道连接或凭据访问。

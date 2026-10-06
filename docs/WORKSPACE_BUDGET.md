# WORKSPACE_BUDGET

> 网络安全全栈 CLI 安装、缓存清理和 doctor 完成后的持久化候选预算。系统级 apt、`/usr/local`、`/opt` 不在 `/home/user` 快照内；必须依赖 setup 脚本重建，不能假定跨轮存在。

## 总体积

| 指标 | 当前值 | 上限 | 余量 |
|---|---:|---:|---:|
| 持久化候选字节 | 12,370,020 B（11.80 MiB） | 134,217,728 B（128 MiB） | 121,847,708 B（116.20 MiB） |
| 普通文件数 | 1,175 | 10,000 | 8,825 |
| 占用比例 | 9.22% | 100% | 90.78% |

结论：远低于 128 MiB；未逼近 100 MiB 清理线。已删除约 138 MiB pip cache、约 43 MiB Go module/build cache，并执行 `apt-get clean`。首次普通权限删除 Go cache失败的原文已保留，随后使用 sudo 成功清理。

## B档“仅记录”

| 工具 | 不安装原因 | 记录的安装方式 | 估计体积 |
|---|---|---|---:|
| metasploit-framework | 大型框架 | 官方 msfupdate/omnibus | 约1–2GB |
| ghidra | 大型 GUI 套件 | 官方 ZIP | 约1–2GB |
| ghidra-headless | 与 Ghidra 同包 | `support/analyzeHeadless` | 约1–2GB |
| rockyou | 大型词表 | `apt install wordlists` | 解压约130MB |
| SecLists | 大型词表仓库 | shallow clone | 约1GB以上 |

## `du -sh /home/user/*` 原始输出

```text
512	/home/user/ACTIVE_SESSION
512	/home/user/dynamic_angr_selftest_raw.txt
512	/home/user/dynamic_curl_triage_console_raw.txt
512	/home/user/dynamic_pip_install_stderr.txt
512	/home/user/git_clone_output.txt
512	/home/user/git_push_output.txt
512	/home/user/p1_curl_triage_console_raw.txt
512	/home/user/p2_anomaly_final_raw.txt
512	/home/user/p2_anomaly_raw.txt
512	/home/user/p2_fields_final_raw.txt
512	/home/user/p2_fields_raw.txt
512	/home/user/p2_fixture_final_raw.txt
512	/home/user/p2_fixture_raw.txt
512	/home/user/p2_pip_stderr.txt
512	/home/user/p2_rebuild_final_raw.txt
512	/home/user/p2_rebuild_raw.txt
512	/home/user/p3_endpoint_public_final_raw.txt
512	/home/user/p3_endpoint_public_raw.txt
512	/home/user/p3_secret_raw.txt
512	/home/user/p3_sourcemap_final_raw.txt
512	/home/user/p3_sourcemap_raw.txt
512	/home/user/p4_binwalk_check_raw.txt
512	/home/user/p4_strcrypto_final_raw.txt
512	/home/user/p4_strcrypto_raw.txt
512	/home/user/p5_batch_raw.txt
512	/home/user/p5_html_raw.txt
512	/home/user/setup_core_selftest_raw.txt
512	/home/user/submission_finish_raw.txt
4.0K	/home/user/P1_DYNAMIC_RECON_REPORT.md
4.0K	/home/user/WORKSPACE_BUDGET.md
4.0K	/home/user/cleanup_workspace.sh
4.0K	/home/user/dynamic_api_extractor_console_raw.txt
4.0K	/home/user/dynamic_apt_update_raw.txt
4.0K	/home/user/dynamic_behavior_console_raw.txt
4.0K	/home/user/dynamic_crash_parser_console_raw.txt
4.0K	/home/user/dynamic_setup_raw.txt
4.0K	/home/user/dynamic_tool_selftest_raw.txt
4.0K	/home/user/git_commit_output.txt
4.0K	/home/user/haha-1-agent-artifacts-2026-10-06.full-manifest.tsv
4.0K	/home/user/ligolo-ng.yaml
4.0K	/home/user/p1_behavior_raw.txt
4.0K	/home/user/p1_final_selftest_raw.txt
4.0K	/home/user/p2_pip_stdout.txt
4.0K	/home/user/p3_beautify_raw.txt
4.0K	/home/user/p4_pack_final_raw.txt
4.0K	/home/user/p4_pack_raw.txt
4.0K	/home/user/p4_unpack_chain_final_raw.txt
4.0K	/home/user/p4_unpack_chain_raw.txt
4.0K	/home/user/p4_upx_apt_raw.txt
4.0K	/home/user/p4_upx_version_raw.txt
4.0K	/home/user/p5_html_first30_raw.txt
4.0K	/home/user/phase0_safe_raw.txt
4.0K	/home/user/setup_core_selftest_final2_raw.txt
4.0K	/home/user/setup_core_selftest_final_raw.txt
4.0K	/home/user/setup_full_binary_git_raw.txt
4.0K	/home/user/setup_full_console_raw.txt
4.0K	/home/user/setup_full_fallbacks_raw.txt
4.0K	/home/user/submission_verify_raw.txt
8.0K	/home/user/LAST_TOOLPACKS_REPORT.md
8.0K	/home/user/build_submission.py
8.0K	/home/user/desktop_app_recon_report.md
8.0K	/home/user/dynamic_recon_report.md
8.0K	/home/user/memory_incremental_upgrade_report.md
8.0K	/home/user/p1_crash_trace.json
8.0K	/home/user/phases_6_7_raw.txt
8.0K	/home/user/setup_full_console_retry_raw.txt
12K	/home/user/MEMORY_UPDATE.md
12K	/home/user/dynamic_apt_install_raw.txt
12K	/home/user/local_recon_round4_safe_raw.txt
12K	/home/user/p1_recovery_raw.txt
12K	/home/user/tools_doctor_report.txt
16K	/home/user/dynamic_pip_install_stdout.txt
16K	/home/user/generate_tools_md.py
16K	/home/user/local_recon_round3_safe_raw.txt
16K	/home/user/local_recon_round4_report.md
20K	/home/user/local_recon_round3_report.md
20K	/home/user/p1_revalidation_raw.txt
24K	/home/user/TOOLS.md
28K	/home/user/local_recon_round2_report.md
28K	/home/user/local_recon_round2_safe_raw.txt
28K	/home/user/p2-protocol-test
40K	/home/user/ENV_FINGERPRINT.md
40K	/home/user/dynamic-fixtures
48K	/home/user/local_recon_raw.txt
48K	/home/user/local_recon_report.md
56K	/home/user/tools_doctor_report.json
60K	/home/user/phases_1_4_safe_raw.txt
61K	/home/user/p3-frontend-test
76K	/home/user/sandbox_recon_full_report.md
102K	/home/user/p4-upx-test
152K	/home/user/haha-1-agent-artifacts-2026-10-06.tar.gz
192K	/home/user/p5-report-test
217K	/home/user/dynamic-curl-triage
217K	/home/user/p1-curl-triage
572K	/home/user/submission
738K	/home/user/tool-install-logs
770K	/home/user/case
1.1M	/home/user/ha-ha
9.5M	/home/user/push-tmp
```

## 最大持久化候选文件

| 路径 | 字节 |
|---|---:|
| `push-tmp/scripts/net/unicornscan/configure` | 860,426 |
| `push-tmp/scripts/net/unicornscan/libs/libpcap-0.9.4.tar.gz` | 425,887 |
| `push-tmp/scripts/net/unicornscan/libs/libdnet-1.10.tar.gz` | 419,752 |
| `push-tmp/scripts/net/unicornscan/docs/latex2man/latex2man.ps` | 355,977 |
| `push-tmp/scripts/net/unicornscan/etc/ports.txt` | 354,215 |
| `push-tmp/scripts/net/unicornscan/libs/libltdl.tar.gz` | 339,741 |
| `push-tmp/scripts/net/unicornscan/aclocal.m4` | 249,493 |
| `push-tmp/scripts/net/unicornscan/docs/latex2man.tgz` | 235,520 |
| `push-tmp/scripts/net/unicornscan/libtool` | 226,391 |
| `push-tmp/scripts/net/unicornscan/etc/oui.txt` | 225,852 |
| `push-tmp/.git/objects/pack/pack-159a8c1ba29d02e753b8733bf441f0568e17d9ee.pack` | 220,928 |
| `push-tmp/scripts/net/unicornscan/m4/libtool.m4` | 212,250 |
| `push-tmp/scripts/net/unicornscan/docs/latex2man/latex2man.pdf` | 208,022 |
| `push-tmp/scripts/net/unicornscan/autostuff/ltmain.sh` | 196,440 |
| `ha-ha/.git/objects/pack/pack-61f3225ae8fa04d1d2b0b8ba324a902c82b26979.pack` | 186,298 |
| `case/arena-js/artifact/index.html` | 170,765 |
| `push-tmp/scripts/net/unicornscan/docs/Unicornscan-Getting_Started.pdf` | 159,288 |
| `haha-1-agent-artifacts-2026-10-06.tar.gz` | 153,675 |
| `push-tmp/references/arena/model-catalog.json` | 151,684 |
| `push-tmp/scripts/net/unicornscan/src/tools/p0f/ORIGINAL-p0f-TARBALL.tgz` | 119,407 |


## 不纳入持久依赖

- apt/pip 安装树、`/usr/local/bin` 预编译文件、`/opt/security-tools` 源码/venv；
- pip/Go/apt cache；
- Docker、GUI、真实硬件和长期服务。

# Changelog

All notable changes to this skill pack. Format loosely follows Keep a Changelog.

## [1.0.0] — 2026-10-18

### Added

- `references/rea-backend.md` — optional Rea MCP backend: probe order, capability routing, degradation matrix, evidence-ID alignment, engine-installation path.
- `SKILL.md` — `## Optional backend: Rea MCP` section; Rea inserted into the tool-selection priority; missing structural scanners and the six task-suite script groups documented.
- `tools/install_ghidra.ps1` — idempotent Windows installer for the Ghidra analysis engine (JDK 21 + Ghidra 12.1.x, resumable download, zip integrity check, user-scoped `JAVA_HOME` / `GHIDRA_INSTALL_DIR`).
- `scripts/tool_audit.py` — optional MCP backend probing (`detected` / `env-hint` / `unknown`; never false-negatives a host-injected server).
- `.github/workflows/tests.yml` — CI matrix (Ubuntu/Windows × Python 3.10/3.13) running `compileall` + `pytest`.
- `LICENSE` (MIT), `SECURITY.md`, `requirements-dev.txt`, this changelog.
- Tests: `test_docs_consistency.py` (documented paths, script inventory and skill routing cannot silently drift), `test_auto_analyze_detection.py` (detection precision), `test_rea_cli_contract.py` (skipped when Rea is absent).
- **Golden regression suite** (`test_parsers_golden.py` + `sample_factory.py`): minimal PE32+ / ELF64 / Mach-O 64 / DEX fixtures are built byte by byte in memory, so the expected machine type, section names, entry RVA, header sizes and hashes are known before the parser runs. The parsers must recover that ground truth, and the fixtures themselves are re-read with `struct` to prove they follow the format specs. No binary sample is committed.

### Changed

- `README.md` rewritten for human readers: coverage matrix, full script inventory, skill table, knowledge-base index, toolchain, optional backend, limits. Agent loading instructions folded into a collapsed section at the end.
- `references/evidence-reporting.md` — dual-track evidence identifiers (`ev_<sha256>` from Rea vs `E1..En` locally) with explicit anti-mixing rules.
- `AGENTS.md`, `docs/INDEX.md` — corrected stale counts (18 → 38 scripts, 7 → 8 skills, nonexistent `net/` removed).

### Fixed

- `tests/test_smoke.py` used to dirty the working tree: it drives the real CLIs, which write into `scripts/<module>/`, and those outputs were tracked. They are now ignored and untracked.
- Removed the vendored `tools/scripts/net/unicornscan` tree (324 files, 6.2 MB, **GPL**) from version control. `tools/setup_full.sh` already clones it at install time, and a GPL tree inside an MIT-licensed repository was a licensing defect, not a feature.
- `auto_analyze.py` anti-analysis scan matched plain substrings, so `.idata$2` (contains `ida`) flagged every MSVC binary with 8 "indicators" and a MEDIUM rating. Matching is now word-boundary based; `whoami.exe` reports 0 instead of 8.
- Timing APIs (`GetTickCount`, `QueryPerformanceCounter`, `rdtsc`) are imported by nearly every Windows program; they were moved out of the anti-analysis list into a separate `timing_api_imports` hint that never raises a risk level.
- `shellcode_tools.find_obfuscated_strings` flagged stack strings on any binary with >10 `0xC6` bytes (`MOV r/m8,imm8`), i.e. every compiled PE. The heuristic now requires >=20 occurrences and >=1% density, and reports `low` confidence instead of `medium`.
- `pe_deep_scan.py` packer detection matched section names as substrings, so every normal PE hit the `DAta` marker through its `.rdata` section and was reported as packed. Matching is exact now (ignoring a leading dot).
- `scripts/debugger_bridge.py` had **never been committed**: the `debugger_*.py` rule meant to ignore pipeline output also swallowed the wrapper itself, so a fresh clone was missing a documented script and three tests failed. Added an explicit negation.
- `scripts/dynamic/crash_trace.py` and `scripts/macho_scan.py` used f-string forms that only compile on 3.12+ (backslash inside an expression, same-quote nesting), which broke the Python 3.10 leg of the CI matrix. Values are now computed before interpolation.
- Windows CI runners keep a legacy code page, so every script printing Chinese aborted with `UnicodeEncodeError` when run as a subprocess. Test subprocesses now run with `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8` and decode output as UTF-8; the workflow sets the same variables at job level. The full matrix (Ubuntu/Windows × 3.10/3.13) is green.

## [0.9.0] — 2026-10-06

### Added

- `control/` multi-agent orchestration layer: `PROTOCOL.md` (control plane + blackboard + task queue), `AGENT_BRIEF.md` (W01–W10 worker boot), `ORCHESTRATOR_BRIEF.md` (dispatcher).
- Eight sub-skills under `skills/`: `binary-triage`, `desktop-app-recon`, `dynamic-recon`, `frontend-re`, `protocol-re`, `report-batch`, `sandbox-recon`, `unpack-deobfusc`, each with case artifacts.
- `tools/setup_advanced.sh` (third batch: r2ghidra, mono/wine/de4dot, memory forensics, intel/recon) and `tools/RUN_INSTALL.md` (staged install + verify + smoke).
- `docs/ARENA-PLATFORM-ARCHITECTURE.md`, `docs/SANDBOX-RECON-MATRIX.md`, `references/arena/model-catalog.json` (332-model snapshot).

### Fixed

- Three failed installs switched to GitHub sources; `tools/MISSING.md` records uninstalled inventory and coverage self-assessment.
- `.gitattributes` enforcing LF, so Windows checkouts cannot break the shell scripts.

## [0.1.0] — 2026-10-06 (initial import)

### Added

- Initial skill pack: `SKILL.md` activation protocol, 18 reference documents, analysis scripts (auto pipeline, triage, PE/ELF/Mach-O/DEX/.NET/APK scanners, crypto constants, ROP, shellcode, YARA), `tests/test_smoke.py` (46 smoke tests).

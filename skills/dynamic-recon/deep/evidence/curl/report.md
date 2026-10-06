# Dynamic Triage Report

- Target: `/usr/bin/curl`
- Started UTC: `2026-10-06T03:48:35Z`
- Timeout per stage: `20s`

## Stage status

| Stage | Exit code |
|---|---:|
| baseline | 0 |
| strace | 0 |
| ltrace | 0 |
| gdb | 0 |

## Artifacts

- `baseline.stderr`
- `baseline.stdout`
- `command.shell`
- `gdb.commands`
- `gdb.stderr`
- `gdb.stdout`
- `ltrace.log`
- `ltrace.stderr`
- `ltrace.stdout`
- `metadata.txt`
- `status.tsv`
- `strace.log`
- `strace.stderr`
- `strace.stdout`
- `summary.json`

> Exit 124 means timeout. ptrace restrictions may make strace/ltrace/gdb fail; inspect each `.stderr` verbatim.

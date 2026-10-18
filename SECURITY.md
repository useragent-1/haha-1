# Security Policy

## Scope

`reverse-flow` is a **local** reverse-engineering skill pack: prompts, Markdown knowledge, and stdlib-only Python scripts. It runs no server, exposes no network listener, and phones home to nothing.

## Authorized use

- Analyze artifacts you own or are authorized to analyze.
- Dynamic analysis, unpacking, exploit development, and malware-behavior validation are intended for isolated local sandboxes, CTF/lab targets, and authorized engagements.
- `tools/setup_*.sh` installs third-party tooling with `apt`/`git clone` and requires elevated privileges in a disposable sandbox. Review before running on a machine you care about.
- `scripts/*` treats the target artifact as read-only; derived files go to the `--out` directory.

## Known risk surface

| Component | Behavior |
|---|---|
| `scripts/shellcode_tools.py emulate` | Executes shellcode inside Unicorn's CPU emulator only — no host syscalls. |
| `scripts/debugger_bridge.py` | Emits x64dbg-Automate Python; it does not attach to or launch a debugger by itself. |
| `tools/setup_*.sh` | Installs packages and clones upstream repositories. Third-party trees under `tools/scripts/net/` are **not** vendored and carry their own licenses (e.g. unicornscan is GPL). |
| Rea MCP backend (optional) | Opens the target through Ghidra/IDA/Hopper providers in a separate process; the original bytes are never written. Requires explicit engine installation (see `tools/install_ghidra.ps1`). |

## Reporting a vulnerability

Open a private security advisory on this repository (Security → Advisories → "Report a vulnerability"). Please include the affected script, a minimal reproducer, and the observed impact. Do not attach live malware samples; describe the family and provide hashes instead.

Expected first response: 7 days.

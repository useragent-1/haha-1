# Crash Trace

- Signal: `SIGSEGV`
- Frames: 3

## Key frames

| # | Address | Function |
|---:|---|---|
| 0 | `0x0000555555555139` | `crash_here` |
| 1 | `0x000055555555514b` | `middle` |
| 2 | `0x0000555555555157` | `main` |

## Registers

- `r10` = `0x7fffffffe8b0`
- `r11` = `0x202`
- `r12` = `0x0`
- `r13` = `0x7fffffffec98`
- `r14` = `0x7ffff7ffd000`
- `r15` = `0x555555557e08`
- `r8` = `0x0`
- `r9` = `0x7ffff7fccaa0`
- `rax` = `0x0`
- `rbp` = `0x7fffffffeb50`
- `rbx` = `0x7fffffffec88`
- `rcx` = `0x555555557e08`
- `rdi` = `0x1`
- `rdx` = `0x7fffffffec98`
- `rip` = `0x555555555139`
- `rsi` = `0x7fffffffec88`
- `rsp` = `0x7fffffffeb50`

## Key memory mappings

Total mappings: 23

| Start | End | Perms | Offset | Path |
|---|---|---|---|---|
| `0x0000555555555000` | `0x0000555555556000` | `r-xp` | `0x1000` | `/home/user/dynamic-fixtures/crash` |
| `0x00007ffff7dea000` | `0x00007ffff7f4d000` | `r-xp` | `0x28000` | `/usr/lib/x86_64-linux-gnu/libc.so.6` |
| `0x00007ffff7fc5000` | `0x00007ffff7fc7000` | `r-xp` | `0x0` | `[vdso]` |
| `0x00007ffff7fc8000` | `0x00007ffff7ff0000` | `r-xp` | `0x1000` | `/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2` |
| `0x00007ffffffde000` | `0x00007ffffffff000` | `rw-p` | `0x0` | `[stack]` |
| `0xffffffffff600000` | `0xffffffffff601000` | `--xp` | `0x0` | `[vsyscall]` |

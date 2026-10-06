#!/usr/bin/env bash
# Authorized dynamic triage only. Runs a target under bounded strace/ltrace/gdb.
set -u

usage() {
  cat <<'EOF'
Usage: triage_run.sh [--timeout SECONDS] [--output DIR] -- TARGET [ARG ...]
Example: triage_run.sh --timeout 15 --output case/curl-dynamic -- /usr/bin/curl --version
EOF
}

TIMEOUT_SECS=15
OUT="dynamic-triage-$(date -u +%Y%m%dT%H%M%SZ)"
while (($#)); do
  case "$1" in
    --timeout) TIMEOUT_SECS=${2:?missing timeout}; shift 2 ;;
    --output) OUT=${2:?missing output}; shift 2 ;;
    --) shift; break ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done
(($#)) || { echo "error: TARGET is required" >&2; usage >&2; exit 2; }
[[ "$TIMEOUT_SECS" =~ ^[1-9][0-9]*$ ]] || { echo "error: timeout must be a positive integer" >&2; exit 2; }
TARGET=$1
[[ -f "$TARGET" && -x "$TARGET" ]] || { echo "error: target is not an executable file: $TARGET" >&2; exit 2; }
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
TARGET=$(readlink -f "$TARGET")
ARGS=("$@")
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)

printf '%q ' "${ARGS[@]}" > "$OUT/command.shell"
printf '\n' >> "$OUT/command.shell"
{
  echo "started_utc=$START"
  echo "target=$TARGET"
  file "$TARGET"
  sha256sum "$TARGET"
  uname -a
} > "$OUT/metadata.txt" 2>&1

run_stage() {
  local name=$1; shift
  local rc
  set +e
  timeout --signal=TERM --kill-after=2s "${TIMEOUT_SECS}s" "$@" >"$OUT/${name}.stdout" 2>"$OUT/${name}.stderr"
  rc=$?
  set -e
  printf '%s\t%s\n' "$name" "$rc" >> "$OUT/status.tsv"
  return 0
}

set -e
printf 'stage\texit_code\n' > "$OUT/status.tsv"
run_stage baseline "${ARGS[@]}"
run_stage strace strace -f -tt -T -yy -s 256 -o "$OUT/strace.log" -- "${ARGS[@]}"
run_stage ltrace ltrace -f -tt -T -s 256 -o "$OUT/ltrace.log" -- "${ARGS[@]}"

cat > "$OUT/gdb.commands" <<'EOF'
set pagination off
set confirm off
set print thread-events off
set debuginfod enabled off
handle SIGPIPE nostop noprint pass
python
import gdb
def dynamic_recon_stop(event):
    print("\n=== GDB_STOP_EVENT ===")
    try: gdb.execute("thread apply all bt full")
    except gdb.error as e: print("backtrace_error:", e)
    try: gdb.execute("info registers")
    except gdb.error as e: print("register_error:", e)
    try: gdb.execute("info proc mappings")
    except gdb.error as e: print("mapping_error:", e)
    try: gdb.execute("x/8i $pc")
    except gdb.error as e: print("disassembly_error:", e)
gdb.events.stop.connect(dynamic_recon_stop)
end
run
printf "\n=== GDB_POST_RUN ===\n"
info program
quit
EOF
run_stage gdb gdb -q -nx -batch -x "$OUT/gdb.commands" --args "${ARGS[@]}"

python3 - "$OUT" "$TARGET" "$START" "$TIMEOUT_SECS" <<'PY'
import csv, json, pathlib, sys, datetime
out=pathlib.Path(sys.argv[1]); target=sys.argv[2]; started=sys.argv[3]; timeout=int(sys.argv[4])
rows=list(csv.DictReader((out/'status.tsv').open(), delimiter='\t'))
report={
  'schema':'dynamic-recon/triage-v1', 'target':target, 'started_utc':started,
  'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'timeout_seconds':timeout, 'stages':rows,
  'artifacts':sorted(p.name for p in out.iterdir() if p.is_file()),
}
(out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Dynamic Triage Report','',f'- Target: `{target}`',f'- Started UTC: `{started}`',f'- Timeout per stage: `{timeout}s`','','## Stage status','','| Stage | Exit code |','|---|---:|']
lines += [f"| {r['stage']} | {r['exit_code']} |" for r in rows]
lines += ['','## Artifacts','']+[f'- `{p.name}`' for p in sorted(out.iterdir()) if p.is_file()]
lines += ['','> Exit 124 means timeout. ptrace restrictions may make strace/ltrace/gdb fail; inspect each `.stderr` verbatim.','']
(out/'report.md').write_text('\n'.join(lines))
PY

echo "dynamic triage complete: $OUT"
cat "$OUT/status.tsv"

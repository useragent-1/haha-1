#!/usr/bin/env bash
# Authorized sample only: identify UPX, unpack a copy, and record hashes/differences.
set -u
usage(){ echo "Usage: unpack_auto.sh --output DIR SAMPLE"; }
OUT=""
while (($#)); do case "$1" in --output) OUT=${2:?};shift 2;; -h|--help)usage;exit 0;; *)break;; esac;done
(($#==1)) && [[ -n "$OUT" ]] || { usage >&2;exit 2; }
SRC=$(readlink -f "$1"); [[ -f "$SRC" ]] || { echo "error: not a file: $SRC" >&2;exit 2; }
mkdir -p "$OUT"; OUT=$(cd "$OUT"&&pwd); cp --preserve=mode,timestamps "$SRC" "$OUT/original.bin"; cp "$SRC" "$OUT/unpacked.bin"
{
 echo "source=$SRC"; file "$SRC"; sha256sum "$SRC"; upx --version | head -3
} >"$OUT/metadata.txt" 2>&1
set +e
timeout 30s upx -t "$OUT/original.bin" >"$OUT/upx-test.stdout" 2>"$OUT/upx-test.stderr"; TEST_RC=$?
if [[ $TEST_RC -eq 0 ]]; then
 timeout 60s upx -d -f "$OUT/unpacked.bin" >"$OUT/upx-unpack.stdout" 2>"$OUT/upx-unpack.stderr"; UNPACK_RC=$?
else
 echo 'not identified as valid UPX by upx -t; no unpack attempted' >"$OUT/upx-unpack.stderr"; : >"$OUT/upx-unpack.stdout"; UNPACK_RC=3
fi
set -e
{
 echo -e 'stage\texit_code'; echo -e "upx-test\t$TEST_RC"; echo -e "upx-unpack\t$UNPACK_RC"
} >"$OUT/status.tsv"
sha256sum "$OUT/original.bin" "$OUT/unpacked.bin" >"$OUT/hashes.sha256"
file "$OUT/original.bin" "$OUT/unpacked.bin" >"$OUT/file.txt"
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)
python3 "$SCRIPT_DIR/dump_diff.py" "$OUT/original.bin" "$OUT/unpacked.bin" -o "$OUT/diff.json" --markdown "$OUT/diff.md" >"$OUT/diff.console" 2>&1
cat "$OUT/status.tsv"; cat "$OUT/hashes.sha256"; echo "output=$OUT"
[[ $UNPACK_RC -eq 0 ]]

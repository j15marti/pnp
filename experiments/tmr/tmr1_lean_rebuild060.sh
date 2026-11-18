#!/usr/bin/env bash
# Fresh proof-project rebuild and dual-kernel replay, not an executable SAT solver.
# Prerequisites: Linux, elan, git, go, cargo, jq, python3, sha256sum.
set -Eeuo pipefail
PIN=16a5ce41304fcdaea4e0be7c132e1c361dc26da5
MATHLIB=0df444a360eaa60ab8c11dca51a86af692955474
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:?Usage: bash tmr1_lean_rebuild060.sh ABSOLUTE_LOG_DIRECTORY}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/tmr1-lean060.XXXXXXXX")
finish() { rc=$?; trap - EXIT; printf '%s\n' "$rc" > "$OUT/exit-code.txt"; printf '%s\n' "$WORK" > "$OUT/build-directory.txt"; exit "$rc"; }
trap finish EXIT
exec > >(tee "$OUT/runner.log") 2>&1
for tool in elan git go cargo jq python3 sha256sum; do command -v "$tool" >/dev/null; done
printf 'UTC_START=%s\n' "$(date -u +%FT%TZ)"
uname -a; free -h; df -h "$WORK"
git init -q "$WORK/source"
git -C "$WORK/source" remote add origin https://github.com/anthropics/formal-math.git
git -C "$WORK/source" fetch --depth 1 origin "$PIN"
git -C "$WORK/source" checkout --detach FETCH_HEAD
test "$(git -C "$WORK/source" rev-parse HEAD)" = "$PIN"
cd "$WORK/source/eth"
test "$(tr -d '\r\n' < lean-toolchain)" = 'leanprover/lean4:v4.33.1'
python3 "$HERE/tmr1_lean_audit060.py" source "$WORK/source" > "$OUT/source-before.json"
elan toolchain install leanprover/lean4:v4.33.1
export PATH="$HOME/.elan/bin:$PATH"
export LEAN_NUM_THREADS=${LEAN_NUM_THREADS:-2}
export LEAN_ABORT_ON_PANIC=1
lean --version | tee "$OUT/lean-version.txt"
lake --version | tee "$OUT/lake-version.txt"
sha256sum "$(elan which lean)" "$(elan which lake)" > "$OUT/tool-binaries.sha256"
# Download only dependency cache into a fresh source tree, not cached eth proofs.
lake exe cache get 2>&1 | tee "$OUT/dependency-cache.log"
test "$(git -C .lake/packages/mathlib rev-parse HEAD)" = "$MATHLIB"
python3 "$HERE/tmr1_lean_audit060.py" dependencies "$WORK/source" > "$OUT/dependencies-before.json"
if [ -d .lake/build ] && find .lake/build -type f -name '*.olean' -print -quit | grep -q .; then
  echo 'Unexpected cached eth proof object before fresh build' >&2; exit 1
fi
lake build Solution 2>&1 | tee "$OUT/build-solution.log"
lake env lean scripts/PrintAxioms.lean 2>&1 | tee "$OUT/axioms.log"
python3 "$HERE/tmr1_lean_audit060.py" axioms "$OUT/axioms.log" > "$OUT/axioms.json"
export COMPARATOR_COMMIT=575674928e239f5bc452aab72d1dd7b0f1326494
export NANODA_COMMIT=68d5ca9db226849b41a6fff59d796ff19d0a8840
export LANDRUN_COMMIT=811cfff51ceaf3d9843708aa6d22e9b84ccac8b4
export LEAN4EXPORT_COMMIT=15f6055e299ad5b89345e533cc2192f4cc00f659
export TOOLS_DIR="$WORK/verification-tools"
export LOG_DIR="$OUT/comparator-logs"
bash ../.github/scripts/comparator-check.sh 2>&1 | tee "$OUT/dual-kernel.log"
python3 "$HERE/tmr1_lean_audit060.py" comparator "$OUT/comparator-logs/comparator.log" > "$OUT/comparator.json"
python3 "$HERE/tmr1_lean_audit060.py" source "$WORK/source" > "$OUT/source-after.json"
python3 "$HERE/tmr1_lean_audit060.py" dependencies "$WORK/source" > "$OUT/dependencies-after.json"
cmp "$OUT/source-before.json" "$OUT/source-after.json"
cmp "$OUT/dependencies-before.json" "$OUT/dependencies-after.json"
git diff --exit-code
printf 'INDEPENDENT_REPLAY_COMPLETE revision=%s UTC_END=%s\n' "$PIN" "$(date -u +%FT%TZ)" | tee "$OUT/SUCCESS.txt"

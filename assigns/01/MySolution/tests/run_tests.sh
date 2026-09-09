#!/bin/sh
#
# Build and run both the ATS original and the Python translation, then
# compare their outputs. Run from anywhere:
#
#     sh assigns/01/MySolution/tests/run_tests.sh
#
# Exits 0 only if every test passes. ATS tests are reported as SKIP, not as
# passes, if no ATS compiler can be found.

set -u

HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$(cd "$HERE/.." && pwd)
BUILD="$HERE/build"
PY=${PYTHON:-python3}

rm -rf "$BUILD"
mkdir -p "$BUILD"

pass=0
fail=0
skip=0

report() {
    # report <status> <name>
    printf '%-6s %s\n' "$1" "$2"
    case $1 in
        PASS) pass=$((pass + 1)) ;;
        FAIL) fail=$((fail + 1)) ;;
        SKIP) skip=$((skip + 1)) ;;
    esac
}

# ---------------------------------------------------------------- ATS setup

if [ -z "${PATSHOME:-}" ]; then
    for d in /opt/homebrew/Cellar/ats2-postiats/*/lib/ats2-postiats-* \
             /usr/local/Cellar/ats2-postiats/*/lib/ats2-postiats-* \
             /usr/local/lib/ats2-postiats-*; do
        if [ -d "$d" ]; then PATSHOME=$d; break; fi
    done
fi

HAVE_ATS=no
if [ -n "${PATSHOME:-}" ] && [ -d "$PATSHOME" ]; then
    PATH="$PATSHOME/bin:$PATH"
    export PATSHOME PATH
    if command -v patscc > /dev/null 2>&1; then HAVE_ATS=yes; fi
fi

if [ "$HAVE_ATS" = no ]; then
    echo "No ATS compiler found. Install it with:  brew install ats2-postiats"
    echo "The ATS half of the comparison will be skipped."
    echo
fi

echo "=== building ==="

if [ "$HAVE_ATS" = yes ]; then
    echo "PATSHOME=$PATSHOME"
    if (cd "$BUILD" && patscc -o queens_ats "$SRC/queens.dats") > "$BUILD/build.log" 2>&1; then
        report PASS "build: queens.dats compiles"
    else
        report FAIL "build: queens.dats compiles"
        cat "$BUILD/build.log"
        HAVE_ATS=no
    fi
fi

if [ "$HAVE_ATS" = yes ]; then
    # The probe driver needs the functions without the program's own main0.
    "$PY" "$HERE/strip_main0.py" "$SRC/queens.dats" "$BUILD/queens_lib.dats"
    cat "$BUILD/queens_lib.dats" "$HERE/probes_body.dats" > "$BUILD/probes.dats"
    if (cd "$BUILD" && patscc -o probes_ats probes.dats) >> "$BUILD/build.log" 2>&1; then
        report PASS "build: ATS probe driver compiles"
    else
        report FAIL "build: ATS probe driver compiles"
        cat "$BUILD/build.log"
        HAVE_ATS=no
    fi
fi

if "$PY" -m py_compile "$SRC/queens.py"; then
    report PASS "build: queens.py compiles"
else
    report FAIL "build: queens.py compiles"
fi

echo
echo "=== test 1: whole program, normal case ==="
echo "Runs each program with no arguments and compares all output."

"$PY" "$SRC/queens.py" > "$BUILD/queens_py.out" 2>&1
py_status=$?
[ $py_status -eq 0 ] && report PASS "queens.py exits 0" || report FAIL "queens.py exits $py_status"

if [ "$HAVE_ATS" = yes ]; then
    "$BUILD/queens_ats" > "$BUILD/queens_ats.out" 2>&1
    ats_status=$?
    [ $ats_status -eq 0 ] && report PASS "queens.dats exits 0" || report FAIL "queens.dats exits $ats_status"

    if diff -u "$BUILD/queens_ats.out" "$BUILD/queens_py.out" > "$BUILD/queens.diff"; then
        report PASS "whole-program output identical, byte for byte"
    else
        report FAIL "whole-program output differs"
        head -40 "$BUILD/queens.diff"
    fi
else
    report SKIP "queens.dats exits 0"
    report SKIP "whole-program output identical, byte for byte"
fi

if [ "$(grep -c '^Solution #' "$BUILD/queens_py.out")" = 92 ]; then
    report PASS "queens.py prints exactly 92 solutions"
else
    report FAIL "queens.py prints exactly 92 solutions"
fi

echo
echo "=== test 2: per-function probes, boundary and unusual cases ==="
echo "Exercises each function directly: rows off the ends of the board,"
echo "empty runs of dots, queens on a shared column and diagonal, and a"
echo "search with nothing left to try."

"$PY" "$HERE/probes.py" > "$BUILD/probes_py.out" 2>&1
[ $? -eq 0 ] && report PASS "Python probes run" || report FAIL "Python probes run"

if [ "$HAVE_ATS" = yes ]; then
    "$BUILD/probes_ats" > "$BUILD/probes_ats.out" 2>&1
    [ $? -eq 0 ] && report PASS "ATS probes run" || report FAIL "ATS probes run"

    if diff -u "$BUILD/probes_ats.out" "$BUILD/probes_py.out" > "$BUILD/probes.diff"; then
        report PASS "probe output identical across both languages"
    else
        report FAIL "probe output differs"
        cat "$BUILD/probes.diff"
    fi
else
    report SKIP "ATS probes run"
    report SKIP "probe output identical across both languages"
fi

echo
echo "=== test 3: own design ==="

echo "3a. Check the answer against an independent brute-force search."
if "$PY" "$HERE/validate_solutions.py"; then
    report PASS "answer confirmed by an independent search"
else
    report FAIL "answer confirmed by an independent search"
fi

echo "3b. The solution-count check must survive python -O."
if "$PY" -O -c "
import sys; sys.path.insert(0, '$SRC')
import queens
try:
    queens.assertloc(False)
except AssertionError:
    sys.exit(0)
sys.exit(1)
"; then
    report PASS "assertloc still fires under -O"
else
    report FAIL "assertloc still fires under -O"
fi

echo "3c. Every board row ends in a trailing space, as the original prints it."
# 8 rows for the diagonal board, then 8 for each of the 92 solutions.
expected_rows=$((8 + 92 * 8))
board_rows=$(grep -cE '^[.Q] ' "$BUILD/queens_py.out")
spaced_rows=$(grep -cE '^[.Q] .* $' "$BUILD/queens_py.out")
if [ "$board_rows" = "$expected_rows" ] && [ "$spaced_rows" = "$expected_rows" ]; then
    report PASS "all $expected_rows board rows keep the trailing space"
else
    report FAIL "board rows $board_rows, of which $spaced_rows end in a space, expected $expected_rows of each"
fi

echo
echo "=== summary ==="
echo "passed $pass, failed $fail, skipped $skip"
[ $fail -eq 0 ] || exit 1
exit 0

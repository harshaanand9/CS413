# Testing the translation

Both programs are built and run, and their outputs are compared. Everything
below is reproduced by one command from the repository root:

```
sh assigns/01/MySolution/tests/run_tests.sh
```

The script exits 0 only if every test passes. If no ATS compiler is
installed it reports the ATS half as SKIP rather than quietly passing.

## How the original is run

The ATS compiler is not part of a normal macOS install. It comes from
Homebrew:

```
brew install ats2-postiats
```

The script then finds `PATSHOME` under the Homebrew cellar on its own, and
builds the original with `patscc`. No manual environment setup is needed.

## What is being compared

Neither program reads input, so there are no inputs to vary. The comparison
is instead made at two levels: the whole program run end to end, and each
function driven directly by a pair of matching probe drivers.

The probe drivers are the point of the exercise. `tests/probes_body.dats`
and `tests/probes.py` print the same labels in the same order, one line per
probe, so `diff` on their outputs is a direct behavioural comparison of the
two implementations function by function. The ATS driver is compiled against
a copy of `queens.dats` with its `main0` mechanically removed by
`tests/strip_main0.py`, so the probes exercise the real definitions rather
than a second hand-maintained copy that could drift.

## The tests

### Test 1, normal case: the whole program

Run each program with no arguments and compare all output, which is the
diagonal board followed by all 92 solutions. The two outputs are compared
byte for byte, so a difference in spacing or in the order solutions are
found would fail. Both are also required to exit 0, which means the
program's own check that it found 92 solutions passed.

### Test 2, boundary and unusual cases: the probe drivers

Each function is driven directly, at and past its edges:

| Probe | Why it is interesting |
| --- | --- |
| `board_get` at rows -1, 8 and 100 | Off both ends of the board. The fallback returns 0, and the translation must agree. |
| `board_set` at rows -1 and 8 | Out of range, so the board must come back untouched. |
| The board reprinted after every `board_set` | A board is immutable in ATS. Python tuples must not be mutated either. |
| `print_dots(0)` and `print_dots(-1)` | The empty run of dots, printed inside brackets so an accidental space would show. |
| `print_row(0)` and `print_row(7)` | The two extreme rows, where one run of dots is empty. |
| `safety_test1` on the same square, same column, short diagonal and long diagonal | Every way two queens can attack, plus two safe pairs. |
| `safety_test2` with `i` of -1 | No rows left to check, so the answer is vacuously true. |
| `search` with `j` already past the last column | Nothing left to try, so it returns its counter untouched. Run with counters of 0 and 41 to show the counter is carried through rather than recomputed. |

### Test 3, own design

**3a. An independent search.** Comparing the translation against the
original proves only that they agree. If both misunderstood the puzzle they
would agree and both be wrong. So `tests/validate_solutions.py` works the
answer out a third way: it filters all 40320 permutations of the eight
columns using arithmetic written from the definition of the puzzle, then
parses the boards back out of the program's printed output and checks that
the two sets agree, that every printed board is legal, that none repeats,
and that they appear in depth-first order.

**3b. A regression test for the fix made in step 5.** The original calls
`assertloc`, which ATS cannot compile away, and the first generated
translation used a bare `assert`, which Python discards under `-O`. This
test runs the interpreter with `-O` and requires the check to still fire.
It fails against the code as first generated and passes against the code as
corrected.

**3c. Trailing spaces.** Every board row ends in a space before its newline,
because the original prints `"Q "` and `". "` and then a separate newline.
This is the easiest detail to lose when translating to a language whose
`print` appends its own newline. The test counts board rows and rows ending
in a space and requires both to equal 744, being 8 rows for the diagonal
board and 8 for each of the 92 solutions.

## Results

Recorded on the run below.

| | |
| --- | --- |
| Date | 2026-09-08 |
| Machine | macOS 15.6.1, arm64 |
| ATS compiler | ats2-postiats 0.4.2 via Homebrew |
| C backend | Apple clang version 17.0.0 (clang-1700.0.13.5) |
| Python | Python 3.13.5 |

All 13 tests pass and nothing is skipped.

```
=== building ===
PATSHOME=/opt/homebrew/Cellar/ats2-postiats/0.4.2_1/lib/ats2-postiats-0.4.2
PASS   build: queens.dats compiles
PASS   build: ATS probe driver compiles
PASS   build: queens.py compiles

=== test 1: whole program, normal case ===
Runs each program with no arguments and compares all output.
PASS   queens.py exits 0
PASS   queens.dats exits 0
PASS   whole-program output identical, byte for byte
PASS   queens.py prints exactly 92 solutions

=== test 2: per-function probes, boundary and unusual cases ===
Exercises each function directly: rows off the ends of the board,
empty runs of dots, queens on a shared column and diagonal, and a
search with nothing left to try.
PASS   Python probes run
PASS   ATS probes run
PASS   probe output identical across both languages

=== test 3: own design ===
3a. Check the answer against an independent brute-force search.
  ok   program printed 92 boards
  ok   independent search also finds 92
  ok   every printed board is legal
  ok   no board is printed twice
  ok   both searches agree on the set
  ok   printed in depth-first order
PASS   answer confirmed by an independent search
3b. The solution-count check must survive python -O.
PASS   assertloc still fires under -O
3c. Every board row ends in a trailing space, as the original prints it.
PASS   all 744 board rows keep the trailing space

=== summary ===
passed 13, failed 0, skipped 0
```

## The one test that failed while being written

The trailing-space test first asserted 800 rows, and failed at 744. The
program was right and the test was wrong: the arithmetic is 8 rows for the
diagonal board plus 8 for each of 92 solutions, which is 744, not 800. The
expectation now derives that number rather than stating it, so it cannot
drift again. It is recorded here because a test suite that has never
reported a failure has not really been tested either.

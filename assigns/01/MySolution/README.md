# Assignment 1: GitHub Repository and AI-Assisted Code Translation

The eight-queens puzzle, translated from ATS to Python 3, then reviewed and
tested against the original.

## Contents

| File | What it is |
| --- | --- |
| `queens.dats` | The original program, in ATS. Taken unmodified from the "Introduction to Programming in ATS" chapter on functions. |
| `queens.py` | The translation, in Python 3. |
| `AI-TRANSCRIPT.md` | Record of the interaction with the AI. |
| `TESTS.md` | The test plan and the recorded results of running it. |
| `tests/` | The test suite itself. |

## Running the programs

The translation needs nothing but Python 3:

```
python3 queens.py
```

The original needs the ATS compiler, which is not part of a normal macOS
install:

```
brew install ats2-postiats
patscc -o queens_ats queens.dats
./queens_ats
```

Both print the diagonal board, then all 92 solutions, and their output is
identical byte for byte.

## Running the tests

From the repository root:

```
sh assigns/01/MySolution/tests/run_tests.sh
```

The script builds both programs, compares them at the whole-program level and
function by function, and checks the answer against an independent search. It
exits 0 only if every test passes. Without an ATS compiler installed it
reports the ATS tests as skipped rather than passing them silently. See
`TESTS.md` for what each test covers and for the results of the last run.

## AI Reflection

The AI did a really good job at creating the foundation for the translated
code. With further prompting, the AI can further strengthen the translation
and clean up errors found in the code. The ninety two solutions were verified
in the first translation but several other errors were still left dormant. For
example, the AI found out that the assert statement silently disappeared from
the code during some test runs. This would mean that the solution count check
would not execute. But other than this mistake and one informal convention
used for an if statement's body, the AI made zero errors in the code after
further probing. The AI did make a mistake in generating a test case though.
It first asserted 800 rows for its trailing space test, a test which verifies
the outputted board configuration's Q and . placements. It then corrected
itself by asserted 744 rows which makes sense as 8+8*92 = 744. We do 8*92
because of the 8 rows per 92 solutions and we add another 8 due to the 8 rows
for the diagonal board. The AI generated code could not have been trusted
without testing, as only after further probing I found about the dormant
errors. AI made the efficiency in which I completed this assignment much
higher. I still had high level control over the AI, but instead of spending my
time trying to translate the code line by line and generate test cases for it,
I instead got to probe at the translated code for any potential errors and
described the sort of test cases I wanted.

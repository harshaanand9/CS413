#!/usr/bin/env python3
"""Own-design test: check the program's answer against an independent search.

The eight-queens program is its own worst judge. If the translation and the
original share a misunderstanding of the puzzle, comparing them to each other
proves nothing. So this test ignores both and works out the answer a
different way: it filters all 40320 permutations of the eight columns for the
ones with no two queens on a shared diagonal, using arithmetic written from
the definition of the puzzle rather than copied from the program.

It then parses the boards back out of the program's own printed output and
checks that the two sets agree, that every printed board is legal, that none
repeats, and that they come out in the order a depth-first search produces.
"""

import itertools
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
QUEENS = os.path.join(HERE, "..", "queens.py")


def legal(board) -> bool:
    """True when no two queens on this board attack each other."""
    return all(board[p] != board[q] and abs(p - q) != abs(board[p] - board[q])
               for p, q in itertools.combinations(range(8), 2))


def boards_from_output(text: str):
    """Recover the board of every solution the program printed."""
    lines = text.split("\n")
    boards, i = [], 0
    while i < len(lines):
        if lines[i].startswith("Solution #"):
            rows = lines[i + 2:i + 10]
            boards.append(tuple(r.split(" ").index("Q") for r in rows))
            i += 10
        else:
            i += 1
    return boards


def main() -> int:
    printed = boards_from_output(
        subprocess.run([sys.executable, QUEENS],
                       capture_output=True, text=True, check=True).stdout)
    expected = sorted(p for p in itertools.permutations(range(8)) if legal(p))

    checks = [
        ("program printed 92 boards", len(printed) == 92),
        ("independent search also finds 92", len(expected) == 92),
        ("every printed board is legal", all(legal(b) for b in printed)),
        ("no board is printed twice", len(set(printed)) == len(printed)),
        ("both searches agree on the set", sorted(printed) == expected),
        ("printed in depth-first order", printed == expected),
    ]

    failed = 0
    for name, ok in checks:
        print(("  ok   " if ok else "  FAIL ") + name)
        failed += 0 if ok else 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

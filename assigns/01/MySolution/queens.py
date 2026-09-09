#!/usr/bin/env python3
"""Example: Eight Queens Puzzle.

A Python 3 translation of queens.dats, the ATS solution given in
"Introduction to Programming in ATS" (Hongwei Xi), in the chapter on
functions. The translation follows the original function by function and
reproduces its output byte for byte.

One structural change is unavoidable. Every recursive function in the
original is tail-recursive, and the ATS compiler turns those tail calls into
local jumps, so the original runs in constant stack space. Python makes no
such guarantee. The chain of tail calls in [search] is 17685 calls long,
against a default recursion limit of 1000, so [search] is written here as a
loop that rebinds its parameters. Each rebinding is marked with the ATS call
it stands for.

The board accessors below are deliberately left in the long-winded form the
original uses. The book points out that they are unwieldy, and explains why:
a board is a tuple because arrays have not been introduced at that point in
the text. Collapsing them to bd[i] would read better as Python but would
stop being a translation of this program.
"""

import sys

N = 8  # HX: this should not be changed!

# A board configuration. Entry i is the column position of the queen piece on
# row i. This is the [int8] of the original, spelled out to the same width.
Board = tuple[int, int, int, int, int, int, int, int]


def print_dots(i: int) -> None:
    if i > 0:
        sys.stdout.write(". ")
        print_dots(i - 1)
# end of [print_dots]


def print_row(i: int) -> None:
    print_dots(i)
    sys.stdout.write("Q ")
    print_dots(N - i - 1)
    sys.stdout.write("\n")
# end of [print_row]


def print_newline() -> None:
    """Print a newline, then flush standard output, as the ATS function does."""
    sys.stdout.write("\n")
    sys.stdout.flush()
# end of [print_newline]


def print_board(bd: Board) -> None:
    print_row(bd[0])
    print_row(bd[1])
    print_row(bd[2])
    print_row(bd[3])
    print_row(bd[4])
    print_row(bd[5])
    print_row(bd[6])
    print_row(bd[7])
    print_newline()
# end of [print_board]


def board_get(bd: Board, i: int) -> int:
    if i == 0:
        return bd[0]
    elif i == 1:
        return bd[1]
    elif i == 2:
        return bd[2]
    elif i == 3:
        return bd[3]
    elif i == 4:
        return bd[4]
    elif i == 5:
        return bd[5]
    elif i == 6:
        return bd[6]
    elif i == 7:
        return bd[7]
    else:
        return 0  # end of [if]
# end of [board_get]


def board_set(bd: Board, i: int, j: int) -> Board:
    (x0, x1, x2, x3, x4, x5, x6, x7) = bd
    if i == 0:
        x0 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 1:
        x1 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 2:
        x2 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 3:
        x3 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 4:
        x4 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 5:
        x5 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 6:
        x6 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 7:
        x7 = j
        return (x0, x1, x2, x3, x4, x5, x6, x7)
    else:
        return bd  # end of [if]
# end of [board_set]


def safety_test1(i0: int, j0: int, i: int, j: int) -> bool:
    """Can a queen on row i0, column j0 capture one on row i, column j?

    [abs] is the absolute value function.
    """
    return j0 != j and abs(i0 - i) != abs(j0 - j)
# end of [safety_test1]


def safety_test2(i0: int, j0: int, bd: Board, i: int) -> bool:
    """Can a queen on row i0, column j0 capture any piece on a row <= i?"""
    if i >= 0:
        if safety_test1(i0, j0, i, board_get(bd, i)):
            return safety_test2(i0, j0, bd, i - 1)
        else:
            return False
        # end of [if]
    else:
        return True  # end of [if]
# end of [safety_test2]


def search(bd: Board, i: int, j: int, nsol: int) -> int:
    """A standard depth-first search. Returns the number of distinct solutions.

    Each [continue] below stands for one tail call in the original, and the
    assignment preceding it binds that call's arguments. Python evaluates the
    whole right-hand side before rebinding any name, so the backtracking case
    still reads the old [i] when it calls board_get.
    """
    while True:
        if j < N:
            test = safety_test2(i, j, bd, i - 1)
            if test:
                bd1 = board_set(bd, i, j)
                if i + 1 == N:
                    sys.stdout.write("Solution #" + str(nsol + 1) + ":\n\n")
                    print_board(bd1)
                    # search (bd, i, j+1, nsol+1)
                    bd, i, j, nsol = bd, i, j + 1, nsol + 1
                    continue
                else:
                    # search (bd1, i+1, 0, nsol): positioning next piece
                    bd, i, j, nsol = bd1, i + 1, 0, nsol
                    continue
                # end of [if]
            else:
                # search (bd, i, j+1, nsol)
                bd, i, j, nsol = bd, i, j + 1, nsol
                continue
            # end of [if]
        else:
            if i > 0:
                # search (bd, i-1, board_get (bd, i-1) + 1, nsol)
                bd, i, j, nsol = bd, i - 1, board_get(bd, i - 1) + 1, nsol
                continue
            else:
                return nsol
            # end of [if]
# end of [search]


def assertloc(test: bool) -> None:
    """Translation of the ATS [assertloc].

    Written out as an explicit raise rather than Python's [assert] statement,
    because [assert] is discarded when the interpreter runs under -O. ATS
    offers no such escape, and a check that can vanish is not the same check.
    The traceback of the raised error reports the failing line, which is the
    location that [assertloc] would have printed.
    """
    if not test:
        raise AssertionError("assertion failed")
# end of [assertloc]


def main0() -> None:
    print_board((0, 1, 2, 3, 4, 5, 6, 7))
    nsol = search((0, 0, 0, 0, 0, 0, 0, 0), 0, 0, 0)
    assertloc(nsol == 92)
# end of [main0]


if __name__ == "__main__":
    main0()

# end of [queens.py]

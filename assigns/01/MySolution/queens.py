#!/usr/bin/env python3
#
# Example: Eight Queens Puzzle
#
# A Python 3 translation of queens.dats, the ATS solution given in
# "Introduction to Programming in ATS" (Hongwei Xi), chapter on functions.
# The translation follows the original function by function and aims to
# reproduce its output byte for byte.
#
# One structural change is unavoidable. Every recursive function in the
# original is tail-recursive, and the ATS compiler turns those tail calls
# into local jumps, so the original runs in constant stack space. Python
# has no such guarantee, so [search], whose chain of tail calls is many
# thousands of frames deep, is written below as a loop that rebinds its
# parameters. The shallow recursions ([print_dots], [safety_test2]) never
# exceed a depth of 8 and are left recursive, as in the original.

import sys

N = 8  # HX: this should not be changed!

# A board configuration is an 8-tuple of ints. Entry i is the column
# position of the queen piece on row i. This is the [int8] of the original.


def print_dots(i):
    # type: (int) -> None
    if i > 0:
        sys.stdout.write(". ")
        print_dots(i - 1)
# end of [print_dots]


def print_row(i):
    # type: (int) -> None
    print_dots(i)
    sys.stdout.write("Q ")
    print_dots(N - i - 1)
    sys.stdout.write("\n")
# end of [print_row]


def print_newline():
    # type: () -> None
    # Prints a newline and then flushes standard output, as in ATS.
    sys.stdout.write("\n")
    sys.stdout.flush()
# end of [print_newline]


def print_board(bd):
    # type: (tuple) -> None
    print_row(bd[0]); print_row(bd[1]); print_row(bd[2]); print_row(bd[3])
    print_row(bd[4]); print_row(bd[5]); print_row(bd[6]); print_row(bd[7])
    print_newline()
# end of [print_board]


def board_get(bd, i):
    # type: (tuple, int) -> int
    if i == 0: return bd[0]
    elif i == 1: return bd[1]
    elif i == 2: return bd[2]
    elif i == 3: return bd[3]
    elif i == 4: return bd[4]
    elif i == 5: return bd[5]
    elif i == 6: return bd[6]
    elif i == 7: return bd[7]
    else: return 0  # end of [if]
# end of [board_get]


def board_set(bd, i, j):
    # type: (tuple, int, int) -> tuple
    (x0, x1, x2, x3, x4, x5, x6, x7) = bd
    if i == 0:
        x0 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 1:
        x1 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 2:
        x2 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 3:
        x3 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 4:
        x4 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 5:
        x5 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 6:
        x6 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    elif i == 7:
        x7 = j; return (x0, x1, x2, x3, x4, x5, x6, x7)
    else:
        return bd  # end of [if]
# end of [board_set]


def safety_test1(i0, j0, i, j):
    # type: (int, int, int, int) -> bool
    # Tests whether a queen on row i0, column j0 can capture one on row i,
    # column j. [abs] is the absolute value function.
    return j0 != j and abs(i0 - i) != abs(j0 - j)
# end of [safety_test1]


def safety_test2(i0, j0, bd, i):
    # type: (int, int, tuple, int) -> bool
    # Tests whether a queen on row i0, column j0 can capture any piece on
    # the given board sitting on a row numbered i or less.
    if i >= 0:
        if safety_test1(i0, j0, i, board_get(bd, i)):
            return safety_test2(i0, j0, bd, i - 1)
        else:
            return False
        # end of [if]
    else:
        return True  # end of [if]
# end of [safety_test2]


def search(bd, i, j, nsol):
    # type: (tuple, int, int, int) -> int
    # A standard depth-first search. Returns the number of distinct
    # solutions found. Each [continue] below stands for one tail call in
    # the original; the assignment preceding it binds that call's
    # arguments. Python evaluates the whole right-hand side before
    # rebinding, so the backtracking case still reads the old [i].
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


def main0():
    # type: () -> None
    print_board((0, 1, 2, 3, 4, 5, 6, 7))
    nsol = search((0, 0, 0, 0, 0, 0, 0, 0), 0, 0, 0)
    assert nsol == 92
# end of [main0]


if __name__ == "__main__":
    main0()

# end of [queens.py]

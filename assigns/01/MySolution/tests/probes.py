#!/usr/bin/env python3
"""Probe driver for the Python translation.

Prints one labelled line per probe. tests/probes_body.dats prints exactly
the same labels from the ATS original, so the two outputs can be compared
with diff. Any behavioural difference between the two implementations shows
up as a differing line.

The probes are kept in the same order, with the same wording, as the ATS
driver. Keep the two in step when editing either.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from queens import (N, board_get, board_set, print_board, print_dots,
                    print_newline, print_row, safety_test1, safety_test2,
                    search)

out = sys.stdout.write


def pb(b: bool) -> None:
    out("true" if b else "false")


def pbd(bd) -> None:
    out("(" + ",".join(str(x) for x in bd) + ")")


# Own design: board_set followed by board_get must return what was set, for
# every row and every column. Exhaustive over all 64 pairs.
def rt_j(bd, i: int, j: int) -> bool:
    if j >= 0:
        if board_get(board_set(bd, i, j), i) == j:
            return rt_j(bd, i, j - 1)
        return False
    return True


def rt_i(bd, i: int) -> bool:
    if i >= 0:
        if rt_j(bd, i, N - 1):
            return rt_i(bd, i - 1)
        return False
    return True


# Own design: safety_test1 must be symmetric. Two queens either attack each
# other or they do not; the answer cannot depend on which is named first.
def sym_j(i0: int, j0: int, i: int, j: int) -> bool:
    if j >= 0:
        if safety_test1(i0, j0, i, j) == safety_test1(i, j, i0, j0):
            return sym_j(i0, j0, i, j - 1)
        return False
    return True


def sym_i(i0: int, j0: int, i: int) -> bool:
    if i >= 0:
        if sym_j(i0, j0, i, N - 1):
            return sym_i(i0, j0, i - 1)
        return False
    return True


def main() -> None:
    bd = (3, 1, 4, 1, 5, 9, 2, 6)
    sol = (0, 4, 7, 5, 2, 6, 1, 3)
    diag = (0, 1, 2, 3, 4, 5, 6, 7)
    zero = (0, 0, 0, 0, 0, 0, 0, 0)

    # ---- normal case: board_get on every legal row
    out("== board_get, rows 0 to 7 ==\n")
    for i in range(8):
        out("get " + str(i) + " = " + str(board_get(bd, i)) + "\n")

    # ---- boundary: board_get off the ends of the board
    out("== board_get, out of range ==\n")
    out("get -1 = " + str(board_get(bd, -1)) + "\n")
    out("get 8 = " + str(board_get(bd, 8)) + "\n")
    out("get 100 = " + str(board_get(bd, 100)) + "\n")

    # ---- normal case: board_set on the first, middle and last rows
    out("== board_set ==\n")
    out("set 0 7 = "); pbd(board_set(bd, 0, 7)); out("\n")
    out("set 3 3 = "); pbd(board_set(bd, 3, 3)); out("\n")
    out("set 7 0 = "); pbd(board_set(bd, 7, 0)); out("\n")

    # ---- boundary: board_set off the ends returns the board untouched
    out("== board_set, out of range ==\n")
    out("set -1 5 = "); pbd(board_set(bd, -1, 5)); out("\n")
    out("set 8 5 = "); pbd(board_set(bd, 8, 5)); out("\n")

    # ---- boundary: the original board must be unchanged by any of the above
    out("bd after sets = "); pbd(bd); out("\n")

    # ---- normal and boundary: safety_test1
    out("== safety_test1 ==\n")
    out("same square = "); pb(safety_test1(0, 0, 0, 0)); out("\n")
    out("same column = "); pb(safety_test1(0, 0, 1, 0)); out("\n")
    out("diagonal = "); pb(safety_test1(0, 0, 1, 1)); out("\n")
    out("long diagonal = "); pb(safety_test1(0, 7, 7, 0)); out("\n")
    out("knight-ish safe = "); pb(safety_test1(0, 0, 1, 2)); out("\n")
    out("far safe = "); pb(safety_test1(0, 0, 7, 3)); out("\n")

    # ---- boundary: safety_test2 with no rows to check is vacuously true
    out("== safety_test2 ==\n")
    out("vacuous -1 = "); pb(safety_test2(4, 4, bd, -1)); out("\n")
    out("sol row 7 = "); pb(safety_test2(7, 3, sol, 6)); out("\n")
    out("sol row 1 = "); pb(safety_test2(1, 4, sol, 0)); out("\n")
    out("clash col = "); pb(safety_test2(1, 0, sol, 0)); out("\n")
    out("clash diag = "); pb(safety_test2(1, 1, sol, 0)); out("\n")

    # ---- boundary: print_dots at and below zero prints nothing
    out("== print_dots ==\n")
    out("dots 0 = ["); print_dots(0); out("]\n")
    out("dots -1 = ["); print_dots(-1); out("]\n")
    out("dots 3 = ["); print_dots(3); out("]\n")

    # ---- boundary: the two extreme rows, where a run of dots is empty
    out("== print_row ==\n")
    print_row(0)
    print_row(3)
    print_row(7)

    # ---- normal case: whole boards
    out("== print_board diagonal ==\n")
    print_board(diag)
    out("== print_board known solution ==\n")
    print_board(sol)

    # ---- boundary: search with nothing left to try returns its counter as is
    out("== search, immediate return ==\n")
    out("j past end, nsol 0 = " + str(search(zero, 0, N, 0)) + "\n")
    out("j past end, nsol 41 = " + str(search(zero, 0, N, 41)) + "\n")

    # ---- own design: the two properties checked exhaustively
    out("== properties ==\n")
    out("set/get round trip = "); pb(rt_i(bd, N - 1)); out("\n")
    out("safety_test1 symmetric from (0,0) = "); pb(sym_i(0, 0, N - 1)); out("\n")
    out("safety_test1 symmetric from (3,5) = "); pb(sym_i(3, 5, N - 1)); out("\n")

    print_newline()


if __name__ == "__main__":
    main()

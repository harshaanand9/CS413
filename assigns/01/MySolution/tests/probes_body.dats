(* ****** ****** *)
//
// Probe driver for the ATS original.
//
// Prints one labelled line per probe. tests/probes.py prints exactly the
// same labels from the Python translation, so the two outputs can be
// compared with diff. Any difference in a function's behaviour between the
// two implementations shows up as a differing line.
//
// This file is concatenated onto a main0-free copy of queens.dats, so the
// functions probed below are the very ones the real program runs.
//
(* ****** ****** *)

fun pb (b: bool): void = if b then print "true" else print "false"

fun pbd (bd: int8): void = begin
  print "(";
  print bd.0; print ","; print bd.1; print ","; print bd.2; print ",";
  print bd.3; print ","; print bd.4; print ","; print bd.5; print ",";
  print bd.6; print ","; print bd.7;
  print ")"
end // end of [pbd]

(* ****** ****** *)
//
// Own design: board_set followed by board_get must return what was set,
// for every row and every column. Exhaustive over all 64 pairs.
//
fun rt_j (bd: int8, i: int, j: int): bool =
  if j >= 0 then (
    if board_get (board_set (bd, i, j), i) = j
      then rt_j (bd, i, j-1) else false
  ) else true
// end of [rt_j]

fun rt_i (bd: int8, i: int): bool =
  if i >= 0 then (
    if rt_j (bd, i, N-1) then rt_i (bd, i-1) else false
  ) else true
// end of [rt_i]

//
// Own design: safety_test1 must be symmetric. Two queens either attack each
// other or they do not; the answer cannot depend on which one is named first.
//
fun sym_j (i0: int, j0: int, i: int, j: int): bool =
  if j >= 0 then (
    if safety_test1 (i0, j0, i, j) = safety_test1 (i, j, i0, j0)
      then sym_j (i0, j0, i, j-1) else false
  ) else true
// end of [sym_j]

fun sym_i (i0: int, j0: int, i: int): bool =
  if i >= 0 then (
    if sym_j (i0, j0, i, N-1) then sym_i (i0, j0, i-1) else false
  ) else true
// end of [sym_i]

(* ****** ****** *)

implement
main0 () = {
//
val bd: int8 = @(3, 1, 4, 1, 5, 9, 2, 6)
val sol: int8 = @(0, 4, 7, 5, 2, 6, 1, 3)
val diag: int8 = @(0, 1, 2, 3, 4, 5, 6, 7)
val zero: int8 = @(0, 0, 0, 0, 0, 0, 0, 0)
//
// ---- normal case: board_get on every legal row
//
val () = print "== board_get, rows 0 to 7 ==\n"
val () = (print "get 0 = "; print (board_get (bd, 0)); print "\n")
val () = (print "get 1 = "; print (board_get (bd, 1)); print "\n")
val () = (print "get 2 = "; print (board_get (bd, 2)); print "\n")
val () = (print "get 3 = "; print (board_get (bd, 3)); print "\n")
val () = (print "get 4 = "; print (board_get (bd, 4)); print "\n")
val () = (print "get 5 = "; print (board_get (bd, 5)); print "\n")
val () = (print "get 6 = "; print (board_get (bd, 6)); print "\n")
val () = (print "get 7 = "; print (board_get (bd, 7)); print "\n")
//
// ---- boundary: board_get off the ends of the board
//
val () = print "== board_get, out of range ==\n"
val () = (print "get -1 = "; print (board_get (bd, ~1)); print "\n")
val () = (print "get 8 = "; print (board_get (bd, 8)); print "\n")
val () = (print "get 100 = "; print (board_get (bd, 100)); print "\n")
//
// ---- normal case: board_set on the first, middle and last rows
//
val () = print "== board_set ==\n"
val () = (print "set 0 7 = "; pbd (board_set (bd, 0, 7)); print "\n")
val () = (print "set 3 3 = "; pbd (board_set (bd, 3, 3)); print "\n")
val () = (print "set 7 0 = "; pbd (board_set (bd, 7, 0)); print "\n")
//
// ---- boundary: board_set off the ends returns the board untouched
//
val () = print "== board_set, out of range ==\n"
val () = (print "set -1 5 = "; pbd (board_set (bd, ~1, 5)); print "\n")
val () = (print "set 8 5 = "; pbd (board_set (bd, 8, 5)); print "\n")
//
// ---- boundary: the original board must be unchanged by any of the above
//
val () = (print "bd after sets = "; pbd (bd); print "\n")
//
// ---- normal and boundary: safety_test1
//
val () = print "== safety_test1 ==\n"
val () = (print "same square = "; pb (safety_test1 (0, 0, 0, 0)); print "\n")
val () = (print "same column = "; pb (safety_test1 (0, 0, 1, 0)); print "\n")
val () = (print "diagonal = "; pb (safety_test1 (0, 0, 1, 1)); print "\n")
val () = (print "long diagonal = "; pb (safety_test1 (0, 7, 7, 0)); print "\n")
val () = (print "knight-ish safe = "; pb (safety_test1 (0, 0, 1, 2)); print "\n")
val () = (print "far safe = "; pb (safety_test1 (0, 0, 7, 3)); print "\n")
//
// ---- boundary: safety_test2 with no rows to check is vacuously true
//
val () = print "== safety_test2 ==\n"
val () = (print "vacuous -1 = "; pb (safety_test2 (4, 4, bd, ~1)); print "\n")
val () = (print "sol row 7 = "; pb (safety_test2 (7, 3, sol, 6)); print "\n")
val () = (print "sol row 1 = "; pb (safety_test2 (1, 4, sol, 0)); print "\n")
val () = (print "clash col = "; pb (safety_test2 (1, 0, sol, 0)); print "\n")
val () = (print "clash diag = "; pb (safety_test2 (1, 1, sol, 0)); print "\n")
//
// ---- boundary: print_dots at and below zero prints nothing
//
val () = print "== print_dots ==\n"
val () = (print "dots 0 = ["; print_dots (0); print "]\n")
val () = (print "dots -1 = ["; print_dots (~1); print "]\n")
val () = (print "dots 3 = ["; print_dots (3); print "]\n")
//
// ---- boundary: the two extreme rows, where a run of dots is empty
//
val () = print "== print_row ==\n"
val () = print_row (0)
val () = print_row (3)
val () = print_row (7)
//
// ---- normal case: whole boards
//
val () = print "== print_board diagonal ==\n"
val () = print_board (diag)
val () = print "== print_board known solution ==\n"
val () = print_board (sol)
//
// ---- boundary: search with nothing left to try returns its counter as is
//
val () = print "== search, immediate return ==\n"
val () = (print "j past end, nsol 0 = "; print (search (zero, 0, N, 0)); print "\n")
val () = (print "j past end, nsol 41 = "; print (search (zero, 0, N, 41)); print "\n")
//
// ---- own design: the two properties checked exhaustively
//
val () = print "== properties ==\n"
val () = (print "set/get round trip = "; pb (rt_i (bd, N-1)); print "\n")
val () = (print "safety_test1 symmetric from (0,0) = "; pb (sym_i (0, 0, N-1)); print "\n")
val () = (print "safety_test1 symmetric from (3,5) = "; pb (sym_i (3, 5, N-1)); print "\n")
//
val () = print_newline ()
//
} (* end of [main0] *)

(* ****** ****** *)

(* end of [probes_body.dats] *)

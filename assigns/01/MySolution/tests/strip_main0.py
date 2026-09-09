#!/usr/bin/env python3
"""Derive a main0-free copy of queens.dats so tests can call its functions.

queens.dats carries its own main0, so it cannot simply be linked into a test
driver that needs one of its own. Rather than keep a second, hand-maintained
copy of the functions, which would drift, this script mechanically removes
the main0 implementation and nothing else. The tests therefore exercise the
same function definitions the real program uses.
"""

import sys

BEGIN = "implement"
BEGIN_NEXT = "main0 () = {"
END = "} (* end of [main0] *)"


def strip(text: str) -> str:
    lines = text.split("\n")
    out, i, removed = [], 0, False
    while i < len(lines):
        if (lines[i].strip() == BEGIN
                and i + 1 < len(lines)
                and lines[i + 1].strip() == BEGIN_NEXT):
            while i < len(lines) and lines[i].strip() != END:
                i += 1
            i += 1  # step past the closing brace itself
            removed = True
            continue
        out.append(lines[i])
        i += 1
    if not removed:
        raise SystemExit("strip_main0: no main0 block found; queens.dats changed shape")
    return "\n".join(out)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        src = f.read()
    with open(sys.argv[2], "w") as f:
        f.write(strip(src))

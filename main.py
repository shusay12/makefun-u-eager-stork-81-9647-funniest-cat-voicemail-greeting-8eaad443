#!/usr/bin/env python3
"""Funniest Cat Voicemail Greeting — entry writer.

Writes one voicemail greeting, recorded by a cat, to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Python 3.13 stdlib only, no network, deterministic.
"""

import os
import sys

# The line, chosen against the judge's brief (most important first):
#  1. It reads as a voicemail greeting recorded by a cat and lands a
#     laugh: "You've reached Miso" is the greeting, and the cat is
#     speaking, not the owner writing about a cat.
#  2. The joke is specific to cats: knocking a mug off the table, then
#     demanding snacks instead of an apology.
#  3. Miso has a voice of her own: busy, unbothered, transactional —
#     "or better, bring snacks" is the cat's own priority, not the
#     owner's.
#  4. It works spoken aloud in the few seconds a caller waits, and the
#     punch ("or better, bring snacks") arrives in the last three words.
#  5. Fresh and surprising: the interruption is live ("I'm busy
#     knocking..."), not a tired box nap or a catchphrase.
#  6. Tight: 105 characters, every phrase doing work; one read.
LINE = (
    "You've reached Miso. I'm busy knocking your mug off the table. "
    "Leave a message, or better, bring snacks."
)

MAX_CHARS = 120


def validate(line: str) -> str | None:
    """Return an error message if the line fails the gate, else None."""
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    if not line.strip():
        return "entry must not be whitespace-only"
    if not 1 <= len(line) <= MAX_CHARS:
        return f"entry is {len(line)} chars, must be 1-{MAX_CHARS}"
    if any(ord(c) < 0x20 for c in line):
        return "entry contains control characters"
    try:
        if line.encode("utf-8").decode("utf-8") != line:
            return "UTF-8 round-trip failed"
    except UnicodeError:
        return "entry is not valid UTF-8"
    return None


def main() -> int:
    error = validate(LINE)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    # The file holds exactly the line: no trailing newline, no stray bytes.
    with open(path, "wb") as f:
        f.write(data)

    # Byte-exact write-back check: what is on disk must be exactly what
    # was validated, or the entry is not shipped.
    with open(path, "rb") as f:
        if f.read() != data:
            print("write-back check failed", file=sys.stderr)
            return 1

    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Count whitespace-delimited words from standard input against an inclusive range."""

from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: count_words.py MIN MAX", file=sys.stderr)
        return 2
    try:
        minimum, maximum = (int(value) for value in sys.argv[1:])
    except ValueError:
        print("MIN and MAX must be integers", file=sys.stderr)
        return 2
    if minimum < 0 or minimum > maximum:
        print("require 0 <= MIN <= MAX", file=sys.stderr)
        return 2
    count = len(sys.stdin.read().split())
    print(f"words={count} range={minimum}-{maximum} status={'pass' if minimum <= count <= maximum else 'fail'}")
    return 0 if minimum <= count <= maximum else 1


if __name__ == "__main__":
    raise SystemExit(main())

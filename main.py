#!/usr/bin/env python3
"""Carrier for THE SOUTHERN LEDGER entry (News Image 20261124, Account 17).

Standard library only. Opens entry.png in the same directory as this file,
checks the PNG gate (exactly 1024x1024 and at most 1 MiB), and writes its
bytes exactly to standard output.
"""
import os
import struct
import sys

MAX_BYTES = 1024 * 1024
EXPECTED_W = 1024
EXPECTED_H = 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        sys.stderr.write("entry.png exceeds 1 MiB gate\n")
        return 1
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.stderr.write("entry.png is not a PNG\n")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width != EXPECTED_W or height != EXPECTED_H:
        sys.stderr.write("entry.png is not 1024x1024\n")
        return 1
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

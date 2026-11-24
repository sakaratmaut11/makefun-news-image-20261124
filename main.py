#!/usr/bin/env python3
"""ONE DAY CHRONICLE — Akun 17 (@sakaratmaut8193), NI24.

Entry carrier: standard library only. Copies the pre-rendered
entry.png (drawn in this session by compose_ak17.py) to the output
directory, after verifying the gate limits by hand: PNG signature,
IHDR exactly 1024x1024, file at most 1 MiB. No network, no randomness;
two runs write byte-identical output.
"""

import os
import struct
import sys

MAX_BYTES = 1048576
WANT_W = 1024
WANT_H = 1024


def read_png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk first")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB gate" % size)
    width, height = read_png_size(src)
    if (width, height) != (WANT_W, WANT_H):
        raise ValueError(
            "entry.png is %dx%d, gate needs exactly 1024x1024" % (width, height)
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    with open(dst, "wb") as fh:
        fh.write(data)
    # Read-back check: the written file must be byte-identical to the source.
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("output differs from entry.png after write")
    print("wrote %s (%d bytes, %dx%d)" % (dst, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())

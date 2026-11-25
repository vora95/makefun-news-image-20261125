#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125 (MAIN account).

THE WORLD TODAY - 50 stories, 6 continents, one front page and a map.
Writes /output/entry.png: a deterministic copy of the front-page image
(entry.png) shipped in this repository. Standard library only, no network.
The output is byte-identical on every run: same source bytes, same sha256.

Validation: the shipped image is checked before copying (sha256, PNG
dimensions read from the IHDR chunk, size <= 1 MiB) and the file actually
written is re-verified the same way, so a partial or corrupt copy can
never pass silently.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "c7a9f7ba8b0893432b96e85b2238b982b611914f04e6364c4caefc0b8cbaa4e4"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(path):
    """Read width/height from the PNG IHDR chunk (no image library)."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if header[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_image(path, label):
    """Hash + dimensions + size of a file; returns True only if all pass."""
    if not os.path.isfile(path):
        print("%s missing: %s" % (label, path), file=sys.stderr)
        return False
    file_hash = sha256_of(path)
    if file_hash != EXPECTED_SHA256:
        print("%s hash mismatch: %s" % (label, file_hash), file=sys.stderr)
        return False
    width, height = png_dimensions(path)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("%s unexpected dimensions: %dx%d" % (label, width, height),
              file=sys.stderr)
        return False
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print("%s too large: %d bytes" % (label, size), file=sys.stderr)
        return False
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if not check_image(SRC, "source entry.png"):
        return 1
    shutil.copyfile(SRC, dst)
    if not check_image(dst, "output entry.png"):
        return 1
    print("wrote", dst, "sha256", EXPECTED_SHA256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

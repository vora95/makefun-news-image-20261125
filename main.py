#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125.

Writes /output/entry.png: a deterministic copy of the front-page image
(entry.png) shipped in this repository. Standard library only, no network.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "494adeb8c9776fe84589d1aef81d7101f26d03d048619787d361c439ea6034cf"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if sha256_of(SRC) != EXPECTED_SHA256:
        print("source entry.png sha256 mismatch", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, dst)
    if sha256_of(dst) != EXPECTED_SHA256:
        print("output entry.png sha256 mismatch", file=sys.stderr)
        return 1
    print("wrote", dst, "sha256", EXPECTED_SHA256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

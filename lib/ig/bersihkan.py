#!/usr/bin/env python3
"""
bersihkan.py - remove invisible characters from a caption or script before posting.

Text copied out of AI tools can carry characters you cannot see: zero-width
spaces, word joiners, byte-order marks, Unicode tag characters, and odd spaces.
They survive copy-paste and can break hashtags, search and line breaks. This
removes them and turns odd spaces into normal spaces. It never rewrites words:
voice and AI-tell fixes stay with content-writer (Voice section 6b).

Usage
  py lib/ig/bersihkan.py konten/<post>/5-caption.md            # report only
  py lib/ig/bersihkan.py konten/<post>/5-caption.md --tulis    # clean the file in place
  py lib/ig/bersihkan.py - < teks.txt                          # read stdin, print clean text

Adapted from the invisible-character part of Jake Schincariol's
instagram-agent-skill (MIT). See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _teks import invisible_spans  # noqa: E402


def clean(text):
    spans = invisible_spans(text)
    drop = {i for i, _, kind in spans if kind == "remove"}
    space = {i for i, _, kind in spans if kind == "space"}
    out = []
    for i, ch in enumerate(text):
        if i in drop:
            continue
        out.append(" " if i in space else ch)
    return "".join(out), spans


def main():
    ap = argparse.ArgumentParser(description="Remove invisible characters.")
    ap.add_argument("file", help="file to check, or - for stdin")
    ap.add_argument("--tulis", action="store_true", help="write the cleaned text back to the file")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    cleaned, spans = clean(raw)

    if args.file == "-":
        sys.stdout.write(cleaned)
        print(f"\n[{len(spans)} karakter dibersihkan]", file=sys.stderr)
        return

    if not spans:
        print("BERSIH  tidak ada karakter tak terlihat.")
        return
    counts = {}
    for _, name, _ in spans:
        counts[name] = counts.get(name, 0) + 1
    print(f"DITEMUKAN  {len(spans)} karakter tak terlihat:")
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>4}  {name}")
    if args.tulis:
        open(args.file, "w", encoding="utf-8").write(cleaned)
        print(f"Sudah dibersihkan: {args.file}")
    else:
        print("Jalankan lagi dengan --tulis untuk membersihkan file.")


if __name__ == "__main__":
    main()

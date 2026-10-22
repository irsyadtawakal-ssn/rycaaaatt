#!/usr/bin/env python3
"""
outlier.py - rank collected reels by how far each beat its own account.

Raw views are not evidence. An account with 2,000,000 followers doing 400,000
views had a normal day; an account with 4,000 followers doing 400,000 views
found something. This ranks on the outlier multiple: views divided by that
account's own median views (or, if the median is missing, its follower count,
which is weaker and the output says so).

Input is a tab-separated file filled in while browsing (planning/riset/<date>.tsv),
with a header row. Columns (Indonesian or English names both work):

    akun  follower  median  views  hook  formula  durasi  catatan

- hook: the first spoken line or first text card, verbatim
- formula: the hook-writer formula Claude names for it (Contrarian, Curiosity Gap,
  Pattern Interrupt, Identity Callout, Stat Shock, Before / After, Story,
  Fix a mistake), or "baru: <short name>" for a shape not in the list
- durasi: length in seconds (optional)

Usage
  py lib/ig/outlier.py planning/riset/2026-10-21.tsv
  py lib/ig/outlier.py planning/riset/2026-10-21.tsv --out planning/riset/2026-10-21-swipe.md

Adapted from swipe.py in Jake Schincariol's instagram-agent-skill (MIT),
rewritten for Indonesian (formulas are named by Claude from hook-writer, not
by English regexes). See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import argparse
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _teks import words  # noqa: E402

ALIASES = {
    "akun": "account", "account": "account", "handle": "account",
    "follower": "followers", "followers": "followers", "pengikut": "followers",
    "median": "median", "views": "views", "tayangan": "views", "view": "views",
    "hook": "hook", "formula": "formula", "durasi": "length", "length": "length",
    "catatan": "note", "note": "note", "platform": "platform", "link": "link",
}


def num(cell):
    if cell is None:
        return None
    c = cell.strip().lower().replace(" ", "")
    m = re.match(r"^([\d.,]+)(rb|k|jt|m)?$", c)
    if not m:
        digits = re.sub(r"[^\d]", "", c)
        return int(digits) if digits else None
    base, unit = m.groups()
    if unit:
        value = float(base.replace(",", "."))
        return int(value * (1000 if unit in ("rb", "k") else 1_000_000))
    return int(re.sub(r"[^\d]", "", base) or 0)


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if len(lines) < 2:
        return []
    head = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split("\t")]
        cells += [""] * (len(head) - len(cells))
        r = dict(zip(head, cells))
        r["views"] = num(r.get("views"))
        r["followers"] = num(r.get("followers"))
        r["median"] = num(r.get("median"))
        r["length"] = num(r.get("length"))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def rb(n):
    """Indonesian thousands separator."""
    return f"{n:,}".replace(",", ".")


def med(vals):
    vals = [v for v in vals if v is not None]
    return round(statistics.median(vals), 1) if vals else None


def analyse(rows):
    for r in rows:
        base = r.get("median") or r.get("followers")
        r["baseline_kind"] = "median" if r.get("median") else ("follower" if r.get("followers") else None)
        r["baseline"] = base
        r["multiple"] = round(r["views"] / base, 2) if base else None
        r["formula"] = (r.get("formula") or "").strip() or "belum dinamai"
        r["words"] = len(words(r["hook"]))
    ranked = sorted(rows, key=lambda r: -(r["multiple"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def counts(items):
        c = {}
        for r in items:
            c[r["formula"]] = c.get(r["formula"], 0) + 1
        return sorted(c.items(), key=lambda kv: -kv[1])

    return {
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "follower_baseline": sum(1 for r in ranked if r["baseline_kind"] == "follower"),
        "reels": ranked,
        "top": top, "bottom": bottom,
        "top_formulas": counts(top), "bottom_formulas": counts(bottom),
        "top_words": med([r["words"] for r in top]), "bottom_words": med([r["words"] for r in bottom]),
        "top_length": med([r["length"] for r in top]), "bottom_length": med([r["length"] for r in bottom]),
        "new_shapes": [r for r in ranked if r["formula"].lower().startswith("baru")],
        "unnamed": sum(1 for r in ranked if r["formula"] == "belum dinamai"),
    }


def confidence(a):
    if a["n"] < 20 or a["accounts"] < 4:
        return "RENDAH: sampel kecil. Anggap ini petunjuk, bukan kesimpulan."
    if a["n"] < 40:
        return "SEDANG: cukup untuk melihat arah, belum cukup untuk aturan."
    return "CUKUP: polanya layak diuji di kontenmu sendiri."


def render(a):
    out = []
    head = f"RISET  ·  {a['n']} reels  ·  {a['accounts']} akun  ·  dasar: median views akun"
    out += ["", head, "=" * max(len(head), 78)]
    if a["follower_baseline"]:
        out.append(f"  catatan: {a['follower_baseline']} baris pakai jumlah follower karena median kosong (lebih lemah)")
    for r in a["reels"]:
        mult = f"{r['multiple']:.1f}x" if r["multiple"] else "  ?"
        mark = "  <- outlier" if (r["multiple"] or 0) >= 3 else ""
        out.append(f"  {mult:>7}  {r['formula'][:20]:<20} {r.get('account', '')[:18]:<18} {r["views"]:>10,}{mark}")
        out.append(f"           \"{r['hook'][:90]}\"")
    out.append("-" * max(len(head), 78))
    out.append("YANG MENONJOL DI SEPERTIGA ATAS")
    out.append("  formula atas:   " + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]))
    out.append("  formula bawah:  " + ", ".join(f"{n} x{c}" for n, c in a["bottom_formulas"][:4]))
    out.append(f"  panjang hook:   atas {a['top_words']} kata vs bawah {a['bottom_words']} kata")
    if a["top_length"] is not None:
        out.append(f"  durasi video:   atas {a['top_length']} dtk vs bawah {a['bottom_length']} dtk")
    if a["new_shapes"]:
        out.append(f"  bentuk baru:    {len(a['new_shapes'])} hook tidak cocok dengan formula hook-writer. Baca manual:")
        for r in a["new_shapes"][:6]:
            out.append(f"                  {r['formula']}  ({r.get('account', '')})  \"{r['hook'][:60]}\"")
    if a["unnamed"]:
        out.append(f"  belum dinamai:  {a['unnamed']} baris tanpa formula. Isi kolom formula dulu.")
    out.append(f"\n  KEYAKINAN  {confidence(a)}\n")
    return "\n".join(out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} reels dari {a['accounts']} akun, diurutkan dari kelipatan terhadap median views akunnya.",
             f"Keyakinan: {confidence(a)}", ""]
    for r in a["reels"]:
        mult = f"{r['multiple']:.1f}x" if r["multiple"] else "?"
        lines += [f"## {mult} · {r['formula']} · {r.get('account', '')}",
                  f"- views {rb(r['views'])} · dasar {rb(r['baseline'])} ({r['baseline_kind']})" if r["baseline"] else f"- views {rb(r['views'])}",
                  f"- hook: \"{r['hook']}\" ({r['words']} kata)"]
        if r.get("length"):
            lines.append(f"- durasi: {r['length']} detik")
        if r.get("link"):
            lines.append(f"- link: {r['link']}")
        if r.get("note"):
            lines.append(f"- catatan: {r['note']}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Rank collected reels by outlier multiple.")
    ap.add_argument("input", help="TSV file, or - for stdin")
    ap.add_argument("--out", help="also write the swipe file as markdown")
    a = ap.parse_args()
    rows = read_rows(a.input)
    if not rows:
        print("Tidak ada baris yang bisa dipakai. Butuh TSV dengan header dan minimal kolom views dan hook.",
              file=sys.stderr)
        sys.exit(2)
    res = analyse(rows)
    print(render(res))
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(to_markdown(res))
        print(f"Ditulis: {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

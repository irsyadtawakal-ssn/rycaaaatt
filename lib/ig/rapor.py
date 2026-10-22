#!/usr/bin/env python3
"""
rapor.py - read tracker/post.csv and compute the numbers the content audit needs.

Raw reach mostly tracks how many people already follow the account, so this
ranks each post by its multiple over the channel's own median reach, and by
sends per reach (the strongest single signal for reaching new people). It
then compares groups (pillar, format, framework, hook formula, cover with or
without face) and says how many posts each comparison rests on.

Usage
  py lib/ig/rapor.py                                   # all rows, all channels
  py lib/ig/rapor.py --channel instagram --dari 2026-10-01 --sampai 2026-10-31
  py lib/ig/rapor.py --out tracker/rapor/2026-10-31.md

Ideas adapted from ig-audit in Jake Schincariol's instagram-agent-skill (MIT).
See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import argparse
import csv
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "..", "..", "tracker", "post.csv")
for _stream in (sys.stdout, sys.stderr):  # UTF-8 output on Windows consoles
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

GROUPS = ["pilar", "format", "kerangka", "formula_hook", "cover_wajah"]


def f(v):
    """Parse a tracker number: 1200, 1.200 (thousands), 12,5 or 12.5, 45%."""
    if v is None:
        return None
    v = str(v).strip().replace("%", "").replace(" ", "")
    if not v:
        return None
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", v):
        v = v.replace(".", "")
    v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def per(a, b, scale=1000):
    return round(a / b * scale, 1) if a is not None and b else None


def med(vals):
    vals = [v for v in vals if v is not None]
    return round(statistics.median(vals), 2) if vals else None


def load(path, channel, start, end):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if not r.get("tanggal"):
                continue
            if channel and r.get("channel", "").lower() != channel.lower():
                continue
            if start and r["tanggal"] < start:
                continue
            if end and r["tanggal"] > end:
                continue
            for k in ["jangkauan", "save", "kirim", "komentar", "follow_baru", "dm", "durasi_detik",
                      "rata_tonton_detik", "persen_selesai", "bertahan_3_detik", "persen_non_follower"]:
                r[k] = f(r.get(k))
            if r["jangkauan"]:
                rows.append(r)
    return rows


def analyse(rows):
    by_channel = {}
    for r in rows:
        by_channel.setdefault(r["channel"], []).append(r["jangkauan"])
    medians = {c: statistics.median(v) for c, v in by_channel.items()}
    for r in rows:
        r["kelipatan"] = round(r["jangkauan"] / medians[r["channel"]], 2) if medians[r["channel"]] else None
        r["kirim_1k"] = per(r["kirim"], r["jangkauan"])
        r["save_1k"] = per(r["save"], r["jangkauan"])
        r["follow_1k"] = per(r["follow_baru"], r["jangkauan"])
        r["tonton_pct"] = (round(r["rata_tonton_detik"] / r["durasi_detik"] * 100, 1)
                           if r["rata_tonton_detik"] and r["durasi_detik"] else None)
    groups = {}
    for g in GROUPS:
        buckets = {}
        for r in rows:
            key = (r.get(g) or "").strip()
            if key:
                buckets.setdefault(key, []).append(r)
        groups[g] = sorted(
            [(k, len(v), med([x["kelipatan"] for x in v]), med([x["kirim_1k"] for x in v]),
              med([x["follow_1k"] for x in v])) for k, v in buckets.items()],
            key=lambda t: -(t[2] or 0))
    return medians, groups


def confidence(n):
    if n < 10:
        return f"RENDAH (n={n}). Belum bisa menyimpulkan pola; catat dulu sampai sekitar 30 post."
    if n < 30:
        return f"SEDANG (n={n}). Arahnya mulai terlihat, tapi satu-dua post bisa mengubah hasil."
    return f"CUKUP (n={n}). Pola yang muncul di beberapa kelompok layak diuji."


def fmt(v, suffix=""):
    return "-" if v is None else f"{v:g}{suffix}"


def report(rows, medians, groups):
    out = ["# Rapor konten", ""]
    out.append(f"{len(rows)} baris · " + " · ".join(f"median jangkauan {c}: {m:,.0f}".replace(",", ".")
                                                     for c, m in medians.items()))
    out += [f"Keyakinan: {confidence(len(rows))}", ""]
    ranked = sorted(rows, key=lambda r: -(r["kelipatan"] or 0))
    cols = "| Tanggal | Channel | Topik | Kelipatan | Kirim/1rb | Save/1rb | Follow/1rb | Non-follower | Bertahan 3 dtk | Ditonton |"
    sep = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"

    def line(r):
        return (f"| {r['tanggal']} | {r['channel']} | {r.get('topik', '')[:40]} | {fmt(r['kelipatan'], 'x')} | "
                f"{fmt(r['kirim_1k'])} | {fmt(r['save_1k'])} | {fmt(r['follow_1k'])} | "
                f"{fmt(r['persen_non_follower'], '%')} | {fmt(r['bertahan_3_detik'], '%')} | {fmt(r['tonton_pct'], '%')} |")

    k = min(5, max(1, len(ranked) // 2))
    out += ["## 5 teratas (kelipatan terhadap median channel)", "", cols, sep] + [line(r) for r in ranked[:k]] + [""]
    out += ["## 5 terbawah", "", cols, sep] + [line(r) for r in ranked[-k:][::-1]] + [""]
    out += ["## Per kelompok", "", "Median per kelompok. Kelompok dengan n di bawah 3 belum bisa dibandingkan.", ""]
    for g, items in groups.items():
        if not items:
            continue
        out += [f"### {g}", "", "| Nilai | n | Kelipatan | Kirim/1rb | Follow/1rb |", "| --- | --- | --- | --- | --- |"]
        out += [f"| {k} | {n} | {fmt(m, 'x')} | {fmt(s)} | {fmt(fo)} |" for k, n, m, s, fo in items]
        out.append("")
    reach_hi = [r for r in rows if (r["persen_non_follower"] or 0) >= 50 and (r["follow_1k"] or 0) < 1]
    if reach_hi:
        out += ["## Sinyal profil", "",
                f"{len(reach_hi)} post menjangkau banyak non-follower (≥50%) tapi follow di bawah 1 per 1.000 jangkauan. "
                "Itu biasanya masalah profil, bukan hook. Jalankan profile-check.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Compute audit numbers from tracker/post.csv")
    ap.add_argument("--file", default=DEFAULT)
    ap.add_argument("--channel")
    ap.add_argument("--dari")
    ap.add_argument("--sampai")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = load(a.file, a.channel, a.dari, a.sampai)
    if not rows:
        print("Belum ada baris dengan angka jangkauan di tracker untuk filter ini.", file=sys.stderr)
        sys.exit(2)
    medians, groups = analyse(rows)
    text = report(rows, medians, groups)
    print(text)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(text + "\n")
        print(f"\nDitulis: {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

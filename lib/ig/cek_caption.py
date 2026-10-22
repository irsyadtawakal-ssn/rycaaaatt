#!/usr/bin/env python3
"""
cek_caption.py - check one caption against the @irsyadtawakal caption rules.

Rules come from brand/03-voice.md (section 6 Caption Instagram, 6b AI tells,
7 Copy per channel) and brand/02-positioning.md (service line). The first
thing it prints for Instagram is what the feed shows before "... more"
(about 125 characters), because that is where most captions fail.

Usage
  py lib/ig/cek_caption.py caption.txt --channel instagram --kata-kunci "ChatGPT,prompt"
  py lib/ig/cek_caption.py konten/<post>/5-caption.md --bagian Threads --channel threads
  py lib/ig/cek_caption.py - --channel tiktok < caption.txt

Options
  --channel     instagram (default), tiktok, threads, linkedin
  --bagian      take only the text under the markdown heading that contains this word
  --kata-kunci  comma-separated keywords that must appear early
  --pilar       pillar number 1-6 (the service line is only allowed for 2 and 4, and on LinkedIn)
  --aset        the post really sends an asset (Prompt Library, template), so a keyword ask is allowed
  --video       the post is a video, so the handle must be at the end of the caption

Exit code 1 when any check FAILs, so it can gate a workflow.

Inspired by caption.py in Jake Schincariol's instagram-agent-skill (MIT),
rewritten for Indonesian and this brand. See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import argparse
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _teks import find_invisible  # noqa: E402

TRUNCATE = 125
LIMITS = {"instagram": 2200, "threads": 500, "linkedin": 3000, "tiktok": None}
TAGS = {"instagram": (3, 5), "tiktok": (3, 5), "threads": (0, 1), "linkedin": (0, 3)}
HANDLE = "@irsyadtawakal"

HASHTAG_RE = re.compile(r"(?:^|\s)(#[^\s#]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|id|io|net|org|ai|app|my\.id)\b/?\S*", re.I)
FILLER_TAGS = {"#fyp", "#fypシ", "#fypage", "#foryou", "#foryoupage", "#viral", "#viralvideo",
               "#explore", "#explorepage", "#trending", "#reels", "#reelsinstagram", "#instagood",
               "#xyzbca", "#masukberanda", "#berandatiktok"}

BAIT = [
    (r"\b(?i:komen(?:tar)?|tulis|ketik)\s+(?i:kata\s+)?[\"“']?[A-Z0-9]{2,}\b", "minta komentar dengan kata tertentu"),
    (r"(?i)\btag\s+(?:teman|temen|temanmu|temenmu|sahabat|orang)\b", "minta tag teman"),
    (r"(?i)\b(?:share|bagikan|kirim(?:kan)?)\s+(?:ini\s+|post\s+ini\s+)?(?:ke|sama)\s+(?:teman|temen|temanmu|temenmu|orang|grup)\b", "minta share atau kirim"),
    (r"(?i)\bfollow\s+(?:dulu|biar|untuk|buat)\b", "minta follow"),
]
STOCK_OPENERS = [r"^\s*di era digital", r"^\s*tahukah kamu", r"^\s*siapa di sini yang", r"^\s*bayangkan (?:jika|kalau)"]
FORMAL = ["merupakan", "adapun", "oleh karena itu"]
HYPE = ["revolusioner", "game changer", "game-changer", "rahasia", "sakti", "wajib coba"]
SELF_ANSWER = re.compile(r"(?:^|[.!\n]\s*)(?:Hasilnya|Kenapa|Caranya|Jawabannya|Intinya|Masalahnya)\?\s", re.I)
BUKAN_TAPI = re.compile(r"\bbukan\b[^.!?\n]{1,60}\b(?:tapi|tetapi|melainkan)\b", re.I)
SERVICE = re.compile(r"\b(?:DM saya|DM aku|hubungi saya|chat saya|konsultasi)\b", re.I)


def take_section(text, word):
    lines = text.splitlines()
    out, inside, found = [], False, False
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            if inside:
                break
            inside = word.lower() in line.lower()
            found = found or inside
            continue
        if inside:
            out.append(line)
    return "\n".join(out).strip() if found else None


def main():
    ap = argparse.ArgumentParser(description="Check a caption against the brand rules.")
    ap.add_argument("file", help="caption file, or - for stdin")
    ap.add_argument("--channel", default="instagram", choices=sorted(LIMITS))
    ap.add_argument("--bagian")
    ap.add_argument("--kata-kunci", default="")
    ap.add_argument("--pilar", type=int)
    ap.add_argument("--aset", action="store_true")
    ap.add_argument("--video", action="store_true")
    a = ap.parse_args()

    raw = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    if a.bagian:
        raw = take_section(raw, a.bagian)
        if raw is None:
            print(f"Tidak ada heading yang memuat '{a.bagian}'.", file=sys.stderr)
            sys.exit(2)
        if not raw:
            print(f"Bagian '{a.bagian}' masih kosong.", file=sys.stderr)
            sys.exit(2)
    text = raw.strip()
    ch = a.channel
    checks = []

    def add(name, status, detail):
        checks.append((status, name, detail))

    body_lines = [l for l in text.splitlines() if l.strip()]
    first = body_lines[0].strip() if body_lines else ""
    window = text[:TRUNCATE]
    tags = HASHTAG_RE.findall(text)
    keywords = [k.strip() for k in a.kata_kunci.split(",") if k.strip()]

    # What the feed shows (Instagram)
    if ch == "instagram":
        print("\n  YANG TERLIHAT DI FEED (sebelum \"... selengkapnya\")")
        print("  +" + "-" * 54 + "+")
        for line in [l for part in window.split("\n") for l in (textwrap.wrap(part, 52) or [""])][:6]:
            print(f"  | {line:<52} |")
        tail = "... selengkapnya" if len(text) > TRUNCATE else "(muat semua)"
        print("  +" + "-" * (54 - len(tail) - 2) + f" {tail} +\n")

    # Length
    limit = LIMITS[ch]
    if limit:
        add("PANJANG", "FAIL" if len(text) > limit else "PASS", f"{len(text)} / {limit} karakter")
    else:
        add("PANJANG", "PASS", f"{len(text)} karakter")

    # Opening
    if not first:
        add("PEMBUKA", "FAIL", "caption kosong")
    elif first.startswith(("#", "@")):
        add("PEMBUKA", "FAIL", "dibuka dengan hashtag atau mention; posisi ini untuk hook")
    elif ch == "instagram" and len(first) > TRUNCATE:
        add("PEMBUKA", "WARN", f"baris pertama {len(first)} karakter, terpotong di {TRUNCATE}")
    else:
        add("PEMBUKA", "PASS", f"baris pertama {len(first)} karakter")

    # Keywords early
    if keywords:
        if ch == "instagram":
            scope, label = window, f"{TRUNCATE} karakter pertama"
        else:
            scope, label = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0], "kalimat pertama"
        missing = [k for k in keywords if k.lower() not in scope.lower()]
        add("KATA KUNCI", "WARN" if missing else "PASS",
            f"belum ada di {label}: {', '.join(missing)}" if missing else f"semua ada di {label}")

    # Hashtags
    lo, hi = TAGS[ch]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    if len(tags) > hi:
        add("HASHTAG", "FAIL", f"{len(tags)} hashtag, batas {ch} {hi}")
    elif filler:
        add("HASHTAG", "WARN", f"hashtag umum yang tidak menjelaskan topik: {' '.join(filler)}")
    elif len(tags) < lo:
        add("HASHTAG", "WARN", f"{len(tags)} hashtag, target {lo}-{hi} sebagai label topik")
    else:
        add("HASHTAG", "PASS", f"{len(tags)} hashtag" + (f": {' '.join(tags)}" if tags else ""))
    if ch == "instagram" and any(t in window for t in tags):
        add("POSISI HASHTAG", "WARN", "ada hashtag di 125 karakter pertama; pindahkan ke bawah")

    # Links
    links = LINK_RE.findall(text)
    if links and ch in ("instagram", "tiktok"):
        add("LINK", "WARN", "link di caption tidak bisa diklik; taruh di bio")

    # Bait
    baits = [name for pat, name in BAIT if re.search(pat, text)]
    if baits and not a.aset:
        add("AJAKAN", "FAIL", "; ".join(baits) + ". Hanya boleh kalau post mengirim aset nyata (--aset)")
    elif baits:
        add("AJAKAN", "PASS", "ajakan kata kunci, post mengirim aset nyata")

    # A real question near the end
    tail_lines = [l for l in body_lines if not l.strip().startswith(("#", "@"))]
    tail_text = " ".join(tail_lines[-2:]) if tail_lines else ""
    add("PERTANYAAN", "PASS" if "?" in tail_text else "WARN",
        "ada pertanyaan di penutup" if "?" in tail_text else "belum ada satu pertanyaan sungguhan di penutup")

    # AI tells (Voice 6b)
    tells = []
    n_bt = len(BUKAN_TAPI.findall(text))
    if n_bt > 1:
        tells.append(f"'bukan ... tapi' {n_bt}x (maks 1)")
    if SELF_ANSWER.search(text):
        tells.append("pertanyaan yang langsung dijawab sendiri")
    if any(re.search(p, text, re.I | re.M) for p in STOCK_OPENERS):
        tells.append("pembuka klise")
    low = text.lower()
    tells += [f"kata formal '{w}'" for w in FORMAL if w in low]
    tells += [f"kata hype '{w}'" for w in HYPE if w in low]
    if "—" in first:
        tells.append("tanda pisah panjang di baris pertama")
    if re.search(r"\btanpa\b[^.!?\n]*\btanpa\b[^.!?\n]*\btanpa\b", low):
        tells.append("deretan 'tanpa'")
    add("CIRI TULISAN AI", "WARN" if tells else "PASS", "; ".join(tells) if tells else "tidak terdeteksi")

    # Service line
    if SERVICE.search(text) and ch != "linkedin" and a.pilar not in (2, 4):
        add("KALIMAT LAYANAN", "WARN",
            "kalimat layanan hanya untuk pilar 2, pilar 4, dan LinkedIn" +
            ("" if a.pilar else " (isi --pilar)"))

    # Handle
    if a.video:
        ends = text.rstrip().endswith(HANDLE) or HANDLE in (body_lines[-1] if body_lines else "")
        add("HANDLE", "PASS" if ends else "WARN",
            "@irsyadtawakal di akhir caption" if ends else "video: tulis @irsyadtawakal di akhir caption")

    # Invisible characters
    inv = find_invisible(text)
    if inv:
        add("KARAKTER TAK TERLIHAT", "FAIL",
            ", ".join(f"{n}x {k}" for k, n in inv.items()) + ". Jalankan lib/ig/bersihkan.py --tulis")

    width = max(len(n) for _, n, _ in checks)
    for status, name, detail in checks:
        print(f"  {status:<4}  {name:<{width}}  {detail}")
    fails = sum(1 for s, _, _ in checks if s == "FAIL")
    warns = sum(1 for s, _, _ in checks if s == "WARN")
    print(f"\n  {fails} FAIL, {warns} WARN  ·  channel {ch}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

"""
_video.py - shared helpers for the lib/video scripts.

Every script takes the post folder (konten/YYYY-MM-DD-<seri>-<nn>) and works
inside <post>/video/. File names in that folder:

    mentah.mp4        raw recording from Irsyad's phone (any name starting with "mentah")
    prep.mp4          conformed to 1080 x 1920, 30 fps CFR, 48 kHz
    potong.mp4        silences over 0.35 s removed (auto-editor)
    potong.json       cut points and durations
    transkrip.json    word-level transcript of potong.mp4, glossary applied
    transkrip.md      the same, readable, with words to check marked
    edit.json         overlay plan (hook, keywords, cards, Contekan, zooms)
    timeline.json     everything with exact times; both renderers read this
"""

import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = os.path.join(ROOT, "lib", "video")
FPS = 30
W, H = 1080, 1920


def video_dir(post):
    d = os.path.join(os.path.abspath(post), "video")
    os.makedirs(d, exist_ok=True)
    return d


def find_raw(vdir):
    for name in sorted(os.listdir(vdir)):
        if name.lower().startswith("mentah") and name.lower().endswith((".mp4", ".mov", ".m4v", ".mkv", ".webm")):
            return os.path.join(vdir, name)
    return None


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"{tool} tidak ditemukan. Cek cara pasang di README.md.")


def run(cmd, **kw):
    print("  $ " + " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], **kw)
    if r.returncode != 0:
        sys.exit(f"Gagal (kode {r.returncode}): {cmd[0]}")
    return r


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)


def duration(path):
    return float(probe(path)["format"]["duration"])


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm(word):
    """Lowercase and strip punctuation, for matching words against anchors."""
    return re.sub(r"[^\w@]+", "", word.lower())


def tc(s):
    m, s = divmod(max(s, 0), 60)
    return f"{int(m)}:{s:05.2f}"


def report(notes):
    """Print FAIL / WARN / OK lines the same way lib/ig scripts do; exit 1 on FAIL."""
    for level, msg in notes:
        print(f"[{level}] {msg}")
    if not notes:
        print("[OK] Tidak ada catatan.")
    return 1 if any(level == "FAIL" for level, _ in notes) else 0

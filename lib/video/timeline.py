#!/usr/bin/env python3
"""
timeline.py - step 3: turn the transcript and the overlay plan into one
timeline.json with exact times. HyperFrames and Remotion both render from it,
so the two engines show the same thing at the same moment.

  py lib/video/timeline.py konten/<post>
  py lib/video/timeline.py konten/<post> --contoh     # write an empty edit.json to fill in

Input:  <post>/video/transkrip.json, potong.json, edit.json
Output: <post>/video/timeline.json, and a FAIL / WARN check against
        Video Brain sections 3-7 (exit 1 on FAIL)

edit.json (times are seconds in potong.mp4, or a word anchor: "konteks" is the
first time that word is said, "konteks#2" the second time):

{
  "hook":        {"teks": "Prompt kamu kurang satu hal", "kata_kunci": "satu",
                  "sampai": null, "ketik": false},
  "kata_kunci":  ["konteks", "prompt#2"],
  "kartu_angka": [{"angka": "5x", "label": "ngulang prompt", "sumber": "pengalaman Irsyad",
                   "pada": "lima", "durasi": 1.2}],
  "contekan":    {"judul": "Contekan", "poin": ["...", "...", "..."], "pada": null, "durasi": 1.5},
  "zoom":        ["masalahnya", 14.2],
  "objek":       [{"gambar": "assets/chat-1.png", "pada": "coba", "durasi": 3}],
  "akhir_kosong": true
}

hook.sampai null = the input bar leaves at the end of the first sentence.
hook.ketik true = the old typed-out version, only for the A/B test (Video Brain 9).
contekan.pada null = it ends where the last sentence starts, so the last line
plays over the face with the empty input bar (Video Brain 7).
Sound effects play only if the real files exist: assets/sfx/ketik.wav and
assets/sfx/ting.wav (keyboard at the end of the first sentence, then "ting").
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _video import FPS, H, ROOT, W, duration, load_json, norm, report, save_json, tc, video_dir  # noqa: E402

MAX_WORDS = 4
MAX_CHARS = 20
GAP_BREAK = 0.30
# Words a caption chunk should not end on: the phrase continues after them.
WEAK_END = {
    "yang", "di", "ke", "dari", "dan", "atau", "tapi", "untuk", "buat", "dengan", "sama", "karena",
    "kalau", "kalo", "jadi", "si", "para", "sang", "itu", "ini", "pada", "dalam", "bisa", "akan",
    "nggak", "gak", "tidak", "belum", "lagi", "lebih", "paling", "the", "a", "an", "of", "to",
}
PUNCT_END = re.compile(r"[.,?!;:…]$")
SENT_END = re.compile(r"[.?!…]$")

EXAMPLE = {
    "hook": {"teks": "", "kata_kunci": "", "sampai": None, "ketik": False},
    "kata_kunci": [],
    "kartu_angka": [],
    "contekan": {"judul": "Contekan", "poin": [], "pada": None, "durasi": 1.5},
    "zoom": [],
    "objek": [],
    "akhir_kosong": True,
}


def caption_text(word):
    """Captions drop sentence punctuation except ? and !."""
    return re.sub(r"[.,;:…]+$", "", word)


class Anchors:
    def __init__(self, words):
        self.words = words

    def index(self, ref):
        """'kata' or 'kata#2' -> word index, or None."""
        m = re.match(r"^(.*?)(?:#(\d+))?$", str(ref).strip())
        target, nth = norm(m.group(1)), int(m.group(2) or 1)
        seen = 0
        for i, w in enumerate(self.words):
            if norm(w["w"]) == target:
                seen += 1
                if seen == nth:
                    return i
        return None

    def time(self, ref, notes, what):
        if ref is None:
            return None
        if isinstance(ref, (int, float)):
            return float(ref)
        i = self.index(ref)
        if i is None:
            notes.append(("FAIL", f"{what}: kata '{ref}' tidak ada di transkrip."))
            return None
        return self.words[i]["start"]


def split_phrase(phrase):
    """Split one phrase into as few lines as fit (1-4 words, 20 characters),
    then prefer even lengths and never end a line on "yang", "di", "untuk"..."""
    n = len(phrase)
    best = [(0.0, 0)] + [(float("inf"), 0)] * n  # best[i] = (cost, start of last line) for phrase[:i]
    for i in range(1, n + 1):
        for j in range(max(0, i - MAX_WORDS), i):
            line = phrase[j:i]
            chars = len(" ".join(caption_text(w["w"]) for w in line))
            if chars > MAX_CHARS and i - j > 1:
                continue
            cost = best[j][0] + 10 + 0.04 * (chars - 13) ** 2
            if i < n and norm(line[-1]["w"]) in WEAK_END:
                cost += 8
            if cost < best[i][0]:
                best[i] = (cost, j)
    lines, i = [], n
    while i > 0:
        j = best[i][1]
        lines.insert(0, phrase[j:i])
        i = j
    return lines


def chunk(words):
    """Phrases end at punctuation or a pause; each phrase is split on its own."""
    chunks, phrase = [], []
    for w in words:
        if phrase and (PUNCT_END.search(phrase[-1]["w"]) or w["start"] - phrase[-1]["end"] > GAP_BREAK):
            chunks += split_phrase(phrase)
            phrase = []
        phrase.append(w)
    if phrase:
        chunks += split_phrase(phrase)
    return chunks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post")
    ap.add_argument("--contoh", action="store_true", help="tulis edit.json kosong untuk diisi")
    a = ap.parse_args()

    vdir = video_dir(a.post)
    edit_path = os.path.join(vdir, "edit.json")
    if a.contoh:
        if os.path.exists(edit_path):
            sys.exit("edit.json sudah ada; tidak ditimpa.")
        save_json(edit_path, EXAMPLE)
        print(f"Ditulis: {edit_path}")
        return

    tr = load_json(os.path.join(vdir, "transkrip.json"))
    if not tr:
        sys.exit("transkrip.json belum ada. Jalankan lib/video/transkrip.py dulu.")
    edit = load_json(edit_path)
    if edit is None:
        sys.exit("edit.json belum ada. Jalankan dengan --contoh lalu isi.")
    cut = load_json(os.path.join(vdir, "potong.json"), {})
    words = [w for w in tr["kata"] if w["w"]]
    if not words:
        sys.exit("Transkrip kosong.")
    total = duration(os.path.join(vdir, "potong.mp4"))
    anchors = Anchors(words)
    notes = []

    # ---- sentences (for the hook exit, the Contekan, the empty input bar) ----
    sentences, start = [], 0
    for i, w in enumerate(words):
        if SENT_END.search(w["w"]) or i == len(words) - 1:
            sentences.append((start, i))
            start = i + 1
    first_end = words[sentences[0][1]]["end"]
    last_start = words[sentences[-1][0]]["start"]
    if first_end > 3.2:
        notes.append(("WARN", f"Kalimat pertama baru selesai di {tc(first_end)}; Video Brain minta sekitar detik 3."))

    # ---- keywords ----
    kw_idx = set()
    for ref in edit.get("kata_kunci", []):
        i = anchors.index(ref)
        if i is None:
            notes.append(("FAIL", f"Kata kunci '{ref}' tidak ada di transkrip."))
        else:
            kw_idx.add(i)

    # ---- captions ----
    index_of = {id(w): i for i, w in enumerate(words)}
    caps = []
    chunks = chunk(words)
    for n, c in enumerate(chunks):
        begin = c[0]["start"]
        if n + 1 < len(chunks):
            end = chunks[n + 1][0]["start"]
            if end - c[-1]["end"] > 0.6:  # long gap: do not leave a stale line up
                end = c[-1]["end"] + 0.3
        else:
            end = min(c[-1]["end"] + 0.4, total)
        parts, kws = [], 0
        for w in c:
            is_kw = index_of[id(w)] in kw_idx and kws == 0
            if index_of[id(w)] in kw_idx:
                kws += 1
            parts.append({"t": caption_text(w["w"]), "kw": is_kw})
        text = " ".join(p["t"] for p in parts)
        if kws > 1:
            notes.append(("WARN", f"Caption '{text}' ({tc(begin)}) punya {kws} kata kunci; hanya yang pertama oranye."))
        if len(text) > MAX_CHARS:
            notes.append(("WARN", f"Caption '{text}' ({tc(begin)}) {len(text)} karakter, lebih dari 20. Satu kata panjang; cek apakah muat."))
        caps.append({"mulai": round(begin, 3), "selesai": round(end, 3), "kata": parts})

    # ---- input bar: hook, then empty at the end ----
    bars = []
    hook = edit.get("hook") or {}
    hook_end = None
    if hook.get("teks"):
        teks = hook["teks"].strip()
        hw = teks.split()
        if len(hw) > 6:
            notes.append(("FAIL", f"Teks hook {len(hw)} kata; maksimal 6 (aturan hook-writer)."))
        kw = norm(hook.get("kata_kunci") or "")
        if kw and kw not in [norm(x) for x in hw]:
            notes.append(("FAIL", f"Kata kunci hook '{hook['kata_kunci']}' tidak ada di teks hook."))
        spoken_first = " ".join(norm(w["w"]) for w in words[: sentences[0][1] + 1])
        if " ".join(norm(x) for x in hw) == spoken_first:
            notes.append(("WARN", "Teks hook sama persis dengan kalimat pertama yang diucapkan; Video Brain minta berbeda."))
        t = anchors.time(hook.get("sampai"), notes, "hook.sampai")
        hook_end = t if t is not None else max(first_end + 0.3, 1.5)
        bars.append({"mulai": 0.0, "selesai": round(hook_end, 3), "kosong": False, "ketik": bool(hook.get("ketik")),
                     "kata": [{"t": x, "kw": bool(kw) and norm(x) == kw} for x in hw]})
    else:
        notes.append(("FAIL", "hook.teks kosong. Input bar dengan hook wajib tampil dari frame 1 (Video Brain 3 dan 5)."))

    # ---- number cards ----
    cards = []
    for k in edit.get("kartu_angka", []):
        t = anchors.time(k.get("pada"), notes, f"kartu {k.get('angka')}")
        if t is None:
            continue
        d = float(k.get("durasi", 1.2))
        if not 1.0 <= d <= 1.5:
            notes.append(("FAIL", f"Kartu angka {k.get('angka')}: durasi {d} s; harus 1-1,5 s."))
        if not k.get("sumber"):
            notes.append(("FAIL", f"Kartu angka {k.get('angka')}: tanpa sumber. Hanya angka dari Irsyad atau yang punya sumber bernama."))
        cards.append({"mulai": round(t, 3), "selesai": round(min(t + d, total), 3), "angka": str(k.get("angka", "")),
                      "label": k.get("label", ""), "sumber": k.get("sumber", "")})

    # ---- Contekan ----
    contekan = None
    ck = edit.get("contekan") or {}
    if ck.get("poin"):
        if not 3 <= len(ck["poin"]) <= 5:
            notes.append(("FAIL", f"Contekan {len(ck['poin'])} poin; harus 3-5."))
        d = float(ck.get("durasi", 1.5))
        t = anchors.time(ck.get("pada"), notes, "contekan.pada")
        if t is None:
            t = max(last_start - d, 0)
        contekan = {"mulai": round(t, 3), "selesai": round(min(t + d, total), 3), "judul": ck.get("judul", "Contekan"),
                    "poin": ck["poin"]}
    else:
        notes.append(("WARN", "Belum ada Contekan. Video Brain 5 dan 7: satu frame ringkasan 1,5 detik sebelum loop."))

    if edit.get("akhir_kosong", True):
        begin = contekan["selesai"] if contekan else last_start
        begin = max(begin, last_start - 0.2)
        if hook_end is not None and begin <= hook_end:
            notes.append(("WARN", "Video terlalu pendek untuk input bar kosong di akhir; dilewati."))
        else:
            bars.append({"mulai": round(begin, 3), "selesai": round(total, 3), "kosong": True, "ketik": False, "kata": []})

    # ---- zooms ----
    zooms = []
    for ref in edit.get("zoom", []):
        t = anchors.time(ref, notes, "zoom")
        if t is not None:
            zooms.append(round(t, 3))
    zooms.sort()
    zoom_spans = []
    for i, t in enumerate(zooms):
        end = min(t + 1.6, zooms[i + 1] if i + 1 < len(zooms) else total)
        zoom_spans.append({"mulai": t, "selesai": round(end, 3), "skala": 1.12})
        if i and t - zooms[i - 1] < 3.0:
            notes.append(("WARN", f"Zoom {tc(zooms[i - 1])} dan {tc(t)} terlalu rapat; jangan dua zoom berturut-turut."))

    # ---- objects above the head ----
    objs = []
    for o in edit.get("objek", []):
        t = anchors.time(o.get("pada"), notes, f"objek {o.get('gambar')}")
        if t is None:
            continue
        path = os.path.join(os.path.abspath(a.post), o.get("gambar", ""))
        if not os.path.isfile(path):
            notes.append(("FAIL", f"Objek {o.get('gambar')} tidak ada di folder post. Pakai screenshot asli atau logo resmi saja."))
            continue
        d = float(o.get("durasi", 3))
        if not 2 <= d <= 4:
            notes.append(("WARN", f"Objek {o.get('gambar')} {d} s; Video Brain minta 2-4 s."))
        if hook_end is not None and t < hook_end:
            notes.append(("FAIL", f"Objek {o.get('gambar')} muncul di {tc(t)}, sebelum input bar pergi ({tc(hook_end)})."))
        if objs and t - objs[-1]["mulai"] < 5:
            notes.append(("WARN", f"Objek di {tc(t)} kurang dari 5 detik setelah objek sebelumnya."))
        objs.append({"mulai": round(t, 3), "selesai": round(min(t + d, total), 3), "gambar": o["gambar"]})

    # ---- sound effects: only real files ----
    sfx = []
    ketik = os.path.join(ROOT, "assets", "sfx", "ketik.wav")
    ting = os.path.join(ROOT, "assets", "sfx", "ting.wav")
    if hook.get("teks"):
        if os.path.isfile(ketik) and os.path.isfile(ting):
            sfx.append({"src": "sfx/ketik.wav", "mulai": round(max(first_end - 0.5, 0), 3), "durasi": 0.5, "volume": 0.6})
            sfx.append({"src": "sfx/ting.wav", "mulai": round(first_end, 3), "durasi": 0.8, "volume": 0.6})
        else:
            notes.append(("WARN", "Suara ketik dan ting belum ada (assets/sfx/ketik.wav, ting.wav); video dirender tanpa efek suara."))

    # ---- rhythm check (Video Brain 3 and 6) ----
    changes = set(cut.get("potongan", []))
    for group in (bars, cards, objs, zoom_spans):
        for x in group:
            changes.update([x["mulai"], x["selesai"]])
    if contekan:
        changes.update([contekan["mulai"], contekan["selesai"]])
    changes = sorted(c for c in changes if 0 < c < total - 0.05)
    first = changes[0] if changes else None
    if first is None or first > 2.0:
        notes.append(("WARN", f"Perubahan visual pertama di {tc(first) if first else '-'}; Video Brain minta potongan pertama sekitar 1,5-2 s. "
                               "Tambah zoom di kata penekanan kalimat pertama."))
    prev = 0.0
    for c in changes + [total]:
        limit = 2.2 if prev < 5 else 5.0
        if c - prev > limit + 0.01:
            notes.append(("WARN", f"Tidak ada perubahan visual {tc(prev)}-{tc(c)} ({c - prev:.1f} s). "
                                   + ("5 detik pertama: tiap 1,5-2 s." if prev < 5 else "Setelah detik 5: tiap 3-5 s.")))
        prev = c

    out = {
        "fps": FPS, "lebar": W, "tinggi": H, "durasi": round(total, 3),
        "video": "potong.mp4", "handle": "@irsyadtawakal",
        "input_bar": bars, "caption": caps, "kartu_angka": cards, "contekan": contekan,
        "zoom": zoom_spans, "objek": objs, "sfx": sfx,
    }
    save_json(os.path.join(vdir, "timeline.json"), out)
    print(f"timeline.json: {tc(total)}, {len(caps)} caption, {len(cards)} kartu angka, "
          f"{'1' if contekan else '0'} Contekan, {len(zoom_spans)} zoom, {len(objs)} objek, {len(sfx)} efek suara\n")
    sys.exit(report(notes))


if __name__ == "__main__":
    main()

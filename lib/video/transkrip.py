#!/usr/bin/env python3
"""
transkrip.py - step 2: word-level transcript of potong.mp4 with faster-whisper,
in Indonesian, then fix misheard terms with the glossary (Video Brain section 4:
"a wrong word on screen costs more trust than a missing one").

  py lib/video/transkrip.py konten/<post>
  py lib/video/transkrip.py konten/<post> --model large-v3 --device cuda
  py lib/video/transkrip.py konten/<post> --glosarium-saja   # re-apply the glossary, no re-transcribe

Output: <post>/video/transkrip.mentah.json  Whisper's words as heard
        <post>/video/transkrip.json         words after the glossary; captions are built from this
        <post>/video/transkrip.md           readable version; words to check are marked [[like this]]

Glossary: lib/video/glosarium.json, plus <post>/video/glosarium.json for words
specific to one video (a name, a tool). "ganti" entries are replaced, "cek"
entries and words Whisper was unsure about are only marked. When a marked word
is wrong, add it to the post glossary and run again with --glosarium-saja.
"""

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _video import LIB, load_json, norm, save_json, tc, video_dir  # noqa: E402

LOW_PROB = 0.5
MAX_PHRASE = 4


def load_glossary(vdir):
    base = load_json(os.path.join(LIB, "glosarium.json"), {})
    extra = load_json(os.path.join(vdir, "glosarium.json"), {})
    ganti = {k.lower(): v for k, v in base.get("ganti", {}).items()}
    ganti.update({k.lower(): v for k, v in extra.get("ganti", {}).items()})
    cek = {norm(w) for w in base.get("cek", []) + extra.get("cek", [])}
    prompt = ", ".join(p for p in [base.get("prompt_awal", ""), extra.get("prompt_awal", "")] if p)
    return ganti, cek, prompt


def decode(path):
    """16 kHz mono float32 via FFmpeg. faster-whisper's own decoder uses PyAV,
    whose version is pinned by auto-editor and does not match; this avoids it."""
    import numpy as np

    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32)


def transcribe(path, model_name, device, prompt):
    from faster_whisper import WhisperModel

    audio = decode(path)

    def go(dev, compute):
        print(f"Whisper {model_name} di {dev} ({compute})...", flush=True)
        model = WhisperModel(model_name, device=dev, compute_type=compute)
        segments, info = model.transcribe(
            audio, language="id", word_timestamps=True, beam_size=5,
            initial_prompt=prompt or None, condition_on_previous_text=False, vad_filter=False,
        )
        words = []
        for seg in segments:
            for w in seg.words or []:
                words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
                              "p": round(w.probability, 3)})
        return words

    if device in ("auto", "cuda"):
        try:
            return go("cuda", "float16")
        except Exception as e:  # missing CUDA/cuDNN DLLs on Windows land here
            if device == "cuda":
                raise
            print(f"GPU tidak bisa dipakai ({type(e).__name__}: {str(e)[:120]}). Pindah ke CPU.", flush=True)
    return go("cpu", "int8")


def join_reduplication(words):
    """Whisper splits 'orang-orang' into 'orang' + '-orang'; put them back together."""
    out = []
    for w in words:
        if out and w["w"].startswith("-"):
            prev = out[-1]
            out[-1] = {**prev, "w": prev["w"] + w["w"], "end": w["end"], "p": min(prev["p"], w["p"])}
        else:
            out.append(dict(w))
    return out


def apply_glossary(words, ganti, cek):
    words = join_reduplication(words)
    out, i = [], 0
    while i < len(words):
        for n in range(min(MAX_PHRASE, len(words) - i), 0, -1):
            group = words[i:i + n]
            key = " ".join(norm(w["w"]) for w in group)
            if key in ganti:
                tail = re.search(r"[^\w@]+$", group[-1]["w"])
                fixed = ganti[key] + (tail.group(0) if tail else "")
                changed = fixed != " ".join(w["w"] for w in group)
                out.append({"w": fixed, "start": group[0]["start"], "end": group[-1]["end"],
                            "p": min(w["p"] for w in group),
                            **({"asli": " ".join(w["w"] for w in group)} if changed else {})})
                i += n
                break
        else:
            out.append(dict(words[i]))
            i += 1
    for w in out:
        if "asli" not in w and (w["p"] < LOW_PROB or norm(w["w"]) in cek):
            w["cek"] = True
    return out


def write_md(path, words):
    lines, line = [], []
    start = words[0]["start"] if words else 0
    for w in words:
        if not line:
            start = w["start"]
        line.append(f"[[{w['w']}]]" if w.get("cek") else w["w"])
        if re.search(r"[.?!]$", w["w"]) or len(line) >= 14:
            lines.append(f"`{tc(start)}` " + " ".join(line))
            line = []
    if line:
        lines.append(f"`{tc(start)}` " + " ".join(line))
    fixed = [f"- {w['asli']} -> {w['w']} ({tc(w['start'])})" for w in words if "asli" in w]
    marked = [f"- {w['w']} ({tc(w['start'])}, yakin {int(w['p'] * 100)}%)" for w in words if w.get("cek")]
    body = ["# Transkrip", "", "Kata dalam [[kurung ganda]] perlu dicek dengan telinga.", "", *lines, ""]
    body += ["## Diganti glosarium", "", *(fixed or ["- (tidak ada)"]), ""]
    body += ["## Perlu dicek", "", *(marked or ["- (tidak ada)"]), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(body))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post")
    ap.add_argument("--model", default="large-v3", help="model Whisper (default large-v3)")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--glosarium-saja", action="store_true", help="pakai transkrip.mentah.json yang ada, hanya terapkan glosarium lagi")
    a = ap.parse_args()

    vdir = video_dir(a.post)
    ganti, cek, prompt = load_glossary(vdir)
    raw_path = os.path.join(vdir, "transkrip.mentah.json")
    if a.glosarium_saja:
        raw = load_json(raw_path)
        if raw is None:
            sys.exit("transkrip.mentah.json belum ada. Jalankan tanpa --glosarium-saja dulu.")
        words = raw["kata"]
    else:
        src = os.path.join(vdir, "potong.mp4")
        if not os.path.exists(src):
            sys.exit("potong.mp4 belum ada. Jalankan lib/video/potong.py dulu.")
        words = transcribe(src, a.model, a.device, prompt)
        save_json(raw_path, {"model": a.model, "bahasa": "id", "kata": words})

    fixed = apply_glossary(words, ganti, cek)
    save_json(os.path.join(vdir, "transkrip.json"), {"kata": fixed})
    write_md(os.path.join(vdir, "transkrip.md"), fixed)

    n_fix = sum(1 for w in fixed if "asli" in w)
    n_cek = sum(1 for w in fixed if w.get("cek"))
    print(f"\n{len(fixed)} kata, {n_fix} dikoreksi glosarium, {n_cek} perlu dicek.")
    print(f"Baca {os.path.join(vdir, 'transkrip.md')}")
    if n_cek:
        print("[CEK] Ada kata yang ditandai. Dengarkan bagian itu; kalau salah, tambahkan ke glosarium post lalu jalankan --glosarium-saja.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
potong.py - step 1 of the video pipeline: conform the raw phone recording and
cut every pause longer than 0.35 s (Video Brain section 6) with auto-editor.

  py lib/video/potong.py konten/<post>
  py lib/video/potong.py konten/<post> --jeda 0.35 --ambang 0.04

Input:  <post>/video/mentah.mp4 (or .mov)
Output: <post>/video/prep.mp4    1080 x 1920, 30 fps CFR, 48 kHz, rotation applied
        <post>/video/potong.mp4  the cut video
        <post>/video/potong.json durations and the time of every cut in potong.mp4

How the 0.35 s works: auto-editor keeps a margin of audio on each side of every
loud section. A margin of half the allowed pause (0.175 s) means a pause up to
0.35 s stays whole, and a longer pause is trimmed down to 0.35 s. Nothing that
is louder than the threshold is ever removed, but a soft word ending can sit
under it: always listen to potong.mp4 before going on.

Colour is untouched (no filter, no smoothing). Face and voice are never
altered: this only removes time.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _video import FPS, H, W, duration, find_raw, load_json, need, probe, run, save_json, tc, video_dir  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post")
    ap.add_argument("--jeda", type=float, default=0.35, help="jeda terpanjang yang dibiarkan, detik (default 0.35)")
    ap.add_argument("--ambang", default="0.04", help="ambang suara auto-editor, 0-1 (default 0.04). Naikkan kalau ruangan bising")
    a = ap.parse_args()

    need("ffmpeg")
    need("auto-editor")
    vdir = video_dir(a.post)
    raw = find_raw(vdir)
    if not raw:
        sys.exit(f"Rekaman mentah belum ada. Simpan sebagai {os.path.join(vdir, 'mentah.mp4')}")

    info = probe(raw)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    if not v or not any(s["codec_type"] == "audio" for s in info["streams"]):
        sys.exit("Rekaman harus punya gambar dan suara.")
    print(f"Mentah: {os.path.basename(raw)}  {v['width']}x{v['height']}  {v.get('avg_frame_rate')}  {tc(float(info['format']['duration']))}")

    # 1. Conform. ffmpeg applies the phone's rotation flag on decode; scale to
    # cover 1080 x 1920 and centre-crop anything extra (a 9:16 file is untouched
    # apart from scaling). Constant 30 fps so both renderers seek exactly.
    prep = os.path.join(vdir, "prep.mp4")
    run(["ffmpeg", "-v", "error", "-stats", "-y", "-i", raw,
         "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1",
         "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", prep])

    # 2. Cut pauses.
    margin = f"{a.jeda / 2:.3f}s"
    potong = os.path.join(vdir, "potong.mp4")
    v3 = os.path.join(vdir, "potong.v3")  # auto-editor forces the .v3 extension
    common = [prep, "--margin", margin, "--edit", f"audio:threshold={a.ambang}", "-fps", str(FPS)]
    run(["auto-editor", *common, "--export", "v3", "-o", v3, "--progress", "none"])
    run(["auto-editor", *common, "-c:v", "libx264", "-b:v", "20M", "-c:a", "aac", "-b:a", "256k",
         "-o", potong, "--progress", "none"])

    tl = load_json(v3)
    clips = tl["v"][0] if tl.get("v") else []
    cuts = [round(c["start"] / FPS, 3) for c in clips[1:]]
    before, after = duration(prep), duration(potong)
    save_json(os.path.join(vdir, "potong.json"), {
        "jeda_maks": a.jeda, "ambang": a.ambang,
        "durasi_mentah": round(before, 3), "durasi_potong": round(after, 3),
        "potongan": cuts,
    })

    print(f"\nDurasi: {tc(before)} -> {tc(after)} ({before - after:.1f} s dibuang, {len(cuts)} potongan)")
    notes = []
    if cuts and cuts[0] > 2.0:
        notes.append(("WARN", f"Potongan pertama baru di {tc(cuts[0])}. Video Brain minta potongan pertama sekitar detik 1,5-2; "
                               "kalau kalimat pertama tanpa jeda, tambahkan snap zoom di edit.json."))
    if not cuts:
        notes.append(("WARN", "Tidak ada jeda yang dipotong. Cek apakah ambang terlalu rendah untuk ruangan ini."))
    if (before - after) / max(before, 0.01) > 0.45:
        notes.append(("WARN", "Lebih dari 45% durasi terbuang. Kemungkinan ambang terlalu tinggi dan memotong suara pelan; dengarkan dulu."))
    notes.append(("CEK", f"Dengarkan {potong} sampai habis: pastikan tidak ada ujung kata yang terpotong."))
    for level, msg in notes:
        print(f"[{level}] {msg}")
    sys.exit(1 if any(l == "FAIL" for l, _ in notes) else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
render.py - step 4: render timeline.json with HyperFrames, Remotion or both,
normalise the voice to about -14 LUFS, export the MP4 and pull out the frames
to look at before anything is shown to Irsyad.

  py lib/video/render.py konten/<post>                     # both engines
  py lib/video/render.py konten/<post> --mesin hf
  py lib/video/render.py konten/<post> --mesin remotion --draft

Output: <post>/output/video-hf.mp4, video-remotion.mp4   final files (H.264, AAC 48 kHz, faststart)
        <post>/output/frame-<mesin>/NN-<time>.png       full-size frames at the key moments
        <post>/output/cek-<mesin>.png                    contact sheet of those frames

Loudness: two-pass FFmpeg loudnorm to -14 LUFS integrated, true peak -1.5 dBTP
(Video Brain section 6), then measured again and printed. Still check on a
phone speaker. Video is copied, not re-encoded, in the loudness pass.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _video import LIB, ROOT, load_json, need, run, save_json, tc, video_dir  # noqa: E402
import hf  # noqa: E402

LUFS, TP, LRA = -14.0, -1.5, 11.0


def node_bin(pkg, name):
    meta = load_json(os.path.join(LIB, "node_modules", pkg, "package.json"))
    if not meta:
        sys.exit(f"{pkg} belum terpasang. Jalankan: cd lib/video && npm install")
    rel = meta["bin"][name] if isinstance(meta["bin"], dict) else meta["bin"]
    return os.path.join(LIB, "node_modules", pkg, rel)


def render_hf(post, vdir, draft):
    folder = hf.build(post)
    out = os.path.join(vdir, "render-hf.mp4")
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")
    run(["node", node_bin("hyperframes", "hyperframes"), "lint", folder], env=env, cwd=LIB)
    run(["node", node_bin("hyperframes", "hyperframes"), "render", folder, "-o", out,
         "-q", "draft" if draft else "delivery"], env=env, cwd=LIB)
    return out


def render_remotion(post, vdir, draft):
    tl = load_json(os.path.join(vdir, "timeline.json"))
    # Remotion serves files from one public folder (<post>/video): copy images
    # and sound effects in and point the props at the copies.
    for i, o in enumerate(tl["objek"]):
        name = f"objek-{i}{os.path.splitext(o['gambar'])[1]}"
        shutil.copy2(os.path.join(os.path.abspath(post), o["gambar"]), os.path.join(vdir, name))
        o["gambar"] = name
    if tl["sfx"]:
        os.makedirs(os.path.join(vdir, "sfx"), exist_ok=True)
        for s in tl["sfx"]:
            shutil.copy2(os.path.join(ROOT, "assets", "sfx", os.path.basename(s["src"])), os.path.join(vdir, s["src"]))
    props = os.path.join(vdir, "remotion-props.json")
    save_json(props, tl)
    out = os.path.join(vdir, "render-remotion.mp4")
    run(["node", node_bin("@remotion/cli", "remotion"), "render", os.path.join(LIB, "remotion", "index.tsx"), "Video", out,
         f"--props={props}", f"--public-dir={vdir}", "--codec=h264", f"--crf={28 if draft else 16}",
         "--audio-codec=aac", "--audio-bitrate=256k"], cwd=LIB)
    return out


def loudnorm(src, dst):
    first = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", f"loudnorm=I={LUFS}:TP={TP}:LRA={LRA}:print_format=json",
         "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr)
    if not m:
        sys.exit("Gagal mengukur loudness:\n" + first.stderr[-800:])
    me = json.loads(m.group(0))
    # Plain gain keeps the voice untouched. When that gain would push peaks
    # over -1.5 dBTP, add a peak limiter after it (loudnorm's own dynamic mode
    # undershoots on short clips), then correct the gain once from a re-measure.
    gain = LUFS - float(me["input_i"])

    def encode(af):
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
             "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", dst])

    if float(me["input_tp"]) + gain <= TP:
        encode(f"loudnorm=I={LUFS}:TP={TP}:LRA={LRA}:measured_I={me['input_i']}:measured_TP={me['input_tp']}:"
               f"measured_LRA={me['input_lra']}:measured_thresh={me['input_thresh']}:"
               f"offset={me['target_offset']}:linear=true")
    else:
        print(f"  Puncak suara terlalu tinggi untuk gain biasa (+{gain:.1f} dB); pakai gain + limiter.")
        limit = 10 ** ((TP - 0.5) / 20)  # sample-peak ceiling with room for true peak
        for _ in range(2):
            encode(f"aresample=192000,volume={gain:.2f}dB,alimiter=limit={limit:.4f}:attack=3:release=60:level=disabled,"
                   f"aresample=48000")
            got, _peak = measure(dst)
            if got is None or abs(got - LUFS) <= 0.3:
                break
            gain += LUFS - got
    return float(me["input_i"])


def measure(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def key_moments(tl):
    D = tl["durasi"]
    moments = [(0.0, "frame-1")]
    for b in tl["input_bar"]:
        if not b["kosong"]:
            moments.append((max(b["selesai"] - 0.1, 0), "hook-akhir"))
    kw = next((c for c in tl["caption"] if any(p["kw"] for p in c["kata"])), None)
    if kw:
        moments.append(((kw["mulai"] + kw["selesai"]) / 2, "kata-kunci"))
    for z in tl["zoom"][:2]:
        moments.append(((z["mulai"] + z["selesai"]) / 2, "zoom"))
    for o in tl["objek"][:2]:
        moments.append(((o["mulai"] + o["selesai"]) / 2, "objek"))
    for k in tl["kartu_angka"]:
        moments.append(((k["mulai"] + k["selesai"]) / 2, "kartu"))
    if tl.get("contekan"):
        c = tl["contekan"]
        moments.append(((c["mulai"] + c["selesai"]) / 2, "contekan"))
    moments.append((max(D - 0.1, 0), "akhir"))
    t = 5.0
    while len(moments) < 12 and t < D - 1:
        moments.append((t, "isi"))
        t += 5.0
    seen, out = set(), []
    for t, name in sorted(moments)[:12]:
        f = round(t * tl["fps"])
        if f not in seen:
            seen.add(f)
            out.append((t, name))
    return out


def frames(video, tl, outdir, sheet):
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    thumbs = []
    for n, (t, name) in enumerate(key_moments(tl), 1):
        path = os.path.join(outdir, f"{n:02d}-{t:05.2f}s-{name}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", path], check=True)
        thumbs.append(path)
    from PIL import Image, ImageDraw

    cols = 6
    tw, th = 270, 480
    rows = (len(thumbs) + cols - 1) // cols
    img = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 30) + (rows + 1) * 8), "#111")
    d = ImageDraw.Draw(img)
    for i, p in enumerate(thumbs):
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 38)
        img.paste(Image.open(p).resize((tw, th)), (x, y))
        d.text((x + 4, y + th + 6), os.path.basename(p)[3:-4], fill="#fff")
    img.save(sheet)
    return thumbs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post")
    ap.add_argument("--mesin", default="keduanya", choices=["keduanya", "hf", "remotion"])
    ap.add_argument("--draft", action="store_true", help="render cepat kualitas rendah untuk cek timing")
    a = ap.parse_args()

    need("ffmpeg")
    vdir = video_dir(a.post)
    tl = load_json(os.path.join(vdir, "timeline.json"))
    if not tl:
        sys.exit("timeline.json belum ada. Jalankan lib/video/timeline.py dulu.")
    outdir = os.path.join(os.path.abspath(a.post), "output")
    os.makedirs(outdir, exist_ok=True)

    engines = ["hf", "remotion"] if a.mesin == "keduanya" else [a.mesin]
    finals = {}
    for e in engines:
        print(f"\n=== Render {e} ===", flush=True)
        raw = render_hf(a.post, vdir, a.draft) if e == "hf" else render_remotion(a.post, vdir, a.draft)
        final = os.path.join(outdir, f"video-{e}.mp4")
        before = loudnorm(raw, final)
        i, p = measure(final)
        frames(final, tl, os.path.join(outdir, f"frame-{e}"), os.path.join(outdir, f"cek-{e}.png"))
        finals[e] = final
        print(f"[{e}] {final}\n      loudness {before:.1f} -> {i} LUFS, puncak {p} dBFS")
        if i is not None and abs(i - LUFS) > 1.0:
            print(f"[WARN] Loudness {i} LUFS, lebih dari 1 LU dari target {LUFS}.")

    if len(finals) == 2:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", finals["hf"], "-i", finals["remotion"],
                            "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-"], capture_output=True, text=True)
        m = re.findall(r"All:([\d.]+)", r.stderr)
        if m:
            print(f"\nKemiripan gambar HyperFrames vs Remotion (SSIM, 1 = identik): {float(m[-1]):.4f}")
    print("\n[CEK] Lihat setiap PNG di folder frame sebelum video ditunjukkan ke Irsyad.")


if __name__ == "__main__":
    main()

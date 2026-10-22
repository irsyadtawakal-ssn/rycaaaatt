#!/usr/bin/env python3
"""
hf.py - build the HyperFrames project for one video from timeline.json.

  py lib/video/hf.py konten/<post>

Writes a self-contained folder <post>/video/hf/ (index.html, captions.css,
komposisi.css, fonts, gsap, the video and any images and sound effects), so
HyperFrames only ever reads files inside it. Render it with lib/video/render.py.

Captions, input bar, cards and the Contekan are timed clips (data-start /
data-duration). The GSAP timeline only drives the snap zoom, the caret blink
and, for the A/B test version, the typed-out hook. No Math.random, no clock.
"""

import argparse
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _video import LIB, ROOT, load_json, video_dir  # noqa: E402


def link_or_copy(src, dst):
    if os.path.exists(dst):
        if os.path.getsize(dst) == os.path.getsize(src) and os.path.getmtime(dst) >= os.path.getmtime(src):
            return
        os.remove(dst)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def words_html(parts, prefix=None, tail=""):
    """tail (the caret) is glued to the last word so it never drops to its own line."""
    out = []
    for i, p in enumerate(parts):
        t = html.escape(p["t"])
        if prefix is not None:  # one span per character, for the typed-out hook
            t = "".join(f'<span class="ch" id="{prefix}-{i}-{j}" style="visibility:hidden">{html.escape(c)}</span>'
                        for j, c in enumerate(p["t"]))
        out.append(f'<span class="kw">{t}</span>' if p["kw"] else t)
    if tail:
        if out:
            out[-1] = f'<span style="white-space:nowrap">{out[-1]}{tail}</span>'
        else:
            out.append(tail)
    return " ".join(out)


def clip(tag_id, cls, a, b, inner, extra=""):
    return (f'<div id="{tag_id}" class="{cls} clip" data-start="{a:.3f}" data-duration="{max(b - a, 1 / 30):.3f}"{extra}>'
            f"{inner}</div>")


def build(post):
    vdir = video_dir(post)
    tl = load_json(os.path.join(vdir, "timeline.json"))
    if not tl:
        sys.exit("timeline.json belum ada. Jalankan lib/video/timeline.py dulu.")
    out = os.path.join(vdir, "hf")
    os.makedirs(os.path.join(out, "fonts"), exist_ok=True)

    css = open(os.path.join(LIB, "captions.css"), encoding="utf-8").read()
    css = css.replace("../../assets/fonts/", "fonts/")
    open(os.path.join(out, "captions.css"), "w", encoding="utf-8").write(css)
    shutil.copy2(os.path.join(LIB, "komposisi.css"), out)
    for f in re.findall(r'url\("fonts/([^"]+)"\)', css):
        shutil.copy2(os.path.join(ROOT, "assets", "fonts", f), os.path.join(out, "fonts", f))
    shutil.copy2(os.path.join(LIB, "node_modules", "gsap", "dist", "gsap.min.js"), out)
    link_or_copy(os.path.join(vdir, tl["video"]), os.path.join(out, tl["video"]))

    D = tl["durasi"]
    body, js = [], []

    body.append(f'<div class="video-wrap" id="vwrap"><video id="v" class="clip" data-start="0" data-duration="{D:.3f}" '
                f'data-has-audio="true" src="{tl["video"]}" playsinline></video></div>')

    objs = []
    for i, o in enumerate(tl["objek"]):
        name = f"objek-{i}{os.path.splitext(o['gambar'])[1]}"
        shutil.copy2(os.path.join(os.path.abspath(post), o["gambar"]), os.path.join(out, name))
        objs.append(clip(f"obj{i}", "objek", o["mulai"], o["selesai"], f'<img src="{name}" alt="">'))
    body.append(f'<div class="zone-atas">{"".join(objs)}</div>')

    for i, b in enumerate(tl["input_bar"]):
        cls = "input-bar is-empty" if b["kosong"] else "input-bar"
        typed = b.get("ketik") and not b["kosong"]
        inner = words_html(b["kata"], prefix=f"h{i}" if typed else None,
                           tail=f'<span class="caret" id="caret{i}"></span>')
        body.append(clip(f"bar{i}", cls, b["mulai"], b["selesai"], inner))
        # caret blink, 0.5 s on / 0.5 s off, written out (no infinite repeat)
        t = b["mulai"] + 0.5
        on = False
        while t < b["selesai"]:
            js.append(f'tl.set("#caret{i}", {{opacity: {1 if on else 0}}}, {t:.3f});')
            on = not on
            t += 0.5
        if typed:
            chars = [(w, j) for w, p in enumerate(b["kata"]) for j in range(len(p["t"]))]
            step = 1.5 / max(len(chars), 1)
            for k, (w, j) in enumerate(chars):
                js.append(f'tl.set("#h{i}-{w}-{j}", {{visibility: "visible"}}, {b["mulai"] + k * step:.3f});')

    for i, c in enumerate(tl["caption"]):
        body.append(clip(f"cap{i}", "cap", c["mulai"], c["selesai"], words_html(c["kata"])))

    for i, k in enumerate(tl["kartu_angka"]):
        inner = (f'<div class="angka">{html.escape(k["angka"])}</div><div class="label">{html.escape(k["label"])}</div>'
                 + (f'<div class="sumber">{html.escape(k["sumber"])}</div>' if k.get("sumber") else ""))
        body.append(clip(f"kartu{i}", "card-angka", k["mulai"], k["selesai"], inner))

    c = tl.get("contekan")
    if c:
        rows = "".join(f"<li>{html.escape(p)}</li>" for p in c["poin"])
        body.append(clip("contekan", "contekan", c["mulai"], c["selesai"],
                         f'<div class="judul">{html.escape(c["judul"])}</div><ol>{rows}</ol>'))

    for z in tl["zoom"]:
        js.append(f'tl.set("#vwrap", {{scale: {z["skala"]}}}, {z["mulai"]:.3f});')
        js.append(f'tl.set("#vwrap", {{scale: 1}}, {z["selesai"]:.3f});')

    for i, s in enumerate(tl["sfx"]):
        name = os.path.basename(s["src"])
        shutil.copy2(os.path.join(ROOT, "assets", "sfx", name), os.path.join(out, name))
        body.append(f'<audio id="sfx{i}" data-start="{s["mulai"]:.3f}" data-duration="{s["durasi"]:.3f}" '
                    f'data-volume="{s["volume"]}" src="{name}"></audio>')

    body.append(f'<div class="handle">{html.escape(tl["handle"])}</div>')

    page = f"""<!doctype html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={tl['lebar']}, height={tl['tinggi']}" />
<title>video</title>
<link rel="stylesheet" href="captions.css" />
<link rel="stylesheet" href="komposisi.css" />
<script src="gsap.min.js"></script>
<style>body {{ margin: 0; background: #000; }}</style>
</head>
<body>
<div id="root" class="frame" data-composition-id="main" data-start="0" data-duration="{D:.3f}"
     data-width="{tl['lebar']}" data-height="{tl['tinggi']}" data-fps="{tl['fps']}">
{chr(10).join(body)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {D:.3f});
window.__timelines.main = tl;
</script>
</body>
</html>
"""
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("post")
    a = ap.parse_args()
    print(f"Ditulis: {build(a.post)}")


if __name__ == "__main__":
    main()

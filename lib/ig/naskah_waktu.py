#!/usr/bin/env python3
"""
naskah_waktu.py - time a video script before recording, and check it against
the three-loop structure in brand/06-video-brain.md (section 2).

It estimates how long each beat takes to say (by Indonesian syllables, which
is fairer than counting words), stacks the beats into timecodes, and flags:
a hook past 3 seconds, a beat over 4 seconds with nothing changing on screen,
fewer than two rehooks, rehooks that all open with the same word, three beats
in a row with nothing concrete in them, and an ending that does not loop back
to the hook.

Input is either the script table from Video Brain section 8 (it reads the
"Loop part" and "Spoken" columns) or plain text with one beat per line and an
optional label in square brackets:

    [hook] Kebanyakan orang nanya ke ChatGPT kayak nanya ke Google.
    [hook] Tapi justru itu yang bikin jawabannya meleset.
    [intensify] Saya juga gitu dulu, ngulang prompt sampai lima kali.
    [set-up] AI itu kayak karyawan baru. Pintar, tapi belum tahu konteks kerjaanmu.
    [rehook] Nah, konteks apa yang perlu dikasih?
    ...
    [payoff] Coba kalimat ini di chat berikutnya.

Usage
  py lib/ig/naskah_waktu.py konten/<post>/1-naskah.md --target 30
  py lib/ig/naskah_waktu.py naskah.txt --sps 6.2
  py lib/ig/naskah_waktu.py naskah.txt --ukur 31.5     # calibrate: you read it in 31.5 s

Speaking rate: --sps is syllables per second. The default (5.5) is only an
estimate. Read one script aloud at your normal on-camera pace, time it, run
with --ukur <seconds>, and use the number it gives you from then on.

Adapted from beats.py in Jake Schincariol's instagram-agent-skill (MIT),
rewritten for Indonesian and the three-loop structure.
See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _teks import CONCRETE_RE, content_words, count_syllables, words  # noqa: E402

DEFAULT_SPS = 5.5
FIRST_LINE_BY = 3.0
HOOK_WINDOW = 5.5
MAX_BEAT = 4.0
INTENSIFY_BY = 10.0
ABSTRACT_RUN = 3


def kind(label):
    l = label.lower()
    if "hook" in l and "rehook" not in l and "ending" not in l and "akhir" not in l:
        return "hook"
    if "intens" in l:
        return "intensify"
    if "rehook" in l:
        return "rehook"
    if "payoff" in l or "ending" in l or "akhir" in l:
        return "payoff"
    if "set" in l:
        return "setup"
    return ""


def parse(raw):
    lines = raw.splitlines()
    table = [l for l in lines if l.strip().startswith("|")]
    beats = []
    if len(table) >= 3:
        head = [c.strip().lower() for c in table[0].strip().strip("|").split("|")]
        try:
            i_spoken = next(i for i, c in enumerate(head) if "spoken" in c or "ucapan" in c or "dialog" in c)
        except StopIteration:
            i_spoken = None
        i_part = next((i for i, c in enumerate(head) if "loop" in c or "bagian" in c or "part" in c), None)
        if i_spoken is not None:
            for row in table[2:]:
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if len(cells) <= i_spoken:
                    continue
                text = cells[i_spoken].strip().strip('"“”')
                if not text or text in ("…", "..."):
                    continue
                label = cells[i_part] if i_part is not None and i_part < len(cells) else ""
                beats.append((label, text))
            return beats
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[([^\]]+)\]\s*(.+)$", line)
        beats.append((m.group(1), m.group(2)) if m else ("", line))
    return beats


def tc(s):
    m, s = divmod(s, 60)
    return f"{int(m)}:{s:04.1f}"


def main():
    ap = argparse.ArgumentParser(description="Time a video script and check its loops.")
    ap.add_argument("file", help="script file, or - for stdin")
    ap.add_argument("--sps", type=float, default=DEFAULT_SPS, help="syllables per second (default 5.5)")
    ap.add_argument("--target", type=float, help="target length in seconds")
    ap.add_argument("--ukur", type=float, help="seconds it actually took you to read the script aloud")
    a = ap.parse_args()

    raw = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    beats = parse(raw)
    if not beats:
        print("Tidak ada baris naskah yang terbaca.", file=sys.stderr)
        sys.exit(2)

    total_syl = sum(count_syllables(t) for _, t in beats)
    if a.ukur:
        rate = total_syl / a.ukur
        print(f"{total_syl} suku kata dalam {a.ukur:.1f} detik = {rate:.2f} suku kata per detik.")
        print(f"Pakai --sps {rate:.1f} untuk naskah berikutnya.")
        return

    rows, clock = [], 0.0
    for label, text in beats:
        dur = count_syllables(text) / a.sps
        rows.append({"label": label, "kind": kind(label), "text": text, "start": clock, "dur": dur,
                     "words": len(words(text)), "concrete": len(CONCRETE_RE.findall(text))})
        clock += dur
    total = clock
    if not any(r["kind"] for r in rows):
        rows[0]["kind"] = "hook"

    head = f"NASKAH  ·  {len(rows)} beat  ·  ~{total:.1f} detik pada {a.sps} suku kata/detik"
    if a.target:
        head += f"  ·  target {a.target:.0f} detik"
    print("\n" + head)
    print("=" * max(len(head), 78))
    for r in rows:
        tag = (r["label"] or "")[:14]
        flag = "  <- lebih dari 4 dtk" if r["dur"] > MAX_BEAT else ""
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {tag:<14} {r['text'][:62]}{flag}")
    print("-" * max(len(head), 78))

    notes = []
    hook = [r for r in rows if r["kind"] == "hook"]
    hook_end = max(r["start"] + r["dur"] for r in hook)
    first_end = rows[0]["dur"]
    if first_end > FIRST_LINE_BY:
        notes.append(("FAIL", f"Kalimat pertama baru selesai di detik {first_end:.1f}, lewat dari 3 detik. "
                              f"Pangkas jadi sekitar 6-8 kata (sekarang {rows[0]['words']})."))
    else:
        notes.append(("PASS", f"Kalimat pertama selesai di detik {first_end:.1f}."))
    if hook_end > HOOK_WINDOW:
        notes.append(("WARN", f"Hook loop selesai di detik {hook_end:.1f}; usahakan sekitar 5 detik."))

    inten = [r for r in rows if r["kind"] == "intensify"]
    if not inten:
        notes.append(("WARN", "Belum ada bagian intensify setelah hook."))
    elif inten[-1]["start"] + inten[-1]["dur"] > INTENSIFY_BY:
        notes.append(("WARN", f"Intensify baru selesai di detik {inten[-1]['start'] + inten[-1]['dur']:.1f}; usahakan sebelum detik 8-10."))

    rehooks = [r for r in rows if r["kind"] == "rehook"]
    if len(rehooks) < 2:
        notes.append(("WARN", f"{len(rehooks)} rehook. Untuk video 20-40 detik, pakai 2."))
    elif len(rehooks) > 3:
        notes.append(("WARN", f"{len(rehooks)} rehook. Lebih dari 3 terasa dipancing terus."))
    firsts = [words(r["text"])[0].lower() for r in rehooks if words(r["text"])]
    if len(firsts) >= 2 and len(set(firsts)) == 1:
        notes.append(("WARN", f"Semua rehook dibuka dengan '{firsts[0]}'. Variasikan."))

    if rows[-1]["kind"] != "payoff" and not any(r["kind"] == "payoff" for r in rows[-2:]):
        notes.append(("WARN", "Bagian terakhir belum ditandai payoff."))

    long_beats = [str(i + 1) for i, r in enumerate(rows) if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(("WARN", f"Beat {', '.join(long_beats)} lebih dari 4 detik. Pecah kalimatnya atau ganti visual di tengahnya."))

    run = 0
    for i, r in enumerate(rows):
        run = run + 1 if r["concrete"] == 0 else 0
        if run == ABSTRACT_RUN:
            notes.append(("WARN", f"Beat {i - 1}-{i + 1} tidak punya angka, nama, atau contoh nyata. Isi salah satunya."))

    first_words = content_words(" ".join(r["text"] for r in hook))
    last_words = content_words(rows[-1]["text"])
    shared = sorted(first_words & last_words)
    if shared:
        notes.append(("PASS", f"Loop: kalimat terakhir mengulang '{', '.join(shared[:3])}' dari hook."))
    else:
        notes.append(("WARN", "Kalimat terakhir tidak mengulang kata dari hook. Ulang satu kata kunci supaya loop-nya nyambung."))

    if a.target:
        delta = total - a.target
        if abs(delta) <= a.target * 0.1:
            notes.append(("PASS", f"Durasi pas ({total:.1f} dari {a.target:.0f} detik)."))
        elif delta > 0:
            notes.append(("WARN", f"Lebih {delta:.1f} detik dari target. Buang sekitar {int(delta * a.sps)} suku kata."))
        else:
            notes.append(("WARN", f"Kurang {-delta:.1f} detik dari target. Video pendek biasanya lebih baik daripada ditambah isi."))

    for status, text in notes:
        print(f"  {status:<4}  {text}")
    print("\n  Perkiraan berdasarkan suku kata. Kalibrasi sekali dengan --ukur.\n")
    sys.exit(1 if any(s == "FAIL" for s, _ in notes) else 0)


if __name__ == "__main__":
    main()

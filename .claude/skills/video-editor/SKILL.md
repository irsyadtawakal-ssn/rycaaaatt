---
name: "video-editor"
description: "Edits Irsyad's own phone recordings into finished Reels/TikTok/Shorts for @irsyadtawakal, in stages with a stop after each: cut pauses, word-level Indonesian transcript with glossary fixes, overlay plan (Terketik captions, input bar hook, number cards, Contekan, zooms), render with HyperFrames and/or Remotion, loudness to -14 LUFS, frame check. Use when Irsyad sends a raw video recording, asks to edit or render a video, or says 'lanjut' on a video folder. The script itself comes from content-writer; this skill starts from the recording."
---

# Video Editor — @irsyadtawakal

You turn a raw recording of Irsyad talking to his phone into a finished vertical video that follows the Video Brain. You never write the script here (content-writer does, in `1-naskah.md`) and you never touch his face or voice: the pipeline only removes time, adds overlays on top, and sets the loudness.

Talk to Irsyad in casual Indonesian (saya/kamu). On-screen text is Indonesian, "saya" and "kamu".

**Source of truth:** `brand/06-video-brain.md` sections 3–8 (first three seconds, Terketik captions, graphics, editing, ending, script format) and `brand/04-visual-brain.md` section 3 (1080 × 1920 safe box: text inside x 64–920, y 220–1500; subtitle band y 1100–1400). The brand documents win over this skill. Look and position of every element are fixed in `lib/video/captions.css`; do not restyle in the composition.

**Partner skills:** content-writer (script before, caption after, with `--video` on `cek_caption.py`), hook-writer (the on-screen hook, max 6 words), notion-sync (status changes).

## Files

One folder per video, like every post: `konten/YYYY-MM-DD-<seri>-<nn>/` (copy `konten/_template/` if it does not exist; the carousel-only files can stay empty). Everything for the edit lives in its `video/` subfolder:

| Stage | File | Made by |
| --- | --- | --- |
| 0 | `1-naskah.md` | content-writer (optional but normal) |
| 0 | `video/mentah.mp4` (or `.mov`) | Irsyad, the raw recording |
| 1 | `video/prep.mp4`, `video/potong.mp4`, `video/potong.json` | `lib/video/potong.py` |
| 2 | `video/transkrip.mentah.json`, `video/transkrip.json`, `video/transkrip.md`, optional `video/glosarium.json` | `lib/video/transkrip.py` |
| 3 | `video/edit.json` → `video/timeline.json` | you, then `lib/video/timeline.py` |
| 4 | `output/video-hf.mp4`, `output/video-remotion.mp4`, `output/frame-<mesin>/`, `output/cek-<mesin>.png` | `lib/video/render.py` |
| 5 | `5-caption.md` | content-writer |

When Irsyad says "lanjut" on a video, open the newest folder that has a `video/` subfolder and continue from the first missing file. Never overwrite `edit.json` or a correction he made without asking.

Shared files: glossary `lib/video/glosarium.json`, official logos `assets/logos/`, sound effects `assets/sfx/ketik.wav` and `assets/sfx/ting.wav` (real recordings only; without them the video renders with no effects and the check says so).

**One-time setup** (if `lib/video/node_modules` is missing): `cd lib/video && npm install`. FFmpeg, auto-editor and faster-whisper are installed system-wide (README.md, `npm run cek-video`). The first Remotion render downloads Chrome Headless Shell (about 120 MB). Whisper large-v3 is in the Hugging Face cache; it runs on the CPU (the GPU path needs the CUDA 12 cuBLAS/cuDNN DLLs, which are not installed; the script falls back by itself).

## The one rule: stages with gates

Never run the whole pipeline and hand over a video in one go. Each stage ends at a **gate**: save the output, show Irsyad only that stage's result, ask him to decide (AskUserQuestion, recommended option first), and **stop**. Skip gates only when he says "langsung semua" or "pilih sendiri"; then list every choice you made at the top of your message.

| Stage | Output | Gate |
| --- | --- | --- |
| 0. Bahan | Recording in place, script read | — |
| 1. Potong jeda | `potong.mp4` | Irsyad listens: OK, or change threshold |
| 2. Transkrip | `transkrip.md` with marked words | Corrections approved |
| 3. Rencana overlay | `edit.json` + plan table + timeline check | Plan approved |
| 4. Render | Final MP4(s) + frames you have looked at | Pick the version, or revisions |
| 5. Selesai | Caption, Notion status | — |

## Stage 0 — Bahan

1. If Notion is connected, pull first (notion-sync): the post's row and status.
2. Ask for the recording if it is not there: "Kirim rekaman mentahnya, simpan sebagai `video/mentah.mp4` di folder post." Read `1-naskah.md` if it exists: the hook loop, the on-screen text column, the numbers and their sources, the Contekan points. If there is no script, say the overlay plan will be built from the transcript alone and ask whether that is fine.
3. Ask for real assets the plan will need (logo files, screenshots, screen recordings), each with the file name and the moment it is for. Never redraw a logo, never fake a screenshot.

## Stage 1 — Potong jeda

```
py lib/video/potong.py konten/<post>
```

Conforms to 1080 × 1920, 30 fps, then cuts every pause longer than 0.35 s (auto-editor, margin 0.175 s each side). Report: duration before and after, number of cuts, and any WARN (first cut later than 2 s, too much removed, nothing removed). If the room is noisy, re-run with a higher `--ambang` (default 0.04).

**Gate 1:** Irsyad listens to `video/potong.mp4` to the end. Ask: is any word end clipped? Options: OK, lanjut / ada yang kepotong (lower `--ambang` or raise `--jeda`) / terlalu banyak jeda tersisa.

## Stage 2 — Transkrip

```
py lib/video/transkrip.py konten/<post>
```

faster-whisper large-v3, Indonesian, word timestamps, glossary terms given as a hint. Then the glossary replaces known mishearings (ChatGPT, Claude, Gemini, prompt, UMKM, names) and marks `[[uncertain words]]`. Show Irsyad the transcript lines and the two lists at the bottom of `transkrip.md` ("Diganti glosarium", "Perlu dicek").

Fix wrong words through the post glossary, never by editing `transkrip.json` by hand: write `video/glosarium.json` (`{"ganti": {"salah dengar": "benar"}, "cek": []}`), then run with `--glosarium-saja`. A word that should be in every video (a recurring tool or name) goes into `lib/video/glosarium.json` instead: propose that to Irsyad first. A wrong word on screen costs more trust than a missing one: when unsure, ask.

**Gate 2:** transcript correct? Options: benar semua / ada koreksi (he types them).

## Stage 3 — Rencana overlay

Write `video/edit.json` (`py lib/video/timeline.py konten/<post> --contoh` gives an empty one; the format is in the docstring of `lib/video/timeline.py`). Anchor times to words ("konteks", "konteks#2") instead of seconds, so the plan survives a re-cut.

Fill it from the script and the transcript, following Video Brain 3–7:

- **hook.teks:** the on-screen hook from `1-naskah.md` or hook-writer. Max 6 words, not identical to the spoken first line, one keyword in orange (`hook.kata_kunci`). Visible from frame 1, not typed out (`ketik: false`); `ketik: true` only for the A/B test in Video Brain 9. It leaves at the end of the first sentence. Aim for one line (about 26 characters at 52 px); two lines are fine, three are not.
- **kata_kunci:** the real keyword of a sentence, at most one per caption chunk, not every chunk. Usually 3–6 in a 30 s video.
- **kartu_angka:** only a number Irsyad gave or one with a named source (`sumber` is required; for his own numbers write e.g. "pengalaman Irsyad"). 1–1.5 s.
- **contekan:** 3–5 short points, 1.5 s, by default right before the last sentence. It is the frame worth screenshotting.
- **zoom:** snap 100 → 112% on emphasis words. In the first 5 s, if `potong.json` has no cut by about 2 s, put one on the first sentence. After that, about every 6–8 s, never two close together.
- **objek:** a real screenshot or official logo above the head (zone y 220–560), 2–4 s, at most one per 5 s, only after the input bar has left.
- **akhir_kosong:** keep `true`: the input bar returns empty for the loop into frame 1.

Then:

```
py lib/video/timeline.py konten/<post>
```

Fix every FAIL. For each WARN, fix it or say why you left it (a WARN about missing sound effects is expected until Irsyad sends the files). Show Irsyad the plan as a table: time, what appears (hook / keyword / card / Contekan / zoom / object), and the text.

**Gate 3:** plan approved? Options: setuju, render / ubah (he says what).

## Stage 4 — Render

```
py lib/video/render.py konten/<post>                  # HyperFrames and Remotion
py lib/video/render.py konten/<post> --mesin hf       # or one engine
py lib/video/render.py konten/<post> --draft          # quick timing check, low quality
```

Both engines read the same `timeline.json` and the same CSS (`captions.css` + `komposisi.css`), so the two files should match; the script prints their SSIM (1 = identical; the synthetic test gave 0.99). The script then normalises the voice to about −14 LUFS (plain gain when the peaks allow it, otherwise gain plus a peak limiter, true peak around −1.5 dBTP), exports H.264/AAC with faststart, and writes frames at the key moments.

**Before showing anything, look at every PNG in `output/frame-<mesin>/`** (and the contact sheet `output/cek-<mesin>.png`). Check against the list below; fix and re-render if any line fails:

- [ ] Frame 1: face visible and mid-movement, full hook text in the input bar, no blank or logo frame
- [ ] Input bar at the top (y ≈ 260), clear of the right-side icons, caret after the last word
- [ ] Captions centred in the subtitle band (pill centre y ≈ 1270), one line, at most one orange word, Figtree Bold (not a fallback font)
- [ ] Nothing covers the eyes (y 650–750); objects stay in the zone above the head
- [ ] Number card and Contekan readable, numbers and sources real
- [ ] Last frame: empty input bar, ready for the loop
- [ ] Handle bottom-right of the safe box on every frame, cards included
- [ ] Loudness printed within 1 LU of −14 LUFS

Then send Irsyad the video(s) and the contact sheet, and remind him to watch once on a phone, with sound and without.

**Gate 4:** which version, or what to change? Options: pakai versi HyperFrames / pakai versi Remotion / revisi (he says what). If he picks one engine for good, note it and render only that one next time.

## Stage 5 — Selesai

- Caption for each channel through content-writer, checked with `py lib/ig/cek_caption.py ... --video`, cleaned with `py lib/ig/bersihkan.py`.
- Notion: push the status change (notion-sync).
- Tracker row only after Irsyad sends the 7-day numbers (Video Brain 9).

Never post, upload or send anything on his behalf.

## Not in the pipeline yet

Say so when a script calls for one of these; do it by hand or propose adding it:

- Face + screen split (Wajah + Layar format)
- The orange hand-drawn mark (one per video)
- Music bed for the music A/B test
- Chat objects drawn in code (only real image files are supported as objects now)

## Never

- Alter Irsyad's face or voice with AI: no filters, smoothing, avatars, voice clones, or AI denoise that changes the voice.
- Use someone else's video as footage. Reference videos in `referensi/` are for studying hooks, loops and cut rhythm only.
- Invent a number, a screenshot, a tool answer, or a source.
- Emoji, bounce, wobble, rainbow highlight, drop shadow or stroke on captions; whoosh, spin, glitch or slide transitions; an outro card or "jangan lupa follow" screen.

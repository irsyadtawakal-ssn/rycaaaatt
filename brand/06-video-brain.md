# Video Brain

Oct 21, 2026 · @irsyadtawakal

## How to use this document

This is the rulebook for every short video made for **@irsyadtawakal**: Reels, TikTok, YouTube Shorts and the talking-head formats. It sits on top of the Visual Brain: colours, fonts, safe zones and the handle position come from Visual Brain section 3 (Reels, TikTok and Stories: 1080 × 1920 px). This document adds the script structure, the first three seconds, captions, graphics, editing pace, the ending and how to test.

Retention is decided by the script first and the edit second. A tight edit cannot rescue a hook that promises nothing. Write the loops before planning a single cut.

The style in one line: **rapi, cepat, jujur**. Clean frames, fast rhythm, and nothing on screen that did not really happen.

## 1. Formats

| Format | What it is | Length to start |
| --- | --- | --- |
| **Opini 30 Detik** | Irsyad to camera with one firm opinion, a fairness turn and the way out | 25–35 s |
| **Cerita Saya** | A real experience from Pilar 4 Story, told to camera | 30–40 s |
| **Jawab Komentar** | A real comment on screen, then Irsyad answers it | 20–35 s |
| **Wajah + Layar** | Face on top, a real screen recording below | 30–40 s |
| **Ngobrol Layar** | Screen only: the chat objects play the conversation, Irsyad's voice over it | 20–35 s |
| **Wajah + Objek** | Talking head with chat objects appearing above his head | 20–35 s |
| **Bukti Layar** | A real result shown first, then how it was made | 30–40 s |
| **Carousel Hidup** | The day's carousel PNGs animated into a video with voice-over | 20–30 s |

Start at 20–40 seconds. A short video is easier to watch to the end while the account is small. Go longer only when the tracker shows people stay.

## 2. Script structure: three loops

The default shape for every video. It is our reading of Kallaway's public material (the three-step hook, "set up, rehook", and a hook at the end). The names "hook loop", "intensify" and "rehook loop" are used here as labels, not as his official definitions.

| Part | Time (30 s video) | Job |
| --- | --- | --- |
| **1. Hook loop** | 0–5 s | Open one big question in the viewer's head. The first sentence lands by about 3 s |
| **2. Intensify** | 5–10 s | Make the stakes clearer, more specific, closer to the viewer, before any answer |
| **3. Set-up 1 → rehook 1** | 10–17 s | Give one piece, then open the next small question |
| **4. Set-up 2 → rehook 2** | 17–25 s | Give the next piece, then open the last small question |
| **5. Payoff + ending hook** | 25–30 s | Close the big question with the concrete thing to try today, then flow into the loop |

### 2a. Hook loop (three steps in about 5 seconds; the first sentence lands by about 3 seconds)

Indonesian words are long: at a normal on-camera pace, 3 seconds holds only about 6–8 words. So the first sentence (the context lean-in) carries the topic and lands by about 3 seconds, and the cutting line and snapback follow straight after. Time every hook with `lib/ig/naskah_waktu.py`, calibrated to Irsyad's own pace.

1. **Context lean-in:** say plainly what the video is about, so the right viewer thinks "ini buat saya".
2. **Scroll-stop interjection:** one short cutting line.
3. **Contrarian snapback:** a line that turns against the first one.

Example: "Kebanyakan orang nanya ke ChatGPT kayak nanya ke Google. Tapi justru itu yang bikin jawabannya meleset."

The three layers land together in the first second (hook-writer, "Reels: the three-layer opening"): the visual, the spoken line and the on-screen text.

### 2b. Intensify

Raise the stakes with something real: Irsyad's own experience, a concrete situation the viewer recognises, or a number with a source. Example: "Saya juga gitu dulu. Waktu bikin laporan stok di kantor, saya harus ngulang prompt lima kali." Use it only if it really happened, otherwise write `[PERLU: detail nyata]`.

Intensify makes the stakes clearer. It never scares. "Kerjaanmu bakal diganti AI" breaks Positioning section 3; "saya ngulang lima kali" does not.

### 2c. Rehook loops

- Each set-up gives one piece of the answer, with the everyday analogy first.
- Each rehook opens one small question that the next part pays off, for example "Nah, konteks apa yang perlu dikasih? Ini bagian yang sering dilewati." or "Yang ketiga ini paling ngaruh."
- A rehook can be visual instead of spoken: a number card or a chat object appearing.
- Vary the opening word. Not "tapi" every time: "masalahnya", "nah", "anehnya", or no word at all.

### 2d. Payoff and ending hook

- The big question from the hook loop is answered here, with the concrete thing to try today: the prompt, the step, the setting.
- The last spoken line flows into the first frame, so the loop feels seamless. The easiest way: repeat one keyword from the hook in the last line (`lib/ig/naskah_waktu.py` checks this).
- The tease for the next episode is at most 1 second, or goes in the caption instead.

### Loop rules

- **Every loop that opens is closed.** A rehook that is not paid off is clickbait.
- **For 20–40 seconds: one main loop and two rehooks.** More than that feels like being baited all the time.
- **Opini tegas** keeps its fairness turn (what Irsyad is not against) and its way out, placed in set-up 2.
- No AI tells (Pilar 2 Voice 6b) in spoken lines either.

## 3. The first three seconds

- **Frame 1:** Irsyad's face is already visible and he is already talking, with movement in the frame (a hand gesture, leaning in, picking up the phone, walking into frame). Not a still face. No logo, no intro, no blank frame.
- **The hook text is fully visible from frame 1** inside the input bar (section 5). It is not typed out letter by letter, so the hook is readable immediately. The keyboard sound and "ting" play at the end of the first sentence.
- **First cut by about 1.5–2 seconds.**
- **In the first 5 seconds, something changes every 1.5–2 seconds:** a cut, a snap zoom, the input bar leaving, a chat object arriving.
- Test against the old version (the hook typed out over 1.5 s) before dropping it for good (section 9).

## 4. Captions: "Terketik"

| Property | Rule |
| --- | --- |
| Font | Figtree Bold 66 px, white |
| Chunk | 1–4 words and at most 20 characters including spaces (that is what fits one line at 66 px), broken at phrase boundaries, never mid-phrase |
| Background | A pill in Deep Indigo at 88% opacity, fully rounded ends, padding 18 × 32 px |
| Keyword | One word per chunk at most in Signal Orange, only for the real keyword of that sentence. Not every chunk gets one |
| Position | Centred horizontally, at most 760 px wide (x 160–920), centre of the pill at about y 1270 (66% of 1920), inside the subtitle band y 1100–1400 from Visual Brain section 3 |
| Timing | A chunk appears on the first word's onset from the word-level transcript and leaves when the next chunk starts. Captions follow the voice, never the other way round |
| Typing effect | Only on the hook and on keyword cards. Normal captions just appear, no caret, so they never lag behind speech |
| Never | Emoji, bounce, wobble, rainbow highlight, drop shadow, a stroke around the letters |

Correct misheard terms with the glossary before rendering (ChatGPT, Claude, Gemini, prompt, UMKM, and names). A wrong word on screen costs more trust than a missing one.

The CSS for these captions is in `lib/video/captions.css`.

## 5. Graphics

- **Input bar (video signature motif):** a chat input box, Deep Indigo at 88% with a 2 px white outline at 15%, corner radius 40 px, 856 px wide (x 64–920, clear of the right-side icons), its top edge at about y 260. It holds the on-screen hook text (at most 6 words, hook-writer rule, not identical to the spoken line), in Figtree Bold 52 px white, one keyword in orange, with the typing caret (Visual Brain section 5) after the last word. It is on screen in the first seconds and comes back empty at the end for the loop. It shares the zone above the head with the chat objects, so the first chat object arrives only after the input bar has left. Listed in the Visual Brain motif table as video only; it never appears on carousels.
- **Chat objects above the head:** in the zone between the top safe edge (y 220) and the forehead (about y 560), so they never cover the face (eyes around y 650–750, Visual Brain section 4). At most one group per 5 seconds, each on screen for 2–4 seconds.
- **Every overlay adds information** that is not already in the spoken line: the prompt, the number, the tool's real answer, a comparison. Decoration is not a reason.
- **Number card:** full screen, Deep Indigo, one giant number in Bricolage 800 orange, 1–1.5 seconds. Only for a number Irsyad gave or one with a named source.
- **Screen + face split:** face in the top half, a real screen recording or real screenshot in the bottom half. Never a mock-up of a result.
- **Tool logos:** only the official files from `assets/logos/`, unaltered and upright.
- **Orange hand-drawn mark:** one per video (a circle, an underline or an arrow on the key moment).
- **Contekan frame:** before the loop, a one-frame summary of the points (3–5 short numbered rows), held for 1.5 seconds. It is the frame worth screenshotting and sending.
- **B-roll kolase (added 26 Oct 2026, Irsyad's decision):** full-screen inserts that cover the face for a moment while the voice keeps running. Reference: the editorial collage style (cut-out photos on paper, kinetic words), studied in `planning/riset/2026-10-26-gaya-broll-ai.md`.
  - **When:** only on an analogy in intensify or a set-up. Never in the first 3 seconds (frame 1 stays the face) and never on the payoff (the payoff stays the real screen or proof).
  - **How much:** 2–3 inserts in a 30 s video, each 1.5–3 seconds, at most about 30% of the running time in total, so the face stays dominant.
  - **Look:** paper background in the pale indigo tint #F4F2FF with a thin grid, black-and-white cut-out photos, Signal Orange as the only colour. Words appear one by one in Bricolage, one word in orange.
  - **Text:** while an insert is on screen, the Terketik caption is hidden and the insert's own words take its place, so text never doubles up.
  - **A metaphor, not a literal picture:** one visual idea per sentence. "Nanya ke ChatGPT kayak nanya ke Google" becomes Irsyad holding a magnifying glass to an empty chat box, not a screenshot of Google.
  - **Objects:** cut-out images of Irsyad, everyday objects, chat objects, official logos. Images of Irsyad are AI-made from his real photos and used only as illustration, never as proof of an event or result (the same conditions as covers, Visual Brain "Photos and video framing"). The AI Irsyad never speaks, never lip-syncs, and his voice is never cloned. No AI images of other real people.
  - **Made from:** still cut-out images (ChatGPT Image or Nano Banana, background removed) animated in code with HyperFrames or Remotion. Gemini Omni only for an element that needs real motion (a hand reaching, Irsyad walking). If an insert is photorealistic video, turn on Instagram's AI label for that post.
- **Handle:** as Visual Brain section 3 (bottom of the safe box, right edge x 900, baseline y 1480, Figtree Medium 34 px white), on screen for the full video.

## 6. Editing

| Rule | Value |
| --- | --- |
| Silences | Cut any pause longer than 0.35 s (auto-editor), then check by ear that no word was clipped |
| Rhythm after the first 5 s | A visual change every 3–5 s |
| Snap zoom | 100% → 112% on emphasis, about every 6–8 s after the first 5 s; never two zooms in a row |
| Transitions | Hard cuts only. No whoosh, spin, glitch or slide transitions. Inside a B-roll kolase insert, objects and words may move in (scale, blur-in, a pin pressing in); cutting into and out of the insert stays a hard cut |
| Sound effects | Only the real keyboard and "ting" sounds, and only where something is typed or appears |
| Music | Test it (section 9): one version with no music, one with a quiet bed under the voice. Stories may use music from the start |
| Loudness | Normalise the voice to a steady level (a common target is −14 LUFS integrated) and check on a phone speaker |
| Colour | Natural. No filters, no skin smoothing |
| Face and voice | The recording is never altered with AI. No avatars, no voice clones. AI images of Irsyad appear only inside B-roll kolase inserts, under the conditions in section 5 |

## 7. Ending

1. Payoff (the thing to try today).
2. Contekan frame, 1.5 seconds.
3. The last line flows into frame 1: the input bar returns empty, ready for the hook.

No outro card, no "jangan lupa follow" screen. Comment and share prompts follow Pilar 2 Voice section 6: none unless a real asset is sent. The next-episode tease lives in the caption, or in at most one second of speech.

## 8. Script format for a video

The script in `1-naskah.md` is a table, one row per beat:

| Time | Loop part | Spoken | On-screen text / caption keyword | Visual (shot, object, screen, card) |
| --- | --- | --- | --- | --- |
| 0–5 s | Hook loop | … | … | … |

Mark the estimated total duration at the top. Read the spoken lines aloud once: if a line does not fit its time, shorten it, do not speed up.

## 9. Measuring and testing

- **Tracker:** for every video, record in `tracker/post.csv` the hook formula, the duration, the average watch time, the percentage who watched to the end, the share of viewers still there at 3 seconds (the hook's grade), the second where the retention graph drops hardest, and the non-follower share of reach. Add a row only after Irsyad sends the 7-day numbers.
- **Rapor:** the content-audit skill reads the tracker (`lib/ig/rapor.py`) and compares posts against Irsyad's own median, not against other accounts.
- **Research:** the viral-research skill shows which hook formulas are beating their own accounts in the niche; test those here before adopting them.
- **One variable per test pair.** Two videos of the same format and similar topic, differing only in the thing being tested. Decide after 3 pairs, not after one.
- **Instagram Trial Reels** can be used for a test version so it reaches non-followers first.
- **Test order:**
  1. Hook typed out over 1.5 s vs hook fully visible from frame 1.
  2. No music vs a quiet music bed (Opini 30 Detik).
  3. Captions 1–2 words vs 3–4 words per chunk.
- When a test settles, update this document and note the date.

## Pre-flight checklist

- [ ] The hook loop, intensify, two rehooks and payoff are all in the script, and every loop is closed
- [ ] `lib/ig/naskah_waktu.py` shows no FAIL: the first sentence lands by about 3 s
- [ ] Frame 1 shows the face mid-sentence, with movement, and the full hook text
- [ ] Something changes every 1.5–2 s in the first 5 s, and every 3–5 s after
- [ ] Captions sit in the subtitle band, follow the voice, and have at most one orange word per chunk
- [ ] Every overlay adds information, nothing covers the face
- [ ] B-roll kolase: none in the first 3 s or on the payoff, 1.5–3 s each, at most ~30% of the video, a metaphor and not a literal picture, no caption doubling
- [ ] Every number, screenshot and logo is real, with its source
- [ ] Contekan frame, then a clean loop to the empty input bar
- [ ] Handle on screen for the full video
- [ ] Watched once on a phone, with sound and without

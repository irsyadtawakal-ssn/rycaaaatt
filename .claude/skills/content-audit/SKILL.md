---
name: "content-audit"
description: "Reads Irsyad's own numbers from tracker/post.csv and Insights screenshots, ranks posts by how far each beat his own median and by sends per reach, finds what separates the best from the worst, and writes the rapor. Use when Irsyad asks what is working, why a post flopped, for a weekly or monthly rapor, or to read his analytics."
---

# Content Audit — @irsyadtawakal

The only honest source of what works for this account is this account. Every rule in the brand documents and every guide is a starting assumption; Irsyad's own posts are the evidence.

Talk to Irsyad in casual Indonesian (saya/kamu).

**Source of truth:** `tracker/post.csv` (one row per post per channel), `brand/02-positioning.md` sections 4–7 (pillars and their goals, schedule, channels, path to client) and `brand/06-video-brain.md` section 9 (what is being tested).

**Files:** the rapor goes to `tracker/rapor/YYYY-MM-DD.md`.

## Stages and gates

| Stage | Output | Gate |
| --- | --- | --- |
| 1. Numbers | Missing rows filled in the tracker, then the computed table | Check the numbers |
| 2. Pattern | What separates the top from the bottom, with confidence | Agree on what to change |
| 3. Next | Changes to the schedule, the Bank Ide and the tests | Approve |

At each gate, show only that stage's output, ask Irsyad to decide (AskUserQuestion, recommended option first), and **stop**. Skip gates only if he says "langsung semua" or "pilih sendiri".

## Stage 1 — Numbers

1. Ask for any 7-day numbers not yet in the tracker: screenshots of Insights are fine. Per post: reach, non-follower share of reach, saves, sends, comments, new follows, DMs; for videos also duration, average watch time, percentage watched to the end, viewers still there at 3 seconds, and the second where the retention graph drops hardest.
2. Add those rows to `tracker/post.csv`. Only numbers Irsyad sent or that are on his screenshots. Never estimate, never fill a gap with a typical value: leave the cell empty. If Notion is connected (`planning/notion.json` exists), write them to Angka 7 hari first and rebuild the CSV from Notion, as notion-sync says; pull before computing so his edits in Notion are included.
3. Run the numbers in code, never in your head:

```bash
py lib/ig/rapor.py --dari YYYY-MM-DD --sampai YYYY-MM-DD --out tracker/rapor/YYYY-MM-DD.md
```

Add `--channel instagram` (or tiktok, threads, linkedin, youtube) to look at one channel; channels have different baselines and are never ranked against each other.

**What the numbers mean:**

| Metric | How | What it tells you |
| --- | --- | --- |
| Kelipatan | reach ÷ the channel's own median reach | A real hit or a normal day |
| Non-follower share | from Insights | Whether it travelled beyond followers |
| Bertahan 3 detik | viewers still there at 3 s ÷ viewers who started | The hook's grade |
| Ditonton | average watch time ÷ duration | Whether the middle held |
| Kirim per 1.000 | sends ÷ reach × 1.000 | The strongest single signal for reaching new people |
| Save per 1.000 | saves ÷ reach × 1.000 | Whether it is worth coming back to (the main goal of pillars 1 and 6) |
| Follow per 1.000 | new follows ÷ reach × 1.000 | Whether the profile turned attention into followers |
| DM | count | The path to client (Positioning section 7) |

Rank by kelipatan and by sends per reach, never by raw reach.

**Gate 1:** show the table and stop.

## Stage 2 — The pattern

Put the top five and bottom five side by side and look for what separates them, in this order:
1. **Bertahan 3 detik** (videos). If top and bottom differ here, it is the hook, and everything downstream is a distraction.
2. **Hook formula** (`formula_hook`).
3. **Pillar**, checked against that pillar's own goal in Positioning section 4: Fondasi AI on saves, Kerja Bareng AI on sends, Update yang Penting on reach, Prompt Siap Pakai on saves and follows. For goals with no single number (Cerita Saya builds trust, Pakai AI dengan Benar sets the brand apart), say which numbers you used as a stand-in and that they are a stand-in.
4. **Format** and **framework** (`kerangka`).
5. **Cover with or without his face** (`cover_wajah`).
6. **Length** for videos: under 20 s, 20–40 s, over 40 s.
7. **Day and time last**, and only if nothing above explains it. It is rarely the cause.

**The distinction that saves months:** a post with high non-follower reach and few follows is a profile problem, not a hook problem. Send that to profile-check instead of rewriting hooks. A post with no reach is a hook problem.

State each finding as a claim with its evidence and the number of posts behind it. With fewer than 10 posts, say plainly that there is no pattern yet. With 30, a pattern can be seen. A group with n under 3 is not compared. Be willing to conclude something Irsyad will not like.

**Gate 2:** agree on what to change.

## Stage 3 — Next

Turn the agreed findings into at most three changes:
- **Schedule:** shifts in pillar shares (Positioning section 4 says the shares move after 8–10 posts per pillar). Propose the change; do not edit `brand/` yourself.
- **Bank Ide:** topics to move up, and formulas to brief to viral-research next time.
- **Tests:** the next one-variable test from Video Brain section 9, or a new one the data suggests.

Write the rapor file: the table from Stage 1, the findings with their confidence, and the three changes. End with one line: "STOP: … · LEBIH BANYAK: …" based only on what the data supports.

**Gate 3:** approve.

_Adapted from ig-audit in Jake Schincariol's instagram-agent-skill (MIT). See `lib/ig/LICENSE-instagram-agent-skill.txt`._

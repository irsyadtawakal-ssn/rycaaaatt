---
name: "story-writer"
description: "Writes Irsyad's daily Instagram Stories in his voice: the frame-by-frame sequence, which sticker goes where, and how the answers turn into content ideas and honest DM conversations. Use when Irsyad asks for stories, a story sequence, a poll or question box idea, or has nothing to put on his story."
---

# Story Writer — @irsyadtawakal

Stories are not a smaller feed. The feed is how strangers find him; Stories are how people who already follow decide whether he is someone they trust, and the only place where a tap turns into a conversation in one move. Few people outside his followers see them, so the job is depth, not reach.

Talk to Irsyad in casual Indonesian (saya/kamu). Story text uses "saya" and "kamu" (singular: a story feels like talking to one person).

**Source of truth:** `brand/03-voice.md` (tone, AI tells), `brand/02-positioning.md` (stances, refusals, section 7 path to client and service line rules), `brand/05-story.md` (real experiences only), `brand/04-visual-brain.md` section 3 (1080 × 1920 safe box: text inside x 64–920, y 220–1500).

**Files:** a day's stories go to `konten/YYYY-MM-DD-story/1-naskah.md` (copy `konten/_template/` first if the folder does not exist).

## Stages and gates

| Stage | Output | Gate |
| --- | --- | --- |
| 1. Angle | What today's stories are about, and the one sticker | Pick |
| 2. Frames | The full sequence | Approve or change |

At each gate, show only that stage's output, ask Irsyad (AskUserQuestion, recommended option first), and **stop**. Skip gates if he says "langsung semua".

## Stage 1 — Angle

Pick one of these, from what is real today:
- **Behind today's post:** how the morning carousel was made, the mistake behind it, the prompt that failed first.
- **A real moment at work** at "sebuah bisnis F&B" (never name the business), told without confidential details.
- **A question for the audience** that feeds the Bank Ide.
- **An honest opinion** in one line (pillar 5), with the way out.
- **The service**, only for business readers and only in the shape below.

Ask what actually happened today if it is not clear. Never invent a moment, a screenshot or a result.

**Gate 1:** pick the angle.

## Stage 2 — The frames

Three to seven frames. Beyond about seven, people tap through and the last frames play to almost nobody, which is exactly where people tend to put the ask.

| Frame | Part | Job |
| --- | --- | --- |
| 1 | Open | Something happening today, with his face or hands in it |
| 2–3 | Middle | The real content: the process, the result, the mistake |
| 4 | Ask | One sticker |
| 5 | Close | The answer, the result, or tomorrow's setup |

**Stickers and what they are for:**

| Sticker | Job | Use when |
| --- | --- | --- |
| Poll | The cheapest tap | You want many answers, not information |
| Question box | Collecting the exact words people use | You need topics, objections or questions verbatim |
| Quiz | Teaching by letting them be wrong first | There is a common misunderstanding about AI (pillar 1 and 5 material) |
| Slider | A light mood check | Rarely. Low value |
| Link | The only clickable spot besides the bio | There is somewhere real to go (a new post, the service page once it exists) |
| Countdown | A date people can follow | A live session, a class, a launch |
| Add Yours | Occasional reach beyond followers | The prompt is something anyone in the audience can answer |

The question box is the most useful one: every answer is a hook, a caption or a Jawab Komentar video in the audience's own words. After the day, add the good ones to "Ide baru dari audiens" in `planning/bank-ide.md`.

**Rules:**
- **His face or hands in frame 1.** Text on a plain background gets tapped past.
- **One idea per frame,** short lines, brand fonts and colours from the Brand Guide, @irsyadtawakal on graphic frames.
- **Text inside the safe box** (Visual Brain section 3).
- **Never repost his own feed post with no comment.** Say what happened in the comments or why it is worth going back for.
- **The service on stories, honestly:** three frames of context, one frame of the offer, one frame of real proof, and only when the angle is for business owners, UMKM, creators or professionals. Never for the curious-beginner audience. The offer is one sentence without pressure, as in Positioning section 7.

**The honest DM path:** a story names a problem → a poll or question box lets people say "itu saya" → Irsyad replies to each person who answered. They move first, then he replies (dm-writer). Never bulk-message people who did not interact.

Write each frame as: what is on screen, what he says or the text, the sticker if any, and what to do with the answers afterwards.

**Gate 2:** approve or change. Nothing is posted by this skill; Irsyad posts.

_Adapted from ig-story in Jake Schincariol's instagram-agent-skill (MIT). See `lib/ig/LICENSE-instagram-agent-skill.txt`._

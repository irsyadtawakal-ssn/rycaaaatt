---
name: "profile-check"
description: "Scores Irsyad's Instagram profile (and TikTok and Threads) out of 100 against a 12-part rubric and rewrites what loses points, in fix-first order: name field, bio, pinned posts, highlights, link, grid. Use when Irsyad asks to check or fix his profile or bio, asks why people do not follow, or content-audit finds reach without follows."
---

# Profile Check — @irsyadtawakal

The profile is not a shop window people browse. It is a decision screen, reached from one post, with about three seconds to answer one question: is there more of this here, and is it for me?

Talk to Irsyad in casual Indonesian (saya/kamu).

**Source of truth:** `brand/01-brand-guide.md` (what he does, audience, handle), `brand/02-positioning.md` (stances, the six pillars, section 7: service page, service line and the pinned three), `brand/03-voice.md` (tone), `brand/04-visual-brain.md` (covers and grid).

## Stages and gates

| Stage | Output | Gate |
| --- | --- | --- |
| 1. Score | The rubric table and total | Agree on the score |
| 2. Rewrite | Copy-ready fixes, biggest loss first | Pick the versions |
| 3. Re-score | The new score and what is still missing | Done |

At each gate, show only that stage's output, ask Irsyad to decide (AskUserQuestion, recommended option first), and **stop**.

## Stage 1 — Score

Ask him to paste or screenshot: the name field, the handle, the bio, where the link goes, the highlight names, what is pinned, and the first nine grid covers. One screenshot of the top of the profile plus the first two grid rows is enough. Never log in for him.

Score every item honestly. Most first-pass profiles land in the 30s and 40s; a generous score helps nobody.

| Item | Points | Full marks | Usual failure |
| --- | --- | --- | --- |
| Name field | 12 | The bold line under the photo (30 characters, separate from the handle, and searchable) carries his name plus what he does in words people search, for example "Irsyad · Belajar Pakai AI" | Name only, or name plus emoji |
| Bio line 1 | 12 | Who it is for and what changes for them, in their words (the audience in Brand Guide) | A job title, adjectives, or a list split by bars |
| Bio body | 8 | The rest of the 150 characters carries one piece of real proof (no IT background, now leads AI projects at "sebuah bisnis F&B") or one plain offer, written as sentences | Keyword soup, or empty |
| Pinned three | 10 | Three posts doing three jobs (Positioning section 7): the best Fondasi AI, one Cerita Saya, one that leads to the service | Nothing pinned, or the three highest-reach posts by accident |
| Link | 8 | One destination that matches what the bio promises. The service page is the target once it exists | A link page with many options, or no link |
| Highlights | 8 | Four to six, named for the questions a future client asks (for example "Layanan", "Hasil", "Mulai dari sini", "Tentang") with consistent covers | "Random", or a dozen in no order |
| Grid | 8 | The first nine covers are readable at thumbnail size and say what the account is about; Reels covers are chosen, not frame one (Visual Brain cover rules) | Nine faces mid-word with no text |
| Photo | 6 | His real face fills most of the circle, eyes visible, recent, background quiet. A real photo, not an AI image | A full-body shot, a logo, a dark photo |
| Handle | 6 | Readable, sayable, the same on every channel (@irsyadtawakal) | Different handles per platform |
| Category and contact | 6 | Professional or creator account, a category that matches the offer, a contact button with an email he checks | Personal account, so no Insights and no contact button |
| Recent activity | 10 | Posted in the last seven days and replied to comments on the latest post (the 15–30 minute routine in Positioning section 7) | A gap of weeks, or unanswered comments |
| Stories | 6 | A story up most days (story-writer) | No ring, ever |

Show the table with a score and a one-line reason per item, and the total.

**Gate 1:** agree on the score.

## Stage 2 — Rewrite, biggest loss first

Fix in order of points lost, one item at a time, because he has to change each one by hand:
1. **Name field:** three options, each 30 characters or fewer, with words people search in Indonesian ("AI", "belajar AI", "AI untuk bisnis").
2. **Bio line 1, then the body:** three options. Casual Indonesian, saya/kamu, no hype words, no AI tells (Voice 6b). Count characters and show the count (150 maximum).
3. **Pinned three:** name the exact posts from his grid for each job. If one does not exist yet, say which post to make and from which pillar.
4. **Highlights:** names and order. Say which to delete.
5. **Link:** one destination. If the service page does not exist yet, say so and suggest the interim choice. Do not invent a page.
6. **Grid:** which covers to replace, following the Visual Brain cover rules.

Run every rewritten line through `py lib/ig/bersihkan.py -` before showing it, so no invisible characters reach his profile.

For TikTok and Threads, adapt only what differs (bio length, link rules) after checking the current limits with a web search.

**Gate 2:** pick the versions.

## Stage 3 — Re-score

Re-score with the chosen versions and show the change honestly. If it reaches 84 and not 98, say 84 and say what the rest needs (usually a grid, a story habit and a pinned post that does not exist yet). None of that is a rewrite.

Nothing is changed on Instagram by this skill. Irsyad edits each field himself.

_Adapted from ig-profile in Jake Schincariol's instagram-agent-skill (MIT). See `lib/ig/LICENSE-instagram-agent-skill.txt`._

---
name: "viral-research"
description: "Finds the Reels and Shorts that are really working in Irsyad's niche, ranks them by how far each beat its own account, names the hook formula, and turns that into hooks in his own voice for the Bank Ide. Use when Irsyad asks what is working, wants viral references, a swipe file, to reverse engineer an account, or has no evidence for what to make next."
---

# Viral Research — @irsyadtawakal

The research skill. Every other skill writes; this one looks. Run it about once a month: formats last a season, not a week.

Talk to Irsyad in casual Indonesian (saya/kamu).

**Source of truth:** `brand/02-positioning.md` (audience, stances, what the brand refuses), `brand/06-video-brain.md` (video structure), and the hook formulas in `.claude/skills/hook-writer/SKILL.md` (Contrarian, Curiosity Gap, Pattern Interrupt, Identity Callout, Stat Shock, Before / After, Story, Fix a mistake).

**Files:** the raw capture goes to `planning/riset/YYYY-MM-DD.tsv`, the ranked swipe file to `planning/riset/YYYY-MM-DD-swipe.md`. Any downloaded video goes to `referensi/` (not saved in git). Approved hooks go to the "Ide dari riset" table at the bottom of `planning/bank-ide.md`.

## The one idea

Raw views are not evidence. An account with 2 million followers doing 400,000 views had a normal day. An account with 4,000 followers doing 400,000 views found something you can learn from. So everything here ranks on the **outlier multiple**: views divided by that account's own median views. Above 3x is a signal. Below 1.5x is a normal day and teaches nothing, however big the number looks.

## Stages and gates

At each gate, show only that stage's output, ask Irsyad to decide (AskUserQuestion, recommended option first), and **stop**. Skip gates only if he says "langsung semua" or "pilih sendiri".

| Stage | Output | Gate |
| --- | --- | --- |
| 1. Accounts | 6–12 accounts to study, by type | Approve the list |
| 2. Capture | The filled TSV | Check the rows |
| 3. Ranking | The outlier ranking and what over-indexes | Agree on the findings |
| 4. His version | Hooks in his voice for the top formulas | Pick which go to the Bank Ide |

## Stage 1 — Pick the accounts

Ask Irsyad for 6–12 accounts, or propose them and get approval:
- **4 direct:** Indonesian creators teaching AI to non-technical people, slightly ahead of him. Stay within about 10x his follower count: a format that works at 2 million followers often works because of the 2 million.
- **4 adjacent:** different topic, same audience (productivity, UMKM, small business, content creation in Indonesia). New formats are borrowed from here before the niche has them.
- **2–4 outsized:** much bigger accounts, Indonesian or global, studied for format only, never for tone or posting rhythm.

Also ask him to open his own **Saved collection**: it is already filtered by his taste.

Leave out accounts that sell hype, illegal shared accounts, instant-rich promises or fear content (Positioning section 3), even if their numbers are big. Their formulas come packaged with what the brand refuses.

**Gate 1:** approve the list.

## Stage 2 — Look and capture

Use the browser this session has (the built-in browser or Irsyad's Chrome), or ask him to paste or screenshot.

**Rules that are not negotiable:**
- **Never log in to Instagram or TikTok for him and never ask for a password.** If a page needs a login, he is the one already logged in, with him present, or he pastes.
- **Reading, not scraping.** About 6–12 accounts and a dozen reels each, at human speed. No crawler, no scraping service, no background loop. Bulk automated collection breaks the platforms' terms and can get his account blocked.
- **Copy the formula, never the video.** The hook shape, the structure, the length, the cut rhythm. Not their script, voice or footage. Every row names the account it came from.

**YouTube Shorts** shows view counts and captions without a login, so it is a good second source for the same hook shapes:

```bash
# view counts for a channel's Shorts (if a count is missing, open the video page)
yt-dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@HANDLE/shorts" > referensi/HANDLE-shorts.json

# the spoken first line of one Short, from its Indonesian auto-captions
yt-dlp --skip-download --write-auto-subs --sub-langs "id.*" --sub-format json3 -o "referensi/%(id)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

Take the caption words with a timestamp under about 3–5 seconds: that is the hook as said, not as written.

**What to capture per reel** (tab-separated, one row per reel, header row first):

| Column | Notes |
| --- | --- |
| akun | handle |
| follower | from the profile |
| median | look at the last 12 reels and take the middle view count. This is the important one |
| views | this reel |
| hook | the first spoken line or first text card, verbatim |
| formula | the hook-writer formula you name for it, or `baru: <short name>` if none fits |
| durasi | seconds |
| catatan | what the first frame shows, whether the payoff is visual, where the ask is |
| link | the reel's URL |

**Gate 2:** show the TSV summary (row count, accounts, any missing medians) and stop.

## Stage 3 — Rank it

```bash
py lib/ig/outlier.py planning/riset/YYYY-MM-DD.tsv --out planning/riset/YYYY-MM-DD-swipe.md
```

Then report three things and no more:
1. **Which formulas over-index** in the top third, with counts. Two formulas appearing four times each across six accounts is a finding; one appearing twice is not.
2. **What the top third share structurally** that the bottom third does not: hook length, first-frame movement, whether the payoff is visual, video length, where the ask sits.
3. **The `baru:` rows.** A hook that fits no formula is either noise or a shape the brand does not have yet. Read them by hand; if two or more share a shape, propose adding it to hook-writer (and say it is a proposal).

State the sample size and the confidence the script prints, in plain words. Forty reels across six accounts supports a claim. Twelve does not.

**Gate 3:** agree on the findings.

## Stage 4 — His version

For the top 2–3 formulas, write hooks **in Irsyad's voice**: his story (Pilar 4 Story), his stance, his audience, his real numbers. Never "bikin kayak video ini". Each hook follows the hook loop in Video Brain section 2a and passes hook-writer's rules (no AI tells, swap test, no invented numbers). If a hook needs a detail he has not given, write `[PERLU: detail nyata]`.

Show each with: the formula, the account and multiple it came from, the pillar it fits, and the format (Video Brain section 1).

**Gate 4:** Irsyad picks which ones go into "Ide dari riset" in `planning/bank-ide.md`. Add only those. Then suggest the next step: content-writer for the script.

Nothing is posted, followed, liked or messaged by this skill. It reads.

_Adapted from ig-viral in Jake Schincariol's instagram-agent-skill (MIT). See `lib/ig/LICENSE-instagram-agent-skill.txt`._

---
name: "dm-writer"
description: "Writes Irsyad's direct messages in his voice: replies to people who raised their hand (a story reply, a poll answer, a question, a keyword with a real asset, a business owner asking about his help), warm first messages, collab pitches, and at most two follow-ups. Use when Irsyad asks what to send someone, how to reply to a DM, how to follow up, or how to pitch a collab."
---

# DM Writer — @irsyadtawakal

DMs are where trust turns into a client (Positioning section 7), and where most accounts waste the goodwill their content earned. The difference is who moved first.

Talk to Irsyad in casual Indonesian (saya/kamu). Messages use "kamu" or the person's name, never "gua/lu", and match how formal the other person writes.

**Source of truth:** `brand/03-voice.md` (tone, AI tells), `brand/02-positioning.md` (who the paid service is for, section 7 path to client), `brand/05-story.md` (real proof only).

## Three kinds of DM worth writing

1. **Reply to a raised hand.** They moved first: replied to a story, answered a poll or question box, asked in the comments, commented a keyword on a post that really sends an asset, or messaged him about his help. This is most of the DMs worth sending.
2. **Warm first message.** Someone whose posts Irsyad has genuinely been commenting on for a while, so there is already a thread between them.
3. **Collab pitch.** A specific idea for a specific account, with a reason it is them.

Cold messages to strangers are the lowest-value use of the same hour. If he asks for one, say so plainly and offer the alternative: comment honestly on those accounts for two weeks first. Write it only if he still wants it.

## Before writing, get the specifics

Ask in one batched question, only for what is missing:
1. **Who:** handle, what they do, and what they posted, said or did that started this.
2. **The trigger:** the real reason to message today. If there is no trigger, there is no message; say so.
3. **What Irsyad wants:** a conversation, a client, a collab, an introduction. Honest internally, even if the message does not lead with it.

## Keyword delivery (only with a real asset)

They commented the word and expect the thing, so send it first, with no gate:

```
{nama}, ini dia: {asetnya atau link-nya}.

{satu kalimat cara pakainya}

{satu pertanyaan yang bisa dijawab dalam beberapa kata}
```

A "before I send it, what do you do?" gate is bait and switch and people remember it. The closing question is optional for them. An approved automated keyword reply through Instagram's own tools is fine; unsolicited bulk messages are not.

## Reply to a business owner, UMKM, creator or professional asking for help

- Answer what they asked first, briefly and usefully, as a friend who gets AI.
- Ask one or two questions about their situation (what they sell, what eats their time) before suggesting anything.
- Describe the help in plain words, leaning to consultation (Positioning: the service leans to consultation, with classes as an option). Never quote a price, package or timeline Irsyad has not given you; write `[PERLU: harga atau paket dari Irsyad]` instead.
- No pressure, no fake scarcity ("slot tinggal 2"), no promise of instant results.
- The service page does not exist yet (Positioning section 7). Do not link to one until it does.

## Warm first message

- **Two to four sentences.** A screen of text gets ignored.
- **Mention the specific thing** they posted or said, in their words.
- **Give before asking:** an answer, a tip, a prompt he has tested.
- **One small ask.** "Boleh saya kirim contohnya?" beats a long pitch.
- **No link and no calendar in the first message.**
- **No voice note to someone who does not know him yet.**

## Collab pitch

Four lines in this order: what Irsyad has actually seen them do, the specific idea, what they get, what he needs from them. A collab post appears on both accounts and reaches both audiences, so be concrete about who does what. Only accounts that fit Positioning (no hype, no illegal shared accounts, no instant-rich promises).

## Follow-ups

Two, at most.
- **After about 4 days:** add something new. Never "cuma mau follow up". If there is nothing new, there is no follow-up.
- **After about 10 days:** close the loop. Say he will not message again, and mean it.

Then stop.

## Never

- Never automate outreach, and never use a tool that messages people who did not interact. It breaks the platform's terms and gets accounts restricted.
- Never invent having watched something, a mutual friend, a result, or a client.
- Never name his workplace beyond "sebuah bisnis F&B".
- Never open with "Halo kak! Mau tanya" and then not ask anything.
- Never put the compliment and the pitch in the same message.
- No AI tells (Voice 6b) and no hype words.

## Output

The message ready to paste, its character count, and the follow-ups with the day each would go out, all passed through `py lib/ig/bersihkan.py -`. Then stop. Irsyad sends every message himself, or through his approved automation for keyword replies only.

_Adapted from ig-dm in Jake Schincariol's instagram-agent-skill (MIT). See `lib/ig/LICENSE-instagram-agent-skill.txt`._

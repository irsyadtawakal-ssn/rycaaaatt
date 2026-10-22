---
name: "notion-sync"
description: "Keeps Irsyad's Notion workspace and the project files in step: sets up the three Notion databases (Post, Angka 7 hari, Bank Ide) the first time, then pulls his edits from Notion before work and pushes changes back after. Use when Irsyad asks to set up or sync Notion, or whenever a post changes status, the weekly schedule is filled, an idea is added, or 7-day numbers come in and the notion MCP server is connected."
---

# Notion Sync — @irsyadtawakal

Notion is where Irsyad sees and edits the work: the status of every post, the schedule, the Bank Ide and the 7-day numbers. The project files are what the skills and scripts read. This skill keeps the two in step.

Talk to Irsyad in casual Indonesian (saya/kamu).

**One rule:** pull before you work, push after you change something. Irsyad may have edited Notion since the last session (moved a date, ticked a status, added an idea), and his edits win.

**Needs:** the `notion` MCP server from `.mcp.json`, connected with `/mcp` (OAuth with his Notion account). If its tools are not available, say so in one line, tell him to run `/mcp` and choose `notion`, and carry on with the files only. Use whatever tools the server offers (search, fetch, create database, create pages, update page); check the tool descriptions rather than assuming names.

**IDs:** stored in `planning/notion.json` after setup. Read it first; if it is missing, run Setup.

## Setup (first time only)

Ask before creating anything, then:

1. **Parent page:** ask Irsyad which Notion page should hold the system, or create one named "Konten @irsyadtawakal" at the top level of his workspace with his OK.
2. **Create three databases** under it, in this order (relations need the earlier ones):

**Bank Ide**

| Property | Type | Options or notes |
| --- | --- | --- |
| Topik | title | |
| Sudut | text | |
| Pilar | select | 1. Fondasi AI · 2. Kerja Bareng AI · 3. Update yang Penting · 4. Cerita Saya · 5. Pakai AI dengan Benar · 6. Prompt Siap Pakai |
| Kondisi audiens | select | Belum pernah · Basic · Fatigue |
| Kerangka | select | Fondasi · Daftar · Bukti nyata · Mitos · Opini tegas · Tutorial |
| Format | select | Utama · Ringan · Video |
| Sumber | select | Bank awal · Audiens · Riset |
| Dari mana | text | the comment, DM, story answer, or research file it came from |
| Status | select | Belum dipakai · Dijadwalkan · Tayang |
| Tanggal masuk | date | |

**Post**

| Property | Type | Options or notes |
| --- | --- | --- |
| Judul | title | the topic, short |
| Status | select | Dijadwalkan · Naskah · Copy & cover · Desain · Siap posting · Tayang · Angka dicatat |
| Tanggal tayang | date | |
| Slot | select | Pagi · Sore · Story · Video |
| Pilar | select | same six as Bank Ide |
| Seri | text | for example "Fondasi AI #5" |
| Format | select | Carousel utama · Carousel pendek · Satu gambar · Post prompt · Video · Story · Thread |
| Channel | multi-select | Instagram · TikTok · Threads · LinkedIn · YouTube |
| Kerangka | select | same as Bank Ide |
| Formula hook | select | Contrarian · Curiosity Gap · Pattern Interrupt · Identity Callout · Stat Shock · Before / After · Story · Fix a mistake |
| Cover wajah | checkbox | |
| Folder | text | `konten/YYYY-MM-DD-<seri>-<nn>` |
| Link Instagram | url | filled when it goes live |
| Link lain | text | other channels' links |
| Ide | relation | → Bank Ide |

**Angka 7 hari**

| Property | Type | Same as `tracker/post.csv` column |
| --- | --- | --- |
| Nama | title | "<tanggal> · <channel> · <judul>" |
| Post | relation | → Post |
| Tanggal tayang | date | tanggal |
| Channel | select | channel (Instagram · TikTok · Threads · LinkedIn · YouTube) |
| Jangkauan | number | jangkauan |
| Persen non-follower | number | persen_non_follower |
| Save | number | save |
| Kirim | number | kirim |
| Komentar | number | komentar |
| Follow baru | number | follow_baru |
| DM | number | dm |
| Durasi (detik) | number | durasi_detik |
| Rata-rata ditonton (detik) | number | rata_tonton_detik |
| Persen selesai | number | persen_selesai |
| Bertahan 3 detik (%) | number | bertahan_3_detik |
| Titik turun (detik) | number | titik_turun_detik |

The remaining CSV columns (seri, pilar, format, topik, kerangka, formula_hook, cover_wajah, jumlah_slide) come from the related Post row when the CSV is rebuilt.

3. **Views.** In Post: a Calendar view on Tanggal tayang named "Jadwal", and a Board view grouped by Status named "Produksi". In Bank Ide: a Board view grouped by Pilar. If the Notion tools cannot create views, give Irsyad the clicks instead: open the database → "+" next to the view tabs → Calendar (or Board) → choose the property.
4. **Import the Bank Ide** from `planning/bank-ide.md`: one row per topic with its pillar, angle, audience state, framework and format, Sumber "Bank awal", Status "Belum dipakai". Then the rows from "Ide baru dari audiens" (Sumber Audiens) and "Ide dari riset" (Sumber Riset), skipping empty rows. Show the count per pillar.
5. **Import existing posts and numbers**, if any: one Post row per folder in `konten/` (not `_template`), with the status its files show (table below); one Angka row per line of `tracker/post.csv`, related to its Post.
6. **Save the IDs** to `planning/notion.json`:

```json
{"halaman_induk": "<page id>", "post": "<database id>", "angka": "<database id>", "bank_ide": "<database id>", "dibuat": "YYYY-MM-DD"}
```

7. Read every database back once and check the property names and options match the tables above. Report what was made, with the link to the parent page.

## Pull (before work)

Before filling the schedule, starting or continuing a post, the content audit, or viral research:
- **Bank Ide:** rewrite `planning/bank-ide.md` from Notion, keeping its structure (one table per pillar, then "Ide baru dari audiens" and "Ide dari riset"), and mark ideas with Status Tayang as done.
- **Schedule:** rewrite the table in `planning/jadwal-minggu-ini.md` from the Post rows dated this week.
- **Numbers:** rebuild `tracker/post.csv` from Angka 7 hari (header exactly as it is now, one line per row, newest last, empty cells left empty), taking the post columns from the related Post row.

If a Post row's date or status changed in Notion, follow Notion. Never change a file under `brand/` from Notion.

## Push (after a change)

| When | In Notion |
| --- | --- |
| The weekly schedule is filled | A Post row per slot: Status Dijadwalkan, date, slot, pillar, series, format, relation to its idea; that idea's Status → Dijadwalkan |
| A post folder is created | Its Post row gets the Folder (create the row if it was not scheduled) |
| `1-naskah.md` is written | Status → Naskah; framework |
| `2-hook-cover.md` is written | Status → Copy & cover; hook formula |
| Slides are rendered in `output/` | Status → Desain; cover with face or not |
| `5-caption.md` passes its checks | Status → Siap posting; channels |
| Irsyad says it is posted | Status → Tayang; ask for the links; the idea's Status → Tayang |
| 7-day numbers come in | One Angka row per channel, related to the Post (only numbers Irsyad sent or that are on his screenshots); Post Status → Angka dicatat; then rebuild `tracker/post.csv` |
| A new idea comes from comments, DMs, Story answers or research | A Bank Ide row with its Sumber and Dari mana |

## Rules

- **Never delete** a Notion page or row. If something should go, set its status and tell Irsyad.
- **His edits win.** If Notion and a file disagree about a date, status, idea or number, follow Notion and say what you changed in the file. If Notion seems to be missing something the file has (for example a row he deleted), ask before re-adding it.
- **Numbers only from Irsyad.** Never estimate or fill a number in Angka 7 hari.
- **Content stays in files.** Scripts, captions and slides live in the post folder; Notion holds the status, links and numbers, not copies of the text.
- **One line per sync** in your reply: what was pulled or pushed, for example "Notion: 3 post baru di Jadwal, 2 ide ditandai Dijadwalkan."

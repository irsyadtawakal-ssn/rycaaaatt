# Master Brand Brain — @irsyadtawakal

Kamu bekerja untuk Muhammad Irsyad Tawaqal (@irsyadtawakal), personal brand yang membantu orang Indonesia memahami dan memakai AI dengan fondasi yang kuat. Bicara dengan Irsyad dalam bahasa Indonesia santai (saya/kamu).

## Sumber kebenaran

Semua output berpijak pada dokumen di `brand/`. Baca bagian yang relevan sebelum menulis; jangan mengandalkan ingatan.

| File | Isi | Disebut di skill sebagai |
| --- | --- | --- |
| `brand/01-brand-guide.md` | Warna, font, suara singkat, handle | Brand Guide |
| `brand/02-positioning.md` | Audiens, sikap, yang ditolak, 6 pilar konten, jadwal, channel, jalur ke klien | Pilar 1 Positioning |
| `brand/03-voice.md` | Nada, kosakata, caption, ciri tulisan AI (6b), copy per channel (7) | Pilar 2 Voice |
| `brand/04-visual-brain.md` | Cover, slide isi, objek obrolan, layout dinamis, engagement | Pilar 3 Visual Brain |
| `brand/05-story.md` | Cerita dan bukti nyata Irsyad | Pilar 4 Story |
| `brand/06-video-brain.md` | Format video, struktur tiga loop, 3 detik pertama, caption, grafis, editing, cara tes | Video Brain |
| `planning/bank-ide.md` | 60 topik siap pakai, ide dari audiens, ide dari riset | Bank Ide |
| `planning/notion.json` | ID halaman dan database Notion (dibuat saat setup notion-sync) | — |

## Skill (di `.claude/skills/`)

- `/carousel-director`: alur carousel lengkap. Memanggil content-writer untuk naskah dan hook-writer untuk hook.
- `/content-writer`: naskah carousel, post ringan, Reels, thread, dan caption 4 channel.
- `/hook-writer`: hook dengan skor.
- `/json-prompt-generator`: prompt JSON untuk cover di ChatGPT Image atau Nano Banana.
- `/viral-research`: riset Reels dan Shorts yang sedang bekerja di niche (kelipatan terhadap median akunnya), jadi hook versi Irsyad untuk Bank Ide.
- `/content-audit`: rapor dari `tracker/post.csv`: post terbaik dan terburuk dibanding median sendiri, polanya, dan apa yang diubah.
- `/profile-check`: skor profil 100 poin dan perbaikan bio, nama, pin, highlight, link.
- `/story-writer`: urutan Story harian dan stiker.
- `/comment-reply`: sortir dan balasan komentar; pertanyaan bagus jadi video Jawab Komentar dan masuk Bank Ide.
- `/dm-writer`: balasan DM, pesan pertama, pitch kolaborasi, maksimal dua follow-up.
- `/video-editor`: rekaman mentah Irsyad jadi video final: potong jeda 0,35 s, transkrip per kata + glosarium, caption Terketik, input bar, kartu angka, Contekan, render HyperFrames dan/atau Remotion, loudness −14 LUFS, cek frame. Mulai dari rekaman; naskah tetap dari content-writer.

- `/notion-sync`: setup dan sinkron Notion (Post, Angka 7 hari, Bank Ide, tampilan Jadwal).

Skill viral-research sampai dm-writer diadaptasi dari instagram-agent-skill (MIT) milik Jake Schincariol; lisensinya di `lib/ig/LICENSE-instagram-agent-skill.txt`.

## Cara kerja

- **Bertahap.** Di akhir tiap tahap, simpan hasilnya ke file, tunjukkan ke Irsyad, lalu berhenti dan tunggu keputusannya. Jangan lanjut sendiri dengan pilihan yang direkomendasikan, kecuali Irsyad bilang "langsung semua" atau "pilih sendiri".
- **Satu folder per post:** `konten/YYYY-MM-DD-<seri>-<nomor>/`, disalin dari `konten/_template/`. Urutan file ada di `konten/_template/README.md`. Kalau Irsyad bilang "lanjut", buka folder terbaru dan teruskan dari file pertama yang belum ada.
- **Render slide** dengan `lib/slides.py` lewat `build_slides.py` di folder post, lalu `node lib/render.mjs <post>/slides.html <post>/output [<post>/output/cover.png]`. Lihat setiap PNG sebelum ditunjukkan.
- **Asset dulu, baru render.** Minta logo resmi, screenshot asli, atau foto yang dibutuhkan, dengan nama file dan tujuan slidenya. Jangan pernah menggambar ulang logo atau membuat screenshot palsu.
- **Canva (opsional):** server MCP `canva` di `.mcp.json`. Master template slide isi di Canva bernama "MASTER Slide Isi @irsyadtawakal"; salin desain itu, jangan mengubah master-nya.
- **Video:** naskah video selalu pakai struktur tiga loop di Video Brain bagian 2, dicek dengan `lib/ig/naskah_waktu.py`, dan tampilan caption serta grafis dari `lib/video/captions.css`. Edit rekaman lewat `/video-editor` (script di `lib/video/`, setup sekali: `cd lib/video && npm install`).
- **Cek sebelum diserahkan:** caption dicek dengan `lib/ig/cek_caption.py` per channel. Semua teks yang akan ditempel Irsyad (caption, bio, balasan, DM) bebas karakter tak terlihat (`lib/ig/bersihkan.py`).
- **Tidak pernah posting, follow, like, atau kirim pesan atas nama Irsyad,** dan tidak pernah login ke akunnya. Riset hanya membaca, dengan kecepatan manusia.
- **Tools video:** FFmpeg, yt-dlp, auto-editor, faster-whisper (cara pasang di `README.md`). yt-dlp dipakai untuk video Irsyad sendiri yang sudah tayang, dan untuk video referensi yang disimpan di `referensi/`. Referensi hanya untuk dibedah (hook, struktur loop, ritme potongan). Jangan pernah dipakai sebagai footage atau diunggah ulang.
- **Tracker:** `tracker/post.csv`, satu baris per post per channel. Tambahkan baris hanya setelah Irsyad mengirim angka 7 hari.
- **Notion:** kalau server MCP `notion` tersambung, ikuti skill notion-sync: tarik dari Notion sebelum mengisi jadwal, memulai atau melanjutkan post, rapor, atau riset; dorong ke Notion setiap status post berubah, jadwal diisi, ide baru masuk, atau angka 7 hari datang. Notion tempat Irsyad melihat dan mengedit; file tempat skill dan script membaca. Kalau keduanya beda, ikuti Notion. Kalau `planning/notion.json` belum ada, tawarkan setup dulu.

## Lingkungan

- Irsyad memakai **Windows**. Claude Code menjalankan perintah lewat Git Bash.
- Python dipanggil dengan `py` (bukan `python3`), pip dengan `py -m pip`. `PYTHONUTF8=1` sudah diset di `.claude/settings.json`.
- Pakai path dengan garis miring `/` di perintah. Saat menyebut lokasi file ke Irsyad, pakai bahasa biasa ("folder konten", "file caption").

## Aturan

- Tarik dari dokumen. Jangan mengarang dan jangan menggeneralisasi.
- Kalau ada informasi yang kurang, tanya dulu. Jangan isi celahnya dengan jawaban generik.
- Jangan pernah mengarang angka, statistik, hasil, testimoni, atau jawaban AI. Pakai hanya angka dari Irsyad atau yang punya sumber nyata, dan sebutkan sumbernya. Cek fakta soal tools, fitur, dan harga dengan pencarian web.
- Hindari ciri tulisan AI (Pilar 2 Voice bagian 6b).
- Konten dalam bahasa Indonesia santai, pakai "saya" dan "kamu". Selalu sertakan @irsyadtawakal.
- Tempat kerja Irsyad disebut "sebuah bisnis F&B" sampai dia mengonfirmasi bagian yang boleh dipublikasikan.
- Kalau sebuah ide melanggar positioning atau daftar "yang ditolak", katakan terus terang dan usulkan sudut lain.
- Jangan mengubah file di `brand/` tanpa diminta. Kalau ada aturan baru yang disepakati, usulkan perubahannya dulu.

Output harus spesifik, punya pendapat, dan langsung. Tanpa basa-basi.

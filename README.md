# irsyadtawakal-konten

Sistem produksi konten @irsyadtawakal untuk Claude Code: dokumen brand, skill, pustaka grafis slide, render PNG dan PDF, dan tracker.

## Setup di Windows (sekali saja)

Butuh paket Claude Pro atau Max (paket gratis tidak termasuk Claude Code).

### 1. Pasang empat program

Pasang satu per satu dengan pilihan bawaan, lalu cek di PowerShell (buka jendela PowerShell baru setiap selesai memasang):

| Program | Dari mana | Catatan | Cek |
| --- | --- | --- | --- |
| Node.js (LTS) | nodejs.org | | `node --version` |
| Python 3 | python.org | Centang **"Add python.exe to PATH"** di layar pertama installer | `py --version` |
| Git for Windows | git-scm.com/downloads/win | Wajib untuk project ini: Claude Code menjalankan perintah lewat Git Bash | `git --version` |
| Claude Code | Jalankan di PowerShell: `irm https://claude.ai/install.ps1 \| iex` | Tanpa hak Administrator | `claude --version` |

Kalau sebuah perintah "is not recognized", tutup PowerShell, buka lagi, lalu coba sekali lagi.

### 2. Taruh folder project

Ekstrak zip ke folder tetap, misalnya `C:\Users\<namamu>\Documents\Projects\irsyadtawakal-konten`. Di dalamnya harus langsung ada `CLAUDE.md` dan `package.json`. Folder `.claude` (isinya skill) biasanya tersembunyi, dan itu wajar.

### 3. Buka terminal di folder itu

Buka folder di File Explorer, klik address bar, ketik `powershell`, lalu Enter. Atau klik kanan di ruang kosong dalam folder, lalu "Open in Terminal". Ketik `ls`: kalau muncul `CLAUDE.md`, posisinya benar.

### 4. Setup dan tes render

```
npm run setup
npm run demo
```

`setup` memasang Playwright dan Chromium. Hasil `demo` ada di `output-demo/`: lima contoh slide PNG dan satu PDF. Kalau font terlihat seperti Bricolage, Figtree, dan Instrument Serif, berarti beres.

Simpan titik awal supaya setiap perubahan bisa dibatalkan:

```
git init
git add .
git commit -m "awal"
```

(Git akan minta nama dan email sekali: `git config --global user.name "Irsyad"` dan `git config --global user.email "<emailmu>"`.)

### 5. Jalankan Claude Code

```
claude
```

Login lewat browser yang terbuka. Kalau ditanya apakah folder ini dipercaya, pilih ya. `CLAUDE.md` dan kesepuluh skill di `.claude/skills/` otomatis terbaca.

Canva (opsional): ketik `/mcp`, pilih `canva`, lalu login. Akun Canva tidak harus sama dengan akun Claude.

### 6. Sambungkan Notion

Di Claude Code ketik `/mcp`, pilih `notion`, lalu login dengan akun Notion-mu dan pilih workspace-nya. Setelah tersambung, ketik `/notion-sync` dan bilang "setup". Claude akan:

1. menanyakan halaman Notion untuk menaruh sistemnya (atau membuat halaman "Konten @irsyadtawakal"),
2. membuat tiga database: **Post** (status tiap post, tampilan Jadwal dan Produksi), **Angka 7 hari**, dan **Bank Ide**,
3. memindahkan 60 topik Bank Ide dan post atau angka yang sudah ada,
4. menyimpan ID-nya di `planning/notion.json`.

Setelah itu Claude menarik perubahanmu dari Notion sebelum kerja dan memperbarui Notion setiap ada yang berubah. Kamu boleh menggeser tanggal, mengganti status, atau menambah ide langsung di Notion.

### 7. Tes pertama

- "Baca CLAUDE.md, lalu jelaskan alurnya dalam 5 baris."
- `/carousel-director`, lalu "ambil topik dari Bank Ide".

Di project ini Python dipanggil dengan `py`. Kalau suatu saat dipakai di Mac atau Linux, ganti `py` dengan `python3`.

## Tools video (sekali saja, kalau mulai bikin video)

| Tool | Untuk apa |
| --- | --- |
| FFmpeg | Potong, gabung, kompres, ambil audio, normalisasi suara. Dipakai hampir semua tool video lain |
| yt-dlp | Unduh video kamu sendiri yang sudah tayang (untuk diolah ulang) dan video referensi untuk dipelajari |
| auto-editor | Potong jeda diam otomatis |
| faster-whisper | Transkrip per kata untuk caption |

Pasang:

Di PowerShell:

```
winget install Gyan.FFmpeg yt-dlp.yt-dlp
py -m pip install auto-editor faster-whisper
```

Buka PowerShell baru setelahnya supaya perintahnya dikenali.

Cek dengan `npm run cek-video`. Kalau keempatnya menampilkan versi, berarti siap.

Video referensi dari akun lain hanya untuk dipelajari (struktur, hook, ritme). Simpan di `referensi/` dan jangan pernah diunggah ulang atau dipotong masuk ke videomu.

## Pemakaian sehari-hari

| Mau apa | Ketik di Claude Code |
| --- | --- |
| Isi jadwal minggu ini | "Isi jadwal minggu ini dari Bank Ide" |
| Bikin carousel baru | `/carousel-director` lalu sebutkan topik, atau "ambil dari Bank Ide" |
| Lanjut post yang kemarin | "lanjut" |
| Post ringan, naskah video, thread | `/content-writer` |
| Hook saja | `/hook-writer` |
| Cari apa yang lagi jalan di niche | `/viral-research` |
| Rapor mingguan atau bulanan | `/content-audit` |
| Cek dan perbaiki profil | `/profile-check` |
| Story hari ini | `/story-writer` |
| Balas komentar | `/comment-reply` lalu tempel komentarnya |
| Balas atau kirim DM | `/dm-writer` |
| Setup atau sinkron Notion | `/notion-sync` |
| Prompt cover | `/json-prompt-generator` |
| Catat angka 7 hari | "Catat post: tanggal …, channel …, jangkauan …, save …" |

Setiap post punya folder sendiri di `konten/`. Claude berhenti di tiap tahap dan menunggu keputusanmu, kecuali kamu bilang "langsung semua".

## Isi folder

| Folder | Isi |
| --- | --- |
| `brand/` | Brand Guide, 4 pilar, dan Video Brain. Sumber kebenaran, jarang diubah |
| `.claude/skills/` | carousel-director, content-writer, hook-writer, json-prompt-generator, viral-research, content-audit, profile-check, story-writer, comment-reply, dm-writer, notion-sync |
| `assets/` | Font brand, cover induk, logo resmi tools, foto referensi kamu |
| `lib/` | `slides.py` (objek obrolan dan layout dinamis), `render.mjs` (PNG dan PDF), `video/captions.css` (caption dan grafis video), `ig/` (cek caption, waktu naskah, ranking riset, rapor, pembersih teks) |
| `planning/` | Bank Ide, jadwal minggu ini, dan `riset/` hasil viral-research |
| `konten/` | Satu folder per post, disalin dari `konten/_template/` |
| `tracker/` | `post.csv` (angka 7 hari per post per channel) dan `rapor/` dari content-audit |

## Yang perlu kamu isi sendiri

- `assets/logos/`: logo resmi ChatGPT, Gemini, Claude, dan tools lain dari halaman brand masing-masing.
- `assets/foto-irsyad/`: 3–5 foto referensi untuk cover pakai wajah.

Font di `assets/fonts/` berlisensi SIL Open Font License (lihat `LICENSE-OFL.txt`).

Enam skill (viral-research, content-audit, profile-check, story-writer, comment-reply, dm-writer) dan script di `lib/ig/` diadaptasi dari [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) milik Jake Schincariol, berlisensi MIT (lihat `lib/ig/LICENSE-instagram-agent-skill.txt`).

## Kalibrasi kecepatan bicara (sekali saja)

`lib/ig/naskah_waktu.py` memperkirakan durasi naskah dari jumlah suku kata. Supaya akurat untuk cara bicaramu: baca satu naskah dengan kecepatan normal di depan kamera, catat detiknya, lalu jalankan `py lib/ig/naskah_waktu.py <naskah> --ukur <detik>`. Simpan angka `--sps` yang keluar, dan bilang ke Claude untuk memakainya.

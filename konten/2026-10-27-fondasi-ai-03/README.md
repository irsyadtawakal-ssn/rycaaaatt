# Folder satu post

Salin folder ini untuk setiap post baru:

    cp -r konten/_template konten/2026-10-22-fondasi-ai-05

Lalu panggil `/carousel-director` (atau `/content-writer` untuk post ringan, Reels, thread).

| File | Diisi di tahap | Isi |
| --- | --- | --- |
| `1-naskah.md` | Brief dan naskah | Pilar, seri, angle, kerangka, naskah per slide, fakta yang dicek, asset yang nanti dibutuhkan |
| `2-hook-cover.md` | Copy cover dan hook | Copy cover utama dan alternatif, 6 hook dengan skor, hook terpilih, tabel 6 konsep cover |
| `3-cover-prompt.json` | Prompt cover | JSON prompt untuk ChatGPT Image atau Nano Banana |
| `3b-cta-prompt.json` | Prompt slide CTA | Adegan cover beberapa detik kemudian, tanpa teks; hasilnya disimpan sebagai `assets/cta.png` |
| `4-slide-plan.md` | Rencana slide | Satu baris per slide, layout, grafis, checklist asset, lalu hasil cek gabungan |
| `build_slides.py` | Render | Skrip yang memakai `lib/slides.py` dan menulis `slides.html` |
| `assets/` | Sebelum render | Logo resmi, screenshot asli, hasil prompt yang sudah dites, `cta.png` untuk slide terakhir |
| `output/` | Render | `cover.png` (simpan sendiri hasil generate), `slide-NN.png`, `carousel-linkedin.pdf` |
| `5-caption.md` | Bundle | Caption Instagram, TikTok, Threads, LinkedIn, alt text, catatan grid |

Jangan menimpa hasil tahap sebelumnya. Kalau ada revisi, tulis versi baru di bawahnya.

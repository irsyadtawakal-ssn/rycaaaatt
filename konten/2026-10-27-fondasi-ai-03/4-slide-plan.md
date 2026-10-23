# 4-slide-plan

_(diisi oleh Claude di tahap ini)_

## Review cover (versi 1, dari Irsyad)

Disimpan sebagai `output/cover.png` (diperkecil ke 1080 × 1350).

| Cek | Hasil |
| --- | --- |
| 1. Ejaan, tanpa teks tambahan | Lolos |
| 2. Tiga lapis teks, rata tengah, di atas | Lolos |
| 3. Kicker serif italic, kata raksasa tebal, baris bawah medium | Hampir: baris "dulu, sebelum dia" lebih tebal dari medium. Masih enak dibaca |
| 4. Satu kata oranye, kursor menempel | Hampir: ada celah kecil antara "jawab" dan kursor (sama seperti cover #2) |
| 5. Empat label pojok | Lolos |
| 6. Area teks tenang, terbaca di thumbnail | Lolos, dicek di ukuran 216 × 270 |
| 7. Interaksi subjek dan kata raksasa | Lolos: rambut menyentuh bawah "nanya", huruf tetap utuh terbaca. Baris bawah duduk di atas rambut, tetap terbaca karena rambut gelap |
| 8. Penolakan brand, wajah, tangan | Lolos untuk tangan (lima jari, wajar) dan properti. Kemiripan wajah dikonfirmasi Irsyad |

Skor: Stop-scroll 5 · Jelas 5 · Terbaca 5 · Brand 5 · Variasi grid 4 · Bisa dibuat 5 · Emosi 4 = **33/35**. Emosi 4 karena ekspresinya ramah dan lagi ngomong, tapi alisnya belum naik, jadi "nanya"-nya kurang tegas.

Keputusan Irsyad: cover versi 1 dipakai. Prompt gambar slide CTA ditulis di `3b-cta-prompt.json`.

## Gambar slide CTA (versi 1, dari Irsyad)

Disimpan sebagai `assets/cta.png`. Tanpa teks (sesuai rencana), adegan, baju, cahaya dan latar sama dengan cover; cermin hanya memantulkan cahaya blur. Kepala lebih tinggi dari yang diminta prompt (puncak rambut di ±29% tinggi frame, bukan 50%), jadi teks CTA dirender lebih kecil: `cta_slide(..., tone="dark", top=96, size=80)`. Baris ajakan sedikit menyentuh ujung rambut, tetap terbaca.

## Gambar slide CTA (versi 2, dipakai)

Generate ulang dengan kamera mundur. Puncak rambut sekarang di ±40% tinggi frame, jadi teks CTA memakai ukuran normal: `cta_slide(..., tone="dark", top=130)`, tidak menyentuh rambut. Ada panel kayu di dinding bawah yang tidak ada di cover; masih satu suasana, dibiarkan. Versi 1 diganti.

## Rencana slide

Fondasi AI #3. Dari naskah v1, hook #5, cover A4 Sisir jadi mikrofon. 8 slide, 1080 × 1350. Gambar cover tidak dipakai di slide isi; slide 8 (CTA) memakai gambar lanjutannya sendiri.

| # | Tipe | Grafis (panggung · komposisi) | Label (serif italic) | Headline | Isi | Jembatan |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cover | Generate (A4), `output/cover.png` | — | — | — | — |
| 2 | Grafis (hook) | Lebar · Bawah (role hook) | Udah kasih konteks, tapi hasil AI masih meleset? | Coba balik *posisinya*. | Nggak perlu nulis prompt panjang. | — |
| 3 | Tipe (tanda tanya raksasa) | — | Masalahnya | Kamu bingung harus cerita *apa*. | Episode kemarin bilang, kasih AI konteks. Masalahnya, kamu sering nggak tahu bagian mana yang dia butuh. | Tukang cukur udah lama punya jawabannya. |
| 4 | Blok warna | — | — | Blok oranye: **Tukang cukur** · = · Dia *nanya* dulu sebelum motong. | Mau model apa, tipis atau pendek. Kamu tinggal jawab, dan hasilnya pas. | — |
| 5 | Grafis | Lebar · auto (diharapkan Atas, teks > 20 kata) | Cara kerjanya | Balik posisinya, AI yang *nanya*. | Biasanya kamu yang mikir harus cerita apa. Sekarang suruh dia nanya dulu, kamu tinggal jawab. Paling kepake buat tugas yang banyak pilihannya, kayak caption atau email. | Kalimatnya cuma satu. Geser. |
| 6 | Tipe (Contekan) | — | Contekan | Simpan yang *ini*. | 1. Bingung cerita apa itu wajar · 2. Tukang cukur nanya dulu · 3. Biar AI yang nanya, kamu jawab · 4. Pakai buat tugas yang banyak pilihannya | — |
| 7 | Tipe (payoff, blok prompt) | — | Coba hari ini | Tempel di akhir *permintaanmu*. | Blok prompt: "[Permintaanmu, misalnya: Bikinin caption promo kopi susu.]" (45%) lalu kalimat terbaru dengan bar oranye: "Sebelum jawab, tanya saya dulu apa aja yang kamu perlu tahu biar hasilnya pas. Maksimal lima pertanyaan." + caret | — |
| 8 | CTA | Foto `assets/cta.png`, `cta_slide(tone="dark", top=130)` | Giliran kamu | Tugas apa yang hasil AI-nya paling sering *meleset*? | Simpan biar nggak lupa. Follow buat fondasi berikutnya. | — (slide terakhir) |

Pojok: @irsyadtawakal kiri atas, nomor slide kanan atas, "Geser →" kanan bawah. Slide 8: "Simpan dulu" dan "Ikuti @irsyadtawakal".

Perubahan kecil dari naskah v1 supaya pas di slide (isi sama):
- Slide 2: hook 12 kata dipecah jadi label (pertanyaannya) + headline 3 kata. Isi baru satu baris pendek, dibayar slide 5 dan 7.
- Slide 3: dapat label "Masalahnya" dan tanda tanya oranye raksasa yang keluar dari tepi kiri.

## Ritme

Grafis (Bawah) · Tipe · Blok warna · Grafis (Atas) · Tipe · Tipe · CTA.
- 2 slide grafis (batas 3 untuk 7–8 slide). Slide CTA tidak dihitung.
- Bawah hanya sekali, tidak ada komposisi yang sama dua kali.
- Tipe paling banyak dua berturut-turut (6 dan 7).
- Jembatan di slide 3 dan 5 (2 dari 8), keduanya dibayar slide berikutnya.
- Tidak ada slide jeda.

## Spesifikasi grafis

**Slide 2 · balik posisi** (lebar 1080 × 640)
- Ide: bubble kamu dan bubble AI tukar tempat.
- Objek: bubble AI mengetik (Indigo Lift, titik terakhir oranye), miring −4°, kiri atas; bubble kamu (hero, putih solid) berisi **"Bikinin caption promo kopi susu"**, miring 4°, kanan bawah, menumpuk sedikit di bawah bubble AI; input bar kosong dengan caret, putih 20%, keluar dari tepi kiri bawah.
- Tanda oranye: panah tangan melengkung dari bubble kamu ke bubble AI (tanda tukar posisi).
- Doodle: tidak ada.

**Slide 5 · AI yang nanya** (lebar 1080 × 640)
- Ide: kamu kirim permintaan plus satu kalimat, AI belum menjawab, dia menyiapkan pertanyaan.
- Objek: bubble kamu (hero) **"Bikinin caption promo. Sebelum jawab, tanya saya dulu."**, miring −4°, atas; bubble AI mengetik, miring 5°, kanan bawah; tiga chip kecil berisi "?" saja, melayang keluar dari bubble AI, miring berbeda-beda.
- Tanda oranye: garis bawah bergelombang di bawah "tanya saya dulu".
- Doodle: plus putih kecil di kiri bawah.
- Tidak ada pertanyaan AI yang ditulis. Kalau kamu kirim screenshot asli hasil tes prompt slide 7, chip "?" bisa diganti satu pertanyaan asli dari AI.

Semua grafis: tanpa tekstur, bayangan, atau glow. Kedalaman hanya dari tumpukan dan opasitas.

## Checklist asset

| Asset | Untuk | Nama file | Status |
| --- | --- | --- | --- |
| Cover hasil generate (A4) | Slide 1 dan PDF LinkedIn | `output/cover.png` | Ada |
| Gambar slide CTA | Slide 8 | `assets/cta.png` | Ada (versi 2) |
| Screenshot asli tes prompt slide 7 (opsional, data pribadi ditutup) | Satu pertanyaan asli di grafis slide 5 | `assets/contoh-nanya-balik.png` | Belum. Kalau tidak ada, chip tetap "?" |

Tidak ada logo (slide tidak menyebut nama tools).

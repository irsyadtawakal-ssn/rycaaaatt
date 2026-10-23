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

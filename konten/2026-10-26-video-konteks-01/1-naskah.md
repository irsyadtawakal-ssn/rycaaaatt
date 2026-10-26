# 1-naskah — Video uji: AI "lupa" di chat panjang

- **Status:** tahap 2, draft (belum disetujui)
- **Pilar:** 1 Fondasi AI · **Seri:** video uji, tanpa nomor (uji pipeline motion graphic + B-roll kolase)
- **Format:** Wajah + Objek, dengan 2 B-roll kolase (Video Brain bagian 5)
- **Audiens:** sudah pakai AI tapi masih basic · **Target:** pemula penasaran, profesional
- **Sikap:** #1 Fondasi lebih penting daripada hype
- **Kerangka:** Fondasi
- **Insight:** AI tidak lupa seperti manusia. Teks yang bisa ia "lihat" dalam satu chat ada batasnya (context window), dan makin panjang chat-nya, makin gampang info penting terlewat.
- **Payoff:** chat sudah panjang → minta AI merangkum keputusan dan aturan → buka chat baru → tempel rangkumannya.

## Naskah

Durasi perkiraan: ±32 s (`naskah_waktu.py`, 5,5 suku kata/detik, belum dikalibrasi dengan kecepatan bicara Irsyad).

| Time | Loop part | Spoken | On-screen text / caption keyword | Visual (shot, object, screen, card) |
| --- | --- | --- | --- | --- |
| 0–2,2 s | Hook | Ngobrol panjang sama ChatGPT, terus dia lupa? | Input bar: "Kok AI-nya **lupa**?" · kata kunci: lupa | Wajah, condong ke kamera sambil mengangkat HP |
| 2,2–4,2 s | Hook | Dia nggak lupa. Papannya kepenuhan. | kata kunci: kepenuhan | Potongan pertama di ±2 s · snap zoom di "kepenuhan" · input bar keluar |
| 4,2–6,7 s | Intensify | Di awal kamu bilang, jangan pakai emoji. | kata kunci: emoji | Wajah · objek chat di atas kepala: bubble "jangan pakai emoji" |
| 6,7–9,6 s | Intensify | Puluhan pesan kemudian, emojinya balik lagi. | (teks kinetik B-roll) | **B-roll kolase 1** (±2,9 s) |
| 9,6–11,2 s | Set-up 1 | Bayangin papan pesanan di dapur. | kata kunci: papan | Wajah |
| 11,2–13,6 s | Set-up 1 | Kalau penuh, catatan lama dihapus. | (teks kinetik B-roll) | **B-roll kolase 2** (±2,4 s) |
| 13,6–16 s | Set-up 1 | Di AI, papan itu namanya context window. | kata kunci: context window | Wajah · objek chat: kartu "context window" |
| 16–18,7 s | Rehook 1 | Anehnya, makin sering kamu ngulang, makin parah. | kata kunci: ngulang | Wajah, snap zoom |
| 18,7–20,3 s | Set-up 2 | Riset tahun 2023 nemu, | Label sumber: Liu dkk., 2023, "Lost in the Middle" | Wajah · label sumber di atas kepala |
| 20,3–24,4 s | Set-up 2 | makin panjang teksnya, info penting makin gampang kelewat. | kata kunci: kelewat | Wajah, potongan baru (ganti visual di tengah kalimat) |
| 24,4–26,2 s | Rehook 2 | Jadi jangan ngulang. Pindah papan. | kata kunci: pindah | Wajah · coretan oranye di bawah "pindah papan" |
| 26,2–28,7 s | Payoff | Ketik, rangkum semua aturan kita dalam poin. | kata kunci: rangkum | **Layar asli**: Irsyad mengetik prompt itu di chat panjang |
| 28,7–30,4 s | Payoff | Copy, buka chat baru, tempel. | — | **Layar asli**: copy, chat baru, tempel |
| 30,4–31,9 s | Contekan | (diam / lanjut napas) | 1. AI punya papan terbatas · 2. Chat panjang, info kelewat · 3. Ngulang bikin makin penuh · 4. Rangkum, chat baru, tempel | Frame Contekan 1,5 s |
| 31,9–33,7 s | Ending hook | Ngobrol udah panjang? Pindah papan. | — | Wajah · input bar kembali kosong (loop ke frame 1) |

### Hasil cek waktu

- PASS kalimat pertama selesai di 2,2 s · PASS loop (mengulang "ngobrol, panjang") · PASS durasi.
- WARN beat 2–4 "tidak punya contoh nyata": dibiarkan, "jangan pakai emoji" sudah contoh konkret yang tidak terdeteksi script.
- WARN beat 9–11: dibiarkan, isinya prompt literal dan langkah konkret.
- Beat "Riset tahun 2023 …" dipecah dua dengan pergantian visual, supaya tidak ada beat > 4 s tanpa perubahan.

## B-roll kolase (Video Brain bagian 5)

| No | Momen | Opsi A (tanpa wajah) | Opsi B (dengan wajah) | Teks kinetik di dalam B-roll |
| --- | --- | --- | --- | --- |
| 1 | Intensify, "puluhan pesan kemudian, emojinya balik lagi" | Struk chat panjang menjulur dari HP, pesan paling atas ber-pin oranye | Irsyad menarik struk chat panjang dari HP, menoleh ke ujung atasnya | "jangan pakai **emoji**" |
| 2 | Set-up 1, "kalau penuh, catatan lama dihapus" | Papan tulis pesanan penuh, penghapus oranye di baris atas | Irsyad memegang penghapus oranye, menghapus baris paling atas papan | "catatan lama **dihapus**" |

Total B-roll ±5,3 s dari ±33 s (≈16%). Tidak ada di 3 detik pertama dan tidak di payoff. Payoff tetap layar asli.

## Fakta yang dicek

- **Context window:** batas teks yang bisa diproses model dalam satu percakapan; besarnya beda per model dan per paket. Angka spesifik sengaja tidak disebut karena sering berubah. Memory (fitur ingatan lintas chat) berbeda dengan context window. Sumber sekunder: [fast.io](https://fast.io/resources/chatgpt-conversation-too-long/), [TechCrunch 2023](https://techcrunch.com/2023/03/14/openai-is-testing-a-version-of-gpt-4-that-can-remember-long-conversations/). Belum ada halaman resmi OpenAI yang ditemukan.
- **"Makin panjang teksnya, info penting makin gampang kelewat":** Liu dkk., "Lost in the Middle: How Language Models Use Long Contexts", arXiv Juli 2023, terbit di TACL vol. 12 (2024). Temuan: performa turun saat konteks makin panjang, dan paling buruk saat info penting ada di tengah. [arXiv](https://arxiv.org/abs/2307.03172v3), [ACL Anthology](https://preview.aclanthology.org/setup/2024.tacl-1.9)
- **"Catatan lama dihapus"** adalah analogi, bukan klaim cara kerja persis ChatGPT. Yang pasti: ruangnya terbatas dan info bisa terlewat.

## Asset yang dibutuhkan

| File | Untuk | Catatan |
| --- | --- | --- |
| `video/mentah.mp4` | Rekaman wajah | Baca naskah di atas, satu take atau per bagian |
| `assets/layar-rangkum.mp4` | Payoff | Rekaman layar asli: ketik prompt rangkum di chat panjang, copy, buka chat baru, tempel |
| `assets/broll-1-a.png` / `-b.png` | B-roll 1 | Dari prompt di `assets/broll/` (disesuaikan setelah naskah disetujui) |
| `assets/broll-2-a.png` / `-b.png` | B-roll 2 | Sama |

## Tes sebelum tayang

Irsyad coba sekali prompt "Rangkum semua keputusan dan aturan kita dalam poin" di chat panjang yang asli. Hasil yang benar: daftar poin berisi aturan dari awal chat (misalnya "jangan pakai emoji"), dan setelah ditempel di chat baru, jawaban berikutnya mengikuti aturan itu.

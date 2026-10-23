"""Brand board carousel @irsyadtawakal: satu halaman HTML yang merangkum Visual Brain untuk carousel.

Slide contoh dirender dari lib/slides.py (bukan gambar tempelan), jadi selalu ikut aturan terbaru.
Isi kalimat di slide contoh hanya untuk memperlihatkan tata letak, bukan naskah post.

    py lib/brand_board.py    # tulis assets/brand-board/carousel.html
"""
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
from slides import *  # noqa: E402,F401
from slides import IND, LIFT, OR, PW, WH, CSS, FIT_JS, _corners, _headline, _e, fonts_css  # noqa: E402

COVER = "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "cover-induk.png").read_bytes()).decode()

# ---------- slide contoh ----------

g_bubble = (bubble_user("Tolong bantu saya bikin caption promo kopi…", 40, 70, 860)
            + bubble_ai_typing(420, 330, 620) + mark_arrow(700, 290, 820, 345, bend=-10) + doodle_plus(990, 80))
g_cards = (app_card("ChatGPT", 120, 150, 300, 400, -14) + app_card("Claude", 660, 150, 300, 400, 13)
           + app_card("Gemini", 380, 110, 320, 430, -2, hero=True, check=True, sub="akun sendiri")
           + mark_underline(380, 720, 575))
g_stack = (sticky("siapa kamu", "Pemilik warung kopi di Bogor", 30, 120, 440, 280, -6)
           + sticky("tujuannya", "Caption promo buat minggu ini", 60, 430, 420, 260, 4, tone="wh")
           + sticky("gayanya", "Santai, pakai bahasa sehari-hari", 30, 730, 440, 260, -3)
           + mark_arrow(470, 300, 470, 520, bend=40))


def type_slide(n):
    return (f'<div class="s" id="s{n}">{_corners(n)}'
            f'<div style="position:absolute;left:-40px;top:150px;font:800 520px/0.9 \'Bricolage Grotesque\';'
            f'font-stretch:80%;letter-spacing:-0.02em;color:{OR}">3</div>'
            f'<div class="txt" style="top:760px"><div class="lab">Langkah 3 dari 3</div>'
            f'<h1>Minta AI tanya balik <em>dulu</em></h1>'
            f'<div class="body">Satu kalimat tambahan, jawabannya jauh lebih pas.</div></div></div>')


def block_slide(n):
    return (f'<div class="s" id="s{n}">{_corners(n)}'
            f'<div style="position:absolute;left:0;right:0;top:0;height:540px;background:{OR};color:{IND};'
            f'padding:150px 64px 0"><div style="font:italic 56px \'Instrument Serif\'">Istilahnya</div>'
            f'<div style="font:800 190px/1 \'Bricolage Grotesque\';font-stretch:80%;letter-spacing:-2px;margin-top:10px">konteks</div></div>'
            f'<div class="txt" style="top:640px"><div style="font:800 150px/1 \'Bricolage Grotesque\';color:{OR}">=</div>'
            f'<div style="font:700 56px/1.2 Figtree;margin-top:16px">Info latar yang cuma kamu yang tahu</div></div></div>')


def pause_slide(n):
    return (f'<div class="s" id="s{n}" style="background:{PW};color:{IND}">'
            f'<div class="corner tl" style="color:{IND}">@irsyadtawakal</div><div class="corner tr" style="color:{IND}">{n}</div><div class="corner br" style="color:{IND}">Geser →</div>'
            f'<div class="txt" style="top:300px"><div class="lab" style="color:{IND}">Mitos atau fakta</div>'
            f'<div style="font:700 64px/1.2 Figtree;text-decoration:line-through;opacity:.4;margin-top:24px">AI pasti benar</div>'
            f'<div style="font:800 150px/1 \'Bricolage Grotesque\';font-stretch:80%;letter-spacing:-2px;margin-top:80px">'
            f'AI bisa <span style="color:{OR}">keliru</span></div></div></div>')


slides = build([
    slide(2, "Kabar baiknya", "Satu permintaan kecil bikin AI *paham*",
          "Nggak perlu jago teknologi. Cukup tiga langkah ini.", g_bubble, role="hook"),
    slide(3, "Langkah 1 dari 3", "Buka versi gratis yang *resmi*",
          "ChatGPT, Gemini, atau Claude. Daftar pakai akunmu sendiri.", g_cards,
          bridge="Berikutnya: langkah yang paling sering dilewati"),
    slide(4, "Langkah 2 dari 3", "Kasih tahu siapa kamu dan *tujuannya*",
          "Itu namanya konteks: info latar yang cuma kamu yang tahu.", g_stack, aspect="tinggi"),
    type_slide(5), block_slide(6), pause_slide(7),
    recap_slide(8, ["Buka versi gratis yang resmi", "Kasih tahu siapa kamu dan tujuannya",
                    "Minta AI tanya balik dulu"], headline="Tiga langkah, satu *layar*"),
])


def thumb(html, caption, tag):
    return (f'<figure><div class="th"><div class="sc">{html}</div></div>'
            f'<figcaption><b>{tag}</b>{caption}</figcaption></figure>')


# ---------- halaman ----------

BOARD_CSS = f"""
body{{background:#1B1250;color:#fff;font-family:Figtree,sans-serif;margin:0;padding:0 0 120px}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 32px}}
section{{padding:72px 0 8px;border-top:1px solid rgba(255,255,255,.15)}}
section:first-of-type{{border:0}}
.kick{{font:italic 34px 'Instrument Serif';opacity:.85}}
.big{{font:800 76px/1 'Bricolage Grotesque';font-stretch:80%;letter-spacing:-1px;margin:6px 0 18px}}
.big em{{font-style:normal;color:{OR}}}
.lead{{font:400 20px/1.5 Figtree;max-width:760px;opacity:.9;margin-bottom:36px}}
.sw{{display:flex;height:150px;border-radius:20px;overflow:hidden;margin-bottom:20px}}
.sw div{{display:flex;flex-direction:column;justify-content:flex-end;padding:18px 22px;font:700 18px Figtree}}
.sw small{{font:500 14px Figtree;opacity:.85}}
.tints{{display:flex;gap:16px;margin-bottom:12px}}
.tints div{{flex:1;height:84px;border-radius:16px;padding:14px 18px;font:500 14px/1.4 Figtree;display:flex;flex-direction:column;justify-content:flex-end}}
.rules{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px}}
.rules div{{border:1px solid rgba(255,255,255,.2);border-radius:16px;padding:18px 22px;font:500 17px/1.45 Figtree}}
.rules b{{color:{OR};font:800 28px 'Bricolage Grotesque';margin-right:10px}}
table{{border-collapse:collapse;width:100%;font:400 16px/1.4 Figtree}}
th,td{{text-align:left;padding:14px 12px;border-top:1px solid rgba(255,255,255,.15);vertical-align:top}}
th{{font:500 13px Figtree;opacity:.65;text-transform:none;border-top:0}}
.spec-h{{font:800 52px/1 'Bricolage Grotesque';font-stretch:80%;letter-spacing:-1px}}
.row{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:28px}}
figure{{margin:0}}
.th{{width:100%;aspect-ratio:1080/1350;position:relative;overflow:hidden;border-radius:10px;box-shadow:0 0 0 1px rgba(255,255,255,.18)}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1350px;transform-origin:0 0;transform:scale(var(--k,.23))}}
figcaption{{font:400 15px/1.45 Figtree;margin-top:12px;opacity:.9}}
figcaption b{{display:block;font:700 16px Figtree;color:#fff;margin-bottom:2px}}
.cov{{width:100%;aspect-ratio:1080/1350;object-fit:cover;border-radius:10px;box-shadow:0 0 0 1px rgba(255,255,255,.18);display:block}}
.two{{display:grid;grid-template-columns:minmax(260px,340px) 1fr;gap:40px;align-items:start}}
@media(max-width:760px){{.two{{grid-template-columns:1fr}}.big{{font-size:52px}}}}
.no li{{margin:0 0 10px 18px;font:400 17px/1.5 Figtree}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:36px}}
.cols h3{{font:800 30px 'Bricolage Grotesque';margin-bottom:14px}}
.mot{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.mot div{{background:rgba(255,255,255,.07);border-radius:14px;padding:16px 18px;font:400 15px/1.45 Figtree}}
.mot b{{display:block;font:700 16px Figtree;margin-bottom:4px}}
"""

SCALE_JS = """<script>
function fit(){document.querySelectorAll('.th').forEach(t=>{t.firstElementChild.style.transform='scale('+(t.clientWidth/1080)+')'})}
addEventListener('resize',fit);document.fonts.ready.then(()=>{fit()});fit();
</script>"""

html = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Brand board carousel — @irsyadtawakal</title>
{fonts_css(embed=True)}<style>{CSS}{BOARD_CSS}</style></head><body><div class="wrap">

<section>
  <div class="kick">Visual Brain · carousel 1080 × 1350</div>
  <div class="big">Ruang gelap, satu kata <em>menyala</em></div>
  <p class="lead">Kanvas indigo pekat, judul putih besar, satu kata oranye, dan banyak ruang kosong. Seperti teman yang pintar menjelaskan AI, bukan perusahaan teknologi yang menjual. Moodnya: kejernihan larut malam. Halaman ini ringkasan dari <code>brand/04-visual-brain.md</code>; kalau beda, dokumen itu yang menang.</p>
  <div class="rules">
    <div><b>1</b>Tiga warna saja: Indigo, Putih, Oranye.</div>
    <div><b>2</b>Tiga font: Bricolage (judul), Figtree (sisanya), Instrument Serif Italic (kicker cover, label pendek, kutipan jeda).</div>
    <div><b>3</b>Latar bawaan Deep Indigo.</div>
    <div><b>4</b>Tiap judul punya tepat satu kata oranye.</div>
    <div><b>5</b>Oranye hanya besar dan tebal. Tidak pernah teks kecil, tidak pernah di atas putih.</div>
    <div><b>6</b>@irsyadtawakal ada di setiap slide, pojok kiri atas.</div>
  </div>
</section>

<section>
  <div class="kick">1 · Palet</div>
  <div class="big">60 / 30 / 10 di <em>setiap</em> frame</div>
  <div class="sw">
    <div style="flex:6;background:{IND}">Deep Indigo ~60%<small>#261A66 · latar, teks di slide jeda dan blok oranye</small></div>
    <div style="flex:3;background:{WH};color:{IND}">Putih ~30%<small>#FFFFFF · judul, body, handle, garis</small></div>
    <div style="flex:1;background:{OR};min-width:120px">Oranye ~10%<small>#EF5F18</small></div>
  </div>
  <div class="tints">
    <div style="background:{LIFT}">Indigo Lift #3A2A9C<span style="opacity:.8">Gradien halus di slide grafis. Bukan warna teks.</span></div>
    <div style="background:{PW};color:{IND}">Pause White #F4F2FF<span style="opacity:.8">Latar slide jeda. Maksimal 1 per carousel.</span></div>
  </div>
  <p class="lead" style="margin-top:20px">Kontras (dihitung dari hex): putih di indigo ±15:1, oranye di indigo ±4,5:1 (hanya teks besar tebal dan bentuk), putih di oranye ±3,3:1 (teks harus besar dan tebal). Putih boleh transparan: 70% untuk label pendukung, 15% untuk garis pembatas.</p>
</section>

<section>
  <div class="kick">2 · Tipografi</div>
  <div class="big">Bricolage berteriak, Figtree <em>menjelaskan</em></div>
  <table>
    <tr><th>Peran</th><th>Font</th><th>Ukuran (kanvas 1080)</th><th>Warna</th></tr>
    <tr><td>Judul</td><td>Bricolage Grotesque ExtraBold 800, lebar ±80%</td><td>120–150 px, line height 1.0</td><td>Putih, satu kata oranye</td></tr>
    <tr><td>Angka langkah besar</td><td>Bricolage ExtraBold 800</td><td>180–240 px</td><td>Oranye</td></tr>
    <tr><td>Subteks</td><td>Figtree Bold 700</td><td>48–56 px</td><td>Putih</td></tr>
    <tr><td>Body</td><td>Figtree Regular 400 / Medium 500</td><td>36–44 px, line height 1.4</td><td>Putih</td></tr>
    <tr><td>Handle, label, nomor slide</td><td>Figtree Medium 500</td><td>±26–34 px</td><td>Putih (nomor 70–85%)</td></tr>
    <tr><td>Kicker cover</td><td>Instrument Serif Italic</td><td>96–110 px</td><td>Indigo di cover terang, putih di cover gelap</td></tr>
    <tr><td>Label slide isi</td><td>Instrument Serif Italic</td><td>48–64 px ("Langkah 1 dari 3", "Istilahnya")</td><td>Putih</td></tr>
  </table>
  <p class="lead" style="margin-top:20px">Judul 8 kata atau kurang, maksimal 3 baris, huruf kapital hanya di awal kalimat, rata kiri (tengah hanya di cover), tidak boleh dipenggal di tengah kata. Body maksimal ±40 kata per slide. Maksimal tiga ukuran huruf per frame, dan judul minimal 2,5× body.</p>
</section>

<section>
  <div class="kick">3 · Cover</div>
  <div class="big">Satu layout, <em>gambar</em> bebas</div>
  <div class="two">
    <figure><img class="cov" src="{COVER}" alt="Cover induk">
      <figcaption><b>Cover induk</b>Rujukan yang dilampirkan di setiap generate cover.</figcaption></figure>
    <div>
      <p class="lead">Cover dibuat utuh (gambar dan teks) di ChatGPT Image atau Nano Banana dari prompt JSON. Yang dikunci hanya <b>layout, tipografi, dan handle</b>. Adegan, subjek, suasana, dan warna bebas per topik.</p>
      <ul class="no" style="list-style:disc">
        <li>Blok teks tengah, maksimal ±30% bingkai, di area gambar yang paling tenang (atas secara default).</li>
        <li>Tiga lapis: <b>kicker</b> serif italic (2–4 kata), <b>kata raksasa</b> Bricolage condensed ±360 px huruf kecil (maks. 10 huruf, tidak pernah oranye), <b>satu baris</b> Bricolage Medium ±46 px (maks. 8 kata) dengan satu kata oranye lalu kursor tipis menempel.</li>
        <li>Empat label pojok: @irsyadtawakal (kiri atas), seri dan nomor (kanan atas), "Simpan dulu" (kiri bawah), "Geser →" (kanan bawah).</li>
        <li>Teks seluruhnya indigo di gambar terang atau seluruhnya putih di gambar gelap, tidak pernah campur.</li>
        <li>Tanpa baris hook dan tanpa nomor slide di cover. Hook pindah ke slide 2 dan baris pertama caption.</li>
        <li>Subjek Irsyad di ±separuh cover, tidak lebih dari dua cover Irsyad berdampingan di grid. Satu benda oranye di gambar boleh menggemakan kata oranye.</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="kick">4 · Slide isi</div>
  <div class="big">Lima tipe, <em>ritme</em> yang bergantian</div>
  <p class="lead">Contoh di bawah dirender langsung dari <code>lib/slides.py</code>. Kalimatnya hanya pengisi layout. Grafis selalu "objek obrolan": bubble, kartu aplikasi, sticky note, kolom ketik, miring dan bertumpuk, dengan contoh kalimat nyata di dalamnya dan tepat satu coretan tangan oranye.</p>
  <div class="row">
    {thumb(slides[0], "Teks di atas, grafis lebar di bawah, latar gradien halus. Untuk slide 2 (hook) dan \"Coba hari ini\".", "1 · Slide gambar (Bawah)")}
    {thumb(slides[1], "Grafis lebar dengan kartu aplikasi; objek utama putih solid di depan. Bridge line menggoda slide berikutnya.", "2 · Slide jendela (Tengah)")}
    {thumb(slides[2], "Grafis tinggi (tumpukan sticky note) di panel samping, teks di kolom satunya. Samping kiri dan kanan bergantian.", "2 · Samping kanan")}
    {thumb(slides[3], "Indigo polos. Angka oranye raksasa keluar dari tepi kiri, judul di bawahnya. Juga untuk daftar tiga baris.", "3 · Slide ketik")}
    {thumb(slides[4], "Blok oranye ±40% tinggi dengan istilah berwarna indigo, lalu \"=\" oranye dan perbandingan sehari-hari.", "4 · Slide blok warna")}
    {thumb(slides[5], "Latar Pause White, teks indigo. Mitos dicoret 40%, fakta dengan satu kata oranye ≥120 px. Maksimal 1 per carousel.", "5 · Slide jeda")}
    {thumb(slides[6], "Tipe ketik tepat sebelum \"Coba hari ini\": 3–5 poin bernomor oranye. Slide yang disimpan orang, harus bisa berdiri sendiri.", "Contekan")}
  </div>
  <p class="lead" style="margin-top:36px">Aturan ritme: tidak ada dua slide gambar berurutan, tidak lebih dari dua slide bertipe sama berurutan, komposisi tidak sama dua kali berturut-turut. Carousel 7–8 slide maksimal 3 slide grafis, 9–10 slide maksimal 4. Slide 2 dan "Coba hari ini" adalah slide gambar atau slide ketik. Gambar cover tidak pernah muncul di slide isi, kecuali slide CTA di akhir.</p>
  <p class="lead" style="margin-top:24px">Slide CTA (slide terakhir, sejak 23 Okt 2026): adegan cover beberapa detik kemudian, digenerate baru tanpa teks (bukan potongan cover), 45% bagian atas dibiarkan tenang. Di atasnya, rata tengah: "Giliran kamu" serif italic, satu pertanyaan komentar soal topik carousel (maksimal 10 kata, satu kata oranye), lalu "Simpan biar nggak lupa. Follow buat fondasi berikutnya." Pertanyaannya sama dengan penutup caption Instagram. Teaser episode berikutnya tidak dipakai lagi.</p>
</section>

<section>
  <div class="kick">5 · Tata letak</div>
  <div class="big">Rata kiri, <em>35%</em> kosong</div>
  <div class="cols">
    <div><h3>Ukuran dan margin</h3>
      <ul class="no" style="list-style:disc">
        <li>Kanvas utama 1080 × 1350. Margin samping 64 px. Semua jarak kelipatan 8: 16, 24, 32, 48, 64, 96, 128.</li>
        <li>Label pojok: 44 px dari atas, 52 px dari bawah, 64 px dari samping. Figtree Medium ±26 px, putih 85%.</li>
        <li>Slide terakhir: "Simpan dulu" kiri bawah, "Ikuti @irsyadtawakal" kanan bawah.</li>
      </ul></div>
    <div><h3>Ruang napas</h3>
      <ul class="no" style="list-style:disc">
        <li>Teks maksimal 40% luas kanvas; 35–50% frame kosong.</li>
        <li>Satu blok teks dan satu grafis per slide. Tidak muat? Jadikan dua slide.</li>
        <li>Bridge line: Figtree Medium 30 px, putih 70%, ±120 px dari tepi bawah, hanya untuk teaser yang benar-benar dibayar slide berikutnya, maksimal di separuh slide.</li>
      </ul></div>
  </div>
</section>

<section>
  <div class="kick">6 · Motif</div>
  <div class="big">Dikenali sebelum <em>handle</em> dibaca</div>
  <div class="mot">
    <div><b>Kata oranye</b>Satu kata judul, Bricolage 800, di setiap frame.</div>
    <div><b>Coretan tangan oranye</b>Satu lingkaran, garis bawah bergelombang, coretan, atau panah per grafis. Tanda tangan brand.</div>
    <div><b>Geser →</b>Label pojok kanan bawah, di semua slide kecuali terakhir.</div>
    <div><b>Blok prompt</b>Teks polos di indigo, kalimat lama 45%, kalimat baru dengan bar oranye 6 px di kiri dan kursor.</div>
    <div><b>Angka langkah besar</b>Oranye, 180–240 px, keluar dari tepi kiri.</div>
    <div><b>Label serif italic</b>"Langkah 1 dari 3", "Istilahnya", "Contekan" di atas judul.</div>
    <div><b>Mitos dan fakta</b>Mitos dicoret 40%, fakta dengan satu kata oranye besar. Tanpa merah dan hijau.</div>
    <div><b>Kursor mengetik</b>Batang tipis tepat setelah kata terakhir di cover atau blok prompt.</div>
  </div>
  <p class="lead" style="margin-top:24px">Maksimal tiga motif per frame di luar kata oranye dan handle. Motif tidak diubah ukuran atau warnanya agar "pas"; kalau tidak muat, ubah layout. Motif baru ditambahkan ke Visual Brain dulu, baru dipakai.</p>
</section>

<section>
  <div class="kick">7 · Yang ditolak</div>
  <div class="big">Kalau ada ini, <em>salah</em></div>
  <div class="cols">
    <div><h3>Warna dan huruf</h3><ul class="no" style="list-style:disc">
      <li>Gradien ungu-biru "AI", glow, neon, hitam, merah/hijau untuk benar/salah.</li>
      <li>Teks oranye kecil, panjang, atau di atas putih (kecuali satu kata besar di slide jeda).</li>
      <li>Font keempat, HURUF KAPITAL SEMUA, judul di tengah (kecuali blok cover), teks rata kanan-kiri, kontur atau bayangan pada teks.</li>
      <li>Judul lebih dari 8 kata atau lebih dari satu kata oranye.</li></ul></div>
    <div><h3>Gambar dan suasana</h3><ul class="no" style="list-style:disc">
      <li>Robot, otak menyala, papan sirkuit, kode biner, hologram, wajah AI mirip manusia.</li>
      <li>Foto stok orang menunjuk layar, jabat tangan, kantor generik. Foto berwarna orang di slide isi.</li>
      <li>Antarmuka palsu, jawaban chatbot karangan, screenshot yang diedit. Grafik atau angka tanpa sumber nyata.</li>
      <li>Visual menakutkan, tanda bahaya, "AI mengambil alih". Meme, emoji, stiker.</li>
      <li>Watermark atau logo selain @irsyadtawakal (kecuali logo resmi alat di kartu aplikasi).</li></ul></div>
  </div>
</section>

</div>{SCALE_JS}{FIT_JS}</body></html>"""

if __name__ == "__main__":
    out_dir = ROOT / "assets" / "brand-board"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "carousel.html"
    out.write_text(html, encoding="utf-8")
    print("ditulis", out)

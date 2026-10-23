"""Pustaka grafis slide isi @irsyadtawakal, gaya "objek obrolan" (sejak 13 Okt 2026).

Isinya objek dunia chat: bubble, kartu aplikasi, sticky note, kolom ketik, chip, kursor.
Objek dibuat besar, miring, dan ditumpuk, dengan contoh kalimat nyata di dalamnya, ditambah
tepat satu coretan tangan oranye per grafis. Aturan lengkapnya ada di Visual Brain bagian 6.

Cara pakai:
    g = app_card("ChatGPT", 120, 150, 300, 400, -14) + ...
    html = page([window_slide(3, "Langkah 1", "Buka versi gratis yang *resmi*", "Body...", g)])
Render HTML ke PNG 1080x1350 dengan Playwright atau Chromium (screenshot tiap elemen .s).
Jalankan file ini langsung untuk membuat demo.html berisi contoh slide, lalu render dengan:
    node lib/render.mjs demo.html output/

Logo alat (ChatGPT, Gemini, Claude): pakai HANYA file logo resmi dari halaman brand
masing-masing, tanpa diubah. Isi parameter logo= dengan path filenya. Logo selalu tegak walau
kartunya miring. Kalau tidak ada file resmi, kartu cukup menampilkan nama alatnya.
"""
import html as _h
import math
import random

IND, LIFT, OR, PW, WH = "#261A66", "#3A2A9C", "#EF5F18", "#F4F2FF", "#FFFFFF"

# Font brand dibaca dari assets/fonts (tidak perlu internet saat render).
import base64 as _b64
from pathlib import Path as _Path
_FONT_PATH = _Path(__file__).resolve().parent.parent / "assets" / "fonts"

def fonts_css(embed=False):
    """@font-face untuk tiga font brand. embed=True menanam font di dalam HTML (base64), jadi
    file tetap tampil benar kalau dipindah, dikirim, atau dibuka di pratinjau. embed=False memakai
    alamat file lokal: lebih kecil, cukup untuk render PNG di laptop ini."""
    def src(name):
        f = _FONT_PATH / name
        url = f"data:font/woff2;base64,{_b64.b64encode(f.read_bytes()).decode()}" if embed else f.as_uri()
        return f"src:url({url}) format('woff2')"
    return (
        "<style>"
        f"@font-face{{font-family:'Bricolage Grotesque';{src('bricolage-grotesque-variable.woff2')};"
        "font-weight:200 800;font-stretch:75% 100%}"
        f"@font-face{{font-family:Figtree;{src('figtree-400.woff2')};font-weight:400}}"
        f"@font-face{{font-family:Figtree;{src('figtree-500.woff2')};font-weight:500}}"
        f"@font-face{{font-family:Figtree;{src('figtree-700.woff2')};font-weight:700}}"
        f"@font-face{{font-family:'Instrument Serif';{src('instrument-serif-italic.woff2')};font-style:italic}}"
        "</style>"
    )

FONTS = fonts_css()

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
.s{{width:1080px;height:1350px;position:relative;overflow:hidden;background:{IND};color:#fff;font-family:Figtree,sans-serif}}
.grad{{background:radial-gradient(120% 90% at 80% 100%,{LIFT} 0%,{IND} 60%)}}
.corner{{position:absolute;z-index:5;font:500 26px Figtree;opacity:.85}}
.tl{{top:44px;left:64px}}.tr{{top:44px;right:64px}}.br{{bottom:52px;right:64px}}.bl{{bottom:52px;left:64px}}
.lab{{font:italic 56px 'Instrument Serif';margin-bottom:18px}}
h1{{font-family:'Bricolage Grotesque';font-weight:800;font-stretch:80%;font-size:104px;line-height:.98;letter-spacing:-1px}}
h1 em{{font-style:normal;color:{OR}}}
.body{{font:400 38px/1.4 Figtree;margin-top:30px;opacity:.92}}
.txt{{position:absolute;left:64px;right:64px}}
.zone{{position:absolute;left:0;right:0;top:0;height:640px;overflow:hidden;background:{LIFT}}}
.o{{position:absolute}}
svg.mk{{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}}
"""

def _e(t):
    return _h.escape(t)

def _headline(t):
    # *kata* -> kata oranye (tepat satu per headline)
    parts = t.split("*")
    return "".join(f"<em>{_e(p)}</em>" if i % 2 else _e(p) for i, p in enumerate(parts))

# ---------- objek ----------

def bubble_user(text, x, y, w, rot=-5, size=44, time="09.41", avatar="K"):
    """Bubble chat dari kamu: putih solid, ekor di kiri bawah, contoh kalimat nyata.
    time: jam kirim kecil di pojok kanan bawah (None untuk menyembunyikan);
    avatar: huruf di lingkaran kecil di sisi ekor (None untuk menyembunyikan)."""
    av = (f'<div style="position:absolute;left:-34px;bottom:-40px;width:84px;height:84px;border-radius:50%;'
          f'background:{LIFT};border:4px solid {WH};display:flex;align-items:center;justify-content:center;'
          f'font:700 36px Figtree;color:{WH}">{_e(avatar)}</div>') if avatar else ""
    tm = (f'<div style="margin-top:14px;text-align:right;font:500 26px Figtree;opacity:.55">{_e(time)} ✓✓</div>'
          if time else "")
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);'
            f'background:{WH};color:{IND};border-radius:48px 48px 48px 12px;padding:48px 56px 36px;'
            f'font:500 {size}px/1.35 Figtree">{_e(text)}{tm}{av}</div>')

def bubble_ai_typing(x, y, w, h=170, rot=4):
    """Bubble AI sedang mengetik: titik terakhir oranye. Jangan isi jawaban AI karangan."""
    dots = "".join(f'<i style="width:40px;height:40px;border-radius:50%;background:{c};opacity:{a}"></i>'
                   for c, a in ((WH, .5), (WH, .75), (OR, 1)))
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);'
            f'background:{LIFT};border:3px solid rgba(255,255,255,.35);border-radius:48px 48px 12px 48px;'
            f'display:flex;align-items:center;padding-left:56px;gap:22px">{dots}</div>')

def bubble_ai_empty(x, y, w, h, label="AI", rot=0):
    """Bubble AI kosong bergaris putus: AI belum tahu apa-apa."""
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);'
            f'border:4px dashed rgba(255,255,255,.55);border-radius:48px 48px 48px 12px;display:flex;'
            f'align-items:center;justify-content:center;font:700 44px Figtree">{_e(label)}</div>')

def app_card(name, x, y, w, h, rot=0, hero=False, logo=None, check=False, sub=None):
    """Kartu aplikasi. hero=True: putih solid di depan. logo=path file logo resmi (tetap tegak)."""
    bg = f"background:{WH};color:{IND}" if hero else "background:rgba(255,255,255,.14);border:3px solid rgba(255,255,255,.45)"
    inner = ""
    if logo:
        inner += (f'<img src="{_e(logo)}" style="width:{int(w*.42)}px;height:{int(w*.42)}px;object-fit:contain;'
                  f'transform:rotate({-rot}deg);margin-top:{int(h*.16)}px">')
    elif check:
        inner += (f'<div style="width:120px;height:120px;border-radius:50%;background:{PW};margin-top:{int(h*.16)}px;'
                  f'display:flex;align-items:center;justify-content:center"><svg width="64" height="64">'
                  f'<path d="M14 34 L28 48 L52 18" fill="none" stroke="{IND}" stroke-width="8" '
                  f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    if not logo and not check:
        # tanpa file logo resmi: nama alat besar dan tegak di tengah kartu, bukan teks kecil di sudut
        inner += (f'<div style="margin-top:auto;margin-bottom:auto;transform:rotate({-rot}deg);'
                  f'font:700 {int(w*.15)}px Figtree">{_e(name)}</div>')
    else:
        inner += f'<div style="margin-top:auto;font:{700 if hero else 500} {36 if hero else 34}px Figtree">{_e(name)}</div>'
    if sub:
        inner += f'<div style="font:500 26px Figtree;opacity:.7;margin-top:8px">{_e(sub)}</div>'
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);{bg};'
            f'border-radius:44px;display:flex;flex-direction:column;align-items:center;padding-bottom:44px">{inner}</div>')

def sticky(label, text, x, y, w, h, rot=-6, tone="pw"):
    """Sticky note: label kecil abu di atas, contoh nyata tebal di bawahnya."""
    bg = PW if tone == "pw" else WH
    fold = (f'<div style="position:absolute;right:0;bottom:0;width:64px;height:64px;'
            f'background:rgba(38,26,102,.14);border-radius:28px 0 28px 0;clip-path:polygon(100% 0,0 100%,100% 100%)"></div>')
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);'
            f'background:{bg};color:{IND};border-radius:28px;padding:40px">{fold}'
            f'<div style="font:500 26px Figtree;opacity:.6">{_e(label)}</div>'
            f'<div style="font:700 40px/1.2 Figtree;margin-top:14px">{_e(text)}</div></div>')

def input_bar(placeholder, value="", x=64, y=560, w=1020, rot=-3, caret=False):
    """Kolom ketik: pil putih panjang. value bisa berisi rahasia bertitik untuk dicoret."""
    c = f'<span style="width:4px;height:52px;background:{IND};display:inline-block"></span>' if caret else ""
    send = (f'<div style="margin-left:auto;margin-right:-30px;width:90px;height:90px;border-radius:50%;background:{IND};'
            f'display:flex;align-items:center;justify-content:center;flex:none"><svg width="44" height="44">'
            f'<path d="M8 22 H34 M22 9 L35 22 L22 35" fill="none" stroke="#fff" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
            f'<div style="height:150px;border-radius:75px;background:{WH};color:{IND};display:flex;align-items:center;'
            f'padding:0 56px;font:500 44px Figtree;gap:22px"><span style="opacity:.5">{_e(placeholder)}</span>'
            f'<span style="font:700 78px/1 Figtree;letter-spacing:4px;position:relative;top:10px">{_e(value)}</span>{c}{send}</div></div>')

def chip(text, x, y, rot=0, size=34):
    return (f'<div class="o" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);padding:{int(size*.65)}px {int(size*1.05)}px;'
            f'border-radius:999px;border:3px solid rgba(255,255,255,.5);font:500 {size}px Figtree">{_e(text)}</div>')

# ---------- tanda oranye (tepat satu per grafis) dan doodle putih (maks. satu) ----------

def _wob(points, amp=4, seed=7):
    r = random.Random(seed)
    return [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in points]

def _path(pts):
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f" Q{x0:.0f} {y0:.0f} {(x0+x1)/2:.0f} {(y0+y1)/2:.0f}"
    return d + f" L{pts[-1][0]:.0f} {pts[-1][1]:.0f}"

def _svg(d, w=8):
    return (f'<svg class="mk" width="1080" height="1350"><path d="{d}" fill="none" stroke="{OR}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def mark_loop(cx, cy, rx, ry, turns=1.15, seed=3):
    """Lingkaran tangan yang sedikit lewat dari titik awal."""
    n = 40
    pts = [(cx + rx*math.cos(2*math.pi*turns*i/n - 1.9)*(1 + .04*i/n),
            cy + ry*math.sin(2*math.pi*turns*i/n - 1.9)) for i in range(n + 1)]
    return _svg(_path(_wob(pts, 3, seed)), 7)

def mark_underline(x0, x1, y, amp=10):
    pts = [(x0 + (x1-x0)*i/12, y + amp*math.sin(i*1.1)) for i in range(13)]
    return _svg(_path(_wob(pts, 2)), 7)

def mark_arrow(x0, y0, x1, y1, bend=-60):
    mx, my = (x0+x1)/2, (y0+y1)/2 + bend
    a = math.atan2(y1-my, x1-mx)
    h1 = (x1 - 28*math.cos(a-.5), y1 - 28*math.sin(a-.5))
    h2 = (x1 - 28*math.cos(a+.5), y1 - 28*math.sin(a+.5))
    d = (f"M{x0} {y0} Q{mx:.0f} {my:.0f} {x1} {y1} "
         f"M{h1[0]:.0f} {h1[1]:.0f} L{x1} {y1} L{h2[0]:.0f} {h2[1]:.0f}")
    return _svg(d, 7)

def mark_strike(x0, x1, y, h=55):
    """Coretan zig-zag untuk menghapus rahasia di kolom ketik."""
    pts = [(x0 + (x1-x0)*i/8, y + (h/2 if i % 2 else -h/2)) for i in range(9)]
    return _svg("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in _wob(pts, 3)), 9)

def doodle_plus(x, y, s=56):
    return (f'<svg class="mk" width="1080" height="1350"><path d="M{x} {y-s/2} v{s} M{x-s/2} {y} h{s}" '
            f'stroke="#fff" stroke-opacity=".55" stroke-width="5" stroke-linecap="round"/></svg>')

# ---------- slide ----------

def _corners(n, last=False):
    if last:
        return (f'<div class="corner tl">@irsyadtawakal</div><div class="corner tr">{n}</div>'
                '<div class="corner bl">Simpan dulu</div><div class="corner br">Ikuti @irsyadtawakal</div>')
    return f'<div class="corner tl">@irsyadtawakal</div><div class="corner tr">{n}</div><div class="corner br">Geser →</div>'

def _bridge(text):
    """Jembatan ke slide berikutnya: teaser jujur, kecil, di atas label pojok."""
    if not text:
        return ""
    return (f'<div style="position:absolute;left:64px;right:260px;bottom:120px;font:500 30px Figtree;'
            f'opacity:.7">{_e(text)} →</div>')

def window_slide(n, label, headline, body, graphic, last=False, bridge=None):
    """Tipe 2: grafis di zona atas ~45%, teks di bawah. label contoh: "Langkah 1 dari 3"."""
    return (f'<div class="s" id="s{n}">{_corners(n, last)}<div class="zone">{graphic}</div>'
            f'<div class="txt" style="top:700px"><div class="lab">{_e(label)}</div><h1>{_headline(headline)}</h1>'
            f'<div class="body">{_e(body)}</div></div>{_bridge(bridge)}</div>')

def recap_slide(n, rows, label="Contekan", headline=None):
    """Slide contekan sebelum "Coba hari ini": 3-5 baris bernomor oranye, pembatas putih 15%."""
    items = "".join(
        f'<div style="display:flex;gap:36px;align-items:baseline;padding:52px 0;border-top:2px solid rgba(255,255,255,.15)">'
        f'<span style="font:800 88px/1 \'Bricolage Grotesque\';font-stretch:80%;color:{OR};width:70px">{i}</span>'
        f'<span style="font:700 50px/1.25 Figtree">{_e(r)}</span></div>' for i, r in enumerate(rows, 1))
    head = f'<h1 style="margin-bottom:40px">{_headline(headline)}</h1>' if headline else ""
    return (f'<div class="s" id="s{n}">{_corners(n)}<div class="txt" style="top:150px">'
            f'<div class="lab">{_e(label)}</div>{head}{items}</div></div>')

def cta_slide(n, image, question, line="Simpan biar nggak lupa. Follow buat fondasi berikutnya.",
              kicker="Giliran kamu", tone="light", top=150, size=96):
    """Slide terakhir (CTA): foto lanjutan cover, full-bleed, dengan pertanyaan komentar di atasnya.

    image: path relatif dari slides.html, misalnya "assets/cta.png" (digenerate tanpa teks,
    area atas dibiarkan tenang). question: satu pertanyaan soal isi carousel yang bisa dijawab
    dari pengalaman pembaca, dengan *satu* kata oranye. tone: "light" (teks indigo, untuk foto
    terang) atau "dark" (teks putih). Teks rata tengah seperti cover. Kalau kepala di foto
    terlalu tinggi, kecilkan size (minimal 72) dan top, jangan menimpa wajah atau rambut."""
    col = IND if tone == "light" else WH
    return (f'<div class="s" id="s{n}" style="background:#ccc url(\'{_e(image)}\') center/cover no-repeat;color:{col}">'
            f'{_corners(n, last=True)}'
            f'<div class="txt" style="top:{top}px;text-align:center">'
            f'<div class="lab" style="font-size:{round(size*.62)}px;margin-bottom:{round(size*.12)}px">{_e(kicker)}</div>'
            f'<h1 style="font-size:{size}px">{_headline(question)}</h1>'
            f'<div style="font:500 {round(size*.4)}px/1.35 Figtree;margin-top:{round(size*.25)}px">{_e(line)}</div></div></div>')

def image_slide(n, label, headline, body, graphic, last=False, bridge=None):
    """Tipe 1: teks di atas, grafis penuh di separuh bawah, latar gradien."""
    return (f'<div class="s grad" id="s{n}">{_corners(n, last)}'
            f'<div class="txt" style="top:150px"><div class="lab">{_e(label)}</div><h1>{_headline(headline)}</h1>'
            f'<div class="body">{_e(body)}</div></div>{graphic}{_bridge(bridge)}</div>')

# ---------- layout dinamis ----------
#
# Grafis digambar di atas "panggung" (stage) dengan koordinatnya sendiri:
#   lebar  = 1080 x 640   (cocok untuk kartu berjajar, bubble, kolom ketik)
#   tinggi = 520 x 1100   (cocok untuk tumpukan sticky note, daftar ke bawah)
#   kotak  = 900 x 900
# Komposisi menentukan di mana panggung dan teks diletakkan. Panggung diskalakan
# agar pas di zonanya. Ukuran judul dan body menyesuaikan panjang teks (auto-fit).

STAGES = {"lebar": (1080, 640), "tinggi": (520, 1100), "kotak": (900, 900)}

# zone = (x, y, w, h) untuk grafis; text = (x, y, w, h) kotak teks; panel = latar zona
COMPOSITIONS = {
    "atas":          {"zone": (0, 0, 1080, 640),    "text": (64, 690, 952, 560),  "panel": True,  "grad": False, "hmax": 104, "valign": "start"},
    "bawah":         {"zone": (0, 690, 1080, 660),  "text": (64, 140, 952, 520),  "panel": False, "grad": True,  "hmax": 104, "valign": "start"},
    "tengah":        {"zone": (0, 470, 1080, 560),  "text": (64, 140, 952, 310),  "panel": False, "grad": False, "hmax": 96,  "valign": "start",
                      "body_box": (64, 1030, 952, 150)},
    "samping_kanan": {"zone": (560, 0, 520, 1350),  "text": (64, 160, 452, 1050), "panel": True,  "grad": False, "hmax": 92,  "valign": "center"},
    "samping_kiri":  {"zone": (0, 0, 520, 1350),    "text": (584, 160, 432, 1050), "panel": True, "grad": False, "hmax": 92,  "valign": "center"},
    "kotak":         {"zone": (90, 100, 900, 780),  "text": (64, 900, 952, 350),  "panel": False, "grad": True,  "hmax": 92,  "valign": "start"},
}
OPTIONS = {"lebar": ["atas", "bawah", "tengah"], "tinggi": ["samping_kanan", "samping_kiri"], "kotak": ["kotak"]}

FIT_JS = """
<script>
window.__fitDone = false;
document.fonts.ready.then(() => {
  document.querySelectorAll('[data-fit-box]').forEach(box => {
    const h = box.querySelector('h1'), b = box.querySelector('.body') || document.querySelector(box.dataset.bodyRef || '#none');
    let hs = +h.dataset.max, bs = b ? +b.dataset.max : 0;
    const hmin = +h.dataset.min, bmin = b ? +b.dataset.min : 0;
    const set = () => { h.style.fontSize = hs + 'px'; if (b) b.style.fontSize = bs + 'px'; };
    const over = () => box.scrollHeight > box.clientHeight + 1 || h.scrollWidth > h.clientWidth + 1 ||
                       (b && b.closest('[data-fit-body]') && b.scrollHeight > b.closest('[data-fit-body]').clientHeight + 1);
    set();
    for (let k = 0; k < 200 && over(); k++) {
      if (hs > hmin) hs -= 4; else if (b && bs > bmin) bs -= 2; else break;
      set();
    }
  });
  window.__fitDone = true;
});
</script>
"""

def _words(t):
    return len((t or "").replace("*", "").split())

def slide(n, label, headline, body, graphic=None, aspect="lebar", layout="auto", role=None, bridge=None, last=False):
    """Satu slide isi dengan layout dinamis. graphic digambar di koordinat panggung `aspect`.
    layout="auto" dipilih oleh build(); atau isi salah satu nama di COMPOSITIONS.
    role: "hook" (slide 2), "payoff" (Coba hari ini), atau None."""
    return {"n": n, "label": label, "headline": headline, "body": body, "graphic": graphic or "",
            "aspect": aspect, "layout": layout, "role": role, "bridge": bridge, "last": last}

def choose_layouts(items):
    """Pilih komposisi otomatis dari isi:
    - aspek grafis menentukan pilihan (lebar, tinggi, kotak);
    - slide hook dan payoff memakai "bawah" (slide gambar) bila grafisnya lebar;
    - teks panjang (lebih dari 20 kata) memakai komposisi dengan ruang teks terbesar;
    - komposisi tidak sama dengan slide sebelumnya, "bawah" tidak dua kali berurutan,
      dan sisi samping bergantian kiri dan kanan."""
    prev = None
    for it in items:
        if not isinstance(it, dict):
            prev = "lain"; continue
        if it["layout"] != "auto":
            prev = it["layout"]; continue
        opts = list(OPTIONS[it["aspect"]])
        long_text = _words(it["headline"]) + _words(it["body"]) > 20
        if it["aspect"] == "lebar":
            if it["role"] in ("hook", "payoff"):
                opts = ["bawah", "atas", "tengah"]
            elif long_text:
                opts = ["atas", "bawah", "tengah"]
            else:
                opts = ["tengah", "atas", "bawah"]
        pick = next((o for o in opts if o != prev), opts[0])
        it["layout"] = pick
        prev = pick
    return items

def _stage(graphic, aspect, zone):
    W, H = STAGES[aspect]
    zx, zy, zw, zh = zone
    k = min(zw / W, zh / H, 1.1)
    ox, oy = (zw - W * k) / 2, (zh - H * k) / 2
    return (f'<div style="position:absolute;left:{ox:.0f}px;top:{oy:.0f}px;width:{W}px;height:{H}px;'
            f'transform:scale({k:.4f});transform-origin:0 0">{graphic}</div>')

def render(it):
    if not isinstance(it, dict):
        return it
    c = COMPOSITIONS[it["layout"]]
    zx, zy, zw, zh = c["zone"]
    tx, ty, tw, th = c["text"]
    panel = f"background:{LIFT};" if c["panel"] else ""
    zone = (f'<div style="position:absolute;left:{zx}px;top:{zy}px;width:{zw}px;height:{zh}px;overflow:hidden;{panel}">'
            f'{_stage(it["graphic"], it["aspect"], c["zone"])}</div>')
    # judul pendek boleh tampil lebih besar; auto-fit tetap mengecilkan kalau tidak muat
    w = _words(it["headline"])
    hmax = int(c["hmax"] * (1.4 if w <= 3 else 1.2 if w <= 5 else 1.0))
    hmin = 60
    head = (f'<div class="lab">{_e(it["label"])}</div>'
            f'<h1 data-max="{hmax}" data-min="{hmin}">{_headline(it["headline"])}</h1>')
    body = f'<div class="body" data-max="44" data-min="36">{_e(it["body"])}</div>' if it["body"] else ""
    jc = "center" if c["valign"] == "center" else "flex-start"
    box_style = (f'position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;overflow:hidden;'
                 f'display:flex;flex-direction:column;justify-content:{jc}')
    if "body_box" in c and body:
        bx, by, bw, bh = c["body_box"]
        bid = f'b{it["n"]}'
        body_el = body.replace('class="body"', f'class="body" id="{bid}"', 1)
        texts = (f'<div data-fit-box data-body-ref="#{bid}" style="{box_style}">{head}</div>'
                 f'<div data-fit-body style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;overflow:hidden">{body_el}</div>')
    else:
        texts = f'<div data-fit-box style="{box_style}">{head}{body}</div>'
    bridge = ""
    if it["bridge"]:
        bridge = (f'<div style="position:absolute;left:{tx}px;width:{tw}px;bottom:120px;font:500 30px Figtree;'
                  f'opacity:.7">{_e(it["bridge"])} →</div>')
    cls = "s grad" if c["grad"] else "s"
    return f'<div class="{cls}" id="s{it["n"]}" data-layout="{it["layout"]}">{_corners(it["n"], it["last"])}{zone}{texts}{bridge}</div>'

def build(items):
    """Pilih layout otomatis lalu render. items boleh berisi slide() dan HTML jadi (recap_slide, dll.)."""
    return [render(it) for it in choose_layouts(items)]

def page(slides):
    """Gabungkan slide jadi satu HTML. Saat merender ke PNG, tunggu window.__fitDone === true."""
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head>'
            f'<body style="background:#111">{"".join(slides)}{FIT_JS}</body></html>')

# ---------- demo ----------

if __name__ == "__main__":
    # Grafis panggung lebar (1080 x 640)
    g_bubble = (bubble_user("Tolong bantu saya bikin caption promo kopi…", 50, 20, 900, size=52)
                + bubble_ai_typing(380, 340, 760, h=190) + mark_arrow(700, 305, 830, 365, bend=-10) + doodle_plus(1000, 90))
    g_cards = (app_card("ChatGPT", 40, 80, 360, 470, -14) + app_card("Claude", 680, 80, 360, 470, 13)
               + app_card("Gemini", 360, 20, 380, 560, -2, hero=True, check=True, sub="akun sendiri")
               + mark_underline(380, 720, 610))
    g_input = (input_bar("Password saya:", "••••••••", -40, 150, 1160, -3)
               + chip("No. rekening", 80, 390, 2, 44) + chip("Data pelanggan", 440, 420, -2, 44)
               + mark_strike(350, 660, 240, 44))
    # Grafis panggung tinggi (520 x 1100): tumpukan sticky note
    g_stack = (sticky("siapa kamu", "Pemilik warung kopi di Bogor", 30, 120, 440, 280, -6)
               + sticky("tujuannya", "Caption promo buat minggu ini", 60, 430, 420, 260, 4, tone="wh")
               + sticky("gayanya", "Santai, pakai bahasa sehari-hari", 30, 730, 440, 260, -3)
               + mark_arrow(470, 300, 470, 520, bend=40))
    items = [
        slide(2, "Kabar baiknya", "Satu permintaan kecil bikin AI *paham*",
              "Nggak perlu jago teknologi. Cukup tiga langkah ini.", g_bubble, role="hook"),
        slide(3, "Langkah 1 dari 3", "Buka versi gratis yang *resmi*",
              "ChatGPT, Gemini, atau Claude. Daftar pakai akunmu sendiri.", g_cards,
              bridge="Berikutnya: langkah yang paling sering dilewati"),
        slide(4, "Langkah 2 dari 3", "Kasih tahu siapa kamu dan *tujuannya*",
              "Itu namanya konteks: info latar yang cuma kamu yang tahu. Makin jelas konteksnya, makin sedikit AI menebak-nebak, dan makin pas hasilnya buat kamu.",
              g_stack, aspect="tinggi"),
        slide(5, "Jaga datamu", "Jangan *ketik* ini",
              "Anggap obrolanmu bisa dibaca orang lain.", g_input),
        recap_slide(6, ["Buka versi gratis yang resmi", "Kasih tahu siapa kamu dan tujuannya",
                        "Minta AI tanya balik dulu"], headline="Tiga langkah, satu *layar*"),
    ]
    open("demo.html", "w", encoding="utf-8").write(page(build(items)))
    print("ditulis demo.html — render tiap .s (1080x1350) ke PNG setelah window.__fitDone true")

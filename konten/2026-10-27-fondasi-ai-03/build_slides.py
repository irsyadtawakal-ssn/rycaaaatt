"""Render slide isi Fondasi AI #3 · Minta AI tanya balik dulu. Dijalankan dari folder root project:

    py konten/2026-10-27-fondasi-ai-03/build_slides.py
    node lib/render.mjs konten/2026-10-27-fondasi-ai-03/slides.html konten/2026-10-27-fondasi-ai-03/output konten/2026-10-27-fondasi-ai-03/output/cover.png

Rencana: 4-slide-plan.md. Slide tanda tanya, blok warna, dan blok prompt belum ada di
lib/slides.py, jadi ditulis di sini sebagai HTML jadi (sama seperti Fondasi AI #2).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "lib"))
from slides import *  # noqa: E402,F401
from slides import _corners, _bridge, _e, _headline  # noqa: E402

# Ruang untuk jembatan: kotak teks berhenti di atas garis jembatan (bottom 120 px).
import slides as _lib  # noqa: E402
_lib.COMPOSITIONS["atas"]["text"] = (64, 690, 952, 480)

BRICO = "font-family:'Bricolage Grotesque';font-weight:800;font-stretch:80%"


# ---------- tipe slide di luar layout dinamis ----------

def question_slide(n, label, headline, body, bridge=None):
    """Tipe 3: tanda tanya oranye raksasa keluar dari tepi kiri, teks di bawahnya."""
    return (f'<div class="s" id="s{n}">{_corners(n)}'
            f'<div style="position:absolute;left:10px;top:90px;{BRICO};font-size:560px;line-height:1;color:{OR}">?</div>'
            f'<div class="txt" style="top:690px"><div class="lab">{_e(label)}</div><h1>{_headline(headline)}</h1>'
            f'<div class="body">{_e(body)}</div></div>{_bridge(bridge)}</div>')


def colour_block_slide(n, term, headline, body):
    """Tipe 4: blok oranye berisi istilah (Deep Indigo), lalu "=" oranye dan perumpamaannya."""
    corners = (f'<div class="corner tl" style="color:{IND}">@irsyadtawakal</div>'
               f'<div class="corner tr" style="color:{IND}">{n}</div><div class="corner br">Geser →</div>')
    return (f'<div class="s" id="s{n}">{corners}'
            f'<div style="position:absolute;left:0;top:0;width:1080px;height:520px;background:{OR}"></div>'
            f'<div style="position:absolute;left:64px;right:64px;top:300px;{BRICO};font-size:150px;line-height:.9;'
            f'color:{IND}">{_e(term)}</div>'
            f'<div class="txt" style="top:540px"><div style="{BRICO};font-size:170px;line-height:1;color:{OR}">=</div>'
            f'<h1 style="font-size:92px">{_headline(headline)}</h1>'
            f'<div class="body" style="font-size:38px;margin-top:26px">{_e(body)}</div></div></div>')


def prompt_slide(n, label, headline, earlier, newest):
    """Tipe 3 payoff: blok prompt teks polos. Kalimat lama 45%, kalimat terbaru dengan bar oranye 6 px dan caret."""
    return (f'<div class="s" id="s{n}">{_corners(n)}<div class="txt" style="top:150px">'
            f'<div class="lab">{_e(label)}</div><h1>{_headline(headline)}</h1>'
            f'<div style="margin-top:70px;font:500 42px/1.45 Figtree">'
            f'<div style="opacity:.45">{_e(earlier)}</div>'
            f'<div style="margin-top:26px;border-left:6px solid {OR};padding-left:30px">{_e(newest)}'
            f'<span style="display:inline-block;width:5px;height:50px;background:{WH};margin-left:8px;'
            f'vertical-align:-8px"></span></div></div></div></div>')


# ---------- grafis (koordinat panggung) ----------

# Slide 2 · lebar: bubble kamu dan bubble AI tukar posisi
g2 = (bubble_ai_typing(80, 50, 460, h=170, rot=-4)
      + bubble_user("Bikinin caption promo kopi susu", 400, 250, 620, rot=4, size=50)
      + mark_arrow(620, 260, 470, 140, bend=-70))

UL_X0, UL_X1, UL_Y = 270, 605, 300

# Slide 5 · lebar: AI belum menjawab, dia menyiapkan pertanyaan (tanpa isi karangan)
g5 = (bubble_user("Bikinin caption promo. Sebelum jawab, tanya saya dulu.", 70, 110, 900, rot=-3, size=46)
      + bubble_ai_typing(560, 430, 400, h=150, rot=5)
      + chip("?", 430, 440, -10, 48) + chip("?", 990, 400, 8, 48) + chip("?", 980, 560, -6, 48)
      + mark_underline(UL_X0, UL_X1, UL_Y)
      + doodle_plus(120, 540))


ITEMS = [
    slide(2, "Udah kasih konteks, tapi hasil AI masih meleset?", "Coba balik *posisinya*.",
          "Nggak perlu nulis prompt panjang.", g2, role="hook"),
    question_slide(3, "Masalahnya", "Kamu bingung harus cerita *apa*.",
                   "Episode kemarin bilang, kasih AI konteks. Masalahnya, kamu sering nggak tahu bagian mana yang dia butuh.",
                   bridge="Tukang cukur udah lama punya jawabannya."),
    colour_block_slide(4, "Tukang cukur", "Dia *nanya* dulu sebelum motong.",
                       "Mau model apa, tipis atau pendek. Kamu tinggal jawab, dan hasilnya pas."),
    slide(5, "Cara kerjanya", "Balik posisinya, AI yang *nanya*.",
          "Biasanya kamu yang mikir harus cerita apa. Sekarang suruh dia nanya dulu, kamu tinggal jawab. "
          "Paling kepake buat tugas yang banyak pilihannya, kayak caption atau email.",
          g5, bridge="Kalimatnya cuma satu. Geser."),
    recap_slide(6, ["Bingung cerita apa itu wajar", "Tukang cukur nanya dulu",
                    "Biar AI yang nanya, kamu jawab", "Pakai buat tugas yang banyak pilihannya"],
                headline="Simpan yang *ini*."),
    prompt_slide(7, "Coba hari ini", "Tempel di akhir *permintaanmu*.",
                 "[Permintaanmu, misalnya: Bikinin caption promo kopi susu.]",
                 "Sebelum jawab, tanya saya dulu apa aja yang kamu perlu tahu biar hasilnya pas. Maksimal lima pertanyaan."),
    cta_slide(8, "assets/cta.png", "Tugas apa yang hasil AI-nya paling sering *meleset*?", tone="dark", top=130),
]

if __name__ == "__main__":
    out = HERE / "slides.html"
    out.write_text(page(build(ITEMS)), encoding="utf-8")
    print("ditulis", out)

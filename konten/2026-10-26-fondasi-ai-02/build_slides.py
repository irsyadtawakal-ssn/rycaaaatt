"""Render slide isi Fondasi AI #2 · Kenapa AI bisa jawab ngasal. Dijalankan dari folder root project:

    py konten/2026-10-26-fondasi-ai-02/build_slides.py
    node lib/render.mjs konten/2026-10-26-fondasi-ai-02/slides.html konten/2026-10-26-fondasi-ai-02/output konten/2026-10-26-fondasi-ai-02/output/cover.png

Rencana: 4-slide-plan.md. Slide jeda, blok warna, tiga baris, dan blok prompt belum ada di
lib/slides.py, jadi ditulis di sini sebagai HTML jadi.
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
_lib.COMPOSITIONS["kotak"].update(zone=(90, 100, 900, 690), text=(64, 820, 952, 330))

BRICO = "font-family:'Bricolage Grotesque';font-weight:800;font-stretch:80%"


# ---------- objek tambahan (gaya sama dengan pustaka) ----------

def typed_bar(text, x, y, w, rot=-3):
    """Kolom ketik berisi kalimat yang sedang diketik, dengan caret. Hero: putih solid."""
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);'
            f'height:150px;border-radius:75px;background:{WH};color:{IND};display:flex;align-items:center;'
            f'padding:0 56px;gap:10px;font:700 54px Figtree">{_e(text)}'
            f'<span style="width:5px;height:60px;background:{IND};display:inline-block"></span></div>')


def sticky_ghost(label, text, x, y, w, h, rot=-6):
    """Sticky note pendukung: putih 24% dengan garis putih 3 px."""
    return (f'<div class="o" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);'
            f'background:rgba(255,255,255,.24);border:3px solid rgba(255,255,255,.7);border-radius:28px;padding:40px">'
            f'<div style="font:500 26px Figtree;opacity:.75">{_e(label)}</div>'
            f'<div style="font:700 40px/1.2 Figtree;margin-top:14px">{_e(text)}</div></div>')


def doodle_tick(x, y, s=56):
    return (f'<svg class="mk" width="1080" height="1350"><path d="M{x} {y} l{s*.35:.0f} {s*.35:.0f} l{s*.65:.0f} {-s*.7:.0f}" '
            f'fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------- tipe slide di luar layout dinamis ----------

def pause_slide(n, label, myth, fact, body, bridge=None):
    """Tipe 5: off-white, mitos dicoret 40%, fakta dengan satu kata oranye besar."""
    return (f'<div class="s" id="s{n}" style="background:{PW};color:{IND}">{_corners(n)}'
            f'<div class="txt" style="top:300px"><div class="lab">{_e(label)}</div>'
            f'<div style="{BRICO};font-size:84px;line-height:1;opacity:.4;text-decoration:line-through;'
            f'text-decoration-thickness:7px;margin-bottom:56px">{_e(myth)}</div>'
            f'<h1 style="font-size:124px;line-height:.95">{_headline(fact)}</h1>'
            f'<div class="body" style="font-size:42px">{_e(body)}</div></div>{_bridge(bridge)}</div>')


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


def rows_slide(n, label, headline, body, rows, note=None):
    """Tipe 3: tiga baris dengan pembatas putih 15%."""
    items = "".join(
        f'<div style="padding:34px 0;border-top:2px solid rgba(255,255,255,.15)">'
        f'<div style="font:700 56px/1.1 Figtree">{_e(t)}</div>'
        f'<div style="font:400 38px/1.35 Figtree;opacity:.8;margin-top:8px">{_e(d)}</div></div>' for t, d in rows)
    foot = f'<div style="font:500 28px Figtree;opacity:.6;margin-top:22px">{_e(note)}</div>' if note else ""
    return (f'<div class="s" id="s{n}">{_corners(n)}<div class="txt" style="top:140px">'
            f'<div class="lab">{_e(label)}</div><h1>{_headline(headline)}</h1>'
            f'<div class="body" style="margin:22px 0 40px">{_e(body)}</div>{items}{foot}</div></div>')


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

# Slide 2 · lebar: chat pertama yang terlalu pendek, AI mulai nebak
g2 = (bubble_user("Bikinin caption promo dong", 70, 60, 680, rot=-5, size=54)
      + bubble_ai_typing(470, 380, 520, h=170, rot=4)
      + mark_arrow(990, 70, 800, 170, bend=-40))

# Slide 5 · lebar: saran kata seperti keyboard HP
g5 = (typed_bar("Kopi susu gula", 70, 90, 860, rot=-3)
      + chip("aren", 130, 350, -4, 50) + chip("batu", 470, 380, 3, 50) + chip("merah", 840, 345, 6, 50)
      + mark_loop(242, 420, 165, 100)
      + doodle_plus(1010, 245))

# Slide 7 · kotak: dua catatan yang ditempel di awal chat
g7 = (sticky_ghost("siapa kamu", "Pemilik warung kopi di Bogor, lagi bikin promo", 40, 60, 540, 360, -7)
      + sticky("kalau nggak yakin", "Bilang aja nggak yakin", 330, 420, 520, 300, 5)
      + mark_underline(385, 785, 625)
      + doodle_tick(760, 110))

# Slide 10 · lebar: AI belum jawab, dia mau nanya dulu
g10 = (bubble_user("Bikinin caption promo buat minggu ini", 60, 30, 780, rot=-4, size=48)
       + bubble_ai_typing(540, 360, 440, h=170, rot=5)
       + mark_loop(760, 445, 280, 125))


ITEMS = [
    slide(2, "Kalau jawaban AI-mu sering meleset,", "Yang kurang ada di *chat* pertamamu.",
          "Dan itu gampang dibenerin.", g2, role="hook"),
    pause_slide(3, "Yang sering dikira", "AI lagi bohongin kamu.", "Dia nggak tahu jawabannya *salah*.",
                "Kerjanya cuma nerusin kalimat.", bridge='Terus, kenapa dia nggak bilang "nggak tahu" aja?'),
    colour_block_slide(4, "AI tanpa konteks", "Kayak teman pinter yang *gengsi* ngaku nggak tahu.",
                       "Ditanya apa aja, pasti dijawab. Kalau kamu nggak cerita situasinya, "
                       "bagian yang kosong dia isi pakai tebakan."),
    slide(5, "Cara kerjanya", "Mirip saran kata di *keyboard* HP.",
          "Waktu kamu ngetik, HP nyodorin kata yang biasanya muncul berikutnya. AI juga begitu, cuma jauh "
          "lebih pinter. Dia pilih kata yang paling nyambung, belum tentu yang benar. Kalau tebakannya "
          "meleset tapi kedengeran yakin, itu yang disebut halusinasi.",
          g5, bridge="Ada tiga hal yang paling sering dia salah tebak."),
    rows_slide(6, "Rawan ngasal", "Paling sering *meleset* di sini.",
               "Hal yang jarang ada di bahan belajarnya, susah dia tebak.",
               [("Nama", "Orang atau tempat yang jarang dibahas"),
                ("Tanggal", "Misalnya ulang tahun seseorang"),
                ("Angka", "Misalnya omzet warung tetangga")],
               note="Contoh tanggal ulang tahun dipakai OpenAI sendiri."),
    slide(7, "Biar nggak ngasal", "Kasih dia *dua* hal.",
          "Pertama, ceritain kamu siapa dan lagi ngerjain apa. Kedua, bilang ke dia: kalau nggak yakin, ngaku aja.",
          g7, aspect="kotak", bridge="Geser, ada rangkumannya."),
    recap_slide(8, ["AI milih kata yang paling nyambung", "Nggak dikasih konteks, dia nebak",
                    "Paling sering salah: nama, tanggal, angka", "Ceritain situasimu, suruh ngaku kalau nggak yakin"],
                headline="Simpan yang *ini*."),
    prompt_slide(9, "Coba hari ini", "Tempel ini di awal *chat* kamu.",
                 "Saya [kerjaanmu], lagi [ngerjain apa]. Saya mau [hasil yang kamu mau].",
                 "Kalau kamu nggak yakin soal nama, tanggal, atau angka, bilang aja nggak yakin. Jangan nebak."),
    slide(10, "Besok sore · Fondasi AI #3", "Satu kalimat biar AI *nanya* dulu.",
          "Sebelum dia jawab apa pun.", g10, last=True),
]

if __name__ == "__main__":
    out = HERE / "slides.html"
    out.write_text(page(build(ITEMS)), encoding="utf-8")
    print("ditulis", out)

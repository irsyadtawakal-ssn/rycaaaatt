"""Render slide isi untuk post ini. Dijalankan dari folder root project:

    py konten/<folder-post>/build_slides.py
    node lib/render.mjs konten/<folder-post>/slides.html konten/<folder-post>/output konten/<folder-post>/output/cover.png

Claude menulis ulang bagian ITEMS sesuai 4-slide-plan.md.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "lib"))
from slides import *  # noqa: E402,F401

LOGO = ROOT / "assets" / "logos"   # contoh: app_card("ChatGPT", ..., logo=(LOGO / "chatgpt.png").as_uri())

ITEMS = [
    slide(2, "Kabar baiknya", "Contoh judul dengan satu kata *oranye*",
          "Ganti isi ini sesuai rencana slide.",
          bubble_user("Contoh pesan kamu…", 40, 70, 860) + bubble_ai_typing(420, 330, 620),
          role="hook"),
    recap_slide(3, ["Poin pertama", "Poin kedua", "Poin ketiga"], headline="Contekan *singkat*"),
]

if __name__ == "__main__":
    out = HERE / "slides.html"
    out.write_text(page(build(ITEMS)), encoding="utf-8")
    print("ditulis", out)

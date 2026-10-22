"""Shared text helpers for the lib/ig scripts (Indonesian-aware).

Adapted from ideas in Jake Schincariol's instagram-agent-skill (MIT),
rewritten for Indonesian. See lib/ig/LICENSE-instagram-agent-skill.txt.
"""

import re
import sys
import unicodedata


# Windows consoles often default to a legacy code page; print Indonesian text, emoji and box characters safely.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Words: any run of letters or digits, so Indonesian (and names) count correctly.
WORD_RE = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*", re.UNICODE)

# Something checkable: a number, a price, a percentage, or a capitalised name/tool
# that is not the first word of a sentence.
CONCRETE_RE = re.compile(
    r"\bRp\s?\d[\d.,]*|\b\d[\d.,]*\s?(?:%|x|×|jt|juta|rb|ribu|detik|menit|jam|hari|minggu|bulan|tahun)?\b"
    r"|(?<![.!?]\s)(?<!^)\b[A-Z][A-Za-z]{2,}\b"
    r"|(?i:\b(?:satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|seratus|seribu|sejuta|setengah)\b"
    r"|\b\w+\s(?:belas|puluh|ratus|ribu|juta)\b)",
    re.MULTILINE,
)

# Common Indonesian function words, ignored when looking for a loop word.
STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "aja", "saja", "juga", "ya", "yaa",
    "nah", "oke", "jadi", "kalau", "kalo", "kamu", "saya", "aku", "kita", "kami", "dia",
    "mereka", "ada", "tidak", "nggak", "ngga", "gak", "ga", "bukan", "tapi", "tetapi",
    "atau", "untuk", "buat", "dengan", "sama", "pada", "dalam", "akan", "bisa", "udah",
    "sudah", "belum", "lagi", "terus", "lalu", "karena", "soalnya", "biar", "supaya",
    "agar", "kayak", "seperti", "banget", "sih", "deh", "kok", "loh", "lho", "dong",
    "kan", "pun", "lah", "kah", "apa", "gimana", "bagaimana", "kenapa", "mana", "siapa",
    "satu", "cuma", "hanya", "lebih", "paling", "masih", "baru", "the", "a", "an",
}

# Invisible and look-alike characters that survive copy-paste from AI tools.
INVISIBLE = {
    "​": "zero-width space", "‌": "zero-width non-joiner",
    "‍": "zero-width joiner", "⁠": "word joiner", "﻿": "byte-order mark",
    "­": "soft hyphen", "⁡": "invisible function", "⁢": "invisible times",
    "⁣": "invisible separator", "⁤": "invisible plus", "᠎": "mongolian vowel separator",
}
SPACES = {" ": "non-breaking space", " ": "narrow no-break space",
          " ": "figure space", " ": "thin space", " ": "hair space"}


def words(text):
    return WORD_RE.findall(text)


def syllables(word):
    """Approximate Indonesian syllables: one per vowel group, with ai/au/oi/ei as one.

    Indonesian spelling is close to phonetic, so vowel groups are a fair count.
    Digits are spelled out roughly (each digit about two syllables).
    """
    w = word.lower()
    if w.isdigit():
        return max(1, len(w) * 2)
    w = re.sub(r"(ai|au|oi|ei)", "a", w)
    n = len(re.findall(r"[aiueoéy]+", w))
    return max(1, n)


def count_syllables(text):
    return sum(syllables(w) for w in words(text))


def content_words(text):
    return {w.lower() for w in words(text) if w.lower() not in STOPWORDS and len(w) > 2}


def is_tag_char(ch):
    return 0xE0000 <= ord(ch) <= 0xE007F


def _is_emoji_side(ch):
    return bool(ch) and (ord(ch) > 0xFFFF or ch == "️" or 0x2600 <= ord(ch) <= 0x27BF)


def invisible_spans(text):
    """List (index, name, kind) for each invisible or odd-space character.

    kind is "remove" or "space". A zero-width joiner between two emoji parts
    (for example a family or job emoji) is part of the emoji and is kept.
    """
    out = []
    for i, ch in enumerate(text):
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if ch == "‍" and _is_emoji_side(prev) and _is_emoji_side(nxt):
            continue
        if ch in INVISIBLE:
            out.append((i, INVISIBLE[ch], "remove"))
        elif ch in SPACES:
            out.append((i, SPACES[ch], "space"))
        elif is_tag_char(ch):
            out.append((i, "unicode tag character", "remove"))
        elif unicodedata.category(ch) == "Cf" and ch not in "‎‏":
            out.append((i, f"format character U+{ord(ch):04X}", "remove"))
    return out


def find_invisible(text):
    found = {}
    for _, name, _ in invisible_spans(text):
        found[name] = found.get(name, 0) + 1
    return found

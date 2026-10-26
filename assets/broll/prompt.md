# Prompt B-roll kolase: dua opsi

Status: **uji gaya.** Contoh adegan diambil dari contoh hook di Video Brain ("Kebanyakan orang nanya ke ChatGPT kayak nanya ke Google"). Aturan lengkap: Video Brain bagian 5, "B-roll kolase".

- **Opsi A — tanpa wajah:** hanya benda. Bisa dibuat sekarang.
- **Opsi B — dengan wajah:** Irsyad sebagai tokoh potongan. Butuh 2–3 foto asli di folder `assets/foto-irsyad/`, dilampirkan manual di ChatGPT/Gemini.

## Cara pakai

1. Satu prompt = satu gambar. Paste JSON-nya ke ChatGPT Image atau Nano Banana, ukuran **potret 2:3**.
2. Opsi B: lampirkan 2–3 foto (depan, tiga perempat) **sebelum** paste prompt.
3. Latar putih polos. Di ChatGPT boleh tambahkan "transparent background"; kalau tidak, latarnya dihapus belakangan.
4. Simpan hasilnya di folder ini dengan nama file yang tertulis (mis. `broll-01-a.png`).
5. Generate ulang kalau muncul teks, logo, warna selain satu oranye, latar ruangan, atau (opsi B) wajah yang tidak mirip.
6. Kertas grid, teks kata per kata, dan gerakan ditambahkan di kode (HyperFrames/Remotion), bukan di gambar.

| No | Momen di video | Opsi A (tanpa wajah) | Opsi B (dengan wajah) |
| --- | --- | --- | --- |
| 01 | Intensify: ngulang prompt lima kali | Tumpukan lima bubble chat kertas yang diremas | Irsyad memijat dahi, memegang bubble yang diremas |
| 02 | Set-up 1: nanya kayak ke Google | Kaca pembesar di atas kolom chat kosong | Irsyad mengintip lewat kaca pembesar ke kolom chat kosong |
| 03 | Set-up 2: kasih konteks | Nota panjang menjulur dari bubble chat | Irsyad menyodorkan nota pesanan yang panjang ke kamera |

Satu-satunya warna di semua gambar: oranye #EF5F18 pada satu benda.

---

## 01. Intensify: "saya ngulang prompt lima kali"

**broll-01-a.png** (opsi A, tanpa wajah)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of five crumpled paper speech bubbles (like chat bubbles cut from paper) piled on top of each other, each one crushed into a ball except the top one which is half-unfolded. The only colour in the image is the top bubble's edge, Signal Orange #EF5F18; everything else is strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "a small pile of five crumpled paper chat bubbles",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "static, the top bubble half-unfolded"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "materials": {
      "surfaces": "matte office paper with deep creases, torn fibres at the folds"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "paper creases and fibres",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange edge only",
        "magazine collage feel",
        "soft contact shadow",
        "tactile paper",
        "clean white margin"
      ],
      "avoid": [
        "more or fewer than five bubbles",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

**broll-01-b.png** (opsi B, dengan wajah — lampirkan foto)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of the person, waist-up, rubbing their forehead with one hand in tired frustration while holding a crumpled paper chat bubble in the other hand. The only colour in the image is the crumpled bubble, Signal Orange #EF5F18; the person and their clothes are strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "the person from the reference photos holding a crumpled paper chat bubble",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "rubbing the forehead, mid-sigh"
    },
    "person": {
      "identity": "The same person from the attached reference photos. Keep their face, facial structure, skin tone, hairstyle and body proportions exactly the same. Do not beautify, slim or change their age.",
      "expression": "tired frustration: eyes half-closed, brows pulled together, mouth in a small exhale",
      "gaze": "down at the crumpled bubble in the hand",
      "pose_gesture": "waist-up, one hand rubbing the forehead, the other hand holding the crumpled bubble at chest height",
      "framing": "waist-up, face about one fifth of the frame height, upper third",
      "wardrobe": "plain crew-neck t-shirt, no logo",
      "interaction": "holds the orange bubble, which is the only colour"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "genuine tired frustration",
        "readable face at small size",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange prop only",
        "film grain",
        "natural skin texture",
        "magazine collage feel"
      ],
      "avoid": [
        "a different-looking face",
        "beautified or airbrushed skin",
        "changed age",
        "changed facial structure",
        "extra fingers or warped hands",
        "stiff posed smile",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

---

## 02. Set-up 1: "nanya ke ChatGPT kayak nanya ke Google" (satu kata)

**broll-02-a.png** (opsi A, tanpa wajah)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of a vintage brass magnifying glass held over a long, empty chat message input bar (a rounded rectangle text field with a small send-arrow button, made of white card paper). The input bar is completely empty. The only colour in the image is the send-arrow button, Signal Orange #EF5F18; everything else is strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "a magnifying glass over an empty chat input bar made of paper",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "static, the lens magnifies the empty field"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "materials": {
      "surfaces": "matte white card for the input bar, aged brass handle",
      "transparency": "realistic lens refraction magnifying the empty field"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "empty input field",
        "glass refraction",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange button only",
        "paper card texture",
        "magazine collage feel",
        "soft contact shadow"
      ],
      "avoid": [
        "text inside the input bar",
        "a search engine logo or search page",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

**broll-02-b.png** (opsi B, dengan wajah — lampirkan foto)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of the person, waist-up, holding a large vintage magnifying glass up to a long, empty chat message input bar made of white card paper that floats beside them, peering through it with a puzzled look. The only colour in the image is the input bar's small send-arrow button, Signal Orange #EF5F18; the person and everything else are strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "the person from the reference photos peering through a magnifying glass at an empty chat input bar",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "peering, caught mid-movement while leaning in"
    },
    "person": {
      "identity": "The same person from the attached reference photos. Keep their face, facial structure, skin tone, hairstyle and body proportions exactly the same. Do not beautify, slim or change their age.",
      "expression": "puzzled: one eyebrow raised, head tilted, lips pressed to one side",
      "gaze": "through the lens at the empty input bar, leading the viewer to it",
      "pose_gesture": "waist-up, leaning in, one hand holding the magnifying glass at eye level",
      "framing": "waist-up, face about one fifth of the frame height",
      "wardrobe": "plain crew-neck t-shirt, no logo",
      "interaction": "the input bar floats at chest height to the right, the lens between the eye and the bar"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "materials": {
      "transparency": "realistic lens refraction"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "puzzled curiosity",
        "readable face at small size",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange button only",
        "glass refraction",
        "film grain",
        "magazine collage feel"
      ],
      "avoid": [
        "a different-looking face",
        "beautified or airbrushed skin",
        "changed age",
        "changed facial structure",
        "extra fingers or warped hands",
        "stiff posed smile",
        "text inside the input bar",
        "a search engine logo or search page",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

---

## 03. Set-up 2: "kasih konteks" (seperti pesan lengkap ke penjual warung)

**broll-03-a.png** (opsi A, tanpa wajah)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of a long paper receipt-style note unrolling out of a paper chat bubble and curling down onto the ground, like an order list that is much longer than expected. The note has only faint grey lines suggesting handwriting, no readable words. The only colour in the image is a paperclip on the bubble, Signal Orange #EF5F18; everything else is strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "a long receipt-like note unrolling from a paper chat bubble",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "static, the note curling down in a loose spiral"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "materials": {
      "surfaces": "thin thermal receipt paper with a slight curl, matte card for the bubble, a small metal paperclip"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "long curling paper",
        "faint grey line marks",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange paperclip only",
        "thermal-paper texture",
        "magazine collage feel",
        "soft contact shadow"
      ],
      "avoid": [
        "readable handwriting or words on the note",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

**broll-03-b.png** (opsi B, dengan wajah — lampirkan foto)

```json
{
  "prompt": {
    "scene": {
      "description": "Black-and-white editorial cut-out photo of the person, waist-up, confidently holding out a very long paper receipt-style order note that unrolls from their hand down past the bottom of the frame, like handing a detailed order to a food stall. The note has only faint grey lines suggesting handwriting, no readable words. The only colour in the image is a paperclip on the note, Signal Orange #EF5F18; the person and everything else are strict greyscale. isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly.",
      "subject": "the person from the reference photos holding out a long unrolling order note",
      "setting": "isolated on a plain pure white background (#FFFFFF), nothing else in the frame, generous empty margin around the subject so it can be cut out cleanly",
      "action": "holding the note out toward the viewer, caught mid-gesture"
    },
    "person": {
      "identity": "The same person from the attached reference photos. Keep their face, facial structure, skin tone, hairstyle and body proportions exactly the same. Do not beautify, slim or change their age.",
      "expression": "confident: relaxed half-smile with one corner higher, chin slightly down",
      "gaze": "direct eye contact into the lens",
      "pose_gesture": "waist-up, one arm extended holding the top of the note, the note unrolling down",
      "framing": "waist-up, face about one fifth of the frame height",
      "wardrobe": "plain crew-neck t-shirt, no logo",
      "interaction": "the orange paperclip sits at the top of the note near the hand"
    },
    "style": {
      "primary": "editorial black-and-white photo collage cut-out, like a single photo cut from a magazine with scissors",
      "rendering_quality": "detailed, high-resolution",
      "surface_textures": "fine film grain, slightly matte newsprint-like tones, true greyscale",
      "lighting": "soft studio key light from upper left at about 40 degrees, gentle fill, one soft contact shadow under the object only"
    },
    "technical": {
      "camera": {
        "focal_length": "70mm",
        "aperture": "f/8",
        "depth_of_field": "deep, the whole object sharp",
        "angle": "eye level, slightly from above"
      },
      "resolution": "high definition, portrait 2:3 (1024 x 1536)",
      "rendering": "monochrome, rich blacks, clean whites, no colour cast"
    },
    "composition": {
      "perspective": "flat collage feel, single subject, no environment",
      "framing": "centered",
      "subject_placement": "subject centred, filling about 70% of the frame height"
    },
    "quality": {
      "include": [
        "confident half-smile",
        "readable face at small size",
        "long curling paper",
        "crisp cut-out silhouette",
        "true greyscale",
        "one orange paperclip only",
        "film grain",
        "magazine collage feel"
      ],
      "avoid": [
        "a different-looking face",
        "beautified or airbrushed skin",
        "changed age",
        "changed facial structure",
        "extra fingers or warped hands",
        "stiff posed smile",
        "readable handwriting or words on the note",
        "any colour other than the one orange element",
        "text, letters, numbers, watermarks or logos anywhere",
        "background scenery, horizon, floor or room",
        "neon glow, holograms, robots, glowing brains, circuit patterns",
        "3D cartoon or plastic render look",
        "cropped edges of the object",
        "busy cast shadows"
      ],
      "reference_standard": "editorial cut-out collages in The New Yorker and Bloomberg Businessweek, Dada photomontage"
    }
  }
}
```

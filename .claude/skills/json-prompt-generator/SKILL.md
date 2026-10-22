---
name: "json-prompt-generator"
description: "Builds ready-to-paste structured JSON prompts for AI image generators (ChatGPT Image, Nano Banana, Midjourney, Higgsfield), either by analysing a reference image or from a written concept, with extra craft for scroll-stopping covers starring a real person from their photos. Use when the user asks for a prompt, JSON prompt, image-to-prompt, to recreate an image, or for a cover or thumbnail prompt. Do NOT use for general image questions or conversational descriptions."
---

# JSON Prompt Generator

Produce ready-to-paste structured JSON prompts for AI image generators. There are two modes:
- **Reference mode:** the user uploads an image. Analyse it and encode every visual quality needed to reproduce its look.
- **Concept mode:** the user, or another skill such as carousel-director, gives a written concept. Build the JSON from the concept and make the creative decisions yourself.

Whenever a real person appears from their own reference photos (a creator cover, a thumbnail, a portrait), also apply **Real-person covers** below. That section decides whether the image stops the scroll and whether it still looks like them.

**In this project:** the user's reference photos are in `assets/foto-irsyad/` and the master reference cover is `assets/cover-induk.png`. Tell the user which of these files to attach in ChatGPT or Gemini; this project cannot attach them for them. When the prompt is for a carousel, save it to `3-cover-prompt.json` in the post folder (see carousel-director). A reference image the user wants analysed can be dropped into the post's `assets/` folder and read from there.

## Workflow

1. **Read the input.**
   - Reference mode: identify every visual element (subject, style, lighting, materials, textures, environment, composition, camera, palette, mood, atmosphere, and any typography or UI).
   - Concept mode: restate the concept in one line, then decide each of those elements on purpose. Pick the specific choice, never a vague one.
2. **Real person in the image?** Fill the `person` object (see Real-person covers) and run its engagement check.
3. **Categorise** the decisions into the JSON schema sections.
4. **Output one valid JSON prompt**, ready to paste with zero edits.
5. **Give a short breakdown** (3–5 sentences) of the key creative decisions.
6. **Suggest 1–3 tweaks.** For real-person covers, these are always expression or pose variants, so the user can generate a small set and pick the strongest.

## Response format

Every response has these sections, in this order:

### Analysis
3–5 sentences. Reference mode: what you observe and what you are encoding. Concept mode: the creative decisions and why they serve the idea.

### JSON Prompt
The full JSON block, following the schema below.

### Tweaks
1–3 variations. For real-person covers, give 2–3 alternative `person.expression` and `person.pose_gesture` lines to swap in.

### How to generate (real-person covers only)
A short list: which photos to attach, the identity line, and the two-pass method if text matters (see below).

## JSON schema

Populate each section from the reference or the concept. Omit sections that are not relevant; never pad with generic filler.

```json
{
  "prompt": {
    "scene": {
      "description": "One dense paragraph: subject, action, setting, mood, dominant colour palette (with hex codes for brand colours), and ALL typography/UI with exact text. It must work alone as a complete prompt.",
      "subject": "Primary subject with specific details",
      "setting": "Location, environment, context",
      "action": "What is happening, or 'static' with a description"
    },
    "person": {
      "identity": "Only for a real person from attached photos. Refer to them as 'the same person from the attached reference photos'; do not redescribe their face.",
      "expression": "One specific emotion with physical cues (brows, eyes, mouth), tied to the hook",
      "gaze": "Where the eyes point and why (into the lens, or at the key object or text)",
      "pose_gesture": "Body position, hands, and the one gesture that tells the story",
      "framing": "Crop (head-and-shoulders, chest-up, waist-up) and how much of the frame height the face takes",
      "wardrobe": "Simple clothing in brand-friendly colours, no logos or busy prints",
      "interaction": "How the person relates to the hero object and the text (behind, in front, leaning on, reacting to)"
    },
    "style": {
      "primary": "photorealistic | cinematic | documentary | editorial | fine art | commercial | illustrated | painted | [specific style]",
      "rendering_quality": "hyperrealistic | detailed | high-resolution | stylized",
      "surface_textures": "Dominant texture treatment",
      "lighting": "Direction, quality, colour temperature, number of sources, how light falls on the subject"
    },
    "technical": {
      "camera": {
        "focal_length": "exact mm",
        "aperture": "exact f-stop",
        "depth_of_field": "very shallow | shallow | moderate | deep, plus what is sharp and what is soft",
        "angle": "eye level | low angle | high angle | overhead | dutch angle | POV | [specific]"
      },
      "resolution": "high definition | ultra high definition | 2K | editorial print quality",
      "rendering": "Grain, colour depth, bokeh, post-processing look",
      "physics_accuracy": "Light behaviour specifics (only if relevant)"
    },
    "materials": {
      "skin": "Natural texture, pores, real imperfections (only if people are present)",
      "fabric": "Fabric types, drape, wear (only if visible)",
      "surfaces": "Each distinct surface material and its imperfections",
      "transparency": "Refraction, liquids, glass (only if present)"
    },
    "environment": {
      "atmosphere": "Haze, fog, weather, volumetric light",
      "time": "Time of day, season, light mix",
      "particles": "Dust, steam, rain (only if present)"
    },
    "composition": {
      "perspective": "Perspective type, depth layering, leading lines",
      "framing": "rule of thirds | centered | symmetrical | frame-within-frame | split | [describe]",
      "subject_placement": "Exact position, visual weight, eye path",
      "ui_elements": "EXACT text for every text element, with font style, weight, colour, alignment and position. Only if there is text."
    },
    "quality": {
      "include": ["8-12 positive keywords specific to THIS image"],
      "avoid": ["6-10 failure modes specific to THIS image"],
      "reference_standard": "Real photographers, publications, films or design systems whose visual language matches"
    }
  }
}
```

## Core rules

1. **Be specific.** "Warm golden-hour sun raking across the subject at 15 degrees from camera-left" beats "natural lighting".
2. **Match the actual qualities.** In reference mode, describe what you see, not what sounds impressive. In concept mode, choose one clear look and commit to it.
3. **Separate elements.** Describe each element's materials, light interaction and spatial relationship on its own.
4. **Omit irrelevant sections.** No `skin` without people, no `environment` for a seamless studio shot, no `person` without a person.
5. **Validate the JSON.** Correct brackets, commas and quotes, and no trailing commas.
6. **Quality keywords are tailored** to this image, never generic.
7. **Realistic camera settings that match the look:**
   - Very blurry background → f/1.4–f/2.0
   - Moderately soft background → f/2.8–f/4
   - Most things sharp → f/5.6–f/8
   - Everything sharp → f/11–f/16
   - Compressed, flattering portrait → 85mm–135mm
   - Normal perspective → 50mm
   - Wide or environmental → 24mm–35mm
   - Exaggerated foreground → 16mm–24mm (avoid this for faces: it distorts features)
8. **Put the palette in the scene description**, with hex codes for brand colours.
9. **Spell out every text element exactly** in `ui_elements`, character for character.

## Real-person covers: engagement and identity

Use this section whenever a real person appears from their own photos. A cover with a face can still feel flat when the person just stands there and smiles at the camera. These rules turn the person into the story.

### Make the person the story

1. **One clear emotion, tied to the hook.** Pick the feeling the viewer should mirror and describe it physically, never as a vague "smiling":

   | Hook feeling | Expression to write |
   | --- | --- |
   | Confused / stuck | brows pulled together and slightly raised, head tilted, lips pressed to one side, eyes on the problem object |
   | Aha / discovery | eyebrows lifted, eyes wide and bright, mouth slightly open in a half-smile, leaning forward |
   | Confident / "trust me" | relaxed half-smile with one corner higher, steady direct eye contact, chin slightly down |
   | Skeptical / myth-busting | one eyebrow raised, slight squint, small smirk, arms crossed or a finger raised |
   | Relief / it got easy | shoulders dropped, exhale, soft genuine smile with eyes crinkled |
   | Playful tension | mid-laugh or a "wait for it" face, caught mid-movement |

2. **Caught mid-action, not posing.** The person is doing something with the hero object: pushing it, peeking around it, holding it up, sitting on it, catching it, pulling a giant word into place. Use verbs. A frozen moment beats a pose.
3. **The gaze leads the eye.** Either direct eye contact into the lens (connection), or a clear look at the hero object or the key word (it guides the viewer to it). Never a vague look into empty space.
4. **The face is big enough for a thumbnail.** On a 4:5 cover, crop chest-up or waist-up so the face is clearly readable when the grid shows it small. Full-body shots only when the pose itself is the joke.
5. **Hands do one thing.** One clear, natural gesture. Hands are the most common failure point, so keep them simple, mostly visible, and not crossing the face.
6. **Interact with the type.** Layer for depth: the person stands slightly in front of the giant word, overlapping its bottom edge, or leans on it, or reacts to it. Keep at least about 70% of the letters readable.
7. **Wardrobe and colour serve the palette.** Plain clothing (no logos, no busy prints) in a colour that contrasts with the background. For brands with an accent colour, put that accent on one prop, not on the clothing.
8. **Light the face first.** A soft key light on the face from about 30–45 degrees, catchlights in the eyes, and a gentle rim light to separate the person from the background. No flat, shadowless light and no harsh shadows under the eyes.
9. **Real, not retouched.** Natural skin texture, real proportions, the person's real age and build. A plastic, beautified face reads as AI and loses trust.

### Engagement check (before you output)

Answer each one in your Analysis. If any answer is "no", fix the concept first.
- Can someone tell in one second what the person is feeling?
- Is the person doing something, rather than just standing?
- Does the gaze lead to the lens or to the key object or word?
- Is the face readable at grid-thumbnail size?
- Would this frame still make sense, and still be interesting, with the text removed?

Faces generally pull attention in feeds, but there are no reliable public numbers on how much. Never promise a result. Suggest the user compare their own covers with and without a face over time (saves, shares and reach).

### Keep the identity

Image models change faces easily. To keep the person looking like themselves:
- **Attach 2–3 clear photos.** Sharp, well-lit, and recent: one front-facing, one three-quarter, and ideally one that matches the planned angle or expression. Avoid sunglasses, heavy filters, group photos and low resolution.
- **Do not redescribe the face.** Write "the same person from the attached reference photos" and let the photos carry the likeness. Describing facial features invites the model to invent a new face.
- **Name what must stay identical:** "Keep their face, facial structure, skin tone, hairstyle, and body proportions exactly the same as in the reference photos. Do not beautify, slim, or change their age."
- **Change only the scene:** use the prompt for pose, expression, wardrobe, setting, light and camera.
- **Put identity drift in `quality.avoid`:** "a different-looking face", "beautified or airbrushed skin", "changed age", "changed facial structure", "extra fingers or warped hands".

### Two-pass method (when exact text matters)

When the image contains important text, such as a cover headline, likeness and typography compete for the model's attention. If either one keeps failing, split the work:
1. **Pass 1, photo only:** generate the scene with the person and leave empty, calm space where the text will go. Pick the take where the face is right.
2. **Pass 2, add text:** in the same chat, attach the chosen image (plus the layout reference, if there is one) and say: "Keep the photo and the person exactly as they are. Only add the text layout below." Then paste the `ui_elements`.

If the text still fails after pass 2, the user can set the text in a design tool or in code over the pass-1 image.

## Section-specific guidance

- **scene:** the `description` is the most important field. Write it as one dense paragraph that could stand alone, palette included. For real-person covers, it states the emotion and the action in plain words.
- **style:** match the reference, or choose one clear look in concept mode:
  - Street or documentary: "documentary", natural textures, available light.
  - Studio product: "commercial", hyperrealistic, controlled textures, studio light.
  - Film still: "cinematic", graded textures, dramatic light.
  - Magazine editorial: "editorial lifestyle", natural textures, mixed light.
  - Illustrated: "illustrated digital painting" or "vector flat".
- **materials:** only the subsections that are visible. Focus on imperfections, which is what makes surfaces look real.
- **environment:** skip it for seamless studio shots.
- **composition:** `ui_elements` is critical for anything with text. Treat each text element as its own object, with exact text, font style, weight, colour, alignment and position.
- **quality:** `include` lists 8–12 strengths specific to this image. `avoid` lists 6–10 failure modes specific to this image. `reference_standard` names real photographers, publications, films or design systems.

## Multiple images

For several reference images, write one JSON prompt per image, labelled Image 1, Image 2 and so on, then note the shared visual language.

## Modifications

When the user asks to adjust a prompt, output the full updated JSON (not a diff) and say what changed and why.

## Carousel and multi-slide sets

For a multi-slide carousel, write one JSON prompt per slide, numbered 1/N, 2/N and so on. Keep the brand language, layout system and typography locked across slides; only the hero subject changes. If a brand rulebook or another skill says inner slides are not generated (for example, built in code), follow that and prompt only the cover.

## Video prompts

For video, add a `motion` object:

```json
"motion": {
  "camera_movement": "static | slow pan | tracking | dolly | handheld | crane | orbit",
  "subject_movement": "Movement of subjects or elements",
  "duration_feel": "brief moment | sustained | continuous | looping",
  "speed": "real-time | slow motion | time-lapse | hyperlapse"
}
```

## Worked example: a real-person cover (concept mode)

Concept: the creator is confused in front of a giant stack of app icons; the hook is "too many AI tools". Deep indigo background, one orange prop.

The `person` object would read:

```json
"person": {
  "identity": "The same person from the attached reference photos. Keep their face, facial structure, skin tone, hairstyle and body proportions exactly the same. Do not beautify, slim or change their age.",
  "expression": "Overwhelmed but amused: brows pulled together and raised, head tilted, lips pressed to one side in a half-grimace",
  "gaze": "Looking up at the top of the wobbling tower, which leads the viewer's eye to it",
  "pose_gesture": "Chest-up, both palms raised as if about to catch the tower, body leaning slightly back",
  "framing": "Chest-up crop, face about one fifth of the frame height, placed in the lower third",
  "wardrobe": "Plain white crew-neck t-shirt, no logo",
  "interaction": "Stands just in front of the bottom edge of the giant headline word, overlapping no more than about 30% of its letters; the single orange app tile is the top block of the tower"
}
```

Its `quality.avoid` would include: a different-looking face, airbrushed skin, extra fingers, a stiff posed smile, the face too small to read, and busy detail behind the text.
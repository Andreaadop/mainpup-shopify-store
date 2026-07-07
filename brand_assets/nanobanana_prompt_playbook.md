# Nano Banana Pro Prompt Playbook — MainPup

Distilled from [awesome-nanobanana-pro](./references/awesome-nanobanana-pro/) and adapted for MainPup's Shopify store. Kiwi (poodle × yorkie mix, silver-grey + white, apricot muzzle) is the recurring model. Reference photos live in [brand_assets/models/kiwi/](./models/kiwi/).

Fill in `{{VARIABLES}}` per shot. Every prompt below is meant to be paired with one or more reference images uploaded to Nano Banana Pro.

---

## 1. Kiwi Portrait — Studio Hero Shot

**When to use:** homepage hero, about page, brand story sections.

**Reference to upload:** `_MG_6381.jpg` or `_MG_6357.jpg` (clean studio shots — best facial reference).

```text
A professional, high-resolution portrait of the small silver-grey and white poodle × yorkshire terrier mix from the reference image, maintaining her exact facial structure, coat coloring (silver-grey ears and back, white face and chest, warm apricot tint on the muzzle), and expressive dark eyes. Framed from the chest up, looking directly at the camera. Background: solid {{BRAND_HEX}} studio backdrop. Lighting: soft, diffused studio lighting from above, gentle catchlight in the eyes, subtle rim light separating her coat from the background. Shot on an 85mm f/1.8 lens, shallow depth of field, exquisite focus on the eyes, natural bokeh. Preserve individual strands of her wavy-wiry coat, natural black nose texture, and realistic fur detail. Cinematic color grade with subtle warmth. Editorial, premium, approachable.
```

---

## 2. Product Photography — Clean E-commerce Shot

**When to use:** every product listing page. Isolate the item on white with a natural contact shadow.

**Reference to upload:** raw product photo (messy background, hands, box — doesn't matter).

```text
Identify the main product in the uploaded photo (automatically remove any hands, packaging clutter, or messy background). Recreate it as a premium e-commerce product shot for a Shopify store.

Subject isolation: Cleanly extract the product with pixel-perfect edges.
Background: Pure white studio background (RGB 255, 255, 255) with a subtle, natural contact shadow at the base to ground the object.
Lighting: Soft, even commercial studio lighting to highlight texture and material. No harsh glare, no color casts.
Retouching: Correct any lens distortion, sharpen edges, color-correct so the product looks brand new.
Framing: Centered composition, slight top-down or 3/4 angle depending on best product silhouette. Ample negative space for Shopify's product template.
```

---

## 3. Kiwi With a Product — Lifestyle Studio

**When to use:** hero product images where Kiwi is modeling / interacting with a MainPup item.

**Reference to upload:** (1) Kiwi photo (`_MG_6365.jpg` works — she's mid-carrot-toy already), (2) the product photo.

```text
Using Image 1 (the small silver-grey and white poodle × yorkshire mix — Kiwi) and Image 2 (the product), create a hyper-realistic lifestyle studio photo where Kiwi is naturally interacting with the product ({{holding it in her mouth / wearing it / lying next to it}}).

Fit & interaction: The product must sit naturally against her coat / mouth / body, with realistic shadows, contact points, and any fabric drape conforming to her posture.
High-fidelity preservation: Preserve Kiwi's exact facial features, coat pattern (silver-grey ears/back, white chest, apricot muzzle), and expressive dark eyes from Image 1. Preserve the product's exact colors, materials, and any logos from Image 2 with extreme accuracy.
Seamless integration: Match ambient lighting, color temperature, and shadow direction across both subjects.
Background: {{soft cream #F5F0E8 seamless / warm neutral wood floor / MainPup brand color backdrop}}.
Photography style: Clean e-commerce lookbook, Canon EOS R5 with 50mm f/1.8 lens, natural and professional, shallow depth of field.
```

---

## 4. Kiwi Meme Sticker

**When to use:** social posts, packaging inserts, thank-you cards, community/social sections of the site.

**Reference to upload:** any expressive Kiwi shot — `IMG_0403.jpeg` (tongue out, happy) or `IMG_7563.jpeg` (side-eye) are gold.

```text
Turn this photo of the small silver-grey and white poodle × yorkshire mix into a funny hand-drawn sticker.

Style: Minimalist ugly-cute line drawing, doodle style, thick uneven black outlines, flat pastel fill colors. Pure white background.
Expression: Exaggerate the dog's expression to look {{extremely judgemental / dramatically shocked / lazily disappointed / suspiciously side-eyeing}}.
Accessories: Add doodled elements around the head — {{sweat drops / question marks / sparkles / tiny hearts / squiggly speed lines}}.
Text: Add handwritten text at the bottom: '{{caption text}}'. Messy, funny, hand-lettered style.
Keep her signature two-tone coat visible in the drawing (grey ears, white face).
```

---

## 5. Luxury Product Shot — Floating / Editorial

**When to use:** premium product launches, campaign hero shots, editorial banners.

**Reference to upload:** the product photo.

```text
Product:
MainPup {{PRODUCT NAME}} — {{shape/silhouette description}}, {{material and color}}, {{key visible detail}}.

Scene:
Luxury product shot floating above {{dark water / soft cream silk / cracked terracotta}}, with {{fresh daisies / dried grasses / scattered kibble reimagined as pearls}} arranged around it. {{Golden hour glow / bright fresh light / soft north-window light}} creates {{reflections and ripples / soft cast shadows}} across the surface.

Mood & Style:
{{Ethereal and premium / fresh and clean / warm and honest}}, high-end commercial photography, {{3/4 hero angle / dead-on macro}}, shallow depth of field with soft bokeh background.
```

---

## 6. Promotional Poster — Sale / Launch Banner

**When to use:** homepage banners, email hero images, IG story ads.

**Reference to upload:** hero product or a Kiwi + product composite.

```text
Design a professional promotional poster for MainPup — {{campaign name, e.g., "Spring Chew Drop"}}.

Composition: Cinematic close-up of {{product / Kiwi holding the product}}, {{soft cream backdrop with subtle grain / warm wood table with scattered daisies}}, cozy premium atmosphere.

Text integration:
1. Main title: '{{HEADLINE}}' in {{elegant serif / bold rounded sans}} typography at the top, {{color hex}}.
2. Offer badge: '{{OFFER, e.g., "2 for $30"}}' in a modern sticker-style badge on the {{right/left}} side.
3. Footer: '{{Limited Time / Free Shipping Over $50}}' in small clean text at the bottom.

Quality: All text perfectly spelled, kerned, and integrated into the image's depth of field. Type must feel photographed with the scene, not slapped on.
```

---

## 7. Y2K Scrapbook Collage — Kiwi Multi-Pose

**When to use:** playful "About Kiwi" section, IG carousel, seasonal campaigns.

**Reference to upload:** best clean Kiwi headshot (`_MG_6381.jpg`).

```text
facelock_identity: true
accuracy: 100%

scene: Colorful Y2K scrapbook poster aesthetic, vibrant stickers, the same small silver-grey and white poodle × yorkshire mix appearing in multiple poses across the collage — frameless cutouts, colorful crayon strokes and washi-tape edges, playful hand-doodled hearts and stars. Includes: close-up smiling head tilt, full-body sitting pose with a tiny bandana, mid-shot with tongue out mid-bark, sleeping curled up, holding a squeaky toy, and looking up with puppy eyes.

textures: Holographic accents, pastel gradients, glitter dots, magazine cut-out graphics, chaotic-but-balanced layout.

main_subject: Kiwi as the central figure in the middle of the collage, playful confident pose, cute-cool expression.

background: {{cream / soft mint / MainPup brand tint}} scrapbook paper with subtle notebook grid.

typography: Handwritten stickers with words like '{{Kiwi}}', '{{good girl}}', '{{main pup}}', '{{★}}', mixed fonts, Y2K bubble letters.
```

---

## 8. 3D Chibi MainPup Storefront

**When to use:** brand storytelling, About page hero, packaging insert card, merch.

**Reference to upload:** MainPup logo + a Kiwi photo (optional).

```text
3D chibi-style miniature concept store of MainPup, creatively designed with an exterior inspired by the brand's iconic imagery (a giant {{stylized dog bone / oversized carrot chew toy / dog biscuit shaped storefront}}). Two floors with large glass windows clearly showcasing the cozy interior: {{MainPup brand color}}-themed decor, warm lighting, and tiny staff figures in MainPup aprons.

Adorable tiny dog figures — including a small silver-grey and white poodle × yorkshire mix (Kiwi) — stroll along the storefront, surrounded by benches, street lamps, and potted plants.

Rendered in miniature cityscape style using Cinema 4D, blind-box toy aesthetic, rich detail, soft warm afternoon lighting. --ar 2:3
```

---

## 9. Blind-Box Kiwi Figurine

**When to use:** merch mockups, packaging art, "collect them all" campaign, Instagram reveals.

**Reference to upload:** clean Kiwi headshot.

```text
Transform the small silver-grey and white poodle × yorkshire mix in the uploaded photo into a cute 3D Pop Mart style blind box character.

Likeness: Keep key features recognizable — silver-grey ears and back, white face and chest, warm apricot muzzle tint, dark round expressive eyes, wavy-wiry coat texture stylized as smooth toy fur.
Style: C4D rendering, ambient occlusion, cute Q-version proportions (big head, small body), soft studio lighting, pastel palette.
Accessories: {{Tiny MainPup collar / mini bandana / miniature carrot toy}}.
Background: A simple solid matte {{MainPup brand hex}} background.
Detail: Smooth plastic toy texture with a slight glossy finish, forward-facing, friendly expression.
```

---

## Notes on Getting Best Results

- **Always upload references.** Nano Banana Pro is strongest when preserving identity from an image. For anything with Kiwi, upload at least one of the `_MG_` studio shots — they have the cleanest facial data.
- **Preserve identity language.** Repeat coat description ("silver-grey ears, white face, apricot muzzle") in every prompt — it stops the model from generalizing her into a generic terrier.
- **Structured JSON vs. natural language.** Both work. Use JSON when you want strict slot-filling (multi-pose Y2K, chibi store); use natural language for cinematic/editorial shots.
- **Aspect ratios.** Add `--ar 2:3` for portrait, `--ar 16:9` for hero banners, `--ar 1:1` for product tiles / IG feed.
- **Iterate on lighting words.** "Soft north-window light," "golden hour glow," "diffused studio bounce" — these move the needle more than adjective stacking.

Full source library: [references/awesome-nanobanana-pro/README.md](./references/awesome-nanobanana-pro/README.md) — 60+ prompts across 11 categories if you need something not covered above.

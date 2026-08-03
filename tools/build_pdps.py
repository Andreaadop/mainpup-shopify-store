#!/usr/bin/env python3
"""
build_pdps.py — Generate all mainpups product detail pages from one template.

WAT tool. Reads the downloaded Printify mockups under
brand_assets/products/web/pdp/<slug>/ plus the per-design content defined below,
and writes homepage/<slug>.html for each design (World's Best Dog -> product.html,
to preserve its existing URL). Every page shares the exact same markup/CSS so they
stay consistent; only the product-specific content is substituted.

Re-run any time to regenerate. Idempotent.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDP  = os.path.join(ROOT, "brand_assets", "products", "web", "pdp")

def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

COLOR_HEX = {
    "White":"#ffffff","Ivory":"#FFF7E7","Chambray":"#C7D9E4","Blossom":"#F4CBDD",
    "Orchid":"#C79BC2","Bay":"#7FB0AB","Blue Jean":"#7C97AE","Blue Spruce":"#3C574F",
    "Sage":"#9DAA8B","Grey":"#8f8f8f","Pepper":"#5F605B","Berry":"#7E4B63",
    "True Navy":"#1F2036","Black":"#101010",
}

# ---- per-design content -----------------------------------------------------
# slug, name, tagline, hero image (homepage), rating, review count, description
DESIGNS = [
 dict(slug="best-dog", file="product.html", name="World's Best Dog",
      tag="it's official now. it's on a shirt.", hero="best-dog.jpg",
      rating="4.9", reviews="214",
      desc="Your dog, printed in a bold two-tone portrait ringed with “world's best dog.” Send one clear photo — we turn it into the design and show you a proof before anything gets printed."),
 dict(slug="royalty", file="royalty.html", name="Royalty Portrait",
      tag="your pet already thinks this.", hero="royalty.jpg",
      rating="4.9", reviews="186",
      desc="Your pet, crowned. A regal dualtone portrait framed like an old-master oil painting — because they already act like royalty. Send one clear photo and we'll show you a proof before we print."),
 dict(slug="sunflower", file="sunflower.html", name="Sunflower Collage",
      tag="peak summer, peak pet.", hero="sunflower.jpg",
      rating="4.8", reviews="142",
      desc="Your pet in a sun-soaked collage of sunflowers and warm light — a bright, summery dualtone portrait. Send one clear photo and approve the proof before anything prints."),
 dict(slug="pixel-pet", file="pixel-pet.html", name="Pixel Pet",
      tag="best boy detected. loading…", hero="pixelated.jpg",
      rating="4.9", reviews="97",
      desc="Your pet, rendered in loving 8-bit pixels on a retro-computer readout — “best boy detected.” Send one clear photo and we'll turn it into pixel art. Proof first, always."),
 dict(slug="rookie-card", file="rookie-card.html", name="Rookie Card",
      tag="undefeated at napping.", hero="athlete.jpg",
      rating="4.8", reviews="123",
      desc="Your pet on their own pro trading card — stats, a foil-style frame, and an undefeated record at napping. Send one clear photo; approve the proof before we print."),
 dict(slug="iconic", file="iconic.html", name="Iconic Superstar",
      tag="famous in your house, at least.", hero="iconic.jpg",
      rating="4.9", reviews="168",
      desc="Your pet as the superstar they clearly are — a bold, magazine-cover dualtone portrait. Send one clear photo and we'll show you a proof before printing."),
 dict(slug="y2k-gamer", file="y2k-gamer.html", name="Y2K Gamer",
      tag="new high score: cutest.", hero="y2k-gamer.jpg",
      rating="4.8", reviews="88",
      desc="Your pet as a Y2K game hero — pixel hearts, high scores, early-2000s energy. Send one clear photo; nothing prints until you approve the proof."),
 dict(slug="pop-star", file="pop-star.html", name="2000's Pop Star",
      tag="certified platinum cuddler.", hero="pop-star.jpg",
      rating="4.9", reviews="112",
      desc="Your pet headlining like a 2000's pop icon — spotlight, sparkle, platinum-cuddler status. Send one clear photo and approve the proof before we print."),
]
BY_SLUG = {d["slug"]: d for d in DESIGNS}

SIZES_JS = ("[{s:'S',price:33.99},{s:'M',price:32.99},{s:'L',price:33.99},{s:'XL',price:33.99},"
            "{s:'2XL',price:34.99},{s:'3XL',price:34.99},{s:'4XL',price:42.05}]")

# rebuild color order + angles from files on disk
def design_media(slug):
    folder = os.path.join(PDP, slug)
    files = set(os.listdir(folder))
    # colors present (front files)
    colors = []
    for c in COLOR_HEX:
        fn = f"{slug}-{slugify(c)}-front.jpg"
        if fn in files:
            colors.append((c, COLOR_HEX[c], fn))
    # angle files exist for exactly one color — derive it from the -back file
    dc = None
    m = [f for f in files if f.endswith("-back.jpg")]
    if m:
        dc = m[0][len(slug)+1:-len("-back.jpg")]
    extra = {}
    if dc:
        for lab, key in [("person-5-context","lifestyle"),("back","back"),("folded","folded")]:
            fn = f"{slug}-{dc}-{lab}.jpg"
            if fn in files: extra[key] = fn
    # default color = the one with angle shots (keeps the gallery color-consistent)
    default_color = next((c for c in colors if slugify(c[0]) == dc), colors[0])[0]
    colors.sort(key=lambda t: (t[0] != default_color,))
    return colors, extra, default_color

def related_of(slug):
    order = [d["slug"] for d in DESIGNS]
    i = order.index(slug)
    return [order[(i+k) % len(order)] for k in range(1,5)]

TEMPLATE = open(os.path.join(os.path.dirname(__file__), "pdp_template.html"), encoding="utf-8").read()

def build(d):
    slug = d["slug"]
    colors, extra, default_color = design_media(slug)
    base = f"../brand_assets/products/web/pdp/{slug}/"
    front0 = colors[0][2]

    # thumbnails
    thumbs = []
    thumbs.append(f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="front" aria-current="true" aria-label="Front view"><img src="{base}{front0}" alt="" class="w-full h-full object-cover"></button>')
    if "lifestyle" in extra:
        thumbs.append(f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="lifestyle" aria-current="false" aria-label="On-model view"><img src="{base}{extra["lifestyle"]}" alt="" class="w-full h-full object-cover"></button>')
    if "back" in extra:
        thumbs.append(f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="back" aria-current="false" aria-label="Back view"><img src="{base}{extra["back"]}" alt="" class="w-full h-full object-cover"></button>')
    if "folded" in extra:
        thumbs.append(f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="folded" aria-current="false" aria-label="Folded view"><img src="{base}{extra["folded"]}" alt="" class="w-full h-full object-cover"></button>')
    thumbs_html = "\n        ".join(thumbs)

    # colors JS
    colors_js = ",\n    ".join(
        "{name:%s, hex:'%s', front:'%s'}" % (json.dumps(c[0]), c[1], c[2]) for c in colors
    )
    extra_js = ",".join("%s:'%s'" % (k, v) for k, v in extra.items())

    # floating "same design, other styles" — bare cutout PNGs, no card
    cut = f"{base}cut/"
    styles = f'''<div class="grid grid-cols-3 gap-4 sm:gap-8 max-w-3xl">
      <div class="style-opt group">
        <div class="style-figure"><img src="{cut}{slug}-tee.png" alt="{d['name']} relaxed tee" class="float-garment"></div>
        <span class="block font-bold text-navy text-sm mt-2">Relaxed Tee <span class="style-tag">Selected</span></span>
        <span class="text-xs text-navy/60">from $32.99</span>
      </div>
      <div class="style-opt group">
        <div class="style-figure"><img src="{cut}{slug}-sweatshirt.png" alt="{d['name']} sweatshirt" class="float-garment"></div>
        <span class="block font-bold text-navy text-sm mt-2">Sweatshirt</span>
        <span class="text-xs text-navy/60">from $41.99</span>
      </div>
      <div class="style-opt group">
        <div class="style-figure"><img src="{cut}{slug}-softstyle.png" alt="{d['name']} softstyle tee" class="float-garment"></div>
        <span class="block font-bold text-navy text-sm mt-2">Softstyle Tee</span>
        <span class="text-xs text-navy/60">from $27.99</span>
      </div>
    </div>'''

    # you might also like
    tiles = []
    for k, rs in enumerate(related_of(slug)):
        rd = BY_SLUG[rs]
        rot = "-1deg" if k % 2 == 0 else "1deg"
        tiles.append(f'''<a href="/homepage/{rd['file']}" class="tile-wrap group block rotate-[{rot}]">
        <div class="tile tile-sticker rounded-2xl overflow-hidden bg-white aspect-[6/7]">
          <img src="../brand_assets/products/web/{rd['hero']}" alt="{rd['name']} custom pet tee" loading="lazy" class="w-full h-full object-cover">
        </div>
        <div class="mt-3 px-1"><h3 class="font-bold text-navy text-sm">{rd['name']}</h3><p class="text-xs text-navy/55 italic">"{rd['tag']}"</p></div>
      </a>''')
    tiles_html = "\n      ".join(tiles)

    html = TEMPLATE
    repl = {
        "@@TITLE@@": f"{d['name']} — Custom Pet Tee | mainpups",
        "@@META@@": f"Turn your dog or cat into the {d['name']} custom tee. Upload a photo, approve the proof, then we print. No proof, no charge.",
        "@@NAME@@": d["name"],
        "@@RATING@@": d["rating"],
        "@@REVIEWS@@": d["reviews"],
        "@@DESC@@": d["desc"],
        "@@MAIN_IMG@@": f"{base}{front0}",
        "@@THUMBS@@": thumbs_html,
        "@@DEFAULT_COLOR@@": default_color,
        "@@STYLES@@": styles,
        "@@TILES@@": tiles_html,
        "@@COLORS_JS@@": colors_js,
        "@@SIZES_JS@@": SIZES_JS,
        "@@BASE_JS@@": base,
        "@@EXTRA_JS@@": extra_js,
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    out = os.path.join(ROOT, "homepage", d["file"])
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, f"({len(colors)} colors, {len(extra)} extra views)")

if __name__ == "__main__":
    for d in DESIGNS:
        build(d)

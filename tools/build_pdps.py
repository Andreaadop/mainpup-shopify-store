#!/usr/bin/env python3
"""
build_pdps.py — Generate every mainpups product page (8 designs x 3 garments = 24)
from one template, plus the collection grid/filters. Uses real Printify mockups
downloaded under brand_assets/products/web/pdp/<slug>/[<garment>/].

Tee pages keep their original URLs (best-dog -> product.html, others -> <slug>.html).
Crewneck -> <slug>-crewneck.html, Softstyle -> <slug>-softstyle.html.

Re-run any time. Idempotent.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDP  = os.path.join(ROOT, "brand_assets", "products", "web", "pdp")

def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

COLOR_HEX = {
    "White":"#ffffff","Ivory":"#FFF7E7","Chambray":"#C7D9E4","Blossom":"#F4CBDD",
    "Orchid":"#C79BC2","Bay":"#7FB0AB","Blue Jean":"#7C97AE","Blue Spruce":"#3C574F",
    "Sage":"#9DAA8B","Grey":"#8f8f8f","Pepper":"#5F605B","Berry":"#7E4B63",
    "True Navy":"#1F2036","Black":"#101010","Navy":"#1F2A44","Sand":"#D8C4A5",
    "Natural":"#EDE4CF","Light Blue":"#BFD6E6","Light Pink":"#F3C9D8","Maroon":"#5A2231",
    "Military Green":"#4B5320","Dark Heather":"#3F4145","Dark Chocolate":"#3B2A25",
    "Sport Grey":"#B4B4B4",
}

DESIGNS = [
 dict(slug="best-dog", name="World's Best Dog", tag="it's official now. it's on a shirt.", hero="best-dog.jpg",
      rating="4.9", reviews="214",
      desc="Your pet, printed in a bold two-tone portrait ringed with “world's best dog.” Send one clear photo — we turn it into the design and show you a proof before anything gets printed."),
 dict(slug="royalty", name="Royalty Portrait", tag="your pet already thinks this.", hero="royalty.jpg",
      rating="4.9", reviews="186",
      desc="Your pet, crowned. A regal dualtone portrait framed like an old-master oil painting — because they already act like royalty. Send one clear photo and we'll show you a proof before we print."),
 dict(slug="sunflower", name="Sunflower Collage", tag="peak summer, peak pet.", hero="sunflower.jpg",
      rating="4.8", reviews="142",
      desc="Your pet in a sun-soaked collage of sunflowers and warm light — a bright, summery dualtone portrait. Send one clear photo and approve the proof before anything prints."),
 dict(slug="pixel-pet", name="Pixel Pet", tag="best boy detected. loading…", hero="pixelated.jpg",
      rating="4.9", reviews="97",
      desc="Your pet, rendered in loving 8-bit pixels on a retro-computer readout — “best boy detected.” Send one clear photo and we'll turn it into pixel art. Proof first, always."),
 dict(slug="rookie-card", name="Rookie Card", tag="undefeated at napping.", hero="athlete.jpg",
      rating="4.8", reviews="123",
      desc="Your pet on their own pro trading card — stats, a foil-style frame, and an undefeated record at napping. Send one clear photo; approve the proof before we print."),
 dict(slug="iconic", name="Iconic Superstar", tag="famous in your house, at least.", hero="iconic.jpg",
      rating="4.9", reviews="168",
      desc="Your pet as the superstar they clearly are — a bold, magazine-cover dualtone portrait. Send one clear photo and we'll show you a proof before printing."),
 dict(slug="y2k-gamer", name="Y2K Gamer", tag="new high score: cutest.", hero="y2k-gamer.jpg",
      rating="4.8", reviews="88",
      desc="Your pet as a Y2K game hero — pixel hearts, high scores, early-2000s energy. Send one clear photo; nothing prints until you approve the proof."),
 dict(slug="pop-star", name="2000's Pop Star", tag="certified platinum cuddler.", hero="pop-star.jpg",
      rating="4.9", reviews="112",
      desc="Your pet headlining like a 2000's pop icon — spotlight, sparkle, platinum-cuddler status. Send one clear photo and approve the proof before we print."),
]
BY_SLUG = {d["slug"]: d for d in DESIGNS}

def sizes_js(pairs):
    return "[" + ",".join("{s:'%s',price:%s}" % (s, p) for s, p in pairs) + "]"

TEE_SIZES  = [("S",33.99),("M",32.99),("L",33.99),("XL",33.99),("2XL",34.99),("3XL",34.99),("4XL",42.05)]
CREW_SIZES = [("S",42.99),("M",41.99),("L",42.99),("XL",42.99),("2XL",44.99),("3XL",46.99),("4XL",48.99),("5XL",50.99)]
SOFT_SIZES = [("S",28.99),("M",27.99),("L",28.99),("XL",28.99),("2XL",29.99),("3XL",31.99),("4XL",33.99),("5XL",35.99)]

FABRIC = {
 "tee": (
   "<li><strong>Fabric:</strong> Comfort Colors 1717 — 100% ring-spun cotton, garment-dyed &amp; soft-washed. Heavyweight 6.1 oz, broken-in from day one.</li>"
   "<li><strong>Fit:</strong> Unisex, relaxed — size down for a classic fit.</li>"
   "<li><strong>Print:</strong> DTG (direct-to-garment), detailed and soft to the touch.</li>"
   "<li><strong>Care:</strong> Machine wash cold, inside out. Tumble dry low.</li>"),
 "crewneck": (
   "<li><strong>Fabric:</strong> Gildan 18000 Heavy Blend — 50/50 cotton/polyester, 8.0 oz. Ribbed collar and cuffs that hold their shape wash after wash.</li>"
   "<li><strong>Fit:</strong> Unisex, relaxed crewneck — roomy through the body.</li>"
   "<li><strong>Print:</strong> DTG, soft to the touch and built to last.</li>"
   "<li><strong>Care:</strong> Machine wash cold, inside out. Tumble dry low. Don't iron the print.</li>"),
 "softstyle": (
   "<li><strong>Fabric:</strong> Gildan 64000 Softstyle — 100% ring-spun cotton, lightweight 4.5 oz with a smooth printable face.</li>"
   "<li><strong>Fit:</strong> Unisex, slim modern fit — size up for a relaxed look.</li>"
   "<li><strong>Print:</strong> DTG, crisp detail on a soft hand-feel.</li>"
   "<li><strong>Care:</strong> Machine wash cold, inside out. Tumble dry low.</li>"),
}

# garment definitions (order = display order in the "other styles" row)
GARMENTS = [
 dict(key="tee", label="Relaxed Tee", float="tee", cat="tee",
      subtitle="Dualtone custom pet tee · Comfort Colors® garment-dyed",
      base="$32.99", sizes=TEE_SIZES, subfolder=""),
 dict(key="crewneck", label="Crewneck", float="sweatshirt", cat="crewneck",
      subtitle="Dualtone custom pet crewneck · Gildan 18000 Heavy Blend",
      base="$41.99", sizes=CREW_SIZES, subfolder="crewneck"),
 dict(key="softstyle", label="Softstyle Tee", float="softstyle", cat="softstyle",
      subtitle="Dualtone custom pet tee · Gildan Softstyle, lightweight",
      base="$27.99", sizes=SOFT_SIZES, subfolder="softstyle"),
]
BY_G = {g["key"]: g for g in GARMENTS}

def page_file(slug, gkey):
    if gkey == "tee":
        return "product.html" if slug == "best-dog" else f"{slug}.html"
    return f"{slug}-{gkey}.html"

def media_folder(slug, gkey):
    sub = BY_G[gkey]["subfolder"]
    return os.path.join(PDP, slug, sub) if sub else os.path.join(PDP, slug)

def media_base(slug, gkey):
    sub = BY_G[gkey]["subfolder"]
    return f"../brand_assets/products/web/pdp/{slug}/" + (f"{sub}/" if sub else "")

ANGLES = [("person-5-context","lifestyle"),("back","back"),("folded","folded")]

def design_media(slug, gkey):
    folder = media_folder(slug, gkey)
    files = set(os.listdir(folder)) if os.path.isdir(folder) else set()
    colors = [(c, COLOR_HEX[c], f"{slug}-{slugify(c)}-front.jpg")
              for c in COLOR_HEX if f"{slug}-{slugify(c)}-front.jpg" in files]
    # default color = the color that has angle shots (keeps gallery consistent)
    dc = None
    for lab, _ in ANGLES:
        m = [f for f in files if f.endswith(f"-{lab}.jpg")]
        if m:
            dc = m[0][len(slug)+1:-(len(lab)+5)]  # strip "<slug>-" and "-<lab>.jpg"
            break
    extra = {}
    if dc:
        for lab, key in ANGLES:
            fn = f"{slug}-{dc}-{lab}.jpg"
            if fn in files: extra[key] = fn
    if not colors:  # safety
        return [], {}, None
    default_color = next((c for c in colors if slugify(c[0]) == dc), colors[0])[0]
    colors.sort(key=lambda t: (t[0] != default_color,))
    return colors, extra, default_color

def related_of(slug):
    order = [d["slug"] for d in DESIGNS]
    i = order.index(slug)
    return [order[(i+k) % len(order)] for k in range(1, 5)]

TEMPLATE = open(os.path.join(os.path.dirname(__file__), "pdp_template.html"), encoding="utf-8").read()

def build_page(d, g):
    slug, gkey = d["slug"], g["key"]
    colors, extra, default_color = design_media(slug, gkey)
    if not colors:
        print("  !! no media for", slug, gkey, "- skipped"); return
    base = media_base(slug, gkey)
    front0 = colors[0][2]

    thumbs = [f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="front" aria-current="true" aria-label="Front view"><img src="{base}{front0}" alt="" class="w-full h-full object-cover"></button>']
    for key, lbl in [("lifestyle","On-model view"),("back","Back view"),("folded","Folded view")]:
        if key in extra:
            thumbs.append(f'<button class="thumb rounded-xl overflow-hidden aspect-square" data-view="{key}" aria-current="false" aria-label="{lbl}"><img src="{base}{extra[key]}" alt="" class="w-full h-full object-cover"></button>')
    thumbs_html = "\n        ".join(thumbs)

    colors_js = ",\n    ".join("{name:%s, hex:'%s', front:'%s'}" % (json.dumps(c[0]), c[1], c[2]) for c in colors)
    extra_js = ",".join("%s:'%s'" % (k, v) for k, v in extra.items())

    # "same design, other styles" — links to sibling garment pages
    cut = f"../brand_assets/products/web/pdp/{slug}/cut/"
    cards = []
    for og in GARMENTS:
        img = f'<div class="style-figure"><img src="{cut}{slug}-{og["float"]}.png" alt="{d["name"]} {og["label"].lower()}" class="float-garment"></div>'
        price = f'<span class="text-xs text-navy/60">from {og["base"]}</span>'
        if og["key"] == gkey:
            cards.append(f'''<div class="style-opt group">
        {img}
        <span class="block font-bold text-navy text-sm mt-2">{og["label"]} <span class="style-tag">Selected</span></span>
        {price}
      </div>''')
        else:
            cards.append(f'''<a href="{page_file(slug, og["key"])}" class="style-opt group block">
        {img}
        <span class="block font-bold text-navy text-sm mt-2 group-hover:text-burgundy">{og["label"]}</span>
        {price}
      </a>''')
    styles = '<div class="grid grid-cols-3 gap-4 sm:gap-8 max-w-3xl">\n      ' + "\n      ".join(cards) + '\n    </div>'

    # you might also like — other designs, same garment
    tiles = []
    for k, rs in enumerate(related_of(slug)):
        rd = BY_SLUG[rs]; rot = "-1deg" if k % 2 == 0 else "1deg"
        tiles.append(f'''<a href="{page_file(rs, gkey)}" class="tile-wrap group block rotate-[{rot}]">
        <div class="tile tile-sticker rounded-2xl overflow-hidden bg-white aspect-[6/7]">
          <img src="../brand_assets/products/web/{rd['hero']}" alt="{rd['name']} custom pet {g['label'].lower()}" loading="lazy" class="w-full h-full object-cover">
        </div>
        <div class="mt-3 px-1"><h3 class="font-bold text-navy text-sm">{rd['name']}</h3><p class="text-xs text-navy/55 italic">"{rd['tag']}"</p></div>
      </a>''')
    tiles_html = "\n      ".join(tiles)

    price0 = "$" + ("%.2f" % [p for s, p in g["sizes"] if s == "M"][0])
    html = TEMPLATE
    for k, v in {
        "@@TITLE@@": f"{d['name']} — Custom Pet {g['label']} | mainpups",
        "@@META@@": f"Turn your dog or cat into the {d['name']} custom {g['label'].lower()}. Upload a photo, approve the proof, then we print. No proof, no charge.",
        "@@NAME@@": d["name"], "@@SUBTITLE@@": g["subtitle"],
        "@@RATING@@": d["rating"], "@@REVIEWS@@": d["reviews"], "@@DESC@@": d["desc"],
        "@@MAIN_IMG@@": f"{base}{front0}", "@@THUMBS@@": thumbs_html,
        "@@DEFAULT_COLOR@@": default_color, "@@FABRIC@@": FABRIC[gkey], "@@PRICE0@@": price0,
        "@@STYLES@@": styles, "@@TILES@@": tiles_html,
        "@@COLORS_JS@@": colors_js, "@@SIZES_JS@@": sizes_js(g["sizes"]),
        "@@BASE_JS@@": base, "@@EXTRA_JS@@": extra_js,
    }.items():
        html = html.replace(k, v)
    open(os.path.join(ROOT, "homepage", page_file(slug, gkey)), "w", encoding="utf-8").write(html)

def build_collection():
    path = os.path.join(ROOT, "homepage", "collection.html")
    html = open(path, encoding="utf-8").read()
    counts = {"tee":0,"crewneck":0,"softstyle":0}
    cards = []
    i = 0
    for d in DESIGNS:
        for g in GARMENTS:
            colors, extra, dc = design_media(d["slug"], g["key"])
            if not colors: continue
            counts[g["key"]] += 1
            if g["key"] == "tee":
                img = f"../brand_assets/products/web/{d['hero']}"
            else:
                img = media_base(d["slug"], g["key"]) + colors[0][2]
            rot = "-1deg" if i % 2 == 0 else "1deg"; i += 1
            cards.append(f'''<a href="{page_file(d['slug'], g['key'])}" data-cat="{g['cat']}" class="tile-wrap group product-card block rotate-[{rot}]">
          <div class="tile tile-sticker relative rounded-2xl overflow-hidden bg-white aspect-[6/7]">
            <span class="absolute top-3 left-3 z-10 text-[.7rem] pixel font-bold uppercase tracking-wide bg-white text-navy border-2 border-navy rounded-full px-2.5 py-1 rotate-[-3deg]">{g['label']}</span>
            <img src="{img}" alt="{d['name']} custom pet {g['label'].lower()}" loading="lazy" class="w-full h-full object-cover">
          </div>
          <div class="mt-4 px-1">
            <div class="flex items-baseline justify-between gap-3">
              <h3 class="font-bold text-navy">{d['name']}</h3>
              <span class="display text-burgundy text-lg shrink-0">{g['base']}</span>
            </div>
            <p class="text-sm text-navy/60 italic">"{d['tag']}"</p>
          </div>
        </a>''')
    grid = "\n\n        ".join(cards)
    total = sum(counts.values())
    filters = f'''<button class="chip btn" data-filter="all" aria-pressed="true">All <span class="n">{total}</span></button>
        <button class="chip btn" data-filter="tee" aria-pressed="false">T-Shirts <span class="n">{counts['tee']}</span></button>
        <button class="chip btn" data-filter="crewneck" aria-pressed="false">Crewnecks <span class="n">{counts['crewneck']}</span></button>
        <button class="chip btn" data-filter="softstyle" aria-pressed="false">Softstyle <span class="n">{counts['softstyle']}</span></button>'''

    html = re.sub(r'<!--GRID-->.*?<!--/GRID-->', "<!--GRID-->\n        " + grid + "\n        <!--/GRID-->", html, flags=re.S)
    html = re.sub(r'<!--FILTERS-->.*?<!--/FILTERS-->', "<!--FILTERS-->\n        " + filters + "\n        <!--/FILTERS-->", html, flags=re.S)
    html = html.replace("card.dataset.theme === filter", "card.dataset.cat === filter")
    open(path, "w", encoding="utf-8").write(html)
    print(f"collection: {total} cards ({counts})")

if __name__ == "__main__":
    n = 0
    for d in DESIGNS:
        for g in GARMENTS:
            build_page(d, g); n += 1
    print("pages written:", n)
    build_collection()

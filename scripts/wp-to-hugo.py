#!/usr/bin/env python3
"""
Migra posts de WordPress (via REST API) a fitxers Markdown per a Hugo.
Ús: python3 scripts/wp-to-hugo.py
"""
import json, re, os, sys, urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

try:
    import html2text
except ImportError:
    print("Falta html2text. Executa: .venv/bin/pip install html2text")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────
WP_BASE      = "https://cuinetes.linuxbcn.com/wp-json/wp/v2"
CONTENT_DIR  = Path("content/receptes")
IMAGES_DIR   = Path("static/images/receptes")
WP_UPLOADS   = "https://cuinetes.linuxbcn.com/wp-content/uploads/"

# ── html2text config ──────────────────────────────────────────
h = html2text.HTML2Text()
h.ignore_links      = False
h.ignore_images     = True   # les gestionem per separat
h.body_width        = 0
h.ignore_emphasis   = False
h.single_line_break = False

# ── Helpers ───────────────────────────────────────────────────
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cuinetes-migrator/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def download_image(url, slug):
    """Descarrega la imatge i retorna el path relatiu /images/receptes/..."""
    ext = url.split("?")[0].split(".")[-1].lower()
    if ext not in ("jpg","jpeg","png","webp","gif"):
        ext = "jpg"
    # Agafa el nom de fitxer original sense mides (ex: IMG_123-768x1024 → IMG_123)
    basename = url.split("/")[-1].split("?")[0]
    basename = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', basename)
    dest = IMAGES_DIR / basename
    if not dest.exists():
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"    ↓ {basename}")
        except Exception as e:
            print(f"    ✗ {url}: {e}")
            return ""
    return f"/images/receptes/{basename}"

def extract_first_image(html):
    """Extreu la URL de la primera imatge del contingut."""
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    if m:
        src = m.group(1)
        # Prefereix la URL sense srcset (la original)
        srcset_m = re.search(r'srcset=["\']([^"\']+)["\']', html)
        if srcset_m:
            # Agafa l'última URL del srcset (la més gran)
            srcs = [s.strip().split()[0] for s in srcset_m.group(1).split(",") if s.strip()]
            if srcs:
                src = srcs[-1]
        return src
    return ""

def html_to_md(html):
    """Converteix HTML de Gutenberg a Markdown net."""
    # Elimina galeries de blocs (no les volem al cos)
    html = re.sub(r'<figure class="wp-block-gallery[^"]*"[^>]*>.*?</figure>', '', html, flags=re.DOTALL)
    # Elimina figures soltes (imatges dins el text)
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL)
    # Elimina classes i atributs WP
    html = re.sub(r' class="[^"]*"', '', html)
    html = re.sub(r' data-[^=]+="[^"]*"', '', html)
    html = re.sub(r' style="[^"]*"', '', html)
    md = h.handle(html)
    # Neteja línies en blanc múltiples
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()

def sanitize_tag(t):
    """Normalitza tags: minúscules, sense accents redundants."""
    return t.strip().lower()

# ── Carrega mapes de categories i tags ────────────────────────
print("Carregant categories i tags...")
cat_map = {c["id"]: c["name"] for c in fetch(f"{WP_BASE}/categories?per_page=100")}
tag_map = {t["id"]: t["name"] for t in fetch(f"{WP_BASE}/tags?per_page=100")}

# Mapa WP categories → Hugo categories
WP_CAT_TO_HUGO = {
    "receptes":        None,   # ignorem la categoria genèrica
    "Sense categoria": None,
}

CONTENT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# ── Migra tots els posts ───────────────────────────────────────
print("Descarregant posts...")
posts = fetch(f"{WP_BASE}/posts?per_page=100&_fields=id,title,slug,date,content,excerpt,categories,tags&page=1")
print(f"{len(posts)} posts trobats\n")

migrated = 0
for p in posts:
    slug    = p["slug"]
    title   = p["title"]["rendered"]
    # Decodifica entitats HTML bàsiques
    title   = title.replace("&#8217;", "'").replace("&amp;", "&").replace("&#8220;", '"').replace("&#8221;", '"')
    date    = p["date"][:10]  # YYYY-MM-DD
    html    = p["content"]["rendered"]
    excerpt = p.get("excerpt", {}).get("rendered", "")

    # Imatge destacada: primera del contingut
    first_img_url = extract_first_image(html)
    image_path = ""
    if first_img_url:
        image_path = download_image(first_img_url, slug)

    # Tags → ingredients
    tags = [sanitize_tag(tag_map[t]) for t in p.get("tags", []) if t in tag_map]
    # Filtra tags genèrics de WP que no aporten
    skip_tags = {"avuidino", "barcelona", "barat", "bo", "la recepta", "sense gluten"}
    tags = [t for t in tags if t not in skip_tags]

    # Contingut → Markdown
    body = html_to_md(html)

    # Lead des de l'excerpt
    lead = ""
    if excerpt:
        lead_md = html_to_md(excerpt)
        lead = lead_md.strip().replace("\n", " ")[:200]

    # Front matter
    cats_yaml = "  - receptes"  # per defecte — ajustar manualment després
    tags_yaml = "\n".join(f"  - \"{t}\"" for t in tags) if tags else ""

    fm_lines = [
        "---",
        f'title: "{title}"',
        f"date: {date}",
        "draft: false",
        "categories:",
        cats_yaml,
    ]
    if tags:
        fm_lines.append("tags:")
        fm_lines.append(tags_yaml)
    if image_path:
        fm_lines.append(f'image: "{image_path}"')
    if lead:
        fm_lines.append(f'lead: "{lead}"')
    fm_lines += [
        'dificultat: ""',
        'temps: ""',
        "racions: 4",
        "---",
    ]

    front_matter = "\n".join(fm_lines)
    md_content   = f"{front_matter}\n\n{body}\n"

    out_path = CONTENT_DIR / f"{slug}.md"
    out_path.write_text(md_content, encoding="utf-8")
    migrated += 1
    print(f"✓ {slug}")

print(f"\n{migrated} receptes migrades a {CONTENT_DIR}/")
print("Recorda: revisa les categories i dificultat/temps manualment.")

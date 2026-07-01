#!/usr/bin/env python3
"""
Descàrrega les darreres N publicacions d'un perfil públic d'Instagram
i genera static/instagram.json amb paths locals.

Ús: python3 scripts/fetch-instagram.py
Requereix: pip install instaloader
"""
import json, sys, os, shutil
from pathlib import Path
from datetime import datetime, timezone

try:
    import instaloader
except ImportError:
    print("ERROR: pip install instaloader", file=sys.stderr)
    sys.exit(1)

IG_USER   = os.environ.get("IG_USERNAME", "cuinetes_linuxbcn")
MAX_POSTS = int(os.environ.get("IG_MAX_POSTS", "9"))
OUT_JSON  = Path("static/instagram.json")
IMG_DIR   = Path("static/images/instagram")

IMG_DIR.mkdir(parents=True, exist_ok=True)

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    quiet=True,
)

print(f"Obtenint perfil @{IG_USER}...")
try:
    profile = instaloader.Profile.from_username(L.context, IG_USER)
except instaloader.exceptions.ProfileNotExistsException:
    print(f"ERROR: perfil @{IG_USER} no existeix", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

posts_data = []
count = 0

for post in profile.get_posts():
    if count >= MAX_POSTS:
        break
    if post.is_video:
        # Per vídeos agafem la miniatura
        img_url = post.url
    else:
        img_url = post.url

    # Nom de fitxer local basat en el shortcode
    ext = "jpg"
    local_name = f"{post.shortcode}.{ext}"
    local_path = IMG_DIR / local_name
    web_path   = f"/images/instagram/{local_name}"

    # Descarrega si no existeix
    if not local_path.exists():
        try:
            import urllib.request
            req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                local_path.write_bytes(r.read())
            print(f"  ↓ {local_name}")
        except Exception as e:
            print(f"  ✗ {local_name}: {e}", file=sys.stderr)
            web_path = ""

    # Caption: primers 120 caràcters
    caption = (post.caption or "").strip()
    if len(caption) > 120:
        caption = caption[:117] + "…"

    posts_data.append({
        "shortcode": post.shortcode,
        "url":       f"https://www.instagram.com/p/{post.shortcode}/",
        "image":     web_path,
        "caption":   caption,
        "date":      post.date_utc.strftime("%Y-%m-%d"),
        "likes":     post.likes,
        "is_video":  post.is_video,
    })
    count += 1
    print(f"  ✓ {post.shortcode} ({post.date_utc.strftime('%Y-%m-%d')})")

output = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "profile":      f"https://www.instagram.com/{IG_USER}/",
    "username":     IG_USER,
    "posts":        posts_data,
}

OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2))
print(f"\n✓ {len(posts_data)} posts → {OUT_JSON}")

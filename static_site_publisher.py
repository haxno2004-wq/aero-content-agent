"""
Publishes an article as a Jekyll post file. GitHub Pages builds Jekyll sites
automatically and for free (no hosting cost, no card needed) - this just needs
Settings -> Pages -> enabled on the repo, once.

Two modes (config.POST_STATUS):
  "draft"   -> writes to _drafts/, which Jekyll/GitHub Pages ignores completely.
               Nothing goes live until you manually move the file into _posts/
               and commit - that's your fact-check/review gate.
  "publish" -> writes straight to _posts/, live as soon as it's committed.
"""
import datetime
import re
from pathlib import Path

import config

POSTS_DIR = Path("_posts")
DRAFTS_DIR = Path("_drafts")


def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug[:60].rstrip("-")


def publish_post(title: str, body_html: str, tags: list, meta_description: str) -> dict:
    is_draft = config.POST_STATUS.lower() != "publish"
    target_dir = DRAFTS_DIR if is_draft else POSTS_DIR
    target_dir.mkdir(exist_ok=True)

    today = datetime.date.today()
    slug = _slugify(title)
    # _drafts/ filenames have no date prefix (Jekyll convention); _posts/ needs one.
    filename = target_dir / (f"{slug}.md" if is_draft else f"{today.isoformat()}-{slug}.md")

    # Jekyll front matter + body. Front matter values are YAML - keep quoting simple/safe.
    safe_title = title.replace('"', "'")
    safe_desc = meta_description.replace('"', "'")
    tags_yaml = "[" + ", ".join(f'"{t}"' for t in tags) + "]"

    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "{safe_title}"\n'
        f'description: "{safe_desc}"\n'
        f"tags: {tags_yaml}\n"
        f"date: {today.isoformat()} 09:00:00 +0530\n"
        "---\n\n"
    )

    filename.write_text(front_matter + body_html)

    if is_draft:
        # Not live yet - nothing to link to until you move this into _posts/.
        return {"file": str(filename), "url_path": None, "status": "draft (needs review)"}

    # Path Jekyll will publish this at, given permalink: /:year/:month/:day/:title/ in _config.yml
    url_path = f"/{today.year}/{today.month:02d}/{today.day:02d}/{slug}/"
    return {"file": str(filename), "url_path": url_path, "status": "published"}

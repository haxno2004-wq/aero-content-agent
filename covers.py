"""
Deterministic, offline SVG cover images for every article.

Why generated SVG instead of stock photos:
  * zero external requests (works inside GitHub Pages' built environment
    and passes without any API key or image library),
  * every link in the site stays self-contained (nothing hotlinks a CDN),
  * the same slug always produces the same image (no Git churn).

Covers are written to assets/covers/<slug>.svg the first time they are
needed and only rewritten when missing.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

COVERS_DIR = Path("assets/covers")

# 1200x630 is the standard og:image / social-card ratio.
W, H = 1200, 630

# Topic emoji: first keyword that matches wins. Engineering-neutral fallback.
_EMOJI = [
    ("turbulence", "🌪️"),
    ("cfd", "🌀"),
    ("ansys", "🛠️"),
    ("mesh", "🕸️"),
    ("uav", "🛸"),
    ("drone", "🛸"),
    ("wind", "🌬️"),
    ("airfoil", "✈️"),
    ("wing", "✈️"),
    ("modal", "📊"),
    ("thermal", "🌡️"),
    ("impact", "💥"),
    ("python", "🐍"),
    ("matlab", "🧪"),
    ("composite", "🧱"),
    ("career", "🧭"),
    ("research", "🔬"),
]


def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug[:60].rstrip("-")


def _wrap(text: str, width: int = 26, max_lines: int = 3) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
        if len(lines) == max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len(" ".join(words)) > sum(len(l) for l in lines) + max_lines:
        lines[-1] = lines[-1].rstrip(",.;:") + "…"
    return lines


def cover_for(title: str, slug: str | None = None) -> tuple[Path, str]:
    """Return (path_on_site, exists=True after call) for the post's cover image.

    Idempotent: regenerates only if the file is missing (or FORCE=1).
    """
    slug = slug or _slugify(title)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    out = COVERS_DIR / f"{slug}.svg"

    if not out.exists() or __import__("os").environ.get("FORCE"):
        digest = hashlib.md5(slug.encode()).hexdigest()
        h1 = int(digest[:2], 16)            # base hue
        h2 = (h1 + 40 + int(digest[2:4], 16) % 80) % 360
        emoji = next((e for kw, e in _EMOJI if kw in slug), "🚀")
        lines = _wrap(title)
        n = len(lines)
        ty = H / 2 - (n - 1) * 26 + 10
        text_spans = "".join(
            f'<tspan x="{W // 2}" dy="{0 if i == 0 else 52}">{line}</tspan>'
            for i, line in enumerate(lines)
        )
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="hsl({h1} 60% 14%)"/>
    <stop offset="1" stop-color="hsl({h2} 65% 24%)"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<circle cx="{W * 0.82}" cy="{H * 0.18}" r="220" fill="hsl({h2} 70% 40%)" opacity="0.18"/>
<circle cx="{W * 0.12}" cy="{H * 0.85}" r="180" fill="hsl({h1} 70% 45%)" opacity="0.16"/>
<text x="{W - 40}" y="64" text-anchor="end" font-family="system-ui, sans-serif"
      font-size="30" fill="#ffffff" opacity="0.75" font-weight="700">AERO / CFD NOTES</text>
<text x="{W // 2}" y="{H / 2 - 30}" font-size="150" text-anchor="middle">{emoji}</text>
<text x="{W // 2}" y="{ty}" text-anchor="middle" fill="#ffffff"
      font-family="system-ui, sans-serif" font-size="44" font-weight="700">{text_spans}</text>
</svg>
'''
        out.write_text(svg, encoding="utf-8")
    return out, True

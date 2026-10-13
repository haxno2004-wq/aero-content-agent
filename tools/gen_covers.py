"""
Backfill tool: generate deterministic SVG covers + add `hero:` front matter to
every existing post/draft, and move _drafts/ files into _posts/ (publish mode).

Run at repo root:
  python tools/gen_covers.py            # covers + hero front matter only
  python tools/gen_covers.py --publish  # also publish drafts into _posts/
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import covers  # noqa: E402

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def add_hero(md_path: Path) -> bool:
    """Insert `hero: assets/covers/<slug>.svg` into post front matter if absent."""
    text = md_path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        print(f"  !! no front matter: {md_path.name}")
        return False
    fm = m.group(1)
    if re.search(r"^hero:", fm, re.M):
        return False
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", md_path.stem)
    title = re.search(r'^title:\s*"(.+)"', fm, re.M)
    cover_file, _ = covers.cover_for(title.group(1) if title else stem, stem)
    hero = str(covers.COVERS_DIR / f"{stem}.svg").replace("\\", "/")
    new_fm = fm + f"\nhero: {hero}"
    md_path.write_text(text[: m.start(1)] + new_fm + text[m.end(1):], encoding="utf-8")
    return True


def publish_drafts() -> int:
    (ROOT / "_posts").mkdir(exist_ok=True)
    moved = 0
    for draft in sorted((ROOT / "_drafts").glob("*.md")):
        fm = FM_RE.match(draft.read_text(encoding="utf-8"))
        date = "2026-10-13"
        if fm:
            dm = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", fm.group(1), re.M)
            if dm:
                date = dm.group(1)
        target = ROOT / "_posts" / f"{date}-{draft.name}"
        draft.rename(target)
        add_hero(target)
        print(f"  published: {target.name}")
        moved += 1
    return moved


def main():
    publish = "--publish" in sys.argv
    n = publish_drafts() if publish else 0
    for md in (ROOT / "_drafts").glob("*.md"):
        add_hero(md)
    for md in (ROOT / "_posts").glob("*.md"):
        add_hero(md)
    print(f"done: {n} drafts published, covers generated in assets/covers/")


if __name__ == "__main__":
    main()

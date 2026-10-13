"""
Regenerates upcoming.md — the public view of the editorial queue.

Called by run_pipeline.py after every run, so the page always shows what's
publishing next and confirms which articles already shipped. Readers get
transparency ("what is this site going to cover?"), and the fresh text laid
down on every run gives the Googlebot something new to crawl daily.
"""
import json
import datetime
from pathlib import Path

TOPICS_FILE = Path("topics.json")
OUT = Path("upcoming.md")


def write_page(topics: list | None = None) -> str:
    topics = topics or json.loads(TOPICS_FILE.read_text(encoding="utf-8"))
    unused = [t for t in topics if not t.get("used")]
    used_n = len(topics) - len(unused)
    today = datetime.date.today().isoformat()

    lines = [
        "---",
        'layout: default',
        'title: "Upcoming topics"',
        'description: "What this CFD/ANSYS/UAV tutorial site will publish next — the live editorial queue."',
        "---",
        "",
        "<h1>What we're publishing next</h1>",
        f"<p><strong>{len(unused)} topics queued</strong> · "
        f"{used_n} articles already live · last updated {today}. "
        f"Each one becomes a full step-by-step tutorial within ~40 days "
        f"(1 article/day). See everything already published on the "
        f'<a href="/">homepage grid</a>.</p>',
        "",
    ]

    for i, t in enumerate(unused, 1):
        # HTML-escape the topic like the publisher does for titles.
        title = t["topic"].replace('&', '&amp;').replace('<', '&lt;').replace('"', "'")
        if i == 1:
            lines.append('<ul class="queue">')
        lines.append(f'<li class="q">{title}</li>')
        if i == len(unused):
            lines.append('</ul>')

    css = "\n<style>\nul.queue { list-style: none; padding: 0; counter-reset: q; }\nli.q { padding: 8px 0; border-bottom: 1px dashed var(--card2); counter-increment: q; }\nli.q::before { content: counter(q) \".\"; color: var(--muted); font-weight: 600; margin-right: 10px; }\n</style>\n"
    body = "\n".join(lines) + css
    OUT.write_text(body, encoding="utf-8")
    return f"upcoming.md regenerated: {len(unused)} queued"


if __name__ == "__main__":
    print(write_page())

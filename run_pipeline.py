"""
Daily entry point. For each unused topic (up to ARTICLES_PER_RUN):
  1. generate an article via NVIDIA
  2. write it as a Jekyll post (published free via GitHub Pages once committed)
  3. mark the topic used in topics.json
Then sends one Telegram digest summarizing the whole run - success, failures, links.
The GitHub Actions workflow commits topics.json + _posts/ back to the repo after this runs.
"""
import datetime
import json
from pathlib import Path

import config
from content_generator import generate_article
from static_site_publisher import publish_post
from telegram_notifier import send_message

TOPICS_FILE = Path("topics.json")


def load_topics():
    return json.loads(TOPICS_FILE.read_text())


def save_topics(topics):
    TOPICS_FILE.write_text(json.dumps(topics, indent=2))


def main():
    topics = load_topics()
    unused = [t for t in topics if not t.get("used")]

    if not unused:
        send_message("⚠️ All seed topics have been used. Add more topics to topics.json.")
        return

    batch = unused[: config.ARTICLES_PER_RUN]
    results = []

    for t in batch:
        try:
            article = generate_article(t["topic"])
            pub = publish_post(
                title=article["title"],
                body_html=article["body_html"],
                tags=article.get("tags", []),
                meta_description=article.get("meta_description", ""),
            )

            t["used"] = True
            t["published_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            t["post_file"] = pub.get("file")
            t["post_status"] = pub.get("status")

            if pub.get("url_path"):
                full_link = (config.SITE_BASE_URL.rstrip("/") + pub["url_path"]) if config.SITE_BASE_URL else pub["url_path"]
                t["post_link"] = full_link
                results.append(f"✅ {article['title']} (live)\n{full_link}")
            else:
                t["post_link"] = None
                results.append(f"📝 {article['title']} (draft - review at {pub['file']}, then move to _posts/)")

        except Exception as e:  # noqa: BLE001 - keep going and report the error instead of crashing the whole run
            results.append(f"❌ Failed on: {t['topic']}\nError: {e}")

    save_topics(topics)

    summary = "📰 <b>Daily content run</b>\n\n" + "\n\n".join(results)
    remaining = len([t for t in topics if not t.get("used")])
    summary += f"\n\n{remaining} topics remaining in the queue."
    if not config.SITE_BASE_URL:
        summary += "\n\n(Set SITE_BASE_URL once your GitHub Pages site is live, so links here are clickable.)"
    send_message(summary)


if __name__ == "__main__":
    main()

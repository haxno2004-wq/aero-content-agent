"""
Sends a daily digest message to your Telegram - this is the "separate platform
to monitor" piece, independent of the content-generation/publishing pipeline.
"""
import requests

import config


def send_message(text: str) -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[telegram] Not configured - skipping notification. Message was:\n", text)
        return

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        json={
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"[telegram] Failed to send message: {resp.status_code} {resp.text}")

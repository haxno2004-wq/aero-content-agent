"""
Calls your free NVIDIA model to generate one tutorial article.

Deliberately NOT using JSON output here. Asking an LLM to wrap a large HTML
article inside a JSON string is fragile - a single unescaped quote or literal
newline in the body breaks json.loads(). Instead we use a simple plain-text
format with a clear marker before the body, which needs zero escaping.
"""
import requests

import config

SYSTEM_PROMPT = """You are an expert aerospace/mechanical engineer and technical writer \
who specializes in CFD, ANSYS (Fluent/CFX/Static Structural), FEM, LS-DYNA, composite \
materials, and UAV/drone aerodynamics and structures.

Write a detailed, technically accurate, SEO-friendly tutorial article for engineering \
students and early-career engineers on the topic given by the user.

Rules:
- Be technically precise. Do NOT invent specific numeric values, formulas, or citations \
you are not certain of - explain the concept and general approach qualitatively instead \
of stating a wrong number.
- Write like a practitioner walking someone through the real workflow (steps, common \
mistakes, what to check), not a vague overview.
- 900-1400 words in the body.
- Body must be clean HTML using only <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em> tags. \
No <h1> (the title is handled separately), no <script>, no external links unless \
explicitly asked for.

Respond in EXACTLY this plain-text format and nothing else - no JSON, no markdown \
code fences, no extra commentary before or after:

TITLE: <the article title, one line, no quotes around it>
DESCRIPTION: <meta description under 155 characters, one line>
TAGS: <comma-separated tags, one line, e.g. cfd, ansys, aerodynamics>
---BODY---
<the full HTML body of the article starts immediately after that line and \
continues to the end of your response>
"""


def _extract_field(header_text: str, field_name: str) -> str:
    prefix = field_name.upper() + ":"
    for line in header_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith(prefix):
            return stripped[len(prefix):].strip()
    return ""


def generate_article(topic: str) -> dict:
    if not config.NVIDIA_API_KEY:
        raise RuntimeError("NVIDIA_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {config.NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.NVIDIA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write the tutorial article on: {topic}"},
        ],
        "temperature": 0.6,
        "max_tokens": 3000,
        # Nemotron's reasoning models "think" before answering (like DeepSeek-R1).
        # We don't need that for straightforward article writing - keeping it off
        # is faster and keeps the reasoning trace out of the output we're parsing.
        # NOTE: this must be a top-level field in the raw JSON body (not wrapped
        # in "extra_body" - that's an OpenAI Python-library-only convention that
        # doesn't mean anything to the raw REST API we're calling with `requests`).
        "chat_template_kwargs": {"enable_thinking": False},
    }

    resp = requests.post(
        f"{config.NVIDIA_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=180,
    )
    if not resp.ok:
        # Surface NVIDIA's actual error detail (not just "400 Bad Request") so
        # the Telegram digest tells you what's actually wrong.
        raise RuntimeError(f"NVIDIA API {resp.status_code}: {resp.text[:500]}")

    raw = resp.json()["choices"][0]["message"]["content"].strip()

    if "---BODY---" not in raw:
        raise ValueError(
            "Model output didn't contain the '---BODY---' marker - "
            f"got (first 300 chars): {raw[:300]!r}"
        )

    header_part, body_part = raw.split("---BODY---", 1)
    body_html = body_part.strip()

    title = _extract_field(header_part, "TITLE")
    description = _extract_field(header_part, "DESCRIPTION")
    tags_line = _extract_field(header_part, "TAGS")
    tags = [t.strip() for t in tags_line.split(",") if t.strip()]

    if not title:
        raise ValueError(f"Could not find TITLE in model output: {header_part!r}")
    if not body_html:
        raise ValueError("Body section was empty after the '---BODY---' marker")

    return {
        "title": title,
        "meta_description": description,
        "tags": tags,
        "body_html": body_html,
    }

"""
Calls your free NVIDIA model to generate one tutorial article as structured JSON.
"""
import json
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

Return ONLY valid JSON, no markdown code fences, with exactly these keys:
{
  "title": "...",
  "meta_description": "... (under 155 characters)",
  "tags": ["...", "...", "..."],
  "body_html": "..."
}
"""


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
        "max_tokens": 2500,
    }

    resp = requests.post(
        f"{config.NVIDIA_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()

    # Some models wrap JSON in ```json fences despite instructions - strip if present.
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    article = json.loads(raw)
    for key in ("title", "meta_description", "tags", "body_html"):
        if key not in article:
            raise ValueError(f"Model output missing required key: {key}")
    return article

"""
Central config. Everything is read from environment variables so the same
code works locally (via a .env file) and in GitHub Actions (via repo secrets).
Nothing sensitive is hard-coded here.
"""
import os

# --- NVIDIA (build.nvidia.com) ---
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

# IMPORTANT: model slugs on build.nvidia.com change over time and which ones
# are on the free tier changes too. Log into build.nvidia.com -> API Catalog,
# pick a current free/available chat model, and put its exact slug here
# (or override via the NVIDIA_MODEL env var / GitHub secret instead of editing this file).
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")

# --- Site (free GitHub Pages - no hosting cost) ---
# https://<your-username>.github.io/<your-repo-name>  - fill this in once you've
# created the repo and turned on Pages (Settings -> Pages -> Source: main / root).
# Only used to build the link shown in your Telegram digest - not required for
# publishing itself to work.
SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "")

# "draft" writes to _drafts/ (invisible to Jekyll/GitHub Pages until you move it) -
# use this for the first couple of weeks so nothing goes live unreviewed.
# "publish" writes straight to _posts/ (live as soon as it's committed).
POST_STATUS = os.environ.get("POST_STATUS", "draft")

# --- Telegram (your monitoring channel) ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# --- Pipeline behavior ---
ARTICLES_PER_RUN = int(os.environ.get("ARTICLES_PER_RUN", "1"))

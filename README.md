# Aero/CFD Content Agent

Autonomous pipeline: generates a technical tutorial article (your free NVIDIA
model) → writes it as a Jekyll post → GitHub Pages hosts the site for free →
sends you a Telegram digest so you can review in your 30-60 min/day.

**Total cost to run this: $0.** No hosting bill, no domain required to start.
Runs entirely on GitHub Actions' free scheduler, so it keeps working even
after your laptop is packed away for the move.

---

## What you need to set up once (do these in order)

### 1. NVIDIA API key (free)
- Go to build.nvidia.com, sign in, generate an API key.
- Free-tier model availability changes over time - open the API Catalog and pick
  a currently-available free chat/instruct model, then note its exact slug
  (e.g. `meta/llama-3.1-70b-instruct` is what this code defaults to, but **verify
  it's still valid** - swap it via the `NVIDIA_MODEL` secret if not).

### 2. A GitHub repo with Pages turned on (this is your free site)
- Create a new **public** repo (Pages' free tier needs public, unless you're on
  GitHub Pro), push everything in this folder to it.
- Go to **Settings → Pages** and set Source to "Deploy from a branch",
  branch `main`, folder `/ (root)`. Save.
- GitHub builds the Jekyll site (using `_config.yml`, `index.md`, `_posts/`)
  completely automatically - no build step needed in this repo at all, and no
  hosting account of any kind.
- Your site will be live at `https://<your-username>.github.io/<repo-name>/`
  within a minute or two. Once you know that URL, set it as the
  `SITE_BASE_URL` secret (step 4) so Telegram links are clickable.
- *(Later, once you have a bit of spare money, you can point a ~$10/year
  custom domain at this for free via a `CNAME` file - not required to start.)*

### 3. Telegram bot (your monitoring platform)
- Message **@BotFather** on Telegram, send `/newbot`, follow the prompts. You'll
  get a bot token - that's `TELEGRAM_BOT_TOKEN`.
- Message your new bot anything once (so it can see you), then visit
  `https://api.telegram.org/bot<token>/getUpdates` in a browser and find your
  numeric `chat.id` in the JSON - that's `TELEGRAM_CHAT_ID`.

### 4. Add the secrets
Go to **Settings → Secrets and variables → Actions → New repository secret**
and add each of: `NVIDIA_API_KEY`, `NVIDIA_BASE_URL`, `NVIDIA_MODEL`,
`SITE_BASE_URL`, `POST_STATUS` (set to `draft` to start), `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`, `ARTICLES_PER_RUN`.

Test it immediately: go to the **Actions** tab → "Daily Content Publish" →
**Run workflow** (the `workflow_dispatch` trigger), instead of waiting for the
scheduled time.

---

## How to run it locally first (recommended before trusting the Action)

```bash
pip install -r requirements.txt
cp .env.example .env      # fill in your real values
# then, on Windows PowerShell, load the .env into your session and run:
python run_pipeline.py
```

Check your Telegram for the digest, and look for a new file under `_drafts/`.

---

## The review habit (your 30-60 min/day)

Keep `POST_STATUS=draft` for at least the first couple of weeks. Every day:
1. Read the Telegram digest - it'll say "draft (needs review)" with a file path.
2. Open that file under `_drafts/` and fact-check it against what you actually
   know (this is exactly where your engineering background matters - catch
   anything the model got subtly wrong before it's public).
3. Fix anything wrong, add a date-prefixed filename (`YYYY-MM-DD-slug.md`),
   move it into `_posts/`, and commit + push. GitHub Pages rebuilds the site
   automatically within a minute or two.

Once you trust the output consistently, switch the `POST_STATUS` secret to
`publish` and it truly runs unattended - new posts go straight into `_posts/`
and are live immediately. Telegram digest becomes a pure status check rather
than a review queue.

---

## Monetization (add once you have ~15-20 solid posts live)
- **Google AdSense**: apply once the site has real content and a bit of
  traffic - a brand-new site with 2 posts usually gets rejected. Works fine on
  a `github.io` subdomain to start; a custom domain later can help approval
  odds and looks more credible to readers.
- **Amazon Associates**: add contextual affiliate links (ANSYS/engineering
  reference books, relevant hardware) into posts - can be done manually at
  first, or by extending `content_generator.py`'s prompt to leave a placeholder
  you fill in.

## Extending
- Add more rows to `topics.json` whenever the queue is running low (Telegram
  will warn you when it's empty).
- `ARTICLES_PER_RUN` can go above 1 once you're confident in quality and want
  to scale faster.

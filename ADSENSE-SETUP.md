# AdSense setup — Aero/CFD Notes

The site ships **AdSense-ready but ad-free** until you get approval — that's a
policy requirement, not a limitation (loading ad code on an unreviewed site
gets the application rejected).

## What's already wired

| Slot | Where | Renders when enabled |
|---|---|---|
| Auto-ads script (Google picks best placements) | `<head>` of every page | `{% if site.adsense_client %}` in `_layouts/default.html` |
| End-of-article "Sponsored" block | every post, under the body | `_layouts/post.html` |
| Homepage "Sponsored" band | between article grid and footer | `index.html` |

While `adsense_client` is empty in `_config.yml`, none of this renders —
the reserved `<div class="ad-slot" hidden>` keeps layout stable.

## Steps to turn ads on (15 min, after Google approves)

1. **Apply at https://adsense.google.com** — add either:
   - the short public mirror URL (`aeronotes.pages.dev`, preferred — it has its
     own hostname root, so `ads.txt` sits where Google checks), or
   - your own custom domain if you buy one (₹700–800/yr) — alternatively best.
   Use the live site with all 25 articles, not a parked page.
2. Verify ownership via the **meta tag method** if the CNAME/ads.txt method
   doesn't fit; GitHub Pages serves whatever file/text you commit.
3. Once approved, put your publisher id in `_config.yml`:
   ```yaml
   adsense_client: "ca-pub-XXXXXXXXXXXXXXXX"
   ```
4. Fill in the real line in `ads.txt` at the repo root:
   ```
   google.com, ca-pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
   ```
   (Delete the current placeholder comment-only file first — commit both
   changes in one commit and let the Pages build run.)
5. Check the site renders ads, then wait for first impressions. Realistic
   ramp: weeks of near-zero, then slow growth with traffic. RPM on technical
   content is decent but volume is small early.

## Important policy notes (from live research, 2026-10)

- `github.io` and `pages.dev` are Public-Suffix-List platforms; Google's
  published site rules allow adding such subdomains — approval still
  depends on content review, not hosting.
- **Project-URL ads.txt problem on github.io**: Google expects `ads.txt` at
  the hostname root (`username.github.io/ads.txt`), not inside the repo
  path. That's exactly why the `.pages.dev` mirror or a custom domain is the
  better AdSense identity for this site.
- Don't run ads alongside destructive layout: the two slots above are styled
  to sit between content, never to shift it (no layout-jump CLS penalty).

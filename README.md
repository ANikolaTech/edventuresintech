# Edventures in Tech website
Free site on GitHub Pages. A GitHub Action reads the podcast RSS feed every morning and updates the episode list, so new episodes appear with no human steps.
- `index.html` page design (Claude maintains)
- `config.json` guests, YouTube links, legacy episodes 1–52 (Claude maintains)
- `episodes.json` generated from the feed; do not edit by hand
- `build.py` feed reader; `.github/workflows/update.yml` the daily schedule

# Compact GitHub Pages picker

URL: https://iman-py.github.io/open-tv-atlas/

One page, static HTML/CSS/JavaScript. No backend, accounts, or third-party fonts. Assets are served by GitHub Pages; the current catalog and playlist URLs come from GitHub Raw. A bundled catalog is used if the live fetch fails.

The picker is optional: users can paste raw M3U links into their player directly. English is first and Farsi is second. Setup and the browser demo stay collapsed until requested.

## Preview

From the repository root:

```bash
python3 website/build_catalog.py index.json
python3 -m http.server 8765 --directory website/dist
```

Open http://localhost:8765/. `.github/workflows/pages.yml` deploys this directory to GitHub Pages after changes and successful daily playlist updates.

`dist/demo.webm` records actual browser interactions, not StreamVault playback. The sharing image is `dist/social-preview.png`.

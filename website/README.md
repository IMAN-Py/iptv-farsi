# Open TV Atlas website

Public URL: https://open-tv-atlas.vividtuna13.chatgpt.site/

This directory mirrors the static site's source and media. The Sites deployment checkout is separate from this repository. A GitHub push does not itself redeploy Sites.

The browser fetches the repository's `index.json` on every visit, so playlist selections use the latest daily collection. A bundled fallback is available if that request fails. Crawlable language pages and the fallback are snapshots rebuilt when the website is deployed; they link to the continuously refreshed M3U URLs.

## Preview

From the repository root:

```bash
python3 website/build_catalog.py index.json
python3 -m http.server 8765 --directory website/dist
```

Open http://localhost:8765/. The generator writes language pages, the directory, setup guide, sitemap, robots file, and catalog fallback into `dist/`. For publishing, use the Sites workflow with the retained project identity; never store source credentials in this repository.

`dist/demo.webm` records actual browser interactions. It does not depict StreamVault playback. `dist/social-preview.png` is the sharing image used in the website metadata.

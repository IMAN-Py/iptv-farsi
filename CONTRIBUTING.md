# Contributing

Thanks for helping make these playlists easier to use.

## Report a problem

Use the issue templates for broken streams, metadata errors, or suggestions. Include the playlist URL, channel ID, player, country, and what happened. Do not include private account credentials or access tokens.

The project builds on [iptv-org/iptv](https://github.com/iptv-org/iptv) and [iptv-org/database](https://github.com/iptv-org/database). Submit new public stream links or corrections to those projects using their contribution rules; this collection picks them up after the upstream data updates. Report generator and documentation bugs here.

## Work on the generator

1. Create a branch with a focused change.
2. Install `requirements.txt` in a virtual environment.
3. Add a regression test for a behavior change.
4. Run `python -m unittest discover -s tests`.
5. For generation changes, run `python iptv_builder.py --collection`, `python scripts/update_catalog.py`, and `python scripts/validate_collection.py`.
6. Explain the user-visible behavior and how you checked it in your pull request.

## Generated files

Do not hand-edit `.m3u` files, `index.json`, `DIRECTORY.md`, `CHANNELS.md`, language README files, or the marked generated blocks in the root README. The daily workflow will overwrite them. Change `iptv_builder.py` or `scripts/update_catalog.py` instead.

Keep the three original Farsi URLs and the Farsi-only feed rule intact. Source categories are not a promise about the currently airing programme. Do not describe structural validation as live stream verification, or inflate channel counts by counting alternative URLs as different channels.

No account secrets are needed to run tests or generate playlists. Be kind and specific in issues and reviews; Persian and English reports are welcome.

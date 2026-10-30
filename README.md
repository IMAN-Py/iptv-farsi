<p align="center"><img src="assets/banner.svg" alt="Open TV Atlas — live TV, in your language" width="100%"></p>

# Open TV Atlas — Free IPTV Playlists by Language & Category

**Live TV, in your language.** Free M3U playlists for hundreds of languages, sorted by category — sports, movies, news, music, kids and more — in HD and SD.

[![Update playlists](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/update-playlists.yml/badge.svg)](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/update-playlists.yml)
[![Tests](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/test.yml/badge.svg)](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-5eead4)](LICENSE)

**[Pick your language →](https://iman-py.github.io/open-tv-atlas/)** · [All languages & categories](DIRECTORY.md) · [فارسی](#farsi) · [Player setup](#setup) · [FAQ](FAQ.md) · [Report a problem](https://github.com/IMAN-Py/open-tv-atlas/issues/new/choose)

1. **Choose a language** in the [picker](https://iman-py.github.io/open-tv-atlas/) or the [directory](DIRECTORY.md).
2. **Copy the playlist link** — all channels, HD, or SD.
3. **Paste it into your player** — VLC, TiviMate, or any app that accepts an M3U URL.

No account, no installation, no backend: playlists are rebuilt daily from [iptv-org](https://github.com/iptv-org) and served from GitHub Pages.

<a id="english"></a>
## English — quick start

Paste this URL into the **M3U URL / Add Playlist** field of your player:

```text
https://iman-py.github.io/open-tv-atlas/playlists/eng/all.m3u
```

| English playlist | Copy this URL |
| --- | --- |
| All channels | `https://iman-py.github.io/open-tv-atlas/playlists/eng/all.m3u` |
| HD | `https://iman-py.github.io/open-tv-atlas/playlists/eng/hd.m3u` |
| SD / unknown | `https://iman-py.github.io/open-tv-atlas/playlists/eng/sd.m3u` |

**[English sports, movies, news, music, kids, and more →](playlists/eng/README.md)**

English lists include feeds whose source metadata lists English, including multilingual feeds. Looking for another language? Browse the [full directory](DIRECTORY.md), or use the Farsi links below.

<a id="farsi"></a>
## فارسی — شروع سریع

پلی‌لیست فارسی و لینک‌های قبلی آن همچنان به‌سادگی در دسترس هستند. لینک زیر را در بخش **M3U URL / Add Playlist** پلیر خود وارد کنید؛ برای استفاده نیازی به دانلود کد یا ساخت حساب ندارید.

```text
https://iman-py.github.io/open-tv-atlas/playlist.m3u
```

| نسخه فارسی | لینک قابل کپی در پلیر |
| --- | --- |
| همه کانال‌های فارسی | `https://iman-py.github.io/open-tv-atlas/playlist.m3u` |
| کیفیت HD | `https://iman-py.github.io/open-tv-atlas/playlist_hd.m3u` |
| کیفیت SD یا نامشخص | `https://iman-py.github.io/open-tv-atlas/playlist_sd.m3u` |

**[ورزش، فیلم، اخبار، موسیقی و دسته‌بندی‌های فارسی ←](playlists/fas/README.md)** · **[فهرست کانال‌های فارسی](CHANNELS.md)**

کانال‌های فارسی فقط از فیدهایی انتخاب می‌شوند که زبان آن‌ها در منبع داده صرفاً فارسی است. لینک‌های قدیمی فارسی تغییر نکرده‌اند. پلی‌لیست‌ها هر روز برای به‌روزرسانی زمان‌بندی شده‌اند؛ پخش زنده همه لینک‌ها تضمین نمی‌شود.

<!-- playlist-stats:start -->
**210 languages · 29 categories**

**English: 2490 channels · 4466 stream entries · 3342 HD · 1124 SD / unknown**

**Farsi: 192 channels · 219 stream entries · 73 HD · 146 SD / unknown**

Counts describe playlist entries, not verified live streams.
<!-- playlist-stats:end -->

<a id="browse"></a>
## Find your playlist

1. **Choose your language** in the [playlist directory](DIRECTORY.md).
2. Open its page for **all channels, HD, SD, and available categories**.
3. Copy the URL into your player and refresh the playlist when needed.

<!-- featured-playlists:start -->
### Language shortcuts

| Language | All | HD | SD / unknown | Categories |
| --- | --- | --- | --- | --- |
| [English](playlists/eng/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/sd.m3u) | [Browse](playlists/eng/README.md#categories) |
| [فارسی · Farsi / Persian](playlists/fas/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/sd.m3u) | [Browse](playlists/fas/README.md#categories) |
| [Arabic](playlists/ara/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/ara/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/ara/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/ara/sd.m3u) | [Browse](playlists/ara/README.md#categories) |
| [Turkish](playlists/tur/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/tur/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/tur/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/tur/sd.m3u) | [Browse](playlists/tur/README.md#categories) |
| [Kurdish](playlists/kur/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/kur/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/kur/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/kur/sd.m3u) | [Browse](playlists/kur/README.md#categories) |
| [Pashto](playlists/pus/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/pus/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/pus/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/pus/sd.m3u) | [Browse](playlists/pus/README.md#categories) |
| [Urdu](playlists/urd/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/urd/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/urd/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/urd/sd.m3u) | [Browse](playlists/urd/README.md#categories) |
| [Hindi](playlists/hin/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/hin/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/hin/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/hin/sd.m3u) | [Browse](playlists/hin/README.md#categories) |
| [Spanish](playlists/spa/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/spa/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/spa/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/spa/sd.m3u) | [Browse](playlists/spa/README.md#categories) |
| [French](playlists/fra/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fra/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fra/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fra/sd.m3u) | [Browse](playlists/fra/README.md#categories) |
| [German](playlists/deu/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/deu/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/deu/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/deu/sd.m3u) | [Browse](playlists/deu/README.md#categories) |
| [Russian](playlists/rus/README.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/rus/all.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/rus/hd.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/rus/sd.m3u) | [Browse](playlists/rus/README.md#categories) |

**[Browse every language →](DIRECTORY.md)**

### Category shortcuts

| Category | English | Farsi only | All languages |
| --- | --- | --- | --- |
| [Sports · ورزش](categories/sports.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/sports.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/sports.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/sports.m3u) |
| [Movies · فیلم](categories/movies.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/movies.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/movies.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/movies.m3u) |
| [News · اخبار](categories/news.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/news.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/news.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/news.m3u) |
| [Music · موسیقی](categories/music.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/music.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/music.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/music.m3u) |
| [Kids · کودک](categories/kids.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/kids.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/kids.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/kids.m3u) |
| [Documentary · مستند](categories/documentary.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/documentary.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/documentary.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/documentary.m3u) |
| [Series · سریال](categories/series.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/series.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/series.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/series.m3u) |
| [Entertainment · سرگرمی](categories/entertainment.md) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/eng/entertainment.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/playlists/fas/entertainment.m3u) | [M3U](https://iman-py.github.io/open-tv-atlas/categories/entertainment.m3u) |

Open a language page for category links in that language. A dash means no matching entries are available.
<!-- featured-playlists:end -->

Category lists contain channels tagged with that category by the source. A sports list is a list of sports channels, not an event schedule. A movie list contains live movie channels, not an on-demand movie library. Languages other than Farsi can include multilingual feeds that list the selected language.

## Why use this collection?

- **Combine language and category.** Pick English sports, Arabic movies, or Farsi music when available.
- **Keep your existing Farsi setup.** The original three playlist URLs remain supported.
- **See what is included.** Generated directories show real entry counts and available categories.
- **Choose your quality.** Every language has HD and SD / unknown variants; reported stream quality takes priority over URL hints.
- **Updates include the directory.** Daily automation rebuilds playlists and documentation from the same data.
- **Open and reproducible.** Source code, tests, and a machine-readable [playlist index](index.json) are included.

<a id="setup"></a>
## Start watching

| Player | What to do |
| --- | --- |
| **[StreamVault](https://github.com/Davidona/StreamVault-IPTV) — suggested for Android TV** | Add an M3U source and paste a playlist URL from this repository. |
| VLC desktop | Open a network stream, paste the playlist URL, and play. |
| TiviMate / IPTV Smarters / other IPTV players | Add a playlist, choose M3U URL, paste a link, then refresh channels. |
| Android TV / Apple TV | Use an app that supports M3U playlist URLs and add the same link. |

### Android TV: StreamVault

We suggest **[StreamVault](https://github.com/Davidona/StreamVault-IPTV)** for Android TV. It is a free player designed for TV remotes and supports M3U playlist URLs.

1. Get the app from its **[official GitHub releases](https://github.com/Davidona/StreamVault-IPTV/releases/latest)** and install it on your Android TV device.
2. Choose an M3U source and paste an [English playlist](playlists/eng/README.md), a [Farsi playlist](playlists/fas/README.md), or another link from the [directory](DIRECTORY.md).
3. Let the playlist load, then browse the live channels and categories.

برای اندروید تی‌وی، **[StreamVault](https://github.com/Davidona/StreamVault-IPTV)** را پیشنهاد می‌کنیم. پس از نصب، منبع M3U را انتخاب کنید و لینک پلی‌لیست فارسی یا زبان دلخواه را وارد کنید.

**Use the raw URL**, starting with `https://raw.githubusercontent.com/`, rather than a GitHub file-view page. Player support and menu names vary. When one stream fails, try another stream for the same channel; availability depends on the broadcaster and your region.

If raw GitHub is unreachable, try this alternative for the Farsi list. CDN caching may delay updates:

```text
https://cdn.jsdelivr.net/gh/IMAN-Py/open-tv-atlas@main/playlist.m3u
```

See the [FAQ](FAQ.md) for missing channels, quality labels, TV guides, and troubleshooting.

## Updates and data

Updates are scheduled daily at **06:00 UTC / 09:30 Tehran**. GitHub can delay scheduled runs; the [latest workflow result](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/update-playlists.yml) shows whether a refresh succeeded. A refresh rebuilds metadata and playlists; it does **not** test playback of every stream.

This is an independent project built on [iptv-org/iptv](https://github.com/iptv-org/iptv), [iptv-org/database](https://github.com/iptv-org/database), and the [iptv-org API](https://github.com/iptv-org/api). This project is not affiliated with iptv-org.

Feeds are matched by channel **and feed ID**. Streams without a feed ID use the channel's main feed. Streams with missing language metadata or unmatched feed IDs are omitted. Category pages are generated only when matching entries exist; unclassified channels remain in their language's all/HD/SD lists.

## Build it yourself

Python 3.12 or newer is recommended.

```bash
git clone https://github.com/IMAN-Py/open-tv-atlas.git
cd open-tv-atlas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests

# Rebuild all languages, categories, and the three original Farsi URLs
python iptv_builder.py --collection
python scripts/update_catalog.py
python scripts/validate_collection.py
```

To build just one language without downloading the full channel catalog:

```bash
python iptv_builder.py --lang fas --output playlist.m3u
python iptv_builder.py --lang eng --output english.m3u
```

The single-language command also creates `_hd.m3u` and `_sd.m3u` variants. `playlists/`, `categories/`, `DIRECTORY.md`, `CHANNELS.md`, and `index.json` are generated; see [CONTRIBUTING.md](CONTRIBUTING.md) before editing them.

## Help make it better

Found a broken stream or confusing setup step? [Open an issue](https://github.com/IMAN-Py/open-tv-atlas/issues/new/choose). Corrections, tests, and documentation improvements are welcome. See the [contribution guide](CONTRIBUTING.md).

**If this saves you time, star the repository so you can find it again, and share the playlist directory with someone who would use it.**

## Repository traffic

<!-- cumulative-traffic -->
[![Views in the last 14 days](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FIMAN-Py%2Fopen-tv-atlas%2Fmain%2F.github%2Ftraffic%2Fviews-14d.json)](https://github.com/IMAN-Py/open-tv-atlas/blob/main/.github/traffic/history.json)
[![Clones in the last 14 days](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FIMAN-Py%2Fopen-tv-atlas%2Fmain%2F.github%2Ftraffic%2Fclones-14d.json)](https://github.com/IMAN-Py/open-tv-atlas/blob/main/.github/traffic/history.json)

Views and clones over the last 14 days come straight from GitHub’s traffic API and are refreshed periodically
from the maintainer’s Mac; the full archive lives in [`history.json`](.github/traffic/history.json). These badges include
automated activity (CI, mirrors, scanners) and may lag by a few hours.
<!-- /cumulative-traffic -->

## License and content

The generator and documentation are [MIT licensed](LICENSE). Video streams are hosted by third parties; this repository hosts playlist text, not video. The code license grants no rights to third-party broadcasts. For a content concern, open an issue with the channel ID and affected URL.

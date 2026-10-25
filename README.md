# IPTV فارسی

پلی‌لیست رایگان کانال‌های **فقط فارسی** برای VLC، TiviMate، IPTV Smarters و هر پلیر M3U.

منبع داده: [iptv-org](https://github.com/iptv-org). این پروژه خودِ استریم‌ها را میزبانی نمی‌کند؛ لینک‌های عمومی را جمع می‌کند و هر روز به‌روز می‌شود.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Playlists](https://img.shields.io/badge/playlists-Farsi%20only-blue)](#استفاده-سریع)
[![Update](https://github.com/IMAN-Py/iptv-farsi/actions/workflows/update-playlists.yml/badge.svg)](https://github.com/IMAN-Py/iptv-farsi/actions/workflows/update-playlists.yml)

---

## استفاده سریع

یکی از این لینک‌ها را در پلیر IPTV اضافه کنید:

| پلی‌لیست | لینک |
| --- | --- |
| همه کانال‌های فارسی | `https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist.m3u` |
| فقط HD | `https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist_hd.m3u` |
| فقط SD | `https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist_sd.m3u` |

اگر پلیر لینک GitHub را باز نکرد، از این نسخه استفاده کنید:

`https://cdn.jsdelivr.net/gh/IMAN-Py/iptv-farsi@main/playlist.m3u`

---

## نصب در پلیرها

### VLC
1. Media → Open Network Stream
2. لینک پلی‌لیست را بچسبانید
3. Play

### TiviMate / IPTV Smarters / GSE / OTT Navigator
1. Add Playlist → M3U URL
2. یکی از لینک‌های بالا را وارد کنید
3. نام دلخواه بگذارید، مثلاً `Farsi IPTV`

### اپل تی‌وی / اندروید تی‌وی
همان لینک M3U را در اپلیکیشن IPTV دستگاه اضافه کنید. نیازی به دانلود فایل نیست.

---

## ساخت دوباره روی سیستم خودتان

```bash
git clone https://github.com/IMAN-Py/iptv-farsi.git
cd iptv-farsi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python iptv_builder.py --lang fas --output playlist.m3u
```

خروجی:

- `playlist.m3u` — همه استریم‌های فارسی
- `playlist_hd.m3u` — کیفیت ۷۲۰p به بالا
- `playlist_sd.m3u` — بقیه

فقط کانال‌هایی که زبان‌شان **صرفاً فارسی (`fas`)** است وارد لیست می‌شوند، نه کانال‌های چندزبانه.

---

## English

Free **Farsi-only** IPTV playlists. Add one URL to any M3U player.

- All: https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist.m3u
- HD: https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist_hd.m3u
- SD: https://raw.githubusercontent.com/IMAN-Py/iptv-farsi/main/playlist_sd.m3u

Playlists are rebuilt daily from [iptv-org](https://github.com/iptv-org). This repo does not host video streams.

```bash
pip install -r requirements.txt
python iptv_builder.py --lang fas
```

---

## سلب مسئولیت

کانال‌ها ممکن است قطع شوند، جابه‌جا شوند یا در بعضی کشورها در دسترس نباشند. استفاده از محتوا باید مطابق قوانین محلی باشد. این پروژه وابسته به جامعه iptv-org است.

## مجوز

[MIT](LICENSE)

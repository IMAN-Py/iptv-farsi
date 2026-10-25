# Frequently asked questions

[← Back to playlists](README.md)

### Which link should I use for English?

Use `https://raw.githubusercontent.com/IMAN-Py/open-tv-atlas/main/playlists/eng/all.m3u`. For sports, movies, news, or another category, open the [English page](playlists/eng/README.md).

### Which link should I use for Farsi?

Use `https://raw.githubusercontent.com/IMAN-Py/open-tv-atlas/main/playlist.m3u`. The original Farsi links are preserved. For only sports, movies, or another category, open the [Farsi page](playlists/fas/README.md).

### How do I find another language?

Open the [directory](DIRECTORY.md), choose a language, then copy its all-channels or category URL. Available languages and categories come from source metadata and are rebuilt automatically.

### Why is a language or category missing?

There may be no matching stream with usable language/feed metadata. Empty category lists are not advertised. A general channel that sometimes shows sport is not automatically a sports channel: categories come from iptv-org's channel database, not the current programme.

### Are all streams tested and working?

No. A successful refresh means the data downloaded and the collection passed structural checks. Broadcasters can change URLs, restrict regions, or go off air. Entry counts are not a count of verified working channels. Try another stream, refresh your playlist, and include the affected URL when reporting a failure.

### Why can a channel appear more than once?

One channel can have several stream URLs or qualities. Duplicate channel-and-URL pairs are removed within each playlist, but alternative streams remain. A multilingual feed can appear in more than one language list. Farsi lists are stricter: only feeds marked exclusively `fas` are included.

### What does HD mean?

HD means a reported vertical resolution of at least 720 pixels, or an explicit HD/FHD/UHD/4K/8K label. When quality is absent, the generator uses available dimensions or URL hints. SD lists also include unknown quality. This is classification, not a measurement of playback resolution or bitrate.

### Can I watch a specific match or movie?

This project organizes live channels. It does not promise particular events, provide an on-demand catalog, or unlock subscription content.

### Does this include a programme guide (EPG)?

Not currently. Playlists preserve upstream channel IDs in `tvg-id`, which can help a compatible player match an external guide. The [iptv-org EPG project](https://github.com/iptv-org/epg) is a separate reference; guide coverage and exact ID matching depend on the provider.

### Why is yesterday's playlist still showing?

Refresh the playlist inside your player. Check the [update workflow](https://github.com/IMAN-Py/open-tv-atlas/actions/workflows/update-playlists.yml) for failures or delays. Players and CDNs can cache files, and a successful run may have nothing new to commit.

### Can I report a wrong channel name, category, or language?

Yes. Include the channel ID and playlist URL in an [issue](https://github.com/IMAN-Py/open-tv-atlas/issues/new/choose). Upstream metadata corrections belong in [iptv-org/database](https://github.com/iptv-org/database); broken stream URLs belong in [iptv-org/iptv](https://github.com/iptv-org/iptv). Fixes to this generator belong here.

### آیا نسخه فارسی همچنان مستقل است؟

بله. سه لینک قبلی فارسی بدون تغییر باقی مانده‌اند. دسته‌بندی‌های فارسی در صفحه مخصوص فارسی در دسترس هستند و اضافه شدن زبان‌های دیگر، محتوای این لینک‌ها را چندزبانه نمی‌کند.

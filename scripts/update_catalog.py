"""Generate navigation and honest playlist counts from published output."""
import argparse
from collections import defaultdict
import html
import json
from pathlib import Path
import re

RAW = 'https://iman-py.github.io/open-tv-atlas/'
FEATURED = ['eng', 'fas', 'ara', 'tur', 'kur', 'pus', 'urd', 'hin', 'spa', 'fra', 'deu', 'rus']
CATEGORIES = ['sports', 'movies', 'news', 'music', 'kids', 'documentary', 'series', 'entertainment']
PERSIAN = {'sports': 'ورزش', 'movies': 'فیلم', 'news': 'اخبار', 'music': 'موسیقی', 'kids': 'کودک',
           'documentary': 'مستند', 'series': 'سریال', 'entertainment': 'سرگرمی', 'general': 'عمومی',
           'business': 'اقتصاد', 'classic': 'کلاسیک', 'comedy': 'کمدی', 'cooking': 'آشپزی',
           'culture': 'فرهنگ', 'education': 'آموزش', 'family': 'خانواده', 'lifestyle': 'سبک زندگی',
           'religious': 'مذهبی'}


def read_entries(path):
    entries = []
    pending = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('#EXTINF:'):
            pending = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
        elif line and not line.startswith('#') and pending is not None:
            pending['url'] = line
            entries.append(pending)
            pending = None
    return entries


def cell(value):
    return html.escape(str(value)).replace('|', '&#124;').replace('\n', ' ')


def label(code, name):
    return 'فارسی · Farsi / Persian' if code == 'fas' else cell(name)


def link(item, text='M3U'):
    return f'[{text}]({RAW}{item["path"]})' if item['streams'] else '—'


def replace_block(contents, key, body):
    start, end = f'<!-- {key}:start -->', f'<!-- {key}:end -->'
    if contents.count(start) != 1 or contents.count(end) != 1:
        raise ValueError(f'Expected exactly one {key} block')
    before, rest = contents.split(start)
    _, after = rest.split(end)
    return before + start + '\n' + body + '\n' + end + after


def channel_table(entries):
    grouped = defaultdict(list)
    for entry in entries:
        grouped[entry['tvg-id']].append(entry)
    lines = ['| Channel | Channel ID | Reported quality | Streams |', '| --- | --- | --- | ---: |']
    for channel, rows in sorted(grouped.items(), key=lambda item: item[1][0].get('tvg-name', item[0]).casefold()):
        name = rows[0].get('tvg-name') or channel
        qualities = ', '.join(sorted({r.get('tvg-quality') or 'Unknown' for r in rows}))
        lines.append(f'| {cell(name)} | {cell(channel)} | {cell(qualities)} | {len(rows)} |')
    return lines


def update_catalog(root):
    index = json.loads((root / 'index.json').read_text(encoding='utf-8'))
    languages = {item['code']: item for item in index['languages']}
    categories = {item['id']: item for item in index['categories']}
    farsi = languages['fas']
    summaries = [f'**{len(languages)} languages · {len(categories)} categories**']
    for code, title in [('eng', 'English'), ('fas', 'Farsi')]:
        if code in languages:
            item = languages[code]
            summaries.append(f'**{title}: {item["all"]["channels"]} channels · {item["all"]["streams"]} stream entries '
                             f'· {item["hd"]["streams"]} HD · {item["sd"]["streams"]} SD / unknown**')
    summaries.append('Counts describe playlist entries, not verified live streams.')
    stats = '\n\n'.join(summaries)
    featured = ['### Language shortcuts', '', '| Language | All | HD | SD / unknown | Categories |', '| --- | --- | --- | --- | --- |']
    for code in FEATURED:
        if code not in languages:
            continue
        item = languages[code]
        featured.append(f'| [{label(code, item["name"])}](playlists/{code}/README.md) | {link(item["all"])} | '
                        f'{link(item["hd"])} | {link(item["sd"])} | [Browse](playlists/{code}/README.md#categories) |')
    featured += ['', '**[Browse every language →](DIRECTORY.md)**', '', '### Category shortcuts', '',
                 '| Category | English | Farsi only | All languages |', '| --- | --- | --- | --- |']
    fc = {item['id']: item for item in farsi['categories']}
    ec = {item['id']: item for item in languages.get('eng', {}).get('categories', [])}
    for category in CATEGORIES:
        if category in categories:
            featured.append(f'| [{category.title()} · {PERSIAN[category]}](categories/{category}.md) | {link(ec[category]) if category in ec else "—"} | {link(fc[category]) if category in fc else "—"} | {link(categories[category])} |')
    featured += ['', 'Open a language page for category links in that language. A dash means no matching entries are available.']
    readme = root / 'README.md'
    contents = readme.read_text(encoding='utf-8')
    contents = replace_block(contents, 'playlist-stats', stats)
    contents = replace_block(contents, 'featured-playlists', '\n'.join(featured))
    readme.write_text(contents, encoding='utf-8')

    directory = ['# Playlist directory · راهنمای پلی‌لیست‌ها', '', '[← Quick start](README.md) · [فارسی](playlists/fas/README.md)', '',
                 stats, '', 'Choose a language to see copyable URLs, categories, and channel names. '
                 'Farsi lists contain only exclusively Farsi feeds; other languages may include multilingual feeds. '
                 'Categories and languages follow upstream metadata. Empty quality variants are shown as a dash.', '',
                 '## Languages', '', '| Language | Code | Channels | Stream entries | All | HD | SD / unknown |',
                 '| --- | --- | ---: | ---: | --- | --- | --- |']
    for item in index['languages']:
        code = item['code']
        directory.append(f'| [{label(code, item["name"])}](playlists/{code}/README.md) | `{code}` | {item["all"]["channels"]} | '
                         f'{item["all"]["streams"]} | {link(item["all"])} | {link(item["hd"])} | {link(item["sd"])} |')
        page = [f'# {label(code, item["name"])} IPTV Playlist — Free Live TV M3U', '', '[← All languages](../../DIRECTORY.md) · [Player setup](../../README.md#setup)', '',
                f'Find free {cell(item["name"])} live TV playlist URLs for M3U-compatible players such as VLC and TiviMate. '
                'Choose all channels, HD, SD, or a category below. Playlist links are refreshed daily from iptv-org; '
                'individual streams may be unavailable or region restricted.', '',
                f'**{item["all"]["channels"]} channels · {item["all"]["streams"]} stream entries**', '',
                'Copy this URL into the M3U URL field of your player:', '', '```text', RAW + item['all']['path'], '```', '',
                '| Version | Entries | Copy this URL |', '| --- | ---: | --- |']
        for variant, name in [('all', 'All channels'), ('hd', 'HD'), ('sd', 'SD / unknown')]:
            info = item[variant]
            page.append(f'| {name} | {info["streams"]} | `{RAW}{info["path"]}` |' if info['streams'] else f'| {name} | 0 | No matching streams |')
        if code == 'fas':
            page += ['', 'لینک‌های اصلی فارسی بدون تغییر باقی مانده‌اند: [همه](../../playlist.m3u)، [HD](../../playlist_hd.m3u)، [SD](../../playlist_sd.m3u). '
                     'برای استفاده در پلیر، لینک کامل جدول بالا را کپی کنید. فقط فیدهای تک‌زبانه فارسی در این صفحه قرار دارند.']
        page += ['', '<a id="categories"></a>', '## Categories', '',
                 'Each list combines this language with a source category. Counts are stream entries; '
                 'channels may have alternative streams. Categories describe channels, not individual programmes.', '']
        if item['categories']:
            page += ['| Category | Channels | Entries | Copy this URL |', '| --- | ---: | ---: | --- |']
            for cat in sorted(item['categories'], key=lambda c: (CATEGORIES.index(c['id']) if c['id'] in CATEGORIES else 100, c['id'])):
                title = cat['id'].title()
                if code == 'fas' and cat['id'] in PERSIAN:
                    title += ' · ' + PERSIAN[cat['id']]
                page.append(f'| {title} | {cat["channels"]} | {cat["streams"]} | `{RAW}{cat["path"]}` |')
        else:
            page.append('No categorized streams are available for this language. Use the all-channels list above.')
        page += ['', '## Included channels', '', 'Availability is not verified. Use your browser’s Find command to search this table.', '']
        page += channel_table(read_entries(root / item['all']['path']))
        (root / f'playlists/{code}/README.md').write_text('\n'.join(page) + '\n', encoding='utf-8')
    directory += ['', '## Categories across all languages', '', 'For a language-specific category, open its language page above.', '',
                  '| Category | Channels | Stream entries | Copy this URL |', '| --- | ---: | ---: | --- |']
    for item in index['categories']:
        category = item['id']
        directory.append(f'| [{category.title()}](categories/{category}.md) | {item["channels"]} | {item["streams"]} | `{RAW}{item["path"]}` |')
        page = [f'# Free {category.title()} IPTV Playlist — M3U Links by Language', '',
                '[← All playlists](../DIRECTORY.md) · [Player setup](../README.md#setup)', '',
                f'Browse live {category} channels from the iptv-org collection. '
                'Use the worldwide M3U playlist or choose a language below. '
                'English appears first, followed by Farsi, then the other available languages.', '',
                f'**{item["channels"]} channels · {item["streams"]} stream entries**', '',
                '## All languages', '', 'Copy this URL into your player’s M3U playlist field:', '',
                '```text', RAW + item['path'], '```', '',
                '## Choose a language', '', '| Language | Channels | Entries | Copy this URL |', '| --- | ---: | ---: | --- |']
        for language in index['languages']:
            matching = next((cat for cat in language['categories'] if cat['id'] == category), None)
            if matching:
                code = language['code']
                page.append(f'| [{label(code, language["name"])}](../playlists/{code}/README.md) | {matching["channels"]} | '
                            f'{matching["streams"]} | `{RAW}{matching["path"]}` |')
        page += ['', '## How to use this playlist', '',
                 '1. Copy the full URL for all languages or your preferred language.',
                 '2. In VLC, open a network stream; in an IPTV player, add an M3U playlist URL.',
                 '3. Refresh the playlist periodically to pick up source changes.', '',
                 f'Categories describe channels tagged as **{category}** in upstream metadata, '
                 'not the programme airing right now. These are live channel links, not an on-demand library or an event guarantee. '
                 'Counts include alternative streams and do not mean every link has been playback-tested.', '',
                 'Source: [iptv-org](https://github.com/iptv-org/iptv). '
                 'For playback or metadata problems, see the [FAQ](../FAQ.md) or '
                 '[report an issue](https://github.com/IMAN-Py/open-tv-atlas/issues/new/choose).']
        (root / f'categories/{category}.md').write_text('\n'.join(page) + '\n', encoding='utf-8')
    (root / 'DIRECTORY.md').write_text('\n'.join(directory) + '\n', encoding='utf-8')
    channel_doc = ['# Farsi channel directory · فهرست کانال‌های فارسی', '',
                   '[← Farsi playlists and categories](playlists/fas/README.md) · [Other languages](DIRECTORY.md)', '', stats, '',
                   'Generated from the published Farsi playlist. Alternative stream URLs can belong to the same channel. '
                   'Reported quality and presence in this list do not guarantee playback.', '']
    channel_doc += channel_table(read_entries(root / 'playlist.m3u'))
    (root / 'CHANNELS.md').write_text('\n'.join(channel_doc) + '\n', encoding='utf-8')
    for path in (root / 'playlists').glob('*/README.md'):
        if path.parent.name not in languages:
            path.unlink()
    for path in (root / 'categories').glob('*.md'):
        if path.stem not in categories:
            path.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    update_catalog(parser.parse_args().root)

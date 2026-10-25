#!/usr/bin/env python3
"""Build worldwide IPTV playlists by language, category, and quality."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import StringIO
import json
import logging
from pathlib import Path
import re

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_FEEDS_URL = 'https://raw.githubusercontent.com/iptv-org/database/master/data/feeds.csv'
DEFAULT_STREAMS_URL = 'https://iptv-org.github.io/api/streams.json'
DEFAULT_CHANNELS_URL = 'https://iptv-org.github.io/api/channels.json'
DEFAULT_LANGUAGES_URL = 'https://iptv-org.github.io/api/languages.json'
DEFAULT_LANG = 'fas'
DEFAULT_OUTPUT = 'playlist.m3u'
REQUEST_TIMEOUT = 30
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def fetch_dataframe(url: str, file_type: str = 'csv') -> pd.DataFrame:
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=retry))
        response = session.get(url, headers={'User-Agent': 'OpenTVAtlas/3.0'}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    if file_type == 'csv':
        return pd.read_csv(StringIO(response.text))
    if file_type == 'json':
        return pd.DataFrame(response.json())
    raise ValueError(f'Unsupported file type: {file_type}')


def is_stream_hd(height: object, width: object, quality: str, url: str) -> bool:
    """Prefer reported resolution; use URL hints only if quality is unknown."""
    resolution = re.search(r'(\d{3,4})[pi]?', quality.lower())
    if resolution:
        return int(resolution.group(1)) >= 720
    if quality.lower() in {'sd', 'hd', 'fhd', 'uhd', '4k', '8k'}:
        return quality.lower() != 'sd'
    for value, threshold in ((height, 720), (width, 1280)):
        try:
            if float(value) >= threshold:
                return True
        except (ValueError, TypeError):
            pass
    return bool(re.search(r'(?:^|[/_.-])(?:hd|fhd|uhd|720p?|1080p?|2160p?|4k)(?:[/_.-]|$)', url.lower()))


def clean(value: object) -> str:
    return str(value).replace('"', "'").replace('\r', ' ').replace('\n', ' ').strip()


@dataclass(frozen=True)
class Entry:
    channel: str
    name: str
    url: str
    languages: tuple[str, ...]
    categories: tuple[str, ...]
    quality: str
    hd: bool
    user_agent: str = ''
    referrer: str = ''


def prepare_entries(feeds, streams, channels=None, include_offline=False):
    if not {'channel', 'languages'}.issubset(feeds.columns):
        raise ValueError('Feed metadata must include channel and languages')
    if not {'channel', 'url'}.issubset(streams.columns):
        raise ValueError('Stream metadata must include channel and url')
    if not include_offline and 'status' in streams.columns:
        streams = streams[streams['status'] != 'offline']
    if 'feed' in streams.columns and 'id' in feeds.columns:
        has_feed = streams['feed'].fillna('').ne('')
        exact = pd.merge(streams[has_feed], feeds, left_on=['channel', 'feed'],
                         right_on=['channel', 'id'], how='inner', suffixes=('_stream', '_feed'))
        main = feeds[feeds['is_main'].astype(str).str.lower().eq('true')] if 'is_main' in feeds else feeds.iloc[:0]
        fallback = pd.merge(streams[~has_feed], main, on='channel', how='inner', suffixes=('_stream', '_feed'))
        merged = pd.concat([exact, fallback], ignore_index=True)
    else:
        merged = pd.merge(streams, feeds, on='channel', how='inner', suffixes=('_stream', '_feed'))
    # Object dtype permits empty strings in optional numeric fields on pandas 3.
    merged = merged.astype(object).where(pd.notna(merged), '')
    metadata = {}
    if channels is not None:
        if not {'id', 'name', 'categories'}.issubset(channels.columns):
            raise ValueError('Channel metadata must include id, name, and categories')
        metadata = {r['id']: r for r in channels.to_dict('records')}
    entries = []
    seen = set()
    for row in merged.to_dict('records'):
        channel, url = clean(row['channel']), str(row['url']).strip()
        languages = tuple(sorted({p.strip() for p in str(row['languages']).split(';') if re.fullmatch(r'[a-z]{3}', p.strip())}))
        if not channel or not languages or not url.startswith(('http://', 'https://')) or '\n' in url or '\r' in url:
            continue
        key = (channel, url, languages)
        if key in seen:
            continue
        seen.add(key)
        info = metadata.get(channel, {})
        categories = info.get('categories', [])
        categories = tuple(sorted(c for c in categories if re.fullmatch(r'[a-z]+', c))) if isinstance(categories, list) else ()
        name = clean(info.get('name') or row.get('title') or channel)
        quality = clean(row.get('quality') or row.get('format') or '')
        entries.append(Entry(channel, name, url, languages, categories, quality,
                             is_stream_hd(row.get('height'), row.get('width'), quality, url),
                             clean(row.get('user_agent', '')), clean(row.get('referrer', ''))))
    return sorted(entries, key=lambda e: (e.name.casefold(), e.channel, e.url, e.languages))


def select_language(entries, lang):
    # Preserve the original promise: Farsi lists contain Farsi-only feeds.
    selected = {}
    for entry in entries:
        matches = entry.languages == ('fas',) if lang == 'fas' else lang in entry.languages
        if matches:
            selected.setdefault((entry.channel, entry.url), entry)
    return list(selected.values())


def render_playlist(entries):
    lines = ['#EXTM3U']
    seen = set()
    for e in entries:
        if (e.channel, e.url) in seen:
            continue
        seen.add((e.channel, e.url))
        group = ';'.join(c.title() for c in e.categories) or 'Uncategorized'
        lines.append(f'#EXTINF:-1 tvg-id="{e.channel}" tvg-name="{e.name}" group-title="{group}" '
                     f'tvg-language="{";".join(e.languages)}" tvg-quality="{e.quality}",{e.name}')
        if e.user_agent:
            lines.append(f'#EXTVLCOPT:http-user-agent={e.user_agent}')
        if e.referrer:
            lines.append(f'#EXTVLCOPT:http-referrer={e.referrer}')
        lines.extend([e.url, ''])
    return '\n'.join(lines) + '\n'


def write_outputs(root, outputs):
    for name, contents in outputs.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding='utf-8')


def build_playlist(lang=DEFAULT_LANG, output_file=DEFAULT_OUTPUT, feeds_url=DEFAULT_FEEDS_URL,
                   streams_url=DEFAULT_STREAMS_URL, include_offline=False):
    feeds = fetch_dataframe(feeds_url)
    streams = fetch_dataframe(streams_url, 'json')
    entries = select_language(prepare_entries(feeds, streams, include_offline=include_offline), lang)
    if not entries:
        raise ValueError(f'No streams for {lang}; keeping existing playlists')
    path = Path(output_file)
    outputs = {path.name: render_playlist(entries),
               f'{path.stem}_hd{path.suffix}': render_playlist([e for e in entries if e.hd]),
               f'{path.stem}_sd{path.suffix}': render_playlist([e for e in entries if not e.hd])}
    write_outputs(path.parent, outputs)
    logging.info('Generated %s stream entries for %s', len(entries), lang)


def collection_outputs(entries, language_names):
    """Render the whole collection before replacing any published file."""
    farsi = select_language(entries, 'fas')
    if not farsi:
        raise ValueError('No Farsi streams; refusing to replace the published collection')
    outputs = {}
    index = {'languages': [], 'categories': []}

    def add(path, selected):
        text = render_playlist(selected)
        outputs[path] = text
        return {'path': path, 'streams': text.count('#EXTINF:'),
                'channels': len({e.channel for e in selected})}

    codes = sorted({code for e in entries for code in e.languages},
                   key=lambda c: (0 if c == 'eng' else 1 if c == 'fas' else 2,
                                  language_names.get(c, c).casefold()))
    for code in codes:
        selected = select_language(entries, code)
        if not selected:
            continue
        prefix = f'playlists/{code}'
        item = {'code': code, 'name': language_names.get(code, code), 'categories': []}
        item['all'] = add(f'{prefix}/all.m3u', selected)
        item['hd'] = add(f'{prefix}/hd.m3u', [e for e in selected if e.hd])
        item['sd'] = add(f'{prefix}/sd.m3u', [e for e in selected if not e.hd])
        for category in sorted({c for e in selected for c in e.categories}):
            item['categories'].append({'id': category, **add(f'{prefix}/{category}.m3u', [e for e in selected if category in e.categories])})
        index['languages'].append(item)
    for category in sorted({c for e in entries for c in e.categories}):
        index['categories'].append({'id': category, **add(f'categories/{category}.m3u', [e for e in entries if category in e.categories])})
    for original, variant in [('playlist.m3u', 'all'), ('playlist_hd.m3u', 'hd'), ('playlist_sd.m3u', 'sd')]:
        outputs[original] = outputs[f'playlists/fas/{variant}.m3u']
    outputs['index.json'] = json.dumps(index, ensure_ascii=False, indent=2) + '\n'
    return outputs


def build_collection(root):
    feeds = fetch_dataframe(DEFAULT_FEEDS_URL)
    streams = fetch_dataframe(DEFAULT_STREAMS_URL, 'json')
    channels = fetch_dataframe(DEFAULT_CHANNELS_URL, 'json')
    languages = fetch_dataframe(DEFAULT_LANGUAGES_URL, 'json')
    if not {'code', 'name'}.issubset(languages.columns):
        raise ValueError('Language metadata must include code and name')
    entries = prepare_entries(feeds, streams, channels)
    outputs = collection_outputs(entries, dict(zip(languages['code'], languages['name'])))
    # Remove obsolete generated playlists so vanished categories do not stay stale.
    # The two directories are reserved for generated output.
    stale = [p for folder in ('playlists', 'categories') for p in (root / folder).rglob('*.m3u')
             if p.relative_to(root).as_posix() not in outputs]
    write_outputs(root, outputs)
    for path in stale:
        path.unlink()
    logging.info('Generated %s playlists from %s matched stream/feed entries', len(outputs) - 1, len(entries))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-l', '--lang', default=DEFAULT_LANG, help='ISO 639-3 language code (default: fas)')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT, help='Output path for a single language')
    parser.add_argument('--include-offline', action='store_true', help='Include streams explicitly marked offline')
    parser.add_argument('--collection', action='store_true', help='Build all available languages and categories')
    parser.add_argument('--root', type=Path, default=Path('.'), help='Collection output directory')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.collection:
        build_collection(args.root)
    else:
        build_playlist(args.lang, args.output, include_offline=args.include_offline)

"""Validate generated files without claiming to verify live stream availability."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_playlist(path):
    text = path.read_text(encoding='utf-8')
    require(text.startswith('#EXTM3U\n'), f'{path}: missing M3U header')
    rows, pending = [], None
    for line in text.splitlines()[1:]:
        if line.startswith('#EXTINF:'):
            require(pending is None, f'{path}: entry without URL')
            pending = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
            require(all(pending.get(k) for k in ('tvg-id', 'tvg-name', 'tvg-language', 'group-title')), f'{path}: missing attributes')
        elif line and not line.startswith('#'):
            require(pending is not None, f'{path}: URL without entry')
            require(line.startswith(('https://', 'http://')), f'{path}: unsupported URL')
            pending['url'] = line
            rows.append(pending)
            pending = None
    require(pending is None, f'{path}: final entry without URL')
    keys = [(r['tvg-id'], r['url']) for r in rows]
    require(len(keys) == len(set(keys)), f'{path}: duplicate channel/URL entries')
    return rows


def signature(rows):
    return Counter(tuple(sorted(row.items())) for row in rows)


def validate_collection(root):
    index = json.loads((root / 'index.json').read_text(encoding='utf-8'))
    require(bool(index['languages']), 'No languages in collection')
    seen_paths = set()
    cache = {}

    def check(info):
        relative = Path(info['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Invalid playlist path')
        require(info['path'] not in seen_paths, f'Duplicate index path: {relative}')
        seen_paths.add(info['path'])
        rows = read_playlist(root / relative)
        require(len(rows) == info['streams'], f'{relative}: stream count mismatch')
        require(len({r['tvg-id'] for r in rows}) == info['channels'], f'{relative}: channel count mismatch')
        cache[info['path']] = rows
        return rows

    for language in index['languages']:
        code = language['code']
        all_rows, hd, sd = [check(language[key]) for key in ('all', 'hd', 'sd')]
        require(bool(all_rows), f'{code}: empty language playlist')
        require(signature(all_rows) == signature(hd) + signature(sd), f'{code}: HD/SD partition mismatch')
        for row in all_rows:
            languages = row['tvg-language'].split(';')
            require(languages == ['fas'] if code == 'fas' else code in languages, f'{code}: wrong language')
        keys = {(r['tvg-id'], r['url']) for r in all_rows}
        for category in language['categories']:
            rows = check(category)
            require(bool(rows), f'{category["path"]}: empty category')
            require({(r['tvg-id'], r['url']) for r in rows} <= keys, f'{category["path"]}: foreign language entries')
            require(all(category['id'].title() in r['group-title'].split(';') for r in rows), f'{category["path"]}: wrong category')
            category_hd, category_sd = check(category['hd']), check(category['sd'])
            require(signature(rows) == signature(category_hd) + signature(category_sd),
                    f'{category["path"]}: category HD/SD partition mismatch')
    for category in index['categories']:
        rows = check(category)
        require(bool(rows), f'{category["path"]}: empty global category')
        require(all(category['id'].title() in r['group-title'].split(';') for r in rows), f'{category["path"]}: wrong category')
    for original, variant in [('playlist.m3u', 'all'), ('playlist_hd.m3u', 'hd'), ('playlist_sd.m3u', 'sd')]:
        require((root / original).read_bytes() == (root / f'playlists/fas/{variant}.m3u').read_bytes(), f'{original}: Farsi alias mismatch')
    actual = {p.relative_to(root).as_posix() for folder in ('playlists', 'categories') for p in (root / folder).rglob('*.m3u')}
    require(actual == seen_paths, 'Generated files and index disagree')

    # Check relative documentation links and raw playlist links against local files.
    docs = (list(root.glob('*.md')) + list((root / 'playlists').glob('*/README.md'))
            + list((root / 'categories').glob('*.md')))
    raw_prefix = 'https://iman-py.github.io/open-tv-atlas/'
    for path in docs:
        text = path.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://', 'http://', '#')):
                continue
            target = unquote(target.split('#')[0])
            require((path.parent / target).exists(), f'{path}: broken link {target}')
        for target in re.findall(re.escape(raw_prefix) + r'([^\s`)|]+)', text):
            require((root / target).is_file(), f'{path}: broken raw link {target}')
    return len(seen_paths) + 3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    count = validate_collection(parser.parse_args().root)
    print(f'Validated {count} playlists: structure, counts, language/category filters, quality splits, aliases, and documentation links.')

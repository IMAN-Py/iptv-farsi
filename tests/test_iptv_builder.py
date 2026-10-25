import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from iptv_builder import (
    Entry, build_playlist, collection_outputs, is_stream_hd,
    prepare_entries, select_language, write_outputs,
)
from scripts.update_catalog import update_catalog
from scripts.validate_collection import validate_collection


class PlaylistTests(unittest.TestCase):
    def test_missing_languages_are_skipped_and_only_farsi_is_included(self):
        feeds = pd.read_csv(StringIO(
            "channel,languages\n"
            "Missing,\n"
            "Farsi,fas\n"
            "Multilingual,fas;eng\n"
            "English,eng\n"
            "Whitespace,  fas  \n"
        ))
        streams = pd.DataFrame([
            {"channel": channel, "url": f"https://example.com/{channel}.m3u8"}
            for channel in feeds["channel"]
        ])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "playlist.m3u"
            with patch("iptv_builder.fetch_dataframe", side_effect=[feeds, streams]):
                build_playlist(output_file=str(output))
            playlist = output.read_text()
            self.assertTrue(playlist.startswith("#EXTM3U\n"))
            self.assertEqual(playlist.count("#EXTINF:"), 2)
            for channel in ("Farsi", "Whitespace"):
                self.assertIn(f"https://example.com/{channel}.m3u8", playlist)
            for channel in ("Missing", "Multilingual", "English"):
                self.assertNotIn(f"https://example.com/{channel}.m3u8", playlist)
            self.assertEqual(output.with_name("playlist_hd.m3u").read_text(), "#EXTM3U\n")
            self.assertEqual(output.with_name("playlist_sd.m3u").read_text(), playlist)

    def test_feed_id_prevents_cross_language_and_quality_matches(self):
        feeds = pd.DataFrame([
            {"channel": "Example", "id": "FA", "languages": "fas", "format": "1080p", "is_main": True},
            {"channel": "Example", "id": "EN", "languages": "eng", "format": "480p", "is_main": False},
        ])
        streams = pd.DataFrame([
            {"channel": "Example", "feed": "EN", "url": "https://example.com/english.m3u8"},
            {"channel": "Example", "feed": "FA", "url": "https://example.com/farsi.m3u8", "quality": "576p"},
            {"channel": "Example", "feed": None, "url": "https://example.com/main.m3u8"},
            {"channel": "Example", "feed": "Unknown", "url": "https://example.com/wrong.m3u8"},
        ])
        entries = prepare_entries(feeds, streams)
        farsi = select_language(entries, 'fas')
        english = select_language(entries, 'eng')
        self.assertEqual({e.url for e in farsi}, {'https://example.com/farsi.m3u8', 'https://example.com/main.m3u8'})
        self.assertEqual([e.url for e in english], ['https://example.com/english.m3u8'])
        self.assertFalse(next(e for e in farsi if 'farsi' in e.url).hd)
        self.assertTrue(next(e for e in farsi if 'main' in e.url).hd)

    def test_reported_quality_overrides_misleading_url(self):
        self.assertFalse(is_stream_hd(None, None, '480p', 'https://example.com/hd/stream'))
        self.assertTrue(is_stream_hd(None, None, '2160p', 'https://example.com/stream'))
        self.assertTrue(is_stream_hd(None, None, '4K', 'https://example.com/stream'))
        self.assertTrue(is_stream_hd(None, None, '', 'https://example.com/hd/stream'))
        self.assertFalse(is_stream_hd(None, None, '', 'https://example.com/shdog/stream'))

    def test_empty_result_preserves_existing_playlist(self):
        feeds = pd.DataFrame([{'channel': 'Missing', 'languages': 'eng'}])
        streams = pd.DataFrame([{'channel': 'Missing', 'url': 'https://example.com/stream'}])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'playlist.m3u'
            path.write_text('existing playlist')
            with patch('iptv_builder.fetch_dataframe', side_effect=[feeds, streams]):
                with self.assertRaises(ValueError):
                    build_playlist(output_file=str(path))
            self.assertEqual(path.read_text(), 'existing playlist')

    def test_headers_names_and_categories_are_preserved(self):
        feeds = pd.DataFrame([{'channel': 'News', 'languages': 'fas'}])
        streams = pd.DataFrame([{'channel': 'News', 'url': 'https://example.com/live',
                                 'user_agent': 'Player/1.0', 'referrer': 'https://example.com/'}])
        channels = pd.DataFrame([{'id': 'News', 'name': 'Persian News', 'categories': ['news']}])
        entry = prepare_entries(feeds, streams, channels)[0]
        self.assertEqual(entry.name, 'Persian News')
        self.assertEqual(entry.categories, ('news',))
        outputs = collection_outputs([entry], {'fas': 'Persian'})
        text = outputs['playlist.m3u']
        self.assertIn('group-title="News"', text)
        self.assertIn('#EXTVLCOPT:http-user-agent=Player/1.0', text)
        self.assertIn('#EXTVLCOPT:http-referrer=https://example.com/', text)
        self.assertIn(',Persian News\n', text)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.entries = [
            Entry('Farsi', 'Farsi TV', 'https://example.com/fa', ('fas',), ('sports',), '1080p', True),
            Entry('Farsi', 'Farsi TV', 'https://example.com/fa-sd', ('fas',), ('sports',), '480p', False),
            Entry('English', 'English TV', 'https://example.com/en', ('eng',), ('movies',), '720p', True),
            Entry('Multi', 'Multilingual TV', 'https://example.com/multi', ('eng', 'fas'), ('news',), '480p', False),
            Entry('UnknownCategory', 'Other TV', 'https://example.com/other', ('eng',), (), '', False),
        ]
        self.names = {'fas': 'Persian', 'eng': 'English'}

    def test_language_category_intersection_and_original_farsi_urls(self):
        outputs = collection_outputs(self.entries, self.names)
        self.assertIn('playlists/fas/sports.m3u', outputs)
        self.assertNotIn('playlists/fas/movies.m3u', outputs)
        self.assertNotIn('playlists/fas/news.m3u', outputs)
        self.assertNotIn('https://example.com/multi', outputs['playlist.m3u'])
        self.assertIn('https://example.com/multi', outputs['playlists/eng/news.m3u'])
        self.assertNotIn('https://example.com/en', outputs['categories/sports.m3u'])
        self.assertIn('https://example.com/other', outputs['playlists/eng/all.m3u'])
        self.assertEqual(outputs['playlist.m3u'], outputs['playlists/fas/all.m3u'])
        self.assertEqual(outputs['playlist_hd.m3u'], outputs['playlists/fas/hd.m3u'])
        self.assertEqual(outputs['playlist_sd.m3u'], outputs['playlists/fas/sd.m3u'])

    def test_duplicates_do_not_overlap_quality_variants(self):
        entries = self.entries + [Entry('English', 'English TV', 'https://example.com/en',
                                       ('eng', 'fra'), ('movies',), '480p', False)]
        outputs = collection_outputs(entries, self.names)
        self.assertEqual(outputs['playlists/eng/all.m3u'].count('https://example.com/en\n'), 1)
        self.assertNotIn('https://example.com/en\n', outputs['playlists/eng/sd.m3u'])

    def test_missing_farsi_aborts_collection(self):
        with self.assertRaises(ValueError):
            collection_outputs([self.entries[2]], self.names)

    def test_catalog_and_validation_end_to_end_and_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, collection_outputs(self.entries, self.names))
            (root / 'README.md').write_text(
                '<!-- playlist-stats:start -->\n<!-- playlist-stats:end -->\n'
                '<!-- featured-playlists:start -->\n<!-- featured-playlists:end -->\n')
            update_catalog(root)
            self.assertGreater(validate_collection(root), 10)
            self.assertIn('Farsi: 1 channels', (root / 'README.md').read_text())
            before = {p: p.read_bytes() for p in root.rglob('*.md')}
            update_catalog(root)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*.md')})
            # A mismatched alias must fail validation before publication.
            (root / 'playlist.m3u').write_text('#EXTM3U\n')
            with self.assertRaisesRegex(ValueError, 'alias mismatch'):
                validate_collection(root)


if __name__ == "__main__":
    unittest.main()

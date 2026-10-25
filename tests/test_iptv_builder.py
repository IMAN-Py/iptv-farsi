import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from iptv_builder import build_playlist


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


if __name__ == "__main__":
    unittest.main()

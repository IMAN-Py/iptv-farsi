"""Prepare a compact, entirely static GitHub Pages picker."""
import argparse
import json
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('index', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent / 'dist'
data = json.loads(args.index.read_text())
if not data.get('languages'):
    raise ValueError('Missing language index')
shutil.copyfile(args.index, root / 'catalog.json')
(root / '.nojekyll').write_text('')
(root / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://iman-py.github.io/open-tv-atlas/</loc></url></urlset>\n')
# Remove only previously generated directory pages from the earlier larger design.
for name in ['languages', 'directory', 'guide']:
    if (root / name).exists():
        shutil.rmtree(root / name)
if (root / 'robots.txt').exists():
    (root / 'robots.txt').unlink()
print('Built compact static picker with', len(data['languages']), 'language lists')

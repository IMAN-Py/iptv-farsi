"""Build crawlable, useful static directory pages and an offline catalog fallback."""
import argparse
import html
import json
from pathlib import Path
import shutil
from xml.etree.ElementTree import Element, SubElement, ElementTree

BASE = 'https://open-tv-atlas.vividtuna13.chatgpt.site'
RAW = 'https://raw.githubusercontent.com/IMAN-Py/open-tv-atlas/main/'
REPO = 'https://github.com/IMAN-Py/open-tv-atlas'
e = html.escape
root = Path(__file__).parent / 'dist'
parser=argparse.ArgumentParser()
parser.add_argument('index',type=Path)
args=parser.parse_args()
data=json.loads(args.index.read_text())
shutil.copyfile(args.index,root/'catalog.json')
urls=['/']

def write_page(path, title, description, body):
    canonical = BASE + path
    markup=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} — Open TV Atlas</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)} — Open TV Atlas"><meta property="og:description" content="{e(description)}"><meta property="og:image" content="{BASE}/social-preview.png"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css"></head><body><header class="nav wrap"><a class="brand" href="/">◈ Open TV Atlas</a><nav><a href="/directory/">Directory</a><a class="github" href="{REPO}">GitHub ↗</a></nav></header><main class="doc wrap">{body}</main><footer class="wrap"><a href="/">Open TV Atlas</a><p>Independent directory powered by <a href="https://github.com/iptv-org/iptv">iptv-org</a>. No video hosted.</p><a href="{REPO}/issues/new/choose">Report a problem</a></footer></body></html>'''
    target=root/path.strip('/')/'index.html'; target.parent.mkdir(parents=True,exist_ok=True);target.write_text(markup)
    urls.append(path)

links=[]
for language in data['languages']:
    code=language['code']; name='Farsi / Persian · فارسی' if code=='fas' else language['name']
    links.append(f'<a href="/languages/{code}/">{e(name)} <span aria-hidden="true">↗</span></a>')
    rows=[]
    for key,label in [('all','All channels'),('hd','HD'),('sd','SD / unknown')]:
        info=language[key]
        if info['streams']: rows.append(f'<tr><td>{label}</td><td><a href="{RAW}{info["path"]}">Open M3U</a></td></tr>')
    cats=[]
    for cat in language['categories']:
        actions=[f'<a href="{RAW}{cat["path"]}">All qualities</a>']
        for key,label in [('hd','HD'),('sd','SD / unknown')]:
            if cat.get(key,{}).get('streams'): actions.append(f'<a href="{RAW}{cat[key]["path"]}">{label}</a>')
        cats.append(f'<tr><td>{e(cat["id"].title())}</td><td>{" · ".join(actions)}</td><td><a href="/?lang={code}&amp;category={cat["id"]}#picker">Choose in picker ↗</a></td></tr>')
    body=f'''<p class="eyebrow">PLAYLIST DIRECTORY / {e(code.upper())}</p><h1>{e(name)} IPTV playlists</h1><p>Choose a {e(name)} playlist for live television in your M3U-compatible player. The links below refresh with the repository’s daily updates. For current entry counts and easy copying, open the live picker.</p><a class="button dark" href="/?lang={code}#picker">Choose a playlist ↗</a><h2>Quality options</h2><table><thead><tr><th>Version</th><th>Playlist</th></tr></thead><tbody>{''.join(rows)}</tbody></table><h2>Categories</h2><div class="table-scroll"><table><thead><tr><th>Category</th><th>Playlist links</th><th>Picker</th></tr></thead><tbody>{''.join(cats)}</tbody></table></div><h2>Use it on your TV</h2><p>Copy a playlist URL, choose an M3U source in StreamVault or your preferred player, and paste the URL. <a href="/guide/">Read the setup guide</a>.</p><p>{'Farsi lists include only feeds marked exclusively Farsi.' if code=='fas' else 'This language can include multilingual feeds that list it in the source metadata.'} Categories describe channels, not individual programmes. Availability and quality are not playback-tested.</p><p><a href="/directory/">Browse another language →</a></p>'''
    write_page(f'/languages/{code}/',f'{name} IPTV Playlists',f'Find {name} IPTV M3U playlist links by category and quality, with setup instructions for TV players.',body)
write_page('/directory/','IPTV Playlist Directory by Language','Explore live TV M3U playlists by language. English first, Farsi next, then languages from around the world.', '<p class="eyebrow">FIND YOUR LANGUAGE</p><h1>Your language.<br>Your channels.</h1><p>English first, Farsi next, then the rest of the directory. Select a language for its playlist URLs and available categories. Use the <a href="/#picker">live picker</a> for current counts and searchable filters.</p><div class="doc-grid">'+''.join(links)+'</div>')
write_page('/guide/','How to Add an IPTV Playlist to StreamVault or VLC','Set up Open TV Atlas playlists on Android TV with StreamVault, or in VLC. Choose a playlist and copy its M3U URL.', '''<p class="eyebrow">FROM LINK TO PLAYER</p><h1>Get set up in minutes.</h1><p>Open TV Atlas gives you playlist links. Your player opens the streams. Start with the <a href="/#picker">playlist picker</a>.</p><h2>Android TV: StreamVault</h2><ol><li>Download StreamVault from its <a href="https://github.com/Davidona/StreamVault-IPTV/releases/latest">official releases</a> and install it on your Android TV device.</li><li>In Atlas, choose a language, category and quality, then copy the playlist URL.</li><li>Choose an M3U source in StreamVault and paste the full URL. Load the playlist and browse Live TV.</li></ol><p>StreamVault is a separate project. Features and menu names may vary by version. See its <a href="https://github.com/Davidona/StreamVault-IPTV">official documentation</a>.</p><h2>VLC desktop</h2><p>Open a network stream in VLC, paste the M3U playlist URL, and play. Use the playlist view to choose a channel.</p><h2>Other IPTV players</h2><p>Choose Add Playlist or the M3U URL option, paste the full link, and let the app load it. Refresh the playlist periodically for source changes.</p><h2>Watch the browser walkthrough</h2><p>This recording shows the real playlist picker. It does not demonstrate or verify TV playback.</p><video controls preload="metadata" poster="/demo-poster.png"><source src="/demo.webm" type="video/webm">Your browser does not support this video. <a href="/demo.webm">Download the walkthrough</a>.</video><h2>Troubleshooting</h2><p>If a stream fails, try an alternative URL for that channel or refresh your playlist. Some broadcasts are offline or region restricted. These playlists contain live channels, not on-demand movies or guaranteed sports events.</p><p><a href="https://github.com/IMAN-Py/open-tv-atlas/issues/new/choose">Report a problem</a> with the playlist URL, channel ID, player and country.</p>''')
xml=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for path in urls: SubElement(SubElement(xml,'url'),'loc').text=BASE+path
ElementTree(xml).write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
print(f'Generated {len(urls)} crawlable pages and sitemap')

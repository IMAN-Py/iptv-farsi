'use strict';
const RAW = 'https://iman-py.github.io/open-tv-atlas/';
const $ = id => document.getElementById(id);
if (location.hash === '#demo') $('demo').open = true;
const params = new URLSearchParams(location.search);
const state = {lang: params.get('lang') || 'eng', category: params.get('category') || 'all', quality: params.get('quality') || 'all'};
let catalog;
let selected;
const title = s => s.charAt(0).toUpperCase() + s.slice(1);
const label = item => item.code === 'fas' ? 'Farsi / Persian · فارسی' : item.name;
function option(value, text) {const el = document.createElement('option'); el.value = value; el.textContent = text; return el;}
function valid(data) {
  return data && Array.isArray(data.languages) && data.languages.length && data.languages.every(l => /^[a-z]{3}$/.test(l.code) && typeof l.name === 'string' && l.all && Array.isArray(l.categories));
}
function currentLanguage() {return catalog?.languages.find(l => l.code === state.lang);}
function updateLanguages() {
  const query = $('language-search').value.trim().toLocaleLowerCase();
  const list = catalog.languages.filter(l => `${label(l)} ${l.code}`.toLocaleLowerCase().includes(query));
  $('language').replaceChildren(...list.map(l => option(l.code, label(l))));
  $('language').disabled = !list.length;
  if (!list.length) {empty('No matching language', 'Try a different spelling or a three-letter language code.'); return;}
  if (!list.some(l => l.code === state.lang)) state.lang = list[0].code;
  $('language').value = state.lang;
  updateCategories();
}
function updateCategories() {
  const language = currentLanguage();
  $('category').replaceChildren(option('all', 'All channels'), ...language.categories.map(c => option(c.id, title(c.id))));
  if (state.category !== 'all' && !language.categories.some(c => c.id === state.category)) state.category = 'all';
  if (!['all','hd','sd'].includes(state.quality)) state.quality = 'all';
  $('category').value = state.category;
  $('quality').value = state.quality;
  $('language-note').textContent = state.lang === 'fas' ? 'Farsi-only feeds. فیدهای تک‌زبانه فارسی' : 'Includes multilingual feeds that list this language.';
  render();
}
function empty(heading, message) {
  selected = null;
  $('result-title').textContent = heading;
  $('result-subtitle').textContent = message;
  $('channel-count').textContent = '0'; $('stream-count').textContent = '0';
  $('playlist-url').value = ''; $('copy').disabled = true;
  $('open-playlist').removeAttribute('href'); $('open-playlist').setAttribute('aria-disabled','true');
  $('copy-status').textContent = ''; $('share').disabled = !catalog;
}
function render() {
  const language = currentLanguage();
  let info;
  if (state.category === 'all') info = language[state.quality];
  else {const category = language.categories.find(c => c.id === state.category); info = state.quality === 'all' ? category : category?.[state.quality];}
  const categoryName = state.category === 'all' ? 'All channels' : title(state.category);
  const qualityName = {all:'All qualities',hd:'HD',sd:'SD / unknown'}[state.quality];
  const newUrl = new URL(location.href); newUrl.search = new URLSearchParams(state.lang === 'eng' && state.category === 'all' && state.quality === 'all' ? {} : {lang:state.lang,category:state.category,quality:state.quality});
  history.replaceState(null,'',newUrl);
  if (!info || !info.streams) {empty(`${label(language)} · ${categoryName}`, 'No matching streams in this quality. Try All qualities or another category.'); return;}
  if (!/^playlists\/[a-z]{3}\/[a-z_]+\.m3u$/.test(info.path)) {empty('Playlist unavailable','Please report this directory entry.'); return;}
  selected = RAW + info.path;
  $('result-title').textContent = `${label(language)} · ${categoryName}`;
  $('result-subtitle').textContent = `${qualityName} · Ready for an M3U-compatible player`;
  $('channel-count').textContent = info.channels.toLocaleString();
  $('stream-count').textContent = info.streams.toLocaleString();
  $('playlist-url').value = selected; $('copy').disabled = false;
  $('open-playlist').href = selected; $('open-playlist').removeAttribute('aria-disabled');
  $('copy-status').textContent = ''; $('share').disabled = false;
}
async function copy(text, message) {
  try {await navigator.clipboard.writeText(text); $('copy-status').textContent = message;}
  catch { $('copy-status').textContent = 'Clipboard unavailable. Copy this link manually: ' + text; }
}
$('filters').addEventListener('submit', e => e.preventDefault());
$('language-search').addEventListener('input', () => catalog && updateLanguages());
$('language').addEventListener('change', () => {state.lang = $('language').value; updateCategories();});
$('category').addEventListener('change', () => {state.category = $('category').value; render();});
$('quality').addEventListener('change', () => {state.quality = $('quality').value; render();});
$('reset').addEventListener('click', () => {if (!catalog) return; Object.assign(state,{lang:'eng',category:'all',quality:'all'}); $('language-search').value = ''; updateLanguages();});
$('copy').addEventListener('click', () => selected && copy(selected, 'Copied. Paste this link into your player.'));
$('share').addEventListener('click', () => copy(location.href.split('#')[0] + '#picker', 'Selection link copied. Share it with someone.'));
async function load(url) {const response = await fetch(url,{signal:AbortSignal.timeout(12000)}); if (!response.ok) throw Error('Download failed'); const data = await response.json(); if (!valid(data)) throw Error('Invalid catalog'); return data;}
(async () => {
  try {catalog = await load(new URL('./catalog.json', location.href).href); updateLanguages(); $('data-status').textContent = 'Saved directory ready. Checking for updates…';} catch {}
  try {catalog = await load(RAW + 'index.json'); updateLanguages(); $('data-status').textContent = 'Latest directory loaded · refreshed daily';}
  catch {if (catalog) $('data-status').textContent = 'Using the saved directory. Live update unavailable.'; else {empty('Directory unavailable','Please use the GitHub directory or try again later.'); $('data-status').innerHTML = '<a href="https://github.com/IMAN-Py/open-tv-atlas/blob/main/DIRECTORY.md">Open the GitHub directory ↗</a>';}}
})();

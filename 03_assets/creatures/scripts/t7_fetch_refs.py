"""t7_fetch_refs — real-world reference photos from Wikimedia Commons (free licences only), with author + licence recorded.

usage: python3 t7_fetch_refs.py <species_id> "<search query>" [n=5] [--min-width 1000]
→ 03_assets/creatures/00_CREATURE_REFERENCES/photo_refs/<species_id>/<nn>_<title>.jpg + CREDITS.md + credits.json
Only CC0 / Public domain / CC BY / CC BY-SA files are kept (attribution kept in CREDITS.md). Reference use only — never textures in the film.
"""
import sys, os, json, re, time, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '00_CREATURE_REFERENCES', 'photo_refs')
UA = 'T7ReferenceFetcher/0.1 (3D animation reference research; contact via project)'
API = 'https://commons.wikimedia.org/w/api.php'
OK = re.compile(r'^(cc0|pd|public domain|cc by(-sa)? ?[1-4]\.0|cc-by(-sa)?-[1-4]\.0)', re.I)


def _open(url, timeout=60):
    for k in range(6):                      # polite retry on 429 / 5xx (Retry-After respected)
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or k == 5:
                raise
            wait = int(e.headers.get('Retry-After') or 0) or 15 * (k + 1)
            print('  retry in', wait, 's'); time.sleep(wait)


def get(params):
    q = API + '?' + urllib.parse.urlencode(dict(params, format='json'))
    return json.loads(_open(q, 40))


def clean(html):
    return re.sub(r'<[^>]+>', '', html or '').strip()


def fetch(sid, query, n=5, min_w=1000):
    d = os.path.join(OUT, sid); os.makedirs(d, exist_ok=True)
    credits = json.load(open(os.path.join(d, 'credits.json'))) if os.path.exists(os.path.join(d, 'credits.json')) else []
    have = {c['title'] for c in credits}
    r = get(dict(action='query', generator='search', gsrsearch=f'filetype:bitmap {query}', gsrnamespace=6, gsrlimit=40,
                 prop='imageinfo', iiprop='url|size|extmetadata|mime'))
    pages = sorted(r.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    got = 0
    for pg in pages:
        if got >= n:
            break
        ii = (pg.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
        lic = clean(md.get('LicenseShortName', {}).get('value'))
        if ii.get('mime') != 'image/jpeg' or ii.get('width', 0) < min_w or not OK.match(lic) or pg['title'] in have:
            continue
        url = ii['url']                                   # original on upload.wikimedia.org (thumb host not allowed) → resized locally
        if ii.get('size', 0) > 30e6:
            continue
        fn = f'{len(credits) + 1:02d}_' + re.sub(r'[^A-Za-z0-9]+', '_', pg['title'][5:])[:60].strip('_') + '.jpg'
        import io
        from PIL import Image
        im = Image.open(io.BytesIO(_open(url, 120))).convert('RGB')
        im.thumbnail((1280, 1280)); im.save(os.path.join(d, fn), quality=88)
        credits.append(dict(file=fn, title=pg['title'], author=clean(md.get('Artist', {}).get('value'))[:120], license=lic,
                            source=ii.get('descriptionurl'), query=query))
        got += 1; time.sleep(3)
    json.dump(credits, open(os.path.join(d, 'credits.json'), 'w'), indent=1)
    with open(os.path.join(d, 'CREDITS.md'), 'w') as f:
        f.write(f'# Reference photos — {sid} (Wikimedia Commons, reference only)\n\n| File | Author | Licence | Source |\n|---|---|---|---|\n')
        for c in credits:
            f.write(f"| {c['file']} | {c['author']} | {c['license']} | {c['source']} |\n")
    print(sid, 'new', got, 'total', len(credits))


if __name__ == '__main__':
    a = [x for x in sys.argv[1:]]
    fetch(a[0], a[1], int(a[2]) if len(a) > 2 else 5)

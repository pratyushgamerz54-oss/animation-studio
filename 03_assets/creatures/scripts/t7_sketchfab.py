"""t7_sketchfab — search / download free-licence base models from Sketchfab (TASK 07 'mix' pipeline, Director 23 Nov).

  search  : python3 t7_sketchfab.py search "<query>" [n]   → candidates (licence CC0 / CC-BY / CC-BY-SA only, downloadable)
  get     : python3 t7_sketchfab.py get <uid> <species_id>  → 03_assets/creatures/00_CREATURE_REFERENCES/cc_models/<species>/<uid>/
The API token is injected by the session's network proxy (never stored here). Every download writes LICENSE.md with
author, licence and source URL (CC-BY attribution goes into the film credits list).
"""
import sys, os, json, urllib.request, urllib.parse, zipfile, io, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '00_CREATURE_REFERENCES', 'cc_models')
API = 'https://api.sketchfab.com/v3'
OK_LIC = {'cc0', 'by', 'by-sa'}          # no NC (film may be commercial), no ND (we modify the model)


def call(path, params=None):
    url = API + path + ('?' + urllib.parse.urlencode(params) if params else '')
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'T7-asset-pipeline'}), timeout=60))


def search(q, n=12):
    res = []
    for lic in ('cc0', 'by', 'by-sa'):
        d = call('/search', dict(type='models', q=q, downloadable='true', license=lic, count=24, sort_by='-likeCount'))
        for m in d.get('results', []):
            th = max(m.get('thumbnails', {}).get('images', []), key=lambda i: i.get('width', 0) if i.get('width', 0) <= 1024 else 0, default={})
            res.append(dict(uid=m['uid'], name=m['name'], license=m.get('license', {}).get('label') if m.get('license') else lic,
                            lic=lic, author=m.get('user', {}).get('displayName'), faces=m.get('faceCount'), verts=m.get('vertexCount'),
                            animated=m.get('animationCount', 0), likes=m.get('likeCount'), url=m.get('viewerUrl'), thumb=th.get('url')))
        time.sleep(1)
    res.sort(key=lambda r: -(r['likes'] or 0))
    return res[:n]


def get(uid, sid):
    info = call(f'/models/{uid}')
    lic = (info.get('license') or {}).get('slug', '')
    assert any(lic.startswith(x) or lic == x for x in ('cc0', 'by', 'by-sa')) and 'nc' not in lic and 'nd' not in lic, f'licence not allowed: {lic}'
    dl = call(f'/models/{uid}/download')
    src = dl.get('gltf') or dl.get('source')
    d = os.path.join(OUT, sid, uid); os.makedirs(d, exist_ok=True)
    data = urllib.request.urlopen(src['url'], timeout=600).read()
    zipfile.ZipFile(io.BytesIO(data)).extractall(d)
    with open(os.path.join(d, 'LICENSE.md'), 'w') as f:
        f.write(f"# {info['name']}\n\n* Author: {info['user']['displayName']} ({info['user'].get('profileUrl')})\n"
                f"* Licence: {(info.get('license') or {}).get('label')} ({lic})\n* Source: {info.get('viewerUrl')}\n"
                f"* Downloaded: {time.strftime('%Y-%m-%d')} for TASK 07 (base mesh; modified: cleanup, retopology, UV, textures, groom, rig)\n")
    json.dump(info, open(os.path.join(d, 'sketchfab_info.json'), 'w'), indent=1)
    print('saved', d, round(len(data) / 1e6, 1), 'MB')


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        for r in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12):
            print(json.dumps(r))
    else:
        get(sys.argv[2], sys.argv[3])

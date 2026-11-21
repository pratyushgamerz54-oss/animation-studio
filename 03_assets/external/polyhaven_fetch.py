"""Download the Poly Haven (CC0) assets used by the environments.

Run:  python3 03_assets/external/polyhaven_fetch.py            (skips files already present)
Out:  03_assets/external/polyhaven/{models,textures,hdris}/<id>/...   + manifest.json

The binaries are NOT committed to git (too large, >1 GB) — this script re-creates them in any new session.
License: Poly Haven assets are CC0 (public domain) — free for commercial use, no attribution required.
Needs network access to api.polyhaven.com + dl.polyhaven.org (environment "animation-studio").
"""
import os, sys, json, urllib.request, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'polyhaven')
API = 'https://api.polyhaven.com/files/'
UA = {'User-Agent': 'animation-studio-asset-fetch/1.0'}


def req(url):
    return urllib.request.Request(url, headers=UA)

MODELS = ['fir_tree_01', 'fir_sapling_medium', 'tree_small_02', 'shrub_01', 'shrub_02', 'shrub_03', 'grass_medium_01',
          'grass_medium_02', 'fern_02', 'rock_moss_set_01', 'rock_moss_set_02', 'boulder_01', 'moss_01', 'mountainside',
          # TASK 05 terrain production (trees, debris, rocks)
          'pine_tree_01', 'pine_sapling_small', 'fir_sapling', 'dead_tree_trunk', 'dead_tree_trunk_02', 'tree_stump_01',
          'root_cluster_01', 'root_cluster_02', 'pine_roots', 'rock_07', 'rock_09', 'rock_face_01', 'rock_face_02', 'stone_01',
          'namaqualand_boulder_02', 'namaqualand_boulder_03', 'coast_rocks_01', 'dry_branches_medium_01', 'bark_debris_01',
          'shrub_04', 'grass_bermuda_01', 'nettle_plant', 'dandelion_01']
TEXTURES = ['clay_roof_tiles_02', 'plastered_stone_wall', 'rustic_stone_wall', 'cobblestone_floor_04', 'mossy_cobblestone',
            'dark_wooden_planks', 'medieval_wood', 'forest_ground_04', 'grass_path_2', 'aerial_grass_rock', 'aerial_rocks_02',
            'snow_02', 'brown_mud_leaves_01', 'sparse_grass', 'cliff_side', 'worn_mossy_plasterwall',
            # TASK 05 terrain PBR library
            'leafy_grass', 'grass_ground', 'forest_floor', 'mud_forest', 'brown_mud', 'rocky_gravel', 'gravel_ground_01',
            'coast_sand_01', 'sand_01', 'dark_rock', 'rock_ground', 'mossy_rock', 'river_small_rocks', 'snow_field_aerial',
            'snow_04', 'dry_ground_01', 'mud_cracked_dry_03', 'aerial_ground_rock']
HDRIS = [('kloofendal_48d_partly_cloudy_puresky', '4k'), ('qwantani_dusk_2_puresky', '4k'), ('qwantani_night_puresky', '4k')]
MODEL_RES, TEX_RES = '1k', '2k'
TEX_MAPS = {'Diffuse': 'diff', 'nor_gl': 'nor_gl', 'Rough': 'rough', 'AO': 'ao', 'Displacement': 'disp'}


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for k in range(4):
        try:
            with urllib.request.urlopen(req(url), timeout=120) as r, open(path + '.part', 'wb') as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            os.replace(path + '.part', path); return True
        except Exception as e:
            print('retry', url, e); time.sleep(3 * (k + 1))
    raise RuntimeError('failed ' + url)


def files(aid):
    with urllib.request.urlopen(req(API + aid), timeout=60) as r:
        return json.load(r)


def main():
    man = {'license': 'CC0 (Poly Haven)', 'models': {}, 'textures': {}, 'hdris': {}}
    for aid in MODELS:
        x = files(aid)['blend'][MODEL_RES]['blend']; d = os.path.join(OUT, 'models', aid)
        p = os.path.join(d, os.path.basename(x['url'])); get(x['url'], p)
        for rel, inc in x.get('include', {}).items():
            get(inc['url'], os.path.join(d, rel))
        man['models'][aid] = os.path.relpath(p, HERE); print('model', aid, flush=True)
    for aid in TEXTURES:
        f = files(aid); d = os.path.join(OUT, 'textures', aid); man['textures'][aid] = {}
        for key, short in TEX_MAPS.items():
            if key in f and TEX_RES in f[key]:
                fmt = 'jpg' if 'jpg' in f[key][TEX_RES] else 'png'
                u = f[key][TEX_RES][fmt]['url']; p = os.path.join(d, f'{aid}_{short}_{TEX_RES}.{fmt}')
                get(u, p); man['textures'][aid][short] = os.path.relpath(p, HERE)
        print('texture', aid, flush=True)
    for aid, res in HDRIS:
        f = files(aid)['hdri'][res]; u = (f.get('exr') or f['hdr'])['url']
        p = os.path.join(OUT, 'hdris', aid, os.path.basename(u)); get(u, p); man['hdris'][aid] = os.path.relpath(p, HERE)
        print('hdri', aid, flush=True)
    json.dump(man, open(os.path.join(HERE, 'polyhaven_manifest.json'), 'w'), indent=1)
    print('FETCH DONE')


if __name__ == '__main__':
    main()

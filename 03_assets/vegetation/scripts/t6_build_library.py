"""TASK 06 · build a regional vegetation library .blend (Blender 4.5 LTS).

    BPY45 t6_build_library.py -- AV|EF|MK|PL|LK|DS|FB|CT|CV      (region table: t6_regions.py)

Output: 03_assets/vegetation/library/T6_VEG_<REGION>_v001.blend  +  T6_VEG_<REGION>_inventory.json
Layout inside the file:
  T6_LIB_<REGION>                      (scene 'T6_LIBRARY'; every asset at the world origin → ready for scatter / instancing)
    ├─ T6_<REGION>_TREES   ─ one sub-collection per species  (T6_<asset name>)
    ├─ T6_<REGION>_SHRUBS
    └─ T6_<REGION>_PLANTS
  scene 'T6_LINEUP'                    collection instances in a row (browse / compare heights in the viewport)
  object 'T6_WIND_CONTROL'             one empty drives the wind of every asset (custom props strength / gust / speed / flutter,
                                       arrow = wind direction). Wind modifier = geometry nodes 'NG_T6_WIND' (editable).
Every asset object carries its specification as custom properties (t6_label, t6_latin, t6_height_m, t6_canopy_x_m, …).
"""
import os, sys, json, shutil, datetime, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import t6kit as K
import t6_regions as RG

REG = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'AV'
NAMES = RG.NAMES
LIB = os.environ.get('T6_LIB_DIR') or os.path.join(K.VEG, 'library'); os.makedirs(LIB, exist_ok=True)   # T6_LIB_DIR = scratch test builds
OUT = os.path.join(LIB, f'T6_VEG_{NAMES[REG]}_v001.blend')

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.name = 'T6_LIBRARY'; sc.unit_settings.system = 'METRIC'
sc.render.fps = 24; sc.frame_start, sc.frame_end = 1, 240


def coll(name, parent):
    c = bpy.data.collections.new(name); parent.children.link(c); return c


root = coll(f'T6_LIB_{NAMES[REG]}', sc.collection)
groups = {k: coll(f'T6_{NAMES[REG]}_{k}', root) for k in ('TREES', 'SHRUBS', 'PLANTS')}
K.wind_control(); K.wind_instances_group()           # instance-wind group ships with every library (for scatters)
INV = {}
META_KEYS = ('common', 'latin', 'label', 'region', 'category', 'habitat', 'altitude')


def tag(o, D, kind, st):
    for k in META_KEYS:
        o[f't6_{k}'] = str(D.get(k, ''))
    o['t6_kind'] = kind; o['t6_palette'] = json.dumps(D.get('palette', []))
    o['t6_version'] = 'v001 (TASK 06 milestone 2)' if D['name'] in RG.M2_NAMES else 'v001 (TASK 06 milestone 1 concept)'
    o['t6_wind_ready'] = True
    INV[D['name']] = dict({k: D.get(k, '') for k in META_KEYS}, kind=kind, palette=D.get('palette', []), stats=st,
                          bark=D.get('bark', {}).get('tex') if kind != 'plant' else None,
                          atlas=(D.get('leaves') or {}).get('atlas') if kind != 'plant' else None, collection=f"T6_{D['name']}")


def make_scatter_copies(objs, root_name):
    """<asset>_SC: same mesh, NO wind modifier — used by NG_T6_ECOSYSTEM (wind applied once per instance there). The asset's wind
    amplitudes are copied as t6_wind_* properties. Collections T6_<asset>_SC live under <root>_SCATTER (fake user, not in the scene)."""
    sroot = bpy.data.collections.new(root_name + '_SCATTER'); sroot.use_fake_user = True
    for o in objs:
        so = bpy.data.objects.new(o.name + '_SC', o.data)
        for k in o.keys():
            if k.startswith('t6_'):
                so[k] = o[k]
        md = o.modifiers.get('T6_WIND')
        if md:
            ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
            for nm_, key in (('Trunk Sway (m)', 'trunk'), ('Branch Sway (m)', 'branch'), ('Leaf Flutter (m)', 'leaf'),
                             ('Natural Freq (Hz)', 'fn'), ('Flexibility', 'flex'), ('Damping', 'damping')):
                so[f't6_wind_{key}'] = float(md[ids[nm_]])
        c = bpy.data.collections.new(f'T6_{o.name}_SC'); sroot.children.link(c); c.objects.link(so)
    return sroot


for D in [t for t in RG.TREES if t['name'].startswith(REG + '_')]:
    c = coll(f"T6_{D['name']}", groups['TREES'])
    o, st = RG.build_woody(D, 0, c)
    H = st['height_m']; W = D.get('wind')
    if W:                                    # palms: amplitudes per species (stiff trunk, long whippy fronds, fluttering leaflets)
        K.add_wind(o, trunk=W['trunk'] * H, branch=W['branch'], leaf=W['leaf'], flex=1.0)
    else:
        K.add_wind(o, trunk=.02 * H, branch=.22 + .006 * H, leaf=.05, flex=1.0 if D['category'] != 'Dead tree' else .35)   # amplitudes @ 10 m/s
    tag(o, D, 'tree', st); print('TREE', D['name'], st, flush=True)
for D in [t for t in RG.SHRUBS if t['name'].startswith(REG + '_')]:
    c = coll(f"T6_{D['name']}", groups['SHRUBS'])
    o, st = RG.build_woody(D, 0, c)
    K.add_wind(o, trunk=.04, branch=.12 if not D['category'].startswith('Dead') else .05, leaf=.03)
    tag(o, D, 'shrub', st); print('SHRUB', D['name'], st, flush=True)
for D in [p for p in RG.PLANTS if p['name'].startswith(REG + '_')]:
    c = coll(f"T6_{D['name']}", groups['PLANTS'])
    o, st = RG.build_plant(D, 0, c)
    W = D.get('wind')
    if W and (W['branch'] > 0 or W['leaf'] > 0):
        K.add_wind(o, trunk=0.0, branch=W['branch'], leaf=W['leaf'])
    elif not W and D['kind'] not in ('moss', 'mushrooms'):
        K.add_wind(o, trunk=0.0, branch=.30 if D['kind'] != 'vine' else .5, leaf=.03 if D['kind'] != 'lotus' else .012)
    tag(o, D, 'plant', st); print('PLANT', D['name'], st, flush=True)

make_scatter_copies([bpy.data.objects[n] for n in INV], f'T6_LIB_{NAMES[REG]}')
# ---------------------------------------------------------------- browse scene: instances in a row, sorted by height
lu = bpy.data.scenes.new('T6_LINEUP'); lu.unit_settings.system = 'METRIC'
x = 0.0
items = sorted(INV.items(), key=lambda kv: -kv[1]['stats']['height_m'])
for name, v in items:
    st = v['stats']; w = max(st.get('canopy_x_m', st.get('spread_x_m', .5)), .4)
    e = bpy.data.objects.new(f'LINEUP_{name}', None); e.instance_type = 'COLLECTION'
    e.instance_collection = bpy.data.collections[v['collection']]; e.location = (x + w / 2, 0, 0)
    lu.collection.objects.link(e); x += w + max(.5, w * .15)
lu.collection.objects.link(bpy.data.objects['T6_WIND_CONTROL'])

# ---------------------------------------------------------------- checks + save (backup the previous version first)
missing = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath))]
assert not missing, missing
if os.path.exists(OUT):
    bdir = os.path.join(LIB, '_backups'); os.makedirs(bdir, exist_ok=True)
    shutil.copy2(OUT, os.path.join(bdir, os.path.basename(OUT)[:-6] + '__backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.blend'))
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, relative_remap=True)
json.dump(INV, open(OUT[:-6].replace('_v001', '') + '_inventory.json', 'w'), indent=1)
print('SAVED', OUT, round(os.path.getsize(OUT) / 1e6, 1), 'MB', len(INV), 'assets')
print('T6_LIBRARY_DONE')

"""TASK 05 · automated technical QC (runs inside Blender 4.5; also usable in 5.x) → 12_RENDER/T5/qc/qc_t5_<version>.json

  blender -b -P t5_qc.py
Checks: files open · no missing images · terrain tiles evaluate to the expected grid + height range + mask attributes ·
LOD seams (crack size hidden by skirts) · v001 reproduction · rivers never flow uphill · water above the river bed ·
lake shoreline closed by terrain · scatter instances exist + avoid paths / water / Ashram pad · PBR channels on every material ·
2K textures · file sizes < 100 MB (GitHub) · TASK 04 baseline untouched.
"""
import os, sys, json, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
from mathutils import Vector
import worldkit as wk

R = []


def chk(name, ok, detail=''):
    R.append(dict(check=name, result='PASS' if ok else 'FAIL', detail=detail))
    print(('PASS ' if ok else 'FAIL ') + name + ' — ' + str(detail), flush=True)


DATA = wk.P('08_ASHRAM_VALLEY', 'data_v002')
PREP = json.load(open(os.path.join(DATA, 'prep_v002.json'))); TD = PREP['tile_defs']
FILES = ['11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend', '14_NATURE_LIBRARY/T5_NATURE_LIBRARY_TREES_v002.blend',
         '14_NATURE_LIBRARY/T5_NATURE_LIBRARY_GROUND_v002.blend', '08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend',
         '04_FORESTS/FOREST_NORTH_BELT_v002.blend', '03_MOUNTAINS/MOUNTAIN_NW01_v002.blend', '05_RIVERS_AND_LAKES/WATER_v002.blend',
         '00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend']
# ---------------------------------------------------------------- 1. files: size, open, missing images, material channels
for f in FILES:
    p = wk.P(*f.split('/'))
    sz = os.path.getsize(p) / 1e6
    chk(f'file size < 100 MB: {f}', sz < 100, f'{sz:.1f} MB')
    bpy.ops.wm.open_mainfile(filepath=p)
    miss = [im.name for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath, library=im.library))]
    chk(f'opens + no missing images: {f}', not miss, f'{len(bpy.data.images)} images, missing {miss[:5]}')
    if f.startswith('11_'):
        bad = []
        for m in bpy.data.materials:
            if not m.name.startswith('MAT_T5_') or m.name in ('MAT_T5_MIST', 'MAT_T5_HAZE'):
                continue
            bs = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if bs is None:
                bad.append(m.name + ':no BSDF'); continue
            procedural = m.name in ('MAT_T5_TRUNK_FAR', 'MAT_T5_FOAM', 'MAT_T5_WATERFALL')   # constant / procedural colour by design
            need = ([] if procedural else ['Base Color', 'Normal']) + ['Roughness']
            miss_ = [k for k in need if not bs.inputs[k].is_linked and k != 'Roughness' or (k == 'Roughness' and not bs.inputs[k].is_linked and bs.inputs[k].default_value <= 0)]
            if bs.inputs['Metallic'].default_value != 0 or bs.inputs['Metallic'].is_linked:
                miss_.append('metallic≠0')
            if miss_:
                bad.append(f'{m.name}:{miss_}')
        chk('PBR channels (Base Color / Roughness / Normal, Metallic 0) on every terrain material', not bad, bad or 'all OK')
        res = sorted({tuple(im.size) for im in bpy.data.images if im.source == 'FILE'})
        chk('texture resolution = 2K (2048²) for all Poly Haven maps', res == [(2048, 2048)], res)
# ---------------------------------------------------------------- 2. master: terrain tiles, seams, water, scatter
bpy.ops.wm.open_mainfile(filepath=wk.P('00_MASTER_WORLD', 'T5_LANDSCAPE_master_v002.blend'))
sc = bpy.context.scene
cam = bpy.data.objects['CAM_T5_02_FOREST_ESTABLISHING']; sc.camera = cam
dg = bpy.context.evaluated_depsgraph_get()
TILES = {}
for o in sc.objects:
    if o.name.startswith('T5_TERRAIN_'):
        k = o.name.split('_')[-1]; e = o.evaluated_get(dg); me = e.to_mesh()
        V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
        attrs = sorted(a.name for a in me.attributes if a.name.startswith('m_'))
        D = np.load(os.path.join(DATA, f'{k}.npz')); z = D['z']
        md = o.modifiers['HEIGHTFIELD']
        ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
        vres = md[ids['Viewport Resolution']]
        exp_n = int(round((z.shape[1] - 1) * vres + 1))
        skirt = md[ids['Skirt Depth']]
        chk(f'terrain {k}: real mesh evaluates (viewport grid {exp_n}², z within data range incl. skirt, 14 mask attributes)',
            len(attrs) == 14 and len(me.vertices) >= .5 * exp_n * exp_n and V[:, 2].min() >= z.min() - skirt - .1
            and V[:, 2].max() <= z.max() + .1,
            f'{len(me.vertices)} verts, z {V[:, 2].max():.1f} max (data {z.max():.1f}), attrs {len(attrs)}')
        TILES[k] = (D, TD[k]); e.to_mesh_clear()


def bil(k, x, y):
    D, t = TILES[k]; z = D['z']; sp = t['sp']
    c = (x - t['x0']) / sp; r = (t['y1'] - y) / sp
    c0 = np.clip(np.floor(c).astype(int), 0, z.shape[1] - 2); r0 = np.clip(np.floor(r).astype(int), 0, z.shape[0] - 2)
    fx, fy = c - c0, r - r0
    return z[r0, c0] * (1 - fx) * (1 - fy) + z[r0, c0 + 1] * fx * (1 - fy) + z[r0 + 1, c0] * (1 - fx) * fy + z[r0 + 1, c0 + 1] * fx * fy


for fine, coarse, skirt in (('VH', 'L0', 3), ('L0', 'L1', 12), ('FH', 'L1', 3), ('L1', 'L2', 40), ('MT', 'L2', 60), ('WF', 'MT', 4)):
    t = TD[fine]; s = np.linspace(0, 1, 2000)
    xs = np.concatenate([t['x0'] + s * (t['x1'] - t['x0'])] * 2 + [np.full(2000, t['x0']), np.full(2000, t['x1'])])
    ys = np.concatenate([np.full(2000, t['y0']), np.full(2000, t['y1'])] + [t['y0'] + s * (t['y1'] - t['y0'])] * 2)
    gap = np.abs(bil(fine, xs, ys) - bil(coarse, xs, ys))
    chk(f'LOD seam {fine}↔{coarse}: border matches the parent surface (crack < skirt)', gap.max() < skirt * .9, f'max gap {gap.max():.2f} m (skirt {skirt} m), mean {gap.mean():.3f} m')
chk('approved v001 heights reproduced (valley, before detail)', PREP['verify_v001_max_abs_dz_m'] < .01, f"{PREP['verify_v001_max_abs_dz_m']:.2e} m")
chk('valley river levels unchanged vs v001', PREP['river_level_change_vs_v001']['max_in_valley_L1_m'] < .01, PREP['river_level_change_vs_v001'])
W = np.load(os.path.join(DATA, 'water.npz')); RIV, RIVO = W['RIV'], W['RIVO']
up = max(float(np.max(np.diff(RIV[RIVO[i]:RIVO[i + 1], 2]))) if RIVO[i + 1] - RIVO[i] > 1 else 0 for i in range(len(RIVO) - 1))
chk('rivers never flow uphill (water surface monotonic downstream)', up <= 1e-3, f'max rise {up:.4f} m over {len(RIVO) - 1} rivers')
for k in ('VH', 'FH', 'WF', 'L0'):
    t = TD[k]
    m = (RIV[:, 0] > t['x0'] + 5) & (RIV[:, 0] < t['x1'] - 5) & (RIV[:, 1] > t['y0'] + 5) & (RIV[:, 1] < t['y1'] - 5)
    if m.any():
        bed = bil(k, RIV[m, 0], RIV[m, 1]); water = RIV[m, 2] - .4
        bad = (bed > water + .05).mean()
        chk(f'water surface above the river bed in {k}', bad < .01, f'{m.sum()} centreline samples, {bad * 100:.2f}% bed above water')
lk = bpy.data.objects.get('T5_LAKE_SW')
if lk:
    me = lk.data; V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me)
    bvi = np.array(sorted({v.index for e in bm.edges if e.is_boundary for v in e.verts})); bm.free()
    P = V[bvi]; ins = (np.abs(P[:, 0]) < 159000) & (np.abs(P[:, 1]) < 159000)
    tz = bil('L2', P[ins, 0], P[ins, 1])
    chk('lake: water-plane edges lie under the terrain (shoreline = terrain ∩ level)', (tz > P[ins, 2]).mean() > .97,
        f'{(tz > P[ins, 2]).mean() * 100:.1f}% of {ins.sum()} edge vertices covered')
# scatter: instances per system for two shots + placement on bare ground
for cn in ('CAM_T5_02_FOREST_ESTABLISHING', 'CAM_T5_07_GROUND_LEVEL'):
    sc.camera = bpy.data.objects[cn]; bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    cnt = {}; pos = {}
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent and inst.parent.name.startswith('SC_'):
            n = inst.parent.name; cnt[n] = cnt.get(n, 0) + 1
            if cnt[n] < 4000:
                pos.setdefault(n, []).append(tuple(inst.matrix_world.translation))
    chk(f'scatter produces instances ({cn})', sum(cnt.values()) > 1000, cnt)
    for n, P in pos.items():
        if any(s in n for s in ('STONE', 'BOULDER', 'ROCK')):
            continue
        P = np.array(P); k = next((t for t in ('VH', 'FH', 'L0', 'L1') if t in n), None)
        if k is None:
            continue
        D, t = TILES[k]; sp = t['sp']
        c = np.clip(np.round((P[:, 0] - t['x0']) / sp).astype(int), 0, D['z'].shape[1] - 1)
        r = np.clip(np.round((t['y1'] - P[:, 1]) / sp).astype(int), 0, D['z'].shape[0] - 1)
        bare = np.maximum.reduce([D['MC'][r, c, 1] / 255, D['MB'][r, c, 1] / 255, (D['MA'][r, c, 3] / 255 > .9).astype(float)])
        chk(f'{n}: plants / trees not on paths, Ashram pad or water', (bare > .5).mean() < .02, f'{(bare > .5).mean() * 100:.2f}% of {len(P)} sampled')
# ---------------------------------------------------------------- 3. TASK 04 baseline untouched
man = json.load(open(wk.P('TASK04_BASELINE_MANIFEST.json')))
ch = [f for f, v in man['files'].items() if hashlib.sha256(open(wk.P(f), 'rb').read()).hexdigest() != v['sha256']]
chk('TASK 04 v001 baseline files unchanged', not ch, ch or f"{len(man['files'])} files identical")
os.makedirs(wk.P('12_RENDER', 'T5', 'qc'), exist_ok=True)
ver = bpy.app.version_string.split()[0]
out = dict(blender=bpy.app.version_string, time=time.strftime('%Y-%m-%d %H:%M'), passed=sum(r['result'] == 'PASS' for r in R),
           total=len(R), checks=R)
json.dump(out, open(wk.P('12_RENDER', 'T5', 'qc', f'qc_t5_{ver}.json'), 'w'), indent=1, default=str)
print(f"T5_QC {out['passed']}/{out['total']} PASS (Blender {bpy.app.version_string})")

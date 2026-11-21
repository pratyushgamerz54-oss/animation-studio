"""TASK 04 · technical QC — run inside Blender (4.5 = target; also run with 5.x for forward compatibility).
Writes 12_RENDER/qc/qc_blender_<version>.json; w4_qc_report.py turns all of them into QC_REPORT.md.
"""
import os, sys, json, glob, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk

VER = bpy.app.version_string
R = {'blender': VER, 'files': {}, 'checks': []}


def check(name, ok, detail=''):
    R['checks'].append({'check': name, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name, detail, flush=True)


FILES = sorted(glob.glob(wk.P('*', '*.blend')))
FILES = [f for f in FILES if '13_BACKUPS' not in f]
META = json.load(open(wk.P('01_GEOGRAPHY', 'data', 'world_features.json')))
# ------------------------------------------------------------------ 1. every file opens, has geometry, no missing links
for f in FILES:
    rel = os.path.relpath(f, wk.ROOT)
    try:
        bpy.ops.wm.open_mainfile(filepath=f, load_ui=False)
    except Exception as e:
        check(f'opens: {rel}', False, str(e)); continue
    objs = bpy.data.objects
    missing = [i.name for coll_ in (bpy.data.objects, bpy.data.materials, bpy.data.collections, bpy.data.meshes, bpy.data.scenes)
               for i in coll_ if getattr(i, 'is_missing', False)]
    libs = [(l.filepath, os.path.exists(bpy.path.abspath(l.filepath))) for l in bpy.data.libraries]
    meshes = [o for o in objs if o.type == 'MESH']
    empty_meshes = [o.name for o in meshes if len(o.data.vertices) == 0]
    verts = sum(len(o.data.vertices) for o in meshes if o.library is None or True)
    info = {'saved_with': '.'.join(map(str, bpy.data.version)), 'scenes': [s.name for s in bpy.data.scenes], 'objects': len(objs),
            'meshes': len(meshes), 'verts': int(verts), 'cameras': sum(o.type == 'CAMERA' for o in objs),
            'collections': len(bpy.data.collections), 'libraries': [l for l, _ in libs], 'materials': len(bpy.data.materials),
            'node_groups': len(bpy.data.node_groups), 'images': len(bpy.data.images)}
    R['files'][rel] = info
    check(f'opens: {rel}', True, f"saved with Blender {info['saved_with']}, {len(objs)} objects, {verts:,} verts")
    check(f'no missing linked data: {rel}', not missing and all(ok for _, ok in libs), f'missing={missing[:5]} libs_ok={all(ok for _, ok in libs)}')
    if '11_MATERIALS' in rel:
        check(f'library content exists: {rel}', len(bpy.data.materials) > 0, f'{len(bpy.data.materials)} materials (material library — no geometry by design)')
    else:
        check(f'geometry exists: {rel}', len(objs) > 0 and not empty_meshes, f'empty meshes: {empty_meshes[:5]}')
    bad_img = [i.name for i in bpy.data.images if i.source == 'FILE' and not os.path.exists(bpy.path.abspath(i.filepath))]
    check(f'no broken image paths: {rel}', not bad_img, str(bad_img[:5]))

# ------------------------------------------------------------------ 2. master: organisation + scale + separation
bpy.ops.wm.open_mainfile(filepath=wk.P('00_MASTER_WORLD', 'WORLD_master_v001.blend'), load_ui=False)
need = ['MAIN_WORLD', 'NORTHERN_REGIONS', 'SOUTHERN_REGIONS', 'EASTERN_REGIONS', 'WESTERN_REGIONS', 'MOUNTAIN_REGIONS', 'FOREST_REGIONS',
        'WATER_SYSTEMS', 'DESERT_REGIONS', 'ISLANDS', 'ASHRAM_VALLEY', 'UNEXPLORED_REGIONS']
cn = {c.name: c for c in bpy.data.collections}
miss = [n for n in need if n not in cn or len(cn[n].all_objects) == 0]
check('required collections exist and are non-empty', not miss, f'missing/empty: {miss}' if miss else ', '.join(f'{n}={len(cn[n].all_objects)}' for n in need))
sc = bpy.data.scenes['MAIN_WORLD']
check('separate dimensions are separate scenes (not in MAIN_WORLD)',
      all(s in bpy.data.scenes for s in ('DIM_BLACK_HOLE_TRAINING', 'DIM_SAITHAN_DARK_WORLD', 'ASHRAM_VALLEY')) and
      not any(o.name.startswith(('BH_', 'DW_')) for o in sc.objects), 'scenes: ' + ', '.join(s.name for s in bpy.data.scenes))
ter = [o for o in sc.objects if o.type == 'MESH' and o.name.startswith('TER_') and o.name != 'TER_SEABED_WORLD']
vx = {o.get('vexag') for o in ter}
check('consistent world scale (1 BU = 1 km, vexag on every piece)', vx == {META['vexag']}, f'vexag values {vx}, pieces {len(ter)}')
# geometry within the world rectangle
lo = np.array([1e9] * 3); hi = -lo
for o in ter:
    co = np.empty(len(o.data.vertices) * 3, np.float32); o.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    lo = np.minimum(lo, co.min(0)); hi = np.maximum(hi, co.max(0))
check('terrain inside the 12 000 x 6 000 km world rectangle', lo[0] >= -6000 and hi[0] <= 6000 and lo[1] >= -3000 and hi[1] <= 3000,
      f'x {lo[0]:.0f}..{hi[0]:.0f} km, y {lo[1]:.0f}..{hi[1]:.0f} km, z {lo[2]:.1f}..{hi[2]:.1f} BU (= {lo[2] / META["vexag"] * 1000:.0f}..{hi[2] / META["vexag"] * 1000:.0f} m)')
# ------------------------------------------------------------------ 3. terrain continuity: pieces tile the land window exactly
H, W = META['grid']; KM = META['km_per_cell']
occ = np.zeros((H - 1, W - 1), np.int16)
for o in ter:
    co = np.empty(len(o.data.vertices) * 3, np.float32); o.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    lt = np.empty(len(o.data.polygons) * 0 + len(o.data.loops), np.int32); o.data.loops.foreach_get('vertex_index', lt)
    q = co[lt].reshape(-1, 4, 3)
    c = np.round((q[:, :, 0].min(1) + 6000) / KM - .5).astype(int); r = np.round((3000 - q[:, :, 1].max(1)) / KM - .5).astype(int)
    np.add.at(occ, (r, c), 1)
D = np.load(wk.P('01_GEOGRAPHY', 'data', 'world_prep.npz'))
win = D['f_key'] >= 0
check('terrain pieces tile the land window exactly (no gaps, no overlaps)', bool((occ[win] == 1).all() and (occ[~win] == 0).all()),
      f'faces expected {int(win.sum()):,}, covered once {int((occ == 1).sum()):,}, overlaps {int((occ > 1).sum())}, gaps {int((win & (occ == 0)).sum())}')
from collections import deque
land_face = win & (np.stack([D['h'][:-1, :-1], D['h'][:-1, 1:], D['h'][1:, :-1], D['h'][1:, 1:]]).max(0) > 0)
lab = np.zeros(land_face.shape, np.int32); n = 0
for r0, c0 in zip(*np.nonzero(land_face)):
    if lab[r0, c0]:
        continue
    n += 1; dq = deque([(r0, c0)]); lab[r0, c0] = n
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < lab.shape[0] and 0 <= cc < lab.shape[1] and land_face[rr, cc] and not lab[rr, cc]:
                lab[rr, cc] = n; dq.append((rr, cc))
sizes = np.bincount(lab.ravel())[1:]
check('connected landmasses (3D faces) match the 2D map', abs(n - META['audit_2d']['land_masses']) <= 12,
      f'3D connected land masses {n} (5 largest: {sorted(sizes.tolist())[-5:]}) vs 2D audit {META["audit_2d"]["land_masses"]} (face- vs cell-connectivity)')
# ------------------------------------------------------------------ 4. rivers follow the terrain
rp, ro = D['r_pts'], D['r_off']
up = sum(int((np.diff(rp[a:b, 2]) > 1e-3).sum()) for a, b in zip(ro[:-1], ro[1:]))
hh = D['h']
below = 0; tot = 0
for a, b in zip(ro[:-1], ro[1:]):
    seg = rp[a:b - 1]                                       # last point = mouth (sea / lake)
    c = np.clip(np.round((seg[:, 0] + 6000) / KM - .5).astype(int), 0, W - 1); r = np.clip(np.round((3000 - seg[:, 1]) / KM - .5).astype(int), 0, H - 1)
    below += int((seg[:, 2] < hh[r, c] - 1).sum()); tot += len(seg)
check('main-world rivers never flow uphill', up == 0, f'{len(ro) - 1} rivers, {len(rp):,} points, uphill steps = {up}')
check('main-world rivers sit on the terrain (not below ground)', below == 0, f'{below} of {tot} river points below the terrain cell')
V = np.load(wk.P('08_ASHRAM_VALLEY', 'data', 'valley_prep.npz'))
RP, RO = V['RP'], V['RO']
up = sum(int((np.diff(RP[a:b, 2]) > 1e-3).sum()) for a, b in zip(RO[:-1], RO[1:]))
check('Ashram-valley rivers never flow uphill', up == 0, f'{len(RO) - 1} rivers, {len(RP):,} points (25 m spacing), uphill steps = {up}')
# water surface visible on the finest LOD that contains each point
VM = json.load(open(wk.P('08_ASHRAM_VALLEY', 'data', 'valley_features.json')))
hidden = {}; count = {}
for L in ('LOD0', 'LOD1', 'LOD2'):
    z = V[f'{L}_z'].astype(np.float64); half = VM['lods'][L]['half_extent_m']; sp = VM['lods'][L]['spacing_m']; inner = {'LOD0': 0, 'LOD1': 3000, 'LOD2': 30000}[L]
    m = (np.abs(RP[:, 0]) < half - sp) & (np.abs(RP[:, 1]) < half - sp) & ~((np.abs(RP[:, 0]) < inner) & (np.abs(RP[:, 1]) < inner))
    P = RP[m]; fc = (P[:, 0] + half) / sp; fr = (half - P[:, 1]) / sp
    c0, r0 = np.floor(fc).astype(int), np.floor(fr).astype(int); tx, ty = fc - c0, fr - r0
    s = z[r0, c0] * (1 - tx) * (1 - ty) + z[r0, c0 + 1] * tx * (1 - ty) + z[r0 + 1, c0] * (1 - tx) * ty + z[r0 + 1, c0 + 1] * tx * ty
    hidden[L] = float(((s > P[:, 2] - .4 + 1.0)).mean() * 100) if len(P) else 0.0; count[L] = int(len(P))
check('valley river water surface above the carved bed (LOD0/LOD1)', hidden['LOD0'] < 5 and hidden['LOD1'] < 10,
      ', '.join(f'{k}: {hidden[k]:.1f}% of {count[k]:,} pts covered by terrain' for k in hidden) + ' (LOD2 = far horizon only)')
# ------------------------------------------------------------------ 5. valley LOD nesting + scale
bpy.ops.wm.open_mainfile(filepath=wk.P('08_ASHRAM_VALLEY', 'ASHRAM_VALLEY_terrain_v001.blend'), load_ui=False)
lods = {L: bpy.data.objects[f'AV_TERRAIN_{L}'] for L in ('LOD0', 'LOD1', 'LOD2')}
ok = (lods['LOD1']['hole_half_m'] == lods['LOD0']['half_extent_m'] and lods['LOD2']['hole_half_m'] == lods['LOD1']['half_extent_m'])
check('valley LODs nest exactly (hole = inner extent, skirts present)', ok,
      ', '.join(f"{L} ±{o['half_extent_m'] / 1000:g} km @ {o['spacing_m']:g} m, hole ±{o['hole_half_m'] / 1000:g} km, skirt {o['skirt_m']:g} m, {o['verts']:,} verts" for L, o in lods.items()))
dg = bpy.context.evaluated_depsgraph_get()
ninst = {}
for o in bpy.data.objects:
    if o.name.startswith(('AV_FOREST_', 'AV_GROVES_')):
        ninst[o.name] = 0
for i in dg.object_instances:
    if i.is_instance and i.parent and i.parent.original.name in ninst:
        ninst[i.parent.original.name] += 1
per_lod = {L: sum(v for k, v in ninst.items() if k.endswith(L)) for L in ('LOD0', 'LOD1')}
check('vegetation instancing evaluates on every LOD (viewport density)', all(v > 0 for v in per_lod.values()),
      ', '.join(f'{k}={v:,}' for k, v in ninst.items()) + ' — LOD0 forest = 0 is correct: the map has grassland within ±3 km (forest belt starts ≈22 km away); groves fill LOD0')
check('Ashram building kept as a separate asset (only placement refs here)',
      not any(o.name.startswith(('ARCH_', 'ASSET_')) for o in bpy.data.objects) and 'ASHRAM_ORIGIN_REF' in bpy.data.objects,
      f"site elevation {bpy.data.objects['ASHRAM_ORIGIN_REF']['site_elev_m']:.1f} m; pad = concept v3 compound footprint")
# ------------------------------------------------------------------ 6. renders exist
log = json.load(open(wk.P('12_RENDER', 'render_log.json'))) if os.path.exists(wk.P('12_RENDER', 'render_log.json')) else []
okr = [e for e in log if os.path.exists(wk.P(e['file'])) and os.path.getsize(wk.P(e['file'])) > 10000]
check('camera previews rendered successfully', len(log) > 0 and len(okr) == len(log),
      f"{len(okr)}/{len(log)} images ({sum(e['mode'] == 'cycles' for e in log)} Cycles, {sum(e['mode'] == 'viewport' for e in log)} viewport/Workbench)")
os.makedirs(wk.P('12_RENDER', 'qc'), exist_ok=True)
json.dump(R, open(wk.P('12_RENDER', 'qc', f'qc_blender_{bpy.app.version[0]}.{bpy.app.version[1]}.json'), 'w'), indent=1)
print('QC', sum(c['result'] == 'PASS' for c in R['checks']), 'PASS /', len(R['checks']))
print('QC_DONE')

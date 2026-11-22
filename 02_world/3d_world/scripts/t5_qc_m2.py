"""TASK 05 · milestone-2 QC (Blender 4.5) → 12_RENDER/T5/qc/qc_t5_m2_<version>.json
Files open / no missing images / < 100 MB · every region tile evaluates to a real mesh with mask attributes · nested tile borders
match their parent surface · region rivers never flow uphill · v001 baseline untouched."""
import os, sys, json, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk

R = []


def chk(name, ok, detail=''):
    R.append(dict(check=name, result='PASS' if ok else 'FAIL', detail=detail)); print(('PASS ' if ok else 'FAIL ') + name + ' — ' + str(detail), flush=True)


FILES = ['06_DESERTS/DESERT_R04_v002.blend', '06_DESERTS/FORBIDDEN_R05_v002.blend', '04_FORESTS/ENCHANTED_FOREST_R02_v002.blend',
         '03_MOUNTAINS/GREAT_NORTHERN_RANGE_R03_v002.blend', '02_TERRAIN/WORLD_terrain_v002.blend',
         '00_MASTER_WORLD/T5_REGION_R04_DESERT_master_v002.blend', '00_MASTER_WORLD/T5_REGION_R05_FORBIDDEN_master_v002.blend',
         '00_MASTER_WORLD/T5_REGION_R02_ENCHANTED_master_v002.blend', '00_MASTER_WORLD/T5_REGION_R03_RANGE_master_v002.blend',
         '11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend']
for f in FILES:
    p = wk.P(*f.split('/')); sz = os.path.getsize(p) / 1e6
    chk(f'file size < 100 MB: {f}', sz < 100, f'{sz:.1f} MB')
    bpy.ops.wm.open_mainfile(filepath=p)
    miss = [im.name for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath, library=im.library))]
    chk(f'opens + no missing images: {f}', not miss, f'{len(bpy.data.images)} images, missing {miss[:5]}')
    if 'master' in f or f.startswith('11_'):
        continue
    sc = bpy.context.scene
    cd = bpy.data.cameras.new('QC'); co = bpy.data.objects.new('QC_CAM', cd); sc.collection.objects.link(co); sc.camera = co
    dg = bpy.context.evaluated_depsgraph_get()
    for o in sc.objects:
        if o.name.startswith('T5_TERRAIN_') or o.name == 'T5_WORLD_TERRAIN':
            me = o.evaluated_get(dg).to_mesh()
            na = len([a for a in me.attributes if a.name.startswith('m_')])
            chk(f'{f}: {o.name} evaluates to a real mesh with mask attributes', len(me.vertices) > 1000 and na >= 14,
                f'{len(me.vertices)} viewport verts, {na} mask attributes')
            o.evaluated_get(dg).to_mesh_clear()


def bil(z, x0, y1, sp, x, y):
    c = (x - x0) / sp; r = (y1 - y) / sp
    c0 = np.clip(np.floor(c).astype(int), 0, z.shape[1] - 2); r0 = np.clip(np.floor(r).astype(int), 0, z.shape[0] - 2)
    fx, fy = c - c0, r - r0
    return z[r0, c0] * (1 - fx) * (1 - fy) + z[r0, c0 + 1] * fx * (1 - fy) + z[r0 + 1, c0] * (1 - fx) * fy + z[r0 + 1, c0 + 1] * fx * fy


def seam(data, fine, coarse, rects, skirt):
    zf = np.load(os.path.join(data, f'{fine}.npz'))['z'].astype(float); zc = np.load(os.path.join(data, f'{coarse}.npz'))['z'].astype(float)
    (fx0, fx1, fy0, fy1, fsp), (cx0, cx1, cy0, cy1, csp) = rects[fine], rects[coarse]
    s = np.linspace(0, 1, 2000)
    xs = np.concatenate([fx0 + s * (fx1 - fx0)] * 2 + [np.full(2000, fx0), np.full(2000, fx1)])
    ys = np.concatenate([np.full(2000, fy0), np.full(2000, fy1)] + [fy0 + s * (fy1 - fy0)] * 2)
    g = np.abs(bil(zf, fx0, fy1, fsp, xs, ys) - bil(zc, cx0, cy1, csp, xs, ys))
    chk(f'LOD seam {fine}↔{coarse}: border matches the parent surface', g.max() < skirt * .9, f'max gap {g.max():.2f} m (skirt {skirt} m)')


for folder, rk, pairs in (('06_DESERTS', 'R04', (('DN', 'DF', 20), ('DH', 'DN', 3))), ('06_DESERTS', 'R05', (('XN', 'XF', 20), ('XH', 'XN', 3))),
                          ('04_FORESTS', 'R02', (('EN', 'EF', 12), ('EH', 'EN', 3)))):
    data = wk.P(folder, 'data_v002'); RJ = json.load(open(os.path.join(data, f'region_{rk}.json')))
    rects = {k: (-v['half'], v['half'], -v['half'], v['half'], v['sp']) for k, v in RJ['tiles'].items()}
    for a, b, sk in pairs:
        seam(data, a, b, rects, sk)
    wf = os.path.join(data, 'water.npz' if rk == 'R04' else f'water_{rk}.npz')
    if os.path.exists(wf):
        W = np.load(wf); RIV, RIVO = W['RIV'], W['RIVO']
        up = max([float(np.max(np.diff(RIV[RIVO[i]:RIVO[i + 1], 2]))) for i in range(len(RIVO) - 1) if RIVO[i + 1] - RIVO[i] > 1] or [0])
        chk(f'{rk}: drainage lines never flow uphill', up <= 1e-3, f'max rise {up:.4f} m over {len(RIVO) - 1} lines')
PJ = json.load(open(wk.P('08_ASHRAM_VALLEY', 'data_v002', 'prep_v002.json'))); TD = PJ['tile_defs']
rects = {k: (TD[k]['x0'], TD[k]['x1'], TD[k]['y0'], TD[k]['y1'], TD[k]['sp']) for k in ('R3N', 'R3F', 'CV')}
seam(wk.P('08_ASHRAM_VALLEY', 'data_v002'), 'R3N', 'R3F', rects, 60)
seam(wk.P('08_ASHRAM_VALLEY', 'data_v002'), 'CV', 'R3F', rects, 4)
man = json.load(open(wk.P('TASK04_BASELINE_MANIFEST.json')))
ch = [f for f, v in man['files'].items() if hashlib.sha256(open(wk.P(f), 'rb').read()).hexdigest() != v['sha256']]
chk('TASK 04 v001 baseline files unchanged', not ch, ch or f"{len(man['files'])} files identical")
ver = bpy.app.version_string.split()[0]
out = dict(blender=bpy.app.version_string, time=time.strftime('%Y-%m-%d %H:%M'), passed=sum(r['result'] == 'PASS' for r in R), total=len(R), checks=R)
os.makedirs(wk.P('12_RENDER', 'T5', 'qc'), exist_ok=True)
json.dump(out, open(wk.P('12_RENDER', 'T5', 'qc', f'qc_t5_m2_{ver}.json'), 'w'), indent=1, default=str)
print(f"T5_QC_M2 {out['passed']}/{out['total']} PASS")

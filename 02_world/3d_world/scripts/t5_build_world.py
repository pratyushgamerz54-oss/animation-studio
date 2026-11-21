"""TASK 05 · main-world terrain v002 → 02_TERRAIN/WORLD_terrain_v002.blend (Blender 4.5).
Whole map as ONE real mesh from a 32-bit heightfield (NG_T5_HEIGHTFIELD), 3.9 km grid, display relief ×20 (as v001),
biome colours from the map, ocean, 26 lakes as flat planes at their levels (smooth shores), world cameras.
v001 world files stay untouched (frozen baseline)."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk
import t5kit as tk
from t5kit import NB, lin

D = np.load(wk.P('01_GEOGRAPHY', 'data_v002', 'world_v002.npz')); MJ = json.load(open(wk.P('01_GEOGRAPHY', 'data_v002', 'world_v002.json')))
z = D['z'].astype(np.float64); col = D['col'].astype(np.float32); lab = D['lab']
VX = MJ['vexag']; ZS = VX / 1000.0; n, m = z.shape; KMc = MJ['km_per_cell']
STATUS = 'TASK 05 main world v002 — map revision 01 = PROPOSAL (not canon); v001 untouched'
wk.new_file(); sc = bpy.context.scene; sc.name = 'T5_MAIN_WORLD'
sc['status'] = STATUS; sc['units'] = '1 BU = 1 km; Z = metres × 0.02 (relief ×20, same as v001)'
top = wk.coll('T5_MAIN_WORLD'); ct = wk.coll('T5_WORLD_TERRAIN', top); cw = wk.coll('T5_WORLD_WATER', top); cc = wk.coll('T5_WORLD_CAMERAS', top)
MAT = wk.link_materials(['MAT_T5_WATER_LAKE'], tk.MATLIB2)
# world material: map biome colour (attributes) + snow on high peaks + slope darkening
m_, = [bpy.data.materials.new('MAT_T5_WORLD')]; m_.use_nodes = True; nt = m_.node_tree; nt.nodes.clear(); b = NB(nt)
out = b.node('ShaderNodeOutputMaterial'); bs = b.node('ShaderNodeBsdfPrincipled'); b.link(bs.outputs[0], out.inputs['Surface'])
cr = b.node('ShaderNodeCombineColor')
for i, a in enumerate(('m_forest', 'm_rock', 'm_snow')):
    b.link(b.attr(a), cr.inputs[i])
geo = b.node('ShaderNodeNewGeometry'); pz = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Position'], pz.inputs[0])
nz = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Normal'], nz.inputs[0])
v = b.node('ShaderNodeTexCoord').outputs['Object']
base = b.mixc(b.math('MULTIPLY', b.noise(v, 1 / 30.0, 5, .6), .25), cr.outputs[0], lin('#5A5248'))
base = b.mixc(b.maprange(nz.outputs['Z'], .9, .6), base, lin('#6E675E'))                      # rock on steep relief
base = b.mixc(b.maprange(b.math('ADD', pz.outputs['Z'], b.math('MULTIPLY', b.noise(v, 1 / 20.0, 3, .5), 8)), 4200 * ZS, 5000 * ZS), base, lin('#F2F5F8'))
b.link(base, bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = .85
hf = tk.heightfield_group()
hdir = wk.P('02_TERRAIN', 'heightfields_v002')
H = tk.img_float('HF_WORLD_height', (np.where(z > 0, z, z) * ZS).astype(np.float32), os.path.join(hdir, 'WORLD_height.exr'))
C8 = np.clip(np.round(col * 255), 0, 255).astype(np.uint8)
MAi = tk.img_rgb('HF_WORLD_MA', C8, os.path.join(hdir, 'WORLD_MA.png'))
Z8 = np.zeros((n, m, 3), np.uint8)
MBi = tk.img_rgb('HF_WORLD_ZERO', Z8, os.path.join(hdir, 'WORLD_ZERO.png'))
o = bpy.data.objects.new('T5_WORLD_TERRAIN', bpy.data.meshes.new('T5_WORLD_TERRAIN')); ct.objects.link(o)
md = o.modifiers.new('HEIGHTFIELD', 'NODES'); md.node_group = hf
half_x, half_y = m * KMc / 2, n * KMc / 2
tk.set_mod(md, **{'Height': H, 'Mask MA': MAi, 'Mask MB': MBi, 'Mask MC': MBi, 'Mask MD': MBi, 'Min X': -half_x, 'Max X': half_x,
                  'Min Y': -half_y, 'Max Y': half_y, 'Viewport Resolution': .35, 'Render Resolution': 1.0, 'Skirt Depth': 5.0, 'Material': m_})
wk.add_props(o, status=STATUS, grid=[n, m], km_per_cell=KMc, note='coastline = terrain ∩ 0; lakes = planes at their levels (smooth shores)')
# ocean + lakes
oc = wk.box('T5_WORLD_OCEAN', (half_x * 2 + 400, half_y * 2 + 400, .02), (0, 0, -.01), cw, MAT['MAT_T5_WATER_LAKE'])
gx = (np.arange(m) + .5) * KMc - half_x; gy = half_y - (np.arange(n) + .5) * KMc
for L in MJ['lakes']:
    r0, r1, c0, c1 = L['bbox_rc']; r0, c0 = max(r0 - 1, 0), max(c0 - 1, 0); r1, c1 = min(r1 + 2, n - 1), min(c1 + 2, m - 1)
    sub = z[r0:r1 + 1, c0:c1 + 1]; nn, mm_ = sub.shape
    X, Y = np.meshgrid(gx[c0:c1 + 1], gy[r0:r1 + 1])
    Fq = wk.grid_faces(nn, mm_).reshape(-1, 4)
    lk = lab[r0:r1 + 1, c0:c1 + 1] == L['id']
    msk = lk.copy()
    for _ in range(2):
        msk = msk | np.roll(msk, 1, 0) | np.roll(msk, -1, 0) | np.roll(msk, 1, 1) | np.roll(msk, -1, 1)
    fz = (msk.ravel() & (sub.ravel() < L['level_m'] + 1))[Fq].any(1)
    if not fz.any():
        continue
    V, Fk, _ = wk.subset(np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, L['level_m'] * ZS)]), Fq[fz])
    lo = wk.mesh_from_arrays(f'T5_WORLD_LAKE_{L["id"]:02d}', V, Fk, cw, MAT['MAT_T5_WATER_LAKE']); wk.set_float_attr(lo, 'foam', np.zeros(len(V)))
    wk.add_props(lo, status=STATUS, level_m=L['level_m'])
# light + sky + cameras (overview, Aetheria lake district, home-continent range)
wk.sun('T5_WORLD_SUN', 35, 215, 4.0, top, 1.0)
sc.world = wk.sky_world('T5_WORLD_SKY', 35, 215, .3)
F = json.load(open(wk.P('01_GEOGRAPHY', 'data', 'world_features.json')))
ash = F['markers']['ashram'][0]
cams = [('CAM_T5_W01_WORLD', (0, -5200, 3200), (0, 300, 0), 30, 'Main world v002 — all continents, oceans, lakes (relief ×20)'),
        ('CAM_T5_W02_AETHERIA', (ash[0] + 300, ash[1] - 1500, 420), (ash[0] - 300, ash[1] + 150, 20), 30,
         'Aetheria (home continent) v002 — smooth lake shores, coasts, ranges around the Ashram valley (relief ×20)'),
        ('CAM_T5_W03_COAST_ISLANDS', (-500, -900, 260), (-200, 150, 0), 32, 'Western archipelago / coasts v002 — island outlines at 3.9 km (relief ×20)')]
for nm, loc, tgt, lens, desc in cams:
    co = wk.camera(nm, loc, tgt, lens, cc, clip=(.5, 50000)); co['description'] = desc
sc.camera = bpy.data.objects['CAM_T5_W01_WORLD']
wk.setup_cycles(sc, (1280, 720), 32)
wk.viewport_defaults(sc, 50000)
wk.save(wk.P('02_TERRAIN', 'WORLD_terrain_v002.blend'))
print('T5_WORLD_DONE', len(MJ['lakes']))

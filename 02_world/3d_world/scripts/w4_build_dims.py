"""TASK 04 · separate dimensions → 09_DIMENSIONS/*.blend (Blender 4.5). Each dimension = its OWN file + scene,
own origin and scale (1 BU = 1 m). They are never placed in or merged with the main world. No portal connections, travel
rules or inhabitants are modelled or implied. Layouts = PROPOSALS from MAP_H1 / MAP_H2 (same seeds).

GEM location: NOT confirmed → no environment built (only a proposal marker exists in the main world, 01_GEOGRAPHY).
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk

DD = wk.P('09_DIMENSIONS', 'data')

# ================================================================== H1 BLACK HOLE TRAINING AREA
BH = json.load(open(os.path.join(DD, 'black_hole_layout.json')))
wk.new_file()
M = wk.link_materials()
sc = bpy.context.scene; sc.name = 'DIM_BLACK_HOLE_TRAINING'
sc['status'] = BH['status']; sc['units'] = BH['unit']; sc['note'] = 'separate dimension — own space, no shared coordinates with the main world'
top = wk.coll('DIM_BLACK_HOLE_TRAINING')
C = {k: wk.coll(k, top) for k in ('BH_CORE', 'BH_PLATFORMS_INNER_RING', 'BH_PLATFORMS_TRAINING_RINGS', 'BH_PLATFORMS_OUTER_RING',
                                   'BH_DEBRIS_FIELD', 'BH_GUIDES', 'BH_CAMERAS')}
b = BH['black_hole']
hor = wk.blob('BH_EVENT_HORIZON', b['horizon_radius'], C['BH_CORE'], M['MAT_D_HORIZON'], subdiv=4, rough=0)
wk.display_color(hor, '#050508')
import bmesh
# accretion disk: flat annulus (thin), emissive gradient by radius
n = 128; a = np.linspace(0, 2 * np.pi, n, endpoint=False)
rings = np.linspace(b['disk_inner'], b['disk_outer'], 10)
V = np.concatenate([np.column_stack([np.cos(a) * r, np.sin(a) * r, np.zeros(n)]) for r in rings])
F = [[i * n + k, i * n + (k + 1) % n, (i + 1) * n + (k + 1) % n, (i + 1) * n + k] for i in range(len(rings) - 1) for k in range(n)]
disk = wk.mesh_from_arrays('BH_ACCRETION_DISK', V, np.array(F), C['BH_CORE'], M['MAT_D_ACCRETION'])
disk.rotation_euler = (math.radians(4), 0, 0); disk.modifiers.new('thick', 'SOLIDIFY').thickness = 6
wk.display_color(disk, '#FF9A3C')
ph = wk.ring_curve_mesh('BH_PHOTON_RING', b['photon_ring'], 0, 128, 8, C['BH_CORE'], M['MAT_D_PHOTON_RING'])
ph.rotation_euler = (math.radians(90), 0, 0); wk.display_color(ph, '#FFE2B0')
plat_mesh = {}
rng = np.random.default_rng(5)
for i, p in enumerate(BH['platforms']):
    key = {'INNER RING': 'BH_PLATFORMS_INNER_RING', 'TRAINING RINGS': 'BH_PLATFORMS_TRAINING_RINGS', 'OUTER RING': 'BH_PLATFORMS_OUTER_RING'}[p['ring']]
    r = p['radius']
    rock = wk.cone(f'BH_PLATFORM_{i + 1:02d}', r, r * 1.1, 12, C[key], M['MAT_D_PLATFORM_ROCK'], z0=-r * 1.1)   # inverted cone = floating rock
    me = rock.data
    for v in me.vertices:                              # flip apex downward + roughen
        v.co.z = -v.co.z - r * 1.1 if v.co.z > -r * 1.1 + 1e-3 else 0.0
        v.co.x *= 1 + rng.uniform(-.08, .08); v.co.y *= 1 + rng.uniform(-.08, .08)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    topd = wk.cone(f'BH_PLATFORM_{i + 1:02d}_TOP', r * .98, 1.5, 24, C[key], M['MAT_D_PLATFORM_TOP'], r_top=r * .96)
    for o in (rock, topd):
        o.location = (p['x'], p['y'], p['z']); wk.display_color(o, '#7A7068')
    rock['ring'] = p['ring']; rock['radius_m'] = r; rock['note'] = 'PROPOSED floating training platform (MAP_H1)'
deb = wk.blob('BH_DEBRIS_ROCK_MESH', 1.0, None, M['MAT_D_PLATFORM_ROCK'], subdiv=1, rough=.35, seed=3).data
for i, d in enumerate(BH['debris']):
    o = bpy.data.objects.new(f'BH_DEBRIS_{i + 1:03d}', deb); o.location = (d['x'], d['y'], d['z']); o.scale = (d['s'],) * 3
    o.rotation_euler = tuple(rng.uniform(0, 6.28, 3)); C['BH_DEBRIS_FIELD'].objects.link(o)
wk.display_color(bpy.data.objects['BH_DEBRIS_001'], '#6C645C')
for r_, lab, nn in BH['zones']:
    g = wk.ring_curve_mesh(f'BH_GUIDE_{lab.replace(" ", "_")}_{r_}M', r_, 0, 160, 2, C['BH_GUIDES'], M['MAT_D_LENSING_HALO']); g.hide_render = True
    wk.text(f'BH_LBL_{lab.replace(" ", "_")}', f'{lab} ({nn}) — proposal', (r_ * .7, -r_ * .72, 40), 26, C['BH_GUIDES'], M['MAT_D_PHOTON_RING'],
            rot=(math.radians(60), 0, 0)).hide_render = True
lc = wk.coll('BH_LIGHTING', top)
for nm, el, az, en, col in (('BH_DISK_LIGHT_N', 8, 0, 1.6, (1, .6, .3)), ('BH_DISK_LIGHT_S', 8, 180, 1.6, (1, .6, .3)),
                            ('BH_DISK_LIGHT_E', 8, 90, 1.2, (1, .6, .3)), ('BH_DISK_LIGHT_W', 8, 270, 1.2, (1, .6, .3)),
                            ('BH_LENSING_FILL', 60, 200, .25, (.29, .42, 1.0))):
    l = wk.sun(nm, el, az, en, lc, 2); l['note'] = 'stand-in for the accretion-disk glow (blockout lighting)'
w = bpy.data.worlds.new('BH_VOID'); w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (.002, .002, .005, 1); bg.inputs['Strength'].default_value = 1
sc.world = w
for nm, loc, tgt, lens, desc in (('CAM_D1_BH_OVERVIEW', (0, -2300, 1100), (0, 0, -60), 32, 'Overview — black hole + three platform rings (proposal)'),
                                 ('CAM_D1_BH_TRAINING_RING', (820, -520, 90), (-200, 300, 0), 28, 'On the training ring — platforms toward the disk'),
                                 ('CAM_D1_BH_TOP', (0, 0, 3000), (0, 0, 0), 40, 'Top layout check vs MAP_H1')):
    c = wk.camera(nm, loc, tgt, lens, C['BH_CAMERAS'], clip=(1, 50000)); c['description'] = desc
sc.camera = bpy.data.objects['CAM_D1_BH_OVERVIEW']
wk.setup_cycles(sc, (1280, 720), 24)
wk.save(wk.P('09_DIMENSIONS', 'DIM_black_hole_training_v001.blend'))

# ================================================================== H2 SAITHAN'S DARK WORLD
DW = json.load(open(os.path.join(DD, 'dark_world_layout.json')))
T = np.load(os.path.join(DD, 'dark_world_terrain.npz'))
wk.new_file()
M = wk.link_materials()
sc = bpy.context.scene; sc.name = 'DIM_SAITHAN_DARK_WORLD'
sc['status'] = DW['status']; sc['units'] = DW['unit']; sc['note'] = 'separate dimension — own space; visually distinct from the Black Hole Training Area'
top = wk.coll('DIM_SAITHAN_DARK_WORLD')
C = {k: wk.coll(k, top) for k in ('DW_TERRAIN', 'DW_SPIRES', 'DW_CORRUPTED_PORTAL_SITE', 'DW_ATMOSPHERE', 'DW_GUIDES', 'DW_CAMERAS', 'DW_LIGHTING')}
z = T['z'].astype(np.float64); nr, nc = z.shape; st = DW['mesh_step_m']
xs = (np.arange(nc) - (nc - 1) / 2) * st; ys = ((nr - 1) / 2 - np.arange(nr)) * st
X, Y = np.meshgrid(xs, ys)
o = wk.mesh_from_arrays('DW_TERRAIN_ASH_PLAINS', np.stack([X, Y, z], -1).reshape(-1, 3), wk.grid_faces(nr, nc).reshape(-1, 4), C['DW_TERRAIN'], M['MAT_D_ASH_GROUND'])
wk.set_float_attr(o, 'fissure', T['fissure'].astype(np.float32).ravel()); wk.set_float_attr(o, 'corrupt', T['corrupt'].astype(np.float32).ravel())
fz = np.clip(T['fissure'].astype(np.float32).ravel() + T['corrupt'].astype(np.float32).ravel(), 0, 1)[:, None]
dcol = (np.array([.035, .025, .045]) * (1 - fz) + np.array([.6, .04, .04]) * fz)
wk.set_color_attr(o, 'display_col', dcol); o.data.shade_smooth()
o['note'] = 'terrain from MAP_H2 fields (same seeds): ash plains, highlands, glowing fissures, corruption-river channels'
zat = lambda x, y: float(z[int(np.clip(round(((nr - 1) / 2) - y / st), 0, nr - 1)), int(np.clip(round(x / st + (nc - 1) / 2), 0, nc - 1))])
sp_me = wk.cone('DW_SPIRE_MESH', 1.0, 1.0, 5, None, M['MAT_D_OBSIDIAN']).data
wk.display_color(bpy.data.objects.new('tmp', sp_me), '#1A1020')
rng = np.random.default_rng(66)
for i, (x, y, hh) in enumerate(DW['spires']):
    if abs(x) > xs[-1] or abs(y) > ys[0]:
        continue
    s = bpy.data.objects.new(f'DW_SPIRE_{i + 1:03d}', sp_me)
    s.location = (x, y, zat(x, y) - 3); s.scale = (hh * .13, hh * .13, hh)
    s.rotation_euler = (rng.normal(0, .05), rng.normal(0, .05), rng.uniform(0, 6.28)); C['DW_SPIRES'].objects.link(s)
px, py, pr = DW['portal_site']
pz = zat(px, py)
base = wk.cone('DW_PORTAL_SITE_PLINTH', pr, 6, 48, C['DW_CORRUPTED_PORTAL_SITE'], M['MAT_D_PORTAL_SITE'], r_top=pr * .95)
base.location = (px, py, pz - 2); wk.display_color(base, '#2A1E2E')
rim = wk.ring_curve_mesh('DW_PORTAL_SITE_RIM', pr * .8, 0, 96, 3, C['DW_CORRUPTED_PORTAL_SITE'], M['MAT_D_PORTAL_RIM'])
rim.location = (px, py, pz + 4.2); wk.display_color(rim, '#FF2A2A')
base['note'] = 'CORRUPTED PORTAL SITE (MAP_H2 proposal) — place only; the portal VFX = Saithan power (approved look), no rules modelled'
fog = wk.box('DW_FOG_VOLUME', (xs[-1] * 2.2, ys[0] * 2.2, 900), (0, 0, 250), C['DW_ATMOSPHERE'], M['MAT_D_FOG']); fog.display_type = 'BOUNDS'
for nm, x, y in DW['zones']:
    wk.text(f'DW_LBL_{nm.replace(" ", "_")}', nm + ' (proposal)', (x, y, zat(x, y) + 260), 160, C['DW_GUIDES'], M['MAT_D_PORTAL_RIM'],
            rot=(math.radians(60), 0, 0)).hide_render = True
wk.sun('DW_KEY_RED', 14, 200, 2.2, C['DW_LIGHTING'], 3, color=(1.0, .29, .23))
wk.sun('DW_FILL_VIOLET', 40, 20, .5, C['DW_LIGHTING'], 10, color=(.23, .1, .35))
w = bpy.data.worlds.new('DW_SKY'); w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (.03, .008, .02, 1); bg.inputs['Strength'].default_value = 1
sc.world = w
for nm, loc, tgt, lens, desc in (('CAM_D2_DW_OVERVIEW', (3600, -5200, 1900), (-200, 500, 0), 30, 'Overview — ash plains, spire fields, portal site (proposal)'),
                                 ('CAM_D2_DW_SPIRE_FIELD', (-1200, 600, 260), (-2600, 1700, 120), 30, 'Obsidian spire field'),
                                 ('CAM_D2_DW_TOP', (0, 0, 12000), (0, 0, 0), 40, 'Top layout check vs MAP_H2')):
    c = wk.camera(nm, loc, tgt, lens, C['DW_CAMERAS'], clip=(1, 80000)); c['description'] = desc
sc.camera = bpy.data.objects['CAM_D2_DW_OVERVIEW']
wk.setup_cycles(sc, (1280, 720), 24)
wk.save(wk.P('09_DIMENSIONS', 'DIM_saithan_dark_world_v001.blend'))
print('BUILD_DIMS_DONE')

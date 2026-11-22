"""TASK 04 · main-world component files (Blender 4.5). Run:  blender -b -P w4_build_world.py

Reads 01_GEOGRAPHY/data/world_prep.npz (+ world_features.json) and writes one .blend per component:
  01_GEOGRAPHY/WORLD_geography_v001.blend     markers, labels, grid, Ashram-valley + unexplored references
  02_TERRAIN/WORLD_terrain_v001.blend         plains/hills, coasts, ice+tundra, ruined regions, sea bed, underground zones
  03_MOUNTAINS/WORLD_mountains_v001.blend     mountain terrain pieces (+ range lines)
  04_FORESTS/WORLD_forests_v001.blend         forest terrain pieces
  05_RIVERS_AND_LAKES/WORLD_water_v001.blend  ocean, rivers, lakes, lake beds, waterfalls
  06_DESERTS/WORLD_deserts_v001.blend         desert terrain pieces
  07_ISLANDS/WORLD_islands_v001.blend         archipelagos + minor islands
  10_CAMERAS/WORLD_cameras_v001.blend         aerial preview cameras + sun
All terrain pieces are cut from ONE continuous height grid (shared border vertices + global normals) → no gaps, no seams.
Scale: 1 Blender unit = 1 km; heights ×VEXAG (20) for readability — WORLD_ROOT custom props document it.
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk

D = np.load(wk.P('01_GEOGRAPHY', 'data', 'world_prep.npz'))
META = json.load(open(wk.P('01_GEOGRAPHY', 'data', 'world_features.json')))
H, W = META['grid']; KM = META['km_per_cell']; VX = META['vexag']
RK, CK = META['region_keys'], META['class_keys']
REG, CLS = META['regions'], META['classes']
h = D['h']; col = D['col'].astype(np.float32); f_key = D['f_key']
ZS = VX / 1000.0                                                     # metres → display BU
STATUS = 'PROPOSAL — world map v2 revision 01, NOT LOCKED'

# ------------------------------------------------------------------ global grid
cx = (np.arange(W) + .5) * KM - 6000.0
cy = 3000.0 - (np.arange(H) + .5) * KM
GX, GY = np.meshgrid(cx, cy)
GZ = h * ZS
VERTS = np.stack([GX, GY, GZ], -1).reshape(-1, 3)
NORM = wk.heightfield_normals(GZ, KM, KM).reshape(-1, 3)
FACES = wk.grid_faces(H, W).reshape(-1, 4)
FK = f_key.ravel()
ELEV = h.ravel()
COL = col.reshape(-1, 3)
OUTS = {}


def common_props(o, **kw):
    wk.add_props(o, status=STATUS, units='1 BU = 1 km (XY); Z = elevation_km x vexag', vexag=VX, source='02_world/map_v2/data', **kw)


def terrain_piece(key, c):
    sel = FK == key
    v, f, used = wk.subset(VERTS, FACES[sel])
    ri, ci = key // 16, key % 16
    nm = f'TER_{CK[ci]}_{RK[ri]}'
    o = wk.mesh_from_arrays(nm, v, f, c, MATS['MAT_W_TERRAIN'])
    wk.set_color_attr(o, 'biome_col', COL[used]); wk.set_float_attr(o, 'elev_m', ELEV[used])
    wk.smooth_with_normals(o, NORM[used])
    common_props(o, region=RK[ri], region_name=REG[RK[ri]][0], direction=REG[RK[ri]][1], terrain_class=CK[ci],
                 class_name=CLS[CK[ci]][0], faces=int(sel.sum()), area_km2=float(sel.sum() * KM * KM))
    return o


def file_for(ci):
    return CLS[CK[ci]][2]


COMP = {'02_TERRAIN': 'WORLD_terrain_v001', '03_MOUNTAINS': 'WORLD_mountains_v001', '04_FORESTS': 'WORLD_forests_v001',
        '05_RIVERS_AND_LAKES': 'WORLD_water_v001', '06_DESERTS': 'WORLD_deserts_v001', '07_ISLANDS': 'WORLD_islands_v001'}
keys = np.unique(FK[FK >= 0])
inventory = {}

for folder, stem in COMP.items():
    wk.new_file()
    MATS = wk.link_materials()
    sc = bpy.context.scene; sc.name = 'COMPONENT_' + folder
    top = wk.coll(folder)
    for key in keys:
        ri, ci = key // 16, key % 16
        if file_for(ci) != folder:
            continue
        c = wk.coll(f'{CK[ci]}_{RK[ri]}', top)
        o = terrain_piece(key, c)
        inventory[o.name] = {'file': f'{folder}/{stem}.blend', 'collection': c.name, 'verts': len(o.data.vertices), 'faces': len(o.data.polygons)}
    if folder == '02_TERRAIN':
        # ---- sea bed (coarse LOD, stride 4) — sits below the land window so it never z-fights
        S4 = 4
        zz = np.minimum(h[::S4, ::S4], META['shelf_m'] - 50) * ZS
        gx, gy = GX[::S4, ::S4], GY[::S4, ::S4]
        v = np.stack([gx, gy, zz], -1).reshape(-1, 3)
        f = wk.grid_faces(*zz.shape).reshape(-1, 4)
        c = wk.coll('SEABED', top)
        o = wk.mesh_from_arrays('TER_SEABED_WORLD', v, f, c, MATS['MAT_W_TERRAIN'])
        wk.set_color_attr(o, 'biome_col', col[::S4, ::S4].reshape(-1, 3)); o.data.shade_smooth()
        common_props(o, terrain_class='SEABED', lod='stride 4 (31 km)')
        inventory[o.name] = {'file': f'{folder}/{stem}.blend', 'collection': 'SEABED', 'verts': len(v), 'faces': len(f)}
        # ---- underground zones (PROPOSAL): one tunnel volume per cave entrance, descending into the terrain
        c = wk.coll('UNDERGROUND_ZONES', top)
        rng = np.random.default_rng(3)
        for i, (x, y, zm, rk) in enumerate(META['markers']['caves']):
            a = rng.uniform(0, 2 * np.pi); L = 70.0
            t = np.linspace(0, 1, 24)
            path = np.column_stack([x + np.cos(a) * L * t + 6 * np.sin(t * 7), y + np.sin(a) * L * t + 6 * np.cos(t * 5),
                                    zm * ZS - 2 - t * 18])
            cu = bpy.data.curves.new(f'UND_CAVE_ZONE_{i + 1:02d}', 'CURVE'); cu.dimensions = '3D'
            sp = cu.splines.new('POLY'); sp.points.add(len(path) - 1)
            for p, q in zip(sp.points, path):
                p.co = (*q, 1)
            cu.bevel_depth = 3.0; cu.bevel_resolution = 2
            o = bpy.data.objects.new(f'UND_CAVE_ZONE_{i + 1:02d}', cu); c.objects.link(o)
            cu.materials.append(MATS['MAT_W_MARK_UNDERGROUND'])
            o.show_in_front = True; o.display_type = 'WIRE'
            common_props(o, terrain_class='UNDERGROUND', note='PROPOSAL: cave system volume below entrance CV marker (extent NOT confirmed)', region=rk)
    if folder == '03_MOUNTAINS':
        c = wk.coll('RANGE_LINES', top)
        for code, nm, ck, pts, pk, kind in META['ranges']:
            p = np.array(pts, float)
            zz = np.array([GZ[int(np.clip((3000 - y) / KM, 0, H - 1)), int(np.clip((x + 6000) / KM, 0, W - 1))] for x, y in p]) + 15
            o = wk.ribbon(f'RANGE_{code}_{nm.replace(" ", "_")}', np.column_stack([p, zz]), np.full(len(p), 6.0), c, MATS['MAT_W_MARK_RANGE'])
            common_props(o, range_code=code, range_name=nm + ' (proposed name)', continent=ck, kind=kind)
    if folder == '05_RIVERS_AND_LAKES':
        # ---- ocean surface
        S4 = 4
        gx, gy = GX[::S4, ::S4], GY[::S4, ::S4]
        v = np.stack([gx, gy, np.zeros_like(gx)], -1).reshape(-1, 3)
        f = wk.grid_faces(*gx.shape).reshape(-1, 4)
        c = wk.coll('OCEAN', top)
        o = wk.mesh_from_arrays('WAT_OCEAN_WORLD', v, f, c, MATS['MAT_W_OCEAN'])
        oc = D['ocean_col'].astype(np.float32).reshape(-1)
        wk.set_color_attr(o, 'ocean_col', np.column_stack([oc, oc, oc])); o.data.shade_flat()
        wk.display_color(o, '#1E4E78')
        common_props(o, note='sea level = 0 m; colour = depth below (shallow shelf → deep ocean)')
        # ---- rivers (per region)
        rp, ro, rr = D['r_pts'], D['r_off'], D['r_reg']
        by = {}
        for i in range(len(ro) - 1):
            by.setdefault(int(rr[i]), []).append(rp[ro[i]:ro[i + 1]])
        c = wk.coll('RIVERS', top)
        for ri, lst in by.items():
            vs, fs, n0 = [], [], 0
            for seg in lst:
                pts = np.column_stack([seg[:, 0], seg[:, 1], seg[:, 2] * ZS + .6])
                t = np.gradient(pts[:, :2], axis=0); t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
                nr = np.stack([-t[:, 1], t[:, 0]], 1) * (seg[:, 5:6] / 2)
                vv = np.empty((len(pts) * 2, 3)); vv[0::2] = np.column_stack([pts[:, :2] + nr, pts[:, 2]]); vv[1::2] = np.column_stack([pts[:, :2] - nr, pts[:, 2]])
                k = np.arange(len(pts) - 1) * 2 + n0
                fs.append(np.stack([k, k + 1, k + 3, k + 2], 1)); vs.append(vv); n0 += len(vv)
            cc = wk.coll(f'RIVERS_{RK[ri]}', c)
            o = wk.mesh_from_arrays(f'WAT_RIVERS_{RK[ri]}', np.vstack(vs), np.vstack(fs), cc, MATS['MAT_W_RIVER'])
            wk.display_color(o, '#3D86B8')
            common_props(o, region=RK[ri], rivers=len(lst), note='display width 2.5–8 km (true width ≈ 0.5·√drainage km² m, see WORLD_SCALE.md); follows the filled surface → never uphill')
            inventory[o.name] = {'file': f'{folder}/{stem}.blend', 'collection': cc.name, 'verts': n0, 'rivers': len(lst)}
        # ---- lakes: flat surfaces at spill level
        lab = D['lake_lab']; lv = D['lake_level']; lreg = D['lake_reg']
        lab_c = np.stack([lab[:-1, :-1], lab[:-1, 1:], lab[1:, :-1], lab[1:, 1:]]).max(0)
        c = wk.coll('LAKES', top)
        for ri in sorted(set(int(x) for x in lreg[1:])):
            ids = [i for i in range(1, len(lv)) if lreg[i] == ri]
            vs, fs, n0 = [], [], 0
            for i in ids:
                rr_, cc_ = np.nonzero(lab_c == i)
                quad = np.stack([(rr_ + 1) * W + cc_, (rr_ + 1) * W + cc_ + 1, rr_ * W + cc_ + 1, rr_ * W + cc_], 1)
                v, f, used = wk.subset(VERTS, quad)
                v = v.copy(); v[:, 2] = lv[i] * ZS + .25
                vs.append(v); fs.append(f + n0); n0 += len(v)
            cc = wk.coll(f'LAKES_{RK[ri]}', c)
            o = wk.mesh_from_arrays(f'WAT_LAKES_{RK[ri]}', np.vstack(vs), np.vstack(fs), cc, MATS['MAT_W_LAKE'])
            wk.display_color(o, '#2D6E8A')
            common_props(o, region=RK[ri], lakes=len(ids), note='flat water at each lake spill level (from the filled surface)')
            inventory[o.name] = {'file': f'{folder}/{stem}.blend', 'collection': cc.name, 'lakes': len(ids)}
        # ---- waterfalls (proposed sites from the map): instanced vertical sheets
        c = wk.coll('WATERFALLS', top)
        me = wk.box('WFL_SHEET_MESH', (6, 1.2, 14), coll_=None, mat=MATS['MAT_W_WATERFALL']).data
        tmp = bpy.data.objects.new('tmp', me); wk.display_color(tmp, '#DDF2FF'); bpy.data.objects.remove(tmp)
        for i, (x, y, zm, rk) in enumerate(META['markers']['waterfalls']):
            o = bpy.data.objects.new(f'WAT_WATERFALL_{i + 1:02d}', me); o.location = (x, y, zm * ZS + 4); c.objects.link(o)
            common_props(o, region=rk, note='waterfall site PROPOSED (2D map); detailed geometry at region stage')
    wk.save(wk.P(folder, f'{stem}.blend'))

# ================================================================== 01 GEOGRAPHY markers / references
wk.new_file()
MATS = wk.link_materials()
bpy.context.scene.name = 'COMPONENT_01_GEOGRAPHY'
top = wk.coll('01_GEOGRAPHY')
zat = lambda x, y: float(GZ[int(np.clip((3000 - y) / KM, 0, H - 1)), int(np.clip((x + 6000) / KM, 0, W - 1))])
proto = {
    'cities': wk.box('MK_CITY_MESH', (16, 16, 12), mat=MATS['MAT_W_MARK_CITY']).data,
    'towns': wk.cone('MK_TOWN_MESH', 7, 14, 6, mat=MATS['MAT_W_MARK_TOWN']).data,
    'villages': wk.cone('MK_VILLAGE_MESH', 4, 8, 6, mat=MATS['MAT_W_MARK_VILLAGE']).data,
    'remote': wk.cone('MK_REMOTE_MESH', 4, 10, 3, mat=MATS['MAT_W_MARK_REMOTE']).data,
    'ruins': wk.box('MK_RUIN_MESH', (4, 4, 16), mat=MATS['MAT_W_MARK_RUIN']).data,
    'caves': wk.cone('MK_CAVE_MESH', 7, 10, 3, mat=MATS['MAT_W_MARK_CAVE']).data,
    'c1_hidden': wk.cone('MK_HIDDEN_MESH', 8, 18, 4, mat=MATS['MAT_W_MARK_HIDDEN']).data,
}
MKCOL = {'cities': '#FF8C3A', 'towns': '#F2C27A', 'villages': '#FFF1D0', 'remote': '#D9D2C0', 'ruins': '#C49A72', 'caves': '#9A6BFF', 'c1_hidden': '#FF3AD0'}
for k_, m_ in proto.items():
    tmp = bpy.data.objects.new('tmp', m_); wk.display_color(tmp, MKCOL[k_]); bpy.data.objects.remove(tmp)
labels = wk.coll('GEO_LABELS', top)
for key, cname in (('cities', 'GEO_SETTLEMENTS'), ('towns', 'GEO_SETTLEMENTS'), ('villages', 'GEO_SETTLEMENTS'), ('remote', 'GEO_SETTLEMENTS'),
                   ('ruins', 'GEO_RUINS'), ('caves', 'GEO_CAVE_ENTRANCES'), ('c1_hidden', 'GEO_HIDDEN_AND_GEM')):
    c = wk.coll(cname, top)
    for i, (x, y, zm, rk) in enumerate(META['markers'][key]):
        o = bpy.data.objects.new(f'MK_{key.upper()}_{i + 1:03d}', proto[key])            # linked duplicates = instancing
        o.location = (x, y, zat(x, y) + 2); c.objects.link(o)
        common_props(o, marker=key, region=rk, note='PROPOSED site (code only — no names, people or politics invented)')
# Ashram + GEM
c = wk.coll('GEO_ASHRAM', top)
ax, ay, azm, _ = META['markers']['ashram'][0]
o = wk.cone('MK_ASHRAM', 10, 40, 5, c, MATS['MAT_W_MARK_ASHRAM'], z0=0); o.location = (ax, ay, zat(ax, ay)); wk.display_color(o, '#FFD45A')
common_props(o, marker='ASHRAM', note='Ashram = CONFIRMED story location; this position = PROPOSAL (rev 01); detailed terrain = 08_ASHRAM_VALLEY',
             world_km=[ax + 6000, ay + 3000])
for nm, half, w in (('LOD1_60KM', 30, 1.2), ('LOD2_320KM', 160, 3.0)):
    r = wk.rect_curve_mesh(f'REF_ASHRAM_VALLEY_{nm}', ax - half, ax + half, ay - half, ay + half, zat(ax, ay) + 40, w, c, MATS['MAT_W_MARK_ASHRAM'])
    common_props(r, note=f'extent of the detailed Ashram Valley terrain ({nm})')
t = wk.text('LBL_ASHRAM', 'ASHRAM VALLEY\n(proposed position)', (ax, ay + 60, zat(ax, ay) + 60), 28, labels, MATS['MAT_W_MARK_ASHRAM'])
c = wk.coll('GEO_HIDDEN_AND_GEM', top)
gx_, gy_, gzm, grk = META['markers']['gem'][0]
o = wk.cone('MK_GEM_PROPOSAL', 9, 30, 6, c, MATS['MAT_W_MARK_GEM']); o.location = (gx_, gy_, zat(gx_, gy_)); wk.display_color(o, '#5AFFC8')
common_props(o, marker='GEM', note='GEM location NOT CONFIRMED — proposal (MAP_J): hidden ancient region in Veylora. No 3D environment built until confirmed.')
r = wk.ring_curve_mesh('REF_GEM_HIDDEN_REGION', 90, zat(gx_, gy_) + 30, 64, 2.5, c, MATS['MAT_W_MARK_GEM'], center=(gx_, gy_))
wk.text('LBL_GEM', 'GEM hidden region\nPROPOSAL — not confirmed', (gx_, gy_ + 110, zat(gx_, gy_) + 60), 26, labels, MATS['MAT_W_MARK_GEM'])
# continent / ocean / range labels
import importlib.util
CONT = [('C1', 'AETHERIA', (.30, .36)), ('C2', 'SOLMARA', (.62, .58)), ('C3', 'VEYLORA', (.86, .30)), ('C4', 'NOXARA', (.58, .075)), ('C5', 'DRAKMOR', (.20, .80))]
for k, nm, (nx, ny) in CONT:
    x, y = nx * 12000 - 6000, 3000 - ny * 6000
    wk.text(f'LBL_{k}_{nm}', f'{nm}\n{k} · proposed name', (x, y, 170), 110, labels, MATS['MAT_W_MARK_LABEL'])
for nm, (nx, ny) in (('WESTERN OCEAN', (.06, .3)), ('NORTHERN OCEAN', (.48, .2)), ('CENTRAL SEA', (.42, .7)), ('EASTERN OCEAN', (.93, .75))):
    wk.text(f'LBL_OCEAN_{nm.replace(" ", "_")}', nm + ' (proposed)', (nx * 12000 - 6000, 3000 - ny * 6000, 20), 70, labels, MATS['MAT_W_MARK_LABEL'])
for code, nm, ck, pts, pk, kind in META['ranges']:
    x, y = pts[len(pts) // 2]
    wk.text(f'LBL_RANGE_{code}', nm.title() + ' (proposed)', (x, y + 60, zat(x, y) + 80), 45, labels, MATS['MAT_W_MARK_RANGE'])
# unexplored edges + coordinate grid
c = wk.coll('GEO_UNEXPLORED_EDGES', top)
for side, x in (('WEST', -5800), ('EAST', 5800)):
    r = wk.rect_curve_mesh(f'REF_UNEXPLORED_{side}', x - 200 if side == 'WEST' else x, x if side == 'WEST' else x + 200, -3000, 3000, 30, 8, c, MATS['MAT_W_MARK_UNEXPLORED'])
    common_props(r, note='edge of the known world (atlas hatch) — unexplored, NOT modelled')
wk.text('LBL_UNEXPLORED_N', 'UNEXPLORED — Noxara interior / Ice Wall', (960, 2750, 260), 60, labels, MATS['MAT_W_MARK_UNEXPLORED'])
g = wk.coll('GEO_GRID_1000KM', top)
for i, x in enumerate(range(-6000, 6001, 1000)):
    r = wk.ribbon(f'GRID_X_{i:02d}', np.array([[x, -3000, 3], [x, 3000, 3]], float), np.array([3.0, 3.0]), g, MATS['MAT_W_MARK_LABEL'])
for i, y in enumerate(range(-3000, 3001, 1000)):
    r = wk.ribbon(f'GRID_Y_{i:02d}', np.array([[-6000, y, 3], [6000, y, 3]], float), np.array([3.0, 3.0]), g, MATS['MAT_W_MARK_LABEL'])
wk.save(wk.P('01_GEOGRAPHY', 'WORLD_geography_v001.blend'))

# ================================================================== 10 CAMERAS + light
wk.new_file()
bpy.context.scene.name = 'COMPONENT_10_CAMERAS'
cams = wk.coll('WORLD_CAMERAS'); light = wk.coll('WORLD_LIGHTING')
XY = lambda nx, ny: (nx * 12000 - 6000, 3000 - ny * 6000)
CAMS = [
    ('CAM_W00_TOP_ORTHO', (0, 0, 6000), (0, 0, 0), 50, 12500, 'Technical top view of the whole main world (orthographic)'),
    ('CAM_W01_ENTIRE_WORLD', (0, -9600, 7400), (0, 250, 0), 30, None, 'Entire main world — cinematic aerial'),
]
for k, nm, (nx, ny), dist, lens in (('C1', 'AETHERIA', (.30, .36), 3200, 32), ('C2', 'SOLMARA', (.62, .58), 3600, 32), ('C3', 'VEYLORA', (.86, .30), 2700, 32),
                                    ('C4', 'NOXARA', (.58, .075), 3600, 30), ('C5', 'DRAKMOR', (.20, .80), 2200, 32)):
    x, y = XY(nx, ny)
    CAMS.append((f'CAM_W02_REGION_{k}_{nm}', (x - dist * .25, y - dist * .95, dist * .62), (x, y + 40, 0), lens, None, f'Region — {k} {nm} (proposed name)'))
m1 = META['ranges'][0][3]; mx, my = m1[2]
CAMS += [
    ('CAM_W03_MOUNTAINS_MAHAGIRI', (mx - 520, my - 640, 190), (mx + 80, my + 60, 40), 30, None, 'Mountain range — Mahagiri (C1, proposed name), low aerial'),
    ('CAM_W03_MOUNTAINS_SUNSTONE', (*XY(.53, .70), 300), (*XY(.61, .55), 40), 30, None, 'Mountain range — Sunstone Ridge (C2)'),
    ('CAM_W04_FORESTS_VEYLORA', (*XY(.80, .45), 520), (*XY(.87, .30), 0), 30, None, 'Forest zones — Veylora wet / enchanted forests'),
    ('CAM_W04_FORESTS_AETHERIA', (*XY(.34, .52), 420), (*XY(.33, .40), 0), 30, None, 'Forest zones — Aetheria enchanted forest + lake district'),
    ('CAM_W05_RIVERS_SOLMARA', (*XY(.70, .72), 520), (*XY(.66, .55), 0), 30, None, 'River systems — Solmara east'),
    ('CAM_W05_RIVERS_AETHERIA', (*XY(.36, .30), 380), (*XY(.29, .37), 0), 30, None, 'River systems — Aetheria lake district'),
    ('CAM_W06_DESERT_SOLMARA', (*XY(.50, .70), 420), (*XY(.57, .62), 0), 32, None, 'Desert — Solmara interior'),
    ('CAM_W06_DESERT_AETHERIA_WEST', (*XY(.24, .56), 300), (*XY(.21, .46), 0), 32, None, 'Desert + wasteland — Aetheria west (R-04, proposal)'),
    ('CAM_W07_ISLANDS_SAGARA', (*XY(.44, .55), 520), (*XY(.47, .44), 0), 30, None, 'Islands — Sagara archipelago (A1)'),
    ('CAM_W08_ASHRAM_VALLEY_REGION', (ax - 60, ay - 330, 150), (ax, ay + 40, zat(ax, ay)), 30, None, 'Ashram Valley — position in the main world (world scale)'),
]
camdoc = []
for nm, loc, tgt, lens, ortho, desc in CAMS:
    o = wk.camera(nm, loc, tgt, lens, cams, clip=(1, 60000), ortho=ortho)
    o['description'] = desc; camdoc.append({'name': nm, 'desc': desc, 'loc': list(map(float, loc)), 'target': list(map(float, tgt))})
s = wk.sun('SUN_WORLD_KEY', 32, 135, 3.2, light, 1.0)
s['note'] = 'key sun from the south-east, 32° elevation'
wk.save(wk.P('10_CAMERAS', 'WORLD_cameras_v001.blend'))
json.dump({'cameras': camdoc, 'inventory': inventory}, open(wk.P('10_CAMERAS', 'cameras_and_inventory.json'), 'w'), indent=1)
print('objects', len(inventory))
print('BUILD_WORLD_DONE')

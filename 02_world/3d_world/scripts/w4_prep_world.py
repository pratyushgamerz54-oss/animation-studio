"""TASK 04 · STEP 1 — main-world data prep (system python3 + numpy + scipy, NOT Blender).

Reads the PROPOSED world map v2 data (02_world/map_v2/data, revision 01 — NOT LOCKED) and writes everything the
Blender 4.5 build scripts need into 01_GEOGRAPHY/data/ (numpy-only inputs, so the Director can rebuild the 3D files
on a PC with plain Blender 4.5 — Blender ships numpy, not scipy):

  world_prep.npz       height grid (m), display colour, per-face region/class keys, rivers, lakes, ocean shading
  world_features.json  key tables, markers (settlements, ruins, caves, waterfalls, hidden/GEM/Ashram), scale constants

Nothing new is invented here: every height, coastline, river, lake, biome and marker comes from the map data.
"""
import os, sys, json, math
import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))                      # 02_world/3d_world
W2 = os.path.abspath(os.path.join(ROOT, '..', '_shared'))
sys.path.insert(0, W2)
import worldgen2 as wg2                                              # same constants as the 2D atlas (no re-generation)

DATA = os.path.join(ROOT, '..', 'map_v2', 'data')
OUT = os.path.join(ROOT, '01_GEOGRAPHY', 'data'); os.makedirs(OUT, exist_ok=True)

H, W = 768, 1536
KM = 12000 / W                     # 7.8125 km per map cell
VEXAG = 20.0                       # vertical exaggeration of the master-world display mesh (documented in WORLD_SCALE.md)

h = np.load(os.path.join(DATA, 'height_m.npy')).astype(np.float32)
Fh = np.load(os.path.join(DATA, 'filled_m.npy')).astype(np.float32)
acc = np.load(os.path.join(DATA, 'accum.npy')).astype(np.float32)
B = np.load(os.path.join(DATA, 'biome.npy')).astype(np.int16)
cid = np.load(os.path.join(DATA, 'continent_id.npy')).astype(np.int16)
lakes = np.load(os.path.join(DATA, 'lakes.npy')).astype(bool)
fe = json.load(open(os.path.join(DATA, 'features.json')))
sea = h <= 0
land = ~sea
ny = (np.mgrid[0:H, 0:W][0] + .5) / H

# ------------------------------------------------------------------ coordinates
def cell_xy(c, r):
    """map cell (col, row; row 0 = north) -> master-world Blender XY (km). Origin = map centre, +X east, +Y north."""
    return (np.asarray(c, float) + .5) * KM - 6000.0, 3000.0 - (np.asarray(r, float) + .5) * KM

# ------------------------------------------------------------------ regions (all names = PROPOSED, revision 01)
REGIONS = {  # key: (display name, direction collection)
    'C1': ('C1 AETHERIA (home continent)', 'WESTERN'), 'C2': ('C2 SOLMARA', 'SOUTHERN'), 'C3': ('C3 VEYLORA', 'EASTERN'),
    'C4': ('C4 NOXARA', 'NORTHERN'), 'C4U': ('C4 NOXARA — unexplored north', 'NORTHERN'), 'C5': ('C5 DRAKMOR', 'SOUTHERN'),
    'A1': ('A1 SAGARA ARCHIPELAGO', 'WESTERN'), 'A2': ('A2 AGNI ISLAND ARC', 'EASTERN'), 'A3': ('A3 WESTERN ISLES', 'WESTERN'),
    'IW': ('Minor islands — west', 'WESTERN'), 'IE': ('Minor islands — east', 'EASTERN'),
    'IN': ('Minor islands — north', 'NORTHERN'), 'IS': ('Minor islands — south', 'SOUTHERN'),
}
RK = list(REGIONS)
reg = np.full((H, W), -1, np.int16)
for k in (1, 2, 3, 4, 5):
    reg[cid == k] = RK.index(f'C{k}')
reg[(cid == 4) & (ny < .09)] = RK.index('C4U')                       # same mask as the atlas 'unexplored' hatch
# islands = every land mass that is not the main body of a continent (connected components on land)
yy, xx = np.mgrid[0:H, 0:W]
nxv, nyv = (xx + .5) / W, (yy + .5) / H
comp, ncomp = ndi.label(land)
mainland = set()
for k in (1, 2, 3, 4, 5):
    ids, n = np.unique(comp[(cid == k) & land], return_counts=True)
    mainland.add(int(ids[np.argmax(n)]))
isl = land & ~np.isin(comp, list(mainland))
best = np.full((H, W), 9e9)
DIRK = {'WESTERN': 'IW', 'EASTERN': 'IE', 'NORTHERN': 'IN', 'SOUTHERN': 'IS'}
# minor islands → direction of the nearest continent mainland
near = ndi.distance_transform_edt(~np.isin(comp, list(mainland)), return_distances=False, return_indices=True)
ncid = cid[near[0], near[1]]
reg_isl = np.full((H, W), -1, np.int16)
for k in (1, 2, 3, 4, 5):
    reg_isl[ncid == k] = RK.index(DIRK[REGIONS[f'C{k}'][1]])
for key, nm, (cx, cy), (sx, sy), n, sz in wg2.ISLANDS:
    d = np.hypot((nxv - cx) / (sx * 1.8), (nyv - cy) / (sy * 1.8))
    m = (d < 1.0) & (d < best)
    reg_isl[m] = RK.index(key); best = np.where(m, d, best)
reg[isl] = reg_isl[isl]
# shelf around islands: sea cells nearest to an island get the island key (so the shelf faces join the island object)
# ------------------------------------------------------------------ terrain classes
CLASSES = {  # key: (name, thematic collection, component file)
    'MTN': ('Mountains (high rock / snow / > 2 200 m)', 'MOUNTAIN_REGIONS', '03_MOUNTAINS'),
    'FOR': ('Forests (temperate / enchanted / rainforest / taiga)', 'FOREST_REGIONS', '04_FORESTS'),
    'DES': ('Deserts', 'DESERT_REGIONS', '06_DESERTS'),
    'PLN': ('Plains, grassland, savanna, wetland, hills', 'PLAINS_AND_HILLS', '02_TERRAIN'),
    'COA': ('Coasts, beaches, continental shelf', 'COASTAL_AREAS', '02_TERRAIN'),
    'ICE': ('Ice sheet + tundra', 'ICE_AND_TUNDRA', '02_TERRAIN'),
    'RUI': ('Wasteland + forbidden zone (ruined-region terrain, proposal)', 'RUINED_REGIONS', '02_TERRAIN'),
    'LKB': ('Lake beds', 'WATER_SYSTEMS', '05_RIVERS_AND_LAKES'),
    'ISL': ('Islands (all terrain types)', 'ISLANDS', '07_ISLANDS'),
}
CK = list(CLASSES)
cls = np.full((H, W), CK.index('PLN'), np.int16)
cls[np.isin(B, [3, 4, 7, 8])] = CK.index('FOR')
cls[B == 5] = CK.index('DES')
cls[np.isin(B, [9, 10])] = CK.index('ICE')
cls[np.isin(B, [15, 16])] = CK.index('RUI')
cls[(B == 1) | sea] = CK.index('COA')
cls[np.isin(B, [11, 12]) | (h >= 2200)] = CK.index('MTN')
cls[lakes] = CK.index('LKB')
cls[np.isin(reg, [RK.index(k) for k in ('A1', 'A2', 'A3', 'IW', 'IE', 'IN', 'IS')])] = CK.index('ISL')

# ------------------------------------------------------------------ land window (faces) — continuous coast + shelf
SHELF = -300.0
hc = np.stack([h[:-1, :-1], h[:-1, 1:], h[1:, :-1], h[1:, 1:]])
face_in = hc.max(0) > SHELF                                          # face between 4 cell centres
# owner cell of a face = its highest corner → coastal faces belong to the land they touch
corner = np.argmax(hc, 0)
rr = np.arange(H - 1)[:, None] + (corner >= 2)
cc = np.arange(W - 1)[None, :] + (corner % 2)
f_reg = reg[rr, cc]; f_cls = cls[rr, cc]
# shelf faces whose owner cell is sea → class COA of nearest land region (owner cell is the highest corner = coast-side)
f_reg = np.where(face_in, f_reg, -1)
# faces with region -1 (ocean cell with no continent mask) inside the window → nearest land region
miss = face_in & (f_reg < 0)
if miss.any():
    idx = ndi.distance_transform_edt(f_reg < 0, return_distances=False, return_indices=True)
    f_reg = np.where(miss, f_reg[idx[0], idx[1]], f_reg)
ISLK = [RK.index(k) for k in ('A1', 'A2', 'A3', 'IW', 'IE', 'IN', 'IS')]
f_cls = np.where(np.isin(f_reg, ISLK), CK.index('ISL'), f_cls)
f_key = np.where(face_in, f_reg * 16 + f_cls, -1).astype(np.int32)  # one mesh object per (region, class)

# ------------------------------------------------------------------ display colour (natural palette, not the atlas palette)
NAT = {0: '#2A3A48', 1: '#CDBF98', 2: '#7F9A4F', 3: '#33602E', 4: '#235E54', 5: '#D3B27A', 6: '#A99B57', 7: '#1D4F28',
       8: '#2C4D37', 9: '#8D8D79', 10: '#E9EEF2', 11: '#7A736C', 12: '#F3F6F9', 13: '#506F53', 14: '#6F6752',
       15: '#7B6B5A', 16: '#433246'}
hx = lambda s: np.array([int(s[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
col = np.zeros((H, W, 3), np.float32)
for b, s in NAT.items():
    col[B == b] = hx(s)
col[sea] = hx('#6D6A5C') * np.clip(1 + h[sea] / 4000, .35, 1)[:, None]  # sea bed: darker with depth
col = np.stack([ndi.gaussian_filter(col[..., i], .8) for i in range(3)], -1)
snow = np.clip((h - 4300) / 900, 0, 1) * (B != 5)                      # high snow caps on any very high cell
col = col * (1 - snow[..., None]) + hx('#F3F6F9') * snow[..., None]

# ------------------------------------------------------------------ rivers (same rule as the atlas: land & acc>120 & not lake)
down, acc2 = wg2.flow(Fh, sea)
riv = land & (acc > 120) & ~lakes
rv = riv.ravel()
up_has = np.zeros(H * W, bool)
for i in np.nonzero(rv)[0]:
    j = down[i]
    if j >= 0 and rv[j]:
        up_has[j] = True
heads = [i for i in np.nonzero(rv)[0] if not up_has[i]]
seen = np.zeros(H * W, bool); rivers = []
for hd in sorted(heads, key=lambda i: -Fh.ravel()[i]):
    pts = []; i = hd
    while True:
        pts.append(i)
        if seen[i]:
            break
        seen[i] = True
        j = down[i]
        if j < 0 or j == i:
            break
        if not rv[j]:
            pts.append(j); break                                     # mouth: sea or lake cell
        i = j
    if len(pts) >= 3:
        rivers.append(pts)
r_pts, r_off = [], [0]
Fr, accr, hr = Fh.ravel(), acc.ravel(), h.ravel()
for p in rivers:
    rr_, cc_ = np.divmod(np.array(p), W)
    x, y = cell_xy(cc_, rr_)
    z = np.maximum(Fr[p], 0)                                         # filled surface: monotone, never uphill
    z = np.minimum.accumulate(z)
    a = accr[p]
    width_true_m = .5 * np.sqrt(a * KM * KM)                         # ≈ 0.5·√(drainage km²) metres (estimate)
    width_disp_km = 2.5 + 3.0 * np.log10(np.maximum(a, 120) / 120)  # display width (exaggerated, documented)
    r_pts.append(np.stack([x, y, z, a, width_true_m, width_disp_km], 1)); r_off.append(r_off[-1] + len(p))
r_pts = np.concatenate(r_pts).astype(np.float32)
r_reg = reg.ravel()[[p[0] for p in rivers]]

# ------------------------------------------------------------------ lakes: one flat surface per lake component at spill level
lab, nl = ndi.label(lakes)
lake_level = np.zeros(nl + 1, np.float32)
for i in range(1, nl + 1):
    m = lab == i
    lake_level[i] = float(Fh[m].max())
lake_reg = np.array([reg[lab == i][0] if i else -1 for i in range(nl + 1)], np.int16)

# ------------------------------------------------------------------ ocean shading (shallow → deep), coarse grid
S4 = 4
hs = h[::S4, ::S4]
ocean_col = np.clip(-hs / 3500, 0, 1)                                 # 0 shallow … 1 deep

# ------------------------------------------------------------------ markers
def mk(lst):
    out = []
    for p in lst:
        c, r = float(p[0]), float(p[1])
        ci, ri = min(W - 1, int(c)), min(H - 1, int(r))
        x, y = cell_xy(c - .5, r - .5)
        out.append([round(float(x), 2), round(float(y), 2), round(float(max(h[ri, ci], 0)), 1), RK[reg[ri, ci]] if reg[ri, ci] >= 0 else 'SEA'])
    return out
markers = {k: mk(fe[k]) for k in ('cities', 'towns', 'villages', 'remote', 'ruins', 'caves', 'waterfalls', 'c1_hidden')}
markers['ashram'] = mk([fe['ashram']])
markers['gem'] = mk([fe['gem']])
regions_c1 = [[c, n, mk([p])[0] if p else None, st] for c, n, p, st in fe['c1_regions']]

meta = {
    'status': 'PROPOSAL — built from world map v2 revision 01 (NOT LOCKED, awaiting Director approval)',
    'grid': [H, W], 'km_per_cell': KM, 'vexag': VEXAG, 'shelf_m': SHELF,
    'world_km': [12000, 6000], 'origin': 'map centre; +X east, +Y north; master-world 1 Blender unit = 1 km',
    'regions': {k: v for k, v in REGIONS.items()}, 'region_keys': RK,
    'classes': {k: v for k, v in CLASSES.items()}, 'class_keys': CK,
    'continents': fe['continents'], 'audit_2d': fe['audit'], 'markers': markers, 'c1_regions': regions_c1,
    'ranges': [[c, n, k, [list(cell_xy(px * W - .5, py * H - .5)) for px, py in pts], pk, kind] for c, n, k, pts, w_, pk, kind in wg2.RANGES],
    'n_rivers': len(rivers), 'n_lakes': int(nl),
    'elev_m': [float(h.min()), float(h.max())],
}
np.savez_compressed(os.path.join(OUT, 'world_prep.npz'), h=h, col=col.astype(np.float16), f_key=f_key, reg=reg, cls=cls,
                    r_pts=r_pts, r_off=np.array(r_off, np.int32), r_reg=r_reg.astype(np.int16), lake_lab=lab.astype(np.int16),
                    lake_level=lake_level, lake_reg=lake_reg, ocean_col=ocean_col.astype(np.float16), lakes=lakes)
json.dump(meta, open(os.path.join(OUT, 'world_features.json'), 'w'), indent=1)
keys, cnt = np.unique(f_key[f_key >= 0], return_counts=True)
print('faces in land window', int(face_in.sum()), 'objects', len(keys), 'rivers', len(rivers), 'river pts', len(r_pts), 'lakes', nl)
for k, n in zip(keys, cnt):
    print(f'  {RK[k // 16]:4s} {CK[k % 16]}  {n}')
print('PREP_WORLD_DONE')

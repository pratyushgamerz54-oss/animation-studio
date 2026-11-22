"""TASK 04 · STEP 2 — Ashram Valley terrain prep (system python3 + numpy + scipy, NOT Blender).

Source = the DETAILED Aetheria data (02_world/map/data, 3 km cells — the same data behind MAP_G and the world atlas C1).
Local frame (metres): origin = proposed Ashram position, +X east, +Y north, Z = elevation above sea level (m).

Three nested LOD grids (shared edges at the hole borders, skirts hide cracks):
  LOD0  ±3 km    @ 12.5 m   valley floor around the Ashram (close / ground shots)
  LOD1  ±30 km   @ 100 m    valley + forest ring + rivers (aerial shots)
  LOD2  ±160 km  @ 1 000 m  far terrain incl. the snowy range ≈100 km NW (horizon)

Height = bicubic map heights (approved shapes, NOT changed) + procedural detail (fbm / ridged noise, zero-mean on the
valley floor) → rivers carved from the map's own flow network (always downhill) → Ashram pad flattened.
Biome masks come from the same map biomes (domain-warped so 3 km cells don't show as squares).
Writes 08_ASHRAM_VALLEY/data/valley_prep.npz + valley_features.json.
"""
import os, sys, json, math
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, '..', '_shared')))
import worldgen as wg

OLD = os.path.join(ROOT, '..', 'map', 'data')
OUT = os.path.join(ROOT, '08_ASHRAM_VALLEY', 'data'); os.makedirs(OUT, exist_ok=True)
CELL = 3000.0
oh = np.load(os.path.join(OLD, 'height_m.npy')).astype(np.float64)
oF = np.load(os.path.join(OLD, 'filled_m.npy')).astype(np.float64)
oacc = np.load(os.path.join(OLD, 'accum.npy')); ob = np.load(os.path.join(OLD, 'biome.npy')); ol = np.load(os.path.join(OLD, 'lakes.npy'))
OF = json.load(open(os.path.join(OLD, 'features.json')))
AX, AY = OF['ashram']                                            # (col, row) in the C1 grid — PROPOSED position
OH, OW = oh.shape
osea = oh <= 0

def to_cell(x, y):
    return AX + x / CELL, AY - y / CELL                          # col, row (row 0 = north)

def to_local(c, r):
    return (np.asarray(c) - AX) * CELL, (AY - np.asarray(r)) * CELL

# ------------------------------------------------------------------ point-evaluable value noise (deterministic)
_perm = np.random.default_rng(4).permutation(4096)

def _hash(ix, iy, s):
    return (_perm[(_perm[(ix + s * 131) & 4095] + iy) & 4095] / 4095.0) * 2 - 1

def vnoise(x, y, s=0):
    ix, iy = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - ix, y - iy
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _hash(ix, iy, s), _hash(ix + 1, iy, s)
    c, d = _hash(ix, iy + 1, s), _hash(ix + 1, iy + 1, s)
    return (a + (b - a) * ux) * (1 - uy) + (c + (d - c) * ux) * uy

def fbm(x, y, scale, oct, s, gain=.5):
    v = np.zeros_like(x); amp = 1.0; f = 1.0 / scale; tot = 0
    for o in range(oct):
        v += amp * vnoise(x * f + 17.3 * o, y * f - 9.1 * o, s + o); tot += amp
        amp *= gain; f *= 2.03
    return v / tot

def ridged(x, y, scale, oct, s):
    v = np.zeros_like(x); amp = 1.0; f = 1.0 / scale; tot = 0; w = 1.0
    for o in range(oct):
        n = 1 - np.abs(vnoise(x * f + 5.7 * o, y * f + 3.3 * o, s + 50 + o))
        n = n * n * w; w = np.clip(n * 1.5, 0, 1)
        v += amp * n; tot += amp; amp *= .5; f *= 2.1
    return v / tot - .32                                         # ≈ zero-mean

def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def base_h(x, y):
    c, r = to_cell(x, y)
    return ndi.map_coordinates(oh, [r, c], order=3, mode='nearest')

def height(x, y):
    """Uncarved terrain height (m) at local metres."""
    hb = base_h(x, y)
    # warp sample positions slightly so the bicubic 3 km lattice never shows
    rad = np.hypot(x, y)
    m = sstep(1300, 3200, hb)                                    # mountain factor
    hill = sstep(800, 1600, hb)
    valley = np.exp(-(rad / 9000.0) ** 2)                        # big green valley floor around the Ashram stays gentle
    d = (fbm(x, y, 14000, 4, 1) * 120 * (.45 + hill)              # broad undulation (rolling valley floor)
         + ridged(x, y, 5200, 5, 2) * 1500 * m ** 1.3             # ridges / arêtes in the ranges
         + ridged(x, y, 1600, 3, 3) * 260 * m                     # spurs
         + fbm(x, y, 2600, 4, 4) * 60 * (.4 + hill)               # hills / foothills
         + fbm(x, y, 420, 3, 5) * 9 + fbm(x, y, 90, 2, 6) * 1.6)  # small ground relief
    return hb + d * (1 - .45 * valley)

# ------------------------------------------------------------------ rivers from the map's flow network
odown, _ = wg.flow(oF, osea)
R2 = 160000.0
c0, c1 = int(AX - R2 / CELL) - 2, int(AX + R2 / CELL) + 3
r0, r1 = int(AY - R2 / CELL) - 2, int(AY + R2 / CELL) + 3
win = np.zeros_like(osea); win[max(r0, 0):r1, max(c0, 0):c1] = True
oriv = (~osea) & (oacc > 40) & ~ol & win                         # same threshold as MAP_G (rivers drawn there)
rv = oriv.ravel(); up_has = np.zeros(rv.size, bool)
for i in np.nonzero(rv)[0]:
    j = odown[i]
    if j >= 0 and rv[j]:
        up_has[j] = True
seen = np.zeros(rv.size, bool); chains = []
for hd in sorted([i for i in np.nonzero(rv)[0] if not up_has[i]], key=lambda i: -oF.ravel()[i]):
    p = []; i = hd
    while True:
        p.append(i)
        if seen[i]:
            break
        seen[i] = True
        j = odown[i]
        if j < 0 or j == i:
            break
        if not rv[j]:
            p.append(j); break
        i = j
    if len(p) >= 2:
        chains.append(p)

def chaikin(P, n=3):
    for _ in range(n):
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            Q += [.75 * a + .25 * b, .25 * a + .75 * b]
        Q.append(P[-1]); P = np.array(Q)
    return P

rivers = []
acc_tree = None; acc_pts = []
order = sorted(range(len(chains)), key=lambda k: -len(chains[k]))
for k in order:
    p = chains[k]
    rr_, cc_ = np.divmod(np.array(p), OW)
    x, y = to_local(cc_, rr_)
    P0 = chaikin(np.stack([x, y], 1), 3)
    seg = np.hypot(*np.diff(P0, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < 200:
        continue
    ss = np.arange(0, s[-1], 25.0)
    P0 = np.stack([np.interp(ss, s, P0[:, 0]), np.interp(ss, s, P0[:, 1])], 1)
    t = np.gradient(P0, axis=0); t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    t = np.stack([ndi.gaussian_filter1d(t[:, 0], 40), ndi.gaussian_filter1d(t[:, 1], 40)], 1)
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    nrm = np.stack([-t[:, 1], t[:, 0]], 1)
    env = np.clip(ss / 4000, 0, 1) * np.clip((ss[-1] - ss) / 4000, 0, 1)     # ends fixed → confluences/mouths stay joined
    off0 = (fbm(ss, np.full_like(ss, k * 7.31), 14000.0, 2, 90) * 1600 + vnoise(ss / 3500.0, k * 3.7, 91) * 450
            + vnoise(ss / 700.0, k * 5.3, 92) * 80) * env
    off0 = off0 * (1 - .8 * sstep(1100, 2400, base_h(P0[:, 0], P0[:, 1])))   # tight valleys in the ranges
    amp = 1.0
    for _ in range(6):                                           # never let two rivers touch (except at their junctions)
        P = P0 + nrm * (off0 * amp)[:, None]
        if acc_tree is None:
            break
        dd, _ = acc_tree.query(P[env > .99], distance_upper_bound=500)
        if not np.isfinite(dd).any():
            break
        amp *= .55
    a = np.interp(ss, np.linspace(0, s[-1], len(p)), oacc.ravel()[p].astype(float))
    z = height(P[:, 0], P[:, 1])
    z = np.minimum.accumulate(np.maximum(z, 0.0))                 # never uphill
    width = np.clip(6 + 9 * np.sqrt(a / 40.0), 8, 140)           # metres (estimate from drainage area)
    rivers.append(np.stack([P[:, 0], P[:, 1], z, width, a], 1))
    acc_pts.append(P); acc_tree = cKDTree(np.concatenate(acc_pts))
# confluence consistency: a tributary ends ON another river → clamp its last points to that river's level
allp = np.concatenate([r[:, :2] for r in rivers]); allz = np.concatenate([r[:, 2] for r in rivers])
tree_all = cKDTree(allp)
owner = np.concatenate([np.full(len(r), i) for i, r in enumerate(rivers)])
for i, r in enumerate(rivers):
    d, j = tree_all.query(r[-1, :2], k=8)
    for dd, jj in zip(np.atleast_1d(d), np.atleast_1d(j)):
        if owner[jj] != i and dd < 300:
            r[-1, 2] = min(r[-1, 2], allz[jj])
            break
RP = np.concatenate(rivers); RO = np.cumsum([0] + [len(r) for r in rivers])
rtree = cKDTree(RP[:, :2])

# ------------------------------------------------------------------ Ashram pad + path (PROPOSED)
SITE_Z = float(height(np.array([0.0]), np.array([0.0]))[0])
PAD = (-75.0, 75.0, -135.0, 75.0)                               # concept v3 compound (120×124 m) + training ground south

def pad_w(x, y):
    dx = np.maximum(np.maximum(PAD[0] - x, x - PAD[1]), 0); dy = np.maximum(np.maximum(PAD[2] - y, y - PAD[3]), 0)
    return 1 - sstep(0, 160, np.hypot(dx, dy))

# ------------------------------------------------------------------ biome masks
FOR_S = ndi.gaussian_filter(np.isin(ob, [3, 4]).astype(np.float64), .8)
DRY_S = ndi.gaussian_filter(np.isin(ob, [5, 6]).astype(np.float64), .8)

def biome_masks(x, y, hh, slope_deg):
    wx = x + fbm(x, y, 6000, 3, 30) * 2600 + fbm(x, y, 1500, 2, 31) * 600
    wy = y + fbm(x, y, 6000, 3, 32) * 2600 + fbm(x, y, 1500, 2, 33) * 600
    c, r = to_cell(wx, wy)
    b = ob[np.clip(np.round(r).astype(int), 0, OH - 1), np.clip(np.round(c).astype(int), 0, OW - 1)]
    ns = fbm(x, y, 900, 3, 35) * .18
    forest = sstep(.42, .58, ndi.map_coordinates(FOR_S, [r, c], order=1, mode='nearest') + ns)
    rock = np.maximum(sstep(30, 42, slope_deg), (b == 7) * sstep(2400, 3000, hh) * 1.0)
    snowline = 3850 + fbm(x, y, 3000, 3, 34) * 250
    snow = sstep(snowline - 150, snowline + 150, hh) * (1 - sstep(48, 60, slope_deg))
    forest = forest * (1 - sstep(3200, 3500, hh)) * (1 - sstep(34, 42, slope_deg)) * (1 - snow)
    dry = sstep(.42, .58, ndi.map_coordinates(DRY_S, [r, c], order=1, mode='nearest') + ns)
    return forest, rock, snow, dry, b

def build(L, spacing):
    n = int(round(2 * L / spacing)) + 1
    g = np.linspace(-L, L, n)
    X, Y = np.meshgrid(g, g[::-1])                                 # row 0 = north (matches mesh build)
    x, y = X.ravel(), Y.ravel()
    z = height(x, y)
    # rivers
    d, j = rtree.query(np.stack([x, y], 1), distance_upper_bound=4000)
    ok = np.isfinite(d); jj = np.where(ok, j, 0)
    w = RP[jj, 3]; zr = RP[jj, 2]
    far = spacing >= 1000                                        # LOD2: rivers far away → only a narrow valley line, no wide trench
    bank = np.maximum(3 * w, (.6 if far else 1.6) * spacing)
    depth = 1.2 + w / 22
    ri = np.maximum(w / 2, (.35 if far else .75) * spacing)     # coarse LODs: channel spans ≥ 1 vertex row
    inner = ok & (d < ri)
    z_in = (zr - .4 - depth) + depth * (d / ri) ** 2
    z = np.where(inner, np.minimum(z, z_in), z)
    mid = ok & (d >= ri) & (d < ri + bank)
    tb = np.clip((d - ri) / bank, 0, 1) ** 1.6
    z = np.where(mid & (z > zr), zr + tb * (z - zr), z)
    wet = np.where(ok, 1 - sstep(ri * (.5 if far else 1), ri + bank * (.15 if far else .6), d), 0)
    # Ashram pad
    pw = pad_w(x, y)
    z = z * (1 - pw) + SITE_Z * pw
    zz = z.reshape(n, n)
    gy, gx = np.gradient(zz, spacing)
    slope = np.degrees(np.arctan(np.hypot(gx, gy))).ravel()
    forest, rock, snow, dry, b = biome_masks(x, y, z, slope)
    clear = sstep(650, 1100, np.hypot(x, y + 40))                 # open ground around the Ashram (no trees)
    forest = forest * clear * (1 - wet) * (1 - pw)
    # groves: sparse clustered trees on the open grassland (biome stays grassland — no change to the map)
    gn = fbm(x, y, 1800, 4, 40) + fbm(x, y, 400, 2, 41) * .35
    grove = sstep(.18, .42, gn) * (1 - forest) * (1 - rock) * (1 - snow) * (1 - dry) * clear * (1 - wet) * (1 - pw) * (1 - sstep(2400, 2900, z))
    padc = sstep(.93, .995, pw)                                    # colour: compacted earth only on the pad itself
    return dict(n=n, L=L, spacing=spacing, z=zz.astype(np.float32), grove=grove.reshape(n, n).astype(np.float16),
                forest=forest.reshape(n, n).astype(np.float16), rock=rock.reshape(n, n).astype(np.float16),
                snow=snow.reshape(n, n).astype(np.float16), wet=wet.reshape(n, n).astype(np.float16),
                dry=dry.reshape(n, n).astype(np.float16), pad=padc.reshape(n, n).astype(np.float16))

LODS = {'LOD0': (3000.0, 12.5), 'LOD1': (30000.0, 100.0), 'LOD2': (160000.0, 1000.0)}
out = {}
for nm, (L, sp) in LODS.items():
    r = build(L, sp)
    for k, v in r.items():
        out[f'{nm}_{k}'] = v
    print(nm, r['n'], 'z', float(r['z'].min()), float(r['z'].max()), flush=True)

# path (PROPOSED): least-effort route on LOD1 from the gate toward the nearest proposed settlement direction
z1 = out['LOD1_z']; n1 = z1.shape[0]; sp1 = 100.0
gy, gx = np.gradient(z1, sp1)
cost = 1 + (np.hypot(gx, gy) * 30) ** 2
d1, _ = rtree.query(np.stack(np.meshgrid(np.linspace(-30000, 30000, n1), np.linspace(30000, -30000, n1)), -1).reshape(-1, 2))
cost = cost + np.where(d1.reshape(n1, n1) < 60, 40, 0)                 # river crossings are expensive (fords/bridges later)
tg = []
for key in ('villages', 'cities'):
    for (c, r) in OF[key]:
        x, y = to_local(c, r); tg.append((math.hypot(x, y), x, y, key))
tg.sort(); dist_t, tx, ty, tkey = tg[0]
ang = math.atan2(ty, tx)
ex, ey = 29000 * math.cos(ang), 29000 * math.sin(ang)
idx = lambda x, y: int(round((30000 - y) / sp1)) * n1 + int(round((x + 30000) / sp1))
rows, cols, vals = [], [], []
cf = cost.ravel()
for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
    a = np.arange(n1 * n1).reshape(n1, n1)
    r0_, r1_ = max(0, -dr), n1 - max(0, dr); c0_, c1_ = max(0, -dc), n1 - max(0, dc)
    A = a[r0_:r1_, c0_:c1_].ravel(); Bn = a[r0_ + dr:r1_ + dr, c0_ + dc:c1_ + dc].ravel()
    wgt = (cf[A] + cf[Bn]) * .5 * math.hypot(dr, dc)
    rows += [A, Bn]; cols += [Bn, A]; vals += [wgt, wgt]
G = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n1 * n1, n1 * n1)).tocsr()
start = idx(0, -140); goal = idx(ex, ey)
dd, pred = dijkstra(G, indices=start, return_predecessors=True)
path = [goal]
while path[-1] != start and pred[path[-1]] >= 0:
    path.append(pred[path[-1]])
path = path[::-1]
pr, pc = np.divmod(np.array(path), n1)
PX = -30000 + pc * sp1; PY = 30000 - pr * sp1
PP = chaikin(np.stack([PX, PY], 1).astype(float), 3)
PP = PP[np.hypot(PP[:, 0], PP[:, 1] + 140) > 60]                   # start just outside the training ground
PP = np.vstack([[0, -125], PP])                                    # training-ground edge → route (gate is 60 m north)
PZ = height(PP[:, 0], PP[:, 1])

# markers within the LOD2 window (all PROPOSED)
marks = {}
for key in ('villages', 'cities', 'ruins', 'caves', 'waterfalls', 'hidden'):
    L = []
    for (c, r) in OF[key]:
        x, y = to_local(c, r)
        if abs(x) < 160000 and abs(y) < 160000:
            L.append([float(x), float(y), float(base_h(np.array([x]), np.array([y]))[0])])
    marks[key] = L
# nearest snow (detailed biome 8) — direction + distance (same method as MAP_G)
sy_, sx_ = np.nonzero(ob == 8)
k_ = int(np.argmin((sx_ - AX) ** 2 + (sy_ - AY) ** 2))
snow_xy = to_local(sx_[k_], sy_[k_])
meta = {
    'status': 'PROPOSAL — Ashram position + valley = map revision 01 (NOT LOCKED)',
    'frame': 'local metres; origin = proposed Ashram position; +X east, +Y north; Z = elevation above sea level',
    'ashram_cell_C1': [AX, AY], 'site_elev_m': SITE_Z, 'pad_rect_m': PAD,
    'lods': {k: {'half_extent_m': v[0], 'spacing_m': v[1]} for k, v in LODS.items()},
    'n_rivers': len(rivers), 'river_len_km': float(sum(np.hypot(*np.diff(r[:, :2], axis=0).T).sum() for r in rivers) / 1000),
    'river_width_m': [float(RP[:, 3].min()), float(RP[:, 3].max())],
    'path_target': {'kind': tkey, 'dist_km': dist_t / 1000, 'dir_deg': math.degrees(ang)},
    'path_len_km': float(np.hypot(*np.diff(PP, axis=0).T).sum() / 1000),
    'nearest_snow_cell': {'x_km': snow_xy[0] / 1000, 'y_km': snow_xy[1] / 1000, 'dist_km': float(math.hypot(*snow_xy) / 1000)},
    'markers': marks,
}
np.savez_compressed(os.path.join(OUT, 'valley_prep.npz'), RP=RP.astype(np.float32), RO=np.array(RO, np.int64),
                    PATH=np.column_stack([PP, PZ]).astype(np.float32), **out)
json.dump(meta, open(os.path.join(OUT, 'valley_features.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in meta.items() if k != 'markers'}, indent=1))
print('PREP_VALLEY_DONE')

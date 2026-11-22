"""worldgen2 — THE GRAND UNIVERSE: main-world geography v2 (PROPOSAL, not locked).

Run:  python3 02_world/_shared/worldgen2.py
Out:  02_world/map_v2/data/*.npy + features.json      (source of truth for continuity)
      02_world/map_v2/*.png                            (atlas maps — see GEOGRAPHY.md)

World Coordinate System v2 (proposal, ESTIMATES):
  known main world = 12 000 km (W–E) x 6 000 km (N–S); grid cell = 7.8125 km; origin (0,0) = SW corner;
  +X east, +Y north, Z metres above sea level. Equator = map middle row (y = 3 000 km).
  Atlas grid: 1 000 km squares, columns A–L (west→east), rows 1–6 (south→north).
Everything (continents, names, ranges, settlements, the Ashram position) is a PROPOSAL for the Director.
"""
import os, sys, json, math, heapq
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import worldgen as wg

OUT = os.path.join(HERE, '..', 'map_v2'); DATA = os.path.join(OUT, 'data'); os.makedirs(DATA, exist_ok=True)
W, H = 1536, 768
KM = 12000 / W
SEED = 11
F = lambda p, s: ImageFont.truetype(p, s)
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
# ---- merged home continent: the detailed v1 continent (02_world/map, 1 cell = 2 km) becomes C1 HIMAVANT
OLD = os.path.join(HERE, '..', 'map', 'data'); OLD_KM = 3.0
C1W, C1H = int(round(1024 * OLD_KM / (12000 / 1536))), int(round(768 * OLD_KM / (12000 / 1536)))
C1X0, C1Y0 = int(.29 * 1536 - C1W / 2), int(.37 * 768 - C1H / 2)
SXo, SYo = C1W / 1024, C1H / 768
TO = lambda p: (C1X0 + p[0] * SXo, C1Y0 + p[1] * SYo)          # old map cell -> world cell
OLDB = None; OLDLAKE = None
nx, ny = X / W, Y / H                               # ny = 0 north


def fbm(base, octaves, seed, persist=.5):
    return wg.fbm((H, W), base, octaves, persist, seed)


# ---------------------------------------------------------------- continents (all names PROPOSED)
CONT = [  # key, proposed name, centre (nx, ny), radii, rotation, character
    ('C1', 'AETHERIA', (.30, .36), (.165, .17), .25, 'home continent: great northern range, foothill valleys, lakes (Ashram proposed here)'),
    ('C2', 'SOLMARA', (.62, .58), (.13, .17), -.35, 'equatorial / sub-tropical: desert interior, savanna, rainforest coast'),
    ('C3', 'VEYLORA', (.86, .30), (.09, .15), .1, 'wet forest continent: enchanted forests, rivers, misty highlands'),
    ('C4', 'NOXARA', (.58, .075), (.22, .045), 0, 'polar continent: ice sheets, tundra, glaciers (largely unexplored)'),
    ('C5', 'DRAKMOR', (.20, .80), (.11, .095), -.2, 'southern continent: grasslands, plateaus, ancient ruins'),
]
ISLANDS = [  # archipelagos (proposed): centre, spread, count, size
    ('A1', 'SAGARA ARCHIPELAGO', (.47, .44), (.05, .07), 16, 10),
    ('A2', 'AGNI ISLAND ARC', (.75, .58), (.025, .12), 11, 9),
    ('A3', 'WESTERN ISLES', (.06, .55), (.025, .08), 8, 9),
]
RANGES = [  # (code, proposed name, continent, polyline (nx, ny), width, peak m, kind)
    ('M1', 'MAHAGIRI RANGE', 'C1', [((C1X0 + u * C1W) / 1536, (C1Y0 + (.20 + .06 * math.sin(u * 5.1 + .7) + .03 * math.sin(u * 13 + 2)) * C1H) / 768)
                                     for u in (.3, .45, .58, .7, .8)], .028, 0, 'main'),
    ('M3', 'SUNSTONE RIDGE', 'C2', [(.58, .47), (.62, .56), (.66, .68)], .022, 5200, 'main'),
    ('M4', 'VERDANT CROWN', 'C3', [(.86, .19), (.88, .29), (.86, .40)], .018, 4600, 'main'),
    ('M5', 'ICE WALL', 'C4', [(.42, .08), (.58, .06), (.74, .085)], .02, 5600, 'main'),
    ('M6', 'SOUTHERN TEETH', 'C5', [(.14, .78), (.21, .83), (.28, .80)], .016, 3900, 'secondary'),
]


def seg_dist(px, py, pts):
    d = np.full(px.shape, 9.0, np.float32)
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        dx, dy = x1 - x0, (y1 - y0) * H / W
        L2 = dx * dx + dy * dy
        t = np.clip(((px - x0) * dx + (py - y0) * H / W * dy) / L2, 0, 1)
        d = np.minimum(d, np.hypot(px - (x0 + t * dx), (py - y0) * H / W - t * dy))
    return d


def terrain():
    wx, wy = fbm(4, 5, SEED + 1) * 55, fbm(4, 5, SEED + 2) * 55
    px, py = (X + wx) / W, (Y + wy) / H
    land = np.full((H, W), -1.0, np.float32)
    cid = np.zeros((H, W), np.int8)
    for k, (key, nm, (cx, cy), (rx, ry), rot, _) in enumerate(CONT):
        if key == 'C1':
            continue                                  # C1 = the detailed v1 continent, embedded below
        dx, dy = px - cx, (py - cy) * H / W
        c, s = math.cos(rot), math.sin(rot)
        u, v = (dx * c + dy * s) / rx, (-dx * s + dy * c) / (ry * H / W)
        f = 1 - np.sqrt(u * u + v * v) ** 2.0 + fbm(6, 6, SEED + 10 + k) * .55
        cid = np.where(f > land, k + 1, cid); land = np.maximum(land, f)
    rng = np.random.default_rng(SEED)
    for a, nm, (cx, cy), (sx, sy), n, size in ISLANDS:
        for i in range(n):
            ix, iy = cx + rng.normal(0, sx), cy + rng.normal(0, sy)
            r = size * rng.uniform(.4, 1.3)
            f = 1 - np.hypot((X - ix * W) / r, (Y - iy * H) / r) ** 2 + fbm(30, 4, SEED + 50 + i) * .5
            land = np.maximum(land, f * .8)
    edge = np.clip(np.minimum(np.minimum(nx, 1 - nx), np.minimum(ny * 2, (1 - ny) * 2)) / .05, 0, 1)
    land = land * edge - (1 - edge) * .4
    base = np.where(land > 0, land, land)
    h = np.where(base > 0, base * 700 + np.clip(fbm(12, 6, SEED + 3), -1, 1) * 180, base * 4500)
    hills = np.clip(1 - np.abs(fbm(20, 6, SEED + 4)) * 2.4, 0, 1) ** 2
    h += np.where(base > 0, hills * 420 * np.clip(base * 3, 0, 1), 0)
    ridged = np.clip(1 - np.abs(fbm(26, 7, SEED + 5)) * 2.0, 0, 1) ** 1.5
    for code, nm, ck, pts, wdt, peak, kind in RANGES:
        if peak <= 0:
            continue                                  # label-only range (relief comes from the embedded C1 data)
        d = seg_dist(px, py, pts)
        g = np.exp(-(d / wdt) ** 2)
        h += np.where(base > -.05, g * peak * (.42 + .58 * ridged), 0)
    # crater-like Forbidden basin (proposal) on C5 and a great rift valley on C2
    h = smooth_h(h)
    # ---- embed the detailed home continent (v1 map) as C1
    global OLDB, OLDLAKE
    oh = np.load(os.path.join(OLD, 'height_m.npy')); ob = np.load(os.path.join(OLD, 'biome.npy')); ol = np.load(os.path.join(OLD, 'lakes.npy'))
    fz = (C1H / oh.shape[0], C1W / oh.shape[1])
    ohz = ndi.zoom(ndi.gaussian_filter(oh, 1.2), fz, order=1)[:C1H, :C1W]
    obz = ndi.zoom(ob, fz, order=0)[:C1H, :C1W]; olz = ndi.zoom(ol.astype(np.uint8), fz, order=0)[:C1H, :C1W].astype(bool)
    sl = (slice(C1Y0, C1Y0 + ohz.shape[0]), slice(C1X0, C1X0 + ohz.shape[1]))
    sub = h[sl]
    h[sl] = np.where(ohz > 0, ohz, np.minimum(sub, np.maximum(ohz, -2500)))
    cid[sl] = np.where(ohz > 0, 1, np.where(sub > 0, cid[sl], 0))
    OLDB = np.full((H, W), 255, np.uint8); OLDB[sl] = np.where(ohz > 0, np.vectorize(OLD2NEW.get)(obz), 255)
    OLDLAKE = np.zeros((H, W), bool); OLDLAKE[sl] = olz
    return h.astype(np.float32), cid


def smooth_h(h):
    return ndi.gaussian_filter(h, .7)


def priority_flood(h, sea):
    Fh = h.copy(); done = np.zeros(h.shape, bool); pq = []
    border = sea.copy(); border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
    for r, c in zip(*np.nonzero(border)):
        pq.append((float(Fh[r, c]), int(r), int(c))); done[r, c] = True
    heapq.heapify(pq)
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    hl = h.tolist(); Fl = Fh.tolist(); dl = done.tolist()
    while pq:
        z, r, c = heapq.heappop(pq)
        for dr, dc in nb:
            rr, cc = r + dr, c + dc
            if 0 <= rr < H and 0 <= cc < W and not dl[rr][cc]:
                dl[rr][cc] = True
                v = hl[rr][cc]
                if v <= z:
                    v = z + 1e-3
                Fl[rr][cc] = v; heapq.heappush(pq, (v, rr, cc))
    return np.array(Fl, np.float32)


def flow(Fh, sea):
    pad = np.pad(Fh, 1, constant_values=1e9)
    off = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    stack = np.stack([(pad[1 + dr:1 + dr + H, 1 + dc:1 + dc + W] - Fh) / math.hypot(dr, dc) for dr, dc in off])
    k = np.argmin(stack, 0)
    dr = np.array([o[0] for o in off])[k]; dc = np.array([o[1] for o in off])[k]
    down = (np.clip(Y.astype(int) + dr, 0, H - 1) * W + np.clip(X.astype(int) + dc, 0, W - 1))
    down = np.where(sea, -1, down).ravel()
    acc = np.ones(H * W, np.float32)
    for i in np.argsort(-Fh.ravel()):
        j = down[i]
        if j >= 0 and j != i:
            acc[j] += acc[i]
    return down, acc.reshape(H, W)


# ---------------------------------------------------------------- climate + biomes
BIOMES = [  # id, name, hex
    (0, 'Deep ocean', '#0B2545'), (1, 'Coast / beach', '#D9CBA0'), (2, 'Grassland', '#A3BB66'), (3, 'Temperate forest', '#3F7A3F'),
    (4, 'Enchanted forest (proposal)', '#2A6B5E'), (5, 'Desert', '#DDB878'), (6, 'Savanna', '#C2B45E'), (7, 'Tropical rainforest', '#1E5E32'),
    (8, 'Taiga / conifer forest', '#2F5A40'), (9, 'Tundra', '#A7A88E'), (10, 'Ice sheet', '#EEF3F7'), (11, 'High rock', '#8C857C'),
    (12, 'Snow peaks', '#F6F8FA'), (13, 'Wetland', '#5E8A6E'), (14, 'Lake', '#3C8FC0'), (15, 'Wasteland (proposal)', '#8E7A68'),
    (16, 'Forbidden zone (proposal)', '#3B2A3F'),
]
OLD2NEW = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 15, 7: 11, 8: 12, 9: 16, 10: 14}
BCOL = {b: h for b, n, h in BIOMES}


def climate(h, sea, acc):
    land = ~sea
    lat = np.abs(ny - .5) * 2                                    # 0 equator → 1 pole
    temp = 1 - lat ** 1.25 - np.clip(h, 0, None) / 5200
    dsea = ndi.distance_transform_edt(land) * KM
    # prevailing westerlies in mid latitudes, easterlies in the tropics → rain shadow scan
    moist = np.zeros((H, W), np.float32)
    band = np.where(lat < .35, -1, 1)                            # -1: wind from east, 1: from west
    for r in range(H):
        m = 1.0; row = np.zeros(W, np.float32)
        cols = range(W) if band[r, 0] > 0 else range(W - 1, -1, -1)
        prev = 0.0
        for c in cols:
            if sea[r, c]:
                m = min(1.0, m + .08)
            else:
                rise = max(0.0, h[r, c] - prev)
                m *= max(.0, 1 - .00022 * rise - .006)
                m = max(m, .05)
            row[c] = m; prev = max(h[r, c], 0)
        moist[r] = row
    hadley = .55 + .45 * np.cos(lat * math.pi * 3)                 # wet equator, dry ~30°, wet ~60°
    moist = np.clip(moist * .65 + hadley * .35 + .15 * fbm(5, 5, SEED + 30) + .2 * np.exp(-dsea / 300), 0, 1)
    moist = np.where(acc > 400, np.maximum(moist, .5), moist)
    return temp.astype(np.float32), moist.astype(np.float32), dsea


def biomes(h, sea, lakes, temp, moist, dsea):
    B = np.full((H, W), 2, np.uint8)
    t, m = temp, moist
    B[(t > .45) & (m > .45)] = 3
    B[(t > .78) & (m > .58)] = 7
    B[(t > .72) & (m > .22) & (m <= .45)] = 6
    B[(t > .4) & (m <= .24)] = 5
    B[(t <= .45) & (t > .22) & (m > .32)] = 8
    B[(t <= .22)] = 9
    B[(t <= .06)] = 10
    ench = (m > .62) & (t > .45) & (t < .8) & (fbm(3, 4, SEED + 31) > .18)
    B[ench & ((nx > .76) | ((nx > .2) & (nx < .4) & (ny > .3) & (ny < .55)))] = 4
    B[(h > 2600)] = 11
    B[(h > 4200) | ((h > 3000) & (t < .25))] = 12
    wet = (m > .7) & (h < 60) & (h > 0) & (dsea < 40)
    B[wet] = 13
    B[(m < .18) & (t > .5) & (fbm(4, 4, SEED + 32) > .2)] = 15
    B[(~sea) & (dsea < 9) & (h < 30)] = 1
    B[sea] = 0
    B[lakes] = 14
    B = np.where(OLDB != 255, OLDB, B).astype(np.uint8)         # C1 keeps the approved-for-review v1 terrain classes
    B[OLDLAKE] = 14
    return B


# ---------------------------------------------------------------- settlements + features
def spaced(points, score, n, mind_km, taken=()):
    out = []
    for i in np.argsort(-score):
        p = points[i]
        if all(math.dist(p, q) * KM >= mind_km for q in list(out) + list(taken)):
            out.append(p)
        if len(out) >= n:
            break
    return out


def P(mask):
    r, c = np.nonzero(mask); return [(float(a), float(b)) for a, b in zip(c, r)]


def features(h, sea, B, acc, lakes, down, temp, moist, cid, dsea):
    land = ~sea
    rng = np.random.default_rng(SEED + 7)
    riv = land & (acc > 120) & ~lakes
    fe = {}
    # Ashram (CONFIRMED location, PROPOSED position): C1, south of the Mahagiri range, 600–1600 m, by a lake / big river,
    # temperate forest / grassland, 120–450 km from the main crest
    crest = seg_dist(X / W, Y / H, RANGES[0][3]) * W * KM
    green = ndi.uniform_filter(np.isin(B, [3, 8, 4]).astype(np.float32), 9)        # mostly forested surroundings
    ok = land & (cid == 1) & (h > 600) & (h < 1700) & (ny > .24) & (crest > 100) & (crest < 420) & np.isin(B, [3, 8, 4]) & (green > .55)
    lake_d = ndi.distance_transform_edt(~lakes) * KM
    cand = P(ok)
    sc = np.array([math.log1p(acc[int(y), int(x)]) * 1.0 - lake_d[int(y), int(x)] / 60 + green[int(y), int(x)] * 3 for x, y in cand])
    fe['ashram'] = cand[int(np.argmax(sc))] if cand else (W * .3, H * .32)
    OF = json.load(open(os.path.join(OLD, 'features.json')))
    fe['ashram'] = TO(OF['ashram'])                     # same proposed position as the detailed C1 map + 3D concept
    good = land & np.isin(B, [2, 3, 6, 13, 7, 8, 4]) & (h < 600)
    cp = P(good & (acc > 900) & (dsea < 160)); fe['cities'] = spaced(cp, np.array([acc[int(y), int(x)] for x, y in cp]), 18, 600, [fe['ashram']])
    cp = P(good & (acc > 150)); fe['towns'] = spaced(cp, rng.random(len(cp)) + np.array([math.log1p(acc[int(y), int(x)]) for x, y in cp]) * .2, 44, 260, fe['cities'] + [fe['ashram']])
    cp = P(land & np.isin(B, [2, 3, 6, 8, 13, 4, 7]) & (h < 1800) & (acc > 25)); fe['villages'] = spaced(cp, rng.random(len(cp)), 160, 85, fe['cities'] + fe['towns'])
    cp = P(land & np.isin(B, [5, 9, 11, 15, 10]) & (h < 3500)); fe['remote'] = spaced(cp, rng.random(len(cp)), 16, 380, fe['cities'] + fe['towns'])
    cp = P(land & np.isin(B, [5, 3, 7, 4, 15, 2, 6]) & (h > 20)); fe['ruins'] = spaced(cp, rng.random(len(cp)) + np.array([.6 if B[int(y), int(x)] in (5, 7, 4, 15) else 0 for x, y in cp]), 26, 330, fe['cities'])
    cp = P(land & (h > 900) & (h < 3200)); fe['caves'] = spaced(cp, rng.random(len(cp)), 16, 420, [])
    hd = np.where(riv.ravel(), h.ravel() - np.where(down >= 0, h.ravel()[np.clip(down, 0, None)], 0), 0).reshape(H, W)
    cp = P(riv & (hd > 180)); fe['waterfalls'] = spaced(cp, np.array([hd[int(y), int(x)] for x, y in cp]), 14, 350, []) if cp else []
    inC1 = lambda p: cid[min(H - 1, int(p[1])), min(W - 1, int(p[0]))] == 1
    for key, okey in (('cities', 'cities'), ('villages', 'villages'), ('ruins', 'ruins'), ('caves', 'caves'), ('waterfalls', 'waterfalls')):
        fe[key] = [p for p in fe[key] if not inC1(p)] + [TO(p) for p in OF[okey]]
    for key in ('towns', 'remote'):
        fe[key] = [p for p in fe[key] if not inC1(p)]
    fe['c1_hidden'] = [TO(p) for p in OF['hidden']]
    fe['c1_regions'] = [(c, n, TO(p) if p else None, st) for c, n, p, st in OF['regions']]
    fe['c1_city_codes'] = [f'C-{i + 1:02d}' for i in range(len(OF['cities']))]
    # GEM (Director revision 01): location NOT CONFIRMED → PROPOSAL: a hidden ancient region in the main world with a GEM chamber.
    # Placed deep in Veylora's enchanted forest, far from every proposed settlement, in rugged hills.
    gm = land & (cid == 3) & np.isin(B, [4, 3, 7]) & (h > 250) & (h < 2200)
    allset = fe['cities'] + fe['towns'] + fe['villages']
    sp = np.array(allset) if allset else np.zeros((1, 2))
    cp = P(gm)
    if cp:
        cpa = np.array(cp)
        dmin = np.min(np.hypot(cpa[:, None, 0] - sp[None, :, 0], cpa[:, None, 1] - sp[None, :, 1]), 1) * KM
        ench = ndi.uniform_filter((B == 4).astype(np.float32), 15)
        sc_ = np.minimum(dmin, 450) / 450 * 2 + np.array([ench[int(y), int(x)] for x, y in cp]) * 2 + np.array([h[int(y), int(x)] for x, y in cp]) / 2500
        fe['gem'] = cp[int(np.argmax(sc_))]
        fe['gem_isolation_km'] = float(dmin[int(np.argmax(sc_))])
    fe['ruins'] = fe['ruins'] + ([(fe['gem'][0] + 4, fe['gem'][1] + 3)] if 'gem' in fe else [])
    # unexplored territories: polar continent interior + far east ocean margin + C5 south-west plateau
    une = (cid == 4) & land & (ny < .09)
    fe['unexplored_mask'] = une
    # continents: stats
    stats = {}
    for k, (key, nm, c, rr, rot, desc) in enumerate(CONT):
        m = land & (cid == k + 1)
        lab, n = ndi.label(m)
        if n:
            big = 1 + int(np.argmax(ndi.sum(m, lab, range(1, n + 1)))); m = lab == big
        rows, cols = np.nonzero(m)
        area = m.sum() * KM * KM
        bc = {BIOMES[b][1]: round(float((B[m] == b).mean() * 100), 1) for b in range(len(BIOMES)) if (B[m] == b).mean() > .02}
        stats[key] = {'name_proposed': nm, 'area_km2_est': int(area), 'extent_km_est': (int((cols.max() - cols.min()) * KM), int((rows.max() - rows.min()) * KM)),
                      'max_elev_m': int(h[m].max()), 'mean_elev_m': int(h[m].mean()), 'biome_pct': bc, 'desc': desc,
                      'forest_pct': round(float(np.isin(B[m], [3, 4, 7, 8]).mean() * 100), 1),
                      'centre': (float(cols.mean()), float(rows.mean())), 'bbox': (int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())),
                      'ranges': [r[1] for r in RANGES if r[2] == key],
                      'cities': sum(1 for x, y in fe['cities'] if m[int(y), int(x)]), 'towns': sum(1 for x, y in fe['towns'] if m[int(y), int(x)]),
                      'villages': sum(1 for x, y in fe['villages'] if m[int(y), int(x)])}
        idx = np.nonzero((m & (acc > 1500)).ravel())[0]
        stats[key]['major_rivers'] = int(sum(1 for i in idx if down[i] >= 0 and sea.ravel()[down[i]]))   # big rivers reaching the sea
    fe['continents'] = stats
    return fe, riv


def access_routes(h, sea, lakes, fe):
    """PROPOSED access routes: least-cost paths (slope + water penalty) from the Ashram to the nearest town and city."""
    ax, ay = map(int, fe['ashram'])
    R = 90; x0, y0 = max(0, ax - R), max(0, ay - R); x1, y1 = min(W, ax + R), min(H, ay + R)
    hs = h[y0:y1, x0:x1]; gy, gx = np.gradient(hs, KM * 1000)
    cost = 1 + np.hypot(gx, gy) * 60 + np.where(sea[y0:y1, x0:x1] | lakes[y0:y1, x0:x1], 80, 0) + np.where(hs > 3000, 30, 0)
    targets = []
    for key in ('towns', 'cities'):
        best = min(fe[key], key=lambda p: math.dist(p, (ax, ay)))
        if x0 <= best[0] < x1 and y0 <= best[1] < y1:
            targets.append((key, best))
    routes = []
    for key, (tx, ty) in targets:
        start = (ay - y0, ax - x0); goal = (int(ty) - y0, int(tx) - x0)
        dist = {start: 0.0}; prev = {}; pq = [(0.0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == goal:
                break
            if d > dist.get(u, 1e18):
                continue
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == dc == 0:
                        continue
                    v = (u[0] + dr, u[1] + dc)
                    if 0 <= v[0] < hs.shape[0] and 0 <= v[1] < hs.shape[1]:
                        nd = d + cost[v] * math.hypot(dr, dc)
                        if nd < dist.get(v, 1e18):
                            dist[v] = nd; prev[v] = u; heapq.heappush(pq, (nd, v))
        path = [goal]
        while path[-1] in prev:
            path.append(prev[path[-1]])
        routes.append({'to': key, 'target': (tx, ty), 'path': [(c + x0, r + y0) for r, c in path[::-1]],
                       'length_km_est': int(sum(math.dist(a, b) for a, b in zip(path[:-1], path[1:])) * KM)})
    return routes


# ---------------------------------------------------------------- rendering helpers
def hexrgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def colour(h, B, S=2, flat=False):
    hb = ndi.zoom(h, S, order=3); Bb = ndi.zoom(B, S, order=0)
    col = np.zeros(hb.shape + (3,), np.float32); ws = np.zeros(hb.shape, np.float32)
    for b, nm, hx in BIOMES:
        m = (Bb == b).astype(np.float32)
        if not flat and b not in (0, 14):
            m = ndi.gaussian_filter(m, 1.6)
        col += m[..., None] * hexrgb(hx); ws += m
    col /= np.maximum(ws, 1e-3)[..., None]
    land = hb > 0
    dco = ndi.distance_transform_edt(~land)
    sh = np.clip(1 - dco / (22 * S / 2), 0, 1) ** 1.6
    ocean = hexrgb('#0A2747') + (hexrgb('#2F86B0') - hexrgb('#0A2747')) * sh[..., None]
    col = np.where(land[..., None] | (Bb == 14)[..., None], col, ocean)
    if not flat:
        col *= 1 + .05 * wg.fbm(hb.shape, 80, 3, .5, 99)[..., None]
        s = wg.shade(np.maximum(hb, 0) / 7.8, 3.0)
        col = np.where(land[..., None], col * (.5 + .7 * s[..., None]), col)
        coast = land ^ ndi.binary_erosion(land, iterations=1)
        col[coast] = col[coast] * .55 + hexrgb('#EDE3C2') * .45
    return np.clip(col, 0, 255).astype(np.uint8), hb


def rivers(d, acc, down, riv, S, crop=None, scale=None, col=(84, 165, 225), wmul=1.0, arrows=False):
    sc = scale or S; x0, y0 = (crop[0], crop[1]) if crop else (0, 0)
    for r, c in zip(*np.nonzero(riv)):
        j = down[r * W + c]
        if j < 0:
            continue
        r2, c2 = divmod(int(j), W)
        if crop and not (crop[0] <= c <= crop[2] and crop[1] <= r <= crop[3]):
            continue
        w = max(1, int(sc * .6 * math.log10(acc[r, c] / 50 + 1) * wmul))
        d.line(((c - x0 + .5) * sc, (r - y0 + .5) * sc, (c2 - x0 + .5) * sc, (r2 - y0 + .5) * sc), fill=col, width=w)
        if arrows and acc[r, c] > 6000 and (r * 7 + c * 13) % 23 == 0:
            ang = math.atan2(r2 - r, c2 - c); cx, cy = (c - x0 + .5) * sc, (r - y0 + .5) * sc
            d.polygon([(cx + 9 * math.cos(ang), cy + 9 * math.sin(ang)), (cx + 6 * math.cos(ang + 2.4), cy + 6 * math.sin(ang + 2.4)),
                       (cx + 6 * math.cos(ang - 2.4), cy + 6 * math.sin(ang - 2.4))], fill=(20, 60, 120))


def mountain_glyphs(d, h, S, step=9, thr=2200):
    rng = np.random.default_rng(3)
    for r in range(step // 2, H, step):
        for c in range(step // 2, W, step):
            v = h[r, c]
            if v < thr:
                continue
            x, y = (c + rng.uniform(-2, 2)) * S, (r + rng.uniform(-2, 2)) * S
            s = 6 + min(14, (v - thr) / 450)
            d.polygon([(x - s, y + s * .5), (x, y - s), (x + s, y + s * .5)], fill=(118, 108, 96), outline=(55, 45, 38))
            d.polygon([(x, y - s), (x + s, y + s * .5), (x + s * .25, y + s * .5)], fill=(80, 72, 64))
            if v > 3800:
                d.polygon([(x - s * .35, y - s * .3), (x, y - s), (x + s * .35, y - s * .3)], fill=(250, 252, 255))


def forest_glyphs(d, B, S, step=7):
    rng = np.random.default_rng(4)
    for r in range(step // 2, H, step):
        for c in range(step // 2, W, step):
            b = B[r, c]
            if b not in (3, 4, 7, 8):
                continue
            x, y = (c + rng.uniform(-2.5, 2.5)) * S, (r + rng.uniform(-2.5, 2.5)) * S
            colr = {3: (34, 82, 38), 4: (20, 90, 80), 7: (18, 70, 34), 8: (26, 66, 46)}[b]
            if b == 8:
                d.polygon([(x, y - 6), (x - 4, y + 3), (x + 4, y + 3)], fill=colr)
            else:
                d.ellipse((x - 4, y - 4, x + 4, y + 3), fill=colr); d.line((x, y + 3, x, y + 6), fill=(60, 45, 30), width=2)


def compass(d, cx, cy, R=90, col=(240, 230, 205)):
    for a in range(0, 360, 45):
        L = R if a % 90 == 0 else R * .6
        t = math.radians(a - 90)
        p = (cx + L * math.cos(t), cy + L * math.sin(t))
        l1 = (cx + R * .14 * math.cos(t + 1.57), cy + R * .14 * math.sin(t + 1.57)); l2 = (cx + R * .14 * math.cos(t - 1.57), cy + R * .14 * math.sin(t - 1.57))
        d.polygon([p, l1, (cx, cy)], fill=col); d.polygon([p, l2, (cx, cy)], fill=(120, 100, 70))
    d.ellipse((cx - R * .22, cy - R * .22, cx + R * .22, cy + R * .22), outline=col, width=3)
    for k, t in zip('NESW', (-90, 0, 90, 180)):
        a = math.radians(t)
        d.text((cx + (R + 26) * math.cos(a), cy + (R + 26) * math.sin(a)), k, font=F(wg.FS, 30), fill=col, anchor='mm')


def grid(d, S, ox=0, oy=0, col=(255, 255, 255, 55), labels=True):
    step = 1000 / KM
    for i in range(13):
        x = ox + i * step * S; d.line((x, oy, x, oy + H * S), fill=col, width=1)
        if labels and i < 12:
            wg.label(d, x + step * S / 2, oy + 18, 'ABCDEFGHIJKL'[i], 22)
    for j in range(7):
        y = oy + H * S - j * step * S; d.line((ox, y, ox + W * S, y), fill=col, width=1)
        if labels and j < 6:
            wg.label(d, ox + 18, y - step * S / 2, str(j + 1), 22)


def scalebar(d, x, y, S, km=2000, col=(240, 240, 240)):
    px = km / KM * S
    for i in range(4):
        d.rectangle((x + i * px / 4, y, x + (i + 1) * px / 4, y + 14), fill=col if i % 2 == 0 else (40, 40, 40), outline=col)
    for i in range(5):
        d.text((x + i * px / 4, y + 20), f'{int(km * i / 4)}', font=F(wg.FR, 18), fill=col, anchor='ma')
    d.text((x + px + 12, y - 2), 'km (estimate)', font=F(wg.FR, 18), fill=col)


def frame(img, title, sub, legend_w=0, extra_h=0, status='PROPOSAL — NOT LOCKED · awaiting Director approval'):
    Wd, Hd = img.width + legend_w + 80, img.height + 250 + extra_h
    S = Image.new('RGBA', (Wd, Hd), (24, 20, 16, 255)); d = ImageDraw.Draw(S)
    d.rectangle((14, 14, Wd - 14, Hd - 14), outline=(190, 160, 100), width=4); d.rectangle((24, 24, Wd - 24, Hd - 24), outline=(110, 90, 60), width=2)
    ts = 62
    while ts > 30 and d.textlength(title, font=F(wg.FS, ts)) > Wd - 100:
        ts -= 2
    ss = 24
    while ss > 14 and d.textlength(sub, font=F(wg.FR, ss)) > Wd - 100:
        ss -= 1
    d.text((50, 44 + (62 - ts) * .6), title, font=F(wg.FS, ts), fill=(240, 226, 190))
    d.text((52, 122), sub, font=F(wg.FR, ss), fill=(185, 175, 155))
    d.text((50, Hd - 34), status, font=F(wg.FB, 22), fill=(255, 190, 70), anchor='ld')
    S.alpha_composite(img.convert('RGBA'), (40, 180))
    return S, d


def legend_biomes(d, x, y, items=None):
    d.text((x, y), 'TERRAIN / VEGETATION', font=F(wg.FB, 26), fill=(240, 226, 190)); y += 42
    for b, nm, hx in (items or BIOMES):
        d.rectangle((x, y, x + 36, y + 24), fill=tuple(int(v) for v in hexrgb(hx)), outline=(0, 0, 0))
        d.text((x + 50, y), nm, font=F(wg.FR, 20), fill=(225, 220, 210)); y += 32
    return y


def legend_symbols(d, x, y):
    d.text((x, y), 'SYMBOLS (all PROPOSED)', font=F(wg.FB, 26), fill=(240, 226, 190)); y += 44
    for kind, nm in (('ashram', 'Ashram — CONFIRMED location, position PROPOSED'), ('gem', 'GEM hidden region — PROPOSAL'), ('city', 'Major city site'), ('town', 'Town'),
                     ('village', 'Village'), ('remote', 'Remote settlement'), ('ruin', 'Ancient ruins'), ('cave', 'Cave system entrance'),
                     ('fall', 'Waterfall'), ('unexp', 'Unexplored territory')):
        sym(d, kind, x + 18, y + 13, .9)
        d.text((x + 50, y), nm, font=F(wg.FR, 20), fill=(225, 220, 210)); y += 36
    d.line((x, y + 12, x + 36, y + 12), fill=(84, 165, 225), width=5); d.text((x + 50, y), 'River (width = flow)', font=F(wg.FR, 20), fill=(225, 220, 210)); y += 36
    d.polygon([(x + 4, y + 22), (x + 18, y + 2), (x + 32, y + 22)], fill=(118, 108, 96), outline=(55, 45, 38)); d.text((x + 50, y), 'Mountains', font=F(wg.FR, 20), fill=(225, 220, 210)); y += 36
    return y


def sym(d, kind, x, y, s=1.0):
    if kind == 'town':
        d.rectangle((x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s), fill=(245, 236, 210), outline=(40, 30, 20), width=2)
    elif kind == 'remote':
        d.polygon([(x, y - 7 * s), (x - 7 * s, y + 6 * s), (x + 7 * s, y + 6 * s)], fill=(230, 220, 190), outline=(40, 30, 20))
    elif kind in ('gem', 'gemregion'):
        if kind == 'gemregion':
            R_ = 38 * s
            for a0 in range(0, 360, 18):
                d.arc((x - R_, y - R_, x + R_, y + R_), a0, a0 + 9, fill=(120, 255, 200), width=3)
        d.polygon([(x, y - 11 * s), (x + 8 * s, y), (x, y + 11 * s), (x - 8 * s, y)], fill=(90, 255, 200), outline=(10, 60, 50))
    elif kind == 'unexp':
        for k in range(-2, 3):
            d.line((x - 14 + k * 6, y + 10, x - 4 + k * 6, y - 10), fill=(220, 220, 235), width=2)
    else:
        wg.marker(d, kind, x, y, s)


def place(d, x, y, lines, boxes, bounds):
    hs = [ln[1] * 1.3 for ln in lines]; tot = sum(hs)
    wmax = max(d.textlength(t, font=F(wg.FS if kw.get('serif') else wg.FB, sz)) for t, sz, kw in lines)
    for dx, dy in [(0, 0), (0, -55), (0, 55), (0, -100), (0, 100), (-160, 0), (160, 0), (0, 150), (0, -150)]:
        cx = min(max(x + dx, bounds[0] + wmax / 2 + 8), bounds[2] - wmax / 2 - 8)
        bx = (cx - wmax / 2 - 4, y + dy - tot / 2, cx + wmax / 2 + 4, y + dy + tot / 2)
        if not any(bx[0] < b[2] and b[0] < bx[2] and bx[1] < b[3] and b[1] < bx[3] for b in boxes):
            break
    boxes.append(bx); yy = bx[1]
    for (t, sz, kw), hh in zip(lines, hs):
        wg.label(d, cx, yy + hh / 2, t, sz, **kw); yy += hh


# ---------------------------------------------------------------- main
def main():
    h, cid = terrain()
    sea = h <= 0
    print('land %', round((~sea).mean() * 100, 1), 'max', int(h.max()), flush=True)
    Fh = priority_flood(h, sea)
    down, acc = flow(Fh, sea)
    dep = (~sea) & (Fh - h > 6)
    lab, n = ndi.label(dep)
    keep = sorted(((ndi.sum(dep, lab, i), i) for i in range(1, n + 1) if ndi.sum(dep, lab, i) > 12 and ndi.maximum(Fh - h, lab, i) > 35), reverse=True)[:22]
    lakes = ndi.binary_opening(np.isin(lab, [i for _, i in keep]), iterations=1) | OLDLAKE
    temp, moist, dsea = climate(h, sea, acc)
    B = biomes(h, sea, lakes, temp, moist, dsea)
    fe, riv = features(h, sea, B, acc, lakes, down, temp, moist, cid, dsea)
    fe['routes'] = access_routes(h, sea, lakes, fe)
    # ---- continuity audit
    land = ~sea
    rv = riv.ravel(); dd = down
    up = sum(1 for i in np.nonzero(rv)[0] if dd[i] >= 0 and Fh.ravel()[dd[i]] > Fh.ravel()[i] + 1e-6)
    mouths = sum(1 for i in np.nonzero(rv)[0] if dd[i] >= 0 and sea.ravel()[dd[i]])
    lab_land, n_land = ndi.label(land)
    audit = {'river_cells': int(riv.sum()), 'river_steps_uphill_on_filled_surface': int(up), 'river_mouths_to_sea': int(mouths),
             'land_masses': int(n_land), 'lakes': len(keep), 'max_elev_m': int(h.max()),
             'cities_on_river_or_coast': sum(1 for x, y in fe['cities'] if acc[int(y), int(x)] > 900 or dsea[int(y), int(x)] < 160),
             'cities_total': len(fe['cities'])}
    fe['audit'] = audit
    une = fe.pop('unexplored_mask')
    json.dump(fe, open(os.path.join(DATA, 'features.json'), 'w'), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    for nm, a in (('height_m', h), ('filled_m', Fh), ('accum', acc), ('biome', B), ('lakes', lakes), ('temp', temp), ('moist', moist), ('continent_id', cid)):
        np.save(os.path.join(DATA, nm + '.npy'), a)
    print('audit', audit, flush=True)
    render_all(h, B, acc, down, riv, lakes, temp, moist, cid, fe, une, sea)


def render_all(h, B, acc, down, riv, lakes, temp, moist, cid, fe, une, sea):
    S = 2
    col, hb = colour(h, B, S)
    base = Image.fromarray(col).convert('RGBA')
    Image.fromarray(col).save(os.path.join(DATA, 'color_nolabels.png'))
    # ================= A. illustrated master map
    m = base.copy(); d = ImageDraw.Draw(m)
    une_b = ndi.zoom(une.astype(np.uint8), S, order=0).astype(bool)
    hatch = np.zeros(hb.shape + (4,), np.uint8); yy, xx = np.mgrid[0:hb.shape[0], 0:hb.shape[1]]
    hatch[une_b & (((xx + yy) // 6) % 3 == 0)] = (230, 230, 245, 140)
    edge = np.zeros(hb.shape, bool); edge[:, :int(W * S * .03)] = edge[:, -int(W * S * .03):] = True
    hatch[edge & (((xx - yy) // 6) % 3 == 0)] = (200, 210, 230, 70)
    m.alpha_composite(Image.fromarray(hatch)); d = ImageDraw.Draw(m)
    forest_glyphs(d, B, S); rivers(d, acc, down, riv, S); mountain_glyphs(d, h, S)
    ov = Image.new('RGBA', m.size, (0, 0, 0, 0)); grid(ImageDraw.Draw(ov), S); m.alpha_composite(ov); d = ImageDraw.Draw(m)
    labels(d, fe, S, m.size, illustrated=True)
    LW = 760
    full, fd = frame(m, 'THE MAIN WORLD — GEOGRAPHICAL ATLAS', 'Illustrated master map · proposal v2 · known world ≈ 12 000 x 6 000 km (estimate) · '
                     'all names = PROPOSED · grid 1 000 km', LW)
    x0 = m.width + 70; y = 200
    y = legend_biomes(fd, x0, y); y = legend_symbols(fd, x0, y + 20)
    scalebar(fd, x0, y + 30, S * .55); compass(fd, x0 + 560, y + 200, 85)
    fd.text((x0, y + 90), 'Equator = middle of the map (proposal)', font=F(wg.FR, 19), fill=(185, 175, 155))
    fd.text((x0, y + 118), 'Separate dimensions are NOT on this map', font=F(wg.FR, 19), fill=(185, 175, 155))
    fd.text((x0, y + 146), '→ see MAP_H dimensions + MAP_I portals', font=F(wg.FR, 19), fill=(185, 175, 155))
    fd.text((x0, y + 174), 'GEM: proposed hidden region (NOT CONFIRMED)', font=F(wg.FB, 19), fill=(120, 255, 200))
    full.convert('RGB').save(os.path.join(OUT, 'MAP_A_master_illustrated_v2.png'), optimize=True)
    # ================= technical map
    tc, _ = colour(h, B, S, flat=True)
    t = Image.fromarray(tc).convert('RGBA'); td = ImageDraw.Draw(t)
    lv = np.floor(np.maximum(hb, 0) / 1000); e = ((lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))) & (hb > 0)
    a = np.zeros(hb.shape + (4,), np.uint8); a[e] = (30, 25, 20, 150); t.alpha_composite(Image.fromarray(a)); td = ImageDraw.Draw(t)
    rivers(td, acc, down, riv, S, col=(30, 110, 200), wmul=.8)
    ov = Image.new('RGBA', t.size, (0, 0, 0, 0)); grid(ImageDraw.Draw(ov), S, col=(0, 0, 0, 120)); t.alpha_composite(ov); td = ImageDraw.Draw(t)
    labels(td, fe, S, t.size, illustrated=False)
    full, fd = frame(t, 'MAIN WORLD — TECHNICAL MAP', 'Flat biome classes · contours every 1 000 m · codes only · WCS km, origin SW corner (A1) · values = ESTIMATES', LW)
    x0 = t.width + 70; y = legend_biomes(fd, x0, 200); y = legend_symbols(fd, x0, y + 20); scalebar(fd, x0, y + 30, S * .55, col=(240, 240, 240))
    full.convert('RGB').save(os.path.join(OUT, 'MAP_A2_technical_v2.png'), optimize=True)
    # ================= C. mountain + river system map
    e = np.clip(np.maximum(hb, 0) / 8000, 0, 1) ** .6
    rel = np.stack([60 + e * 195, 60 + e * 170, 55 + e * 150], -1) * (.55 + .45 * wg.shade(np.maximum(hb, 0) / 7.8, 3)[..., None])
    rel = np.where((hb <= 0)[..., None], np.array([18, 34, 58]), rel)
    r = Image.fromarray(np.clip(rel, 0, 255).astype(np.uint8)).convert('RGBA'); rd = ImageDraw.Draw(r)
    rivers(rd, acc, down, riv, S, col=(90, 180, 255), wmul=1.2, arrows=True)
    for code, nm, ck, pts, wdt, peak, kind in RANGES:
        pp = [(x * W * S, y * H * S) for x, y in pts]
        rd.line(pp, fill=(255, 120, 60) if kind == 'main' else (255, 200, 90), width=5 if kind == 'main' else 3)
        mid = pp[len(pp) // 2]
        wg.label(rd, mid[0], mid[1] - 36, f'{code} {nm}', 24 if kind == 'main' else 20, color=(255, 210, 150))
        wg.label(rd, mid[0], mid[1] - 10, f'{kind} range · peaks ≈ {int(h[int(pts[len(pts)//2][1]*H), int(pts[len(pts)//2][0]*W)] // 100 * 100)}+ m (est.)', 15, bold=False)
    for p in fe['waterfalls']:
        sym(rd, 'fall', p[0] * S, p[1] * S, 1.1)
    for i, (sz, li) in enumerate([]):
        pass
    full, fd = frame(r, 'MOUNTAIN & RIVER SYSTEMS', 'Relief (sea 0 m → peaks %d m, estimate) · rivers from flow accumulation (always downhill, end at the sea or a lake) · arrows = flow direction' % int(h.max()), 520)
    x0 = r.width + 70; y = 200
    fd.text((x0, y), 'RANGES (PROPOSED names)', font=F(wg.FB, 24), fill=(240, 226, 190)); y += 40
    for code, nm, ck, pts, wdt, peak, kind in RANGES:
        fd.text((x0, y), f'{code} {nm}', font=F(wg.FB, 20), fill=(255, 210, 150)); fd.text((x0, y + 24), f'{CONT[int(ck[1]) - 1][1]} · {kind}', font=F(wg.FR, 17), fill=(185, 175, 155)); y += 56
    y += 10; fd.line((x0, y + 10, x0 + 40, y + 10), fill=(255, 120, 60), width=5); fd.text((x0 + 52, y), 'main range crest', font=F(wg.FR, 19), fill=(225, 220, 210)); y += 34
    fd.line((x0, y + 10, x0 + 40, y + 10), fill=(255, 200, 90), width=3); fd.text((x0 + 52, y), 'secondary range', font=F(wg.FR, 19), fill=(225, 220, 210)); y += 34
    fd.text((x0, y), f"Audit: {fe['audit']['river_steps_uphill_on_filled_surface']} uphill steps", font=F(wg.FB, 19), fill=(140, 255, 160)); y += 28
    fd.text((x0, y), f"{fe['audit']['river_mouths_to_sea']} river mouths reach the sea", font=F(wg.FR, 19), fill=(225, 220, 210))
    full.convert('RGB').save(os.path.join(OUT, 'MAP_C_mountains_rivers_v2.png'), optimize=True)
    # ================= D. forest & vegetation
    veg_ids = [3, 4, 7, 8, 13, 2, 6, 9]
    Bv = np.where(np.isin(B, veg_ids), B, np.where(sea, 0, 99))
    vc = np.zeros((H, W, 3), np.uint8)
    for b, nm, hx in BIOMES:
        vc[Bv == b] = hexrgb(hx)
    vc[Bv == 99] = (205, 196, 176); vc[lakes] = hexrgb('#3C8FC0'); vc[sea] = (14, 36, 62)
    v = Image.fromarray(vc).resize((W * S, H * S), Image.NEAREST).convert('RGBA'); vd = ImageDraw.Draw(v)
    forest_glyphs(vd, B, S, 6); rivers(vd, acc, down, riv, S, col=(60, 130, 200), wmul=.7)
    fs = [(BIOMES[b][1], round(float((B[~sea] == b).mean() * 100), 1)) for b in veg_ids]
    full, fd = frame(v, 'FOREST & VEGETATION MAP', 'Vegetation classes from climate (temperature x moisture) + relief · enchanted forests = PROPOSAL', 560)
    x0 = v.width + 70; y = legend_biomes(fd, x0, 200, [BIOMES[b] for b in veg_ids] + [(99, 'Non-forest / bare / desert', '#CDC4B0')])
    y += 20; fd.text((x0, y), 'SHARE OF LAND (estimate)', font=F(wg.FB, 22), fill=(240, 226, 190)); y += 36
    for nm, pct in fs:
        fd.text((x0, y), f'{nm}: {pct} %', font=F(wg.FR, 19), fill=(225, 220, 210)); y += 28
    full.convert('RGB').save(os.path.join(OUT, 'MAP_D_forest_vegetation_v2.png'), optimize=True)
    # ================= E. climate & terrain
    zones = np.zeros((H, W), np.uint8)
    zones[(temp > .75)] = 1; zones[(temp <= .75) & (temp > .45)] = 2; zones[(temp <= .45) & (temp > .22)] = 3; zones[temp <= .22] = 4
    zcol = {1: '#E0703A', 2: '#E7C35A', 3: '#76B56A', 4: '#7FA8D6'}
    ec = np.zeros((H, W, 3), np.float32)
    for z, hx in zcol.items():
        ec[zones == z] = hexrgb(hx)
    ec = ec * (.55 + .45 * moist[..., None]) + (1 - moist[..., None]) * np.array([60, 40, 20]) * .3
    ec[sea] = (16, 32, 56); ec[lakes] = hexrgb('#3C8FC0')
    ec = ec * (.6 + .4 * wg.shade(np.maximum(h, 0) / 7.8, 3)[..., None])
    c = Image.fromarray(np.clip(ec, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.BILINEAR).convert('RGBA'); cd = ImageDraw.Draw(c)
    for lat, nm in ((.5, 'EQUATOR (proposal)'), (.25, '~45° N'), (.75, '~45° S'), (.1, 'polar circle (approx.)'), (.9, 'polar circle (approx.)')):
        yy = lat * H * S; cd.line((0, yy, W * S, yy), fill=(255, 255, 255), width=2); wg.label(cd, 140, yy - 16, nm, 18)
    full, fd = frame(c, 'CLIMATE & TERRAIN MAP', 'Climate zones by latitude + altitude; brightness = moisture (rain shadows behind ranges, wet coasts) · PROPOSAL', 520)
    x0 = c.width + 70; y = 200
    for z, nm in ((1, 'Tropical (hot)'), (2, 'Warm / sub-tropical'), (3, 'Temperate'), (4, 'Cold / polar / high alpine')):
        fd.rectangle((x0, y, x0 + 36, y + 24), fill=tuple(int(q) for q in hexrgb(zcol[z]))); fd.text((x0 + 50, y), nm, font=F(wg.FR, 20), fill=(225, 220, 210)); y += 34
    fd.text((x0, y + 10), 'Darker = drier, brighter = wetter', font=F(wg.FR, 19), fill=(185, 175, 155))
    fd.text((x0, y + 40), 'Winds: westerlies mid-latitudes,', font=F(wg.FR, 19), fill=(185, 175, 155))
    fd.text((x0, y + 66), 'easterlies in the tropics (proposal)', font=F(wg.FR, 19), fill=(185, 175, 155))
    full.convert('RGB').save(os.path.join(OUT, 'MAP_E_climate_terrain_v2.png'), optimize=True)
    # ================= F. settlements
    sbase = Image.fromarray((np.array(Image.fromarray(tc)) * .45 + 120).astype(np.uint8)).convert('RGBA'); sd = ImageDraw.Draw(sbase)
    rivers(sd, acc, down, riv, S, col=(110, 160, 210), wmul=.6)
    boxes = []
    for kind, key in (('village', 'villages'), ('remote', 'remote'), ('ruin', 'ruins'), ('cave', 'caves'), ('town', 'towns'), ('city', 'cities')):
        for i, p in enumerate(fe[key]):
            sym(sd, kind, p[0] * S, p[1] * S, 1.0 if kind != 'city' else 1.4)
            if kind == 'city':
                place(sd, p[0] * S, p[1] * S + 34, [(f'CITY-{i + 1:02d}', 18, {})], boxes, (0, 0, W * S, H * S))
    a = fe['ashram']; sym(sd, 'ashram', a[0] * S, a[1] * S, 1.4)
    for rt in fe['routes']:
        pp = [(x * S, y * S) for x, y in rt['path']]
        for k in range(0, len(pp) - 1, 2):
            sd.line((pp[k], pp[k + 1]), fill=(160, 60, 30), width=3)
    full, fd = frame(sbase, 'CITIES & SETTLEMENTS', 'All settlements PROPOSED (codes only — no names, rulers or politics invented) · cities on large rivers / coasts', 560)
    x0 = sbase.width + 70; y = legend_symbols(fd, x0, 200); y += 20
    for k, nm in (('cities', 'Major city sites'), ('towns', 'Towns'), ('villages', 'Villages'), ('remote', 'Remote settlements'), ('ruins', 'Ancient ruins'), ('caves', 'Cave systems')):
        fd.text((x0, y), f'{nm}: {len(fe[k])}', font=F(wg.FR, 20), fill=(225, 220, 210)); y += 30
    full.convert('RGB').save(os.path.join(OUT, 'MAP_F_settlements_v2.png'), optimize=True)
    # ================= B. continent maps
    continent_maps(base, h, B, acc, down, riv, fe)
    # ================= G. Ashram regional map
    fe['ashram_routes_detailed'] = ashram_map_detailed(fe)
    gem_map(base, h, B, acc, down, riv, fe)
    dimension_black_hole(); dimension_dark_world()
    # ================= H/I. dimensions + portals
    dimensions()
    portals()
    print('MAPS DONE', flush=True)


def labels(d, fe, S, size, illustrated=True):
    boxes = []
    bnd = (0, 0, size[0], size[1])
    for kind, key in (('village', 'villages'), ('remote', 'remote'), ('ruin', 'ruins'), ('cave', 'caves'), ('fall', 'waterfalls'), ('town', 'towns'), ('city', 'cities')):
        for p in fe[key]:
            sym(d, kind, p[0] * S, p[1] * S, (1.2 if kind == 'city' else .9))
    for p in fe['cities']:
        boxes.append((p[0] * S - 16, p[1] * S - 16, p[0] * S + 16, p[1] * S + 16))
    a = fe['ashram']; sym(d, 'ashram', a[0] * S, a[1] * S, 1.3)
    if 'gem' in fe:
        gx_, gy_ = fe['gem'][0] * S, fe['gem'][1] * S
        sym(d, 'gemregion', gx_, gy_, 1.0)
        place(d, gx_ - 150, gy_ + 70, [('GEM — hidden ancient region', 18, {'color': (120, 255, 200)}), ('PROPOSAL · location NOT CONFIRMED', 14, {})], boxes, bnd)
    place(d, a[0] * S - 190, a[1] * S - 40, [('ASHRAM', 30, {'color': (255, 214, 90), 'serif': True}), ('CONFIRMED location · position PROPOSED', 15, {})], boxes, bnd)
    for k, (key, nm, c, rr, rot, desc) in enumerate(CONT):
        st = fe['continents'][key]; cx, cy = st['centre']
        place(d, cx * S, cy * S + (60 if key == 'C1' else 0), [(' '.join(nm) if illustrated else nm, 46 if illustrated else 34, {'serif': True, 'color': (255, 240, 210)}),
                                   (f'{key} · proposed name · ≈ {st["area_km2_est"] / 1e6:.1f} M km²', 17, {})], boxes, bnd)
    for code, nm, ck, pts, wdt, peak, kind in RANGES:
        x, y = pts[len(pts) // 2]
        place(d, x * W * S, y * H * S - 40, [(nm.title() if illustrated else f'{code} {nm}', 22 if kind == 'main' else 18, {'serif': illustrated, 'color': (250, 225, 200)})], boxes, bnd)
    for a_, nm, (cx, cy), sp, n, s in ISLANDS:
        place(d, cx * W * S, (cy - sp[1] * .8) * H * S, [(nm.title() if illustrated else nm, 20, {'serif': illustrated, 'color': (220, 240, 255)}), ('proposed', 14, {})], boxes, bnd)
    for c, nm, p, st in fe.get('c1_regions', []):
        if p and c not in ('R-01', 'R-07') and 'Range' not in nm:
            place(d, p[0] * S, p[1] * S, [(nm if not illustrated else nm.title(), 17, {'serif': illustrated, 'color': (235, 235, 215)}), (c, 13, {})], boxes, bnd)
    for p in fe.get('c1_hidden', []):
        sym(d, 'hidden', p[0] * S, p[1] * S, .8)
    for (x, y), nm in (((.47, .2), 'NORTHERN OCEAN'), ((.40, .66), 'CENTRAL SEA'), ((.95, .72), 'EASTERN OCEAN'), ((.06, .25), 'WESTERN OCEAN')):
        place(d, x * W * S, y * H * S, [(nm + ' (proposed)', 22, {'serif': True, 'color': (170, 205, 235)})], boxes, bnd)
    if illustrated:
        place(d, .58 * W * S, .03 * H * S + 30, [('— UNEXPLORED —', 22, {'serif': True, 'color': (235, 235, 250)})], boxes, bnd)


def continent_maps(base, h, B, acc, down, riv, fe):
    for key, nm, c, rr, rot, desc in CONT:
        st = fe['continents'][key]; x0, y0, x1, y1 = st['bbox']
        pad = 30; x0, y0 = max(0, x0 - pad), max(0, y0 - pad); x1, y1 = min(W - 1, x1 + pad), min(H - 1, y1 + pad)
        Z = max(1, min(6, int(1500 / max(x1 - x0, 1)), int(1000 / max(y1 - y0, 1))))
        crop = base.crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.LANCZOS)
        hb = ndi.zoom(h[y0:y1, x0:x1], Z, order=1)
        lv = np.floor(np.maximum(hb, 0) / 500); e = ((lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))) & (hb > 0)
        a = np.zeros(hb.shape + (4,), np.uint8); a[e] = (40, 30, 20, 70); crop.alpha_composite(Image.fromarray(a)[:crop.height] if False else Image.fromarray(a).crop((0, 0, crop.width, crop.height)))
        d = ImageDraw.Draw(crop)
        rivers(d, acc, down, riv, Z, crop=(x0, y0, x1, y1), scale=Z)
        boxes = []
        for kind, k2 in (('village', 'villages'), ('remote', 'remote'), ('ruin', 'ruins'), ('cave', 'caves'), ('fall', 'waterfalls'), ('town', 'towns'), ('city', 'cities')):
            for i, p in enumerate(fe[k2]):
                if x0 <= p[0] < x1 and y0 <= p[1] < y1:
                    sym(d, kind, (p[0] - x0) * Z, (p[1] - y0) * Z, 1.1 if kind != 'city' else 1.4)
                    if kind == 'city':
                        place(d, (p[0] - x0) * Z, (p[1] - y0) * Z + 30, [(f'CITY-{fe[k2].index(p) + 1:02d}', 17, {})], boxes, (0, 0, crop.width, crop.height))
        a_ = fe['ashram']
        if x0 <= a_[0] < x1 and y0 <= a_[1] < y1:
            sym(d, 'ashram', (a_[0] - x0) * Z, (a_[1] - y0) * Z, 1.5)
            place(d, (a_[0] - x0) * Z + 140, (a_[1] - y0) * Z, [('ASHRAM (position PROPOSED)', 20, {'color': (255, 214, 90)})], boxes, (0, 0, crop.width, crop.height))
        for code, rn, ck, pts, wdt, peak, kind in RANGES:
            if ck == key:
                x, y = pts[len(pts) // 2]; place(d, (x * W - x0) * Z, (y * H - y0) * Z - 34, [(rn.title(), 24, {'serif': True, 'color': (250, 225, 200)})], boxes, (0, 0, crop.width, crop.height))
        scalebar(d, 30, crop.height - 50, Z, km=500)
        full, fd = frame(crop, f'{key} · {nm} (proposed name)', desc, 620)
        x = crop.width + 70; y = 200
        rows = [('Area (estimate)', f"{st['area_km2_est']:,} km²"), ('Extent W–E x N–S (est.)', f"{st['extent_km_est'][0]:,} x {st['extent_km_est'][1]:,} km"),
                ('Highest point (est.)', f"{st['max_elev_m']:,} m"), ('Mean elevation (est.)', f"{st['mean_elev_m']:,} m"),
                ('Forest cover (est.)', f"{st['forest_pct']} %"), ('Mountain ranges', ', '.join(st['ranges']) or '—'),
                ('Major river systems', str(st['major_rivers'])), ('Proposed city sites', str(st['cities'])), ('Towns / villages', f"{st['towns']} / {st['villages']}")]
        for k, v in rows:
            fd.text((x, y), k, font=F(wg.FB, 21), fill=(240, 226, 190)); fd.text((x, y + 28), v, font=F(wg.FR, 21), fill=(225, 220, 210)); y += 66
        fd.text((x, y + 10), 'TERRAIN MIX (est. % of land)', font=F(wg.FB, 21), fill=(240, 226, 190)); y += 46
        for bn, pct in sorted(st['biome_pct'].items(), key=lambda q: -q[1])[:8]:
            fd.text((x, y), f'{bn}: {pct} %', font=F(wg.FR, 19), fill=(225, 220, 210)); y += 28
        full.convert('RGB').save(os.path.join(OUT, f'MAP_B_continent_{key}_{nm}_v2.png'), optimize=True)


def ashram_map(base, h, B, acc, down, riv, lakes, fe):
    ax, ay = fe['ashram']; R = 48; Z = 12
    x0, y0 = int(max(0, ax - R)), int(max(0, ay - R)); x1, y1 = int(min(W, ax + R)), int(min(H, ay + R))
    hs = h[y0:y1, x0:x1]
    hz = ndi.zoom(hs, Z, order=3) + wg.fbm(((y1 - y0) * Z, (x1 - x0) * Z), 20, 5, .5, 77) * 60 * (ndi.zoom(hs, Z, order=1) > 0)
    Bz = ndi.zoom(B[y0:y1, x0:x1], Z, order=0)
    col = np.zeros(hz.shape + (3,), np.float32); ws = np.zeros(hz.shape, np.float32)
    for b, nm, hx in BIOMES:
        m = ndi.gaussian_filter((Bz == b).astype(np.float32), 6); col += m[..., None] * hexrgb(hx); ws += m
    col /= np.maximum(ws, 1e-3)[..., None]
    col = col * (.45 + .75 * wg.shade(np.maximum(hz, 0) * Z / KM, 1.2)[..., None])
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).convert('RGBA')
    lv = np.floor(np.maximum(hz, 0) / 250); e = ((lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))) & (hz > 0)
    a = np.zeros(hz.shape + (4,), np.uint8); a[e] = (40, 30, 20, 60); im.alpha_composite(Image.fromarray(a))
    d = ImageDraw.Draw(im)
    rivers(d, acc, down, (riv | ((acc > 25) & (h > 0))), Z, crop=(x0, y0, x1 - 1, y1 - 1), scale=Z, wmul=.5)
    forest_glyphs_local(d, Bz)
    for rt in fe['routes']:
        pp = [((x - x0 + .5) * Z, (y - y0 + .5) * Z) for x, y in rt['path'] if x0 <= x < x1 and y0 <= y < y1]
        for k in range(0, len(pp) - 1, 2):
            d.line((pp[k], pp[k + 1]), fill=(150, 50, 25), width=5)
    boxes = []
    for kind, key in (('village', 'villages'), ('town', 'towns'), ('city', 'cities'), ('ruin', 'ruins'), ('cave', 'caves'), ('fall', 'waterfalls'), ('remote', 'remote')):
        for i, p in enumerate(fe[key]):
            if x0 <= p[0] < x1 and y0 <= p[1] < y1:
                sym(d, kind, (p[0] - x0 + .5) * Z, (p[1] - y0 + .5) * Z, 1.6)
                place(d, (p[0] - x0) * Z, (p[1] - y0) * Z + 34, [(f'{key[:-1].upper()} (proposed)', 17, {})], boxes, (0, 0, im.width, im.height))
    px, py = (ax - x0 + .5) * Z, (ay - y0 + .5) * Z
    sym(d, 'ashram', px, py, 2.0)
    place(d, px, py - 70, [('ASHRAM', 36, {'serif': True, 'color': (255, 214, 90)}), ('proposed position (NOT locked)', 17, {})], boxes, (0, 0, im.width, im.height))
    rg = RANGES[0]; place(d, im.width * .5, 60, [('MAHAGIRI RANGE (proposed) — snow peaks to the north', 26, {'serif': True, 'color': (250, 235, 215)})], boxes, (0, 0, im.width, im.height))
    scalebar(d, 30, im.height - 60, Z, km=100)
    elev = int(h[int(ay), int(ax)])
    full, fd = frame(im, 'ASHRAM REGION — LOCATION PROPOSAL', f'≈ {2 * R * KM:.0f} x {2 * R * KM:.0f} km around the proposed site · contours 250 m · dashed red = PROPOSED access routes (least-effort paths)', 640)
    x = im.width + 70; y = 200
    rows = [('Status', 'Ashram = CONFIRMED story location; this position = PROPOSAL'), ('Continent', 'C1 AETHERIA (proposed name)'),
            ('WCS position (est.)', f'({ax * KM:.0f}, {(H - ay) * KM:.0f}) km'), ('Elevation (est.)', f'{elev} m'),
            ('Setting', 'foothill valley south of the Mahagiri Range'), ('Water', 'lake + river system (flow from the range)'),
            ('Forest', 'temperate / conifer forest on slopes'), ('Matches', 'Ashram 3D concept v3 (valley, lake, snow range N)')]
    for k, v in rows:
        fd.text((x, y), k, font=F(wg.FB, 21), fill=(240, 226, 190))
        for j, ln in enumerate([v[i:i + 42] for i in range(0, len(v), 42)]):
            fd.text((x, y + 28 + j * 26), ln, font=F(wg.FR, 19), fill=(225, 220, 210))
        y += 40 + 26 * (len(v) // 42 + 1)
    for rt in fe['routes']:
        fd.text((x, y), f"Route to nearest {rt['to'][:-1]}: ≈ {rt['length_km_est']} km (est.)", font=F(wg.FR, 19), fill=(255, 170, 140)); y += 30
    full.convert('RGB').save(os.path.join(OUT, 'MAP_G_ashram_region_v2.png'), optimize=True)


def ashram_map_detailed(fe):
    """G. Ashram region from the DETAILED C1 data (2 km cells) — same data as the C1 map and the 3D concept."""
    oh = np.load(os.path.join(OLD, 'height_m.npy')); oF = np.load(os.path.join(OLD, 'filled_m.npy'))
    oacc = np.load(os.path.join(OLD, 'accum.npy')); ob = np.load(os.path.join(OLD, 'biome.npy')); ol = np.load(os.path.join(OLD, 'lakes.npy'))
    OF = json.load(open(os.path.join(OLD, 'features.json')))
    osea = oh <= 0; odown, _ = wg.flow(oF, osea)
    ax, ay = OF['ashram']; R = 80; Z = 8
    x0, y0 = int(max(0, ax - R)), int(max(0, ay - 105)); x1, y1 = int(min(oh.shape[1], ax + R + 20)), int(min(oh.shape[0], ay + 75))
    sy_, sx_ = np.nonzero(ob == 8)                                    # nearest snow peaks (detailed data)
    k_ = int(np.argmin((sx_ - ax) ** 2 + (sy_ - ay) ** 2)); rdx, rdy = sx_[k_] - ax, ay - sy_[k_]
    rdir = ['east', 'north-east', 'north', 'north-west', 'west', 'south-west', 'south', 'south-east'][int(((math.degrees(math.atan2(rdy, rdx)) + 22.5) % 360) // 45)]
    rdist = int(math.hypot(rdx, rdy) * OLD_KM)
    hs = oh[y0:y1, x0:x1]
    hz = ndi.zoom(hs, Z, order=3)
    hz = hz + wg.fbm(hz.shape, 24, 5, .5, 77) * 45 * (hz > 0)
    Bz = ndi.zoom(ob[y0:y1, x0:x1], Z, order=0)
    col = np.zeros(hz.shape + (3,), np.float32); ws = np.zeros(hz.shape, np.float32)
    for b, hx in wg.PAL.items():
        m = ndi.gaussian_filter((Bz == b).astype(np.float32), 5); col += m[..., None] * hexrgb(hx); ws += m
    col /= np.maximum(ws, 1e-3)[..., None]
    col = col * (.45 + .75 * wg.shade(np.maximum(hz, 0) * Z / OLD_KM, 1.0)[..., None])
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).convert('RGBA')
    lv = np.floor(np.maximum(hz, 0) / 200); e = ((lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))) & (hz > 0)
    a = np.zeros(hz.shape + (4,), np.uint8); a[e] = (40, 30, 20, 60); im.alpha_composite(Image.fromarray(a))
    d = ImageDraw.Draw(im)
    oriv = (~osea) & (oacc > 40) & ~ol
    for r, c in zip(*np.nonzero(oriv[y0:y1, x0:x1])):
        r += y0; c += x0; j = odown[r * oh.shape[1] + c]
        if j < 0:
            continue
        r2, c2 = divmod(int(j), oh.shape[1])
        w = max(2, int(Z * .45 * math.log10(oacc[r, c] / 30 + 1)))
        d.line(((c - x0 + .5) * Z, (r - y0 + .5) * Z, (c2 - x0 + .5) * Z, (r2 - y0 + .5) * Z), fill=(84, 165, 225), width=w)
    forest_glyphs_local(d, np.where(np.isin(Bz, [3, 4]), 3, 0), 22)
    # PROPOSED access routes: least-effort path to the nearest city site and nearest village
    gy, gx = np.gradient(hs, OLD_KM * 1000)
    cost = 1 + np.hypot(gx, gy) * 40 + np.where(osea[y0:y1, x0:x1] | ol[y0:y1, x0:x1], 60, 0)
    routes = []
    for key in ('cities', 'villages'):
        tgt = [p for p in OF[key] if x0 <= p[0] < x1 and y0 <= p[1] < y1]
        if not tgt:
            continue
        tx, ty = min(tgt, key=lambda p: math.dist(p, (ax, ay)))
        start, goal = (int(ay) - y0, int(ax) - x0), (int(ty) - y0, int(tx) - x0)
        dist = {start: 0.0}; prev = {}; pq = [(0.0, start)]
        while pq:
            dd, u = heapq.heappop(pq)
            if u == goal:
                break
            if dd > dist.get(u, 1e18):
                continue
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    v = (u[0] + dr, u[1] + dc)
                    if (dr or dc) and 0 <= v[0] < hs.shape[0] and 0 <= v[1] < hs.shape[1]:
                        nd = dd + cost[v] * math.hypot(dr, dc)
                        if nd < dist.get(v, 1e18):
                            dist[v] = nd; prev[v] = u; heapq.heappush(pq, (nd, v))
        path = [goal]
        while path[-1] in prev:
            path.append(prev[path[-1]])
        pp = [((c + .5) * Z, (r + .5) * Z) for r, c in path[::-1]]
        for k in range(0, len(pp) - 1, 2):
            d.line((pp[k], pp[k + 1]), fill=(150, 45, 20), width=5)
        routes.append((key[:-1] if key != 'cities' else 'city site', int(sum(math.dist(a_, b_) for a_, b_ in zip(path[:-1], path[1:])) * OLD_KM)))
    boxes = []
    for kind, key in (('village', 'villages'), ('city', 'cities'), ('ruin', 'ruins'), ('cave', 'caves'), ('fall', 'waterfalls')):
        for i, p in enumerate(OF[key]):
            if x0 <= p[0] < x1 and y0 <= p[1] < y1:
                sym(d, kind, (p[0] - x0 + .5) * Z, (p[1] - y0 + .5) * Z, 1.5)
                lab = {'villages': 'village', 'cities': f'C-{i + 1:02d} city site', 'ruins': f'RU-{i + 1:02d} ruins', 'caves': f'CV-{i + 1:02d} cave',
                       'waterfalls': 'waterfall'}[key]
                place(d, (p[0] - x0) * Z, (p[1] - y0) * Z + 32, [(lab + ' (proposed)', 16, {})], boxes, (0, 0, im.width, im.height))
    px, py = (ax - x0 + .5) * Z, (ay - y0 + .5) * Z
    sym(d, 'ashram', px, py, 2.0)
    place(d, px, py - 70, [('ASHRAM', 36, {'serif': True, 'color': (255, 214, 90)}), ('proposed position (NOT locked)', 17, {})], boxes, (0, 0, im.width, im.height))
    place(d, im.width * .5, 95, [(f'Nearest snow peaks: ≈ {rdist} km {rdir} (estimate) · Great Northern Range R-03 further NE', 22, {'serif': True, 'color': (250, 235, 215)})], boxes, (0, 0, im.width, im.height))
    scalebar(d, 30, im.height - 60, Z / OLD_KM * KM, km=100)
    elev = int(oh[int(ay), int(ax)])
    wx, wy = TO((ax, ay))
    full, fd = frame(im, 'ASHRAM REGION — LOCATION PROPOSAL', f'≈ {(x1 - x0) * OLD_KM:.0f} x {(y1 - y0) * OLD_KM:.0f} km around the proposed site (detailed C1 data, 3 km cells) · '
                     'contours 200 m · dashed red = PROPOSED access routes (least-effort paths)', 660)
    x = im.width + 70; y = 200
    rows = [('Status', 'Ashram = CONFIRMED story location; this position = PROPOSAL'), ('Continent', 'C1 AETHERIA (proposed name) — region R-01 Ashram Valley'),
            ('World position (est.)', f'({wx * KM:.0f}, {(H - wy) * KM:.0f}) km in the main-world grid'), ('Elevation (est.)', f'{elev} m'),
            ('Setting (revision 01)', f'large green valley (grassland floor) ringed by forests; snowy range ≈ {rdist} km {rdir}, beyond forests and foothills — visible on clear days (horizon for 5 000 m peaks ≈ 300+ km)'), ('Water', 'several rivers cross the valley (fed by the snowy range); lakes further south-west and south-east'),
            ('Forest', 'dense forest belt between the valley and the mountains'), ('3D concept', 'v3 shows a green valley + distant snow peaks; its backdrop will be re-fitted to this terrain after approval'),
            ('Surrounding settlements', 'proposed villages / city site shown — no names, people or politics invented')]
    for k, v in rows:
        fd.text((x, y), k, font=F(wg.FB, 21), fill=(240, 226, 190))
        lines, cur = [], ''
        for w_ in v.split():
            if len(cur) + len(w_) > 44:
                lines.append(cur); cur = ''
            cur += w_ + ' '
        lines.append(cur)
        for j, ln in enumerate(lines):
            fd.text((x, y + 28 + j * 26), ln, font=F(wg.FR, 19), fill=(225, 220, 210))
        y += 44 + 26 * len(lines)
    for to, km in routes:
        fd.text((x, y), f'Route to nearest {to}: ≈ {km} km (estimate)', font=F(wg.FR, 19), fill=(255, 170, 140)); y += 30
    full.convert('RGB').save(os.path.join(OUT, 'MAP_G_ashram_region_v2.png'), optimize=True)
    return routes


def forest_glyphs_local(d, Bz, step=26):
    rng = np.random.default_rng(9)
    for r in range(step // 2, Bz.shape[0], step):
        for c in range(step // 2, Bz.shape[1], step):
            b = Bz[r, c]
            if b in (3, 4, 7, 8):
                x, y = c + rng.uniform(-8, 8), r + rng.uniform(-8, 8)
                if b == 8:
                    d.polygon([(x, y - 11), (x - 7, y + 6), (x + 7, y + 6)], fill=(28, 70, 44))
                else:
                    d.ellipse((x - 7, y - 7, x + 7, y + 5), fill=(36, 86, 40))


def dimensions():
    """H. separate dimensions map — each dimension its own space, no coordinates shared with the main world."""
    Wd, Hd = 3000, 1500
    im = Image.new('RGBA', (Wd, Hd), (10, 10, 16, 255)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(5)
    for _ in range(1400):
        x, y = rng.uniform(0, Wd), rng.uniform(0, Hd); s = rng.uniform(.5, 2.2); d.ellipse((x - s, y - s, x + s, y + s), fill=(220, 225, 255, int(rng.uniform(80, 255))))
    panels = [('MAIN WORLD', 'physical world · see atlas maps A–G', None, (60, 160, 230)),
              ('BLACK HOLE TRAINING AREA', 'CONFIRMED location · PROPOSED: separate dimension, floating training platforms around a black hole', 'blackhole', (255, 170, 80)),
              ("SAITHAN'S DARK WORLD", 'CONFIRMED location · PROPOSED: separate dimension, ash plains, obsidian spires, corrupted portal', 'dark', (200, 80, 255)),
              ('GEM LOCATION', 'CONFIRMED location · exact place NOT CONFIRMED · PROPOSAL: hidden ancient region on the MAIN WORLD (Veylora) with a GEM chamber — see MAP_J', 'gem', (90, 255, 200))]
    pw = (Wd - 100) // 4
    for k, (t, s, kind, col) in enumerate(panels):
        x0 = 40 + k * (pw + 7); y0 = 240
        d.rounded_rectangle((x0, y0, x0 + pw, y0 + 1040), 30, outline=col + (255,), width=4, fill=(14, 14, 22, 230))
        d.text((x0 + pw / 2, y0 + 40), t, font=F(wg.FS, 34), fill=col, anchor='ma')
        cx, cy = x0 + pw / 2, y0 + 400
        if kind is None:
            g = Image.open(os.path.join(DATA, 'color_nolabels.png')).convert('RGBA').resize((pw - 60, int((pw - 60) / 2)))
            mask = Image.new('L', g.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, g.width, g.height), fill=255)
            im.paste(g, (int(x0 + 30), int(cy - g.height / 2)), mask)
        elif kind in ('blackhole', 'dark'):
            ic = wg.dimension_icon(kind, 420); im.alpha_composite(ic, (int(cx - 210), int(cy - 210)))
            if kind == 'blackhole':
                for i, (r_, a0) in enumerate(((260, .3), (300, 2.2), (330, 4.0), (240, 5.2))):
                    px_, py_ = cx + r_ * math.cos(a0), cy + r_ * .45 * math.sin(a0)
                    d.ellipse((px_ - 26, py_ - 9, px_ + 26, py_ + 9), fill=(120, 110, 100), outline=(255, 190, 110), width=2)
                d.text((cx, cy + 250), 'floating stone platforms (proposal)', font=F(wg.FR, 20), fill=(230, 200, 160), anchor='ma')
            else:
                for i in range(9):
                    px_ = cx - 200 + i * 50 + rng.uniform(-10, 10); hh = rng.uniform(60, 170)
                    d.polygon([(px_ - 12, cy + 230), (px_, cy + 230 - hh), (px_ + 12, cy + 230)], fill=(30, 18, 40), outline=(170, 60, 240))
                d.text((cx, cy + 250), 'obsidian spires + ash plain (proposal)', font=F(wg.FR, 20), fill=(220, 170, 250), anchor='ma')
        else:
            for r_ in range(150, 20, -26):
                d.regular_polygon((cx, cy, r_), 6, rotation=30, outline=col + (255,), width=3)
            d.text((cx, cy), '?', font=F(wg.FS, 120), fill=col, anchor='mm')
            d.text((cx, cy + 250), 'no visual or position confirmed', font=F(wg.FR, 20), fill=(180, 240, 220), anchor='ma')
        yy = y0 + 720
        words = s.split(); line = ''; n = 0
        for w_ in words:
            if len(line) + len(w_) > 38:
                d.text((x0 + 30, yy + n * 30), line, font=F(wg.FR, 21), fill=(225, 225, 235)); n += 1; line = ''
            line += w_ + ' '
        d.text((x0 + 30, yy + n * 30), line, font=F(wg.FR, 21), fill=(225, 225, 235))
        d.text((x0 + 30, y0 + 980), 'Own space · own scale · no shared coordinates', font=F(wg.FB, 18), fill=col)
    d.text((40, 40), 'SEPARATE DIMENSIONS MAP', font=F(wg.FS, 64), fill=(240, 230, 210))
    d.text((40, 120), 'Each special location is drawn as its own space. Nothing here is placed on the main-world map. Looks = PROPOSALS; '
                      'dimension status of the GEM location = NOT CONFIRMED.', font=F(wg.FR, 24), fill=(180, 180, 195))
    d.text((Wd - 40, 50), 'PROPOSAL — awaiting Director approval', font=F(wg.FB, 26), fill=(255, 190, 70), anchor='ra')
    im.convert('RGB').save(os.path.join(OUT, 'MAP_H_dimensions_v2.png'), optimize=True)


def portals():
    """I. portal network — CONFIRMED vs HYPOTHETICAL routes (Director revision 01). Nothing here is story canon."""
    Wd, Hd = 2600, 1600
    im = Image.new('RGB', (Wd, Hd), (14, 15, 22)); d = ImageDraw.Draw(im)
    d.text((40, 36), 'PORTAL NETWORK — PROPOSED CONNECTION DIAGRAM', font=F(wg.FS, 58), fill=(240, 230, 210))
    d.text((40, 110), 'CONFIRMED by the story: magical portals exist. The network itself is NOT established → every route below is HYPOTHETICAL until '
                      'the Director confirms it. No portal rules, costs or distances invented.', font=F(wg.FR, 22), fill=(180, 180, 195))
    N = {'ASHRAM': ((Wd * .30, 520), (255, 214, 90), 'Aetheria · main world'),
         'OTHER MAIN-WORLD\nPLACES': ((Wd * .62, 420), (60, 160, 230), 'any region of the main world'),
         'GEM HIDDEN\nREGION': ((Wd * .78, 760), (90, 255, 200), 'proposal · Veylora · main world'),
         'BLACK HOLE\nTRAINING AREA': ((Wd * .16, 1080), (255, 170, 80), 'separate dimension (proposal)'),
         "SAITHAN'S\nDARK WORLD": ((Wd * .52, 1150), (200, 80, 255), 'separate dimension (proposal)')}
    H_ = [('H1', 'ASHRAM', 'BLACK HOLE\nTRAINING AREA', 'Ashram = training place; training area named “training” → a route is plausible'),
          ('H2', 'OTHER MAIN-WORLD\nPLACES', "SAITHAN'S\nDARK WORLD", 'Saithan has the corrupted-portal power (approved sheet)'),
          ('H3', 'ASHRAM', 'OTHER MAIN-WORLD\nPLACES', 'Hero 1, Pratyush, Ramarat have portal power → travel inside the main world'),
          ('H4', 'OTHER MAIN-WORLD\nPLACES', 'GEM HIDDEN\nREGION', 'only if the story says the GEM can be reached by portal'),
          ('H5', 'ASHRAM', "SAITHAN'S\nDARK WORLD", 'unknown — listed only so the Director can rule it in or out')]
    for code, a, b, why in H_:
        (x0, y0), _, _ = N[a]; (x1, y1), _, _ = N[b]
        L = math.hypot(x1 - x0, y1 - y0); n = int(L / 26)
        for k in range(0, n, 2):
            t0, t1 = k / n, min(1, (k + 1) / n)
            d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=(160, 160, 185), width=5)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d.rounded_rectangle((mx - 46, my - 26, mx + 46, my + 26), 12, fill=(40, 40, 58), outline=(255, 210, 120), width=2)
        d.text((mx, my), code + ' ?', font=F(wg.FB, 24), fill=(255, 220, 130), anchor='mm')
    for nm, ((x, y), col, sub) in N.items():
        d.ellipse((x - 150, y - 150, x + 150, y + 150), fill=(20, 22, 32), outline=col, width=8)
        d.ellipse((x - 118, y - 118, x + 118, y + 118), outline=tuple(int(c * .45) for c in col), width=2)
        d.multiline_text((x, y - 10), nm, font=F(wg.FB, 22 if len(nm) > 18 else 26), fill=col, anchor='mm', align='center')
        d.text((x, y + 70), sub, font=F(wg.FR, 17), fill=(190, 190, 205), anchor='mm')
    x, y = 1880, 960
    d.text((x, y), 'LEGEND', font=F(wg.FB, 26), fill=(240, 230, 210)); y += 44
    d.line((x, y + 12, x + 80, y + 12), fill=(120, 255, 140), width=6); d.text((x + 100, y), 'CONFIRMED route (none yet)', font=F(wg.FR, 21), fill=(225, 225, 235)); y += 40
    for k in range(0, 80, 20):
        d.line((x + k, y + 12, x + k + 10, y + 12), fill=(160, 160, 185), width=5)
    d.text((x + 100, y), 'HYPOTHETICAL route (proposal)', font=F(wg.FR, 21), fill=(225, 225, 235)); y += 56
    for code, a, b, why in H_:
        d.text((x, y), code, font=F(wg.FB, 20), fill=(255, 220, 130))
        words, line, n = why.split(), '', 0
        for w_ in words:
            if len(line) + len(w_) > 40:
                d.text((x + 56, y + n * 24), line, font=F(wg.FR, 18), fill=(210, 210, 222)); n += 1; line = ''
            line += w_ + ' '
        d.text((x + 56, y + n * 24), line, font=F(wg.FR, 18), fill=(210, 210, 222)); y += 24 * (n + 1) + 12
    d.text((40, Hd - 80), 'CONFIRMED portal users (approved character sheets): Hero 1 · Pratyush · Saithan (corrupted portal) · Ramarat.', font=F(wg.FR, 22), fill=(225, 225, 235))
    d.text((40, Hd - 44), 'Director: mark which H-routes exist in the story → they become solid CONFIRMED lines.', font=F(wg.FB, 22), fill=(255, 190, 70))
    im.save(os.path.join(OUT, 'MAP_I_portal_connections_v2.png'), optimize=True)


def gem_map(base, h, B, acc, down, riv, fe):
    """J. GEM hidden ancient region (PROPOSAL) + GEM chamber plan."""
    if 'gem' not in fe:
        return
    gx, gy = fe['gem']; R = 40; Z = 10
    x0, y0 = int(max(0, gx - R)), int(max(0, gy - R)); x1, y1 = int(min(W, gx + R)), int(min(H, gy + R))
    crop = base.crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(crop)
    rivers(d, acc, down, riv | ((acc > 40) & (h > 0)), Z, crop=(x0, y0, x1 - 1, y1 - 1), scale=Z, wmul=.5)
    forest_glyphs_local(d, ndi.zoom(B[y0:y1, x0:x1], Z, order=0), 30)
    px, py = (gx - x0 + .5) * Z, (gy - y0 + .5) * Z
    for r_, a_ in ((170, 255), (120, 180)):
        for a0 in range(0, 360, 10):
            d.arc((px - r_, py - r_, px + r_, py + r_), a0, a0 + 5, fill=(120, 255, 200, a_), width=4)
    sym(d, 'gem', px, py, 2.2)
    sym(d, 'ruin', px + 4 * Z, py + 3 * Z, 1.6)
    boxes = []
    place(d, px, py - 200, [('HIDDEN ANCIENT REGION (proposal)', 26, {'serif': True, 'color': (150, 255, 215)}), ('GEM chamber inside — exact location NOT CONFIRMED', 17, {})], boxes, (0, 0, crop.width, crop.height))
    scalebar(d, 30, crop.height - 60, Z, km=100)
    # chamber plan (schematic, not to world scale)
    P_ = Image.new('RGBA', (760, 760), (12, 16, 18, 255)); pd = ImageDraw.Draw(P_)
    pd.text((380, 26), 'GEM CHAMBER — PLAN (PROPOSAL)', font=F(wg.FB, 26), fill=(150, 255, 215), anchor='ma')
    pd.rectangle((350, 640, 410, 740), fill=(70, 66, 60)); pd.text((420, 700), 'hidden entrance in a cliff (proposal)', font=F(wg.FR, 16), fill=(210, 210, 210))
    pd.rectangle((355, 470, 405, 640), fill=(60, 56, 52)); pd.text((420, 560), 'descending passage', font=F(wg.FR, 16), fill=(210, 210, 210))
    pd.rectangle((250, 380, 510, 470), fill=(80, 74, 66), outline=(150, 140, 120), width=3); pd.text((380, 425), 'antechamber', font=F(wg.FR, 18), fill=(235, 235, 235), anchor='mm')
    pd.ellipse((180, 90, 580, 390), fill=(40, 52, 54), outline=(120, 255, 200), width=4)
    for k in range(8):
        a = k * math.pi / 4; pd.ellipse((380 + 170 * math.cos(a) - 10, 240 + 125 * math.sin(a) - 10, 380 + 170 * math.cos(a) + 10, 240 + 125 * math.sin(a) + 10), fill=(110, 100, 90))
    pd.ellipse((340, 205, 420, 275), fill=(90, 84, 76)); pd.polygon([(380, 215), (398, 240), (380, 265), (362, 240)], fill=(90, 255, 200))
    pd.text((380, 300), 'central chamber · pedestal · GEM', font=F(wg.FR, 17), fill=(235, 235, 235), anchor='mm')
    pd.text((380, 130), 'light shaft from above (proposal)', font=F(wg.FR, 15), fill=(200, 230, 220), anchor='mm')
    pd.text((20, 742), 'Schematic only · no story events, guardians or rules invented', font=F(wg.FR, 14), fill=(160, 170, 170), anchor='ld')
    full, fd = frame(crop, 'GEM — HIDDEN ANCIENT REGION (PROPOSAL)', f'Veylora (proposed name), deep enchanted forest · ≥ {int(fe.get("gem_isolation_km", 0))} km from any proposed settlement · '
                     'location + chamber = PROPOSAL, NOT CONFIRMED', 820, extra_h=60)
    full.alpha_composite(P_, (crop.width + 70, 200))
    gw = (gx * KM, (H - gy) * KM)
    fd.text((crop.width + 70, 990), f'World position (est.): ({gw[0]:.0f}, {gw[1]:.0f}) km', font=F(wg.FR, 20), fill=(225, 220, 210))
    fd.text((crop.width + 70, 1022), f'Elevation (est.): {int(h[int(gy), int(gx)])} m · enchanted forest, ancient ruins nearby', font=F(wg.FR, 20), fill=(225, 220, 210))
    full.convert('RGB').save(os.path.join(OUT, 'MAP_J_gem_hidden_region_v2.png'), optimize=True)


def dimension_black_hole():
    """H1. Black Hole Training Area — proposed dimension layout (own space, own scale, no shared coordinates)."""
    S_ = 1800; im = Image.new('RGBA', (S_ + 700, S_ + 200), (6, 6, 12, 255)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(21)
    for _ in range(2500):
        x, y = rng.uniform(0, S_), rng.uniform(150, S_ + 150); r = rng.uniform(.4, 2); d.ellipse((x - r, y - r, x + r, y + r), fill=(230, 230, 255, int(rng.uniform(60, 255))))
    cx, cy = S_ / 2, S_ / 2 + 150
    ic = wg.dimension_icon('blackhole', 700); im.alpha_composite(ic, (int(cx - 350), int(cy - 350)))
    zones = [(560, 'INNER RING — closest platforms (proposal)', 5, (255, 140, 60)), (700, 'TRAINING RINGS — platform chain (proposal)', 9, (255, 190, 110)),
             (830, 'OUTER RING — arrival / meditation platforms (proposal)', 6, (255, 225, 170))]
    for r_, lab, n, col in zones:
        for a0 in range(0, 360, 6):
            d.arc((cx - r_, cy - r_ * .55, cx + r_, cy + r_ * .55), a0, a0 + 3, fill=col + (150,), width=2)
        for k in range(n):
            a = 2 * math.pi * k / n + r_ / 300
            px, py = cx + r_ * math.cos(a), cy + r_ * .55 * math.sin(a)
            w = 34 + (r_ - 500) / 12
            d.ellipse((px - w, py - w * .35, px + w, py + w * .35), fill=(108, 100, 92), outline=col, width=3)
            d.ellipse((px - w * .9, py - w * .2, px + w * .9, py + w * .45), fill=(70, 64, 58))
    for k in range(260):
        a = rng.uniform(0, 2 * math.pi); r_ = rng.uniform(420, 880); px, py = cx + r_ * math.cos(a), cy + r_ * .55 * math.sin(a)
        s_ = rng.uniform(2, 7); d.polygon([(px, py - s_), (px + s_, py), (px, py + s_), (px - s_ * .8, py)], fill=(120, 110, 100))
    d.text((40, 30), 'BLACK HOLE TRAINING AREA — PROPOSED DIMENSION LAYOUT', font=F(wg.FS, 52), fill=(255, 200, 140))
    d.text((40, 100), 'Separate dimension (PROPOSAL) · own space and scale · no shared coordinates with the main world · '
                      'no physical / dimensional rules invented', font=F(wg.FR, 22), fill=(190, 185, 180))
    x, y = S_ + 40, 220
    d.text((x, y), 'PROPOSED ELEMENTS', font=F(wg.FB, 28), fill=(255, 200, 140)); y += 50
    for t in ('Central black hole + glowing accretion disk', '(the only light source → strong orange rim light)', '',
              'Inner ring: a few large platforms closest', 'to the disk (most dramatic shots)', '',
              'Training rings: chain of platforms around', 'the hole (space for power training + VFX)', '',
              'Outer ring: arrival + meditation platforms', '(calm wide shots)', '', 'Debris field: floating rocks between rings', '',
              'Visual palette: see COLOUR_BIBLE (void #05060C,', 'accretion #FF9A3C / #FFF2D0, lensing #4A6BFF)', '',
              'NOT CONFIRMED: how characters get here,', 'who trains here, any rules of the place.'):
        d.text((x, y), t, font=F(wg.FR, 21), fill=(225, 220, 215)); y += 30
    for r_, lab, n, col in zones:
        d.text((cx + r_ * .72, cy - r_ * .55 * .72 - 14), lab, font=F(wg.FB, 18), fill=col)
    im.convert('RGB').save(os.path.join(OUT, 'MAP_H1_black_hole_training_dimension_v2.png'), optimize=True)


def dimension_dark_world():
    """H2. Saithan's Dark World — proposed dimension layout map (own space)."""
    Wd, Hd = 1800, 1300
    yy, xx = np.mgrid[0:Hd, 0:Wd].astype(np.float32)
    hgt = wg.fbm((Hd, Wd), 5, 6, .55, 61)
    rid = np.clip(1 - np.abs(wg.fbm((Hd, Wd), 9, 6, .5, 62)) * 2.2, 0, 1)
    base = np.stack([30 + 25 * hgt, 24 + 18 * hgt, 34 + 26 * hgt], -1)
    base += (rid[..., None] ** 3) * np.array([110, 30, 50])                          # glowing fissures (blood-stone)
    v = np.clip(1 - np.abs(wg.fbm((Hd, Wd), 3, 4, .5, 63)) * 6, 0, 1)
    base = base * (1 - v[..., None] * .7) + v[..., None] * np.array([150, 40, 50]) * .7  # red rivers of corruption
    sh = wg.shade(hgt * 900, 1.5)
    img = np.clip(base * (.55 + .6 * sh[..., None]), 0, 255).astype(np.uint8)
    im = Image.fromarray(img).convert('RGBA'); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(64)
    for (fx, fy, n) in ((.22, .3, 110), (.72, .25, 90), (.33, .76, 80), (.82, .7, 70)):
        for _ in range(n):
            x = fx * Wd + rng.normal(0, 90); y = fy * Hd + rng.normal(0, 70); hh = rng.uniform(14, 40)
            d.polygon([(x - 5, y), (x, y - hh), (x + 5, y)], fill=(18, 12, 24), outline=(170, 70, 240))
    cx, cy = Wd * .52, Hd * .5
    for r_ in range(90, 20, -12):
        d.ellipse((cx - r_, cy - r_, cx + r_, cy + r_), outline=(255, 42, 42), width=3)
    zones = [((.22, .3), 'OBSIDIAN SPIRE FIELD'), ((.72, .25), 'SPIRE CLIFFS'), ((.33, .76), 'ASH PLAINS'), ((.82, .7), 'SHATTERED HIGHLANDS'),
             ((.52, .5), 'CORRUPTED PORTAL SITE'), ((.6, .88), 'CORRUPTION RIVERS')]
    for (fx, fy), nm in zones:
        wg.label(d, fx * Wd, fy * Hd - 60, nm + ' (proposal)', 22, color=(240, 200, 255))
    full = Image.new('RGBA', (Wd + 640, Hd + 220), (12, 8, 16, 255)); fd = ImageDraw.Draw(full)
    full.alpha_composite(im, (30, 180))
    fd.text((40, 30), "SAITHAN'S DARK WORLD — PROPOSED DIMENSION LAYOUT", font=F(wg.FS, 52), fill=(220, 150, 255))
    fd.text((40, 100), 'Separate dimension (PROPOSAL) · own space and scale · visually separate from the Black Hole Training Area · '
                       'no rules or connections invented', font=F(wg.FR, 22), fill=(190, 180, 200))
    x, y = Wd + 70, 200
    fd.text((x, y), 'PROPOSED ELEMENTS', font=F(wg.FB, 28), fill=(220, 150, 255)); y += 50
    for t in ('Ash plains + obsidian spire fields', 'Blood-stone fissures that glow red', 'Rivers of red corruption (VFX: emissive + fog)',
              'Corrupted portal site — matches Saithan’s', 'approved corrupted-portal power (red rim,', 'black core, reverse swirl)', '',
              'Light: low red key #FF4A3A, violet fill', '#3A1A5A, dense fog #2A1630 (COLOUR_BIBLE)', '',
              'Contrast with Black Hole Training Area:', 'ground-based, red/violet, foggy, oppressive', '(vs. floating platforms, orange/blue, vacuum)', '',
              'NOT CONFIRMED: who lives here, what the', 'place is for, how anyone reaches it.'):
        fd.text((x, y), t, font=F(wg.FR, 21), fill=(225, 215, 230)); y += 30
    full.convert('RGB').save(os.path.join(OUT, 'MAP_H2_saithan_dark_world_dimension_v2.png'), optimize=True)


if __name__ == '__main__':
    main()

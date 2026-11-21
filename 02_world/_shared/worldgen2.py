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
nx, ny = X / W, Y / H                               # ny = 0 north


def fbm(base, octaves, seed, persist=.5):
    return wg.fbm((H, W), base, octaves, persist, seed)


# ---------------------------------------------------------------- continents (all names PROPOSED)
CONT = [  # key, proposed name, centre (nx, ny), radii, rotation, character
    ('C1', 'HIMAVANT', (.30, .36), (.165, .17), .25, 'home continent: great northern range, foothill valleys, lakes (Ashram proposed here)'),
    ('C2', 'MARUDVIPA', (.62, .58), (.13, .17), -.35, 'equatorial / sub-tropical: desert interior, savanna, rainforest coast'),
    ('C3', 'VANADVIPA', (.86, .30), (.09, .15), .1, 'wet forest continent: enchanted forests, rivers, misty highlands'),
    ('C4', 'HIMADVIPA', (.58, .075), (.22, .045), 0, 'polar continent: ice sheets, tundra, glaciers (largely unexplored)'),
    ('C5', 'DAKSHINA', (.20, .80), (.11, .095), -.2, 'southern continent: grasslands, plateaus, ancient ruins'),
]
ISLANDS = [  # archipelagos (proposed): centre, spread, count, size
    ('A1', 'SAGARA ARCHIPELAGO', (.47, .44), (.05, .07), 16, 10),
    ('A2', 'AGNI ISLAND ARC', (.75, .58), (.025, .12), 11, 9),
    ('A3', 'WESTERN ISLES', (.06, .55), (.025, .08), 8, 9),
]
RANGES = [  # (code, proposed name, continent, polyline (nx, ny), width, peak m, kind)
    ('M1', 'MAHAGIRI RANGE', 'C1', [(.17, .27), (.24, .22), (.32, .21), (.40, .24), (.45, .30)], .028, 8200, 'main'),
    ('M2', 'WESTERN SPINE', 'C1', [(.16, .33), (.15, .43), (.18, .52)], .02, 4200, 'secondary'),
    ('M3', 'SUNSTONE RIDGE', 'C2', [(.58, .47), (.62, .56), (.66, .68)], .022, 5200, 'main'),
    ('M4', 'VERDANT CROWN', 'C3', [(.86, .19), (.88, .29), (.86, .40)], .018, 4600, 'main'),
    ('M5', 'ICE WALL', 'C4', [(.42, .08), (.58, .06), (.74, .085)], .02, 5600, 'main'),
    ('M6', 'SOUTHERN TEETH', 'C5', [(.14, .78), (.21, .83), (.28, .80)], .016, 3900, 'secondary'),
    ('M7', 'TWIN HILLS', 'C1', [(.33, .44), (.38, .49)], .016, 2600, 'secondary'),
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
        d = seg_dist(px, py, pts)
        g = np.exp(-(d / wdt) ** 2)
        h += np.where(base > -.05, g * peak * (.42 + .58 * ridged), 0)
    # crater-like Forbidden basin (proposal) on C5 and a great rift valley on C2
    h = smooth_h(h)
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
]
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
    good = land & np.isin(B, [2, 3, 6, 13, 7, 8, 4]) & (h < 600)
    cp = P(good & (acc > 900) & (dsea < 160)); fe['cities'] = spaced(cp, np.array([acc[int(y), int(x)] for x, y in cp]), 18, 600, [fe['ashram']])
    cp = P(good & (acc > 150)); fe['towns'] = spaced(cp, rng.random(len(cp)) + np.array([math.log1p(acc[int(y), int(x)]) for x, y in cp]) * .2, 44, 260, fe['cities'] + [fe['ashram']])
    cp = P(land & np.isin(B, [2, 3, 6, 8, 13, 4, 7]) & (h < 1800) & (acc > 25)); fe['villages'] = spaced(cp, rng.random(len(cp)), 160, 85, fe['cities'] + fe['towns'])
    cp = P(land & np.isin(B, [5, 9, 11, 15, 10]) & (h < 3500)); fe['remote'] = spaced(cp, rng.random(len(cp)), 16, 380, fe['cities'] + fe['towns'])
    cp = P(land & np.isin(B, [5, 3, 7, 4, 15, 2, 6]) & (h > 20)); fe['ruins'] = spaced(cp, rng.random(len(cp)) + np.array([.6 if B[int(y), int(x)] in (5, 7, 4, 15) else 0 for x, y in cp]), 26, 330, fe['cities'])
    cp = P(land & (h > 900) & (h < 3200)); fe['caves'] = spaced(cp, rng.random(len(cp)), 16, 420, [])
    hd = np.where(riv.ravel(), h.ravel() - np.where(down >= 0, h.ravel()[np.clip(down, 0, None)], 0), 0).reshape(H, W)
    cp = P(riv & (hd > 180)); fe['waterfalls'] = spaced(cp, np.array([hd[int(y), int(x)] for x, y in cp]), 14, 350, []) if cp else []
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
        bc = {BIOMES[b][1]: round(float((B[m] == b).mean() * 100), 1) for b in range(16) if (B[m] == b).mean() > .02}
        stats[key] = {'name_proposed': nm, 'area_km2_est': int(area), 'extent_km_est': (int((cols.max() - cols.min()) * KM), int((rows.max() - rows.min()) * KM)),
                      'max_elev_m': int(h[m].max()), 'mean_elev_m': int(h[m].mean()), 'biome_pct': bc, 'desc': desc,
                      'forest_pct': round(float(np.isin(B[m], [3, 4, 7, 8]).mean() * 100), 1),
                      'centre': (float(cols.mean()), float(rows.mean())), 'bbox': (int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())),
                      'ranges': [r[1] for r in RANGES if r[2] == key],
                      'cities': sum(1 for x, y in fe['cities'] if m[int(y), int(x)]), 'towns': sum(1 for x, y in fe['towns'] if m[int(y), int(x)]),
                      'villages': sum(1 for x, y in fe['villages'] if m[int(y), int(x)])}
        mm = m & riv
        stats[key]['major_rivers'] = int(ndi.label(m & (acc > 2500))[1])
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
    Wd, Hd = img.width + legend_w + 80, img.height + 220 + extra_h
    S = Image.new('RGBA', (Wd, Hd), (24, 20, 16, 255)); d = ImageDraw.Draw(S)
    d.rectangle((14, 14, Wd - 14, Hd - 14), outline=(190, 160, 100), width=4); d.rectangle((24, 24, Wd - 24, Hd - 24), outline=(110, 90, 60), width=2)
    d.text((50, 44), title, font=F(wg.FS, 62), fill=(240, 226, 190))
    d.text((52, 122), sub, font=F(wg.FR, 24), fill=(185, 175, 155))
    d.text((Wd - 50, 60), status, font=F(wg.FB, 26), fill=(255, 190, 70), anchor='ra')
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
    for kind, nm in (('ashram', 'Ashram — CONFIRMED location, position PROPOSED'), ('city', 'Major city site'), ('town', 'Town'),
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
    lakes = ndi.binary_opening(np.isin(lab, [i for _, i in keep]), iterations=1)
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
    fd.text((x0, y + 174), 'GEM location: position NOT CONFIRMED', font=F(wg.FB, 19), fill=(120, 255, 200))
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
    ashram_map(base, h, B, acc, down, riv, lakes, fe)
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
    place(d, a[0] * S + 210, a[1] * S + 6, [('ASHRAM', 30, {'color': (255, 214, 90), 'serif': True}), ('CONFIRMED location · position PROPOSED', 15, {})], boxes, bnd)
    for k, (key, nm, c, rr, rot, desc) in enumerate(CONT):
        st = fe['continents'][key]; cx, cy = st['centre']
        place(d, cx * S, cy * S + (60 if key == 'C1' else 0), [(' '.join(nm) if illustrated else nm, 46 if illustrated else 34, {'serif': True, 'color': (255, 240, 210)}),
                                   (f'{key} · proposed name · ≈ {st["area_km2_est"] / 1e6:.1f} M km²', 17, {})], boxes, bnd)
    for code, nm, ck, pts, wdt, peak, kind in RANGES:
        x, y = pts[len(pts) // 2]
        place(d, x * W * S, y * H * S - 40, [(nm.title() if illustrated else f'{code} {nm}', 22 if kind == 'main' else 18, {'serif': illustrated, 'color': (250, 225, 200)})], boxes, bnd)
    for a_, nm, (cx, cy), sp, n, s in ISLANDS:
        place(d, cx * W * S, (cy - sp[1] * .8) * H * S, [(nm.title() if illustrated else nm, 20, {'serif': illustrated, 'color': (220, 240, 255)}), ('proposed', 14, {})], boxes, bnd)
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
    rows = [('Status', 'Ashram = CONFIRMED story location; this position = PROPOSAL'), ('Continent', 'C1 HIMAVANT (proposed name)'),
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
              ('GEM LOCATION', 'CONFIRMED location · whether it is a dimension or on the main world = NOT CONFIRMED', 'gem', (90, 255, 200))]
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
    """I. portal connection diagram — only confirmed links solid; everything else = unknown (dashed '?')."""
    Wd, Hd = 2400, 1500
    im = Image.new('RGB', (Wd, Hd), (14, 15, 22)); d = ImageDraw.Draw(im)
    d.text((40, 36), 'PORTAL CONNECTION DIAGRAM', font=F(wg.FS, 60), fill=(240, 230, 210))
    d.text((40, 112), 'Solid line = CONFIRMED connection · dashed + “?” = possible link, NOT CONFIRMED · no portal rules or distances invented',
           font=F(wg.FR, 24), fill=(180, 180, 195))
    nodes = {'MAIN WORLD\n(incl. ASHRAM)': ((Wd * .5, 430), (60, 160, 230)), 'BLACK HOLE\nTRAINING AREA': ((Wd * .2, 1000), (255, 170, 80)),
             "SAITHAN'S\nDARK WORLD": ((Wd * .8, 1000), (200, 80, 255)), 'GEM LOCATION\n(type unknown)': ((Wd * .5, 1180), (90, 255, 200))}
    keys = list(nodes)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            (x0, y0), _ = nodes[keys[i]]; (x1, y1), _ = nodes[keys[j]]
            L = math.hypot(x1 - x0, y1 - y0); n = int(L / 28)
            for k in range(0, n, 2):
                t0, t1 = k / n, min(1, (k + 1) / n)
                d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=(150, 150, 170), width=4)
            d.ellipse(((x0 + x1) / 2 - 26, (y0 + y1) / 2 - 26, (x0 + x1) / 2 + 26, (y0 + y1) / 2 + 26), fill=(40, 40, 55), outline=(200, 200, 220), width=2)
            d.text(((x0 + x1) / 2, (y0 + y1) / 2), '?', font=F(wg.FB, 30), fill=(255, 220, 120), anchor='mm')
    for nm, ((x, y), col) in nodes.items():
        d.ellipse((x - 150, y - 150, x + 150, y + 150), fill=(20, 22, 32), outline=col, width=8)
        for r_ in (120, 95):
            d.ellipse((x - r_, y - r_, x + r_, y + r_), outline=tuple(int(c * .5) for c in col), width=2)
        d.multiline_text((x, y), nm, font=F(wg.FB, 26), fill=col, anchor='mm', align='center')
    y = 1340
    d.text((40, y), 'CONFIRMED portal users (approved character sheets): Hero 1, Pratyush, Saithan (corrupted portal), Ramarat. '
                    'Which locations their portals connect = NOT CONFIRMED.', font=F(wg.FR, 22), fill=(225, 225, 235))
    d.text((40, y + 40), 'Director: tell us which links exist in the story → they become solid lines.', font=F(wg.FB, 22), fill=(255, 190, 70))
    im.save(os.path.join(OUT, 'MAP_I_portal_connections_v2.png'), optimize=True)


if __name__ == '__main__':
    main()

"""worldgen — procedural MASTER WORLD MAP (proposal v1).

Run:  python3 02_world/_shared/worldgen.py [seed]
Out:  02_world/map/data/  height_m.npy, filled_m.npy, accum.npy, biome.npy, lakes.npy, features.json,
                          height16.png (Blender displacement), color_nolabels.png (Blender texture)
      02_world/map/WORLD_MAP_master_v1.png        full labelled map + legend + dimensions panel
      02_world/map/WORLD_MAP_regional_v1.png      6 regional maps with contours + local scale
      02_world/map/WORLD_MAP_elevation_v1.png     elevation / hydrology reference

World Coordinate System (WCS, proposal): 1 map cell = 1 km. Map = 1024 x 768 km.
Origin (0, 0) = south-west corner, +X = east, +Y = north, Z = metres above sea level.
Grid squares = 100 km, columns A..K (west->east), rows 1..8 (south->north).
Everything on this map is a PROPOSAL: region names are working labels / codes until the Director approves them.
"""
import os, sys, json, math, heapq
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'map'); DATA = os.path.join(OUT, 'data')
os.makedirs(DATA, exist_ok=True)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
SC = 3.0      # km per map cell — this map is the detailed map of the home continent C1 HIMAVANT inside the main world (worldgen2)
W, H = 1024, 768            # km
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FS = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
F = lambda p, s: ImageFont.truetype(p, s)
rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------------------- noise
def fbm(shape, base=4, octaves=7, persist=.5, seed=0):
    """fractal value noise in [-1, 1]-ish; `base` = cells across the short side at octave 0."""
    r = np.random.default_rng(seed)
    hh, ww = shape
    out = np.zeros(shape, np.float32); amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        cs = min(hh, ww) / n                       # pixels per noise cell
        g = r.standard_normal((int(hh / cs) + 4, int(ww / cs) + 4)).astype(np.float32)
        z = ndi.zoom(g, cs, order=3)
        o0 = int(cs)
        out += amp * z[o0:o0 + hh, o0:o0 + ww]; tot += amp; amp *= persist
    return out / tot * 1.6


def smooth(a, s):
    return ndi.gaussian_filter(a, s)


Y, X = np.mgrid[0:H, 0:W].astype(np.float32)     # row 0 = NORTH (image space); WCS y = H - row
nx, ny = X / W, Y / H


# ---------------------------------------------------------------------------- terrain
def terrain():
    wx = fbm((H, W), 3, 5, seed=SEED + 1) * 70
    wy = fbm((H, W), 3, 5, seed=SEED + 2) * 70
    cx, cy = (X + wx) / W - .5, (Y + wy) / H - .52
    d = np.sqrt((cx / .43) ** 2 + (cy / .41) ** 2)
    cont = 1 - d ** 2.2
    n = fbm((H, W), 4, 8, seed=SEED + 3)
    base = cont * 1.05 + n * .32
    edge = np.clip(np.minimum(np.minimum(nx, 1 - nx), np.minimum(ny, 1 - ny)) / .07, 0, 1)
    base = base * edge - (1 - edge) * .35          # open sea all around the map frame
    # northern great range: ridged noise along a wavy arc
    arc = .20 + .06 * np.sin(nx * 5.1 + .7) + .03 * np.sin(nx * 13 + 2)
    dist = (ny - arc)
    ridge = 1 - np.abs(fbm((H, W), 6, 7, seed=SEED + 4)) * 2.2
    north = np.exp(-(dist / .11) ** 2) * np.clip(ridge, 0, 1) ** 1.6 * np.clip((nx - .06) / .1, 0, 1) * np.clip((.97 - nx) / .1, 0, 1)
    # eastern spine (lower, forested)
    ex = .80 + .04 * np.sin(ny * 7)
    east = np.exp(-((nx - ex) / .05) ** 2) * np.exp(-((ny - .55) / .22) ** 2) * np.clip(1 - np.abs(fbm((H, W), 6, 6, seed=SEED + 5)) * 2, 0, 1)
    hills = np.clip(1 - np.abs(fbm((H, W), 10, 6, seed=SEED + 7)) * 2.4, 0, 1) ** 2
    h = np.where(base > 0, base * 1000 + north * 6400 + east * 2800 + hills * 520 * np.clip(base * 3, 0, 1), base * 3800)
    h += np.where(base > 0, fbm((H, W), 16, 6, seed=SEED + 6) * 140, 0)
    # forbidden crater (south-west): blasted bowl with a raised rim
    fc = np.array([.27, .63]); r = np.sqrt(((nx - fc[0]) * W) ** 2 + ((ny - fc[1]) * H) ** 2)
    h = np.where(base > 0, h - 520 * np.exp(-(r / 38) ** 2) + 360 * np.exp(-((r - 46) / 9) ** 2), h)
    return smooth(h.astype(np.float32), .8), (fc[0] * W, fc[1] * H)


def priority_flood(h, sea):
    """Fill depressions (epsilon) so every land cell drains to the sea."""
    Fh = h.copy(); done = np.zeros(h.shape, bool)
    pq = []
    border = sea | np.pad(np.zeros((H - 2, W - 2), bool), 1, constant_values=True)
    for r, c in zip(*np.nonzero(border)):
        heapq.heappush(pq, (float(Fh[r, c]), int(r), int(c))); done[r, c] = True
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
                Fl[rr][cc] = v
                heapq.heappush(pq, (v, rr, cc))
    return np.array(Fl, np.float32)


def flow(Fh, sea):
    pad = np.pad(Fh, 1, constant_values=1e9)
    off = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    stack = np.stack([(pad[1 + dr:1 + dr + H, 1 + dc:1 + dc + W] - Fh) / math.hypot(dr, dc) for dr, dc in off])
    k = np.argmin(stack, 0)
    dr = np.array([o[0] for o in off])[k]; dc = np.array([o[1] for o in off])[k]
    down = np.clip(Y.astype(int) + dr, 0, H - 1) * W + np.clip(X.astype(int) + dc, 0, W - 1)
    down = np.where(sea, -1, down).ravel()
    acc = np.ones(H * W, np.float32)
    order = np.argsort(-Fh.ravel())
    dl = down
    for i in order:
        j = dl[i]
        if j >= 0 and j != i:
            acc[j] += acc[i]
    return down, acc.reshape(H, W)


def spaced(cands, score, n, mind, taken=()):
    idx = np.argsort(-score)
    out = []
    for i in idx:
        p = cands[i]
        if all(math.dist(p, q) >= mind for q in list(out) + list(taken)):
            out.append(p)
        if len(out) >= n:
            break
    return out


def main():
    h, crater = terrain()
    sea = h <= 0
    land = ~sea
    print('land %', round(land.mean() * 100, 1), 'max m', int(h.max()))
    Fh = priority_flood(h, sea)
    down, acc = flow(Fh, sea)
    dep = land & (Fh - h > 8)
    lab0, n0 = ndi.label(dep)
    keep = []
    for i in range(1, n0 + 1):
        area = ndi.sum(dep, lab0, i); depth = ndi.maximum(Fh - h, lab0, i)
        if area > 40 and depth > 45:
            keep.append((area, i))
    keep = [i for _, i in sorted(keep, reverse=True)[:9]]
    lakes = np.isin(lab0, keep)
    lakes = ndi.binary_opening(lakes, iterations=1)
    # climate (proposal): wet east / dry west (rain shadow), cold north + altitude
    dsea = ndi.distance_transform_edt(land)
    moist = np.clip(.15 + .75 * nx + .25 * fbm((H, W), 5, 5, seed=SEED + 9) + .25 * np.exp(-dsea / 60), 0, 1)
    moist = np.where(acc > 30, np.maximum(moist, .55), moist)
    temp = 1 - ny * .2 - np.clip(h, 0, None) / 4200
    # biomes: 0 sea, 1 beach, 2 grass, 3 forest, 4 enchanted forest, 5 desert, 6 wasteland, 7 rock, 8 snow, 9 forbidden, 10 lake
    B = np.full((H, W), 2, np.uint8)
    B[moist > .55] = 3
    ench = (moist + .35 * fbm((H, W), 3, 4, seed=SEED + 11) + .25 * np.exp(-(((nx - .63) / .14) ** 2 + ((ny - .62) / .16) ** 2)) > .95) & (h < 1400)
    B[ench] = 4
    B[(moist < .33) & (h < 1600)] = 5
    B[(moist < .40) & (moist >= .33) & (h < 1600)] = 6
    B[h > 2300] = 7
    B[(h > 3600) | ((temp < .2) & (h > 2600))] = 8
    rc = np.sqrt((X - crater[0]) ** 2 + (Y - crater[1]) ** 2)
    B[rc < 60] = 9
    B[land & (dsea < 2.5) & (h < 40)] = 1
    B[sea] = 0
    B[lakes] = 10
    # ------------------------------------------------------------------ features (all PROPOSED)
    riv = land & (acc > 140) & ~lakes
    pts = lambda m: [(float(c), float(r)) for r, c in zip(*np.nonzero(m))]
    # Ashram Valley: foothill valley on a strong river, 700-1600 m, south of the great range
    cand = land & (acc > 600) & (h > 700) & (h < 1600) & (ny > .25) & (ny < .55) & (nx > .3) & (nx < .7)
    cp = pts(cand)
    ash = spaced(cp, np.array([acc[int(p[1]), int(p[0])] for p in cp]), 1, 0) if cp else [(W * .5, H * .4)]
    ash = ash[0]
    cities_c = land & (acc > 1500) & (h < 300) & (h > 5)
    cp = pts(cities_c)
    cities = spaced(cp, np.array([acc[int(p[1]), int(p[0])] for p in cp]), 3, 170, [ash])
    vil_c = land & (acc > 60) & (h < 1500) & (h > 10) & (B != 9) & (B != 5)
    cp = pts(vil_c); vr = np.random.default_rng(SEED + 20)
    villages = spaced(cp, vr.random(len(cp)), 14, 55, [ash] + cities)
    ru_c = land & (h > 30) & (h < 2200) & (B != 10)
    cp = pts(ru_c)
    ruins = spaced(cp, vr.random(len(cp)) + np.array([.8 if B[int(p[1]), int(p[0])] in (5, 6, 4) else 0 for p in cp]), 6, 120,
                   [ash] + cities)
    cv_c = land & (h > 1500) & (h < 3200)
    cp = pts(cv_c)
    caves = spaced(cp, vr.random(len(cp)), 5, 110, [ash])
    # waterfalls: big drops on rivers
    hd = np.where(riv.ravel(), h.ravel() - np.where(down >= 0, h.ravel()[np.clip(down, 0, None)], 0), 0).reshape(H, W)
    cp = pts(riv & (hd > 60))
    falls = spaced(cp, np.array([hd[int(p[1]), int(p[0])] for p in cp]), 5, 90) if cp else []
    # hidden regions (dashed): a deep-forest glade and a high plateau
    fo = pts(B == 4)
    hidden = []
    if fo:
        hidden.append(tuple(np.array(fo).mean(0)))
    hp = pts(land & (h > 2600) & (h < 3600))
    if hp:
        hidden += spaced(hp, vr.random(len(hp)), 1, 150, hidden + [ash])
    lab, nl = ndi.label(lakes)
    big = sorted(((ndi.sum(lakes, lab, i), i) for i in range(1, nl + 1)), reverse=True)[:3]
    lake_c = [tuple(np.array(ndi.center_of_mass(lakes, lab, i))[::-1]) for _, i in big]

    def centroid(mask):
        lb, nn = ndi.label(mask)
        if nn == 0:
            return None
        big = 1 + int(np.argmax(ndi.sum(mask, lb, range(1, nn + 1))))
        p = np.array(pts(lb == big)); c = p.mean(0)
        return tuple(p[np.argmin(((p - c) ** 2).sum(1))])      # a point that lies inside the region

    regions = [  # code, working label (Director's category), point, status
        ('R-01', 'Ashram Valley', ash, 'PROPOSED position'),
        ('R-02', 'Enchanted Forest', centroid(B == 4), 'PROPOSED'),
        ('R-03', 'Great Northern Range', centroid(B == 8), 'PROPOSED'),
        ('R-04', 'Western Desert & Wastelands', centroid((B == 5) | (B == 6)), 'PROPOSED'),
        ('R-05', 'Forbidden Region', crater, 'PROPOSED'),
        ('R-06', 'Southern Grasslands', centroid((B == 2) & (ny > .55)), 'PROPOSED'),
        ('R-07', 'Eastern Spine', (float(W * .80), float(H * .55)), 'PROPOSED'),
        ('R-08', 'Lake District', lake_c[0] if lake_c else None, 'PROPOSED'),
    ]
    feats = {'wcs': f'local C1 frame: 1 cell = {SC} km, origin SW corner, +X east, +Y north, Z metres; image row 0 = north',
             'ashram': ash, 'cities': cities, 'villages': villages, 'ruins': ruins, 'caves': caves, 'waterfalls': falls,
             'hidden': hidden, 'lakes': lake_c, 'regions': regions, 'crater': crater}
    json.dump(feats, open(os.path.join(DATA, 'features.json'), 'w'), indent=1, default=float)
    np.save(os.path.join(DATA, 'height_m.npy'), h); np.save(os.path.join(DATA, 'filled_m.npy'), Fh)
    np.save(os.path.join(DATA, 'accum.npy'), acc); np.save(os.path.join(DATA, 'biome.npy'), B); np.save(os.path.join(DATA, 'lakes.npy'), lakes)
    hz = np.clip(h, -200, 7000)
    Image.fromarray(((hz + 200) / 7200 * 65535).astype(np.uint16)).save(os.path.join(DATA, 'height16.png'))
    render(h, B, acc, down, lakes, riv, feats)


# ---------------------------------------------------------------------------- rendering
PAL = {0: '#123B63', 1: '#D8CB9E', 2: '#9DBB63', 3: '#3F7A3F', 4: '#2C6B5B', 5: '#D9B477', 6: '#9C8466', 7: '#8A8279',
       8: '#F1F3F6', 9: '#3B2A3F', 10: '#3C8FC0'}


def hexrgb(hx):
    hx = hx.lstrip('#'); return np.array([int(hx[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def shade(h, k=3.6):
    gy, gx = np.gradient(h * .0026 * k)
    nz = 1 / np.sqrt(gx ** 2 + gy ** 2 + 1)
    L = np.array([-.62, -.62, .48]); L /= np.linalg.norm(L)
    return np.clip((-gx * L[0] - gy * L[1] + L[2]) * nz, 0, 1)


def colour(h, B, S=2):
    hb = ndi.zoom(h, S, order=3)
    Bb = ndi.zoom(B, S, order=0)
    # smooth biome blending
    col = np.zeros(hb.shape + (3,), np.float32)
    for k, hx in PAL.items():
        m = smooth((Bb == k).astype(np.float32), 2.2 if k not in (0, 10) else .8)
        col += m[..., None] * hexrgb(hx)
    wsum = sum(smooth((Bb == k).astype(np.float32), 2.2 if k not in (0, 10) else .8) for k in PAL)
    col /= np.maximum(wsum, 1e-3)[..., None]
    land = hb > 0
    # ocean depth + coastal shallows
    dco = ndi.distance_transform_edt(~land)
    sh = np.clip(1 - dco / 26, 0, 1) ** 1.5
    deep = hexrgb('#0A2747'); shallow = hexrgb('#2F86B0')
    ocean = deep + (shallow - deep) * sh[..., None]
    col = np.where(land[..., None] | (Bb == 10)[..., None], col, ocean)
    # elevation tint (higher = cooler / lighter rock) + painterly grain
    alt = np.clip(hb / 4200, 0, 1)[..., None]
    col = col * (1 - .25 * alt) + hexrgb('#C9C4BC') * .25 * alt * (Bb != 8)[..., None] + col * .0
    g = fbm(hb.shape, 64, 3, seed=99)[..., None]
    col *= 1 + .06 * g
    s = shade(np.maximum(hb, 0))
    col = np.where(land[..., None], col * (.48 + .72 * s[..., None]), col)
    # shoreline glow
    coast = land ^ ndi.binary_erosion(land, iterations=1)
    col[coast] = col[coast] * .6 + hexrgb('#E8E0C0') * .4
    return np.clip(col, 0, 255).astype(np.uint8), hb


def contours(img_draw, hb, step, S, color, offset=(0, 0)):
    lv = np.floor(np.maximum(hb, 0) / step)
    edge = (lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))
    edge &= hb > 0
    return edge


def draw_rivers(d, acc, down, riv, S, ox=0, oy=0, crop=None, scale=None):
    sc = scale or S
    for r, c in zip(*np.nonzero(riv)):
        j = down[r * W + c]
        if j < 0:
            continue
        r2, c2 = divmod(int(j), W)
        if crop:
            x0, y0, x1, y1 = crop
            if not (x0 <= c <= x1 and y0 <= r <= y1):
                continue
        w = max(2, int(.75 * sc * math.log10(acc[r, c] / 60 + 1) * 1.7))
        d.line(((c - (crop[0] if crop else 0)) * sc + ox + sc / 2, (r - (crop[1] if crop else 0)) * sc + oy + sc / 2,
                (c2 - (crop[0] if crop else 0)) * sc + ox + sc / 2, (r2 - (crop[1] if crop else 0)) * sc + oy + sc / 2),
               fill=(88, 170, 228), width=w)


def marker(d, kind, x, y, s=1.0):
    if kind == 'city':
        d.rectangle((x - 9 * s, y - 9 * s, x + 9 * s, y + 9 * s), fill=(250, 232, 170), outline=(40, 30, 20), width=3)
        d.rectangle((x - 4 * s, y - 4 * s, x + 4 * s, y + 4 * s), fill=(150, 60, 40))
    elif kind == 'village':
        d.ellipse((x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s), fill=(250, 240, 210), outline=(40, 30, 20), width=2)
    elif kind == 'ruin':
        for k in (-6, 0, 6):
            d.rectangle((x + k * s - 2 * s, y - 8 * s, x + k * s + 2 * s, y + 6 * s), fill=(215, 205, 185), outline=(40, 30, 20))
        d.line((x - 10 * s, y + 7 * s, x + 10 * s, y + 7 * s), fill=(40, 30, 20), width=3)
    elif kind == 'cave':
        d.pieslice((x - 10 * s, y - 9 * s, x + 10 * s, y + 11 * s), 180, 360, fill=(30, 25, 25), outline=(230, 220, 200), width=2)
    elif kind == 'fall':
        d.polygon([(x, y + 10 * s), (x - 8 * s, y - 6 * s), (x + 8 * s, y - 6 * s)], fill=(160, 220, 255), outline=(20, 50, 90))
    elif kind == 'ashram':
        R = 22 * s
        pts = [(x + R * math.cos(a) * (1 if i % 2 == 0 else .45), y + R * math.sin(a) * (1 if i % 2 == 0 else .45))
               for i, a in enumerate(np.linspace(-math.pi / 2, 1.5 * math.pi, 11)[:-1])]
        d.polygon(pts, fill=(255, 200, 60), outline=(60, 25, 0), width=3)
    elif kind == 'hidden':
        R = 34 * s
        for a in range(0, 360, 20):
            d.arc((x - R, y - R, x + R, y + R), a, a + 11, fill=(255, 255, 255), width=3)
    elif kind == 'lake':
        pass


BOXES = []


def place(d, x, y, lines, avoid=True):
    """lines: [(text, size, kwargs)] stacked; tries offsets so blocks do not overlap earlier labels."""
    hs = [ln[1] * 1.35 for ln in lines]
    wmax = max(d.textlength(ln[0], font=F(FS if ln[2].get('serif') else FB, ln[1])) for ln in lines)
    tot = sum(hs)
    for dx, dy in [(0, 0), (0, -60), (0, 60), (0, -110), (0, 110), (-180, 0), (180, 0), (-180, -80), (180, 80), (0, 170)]:
        dx = min(max(dx, wmax / 2 + 12 - x), W * 2 - 12 - wmax / 2 - x)      # keep inside the map frame
        bx = (x + dx - wmax / 2 - 6, y + dy - tot / 2 - 4, x + dx + wmax / 2 + 6, y + dy + tot / 2 + 4)
        if not avoid or not any(bx[0] < b[2] and b[0] < bx[2] and bx[1] < b[3] and b[1] < bx[3] for b in BOXES):
            break
    BOXES.append(bx)
    yy = bx[1] + 4
    for (t, sz, kw), hh in zip(lines, hs):
        label(d, x + dx, yy + hh / 2, t, sz, **kw); yy += hh


def label(d, x, y, t, size=22, bold=True, color=(255, 255, 255), anchor='mm', serif=False):
    d.text((x, y), t, font=F(FS if serif else (FB if bold else FR), size), fill=color, anchor=anchor,
           stroke_width=max(2, size // 9), stroke_fill=(15, 15, 20))


def dimension_icon(kind, size=300):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = size / 2; r = np.hypot(xx - c, yy - c) / c; a = np.arctan2(yy - c, xx - c)
    img = np.zeros((size, size, 3), np.float32)
    if kind == 'blackhole':
        disk = np.exp(-((r - .62) / .13) ** 2) * (1 + .35 * np.sin(a * 3 + r * 20))
        img += disk[..., None] * hexrgb('#FFB35A') + (np.exp(-((r - .62) / .05) ** 2))[..., None] * hexrgb('#FFF2D0')
        img += np.exp(-((r - .40) / .04) ** 2)[..., None] * hexrgb('#FF8A30') * .8
        img *= (r > .36)[..., None]
        img += (np.clip(1 - r, 0, 1) ** 3 * .25)[..., None] * hexrgb('#4A6BFF') * (r > .36)[..., None]
        stars = (np.random.default_rng(3).random((size, size)) > .996)
        img[stars] = 230
    else:
        sw = np.sin(a * 2 + r * 9) * .5 + .5
        img += (np.clip(1 - r, 0, 1) ** 1.3 * (.6 + .4 * sw))[..., None] * hexrgb('#7A1424')
        img += (np.exp(-((r - .78) / .08) ** 2) * (sw > .55))[..., None] * hexrgb('#B04BFF') * .8
        img += (np.exp(-(r / .18) ** 2))[..., None] * hexrgb('#1A0610')
        img *= (r < 1)[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    mask = Image.fromarray(((r < .98) * 255).astype(np.uint8))
    out = Image.new('RGBA', (size, size)); out.paste(im, (0, 0), mask)
    return out


def render(h, B, acc, down, lakes, riv, feats):
    S = 2
    col, hb = colour(h, B, S)
    base = Image.fromarray(col)
    base.save(os.path.join(DATA, 'color_nolabels.png'))
    m = base.copy().convert('RGBA')
    ov = Image.new('RGBA', m.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # contour lines every 500 m (faint) and 1000 m (stronger)
    for step, a in ((500, 38), (1000, 70)):
        e = contours(None, hb, step, S, None)
        arr = np.zeros(hb.shape + (4,), np.uint8); arr[e] = (40, 30, 20, a)
        ov.alpha_composite(Image.fromarray(arr))
    d = ImageDraw.Draw(ov)
    draw_rivers(d, acc, down, riv, S)
    # grid 100 km
    for gx in range(0, W + 1, 100):
        d.line((gx * S, 0, gx * S, H * S), fill=(255, 255, 255, 60), width=1)
    for gy in range(0, H + 1, 100):
        d.line((0, (H - gy) * S, W * S, (H - gy) * S), fill=(255, 255, 255, 60), width=1)
    for i, gx in enumerate(range(0, W, 100)):
        label(d, (gx + 50) * S, 16, 'ABCDEFGHIJK'[i], 20)
    for j, gy in enumerate(range(0, H, 100)):
        label(d, 16, (H - gy - 50) * S, str(j + 1), 20)
    m.alpha_composite(ov)
    d = ImageDraw.Draw(m)
    P = lambda p: (p[0] * S, p[1] * S)
    for p in feats['villages']:
        marker(d, 'village', *P(p))
    for p in feats['ruins']:
        marker(d, 'ruin', *P(p))
    for p in feats['caves']:
        marker(d, 'cave', *P(p))
    for p in feats['waterfalls']:
        marker(d, 'fall', *P(p))
    for p in feats['hidden']:
        marker(d, 'hidden', *P(p), s=2.2)
    a = P(feats['ashram'])
    marker(d, 'ashram', *a, s=1.4)
    BOXES.clear()
    for p in [a] + [P(q) for q in feats['cities']]:
        BOXES.append((p[0] - 22, p[1] - 22, p[0] + 22, p[1] + 22))
    place(d, a[0] + 230, a[1], [('ASHRAM', 36, {'color': (255, 214, 90), 'serif': True}),
                                ('R-01 Ashram Valley · CONFIRMED location', 17, {}), ('position on map = PROPOSAL', 17, {})])
    for k, p in enumerate(feats['cities']):
        marker(d, 'city', *P(p), s=1.4); place(d, P(p)[0], P(p)[1] + 38, [(f'C-{k + 1:02d} city site', 20, {})])
    for code, nm, p, st in feats['regions']:
        if p is None or code == 'R-01':
            continue
        place(d, P(p)[0], P(p)[1], [(nm.upper(), 30, {'serif': True}), (f'{code} · working label · name pending', 16, {'bold': False})])
    for k, p in enumerate(feats['hidden']):
        place(d, P(p)[0], P(p)[1] - 90, [(f'H-{k + 1:02d} hidden area', 17, {})])
    for k, p in enumerate(feats['ruins']):
        place(d, P(p)[0], P(p)[1] + 26, [(f'RU-{k + 1:02d}', 15, {})])
    for k, p in enumerate(feats['caves']):
        place(d, P(p)[0], P(p)[1] + 26, [(f'CV-{k + 1:02d}', 15, {})])
    # legend panel
    PW = 820
    full = Image.new('RGBA', (m.width + PW, max(m.height + 150, 1730)), (16, 18, 24, 255))
    full.alpha_composite(m, (0, 150))
    d = ImageDraw.Draw(full)
    d.rectangle((0, 0, full.width, 146), fill=(12, 13, 18)); d.rectangle((0, 142, full.width, 146), fill=(214, 166, 60))
    d.text((40, 22), 'HIMAVANT — HOME CONTINENT (C1)', font=F(FS, 64), fill=(240, 230, 205))
    d.text((40, 100), f'Detailed map of continent C1 of the main world (see map_v2 atlas)  ·  ≈ {int(1024 * SC)} x {int(768 * SC)} km (estimate)  ·  names = working labels, pending approval',
           font=F(FR, 24), fill=(170, 170, 180))
    d.text((full.width - 40, 40), 'NOT LOCKED — awaiting Director approval', font=F(FB, 28), fill=(255, 190, 70), anchor='ra')
    x0 = m.width + 40; y = 190
    d.text((x0, y), 'LEGEND', font=F(FB, 30), fill=(240, 230, 205)); y += 50
    for k, nm in ((2, 'Grassland'), (3, 'Forest'), (4, 'Enchanted forest (proposal)'), (5, 'Desert'), (6, 'Wasteland'),
                  (7, 'High rock'), (8, 'Snow / glacier'), (9, 'Forbidden zone (proposal)'), (10, 'Lake'), (0, 'Sea')):
        d.rectangle((x0, y, x0 + 40, y + 26), fill=tuple(int(v) for v in hexrgb(PAL[k])), outline=(0, 0, 0))
        d.text((x0 + 56, y), nm, font=F(FR, 22), fill=(220, 220, 225)); y += 36
    y += 10
    for kind, nm in (('ashram', 'Confirmed location (position proposed)'), ('city', 'Ancient city site'), ('village', 'Village / settlement'),
                     ('ruin', 'Ancient ruins'), ('cave', 'Cave entrance'), ('fall', 'Waterfall'), ('hidden', 'Hidden area')):
        marker(d, kind, x0 + 20, y + 14, .9 if kind != 'hidden' else .7)
        d.text((x0 + 56, y), nm, font=F(FR, 22), fill=(220, 220, 225)); y += 40
    d.line((x0, y + 12, x0 + 40, y + 12), fill=(70, 150, 210), width=5); d.text((x0 + 56, y), 'River (width = flow)', font=F(FR, 22), fill=(220, 220, 225)); y += 40
    d.text((x0, y), 'Contours every 500 m (bold 1000 m)', font=F(FR, 20), fill=(160, 160, 170)); y += 46
    # scale bar
    d.text((x0, y), 'SCALE', font=F(FB, 24), fill=(240, 230, 205)); y += 36
    for i in range(4):
        d.rectangle((x0 + i * 100 * S / 2 * 1, y, x0 + (i + 1) * 100 * S / 2, y + 16), fill=(240, 240, 240) if i % 2 == 0 else (40, 40, 40), outline=(240, 240, 240))
    for i in range(5):
        d.text((x0 + i * 100, y + 22), f'{int(i * 50 * SC)} km', font=F(FR, 18), fill=(200, 200, 200), anchor='ma')
    y += 60
    d.text((x0, y), f'Grid square = {int(100 * SC)} km · local origin = SW corner (A1)', font=F(FR, 19), fill=(160, 160, 170)); y += 50
    # compass
    cx, cy = full.width - 110, y - 120
    d.polygon([(cx, cy - 60), (cx - 16, cy), (cx + 16, cy)], fill=(240, 230, 205)); d.polygon([(cx, cy + 60), (cx - 16, cy), (cx + 16, cy)], fill=(90, 90, 100))
    d.text((cx, cy - 92), 'N', font=F(FB, 28), fill=(240, 230, 205), anchor='ma')
    # dimensions
    d.text((x0, y), 'SEPARATE DIMENSIONS (not on the physical map)', font=F(FB, 24), fill=(240, 230, 205)); y += 44
    for kind, t, s1 in (('blackhole', 'Black Hole Training Dimension', 'CONFIRMED location · look = PROPOSAL'),
                        ('dark', "Saithan's Dark World", 'CONFIRMED location · look = PROPOSAL')):
        full.alpha_composite(dimension_icon(kind, 170), (x0, y))
        d.text((x0 + 190, y + 40), t, font=F(FB, 24), fill=(255, 255, 255))
        d.text((x0 + 190, y + 76), s1, font=F(FR, 19), fill=(170, 170, 180))
        d.text((x0 + 190, y + 104), 'Reached via magical portal — portal', font=F(FR, 19), fill=(170, 170, 180))
        d.text((x0 + 190, y + 128), 'locations NOT CONFIRMED', font=F(FR, 19), fill=(170, 170, 180))
        y += 190
    d.text((x0, y), 'GEM LOCATION', font=F(FB, 24), fill=(120, 255, 200)); y += 34
    d.text((x0, y), 'CONFIRMED location · position NOT CONFIRMED', font=F(FR, 19), fill=(170, 170, 180)); y += 26
    d.text((x0, y), '→ not placed on the map until the story says where', font=F(FR, 19), fill=(170, 170, 180)); y += 44
    d.text((x0, y), 'Roads / paths: not drawn (none approved yet)', font=F(FR, 19), fill=(170, 170, 180)); y += 28
    d.text((x0, y), 'Rivers, lakes, ranges: geographic PROPOSAL', font=F(FR, 19), fill=(170, 170, 180))
    full.convert('RGB').save(os.path.join(OUT, 'WORLD_MAP_master_v1.png'), optimize=True)
    print('wrote master map', full.size)
    # elevation / hydrology reference
    e = np.clip(np.maximum(hb, 0) / 6000, 0, 1)
    ramp = np.stack([e * 255, (1 - abs(e - .4)) * 200, (1 - e) * 120], -1)
    ramp = np.where((hb <= 0)[..., None], np.array([10, 25, 50]), ramp) * (.55 + .45 * shade(np.maximum(hb, 0))[..., None])
    er = Image.fromarray(np.clip(ramp, 0, 255).astype(np.uint8)).convert('RGBA')
    dd = ImageDraw.Draw(er); draw_rivers(dd, acc, down, riv, S)
    dd.text((30, 20), 'ELEVATION + HYDROLOGY reference  ·  sea 0 m → peaks %d m  ·  rivers from flow accumulation' % int(h.max()),
            font=F(FB, 28), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    er.convert('RGB').save(os.path.join(OUT, 'WORLD_MAP_elevation_v1.png'), optimize=True)
    regional(base, h, acc, down, riv, feats)


def regional(base, h, acc, down, riv, feats):
    """6 regional maps: 240 x 240 km crops, contours every 100 m, local 25 km grid + scale bar."""
    R = 240; Z = 3; cell = R * Z
    picks = [r for r in feats['regions'] if r[2] is not None][:6]
    sheet = Image.new('RGB', (3 * (cell + 40) + 40, 2 * (cell + 110) + 150), (16, 18, 24))
    d0 = ImageDraw.Draw(sheet)
    d0.text((40, 30), f'REGIONAL MAPS (C1 HIMAVANT)  ·  each panel {int(240 * SC)} x {int(240 * SC)} km  ·  contours 100 m', font=F(FS, 40), fill=(240, 230, 205))
    for k, (code, nm, p, st) in enumerate(picks):
        cx, cy = int(np.clip(p[0], R / 2, W - R / 2)), int(np.clip(p[1], R / 2, H - R / 2))
        x0, y0 = cx - R // 2, cy - R // 2
        crop = base.crop((x0 * 2, y0 * 2, (x0 + R) * 2, (y0 + R) * 2)).resize((cell, cell), Image.LANCZOS).convert('RGBA')
        hb = ndi.zoom(h[y0:y0 + R, x0:x0 + R], Z, order=3)
        lv = np.floor(np.maximum(hb, 0) / 100); e = ((lv != np.roll(lv, 1, 0)) | (lv != np.roll(lv, 1, 1))) & (hb > 0)
        arr = np.zeros(hb.shape + (4,), np.uint8); arr[e] = (30, 20, 10, 70)
        crop.alpha_composite(Image.fromarray(arr))
        d = ImageDraw.Draw(crop)
        draw_rivers(d, acc, down, riv, Z, crop=(x0, y0, x0 + R - 1, y0 + R - 1), scale=Z)
        for g in range(0, R + 1, 25):
            d.line((g * Z, 0, g * Z, cell), fill=(255, 255, 255, 50)); d.line((0, g * Z, cell, g * Z), fill=(255, 255, 255, 50))
        for kind, key in (('village', 'villages'), ('ruin', 'ruins'), ('cave', 'caves'), ('fall', 'waterfalls'), ('city', 'cities')):
            for q in feats[key]:
                if x0 <= q[0] < x0 + R and y0 <= q[1] < y0 + R:
                    marker(d, kind, (q[0] - x0) * Z, (q[1] - y0) * Z, 1.2)
        q = feats['ashram']
        if x0 <= q[0] < x0 + R and y0 <= q[1] < y0 + R:
            marker(d, 'ashram', (q[0] - x0) * Z, (q[1] - y0) * Z, 1.4)
        d.rectangle((20, cell - 50, 20 + 50 * Z, cell - 38), fill=(255, 255, 255)); d.text((20, cell - 34), f'{int(50 * SC)} km', font=F(FB, 18), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        hmax, hmin = int(h[y0:y0 + R, x0:x0 + R].max()), int(max(0, h[y0:y0 + R, x0:x0 + R].min()))
        col, row = k % 3, k // 3
        px, py = 40 + col * (cell + 40), 120 + row * (cell + 110)
        sheet.paste(crop.convert('RGB'), (px, py))
        gxl = 'ABCDEFGHIJK'[int(cx // 100)]; gyl = int((H - cy) // 100) + 1
        d0.text((px, py + cell + 10), f'{code}  {nm}', font=F(FB, 26), fill=(255, 214, 90) if code == 'R-01' else (240, 230, 205))
        d0.text((px, py + cell + 46), f'{st} · grid {gxl}{gyl} · centre ({int(cx * SC)}, {int((H - cy) * SC)}) km local · elev {hmin}–{hmax} m', font=F(FR, 18), fill=(170, 170, 180))
    sheet.save(os.path.join(OUT, 'WORLD_MAP_regional_v1.png'), optimize=True)
    print('wrote regional sheet')


if __name__ == '__main__':
    main()

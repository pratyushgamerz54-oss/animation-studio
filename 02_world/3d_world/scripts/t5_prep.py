"""TASK 05 · STEP 1 — detailed terrain data for the Ashram Valley, its surroundings, the first mountain region (snowy range
≈100 km NW) and the first forest region (northern forest belt). python3 + numpy + scipy + numba (NOT Blender).

Approved geography is kept exactly:
  z = z_v001(x, y)                                  ← t5_field.height (verbatim TASK 04 function, verified below)
    + DETAIL(x, y) · border_weight                  ← new detail only: ridges, micro relief, erosion (faded to 0 at tile edges)
  → rivers carved from the SAME v001 river network (same water levels) → lake (map lake, spill level) → Ashram pad → path.
Tiles (local metres, origin = proposed Ashram position, +X east, +Y north, Z = m a.s.l.):
  VH  valley hero    ±1.2 km  @ 2 m    Ashram surroundings, river, ground-level shots
  FH  forest hero    3 × 3 km @ 2 m    edge of the northern forest belt where the river enters it (forest floor shots)
  L0  valley near    ±6 km    @ 10 m
  L1  valley         ±32 km   @ 40 m   valley + forest belts
  MT  mountain NW    60 × 60 km @ 30 m first mountain region = the snowy range face nearest the Ashram (≈100 km NW)
  L2  horizon        ±160 km  @ 400 m  everything else in the window (great range, lake at the SW edge)
Writes 08_ASHRAM_VALLEY/data_v002/<tile>.npz (+ water.npz, prep_v002.json). Heightfields are turned into 32-bit EXR images
by the Blender build script.  Usage: python3 t5_prep.py [tile ...]   (default: all)
"""
import os, sys, json, math, time
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t5_field as F
import t5_erosion as E
import t5_noise as N

ROOT = os.path.abspath(os.path.join(HERE, '..'))
V1 = os.path.join(ROOT, '08_ASHRAM_VALLEY', 'data')
OUT = os.path.join(ROOT, '08_ASHRAM_VALLEY', 'data_v002'); os.makedirs(OUT, exist_ok=True)
D1 = np.load(os.path.join(V1, 'valley_prep.npz'))
MET1 = json.load(open(os.path.join(V1, 'valley_features.json')))
SITE = F.SITE_Z
sstep, fbm, ridged = F.sstep, F.fbm, F.ridged

TILES = {
    'VH': dict(x0=-1200, x1=1200, y0=-1200, y1=1200, sp=2.0, kind='hero', band=150, holes=[]),
    'FH': dict(x0=-1520, x1=1480, y0=24000, y1=27000, sp=2.0, kind='hero', band=150, holes=[]),   # edges on the 40 m L1 grid
    'L0': dict(x0=-6000, x1=6000, y0=-6000, y1=6000, sp=10.0, kind='valley', band=500, holes=['VH']),
    'L1': dict(x0=-32000, x1=32000, y0=-32000, y1=32000, sp=40.0, kind='valley', band=1500, holes=['L0', 'FH']),
    'MT': dict(x0=-116000, x1=-56000, y0=44000, y1=104000, sp=30.0, kind='mountain', band=2500, holes=['WF']),
    'L2': dict(x0=-160000, x1=160000, y0=-160000, y1=160000, sp=400.0, kind='horizon', band=6000, holes=['L1', 'MT']),
}


def grid(t):
    nx = int(round((t['x1'] - t['x0']) / t['sp'])) + 1; ny = int(round((t['y1'] - t['y0']) / t['sp'])) + 1
    gx = np.linspace(t['x0'], t['x1'], nx); gy = np.linspace(t['y1'], t['y0'], ny)       # row 0 = north
    X, Y = np.meshgrid(gx, gy)
    return X, Y


def rect_dist(X, Y, r):
    """distance from points to the OUTSIDE of rect r (0 inside)."""
    dx = np.maximum(np.maximum(r['x0'] - X, X - r['x1']), 0); dy = np.maximum(np.maximum(r['y0'] - Y, Y - r['y1']), 0)
    return np.hypot(dx, dy)


def border_weight(X, Y, t):
    w = sstep(0, t['band'], np.minimum.reduce([X - t['x0'], t['x1'] - X, Y - t['y0'], t['y1'] - Y]))
    for h in t['holes']:
        w = w * sstep(0, t['band'], rect_dist(X, Y, TILES[h]))
    return w


def bl(sp, wavelength):
    """band-limit: only detail whose wavelength is ≥ 3 grid cells is added (no aliasing / shimmering)."""
    return 1.0 if wavelength >= 3 * sp else 0.0


# ------------------------------------------------------------------ approved height + better mountain detail
def height_t5(x, y):
    """v001 height, but the two blockout RIDGE terms (mountains only, factor m) are re-synthesised with isotropic
    gradient noise + domain warp (same scales, same amplitude, same mean) → no square lattice artefacts.
    Map-derived base heights, valley terms, rivers' positions: identical to v001. Where m = 0 (the whole valley) the
    result IS the v001 height (verified)."""
    x = np.asarray(x, np.float64); y = np.asarray(y, np.float64)
    z = F.height(x, y)
    hb = F.base_h(x, y); m = sstep(1300, 3200, hb)
    k = m > 0
    if k.any():
        xk, yk, mk = x[k], y[k], m[k]
        vf = 1 - .45 * np.exp(-(np.hypot(xk, yk) / 9000.0) ** 2)
        old = (F.ridged(xk, yk, 5200, 5, 2) * 1500 * mk ** 1.3 + F.ridged(xk, yk, 1600, 3, 3) * 260 * mk) * vf
        wx, wy = N.warp(xk, yk, 9000, 2200, 5)
        new = (N.ridged(wx, wy, 5200, 5, 2) * 1500 * mk ** 1.3 + N.ridged(wx, wy, 1600, 3, 3) * 260 * mk) * vf
        z = z.copy(); z[k] = z[k] - old + new
    return z


# ------------------------------------------------------------------ rivers (v001 network; levels re-derived on height_t5)
RP, RO = D1['RP'].astype(np.float64), D1['RO']
RIVERS = [RP[RO[i]:RO[i + 1]].copy() for i in range(len(RO) - 1)]
_RZ1 = [r[:, 2].copy() for r in RIVERS]
for i, r in enumerate(RIVERS):                                     # gentle meanders in the MOUNTAIN reaches only (v001 suppressed
    s_ = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(r[:, :2], axis=0).T))])   # them there → dead-straight gorges)
    tg = np.gradient(r[:, :2], axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1, keepdims=True), 1e-9)
    tg = np.stack([ndi.gaussian_filter1d(tg[:, 0], 8), ndi.gaussian_filter1d(tg[:, 1], 8)], 1)
    tg /= np.maximum(np.linalg.norm(tg, axis=1, keepdims=True), 1e-9)
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    mf = sstep(1100, 2400, F.base_h(r[:, 0], r[:, 1]))
    env = np.clip(s_ / 1500, 0, 1) * np.clip((s_[-1] - s_) / 1500, 0, 1)
    off = (N.fbm(s_, np.full_like(s_, i * 7.31), 900.0, 3, 150) * 42 + N.fbm(s_, np.full_like(s_, i * 3.1), 220.0, 2, 151) * 9) * mf * env
    r[:, :2] = r[:, :2] + nr * off[:, None]
for r in RIVERS:                                                   # same rule as v001: water never flows uphill
    r[:, 2] = np.minimum.accumulate(np.maximum(height_t5(r[:, 0], r[:, 1]), 0.0))
_allp = np.concatenate([r[:, :2] for r in RIVERS]); _allz = np.concatenate([r[:, 2] for r in RIVERS])
_own = np.concatenate([np.full(len(r), i) for i, r in enumerate(RIVERS)]); _tr = cKDTree(_allp)
for i, r in enumerate(RIVERS):                                     # tributary mouths meet the main river's level (v001 rule)
    d, j = _tr.query(r[-1, :2], k=8)
    for dd, jj in zip(np.atleast_1d(d), np.atleast_1d(j)):
        if _own[jj] != i and dd < 300:
            r[-1, 2] = min(r[-1, 2], _allz[jj]); break
_ch = np.concatenate([np.abs(r[:, 2] - z1) for r, z1 in zip(RIVERS, _RZ1)])
_inL1 = (np.abs(_allp[:, 0]) < 32000) & (np.abs(_allp[:, 1]) < 32000)
RIVER_LEVEL_CHANGE = dict(max_all_m=float(_ch.max()), max_in_valley_L1_m=float(_ch[_inL1].max()) if _inL1.any() else 0.0)


# ------------------------------------------------------------------ featured waterfall (largest cascade inside MT) + its hero tile
def _drops():
    out = []
    for i, r in enumerate(RIVERS):
        z = r[:, 2]
        for k in range(len(r) - 2):
            if z[k] - z[k + 2] >= 12:
                out.append((i, k, z[k] - z[k + 2]))
    return out


_mt = TILES['MT']
_cand = [(i, k, d) for i, k, d in _drops() if _mt['x0'] + 6000 < RIVERS[i][k, 0] < _mt['x1'] - 6000
         and _mt['y0'] + 6000 < RIVERS[i][k, 1] < _mt['y1'] - 6000]
_main = max(_cand, key=lambda c: c[2])
# second fall upstream on the same river within ~250 m (if any) → a two-step cascade
_up = [c for c in _cand if c[0] == _main[0] and 3 <= _main[1] - c[1] <= 10 and c[2] >= 25]
FEATURED = [dict(river=int(_main[0]), k=int(_main[1]), drop_m=float(_main[2]))] + \
           [dict(river=int(c[0]), k=int(c[1]), drop_m=float(c[2])) for c in _up[:1]]
# snap the tile to the MT grid lines (x = x0 + i·30, y = y1 − j·30) so the MT hole edges coincide with the WF border
_cx = _mt['x0'] + round((np.mean([RIVERS[f['river']][f['k'], 0] for f in FEATURED]) - _mt['x0']) / 30) * 30
_cy = _mt['y1'] - round((_mt['y1'] - np.mean([RIVERS[f['river']][f['k'], 1] for f in FEATURED])) / 30) * 30
TILES['WF'] = dict(x0=_cx - 450, x1=_cx + 450, y0=_cy - 450, y1=_cy + 450, sp=1.5, kind='wf', band=120, holes=[])
for f in FEATURED:
    r = RIVERS[f['river']]; k = f['k']
    f.update(x=float(r[k, 0]), y=float(r[k, 1]), z_top=float(r[k, 2]), z_bottom=float(r[k + 2, 2]), width_m=float(r[k, 3]),
             lip_x=float(r[k + 1, 0]), lip_y=float(r[k + 1, 1]), out_x=float(r[k + 2, 0]), out_y=float(r[k + 2, 1]))


def lip_profile(ri, a, ss, s, z):
    """vertical waterfall lip for featured falls (only used at ≤ 5 m resolution): hold the upper level until the lip,
    drop within 3 m, then continue at the lower level → a real fall instead of a steep chute."""
    for f in FEATURED:
        if f['river'] != ri:
            continue
        k = f['k'] - a
        if k < 0 or k + 2 >= len(s):
            continue
        s_lip = s[k + 1]; zt, zb = z[k], z[k + 2]
        m1 = (ss >= s[k]) & (ss < s_lip); m2 = (ss >= s_lip) & (ss < s_lip + 3); m3 = (ss >= s_lip + 3) & (ss <= s[k + 2])
        z_ = np.interp(ss, s, z)
        z_[m1] = zt; z_[m2] = zt + (zb - zt) * (ss[m2] - s_lip) / 3; z_[m3] = zb
        yield z_


def river_samples(t, step):
    """river points (x, y, z_water, width) resampled with a cubic spline at `step` m, only near tile t."""
    m = 400 + 3 * 140
    out = []
    for r in RIVERS:
        inb = (r[:, 0] > t['x0'] - m) & (r[:, 0] < t['x1'] + m) & (r[:, 1] > t['y0'] - m) & (r[:, 1] < t['y1'] + m)
        if inb.sum() < 2:
            continue
        idx = np.nonzero(inb)[0]; a, b = max(idx.min() - 2, 0), min(idx.max() + 3, len(r))
        rr = r[a:b]
        s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(rr[:, :2], axis=0).T))])
        if len(rr) < 4 or s[-1] < 1:
            continue
        ss = np.arange(0, s[-1], step)
        cx, cy = CubicSpline(s, rr[:, 0]), CubicSpline(s, rr[:, 1])
        zz = np.interp(ss, s, rr[:, 2])
        if step <= 5:
            for z_ in lip_profile(_ri(r), a, ss, s, rr[:, 2]):
                zz = np.minimum(zz, z_)
        out.append(np.column_stack([cx(ss), cy(ss), zz, np.interp(ss, s, rr[:, 3])]))
    return np.concatenate(out) if out else np.zeros((0, 4))


def _ri(r):
    for i, q in enumerate(RIVERS):
        if q is r:
            return i
    return -1


# ------------------------------------------------------------------ the map lake inside the window (SW edge)
LAB, NL = ndi.label(F.ol)
LAKES = []
for k in range(1, NL + 1):
    rr_, cc_ = np.nonzero(LAB == k)
    lx, ly = F.to_local(cc_, rr_)
    if np.any((np.abs(lx) < 165000) & (np.abs(ly) < 165000)):
        LAKES.append(dict(id=int(k), level=float(np.median(F.oF[rr_, cc_])), cells=int(len(rr_)),
                          bbox=[float(lx.min() - 6000), float(lx.max() + 6000), float(ly.min() - 6000), float(ly.max() + 6000)]))
LAKE_S = ndi.gaussian_filter(np.isin(LAB, [l['id'] for l in LAKES]).astype(np.float64), .7)
LAKE_LEVEL = np.zeros_like(F.oF)
for l in LAKES:
    LAKE_LEVEL[ndi.binary_dilation(LAB == l['id'], iterations=3)] = l['level']


def lake_field(X, Y):
    c, r = F.to_cell(X, Y)
    m = ndi.map_coordinates(LAKE_S, [r, c], order=1, mode='constant')
    lev = ndi.map_coordinates(LAKE_LEVEL, [r, c], order=0, mode='constant')
    return m, lev


# ------------------------------------------------------------------ path (PROPOSED, v001)
PATH = D1['PATH'].astype(np.float64)


def path_dist(X, Y):
    s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(PATH[:, :2], axis=0).T))])
    ss = np.arange(0, s[-1], 1.0)
    P = np.column_stack([np.interp(ss, s, PATH[:, 0]), np.interp(ss, s, PATH[:, 1])])
    d, _ = cKDTree(P).query(np.column_stack([X.ravel(), Y.ravel()]), distance_upper_bound=60)
    return d.reshape(X.shape)


# ------------------------------------------------------------------ detail per tile kind
def detail(X, Y, z0, t):
    sp = t['sp']; hb = F.base_h(X.ravel(), Y.ravel()).reshape(X.shape)
    m = sstep(1300, 3200, hb); hill = sstep(800, 1600, hb)
    d = np.zeros_like(z0)
    if t['kind'] in ('hero', 'valley'):
        # micro relief of the green valley floor: low mounds, swales, small ground undulation (metres)
        for wl, amp, s in ((220, 2.2, 101), (60, .7, 102), (18, .24, 103), (6, .07, 104)):
            d += bl(sp, wl) * fbm(X, Y, wl, 2, s) * amp * (.6 + .8 * hill)
    if t['kind'] == 'wf':
        # bedrock micro relief around the fall: blocky ribs + small ledges (faded at the tile border)
        d += N.ridged(X, Y, 28, 3, 140) * 2.2 + N.fbm(X, Y, 7, 3, 141) * .35 + N.fbm(X, Y, 90, 2, 142) * 3.0
    if t['kind'] in ('mountain', 'horizon'):
        # finer ridges / spurs / ribs on the ranges (v001 stopped at 1.6 km), isotropic + warped
        k = m > 0
        if k.any():
            wx, wy = N.warp(X[k], Y[k], 2500, 450, 9)
            dk = np.zeros(k.sum())
            for wl, amp, s in ((900, 170, 112), (300, 55, 113), (100, 12, 114)):
                dk += bl(sp, wl) * N.ridged(wx, wy, wl, 3, s) * amp * m[k] ** 1.2
            d[k] += dk
        d += bl(sp, 140) * N.fbm(X, Y, 140, 3, 115) * 8 * (.3 + hill)
    return d


def strata(z, slope_deg, h=38.0, k=.45):
    """rock layering on steep faces: ledges every ~h m (only where the slope is cliff-like)."""
    t = z / h; fr = t - np.floor(t)
    zt = (np.floor(t) + sstep(.72, 1.0, fr)) * h
    return (zt - z) * k * sstep(38, 52, slope_deg)


def slope_of(z, sp, smooth_m=0.0):
    zz = ndi.gaussian_filter(z, smooth_m / sp) if smooth_m > sp else z
    gy, gx = np.gradient(zz, sp)
    return np.degrees(np.arctan(np.hypot(gx, gy)))


EROSION = {   # (downsample, drops per cell, radius, erode, deposit) passes; thermal talus (deg)
    'mountain': dict(passes=[(4, 1.5, 2, .3, .2), (1, 1.0, 3, .3, .3)], talus=50, cap=4.0),
    'horizon': dict(passes=[(1, 1.5, 2, .3, .3)], talus=45, cap=4.0),
    'valley': dict(passes=[(1, .45, 2, .12, .3)], talus=40, cap=2.0),
    'hero': dict(passes=[], talus=None, cap=0),
    'wf': dict(passes=[], talus=None, cap=0),
}


def erode(z, sp, kind, seed):
    cfg = EROSION[kind]
    flow = np.zeros_like(z); scree = np.zeros_like(z); z = z.copy()
    for k, (ds, dpc, rad, er, dep) in enumerate(cfg['passes']):
        if ds > 1:
            zc = z[::ds, ::ds]
            H, fl = E.hydraulic(zc / (sp * ds), dpc * zc.size, seed + k, rad, erode=er, deposit=dep, capacity=cfg['cap'])
            dz = ndi.gaussian_filter(H * sp * ds - zc, 1.0)
            dz = ndi.zoom(dz, ds, order=3)[:z.shape[0], :z.shape[1]]
            pad = [(0, z.shape[0] - dz.shape[0]), (0, z.shape[1] - dz.shape[1])]
            z = z + np.pad(dz, pad, mode='edge')
            flow += np.pad(ndi.zoom(fl, ds, order=1)[:z.shape[0], :z.shape[1]], pad, mode='edge') / ds
        else:
            H, fl = E.hydraulic(z / sp, dpc * z.size, seed + k, rad, erode=er, deposit=dep, capacity=cfg['cap'])
            z = z + ndi.gaussian_filter(H * sp - z, 1.0); flow += fl     # light blur removes droplet pits
    if cfg['talus']:
        H, dep = E.thermal(z / sp, math.tan(math.radians(cfg['talus'])), 25, .25)
        z = H * sp; scree = dep * sp
    return z, flow, scree


def build(name):
    t0 = time.time(); t = TILES[name]; sp = t['sp']
    X, Y = grid(t); n, m = X.shape
    x, y = X.ravel(), Y.ravel()
    if t['kind'] == 'wf':                                                # base = the MT tile's eroded surface (bicubic)
        M = np.load(os.path.join(OUT, 'MT.npz')); zm = M['zpre'].astype(np.float64); mt = TILES['MT']
        cc = (X - mt['x0']) / mt['sp']; rr = (mt['y1'] - Y) / mt['sp']
        z0 = ndi.map_coordinates(zm, [rr.ravel(), cc.ravel()], order=3, mode='nearest').reshape(n, m)
    else:
        z0 = height_t5(x, y).reshape(n, m)                               # ← approved v001 terrain (+ isotropic ridges)
    zd = z0 + detail(X, Y, z0, t)
    if t['kind'] == 'mountain':
        zd = zd + strata(zd, slope_of(zd, sp))
    ze, flow, scree = erode(zd, sp, t['kind'], 17 + list(TILES).index(name))
    W = border_weight(X, Y, t)
    delta = (ze - z0) * W
    z = z0 + delta
    flow = flow * W; scree = scree * W
    zpre = z.copy()
    # ---------------- rivers (v001 network + levels)
    R = river_samples(t, min(25.0, max(sp, 2.0)))
    wet = np.zeros_like(z); grav = np.zeros_like(z); dist_r = np.full(z.shape, np.inf)
    if len(R):
        d, j = cKDTree(R[:, :2]).query(np.column_stack([x, y]), distance_upper_bound=4000)
        ok = np.isfinite(d); jj = np.where(ok, j, 0)
        d = d.reshape(n, m); ok = ok.reshape(n, m); jj = jj.reshape(n, m)
        w = R[jj, 3]; zr = R[jj, 2]
        far = sp >= 400
        if sp <= 10:                                                    # natural, irregular banks at fine resolution
            d = d + (fbm(X, Y, 45, 3, 120) * .22 + fbm(X, Y, 9, 2, 121) * .06) * w * ok
        bank = np.maximum(3 * w, (.6 if far else 1.6) * sp)
        depth = 1.2 + w / 22
        ri = np.maximum(w / 2, (.35 if far else .75) * sp)
        inner = ok & (d < ri)
        z_in = (zr - .4 - depth) + depth * (np.clip(d, 0, None) / ri) ** 2
        if sp <= 10:                                                    # bed roughness (stones / pools)
            z_in = z_in + fbm(X, Y, 7, 2, 122) * .18 * (d / ri)
        if t['kind'] == 'wf':                                           # plunge pools at the foot of each fall
            for f in FEATURED:
                dp = np.hypot(X - f['out_x'], Y - f['out_y'])
                pool = (1 - sstep(4, 22, dp)) * 4.5
                z_in = z_in - pool * inner
                z = np.where(dp < 26, np.minimum(z, f['z_bottom'] - .4 + (z - f['z_bottom']) * sstep(10, 26, dp)), z)
        z = np.where(inner, np.minimum(z, z_in), z)
        mid = ok & (d >= ri) & (d < ri + bank)
        tb = np.clip((d - ri) / bank, 0, 1) ** 1.6
        z = np.where(mid & (z > zr), zr + tb * (z - zr), z)
        near = ok & (d >= ri) & (d < ri + .5 * bank)
        z = np.where(near, np.maximum(z, zr - .2), z)                   # banks never below the water surface
        wet = np.where(ok, 1 - sstep(ri * (.5 if far else 1), ri + bank * (.15 if far else .6), d), 0)
        grav = np.where(ok, sstep(ri * .7, ri * .95, d) * (1 - sstep(ri + .15 * bank, ri + .45 * bank, d)), 0) \
            * sstep(-.1, .35, fbm(X, Y, 80, 2, 123))                    # gravel bars / stony banks, patchy
        dist_r = np.where(ok, d, np.inf)
    # ---------------- lake (map lake at its spill level)
    lk, lev = lake_field(x, y); lk = lk.reshape(n, m); lev = lev.reshape(n, m)
    inside = sstep(.35, .65, lk)
    z = np.where(inside > 0, np.minimum(z, lev - inside * 30 - .5), z)
    # ---------------- Ashram pad (v001) + proposed path
    pw = F.pad_w(x, y).reshape(n, m)
    z = z * (1 - pw) + SITE * pw
    pth = np.zeros_like(z)
    if t['kind'] in ('hero', 'valley'):
        pd = path_dist(X, Y)
        pth = 1 - sstep(1.3, 2.6 + sp * .5, pd)
        z = z - .06 * pth * (sp <= 10)
    # ---------------- masks (v001 formulas + new detail masks)
    slope = slope_of(z, sp, 12.0)
    forest, rock, snow, dry, b = F.biome_masks(x, y, z.ravel(), slope.ravel())
    forest, rock, snow, dry = (a.reshape(n, m) for a in (forest, rock, snow, dry))
    if sp <= 10:                                                        # finer, natural forest edges + small clearings
        ns = fbm(X, Y, 140, 3, 130) * .25 + fbm(X, Y, 35, 2, 131) * .1
        forest = forest * sstep(.15, .5, forest + ns) * (1 - .9 * sstep(.38, .5, fbm(X, Y, 260, 3, 132)))
    clear = sstep(650, 1100, np.hypot(X, Y + 40))
    forest = forest * clear * (1 - wet) * (1 - pw)
    gn = fbm(X, Y, 1800, 4, 40) + fbm(X, Y, 400, 2, 41) * .35
    grove = sstep(.18, .42, gn) * (1 - forest) * (1 - rock) * (1 - snow) * (1 - dry) * clear * (1 - wet) * (1 - pw) * (1 - sstep(2400, 2900, z))
    padc = sstep(.93, .995, pw)
    # snow: more in gullies / couloirs and on gentle ground, less on cliffs (accumulation)
    lf = np.log1p(flow) / max(np.log1p(flow).max(), 1e-9) if flow.max() > 0 else flow
    snowline = 3850 + fbm(X, Y, 3000, 3, 34) * 250
    snow = np.clip(snow + .5 * lf * sstep(snowline - 600, snowline, z) * (1 - sstep(45, 60, slope)), 0, 1)
    sc = np.clip(scree / max(np.percentile(scree[scree > 0], 95) if (scree > 0).any() else 1, 1e-6), 0, 1) * (1 - snow)
    cliff = sstep(42, 58, slope_of(z, sp))
    rock = np.maximum(rock, cliff)
    rock = rock * (1 - inside)
    U = lambda a: np.clip(np.round(a * 255), 0, 255).astype(np.uint8)
    MA = np.stack([U(forest), U(rock), U(snow), U(wet)], -1)
    MB = np.stack([U(dry), U(padc), U(grove), U(sc)], -1)
    MC = np.stack([U(grav), U(pth), U(lf), U(cliff)], -1)
    np.savez_compressed(os.path.join(OUT, f'{name}.npz'), z=z.astype(np.float32), MA=MA, MB=MB, MC=MC,
                        rect=np.array([t['x0'], t['x1'], t['y0'], t['y1'], sp]),
                        **({'zpre': zpre.astype(np.float32)} if name == 'MT' else {}))
    st = dict(tile=name, shape=[n, m], spacing_m=sp, rect_m=[t['x0'], t['x1'], t['y0'], t['y1']], holes=t['holes'],
              z_min=float(z.min()), z_max=float(z.max()), detail_max_abs_m=float(np.abs(delta).max()),
              detail_rms_m=float(np.sqrt((delta ** 2).mean())), border_delta_max_m=float(np.abs(np.concatenate(
                  [delta[0], delta[-1], delta[:, 0], delta[:, -1]])).max()),
              cover={k: float((v > 127).mean()) for k, v in (('forest', MA[..., 0]), ('rock', MA[..., 1]), ('snow', MA[..., 2]),
                                                              ('wet', MA[..., 3]), ('grove', MB[..., 2]), ('scree', MB[..., 3]))},
              seconds=round(time.time() - t0, 1))
    print(json.dumps(st), flush=True)
    return st


def waterfalls():
    """steep drops along the v001 river profiles (water level falls ≥ 12 m within ≤ 50 m) = waterfall sites (terrain-derived)."""
    out = []
    for i, r in enumerate(RIVERS):
        z = r[:, 2]
        for k in range(len(r) - 2):
            drop = z[k] - z[k + 2]
            if drop >= 12 and (not out or out[-1]['river'] != i or k - out[-1]['k'] > 6):
                out.append(dict(river=i, k=int(k), x=float(r[k, 0]), y=float(r[k, 1]), z_top=float(z[k]), z_bottom=float(z[k + 2]),
                                width_m=float(r[k, 3]), dir=[float(r[k + 2, 0] - r[k, 0]), float(r[k + 2, 1] - r[k, 1])]))
    return out


def verify_v001():
    """the copied function must reproduce the v001 LOD0 heights wherever v001 did not carve rivers / flatten the pad."""
    z1 = D1['LOD0_z'].astype(np.float64); n = z1.shape[0]
    g = np.linspace(-3000, 3000, n); X, Y = np.meshgrid(g, g[::-1])
    z = height_t5(X.ravel(), Y.ravel()).reshape(n, n)
    d, j = cKDTree(RP[:, :2]).query(np.column_stack([X.ravel(), Y.ravel()]))
    keep = (d > 4 * RP[j, 3] + 40).reshape(n, n) & (F.pad_w(X.ravel(), Y.ravel()).reshape(n, n) < 1e-6)
    return float(np.abs(z - z1)[keep].max()), int(keep.sum())


if __name__ == '__main__':
    names = sys.argv[1:] or list(TILES)
    err, cnt = verify_v001()
    print('VERIFY v001 LOD0 reproduction: max |dz| =', err, 'm over', cnt, 'samples', flush=True)
    assert err < .01, 'height function does not reproduce TASK 04 — stop'
    order = sorted(names, key=lambda k: -np.prod([(TILES[k]['x1'] - TILES[k]['x0']) / TILES[k]['sp'], (TILES[k]['y1'] - TILES[k]['y0']) / TILES[k]['sp']]))
    first = [k for k in order if k != 'WF']
    with Pool(int(os.environ.get('T5_PROCS', '3'))) as pool:
        stats = pool.map(build, first)
    if 'WF' in names:
        stats.append(build('WF'))
    wf = waterfalls()
    # water data for Blender: smooth river centrelines (5 m) within the L2 window, lakes, waterfalls
    riv = []
    for r in RIVERS:
        s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(r[:, :2], axis=0).T))])
        ss = np.arange(0, s[-1], 5.0)
        cx, cy = CubicSpline(s, r[:, 0]), CubicSpline(s, r[:, 1])
        zz = np.interp(ss, s, r[:, 2])
        for z_ in lip_profile(len(riv), 0, ss, s, r[:, 2]):              # featured falls: vertical lip in the water surface too
            zz = np.minimum(zz, z_)
        riv.append(np.column_stack([cx(ss), cy(ss), zz, np.interp(ss, s, r[:, 3])]).astype(np.float32))
    np.savez_compressed(os.path.join(OUT, 'water.npz'), RIV=np.concatenate(riv), RIVO=np.cumsum([0] + [len(a) for a in riv]))
    prev = {}
    pj = os.path.join(OUT, 'prep_v002.json')
    if os.path.exists(pj):
        prev = {s['tile']: s for s in json.load(open(pj)).get('tiles', [])}
    for s in stats:
        prev[s['tile']] = s
    meta = dict(status='TASK 05 detail on the APPROVED TASK 04 blockout (map rev 01 = PROPOSAL)', site_elev_m=SITE,
                verify_v001_max_abs_dz_m=err, frame=MET1['frame'], river_level_change_vs_v001=RIVER_LEVEL_CHANGE,
                tiles=[prev[k] for k in TILES if k in prev], tile_defs=TILES, lakes=LAKES, waterfalls=wf,
                n_rivers=len(RIVERS), erosion=EROSION, featured_waterfalls=FEATURED)
    json.dump(meta, open(pj, 'w'), indent=1)
    print('waterfalls', len(wf), [(round(w['x']), round(w['y']), round(w['z_top'] - w['z_bottom'])) for w in wf][:20])
    print('featured', FEATURED); print('lakes', LAKES); print('river level change vs v001', RIVER_LEVEL_CHANGE)
    print('T5_PREP_DONE')

"""t5_field — TASK 04 Ashram-Valley height + biome functions, copied VERBATIM from w4_prep_valley.py
(same data, same seeds) so TASK 05 detail is built on exactly the approved blockout geography.
t5_prep.py verifies that it reproduces the v001 heights. Pure python3 + numpy + scipy (not Blender)."""
import os, sys, json, math
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, '..', '_shared')))

OLD = os.path.join(ROOT, '..', 'map', 'data')
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


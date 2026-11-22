"""TASK 04 · STEP 3 — separate-dimension layout prep (system python3). Own space, own scale, NO shared coordinates.

Both layouts are read from the PROPOSED dimension maps (MAP_H1 / MAP_H2, worldgen2.py) — the same random seeds are used
so the 3D blockout matches the 2D maps exactly. Nothing about rules, travel or inhabitants is invented.
  Black Hole Training Area : 1 map pixel = 1 m (platform rings 560 / 700 / 830 m)
  Saithan's Dark World     : 1 map pixel = 5 m (9.0 × 6.5 km terrain)
"""
import os, sys, json, math
import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, '..', '_shared')))
import worldgen as wg

OUT = os.path.join(ROOT, '09_DIMENSIONS', 'data'); os.makedirs(OUT, exist_ok=True)

# ---------------- H1 Black Hole Training Area (same zones as dimension_black_hole())
zones = [(560, 'INNER RING', 5), (700, 'TRAINING RINGS', 9), (830, 'OUTER RING', 6)]
plats = []
for r_, lab, n in zones:
    for k in range(n):
        a = 2 * math.pi * k / n + r_ / 300
        w = 34 + (r_ - 500) / 12
        plats.append({'ring': lab, 'x': r_ * math.cos(a), 'y': r_ * math.sin(a), 'radius': w,
                      'z': 18 * math.sin(3 * a + r_ / 90)})   # gentle float offsets (proposal)
rng = np.random.default_rng(21)
deb = [{'x': float(r * math.cos(a)), 'y': float(r * math.sin(a)), 'z': float(rng.normal(0, 25)), 's': float(rng.uniform(2, 7))}
       for a, r in zip(rng.uniform(0, 2 * math.pi, 260), rng.uniform(420, 880, 260))]
bh = {'status': 'PROPOSAL (MAP_H1) — separate dimension, own space', 'unit': '1 BU = 1 m',
      'black_hole': {'horizon_radius': 150, 'photon_ring': 175, 'disk_inner': 200, 'disk_outer': 480},
      'zones': [[r, l, n] for r, l, n in zones], 'platforms': plats, 'debris': deb}
json.dump(bh, open(os.path.join(OUT, 'black_hole_layout.json'), 'w'), indent=1)

# ---------------- H2 Saithan's Dark World (same fields + seeds as dimension_dark_world())
Wd, Hd = 1800, 1300
hgt = wg.fbm((Hd, Wd), 5, 6, .55, 61)
rid = np.clip(1 - np.abs(wg.fbm((Hd, Wd), 9, 6, .5, 62)) * 2.2, 0, 1)
v = np.clip(1 - np.abs(wg.fbm((Hd, Wd), 3, 4, .5, 63)) * 6, 0, 1)
PX = 5.0
S = 4                                                   # mesh every 4 px = 20 m
hs = ndi.zoom(hgt, 1 / S, order=1); rs = ndi.zoom(rid, 1 / S, order=1); vs = ndi.zoom(v, 1 / S, order=1)
z = hs * 240 - (rs ** 3) * 22 - vs * 14                 # ash plains / highlands; fissure + corruption-river channels
rng = np.random.default_rng(64)
sp = []
for (fx, fy, n) in ((.22, .3, 110), (.72, .25, 90), (.33, .76, 80), (.82, .7, 70)):
    for _ in range(n):
        x = fx * Wd + rng.normal(0, 90); y = fy * Hd + rng.normal(0, 70); hh = rng.uniform(14, 40)
        sp.append([(x - Wd / 2) * PX, (Hd / 2 - y) * PX, hh * PX])
zones2 = [((.22, .3), 'OBSIDIAN SPIRE FIELD'), ((.72, .25), 'SPIRE CLIFFS'), ((.33, .76), 'ASH PLAINS'), ((.82, .7), 'SHATTERED HIGHLANDS'),
          ((.52, .5), 'CORRUPTED PORTAL SITE'), ((.6, .88), 'CORRUPTION RIVERS')]
dw = {'status': 'PROPOSAL (MAP_H2) — separate dimension, own space', 'unit': '1 BU = 1 m', 'px_m': PX, 'mesh_step_m': PX * S,
      'size_m': [Wd * PX, Hd * PX], 'spires': sp,
      'zones': [[nm, (fx - .5) * Wd * PX, (.5 - fy) * Hd * PX] for (fx, fy), nm in zones2],
      'portal_site': [(.52 - .5) * Wd * PX, (.5 - .5) * Hd * PX, 90 * PX * .25]}
json.dump(dw, open(os.path.join(OUT, 'dark_world_layout.json'), 'w'), indent=1)
np.savez_compressed(os.path.join(OUT, 'dark_world_terrain.npz'), z=z.astype(np.float32), fissure=(rs ** 3).astype(np.float16), corrupt=vs.astype(np.float16))
print('dims prep', len(plats), 'platforms', len(sp), 'spires', z.shape, float(z.min()), float(z.max()))
print('PREP_DIMS_DONE')

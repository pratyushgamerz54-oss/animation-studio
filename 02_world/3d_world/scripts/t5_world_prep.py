"""TASK 05 · MILESTONE 2 — main-world terrain v002 (whole map, 1 BU = 1 km, display relief ×20 like v001).

From the SAME world map (01_GEOGRAPHY/data/world_prep.npz, 7.8 km cells):
  * grid ×2 (3.9 km) with bicubic interpolation → smoother coastlines / island outlines (no 7.8 km stair-steps)
  * isotropic mountain detail (ridges 25–90 km, amplitude ∝ elevation) + light droplet erosion → readable ranges, peaks, valleys
  * lakes: terrain inside each lake pushed BELOW its level, shore ring kept ABOVE it → the water plane meets the terrain in a
    smooth shoreline (fixes the v001 stair-step lake shores)
  * sea floor shelf kept; coastline = terrain ∩ 0 m
Writes 01_GEOGRAPHY/data_v002/world_v002.npz (z in metres, colour, lake planes).    Usage: python3 t5_world_prep.py
"""
import os, sys, json, time
import numpy as np
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t5_noise as N
import t5_erosion as E

ROOT = os.path.abspath(os.path.join(HERE, '..'))
D = np.load(os.path.join(ROOT, '01_GEOGRAPHY', 'data', 'world_prep.npz'))
META = json.load(open(os.path.join(ROOT, '01_GEOGRAPHY', 'data', 'world_features.json')))
OUT = os.path.join(ROOT, '01_GEOGRAPHY', 'data_v002'); os.makedirs(OUT, exist_ok=True)
H, W = META['grid']; KM = META['km_per_cell']


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


t0 = time.time()
h = D['h'].astype(np.float64); col = D['col'].astype(np.float32); lab = D['lake_lab']; lev = D['lake_level']
S = 2
n, m = H * S, W * S
rr = (np.arange(n) + .5) / S - .5; cc = (np.arange(m) + .5) / S - .5
R_, C_ = np.meshgrid(rr, cc, indexing='ij')
z = ndi.map_coordinates(h, [R_, C_], order=3, mode='nearest')
X = (C_ + .5) * KM - 6000.0; Y = 3000.0 - (R_ + .5) * KM                     # km, same frame as v001 (map centre)
land = z > 0
# isotropic ridges on high ground (km coordinates → metres of relief)
mf = sstep(1200, 3200, z)
wx, wy = N.warp(X, Y, 400, 60, 301)
z = z + (N.ridged(wx, wy, 90, 4, 302) * 900 + N.ridged(wx, wy, 25, 3, 303) * 260) * mf ** 1.2 + N.fbm(X, Y, 40, 3, 304) * 60 * land
z = np.where(land, np.maximum(z, 1.0), z)                                     # keep the coastline where the map has it
# light erosion on land (valleys / spurs at this scale)
sp_m = KM / S * 1000.0
Hc, fl = E.hydraulic(np.maximum(z, 0) / sp_m * 40, .6 * z.size, 7, 2, erode=.25, deposit=.3, capacity=4.0)
dz = ndi.gaussian_filter(Hc * sp_m / 40 - np.maximum(z, 0), 1.0) * land
z = z + dz
# lakes: inside below the level, shore ring above it
labu = ndi.map_coordinates(lab.astype(np.float32), [R_, C_], order=0, mode='nearest').astype(int)
lake_planes = []
for k in range(1, int(lab.max()) + 1):
    if k - 1 >= len(lev):
        break
    L = float(lev[k - 1])
    msk = labu == k
    if not msk.any():
        continue
    inner = ndi.binary_erosion(msk, iterations=1)
    ring = ndi.binary_dilation(msk, iterations=2) & ~msk
    z = np.where(inner, np.minimum(z, L - 25 - 40 * ndi.distance_transform_edt(inner) / 10), z)
    z = np.where(msk & ~inner, np.minimum(z, L - 3), z)
    z = np.where(ring, np.maximum(z, L + 4), z)
    ys, xs = np.nonzero(ndi.binary_dilation(msk, iterations=1))
    lake_planes.append(dict(id=k, level_m=L, bbox_rc=[int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())]))
colu = np.stack([ndi.map_coordinates(col[..., i], [R_, C_], order=1, mode='nearest') for i in range(3)], -1)
np.savez_compressed(os.path.join(OUT, 'world_v002.npz'), z=z.astype(np.float32), col=colu.astype(np.float16), lab=labu.astype(np.int16))
meta = dict(status='TASK 05 main-world terrain v002 — same map (rev 01 = PROPOSAL), ×2 grid + detail; v001 untouched',
            grid=[n, m], km_per_cell=KM / S, frame=META['origin'], vexag=META['vexag'], lakes=lake_planes,
            z_min=float(z.min()), z_max=float(z.max()), seconds=round(time.time() - t0, 1))
json.dump(meta, open(os.path.join(OUT, 'world_v002.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in meta.items() if k != 'lakes'}), 'lakes', len(lake_planes))
print('T5_WORLD_PREP_DONE')

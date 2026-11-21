"""t5_erosion — terrain erosion for TASK 05 (python3 + numpy + numba, NOT Blender).

hydraulic(H, ...)  particle ("droplet") hydraulic erosion: each droplet runs downhill, picks up sediment where it speeds up,
                   drops it where it slows → gullies, ridges sharpen, alluvial fans / flat valley floors appear.
thermal(H, ...)    talus relaxation: material above the angle of repose slides down → scree aprons below cliffs.

Heights are passed in CELL UNITS (metres / cell size) so the behaviour is independent of the grid resolution.
Deterministic (fixed seed) → the same terrain is produced every run.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _grad(H, x, y):
    n, m = H.shape
    ix = int(x); iy = int(y)
    fx = x - ix; fy = y - iy
    a = H[iy, ix]; b = H[iy, ix + 1]; c = H[iy + 1, ix]; d = H[iy + 1, ix + 1]
    gx = (b - a) * (1 - fy) + (d - c) * fy
    gy = (c - a) * (1 - fx) + (d - b) * fx
    h = a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
    return h, gx, gy


@njit(cache=True)
def _hydraulic(H, n_drops, seed, radius, inertia, capacity, min_slope, deposit, erode, evaporate, gravity, max_steps, max_erode,
               FLOW):
    n, m = H.shape
    np.random.seed(seed)
    # brush offsets / weights (cone)
    r = radius
    offs = []
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            d = (dx * dx + dy * dy) ** .5
            if d <= r:
                offs.append((dy, dx, max(0.0, r - d)))
    k = len(offs)
    ody = np.empty(k, np.int64); odx = np.empty(k, np.int64); ow = np.empty(k)
    for i in range(k):
        ody[i] = offs[i][0]; odx[i] = offs[i][1]; ow[i] = offs[i][2]
    for _ in range(n_drops):
        x = np.random.random() * (m - 2 * r - 3) + r + 1
        y = np.random.random() * (n - 2 * r - 3) + r + 1
        dx = 0.0; dy = 0.0; speed = 1.0; water = 1.0; sed = 0.0
        for step in range(max_steps):
            ix = int(x); iy = int(y)
            h, gx, gy = _grad(H, x, y)
            dx = dx * inertia - gx * (1 - inertia)
            dy = dy * inertia - gy * (1 - inertia)
            L = (dx * dx + dy * dy) ** .5
            if L < 1e-9:
                break
            dx /= L; dy /= L
            nx = x + dx; ny = y + dy
            if nx < r + 1 or ny < r + 1 or nx >= m - r - 2 or ny >= n - r - 2:
                break
            FLOW[iy, ix] += water
            nh, _, _ = _grad(H, nx, ny)
            dh = nh - h
            cap = max(-dh, min_slope) * speed * water * capacity
            if sed > cap or dh > 0:
                amt = min(dh, sed) if dh > 0 else (sed - cap) * deposit
                sed -= amt
                fx = x - ix; fy = y - iy
                H[iy, ix] += amt * (1 - fx) * (1 - fy); H[iy, ix + 1] += amt * fx * (1 - fy)
                H[iy + 1, ix] += amt * (1 - fx) * fy; H[iy + 1, ix + 1] += amt * fx * fy
            else:
                amt = min((cap - sed) * erode, -dh, max_erode)
                wsum = 0.0
                for i in range(k):
                    wsum += ow[i]
                for i in range(k):
                    yy = iy + ody[i]; xx = ix + odx[i]
                    e = amt * ow[i] / wsum
                    H[yy, xx] -= e
                sed += amt
            speed = (max(speed * speed + dh * gravity, 0.0)) ** .5
            water *= (1 - evaporate)
            x = nx; y = ny


def hydraulic(H, n_drops, seed=1, radius=3, inertia=.05, capacity=4.0, min_slope=.01, deposit=.3, erode=.3, evaporate=.015,
              gravity=4.0, max_steps=80, max_erode=1.0):
    """In-place on a copy; returns (H_eroded, flow_accumulation)."""
    H = np.ascontiguousarray(H, np.float64).copy()
    FLOW = np.zeros_like(H)
    _hydraulic(H, int(n_drops), int(seed), int(radius), inertia, capacity, min_slope, deposit, erode, evaporate, gravity,
               int(max_steps), max_erode, FLOW)
    return H, FLOW


def thermal(H, talus=1.0, iters=30, rate=.25):
    """talus = max height difference per cell (cell units); returns (H, deposited) — deposited > 0 = scree."""
    H = H.astype(np.float64).copy(); H0 = H.copy()
    for _ in range(iters):
        dH = np.zeros_like(H)
        for ax, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
            nb = np.roll(H, sh, axis=ax)
            d = H - nb - talus
            mv = np.where(d > 0, d * rate * .5, 0.0)
            dH -= mv
            dH += np.roll(mv, -sh, axis=ax)
        dH[0, :] = dH[-1, :] = 0; dH[:, 0] = dH[:, -1] = 0
        H += dH
    return H, np.maximum(H - H0, 0)

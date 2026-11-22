"""t5_noise — isotropic gradient (Perlin-style) noise for TASK 05 terrain detail (numpy, vectorised, deterministic).

Why: the TASK 04 blockout used lattice VALUE noise; its ridged form shows axis-aligned squares when seen in detail.
Gradient noise with a different rotation per octave + domain warping gives natural, direction-free ridges and spurs.
"""
import numpy as np

_P = np.random.default_rng(2025).permutation(4096)
_P = np.concatenate([_P, _P])
_ANG = np.random.default_rng(2026).uniform(0, 2 * np.pi, 4096)
_GX, _GY = np.cos(_ANG), np.sin(_ANG)


def _h(ix, iy, s):
    return _P[(_P[(ix + s * 977) & 4095] + iy) & 4095]


def perlin(x, y, s=0):
    """≈[-0.7, 0.7], zero mean."""
    ix, iy = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - ix, y - iy
    u = fx * fx * fx * (fx * (fx * 6 - 15) + 10); v = fy * fy * fy * (fy * (fy * 6 - 15) + 10)
    out = 0
    acc = []
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        h = _h(ix + dx, iy + dy, s)
        acc.append(_GX[h] * (fx - dx) + _GY[h] * (fy - dy))
    a, b, c, d = acc
    return (a + (b - a) * u) * (1 - v) + (c + (d - c) * u) * v


def _rot(x, y, k):
    t = 0.6 + 1.37 * k
    c, s = np.cos(t), np.sin(t)
    return x * c - y * s, x * s + y * c


def fbm(x, y, scale, octaves, seed, gain=.5, lac=2.03):
    v = 0; amp = 1.0; tot = 0; f = 1.0 / scale
    for o in range(octaves):
        rx, ry = _rot(x * f, y * f, o + seed)
        v = v + amp * perlin(rx + 31.7 * o, ry - 17.3 * o, seed + o)
        tot += amp; amp *= gain; f *= lac
    return v / tot / .5          # ≈[-1, 1]


def ridged(x, y, scale, octaves, seed, gain=.5, lac=2.1, sharp=2.0):
    """ridged multifractal, ≈ zero mean (mean removed empirically), sharp crests."""
    v = 0; amp = 1.0; tot = 0; f = 1.0 / scale; w = 1.0
    for o in range(octaves):
        rx, ry = _rot(x * f, y * f, o + seed + 11)
        n = 1 - np.abs(perlin(rx + 5.1 * o, ry + 9.7 * o, seed + 40 + o) * 1.6)
        n = np.clip(n, 0, 1) ** sharp
        n = n * w; w = np.clip(n * 1.4, 0, 1)
        v = v + amp * n; tot += amp; amp *= gain; f *= lac
    return v / tot - .41      # same mean + spread as the TASK 04 ridged() → mean elevation unchanged


def warp(x, y, scale, amount, seed):
    return (x + fbm(x, y, scale, 3, seed) * amount, y + fbm(x, y, scale, 3, seed + 7) * amount)

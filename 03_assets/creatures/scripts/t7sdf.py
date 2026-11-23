"""t7sdf — TASK 07 signed-distance anatomy modeller (numpy; no Blender needed).

A creature part = list of primitives (round cones, ellipsoids, boxes) combined with smooth union / smooth subtraction.
Each primitive carries a ZONE name (belly, leg, hoof, face, ear, horn ...) that later drives colour, fur and materials.
mesh() → marching cubes (skimage) → (verts, faces), then t7kit turns it into clean quads (Quadriflow) in Blender.
Units: metres (1 BU = 1 m). Axes: +X forward (nose), +Y left, +Z up; ground at z = 0.
"""
import numpy as np

F = np.float32


def _n(v):
    v = np.asarray(v, F); return v / max(np.linalg.norm(v), 1e-9)


def rot_mat(yaw=0.0, pitch=0.0, roll=0.0):
    """degrees; yaw about Z, pitch about Y (positive = nose down), roll about X."""
    y, p, r = np.radians([yaw, pitch, roll])
    Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]], F)
    Ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]], F)
    Rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]], F)
    return (Rz @ Ry @ Rx).astype(F)


def look_mat(fwd, up=(0, 0, 1)):
    """rotation whose local X = fwd."""
    x = _n(fwd); u = np.asarray(up, F)
    y = np.cross(u, x)
    if np.linalg.norm(y) < 1e-6:
        y = np.cross((0, 1, 0), x)
    y = _n(y); z = np.cross(x, y)
    return np.stack([x, y, z], 1).astype(F)       # columns = local axes in world


class Prim:
    def __init__(self, kind, zone, k, sub, bbox, **p):
        self.kind, self.zone, self.k, self.sub, self.bbox, self.p = kind, zone, k, sub, bbox, p

    def d(self, P):
        p = self.p
        if self.kind == 'rcone':
            return sd_round_cone(P, p['a'], p['b'], p['ra'], p['rb'])
        if self.kind == 'ell':
            Q = (P - p['c']) @ p['R']                    # world → local
            return sd_ellipsoid(Q, p['r'])
        if self.kind == 'box':
            Q = np.abs((P - p['c']) @ p['R']) - p['h'] + p['rr']
            return np.linalg.norm(np.maximum(Q, 0), axis=-1) + np.minimum(Q.max(-1), 0) - p['rr']
        raise ValueError(self.kind)


def sd_round_cone(P, a, b, r1, r2):
    a = np.asarray(a, F); b = np.asarray(b, F)
    ba = b - a; l2 = float(ba @ ba); rr = r1 - r2; a2 = l2 - rr * rr; il2 = 1.0 / l2
    pa = P - a; y = pa @ ba; z = y - l2
    q = pa * l2 - y[..., None] * ba
    x2 = (q * q).sum(-1); y2 = y * y * l2; z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    d3 = (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - r1
    d1 = np.sqrt(x2 + z2) * il2 - r2
    d2 = np.sqrt(x2 + y2) * il2 - r1
    return np.where(np.sign(z) * a2 * z2 > k, d1, np.where(np.sign(y) * a2 * y2 < k, d2, d3)).astype(F)


def sd_ellipsoid(Q, r):
    r = np.asarray(r, F)
    k0 = np.linalg.norm(Q / r, axis=-1); k1 = np.linalg.norm(Q / (r * r), axis=-1)
    return (k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)).astype(F)


def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.maximum(k - np.abs(a - b), 0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def smax(a, b, k):
    return -smin(-a, -b, k)


class Part:
    """one watertight surface (body, ear, antler ...)."""

    def __init__(self, name, voxel=0.008):
        self.name, self.voxel, self.prims = name, voxel, []
        self.mirror = []          # indices mirrored in Y

    def _add(self, pr, mirror):
        self.prims.append(pr)
        if mirror:
            q = Prim(pr.kind, pr.zone, pr.k, pr.sub, None, **{k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in pr.p.items()})
            M = np.diag([1, -1, 1]).astype(F)
            for key in ('a', 'b', 'c'):
                if key in q.p:
                    q.p[key] = q.p[key] * np.array([1, -1, 1], F)
            if 'R' in q.p:
                q.p['R'] = (M @ q.p['R'] @ M).astype(F)
            q.bbox = _bbox(q)
            self.prims.append(q)
        return pr

    def rcone(self, a, b, ra, rb, zone='body', k=0.02, sub=False, mirror=False):
        pr = Prim('rcone', zone, k, sub, None, a=np.asarray(a, F), b=np.asarray(b, F), ra=float(ra), rb=float(rb))
        pr.bbox = _bbox(pr); return self._add(pr, mirror)

    def chain(self, pts, radii, zone='body', k=0.02, sub=False, mirror=False):
        for i in range(len(pts) - 1):
            self.rcone(pts[i], pts[i + 1], radii[i], radii[i + 1], zone, k, sub, mirror)

    def ell(self, c, r, R=None, zone='body', k=0.02, sub=False, mirror=False):
        R = np.eye(3, dtype=F) if R is None else np.asarray(R, F)
        pr = Prim('ell', zone, k, sub, None, c=np.asarray(c, F), r=np.asarray(r, F), R=R)
        pr.bbox = _bbox(pr); return self._add(pr, mirror)

    def box(self, c, h, R=None, rr=0.005, zone='body', k=0.01, sub=False, mirror=False):
        R = np.eye(3, dtype=F) if R is None else np.asarray(R, F)
        pr = Prim('box', zone, k, sub, None, c=np.asarray(c, F), h=np.asarray(h, F), R=R, rr=float(rr))
        pr.bbox = _bbox(pr); return self._add(pr, mirror)

    # --------------------------------------------------------------------------------------------------------------------------
    def field(self, P):
        d = np.full(P.shape[:-1], 1.0, F)
        for pr in self.prims:
            dd = pr.d(P)
            d = smax(d, -dd, pr.k) if pr.sub else smin(d, dd, pr.k)
        return d

    def mesh(self, warp=None):
        """warp(P) → displacement field added to the distance (organic wobble / muscle relief)."""
        from skimage import measure
        adds = [p for p in self.prims if not p.sub]
        lo = np.min([p.bbox[0] for p in adds], 0) - 3 * self.voxel
        hi = np.max([p.bbox[1] for p in adds], 0) + 3 * self.voxel
        h = self.voxel
        n = np.ceil((hi - lo) / h).astype(int) + 1
        grid = np.full(n, 1.0, F)
        xs = [lo[i] + h * np.arange(n[i], dtype=F) for i in range(3)]
        for pr in self.prims:
            m = pr.k + 3 * h
            b0 = np.clip(np.floor((pr.bbox[0] - m - lo) / h).astype(int), 0, n - 1)
            b1 = np.clip(np.ceil((pr.bbox[1] + m - lo) / h).astype(int) + 1, 1, n)
            if np.any(b1 <= b0):
                continue
            X, Y, Z = np.meshgrid(xs[0][b0[0]:b1[0]], xs[1][b0[1]:b1[1]], xs[2][b0[2]:b1[2]], indexing='ij')
            P = np.stack([X, Y, Z], -1)
            dd = pr.d(P)
            sl = (slice(b0[0], b1[0]), slice(b0[1], b1[1]), slice(b0[2], b1[2]))
            grid[sl] = smax(grid[sl], -dd, pr.k) if pr.sub else smin(grid[sl], dd, pr.k)
        if warp is not None:
            near = np.abs(grid) < 6 * h
            idx = np.nonzero(near)
            P = np.stack([lo[i] + h * idx[i] for i in range(3)], -1).astype(F)
            grid[idx] += warp(P).astype(F)
        v, f, _, _ = measure.marching_cubes(grid, 0.0, spacing=(h, h, h))
        return (v + lo).astype(F), f.astype(np.int32)

    def zones(self, P, soft=0.012):
        """per-vertex soft weights per zone (additive prims only, subtractions ignored) → dict zone → (N,) float."""
        names = sorted({p.zone for p in self.prims if not p.sub})
        D = {z: np.full(len(P), 9.0, F) for z in names}
        for pr in self.prims:
            if pr.sub:
                continue
            D[pr.zone] = np.minimum(D[pr.zone], pr.d(P))
        S = np.stack([D[z] for z in names], 0)
        W = np.exp(-(S - S.min(0)) / soft)
        W /= W.sum(0)
        return {z: W[i] for i, z in enumerate(names)}, {z: D[z] for z in names}


def _bbox(pr):
    p = pr.p
    if pr.kind == 'rcone':
        a, b, ra, rb = p['a'], p['b'], p['ra'], p['rb']
        return np.minimum(a - ra, b - rb), np.maximum(a + ra, b + rb)
    if pr.kind == 'ell':
        e = np.abs(p['R']) @ p['r']
        return p['c'] - e, p['c'] + e
    if pr.kind == 'box':
        e = np.abs(p['R']) @ p['h']
        return p['c'] - e, p['c'] + e


# ------------------------------------------------------------------------------------------------------------------------------
# value noise (numpy) for organic wobble / colour mottling
def vnoise(P, scale=1.0, seed=0):
    P = np.asarray(P, np.float64) * scale + seed * 17.13
    i = np.floor(P).astype(np.int64); f = P - i
    u = f * f * (3 - 2 * f)

    def h(ix, iy, iz):
        n = (ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791) ^ (seed * 2654435761)
        n = (n ^ (n >> 13)) * 1274126177
        return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0

    r = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (u[:, 0] if dx else 1 - u[:, 0]) * (u[:, 1] if dy else 1 - u[:, 1]) * (u[:, 2] if dz else 1 - u[:, 2])
                r = r + w * h(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz)
    return r * 2 - 1


def fbm(P, scale=1.0, oct=4, seed=0):
    r, a, s = 0, 0.5, scale
    for o in range(oct):
        r = r + a * vnoise(P, s, seed + o); a *= 0.5; s *= 2.03
    return r


def voronoi_f1(P, scale=1.0, seed=0, jitter=0.9):
    """distance to nearest feature point + cell id (spots / rosettes)."""
    P = np.asarray(P, np.float64) * scale
    i = np.floor(P).astype(np.int64)
    best = np.full(len(P), 9.0); cid = np.zeros(len(P))
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c = i + np.array([dx, dy, dz])
                n = (c[:, 0] * 73856093) ^ (c[:, 1] * 19349663) ^ (c[:, 2] * 83492791) ^ (seed * 2654435761)
                rnd = np.stack([((n * k) >> 8 & 0xFFFF) / 65535.0 for k in (1103515245, 22695477, 1664525)], -1)
                fp = c + 0.5 + (rnd - 0.5) * jitter
                d = np.linalg.norm(P - fp, axis=-1)
                m = d < best; best = np.where(m, d, best); cid = np.where(m, rnd[:, 0], cid)
    return best, cid

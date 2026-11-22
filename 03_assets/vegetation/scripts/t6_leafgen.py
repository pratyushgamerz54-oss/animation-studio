"""TASK 06 · procedural LEAF / NEEDLE / FLOWER / PLUME texture atlases (python3 + numpy + Pillow, no Blender).

Every vegetation species gets its OWN atlas so species stay visually distinct (no shared generic leaf):
    textures/leaves/<atlas>_col.png    RGBA sRGB  (alpha = cut-out)
    textures/leaves/<atlas>_nor.png    OpenGL tangent-space normal (from a painted height field: dome, midrib, veins)
    textures/leaves/<atlas>_rough.png  roughness (glossy blade, rougher veins / needles)
    textures/leaves/<atlas>_prev.png   preview on a neutral background (used by the sheets)
Atlas = 2 × 2 tiles (4 variants: shape / size / colour jitter, tile 3 = aged / sun-bleached variant).
Every tile is a TWIG SPRAY (twig + several leaves) whose base (pivot) is the bottom-centre of the tile → the tree generator
attaches the card there. Tile physical size (metres) is stored in atlases.json and used for the card size.

Run:  python3 03_assets/vegetation/scripts/t6_leafgen.py [atlas ...]      (all atlases if none given)
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('T6_LEAF_OUT') or os.path.abspath(os.path.join(HERE, '..', 'textures', 'leaves'))
TILE = 1024          # final tile resolution (atlas 2048²)
SS = 2               # supersampling
N = TILE * SS


def hexc(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def srgb2lin(c):
    return np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)


def lin2srgb(c):
    c = np.clip(c, 0, 1); return np.where(c <= .0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - .055)


def value_noise(n, cells, rng):
    g = rng.random((cells + 1, cells + 1)).astype(np.float32)
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255


class Tile:
    """one N×N canvas (y up). painter's order; each primitive writes colour, alpha, height, roughness."""

    def __init__(self, rng, z=1.0):
        self.rng = rng; self.z = z
        self.C = np.zeros((N, N, 3), np.float32); self.A = np.zeros((N, N), np.float32)
        self.H = np.zeros((N, N), np.float32); self.R = np.full((N, N), .55, np.float32)
        self.noise = value_noise(N, 24, rng) * .6 + value_noise(N, 90, rng) * .4
        ys, xs = np.mgrid[0:N, 0:N].astype(np.float32)
        self.X = .5 + ((xs + .5) / N - .5) * z; self.Y = (1 - (ys + .5) / N) * z     # z > 1 = zoom out (auto-fit)

    def box(self, x0, y0, x1, y1):
        z = self.z
        i0 = max(0, int((1 - y1 / z) * N) - 2); i1 = min(N, int((1 - y0 / z) * N) + 2)
        j0 = max(0, int(((x0 - .5) / z + .5) * N) - 2); j1 = min(N, int(((x1 - .5) / z + .5) * N) + 2)
        return slice(i0, i1), slice(j0, j1)

    def put(self, sl, mask, col, h, r):
        if mask is None or not mask.any():
            return
        m = mask
        for k in range(3):
            ch = self.C[sl + (k,)] if False else self.C[sl][..., k]
            ch[m] = col[..., k][m] if col.ndim == 3 else col[k]
        self.A[sl][m] = 1.0
        hh = self.H[sl]; hh[m] = h[m] if np.ndim(h) else h
        rr = self.R[sl]; rr[m] = r[m] if np.ndim(r) else r

    # ---------------------------------------------------------------- primitives
    def segment(self, p0, p1, w0, w1, col, rough=.7, hscale=.6):
        (x0, y0), (x1, y1) = p0, p1
        pad = max(w0, w1)
        sl = self.box(min(x0, x1) - pad, min(y0, y1) - pad, max(x0, x1) + pad, max(y0, y1) + pad)
        X, Y = self.X[sl], self.Y[sl]
        dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy + 1e-12
        t = np.clip(((X - x0) * dx + (Y - y0) * dy) / L2, 0, 1)
        d = np.hypot(X - (x0 + t * dx), Y - (y0 + t * dy))
        w = (w0 + (w1 - w0) * t) / 2
        m = d <= w
        q = np.clip(d / np.maximum(w, 1e-6), 0, 1)
        shade = (1 - .35 * q ** 2)[..., None]
        c = np.broadcast_to(srgb2lin(col), X.shape + (3,)) * shade * (.9 + .2 * self.noise[sl][..., None])
        self.put(sl, m, c, hscale * np.sqrt(np.clip(1 - q * q, 0, 1)) + .4, rough)

    def curve(self, pts, w0, w1, col, rough=.7):
        n = len(pts) - 1
        for i in range(n):
            self.segment(pts[i], pts[i + 1], w0 + (w1 - w0) * i / n, w0 + (w1 - w0) * (i + 1) / n, col, rough)

    def leaf(self, base, ang, length, width, P, col_top, col_edge, col_vein, jitter=0.0):
        """leaf blade. base (x,y), ang = direction (rad, 0 = +x), length/width in tile units. P = shape params."""
        ca, sa = math.cos(ang), math.sin(ang)
        tip = (base[0] + ca * length, base[1] + sa * length)
        pad = width * .75
        sl = self.box(min(base[0], tip[0]) - pad, min(base[1], tip[1]) - pad, max(base[0], tip[0]) + pad, max(base[1], tip[1]) + pad)
        X, Y = self.X[sl] - base[0], self.Y[sl] - base[1]
        u = (X * ca + Y * sa) / length; v = (-X * sa + Y * ca) / (width / 2)          # v ∈ [-1, 1] at the widest point
        shape = P['shape']; u_lo = -.07 if shape == 'heart' else 0.0; uu = np.clip(u, u_lo, 1)
        if shape == 'heart':          # broad ROUNDED base around the petiole (slight notch), long drip tip (Ficus religiosa)
            body = np.sqrt(np.clip(1 - ((uu - .31) / .385) ** 2, 0, 1)) * (1 - .15 * np.clip(uu, 0, 1))
            tail = np.clip((1 - uu) / .42, 0, 1) ** 1.3 * .22
            w = np.maximum(body, np.where(uu > .5, tail, 0))
        elif shape == 'lance':
            w = np.sin(np.pi * uu ** P.get('skew', .8)) ** P.get('pw', .9)
        elif shape == 'elliptic':
            w = np.sin(np.pi * uu) ** P.get('pw', .55)
        elif shape == 'round':
            w = np.sqrt(np.clip(1 - (2 * uu - 1) ** 2, 0, 1))
        elif shape == 'obovate':
            w = np.sin(np.pi * uu ** 1.35) ** .6
        elif shape == 'lobed':        # oak: rounded lobes along the margin
            w = (np.sin(np.pi * uu ** .85) ** .55) * (.68 + .32 * np.abs(np.sin(uu * np.pi * P.get('lobes', 4.5))))
        elif shape == 'fan':          # fantasy fan leaf (Lantern tree proposal)
            w = np.clip(uu * 1.6, 0, 1) ** .7 * np.where(uu > .75, np.sqrt(np.clip(1 - ((uu - .75) / .25) ** 2, 0, 1)), 1)
        else:
            w = np.sin(np.pi * uu) ** .7
        ser = P.get('serr', 0.0)
        if ser:
            w = w * (1 - ser * (.5 + .5 * np.sin(uu * P.get('teeth', 40) * np.pi)) ** 3)
        inside = (u >= u_lo) & (u <= 1) & (np.abs(v) <= w)
        if P.get('bites', True) and shape not in ('fan',) and self.rng.random() < .2:     # insect bites / torn margins (real leaves)
            for _ in range(self.rng.integers(1, 3)):
                bu = self.rng.uniform(.3, .85); sgn = self.rng.choice([-1, 1]); rb = self.rng.uniform(.05, .11) * length
                wb = np.interp(bu, np.linspace(0, 1, 50), np.clip(np.sin(np.pi * np.linspace(0, 1, 50)) ** .7, 0, 1))
                du_ = (u - bu) * length; dv_ = (v - sgn * wb * 1.05) * width / 2
                inside &= ~(np.sqrt(du_ ** 2 + dv_ ** 2) < rb)
        if not inside.any():
            return
        q = np.clip(np.abs(v) / np.maximum(w, 1e-4), 0, 1)
        nz = self.noise[sl]
        top, edge, vein = srgb2lin(col_top), srgb2lin(col_edge), srgb2lin(col_vein)
        jt = 1 + self.rng.normal(0, .07, 3) + self.rng.normal(0, .06)       # every leaf slightly different
        top = top * jt; edge = edge * (1 + (jt - 1) * .6)
        f = (q ** 1.6)[..., None]
        c = top * (1 - f) + edge * f
        c = c * (.86 + .26 * nz[..., None]) * (1 + jitter * .0)
        c = c * (1 - .25 * np.clip(1 - uu / .25, 0, 1)[..., None] * P.get('basedark', 1))
        # veins (realism pass 22 Nov): soft-edged, low colour contrast, fading towards the margin; relief carried by the normal map
        ribw = length * P.get('rib', .010) * (1.2 - uu)
        dmid = np.abs(v) * w * width / 2
        mid_s = np.clip(1 - dmid / np.maximum(ribw, 1e-6), 0, 1) ** 1.2
        nv = P.get('veins', 9)
        dl = np.abs(((uu - np.abs(v) * P.get('slant', .22)) * nv) % 1 - .5)
        lat_s = np.clip(1 - dl / .04, 0, 1) ** 1.5 * np.clip(1 - q ** 2, 0, 1) * (uu > .05) * (P.get('veinvis', 1) > 0)
        a = (.42 * mid_s + .26 * lat_s)[..., None]
        c = c * (1 - a) + vein * a
        # natural variation inside the blade: lighter along the midrib, darker margin, a few small blemish spots
        c = c * (1 + .07 * (1 - q[..., None]) ** 4) * (1 - .09 * q[..., None] ** 6)
        rng = self.rng
        if rng.random() < .3 and P.get('spots', True):
            for _ in range(rng.integers(1, 4)):
                su, sv = rng.uniform(.2, .85), rng.uniform(-.7, .7)
                rs = rng.uniform(.012, .03) * length
                du_ = (u - su) * length; dv_ = (v - sv) * width / 2
                sm = np.clip(1 - np.sqrt(du_ ** 2 + dv_ ** 2) / rs, 0, 1) ** .8
                spot = np.array(srgb2lin(np.array([.45, .36, .16])), np.float32)
                c = c * (1 - .55 * sm[..., None]) + spot * .55 * sm[..., None]
        mid, lat = mid_s, lat_s
        h = .55 * np.sqrt(np.clip(1 - q * q, 0, 1)) * P.get('dome', 1) + .15 - .20 * lat - .28 * mid + .05 * nz
        if P.get('cup', 0):
            h = h + P['cup'] * q * q
        r = np.clip(P.get('rough', .42) + .18 * lat + .12 * (nz - .5), .15, .95)
        self.put(sl, inside, c.astype(np.float32), h.astype(np.float32), r.astype(np.float32))

    def needle(self, p0, ang, length, width, col_a, col_b):
        p1 = (p0[0] + math.cos(ang) * length, p0[1] + math.sin(ang) * length)
        t = self.rng.random()
        col = col_a * (1 - t) + col_b * t
        self.segment(p0, p1, width, width * .25, col, rough=.5, hscale=.5)

    def blossom(self, c, rad, petals, col, col_c, rot=0.0):
        """5-petal flower seen from the front (rhododendron truss floret, primula, berberis…)."""
        for k in range(petals):
            a = rot + 2 * np.pi * k / petals
            self.leaf(c, a, rad, rad * .9, {'shape': 'obovate', 'veins': 5, 'slant': .1, 'rib': .004, 'rough': .5,
                                           'basedark': .3}, col, col * .82 + .18, col * .75)
        self.segment((c[0] - rad * .08, c[1]), (c[0] + rad * .08, c[1]), rad * .3, rad * .3, col_c, rough=.6)


# ====================================================================== spray layouts
def twig_path(rng, x0=.5, y0=.02, top=.9, bend=.08, n=12):
    b = rng.uniform(-bend, bend)
    return [(x0 + b * (t ** 1.5) + .01 * math.sin(t * 7 + rng.random()), y0 + (top - y0) * t) for t in np.linspace(0, 1, n)]


def at(path, t):
    f = t * (len(path) - 1); i = min(int(f), len(path) - 2); s = f - i
    (ax, ay), (bx, by) = path[i], path[i + 1]
    return (ax + (bx - ax) * s, ay + (by - ay) * s), math.atan2(by - ay, bx - ax)


def spray(T, A, var):
    rng = T.rng
    top, edge, vein, twig = (hexc(A[k]) for k in ('top', 'edge', 'vein', 'twig'))
    if var == 3:       # aged / sun-bleached variant
        top = top * .82 + hexc(A.get('aged', '#9C8F45')) * .18; edge = edge * .8 + hexc(A.get('aged', '#9C8F45')) * .2
    hue = rng.normal(0, .035, 3); top = np.clip(top * (1 + hue), 0, 1)
    lay = A['layout']; P = dict(A['leaf']); L = A['len'] * rng.uniform(.88, 1.08); W = L * A['wratio']
    if lay in ('alternate', 'opposite'):
        path = twig_path(rng, top=A.get('twigtop', .88), bend=.06)
        T.curve(path, A.get('twigw', .012), .004, twig)
        n = A['n']; ts = np.linspace(A.get('t0', .16), .97, n)
        for i, t in enumerate(ts):
            p, a = at(path, t)
            sides = (-1, 1) if lay == 'opposite' else ((-1) ** i,)
            for s in sides:
                spread = math.radians(A.get('spread', 50) + rng.uniform(-12, 12))
                la = a + s * spread
                ll = L * (.65 + .35 * min(1, t * 1.6)) * rng.uniform(.85, 1.1)
                pet = A.get('petiole', .05) * ll
                pb = (p[0] + math.cos(la) * pet, p[1] + math.sin(la) * pet)
                T.segment(p, pb, .005, .004, twig * .8 + top * .2, .6)
                droop = math.radians(A.get('droop', 12)) * -s
                T.leaf(pb, la + droop * .5, ll, W * rng.uniform(.85, 1.1), P, top, edge, vein)
        p, a = at(path, 1.0)
        T.leaf(p, a + rng.uniform(-.15, .15), L * .9, W * .9, P, top, edge, vein)
    elif lay == 'rosette':
        path = twig_path(rng, top=.42, bend=.05)
        T.curve(path, A.get('twigw', .02), .012, twig)
        p, a = at(path, 1.0)
        n = A['n']
        for i in range(n):
            la = math.pi / 2 + (i / (n - 1) - .5) * math.radians(A.get('fan', 300)) + rng.uniform(-.1, .1)
            T.leaf(p, la, L * rng.uniform(.8, 1.05), W * rng.uniform(.9, 1.1), P, top, edge, vein)
        if A.get('flower') and not (A.get('flower_some') and var >= 2):
            F = A['flower']; fc = hexc(F['col']); cc = hexc(F.get('centre', '#F3E07A'))
            ctr = (p[0], p[1] + L * .55)
            for k in range(F['n']):
                r = F['spread'] * math.sqrt(rng.random()); aa = rng.random() * 2 * np.pi
                T.blossom((ctr[0] + r * math.cos(aa), ctr[1] + r * math.sin(aa) * .8), F['size'] * rng.uniform(.8, 1.1), 5,
                          np.clip(fc * rng.uniform(.85, 1.1), 0, 1), cc, rng.random())
    elif lay in ('needle_tuft', 'needle_flat', 'needle_bundle', 'scale'):
        path = twig_path(rng, top=.92, bend=.05)
        T.curve(path, A.get('twigw', .014), .005, twig)
        nl = A['n']; col_a, col_b = top, edge
        sides = np.linspace(.08, .95, A.get('side', 6))
        for i, t in enumerate(sides):        # side shoots
            p, a = at(path, t); s = (-1) ** i
            la = a + s * math.radians(A.get('spread', 55)); sl = L * (1 - .5 * t) * rng.uniform(.8, 1.1)
            q = (p[0] + math.cos(la) * sl, p[1] + math.sin(la) * sl)
            T.segment(p, q, .007, .003, twig, .6)
            sub = [(p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k) for k in np.linspace(0, 1, 6)]
            needles_on(T, sub, la, A, col_a, col_b, rng)
        needles_on(T, path, math.pi / 2, A, col_a, col_b, rng)
    elif lay == 'beard':                     # hanging beard lichen / moss strand (Usnea-like), hangs from the TOP of the tile
        for k in range(A['n']):
            x = .5 + rng.normal(0, .08); pts = [(x, .98)]
            for j in range(18):
                x += rng.normal(0, .012); pts.append((x, .98 - (j + 1) * .045 * rng.uniform(.8, 1.05)))
            T.curve(pts, .010, .003, top * rng.uniform(.8, 1.1))
            for j in range(1, len(pts) - 1, 1):
                for _ in range(3):
                    a = -math.pi / 2 + rng.normal(0, .9)
                    T.needle(pts[j], a, rng.uniform(.02, .05), .004, top, edge)
    elif lay == 'pinnate':                   # fern frond segment: rachis + opposite pinnae
        path = twig_path(rng, top=.97, bend=.03)
        T.curve(path, .010, .005, twig)
        for t in np.linspace(.03, .97, A['n']):
            p, a = at(path, t)
            for s in (-1, 1):
                ll = L * (1 - .55 * t) * rng.uniform(.9, 1.05)
                T.leaf(p, a + s * math.radians(A.get('spread', 70)), ll, W, P, top, edge, vein)
    elif lay == 'plume':                     # grass plume (Saccharum kans grass)
        path = twig_path(rng, top=.97, bend=.04)
        T.curve(path, .006, .002, twig)
        for t in np.linspace(.1, 1, A['n']):
            p, a = at(path, t)
            for _ in range(5):
                T.needle(p, a + rng.normal(0, .55), L * rng.uniform(.4, 1.0) * (1.1 - .5 * t), .0035, top, edge)
    elif lay == 'single':                    # one leaf filling the tile (lotus pad, floating leaves, petals)
        if P['shape'] == 'pad':
            pad_leaf(T, A, top, edge, vein)
        else:
            T.leaf((.5, .03), math.pi / 2, .94, .94 * A['wratio'], P, top, edge, vein)
    return T


def needles_on(T, path, base_ang, A, ca, cb, rng):
    lay = A['layout']; L = A['nlen']
    for t in np.linspace(.04, 1, A['n']):
        p, a = at(path, t)
        if lay == 'needle_tuft':                  # cedar / larch: tufts of short needles on spurs
            for k in range(A.get('tuft', 16)):
                aa = a + rng.normal(0, 1.1) + (math.pi if rng.random() < .25 else 0)
                T.needle(p, aa, L * rng.uniform(.6, 1.1), A.get('nw', .006), ca, cb)
        elif lay == 'needle_flat':                # fir / spruce / yew: comb of needles on both sides
            for s in (-1, 1):
                aa = a + s * math.radians(A.get('nang', 65) + rng.uniform(-12, 12))
                T.needle(p, aa, L * rng.uniform(.8, 1.1), A.get('nw', .007), ca, cb)
        elif lay == 'needle_bundle':              # pines: bundles of 3 long drooping needles
            for k in range(3):
                aa = a + rng.normal(0, .5) - .25 * math.copysign(1, math.cos(a))
                pts = [p]; ang = aa; q = p
                for j in range(6):
                    ang += A.get('ndroop', -.06)
                    q = (q[0] + math.cos(ang) * L / 6, q[1] + math.sin(ang) * L / 6); pts.append(q)
                col = ca * (1 - (rng.random())) + cb * rng.random()
                T.curve(pts, A.get('nw', .005), .0015, col, .45)
        elif lay == 'scale':                      # juniper: dense short awl needles
            for k in range(6):
                aa = a + rng.normal(0, .9)
                T.needle(p, aa, L * rng.uniform(.5, 1), A.get('nw', .007), ca, cb)


def pad_leaf(T, A, top, edge, vein):
    """peltate round pad with a notch and radial veins (lotus / water lily). Centre of tile = petiole point."""
    X, Y = T.X - .5, T.Y - .5
    r = np.hypot(X, Y); a = np.arctan2(Y, X)
    R = .47 * (1 + .02 * np.sin(a * 9))
    notch = A['leaf'].get('notch', 0)
    inside = (r < R) & ~((np.abs(np.angle(np.exp(1j * (a + np.pi / 2)))) < notch) & (r > .02))
    q = r / R
    c = srgb2lin(top) * (1 - q[..., None] ** 2) + srgb2lin(edge) * q[..., None] ** 2
    c = c * (.85 + .3 * T.noise[..., None])
    rad = (np.abs(((a / (2 * np.pi)) * A['leaf'].get('veins', 22)) % 1 - .5) < .04) & (q > .06)
    c = np.where(rad[..., None], c * .5 + srgb2lin(vein) * .5, c)
    h = .3 + .25 * q * q - .15 * rad
    rgh = np.where(rad, .5, A['leaf'].get('rough', .25))
    T.put((slice(None), slice(None)), inside, c.astype(np.float32), h.astype(np.float32), rgh.astype(np.float32))


# ====================================================================== atlas definitions (one per species)
# len = leaf length in tile units, n = leaves per spray, size_m = physical size of ONE tile (card) in metres.
G = lambda **k: k
ATLASES = {
    # ------------------------------------------------------------------ ASHRAM VALLEY (R-01) — species-inspired
    'av_peepal':  G(layout='alternate', n=7, len=.27, wratio=.62, spread=58, petiole=.38, size_m=.55, top='#3E7A2A', edge='#5E9A38',
                    vein='#A8C77A', twig='#6B5A44', aged='#B5863A', leaf=G(shape='heart', veins=11, slant=.18, rough=.30, rib=.012)),
    'av_deodar':  G(layout='needle_tuft', n=16, nlen=.055, nw=.006, tuft=18, side=7, len=.42, wratio=.3, size_m=.50, top='#4E6E5A',
                    edge='#6E8D78', vein='#3A5444', twig='#5D4A3A', aged='#8A8A55', leaf=G(shape='lance')),
    'av_chir':    G(layout='needle_bundle', n=26, nlen=.30, nw=.0055, ndroop=-.07, side=4, spread=40, len=.25, wratio=.3, size_m=.65,
                    top='#7C9A3C', edge='#A5B65A', vein='#5A6E2C', twig='#7A5238', aged='#B79E52', leaf=G(shape='lance')),
    'av_banj':    G(layout='alternate', n=9, len=.24, wratio=.30, spread=48, petiole=.08, size_m=.42, top='#2F5A2E', edge='#7F9A72',
                    vein='#8FA884', twig='#5A4A3C', aged='#8F8A55', leaf=G(shape='lance', skew=.75, serr=.18, teeth=26, veins=12, rough=.40)),
    'av_rhodo':   G(layout='rosette', n=9, len=.34, wratio=.30, fan=320, size_m=.50, top='#2E4F2A', edge='#4D6B3A', vein='#8BA070',
                    twig='#6A4A3A', aged='#7C7A48', leaf=G(shape='elliptic', pw=.6, veins=10, rough=.28),
                    flower=G(n=26, size=.055, spread=.15, col='#C0182B', centre='#3A0A10'), flower_some=True),
    'av_bamboo':  G(layout='alternate', n=8, len=.40, wratio=.12, spread=32, petiole=.04, size_m=.60, top='#5F8A35', edge='#88A851',
                    vein='#9AB86A', twig='#7D8A3A', aged='#B6A45A', leaf=G(shape='lance', skew=.6, pw=.8, veins=0, veinvis=0, rib=.006, rough=.35)),
    'av_berberis': G(layout='alternate', n=12, len=.14, wratio=.45, spread=60, petiole=.05, size_m=.25, top='#3C6A2E', edge='#5E8A3C',
                     vein='#7EA05A', twig='#8A5A3A', aged='#9A5A2E', leaf=G(shape='obovate', veins=5, rough=.35, serr=.1, teeth=14)),
    'av_tulsi':   G(layout='opposite', n=6, len=.20, wratio=.55, spread=52, petiole=.25, size_m=.18, top='#3E6A2C', edge='#5C7E3A',
                    vein='#2F4A22', twig='#5A3A4A', aged='#6A4A5A', leaf=G(shape='elliptic', pw=.7, serr=.06, teeth=18, veins=7, rough=.45)),
    'av_fern':    G(layout='pinnate', n=16, len=.36, wratio=.22, spread=72, size_m=.40, top='#3F7A2C', edge='#5E9640', vein='#7FB060',
                    twig='#4E5A2E', aged='#9A8A45', leaf=G(shape='lance', skew=.9, serr=.25, teeth=22, veins=8, rough=.45)),
    'av_kans':    G(layout='plume', n=34, len=.12, wratio=.1, size_m=.45, top='#F1ECE0', edge='#D8CCB4', vein='#C8BFA8', twig='#B9A77A',
                    aged='#D8C9A0', leaf=G(shape='lance')),
    'av_lotus':   G(layout='single', n=1, len=1, wratio=1, size_m=.55, top='#3F7B3A', edge='#6D9A4D', vein='#A6C68A', twig='#4A6A3A',
                    aged='#8A8A4A', leaf=G(shape='pad', notch=0.0, veins=24, rough=.22)),
    # ------------------------------------------------------------------ ENCHANTED FOREST (R-02) — teal-green key (World Bible)
    'ef_elder':   G(layout='alternate', n=11, len=.17, wratio=.48, spread=55, petiole=.06, size_m=.70, top='#1F4F44', edge='#2F6A58',
                    vein='#5E8F7A', twig='#4A3A30', aged='#5A6A3A', leaf=G(shape='elliptic', pw=.6, veins=8, rough=.32)),
    'ef_beech':   G(layout='alternate', n=8, len=.23, wratio=.55, spread=62, petiole=.06, size_m=.45, top='#2F6A4A', edge='#4A8A60',
                    vein='#7FAE88', twig='#5A4A3E', aged='#9A8A45', leaf=G(shape='elliptic', pw=.65, serr=.05, teeth=12, veins=9, slant=.3, rough=.38)),
    'ef_oak':     G(layout='alternate', n=8, len=.25, wratio=.52, spread=55, petiole=.04, size_m=.45, top='#2C5A3C', edge='#3E7448',
                    vein='#6E9A70', twig='#4E3E32', aged='#8A7A40', leaf=G(shape='lobed', lobes=4.5, veins=6, slant=.2, rough=.40)),
    'ef_yew':     G(layout='needle_flat', n=30, nlen=.065, nw=.010, nang=70, side=6, spread=50, len=.40, wratio=.3, size_m=.40,
                    top='#17382C', edge='#2C5240', vein='#1A3A2C', twig='#5A3A2A', aged='#4A5A2A', leaf=G(shape='lance')),
    'ef_veil':    G(layout='alternate', n=14, len=.20, wratio=.16, spread=28, petiole=.03, size_m=.50, twigtop=.98, top='#4F8F86',
                    edge='#A6C9C0', vein='#C8E0D8', twig='#5A6A60', aged='#7A8A6A', leaf=G(shape='lance', skew=.7, veins=0, veinvis=0, rough=.30)),
    'ef_spiral':  G(layout='alternate', n=9, len=.20, wratio=.85, spread=60, petiole=.15, size_m=.45, top='#5C8C9A', edge='#A9C4CC',
                    vein='#D0E2E6', twig='#6A6A70', aged='#7A8A7A', leaf=G(shape='round', veins=7, slant=.35, rough=.30)),
    'ef_lantern': G(layout='rosette', n=7, len=.40, wratio=.75, fan=240, size_m=.60, top='#2E6A5E', edge='#4A9A86', vein='#9FDCCB',
                    twig='#4A4A40', aged='#5A6A4A', leaf=G(shape='fan', veins=14, slant=.05, rough=.30)),
    'ef_moss':    G(layout='beard', n=7, len=.1, wratio=.1, size_m=.60, top='#8A9A6E', edge='#B8C49A', vein='#6A7A50', twig='#6A7A50',
                    aged='#9A9A70', leaf=G(shape='lance')),
    'ef_fern':    G(layout='pinnate', n=20, len=.34, wratio=.20, spread=75, size_m=.55, top='#2A6A4A', edge='#4A8A5C', vein='#6FA880',
                    twig='#3E4E30', aged='#7A7A40', leaf=G(shape='lance', skew=.9, serr=.3, teeth=24, veins=8, rough=.42)),
    # ------------------------------------------------------------------ MOUNTAIN KINGDOM (R-03)
    'mk_spruce':  G(layout='needle_flat', n=34, nlen=.05, nw=.008, nang=55, side=7, spread=55, len=.40, wratio=.3, size_m=.50,
                    top='#1F3F33', edge='#3C5E4C', vein='#203A30', twig='#5A4434', aged='#6A6A3E', leaf=G(shape='lance')),
    'mk_birch':   G(layout='alternate', n=9, len=.20, wratio=.62, spread=55, petiole=.18, size_m=.32, top='#4A7A34', edge='#76A050',
                    vein='#9EC07A', twig='#5A3A30', aged='#C8A040', leaf=G(shape='elliptic', pw=.6, serr=.12, teeth=30, veins=8, rough=.38)),
    'mk_krumm':   G(layout='needle_bundle', n=22, nlen=.18, nw=.0055, ndroop=-.03, side=5, spread=45, len=.25, wratio=.3, size_m=.45,
                    top='#3A5E3A', edge='#6A8A5A', vein='#2E4A2E', twig='#6A4A34', aged='#8A8A50', leaf=G(shape='lance')),
    'mk_juniper': G(layout='scale', n=40, nlen=.04, nw=.008, side=8, spread=50, len=.36, wratio=.3, size_m=.30, top='#3E5E4E',
                    edge='#7E9A8A', vein='#2A4A3A', twig='#6A4A3A', aged='#7A7A4A', leaf=G(shape='lance')),
    'mk_rhodo_dwarf': G(layout='rosette', n=8, len=.30, wratio=.38, fan=300, size_m=.20, top='#3A5A34', edge='#5A7A46', vein='#8AA070',
                        twig='#6A4A3A', aged='#7A7A48', leaf=G(shape='elliptic', pw=.6, veins=6, rough=.35),
                        flower=G(n=16, size=.06, spread=.12, col='#F2C4CF', centre='#E8D27A')),
}


def build(name):
    A = ATLASES[name]; rng = np.random.default_rng(abs(hash(name)) % (2 ** 31) if False else sum(map(ord, name)) * 7919)
    C = np.zeros((2 * TILE, 2 * TILE, 4), np.uint8); NOR = np.zeros((2 * TILE, 2 * TILE, 3), np.uint8)
    RO = np.zeros((2 * TILE, 2 * TILE), np.uint8)
    seed = rng.integers(1 << 30)
    z0 = A.get('zoom', 1.0)                                         # keep the previous card size when the spray still fits
    for z in sorted({z0} | {z for z in (1.0, 1.12, 1.25, 1.4, 1.6, 1.85) if z >= z0}):
        tiles = []
        for var in range(4):
            T = spray(Tile(np.random.default_rng(seed + var), z), A, var); tiles.append(T)
        b = int(.012 * N)
        edge = max(max(T.A[:b].max(), T.A[:, :b].max(), T.A[:, -b:].max()) for T in tiles)
        if A['layout'] == 'beard':
            edge = max(max(T.A[-b:].max(), T.A[:, :b].max(), T.A[:, -b:].max()) for T in tiles)
        if edge == 0:
            break
    A['zoom'] = z
    for var, T in enumerate(tiles):
        col = lin2srgb(T.C); a = T.A
        # height → normal (OpenGL: +Y up). Blur the height a little so the normal map is smooth.
        Hs = gaussian_filter(T.H, 1.2 * SS)
        gy, gx = np.gradient(Hs)
        k = 9.0
        nx, ny = -gx * k, gy * k          # image rows go down, our Y goes up
        nz = np.ones_like(nx); ln = np.sqrt(nx * nx + ny * ny + nz * nz)
        nrm = np.stack([nx / ln, ny / ln, nz / ln], -1) * .5 + .5
        # dilate colour into transparent pixels (no dark halos with mip-mapping / filtering)
        rgba = np.concatenate([col, a[..., None]], -1)
        im = Image.fromarray((rgba * 255).astype(np.uint8), 'RGBA')
        bg = im.filter(ImageFilter.GaussianBlur(10 * SS)).convert('RGB')
        bgA = np.asarray(im.split()[3].filter(ImageFilter.GaussianBlur(10 * SS)), np.float32)[..., None] / 255
        fill = np.asarray(bg, np.float32) / 255 / np.maximum(bgA, 1e-3)
        fill = np.clip(fill, 0, 1); fill = np.where(bgA > 1e-3, fill, np.mean(col[a > .5], 0) if (a > .5).any() else .2)
        rgb = np.where(a[..., None] > 0, col, fill)
        tile = Image.fromarray((np.concatenate([rgb, a[..., None]], -1) * 255).astype(np.uint8), 'RGBA').resize((TILE, TILE), Image.LANCZOS)
        ntile = Image.fromarray((nrm * 255).astype(np.uint8)).resize((TILE, TILE), Image.LANCZOS)
        rtile = Image.fromarray((np.clip(T.R, 0, 1) * 255).astype(np.uint8)).resize((TILE, TILE), Image.LANCZOS)
        r0, c0 = (var // 2) * TILE, (var % 2) * TILE          # tile 0 = top-left in image = UV (0, .5)–(.5, 1)
        C[r0:r0 + TILE, c0:c0 + TILE] = np.asarray(tile); NOR[r0:r0 + TILE, c0:c0 + TILE] = np.asarray(ntile)
        RO[r0:r0 + TILE, c0:c0 + TILE] = np.asarray(rtile)
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(C, 'RGBA').save(os.path.join(OUT, f'{name}_col.png'), optimize=True)
    Image.fromarray(NOR).save(os.path.join(OUT, f'{name}_nor.png'), optimize=True)
    Image.fromarray(RO).save(os.path.join(OUT, f'{name}_rough.png'), optimize=True)
    bg = Image.new('RGBA', (2 * TILE, 2 * TILE), (214, 216, 212, 255)); bg.alpha_composite(Image.fromarray(C, 'RGBA'))
    bg.convert('RGB').resize((768, 768), Image.LANCZOS).save(os.path.join(OUT, f'{name}_prev.png'))
    print('ATLAS', name, 'zoom', z, flush=True)


if __name__ == '__main__':
    names = sys.argv[1:] or list(ATLASES)
    mp = os.path.join(OUT, 'atlases.json')
    old = json.load(open(mp)) if os.path.exists(mp) else {}
    for k, v in old.items():
        if k in ATLASES:                                   # previous zoom = starting card size (also for rebuilt atlases)
            ATLASES[k]['zoom'] = v.get('zoom', 1)
    for n in names:
        build(n)
    meta = {k: dict(size_m=round(v['size_m'] * v.get('zoom', 1), 3), zoom=v.get('zoom', 1), layout=v['layout'], tiles=4, pivot='bottom-centre' if v['layout'] not in ('beard', 'single') else
                    ('top-centre' if v['layout'] == 'beard' else 'centre')) for k, v in ATLASES.items()}
    json.dump(meta, open(os.path.join(OUT, 'atlases.json'), 'w'), indent=1)
    print('LEAFGEN_DONE', len(names))

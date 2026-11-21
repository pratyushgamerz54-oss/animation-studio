"""TASK 05 · MILESTONE 2 — detailed REGION sites outside the Ashram window (python3 + numpy + scipy + numba, NOT Blender).

Same approved map data (02_world/map/data, Aetheria C1 grid, 3 km cells) and the same TASK 04/05 height function
(t5_prep.height_t5) — each region gets its own LOCAL frame (origin = site centre, metres) so float32 meshes stay precise.
  region R04  Western Desert & Wastelands — dunes (wind-shaped), rock mesas, canyons along the map's drainage lines,
              dry valleys / playas with cracked ground, desert pavement.
Tiles per region: H (hero, ~2 m) · N (near, ~20 m) · F (far, ~300 m) — nested, border-blended onto the parent (seamless).
Writes 06_DESERTS/data_v002/<tile>.npz + region_<key>.json.          Usage: python3 t5_region_prep.py R04
"""
import os, sys, json, math, time
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t5_prep as P
import t5_field as F
import t5_noise as N
import t5_erosion as E
sstep = F.sstep
ROOT = P.ROOT

REGIONS = {
    'R04': dict(name='Western Desert & Wastelands', folder='06_DESERTS', cell=(150.0, 498.0),
                tiles={'DF': dict(half=60000, sp=300.0, parent=None, band=8000),
                       'DN': dict(half=12000, sp=20.0, parent='DF', band=1500),
                       'DH': dict(half=1500, sp=2.0, parent='DN', band=150)},
                wind_deg=280.0),        # prevailing wind FROM the west (slip faces face east) — proposal
}


def frame(reg):
    """region centre in the Ashram-local frame (metres)."""
    cx, cy = F.to_local(np.array(reg['cell'][0]), np.array(reg['cell'][1]))
    return float(cx), float(cy)


# ------------------------------------------------------------------ drainage lines (the map's own flow network) in the window
def drainage(reg, half):
    import worldgen as wg
    OX, OY = frame(reg)
    down, _ = wg.flow(F.oF, F.osea)
    c0, r0 = F.to_cell(OX - half, OY + half); c1, r1 = F.to_cell(OX + half, OY - half)
    c0, c1, r0, r1 = int(c0) - 2, int(c1) + 3, int(r0) - 2, int(r1) + 3
    win = np.zeros_like(F.osea); win[max(r0, 0):r1, max(c0, 0):c1] = True
    riv = (~F.osea) & (F.oacc > 8) & ~F.ol & win                      # ≥ 8 cells = dry wadis too (desert)
    rv = riv.ravel(); up = np.zeros(rv.size, bool)
    for i in np.nonzero(rv)[0]:
        j = down[i]
        if j >= 0 and rv[j]:
            up[j] = True
    seen = np.zeros(rv.size, bool); out = []
    for hd in sorted([i for i in np.nonzero(rv)[0] if not up[i]], key=lambda i: -F.oF.ravel()[i]):
        p = []; i = hd
        while True:
            p.append(i)
            if seen[i]:
                break
            seen[i] = True
            j = down[i]
            if j < 0 or j == i or not rv[j]:
                if j >= 0 and j != i:
                    p.append(j)
                break
            i = j
        if len(p) < 3:
            continue
        rr, cc = np.divmod(np.array(p), F.OW)
        x, y = F.to_local(cc, rr)
        pts = np.stack([x - OX, y - OY], 1).astype(float)
        for _ in range(3):                                            # chaikin smoothing
            Q = [pts[0]]
            for a, b in zip(pts[:-1], pts[1:]):
                Q += [.75 * a + .25 * b, .25 * a + .75 * b]
            Q.append(pts[-1]); pts = np.array(Q)
        s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
        ss = np.arange(0, s[-1], 20.0)
        pts = np.stack([np.interp(ss, s, pts[:, 0]), np.interp(ss, s, pts[:, 1])], 1)
        k = len(pts)
        mean = N.fbm(ss, np.full(k, len(out) * 3.7), 2500, 3, 180) * 380 + N.fbm(ss, np.full(k, len(out) * 1.3), 500, 2, 181) * 60
        env = np.clip(ss / 2000, 0, 1) * np.clip((ss[-1] - ss) / 2000, 0, 1)
        t = np.gradient(pts, axis=0); t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
        pts = pts + np.stack([-t[:, 1], t[:, 0]], 1) * (mean * env)[:, None]
        acc = np.interp(ss, np.linspace(0, ss[-1], len(p)), F.oacc.ravel()[p].astype(float))
        z = P.height_t5(pts[:, 0] + OX, pts[:, 1] + OY)
        z = np.minimum.accumulate(np.maximum(z, 0))
        w = np.clip(8 + 10 * np.sqrt(acc / 40.0), 10, 160)
        wet = (acc > 150).astype(float)                               # large channels keep water; the rest = dry wadis (proposal)
        out.append(np.column_stack([pts, z, w, wet]))
    return out


# ------------------------------------------------------------------ desert shaping
def dunes(X, Y, wind_deg, sp):
    """asymmetric transverse dunes (gentle stoss, ~30° lee / slip face), crest lines curved by domain warping. metres."""
    th = math.radians(wind_deg + 180)                                  # direction the wind blows TO
    ux, uy = math.sin(th), math.cos(th)
    out = np.zeros_like(X)
    for lam, amp, seed in ((900.0, 48.0, 190), (260.0, 8.0, 191), (60.0, 1.4, 192)):
        if lam < 3 * sp:
            continue
        wx, wy = N.warp(X, Y, lam * 2.5, lam * .25, seed)
        ph = (wx * ux + wy * uy) / lam + N.fbm(X, Y, lam * 4, 2, seed + 5) * .35
        f = ph - np.floor(ph)
        prof = np.where(f < .78, f / .78, (1 - f) / .22)               # rise 78 %, slip face 22 %
        prof = prof ** 1.4                                             # sharper crests
        out += (prof - .4) * amp * (.55 + .45 * N.fbm(X, Y, lam * 3, 2, seed + 9))
    return out


def mesas(X, Y, z0, sp):
    """rock tablelands / buttes / inselbergs: terraced, flat-topped, steep walls (strata)."""
    n_ = N.fbm(X, Y, 2600, 4, 200) + N.fbm(X, Y, 700, 3, 201) * .22
    m = sstep(.30, .34, n_)                                            # sharp plateau rims (steep walls), buttes + tablelands
    top = 230 + N.fbm(X, Y, 3000, 2, 202) * 90
    h = m * top
    st = 24.0
    t = h / st; fr = t - np.floor(t)
    h = (np.floor(t) + sstep(.8, 1.0, fr)) * st                        # terraces (ledges every ~18 m)
    return h, m


def build(rkey, tkey):
    t0 = time.time(); reg = REGIONS[rkey]; t = reg['tiles'][tkey]; OX, OY = frame(reg)
    sp, half = t['sp'], t['half']
    n = int(round(2 * half / sp)) + 1
    g = np.linspace(-half, half, n); X, Y = np.meshgrid(g, g[::-1])
    AX_, AY_ = X + OX, Y + OY
    z0 = P.height_t5(AX_.ravel(), AY_.ravel()).reshape(n, n)
    c, r = F.to_cell(AX_, AY_)
    wx = AX_ + N.fbm(AX_, AY_, 6000, 3, 30) * 2600; wy = AY_ + N.fbm(AX_, AY_, 6000, 3, 32) * 2600
    cw, rw = F.to_cell(wx, wy)
    bi = F.ob[np.clip(np.round(rw).astype(int), 0, F.OH - 1), np.clip(np.round(cw).astype(int), 0, F.OW - 1)]
    DES = ndi.gaussian_filter((F.ob == 5).astype(float), .8); WAS = ndi.gaussian_filter((F.ob == 6).astype(float), .8)
    des = sstep(.4, .6, ndi.map_coordinates(DES, [rw, cw], order=1, mode='nearest'))
    was = sstep(.4, .6, ndi.map_coordinates(WAS, [rw, cw], order=1, mode='nearest'))
    sea = z0 <= 0
    # ---- detail: mesas (wasteland + scattered in the desert), dunes (desert sand seas), small relief
    mh, mm = mesas(AX_, AY_, z0, sp)
    mesa_amt = np.clip(was * .9 + des * .35, 0, 1) * (~sea)
    dn = dunes(AX_, AY_, reg['wind_deg'], sp)
    sandsea = des * sstep(-.05, .25, N.fbm(AX_, AY_, 9000, 3, 210)) * (1 - mm) * (~sea)
    d = mh * mesa_amt + dn * sandsea + N.fbm(AX_, AY_, 300, 3, 211) * 3 * (1 - sandsea) * P.bl(sp, 300)
    ze = z0 + d
    flow = np.zeros_like(ze); scree = np.zeros_like(ze)
    if sp >= 15:                                                       # gullies on the mesa walls, talus aprons below
        H, fl = E.hydraulic(ze / sp, .8 * ze.size, 41, 2, erode=.3, deposit=.25, capacity=4.0)
        ze = ze + ndi.gaussian_filter(H * sp - ze, 1.0) * (1 - sandsea); flow = fl
        H2, dep = E.thermal(ze / sp, math.tan(math.radians(55)), 15, .25)
        ze = H2 * sp; scree = dep * sp
    # ---- drainage: canyons in the mesas, flat sandy wadi floors, water only in the big channels
    RV = drainage(reg, half + 3000)
    wet = np.zeros_like(ze); wadi = np.zeros_like(ze)
    if RV:
        R = np.concatenate(RV)
        dd, jj = cKDTree(R[:, :2]).query(np.column_stack([X.ravel(), Y.ravel()]), distance_upper_bound=6000)
        ok = np.isfinite(dd).reshape(n, n); jj = np.where(np.isfinite(dd), jj, 0).reshape(n, n); dd = np.where(np.isfinite(dd), dd, 1e9).reshape(n, n)
        if sp <= 25:
            dd = dd + N.fbm(X, Y, 80, 3, 220) * .25 * R[jj, 3]
        w = R[jj, 3]; zr = R[jj, 2]; wt = R[jj, 4]
        ri = np.maximum(w / 2, .75 * sp); bank = np.maximum(2.5 * w, 1.6 * sp)
        floor = zr - .6 - 1.5 * wt
        inner = ok & (dd < ri)
        ze = np.where(inner, np.minimum(ze, floor + (dd / ri) ** 2 * .8), ze)
        mid = ok & (dd >= ri) & (dd < ri + bank)
        tb = np.clip((dd - ri) / bank, 0, 1) ** 2.4                    # steep canyon walls where the ground is high (mesas)
        ze = np.where(mid & (ze > zr), zr + tb * (ze - zr), ze)
        wet = np.where(ok, (1 - sstep(ri, ri + bank * .3, dd)) * wt, 0)
        wadi = np.where(ok, 1 - sstep(ri * .8, ri + bank * .5, dd), 0) * (1 - wt)
    # ---- seamless border onto the parent tile
    if t['parent']:
        pt = reg['tiles'][t['parent']]; zp = np.load(os.path.join(ROOT, reg['folder'], 'data_v002', f"{t['parent']}.npz"))['z'].astype(float)
        np_ = zp.shape[0]
        cc = (X + pt['half']) / pt['sp']; rr = (pt['half'] - Y) / pt['sp']
        zpar = ndi.map_coordinates(zp, [rr.ravel(), cc.ravel()], order=1, mode='nearest').reshape(n, n)
        e = half - np.maximum(np.abs(X), np.abs(Y))
        wb = sstep(0, t['band'], e)
        ze = ze * wb + zpar * (1 - wb)
    # ---- masks (desert interpretation of the shared mask slots — see MAT_T5_TERRAIN_DESERT)
    gy, gx = np.gradient(ndi.gaussian_filter(ze, max(6.0 / sp, .01)), sp); slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    cliff = sstep(40, 58, slope)
    rock = np.maximum(sstep(26, 38, slope), cliff) * (1 - sandsea * .7)
    sand = np.clip(sandsea * 1.2, 0, 1) * (1 - cliff) + wadi * .6
    loc = ze - ndi.gaussian_filter(ze, 2000 / sp)                       # basins → playas with cracked mud
    playa = sstep(-6, -14, loc) * sstep(2, .8, slope) * (1 - sandsea) * (~sea)
    lf = np.log1p(flow) / max(np.log1p(flow).max(), 1e-9) if flow.max() > 0 else flow
    sc = np.clip(scree / max(np.percentile(scree[scree > 0], 95) if (scree > 0).any() else 1, 1e-6), 0, 1)
    pave = (1 - sand) * (1 - rock) * (1 - playa) * sstep(.0, .3, N.fbm(X + OX, Y + OY, 400, 2, 230) + .2)
    veg = wadi * sstep(.2, .5, N.fbm(X + OX, Y + OY, 120, 2, 231)) * (1 - sandsea)   # sparse shrubs in the wadis
    U = lambda a: np.clip(np.round(a * 255), 0, 255).astype(np.uint8)
    Z = np.zeros_like(ze)
    MA = np.stack([U(Z), U(rock), U(Z), U(np.maximum(wet, sea))], -1)            # forest, rock, snow, wet
    MB = np.stack([U(sand), U(playa), U(veg), U(sc)], -1)                        # dry→SAND, pad→PLAYA (cracked), grove→shrubs, scree
    MC = np.stack([U(pave), U(Z), U(lf), U(cliff)], -1)                          # gravel→PAVEMENT, path, flow, cliff
    os.makedirs(os.path.join(ROOT, reg['folder'], 'data_v002'), exist_ok=True)
    np.savez_compressed(os.path.join(ROOT, reg['folder'], 'data_v002', f'{tkey}.npz'), z=ze.astype(np.float32), MA=MA, MB=MB, MC=MC,
                        rect=np.array([-half, half, -half, half, sp]))
    st = dict(region=rkey, tile=tkey, shape=[n, n], spacing_m=sp, half_m=half, z_min=float(ze.min()), z_max=float(ze.max()),
              cover={k: float((v > .5).mean()) for k, v in (('sand', sand), ('rock', rock), ('playa', playa), ('cliff', cliff), ('wet', wet))},
              drainage_lines=len(RV), seconds=round(time.time() - t0, 1))
    print(json.dumps(st), flush=True)
    return st, RV


if __name__ == '__main__':
    rk = sys.argv[1] if len(sys.argv) > 1 else 'R04'
    reg = REGIONS[rk]; OX, OY = frame(reg)
    stats = []; RVs = None
    for tk_ in ('DF', 'DN', 'DH'):
        st, RV = build(rk, tk_)
        stats.append(st)
        if tk_ == 'DN':
            RVs = RV
    W = [r.astype(np.float32) for r in RVs]
    np.savez_compressed(os.path.join(ROOT, reg['folder'], 'data_v002', 'water.npz'), RIV=np.concatenate(W), RIVO=np.cumsum([0] + [len(a) for a in W]))
    meta = dict(region=rk, name=reg['name'], status='PROPOSAL — detailed terrain inside the approved map region (map rev 01 = proposal)',
                frame=f'local metres; origin = site centre = C1 cell {reg["cell"]} = Ashram-local ({OX:.0f}, {OY:.0f}) m; +X east, +Y north',
                origin_ashram_local_m=[OX, OY], tiles={k: dict(v) for k, v in reg['tiles'].items()}, stats=stats, wind_deg=reg['wind_deg'],
                notes=['dunes / mesas / playas are procedural detail inside the map\'s desert + wasteland biomes',
                       'drainage = the map\'s own flow network; channels with > 150 cells keep water, smaller ones are dry wadis (PROPOSAL)'])
    json.dump(meta, open(os.path.join(ROOT, reg['folder'], 'data_v002', f'region_{rk}.json'), 'w'), indent=1)
    print('T5_REGION_PREP_DONE', rk)

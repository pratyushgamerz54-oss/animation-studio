"""t6kit_m2 — TASK 06 milestone 2 additions to the vegetation toolkit (Blender 4.5): palm generator (date palm, coconut palm),
palm material set (bark scan / frond / dead frond / nut). Uses t6kit (same Geo / Branch / tube / wind attributes)."""
import math
import numpy as np
import bpy
from mathutils import Vector
import t6kit as K
from t6kit import Geo, Branch, perp, rot_about, UP


def leaflet(G, base, d, side, length, width, droop, segs, mi, attrs, rng):
    """palm leaflet: tapered strip with a V-fold along the midrib, droops at the tip; grad 0 → 1 along the leaflet."""
    d = Vector(d).normalized(); side = (side - d * side.dot(d)).normalized(); nrm = d.cross(side).normalized()
    if nrm.z < 0:
        nrm = -nrm
    rows = []; p = Vector(base); fold = rng.uniform(.15, .35)
    for i in range(segs + 1):
        t = i / segs
        w = width * (math.sin(math.pi * min(.97, .12 + .88 * t)) ** .6) * (1 - .6 * t)
        a = dict(attrs); a['wind_leaf'] = t; a['grad'] = t
        rows.append(G.add_verts([p - side * w / 2 + nrm * w * fold, p, p + side * w / 2 + nrm * w * fold], **a))
        d = (d - Vector((0, 0, droop)) / segs).normalized()
        p = p + d * length / segs
    for i in range(segs):
        r0, r1 = rows[i], rows[i + 1]; v0, v1 = i / segs, (i + 1) / segs
        G.add_face((r0, r0 + 1, r1 + 1, r1), ((0, v0), (.5, v0), (.5, v1), (0, v1)), mi)
        G.add_face((r0 + 1, r0 + 2, r1 + 2, r1 + 1), ((.5, v0), (1, v0), (1, v1), (.5, v1)), mi)


def build_palm(S, seed=0, collection=None, mats=None):
    """S['palm'] = dict(lean, curve, r0, rtop, flare, ring, fronds, frond_len, droop, elev=(lo, hi), pinnae, pinna_len, pinna_w,
    v_angle (+ = stiff V up like date palm, − = drooping like coconut), pinna_droop, dead)."""
    rng = np.random.default_rng(S.get('seed', 1) * 1000 + seed)
    P = S['palm']; Htot = S['height'] * rng.uniform(.93, 1.07)
    H = Htot - P['frond_len'] * .72 * math.sin(math.radians(P['elev'][1]))        # design height = overall (crown top), trunk shorter
    lean = math.radians(P.get('lean', 4) * rng.uniform(.6, 1.4)); az = rng.uniform(0, 2 * np.pi); n = P.get('segs', 32)
    pts, rad = [], []
    for i in range(n + 1):
        t = i / n; z = -.35 + (H + .35) * t
        off = math.tan(lean) * H * (t ** P.get('curve', 1.5))
        pts.append(Vector((math.cos(az) * off + .03 * math.sin(t * 9), math.sin(az) * off, z)))
        rad.append(P['r0'] + (P['rtop'] - P['r0']) * t ** .7)
    trunk = Branch(pts, rad, 0, rng.random(), 0.0, kind='trunk')
    St = dict(S); St['trunk'] = dict(flare=P.get('flare', .25), flare_h=P.get('flare_h', .03), lobes=0, nodes=P.get('ring', .12))
    G = Geo()
    K.tube(G, trunk, P.get('tsides', 16), S['bark'].get('tile', 1.0), St, H, rng)     # tsides / lsegs: LOD
    top = pts[-1]; nf = P['fronds']; wt_top = 1.0
    golden = math.radians(137.5)
    for f in range(nf + P.get('dead', 0)):
        dead = f >= nf
        if dead:
            e = math.radians(rng.uniform(-85, -62)); L = P['frond_len'] * rng.uniform(.6, .85)
        else:
            u = f / max(nf - 1, 1); e = math.radians(P['elev'][1] + (P['elev'][0] - P['elev'][1]) * u + rng.normal(0, 6))
            L = P['frond_len'] * rng.uniform(.8, 1.08) * (.75 + .25 * min(1, u * 2))
        a_ = f * golden + rng.normal(0, .15)
        d0 = Vector((math.cos(a_) * math.cos(e), math.sin(a_) * math.cos(e), math.sin(e)))
        fp, fr = K.grow(rng, top - Vector((0, 0, .15)), d0, L, .05, .012, 12, grav=P.get('droop', -.8) * (1.6 if dead else 1.0),
                        wander=math.radians(2))
        ph = rng.random(); mi_r = 2 if dead else 1
        fb = Branch(fp, fr, 2, ph, 0.0)
        # rachis tube (own attributes: the whole frond follows the trunk top + bends as a branch)
        k = 5; rings = []
        for i, p in enumerate(fp):
            tt = i / (len(fp) - 1)
            d = (fp[min(i + 1, len(fp) - 1)] - fp[max(i - 1, 0)]).normalized(); nv = perp(d); bv = d.cross(nv)
            ring = [p + (nv * math.cos(a) + bv * math.sin(a)) * fr[i] for a in np.linspace(0, 2 * np.pi, k, endpoint=False)]
            rings.append(G.add_verts(ring, wind_trunk=wt_top, wind_branch=.9 * tt ** 1.3, wind_phase=ph, leaf_rand=ph, grad=.2))
        for i in range(len(rings) - 1):
            for j in range(k):
                j1 = (j + 1) % k; a0, a1 = rings[i], rings[i + 1]
                G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k, i / 12), ((j + 1) / k, i / 12), ((j + 1) / k, (i + 1) / 12), (j / k, (i + 1) / 12)), mi_r)
        npn = P['pinnae'] if not dead else int(P['pinnae'] * .6)
        for j in range(2, npn):
            t = j / npn; p, d, r = fb.at(t)
            side = d.cross(UP)
            if side.length < 1e-3:
                side = perp(d)
            side.normalize(); up_l = side.cross(d).normalized()
            if up_l.z < 0:
                up_l = -up_l
            plen = P['pinna_len'] * (math.sin(math.pi * (.08 + .9 * t)) ** .55) * rng.uniform(.85, 1.1)
            for sgn in (-1, 1):
                if dead and rng.random() < .35:
                    continue                                      # dead fronds lose leaflets
                dirv = (side * sgn * .85 + d * .45 + up_l * P.get('v_angle', .3)).normalized()
                attrs = dict(wind_trunk=wt_top, wind_branch=.9 * t ** 1.3 + .15, wind_phase=ph, leaf_rand=rng.random(), grad=0.0)
                leaflet(G, p, dirv, d, plen, P['pinna_w'] * rng.uniform(.85, 1.15), P.get('pinna_droop', .3) * (2.2 if dead else 1),
                        P.get('lsegs', 4), mi_r, attrs, rng)
    top_z = max(float(v[:, 2].max()) for v in G.V); f = 1.0
    if top_z > Htot * 1.10 or top_z < Htot * .90:                  # keep within ±10 % of the design height (as build_tree)
        f = Htot / top_z; G.V = [v * f for v in G.V]; top = top * f
    for k_ in range(P.get('nuts', 0)):                     # coconut clusters hanging just below the crown (slot 3)
        a_ = rng.uniform(0, 2 * np.pi); rr = P['rtop'] * rng.uniform(1.3, 2.2)
        c = top + Vector((math.cos(a_) * rr, math.sin(a_) * rr, -rng.uniform(.25, .7)))
        R = rng.uniform(.11, .14)
        prof = [(R * .05, -R * 1.15), (R * .7, -R * .9), (R, -R * .2), (R * .92, R * .5), (R * .5, R * .95), (R * .03, R * 1.05)]
        K.lathe(G, prof, c, Vector((rng.normal(0, .3), rng.normal(0, .3), 1)).normalized(), 12, 3,
                dict(wind_trunk=wt_top, wind_branch=.05, wind_leaf=0.0, wind_phase=rng.random(), leaf_rand=rng.random(), grad=.5),
                wobble=.06, seed=int(rng.integers(1 << 30)))
    me = G.to_mesh(S['name'], mats or [])
    o = bpy.data.objects.new(S['name'], me)
    if collection is not None:
        collection.objects.link(o)
    bb = np.array([v.co[:] for v in me.vertices])
    st = dict(height_m=round(float(bb[:, 2].max()), 2), canopy_x_m=round(float(np.ptp(bb[:, 0])), 2), canopy_y_m=round(float(np.ptp(bb[:, 1])), 2),
              trunk_d_m=round(2 * P['r0'] * (1 + P.get('flare', .25)), 2), branches=nf + P.get('dead', 0), leaf_cards=0,
              tris=sum(len(p.vertices) - 2 for p in me.polygons), verts=len(me.vertices), lowest_z=round(float(bb[:, 2].min()), 2), height_scale=round(f, 3))
    for k_, v in st.items():
        o[f't6_{k_}'] = v
    return o, st


def palm_mats(S):
    nm = S['name']; B = S['bark']; C = S.get('frond_cols', [(0, '#2E4A1E'), (.6, '#4E7A30'), (1, '#7A9A4A')])
    bark = K.mat_bark(f'MAT_T6_{nm}_BARK', B['tex'], B.get('tint', '#FFFFFF'), B.get('moss', 0), lichen=B.get('lichen', 0))
    frond = K.mat_simple(f'MAT_T6_{nm}_FROND', C[1][1], rough=.5, attr_grad='grad', grad_cols=C, transl=.3, spec=.35)
    dead = K.mat_simple(f'MAT_T6_{nm}_DEADFROND', '#8A7450', rough=.8, attr_grad='grad',
                        grad_cols=[(0, '#5A4A32'), (.6, '#8A7450'), (1, '#A89068')], transl=.15)
    nut = K.mat_simple(f'MAT_T6_{nm}_NUT', '#7A6A2A', rough=.55, var_col='#5A6A2A', var_scale=8.0)
    return [bark, frond, dead, nut]

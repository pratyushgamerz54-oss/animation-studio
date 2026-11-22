"""TASK 06 · small-plant generators (grass, wildflowers, ferns, aquatic, moss, fungi, alpine) — real geometry, Blender 4.5.

Every plant = ONE object, origin at the ground point, real-world size, UVs, wind attributes (same names as trees, see t6kit),
material slots listed in PLANTS[...]['mats']. Grass blades / petals / leaves are geometry (not cards) so close-ups hold up;
ferns and the kans-grass plume use their species atlas cards.
"""
import math
import numpy as np
import bpy
from mathutils import Vector
import t6kit as K
from t6kit import Geo, perp, rot_about, UP

SI, PF = 'SPECIES-INSPIRED', 'FANTASY (APPROVED R-02)'


# ====================================================================== primitives
def blade(G, base, d, h, w, bend, segs, mi, rng, wphase, twist=0.0, curl=0.0, tipw=.05, grad0=0.0):
    """grass / reed / leaf blade: strip of quads, width profile, bends with gravity. grad 0 root → 1 tip."""
    d = Vector(d).normalized(); side = perp(d)
    side = Vector((side.x, side.y, 0)).normalized() if abs(d.z) > .3 else side
    p = Vector(base); rows = []; ds = h / segs
    for i in range(segs + 1):
        t = i / segs
        ww = w * (1 - t) ** .6 * (1 - tipw) + w * tipw * (1 - t) if t < 1 else 0.0
        ww = max(ww, w * .02)
        s_ = rot_about(side, d, twist * t)
        nrm = d.cross(s_).normalized()
        a = p - s_ * ww / 2 + nrm * curl * ww; b_ = p + s_ * ww / 2 + nrm * curl * ww
        g = grad0 + (1 - grad0) * t
        rows.append(G.add_verts([a, p, b_], wind_trunk=0.0, wind_branch=t ** 1.5 * h * .6, wind_leaf=t ** 2, wind_phase=wphase,
                                leaf_rand=wphase, grad=g))
        d = (d + Vector((0, 0, -bend)) * (1.0 / segs)).normalized()
        p = p + d * ds
    for i in range(segs):
        r0, r1 = rows[i], rows[i + 1]; v0, v1 = i / segs, (i + 1) / segs
        G.add_face((r0, r0 + 1, r1 + 1, r1), ((0, v0), (.5, v0), (.5, v1), (0, v1)), mi)
        G.add_face((r0 + 1, r0 + 2, r1 + 2, r1 + 1), ((.5, v0), (1, v0), (1, v1), (.5, v1)), mi)
    return p, d


def stem(G, pts, r0, r1, k, mi, wphase, h_ref):
    """thin tube along a polyline."""
    n = len(pts); T = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
    nv = perp(T[0]); rings = []
    for i in range(n):
        nv = (nv - T[i] * nv.dot(T[i])).normalized(); bv = T[i].cross(nv)
        r = r0 + (r1 - r0) * i / (n - 1)
        ring = [pts[i] + (nv * math.cos(a) + bv * math.sin(a)) * r for a in np.linspace(0, 2 * np.pi, k, endpoint=False)]
        t = i / (n - 1)
        rings.append(G.add_verts(ring, wind_trunk=0.0, wind_branch=(max(pts[i].z, 0) / max(h_ref, .01)) ** 1.5 * h_ref * .5,
                                 wind_leaf=0.0, wind_phase=wphase, leaf_rand=wphase, grad=t))
    for i in range(n - 1):
        for j in range(k):
            j1 = (j + 1) % k; a0, a1 = rings[i], rings[i + 1]
            G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k, i / n), ((j + 1) / k, i / n), ((j + 1) / k, (i + 1) / n), (j / k, (i + 1) / n)), mi)


def curve_pts(base, d, length, segs, grav, rng, wander=.05):
    pts = [Vector(base)]; d = Vector(d).normalized()
    for i in range(segs):
        d = (d + Vector((0, 0, grav)) / segs + Vector(rng.normal(0, wander, 3))).normalized()
        pts.append(pts[-1] + d * length / segs)
    return pts, d


def petal(G, base, out, up, L, W, cup, mi, wphase, h_ref, shape='oval', segs=4, droop=0.0, rough_edge=0.0, rng=None, grad=1.0):
    """petal / small leaf as real geometry: fan of rows along `out`, width profile by shape, cupped towards `up`."""
    out = Vector(out).normalized(); up = Vector(up).normalized(); side = out.cross(up).normalized(); up = side.cross(out).normalized()
    rows = []
    for i in range(segs + 1):
        t = i / segs
        if shape == 'oval':
            w = math.sin(math.pi * min(.98, .08 + .92 * t)) ** .7
        elif shape == 'obovate':
            w = math.sin(math.pi * min(.98, .05 + .95 * t) ** 1.4) ** .6
        elif shape == 'lance':
            w = math.sin(math.pi * t) ** .9
        elif shape == 'round':
            w = math.sqrt(max(0, 1 - (2 * t - 1) ** 2))
        elif shape == 'trumpet':
            w = .25 + .75 * t ** 1.5
        else:
            w = math.sin(math.pi * t)
        w = max(w, .04) * W / 2
        if rough_edge and rng is not None:
            w *= 1 + rng.uniform(-rough_edge, rough_edge)
        c = base + out * L * t + up * (cup * L * t * t - droop * L * t ** 3)
        pts = [c - side * w + up * cup * w * .6, c, c + side * w + up * cup * w * .6]
        rows.append(G.add_verts(pts, wind_trunk=0.0, wind_branch=(max(c.z, 0) / max(h_ref, .01)) * h_ref * .5, wind_leaf=t,
                                wind_phase=wphase, leaf_rand=wphase, grad=grad * t))
    for i in range(segs):
        r0, r1 = rows[i], rows[i + 1]; v0, v1 = i / segs, (i + 1) / segs
        G.add_face((r0, r0 + 1, r1 + 1, r1), ((0, v0), (.5, v0), (.5, v1), (0, v1)), mi)
        G.add_face((r0 + 1, r0 + 2, r1 + 2, r1 + 1), ((.5, v0), (1, v0), (1, v1), (.5, v1)), mi)


def dome(G, c, r, h, k, mi, wphase, rings=4, flat_bottom=True):
    prof = [(r * math.cos(a), h * math.sin(a)) for a in np.linspace(0, np.pi / 2, rings + 1)]
    prof[-1] = (r * .02, h)
    attrs = dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=.3, wind_phase=wphase, leaf_rand=wphase, grad=1.0)
    K.lathe(G, prof, c, UP, k, mi, attrs)


def flower(G, c, axis, n, L, W, cup, mi_petal, mi_centre, wphase, h_ref, shape='oval', centre_r=None, layers=1, droop=0.0, rng=None,
           centre_h=None):
    axis = Vector(axis).normalized(); ref = perp(axis)
    for ly in range(layers):
        for i in range(n):
            a = 2 * np.pi * (i + ly * .5) / n
            out = rot_about(ref, axis, a)
            out = (out * math.cos(math.radians(8 + ly * 18)) + axis * math.sin(math.radians(8 + ly * 18))).normalized()
            petal(G, c + axis * .002 * ly, out, axis, L * (1 - .15 * ly), W, cup + .1 * ly, mi_petal, wphase, h_ref, shape, droop=droop, rng=rng)
    if centre_r:
        prof = [(centre_r, 0), (centre_r * .9, (centre_h or centre_r * .5) * .6), (centre_r * .4, centre_h or centre_r * .5), (.0005, (centre_h or centre_r * .5) * 1.05)]
        K.lathe(G, prof, c, axis, 10, mi_centre, dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=.2, wind_phase=wphase, leaf_rand=wphase, grad=1.0))


def card_at(G, p, axis, size, mi, rng, wphase, up_hint=UP, bend=0.0):
    """leaf-atlas card (fern frond segment / plume): pivot = bottom centre, folded, random tile."""
    axis = Vector(axis).normalized(); side = axis.cross(up_hint)
    if side.length < 1e-4:
        side = perp(axis)
    side.normalize(); side = rot_about(side, axis, rng.normal(0, .25)); nrm = side.cross(axis).normalized()
    if nrm.z < 0:
        side, nrm = -side, -nrm
    var = int(rng.integers(4)); u0, v0 = K.tile_uv(var); fold = .2; hw = size / 2
    lb = p - side * hw * math.cos(fold) + nrm * hw * math.sin(fold); rb = p + side * hw * math.cos(fold) + nrm * hw * math.sin(fold)
    top = axis * size + Vector((0, 0, -bend * size))
    a = G.add_verts([lb, p, rb], wind_branch=max(p.z, 0) * .5, wind_leaf=0.0, wind_phase=wphase, leaf_rand=rng.random())
    c = G.add_verts([lb + top, p + top, rb + top], wind_branch=max(p.z, 0) * .5 + .3, wind_leaf=1.0, wind_phase=wphase, leaf_rand=rng.random())
    G.add_face((a, a + 1, c + 1, c), ((u0, v0), (u0 + .25, v0), (u0 + .25, v0 + .5), (u0, v0 + .5)), mi)
    G.add_face((a + 1, a + 2, c + 2, c + 1), ((u0 + .25, v0), (u0 + .5, v0), (u0 + .5, v0 + .5), (u0 + .25, v0 + .5)), mi)
    return p + top, axis


def rand_dir(rng, spread_deg, up=UP):
    a = rng.uniform(0, 2 * np.pi); s = math.radians(spread_deg) * math.sqrt(rng.random())
    return Vector((math.cos(a) * math.sin(s), math.sin(a) * math.sin(s), math.cos(s)))


# ====================================================================== plant builders
def grass_tuft(G, rng, P):
    for i in range(P['blades']):
        r = P['radius'] * math.sqrt(rng.random()); a = rng.uniform(0, 2 * np.pi)
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.01))
        d = rand_dir(rng, P['spread']) + Vector((math.cos(a), math.sin(a), 0)) * P.get('splay', .2) * r / max(P['radius'], 1e-3)
        h = P['h'] * rng.uniform(.55, 1.1)
        mi = 0 if rng.random() > P.get('dry', 0) else 1
        blade(G, base, d, h, P['w'] * rng.uniform(.7, 1.2), P['bend'] * rng.uniform(.6, 1.4), P.get('segs', 5), mi, rng, rng.random(),
              twist=rng.normal(0, .6), curl=P.get('curl', .15))
    for i in range(P.get('plumes', 0)):          # flowering stalks with plume cards (kans grass)
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * .5 * math.sqrt(rng.random())
        base = Vector((math.cos(a) * r, math.sin(a) * r, 0)); d = rand_dir(rng, 12)
        pts, dd = curve_pts(base, d, P['h'] * rng.uniform(1.0, 1.25), 8, -.1, rng, .02)
        stem(G, pts, .006, .003, 4, 1, rng.random(), P['h'])
        card_at(G, pts[-1], (dd + Vector((0, 0, .3))).normalized(), P['plume_size'] * rng.uniform(.8, 1.2), 2, rng, rng.random(), bend=.15)


def herb(G, rng, P):
    """basal rosette / leafy stem + flower heads."""
    H = P['h']
    for i in range(P.get('basal', 0)):          # basal leaves
        a = 2 * np.pi * i / P['basal'] + rng.normal(0, .2)
        out = Vector((math.cos(a), math.sin(a), rng.uniform(.25, .6))).normalized()
        petal(G, Vector((0, 0, .005)), out, UP, P['leaf_l'] * rng.uniform(.75, 1.1), P['leaf_w'], .12, 0, rng.random(), H,
              P.get('leaf_shape', 'oval'), segs=5, droop=P.get('leaf_droop', .25), rng=rng, rough_edge=P.get('leaf_rough', 0))
    for s in range(P['stems']):
        d = rand_dir(rng, P.get('spread', 15)); h = H * rng.uniform(.75, 1.05)
        pts, dd = curve_pts(Vector((rng.normal(0, .01), rng.normal(0, .01), 0)), d, h, 8, P.get('stem_grav', -.05), rng, .03)
        stem(G, pts, P.get('stem_r', .0025), P.get('stem_r', .0025) * .7, 5, 0 if P.get('stem_mat', 0) == 0 else P['stem_mat'], rng.random(), H)
        for j in range(P.get('stem_leaves', 0)):
            q = pts[2 + j % (len(pts) - 4)]; a = rng.uniform(0, 2 * np.pi)
            petal(G, q, Vector((math.cos(a), math.sin(a), .5)), UP, P['leaf_l'] * .6, P['leaf_w'] * .6, .1, 0, rng.random(), H,
                  P.get('leaf_shape', 'oval'), segs=3, droop=.2)
        top = pts[-1]; F = P['flower']
        if F['type'] == 'radial':
            flower(G, top, (dd + UP).normalized(), F['n'], F['L'], F['W'], F['cup'], 1, 2, rng.random(), H, F.get('shape', 'oval'),
                   F.get('centre'), F.get('layers', 1), F.get('droop', 0), rng, F.get('centre_h'))
        elif F['type'] == 'ball':               # primula: ball of florets
            for k in range(F['n']):
                v = Vector(rng.normal(0, 1, 3)).normalized()
                if v.z < -.3:
                    v.z = -v.z
                c = top + v * F['R']
                flower(G, c, v, 5, F['L'], F['W'], .15, 1, 2, rng.random(), H, 'obovate', F['L'] * .25, 1, 0, rng)
        elif F['type'] == 'pompom':             # marigold
            for ly in range(F['layers']):
                n = F['n'] - ly * 3
                for k in range(n):
                    a = 2 * np.pi * k / n + ly * .4
                    out = Vector((math.cos(a), math.sin(a), .2 + ly * .45)).normalized()
                    petal(G, top + UP * .004 * ly, out, UP, F['L'] * (1 - .12 * ly), F['W'], .3, 1, rng.random(), H, 'obovate', rng=rng,
                          rough_edge=.15)
            dome(G, top, F['L'] * .3, F['L'] * .25, 8, 2, rng.random())
        elif F['type'] == 'trumpet':            # gentian: upright trumpet + 5 lobes
            ax = (dd + UP * 2).normalized(); L = F['L']
            prof = [(L * .08, 0), (L * .16, L * .3), (L * .26, L * .7), (L * .34, L)]
            K.lathe(G, prof, top, ax, 10, 1, dict(wind_trunk=0.0, wind_branch=.05, wind_leaf=.4, wind_phase=rng.random(), leaf_rand=rng.random(), grad=1.0))
            ref = perp(ax)
            for k in range(5):
                out = rot_about(ref, ax, 2 * np.pi * k / 5)
                petal(G, top + ax * L + out * L * .3, (out + ax * .3).normalized(), ax, L * .3, L * .32, .1, 1, rng.random(), H, 'round')
        elif F['type'] == 'star':               # edelweiss: woolly bracts in a star + small heads
            flower(G, top, (dd + UP * 2).normalized(), F['n'], F['L'], F['W'], .05, 1, 2, rng.random(), H, 'lance', None, 1, 0, rng)
            for k in range(6):
                v = Vector((rng.normal(0, 1), rng.normal(0, 1), 0)).normalized() * F['L'] * .18
                dome(G, top + v + UP * .002, F['L'] * .1, F['L'] * .08, 6, 2, rng.random(), rings=2)
        if F.get('nod'):
            pass


def fern(G, rng, P):
    """fern as real geometry: arching rachis tube + opposite pinnae (serrated lance leaflets) sized by a frond profile."""
    n = P['fronds']
    for i in range(n):
        a = 2 * np.pi * i / n + rng.normal(0, .25); el = math.radians(rng.uniform(*P['elev']))
        d = Vector((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el)))
        L = P['size'] * P['chain'] * rng.uniform(.75, 1.1); ph = rng.random()
        pts, dd = curve_pts(Vector((0, 0, 0)), d, L, 14, -P.get('arch', .45) * 2.2, rng, .01)
        stem(G, pts, P.get('rachis', .004), .0012, 4, 1, ph, L)
        npin = P.get('pinnae', 22)
        for j in range(2, npin):
            t = j / npin; q_i = t * (len(pts) - 1); k = min(int(q_i), len(pts) - 2); f = q_i - k
            q = pts[k].lerp(pts[k + 1], f); tang = (pts[k + 1] - pts[k]).normalized()
            side = tang.cross(UP)
            if side.length < 1e-4:
                side = perp(tang)
            side.normalize(); up = side.cross(tang).normalized()
            if up.z < 0:
                up = -up
            prof = math.sin(math.pi * min(1, t * 1.15)) ** .8 * (1 - .25 * t)
            pl = L * P.get('pin_len', .16) * prof * rng.uniform(.9, 1.1)
            if pl < .01:
                continue
            for sgn in (-1, 1):
                out = (side * sgn + tang * .55 - up * .1).normalized()
                petal(G, q, out, up, pl, pl * P.get('pin_w', .28), .08, 0, ph, L, 'lance', segs=5, droop=.15, rng=rng,
                      rough_edge=P.get('serr', .25), grad=.4 + .6 * t)
    dome(G, Vector((0, 0, -.01)), P['size'] * .12, P['size'] * .08, 8, 1, 0.0, rings=2)


def lotus(G, rng, P):
    """floating + emergent pads (atlas 'single' pad tile), pink flower(s), seed pod. z = 0 is the WATER SURFACE."""
    for i in range(P['pads']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * math.sqrt(rng.random())
        c = Vector((math.cos(a) * r, math.sin(a) * r, 0.0)); emergent = rng.random() < P.get('emergent', .3)
        R = P['pad_r'] * rng.uniform(.6, 1.15)
        if emergent:
            h = rng.uniform(.25, .7); pts, _ = curve_pts(c - Vector((0, 0, .6)), UP, h + .6, 6, 0, rng, .03)
            stem(G, pts, .008, .006, 5, 3, rng.random(), 1.0); c = pts[-1]
        # pad: disc of 16 segments, slightly cupped, UV = atlas tile
        var = int(rng.integers(4)); u0, v0 = K.tile_uv(var); k = 18; ph = rng.random(); rot = rng.uniform(0, 2 * np.pi)
        cup = .12 if emergent else .02
        ctr = G.add_verts([c + Vector((0, 0, .004))], wind_branch=.05 if not emergent else .3, wind_leaf=.0, wind_phase=ph, leaf_rand=ph)
        ring = []
        for j in range(k):
            ang = rot + 2 * np.pi * j / k
            q = c + Vector((math.cos(ang) * R, math.sin(ang) * R, cup * R + .003 + .01 * math.sin(ang * 3)))
            ring.append(q)
        r0 = G.add_verts(ring, wind_branch=.05 if not emergent else .35, wind_leaf=.6, wind_phase=ph, leaf_rand=ph)
        for j in range(k):
            j1 = (j + 1) % k
            ua = (u0 + .25 + .23 * math.cos(2 * np.pi * j / k), v0 + .25 + .23 * math.sin(2 * np.pi * j / k))
            ub = (u0 + .25 + .23 * math.cos(2 * np.pi * j1 / k), v0 + .25 + .23 * math.sin(2 * np.pi * j1 / k))
            G.add_face((ctr, r0 + j, r0 + j1), ((u0 + .25, v0 + .25), ua, ub), 0)
    for f in range(P['flowers']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * .5 * math.sqrt(rng.random())
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.5)); h = rng.uniform(.6, 1.1)
        pts, dd = curve_pts(base, UP, h + .5, 6, 0, rng, .02)
        stem(G, pts, .007, .005, 5, 3, rng.random(), 1.0)
        flower(G, pts[-1], UP, 9, .11, .07, .9, 1, 2, rng.random(), 1.0, 'oval', .025, 2, 0, rng, .02)
    for f in range(P.get('pods', 0)):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * .6 * math.sqrt(rng.random())
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.5)); pts, dd = curve_pts(base, UP, rng.uniform(1.0, 1.4), 6, -.05, rng, .03)
        stem(G, pts, .006, .005, 5, 3, rng.random(), 1.0)
        K.lathe(G, [(.01, 0), (.035, .02), (.045, .04), (.04, .045), (.001, .046)], pts[-1], dd, 12, 2,
                dict(wind_trunk=0.0, wind_branch=.3, wind_leaf=.2, wind_phase=rng.random(), leaf_rand=0.5, grad=1.0))


def cattail(G, rng, P):
    for i in range(P['blades']):
        r = P['radius'] * math.sqrt(rng.random()); a = rng.uniform(0, 2 * np.pi)
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.15)); d = rand_dir(rng, 10)
        blade(G, base, d, P['h'] * rng.uniform(.6, 1.05), P['w'], .35 * rng.uniform(.3, 1.5), 7, 0, rng, rng.random(), twist=rng.normal(0, .8), curl=.25)
    for i in range(P['spikes']):
        r = P['radius'] * .7 * math.sqrt(rng.random()); a = rng.uniform(0, 2 * np.pi)
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.15)); pts, dd = curve_pts(base, rand_dir(rng, 6), P['h'] * rng.uniform(.9, 1.15), 8, 0, rng, .01)
        stem(G, pts, .005, .003, 5, 0, rng.random(), P['h'])
        L = .2; top = pts[-1] - dd * .1
        K.lathe(G, [(.002, 0), (.017, .01), (.02, .05), (.02, L - .03), (.016, L), (.003, L + .005)], top - dd * L * .8, dd, 10, 1,
                dict(wind_trunk=0.0, wind_branch=P['h'] * .5, wind_leaf=.2, wind_phase=rng.random(), leaf_rand=.5, grad=1.0))


def moss(G, rng, P):
    """moss cushions / carpet: noise-displaced flattened domes (mat slot 0) — shader does the fine detail."""
    for i in range(P['n']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * math.sqrt(rng.random())
        c = Vector((math.cos(a) * r, math.sin(a) * r, -.01)); R = P['r'] * rng.uniform(.5, 1.2); h = R * P['flat'] * rng.uniform(.7, 1.3)
        k = 14; rings = 5
        prof = [(R * math.cos(t) * (1 + .1 * rng.normal()), h * math.sin(t)) for t in np.linspace(0, np.pi / 2, rings + 1)]
        prof[-1] = (R * .02, h); prof[0] = (R * 1.05, -.01)
        K.lathe(G, prof, c, UP, k, 0, dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=rng.random(), grad=.5))
    if P.get('sporophytes'):
        for i in range(P['sporophytes']):
            a = rng.uniform(0, 2 * np.pi); r = P['radius'] * math.sqrt(rng.random())
            base = Vector((math.cos(a) * r, math.sin(a) * r, P['r'] * P['flat'] * .6))
            pts, dd = curve_pts(base, rand_dir(rng, 20), .03, 3, -.2, rng, .05)
            stem(G, pts, .0006, .0005, 3, 1, rng.random(), .05)
            dome(G, pts[-1], .0015, .003, 5, 1, 0.0, rings=2)


def mushrooms(G, rng, P):
    for i in range(P['n']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * math.sqrt(rng.random())
        base = Vector((math.cos(a) * r, math.sin(a) * r, -.005)); h = P['h'] * rng.uniform(.5, 1.2); cr = P['cap'] * rng.uniform(.6, 1.2)
        d = rand_dir(rng, 14)
        pts, dd = curve_pts(base, d, h, 5, .0, rng, .04)
        stem(G, pts, cr * .22, cr * .18, 8, 0, rng.random(), .1)
        top = pts[-1]
        cap = [(cr * .2, -cr * .15), (cr * .95, -cr * .12), (cr * 1.0, -cr * .02), (cr * .85, cr * .25 * P.get('dome', 1)),
               (cr * .5, cr * .45 * P.get('dome', 1)), (cr * .02, cr * .5 * P.get('dome', 1))]
        K.lathe(G, cap, top, dd, 14, 1, dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=rng.random(), grad=1.0))
        gill = [(cr * .2, -cr * .14), (cr * .94, -cr * .13)]
        K.lathe(G, gill, top - dd * .001, dd, 14, 2, dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=.5, grad=0.0))


def vine(G, rng, P):
    """hanging liana: rope tube hanging in a catenary-like curve from z = H to near the ground, small leaf cards along it."""
    H = P['h']
    for s in range(P['strands']):
        x0 = rng.normal(0, P['spread']); y0 = rng.normal(0, P['spread'] * .3)
        pts = []
        L = H * rng.uniform(.55, 1.0); n = 24
        for i in range(n + 1):
            t = i / n
            pts.append(Vector((x0 + .25 * math.sin(t * 3 + s) * t, y0 + .1 * math.sin(t * 5 + s), H - L * t)))
        ph = rng.random()
        k = 5; rings = []
        for i, p in enumerate(pts):
            t = i / n; r = P['r'] * (1 - .5 * t)
            ring = [p + Vector((math.cos(a) * r, math.sin(a) * r, 0)) for a in np.linspace(0, 2 * np.pi, k, endpoint=False)]
            rings.append(G.add_verts(ring, wind_trunk=0.0, wind_branch=t ** 1.4 * 1.2, wind_leaf=0.0, wind_phase=ph, leaf_rand=ph))
        for i in range(n):
            for j in range(k):
                j1 = (j + 1) % k; a0, a1 = rings[i], rings[i + 1]
                G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k, i / n * 4), ((j + 1) / k, i / n * 4), ((j + 1) / k, (i + 1) / n * 4), (j / k, (i + 1) / n * 4)), 0)
        for i in range(2, n, 1):
            for _ in range(P['leaves_per']):
                d = Vector((rng.normal(0, 1), rng.normal(0, 1), rng.uniform(-.6, .4))).normalized()
                card_at(G, pts[i], d, P['card'] * rng.uniform(.8, 1.2), 1, rng, ph)
        for v in G.A['wind_branch'][-1:]:
            pass


BUILDERS = dict(grass=grass_tuft, herb=herb, fern=fern, lotus=lotus, cattail=cattail, moss=moss, mushrooms=mushrooms, vine=vine)


# ====================================================================== catalogue (milestone 1)
GRASS_G = [(0, '#2E4A1E'), (.55, '#5E8A34'), (1, '#A9B862')]
PLANTS = [
    # ------------------------------------------------------------------ R-01 ASHRAM VALLEY
    dict(name='AV_G01_MEADOW_GRASS', common='Valley meadow grass', latin='Poa / Festuca mix', label=SI, region='R-01', category='Grass',
         kind='grass', seed=101, P=dict(blades=260, radius=.16, h=.34, w=.006, bend=.9, spread=28, splay=.4, dry=.12),
         mats=[('grass', GRASS_G), ('grass', [(0, '#4A4A22'), (.5, '#9A8A4A'), (1, '#D1BE7E')])], palette=['#2E4A1E', '#5E8A34', '#A9B862', '#D1BE7E']),
    dict(name='AV_G02_KANS_GRASS', common='Kans grass (tall, plumed)', latin='Saccharum spontaneum', label=SI, region='R-01', category='Grass',
         kind='grass', seed=102, P=dict(blades=120, radius=.35, h=1.9, w=.012, bend=1.3, spread=16, splay=.3, segs=7, plumes=14, plume_size=.55),
         mats=[('grass', [(0, '#3A4E22'), (.6, '#6E8A3A'), (1, '#B6B36A')]), ('simple', '#8A7A4A'), ('leaf', 'av_kans')],
         palette=['#3A4E22', '#6E8A3A', '#F1ECE0', '#D8CCB4']),
    dict(name='AV_G03_DRY_PATH_GRASS', common='Dry path-edge grass', latin='Heteropogon contortus (spear grass)', label=SI, region='R-01',
         category='Grass', kind='grass', seed=103, P=dict(blades=130, radius=.12, h=.45, w=.005, bend=1.1, spread=30, splay=.5, dry=.6),
         mats=[('grass', [(0, '#3A4A22'), (.5, '#7A8A3A'), (1, '#B8A860')]), ('grass', [(0, '#5A4A2A'), (.5, '#A88A4A'), (1, '#D8C08A')])],
         palette=['#7A8A3A', '#A88A4A', '#D8C08A']),
    dict(name='AV_F01_BUTTERCUP', common='Himalayan buttercup', latin='Ranunculus hirtellus', label=SI, region='R-01', category='Wildflower',
         kind='herb', seed=111, P=dict(h=.32, stems=4, spread=18, basal=6, leaf_l=.07, leaf_w=.06, leaf_shape='round', leaf_rough=.25,
                                        flower=dict(type='radial', n=5, L=.013, W=.014, cup=.6, shape='round', centre=.005)),
         mats=[('herbleaf', '#3E6A2A'), ('simple_gloss', '#F2C21A'), ('simple', '#C89A1A')], palette=['#F2C21A', '#C89A1A', '#3E6A2A']),
    dict(name='AV_F02_PRIMULA', common='Drumstick primula', latin='Primula denticulata', label=SI, region='R-01', category='Wildflower',
         kind='herb', seed=112, P=dict(h=.22, stems=1, spread=4, basal=9, leaf_l=.11, leaf_w=.04, leaf_shape='obovate', leaf_droop=.4,
                                        flower=dict(type='ball', n=60, R=.026, L=.011, W=.010)),
         mats=[('herbleaf', '#4E7A34'), ('petal', '#A87AD0'), ('simple', '#F0E06A')], palette=['#A87AD0', '#7A4AA8', '#4E7A34']),
    dict(name='AV_F03_WILD_DAISY', common='Wild daisy / pearly everlasting', latin='Anaphalis / Bellis-like (meadow daisy)', label=SI,
         region='R-01', category='Wildflower', kind='herb', seed=113,
         P=dict(h=.16, stems=5, spread=22, basal=7, leaf_l=.05, leaf_w=.02, leaf_shape='obovate',
                flower=dict(type='radial', n=18, L=.012, W=.004, cup=.05, shape='lance', centre=.004, centre_h=.003)),
         mats=[('herbleaf', '#4A7230'), ('petal', '#F4F2EA'), ('simple', '#F0C02A')], palette=['#F4F2EA', '#F0C02A', '#4A7230']),
    dict(name='AV_F04_MARIGOLD', common='Marigold (genda) — cultivated', latin='Tagetes erecta', label=SI, region='R-01 (Ashram gardens)',
         category='Garden flower', kind='herb', seed=114, P=dict(h=.5, stems=9, spread=22, basal=0, stem_leaves=12, leaf_l=.09, leaf_w=.022,
                                                                  leaf_shape='lance', stem_r=.004,
                                                                  flower=dict(type='pompom', n=14, layers=4, L=.03, W=.018)),
         mats=[('herbleaf', '#3A6228'), ('petal', '#F08A12'), ('simple', '#C86A0A')], palette=['#F08A12', '#F2B21A', '#3A6228']),
    dict(name='AV_FE01_SWORD_FERN', common='Valley sword fern', latin='Polystichum / Dryopteris-like', label=SI, region='R-01', category='Fern',
         kind='fern', seed=121, P=dict(fronds=14, size=.30, chain=3, elev=(40, 72), arch=.45, pinnae=24, pin_len=.17),
         mats=[('grass', [(0, '#2E5A1E'), (.6, '#4E8A30'), (1, '#7FB060')]), ('simple', '#5A4A2E')], palette=['#3F7A2C', '#5E9640', '#7FB060']),
    dict(name='AV_AQ01_LOTUS', common='Sacred lotus', latin='Nelumbo nucifera', label=SI, region='R-01 (Ashram pond / still water)',
         category='Aquatic plant', kind='lotus', seed=131, P=dict(pads=16, radius=1.1, pad_r=.26, emergent=.35, flowers=3, pods=2),
         mats=[('leaf', 'av_lotus'), ('petal', '#F2A6C0'), ('simple', '#E8C84A'), ('simple', '#4E7A3A')],
         palette=['#3F7B3A', '#F2A6C0', '#E06A92', '#E8C84A'], water=True),
    dict(name='AV_AQ02_CATTAIL', common='Reed-mace / cattail', latin='Typha angustifolia', label=SI, region='R-01 (pond + river margins)',
         category='Aquatic plant', kind='cattail', seed=132, P=dict(blades=55, radius=.35, h=1.9, w=.014, spikes=7),
         mats=[('grass', [(0, '#3A4A24'), (.6, '#6A8A3E'), (1, '#9AA66A')]), ('simple', '#5A3A22')], palette=['#6A8A3E', '#9AA66A', '#5A3A22'],
         water=True),
    dict(name='AV_M01_MOSS_CUSHION', common='Cushion moss', latin='Leucobryum-like', label=SI, region='R-01 / R-02', category='Moss',
         kind='moss', seed=141, P=dict(n=9, radius=.18, r=.09, flat=.45, sporophytes=40),
         mats=[('moss', ('#3F5E22', '#7E9A3A', '#8A8A55')), ('simple', '#8A5A2A')], palette=['#3F5E22', '#7E9A3A', '#8A8A55']),
    dict(name='AV_MU01_BROWN_MUSHROOMS', common='Brown woodland mushrooms', latin='Agaricales (generic)', label=SI, region='R-01 / R-02',
         category='Mushroom', kind='mushrooms', seed=151, P=dict(n=7, radius=.07, h=.07, cap=.028),
         mats=[('simple', '#E2D6BE'), ('simple_var', ('#8A5A34', '#5A3A22')), ('simple', '#C8B49A')], palette=['#8A5A34', '#5A3A22', '#E2D6BE']),
    # ------------------------------------------------------------------ R-02 ENCHANTED FOREST
    dict(name='EF_FE01_GIANT_FERN', common='Giant forest fern', latin='inspired by Dryopteris / Dicksonia fronds', label=SI, region='R-02',
         category='Fern', kind='fern', seed=221, P=dict(fronds=18, size=.55, chain=3, elev=(35, 75), arch=.42, pinnae=30, pin_len=.15, rachis=.007),
         mats=[('grass', [(0, '#1E4A34'), (.6, '#3A7A50'), (1, '#6FA880')]), ('simple', '#4A3A26')], palette=['#2A6A4A', '#4A8A5C', '#6FA880']),
    dict(name='EF_M01_MOSS_CARPET', common='Deep moss carpet', latin='Thuidium / Hypnum-like', label=SI, region='R-02', category='Moss',
         kind='moss', seed=241, P=dict(n=26, radius=.6, r=.2, flat=.28, sporophytes=120),
         mats=[('moss', ('#2E5A2E', '#5E8A3A', '#6A7A48')), ('simple', '#8A6A3A')], palette=['#2E5A2E', '#5E8A3A', '#6A7A48']),
    dict(name='EF_MU01_GLOWCAP', common='Glowcap mushrooms', latin='fictional (bioluminescent fungi exist, e.g. Mycena — look is a proposal)',
         label=PF, region='R-02', category='Rare fantasy fungus', kind='mushrooms', seed=251, P=dict(n=11, radius=.12, h=.09, cap=.03, dome=1.4),
         mats=[('simple', '#D8E6DA'), ('glow', '#8FE6D2'), ('glow_dim', '#5AB8A6')], palette=['#8FE6D2', '#5AB8A6', '#D8E6DA']),
    dict(name='EF_V01_HANGING_VINE', common='Hanging liana', latin='inspired by woody lianas (Entada / Bauhinia vahlii)', label=SI, region='R-02',
         category='Vine (hanging)', kind='vine', hanging=True, seed=261, P=dict(h=9.0, strands=6, spread=.8, r=.025, leaves_per=5, card=.32),
         mats=[('bark', 'bark_willow'), ('leaf', 'ef_beech')], palette=['#5A5048', '#2F6A4A', '#4A8A60']),
    # ------------------------------------------------------------------ R-03 MOUNTAIN KINGDOM
    dict(name='MK_G01_ALPINE_TUSSOCK', common='Alpine tussock grass', latin='Festuca / Kobresia tussock', label=SI, region='R-03',
         category='Mountain grass', kind='grass', seed=301, P=dict(blades=200, radius=.13, h=.38, w=.004, bend=1.4, spread=35, splay=.6, dry=.45, curl=.3),
         mats=[('grass', [(0, '#3A4A2A'), (.5, '#6E7E44'), (1, '#A8A46A')]), ('grass', [(0, '#5A5236'), (.5, '#9A8A5A'), (1, '#CFC29A')])],
         palette=['#6E7E44', '#A8A46A', '#CFC29A']),
    dict(name='MK_F01_GENTIAN', common='Himalayan gentian', latin='Gentiana ornata', label=SI, region='R-03', category='Alpine flower',
         kind='herb', seed=311, P=dict(h=.08, stems=5, spread=30, basal=10, leaf_l=.03, leaf_w=.006, leaf_shape='lance', stem_grav=-.2,
                                        flower=dict(type='trumpet', L=.035)),
         mats=[('herbleaf', '#3E5E2E'), ('petal', '#2E5ED8'), ('simple', '#E8E0C0')], palette=['#2E5ED8', '#7FA8F0', '#3E5E2E']),
    dict(name='MK_F02_EDELWEISS', common='Himalayan edelweiss', latin='Leontopodium himalayanum', label=SI, region='R-03', category='Alpine flower',
         kind='herb', seed=312, P=dict(h=.14, stems=4, spread=18, basal=8, leaf_l=.035, leaf_w=.008, leaf_shape='lance',
                                        flower=dict(type='star', n=9, L=.022, W=.008)),
         mats=[('woolly', '#9AA08A'), ('woolly', '#F2F0E6'), ('simple', '#D8CC9A')], palette=['#F2F0E6', '#9AA08A', '#D8CC9A']),
    dict(name='MK_F03_BLUE_POPPY', common='Himalayan blue poppy', latin='Meconopsis betonicifolia / grandis', label=SI, region='R-03',
         category='Alpine flower', kind='herb', seed=313, P=dict(h=.75, stems=3, spread=10, basal=7, leaf_l=.14, leaf_w=.05, leaf_shape='oval',
                                                                 leaf_rough=.2, stem_r=.004, stem_grav=-.25,
                                                                 flower=dict(type='radial', n=4, L=.045, W=.05, cup=.55, shape='round', centre=.01, centre_h=.012, droop=.2)),
         mats=[('herbleaf', '#5A7A4A'), ('petal', '#5A9AE0'), ('simple', '#E8C83A')], palette=['#5A9AE0', '#8AB8F0', '#E8C83A', '#5A7A4A']),
    dict(name='MK_M01_ALPINE_CUSHION', common='Alpine cushion plant', latin='Arenaria / Thylacospermum cushion', label=SI, region='R-03',
         category='Mountain vegetation', kind='moss', seed=341, P=dict(n=5, radius=.15, r=.16, flat=.5, sporophytes=60),
         mats=[('moss', ('#4A5E2E', '#7A8A46', '#9A9A6A')), ('simple', '#F4F0E8')], palette=['#4A5E2E', '#7A8A46', '#F4F0E8']),
]


def plant_mats(D):
    out = []
    for i, m in enumerate(D['mats']):
        kind, v = m; nm = f"MAT_T6_{D['name']}_{i}"
        if kind == 'grass':
            out.append(K.mat_simple(nm, v[1][1], rough=.55, attr_grad='grad', grad_cols=v, transl=.35, spec=.4))
        elif kind == 'leaf':
            out.append(K.mat_leaf(nm, v, transl=.3))
        elif kind == 'simple':
            out.append(K.mat_simple(nm, v, rough=.6))
        elif kind == 'simple_gloss':
            out.append(K.mat_simple(nm, v, rough=.15, coat=.6))
        elif kind == 'simple_var':
            out.append(K.mat_simple(nm, v[0], rough=.5, var_col=v[1], var_scale=40))
        elif kind == 'petal':
            out.append(K.mat_petal(nm, v))
        elif kind == 'herbleaf':
            out.append(K.mat_herbleaf(nm, v))
        elif kind == 'woolly':
            out.append(K.mat_simple(nm, v, rough=.9, sheen=1.0))
        elif kind == 'moss':
            out.append(K.mat_moss(nm, *v))
        elif kind == 'bark':
            out.append(K.mat_bark(nm, v, '#B0A898', moss=.3))
        elif kind == 'glow':
            out.append(K.mat_simple(nm, v, rough=.4, sss=.4, emission=v, em_strength=.5, transl=.3))      # subtle (Decision 01 §3)
        elif kind == 'glow_dim':
            out.append(K.mat_simple(nm, v, rough=.5, emission=v, em_strength=.15))
    return out


def build_plant(D, seed=0, collection=None):
    rng = np.random.default_rng(D['seed'] * 1000 + seed)
    G = Geo()
    BUILDERS[D['kind']](G, rng, D['P'])
    me = G.to_mesh(D['name'], plant_mats(D))
    o = bpy.data.objects.new(D['name'], me)
    if collection is not None:
        collection.objects.link(o)
    bb = np.array([v.co[:] for v in me.vertices])
    st = dict(height_m=round(float(bb[:, 2].max()), 3), spread_x_m=round(float(np.ptp(bb[:, 0])), 3), spread_y_m=round(float(np.ptp(bb[:, 1])), 3),
              tris=sum(len(p.vertices) - 2 for p in me.polygons), verts=len(me.vertices), lowest_z=round(float(bb[:, 2].min()), 3))
    for k, v in st.items():
        o[f't6_{k}'] = v
    return o, st

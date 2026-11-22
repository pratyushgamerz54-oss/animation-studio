"""TASK 06 · natural details (brief: "fallen leaves, fallen branches, giant logs, ivy, floating leaves …") — library prefix ND.

Same catalogue format as t6_plants (kind = builder). Every detail is real geometry with real-world size, lying ON the ground
(z = 0) or ON the water surface (z = 0), never floating, never sunk except where wood is partly buried (log, branches).
  ND_L01  leaf litter (broadleaf, mostly last year's brown leaves decomposing + a few fresh green ones — SPRING)
  ND_L02  needle litter (pine / cedar / spruce floor) with a few cones
  ND_B01  fallen branches (broken ends with pale inner wood, twigs, partly sunk into the litter)
  ND_B02  giant fallen log (R-02): moss on top, bracket fungi, splintered broken end, upturned root plate with soil
  ND_I01  ground ivy (creeping carpet over the forest floor / ruins)
  ND_W01  floating leaves (lake / pond surface, z = 0 = water)
Physics note (Director 22 Nov): leaves lie flat with gentle curl and overlap (gravity), lighter fresh leaves on top of the darker
older layer; branches rest on their own stubs; the log rests on the ground along its length and the root plate tilts it.
"""
import math
import numpy as np
from mathutils import Vector
import t6kit as K
import t6_plants as PL
from t6kit import perp, rot_about, UP, Branch

SI = PL.SI


def flat_card(G, c, size, rot, curl, mi, rng, wb=0.0, wl=0.0, lift=0.0):
    """single-leaf atlas tile lying on a surface: 3 × 3 grid, edges + tip curl up (dry leaves cup), random tile (UV 0.5²)."""
    var = int(rng.integers(4)); u0, v0 = K.tile_uv(var)
    ax = Vector((math.cos(rot), math.sin(rot), 0)); sd = Vector((-ax.y, ax.x, 0))
    tilt = Vector((rng.normal(0, .08), rng.normal(0, .08), 0))
    ids = []
    for j, v in enumerate((0.0, .5, 1.0)):
        row = []
        for i, u in enumerate((0.0, .5, 1.0)):
            p = c + ax * (v - .03) * size + sd * (u - .5) * size
            z = c.z + lift + curl * size * ((u - .5) * 2) ** 2 * .35 + curl * size * max(0, v - .6) ** 2 * .6 + (tilt.x * (u - .5) + tilt.y * v) * size * .3
            row.append(Vector((p.x, p.y, max(z, c.z))))
        ids.append(G.add_verts(row, wind_trunk=0.0, wind_branch=wb, wind_leaf=wl * np.array([0, 0, 0]) if j == 0 else wl * j / 2,
                               wind_phase=rng.random(), leaf_rand=rng.random(), grad=v))
    for j in range(2):
        for i in range(2):
            a = ids[j] + i; b = ids[j + 1] + i
            uv = lambda uu, vv: (u0 + uu * .5, v0 + vv * .5)
            G.add_face((a, a + 1, b + 1, b), (uv(i * .5, j * .5), uv((i + 1) * .5, j * .5), uv((i + 1) * .5, (j + 1) * .5), uv(i * .5, (j + 1) * .5)), mi)


def litter(G, rng, P):
    """overlapping layers: older (decomposing, slot 0 atlas) first, fresh fallen leaves (slot 1 atlas) on top; small twigs (slot 2)."""
    n = P['n']; R = P['radius']; size = K.ATLAS_META.get(P['atlas'], {'size_m': .12})['size_m'] * P.get('scale', 1.0)
    for k in range(n):
        r = R * math.sqrt(rng.random()) * (1 + .15 * math.sin(7 * k)); a = rng.uniform(0, 2 * np.pi)
        layer = k / n                                                 # later leaves lie higher (on top of the earlier ones)
        c = Vector((math.cos(a) * r, math.sin(a) * r, .0003 + .012 * layer * (1 - (r / R) ** 2)))
        fresh = rng.random() < P.get('fresh', .1)
        flat_card(G, c, size * rng.uniform(.75, 1.2), rng.uniform(0, 2 * np.pi), rng.uniform(.05, .35) * (0.4 if fresh else 1.0),
                  1 if fresh and P.get('atlas2') else 0, rng)
    for k in range(P.get('twigs', 0)):
        a = rng.uniform(0, 2 * np.pi); r = R * .8 * math.sqrt(rng.random()); c = Vector((math.cos(a) * r, math.sin(a) * r, .006))
        d = Vector((math.cos(rng.uniform(0, 6.3)), math.sin(rng.uniform(0, 6.3)), 0)); L = rng.uniform(.12, .45)
        pts = [c + d * L * t + Vector((0, 0, .003 * math.sin(t * 9))) for t in np.linspace(0, 1, 6)]
        PL.stem(G, pts, .004, .0015, 4, 2, rng.random(), .05)


def needles(G, rng, P):
    """needle litter: thousands of thin needle strips (slot 0, brown → grey) in a mat + cones (slot 1, lathe of scales)."""
    R = P['radius']
    # duff: decomposed needles under the fresh ones — irregular flat patch (slot 2), the mat reads as a continuous rust-brown layer
    k_ = 40; ang = np.linspace(0, 2 * np.pi, k_, endpoint=False); ph = rng.uniform(0, 6.3, 3)
    rim = [Vector((math.cos(t) * R * 1.05 * (1 + .18 * math.sin(3 * t + ph[0]) + .1 * math.sin(7 * t + ph[1]) + .05 * rng.normal()),
                   math.sin(t) * R * 1.05 * (1 + .18 * math.sin(3 * t + ph[0]) + .1 * math.sin(7 * t + ph[1]) + .05 * rng.normal()), .0004)) for t in ang]
    i_r = G.add_verts(rim, grad=.5); i_c = G.add_verts([Vector((0, 0, .0012))], grad=.5)
    for j in range(k_):
        G.add_face((i_c, i_r + j, i_r + (j + 1) % k_), ((.5, .5), (.5 + .5 * math.cos(ang[j]), .5 + .5 * math.sin(ang[j])),
                                                      (.5 + .5 * math.cos(ang[(j + 1) % k_]), .5 + .5 * math.sin(ang[(j + 1) % k_]))), 2)
    for k in range(P['n']):
        r = R * math.sqrt(rng.random()); a = rng.uniform(0, 2 * np.pi); c = Vector((math.cos(a) * r, math.sin(a) * r, .0014 + .006 * rng.random() * (1 - r / R)))
        d = Vector((math.cos(rng.uniform(0, 6.3)), math.sin(rng.uniform(0, 6.3)), rng.normal(0, .05))).normalized()
        L = P['nlen'] * rng.uniform(.6, 1.15); w = P.get('nw', .0012); sd = Vector((-d.y, d.x, 0)).normalized()
        bend = rng.normal(0, .15)
        p1 = c + d * L * .5 + sd * L * bend * .2; p2 = c + d * L
        i0 = G.add_verts([c - sd * w / 2, c + sd * w / 2, p1 - sd * w / 2, p1 + sd * w / 2, p2], grad=rng.random(), leaf_rand=rng.random())
        G.add_face((i0, i0 + 1, i0 + 3, i0 + 2), ((0, 0), (1, 0), (1, .5), (0, .5)), 0)
        G.add_face((i0 + 2, i0 + 3, i0 + 4), ((0, .5), (1, .5), (.5, 1)), 0)
    for k in range(P.get('cones', 0)):                           # opened cones: woody core + ~70 scales in a Fibonacci spiral (slot 1)
        a = rng.uniform(0, 2 * np.pi); r = R * .7 * math.sqrt(rng.random()); L = P['cone_l'] * rng.uniform(.8, 1.15); rr = L * .2
        axis = Vector((math.cos(rng.uniform(0, 6.3)), math.sin(rng.uniform(0, 6.3)), 0.0)).normalized()
        base = Vector((math.cos(a) * r, math.sin(a) * r, rr * 1.35)) - axis * L * .5     # cone rests on its scales
        attrs = dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=rng.random(), grad=.5)
        K.lathe(G, [(rr * .2, 0), (rr * .55, L * .1), (rr * .6, L * .6), (rr * .3, L * .95), (rr * .05, L)], base, axis, 8, 1, attrs)
        ref = perp(axis); ns = 70
        for i in range(ns):
            t = (i + .5) / ns; ang = i * 2.39996
            prof = math.sin(math.pi * min(1, .08 + t)) ** .6
            out = rot_about(ref, axis, ang)
            q = base + axis * L * t + out * rr * .5 * prof
            d = (out * (.9 if t > .15 else .6) - axis * .25).normalized()
            PL.petal(G, q, d, axis, rr * 1.1 * (.45 + .55 * prof), rr * .9 * (.5 + .5 * prof), .35, 1, 0.0, .05, 'round', segs=3, rng=rng, grad=.5)
    for i, V in enumerate(G.V):                                     # nothing below the ground
        V[:, 2] = np.maximum(V[:, 2], -.002)


def broken_end(G, c, axis, r, k, rng, mi_in, mi_bark, ring0=None):
    """splintered break: jagged fibres (wood breaks along the grain → long splinters) + pale inner wood (own material)."""
    axis = axis.normalized(); nv = perp(axis); bv = axis.cross(nv)
    ang = np.linspace(0, 2 * np.pi, k, endpoint=False)
    rim = [c + (nv * math.cos(a) + bv * math.sin(a)) * r for a in ang]
    i_rim = G.add_verts(rim) if ring0 is None else ring0
    tips = []
    for j, a in enumerate(ang):                       # splinters: longer near one side (the side that tore last)
        L = r * (.15 + 1.6 * rng.random() ** 2.5) * (1 + .8 * max(0, math.cos(a - 1.0)))
        tips.append(c + (nv * math.cos(a) + bv * math.sin(a)) * r * rng.uniform(.2, .8) + axis * L)
    i_tip = G.add_verts(tips); i_c = G.add_verts([c + axis * r * .25])
    for j in range(k):
        j1 = (j + 1) % k
        G.add_face((i_rim + j, i_rim + j1, i_tip + j1, i_tip + j), ((0, 0), (1, 0), (1, 1), (0, 1)), mi_in)
        G.add_face((i_tip + j, i_tip + j1, i_c), ((0, 0), (1, 0), (.5, 1)), mi_in)


def wood_piece(G, rng, pts, r0, r1, k, S, mi_bark=0):
    b = Branch(pts, list(np.linspace(r0, r1, len(pts))), 1, rng.random(), 0.0, kind='branch')
    K.tube(G, b, k, S['bark'].get('tile', 1.0), S, 20.0, rng)
    return b


def branches(G, rng, P):
    """fallen branches lying on the ground: each rests on its lowest points (sunk ≤ 3 cm into litter), broken thick end."""
    S = dict(trunk=dict(), bark=dict(tile=.5), flex=[0, 0, 0, 0, 0])
    for k in range(P['n']):
        a = rng.uniform(0, 2 * np.pi); L = P['len'] * rng.uniform(.5, 1.2); r0 = P['r'] * rng.uniform(.6, 1.2)
        o = Vector((rng.normal(0, P['spread']), rng.normal(0, P['spread']), 0)); d = Vector((math.cos(a), math.sin(a), 0))
        pts = []
        for t in np.linspace(0, 1, 10):
            q = o + d * L * t + Vector((-d.y, d.x, 0)) * L * .12 * math.sin(t * 3 + k)
            pts.append(Vector((q.x, q.y, r0 * (1 - .6 * t) * .75 - .015)))
        wood_piece(G, rng, pts, r0, r0 * .35, 8, S)
        broken_end(G, pts[0], (pts[0] - pts[1]), r0 * .95, 8, rng, 1, 0)
        for s_ in range(P.get('twigs', 3)):                         # side twigs: some rest on the ground, some stick up
            t = rng.uniform(.2, .9); i = int(t * 9); q = pts[i]
            dd = (d * .6 + Vector((-d.y, d.x, 0)) * rng.choice([-1, 1]) + Vector((0, 0, rng.uniform(-.1, .7)))).normalized()
            tl = L * rng.uniform(.15, .4)
            tp = [q + dd * tl * u + Vector((0, 0, -.08 * tl * u * u)) for u in np.linspace(0, 1, 5)]
            for p_ in tp:
                p_.z = max(p_.z, r0 * .2)
            wood_piece(G, rng, tp, r0 * .35, r0 * .08, 5, S)


def log(G, rng, P):
    """giant fallen log along +X: rests on the ground (bottom 12 % of the radius buried), sags a little, moss on the upper side
    (mat_bark moss), bracket fungi (slot 2), splintered broken end (+X, inner wood slot 1), upturned root plate (−X, soil slot 3)."""
    L, R = P['len'], P['r']; S = dict(trunk=dict(flare=0.0, lobes=0, nodes=0), bark=dict(tile=1.0), flex=[0] * 5)
    pts = [Vector((L * t - L * .15, .25 * math.sin(t * 2.2), R * (1 - .3 * t) * .88 - .02 * math.sin(math.pi * t))) for t in np.linspace(0, 1, 26)]
    rad = [R * (1 - .3 * t) for t in np.linspace(0, 1, 26)]
    b = Branch(pts, rad, 0, rng.random(), 0.0, kind='trunk')
    K.tube(G, b, 28, 1.0, S, 4.0, rng)
    broken_end(G, pts[-1], pts[-1] - pts[-2], rad[-1] * .97, 24, rng, 1, 0)
    for k in range(P.get('fungi', 8)):                             # brackets on the sides, half-way down (shade, moist)
        t = rng.uniform(.15, .85); p, d, r = b.at(t); side = Vector((0, rng.choice([-1, 1]), rng.uniform(-.2, .3))).normalized()
        K.bracket(G, p + side * r * .95, side, P.get('fungus', .18) * rng.uniform(.6, 1.3), rng)
    # root plate: tilted soil disc with root stubs (the tree was uprooted — roots tore out a plate of earth)
    c = pts[0] - Vector((R * .2, 0, 0)); axis = Vector((-1, 0, .35)).normalized(); Rp = R * P.get('plate', 2.3)
    prof = [(Rp * .02, R * .55), (Rp * .5, R * .5), (Rp * .85, R * .35), (Rp, 0), (Rp * .9, -R * .45), (Rp * .4, -R * .6), (Rp * .02, -R * .6)]
    K.lathe(G, prof, c, axis, 28, 3, dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=.5, grad=0.0, soil_w=1.0),
            wobble=.38, seed=int(rng.integers(1 << 30)))            # torn earth: very irregular outline
    nv = perp(axis); bv = axis.cross(nv)
    for k in range(P.get('roots', 14)):                           # torn roots: radial from the plate RIM, sagging under gravity
        a = 2 * np.pi * k / P.get('roots', 14) + rng.normal(0, .2); out = nv * math.cos(a) + bv * math.sin(a)
        q0 = c + out * Rp * rng.uniform(.75, .95) + axis * R * rng.uniform(-.1, .3)
        dd = (out + axis * rng.uniform(-.1, .25)).normalized()
        rl = R * rng.uniform(.6, 1.8); r0 = R * .1 * rng.uniform(.5, 1.2)
        rp = [q0 + dd * rl * u + Vector((0, 0, -.45 * rl * u * u)) + Vector(rng.normal(0, .04, 3)) * u for u in np.linspace(0, 1, 8)]
        rb = Branch(rp, list(np.linspace(r0, r0 * .15, 8)), 0, rng.random(), 0.0, kind='root')
        K.tube(G, rb, 7, 1.0, S, 4.0, rng)
    for k in range(P.get('stubs', 22)):                           # short broken root ends + fibres on the plate face (soil side)
        a = rng.uniform(0, 2 * np.pi); out = nv * math.cos(a) + bv * math.sin(a)
        q0 = c + out * Rp * math.sqrt(rng.random()) * .85 + axis * R * .5
        dd = (axis * rng.uniform(.6, 1.0) + out * rng.uniform(-.4, .6)).normalized(); rl = R * rng.uniform(.1, .45)
        rp = [q0 + dd * rl * u + Vector((0, 0, -.2 * rl * u)) for u in np.linspace(0, 1, 4)]
        rb = Branch(rp, list(np.linspace(R * .035, R * .008, 4)), 0, rng.random(), 0.0, kind='root')
        K.tube(G, rb, 5, 1.0, S, 4.0, rng)
    # pull everything that dipped under the ground plane up to −2 cm max (except the buried bottom of the log + plate)
    for i, V in enumerate(G.V):
        V[:, 2] = np.maximum(V[:, 2], -R * .12)


def ivy_ground(G, rng, P):
    """creeping ivy carpet on the ground (z = 0): runners + leaf cards lying almost flat (normal up), a few climbing a little."""
    R = P['radius']; size = K.ATLAS_META.get(P['atlas'], {'size_m': .36})['size_m'] * P.get('scale', .8)
    for s in range(P['runners']):
        a = rng.uniform(0, 2 * np.pi); p = Vector((rng.normal(0, R * .2), rng.normal(0, R * .2), P['r'])); d = Vector((math.cos(a), math.sin(a), 0))
        pts = [p.copy()]
        for i in range(int(R * 1.6 / .08)):
            d = (d + Vector((rng.normal(0, .35), rng.normal(0, .35), 0))).normalized(); q = pts[-1] + d * .08; q.z = P['r'] + .003 * rng.random() * (i > 2)
            if q.length > R * 1.05:
                break
            pts.append(q)
        if len(pts) < 3:
            continue
        ph = rng.random()
        from t6_plants_m2 import rope
        rope(G, pts, P['r'], P['r'] * .5, 5, 0, ph, 0.0, .01)
        for i in range(1, len(pts)):
            for _ in range(P.get('per', 2)):
                rot = rng.uniform(0, 2 * np.pi); c = pts[i] + Vector((0, 0, .004 + .03 * rng.random()))
                flat_card(G, c, size * rng.uniform(.7, 1.2), rot, rng.uniform(.1, .5), 1, rng, wb=.01, wl=.6, lift=.0)


def floating(G, rng, P):
    """leaves floating on still water (z = 0 = water surface): flat, slightly cupped, clustered by the breeze (one side denser)."""
    R = P['radius']; size = K.ATLAS_META.get(P['atlas'], {'size_m': .12})['size_m'] * P.get('scale', 1.0)
    for k in range(P['n']):
        r = R * math.sqrt(rng.random()); a = rng.uniform(0, 2 * np.pi)
        if rng.random() < .5:
            a = rng.normal(.6, .7)                                   # drift pile-up on the lee side
        c = Vector((math.cos(a) * r, math.sin(a) * r, 0.0))
        flat_card(G, c, size * rng.uniform(.75, 1.2), rng.uniform(0, 2 * np.pi), rng.uniform(.05, .25), 0 if rng.random() > P.get('fresh', .2) else 1,
                  rng, wb=.02, wl=.15)


BUILDERS = dict(litter=litter, needles=needles, branches=branches, log=log, ivy_ground=ivy_ground, floating=floating)

DETAILS = [
    dict(name='ND_L01_LEAF_LITTER_BROADLEAF', common='Leaf litter (broadleaf, spring)', latin="last year's oak / beech / peepal leaves decomposing + a few fresh",
         label=SI, region='R-01 / R-02 / R-08 / C-sites (under broadleaf trees)', category='Natural detail', kind='litter', seed=9901,
         habitat='under broadleaf trees and in hollows; scatter as overlapping patches; SPRING = mostly old brown leaves + a few fresh green ones',
         P=dict(n=420, radius=.75, atlas='nd_litter_old', atlas2='nd_litter_fresh', fresh=.12, twigs=10, scale=1.0),
         mats=[('leaf', 'nd_litter_old'), ('leaf', 'nd_litter_fresh'), ('bark', 'bark_brown_01')], wind=dict(branch=0.0, leaf=0.0),
         palette=['#6A4A2E', '#8A6A42', '#B0905A', '#5E7A3A']),
    dict(name='ND_L02_NEEDLE_LITTER', common='Needle litter + cones', latin='Pinus / Cedrus / Picea needle mat', label=SI,
         region='R-01 (chir pine, deodar) / R-03 (spruce, fir)', category='Natural detail', kind='needles', seed=9902,
         habitat='under conifers: a springy rust-brown mat of fallen needles with cones', P=dict(n=12000, radius=.7, nlen=.11, nw=.0019, cones=6, cone_l=.13),
         mats=[('grass', [(0, '#6A4A2A'), (.5, '#8E6A40'), (1, '#A88A5E')]), ('simple_var', ('#7A5A3A', '#4A3422')), ('simple_var', ('#5A4028', '#3A2A1C'))],
         wind=dict(branch=0.0, leaf=0.0),
         palette=['#6A4A2A', '#8E6A40', '#A88A5E', '#4A3422']),
    dict(name='ND_B01_FALLEN_BRANCHES', common='Fallen branches', latin='dead wood (any broadleaf)', label=SI, region='all forested regions',
         category='Natural detail', kind='branches', seed=9903, habitat='forest floor: storm-broken limbs, splintered ends (pale inner wood), side twigs; partly sunk into litter',
         P=dict(n=4, len=2.6, r=.05, spread=.6, twigs=4), mats=[('bark', 'bark_brown_02'), ('simple_var', ('#B89A6A', '#8A6A44'))], wind=dict(branch=0.0, leaf=0.0),
         palette=['#5A4A3A', '#B89A6A', '#8A6A44']),
    dict(name='ND_B02_GIANT_LOG', common='Giant fallen log (uprooted)', latin='fallen old-growth trunk (R-02 Giant Elder / Moss Oak size)', label=SI,
         region='R-02 (also R-01 forest ring, R-03 M1)', category='Natural detail', kind='log', seed=9904,
         habitat='old forest floor: an uprooted giant lying along the ground; moss + ferns on the top, bracket fungi, splintered break, root plate with soil',
         P=dict(len=16.0, r=.85, fungi=12, fungus=.2, plate=2.4, roots=26, stubs=26),
         mats=[('mossbark', 'bark_willow'), ('simple_var', ('#B89A6A', '#7A5A3A')), ('simple_var', ('#B8925A', '#6E4A2A')), ('soil', 'brown_mud')],
         wind=dict(branch=0.0, leaf=0.0), palette=['#5A5048', '#4E6A3A', '#B89A6A', '#B8925A', '#5A4430']),
    dict(name='ND_I01_GROUND_IVY', common='Ground ivy carpet', latin='Hedera nepalensis (creeping)', label=SI, region='R-02 / C-sites / R-01 shady banks',
         category='Natural detail', kind='ivy_ground', seed=9905, habitat='shady forest floor, ruins and banks; creeping runners with leaves held just above the ground',
         P=dict(radius=.8, runners=9, r=.004, per=2, atlas='ct_ivy', scale=.75), mats=[('bark', 'bark_brown_01'), ('leaf', 'ct_ivy')], wind=dict(branch=.01, leaf=.015),
         palette=['#1E3A22', '#2E4A2A', '#9AB08A']),
    dict(name='ND_W01_FLOATING_LEAVES', common='Floating leaves (water surface)', latin='fallen leaves on still water', label=SI,
         region='R-08 lake bays / R-01 Ashram pond / R-02 pools', category='Natural detail (water surface z = 0)', kind='floating', seed=9906,
         habitat='still water near shore trees; drifts pile up on the lee side; place at the water level', P=dict(n=90, radius=1.2, atlas='nd_litter_old', fresh=.25, scale=1.0),
         mats=[('leaf', 'nd_litter_old'), ('leaf', 'nd_litter_fresh')], wind=dict(branch=.02, leaf=.004), palette=['#6A4A2E', '#8A6A42', '#5E7A3A']),
]


def plant_mats(D):
    out = []
    for i, (kind, v) in enumerate(D['mats']):
        nm = f"MAT_T6_{D['name']}_{i}"
        if kind == 'soil':
            out.append(K.mat_ground(nm, v, 1.2, '#B0A090'))           # real scanned soil (already non-polished)
        elif kind == 'mossbark':                                       # fallen giant: thick moss on the upper side (up-facing + moss_w)
            out.append(K.mat_bark(nm, v, '#9A9488', moss=.85, moss_col='#4A6A30', lichen=.3))
        else:
            out += PL.plant_mats(dict(name=f"{D['name']}_TMP{i}", mats=[(kind, v)])); out[-1].name = nm
    return out


def build_plant(D, seed=0, collection=None):
    import bpy
    rng = np.random.default_rng(D['seed'] * 1000 + seed)
    G = K.Geo(); BUILDERS[D['kind']](G, rng, D['P'])
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

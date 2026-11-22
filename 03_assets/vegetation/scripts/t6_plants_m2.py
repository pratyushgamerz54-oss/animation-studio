"""TASK 06 · small plants — MILESTONE 2 (remaining regions + additions). Same format as t6_plants.PLANTS.

New builders: succulent (ribbed candelabra euphorbia with spines), ivy (wall curtain: climbing stems + leaf cards lying on the
wall plane y = 0, facing −Y), waterlily (floating notched pads with petioles down to the rhizome + flowers AT the water surface).
Root curtain (caves) = the vine builder without leaves. Wind per plant: D['wind'] = dict(branch, leaf) (succulent / ivy are stiff).
"""
import math
import numpy as np
from mathutils import Vector
import t6kit as K
import t6_plants as PL
from t6kit import perp, rot_about, UP

SI, PF = PL.SI, PL.PF


def rope(G, pts, r0, r1, k, mi, wphase, wb0=0.0, wb1=.03, wl=0.0, grad=None):
    """tube along a polyline with explicit (small) wind weights — for stiff / wall-held stems."""
    n = len(pts); T = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
    nv = perp(T[0]); rings = []
    for i in range(n):
        nv = (nv - T[i] * nv.dot(T[i])).normalized(); bv = T[i].cross(nv); t = i / (n - 1); r = r0 + (r1 - r0) * t
        ring = [pts[i] + (nv * math.cos(a) + bv * math.sin(a)) * r for a in np.linspace(0, 2 * np.pi, k, endpoint=False)]
        rings.append(G.add_verts(ring, wind_trunk=0.0, wind_branch=wb0 + (wb1 - wb0) * t, wind_leaf=wl * t, wind_phase=wphase,
                                 leaf_rand=wphase, grad=t if grad is None else grad))
    for i in range(n - 1):
        for j in range(k):
            j1 = (j + 1) % k; a0, a1 = rings[i], rings[i + 1]
            G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k, i / n), ((j + 1) / k, i / n), ((j + 1) / k, (i + 1) / n), (j / k, (i + 1) / n)), mi)


# ====================================================================== succulent (Euphorbia caducifolia / E. royleana)
def succulent(G, rng, P):
    """candelabra: short base + arms that turn upward; each arm is a RIBBED column (P['ribs'] ribs) with paired spines on the rib
    crests (slot 1). Real succulents are irregular: arm length, lean and rib depth vary."""
    ribs = P.get('ribs', 5); k = ribs * 4
    def column(base, d, L, r, ph):
        pts, dd = PL.curve_pts(base, d, L, max(6, int(L / .06)), P.get('upturn', 2.2), rng, .015)
        n = len(pts); T = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
        nv = perp(T[0]); rings = []; amp = P.get('rib_amp', .16) * rng.uniform(.8, 1.2); tw = rng.uniform(0, 2 * np.pi)
        for i in range(n):
            nv = (nv - T[i] * nv.dot(T[i])).normalized(); bv = T[i].cross(nv); t = i / (n - 1)
            rr = r * (1 - .25 * t ** 3) * (1 + .05 * math.sin(t * 17 + ph * 6))          # slight constrictions (growth segments)
            if t > .96:
                rr *= max(.15, (1 - t) / .04)                                           # rounded tip
            ang = np.linspace(0, 2 * np.pi, k, endpoint=False) + tw
            prof = 1 + amp * np.cos(ribs * ang)
            ring = [pts[i] + (nv * math.cos(a) + bv * math.sin(a)) * rr * prof[j] for j, a in enumerate(ang)]
            wb = .02 * (max(pts[i].z, 0) / max(P['h'], .1)) ** 1.5
            rings.append(G.add_verts(ring, wind_trunk=0.0, wind_branch=wb, wind_leaf=0.0, wind_phase=ph, leaf_rand=ph, grad=t))
            if i % 2 == 0 and .05 < t < .95:                                            # spine pairs on every rib crest
                for rj in range(ribs):
                    a = tw + 2 * np.pi * rj / ribs; out = (nv * math.cos(a) + bv * math.sin(a))
                    q = pts[i] + out * rr * (1 + amp)
                    for sgn in (-1, 1):
                        sd = (out + T[i].cross(out) * sgn * .6 + T[i] * .2).normalized() * P.get('spine', .006)
                        s0 = G.add_verts([q - T[i] * .001, q + T[i] * .001, q + sd], wind_branch=wb, wind_phase=ph, leaf_rand=ph, grad=1.0)
                        G.add_face((s0, s0 + 1, s0 + 2), ((0, 0), (1, 0), (.5, 1)), 1)
        for i in range(n - 1):
            for j in range(k):
                j1 = (j + 1) % k; a0, a1 = rings[i], rings[i + 1]
                G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k, i / n * 3), ((j + 1) / k, i / n * 3), ((j + 1) / k, (i + 1) / n * 3), (j / k, (i + 1) / n * 3)), 0)
        return pts
    trunk = column(Vector((0, 0, -.05)), UP, P['h'] * P.get('trunk', .35), P['r'] * 1.25, rng.random())
    for a_i in range(P['arms']):
        q = trunk[int(len(trunk) * rng.uniform(.35, .95))]; az = 2 * np.pi * a_i / P['arms'] + rng.normal(0, .35)
        d = Vector((math.cos(az), math.sin(az), rng.uniform(-.05, .35))).normalized()
        column(q, d, P['h'] * rng.uniform(.55, .95), P['r'] * rng.uniform(.75, 1.0), rng.random())
    for b in range(P.get('base_shoots', 0)):                                            # young shoots from the base
        az = rng.uniform(0, 2 * np.pi); rr = P['r'] * rng.uniform(2.5, 5)
        column(Vector((math.cos(az) * rr, math.sin(az) * rr, -.03)), PL.rand_dir(rng, 15), P['h'] * rng.uniform(.2, .45), P['r'] * .7, rng.random())


# ====================================================================== ivy curtain on a wall (plane y = 0, leaves face −Y)
def wall_card(G, p, axis, size, mi, rng, wphase, wb):
    """atlas card lying ON the wall (normal −Y, a small outward tilt), pivot = bottom centre."""
    axis = Vector((axis.x, 0, axis.z)).normalized(); out = Vector((0, -1, 0))
    side = axis.cross(out).normalized(); tilt = rng.uniform(.15, .45)
    up_ax = (axis * math.cos(tilt) + out * math.sin(tilt)).normalized()
    var = int(rng.integers(4)); u0, v0 = K.tile_uv(var); fold = .18; hw = size / 2
    lb = p - side * hw * math.cos(fold) + out * hw * math.sin(fold); rb = p + side * hw * math.cos(fold) + out * hw * math.sin(fold)
    top = up_ax * size
    nrm = [tuple(out)] * 4
    a = G.add_verts([lb, p, rb], wind_branch=wb, wind_leaf=0.0, wind_phase=wphase, leaf_rand=rng.random())
    c = G.add_verts([lb + top, p + top, rb + top], wind_branch=wb, wind_leaf=1.0, wind_phase=wphase, leaf_rand=rng.random())
    G.add_face((a, a + 1, c + 1, c), ((u0, v0), (u0 + .25, v0), (u0 + .25, v0 + .5), (u0, v0 + .5)), mi, nrm)
    G.add_face((a + 1, a + 2, c + 2, c + 1), ((u0 + .25, v0), (u0 + .5, v0), (u0 + .5, v0 + .5), (u0 + .25, v0 + .5)), mi, nrm)


def ivy(G, rng, P):
    H, W = P['h'], P['w']; size = K.ATLAS_META.get(P['atlas'], {'size_m': .36})['size_m'] * P.get('scale', 1.0)
    for s in range(P['stems']):
        x = rng.uniform(-W * .35, W * .35); pts = [Vector((x, -.01, -.03))]; d = Vector((rng.normal(0, .3), 0, 1)).normalized()
        L = H * rng.uniform(.6, 1.05); n = int(L / .08)
        for i in range(n):                                       # climbs: random walk in the wall plane, prefers up
            d = (d + Vector((rng.normal(0, .35), 0, .25))).normalized()
            q = pts[-1] + d * .08; q.x = max(-W / 2, min(W / 2, q.x)); q.y = -.008 - .004 * rng.random(); pts.append(q)
        ph = rng.random(); rope(G, pts, P['r'], P['r'] * .45, 5, 0, ph, 0.0, .02)
        for i in range(2, len(pts) - 1):                         # side shoots hanging / spreading + leaf cards
            if rng.random() < P.get('density', .8):
                for _ in range(P.get('per', 2)):
                    ax = Vector((rng.normal(0, 1), 0, rng.uniform(-1.0, .4))).normalized()
                    wall_card(G, pts[i], ax, size * rng.uniform(.75, 1.2), 1, rng, ph, .01 + .02 * rng.random())
        for _ in range(P.get('hang', 0) // max(P['stems'], 1)):  # loose trailing shoots off the top / ledges sway a little more
            q = pts[int(len(pts) * rng.uniform(.6, 1.0)) - 1]; tp = [q]
            for i in range(8):
                tp.append(tp[-1] + Vector((rng.normal(0, .02), -.006, -.06)))
            rope(G, tp, P['r'] * .45, P['r'] * .3, 4, 0, ph, .02, .12)
            for i in range(2, len(tp), 2):
                wall_card(G, tp[i], Vector((rng.normal(0, .6), 0, -1)), size * .8, 1, rng, ph, .05 + .07 * i / len(tp))


# ====================================================================== water lily (z = 0 = water surface)
def waterlily(G, rng, P):
    R0 = Vector((0, 0, -P.get('depth', .9)))                     # rhizome on the lake bed
    for i in range(P['pads']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * math.sqrt(rng.random())
        c = Vector((math.cos(a) * r, math.sin(a) * r, 0.0)); R = P['pad_r'] * rng.uniform(.55, 1.15)
        var = int(rng.integers(4)); u0, v0 = K.tile_uv(var); k = 20; ph = rng.random(); rot = rng.uniform(0, 2 * np.pi)
        ctr = G.add_verts([c + Vector((0, 0, .004))], wind_branch=.04, wind_leaf=.0, wind_phase=ph, leaf_rand=ph)
        ring = [c + Vector((math.cos(rot + 2 * np.pi * j / k) * R, math.sin(rot + 2 * np.pi * j / k) * R,
                            .002 + .004 * math.sin(3 * j * 2 * np.pi / k + ph * 6) * (j % 2))) for j in range(k)]
        r0 = G.add_verts(ring, wind_branch=.05, wind_leaf=.35, wind_phase=ph, leaf_rand=ph)
        for j in range(k):
            j1 = (j + 1) % k
            ua = (u0 + .25 + .23 * math.cos(2 * np.pi * j / k), v0 + .25 + .23 * math.sin(2 * np.pi * j / k))
            ub = (u0 + .25 + .23 * math.cos(2 * np.pi * j1 / k), v0 + .25 + .23 * math.sin(2 * np.pi * j1 / k))
            G.add_face((ctr, r0 + j, r0 + j1), ((u0 + .25, v0 + .25), ua, ub), 0)
        mid = (R0 + c) * .5 + Vector((rng.normal(0, .15), rng.normal(0, .15), 0))          # petiole: slack curve down to the rhizome
        pts = [R0.lerp(mid, t) .lerp(mid.lerp(c - Vector((0, 0, .01)), t), t) for t in np.linspace(0, 1, 8)]
        rope(G, pts, .004, .003, 4, 3, ph, 0.0, .04)
    for f in range(P['flowers']):
        a = rng.uniform(0, 2 * np.pi); r = P['radius'] * .7 * math.sqrt(rng.random()); ph = rng.random()
        c = Vector((math.cos(a) * r, math.sin(a) * r, .012))
        pts = [R0.lerp(c, t) + Vector((math.sin(t * 3 + f) * .08, 0, 0)) * (1 - t) for t in np.linspace(0, 1, 8)]
        rope(G, pts, .005, .004, 5, 3, ph, 0.0, .04)
        PL.flower(G, c, UP, P.get('petals', 14), P['petal_L'], P['petal_W'], .5, 1, 2, ph, 1.0, 'lance', P['petal_L'] * .22, 2, 0, rng,
                  P['petal_L'] * .15)
        for s_ in range(4):                                      # green sepals under the petals
            o_ = rot_about(Vector((1, 0, 0)), UP, 2 * np.pi * s_ / 4 + .4)
            PL.petal(G, c - UP * .004, (o_ + UP * .15).normalized(), UP, P['petal_L'] * .95, P['petal_W'] * 1.2, .25, 3, ph, 1.0, 'lance', rng=rng)


BUILDERS = dict(succulent=succulent, ivy=ivy, waterlily=waterlily)

GRASS_G = PL.GRASS_G
PLANTS = [
    # ------------------------------------------------------------------ R-06 GREEN PLAINS
    dict(name='PL_G01_TALL_GRASS', common='Tall plains grass (spring)', latin='Themeda triandra / Sehima (tall grass mosaic)', label=SI,
         region='R-06', category='Grass', kind='grass', seed=6101, habitat='tall-grass patches of the plains (knee to waist height); spring = green, last year\'s straw at the base',
         P=dict(blades=220, radius=.22, h=.95, w=.007, bend=1.1, spread=20, splay=.35, segs=7, dry=.16, thatch=.32),
         mats=[('grass', [(0, '#34501F'), (.55, '#62883A'), (1, '#A4B060')]), ('grass', [(0, '#4A4626'), (.5, '#9A8A50'), (1, '#CDB980')])],
         palette=['#34501F', '#62883A', '#A4B060', '#CDB980']),
    dict(name='PL_G02_DOOB_GRASS', common='Doob / Bermuda grass (short sward)', latin='Cynodon dactylon', label=SI, region='R-06 (also R-01 paths)',
         category='Grass', kind='grass', seed=6102, habitat='short grazed sward between the tall patches, along paths and riverbanks',
         P=dict(blades=320, radius=.14, h=.11, w=.0028, bend=1.6, spread=45, splay=.7, segs=4, dry=.2, thatch=.3, curl=.2),
         mats=[('grass', [(0, '#2E4A1E'), (.55, '#557E30'), (1, '#8AA450')]), ('grass', [(0, '#4A4A26'), (.5, '#8A8450'), (1, '#BDB07A')])],
         palette=['#2E4A1E', '#557E30', '#8AA450']),
    dict(name='PL_F01_WILD_MUSTARD', common='Wild mustard (spring yellow drifts)', latin='Sinapis arvensis / Brassica juncea (wild)', label=SI,
         region='R-06', category='Wildflower', kind='herb', seed=6111, habitat='SPRING key colour of the plains: yellow drifts along field edges + fallow ground',
         P=dict(h=.75, stems=14, spread=20, basal=5, stem_leaves=3, leaf_l=.11, leaf_w=.05, leaf_shape='obovate', leaf_rough=.3, stem_r=.0025,
                flower=dict(type='radial', n=4, L=.009, W=.008, cup=.35, shape='obovate', centre=.002)),
         mats=[('herbleaf', '#4E7034'), ('petal', '#E8C41E'), ('simple', '#B89A1A')], palette=['#E8C41E', '#B89A1A', '#4E7034']),
    dict(name='PL_F02_GLOBE_THISTLE', common='Globe thistle', latin='Echinops cornigerus / E. echinatus', label=SI, region='R-06 (dry hills, rocky patches)',
         category='Wildflower', kind='herb', seed=6112, habitat='dry stony hillocks of the plains; spiny grey-green leaves, steel-blue globe heads',
         P=dict(h=.6, stems=4, spread=14, basal=7, stem_leaves=4, leaf_l=.13, leaf_w=.04, leaf_shape='lance', leaf_rough=.45, stem_r=.0035,
                flower=dict(type='ball', n=70, R=.018, L=.006, W=.004)),
         mats=[('herbleaf', '#6E7E62'), ('petal', '#6A78B0'), ('simple', '#8A90A8')], palette=['#6A78B0', '#8A90A8', '#6E7E62']),
    dict(name='PL_F03_WHITE_CLOVER', common='White clover', latin='Trifolium repens', label=SI, region='R-06 (also R-01 meadows)', category='Wildflower',
         kind='herb', seed=6113, habitat='moist sward, path edges and river meadows; low trefoil leaves + white-pink ball heads (spring)',
         P=dict(h=.11, stems=6, spread=30, basal=14, leaf_l=.018, leaf_w=.016, leaf_shape='round', leaf_droop=.1, stem_r=.0012,
                flower=dict(type='ball', n=34, R=.009, L=.0055, W=.003)),
         mats=[('herbleaf', '#3E6A2E'), ('petal', '#F2ECE2'), ('simple', '#D8B8B0')], palette=['#F2ECE2', '#D8B8B0', '#3E6A2E']),
    # ------------------------------------------------------------------ R-08 CRYSTAL LAKES
    dict(name='LK_AQ01_WATER_LILY', common='White water-lily', latin='Nymphaea alba / N. tetragona', label=SI, region='R-08 (still bays)',
         category='Aquatic plant', kind='waterlily', seed=8101, water=True, habitat='still, clear bays of the lakes (0.5–2 m deep); pads float, flowers open AT the surface',
         P=dict(pads=22, radius=1.0, pad_r=.16, flowers=4, petals=14, petal_L=.055, petal_W=.02, depth=.9, atlas='lk_lily'),
         mats=[('leaf', 'lk_lily'), ('petal', '#F4F0E6'), ('simple', '#E8C43A'), ('simple', '#5A6A3A')],
         wind=dict(branch=.05, leaf=.012), palette=['#2F5A2A', '#4E6A2E', '#F4F0E6', '#E8C43A']),
    dict(name='LK_AQ02_SEDGE', common='Lake-shore sedge', latin='Carex (tussock sedge)', label=SI, region='R-08 (shore + wet meadows)', category='Aquatic plant',
         kind='grass', seed=8102, habitat='wet shore belt and boggy meadows around the lakes; stiff arching blades, dense tussocks',
         P=dict(blades=170, radius=.18, h=.62, w=.007, bend=1.0, spread=24, splay=.45, segs=6, dry=.18, thatch=.35, curl=.25),
         mats=[('grass', [(0, '#2E4422'), (.55, '#5A7A3A'), (1, '#94A266')]), ('grass', [(0, '#4A4226'), (.5, '#8A7E4A'), (1, '#B8A878')])],
         palette=['#2E4422', '#5A7A3A', '#94A266']),
    dict(name='LK_AQ03_REED_SPRING', common='Common reed — SPRING (green, no plumes)', latin='Phragmites australis', label=SI,
         region='R-08 (reed belts) + R-06 rivers', category='Aquatic plant', kind='grass', seed=8103,
         habitat='reed belts in shallow water + river margins; SPRING look (Decision 01 §6) — the feathery plumes appear only late summer / autumn',
         P=dict(blades=90, radius=.3, h=2.2, w=.016, bend=1.4, spread=12, splay=.25, segs=8, dry=.14, thatch=.3, plumes=0, plume_size=.4),
         mats=[('grass', [(0, '#3A4E24'), (.6, '#62843A'), (1, '#A0AE6A')]), ('grass', [(0, '#5A5030'), (.5, '#9A8A58'), (1, '#C8B888')])],
         palette=['#3A4E24', '#62843A', '#A0AE6A']),
    dict(name='LK_M01_WET_ROCK_MOSS', common='Wet-rock moss', latin='Fontinalis / Hygrohypnum-like', label=SI, region='R-08 (splash zone, wet rocks)',
         category='Moss', kind='moss', seed=8141, P=dict(n=14, radius=.3, r=.12, flat=.3, sporophytes=40),
         mats=[('moss', ('#24401E', '#466A2A', '#5A6A3A')), ('simple', '#7A5A2A')], palette=['#24401E', '#466A2A', '#5A6A3A']),
    # ------------------------------------------------------------------ R-04 GOLDEN DESERT
    dict(name='DS_S01_CALOTROPIS', common='Aak / Sodom apple', latin='Calotropis procera', label=SI, region='R-04 (desert edge, wadis)',
         category='Desert shrub', kind='herb', seed=4101, habitat='sandy desert edge, roadsides and wadis; big waxy grey-green leaves, lavender-white star flowers',
         P=dict(h=1.5, stems=8, spread=22, basal=0, stem_leaves=12, leaf_l=.15, leaf_w=.085, leaf_shape='oval', leaf_rough=.08, stem_r=.012, stem_grav=.02,
                flower=dict(type='radial', n=5, L=.013, W=.009, cup=.25, shape='oval', centre=.004, centre_h=.005)),
         mats=[('herbleaf', '#8A9A7A'), ('petal', '#D8C8E0'), ('simple', '#8A5A8A')], wind=dict(branch=.12, leaf=.02),
         palette=['#8A9A7A', '#B0BCA4', '#D8C8E0', '#8A5A8A']),
    dict(name='DS_G01_SEWAN_GRASS', common='Sewan desert grass', latin='Lasiurus sindicus', label=SI, region='R-04 (interdune hollows)',
         category='Grass', kind='grass', seed=4102, habitat='interdune hollows and sandy flats; tough blue-green tussocks with much dead straw',
         P=dict(blades=150, radius=.16, h=.62, w=.0045, bend=1.2, spread=30, splay=.5, segs=6, dry=.5, thatch=.5, curl=.25),
         mats=[('grass', [(0, '#4A5232'), (.55, '#7A8A5A'), (1, '#AAB084')]), ('grass', [(0, '#6A5A3A'), (.5, '#AA9466'), (1, '#D8C49A')])],
         palette=['#7A8A5A', '#AAB084', '#D8C49A']),
    dict(name='DS_S02_EUPHORBIA', common='Leafless candelabra spurge', latin='Euphorbia caducifolia', label=SI, region='R-04 (rocky slopes)',
         category='Succulent', kind='succulent', seed=4103, habitat='rocky slopes and stony desert; leafless ribbed green stems with paired spines (cactus-like, NOT a cactus)',
         P=dict(h=1.7, r=.035, arms=9, ribs=5, rib_amp=.17, spine=.007, trunk=.3, upturn=2.4, base_shoots=4),
         mats=[('succulent', '#56704A'), ('simple', '#4A3A2A')], wind=dict(branch=.01, leaf=.0),
         palette=['#56704A', '#7A8A5A', '#4A3A2A']),
    # ------------------------------------------------------------------ R-05 FORBIDDEN LANDS
    dict(name='FB_M01_ASH_LICHEN', common='Grey crust lichen', latin='Lecanora / Xanthoparmelia-like crust', label=SI, region='R-05 (rim rocks)',
         category='Lichen', kind='moss', seed=5141, habitat='rocks of the crater rim; flat grey crusts — almost the only life (approved dead look)',
         P=dict(n=12, radius=.25, r=.09, flat=.08, sporophytes=0),
         mats=[('moss', ('#6E7268', '#A4A898', '#8A8670')), ('simple', '#5A5A52')], palette=['#6E7268', '#A4A898', '#8A8670']),
    dict(name='FB_G01_HARDY_GRASS', common='Hardy rim grass', latin='Aristida (three-awn) / Cenchrus — sparse', label=SI, region='R-05 (outer rim only)',
         category='Grass', kind='grass', seed=5102, habitat='only on the OUTER rim of the crater; thin, mostly dry, very sparse (crater floor + lake shore stay lifeless)',
         P=dict(blades=55, radius=.1, h=.32, w=.0028, bend=1.3, spread=34, splay=.6, segs=5, dry=.7, thatch=.55, curl=.3),
         mats=[('grass', [(0, '#4A4A30'), (.55, '#6E704A'), (1, '#9A9670')]), ('grass', [(0, '#5A5440'), (.5, '#948A6A'), (1, '#C0B49A')])],
         palette=['#6E704A', '#948A6A', '#C0B49A']),
    # ------------------------------------------------------------------ C-01 / C-02 / C-03 surroundings (overgrown ruins — ruined vs inhabited NOT CONFIRMED)
    dict(name='CT_V01_IVY_CURTAIN', common='Ivy curtain on stone', latin='Hedera nepalensis (Himalayan ivy)', label=SI, region='C-01 / C-02 / C-03 (walls)',
         category='Climber', kind='ivy', seed=9101, habitat='walls, pillars and rock faces at the three sites (proposal for the overgrown look); place against a wall facing −Y',
         P=dict(h=3.2, w=2.4, stems=7, r=.007, density=.85, per=2, hang=12, atlas='ct_ivy', scale=1.0),
         mats=[('bark', 'bark_brown_01'), ('leaf', 'ct_ivy')], wind=dict(branch=.04, leaf=.03), palette=['#1E3A22', '#2E4A2A', '#9AB08A', '#4A4A30']),
    dict(name='CT_M01_RUIN_MOSS', common='Ruin moss (ledges, steps)', latin='Bryum / Tortula-like', label=SI, region='C-01 / C-02 / C-03',
         category='Moss', kind='moss', seed=9141, habitat='ledges, steps and joints of old masonry at the sites', P=dict(n=10, radius=.22, r=.08, flat=.35, sporophytes=60),
         mats=[('moss', ('#3A5424', '#6A8A38', '#8A8A55')), ('simple', '#9A6A30')], palette=['#3A5424', '#6A8A38', '#8A8A55']),
    dict(name='CT_G01_CRACK_GRASS', common='Grass in cracks', latin='Poa annua / Eragrostis (pioneer grasses)', label=SI, region='C-01 / C-02 / C-03',
         category='Grass', kind='grass', seed=9102, habitat='cracks between paving stones and wall joints at the sites',
         P=dict(blades=60, radius=.05, h=.16, w=.003, bend=1.2, spread=40, splay=.6, segs=4, dry=.25, thatch=.3),
         mats=[('grass', [(0, '#34501F'), (.55, '#5E8A34'), (1, '#9AB25A')]), ('grass', [(0, '#4A4A22'), (.5, '#8A8A4A'), (1, '#B8B070')])],
         palette=['#34501F', '#5E8A34', '#9AB25A']),
    # ------------------------------------------------------------------ CV-01…05 HIDDEN UNDERGROUND (no glow — Decision 01 approved glow for R-02 only)
    dict(name='CV_M01_PALE_CAVE_MOSS', common='Pale cave-mouth moss', latin='Schistostega / Fissidens-like (low-light moss)', label=SI,
         region='CV-01…05 (entrance twilight zone)', category='Moss', kind='moss', seed=7141,
         habitat='only in the twilight zone of cave entrances (some daylight); pale yellow-green, thin',
         P=dict(n=12, radius=.25, r=.09, flat=.22, sporophytes=30),
         mats=[('moss', ('#5A6A3A', '#8A9A5A', '#9A9A7A')), ('simple', '#8A7A4A')], palette=['#5A6A3A', '#8A9A5A', '#9A9A7A']),
    dict(name='CV_MU01_CAVE_FUNGI', common='Pale cave fungi', latin='Mycena / Coprinellus-like (no glow)', label=SI, region='CV-01…05 (wet rock, rotting roots)',
         category='Mushroom', kind='mushrooms', seed=7151, habitat='wet rock + rotting roots deeper in the caves; thin pale stems, small caps. NO bioluminescence (proposal only)',
         P=dict(n=16, radius=.08, h=.07, cap=.012, dome=1.6),
         mats=[('simple', '#D8D2C4'), ('simple_var', ('#B8AA94', '#8A7A66')), ('simple', '#C8BEAE')], palette=['#D8D2C4', '#B8AA94', '#8A7A66']),
    dict(name='CV_V01_ROOT_CURTAIN', common='Root curtain (from the surface)', latin='tree roots hanging through the cave ceiling', label=SI,
         region='CV-01…05 (shallow caves under forests)', category='Roots (hanging)', kind='vine', hanging=True, seed=7161,
         habitat='shallow caves below forests: fine roots hang from the ceiling; attach the top at the ceiling (z_top)',
         P=dict(h=3.6, strands=22, spread=.6, r=.006, leaves_per=0, card=.1),
         mats=[('bark', 'bark_brown_01')], wind=dict(branch=.06, leaf=.0), palette=['#5A4A3A', '#7A6A54', '#3A3028']),
    # ------------------------------------------------------------------ R-02 ENCHANTED FOREST addition (approved fantasy, subtle glow)
    dict(name='EF_M02_GLOW_MOSS', common='Glow moss (dusk)', latin='fictional (moss with faintly glowing spore capsules)', label=PF, region='R-02',
         category='Rare fantasy moss', kind='moss', seed=2242,
         habitat='R-02 only (approved fantasy variety, Decision 01 §3): on old roots and logs in the deepest shade; capsules glow faintly at dusk / night (emission 0.15)',
         P=dict(n=18, radius=.4, r=.14, flat=.3, sporophytes=160),
         mats=[('moss', ('#24483A', '#3E6A4E', '#5A7A5A')), ('glow_dim', '#8FE6D2')], palette=['#24483A', '#3E6A4E', '#8FE6D2']),
]


def plant_mats(D):
    """milestone-1 material kinds + 'succulent' (waxy ribbed skin with bloom, scars)."""
    out = []
    for i, (kind, v) in enumerate(D['mats']):
        nm = f"MAT_T6_{D['name']}_{i}"
        if kind == 'succulent':
            out.append(K.mat_simple(nm, v, rough=.5, var_col='#7E8A62', var_scale=5.0, coat=.08, spec=.35))
        else:
            out += PL.plant_mats(dict(name=D['name'], mats=[(kind, v)]))
            out[-1].name = nm
    return out


def build_plant(D, seed=0, collection=None):
    """milestone-2 plants: new builders here, the rest via the milestone-1 builders (same Geo / stats)."""
    import bpy
    rng = np.random.default_rng(D['seed'] * 1000 + seed)
    G = K.Geo()
    (BUILDERS.get(D['kind']) or PL.BUILDERS[D['kind']])(G, rng, D['P'])
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

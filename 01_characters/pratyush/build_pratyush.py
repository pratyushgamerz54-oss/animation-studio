"""Build CHAR_PRATYUSH from scratch (design-sheet v1 proposal).

Run:  python3 01_characters/pratyush/build_pratyush.py
Out:  01_characters/pratyush/blend/pratyush_v001.blend
All appearance values are PROPOSALS (see design/DESIGN_SHEET.md, U-04).
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import bpy
from mathutils import Vector
import charkit as ck
from pratyush_spec import SPEC, PAL, EXPRESSIONS, MOUTH_SHAPES, BROW_SHAPES

N = 'PRATYUSH'
H = SPEC['height_m']


def name(part):
    return f'CHAR_{N}_{part}'


# ---------------------------------------------------------------- collections
def collections():
    root = ck.get_coll('CHARACTERS')
    c = {k: ck.get_coll(f'{k}_{N}', root) for k in
         ('BODY', 'FACE', 'HAIR', 'CLOTHING', 'ACCESSORIES', 'RIG', 'CONTROLS', 'VFX')}
    c['ROOT'] = root
    return c


# ---------------------------------------------------------------- materials
def materials():
    m = {}
    m['skin'] = ck.principled('MAT_PRATYUSH_SKIN', PAL['skin'], rough=0.48, sss=0.18,
                              sss_radius=(1.0, 0.4, 0.25), bump=0.15, bump_scale=600, spec=0.45)
    m['lip'] = ck.principled('MAT_PRATYUSH_LIP', PAL['lip'], rough=0.38, sss=0.15)
    m['mouth'] = ck.mouth_interior_material('MAT_PRATYUSH_MOUTH')
    m['eye'] = ck.eye_material('MAT_PRATYUSH_EYE', PAL['eye'], PAL['eye_dark'], glow_hex=PAL['power_eye'])
    m['lid'] = ck.lid_material('MAT_PRATYUSH_LID', PAL['skin'])
    m['hair'] = ck.principled('MAT_PRATYUSH_HAIR', PAL['hair'], rough=0.42, sheen=0.5, spec=0.35)
    m['hair_streak'] = ck.principled('MAT_PRATYUSH_HAIR_STREAK', PAL['hair_streak'], rough=0.35, sheen=0.4,
                                     emit=PAL['hair_streak'], emit_strength=0.0)
    m['brow'] = ck.principled('MAT_PRATYUSH_BROW', PAL['hair'], rough=0.75, spec=0.2)
    m['suit'] = ck.attr_mix_material('MAT_PRATYUSH_SUIT', 'accent', PAL['suit'], PAL['accent'],
                                     threshold=0.80, rough=0.45, sheen=0.35, accent_emit=0.8, bump=0.35)
    m['armor'] = ck.attr_mix_material('MAT_PRATYUSH_ARMOR', 'accent', PAL['armor'], PAL['accent'],
                                      threshold=0.8, rough=0.32, sheen=0.0, accent_emit=1.0, bump=0.1)
    m['armor'].node_tree.nodes['BSDF'].inputs['Metallic'].default_value = 0.65
    m['boot'] = ck.attr_mix_material('MAT_PRATYUSH_BOOT', 'accent', PAL['boot'], PAL['shoe_sole'],
                                     threshold=0.6, rough=0.4, sheen=0.1, accent_emit=0.6, bump=0.1)
    m['glove'] = ck.principled('MAT_PRATYUSH_GLOVE', PAL['glove'], rough=0.45, sheen=0.2, bump=0.2, bump_scale=800)
    m['belt'] = ck.principled('MAT_PRATYUSH_BELT', PAL['belt'], rough=0.45, bump=0.2, bump_scale=500)
    m['metal'] = ck.principled('MAT_PRATYUSH_METAL', PAL['metal'], rough=0.25, metal=1.0)
    m['core'] = ck.emission('MAT_PRATYUSH_CORE', PAL['power_glow'], 6.0)
    m['zip'] = ck.principled('MAT_PRATYUSH_ZIP', PAL['metal'], rough=0.3, metal=1.0)
    return m


# ---------------------------------------------------------------- body
def body_skeleton():
    """Joint skeleton in T-pose. Returns joints, edges, radii, named index map."""
    J, E, R, idx = [], [], [], {}

    def j(nm, co, r, parent=None):
        idx[nm] = len(J)
        J.append(Vector(co))
        R.append(r)
        if parent is not None:
            E.append((idx[parent], idx[nm]))

    s = SPEC
    # torso (radii: (x-width, y-depth) — see build notes)
    j('pelvis', (0, 0.012, 0.97), (0.155, 0.105))
    j('waist', (0, 0.006, 1.09), (0.130, 0.090), 'pelvis')
    j('spine', (0, 0.004, 1.20), (0.142, 0.096), 'waist')
    j('chest', (0, -0.006, 1.31), (0.165, 0.108), 'spine')
    j('chest_up', (0, 0.002, 1.40), (0.160, 0.096), 'chest')
    j('neck', (0, 0.016, 1.475), (0.054, 0.056), 'chest_up')
    j('neck_top', (0, 0.020, 1.555), (0.050, 0.052), 'neck')
    for sd, sx in (('L', 1), ('R', -1)):
        # arm (T-pose, along X)
        j(f'shoulder_{sd}', (sx * 0.185, 0.0, 1.425), (0.062, 0.058), 'chest_up')
        j(f'uparm_{sd}', (sx * 0.33, 0.0, 1.43), (0.047, 0.050), f'shoulder_{sd}')
        j(f'elbow_{sd}', (sx * 0.47, 0.0, 1.43), (0.040, 0.040), f'uparm_{sd}')
        j(f'forearm_{sd}', (sx * 0.58, 0.0, 1.43), (0.040, 0.036), f'elbow_{sd}')
        j(f'wrist_{sd}', (sx * 0.72, 0.0, 1.43), (0.028, 0.022), f'forearm_{sd}')
        j(f'palm_{sd}', (sx * 0.79, 0.0, 1.43), (0.040, 0.016), f'wrist_{sd}')
        # fingers: index, middle, ring, pinky  (y offsets across the palm)
        for fn, fy, fl in (('index', -0.026, 0.092), ('middle', -0.008, 0.100),
                           ('ring', 0.010, 0.094), ('pinky', 0.026, 0.078)):
            base = sx * 0.825
            seg = [0.0, 0.45, 0.75, 1.0]
            prev = f'palm_{sd}'
            for k, t in enumerate(seg):
                nm = f'{fn}{k}_{sd}'
                r = 0.0088 * (1 - 0.22 * t) * (0.85 if fn == 'pinky' else 1.0)
                j(nm, (base + sx * fl * t, fy, 1.43 - 0.004 * t), (r, r * 0.9), prev)
                prev = nm
        # thumb: from wrist, forward (-Y) and out
        prev = f'wrist_{sd}'
        for k, (tx, ty, tz) in enumerate(((0.745, -0.024, 1.422), (0.775, -0.046, 1.420),
                                          (0.800, -0.062, 1.419), (0.822, -0.074, 1.418))):
            nm = f'thumb{k}_{sd}'
            r = 0.0115 * (1 - 0.18 * k)
            j(nm, (sx * tx, ty, tz), (r, r * 0.95), prev)
            prev = nm
        # leg
        j(f'hip_{sd}', (sx * 0.092, 0.0, 0.90), (0.088, 0.090), 'pelvis')
        j(f'thigh_{sd}', (sx * 0.098, 0.0, 0.70), (0.070, 0.074), f'hip_{sd}')
        j(f'knee_{sd}', (sx * 0.100, -0.008, 0.49), (0.050, 0.054), f'thigh_{sd}')
        j(f'calf_{sd}', (sx * 0.100, 0.006, 0.34), (0.052, 0.056), f'knee_{sd}')
        j(f'ankle_{sd}', (sx * 0.100, 0.010, 0.085), (0.032, 0.036), f'calf_{sd}')
        j(f'ball_{sd}', (sx * 0.102, -0.115, 0.030), (0.044, 0.026), f'ankle_{sd}')
        j(f'toe_{sd}', (sx * 0.104, -0.185, 0.026), (0.038, 0.020), f'ball_{sd}')
        j(f'heel_{sd}', (sx * 0.100, 0.040, 0.030), (0.032, 0.026), f'ankle_{sd}')
    return J, E, R, idx


def build_body(C, M):
    J, E, R, idx = body_skeleton()
    body = ck.skin_body(name('BODY'), C['BODY'], J, E, R, subdiv_base=1)
    # anatomy pass: (centre, sigma xyz, amplitude, mirror)
    ck.sculpt(body, [
        ((0.068, -0.095, 1.335), (0.055, 0.04, 0.045), 0.010, True),   # pecs
        ((0.205, 0.0, 1.435), (0.045, 0.05, 0.045), 0.010, True),      # deltoids
        ((0.085, 0.03, 1.475), (0.05, 0.04, 0.03), 0.012, True),       # trapezius
        ((0.090, 0.095, 1.36), (0.05, 0.03, 0.07), 0.006, True),       # scapula
        ((0.070, 0.105, 0.925), (0.06, 0.04, 0.06), 0.016, True),      # glutes
        ((0.100, 0.050, 0.37), (0.04, 0.03, 0.07), 0.009, True),       # calves
        ((0.100, -0.060, 0.73), (0.04, 0.03, 0.10), 0.006, True),      # quads
        ((0.30, 0.0, 1.45), (0.06, 0.04, 0.03), 0.006, True),          # biceps/triceps top
        ((0.56, 0.0, 1.44), (0.05, 0.04, 0.03), 0.004, True),          # forearm
        ((0.0, -0.095, 1.17), (0.07, 0.04, 0.06), -0.004, False),      # flat abdomen
        ((0.035, -0.06, 1.445), (0.05, 0.03, 0.012), 0.003, True),     # collarbone
    ])
    ck.assign(body, M['skin'])
    ck.store_rest_attrs(body)
    return body, idx


# ---------------------------------------------------------------- head
HEAD_C = Vector((0, 0.006, 1.642))    # head centre (world); top = 1.75 m
SX, SY = 0.080, 0.100                 # half width / half depth
SZT, SZB = 0.108, 0.124               # half height above / below centre


def lerp_table(x, table):
    """Piecewise-linear lookup; table = [(x0,y0),(x1,y1),...] with x ascending."""
    if x <= table[0][0]:
        return table[0][1]
    for (a, fa), (b, fb) in zip(table, table[1:]):
        if x <= b:
            t = (x - a) / (b - a)
            t = t * t * (3 - 2 * t)
            return fa + (fb - fa) * t
    return table[-1][1]


def head_shape(p):
    x, y, z = p.x, p.y, p.z
    G = ck.gauss
    X, Y = x * SX, y * SY
    Z = z * (SZT if z > 0 else SZB)
    # width profile: cranium -> cheek -> jaw angle -> chin
    X *= lerp_table(z, [(-1.0, 0.56), (-0.64, 0.88), (-0.32, 0.97), (0.25, 1.0), (1.0, 0.92)])
    X *= 1 - 0.04 * G(z - 0.30, 0.15) * G(y + 0.2, 0.4)          # temples
    if y > 0:
        Y *= 1 - 0.50 * max(0.0, -z) ** 1.15                      # nape
        Y *= 1 + 0.06 * max(0.0, z) * y                           # occiput
    else:
        Y *= lerp_table(z, [(-1.0, 0.80), (-0.55, 0.93), (0.0, 0.97), (1.0, 1.0)])
    f = max(0.0, -y) ** 2.5                                       # front-face weight
    d = 0.0
    # nose: bridge -> tip, then sharp underside
    t = min(1.0, max(0.0, (0.06 - z) / 0.36))
    na = (0.005 + 0.021 * t ** 1.6) * ck.smoothstep(-0.40, -0.30, z)
    d += na * G(x, 0.07 + 0.06 * t) * f
    for s in (-1, 1):
        d += 0.0075 * G(x - s * 0.13, 0.05) * G(z + 0.33, 0.045) * f   # alae
        d -= 0.0100 * G(x - s * 0.40, 0.15) * G(z - 0.01, 0.11) * f    # eye sockets
        X += s * 0.0035 * G(x - s * 0.72, 0.16) * G(z + 0.12, 0.14)    # cheekbones
        d += 0.0020 * G(x - s * 0.55, 0.18) * G(z + 0.18, 0.12) * f    # cheek front
    d += 0.0060 * G(z - 0.17, 0.07) * G(x, 0.50) * f                    # brow ridge
    d += 0.0060 * G(z + 0.46, 0.08) * G(x, 0.28) * f                    # upper-lip mound
    d += 0.0035 * G(z + 0.58, 0.06) * G(x, 0.24) * f                    # lower lip
    d -= 0.0020 * G(z + 0.69, 0.05) * G(x, 0.22) * f                    # mentolabial groove
    d += 0.0075 * G(z + 0.83, 0.09) * G(x, 0.20) * f                    # chin
    Y -= d
    return Vector((X, Y, Z))


def smooth(e0, e1, x):
    return ck.smoothstep(min(e0, e1), max(e0, e1), x) if e0 < e1 else 1 - ck.smoothstep(e1, e0, x)


def build_head(C, M):
    head = ck.deformed_sphere(name('HEAD'), C['BODY'], head_shape, cuts=18)
    head.location = HEAD_C
    ck.assign(head, M['skin'])
    # ears
    for sd, sx in (('L', 1), ('R', -1)):
        def ear(p, sx=sx):
            X = p.x * 0.010
            Y = p.y * 0.017
            Z = p.z * 0.029
            # cup: push centre inward
            X -= 0.004 * max(0, 1 - (p.y ** 2 + p.z ** 2)) * (1 if p.x > 0 else 0.3)
            return Vector((X * sx, Y, Z))
        e = ck.deformed_sphere(name(f'EAR_{sd}'), C['BODY'], ear, cuts=6)
        e.location = HEAD_C + Vector((sx * (SX * 0.95), 0.014, -0.012))
        e.rotation_euler = (math.radians(-10), 0, math.radians(sx * 18))
        ck.assign(e, M['skin'])
        ck.add_subsurf(e, 1, 2)
    ck.add_subsurf(head, 1, 2)
    return head


# ---------------------------------------------------------------- face kit
EYE_R = 0.0128
EYE_X = 0.0322
EYE_Z = 0.0035      # relative to head centre


def build_face(C, M, head):
    face = {}
    bvh = ck.bvh_of(head)
    # head is located at HEAD_C; bvh is in local space
    for sd, sx in (('L', 1), ('R', -1)):
        ys = ck.surface_y(bvh, sx * EYE_X, EYE_Z)
        center = HEAD_C + Vector((sx * EYE_X, ys + EYE_R * 0.62, EYE_Z))
        eye = ck.deformed_sphere(name(f'EYE_{sd}'), C['FACE'], lambda p: p, cuts=8)
        eye.scale = (EYE_R,) * 3
        eye.location = center
        ck.assign(eye, M['eye'])
        ck.add_subsurf(eye, 1, 2)
        face[f'eye_{sd}'] = eye
        for part, up in (('LID_UP', True), ('LID_LO', False)):
            lid = ck.lid_shell(name(f'{part}_{sd}'), C['FACE'], EYE_R * 1.10, upper=up)
            lid.location = center
            ck.assign(lid, M['lid'])
            ck.add_subsurf(lid, 1, 1)
            face[f'{part.lower()}_{sd}'] = lid
    # mouth & brows are built in head-local space, then placed at HEAD_C
    mouth = ck.build_mouth(name('MOUTH'), C['FACE'], head, (0.0, -0.064), MOUTH_SHAPES,
                           [M['mouth'], M['lip']])
    mouth.location = HEAD_C
    face['mouth'] = mouth
    brows = ck.build_brows(name('BROWS'), C['FACE'], head,
                           [(-0.011, 0.0205), (0.011, 0.0205)], BROW_SHAPES, M['brow'])
    brows.location = HEAD_C
    face['brows'] = brows
    return face


def set_expression(face, expr_name):
    """Apply one of the EXPRESSIONS presets to the face kit."""
    e = EXPRESSIONS[expr_name]
    for kb_owner, key in ((face['mouth'], e['mouth']), (face['brows'], e['brows'])):
        for kb in kb_owner.data.shape_keys.key_blocks[1:]:
            kb.value = 1.0 if kb.name == key else 0.0
    up, lo = e.get('lid_up', -24), e.get('lid_lo', 30)
    for sd in ('L', 'R'):
        u = up + e.get(f'lid_up_{sd}', 0)
        face[f'lid_up_{sd}'].rotation_euler = (math.radians(u), 0, 0)
        face[f'lid_lo_{sd}'].rotation_euler = (math.radians(lo), 0, 0)
        gx, gz = e.get('gaze', (0, 0))
        face[f'eye_{sd}'].rotation_euler = (math.radians(gz), 0, math.radians(gx))


# ---------------------------------------------------------------- hair
def head_unit(co):
    """Approximate unit-sphere direction of a head-local point."""
    return Vector((co.x / SX, co.y / SY, co.z / (SZT if co.z > 0 else SZB)))


def hairline(u):
    r = math.hypot(u.x, u.y) or 1e-6
    fy = -u.y / r                       # 1 = front, 0 = side, -1 = back
    return lerp_table(fy, [(-1.0, -0.58), (-0.3, -0.20), (0.0, 0.22), (0.55, 0.42), (1.0, 0.50)])


def build_hair(C, M, head):
    import random
    rnd = random.Random(7)
    # 1) scalp cap
    cap = ck.trim_copy(head, name('HAIR_CAP'), C['HAIR'],
                       lambda co: head_unit(co).z > hairline(head_unit(co)), offset=0.0035, solid=0.004)
    cap.modifiers.clear()
    s = cap.modifiers.new('Solidify', 'SOLIDIFY'); s.thickness = 0.003; s.offset = -1.0
    ck.add_subsurf(cap, 1, 2)
    ck.assign(cap, M['hair'])
    # 2) spiky clumps: flattened, sharply tapered ribbons
    strands = []
    for p in ck.fib_sphere(300):
        u = p
        if u.z < hairline(u) + 0.02:
            continue
        r = math.hypot(u.x, u.y) or 1e-6
        fy = -u.y / r
        root = head_shape(u)
        n = u.normalized()
        side = math.copysign(1, u.x)
        if fy > 0.40 and u.z < 0.82:          # front fringe: lifts up, flicks back
            d1 = (n * 0.25 + Vector((u.x * 0.6, -0.20, 1.0))).normalized()
            d2 = Vector((u.x * 0.5, 0.75, 0.55)).normalized()
            L, W = 0.110, 0.021
        elif u.z > 0.55:                       # crown: up & back spikes
            d1 = (n * 0.55 + Vector((0, 0.40, 0.70))).normalized()
            d2 = Vector((u.x * 0.5, 0.90, 0.25)).normalized()
            L, W = 0.120, 0.022
        elif fy > -0.35:                       # sides: swept back, tight
            d1 = (n * 0.30 + Vector((side * 0.1, 0.85, 0.30))).normalized()
            d2 = Vector((side * 0.15, 0.95, 0.10)).normalized()
            L, W = 0.080, 0.018
        else:                                  # back: down-back spikes
            d1 = (n * 0.50 + Vector((0, 0.50, -0.30))).normalized()
            d2 = Vector((u.x * 0.4, 0.55, -0.70)).normalized()
            L, W = 0.080, 0.019
        L *= rnd.uniform(0.80, 1.20)
        jit = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * 0.15
        p0 = root - n * 0.004
        p1 = root + n * L * 0.12 + (d1 * L * 0.10)
        p2 = p1 + (d1 + jit).normalized() * L * 0.42
        p3 = p2 + (d2 + jit).normalized() * L * 0.48
        mi = 1 if (fy > 0.80 and 0.50 < u.z < 0.70 and 0.08 < u.x < 0.30) else 0
        strands.append({'pts': [q + HEAD_C for q in (p0, p1, p2, p3)], 'width': W * rnd.uniform(0.85, 1.15),
                        'thick': 0.0065, 'mat': mi, 'twist': rnd.uniform(-0.5, 0.5)})
    hair = ck.loft_hair(name('HAIR'), C['HAIR'], strands, HEAD_C, mats=[M['hair'], M['hair_streak']])
    ck.add_subsurf(hair, 1, 1)
    return [cap, hair]


# ---------------------------------------------------------------- clothing
def build_clothing(C, M, body, arm):
    out = {}
    bvh_body = ck.bvh_of(body)

    def acc(ob, fn):
        ck.float_attr(ob, 'accent', fn)

    import math as _m
    suit = ck.trim_copy(body, name('SUIT'), C['CLOTHING'],
                        lambda c: 0.10 < c.z < 1.515 and abs(c.x) < 0.705, offset=0.004, solid=0.002)
    acc(suit, lambda c, n: 1.0 if (
        (abs(c.x) > 0.26 and n.z > 0.86 and c.z > 1.3) or                         # arm piping
        (abs(c.x) < 0.22 and abs(n.x) > 0.975 and 0.95 < c.z < 1.36) or            # torso side lines
        (abs(c.x) > 0.04 and c.z < 0.93 and n.x * _m.copysign(1, c.x) > 0.97) or  # leg outer lines
        (c.y < -0.04 and abs(c.z - (1.21 - 0.55 * abs(c.x))) < 0.012 and abs(c.x) < 0.16)  # V chevron
    ) else 0.0)
    ck.assign(suit, M['suit'])
    out['suit'] = suit

    col = ck.trim_copy(body, name('COLLAR'), C['CLOTHING'],
                       lambda c: 1.43 < c.z < 1.535 and abs(c.x) < 0.11, offset=0.017, solid=0.005)
    acc(col, lambda c, n: 1.0 if c.z > 1.522 else 0.0)
    ck.assign(col, M['armor'])
    out['collar'] = col

    def armor(key, keep, off, edge=None):
        o = ck.trim_copy(body, name(key), C['ACCESSORIES'], keep, offset=off, solid=0.005)
        acc(o, edge or (lambda c, n: 0.0))
        bv = o.modifiers.new('Bevel', 'BEVEL'); bv.width = 0.0015; bv.segments = 2
        o.modifiers.move(len(o.modifiers) - 1, 0)
        ck.assign(o, M['armor'])
        out[key.lower()] = o
        return o

    armor('CHEST_PLATE', lambda c: c.y < -0.012 and 1.23 < c.z < 1.47 and abs(c.x) < 0.20, 0.011,
          lambda c, n: 1.0 if (c.z < 1.245 or abs(c.x) > 0.185) else 0.0)
    armor('PAULDRON_L', lambda c: 0.15 < c.x < 0.31 and c.z > 1.375, 0.019,
          lambda c, n: 1.0 if c.x > 0.29 else 0.0)
    armor('PAULDRON_R', lambda c: -0.31 < c.x < -0.15 and c.z > 1.375, 0.019,
          lambda c, n: 1.0 if c.x < -0.29 else 0.0)
    armor('KNEE_L', lambda c: c.x > 0 and 0.44 < c.z < 0.57 and c.y < 0.005, 0.014)
    armor('KNEE_R', lambda c: c.x < 0 and 0.44 < c.z < 0.57 and c.y < 0.005, 0.014)

    for sd, sx in (('L', 1), ('R', -1)):
        so = ck.trim_copy(body, name(f'BOOT_{sd}'), C['CLOTHING'],
                          lambda c, sx=sx: c.z < 0.33 and c.x * sx > 0, offset=0.011, solid=0.003)
        acc(so, lambda c, n: 1.0 if (c.z < 0.024 or 0.285 < c.z or abs(c.z - 0.16) < 0.008) else 0.0)
        ck.assign(so, M['boot'])
        out[f'boot_{sd}'] = so
        gl = ck.trim_copy(body, name(f'GLOVE_{sd}'), C['ACCESSORIES'],
                          lambda c, sx=sx: 0.698 < c.x * sx, offset=0.0028, solid=0.0015)
        ck.assign(gl, M['glove'])
        out[f'glove_{sd}'] = gl
        br = ck.trim_copy(body, name(f'BRACER_{sd}'), C['ACCESSORIES'],
                          lambda c, sx=sx: 0.60 < c.x * sx < 0.685, offset=0.014, solid=0.005)
        ck.assign(br, M['metal'])
        out[f'bracer_{sd}'] = br
        # glowing speed-core on top of each bracer
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.011, depth=0.006,
                                            location=(sx * 0.6425, 0.0, 1.43 + 0.0405))
        core = bpy.context.object
        core.name = name(f'BRACER_CORE_{sd}')
        ck.link(core, C['ACCESSORIES'])
        ck.assign(core, M['core'])
        out[f'core_{sd}'] = core

    be = ck.trim_copy(body, name('BELT'), C['ACCESSORIES'],
                      lambda c: 0.92 < c.z < 1.08 and abs(c.x) < 0.25, offset=0.010, solid=0.006)
    ck.float_attr(be, 'accent', lambda c, n: 1.0 if abs(c.z - 1.0) < 0.012 else 0.0)
    ck.assign(be, M['armor'])
    out['belt'] = be
    yb = ck.surface_y(bvh_body, 0.0, 1.0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, yb - 0.018, 1.0))
    bu = bpy.context.object
    bu.name = name('BELT_BUCKLE')
    bu.scale = (0.042, 0.006, 0.030)
    bev = bu.modifiers.new('Bevel', 'BEVEL'); bev.width = 0.002; bev.segments = 2
    ck.link(bu, C['ACCESSORIES'])
    ck.assign(bu, M['metal'])
    out['buckle'] = bu

    bvh_j = ck.bvh_of(out['chest_plate'])
    # original emblem: forward 'speed chevron' with a lightning notch (centre chest)
    bolt2d = [(0.0, 0.026), (0.034, -0.010), (0.022, -0.020), (0.004, -0.002), (0.006, -0.016),
              (-0.006, -0.008), (-0.004, -0.002), (-0.022, -0.020), (-0.034, -0.010)]
    ex, ez = 0.0, 1.36
    ev = []
    for (u, v) in bolt2d:
        x, z = ex + u * 1.2, ez + v * 1.2
        y = ck.surface_y(bvh_j, x, z)
        ev.append(Vector((x, y - 0.0015, z)))
    em = ck.mesh_object(name('EMBLEM'), ev, [tuple(range(len(ev)))], C['ACCESSORIES'])
    s = em.modifiers.new('Solidify', 'SOLIDIFY'); s.thickness = 0.0012
    ck.assign(em, M['core'])
    out['emblem'] = em
    return out


# ---------------------------------------------------------------- rig (pose proxy)
def build_rig(C, body, idx):
    J, _, _, _ = body_skeleton()
    P = lambda k: tuple(J[idx[k]])
    B = [('root', (0, 0, 0), (0, 0.25, 0), None, False, 0),
         ('pelvis', P('pelvis'), P('waist'), 'root', False, 0),
         ('spine_01', P('waist'), P('spine'), 'pelvis', True, 0),
         ('spine_02', P('spine'), P('chest'), 'spine_01', True, 0),
         ('spine_03', P('chest'), P('chest_up'), 'spine_02', True, 0),
         ('neck', P('neck'), P('neck_top'), 'spine_03', False, 0),
         ('head', P('neck_top'), (0, 0.02, 1.75), 'neck', True, 0)]
    for sd in ('L', 'R'):
        sx = 1 if sd == 'L' else -1
        B += [(f'clavicle_{sd}', (sx * 0.02, 0.0, 1.43), P(f'shoulder_{sd}'), 'spine_03', False, 0),
              (f'upperarm_{sd}', P(f'shoulder_{sd}'), P(f'elbow_{sd}'), f'clavicle_{sd}', True, 0),
              (f'forearm_{sd}', P(f'elbow_{sd}'), P(f'wrist_{sd}'), f'upperarm_{sd}', True, 0),
              (f'hand_{sd}', P(f'wrist_{sd}'), (sx * 0.825, 0.0, 1.43), f'forearm_{sd}', True, 0)]
        for fn in ('index', 'middle', 'ring', 'pinky', 'thumb'):
            par = f'hand_{sd}'
            for k in range(3):
                bn = f'{fn}_{k + 1:02d}_{sd}'
                B.append((bn, P(f'{fn}{k}_{sd}'), P(f'{fn}{k + 1}_{sd}'), par, k > 0, 0))
                par = bn
        B += [(f'thigh_{sd}', P(f'hip_{sd}'), P(f'knee_{sd}'), 'pelvis', False, 0),
              (f'shin_{sd}', P(f'knee_{sd}'), P(f'ankle_{sd}'), f'thigh_{sd}', True, 0),
              (f'foot_{sd}', P(f'ankle_{sd}'), P(f'ball_{sd}'), f'shin_{sd}', True, 0),
              (f'toe_{sd}', P(f'ball_{sd}'), P(f'toe_{sd}'), f'foot_{sd}', True, 0)]
    arm = ck.build_armature(name('RIG'), C['RIG'], B)
    return arm


POSES = {
    'T': {},
    'A': {'upperarm': 45, 'clavicle': 4},
    'NEUTRAL': {'upperarm': 74, 'clavicle': 6, 'forearm': -12, 'fingers': 14, 'thumb': 8},
}


def set_pose(arm, pose):
    ck.reset_pose(arm)
    p = POSES[pose]
    for sd, s in (('L', 1), ('R', -1)):
        if 'clavicle' in p:
            ck.world_rot(arm, f'clavicle_{sd}', (0, 1, 0), s * p['clavicle'])
        if 'upperarm' in p:
            ck.world_rot(arm, f'upperarm_{sd}', (0, 1, 0), s * (p['upperarm'] - p.get('clavicle', 0)))
        if 'forearm' in p:
            ck.world_rot(arm, f'forearm_{sd}', (0, 0, 1), s * p['forearm'])
        for fn in ('index', 'middle', 'ring', 'pinky'):
            for k in range(3):
                if 'fingers' in p:
                    ck.world_rot(arm, f'{fn}_{k + 1:02d}_{sd}', (0, 1, 0), s * p['fingers'] * (1 + 0.3 * k))
        if 'thumb' in p:
            ck.world_rot(arm, f'thumb_02_{sd}', (0, 0, 1), -s * p['thumb'])
    bpy.context.view_layer.update()


def rig_everything(C, body, arm, head_parts, cloth):
    for ob in cloth.values():
        if ob.name.endswith(('BUCKLE',)) or 'CORE' in ob.name or 'ZIP' in ob.name or 'EMBLEM' in ob.name:
            continue
        for vg in body.vertex_groups:
            ob.vertex_groups.new(name=vg.name)
        ck.bind_copy(ob, arm)
    # rigid pieces follow a single bone
    ck.bone_parent(cloth['buckle'], arm, 'pelvis')
    ck.bone_parent(cloth['emblem'], arm, 'spine_03')
    for sd in ('L', 'R'):
        ck.bone_parent(cloth[f'core_{sd}'], arm, f'forearm_{sd}')
    for ob in head_parts:
        ck.bone_parent(ob, arm, 'head')


def subdivide_display(objs):
    for ob in objs:
        if ob.type == 'MESH' and not any(m.type == 'SUBSURF' for m in ob.modifiers):
            ck.add_subsurf(ob, 1, 2)


if __name__ == '__main__':
    ck.reset()
    C = collections()
    M = materials()
    body, idx = build_body(C, M)
    head = build_head(C, M)
    face = build_face(C, M, head)
    set_expression(face, 'neutral')
    hair = build_hair(C, M, head)
    arm = build_rig(C, body, idx)
    ck.auto_weight(body, arm)
    cloth = build_clothing(C, M, body, arm)
    head_parts = [head] + [o for o in bpy.data.objects if o.name.startswith(name('EAR'))] \
        + list(face.values()) + hair
    rig_everything(C, body, arm, head_parts, cloth)
    subdivide_display([body] + list(cloth.values()))
    set_pose(arm, 'NEUTRAL')
    out = os.path.join(HERE, 'blend', 'pratyush_v001.blend')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print('SAVED', out)

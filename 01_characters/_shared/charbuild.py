"""charbuild — config-driven character builder shared by all 7 characters.

Each character folder has <id>_config.py with a CFG dict. build(CFG, out_path)
creates the complete Blender asset: body, sculpted head, face kit with expression
and phoneme shape keys, hair / beard / horns, costume pieces, accessories, pose
rig with weights, and saves the .blend.

Coordinates: metres, Z up, character faces -Y. Costume regions are written in a
normalised 1.75 m body space (c = rest position / s) so the same numbers work for
every height.
"""
import math, random
import bpy, bmesh
from mathutils import Vector, Matrix
from mathutils.kdtree import KDTree
import charkit as ck

G = ck.gauss


# ======================================================================= expressions
# mouth params: corner_l/r, open_u/open_l, width, pucker, lip_u/lip_l, v0
MOUTH = {
    'neutral': {},
    'happy': {'corner_l': .0065, 'corner_r': .0065, 'open_u': .0018, 'open_l': .0040, 'width': 1.10},
    'angry': {'corner_l': -.0026, 'corner_r': -.0026, 'open_u': .0022, 'open_l': .0022, 'width': .96},
    'furious': {'corner_l': -.0040, 'corner_r': -.0040, 'open_u': .0040, 'open_l': .0075, 'width': 1.10},
    'sad': {'corner_l': -.0061, 'corner_r': -.0061, 'width': .90},
    'fear': {'corner_l': -.0023, 'corner_r': -.0023, 'open_u': .0020, 'open_l': .0058, 'width': 1.08},
    'shocked': {'open_u': .0040, 'open_l': .0115, 'width': .74, 'pucker': .6},
    'confident': {'corner_l': .0017, 'corner_r': .0061, 'width': 1.00},
    'evil': {'corner_l': .0070, 'corner_r': .0099, 'open_u': .0030, 'open_l': .0034, 'width': 1.28},
    'manipulative': {'corner_l': .0015, 'corner_r': .0075, 'open_u': .0008, 'open_l': .0010, 'width': 1.05},
    'serious': {'corner_l': -.0012, 'corner_r': -.0012, 'width': .93, 'lip_u': .0026},
    'crying': {'corner_l': -.0073, 'corner_r': -.0073, 'open_u': .0030, 'open_l': .0080, 'width': 1.05},
    'pain': {'corner_l': -.0035, 'corner_r': -.0045, 'open_u': .0030, 'open_l': .0035, 'width': 1.15},
    'concentration': {'corner_l': -.0010, 'corner_r': -.0010, 'open_u': .0012, 'open_l': .0012, 'width': .98},
    'frustrated': {'corner_l': -.0040, 'corner_r': -.0020, 'width': .88, 'lip_u': .0024},
    'suspicious': {'corner_l': -.0005, 'corner_r': .0020, 'width': .92},
    'wise': {'corner_l': .0028, 'corner_r': .0028, 'width': 1.0},
    'disappointed': {'corner_l': -.0050, 'corner_r': -.0050, 'width': .95},
    'concerned': {'corner_l': -.0028, 'corner_r': -.0028, 'open_u': .0006, 'open_l': .0012, 'width': .94},
    # phonemes
    'PH_A': {'open_u': .0040, 'open_l': .0120}, 'PH_E': {'open_u': .0030, 'open_l': .0060, 'width': 1.15,
                                                          'corner_l': .001, 'corner_r': .001},
    'PH_I': {'open_u': .0020, 'open_l': .0040, 'width': 1.20, 'corner_l': .002, 'corner_r': .002},
    'PH_O': {'open_u': .0050, 'open_l': .0100, 'width': .70, 'pucker': .7},
    'PH_U': {'open_u': .0020, 'open_l': .0030, 'width': .56, 'pucker': 1, 'lip_u': .004, 'lip_l': .005},
    'PH_MBP': {'lip_u': .0024, 'lip_l': .0032, 'width': .97},
    'PH_FV': {'open_u': .0006, 'open_l': .0018, 'lip_l': .0030},
    'PH_L': {'open_u': .0030, 'open_l': .0070, 'width': .95},
    'PH_W': {'open_u': .0018, 'open_l': .0030, 'width': .50, 'pucker': 1, 'lip_u': .004, 'lip_l': .005},
    'PH_REST': {'open_u': .0004, 'open_l': .0006},
}
PHONEMES = ['PH_A', 'PH_E', 'PH_I', 'PH_O', 'PH_U', 'PH_MBP', 'PH_FV', 'PH_L', 'PH_W', 'PH_REST']
BROW = {
    'neutral': {}, 'happy': {'inner': .0028, 'outer': .0021},
    'angry': {'inner': -.0059, 'outer': .0028, 'arch': .001},
    'furious': {'inner': -.0075, 'outer': .0035, 'arch': .0005},
    'sad': {'inner': .0059, 'outer': -.0028, 'arch': .001}, 'fear': {'inner': .0070, 'outer': .0014},
    'shocked': {'inner': .0084, 'outer': .0070, 'arch': .004}, 'confident': {'l_extra': .0045},
    'evil': {'inner': -.0056, 'outer': .0042, 'l_extra': .0028},
    'manipulative': {'inner': -.0020, 'outer': .0030, 'l_extra': .0040},
    'serious': {'inner': -.0022, 'outer': .0007}, 'crying': {'inner': .0073, 'outer': -.0031},
    'pain': {'inner': .0050, 'outer': -.0030, 'arch': .0005},
    'concentration': {'inner': -.0050, 'outer': -.0005},
    'frustrated': {'inner': -.0035, 'outer': -.0010, 'l_extra': -.0015},
    'suspicious': {'inner': -.0030, 'outer': .0000, 'l_extra': .0040},
    'wise': {'inner': .0015, 'outer': .0000},
    'disappointed': {'inner': .0035, 'outer': -.0020},
    'concerned': {'inner': .0050, 'outer': -.0005},
}
LIDS = {  # upper (more negative = more open), lower (larger = more open)
    'neutral': (-24, 30), 'happy': (-22, 12), 'angry': (-11, 22), 'furious': (-14, 24), 'sad': (-13, 28),
    'fear': (-42, 42), 'shocked': (-48, 46), 'confident': (-17, 24), 'evil': (-11, 16),
    'manipulative': (-13, 20), 'serious': (-17, 26), 'crying': (2, 8), 'pain': (-2, 10),
    'concentration': (-9, 18), 'frustrated': (-13, 24), 'suspicious': (-8, 18), 'wise': (-16, 20),
    'disappointed': (-10, 28), 'concerned': (-26, 32), 'blink': (6, -4),
}
EXTRA = {'sad': {'gaze': (0, -10)}, 'disappointed': {'gaze': (0, -12)}, 'confident': {'lid_up_L': -6},
         'suspicious': {'lid_up_L': -8, 'gaze': (8, 0)}, 'crying': {'tears': True}, 'manipulative': {'gaze': (-6, 0)}}


def expression(nm):
    up, lo = LIDS[nm]
    e = {'mouth': nm if nm in MOUTH else 'neutral', 'brows': nm if nm in BROW else 'neutral',
         'lid_up': up, 'lid_lo': lo}
    e.update(EXTRA.get(nm, {}))
    return e


# ======================================================================= builder
class Char:
    def __init__(self, cfg):
        self.cfg = cfg
        self.id = cfg['id']
        self.s = cfg.get('height', 1.75) / 1.75
        self.b = dict(shoulder=1, chest=1, waist=1, hip=1, limb=1, muscle=1, neck=1, belly=0, legs=1)
        self.b.update(cfg.get('build', {}))
        self.h = dict(size=1, width=1, depth=1, jaw=1, chin=1, cheek=1, nose=1, nose_w=1, brow=1,
                      cranium=1, ears='human', age=0, lips=1)
        self.h.update(cfg.get('head', {}))
        self.objs = {}

    def nm(self, part):
        return f'CHAR_{self.id}_{part}'

    # ------------------------------------------------------------- collections
    def collections(self):
        root = ck.get_coll('CHARACTERS')
        self.C = {k: ck.get_coll(f'{k}_{self.id}', root) for k in
                  ('BODY', 'FACE', 'HAIR', 'CLOTHING', 'ACCESSORIES', 'RIG', 'CONTROLS', 'VFX')}
        self.C['MATERIALS'] = ck.get_coll(f'MATERIALS_{self.id}', root)

    # ------------------------------------------------------------- materials
    def materials(self):
        cfg, P = self.cfg, self.cfg['pal']
        M = {}
        sk = cfg.get('skin', {})
        M['skin'] = ck.skin_material(f'MAT_{self.id}_SKIN', P['skin'], P.get('skin_tint', P['skin']),
                                     rough=sk.get('rough', 0.48), sss=sk.get('sss', 0.18),
                                     age=self.h['age'])
        M['lip'] = ck.principled(f'MAT_{self.id}_LIP', P.get('lip', P['skin']), rough=0.38, sss=0.15)
        M['mouth'] = ck.mouth_interior_material(f'MAT_{self.id}_MOUTH', teeth_hex=P.get('teeth', '#EEE9E0'))
        ey = cfg.get('eye', {})
        M['eye'] = ck.eye_material(f'MAT_{self.id}_EYE', P['eye'], P.get('eye_dark', '#2A170C'),
                                   sclera_hex=P.get('sclera', '#EDE8E2'), glow_hex=P.get('power_eye', P['eye']),
                                   base_glow=ey.get('base_glow', 0.0))
        M['lid'] = ck.lid_material(f'MAT_{self.id}_LID', P['skin'], lash_hex=P.get('lash', '#120E0C'))
        hc = P.get('hair', '#17120F')
        M['hair'] = ck.hair_material(f'MAT_{self.id}_HAIR', hc, P.get('hair_tip', hc),
                                     rough=cfg.get('hair', {}).get('rough', 0.42))
        M['hair_streak'] = ck.principled(f'MAT_{self.id}_HAIR_STREAK', P.get('hair_streak', hc), rough=0.35,
                                         sheen=0.4, emit=P.get('hair_streak', hc), emit_strength=0.0)
        M['brow'] = ck.principled(f'MAT_{self.id}_BROW', P.get('brow', hc), rough=0.75, spec=0.2)
        for k, d in cfg.get('materials', {}).items():
            t = d.get('type', 'principled')
            mn = f'MAT_{self.id}_{k.upper()}'
            if t == 'emission':
                M[k] = ck.emission(mn, d['base'], d.get('strength', 6))
            elif t == 'accent':
                M[k] = ck.attr_mix_material(mn, 'accent', d['base'], d['accent'], threshold=d.get('threshold', 0.8),
                                            rough=d.get('rough', 0.5), sheen=d.get('sheen', 0.2),
                                            accent_emit=d.get('emit', 0.0), bump=d.get('bump', 0.2))
                M[k].node_tree.nodes['BSDF'].inputs['Metallic'].default_value = d.get('metal', 0.0)
            elif t == 'glass':
                M[k] = ck.principled(mn, d['base'], rough=d.get('rough', 0.05))
                M[k].node_tree.nodes['BSDF'].inputs['Transmission Weight'].default_value = 1.0
            else:
                M[k] = ck.principled(mn, d['base'], rough=d.get('rough', 0.5), metal=d.get('metal', 0.0),
                                     sheen=d.get('sheen', 0.0), bump=d.get('bump', 0.0),
                                     bump_scale=d.get('bump_scale', 500), coat=d.get('coat', 0.0),
                                     emit=d.get('emit_color'), emit_strength=d.get('emit', 0.0))
        self.M = M

    # ------------------------------------------------------------- body
    def skeleton(self):
        s, b = self.s, self.b
        J, E, R, idx = [], [], [], {}

        def j(n, co, r, parent=None):
            idx[n] = len(J)
            J.append(Vector(co) * s)
            R.append((r[0] * s, r[1] * s))
            if parent is not None:
                E.append((idx[parent], idx[n]))

        ch, wa, hp, lb, sh = b['chest'], b['waist'], b['hip'], b['limb'], b['shoulder']
        bel = b['belly']
        j('pelvis', (0, .012, .97), (.155 * hp, .105 * hp))
        j('waist', (0, .006 - bel * .02, 1.09), (.130 * wa + bel * .02, .090 * wa + bel * .04), 'pelvis')
        j('spine', (0, .004 - bel * .01, 1.20), (.142 * (ch + wa) / 2, .096 * (ch + wa) / 2 + bel * .02), 'waist')
        j('chest', (0, -.006, 1.31), (.165 * ch, .108 * ch), 'spine')
        j('chest_up', (0, .002, 1.40), (.160 * sh, .096 * ch), 'chest')
        nk = b['neck']
        j('neck', (0, .016, 1.475), (.054 * nk, .056 * nk), 'chest_up')
        j('neck_top', (0, .020, 1.555), (.050 * nk, .052 * nk), 'neck')
        sx0 = .185 * sh
        for sd, sx in (('L', 1), ('R', -1)):
            j(f'shoulder_{sd}', (sx * sx0, 0, 1.425), (.062 * lb * sh, .058 * lb), 'chest_up')
            off = sx0 - .185
            j(f'uparm_{sd}', (sx * (.33 + off), 0, 1.43), (.047 * lb, .050 * lb), f'shoulder_{sd}')
            j(f'elbow_{sd}', (sx * (.47 + off), 0, 1.43), (.040 * lb, .040 * lb), f'uparm_{sd}')
            j(f'forearm_{sd}', (sx * (.58 + off), 0, 1.43), (.040 * lb, .036 * lb), f'elbow_{sd}')
            j(f'wrist_{sd}', (sx * (.72 + off), 0, 1.43), (.028 * lb, .022 * lb), f'forearm_{sd}')
            j(f'palm_{sd}', (sx * (.79 + off), 0, 1.43), (.040 * lb, .016 * lb), f'wrist_{sd}')
            for fn, fy, fl in (('index', -.026, .092), ('middle', -.008, .100), ('ring', .010, .094),
                               ('pinky', .026, .078)):
                prev = f'palm_{sd}'
                for k, t in enumerate((0, .45, .75, 1.0)):
                    n = f'{fn}{k}_{sd}'
                    r = .0088 * (1 - .22 * t) * (.85 if fn == 'pinky' else 1) * lb ** .5
                    j(n, (sx * (.825 + off + fl * t), fy, 1.43 - .004 * t), (r, r * .9), prev)
                    prev = n
            prev = f'wrist_{sd}'
            for k, (tx, ty, tz) in enumerate(((.745, -.024, 1.422), (.775, -.046, 1.420), (.800, -.062, 1.419),
                                              (.822, -.074, 1.418))):
                n = f'thumb{k}_{sd}'
                r = .0115 * (1 - .18 * k) * lb ** .5
                j(n, (sx * (tx + off), ty, tz), (r, r * .95), prev)
                prev = n
            lg = b['legs']
            j(f'hip_{sd}', (sx * .092 * hp, 0, .90), (.088 * lb * lg, .090 * lb * lg), 'pelvis')
            j(f'thigh_{sd}', (sx * .098 * hp, 0, .70), (.070 * lb * lg, .074 * lb * lg), f'hip_{sd}')
            j(f'knee_{sd}', (sx * .100 * hp, -.008, .49), (.050 * lb, .054 * lb), f'thigh_{sd}')
            j(f'calf_{sd}', (sx * .100 * hp, .006, .34), (.052 * lb, .056 * lb), f'knee_{sd}')
            j(f'ankle_{sd}', (sx * .100 * hp, .010, .085), (.032, .036), f'calf_{sd}')
            j(f'ball_{sd}', (sx * .102 * hp, -.115, .030), (.044, .026), f'ankle_{sd}')
            j(f'toe_{sd}', (sx * .104 * hp, -.185, .026), (.038, .020), f'ball_{sd}')
            j(f'heel_{sd}', (sx * .100 * hp, .040, .030), (.032, .026), f'ankle_{sd}')
        return J, E, R, idx

    def build_body(self):
        J, E, R, idx = self.skeleton()
        self.J, self.idx = J, idx
        body = ck.skin_body(self.nm('BODY'), self.C['BODY'], J, E, R, subdiv_base=1)
        s, m = self.s, self.b['muscle']
        sh = self.b['shoulder']
        bumps = [
            ((.068, -.095, 1.335), (.055, .04, .045), .010 * m, True),
            ((.205 * sh, 0, 1.435), (.045, .05, .045), .010 * m, True),
            ((.085, .03, 1.475), (.05, .04, .03), .012 * m, True),
            ((.090, .095, 1.36), (.05, .03, .07), .006 * m, True),
            ((.070, .105, .925), (.06, .04, .06), .016, True),
            ((.100, .050, .37), (.04, .03, .07), .009 * m, True),
            ((.100, -.060, .73), (.04, .03, .10), .006 * m, True),
            ((.30, 0, 1.45), (.06, .04, .03), .006 * m, True),
            ((.56, 0, 1.44), (.05, .04, .03), .004 * m, True),
            ((0, -.095, 1.17), (.07, .04, .06), -.004 + self.b['belly'] * .02, False),
            ((.035, -.06, 1.445), (.05, .03, .012), .003, True),
        ]
        bumps = [(tuple(v * s for v in c), tuple(v * s for v in sg), a * s, mi) for c, sg, a, mi in bumps]
        ck.sculpt(body, bumps)
        ck.assign(body, self.M['skin'])
        ck.store_rest_attrs(body)
        self.body = body

    # ------------------------------------------------------------- head
    def head_frame(self):
        hs, h = self.h['size'] * self.s ** 0.3, self.h
        self.hs = hs
        nt = self.J[self.idx['neck_top']]
        self.SX = .080 * hs * h['width']
        self.SY = .100 * hs * h['depth']
        self.SZT = .108 * hs * h['cranium']
        self.SZB = .124 * hs
        self.HEAD_C = Vector((0, nt.y - .014 * hs, nt.z + .087 * hs))

    def head_shape(self, p):
        """Sculpted head from a unit-sphere point. Front = -Y."""
        h = self.h
        x, y, z = p.x, p.y, p.z
        X, Y = x * self.SX, y * self.SY
        Z = z * (self.SZT if z > 0 else self.SZB)
        hs = self.hs
        jaw, chin = h['jaw'], h['chin']
        X *= ck.lerp_table(z, [(-1.0, .52 * chin), (-.82, .66 * (chin + jaw) / 2), (-.62, .86 * jaw),
                                (-.32, .93), (.0, .98), (.25, 1.0), (1.0, .93)])
        X *= 1 - .045 * G(z - .30, .15) * G(y + .2, .4)                            # temples
        if y > 0:
            Y *= 1 - .50 * max(0., -z) ** 1.15
            Y *= 1 + .07 * max(0., z) * y
        else:
            Y *= ck.lerp_table(z, [(-1., .92), (-.55, .98), (0., .99), (.35, .98), (1., .92)])
        # jaw floor: flatten the underside so a crisp jawline runs chin -> gonion
        if y > -.80 and z < -.45:
            zf = ck.lerp_table(y, [(-.80, -1.0), (-.35, -.86), (.10, -.64), (.40, -.55)]) * self.SZB
            if Z < zf:
                Z = zf + (Z - zf) * .22
        f = max(0., -y) ** 2.5
        d = 0.0
        nose = h['nose'] * hs
        nw = h['nose_w']
        # nasion dip between the eyes, then bridge -> ball tip -> sharp underside
        d -= .0030 * G(z - .10, .05) * G(x, .12) * f * h['brow']
        t = min(1., max(0., (.08 - z) / .38))
        na = (.004 + .020 * t ** 1.5) * ck.smoothstep(-.42, -.31, z) * nose
        d += na * G(x, (.055 + .07 * t) * nw) * f
        d += .0045 * nose * G(z + .29, .045) * G(x, .09 * nw) * f                  # tip ball
        for sd in (-1, 1):
            d += .0080 * nose * G(x - sd * .14 * nw, .05) * G(z + .335, .045) * f   # alae
            d -= .0030 * nose * G(x - sd * .23 * nw, .04) * G(z + .33, .06) * f    # alar crease
            d -= .0110 * G(x - sd * .40, .15) * G(z - .01, .11) * f                # eye sockets
            d -= .0040 * G(x - sd * .27, .06) * G(z + .02, .07) * f                # inner canthus depth
            X += sd * .0045 * h['cheek'] * G(x - sd * .72, .15) * G(z + .10, .13)   # zygomatic arch
            d += .0035 * h['cheek'] * G(x - sd * .55, .14) * G(z + .14, .10) * f   # cheekbone front
            d -= .0028 * G(x - sd * .58, .14) * G(z + .42, .10) * f                # sub-malar hollow
            # nasolabial fold: line from ala to mouth corner
            for k in range(5):
                u = k / 4
                d -= .0012 * G(x - sd * (.22 + .12 * u), .035) * G(z + (.36 + .16 * u), .035) * f
            # jaw angle (gonion) & masseter
            X += sd * .0050 * jaw * G(z + .62, .10) * G(y - .05, .30) * (1 if sd * x > 0 else 0)
            d += .0020 * G(x - sd * .30, .08) * G(z + .47, .05) * f                # lip corners mound
        d += .0090 * h['brow'] * G(z - .17, .060) * G(x, .52) * f                    # brow ridge
        d += .0030 * G(z - .40, .15) * G(x, .45) * f                                 # frontal bone
        d -= .0016 * G(x, .035) * G(z + .42, .05) * f                                # philtrum groove
        for sd in (-1, 1):
            d += .0010 * G(x - sd * .05, .025) * G(z + .42, .05) * f                 # philtrum ridges
        d += .0070 * G(z + .60, .20) * G(x, .38) * f                                 # maxilla/mandible forward
        d += .0080 * h['lips'] * G(z + .47, .07) * G(x, .27) * f                     # upper-lip mound
        d += .0045 * h['lips'] * G(z + .59, .055) * G(x, .23) * f                    # lower lip
        d -= .0026 * G(z + .70, .045) * G(x, .22) * f                                # mentolabial groove
        d += .0110 * chin * G(z + .84, .09) * G(x, .24 * chin) * f                   # chin
        # age: sagging jowls, deeper folds
        a = h['age']
        if a:
            for sd in (-1, 1):
                X += sd * .003 * a * G(z + .70, .10) * G(y + .3, .3)
            d -= .002 * a * G(z - .02, .05) * G(x, .6) * f
        Y -= d * hs / max(hs, 1e-6)
        return Vector((X, Y, Z))

    def build_head(self):
        self.head_frame()
        head = ck.deformed_sphere(self.nm('HEAD'), self.C['BODY'], self.head_shape, cuts=26)
        head.location = self.HEAD_C
        ck.assign(head, self.M['skin'])
        # blush / redness map (cheeks, nose, ears region, lips area)
        def blush(co, n):
            u = self.head_unit(co)
            f = max(0., -u.y) ** 2
            v = 0.0
            for sd in (-1, 1):
                v += .8 * G(u.x - sd * .52, .17) * G(u.z + .20, .14) * f
            v += .7 * G(u.x, .12) * G(u.z + .28, .10) * f
            v += .5 * G(u.z + .53, .12) * G(u.x, .30) * f
            v += .5 * max(0., abs(u.x) - .85) * 4
            return min(1., v)
        ck.float_attr(head, 'blush', blush)
        hs = self.hs
        for sd, sx in (('L', 1), ('R', -1)):
            pointed = self.h['ears'] == 'pointed'

            def ear(p, sx=sx, pointed=pointed):
                X, Y, Z = p.x * .0095, p.y * .016, p.z * .029
                # helix rim: hollow the centre (concha)
                rim = max(0., 1 - (p.y ** 2 + p.z ** 2))
                X -= .0045 * rim * (1 if p.x > 0 else .25)
                if pointed and p.z > 0:
                    Z += .028 * p.z ** 3
                    Y += .016 * p.z ** 3
                return Vector((X * sx, Y, Z)) * hs
            e = ck.deformed_sphere(self.nm(f'EAR_{sd}'), self.C['BODY'], ear, cuts=8)
            e.location = self.HEAD_C + Vector((sx * self.SX * .95, .014 * hs, -.012 * hs))
            e.rotation_euler = (math.radians(-10), 0, math.radians(sx * 18))
            ck.assign(e, self.M['skin'])
            ck.add_subsurf(e, 1, 2)
            self.objs[f'ear_{sd}'] = e
        ck.add_subsurf(head, 1, 2)
        self.head = head

    def head_unit(self, co):
        return Vector((co.x / self.SX, co.y / self.SY, co.z / (self.SZT if co.z > 0 else self.SZB)))

    # ------------------------------------------------------------- face
    def build_face(self):
        hs = self.hs
        es = self.cfg.get('eyes', {}).get('size', 1.0)
        er, ex, ez = .0128 * hs * es, .0322 * hs * self.cfg.get('eyes', {}).get('spacing', 1.0), .0035 * hs
        bvh = ck.bvh_of(self.head)
        F = {}
        for sd, sx in (('L', 1), ('R', -1)):
            ys = ck.surface_y(bvh, sx * ex, ez)
            c = self.HEAD_C + Vector((sx * ex, ys + er * .62, ez))
            eye = ck.deformed_sphere(self.nm(f'EYE_{sd}'), self.C['FACE'], lambda p: p, cuts=8)
            eye.scale = (er,) * 3
            eye.location = c
            ck.assign(eye, self.M['eye'])
            ck.add_subsurf(eye, 1, 2)
            F[f'eye_{sd}'] = eye
            for part, up in (('LID_UP', True), ('LID_LO', False)):
                lid = ck.lid_shell(self.nm(f'{part}_{sd}'), self.C['FACE'], er * 1.10, upper=up)
                lid.location = c
                ck.assign(lid, self.M['lid'])
                ck.add_subsurf(lid, 1, 1)
                F[f'{part.lower()}_{sd}'] = lid
        exprs = self.cfg['expressions']
        mouth_keys = {'neutral': {}}
        for e in exprs:
            if e in MOUTH:
                mouth_keys[e] = MOUTH[e]
        for p in PHONEMES:
            mouth_keys[p] = MOUTH[p]
        mouth_keys = {k: scale_mouth(v, hs) for k, v in mouth_keys.items()}
        mouth = ck.build_mouth(self.nm('MOUTH'), self.C['FACE'], self.head, (0., -.064 * hs), mouth_keys,
                               [self.M['mouth'], self.M['lip']], W=.022 * hs * self.cfg.get('mouth_w', 1.0))
        mouth.location = self.HEAD_C
        F['mouth'] = mouth
        brow_keys = {'neutral': {}}
        for e in exprs:
            if e in BROW:
                brow_keys[e] = {k: v * hs for k, v in BROW[e].items()}
        brows = ck.build_brows(self.nm('BROWS'), self.C['FACE'], self.head,
                               [(-.011 * hs, .0205 * hs), (.011 * hs, .0205 * hs)], brow_keys, self.M['brow'],
                               W=.026 * hs, thick=self.cfg.get('brow_thick', 1.0) * hs)
        brows.location = self.HEAD_C
        F['brows'] = brows
        self.F = F

    # ------------------------------------------------------------- hair & co
    def hairline(self, u, front=.50, side=.22, back=-.58):
        r = math.hypot(u.x, u.y) or 1e-6
        fy = -u.y / r
        return ck.lerp_table(fy, [(-1., back), (-.3, back * .35), (0., side), (.55, front * .84), (1., front)])

    def build_hair(self):
        hc = self.cfg.get('hair', {'style': 'none'})
        st = hc['style']
        out = []
        if st in ('none', 'bald'):
            self.hair = out
            return
        rnd = random.Random(hc.get('seed', 7))
        hl = hc.get('hairline', {})
        line = lambda u: self.hairline(u, **hl)
        cap = ck.trim_copy(self.head, self.nm('HAIR_CAP'), self.C['HAIR'],
                           lambda co: self.head_unit(co).z > line(self.head_unit(co)), offset=.0035 * self.hs)
        cap.modifiers.clear()
        so = cap.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = .003; so.offset = -1
        ck.add_subsurf(cap, 1, 2)
        ck.assign(cap, self.M['hair'])
        out.append(cap)
        strands = []
        HC, hs = self.HEAD_C, self.hs
        L0 = hc.get('length', 1.0)
        for p in ck.fib_sphere(hc.get('density', 300)):
            u = p
            if u.z < line(u) + .02:
                continue
            r = math.hypot(u.x, u.y) or 1e-6
            fy = -u.y / r
            root = self.head_shape(u)
            n = u.normalized()
            side = math.copysign(1, u.x)
            jit = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * .15
            mi = 0
            if st == 'spiky':
                if fy > .40 and u.z < .82:
                    d1 = (n * .25 + Vector((u.x * .6, -.2, 1))).normalized(); d2 = Vector((u.x * .5, .75, .55)).normalized(); L, W = .110, .021
                elif u.z > .55:
                    d1 = (n * .55 + Vector((0, .4, .7))).normalized(); d2 = Vector((u.x * .5, .9, .25)).normalized(); L, W = .120, .022
                elif fy > -.35:
                    d1 = (n * .3 + Vector((side * .1, .85, .3))).normalized(); d2 = Vector((side * .15, .95, .1)).normalized(); L, W = .080, .018
                else:
                    d1 = (n * .5 + Vector((0, .5, -.3))).normalized(); d2 = Vector((u.x * .4, .55, -.7)).normalized(); L, W = .080, .019
                L *= rnd.uniform(.8, 1.2) * L0
                p0 = root - n * .004; p1 = root + n * L * .12 + d1 * L * .1
                p2 = p1 + (d1 + jit).normalized() * L * .42; p3 = p2 + (d2 + jit).normalized() * L * .48
                pts = [p0, p1, p2, p3]
                mi = 1 if (hc.get('streak') and fy > .80 and .50 < u.z < .70 and .08 < u.x < .30) else 0
                th = .0065
            elif st == 'swept':      # short, swept up-and-back, flame-like tips
                up = Vector((0, .55, .80)).normalized()
                d1 = (n * .45 + up + Vector((side * .1 * abs(u.x), 0, 0))).normalized()
                d2 = Vector((u.x * .3, .95, .25 - .2 * (1 - u.z))).normalized()
                L, W = (.085 if fy > 0 else .070) * rnd.uniform(.8, 1.2) * L0, .020
                p0 = root - n * .004; p1 = root + n * L * .15
                p2 = p1 + (d1 + jit * .6).normalized() * L * .45; p3 = p2 + (d2 + jit).normalized() * L * .45
                pts, th = [p0, p1, p2, p3], .006
            elif st == 'long_back':  # slicked back, falls to the upper back
                pts = [root - n * .003]
                cur = u.normalized()
                tgt = Vector((u.x * .35, 1.0, -.75)).normalized()
                for k in range(1, 5):
                    cur = cur.lerp(tgt, .35).normalized()
                    pts.append(self.head_shape(cur) * 1.045 + n * .002 * k)
                last = pts[-1]
                drop = hc.get('drop', .20) * rnd.uniform(.8, 1.15) * L0
                pts.append(last + Vector((u.x * .01, .03, -drop * .5)))
                pts.append(last + Vector((u.x * .02, .05 + .02 * rnd.random(), -drop)))
                W, th = .020, .0045
            else:
                continue
            strands.append({'pts': [q + HC for q in pts], 'width': W * rnd.uniform(.85, 1.15) * hs,
                            'thick': th * hs, 'mat': mi, 'twist': rnd.uniform(-.5, .5)})
        hair = ck.loft_hair(self.nm('HAIR'), self.C['HAIR'], strands, HC, mats=[self.M['hair'], self.M['hair_streak']])
        ck.add_subsurf(hair, 1, 1)
        out.append(hair)
        self.hair = out

    def build_beard(self):
        bd = self.cfg.get('beard')
        if not bd:
            self.beard = []
            return
        rnd = random.Random(11)
        strands, HC, hs = [], self.HEAD_C, self.hs
        L0 = bd.get('length', .25)
        for p in ck.fib_sphere(1100):
            u = p
            if u.y > .15 or u.z > -.28:
                continue
            if u.z > -.50 and abs(u.x) > .55:      # no beard on the upper cheeks
                continue
            if abs(u.x) < .42 and -.66 < u.z < -.40:     # keep the mouth clear
                continue
            mous = -.46 < u.z < -.30 and abs(u.x) < .55 and u.y < -.5
            if not mous and u.z > -.45 and abs(u.x) < .75:
                continue
            root = self.head_shape(u)
            n = u.normalized()
            if mous:   # moustache: out and down past the mouth corners
                sd = math.copysign(1, u.x)
                pts = [root - n * .002, root + n * .004 + Vector((sd * .006, -.002, -.004)),
                       root + Vector((sd * .022, -.010, -.020)), root + Vector((sd * .030, -.012, -.045))]
                W, th = .010, .003
            else:
                L = L0 * rnd.uniform(.75, 1.15) * (1 - .4 * max(0, abs(u.x) - .4))
                fwd = -.03 - .06 * L0
                pts = [root - n * .003, root + n * .005, root + Vector((u.x * .006, fwd * .5, -L * .35)),
                       root + Vector((u.x * .004 * rnd.uniform(.5, 1.5), fwd, -L * .75)),
                       root + Vector((u.x * .002, fwd * 1.05, -L))]
                W, th = .010, .0028
            strands.append({'pts': [q + HC for q in pts], 'width': W * hs * rnd.uniform(.8, 1.2), 'thick': th * hs,
                            'mat': 0, 'twist': rnd.uniform(-.4, .4)})
        beard = ck.loft_hair(self.nm('BEARD'), self.C['HAIR'], strands, HC + Vector((0, .05, -.05)),
                             mats=[self.M['hair']])
        ck.add_subsurf(beard, 1, 1)
        self.beard = [beard]

    def build_horns(self):
        hn = self.cfg.get('horns') or []
        out = []
        for i, h in enumerate(hn):
            for sd in ((1, -1) if h.get('mirror', True) else (1,)):
                u = Vector((h['root'][0] * sd, h['root'][1], h['root'][2])).normalized()
                root = self.head_shape(u) + self.HEAD_C
                pts = [root - u * .01]
                cur = root
                for k, dv in enumerate(h['path']):
                    cur = cur + Vector((dv[0] * sd, dv[1], dv[2])) * self.hs
                    pts.append(cur)
                strand = {'pts': pts, 'width': h['radius'] * self.hs, 'thick': h['radius'] * self.hs * .95, 'mat': 0}
                o = ck.loft_hair(self.nm(f'HORN_{i}_{"L" if sd > 0 else "R"}'), self.C['ACCESSORIES'], [strand],
                                 root + Vector((0, 0, -1)), samples=16, ring=12,
                                 mats=[self.M[h.get('mat', 'horn')]])
                ck.add_subsurf(o, 1, 2)
                out.append(o)
        self.horns = out

    # ------------------------------------------------------------- costume
    def norm(self, co):
        return co / self.s

    def build_costume(self):
        out = {}
        for piece in self.cfg.get('costume', []):
            k = piece['kind']
            fn = getattr(self, f'pc_{k}')
            res = fn(piece, out)
            if res is None:
                continue
            for o in (res if isinstance(res, list) else [res]):
                out[o.name] = o
        self.cloth = out

    def _acc(self, ob, rule):
        if rule:
            ck.float_attr(ob, 'accent', lambda c, n: 1.0 if rule(c / self.s, n) else 0.0)

    def pc_trim(self, p, out):
        coll = self.C[p.get('coll', 'CLOTHING')]
        keep = p['keep']
        mirror = p.get('mirror', False)
        res = []
        for sd, sx in ((('L', 1), ('R', -1)) if mirror else ((None, 1),)):
            nm = self.nm(p['name'] + (f'_{sd}' if sd else ''))
            kf = (lambda c, sx=sx: keep(Vector((c.x * sx, c.y, c.z)) / self.s)) if mirror else (lambda c: keep(c / self.s))
            ofs = p.get('offset', .004) * self.s
            o = ck.trim_copy(self.body, nm, coll, kf, offset=ofs, solid=p.get('solid', .003) * self.s,
                             offset_fn=p.get('offset_fn') and (lambda c, f=p['offset_fn'], sx=sx: f(Vector((c.x * sx, c.y, c.z)) / self.s) * self.s))
            if len(o.data.polygons) == 0:
                raise RuntimeError(f'costume piece {nm} is empty — region too narrow')
            # the copied mesh carries the body's deform weights by index: give it matching groups
            for vg in self.body.vertex_groups:
                o.vertex_groups.new(name=vg.name)
            if p.get('accent'):
                r = p['accent']
                self._acc(o, (lambda c, n, r=r, sx=sx: r(Vector((c.x * sx, c.y, c.z)), Vector((n.x * sx, n.y, n.z)))) if mirror else r)
            if p.get('bevel'):
                bv = o.modifiers.new('Bevel', 'BEVEL'); bv.width = .0015; bv.segments = 2
                bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(40); bv.use_clamp_overlap = True
                o.modifiers.move(len(o.modifiers) - 1, 0)
            ck.assign(o, self.M[p['mat']])
            if p.get('rigid'):
                o['bind_bone'] = f"{p['rigid']}_{sd}" if sd else p['rigid']
            res.append(o)
        return res

    def pc_spikes(self, p, out):
        """Cone spikes grown from a costume piece's surface (rest pose)."""
        rnd = random.Random(p.get('seed', 3))
        res = []
        for tgt in p['targets']:
            src = bpy.data.objects[self.nm(tgt)]
            dg = bpy.context.evaluated_depsgraph_get()
            ev = src.evaluated_get(dg)
            me = ev.to_mesh()
            cand = [(v.co.copy(), v.normal.copy()) for v in me.vertices if p['where'](v.co / self.s, v.normal)]
            ev.to_mesh_clear()
            rnd.shuffle(cand)
            strands = []
            for co, n in cand[:p.get('count', 6)]:
                L = p['length'] * rnd.uniform(.7, 1.2) * self.s
                bias = Vector(p.get('bias', (0, 0, .4)))
                if co.x < 0:
                    bias.x = -bias.x
                d = (n + bias).normalized()
                strands.append({'pts': [co - n * .004, co + d * L * .4, co + (d + Vector((0, 0, .3))).normalized() * L],
                                'width': p['radius'] * self.s, 'thick': p['radius'] * self.s, 'mat': 0})
            o = ck.loft_hair(self.nm(f'{tgt}_SPIKES'), self.C['ACCESSORIES'], strands, Vector((0, 0, -10)),
                             samples=8, ring=8, mats=[self.M[p['mat']]])
            o['bind_to'] = tgt
            res.append(o)
        return res

    def pc_disc(self, p, out):
        """Emissive / metal disc (chest core, lenses, sigils) projected on a target surface.
        top=True projects from above (e.g. bracer cores); mirror=True makes an R copy."""
        res = []
        for sd, sx in ((('L', 1), ('R', -1)) if p.get('mirror') else ((None, 1),)):
            on = p.get('on')
            if on and p.get('mirror') and on.endswith('_L'):
                on = on[:-1] + sd
            tgt = bpy.data.objects[self.nm(on)] if on else self.body
            bvh = ck.bvh_of(tgt)
            x, z = sx * p['pos'][0] * self.s, p['pos'][1] * self.s
            if p.get('top'):
                hit = bvh.ray_cast(Vector((x, 0, z + .5)), Vector((0, 0, -1)), 1.0)
                loc, rot = (x, 0, (hit[0].z if hit[0] else z) + .001), (0, 0, 0)
            else:
                y = ck.surface_y(bvh, x, z)
                loc, rot = (x, (y if y is not None else -.12) - .001, z), (math.pi / 2, 0, 0)
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=p['radius'] * self.s,
                                                depth=p.get('depth', .006) * self.s, location=loc, rotation=rot)
            o = bpy.context.object
            nm = p['name'] if not p.get('mirror') else p['name'][:-1] + sd
            o.name = self.nm(nm)
            ck.link(o, self.C['ACCESSORIES'])
            ck.assign(o, self.M[p['mat']])
            bone = p.get('bone', 'spine_03')
            o['bind_bone'] = bone[:-1] + sd if (p.get('mirror') and bone.endswith('_L')) else bone
            res.append(o)
        return res

    def pc_emblem(self, p, out):
        tgt = bpy.data.objects[self.nm(p['on'])]
        bvh = ck.bvh_of(tgt)
        ev = []
        for (u, v) in p['poly']:
            x, z = (p['pos'][0] + u * p.get('scale', 1)) * self.s, (p['pos'][1] + v * p.get('scale', 1)) * self.s
            y = ck.surface_y(bvh, x, z)
            ev.append(Vector((x, (y or -.12) - .0015, z)))
        o = ck.mesh_object(self.nm(p['name']), ev, [tuple(range(len(ev)))], self.C['ACCESSORIES'])
        so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = .0012
        ck.assign(o, self.M[p['mat']])
        o['bind_bone'] = p.get('bone', 'spine_03')
        return o

    def pc_box(self, p, out):
        loc = [v * self.s for v in p['loc']]
        if p.get('project', True):
            y = ck.surface_y(ck.bvh_of(self.body), loc[0], loc[2])
            if y is not None:
                loc[1] = y - p['size'][1] * self.s * .5 - p.get('gap', .011) * self.s
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.object
        o.name = self.nm(p['name'])
        o.scale = tuple(v * self.s for v in p['size'])
        bv = o.modifiers.new('Bevel', 'BEVEL'); bv.width = .002; bv.segments = 2
        ck.link(o, self.C['ACCESSORIES'])
        ck.assign(o, self.M[p['mat']])
        o['bind_bone'] = p.get('bone', 'pelvis')
        return o

    def pc_skirt(self, p, out):
        """Long robe skirt / coat tails: lofted rings from the waist to the hem."""
        s = self.s
        z0, z1 = p.get('z_top', 1.02) * s, p.get('z_bottom', .03) * s
        rings, seg = 14, 48
        bvh = ck.bvh_of(self.body)
        verts, faces = [], []
        open_f = p.get('open_front', 0.0)   # radians of the front gap
        a0, a1 = -math.pi / 2 + open_f / 2, 3 * math.pi / 2 - open_f / 2
        closed = open_f <= 0
        nseg = seg if closed else seg + 1
        base_r = []
        for k in range(nseg):
            a = a0 + (a1 - a0) * k / seg
            d = Vector((math.cos(a), math.sin(a), 0))
            # hip radius from body along direction d at z0
            hit = bvh.ray_cast(Vector((0, .01 * s, z0)) + d * .5, -d, 1.0)
            r = ((hit[0] - Vector((0, .01 * s, z0))).length if hit[0] else .17 * s) + p.get('offset', .02) * s
            base_r.append((d, r))
        for i in range(rings + 1):
            t = i / rings
            z = z0 + (z1 - z0) * t
            fl = 1 + p.get('flare', .3) * t ** 1.4
            for k in range(nseg):
                d, r = base_r[k]
                back = max(0., d.y) * p.get('back_extra', 0.0) * t
                wav = .006 * s * math.sin(k * 1.7 + i * .9) * t
                verts.append(Vector((0, .01 * s, z)) + d * (r * fl + back + wav))
        for i in range(rings):
            for k in range(nseg if closed else seg):
                a = i * nseg + k
                b = i * nseg + (k + 1) % nseg
                faces.append((a, b, b + nseg, a + nseg))
        o = ck.mesh_object(self.nm(p['name']), verts, faces, self.C['CLOTHING'])
        o.data.shade_smooth()
        hem, front = p.get('hem', .06), p.get('front_band', 0.0)
        acc = o.data.attributes.new('accent', 'FLOAT', 'POINT')
        for i, v in enumerate(o.data.vertices):
            ring, k = divmod(i, nseg)
            t = ring / rings
            edge = (not closed) and (k <= 1 or k >= nseg - 2) and front > 0
            acc.data[i].value = 1.0 if (t > 1 - hem / max(.01, (z0 - z1) / s) or edge) else 0.0
        so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = p.get('solid', .004) * s
        ck.assign(o, self.M[p['mat']])
        o['weights'] = 'skirt'
        return o

    def pc_cape(self, p, out):
        """Cape / mantle / tabard: a curved sheet hanging from the shoulders (back or front)."""
        s = self.s
        rows, cols = 12, 16
        w, top, bot = p.get('width', .40) * s, p.get('z_top', 1.46) * s, p.get('z_bottom', .55) * s
        side = p.get('side', 'back')
        sg = 1 if side == 'back' else -1
        bvh = ck.bvh_of(self.body)
        verts, faces = [], []
        for i in range(rows + 1):
            t = i / rows
            z = top + (bot - top) * t
            for k in range(cols + 1):
                u = -1 + 2 * k / cols
                x = u * w * (1 + p.get('flare', .25) * t)
                hit = bvh.ray_cast(Vector((x, sg * .6 * s, z)), Vector((0, -sg, 0)), 2.0)
                yb = hit[0].y if hit[0] else sg * .12 * s
                y = yb + sg * (p.get('offset', .03) * s + .05 * s * t ** 1.5) + sg * .01 * s * (1 - u * u)
                if p.get('tattered') and i == rows:
                    z += (.04 * s) * math.sin(k * 2.3) * (1 if k % 2 else -.5)
                verts.append(Vector((x, y, z)))
        for i in range(rows):
            for k in range(cols):
                a = i * (cols + 1) + k
                faces.append((a, a + 1, a + cols + 2, a + cols + 1) if sg > 0 else (a, a + cols + 1, a + cols + 2, a + 1))
        o = ck.mesh_object(self.nm(p['name']), verts, faces, self.C['CLOTHING'])
        o.data.shade_smooth()
        acc = o.data.attributes.new('accent', 'FLOAT', 'POINT')
        for i in range(len(verts)):
            ring, k = divmod(i, cols + 1)
            acc.data[i].value = 1.0 if (ring >= rows - 1 or k == 0 or k == cols) and p.get('trim', True) else 0.0
        so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = p.get('solid', .004) * s
        ck.add_subsurf(o, 1, 2)
        ck.assign(o, self.M[p['mat']])
        o['weights'] = 'cape'
        return o

    def pc_hood(self, p, out):
        """Hood: inflated head shell with an open face, peaked at the back-top."""
        hs = self.hs

        def shape(pp):
            v = self.head_shape(pp) * p.get('scale', 1.35)
            if pp.z > .3 and pp.y > -.2:
                v += Vector((0, .02 * pp.y, .025 * (pp.z - .3))) * hs
            return v
        o = ck.deformed_sphere(self.nm(p['name']), self.C['CLOTHING'], shape, cuts=16)
        me = o.data
        bm = bmesh.new(); bm.from_mesh(me)
        kill = [f for f in bm.faces if all((v.co.y < -.02 * hs and abs(v.co.x) < .075 * hs and -.13 * hs < v.co.z < .085 * hs)
                                          or v.co.z < -.14 * hs for v in f.verts)]
        bmesh.ops.delete(bm, geom=kill, context='FACES')
        bm.to_mesh(me); bm.free()
        o.location = self.HEAD_C + Vector((0, .006 * hs, .004 * hs))
        so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = .006 * hs
        ck.add_subsurf(o, 1, 2)
        ck.assign(o, self.M[p['mat']])
        o['bind_bone'] = 'head'
        return o

    def pc_collar(self, p, out):
        """Tall flared ornamental collar around the neck."""
        s = self.s
        verts, faces = [], []
        rings, seg = 6, 40
        nt = self.J[self.idx['neck']]
        for i in range(rings + 1):
            t = i / rings
            z = (p.get('z0', 1.43) + (p.get('z1', 1.60) - p.get('z0', 1.43)) * t) * s
            r = (p.get('r0', .085) + (p.get('r1', .11) - p.get('r0', .085)) * t ** 1.5) * s
            for k in range(seg):
                a = 2 * math.pi * k / seg
                if p.get('open_front') and math.sin(a) < -.8:
                    rr = r * .92
                else:
                    rr = r
                verts.append(Vector((math.cos(a) * rr * 1.1, nt.y + math.sin(a) * rr, z - (.05 * s * max(0, -math.sin(a)) * t if p.get('dip') else 0))))
        for i in range(rings):
            for k in range(seg):
                a = i * seg + k; b = i * seg + (k + 1) % seg
                faces.append((a, b, b + seg, a + seg))
        o = ck.mesh_object(self.nm(p['name']), verts, faces, self.C['ACCESSORIES'])
        o.data.shade_smooth()
        acc = o.data.attributes.new('accent', 'FLOAT', 'POINT')
        for i in range(len(verts)):
            acc.data[i].value = 1.0 if i // seg in (0, rings) else 0.0
        so = o.modifiers.new('Solidify', 'SOLIDIFY'); so.thickness = .004 * s
        ck.add_subsurf(o, 1, 2)
        ck.assign(o, self.M[p['mat']])
        o['bind_bone'] = 'spine_03'
        return o

    def pc_tail(self, p, out):
        """Hanging ribbon (sash tail, loincloth flap): a loft strip."""
        s = self.s
        pts = [Vector(q) * s for q in p['pts']]
        o = ck.loft_hair(self.nm(p['name']), self.C['CLOTHING'],
                         [{'pts': pts, 'width': p.get('width', .05) * s, 'thick': .004 * s, 'mat': 0}],
                         Vector((0, 10, 1)) * s, samples=12, ring=8, mats=[self.M[p['mat']]], taper=False)
        o['weights'] = 'skirt'
        return o

    # ------------------------------------------------------------- rig
    def build_rig(self):
        J, idx = self.J, self.idx
        P = lambda k: tuple(J[idx[k]])
        top = (0, self.HEAD_C.y + .01, self.HEAD_C.z + self.SZT)
        B = [('root', (0, 0, 0), (0, .25 * self.s, 0), None, False, 0),
             ('pelvis', P('pelvis'), P('waist'), 'root', False, 0),
             ('spine_01', P('waist'), P('spine'), 'pelvis', True, 0),
             ('spine_02', P('spine'), P('chest'), 'spine_01', True, 0),
             ('spine_03', P('chest'), P('chest_up'), 'spine_02', True, 0),
             ('neck', P('neck'), P('neck_top'), 'spine_03', False, 0),
             ('head', P('neck_top'), top, 'neck', True, 0)]
        for sd in ('L', 'R'):
            sx = 1 if sd == 'L' else -1
            sh = J[idx[f'shoulder_{sd}']]
            B += [(f'clavicle_{sd}', (sx * .02 * self.s, 0, sh.z + .005 * self.s), P(f'shoulder_{sd}'), 'spine_03', False, 0),
                  (f'upperarm_{sd}', P(f'shoulder_{sd}'), P(f'elbow_{sd}'), f'clavicle_{sd}', True, 0),
                  (f'forearm_{sd}', P(f'elbow_{sd}'), P(f'wrist_{sd}'), f'upperarm_{sd}', True, 0),
                  (f'hand_{sd}', P(f'wrist_{sd}'), tuple(J[idx[f'index0_{sd}']] * .5 + J[idx[f'ring0_{sd}']] * .5),
                   f'forearm_{sd}', True, 0)]
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
        self.arm = ck.build_armature(self.nm('RIG'), self.C['RIG'], B)

    def bind(self):
        arm, body = self.arm, self.body
        ck.auto_weight(body, arm)
        return arm

    def bind_costume(self):
        arm, body = self.arm, self.body
        kd = KDTree(len(body.data.vertices))
        for i, v in enumerate(body.data.vertices):
            kd.insert(v.co, i)
        kd.balance()
        names = [vg.name for vg in body.vertex_groups]
        for o in list(self.cloth.values()):
            if o.get('bind_bone'):
                ck.bone_parent(o, arm, o['bind_bone'])
                continue
            if o.get('bind_to'):
                tgt = bpy.data.objects[self.nm(o['bind_to'])]
                if tgt.get('bind_bone'):
                    ck.bone_parent(o, arm, tgt['bind_bone'])
                    continue
                copy_nearest_weights(o, tgt if tgt.vertex_groups else body, names, kd if not tgt.vertex_groups else None)
                ck.bind_copy(o, arm)
                continue
            if o.get('weights') in ('skirt', 'cape') or not o.vertex_groups:
                mode = o.get('weights')
                copy_nearest_weights(o, body, names, kd, mode=mode, s=self.s)
            ck.bind_copy(o, arm)
        heads = [self.head] + list(self.F.values()) + self.hair + self.beard + self.horns + \
            [self.objs['ear_L'], self.objs['ear_R']]
        for o in heads:
            ck.bone_parent(o, arm, 'head')

    def build(self, out_path):
        ck.reset()
        self.collections()
        self.materials()
        self.build_body()
        self.build_head()
        self.build_face()
        self.build_hair()
        self.build_beard()
        self.build_horns()
        self.build_rig()
        self.bind()                       # body weights first: trimmed clothing copies inherit them
        self.build_costume()
        self.bind_costume()
        for o in [self.body] + list(self.cloth.values()):
            if o.type == 'MESH' and not any(m.type == 'SUBSURF' for m in o.modifiers):
                ck.add_subsurf(o, 1, 2)
        set_expression(self, 'neutral')
        set_pose(self.arm, 'NEUTRAL', self.s)
        meta = bpy.data.texts.new('CHARACTER_INFO')
        meta.write(f"id={self.id}\nheight={self.cfg.get('height')}\npowers={self.cfg.get('powers')}\n")
        bpy.ops.wm.save_as_mainfile(filepath=out_path)
        return self


def scale_mouth(d, hs):
    return {k: (v * hs if k.startswith(('corner', 'open', 'lip', 'v0')) else v) for k, v in d.items()}


def copy_nearest_weights(o, src, names, kd, mode=None, s=1.0):
    """Give `o` the vertex weights of the nearest src (body) vertices.
    skirt: sample at thigh height so hems follow the legs smoothly; cape: follow the spine."""
    for n in names:
        if n not in o.vertex_groups:
            o.vertex_groups.new(name=n)
    if kd is None:
        kd = KDTree(len(src.data.vertices))
        for i, v in enumerate(src.data.vertices):
            kd.insert(v.co, i)
        kd.balance()
    sv = src.data.vertices
    gname = {g.index: g.name for g in src.vertex_groups}
    for v in o.data.vertices:
        q = v.co.copy()
        if mode == 'skirt':
            q = Vector((q.x * .55, q.y * .55, max(q.z, .60 * s)))
        elif mode == 'cape':
            q = Vector((q.x * .4, q.y * .5, max(q.z, 1.05 * s)))
        acc = {}
        hits = kd.find_n(q, 4)
        tot = 0.0
        for co, i, dist in hits:
            w = 1.0 / (dist + 1e-4)
            tot += w
            for g in sv[i].groups:
                acc[gname[g.group]] = acc.get(gname[g.group], 0) + g.weight * w
        for gn, w in acc.items():
            o.vertex_groups[gn].add([v.index], w / tot, 'REPLACE')


# ======================================================================= runtime helpers
def face_of(cid):
    f = {'mouth': bpy.data.objects[f'CHAR_{cid}_MOUTH'], 'brows': bpy.data.objects[f'CHAR_{cid}_BROWS']}
    for sd in ('L', 'R'):
        for k in ('EYE', 'LID_UP', 'LID_LO'):
            f[f'{k.lower()}_{sd}'] = bpy.data.objects[f'CHAR_{cid}_{k}_{sd}']
    return f


def set_expression(ch_or_face, nm):
    F = ch_or_face.F if hasattr(ch_or_face, 'F') else ch_or_face
    e = expression(nm)
    for owner, key in ((F['mouth'], e['mouth']), (F['brows'], e['brows'])):
        names = [kb.name for kb in owner.data.shape_keys.key_blocks]
        for kb in owner.data.shape_keys.key_blocks[1:]:
            kb.value = 1.0 if kb.name == (key if key in names else 'neutral') else 0.0
    for sd in ('L', 'R'):
        u = e['lid_up'] + e.get(f'lid_up_{sd}', 0)
        F[f'lid_up_{sd}'].rotation_euler = (math.radians(u), 0, 0)
        F[f'lid_lo_{sd}'].rotation_euler = (math.radians(e['lid_lo']), 0, 0)
        gx, gz = e.get('gaze', (0, 0))
        F[f'eye_{sd}'].rotation_euler = (math.radians(gz), 0, math.radians(gx))
    return e


def set_phoneme(F, ph):
    for kb in F['mouth'].data.shape_keys.key_blocks[1:]:
        kb.value = 1.0 if kb.name == ph else 0.0


def set_pose(arm, name, s=1.0):
    ck.reset_pose(arm)
    W = lambda b, ax, d: ck.world_rot(arm, b, ax, d)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)

    def fingers(sd, sg, d):
        for fn in ('index', 'middle', 'ring', 'pinky'):
            for k in range(3):
                W(f'{fn}_{k + 1:02d}_{sd}', Y, sg * d * (1 + .3 * k))
    if name == 'A':
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'clavicle_{sd}', Y, sg * 4); W(f'upperarm_{sd}', Y, sg * 41)
    elif name == 'NEUTRAL':
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'clavicle_{sd}', Y, sg * 6); W(f'upperarm_{sd}', Y, sg * 68)
            W(f'forearm_{sd}', Z, sg * -12); fingers(sd, sg, 14); W(f'thumb_02_{sd}', Z, -sg * 8)
    elif name == 'DASH':
        W('spine_01', X, 10); W('spine_02', X, 8); W('neck', X, -6); W('head', X, -10)
        W('thigh_L', X, -55); W('shin_L', X, 60); W('foot_L', X, -10)
        W('thigh_R', X, 32); W('shin_R', X, 80); W('foot_R', X, 25)
        W('upperarm_L', Y, 72); W('upperarm_L', X, 50); W('forearm_L', Z, -75)
        W('upperarm_R', Y, -72); W('upperarm_R', X, -55); W('forearm_R', Z, 75)
        fingers('L', 1, 45); fingers('R', -1, 45)
    elif name in ('CAST_L', 'CAST_R', 'CAST_BOTH'):
        sides = {'CAST_L': ['L'], 'CAST_R': ['R'], 'CAST_BOTH': ['L', 'R']}[name]
        for cs in ('L', 'R'):
            sg = 1 if cs == 'L' else -1
            if cs in sides:
                W(f'upperarm_{cs}', Z, -sg * 62); W(f'upperarm_{cs}', Y, sg * 8)
                W(f'hand_{cs}', Y, -sg * 28); fingers(cs, sg, -4); W(f'thumb_02_{cs}', Z, -sg * 10)
            else:
                W(f'upperarm_{cs}', Y, sg * 72); W(f'forearm_{cs}', Z, -sg * 25); fingers(cs, sg, 55)
        if len(sides) == 1:
            sg = 1 if sides[0] == 'L' else -1
            W('spine_02', Z, sg * 10); W('head', Z, sg * 14)
            W(f'thigh_{sides[0]}', X, -12)
    elif name == 'POWER_UP':   # arms low & wide, fists, chest out — charging
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'upperarm_{sd}', Y, sg * 50); W(f'upperarm_{sd}', X, 12); W(f'forearm_{sd}', Z, -sg * 35)
            fingers(sd, sg, 40); W(f'thigh_{sd}', Y, sg * 6)
        W('spine_03', X, -6); W('head', X, 6)
    elif name == 'RUN':
        W('spine_01', X, 14); W('head', X, -12)
        W('thigh_L', X, -70); W('shin_L', X, 95); W('thigh_R', X, 25); W('shin_R', X, 45); W('foot_R', X, 20)
        W('upperarm_L', Y, 70); W('upperarm_L', X, 40); W('forearm_L', Z, -90)
        W('upperarm_R', Y, -70); W('upperarm_R', X, -45); W('forearm_R', Z, 90)
        fingers('L', 1, 50); fingers('R', -1, 50)
    elif name == 'JUMP':
        W('spine_01', X, -8); W('head', X, -8)
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'upperarm_{sd}', Y, sg * 10); W(f'upperarm_{sd}', X, -40)
            W(f'thigh_{sd}', X, -45); W(f'shin_{sd}', X, 70); W(f'foot_{sd}', X, 30)
            fingers(sd, sg, 20)
    elif name == 'LAND':
        W('spine_01', X, 28); W('spine_02', X, 10); W('head', X, -25)
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'thigh_{sd}', X, -85); W(f'shin_{sd}', X, 110); W(f'foot_{sd}', X, -25)
            W(f'upperarm_{sd}', Y, sg * 55); W(f'upperarm_{sd}', X, -25); W(f'forearm_{sd}', Z, -sg * 20)
            fingers(sd, sg, 30)
    elif name == 'TURN':
        W('spine_01', Z, 15); W('spine_02', Z, 15); W('neck', Z, 15); W('head', Z, 15)
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'upperarm_{sd}', Y, sg * 68); fingers(sd, sg, 14)
        W('thigh_L', X, -10)
    elif name == 'FIGHT':
        W('spine_01', Z, -20); W('spine_02', X, 8); W('head', Z, 15)
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'upperarm_{sd}', Y, sg * 60); W(f'upperarm_{sd}', X, -45); W(f'forearm_{sd}', Z, -sg * 110)
            fingers(sd, sg, 65)
        W('thigh_L', X, -25); W('shin_L', X, 25); W('thigh_R', X, 15); W('shin_R', X, 25)
    elif name == 'DEFORM_TEST':  # extreme joints for QC
        for sd, sg in (('L', 1), ('R', -1)):
            W(f'upperarm_{sd}', Y, sg * 20); W(f'forearm_{sd}', Z, -sg * 120)
            for fn in ('index', 'middle', 'ring', 'pinky'):
                for k in range(3):
                    W(f'{fn}_{k + 1:02d}_{sd}', Y, sg * 70)
            W(f'thigh_{sd}', X, -80); W(f'shin_{sd}', X, 110)
    bpy.context.view_layer.update()

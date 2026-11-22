"""t6kit — TASK 06 ecosystem / vegetation toolkit (Blender 4.5 LTS; also runs in 5.x).

  * build_tree(spec)   procedural species tree: real tube geometry (trunk flare + buttress lobes, multi-leader splits, clumps,
                       whorls, weeping, stilt / surface / aerial roots), bark UVs with constant texel density and no seams,
                       leaf / needle cards (folded, 4 atlas variants, crown-shaped custom normals), wind attributes.
  * materials          bark (Poly Haven scanned PBR + moss / lichen overlay), leaves (atlas colour+alpha / normal / roughness,
                       translucency, per-card hue jitter), procedural culm / grass / petal / moss / fungus / pod materials.
  * wind               NG_T6_WIND geometry-nodes deformer driven by ONE scene object `T6_WIND_CONTROL` (see wind_setup()).

Wind attributes written on every vegetation mesh (POINT domain, float):
  wind_trunk   0 at the ground → ~1 at the top     (whole-plant sway)
  wind_branch  0 at a branch base → grows towards twig tips, accumulated through the branch hierarchy
  wind_leaf    0 at the leaf-card pivot → 1 at the card tip (flutter)
  wind_phase   per-branch random 0..1 (children inherit + offset) → branches do not move in sync
  leaf_rand    per-card random 0..1 (colour variation)
"""
import os, sys, math, json
import numpy as np
import bpy
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__))
VEG = os.path.abspath(os.path.join(HERE, '..'))                       # 03_assets/vegetation
PH = os.path.abspath(os.path.join(VEG, '..', 'external', 'polyhaven'))
LEAVES = os.path.join(VEG, 'textures', 'leaves')
ATLAS_META = json.load(open(os.path.join(LEAVES, 'atlases.json'))) if os.path.exists(os.path.join(LEAVES, 'atlases.json')) else {}
UP = Vector((0, 0, 1))


def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


# ====================================================================== shader helpers
class NB:
    def __init__(self, nt):
        self.nt = nt; self.x = 0

    def n(self, kind, **kw):
        nd = self.nt.nodes.new(kind); self.x += 1; nd.location = (self.x * 60 % 1800, -(self.x // 30) * 300)
        for k, v in kw.items():
            if k in nd.inputs.keys() and not hasattr(nd, k):
                nd.inputs[k].default_value = v
            else:
                setattr(nd, k, v)
        return nd

    def l(self, a, b):
        self.nt.links.new(a, b)

    def inp(self, nd, name, val):
        if isinstance(val, bpy.types.NodeSocket):
            self.l(val, nd.inputs[name])
        else:
            nd.inputs[name].default_value = val

    def math(self, op, a, b=0.0, clamp=False):
        nd = self.n('ShaderNodeMath', operation=op, use_clamp=clamp)
        self.inp(nd, 0, a) if False else None
        for i, v in enumerate((a, b)):
            if isinstance(v, bpy.types.NodeSocket):
                self.l(v, nd.inputs[i])
            else:
                nd.inputs[i].default_value = v
        return nd.outputs[0]

    def mix(self, fac, a, b, blend='MIX'):
        nd = self.n('ShaderNodeMix', data_type='RGBA', blend_type=blend)
        for sock, v in ((nd.inputs[0], fac), (nd.inputs[6], a), (nd.inputs[7], b)):
            if isinstance(v, bpy.types.NodeSocket):
                self.l(v, sock)
            else:
                sock.default_value = v if not isinstance(v, (tuple, list)) or len(v) == 4 else (*v, 1)
        return nd.outputs[2]

    def ramp(self, fac, stops):
        nd = self.n('ShaderNodeValToRGB'); r = nd.color_ramp
        for i, (p, c) in enumerate(stops):
            e = r.elements[i] if i < 2 else r.elements.new(p)
            e.position = p; e.color = c
        self.l(fac, nd.inputs[0])
        return nd.outputs[0]

    def noise(self, vec, scale, detail=4.0, rough=.55):
        nd = self.n('ShaderNodeTexNoise'); nd.inputs['Scale'].default_value = scale
        nd.inputs['Detail'].default_value = detail; nd.inputs['Roughness'].default_value = rough
        if vec is not None:
            self.l(vec, nd.inputs['Vector'])
        return nd

    def attr(self, name):
        return self.n('ShaderNodeAttribute', attribute_type='GEOMETRY', attribute_name=name).outputs['Fac']


def img(path, noncolor=False):
    im = bpy.data.images.load(path, check_existing=True)
    im.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    return im


def bark_maps(tex):
    d = os.path.join(PH, 'textures', tex); out = {}
    for k in ('diff', 'rough', 'nor_gl', 'disp', 'ao'):
        p = os.path.join(d, f'{tex}_{k}_2k.jpg')
        if not os.path.exists(p):
            p = p[:-4] + '.png'
        if os.path.exists(p):
            out[k] = p
    if 'diff' not in out:
        raise FileNotFoundError(f'{tex}: run 03_assets/external/polyhaven_fetch.py')
    return out


def new_mat(name):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    return m, nt, NB(nt)


def mat_bark(name, tex, tint='#FFFFFF', moss=0.0, moss_col='#4E6B2C', lichen=0.0, rough_add=0.0, bump=.35, twist=0.0,
             bleach=0.0):
    """Scanned bark (Poly Haven CC0) on the tree's own UVs (u = around, v = along, metres / tile in the tree).
    moss: amount of moss on up-facing + lower bark (also uses the 'moss_w' attribute painted by the generator).
    bleach: pale papery bark (birch) — lerp to near-white keeping the scan's dark marks."""
    m, nt, b = new_mat(name); M = bark_maps(tex)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]
    T = {}
    for k, p in M.items():
        t = b.n('ShaderNodeTexImage', interpolation='Linear'); t.image = img(p, k != 'diff'); b.l(uv, t.inputs['Vector']); T[k] = t
    col = T['diff'].outputs['Color']
    if 'ao' in T:
        col = b.mix(.55, col, T['ao'].outputs['Color'], 'MULTIPLY')
    col = b.mix(1.0, col, hexc(tint), 'MULTIPLY')
    if bleach:
        lum = b.n('ShaderNodeRGBToBW'); b.l(col, lum.inputs[0])
        pale = b.ramp(lum.outputs[0], [(0.0, hexc('#2A2622')), (.10, hexc('#8A847A')), (.28, hexc('#E9E4DA'))])
        col = b.mix(bleach, col, pale)
    rough = T['rough'].outputs['Color'] if 'rough' in T else .85
    if rough_add:
        rough = b.math('ADD', rough, rough_add, True)
    if moss or lichen:
        geo = b.n('ShaderNodeNewGeometry')
        sep = b.n('ShaderNodeSeparateXYZ'); b.l(geo.outputs['Normal'], sep.inputs[0])
        nz = b.noise(geo.outputs['Position'], 1.6, 6, .6)
        nz2 = b.noise(geo.outputs['Position'], 7.0, 4, .6)
        up = b.math('MULTIPLY', b.math('ADD', sep.outputs['Z'], .35), 1.2, True)
        w = b.math('ADD', b.math('MULTIPLY', up, .6), b.math('MULTIPLY', b.attr('moss_w'), .8))
        w = b.math('MULTIPLY', w, b.math('ADD', nz.outputs['Fac'], -.18))
        disp_h = T['disp'].outputs['Color'] if 'disp' in T else .5
        w = b.math('MULTIPLY', w, b.math('SUBTRACT', 1.3, disp_h))              # moss collects in the bark furrows first
        fac = b.n('ShaderNodeMapRange'); b.l(w, fac.inputs['Value'])
        fac.inputs['From Min'].default_value = .55 - moss * .38; fac.inputs['From Max'].default_value = .62 - moss * .38 + .1
        mc = b.mix(nz2.outputs['Fac'], hexc(moss_col), hexc('#86983E'))
        if lichen:
            lc = b.mix(nz2.outputs['Fac'], hexc('#A9AE8E'), hexc('#C9C29A'))
            lf = b.n('ShaderNodeMapRange'); b.l(b.math('MULTIPLY', nz2.outputs['Fac'], nz.outputs['Fac']), lf.inputs['Value'])
            lf.inputs['From Min'].default_value = .36 - lichen * .1; lf.inputs['From Max'].default_value = .40 - lichen * .1
            col = b.mix(lf.outputs['Result'], col, lc)
        col = b.mix(fac.outputs['Result'], col, mc)
        rough = b.mix(fac.outputs['Result'], rough, (.95, .95, .95, 1))
    b.l(col, bsdf.inputs['Base Color'])
    if isinstance(rough, bpy.types.NodeSocket):
        b.l(rough, bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = rough
    nm = b.n('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 1.0
    b.l(T['nor_gl'].outputs['Color'], nm.inputs['Color'])
    if 'disp' in T:
        bp = b.n('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = .02
        b.l(T['disp'].outputs['Color'], bp.inputs['Height']); b.l(nm.outputs['Normal'], bp.inputs['Normal'])
        b.l(bp.outputs['Normal'], bsdf.inputs['Normal'])
    else:
        b.l(nm.outputs['Normal'], bsdf.inputs['Normal'])
    b.l(bsdf.outputs[0], out.inputs['Surface'])
    m['t6_bark'] = tex
    m.diffuse_color = hexc(tint)
    return m


def mat_leaf(name, atlas, hue_var=.04, val_var=.12, transl=.35, tint='#FFFFFF', backlit='#FFFFFF', emission=None):
    """leaf / needle cards: atlas colour (alpha cut-out) + normal + roughness; translucency; per-card colour jitter."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]
    tc = b.n('ShaderNodeTexImage', interpolation='Linear'); tc.image = img(os.path.join(LEAVES, f'{atlas}_col.png'))
    tc.image.alpha_mode = 'STRAIGHT'
    tn = b.n('ShaderNodeTexImage', interpolation='Linear'); tn.image = img(os.path.join(LEAVES, f'{atlas}_nor.png'), True)
    tr = b.n('ShaderNodeTexImage', interpolation='Linear'); tr.image = img(os.path.join(LEAVES, f'{atlas}_rough.png'), True)
    for t in (tc, tn, tr):
        b.l(uv, t.inputs['Vector'])
    rnd = b.attr('leaf_rand')
    hsv = b.n('ShaderNodeHueSaturation')
    b.l(b.math('MULTIPLY', b.math('SUBTRACT', rnd, .5), hue_var * 2), hsv.inputs['Hue']) if False else None
    hue = b.math('ADD', b.math('MULTIPLY', b.math('SUBTRACT', rnd, .5), hue_var * 2), .5)
    b.l(hue, hsv.inputs['Hue'])
    val = b.math('ADD', b.math('MULTIPLY', b.math('SUBTRACT', rnd, .5), val_var * 2), 1.0)
    b.l(val, hsv.inputs['Value'])
    b.l(b.mix(1.0, tc.outputs['Color'], hexc(tint), 'MULTIPLY'), hsv.inputs['Color'])
    col = hsv.outputs['Color']
    b.l(col, bsdf.inputs['Base Color'])
    b.l(tc.outputs['Alpha'], bsdf.inputs['Alpha'])
    b.l(tr.outputs['Color'], bsdf.inputs['Roughness'])
    nm = b.n('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = .8
    b.l(tn.outputs['Color'], nm.inputs['Color']); b.l(nm.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Specular IOR Level'].default_value = .45
    # translucency: Principled + Translucent mixed (works in Cycles and EEVEE)
    tl = b.n('ShaderNodeBsdfTranslucent')
    b.l(b.mix(1.0, col, hexc(backlit), 'MULTIPLY'), tl.inputs['Color']); b.l(nm.outputs['Normal'], tl.inputs['Normal'])
    mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl
    b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2])
    tr_ = b.n('ShaderNodeBsdfTransparent')
    mx2 = b.n('ShaderNodeMixShader'); b.l(tc.outputs['Alpha'], mx2.inputs[0]); b.l(tr_.outputs[0], mx2.inputs[1]); b.l(mx.outputs[0], mx2.inputs[2])
    b.l(mx2.outputs[0], out.inputs['Surface'])
    try:
        m.surface_render_method = 'DITHERED'
    except Exception:
        m.blend_method = 'HASHED'
    m['t6_atlas'] = atlas
    return realism(m, 'leaf')


def mat_simple(name, base, rough=.5, sss=0.0, var_col=None, var_scale=6.0, emission=None, em_strength=0.0, transl=0.0,
               spec=.5, attr_grad=None, grad_cols=None, sheen=0.0, coat=0.0):
    """procedural material: base colour + noise variation (var_col), optional gradient along an attribute (e.g. 'grad'
    0 root → 1 tip for grass), emission (fantasy proposals), translucency."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    col = hexc(base)
    if attr_grad and grad_cols:
        col = b.ramp(b.attr(attr_grad), [(p, hexc(c)) for p, c in grad_cols])
    if var_col:
        geo = b.n('ShaderNodeNewGeometry'); nz = b.noise(geo.outputs['Position'], var_scale, 3, .5)
        col = b.mix(b.math('MULTIPLY', nz.outputs['Fac'], 1.0), col, hexc(var_col))
        rnd = b.attr('leaf_rand')
        col = b.mix(b.math('MULTIPLY', rnd, .6), col, hexc(var_col))
    if isinstance(col, bpy.types.NodeSocket):
        b.l(col, bsdf.inputs['Base Color'])
    else:
        bsdf.inputs['Base Color'].default_value = col
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Specular IOR Level'].default_value = spec
    if sss:
        bsdf.inputs['Subsurface Weight'].default_value = sss; bsdf.inputs['Subsurface Radius'].default_value = (.1, .1, .05)
    if sheen:
        bsdf.inputs['Sheen Weight'].default_value = sheen
    if coat:
        bsdf.inputs['Coat Weight'].default_value = coat
    if emission:
        bsdf.inputs['Emission Color'].default_value = hexc(emission); bsdf.inputs['Emission Strength'].default_value = em_strength
    shader = bsdf.outputs[0]
    if transl:
        tl = b.n('ShaderNodeBsdfTranslucent')
        if isinstance(col, bpy.types.NodeSocket):
            b.l(col, tl.inputs['Color'])
        else:
            tl.inputs['Color'].default_value = col
        mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl
        b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2]); shader = mx.outputs[0]
    b.l(shader, out.inputs['Surface'])
    m.diffuse_color = hexc(base)
    return realism(m, 'blade' if attr_grad else ('gloss' if rough < .25 else ('fungus' if var_scale >= 30 else 'surface')))


def mat_moss(name, c1='#3F5E22', c2='#7E9A3A', dry='#8A8A55'):
    """moss cushion / carpet: fine noise bump + 3-tone colour, very rough, a little subsurface."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    geo = b.n('ShaderNodeNewGeometry')
    n1 = b.noise(geo.outputs['Position'], 9, 6, .65); n2 = b.noise(geo.outputs['Position'], 60, 3, .5)
    col = b.mix(n1.outputs['Fac'], hexc(c1), hexc(c2)); col = b.mix(b.math('MULTIPLY', n2.outputs['Fac'], .45), col, hexc(dry))
    b.l(col, bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = .95; bsdf.inputs['Subsurface Weight'].default_value = .15
    bsdf.inputs['Subsurface Radius'].default_value = (.05, .08, .02); bsdf.inputs['Sheen Weight'].default_value = .1
    vn = b.n('ShaderNodeTexVoronoi'); vn.inputs['Scale'].default_value = 140; b.l(geo.outputs['Position'], vn.inputs['Vector'])
    bp = b.n('ShaderNodeBump'); bp.inputs['Strength'].default_value = .7; bp.inputs['Distance'].default_value = .004
    b.l(vn.outputs['Distance'], bp.inputs['Height']); b.l(bp.outputs['Normal'], bsdf.inputs['Normal'])
    b.l(bsdf.outputs[0], out.inputs['Surface'])
    m.diffuse_color = hexc(c1)
    return m


# ====================================================================== geometry accumulator
class Geo:
    """numpy-friendly mesh accumulator: verts, faces (any n-gon), per-corner UVs, material index, POINT attributes."""
    ATTRS = ('wind_trunk', 'wind_branch', 'wind_leaf', 'wind_phase', 'leaf_rand', 'moss_w', 'grad')

    def __init__(self):
        self.V = []; self.F = []; self.UV = []; self.MI = []; self.A = {k: [] for k in self.ATTRS}; self.NRM = []   # NRM per corner (None = auto)
        self.nv = 0

    def add_verts(self, pts, **attrs):
        i0 = self.nv
        pts = np.asarray(pts, np.float64).reshape(-1, 3); n = len(pts)
        self.V.append(pts)
        for k in self.ATTRS:
            v = attrs.get(k, 0.0)
            self.A[k].append(np.broadcast_to(np.asarray(v, np.float64), (n,)).copy())
        self.nv += n
        return i0

    def add_face(self, idx, uvs, mi=0, nrm=None):
        self.F.append(tuple(idx)); self.UV.append(uvs); self.MI.append(mi); self.NRM.append(nrm)

    def to_mesh(self, name, mats):
        V = np.concatenate(self.V) if self.V else np.zeros((0, 3))
        me = bpy.data.meshes.new(name)
        me.from_pydata(V.tolist(), [], self.F)
        uvl = me.uv_layers.new(name='UVMap')
        flat = [c for f in self.UV for uv in f for c in uv]
        uvl.data.foreach_set('uv', flat)
        me.polygons.foreach_set('material_index', self.MI)
        me.polygons.foreach_set('use_smooth', [True] * len(self.F))
        for k in self.ATTRS:
            a = me.attributes.new(k, 'FLOAT', 'POINT'); a.data.foreach_set('value', np.concatenate(self.A[k]).astype(np.float32))
        for mt in mats:
            me.materials.append(mt)
        if any(n is not None for n in self.NRM):
            cn = []
            for f, n in zip(self.F, self.NRM):
                if n is None:
                    cn += [(0.0, 0.0, 0.0)] * len(f)
                else:
                    cn += [tuple(x) for x in n]
            try:
                me.normals_split_custom_set(cn)
            except Exception as e:
                print('custom normals skipped', e)
        me.validate(clean_customdata=False); me.update()
        return me


# ====================================================================== branch structure
def perp(d):
    a = Vector((1, 0, 0)) if abs(d.x) < .9 else Vector((0, 1, 0))
    return d.cross(a).normalized()


def rot_about(v, axis, ang):
    return Quaternion(axis, ang) @ v


class Branch:
    def __init__(self, pts, radii, level, phase, wbase, parent=None, t_on_parent=0.0, kind='branch'):
        self.P = pts; self.R = radii; self.level = level; self.phase = phase; self.wbase = wbase
        self.parent = parent; self.tp = t_on_parent; self.kind = kind
        seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
        self.S = np.concatenate([[0], np.cumsum(seg)]); self.L = float(self.S[-1])

    def at(self, t):
        """point, tangent, radius at fraction t of the length."""
        s = t * self.L; i = int(np.searchsorted(self.S, s, side='right') - 1); i = min(max(i, 0), len(self.P) - 2)
        f = (s - self.S[i]) / max(self.S[i + 1] - self.S[i], 1e-9)
        p = self.P[i].lerp(self.P[i + 1], f); d = (self.P[i + 1] - self.P[i]).normalized()
        r = self.R[i] + (self.R[i + 1] - self.R[i]) * f
        return p, d, r


def grow(rng, origin, d, length, r0, r_tip, segs, grav=0.0, wander=0.0, twist=0.0, flex=(), kink=0.0, up_end=0.0,
         floor=None, restore=0.0):
    """a single path from origin along d: gravity (+ up / − droop) bends it, wander = random walk (radians per segment),
    restore = pull back towards the start direction (straight trunks), floor = branches never dive below this height
    (they turn up again like real limbs resting near the ground)."""
    pts = [Vector(origin)]; d = Vector(d).normalized(); ds = length / segs; d0 = d.copy()
    axis_w = perp(d)
    for i in range(segs):
        t = (i + 1) / segs
        g = grav + up_end * t * t
        d = (d + Vector((0, 0, g)) * (1.0 / segs)).normalized()
        if wander:
            axis_w = rot_about(axis_w, d, rng.normal(0, 1.0))
            d = rot_about(d, axis_w, rng.normal(0, wander)).normalized()
        if kink and rng.random() < kink:
            d = rot_about(d, perp(d), rng.normal(0, .18)).normalized()
        if restore:
            d = (d + (d0 - d) * restore).normalized()
        if floor is not None and pts[-1].z < floor + 1.5 and d.z < .15:
            k = min(1.0, (floor + 1.5 - pts[-1].z) / 1.5)
            d = Vector((d.x, d.y, d.z + (.15 - d.z) * k)).normalized()
        pts.append(pts[-1] + d * ds)
    tt = np.linspace(0, 1, segs + 1)
    radii = list(r0 * (1 - tt) ** .9 + r_tip * tt)
    return pts, radii


def shape_ratio(shape, r):
    r = min(max(r, 0.0), 1.0)
    return {'conical': .15 + .85 * (1 - r), 'spherical': .25 + .75 * math.sin(math.pi * r),
            'hemispherical': .25 + .75 * math.sin(math.pi / 2 * (1 - r) + .3), 'cylindrical': 1.0,
            'tapered': .5 + .5 * (1 - r), 'flame': (r / .7 if r < .7 else (1 - r) / .3) * .9 + .1,
            'inverse': .25 + .75 * r, 'tend_flame': .5 + .5 * (r / .7 if r < .7 else (1 - r) / .3),
            'umbrella': .25 + .75 * r ** 1.4, 'spreading': .55 + .45 * math.sin(math.pi * (.2 + .8 * r))}[shape]


# ====================================================================== the tree
def build_tree(S, seed=0, collection=None, mats=None):
    """S = species spec (see t6_species.py). Returns the object (origin = trunk foot on the ground plane z = 0)."""
    rng = np.random.default_rng(S.get('seed', 1) * 1000 + seed)
    H = S['height'] * rng.uniform(.93, 1.07)
    Tk = S['trunk']; tile = S['bark'].get('tile', 1.0)
    stems = []
    # ---------------------------------------------------------------- level 0: trunk / leaders / clump culms
    if Tk.get('clump'):
        Cl = Tk['clump']
        for k in range(Cl['n']):
            a = rng.uniform(0, 2 * np.pi); rr = Cl['radius'] * math.sqrt(rng.random())
            base = Vector((math.cos(a) * rr, math.sin(a) * rr, -.15))
            h = H * rng.uniform(Cl.get('hmin', .6), 1.0)
            lean = math.radians(Cl.get('lean', 8) + rr / max(Cl['radius'], 1e-3) * Cl.get('splay', 14)) * rng.uniform(.7, 1.2)
            d = Vector((math.cos(a) * math.sin(lean), math.sin(a) * math.sin(lean), math.cos(lean)))
            r0 = Tk['radius'] * rng.uniform(.7, 1.1)
            pts, rad = grow(rng, base, d, h, r0, r0 * Tk.get('taper', .35), Tk.get('segs', 30), grav=Tk.get('grav', 0.0),
                            wander=math.radians(Tk.get('wander', 1.5)), up_end=Tk.get('arch', 0.0), floor=.05, restore=Tk.get('restore', .04))
            stems.append(Branch(pts, rad, 0, rng.random(), 0.0, kind='trunk'))
    else:
        lean = math.radians(Tk.get('lean', 2)); la = rng.uniform(0, 2 * np.pi)
        d = Vector((math.cos(la) * math.sin(lean), math.sin(la) * math.sin(lean), math.cos(lean)))
        split = Tk.get('split')
        Lt = H * (split['h'] if split else Tk.get('length', 1.0))
        r0 = Tk['radius'] * rng.uniform(.92, 1.08)
        r_end = r0 * (Tk.get('split_r', .75) if split else Tk.get('taper', .05))
        pts, rad = grow(rng, Vector((0, 0, -Tk.get('sink', .4))), d, Lt + Tk.get('sink', .4), r0, r_end, Tk.get('segs', 40),
                        grav=Tk.get('grav', 0.0), wander=math.radians(Tk.get('wander', 3)), kink=Tk.get('kink', 0.0),
                        restore=Tk.get('restore', .12))
        trunk = Branch(pts, rad, 0, rng.random(), 0.0, kind='trunk'); stems.append(trunk)
        if split:
            top, dtop, rtop = trunk.at(1.0)
            n = split['n']; a0 = rng.uniform(0, 2 * np.pi)
            for k in range(n):
                az = a0 + 2 * np.pi * k / n + rng.normal(0, .3)
                ang = math.radians(split['angle'] * rng.uniform(.7, 1.25))
                dd = Vector((math.cos(az) * math.sin(ang), math.sin(az) * math.sin(ang), math.cos(ang)))
                Ll = (H - top.z) * rng.uniform(.85, 1.1) / max(dd.z, .5) * split.get('len', 1.0)
                rr = rtop * rng.uniform(.62, .8)
                pts, rad = grow(rng, top - dd * rtop * .5, dd, Ll, rr, rr * Tk.get('taper', .12), Tk.get('segs', 40) // 2,
                                grav=split.get('grav', 0.0), wander=math.radians(Tk.get('wander', 3) * 1.4), floor=S.get('floor', .6),
                                restore=Tk.get('restore', .12) * .5)
                stems.append(Branch(pts, rad, 0, rng.random(), 0.0, parent=trunk, t_on_parent=1.0, kind='leader'))
    branches = list(stems)
    # ---------------------------------------------------------------- branch levels
    parents = stems
    crown_base = S.get('crown_base', .3) * H
    for li, Lv in enumerate(S['levels']):
        level = li + 1; kids = []
        for par in parents:
            if level == 1:
                # trunk-borne: only above the crown base (absolute height)
                ts = [t for t in np.linspace(0, 1, 200) if par.at(t)[0].z >= crown_base]
                if not ts:
                    continue
                t0, t1 = ts[0], min(ts[-1], Lv.get('end', .98))
                frac = (t1 - t0) * par.L / max(H - crown_base, 1)
                n = Lv['count'] * frac * (1.0 if par.kind == 'trunk' else Lv.get('leader_mul', 1.0)) / (1 if len(stems) == 1 else
                                                                                                       max(1, len(stems) * .6))
            else:
                t0, t1 = Lv.get('start', .2), Lv.get('end', 1.0)
                n = Lv['count'] * (par.L / max(Lv.get('ref_len', par.L), 1e-3)) if Lv.get('per_len') else Lv['count']
            n = int(rng.poisson(max(n, 0))) if n < 6 else int(round(n * rng.uniform(.85, 1.15)))
            if n <= 0:
                continue
            whorl = Lv.get('whorl', 0)
            if whorl:
                nw = max(1, n // whorl)
                tlist = [(t0 + (t1 - t0) * (i + rng.uniform(-.25, .25)) / nw, k) for i in range(nw) for k in range(whorl)]
            else:
                tlist = [(t0 + (t1 - t0) * (i + rng.uniform(.1, .9)) / n, 0) for i in range(n)]
            az = rng.uniform(0, 2 * np.pi)
            for i, (t, k) in enumerate(tlist):
                t = min(max(t, 0), 1)
                p, d, r_par = par.at(t)
                if whorl:
                    azi = az + 2 * np.pi * k / whorl + i // whorl * 1.1 + rng.normal(0, .25)
                else:
                    az += math.radians(Lv.get('rot', 137.5) + rng.normal(0, Lv.get('rot_var', 25))); azi = az
                ref = perp(d)
                ref = (ref - d * ref.dot(d)).normalized()
                radial = rot_about(ref, d, azi)
                if level == 1 and Lv.get('flatten'):
                    radial = Vector((radial.x, radial.y, radial.z * (1 - Lv['flatten']))).normalized()
                down = math.radians(Lv['down'] + rng.normal(0, Lv.get('down_var', 8)))
                if Lv.get('down_end') is not None:
                    down = math.radians(Lv['down'] + (Lv['down_end'] - Lv['down']) * t + rng.normal(0, Lv.get('down_var', 8)))
                dc = (d * math.cos(down) + radial * math.sin(down)).normalized()
                if level == 1:
                    rel = (p.z - crown_base) / max(H - crown_base, 1)
                    Lc = H * Lv['len'] * shape_ratio(S.get('shape', 'spherical'), rel)
                else:
                    Lc = par.L * Lv['len'] * (1 - Lv.get('len_taper', .5) * t)
                Lc *= rng.uniform(1 - Lv.get('len_var', .15), 1 + Lv.get('len_var', .15))
                if Lc < .05:
                    continue
                rc = min(r_par * .9, max(Lv.get('rmin', .004), r_par * Lv.get('ratio', .5) * (Lc / max(par.L, 1e-3)) ** Lv.get('rpow', .4)))
                if Lv.get('rabs'):
                    rc = min(r_par * .85, Lv['rabs'] * rng.uniform(.8, 1.2))
                pts, rad = grow(rng, p, dc, Lc, rc, max(rc * Lv.get('taper', .2), .002), Lv.get('segs', 8),
                                grav=Lv.get('grav', 0.0), wander=math.radians(Lv.get('wander', 6)), kink=Lv.get('kink', 0.0),
                                up_end=Lv.get('up_end', 0.0), floor=S.get('floor', .6) if level <= 2 else None)
                wb = par.wbase + par_w(par, t, S)
                kids.append(Branch(pts, rad, level, (par.phase + rng.uniform(.1, .5)) % 1, wb, parent=par, t_on_parent=t))
        branches += kids; parents = kids
    # ---------------------------------------------------------------- roots (surface / buttress / stilt) + aerial roots
    roots = []
    Rt = S.get('roots')
    if Rt:
        base_r = stems[0].R[0]
        for k in range(Rt['n']):
            a = 2 * np.pi * k / Rt['n'] + rng.normal(0, .25)
            radial = Vector((math.cos(a), math.sin(a), 0))
            z0 = Rt.get('z0', .25) * base_r * (1 if not Rt.get('stilt') else 1) + (Rt.get('stilt_h', 0) * rng.uniform(.7, 1.1) if Rt.get('stilt') else 0)
            p0 = Vector((0, 0, z0)) + radial * base_r * Rt.get('start_r', .5)
            dn = math.radians(Rt.get('down', 75) + rng.normal(0, 6))
            d = (radial * math.sin(dn) - UP * math.cos(dn)).normalized()
            L = Rt['len'] * rng.uniform(.7, 1.25)
            pts, rad = grow(rng, p0, d, L, base_r * Rt.get('ratio', .35), base_r * .04, Rt.get('segs', 10), grav=Rt.get('grav', -.4),
                            wander=math.radians(Rt.get('wander', 10)))
            # keep surface roots hugging the ground: clamp to a shallow arc that dives below z=0 at the end
            if not Rt.get('stilt'):
                for i, q in enumerate(pts):
                    t = i / (len(pts) - 1)
                    q.z = z0 * (1 - t) ** 1.6 + rad[i] * .25 - Rt.get('sink', .15) * t ** 2      # hug the ground, end buried
            roots.append(Branch(pts, rad, 0, rng.random(), 0.0, kind='root'))
    Ar = S.get('aerial')
    if Ar:
        cands = [b for b in branches if b.level == 1]
        for k in range(Ar['n'] if cands else 0):
            b = cands[rng.integers(len(cands))]; t = rng.uniform(.15, .6); p, d, r = b.at(t)
            L = p.z + .3
            pts, rad = grow(rng, p, Vector((0, 0, -1)), L, Ar.get('r', .03) * rng.uniform(.6, 1.4), Ar.get('r', .03) * .7, max(6, int(L / .6)),
                            wander=math.radians(2.5))
            roots.append(Branch(pts, rad, 3, b.phase, b.wbase + .3, kind='aerial'))
    # ---------------------------------------------------------------- mesh
    G = Geo()
    sides_l = S.get('sides', [20, 10, 6, 4, 3])
    for b in branches + roots:
        lv = b.level if b.kind != 'aerial' else 3
        k = sides_l[min(lv, len(sides_l) - 1)] if b.kind != 'root' else max(8, sides_l[0] // 2)
        if b.kind == 'trunk' and Tk.get('clump'):
            k = sides_l[0]
        tube(G, b, k, tile, S, H, rng)
    nb = len(branches) + len(roots)
    # ---------------------------------------------------------------- leaves
    Lf = S.get('leaves'); ncards = 0
    crown_c = Vector((0, 0, crown_base + (H - crown_base) * .55))
    if Lf:
        meta = ATLAS_META.get(Lf['atlas'], {'size_m': .5, 'layout': 'alternate'})
        size = meta['size_m'] * Lf.get('scale', 1.0)
        lv_set = set(len(S['levels']) + l if l < 0 else l for l in Lf.get('levels', [-1]))
        for b in branches:
            if b.level not in lv_set:
                continue
            n = max(1, int(round(b.L * Lf['per_m'] * rng.uniform(.8, 1.2))))
            for i in range(n):
                t = Lf.get('start', .25) + (1 - Lf.get('start', .25)) * (i + rng.uniform(0, 1)) / n
                if Lf.get('tip') and i == n - 1:
                    t = 1.0
                ncards += card(G, b, min(t, 1), size * rng.uniform(.8, 1.15), Lf, rng, crown_c, S, H, meta)
    Mo = S.get('beards')           # hanging moss / lichen strands (card chains)
    if Mo:
        meta = ATLAS_META.get(Mo['atlas'], {'size_m': .6})
        cands = [b for b in branches if b.level in (1, 2)]
        for k in range(Mo['n']):
            b = cands[rng.integers(len(cands))]; p, d, r = b.at(rng.uniform(.2, .9))
            p = p - Vector((0, 0, r * .8))
            chain = rng.integers(Mo.get('min', 1), Mo.get('max', 3) + 1)
            for j in range(chain):
                ncards += hang_card(G, p, meta['size_m'] * Mo.get('scale', 1.0), rng, b, S, H, j)
                p = p - Vector((0, 0, meta['size_m'] * Mo.get('scale', 1.0) * .92))
    Pd = S.get('pods')             # hanging seed pods (Lantern tree proposal) → material slot 2
    if Pd:
        cands = [b for b in branches if b.level == len(S['levels'])]
        for k in range(min(Pd['n'], len(cands))):
            b = cands[rng.integers(len(cands))]; p, d, r = b.at(rng.uniform(.6, 1.0))
            pod(G, p, Pd['size'] * rng.uniform(.75, 1.25), Pd.get('stalk', .25) * rng.uniform(.6, 1.4), b, S, H, rng)
    Fu = S.get('fungi')            # bracket fungi on the trunk (dead tree / old trees) → slot 2
    if Fu:
        for k in range(Fu['n']):
            t = rng.uniform(.05, .45); p, d, r = stems[0].at(t)
            a = rng.uniform(0, 2 * np.pi); radial = Vector((math.cos(a), math.sin(a), 0))
            bracket(G, p + radial * r * .92, radial, Fu['size'] * rng.uniform(.6, 1.3), rng)
    # height normalisation: keep the finished plant within ±10 % of its (seed-varied) design height
    top = max(float(v[:, 2].max()) for v in G.V)
    f = 1.0
    if top > H * 1.10 or top < H * .90:
        f = H / top
        G.V = [v * f for v in G.V]
    mats = mats or []
    me = G.to_mesh(S['name'], mats)
    o = bpy.data.objects.new(S['name'], me)
    if collection is not None:
        collection.objects.link(o)
    bb = np.array([v.co[:] for v in me.vertices])
    stats = dict(height_m=round(float(bb[:, 2].max()), 2), canopy_x_m=round(float(np.ptp(bb[:, 0])), 2),
                 canopy_y_m=round(float(np.ptp(bb[:, 1])), 2), trunk_d_m=round(2 * stems[0].R[0] * (1 + Tk.get('flare', 0)) * f, 2) if not Tk.get('clump')
                 else round(2 * Tk['clump']['radius'], 2), branches=nb, leaf_cards=ncards, tris=sum(len(p.vertices) - 2 for p in me.polygons),
                 verts=len(me.vertices), lowest_z=round(float(bb[:, 2].min()), 2), height_scale=round(f, 3))
    for k, v in stats.items():
        o[f't6_{k}'] = v
    return o, stats


def par_w(par, t, S):
    """wind weight accumulated along a parent branch up to t (more flexible further out & on thinner levels)."""
    flex = S.get('flex', [0.0, .35, .6, .9, 1.0])
    return flex[min(par.level, len(flex) - 1)] * t ** 1.2


def tube(G, b, k, tile, S, H, rng):
    Tk = S['trunk']; P = b.P; R = b.R; n = len(P)
    # parallel-transport frames
    T = [(P[min(i + 1, n - 1)] - P[max(i - 1, 0)]).normalized() for i in range(n)]
    N0 = perp(T[0]); frames = [N0]
    for i in range(1, n):
        v = frames[-1] - T[i] * frames[-1].dot(T[i])
        frames.append(v.normalized() if v.length > 1e-6 else perp(T[i]))
    flare = Tk.get('flare', 0) if b.kind == 'trunk' else 0
    lobes = Tk.get('lobes', 0) if b.kind == 'trunk' else 0
    lobe_amp = Tk.get('lobe_amp', 0); fh = Tk.get('flare_h', .06) * H
    twist = Tk.get('twist', 0.0) if b.kind in ('trunk', 'leader') else 0.0
    nodes = Tk.get('nodes', 0) if b.kind == 'trunk' else 0
    phase_l = rng.uniform(0, 2 * np.pi)
    circ = 2 * math.pi * R[0] * (1 + flare)
    urep = max(1, int(round(circ / tile)))
    flex = S.get('flex', [0.0, .35, .6, .9, 1.0])
    ring_idx = []
    for i in range(n):
        p, t_, nv = P[i], T[i], frames[i]
        bv = t_.cross(nv)
        z = p.z
        rf = R[i] * (1 + flare * math.exp(-max(z, 0) / max(fh, 1e-3)))
        if nodes:
            s = b.S[i] % nodes; rf *= 1 + .07 * math.exp(-(min(s, nodes - s) / .04) ** 2)
        tw = twist * (b.S[i] / max(H, 1))
        pts = []; ang = np.linspace(0, 2 * np.pi, k, endpoint=False) + tw
        lob = np.zeros(k)
        if lobes:
            lob = lobe_amp * np.maximum(0, np.cos(lobes * ang + phase_l)) ** 2.5 * math.exp(-max(z, 0) / max(fh * 1.6, 1e-3))
        bumps = 1 + .035 * np.sin(ang * 3 + i * .7) * (b.kind == 'trunk')
        for j in range(k):
            dirv = nv * math.cos(ang[j]) + bv * math.sin(ang[j])
            pts.append(p + dirv * rf * (1 + lob[j]) * bumps[j])
        tpos = b.S[i] / max(b.L, 1e-6)
        if b.kind in ('trunk', 'leader', 'root'):
            wt = max(z, 0) / H
            wb = 0.0 if b.kind != 'leader' else 0.0
        else:
            wt = max(b.P[0].z, 0) / H
            wb = b.wbase + flex[min(b.level, len(flex) - 1)] * tpos ** 1.2
        if b.kind == 'aerial':
            wb = b.wbase * (1 - tpos) ** 2; wt = wt * (1 - tpos)
        if b.kind == 'root':
            wt = 0.0
        moss = max(0.0, 1 - max(z, 0) / (.12 * H)) if b.kind in ('trunk', 'root') else (.3 if b.level == 1 else 0.0)
        i0 = G.add_verts(pts, wind_trunk=min(wt, 1.2) ** 1.5, wind_branch=wb, wind_phase=b.phase, moss_w=moss)
        ring_idx.append(i0)
    vrep = tile
    for i in range(n - 1):
        a0, a1 = ring_idx[i], ring_idx[i + 1]
        v0 = b.S[i] / vrep; v1 = b.S[i + 1] / vrep
        for j in range(k):
            j1 = (j + 1) % k
            u0 = j / k * urep; u1 = (j + 1) / k * urep
            G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((u0, v0), (u1, v0), (u1, v1), (u0, v1)), 0)
    # cap the open trunk foot / branch tips are near-zero radius → no caps needed


def tile_uv(var):
    u0 = .5 * (var % 2); v0 = .5 if var < 2 else 0.0
    return u0, v0


def card(G, b, t, size, Lf, rng, crown_c, S, H, meta):
    """one folded leaf / needle card attached at branch point t. Returns 1."""
    p, d, r = b.at(t)
    az = rng.uniform(0, 2 * np.pi)
    ref = perp(d); radial = rot_about(ref, d, az)
    ang = math.radians(Lf.get('angle', 45) + rng.normal(0, 15))
    axis = (d * math.cos(ang) + radial * math.sin(ang)).normalized()
    if t >= .999:
        axis = (d + radial * .2).normalized()
    g = Lf.get('droop', 0.0) + rng.normal(0, .1)
    axis = (axis + Vector((0, 0, g))).normalized()
    out = (p - crown_c); out.z *= .6
    out = out.normalized() if out.length > 1e-6 else UP
    side = axis.cross(UP * .7 + out * .5 + Vector((rng.normal(0, .4), rng.normal(0, .4), 0)))
    if side.length < 1e-4:
        side = perp(axis)
    side.normalize(); side = rot_about(side, axis, rng.normal(0, .35))
    nrm = side.cross(axis).normalized()
    if nrm.z < -.2 and Lf.get('face_up', True):
        side = -side; nrm = -nrm
    fold = Lf.get('fold', .22)
    w = size; h = size
    base = p + d * 0.0 - axis * size * .02
    hw = w / 2
    lb = base - side * hw * math.cos(fold) + nrm * hw * math.sin(fold)
    rb = base + side * hw * math.cos(fold) + nrm * hw * math.sin(fold)
    cb = base
    top = axis * h
    if Lf.get('bend'):
        top2 = axis * h * .5; tip_off = Vector((0, 0, -Lf['bend'] * h))
    var = int(rng.integers(4)); u0, v0 = tile_uv(var)
    wt = max(p.z, 0) / H
    wb = b.wbase + S.get('flex', [0, .35, .6, .9, 1])[min(b.level, 4)] * t ** 1.2
    rnd = rng.random()
    quads = []
    ids = []
    for row, (ofs, vv, lw) in enumerate(((Vector((0, 0, 0)), 0.0, 0.0), (top, 1.0, 1.0))):
        if row == 1 and Lf.get('bend'):
            ofs = top + Vector((0, 0, -Lf['bend'] * h))
        ids.append(G.add_verts([lb + ofs, cb + ofs, rb + ofs], wind_trunk=min(wt, 1.2) ** 1.5, wind_branch=wb, wind_leaf=lw,
                               wind_phase=(b.phase + rnd * .3) % 1, leaf_rand=rnd))
    a, c = ids
    cn = (nrm * .45 + out * .55).normalized()
    cn = tuple(cn)
    G.add_face((a, a + 1, c + 1, c), ((u0, v0), (u0 + .25, v0), (u0 + .25, v0 + .5), (u0, v0 + .5)), 1, (cn,) * 4)
    G.add_face((a + 1, a + 2, c + 2, c + 1), ((u0 + .25, v0), (u0 + .5, v0), (u0 + .5, v0 + .5), (u0 + .25, v0 + .5)), 1, (cn,) * 4)
    return 1


def hang_card(G, p, size, rng, b, S, H, j):
    """beard-moss / hanging strand card, pivot at the TOP, hanging straight down (+ a little random yaw)."""
    yaw = rng.uniform(0, np.pi); side = Vector((math.cos(yaw), math.sin(yaw), 0)); nrm = side.cross(Vector((0, 0, -1)))
    hw = size / 2; var = int(rng.integers(4)); u0, v0 = tile_uv(var)
    wt = max(p.z, 0) / H; wb = b.wbase + .8 + j * .3; rnd = rng.random()
    top = G.add_verts([p - side * hw, p, p + side * hw], wind_trunk=min(wt, 1.2) ** 1.5, wind_branch=wb, wind_leaf=j * .5,
                      wind_phase=b.phase, leaf_rand=rnd)
    q = p - Vector((0, 0, size))
    bot = G.add_verts([q - side * hw + nrm * hw * .25, q, q + side * hw - nrm * hw * .25], wind_trunk=min(wt, 1.2) ** 1.5,
                      wind_branch=wb + .3, wind_leaf=j * .5 + .5, wind_phase=b.phase, leaf_rand=rnd)
    G.add_face((bot, bot + 1, top + 1, top), ((u0, v0), (u0 + .25, v0), (u0 + .25, v0 + .5), (u0, v0 + .5)), 1)
    G.add_face((bot + 1, bot + 2, top + 2, top + 1), ((u0 + .25, v0), (u0 + .5, v0), (u0 + .5, v0 + .5), (u0 + .25, v0 + .5)), 1)
    return 1


def lathe(G, profile, base, axis, k, mi, attrs, u_scale=1.0, wobble=0.0, seed=0):
    """surface of revolution: profile = [(r, h)…] along axis from base. wobble > 0 = organic irregular outline (natural
    objects are never perfectly round): radius × (1 + wobble·(low-frequency waves + noise)), slightly tilted rims."""
    axis = axis.normalized(); nv = perp(axis); bv = axis.cross(nv)
    rings = []; rs = np.random.default_rng(seed)
    ph = rs.uniform(0, 2 * np.pi, 3); amp = rs.uniform(.4, 1.0, 3); jit = rs.normal(0, 1, (len(profile), k))
    for ri, (r, h) in enumerate(profile):
        ang = np.linspace(0, 2 * np.pi, k, endpoint=False)
        f = 1 + wobble * (amp[0] * np.sin(2 * ang + ph[0]) * .5 + amp[1] * np.sin(3 * ang + ph[1]) * .35 + amp[2] * np.sin(5 * ang + ph[2]) * .2
                          + .25 * jit[ri]) if wobble else np.ones(k)
        tilt = wobble * .6 * r * np.sin(ang + ph[0]) if wobble else np.zeros(k)
        pts = [base + axis * (h + tilt[j]) + (nv * math.cos(a) + bv * math.sin(a)) * r * f[j] for j, a in enumerate(ang)]
        rings.append(G.add_verts(pts, **attrs))
    for i in range(len(rings) - 1):
        a0, a1 = rings[i], rings[i + 1]
        for j in range(k):
            j1 = (j + 1) % k
            G.add_face((a0 + j, a0 + j1, a1 + j1, a1 + j), ((j / k * u_scale, i / len(rings)), ((j + 1) / k * u_scale, i / len(rings)),
                                                            ((j + 1) / k * u_scale, (i + 1) / len(rings)), (j / k * u_scale, (i + 1) / len(rings))), mi)


def pod(G, p, size, stalk, b, S, H, rng):
    wt = max(p.z, 0) / H; wb = b.wbase + 1.0
    attrs = dict(wind_trunk=min(wt, 1.2) ** 1.5, wind_branch=wb, wind_leaf=.6, wind_phase=b.phase, leaf_rand=rng.random())
    top = p; bot = p - Vector((0, 0, stalk))
    lathe(G, [(.006, 0), (.005, stalk)], bot, Vector((0, 0, 1)), 4, 0, attrs)
    prof = [(size * .05, 0), (size * .32, size * .12), (size * .45, size * .35), (size * .40, size * .62), (size * .22, size * .88), (size * .04, size)]
    lathe(G, [(r, -h) for r, h in prof], bot, Vector((0, 0, 1)), 10, 2, attrs)


def bracket(G, p, radial, size, rng):
    """semicircular shelf fungus on bark."""
    attrs = dict(wind_trunk=0.0, wind_branch=0.0, wind_leaf=0.0, wind_phase=0.0, leaf_rand=rng.random())
    side = radial.cross(UP).normalized(); k = 10
    rows = []
    for ri, (rr, dz) in enumerate(((0.0, 0.0), (.45, .03), (.85, .02), (1.0, -.02))):
        pts = [p + (radial * math.cos(a) + side * math.sin(a)) * size * rr * (1 if a == 0 else 1) * (.6 + .4 * abs(math.cos(a))) +
               UP * size * dz * (1 + .3 * rng.random()) for a in np.linspace(-np.pi / 2, np.pi / 2, k)]
        rows.append(G.add_verts(pts, **attrs))
    for i in range(len(rows) - 1):
        for j in range(k - 1):
            a0, a1 = rows[i], rows[i + 1]
            G.add_face((a0 + j, a0 + j + 1, a1 + j + 1, a1 + j), ((j / k, i / 4), ((j + 1) / k, i / 4), ((j + 1) / k, (i + 1) / 4), (j / k, (i + 1) / 4)), 2)
    under = [p + (radial * math.cos(a) + side * math.sin(a)) * size * .9 * (.6 + .4 * abs(math.cos(a))) - UP * size * .08
             for a in np.linspace(-np.pi / 2, np.pi / 2, k)]
    u0 = G.add_verts(under, **attrs); last = rows[-1]
    for j in range(k - 1):
        G.add_face((last + j + 1, last + j, u0 + j, u0 + j + 1), ((0, 0), (1, 0), (1, 1), (0, 1)), 2)


# ====================================================================== wind (geometry nodes)
def wind_control():
    o = bpy.data.objects.get('T6_WIND_CONTROL')
    if o is None:
        o = bpy.data.objects.new('T6_WIND_CONTROL', None); o.empty_display_type = 'SINGLE_ARROW'; o.empty_display_size = 3
        bpy.context.scene.collection.objects.link(o)
        o.rotation_euler = (math.radians(90), 0, math.radians(35))       # arrow (+Z of the empty) = wind direction
        for k, v, lo, hi, desc in (('strength', 1.0, 0, 10, 'overall wind strength (0 = calm, 1 = breeze, 3 = strong wind, 6+ = storm)'),
                                   ('gust', .5, 0, 3, 'gust amplitude (slow strength variation)'),
                                   ('speed', 1.0, 0, 5, 'animation speed multiplier'),
                                   ('flutter', 1.0, 0, 5, 'leaf / grass blade flutter')):
            o[k] = v
            ui = o.id_properties_ui(k); ui.update(min=lo, max=hi, description=desc)
    return o


class _GN:
    """tiny geometry-nodes builder (math helpers)."""
    def __init__(self, ng):
        self.ng = ng; self.nodes = ng.nodes; self.L = ng.links.new; self.k = 0
    def N(self, kind, **kw):
        nd = self.nodes.new(kind); self.k += 1; nd.location = ((self.k % 40) * 180, -(self.k // 40) * 220)
        for a, v in kw.items():
            setattr(nd, a, v)
        return nd
    def _in(self, sock, v):
        if isinstance(v, bpy.types.NodeSocket):
            self.L(v, sock)
        else:
            sock.default_value = v
    def M(self, op, a, b=None, c=None):
        nd = self.N('ShaderNodeMath', operation=op)
        for i, v in enumerate((a, b, c)):
            if v is not None:
                self._in(nd.inputs[i], v)
        return nd.outputs[0]
    def V(self, op, a, b=None, scale=None):
        nd = self.N('ShaderNodeVectorMath', operation=op)
        for i, v in enumerate((a, b)):
            if v is not None:
                self._in(nd.inputs[i], v)
        if scale is not None:
            self._in(nd.inputs['Scale'], scale)
        return nd.outputs['Value'] if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE') else nd.outputs['Vector']
    def A(self, name):
        nd = self.N('GeometryNodeInputNamedAttribute', data_type='FLOAT'); nd.inputs['Name'].default_value = name
        return nd.outputs['Attribute']
    def noise(self, vec, w, scale, dims='4D', detail=2.0):
        nd = self.N('ShaderNodeTexNoise'); nd.noise_dimensions = dims
        nd.inputs['Scale'].default_value = scale; nd.inputs['Detail'].default_value = detail
        if vec is not None and dims != '1D':
            self._in(nd.inputs['Vector'], vec)
        if w is not None and dims in ('1D', '4D'):
            self._in(nd.inputs['W'], w)
        return nd


def _wind_field(g, gi, pos_world, t):
    """shared physics of the wind field at a world position:
    wind dir W (control +Z, flattened) · speed U = 4·Strength m/s · gust fronts ADVECTED along W at ~0.8·U (4D noise of
    position and t − s/c) · dynamic pressure q = (U·G / 10 m/s)²  → returns (W, Wp crosswind, q, G, U)."""
    oi = g.N('GeometryNodeObjectInfo'); oi.transform_space = 'ORIGINAL'; g.L(gi.outputs['Wind Control'], oi.inputs['Object'])
    rot = g.N('FunctionNodeRotateVector'); rot.inputs['Vector'].default_value = (0, 0, 1); g.L(oi.outputs['Rotation'], rot.inputs['Rotation'])
    W = g.V('NORMALIZE', g.V('MULTIPLY', rot.outputs['Vector'], (1, 1, 0)))
    Wp = g.V('NORMALIZE', g.V('CROSS_PRODUCT', W, (0, 0, 1)))
    U = g.M('MULTIPLY', gi.outputs['Strength'], 4.0)
    c = g.M('MAXIMUM', g.M('MULTIPLY', U, .8), 1.0)
    s = g.V('DOT_PRODUCT', pos_world, W)
    tau = g.M('SUBTRACT', t, g.M('DIVIDE', s, c))                               # retarded time: gust fronts travel downwind
    gn = g.noise(g.V('SCALE', pos_world, scale=g.M('DIVIDE', 1.0, gi.outputs['Gust Size (m)'])), g.M('MULTIPLY', tau, .35), 1.0, '4D', 1.0)
    G = g.M('MAXIMUM', g.M('ADD', 1.0, g.M('MULTIPLY', g.M('SUBTRACT', gn.outputs['Fac'], .5), g.M('MULTIPLY', gi.outputs['Gust'], 2.4))), .05)
    UG = g.M('MULTIPLY', U, G)
    q = g.M('MULTIPLY', g.M('POWER', g.M('DIVIDE', UG, 10.0), 2.0), 1.0)      # drag ∝ v²
    return W, Wp, q, G, U, tau


def wind_group():
    """NG_T6_WIND v2 — physically-based vegetation wind (deformer). Per vertex, using the wind_* attributes:
      · drag force ∝ (wind speed × gust)²  (Strength 1 = 4 m/s breeze, 2.5 = 10 m/s, 6 = 24 m/s storm)
      · gust fronts advected downwind (trees / grass get hit one after another), 4D-noise turbulence
      · trunk: mean lean + oscillation at the plant's NATURAL FREQUENCY (≈ 4 / height Hz), response LAGS the gust (inertia),
        crosswind wobble (vortex shedding, 30 %), length-preserving arc bend (points drop as they bend: Δz = −d² / 2h)
      · branches: higher frequency (≈ 3.5 × fn), per-branch phase, local turbulence, also length-preserving
      · leaves / blades / petals: flutter ∝ √q at high frequency
      · foot fixed (wind_trunk = 0 at the ground); calm (Strength 0) = completely still."""
    name = 'NG_T6_WIND'
    old = bpy.data.node_groups.get(name)
    if old is not None and old.get('t6_wind_version') == 3:
        return old
    if old is not None:
        old.name = name + '_v1_old'
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree'); ng['t6_wind_version'] = 3
    S = lambda n, io, t, d=None, lo=None, hi=None: _sock(ng, n, io, t, d, lo, hi)
    S('Geometry', 'INPUT', 'NodeSocketGeometry'); S('Geometry', 'OUTPUT', 'NodeSocketGeometry')
    S('Wind Control', 'INPUT', 'NodeSocketObject')
    S('Strength', 'INPUT', 'NodeSocketFloat', 1.0, 0, 20); S('Gust', 'INPUT', 'NodeSocketFloat', .5, 0, 5)
    S('Speed', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10); S('Flutter', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10)
    S('Flexibility', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10)
    S('Trunk Sway (m)', 'INPUT', 'NodeSocketFloat', .15, 0, 10); S('Branch Sway (m)', 'INPUT', 'NodeSocketFloat', .12, 0, 5)
    S('Leaf Flutter (m)', 'INPUT', 'NodeSocketFloat', .03, 0, 1)
    S('Natural Freq (Hz)', 'INPUT', 'NodeSocketFloat', .3, .02, 10); S('Damping', 'INPUT', 'NodeSocketFloat', .15, 0, 1)
    S('Gust Size (m)', 'INPUT', 'NodeSocketFloat', 45.0, 1, 1000)
    S('Bend Offset (m)', 'INPUT', 'NodeSocketFloat', .5, .005, 10)       # small for grass blades (they arc strongly), ~0.5 m for trees
    g = _GN(ng); gi = g.N('NodeGroupInput'); go = g.N('NodeGroupOutput')
    selfo = g.N('GeometryNodeSelfObject'); so = g.N('GeometryNodeObjectInfo'); so.transform_space = 'ORIGINAL'
    g.L(selfo.outputs[0], so.inputs['Object'])
    P = g.N('GeometryNodeInputPosition').outputs[0]
    Pw = g.V('ADD', P, so.outputs['Location'])                                  # world position → each plant feels its own gusts
    t = g.M('MULTIPLY', g.N('GeometryNodeInputSceneTime').outputs['Seconds'], gi.outputs['Speed'])
    fn = gi.outputs['Natural Freq (Hz)']; ph = g.A('wind_phase')
    TWO_PI = 6.283185
    # trunk: gust felt with a lag (inertia) of ≈ (0.25 + damping) / fn seconds
    lag = g.M('DIVIDE', g.M('ADD', .25, gi.outputs['Damping']), fn)
    W, Wp, q, G, U, tau = _wind_field(g, gi, Pw, g.M('SUBTRACT', t, lag))
    flex = gi.outputs['Flexibility']
    turb = g.M('ADD', .25, g.M('MULTIPLY', gi.outputs['Gust'], .5))
    wt = g.A('wind_trunk')
    A_t = g.M('MULTIPLY', g.M('MULTIPLY', g.M('MULTIPLY', wt, gi.outputs['Trunk Sway (m)']), q), flex)
    osc_t = g.M('SINE', g.M('ADD', g.M('MULTIPLY', t, g.M('MULTIPLY', fn, TWO_PI)), g.M('MULTIPLY', ph, .6)))
    osc_c = g.M('SINE', g.M('ADD', g.M('MULTIPLY', t, g.M('MULTIPLY', fn, TWO_PI * 1.31)), 1.7))
    along_t = g.M('MULTIPLY', A_t, g.M('ADD', .7, g.M('MULTIPLY', osc_t, turb)))   # mean lean + resonance
    cross_t = g.M('MULTIPLY', A_t, g.M('MULTIPLY', osc_c, g.M('MULTIPLY', turb, .3)))
    D_t = g.V('ADD', g.V('SCALE', W, scale=along_t), g.V('SCALE', Wp, scale=cross_t))
    # branches: faster, per-branch phase, local turbulence (no lag — light)
    W2, Wp2, q2, G2, U2, tau2 = _wind_field(g, gi, Pw, t)
    fb = g.M('MULTIPLY', fn, 3.5)
    wb = g.A('wind_branch')
    A_b = g.M('MULTIPLY', g.M('MULTIPLY', g.M('MULTIPLY', wb, gi.outputs['Branch Sway (m)']), q2), flex)
    osc_b = g.M('SINE', g.M('ADD', g.M('MULTIPLY', t, g.M('MULTIPLY', fb, TWO_PI)), g.M('MULTIPLY', ph, TWO_PI)))
    tn = g.noise(g.V('SCALE', Pw, scale=.35), g.M('MULTIPLY', tau2, 1.3), 1.0, '4D', 2.0)
    tv = g.V('SUBTRACT', tn.outputs['Color'], (.5, .5, .5))
    D_b = g.V('ADD', g.V('SCALE', W2, scale=g.M('MULTIPLY', A_b, g.M('ADD', .55, g.M('MULTIPLY', osc_b, .45)))),
              g.V('SCALE', tv, scale=g.M('MULTIPLY', A_b, 1.2)))
    # length-preserving bend: horizontal displacement d at height h drops by d² / 2h (arc instead of shear)
    D = g.V('ADD', D_t, g.V('MULTIPLY', D_b, (1, 1, .35)))
    sep = g.N('ShaderNodeSeparateXYZ'); g.L(P, sep.inputs[0])
    h = g.M('ADD', g.M('MAXIMUM', sep.outputs['Z'], 0.0), gi.outputs['Bend Offset (m)'])
    dl = g.V('LENGTH', g.V('MULTIPLY', D, (1, 1, 0)))
    drop = g.M('MINIMUM', g.M('DIVIDE', g.M('MULTIPLY', dl, dl), g.M('MULTIPLY', h, 2.0)), g.M('MULTIPLY', g.M('MAXIMUM', sep.outputs['Z'], 0.0), .9))   # never below its base
    D = g.V('SUBTRACT', D, g.V('SCALE', (0, 0, 1), scale=drop))
    # leaf / blade flutter: ∝ sqrt(q), high frequency
    fl = g.M('MULTIPLY', g.M('MULTIPLY', g.A('wind_leaf'), gi.outputs['Leaf Flutter (m)']),
             g.M('MULTIPLY', gi.outputs['Flutter'], g.M('SQRT', q2)))
    fnz = g.noise(g.V('SCALE', Pw, scale=4.0), g.M('MULTIPLY', t, g.M('ADD', 3.0, g.M('MULTIPLY', U2, .4))), 1.0, '4D', 1.0)
    D = g.V('ADD', D, g.V('SCALE', g.V('SUBTRACT', fnz.outputs['Color'], (.5, .5, .5)), scale=g.M('MULTIPLY', fl, 2.2)))
    sp = g.N('GeometryNodeSetPosition'); g.L(gi.outputs['Geometry'], sp.inputs['Geometry']); g.L(D, sp.inputs['Offset'])
    g.L(sp.outputs[0], go.inputs['Geometry'])
    return ng


def wind_instances_group():
    """NG_T6_WIND_INSTANCES — wind for SCATTERED instances (grass fields, flowers, far trees) inside a scatter node tree:
    every instance tilts about its own base downwind by θ = atan(d / h) (same advected gust field + drag ∝ v², natural-frequency
    sway with a per-instance phase). Inputs: Instances, Wind Control, Strength, Gust, Speed, Plant Height (m), Sway (m), Natural Freq."""
    name = 'NG_T6_WIND_INSTANCES'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree'); ng.use_fake_user = True   # kept in the library for scatters
    S = lambda n, io, t, d=None, lo=None, hi=None: _sock(ng, n, io, t, d, lo, hi)
    S('Instances', 'INPUT', 'NodeSocketGeometry'); S('Instances', 'OUTPUT', 'NodeSocketGeometry')
    S('Wind Control', 'INPUT', 'NodeSocketObject')
    S('Strength', 'INPUT', 'NodeSocketFloat', 1.0, 0, 20); S('Gust', 'INPUT', 'NodeSocketFloat', .5, 0, 5)
    S('Speed', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10); S('Plant Height (m)', 'INPUT', 'NodeSocketFloat', .4, .01, 100)
    S('Sway (m)', 'INPUT', 'NodeSocketFloat', .06, 0, 10); S('Natural Freq (Hz)', 'INPUT', 'NodeSocketFloat', 1.2, .02, 10)
    S('Gust Size (m)', 'INPUT', 'NodeSocketFloat', 25.0, 1, 1000)
    g = _GN(ng); gi = g.N('NodeGroupInput'); go = g.N('NodeGroupOutput')
    selfo = g.N('GeometryNodeSelfObject'); so = g.N('GeometryNodeObjectInfo'); so.transform_space = 'ORIGINAL'
    g.L(selfo.outputs[0], so.inputs['Object'])
    P = g.V('ADD', g.N('GeometryNodeInputPosition').outputs[0], so.outputs['Location'])
    t = g.M('MULTIPLY', g.N('GeometryNodeInputSceneTime').outputs['Seconds'], gi.outputs['Speed'])
    W, Wp, q, G, U, tau = _wind_field(g, gi, P, t)
    idx = g.N('GeometryNodeInputIndex').outputs[0]
    rnd = g.N('FunctionNodeRandomValue', data_type='FLOAT'); g.L(idx, rnd.inputs['ID'])
    osc = g.M('SINE', g.M('ADD', g.M('MULTIPLY', t, g.M('MULTIPLY', gi.outputs['Natural Freq (Hz)'], 6.283)), g.M('MULTIPLY', rnd.outputs[1], 6.283)))
    d = g.M('MULTIPLY', g.M('MULTIPLY', gi.outputs['Sway (m)'], q), g.M('ADD', .75, g.M('MULTIPLY', osc, .35)))
    theta = g.M('ARCTANGENT', g.M('DIVIDE', d, gi.outputs['Plant Height (m)']))
    axis = g.V('CROSS_PRODUCT', (0, 0, 1), W)                                    # tilt the top downwind
    rq = g.N('FunctionNodeAxisAngleToRotation'); g.L(axis, rq.inputs['Axis']); g.L(theta, rq.inputs['Angle'])
    ri = g.N('GeometryNodeRotateInstances'); g.L(gi.outputs['Instances'], ri.inputs['Instances']); g.L(rq.outputs[0], ri.inputs['Rotation'])
    ri.inputs['Local Space'].default_value = False
    pos_i = g.N('GeometryNodeInputPosition').outputs[0]; g.L(pos_i, ri.inputs['Pivot Point'])
    g.L(ri.outputs[0], go.inputs['Instances'])
    return ng


def _sock(ng, name, io, typ, d=None, lo=None, hi=None):
    s = ng.interface.new_socket(name, in_out=io, socket_type=typ)
    if d is not None:
        s.default_value = d
    if lo is not None:
        s.min_value = lo
    if hi is not None:
        s.max_value = hi
    return s


def add_wind(o, trunk=.15, branch=.12, leaf=.03, flex=1.0, fn=None, damping=.15, gust_size=45.0):
    """wind modifier on a vegetation object. Strength / gust / speed / flutter are DRIVEN by T6_WIND_CONTROL's custom
    properties (single-property drivers: no Python expressions → work without 'auto-run scripts')."""
    ctrl = wind_control(); ng = wind_group()
    md = o.modifiers.new('T6_WIND', 'NODES'); md.node_group = ng
    ids = {it.name: it.identifier for it in ng.interface.items_tree if getattr(it, 'in_out', None) == 'INPUT'}
    md[ids['Wind Control']] = ctrl
    md[ids['Trunk Sway (m)']] = trunk; md[ids['Branch Sway (m)']] = branch; md[ids['Leaf Flutter (m)']] = leaf
    md[ids['Flexibility']] = flex
    if fn is None:                               # natural sway frequency ≈ 4 / height (tall trees slow, grass fast)
        H = max(float(o.get('t6_height_m', 1.0)), .05)
        fn = min(max(4.0 / H, .15), 2.5)
    md[ids['Natural Freq (Hz)']] = fn; md[ids['Damping']] = damping; md[ids['Gust Size (m)']] = gust_size
    for sock, prop in (('Strength', 'strength'), ('Gust', 'gust'), ('Speed', 'speed'), ('Flutter', 'flutter')):
        fc = o.driver_add(f'modifiers["T6_WIND"]["{ids[sock]}"]'); dr = fc.driver; dr.type = 'AVERAGE'
        v = dr.variables.new(); v.type = 'SINGLE_PROP'; v.targets[0].id_type = 'OBJECT'; v.targets[0].id = ctrl
        v.targets[0].data_path = f'["{prop}"]'
    return md


def mat_herbleaf(name, base, vein='#9AC070', rough=.45, transl=.35):
    """geometry leaf (herbs / alpine plants): UV u = across, v = along → procedural midrib + lateral veins (colour + bump),
    darker base, lighter tip, translucency."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]; sep = b.n('ShaderNodeSeparateXYZ'); b.l(uv, sep.inputs[0])
    du = b.math('ABSOLUTE', b.math('SUBTRACT', sep.outputs['X'], .5))
    mid = b.math('LESS_THAN', du, .035)
    lat = b.math('LESS_THAN', b.math('ABSOLUTE', b.math('SUBTRACT', b.math('FRACT', b.math('SUBTRACT', b.math('MULTIPLY', sep.outputs['Y'], 7.0),
                                                                                              b.math('MULTIPLY', du, 3.0))), .5)), .06)
    veins = b.math('MAXIMUM', mid, b.math('MULTIPLY', lat, .6))
    geo = b.n('ShaderNodeNewGeometry'); nz = b.noise(geo.outputs['Position'], 60, 3, .5)
    col = b.mix(b.math('MULTIPLY', sep.outputs['Y'], .5), hexc(base), tuple(min(1, c * 1.35) for c in hexc(base)[:3]) + (1,))
    col = b.mix(b.math('MULTIPLY', nz.outputs['Fac'], .25), col, (0.02, .03, .01, 1), 'MULTIPLY') if False else col
    col = b.mix(b.math('MULTIPLY', veins, .35), col, hexc(vein))      # realism: veins subtle in colour, visible in relief
    col = b.mix(b.math('MULTIPLY', b.math('SUBTRACT', nz.outputs['Fac'], .5), .3), col, (0, 0, 0, 1))
    b.l(col, bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = rough
    bp = b.n('ShaderNodeBump'); bp.inputs['Strength'].default_value = .5; bp.inputs['Distance'].default_value = .002
    b.l(b.math('SUBTRACT', 1.0, veins), bp.inputs['Height']); b.l(bp.outputs['Normal'], bsdf.inputs['Normal'])
    tl = b.n('ShaderNodeBsdfTranslucent'); b.l(col, tl.inputs['Color']); b.l(bp.outputs['Normal'], tl.inputs['Normal'])
    mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl; b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2])
    b.l(mx.outputs[0], out.inputs['Surface']); m.diffuse_color = hexc(base)
    return realism(m, 'leaf')


def mat_petal(name, base, rough=.4, transl=.35, sss=.25):
    """petal: colour ramp along the petal (grad attribute: 0 base → 1 tip), fine streaks along UV v, translucency, subsurface."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    c = hexc(base); dark = tuple(x * .55 for x in c[:3]) + (1,); light = tuple(min(1, x * 1.25 + .03) for x in c[:3]) + (1,)
    col = b.ramp(b.attr('grad'), [(0.0, dark), (.35, c), (1.0, light)])
    uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]; sep = b.n('ShaderNodeSeparateXYZ'); b.l(uv, sep.inputs[0])
    st = b.n('ShaderNodeTexWave'); st.wave_type = 'BANDS'; st.bands_direction = 'X'; st.inputs['Scale'].default_value = 6
    st.inputs['Distortion'].default_value = 2; b.l(uv, st.inputs['Vector'])
    col = b.mix(b.math('MULTIPLY', st.outputs['Fac'], .32), col, dark)
    b.l(col, bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Subsurface Weight'].default_value = sss; bsdf.inputs['Sheen Weight'].default_value = .3
    tl = b.n('ShaderNodeBsdfTranslucent'); b.l(col, tl.inputs['Color'])
    mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl; b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2])
    b.l(mx.outputs[0], out.inputs['Surface']); m.diffuse_color = c
    return realism(m, 'petal')


# ====================================================================== REALISM PASS (Director 22 Nov: "texture asli, polish jaisa nahi")
REAL = {   # roughness = r·scale + min (+ noise ± var) · spec = Specular IOR Level · mott = colour mottling · bump = micro-bump strength
    'leaf':   dict(r_scale=.45, r_min=.40, r_var=.10, spec=.22, mott=.20, blem=.30, bump=.28, bump_scale=260.0, ao=.45),
    'petal':  dict(r_scale=.40, r_min=.42, r_var=.08, spec=.25, mott=.16, blem=.0, bump=.18, bump_scale=400.0, ao=.55),
    'surface': dict(r_scale=.55, r_min=.35, r_var=.12, spec=.26, mott=.20, blem=.0, bump=.35, bump_scale=140.0, ao=.5),
    'fungus': dict(r_scale=.50, r_min=.42, r_var=.12, spec=.22, mott=.28, blem=.45, bump=.45, bump_scale=90.0, ao=.6),
    'blade':  dict(r_scale=.50, r_min=.40, r_var=.10, spec=.22, mott=.18, blem=.15, bump=.18, bump_scale=300.0, ao=.4),
    'gloss':  dict(r_scale=1.0, r_min=.08, r_var=.06, spec=.40, mott=.10, blem=.0, bump=.08, bump_scale=300.0, ao=.4),
}


def realism(m, kind='surface'):
    """Natural, non-polished look for a material built by this kit: rougher + less specular, object-space colour mottling at two
    scales, small blemishes / spots (leaves, fungi), lengthwise streaks on grass blades, per-object random tint, micro-bump
    chained after the existing normal / bump. Idempotent per material (m['t6_realism'])."""
    if m.get('t6_realism'):
        return m
    P = REAL[kind]; nt = m.node_tree; b = NB(nt)
    bs = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED']
    if not bs:
        return m
    bs = bs[0]
    def src(inp):
        if inp.is_linked:
            s = inp.links[0].from_socket; nt.links.remove(inp.links[0]); return s
        v = inp.default_value
        return tuple(v) if hasattr(v, '__len__') else float(v)
    geo = b.n('ShaderNodeNewGeometry'); pos = geo.outputs['Position']
    n1 = b.noise(pos, 7.0, 3, .5).outputs['Fac']; n2 = b.noise(pos, 38.0, 4, .6).outputs['Fac']
    # ---- roughness
    r = src(bs.inputs['Roughness'])
    if isinstance(r, float):
        r = b.n('ShaderNodeValue'); r.outputs[0].default_value = bs.inputs['Roughness'].default_value; r = r.outputs[0]
    elif isinstance(r, tuple):
        r = r[0]
    r2 = b.math('ADD', b.math('MULTIPLY', r, P['r_scale']), P['r_min'])
    r2 = b.math('ADD', r2, b.math('MULTIPLY', b.math('SUBTRACT', n2, .5), P['r_var'] * 2), True)
    b.l(r2, bs.inputs['Roughness'])
    bs.inputs['Specular IOR Level'].default_value = P['spec']
    if bs.inputs['Coat Weight'].default_value > 0:
        bs.inputs['Coat Weight'].default_value *= .35; bs.inputs['Coat Roughness'].default_value = .35
    # ---- colour: mottling (2 scales) + per-object random tint + blemishes + blade streaks
    c = src(bs.inputs['Base Color'])
    if isinstance(c, float):
        c = (c, c, c, 1)
    mott = b.math('ADD', 1.0 - P['mott'], b.math('MULTIPLY', b.math('ADD', b.math('MULTIPLY', n1, .6), b.math('MULTIPLY', n2, .4)), P['mott'] * 2))
    hsv = b.n('ShaderNodeHueSaturation'); b.l(mott, hsv.inputs['Value'])
    oi = b.n('ShaderNodeObjectInfo')
    b.l(b.math('ADD', .5, b.math('MULTIPLY', b.math('SUBTRACT', oi.outputs['Random'], .5), .03)), hsv.inputs['Hue'])
    b.l(b.math('ADD', .92, b.math('MULTIPLY', oi.outputs['Random'], .12)), hsv.inputs['Saturation'])
    if isinstance(c, bpy.types.NodeSocket):
        b.l(c, hsv.inputs['Color'])
    else:
        hsv.inputs['Color'].default_value = c
    col = hsv.outputs['Color']
    if P['blem']:
        vo = b.n('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 55.0 if kind != 'fungus' else 140.0; b.l(pos, vo.inputs['Vector'])
        sp = b.n('ShaderNodeMapRange'); b.l(vo.outputs['Distance'], sp.inputs['Value'])
        sp.inputs['From Min'].default_value = .08; sp.inputs['From Max'].default_value = .02
        blem_col = (0.16, 0.12, 0.05, 1) if kind != 'fungus' else (0.55, 0.48, 0.36, 1)
        col = b.mix(b.math('MULTIPLY', sp.outputs['Result'], P['blem']), col, blem_col)
    if kind == 'blade':
        uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]
        wv = b.n('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = 9
        wv.inputs['Distortion'].default_value = 3; b.l(uv, wv.inputs['Vector'])
        col = b.mix(b.math('MULTIPLY', wv.outputs['Fac'], .18), col, (0.02, 0.03, 0.01, 1), 'MULTIPLY') if False else \
            b.mix(b.math('MULTIPLY', wv.outputs['Fac'], .16), col, (0.0, 0.0, 0.0, 1))
        rnd = b.attr('leaf_rand')
        col = b.mix(b.math('MULTIPLY', rnd, .25), col, (0.42, 0.40, 0.18, 1))           # some blades older / yellower
    if kind == 'fungus':        # cap: fibrous radial streaks (UV u = around) + darker centre (UV v → 1 = top centre)
        uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]; sp_ = b.n('ShaderNodeSeparateXYZ'); b.l(uv, sp_.inputs[0])
        wv = b.n('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = 30
        wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 4; b.l(uv, wv.inputs['Vector'])
        col = b.mix(b.math('MULTIPLY', wv.outputs['Fac'], .3), col, (0.05, 0.03, 0.015, 1))
        col = b.mix(b.math('MULTIPLY', b.math('POWER', sp_.outputs['Y'], 2.0), .45), col, (0.04, 0.025, 0.012, 1))
    if P.get('ao'):             # dirt / shadowed albedo in crevices, folds and between leaves (Cycles AO node)
        ao = b.n('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = .04; ao.samples = 8
        b.l(col, ao.inputs['Color'])
        dirt = b.n('ShaderNodeMapRange'); b.l(ao.outputs['AO'], dirt.inputs['Value'])
        dirt.inputs['To Min'].default_value = 1 - P['ao']; dirt.inputs['To Max'].default_value = 1.0
        col = b.mix(1.0, col, b.n('ShaderNodeCombineColor').outputs[0] if False else col, 'MIX')
        mulc = b.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mulc.inputs[0].default_value = 1.0
        b.l(col, mulc.inputs[6]); cc = b.n('ShaderNodeCombineColor')
        for i in range(3):
            b.l(dirt.outputs['Result'], cc.inputs[i])
        b.l(cc.outputs[0], mulc.inputs[7]); col = mulc.outputs[2]
    b.l(col, bs.inputs['Base Color'])
    for tl in [n for n in nt.nodes if n.type == 'BSDF_TRANSLUCENT']:          # translucency follows the new colour
        if not tl.inputs['Color'].is_linked or tl.inputs['Color'].links[0].from_node.type != 'MIX':
            pass
    # ---- micro bump (after the existing normal map / bump)
    nrm = src(bs.inputs['Normal'])
    bp = b.n('ShaderNodeBump'); bp.inputs['Strength'].default_value = P['bump']; bp.inputs['Distance'].default_value = .0015
    nb = b.noise(pos, P['bump_scale'], 4, .65).outputs['Fac']; b.l(nb, bp.inputs['Height'])
    if isinstance(nrm, bpy.types.NodeSocket):
        b.l(nrm, bp.inputs['Normal'])
    b.l(bp.outputs['Normal'], bs.inputs['Normal'])
    for tl in [n for n in nt.nodes if n.type == 'BSDF_TRANSLUCENT']:
        b.l(bp.outputs['Normal'], tl.inputs['Normal'])
    m['t6_realism'] = kind
    return m


def mat_ground(name, tex, scale=2.0, tint='#FFFFFF', tex2=None, mix_scale=.08):
    """real scanned ground (Poly Haven CC0, object-space tiled): diffuse·AO, roughness, normal; optional 2nd scan blended by
    large-scale noise (breaks tiling, e.g. grass ground + soil patches)."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bs = b.n('ShaderNodeBsdfPrincipled')
    geo = b.n('ShaderNodeNewGeometry')
    def layer(t, sc):
        M = bark_maps(t); vm = b.n('ShaderNodeVectorMath', operation='SCALE'); b.l(geo.outputs['Position'], vm.inputs[0])
        vm.inputs['Scale'].default_value = 1 / sc; T = {}
        for k, p in M.items():
            n = b.n('ShaderNodeTexImage'); n.image = img(p, k != 'diff'); b.l(vm.outputs['Vector'], n.inputs['Vector']); T[k] = n
        col = T['diff'].outputs['Color']
        if 'ao' in T:
            col = b.mix(.6, col, T['ao'].outputs['Color'], 'MULTIPLY')
        return col, T['rough'].outputs['Color'], T['nor_gl'].outputs['Color']
    c, r, nrm = layer(tex, scale)
    if tex2:
        c2, r2, n2 = layer(tex2, scale * .8)
        f = b.n('ShaderNodeMapRange'); b.l(b.noise(geo.outputs['Position'], mix_scale, 4, .6).outputs['Fac'], f.inputs['Value'])
        f.inputs['From Min'].default_value = .45; f.inputs['From Max'].default_value = .62
        c = b.mix(f.outputs['Result'], c, c2); r = b.mix(f.outputs['Result'], r, r2); nrm = b.mix(f.outputs['Result'], nrm, n2)
    c = b.mix(1.0, c, hexc(tint), 'MULTIPLY')
    b.l(c, bs.inputs['Base Color']); b.l(r, bs.inputs['Roughness']); bs.inputs['Specular IOR Level'].default_value = .3
    nm = b.n('ShaderNodeNormalMap'); b.l(nrm, nm.inputs['Color']); b.l(nm.outputs['Normal'], bs.inputs['Normal'])
    b.l(bs.outputs[0], out.inputs['Surface'])
    return m

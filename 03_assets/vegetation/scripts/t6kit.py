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
    return m


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
    return m


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


def lathe(G, profile, base, axis, k, mi, attrs, u_scale=1.0):
    """surface of revolution: profile = [(r, h)…] along axis from base. Returns nothing."""
    axis = axis.normalized(); nv = perp(axis); bv = axis.cross(nv)
    rings = []
    for (r, h) in profile:
        pts = [base + axis * h + (nv * math.cos(a) + bv * math.sin(a)) * r for a in np.linspace(0, 2 * np.pi, k, endpoint=False)]
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


def wind_group():
    """NG_T6_WIND: deforms a vegetation mesh using its wind_* attributes.
    offset = W·S·g(t)·(A_t·wind_trunk·sin(ω_t t + φ) + A_b·wind_branch·sin(ω_b t + 2πφ_b) ) + flutter·wind_leaf·noise(P, t)
    W = wind direction (from T6_WIND_CONTROL's +Z axis), S = strength, g(t) = 1 + gust·noise(t)."""
    name = 'NG_T6_WIND'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    S = lambda n, io, t, d=None, lo=None, hi=None: _sock(ng, n, io, t, d, lo, hi)
    S('Geometry', 'INPUT', 'NodeSocketGeometry'); S('Geometry', 'OUTPUT', 'NodeSocketGeometry')
    S('Wind Control', 'INPUT', 'NodeSocketObject')
    S('Strength', 'INPUT', 'NodeSocketFloat', 1.0, 0, 20); S('Gust', 'INPUT', 'NodeSocketFloat', .5, 0, 5)
    S('Speed', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10); S('Flutter', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10)
    S('Flexibility', 'INPUT', 'NodeSocketFloat', 1.0, 0, 10)
    S('Trunk Sway (m)', 'INPUT', 'NodeSocketFloat', .15, 0, 10); S('Branch Sway (m)', 'INPUT', 'NodeSocketFloat', .12, 0, 5)
    S('Leaf Flutter (m)', 'INPUT', 'NodeSocketFloat', .03, 0, 1)
    nt = ng; nodes = nt.nodes; L = nt.links.new
    gi = nodes.new('NodeGroupInput'); go = nodes.new('NodeGroupOutput')
    def N(kind, **kw):
        nd = nodes.new(kind)
        for k, v in kw.items():
            setattr(nd, k, v)
        return nd
    def M(op, a, b=None, c=None):
        nd = N('ShaderNodeMath', operation=op)
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, bpy.types.NodeSocket):
                L(v, nd.inputs[i])
            else:
                nd.inputs[i].default_value = v
        return nd.outputs[0]
    def VM(op, a, b=None, scale=None):
        nd = N('ShaderNodeVectorMath', operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, bpy.types.NodeSocket):
                L(v, nd.inputs[i])
            else:
                nd.inputs[i].default_value = v
        if scale is not None:
            if isinstance(scale, bpy.types.NodeSocket):
                L(scale, nd.inputs['Scale'])
            else:
                nd.inputs['Scale'].default_value = scale
        return nd.outputs['Vector'] if op != 'DOT_PRODUCT' else nd.outputs['Value']
    def A(name):
        nd = N('GeometryNodeInputNamedAttribute', data_type='FLOAT'); nd.inputs['Name'].default_value = name
        return nd.outputs['Attribute']
    oi = N('GeometryNodeObjectInfo'); oi.transform_space = 'ORIGINAL'; L(gi.outputs['Wind Control'], oi.inputs['Object'])
    # direction = control's local +Z rotated to world (rotate vector by the object's rotation), flattened to XY
    rot = N('FunctionNodeRotateVector'); rot.inputs['Vector'].default_value = (0, 0, 1)
    L(oi.outputs['Rotation'], rot.inputs['Rotation'])
    flat = VM('MULTIPLY', rot.outputs['Vector'], (1, 1, .15)); wdir = VM('NORMALIZE', flat)
    tm = N('GeometryNodeInputSceneTime')
    t = M('MULTIPLY', tm.outputs['Seconds'], gi.outputs['Speed'])
    # gust: slow 1D noise over time
    gn = N('ShaderNodeTexNoise'); gn.noise_dimensions = '1D'; gn.inputs['Scale'].default_value = .25
    L(t, gn.inputs['W'])
    gust = M('ADD', 1.0, M('MULTIPLY', M('SUBTRACT', gn.outputs['Fac'], .5), M('MULTIPLY', gi.outputs['Gust'], 2.0)))
    S_ = M('MULTIPLY', M('MULTIPLY', gi.outputs['Strength'], gust), gi.outputs['Flexibility'])
    pos = N('GeometryNodeInputPosition').outputs[0]
    # per-plant phase from object position (instances get different phases)
    sx = N('ShaderNodeSeparateXYZ'); L(oi.outputs['Location'], sx.inputs[0]) if False else None
    ph = A('wind_phase')
    # trunk: 0.3 Hz sway + small 2nd harmonic, mean bend downwind (lean) + oscillation
    st = M('SINE', M('ADD', M('MULTIPLY', t, 1.9), M('MULTIPLY', ph, .5)))
    trunk = M('MULTIPLY', M('MULTIPLY', A('wind_trunk'), gi.outputs['Trunk Sway (m)']), M('ADD', .6, M('MULTIPLY', st, .4)))
    sb = M('SINE', M('ADD', M('MULTIPLY', t, 4.3), M('MULTIPLY', ph, 6.283)))
    branch = M('MULTIPLY', M('MULTIPLY', A('wind_branch'), gi.outputs['Branch Sway (m)']), M('ADD', .35, M('MULTIPLY', sb, .65)))
    amp = M('MULTIPLY', M('ADD', trunk, branch), S_)
    off1 = VM('SCALE', wdir, scale=amp)
    # small vertical bob for branches (perpendicular motion)
    bob = M('MULTIPLY', M('MULTIPLY', M('MULTIPLY', A('wind_branch'), gi.outputs['Branch Sway (m)']), M('SINE', M('ADD', M('MULTIPLY', t, 3.1), M('MULTIPLY', ph, 9.0)))), M('MULTIPLY', S_, .35))
    off2 = VM('SCALE', (0, 0, 1), scale=bob)
    # leaf flutter: 3D noise in space-time
    comb = N('ShaderNodeCombineXYZ'); L(M('MULTIPLY', t, 7.0), comb.inputs['Z'])
    pv = VM('ADD', VM('SCALE', pos, scale=3.0), comb.outputs[0])
    fn = N('ShaderNodeTexNoise'); fn.noise_dimensions = '3D'; fn.inputs['Scale'].default_value = 1.0; L(pv, fn.inputs['Vector'])
    fv = VM('SUBTRACT', fn.outputs['Color'], (.5, .5, .5))
    fl = M('MULTIPLY', M('MULTIPLY', A('wind_leaf'), gi.outputs['Leaf Flutter (m)']), M('MULTIPLY', gi.outputs['Flutter'], M('MINIMUM', S_, 4.0)))   # calm = still
    off3 = VM('SCALE', fv, scale=M('MULTIPLY', fl, 2.0))
    off = VM('ADD', VM('ADD', off1, off2), off3)
    sp = N('GeometryNodeSetPosition'); L(gi.outputs['Geometry'], sp.inputs['Geometry']); L(off, sp.inputs['Offset'])
    L(sp.outputs[0], go.inputs['Geometry'])
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


def add_wind(o, trunk=.15, branch=.12, leaf=.03, flex=1.0):
    """wind modifier on a vegetation object. Strength / gust / speed / flutter are DRIVEN by T6_WIND_CONTROL's custom
    properties (single-property drivers: no Python expressions → work without 'auto-run scripts')."""
    ctrl = wind_control(); ng = wind_group()
    md = o.modifiers.new('T6_WIND', 'NODES'); md.node_group = ng
    ids = {it.name: it.identifier for it in ng.interface.items_tree if getattr(it, 'in_out', None) == 'INPUT'}
    md[ids['Wind Control']] = ctrl
    md[ids['Trunk Sway (m)']] = trunk; md[ids['Branch Sway (m)']] = branch; md[ids['Leaf Flutter (m)']] = leaf
    md[ids['Flexibility']] = flex
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
    col = b.mix(b.math('MULTIPLY', veins, .7), col, hexc(vein))
    col = b.mix(b.math('MULTIPLY', b.math('SUBTRACT', nz.outputs['Fac'], .5), .3), col, (0, 0, 0, 1))
    b.l(col, bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = rough
    bp = b.n('ShaderNodeBump'); bp.inputs['Strength'].default_value = .35; bp.inputs['Distance'].default_value = .002
    b.l(b.math('SUBTRACT', 1.0, veins), bp.inputs['Height']); b.l(bp.outputs['Normal'], bsdf.inputs['Normal'])
    tl = b.n('ShaderNodeBsdfTranslucent'); b.l(col, tl.inputs['Color']); b.l(bp.outputs['Normal'], tl.inputs['Normal'])
    mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl; b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2])
    b.l(mx.outputs[0], out.inputs['Surface']); m.diffuse_color = hexc(base)
    return m


def mat_petal(name, base, rough=.4, transl=.35, sss=.25):
    """petal: colour ramp along the petal (grad attribute: 0 base → 1 tip), fine streaks along UV v, translucency, subsurface."""
    m, nt, b = new_mat(name)
    out = b.n('ShaderNodeOutputMaterial'); bsdf = b.n('ShaderNodeBsdfPrincipled')
    c = hexc(base); dark = tuple(x * .55 for x in c[:3]) + (1,); light = tuple(min(1, x * 1.25 + .03) for x in c[:3]) + (1,)
    col = b.ramp(b.attr('grad'), [(0.0, dark), (.35, c), (1.0, light)])
    uv = b.n('ShaderNodeUVMap', uv_map='UVMap').outputs[0]; sep = b.n('ShaderNodeSeparateXYZ'); b.l(uv, sep.inputs[0])
    st = b.n('ShaderNodeTexWave'); st.wave_type = 'BANDS'; st.bands_direction = 'X'; st.inputs['Scale'].default_value = 6
    st.inputs['Distortion'].default_value = 2; b.l(uv, st.inputs['Vector'])
    col = b.mix(b.math('MULTIPLY', st.outputs['Fac'], .18), col, dark)
    b.l(col, bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Subsurface Weight'].default_value = sss; bsdf.inputs['Sheen Weight'].default_value = .3
    tl = b.n('ShaderNodeBsdfTranslucent'); b.l(col, tl.inputs['Color'])
    mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = transl; b.l(bsdf.outputs[0], mx.inputs[1]); b.l(tl.outputs[0], mx.inputs[2])
    b.l(mx.outputs[0], out.inputs['Surface']); m.diffuse_color = c
    return m

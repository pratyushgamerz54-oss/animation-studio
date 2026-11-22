"""envkit — reusable procedural ENVIRONMENT asset library (no downloaded assets needed).

Everything is generated from code so every location uses the same, consistent assets:
  textures  : leaf / needle-spray / grass-blade RGBA cards (PIL) → 02_world/_shared/tex/
  materials : bark, leaf, needles, grass, terrain (grass/dirt/rock strata/snow), stone flags, coursed stone,
              grimy lime plaster, aged timber, clay roof tiles with moss, brass, clay pots, cloth, water, haze, mist, clouds
  vegetation: broadleaf tree (recursive branches + leaf cards), Himalayan conifer (deodar-like drooping tiers),
              grass clump, bush, rock
  scatter   : geometry-nodes scatter (density from a vertex group) — instanced, never merged
API stays inside what Blender 4.5 and 5.x share.
"""
import os, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex'); os.makedirs(TEX, exist_ok=True)


def hexlin(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple([(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c] + [a])


# ======================================================================= textures (PIL)
def tex_leaf(path, seed=1):
    W = 512; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(seed)
    # a small twig with 7 leaves (one card = one leaf cluster)
    d.line((W * .5, W * .98, W * .5, W * .2), fill=(70, 55, 30, 255), width=6)
    for k in range(7):
        t = .25 + k * .1; side = 1 if k % 2 else -1
        cx, cy = W * .5 + side * W * .18, W * (1 - t) - W * .05
        ang = side * r.uniform(25, 45)
        L, Wd = W * .22, W * .09
        pts = []
        for i in range(21):
            u = i / 20; w = math.sin(math.pi * u) ** .8 * Wd
            pts.append((u * L, w))
        pts += [(u, -w) for u, w in reversed(pts)]
        a = math.radians(ang + (90 if side > 0 else -90) * .0)
        base = (W * .5, cy + W * .06)
        dirx = side
        P = [(base[0] + dirx * (x * math.cos(math.radians(ang)) ) , base[1] - x * math.sin(math.radians(abs(ang))) + y) for x, y in pts]
        g = r.randint(-12, 12)
        d.polygon(P, fill=(60 + g, 105 + g, 40 + g // 2, 255))
        d.line((P[0], P[20]), fill=(95, 135, 60, 255), width=2)
    im.save(path); return path


def tex_needles(path, seed=2):
    W = 512; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(seed)
    d.line((W * .5, W, W * .5, 0), fill=(70, 50, 30, 255), width=7)
    for k in range(110):
        y = W * (1 - k / 110)
        for side in (-1, 1):
            L = W * .44 * math.sin(math.pi * (k / 110) ** .8) + 10
            ang = math.radians(r.uniform(55, 75))
            x2, y2 = W * .5 + side * L * math.sin(ang), y - L * math.cos(ang) * .6
            g = r.randint(-15, 10)
            d.line((W * .5, y, x2, y2), fill=(48 + g, 82 + g, 44 + g, 255), width=6)
    im.save(path); return path


def textures():
    p = {'leaf': os.path.join(TEX, 'leaf_cluster.png'), 'needles': os.path.join(TEX, 'needle_spray.png')}
    if not os.path.exists(p['leaf']):
        tex_leaf(p['leaf'])
    if not os.path.exists(p['needles']):
        tex_needles(p['needles'])
    return p


# ======================================================================= material helpers
class N:
    """tiny node-tree builder"""
    def __init__(self, mat):
        self.m = mat; self.nt = mat.node_tree; self.n = self.nt.nodes; self.l = self.nt.links
        self.bs = self.n.get('Principled BSDF')

    def node(self, t, **kw):
        x = self.n.new(t)
        for k, v in kw.items():
            if k in x.inputs:
                x.inputs[k].default_value = v
            else:
                setattr(x, k, v)
        return x

    def link(self, a, b):
        self.l.new(a, b); return b

    def mix(self, fac, a, b):
        m = self.node('ShaderNodeMix', data_type='RGBA')
        for sock, v in (('A', a), ('B', b)):
            if isinstance(v, tuple):
                m.inputs[sock].default_value = v
            else:
                self.l.new(v, m.inputs[sock])
        if isinstance(fac, (int, float)):
            m.inputs['Factor'].default_value = fac
        else:
            self.l.new(fac, m.inputs['Factor'])
        return m.outputs['Result']

    def ramp(self, fac, stops):
        r = self.node('ShaderNodeValToRGB'); e = r.color_ramp.elements
        e[0].position, e[0].color = stops[0][0], hexlin(stops[0][1]); e[1].position, e[1].color = stops[-1][0], hexlin(stops[-1][1])
        for pos, col in stops[1:-1]:
            x = e.new(pos); x.color = hexlin(col)
        self.l.new(fac, r.inputs['Fac']); return r.outputs['Color']

    def math(self, op, a, b=None):
        m = self.node('ShaderNodeMath', operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                self.l.new(v, m.inputs[i])
        return m.outputs[0]

    def bump(self, h, strength=.3, dist=.02):
        b = self.node('ShaderNodeBump'); b.inputs['Strength'].default_value = strength; b.inputs['Distance'].default_value = dist
        self.l.new(h, b.inputs['Height']); self.l.new(b.outputs['Normal'], self.bs.inputs['Normal']); return b

    def coord(self, kind='Object', scale=(1, 1, 1)):
        tc = self.node('ShaderNodeTexCoord'); mp = self.node('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = scale; self.l.new(tc.outputs[kind], mp.inputs['Vector']); return mp.outputs['Vector']

    def noise(self, vec, scale, detail=6, rough=.55, out='Fac'):
        t = self.node('ShaderNodeTexNoise'); t.inputs['Scale'].default_value = scale; t.inputs['Detail'].default_value = detail
        t.inputs['Roughness'].default_value = rough; self.l.new(vec, t.inputs['Vector']); return t.outputs[out]

    def voronoi(self, vec, scale, feature='F1', out='Distance'):
        t = self.node('ShaderNodeTexVoronoi', feature=feature); t.inputs['Scale'].default_value = scale
        self.l.new(vec, t.inputs['Vector']); return t.outputs[out]

    def ao(self, dist=.6):
        a = self.node('ShaderNodeAmbientOcclusion'); a.inputs['Distance'].default_value = dist; a.samples = 8
        return a.outputs['AO']

    def set(self, name, v):
        if name not in self.bs.inputs:
            return
        if isinstance(v, (int, float, tuple)):
            self.bs.inputs[name].default_value = v
        else:
            self.l.new(v, self.bs.inputs[name])


def newmat(name):
    m = bpy.data.materials.get(name)
    if m:
        return m, None
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, N(m)


# ======================================================================= materials
def mat_bark(name='MAT_ENV_BARK', a='#4E3D2E', b='#2E241B'):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (6, 6, .9))
        c = n.math('MULTIPLY', n.noise(v, 3, 10, .7), n.voronoi(v, 4, 'DISTANCE_TO_EDGE'))
        n.set('Base Color', n.ramp(c, [(0, b), (.35, a), (.6, '#6A5848')])); n.set('Roughness', .9); n.bump(c, .8, .05)
    return m


def mat_card(name, img, tint_a, tint_b, rough=.55, trans=.25):
    """alpha leaf / needle card with colour variation per instance and back-light translucency."""
    m, n = newmat(name)
    if n:
        t = n.node('ShaderNodeTexImage'); t.image = bpy.data.images.load(img, check_existing=True)
        uv = n.node('ShaderNodeTexCoord'); n.link(uv.outputs['UV'], t.inputs['Vector'])
        oi = n.node('ShaderNodeObjectInfo')
        var = n.mix(oi.outputs['Random'], hexlin(tint_a), hexlin(tint_b))
        col = n.node('ShaderNodeMix', data_type='RGBA'); col.inputs['Factor'].default_value = .65
        n.link(t.outputs['Color'], col.inputs['A']); n.link(var, col.inputs['B'])
        n.set('Base Color', col.outputs['Result']); n.set('Alpha', t.outputs['Alpha']); n.set('Roughness', rough)
        n.set('Subsurface Weight', 0.0)
        # translucency: mix principled with translucent BSDF
        tr = n.node('ShaderNodeBsdfTranslucent'); n.link(col.outputs['Result'], tr.inputs['Color'])
        tp = n.node('ShaderNodeBsdfTransparent')
        mx = n.node('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = trans
        n.link(n.bs.outputs['BSDF'], mx.inputs[1]); n.link(tr.outputs['BSDF'], mx.inputs[2])
        cut = n.node('ShaderNodeMixShader'); n.link(t.outputs['Alpha'], cut.inputs['Fac'])
        n.link(tp.outputs['BSDF'], cut.inputs[1]); n.link(mx.outputs['Shader'], cut.inputs[2])
        n.link(cut.outputs['Shader'], n.n['Material Output'].inputs['Surface'])
        try:
            m.blend_method = 'HASHED'
        except Exception:
            pass
    return m


def mat_grass(name='MAT_ENV_GRASS_BLADE'):
    m, n = newmat(name)
    if n:
        uv = n.node('ShaderNodeTexCoord'); sep = n.node('ShaderNodeSeparateXYZ'); n.link(uv.outputs['UV'], sep.inputs['Vector'])
        oi = n.node('ShaderNodeObjectInfo')
        tipcol = n.mix(oi.outputs['Random'], hexlin('#8FA548'), hexlin('#B8B060'))
        c = n.mix(sep.outputs['Y'], hexlin('#2F4A1E'), tipcol)
        n.set('Base Color', c); n.set('Roughness', .6)
        tr = n.node('ShaderNodeBsdfTranslucent'); n.link(c, tr.inputs['Color'])
        mx = n.node('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = .3
        n.link(n.bs.outputs['BSDF'], mx.inputs[1]); n.link(tr.outputs['BSDF'], mx.inputs[2])
        n.link(mx.outputs['Shader'], n.n['Material Output'].inputs['Surface'])
    return m


def mat_terrain(name='MAT_ENV_TERRAIN', snow_z=(1050, 1250), world_scale=1.0):
    """grass (3 greens + dry patches) / dirt / rock strata / snow by height and slope."""
    m, n = newmat(name)
    if not n:
        return m
    geo = n.node('ShaderNodeNewGeometry')
    nz = n.node('ShaderNodeSeparateXYZ'); n.link(geo.outputs['Normal'], nz.inputs['Vector'])
    pz = n.node('ShaderNodeSeparateXYZ'); n.link(geo.outputs['Position'], pz.inputs['Vector'])
    v = n.coord('Object', (1, 1, 1))
    big = n.noise(v, .004 / world_scale, 6, .6)
    mid = n.noise(v, .05 / world_scale, 8, .6)
    fine = n.noise(v, 1.6, 6, .7)
    grass = n.ramp(n.math('ADD', n.math('MULTIPLY', big, .7), n.math('MULTIPLY', mid, .3)),
                   [(.30, '#3C5524'), (.48, '#566E30'), (.58, '#6F7A3C'), (.70, '#87824E')])
    dirt = n.ramp(fine, [(.3, '#6C5A42'), (.7, '#8E7656')])
    dfac = n.math('GREATER_THAN', n.noise(v, .03, 4, .5), .63)
    ground = n.mix(dfac, grass, dirt)
    # rock with strata (wave along Z, distorted)
    wv = n.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='Z'); wv.inputs['Scale'].default_value = .018 / world_scale
    wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 6
    n.link(v, wv.inputs['Vector'])
    cr = n.voronoi(n.coord('Object', (1, 1, 2.5)), .08 / world_scale, 'DISTANCE_TO_EDGE')
    rockh = n.math('ADD', n.math('MULTIPLY', wv.outputs['Fac'], .18), n.math('MULTIPLY', cr, .9))
    rock = n.ramp(n.math('ADD', n.math('MULTIPLY', rockh, .6), n.math('MULTIPLY', n.noise(v, .02 / world_scale, 8, .65), .6)),
                  [(.25, '#4A4640'), (.5, '#6E685F'), (.8, '#8E877C')])
    steep = n.node('ShaderNodeMapRange'); steep.inputs['From Min'].default_value = .70; steep.inputs['From Max'].default_value = .52
    n.link(n.math('ADD', nz.outputs['Z'], n.math('MULTIPLY', mid, .12)), steep.inputs['Value'])
    c1 = n.mix(steep.outputs['Result'], ground, rock)
    hi = n.node('ShaderNodeMapRange'); hi.inputs['From Min'].default_value = snow_z[0]; hi.inputs['From Max'].default_value = snow_z[1]
    n.link(n.math('ADD', pz.outputs['Z'], n.math('MULTIPLY', big, 260)), hi.inputs['Value'])
    flat = n.node('ShaderNodeMapRange'); flat.inputs['From Min'].default_value = .45; flat.inputs['From Max'].default_value = .72
    n.link(nz.outputs['Z'], flat.inputs['Value'])
    sn = n.math('MULTIPLY', hi.outputs['Result'], flat.outputs['Result'])
    col = n.mix(sn, c1, hexlin('#EEF2F6'))
    n.set('Base Color', col)
    n.set('Roughness', n.math('ADD', .96, n.math('MULTIPLY', sn, -.5)))
    n.set('Specular IOR Level', .25)
    n.bump(n.math('ADD', n.math('MULTIPLY', rockh, steep.outputs['Result']), n.math('MULTIPLY', fine, .25)), .45, .3)
    return m


def mat_stone_flags(name='MAT_ENV_STONE_FLAGS', scale=.9):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (1, 1, 1))
        vt = n.node('ShaderNodeTexVoronoi', feature='F1'); vt.inputs['Scale'].default_value = scale; n.link(v, vt.inputs['Vector'])
        ed = n.node('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); ed.inputs['Scale'].default_value = scale; n.link(v, ed.inputs['Vector'])
        grout = n.math('LESS_THAN', ed.outputs['Distance'], .035)
        cell = n.ramp(vt.outputs['Color'], [(0, '#7D7466'), (.5, '#9A8F7D'), (1, '#B2A78F')])
        dirt = n.math('MULTIPLY', n.noise(v, 2, 8), 1.0)
        c = n.mix(n.math('MULTIPLY', dirt, .35), cell, hexlin('#5C5446'))
        c = n.mix(grout, c, hexlin('#4A4338'))
        c = n.mix(n.math('SUBTRACT', 1, n.ao(.5)), c, hexlin('#3A352C'))
        n.set('Base Color', c); n.set('Roughness', .82)
        n.bump(n.math('ADD', n.math('MULTIPLY', grout, -1), n.math('MULTIPLY', n.noise(v, 9, 8), .3)), .5, .02)
    return m


def mat_coursed_stone(name='MAT_ENV_STONE_COURSED'):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (1, 1, 1))
        br = n.node('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = .015
        br.inputs['Mortar Smooth'].default_value = .2; br.offset = .5; br.inputs['Brick Width'].default_value = .9; br.inputs['Row Height'].default_value = .35
        br.inputs['Color1'].default_value = hexlin('#8E8372'); br.inputs['Color2'].default_value = hexlin('#A39782')
        br.inputs['Mortar'].default_value = hexlin('#5A5246'); n.link(v, br.inputs['Vector'])
        nz = n.noise(v, 6, 10, .7)
        c = n.mix(n.math('MULTIPLY', nz, .4), br.outputs['Color'], hexlin('#6E6455'))
        c = n.mix(n.math('SUBTRACT', 1, n.ao(.6)), c, hexlin('#3E372E'))
        # moss at the base
        pz = n.node('ShaderNodeSeparateXYZ'); n.link(n.node('ShaderNodeNewGeometry').outputs['Position'], pz.inputs['Vector'])
        moss = n.math('MULTIPLY', n.math('LESS_THAN', pz.outputs['Z'], .35), n.math('GREATER_THAN', n.noise(v, 3, 6), .55))
        c = n.mix(n.math('MULTIPLY', moss, .7), c, hexlin('#4F5E2C'))
        n.set('Base Color', c); n.set('Roughness', .85)
        n.bump(n.math('ADD', n.math('MULTIPLY', br.outputs['Fac'], -1), n.math('MULTIPLY', nz, .4)), .6, .03)
    return m


def mat_plaster(name='MAT_ENV_LIME_PLASTER'):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (1, 1, 1))
        pz = n.node('ShaderNodeSeparateXYZ'); n.link(n.node('ShaderNodeNewGeometry').outputs['Position'], pz.inputs['Vector'])
        base = n.ramp(n.noise(v, 1.2, 8, .6), [(.3, '#E2D3B6'), (.7, '#EFE3CA')])
        grime_h = n.node('ShaderNodeMapRange'); grime_h.inputs['From Min'].default_value = 1.2; grime_h.inputs['From Max'].default_value = 0.0
        n.link(n.math('ADD', pz.outputs['Z'], n.math('MULTIPLY', n.noise(v, 4, 6), .6)), grime_h.inputs['Value'])
        c = n.mix(n.math('MULTIPLY', grime_h.outputs['Result'], .75), base, hexlin('#8E7C62'))
        streak = n.noise(n.coord('Object', (6, 6, .4)), 2.5, 4)
        c = n.mix(n.math('MULTIPLY', n.math('GREATER_THAN', streak, .62), .35), c, hexlin('#A89778'))
        c = n.mix(n.math('SUBTRACT', 1, n.ao(.8)), c, hexlin('#6E604C'))
        n.set('Base Color', c); n.set('Roughness', .88)
        n.bump(n.noise(v, 18, 6, .7), .12, .01)
    return m


def mat_timber(name='MAT_ENV_TIMBER_AGED', a='#6B4426', b='#3E2614'):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (2.5, 2.5, .25))
        wv = n.node('ShaderNodeTexWave', wave_type='RINGS'); wv.inputs['Scale'].default_value = 3; wv.inputs['Distortion'].default_value = 8
        wv.inputs['Detail'].default_value = 4; n.link(v, wv.inputs['Vector'])
        g = n.math('ADD', n.math('MULTIPLY', wv.outputs['Fac'], .6), n.math('MULTIPLY', n.noise(v, 30, 4), .4))
        c = n.ramp(g, [(.1, b), (.6, a), (.95, '#8A6040')])
        c = n.mix(n.math('SUBTRACT', 1, n.ao(.4)), c, hexlin('#22160C'))
        n.set('Base Color', c); n.set('Roughness', .62); n.bump(g, .25, .01)
    return m


def mat_roof_tiles(name='MAT_ENV_ROOF_TILE'):
    """clay tiles: rows (wave) + staggered joints (brick) + moss / soot patches."""
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (1, 1, 1))
        br = n.node('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 3.2; br.inputs['Mortar Size'].default_value = .02
        br.inputs['Brick Width'].default_value = .55; br.inputs['Row Height'].default_value = .4; br.offset = .5
        br.inputs['Color1'].default_value = hexlin('#A4512F'); br.inputs['Color2'].default_value = hexlin('#8E4428')
        br.inputs['Mortar'].default_value = hexlin('#3A1A0E'); n.link(v, br.inputs['Vector'])
        wv = n.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X'); wv.inputs['Scale'].default_value = 12
        wv.inputs['Distortion'].default_value = .5; n.link(v, wv.inputs['Vector'])
        nz = n.noise(v, .9, 6)
        c = n.mix(n.math('MULTIPLY', n.math('GREATER_THAN', nz, .58), .65), br.outputs['Color'], hexlin('#5E6230'))
        c = n.mix(n.math('MULTIPLY', n.noise(v, 6, 4), .35), c, hexlin('#5A2A18'))
        c = n.mix(n.math('SUBTRACT', 1, n.ao(.5)), c, hexlin('#2A120A'))
        n.set('Base Color', c); n.set('Roughness', .55)
        n.bump(n.math('ADD', wv.outputs['Fac'], n.math('MULTIPLY', br.outputs['Fac'], -1.2)), .9, .04)
    return m


def mat_simple(name, hexc, rough=.5, metal=0., emit=None, strength=0.):
    m, n = newmat(name)
    if n:
        n.set('Base Color', hexlin(hexc)); n.set('Roughness', rough); n.set('Metallic', metal)
        if emit:
            n.set('Emission Color', hexlin(emit)); n.set('Emission Strength', strength)
    return m


def mat_water(name='MAT_ENV_WATER'):
    m, n = newmat(name)
    if n:
        v = n.coord('Object', (1, 1, 1))
        n.set('Base Color', hexlin('#1E4656')); n.set('Roughness', .03)
        try:
            n.set('Transmission Weight', .6); n.set('IOR', 1.33)
        except Exception:
            pass
        n.bump(n.noise(n.coord('Object', (1, 2.2, 1)), .25, 6), .25, .4)
    return m


def mat_volume(name, col, dens, noise_scale=None, anis=.3):
    m, n = newmat(name)
    if n:
        n.n.remove(n.bs)
        vp = n.node('ShaderNodeVolumePrincipled'); vp.inputs['Color'].default_value = hexlin(col); vp.inputs['Anisotropy'].default_value = anis
        if noise_scale:
            d = n.math('MULTIPLY', n.math('MAXIMUM', n.math('SUBTRACT', n.noise(n.coord('Object'), noise_scale, 4), .42), 0), dens * 6)
            n.link(d, vp.inputs['Density'])
        else:
            vp.inputs['Density'].default_value = dens
        n.link(vp.outputs['Volume'], n.n['Material Output'].inputs['Volume'])
    return m


def mat_clouds(name='MAT_ENV_CLOUD_LAYER'):
    m, n = newmat(name)
    if n:
        n.n.remove(n.bs)
        v = n.coord('Object', (1, 1, 1))
        c = n.math('MAXIMUM', n.math('SUBTRACT', n.noise(v, .00018, 8, .55), .5), 0)
        a = n.math('MINIMUM', n.math('MULTIPLY', c, 5), 1)
        em = n.node('ShaderNodeEmission'); em.inputs['Color'].default_value = hexlin('#FFF4E8'); em.inputs['Strength'].default_value = 1.4
        tp = n.node('ShaderNodeBsdfTransparent'); mx = n.node('ShaderNodeMixShader')
        n.link(a, mx.inputs['Fac']); n.link(tp.outputs['BSDF'], mx.inputs[1]); n.link(em.outputs['Emission'], mx.inputs[2])
        n.link(mx.outputs['Shader'], n.n['Material Output'].inputs['Surface'])
    return m


# ======================================================================= mesh builders
def tube(bm, pts, radii, sides=7):
    """loft a tube through pts (list of Vector) with radii; returns nothing (adds to bm)."""
    rings = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = d.orthogonal().normalized(); b = d.cross(a)
        rings.append([bm.verts.new(p + (a * math.cos(2 * math.pi * k / sides) + b * math.sin(2 * math.pi * k / sides)) * radii[i])
                      for k in range(sides)])
    for i in range(len(rings) - 1):
        for k in range(sides):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % sides], rings[i + 1][(k + 1) % sides], rings[i + 1][k]))


def card(bm, uvl, c, normal, up, w, h):
    """one alpha card centred at c, facing `normal`, growing along `up`."""
    side = up.cross(normal).normalized() * w / 2
    up = up.normalized() * h
    vs = [bm.verts.new(c - side), bm.verts.new(c + side), bm.verts.new(c + side + up), bm.verts.new(c - side + up)]
    f = bm.faces.new(vs)
    for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uvl].uv = uv
    return f


def make_broadleaf(name, coll, mats, seed=1, height=11.0, spread=1.0, leaves=3800):
    """recursive branching tree with leaf-cluster cards."""
    r = random.Random(seed)
    bark = bmesh.new(); leaf = bmesh.new(); uvl = leaf.loops.layers.uv.new('UVMap')
    bark.loops.layers.uv.new('UVMap')
    tips = []

    def branch(p, d, L, rad, depth):
        n = max(3, int(L / .6)); pts = [p]; rr = [rad]
        cur, dd = p.copy(), d.copy()
        for i in range(n):
            dd = (dd + Vector((r.uniform(-.18, .18), r.uniform(-.18, .18), r.uniform(-.05, .12)))).normalized()
            cur = cur + dd * (L / n); pts.append(cur.copy()); rr.append(rad * (1 - .75 * (i + 1) / n))
        tube(bark, pts, rr, 7 if depth < 2 else 5)
        if depth >= 3 or L < .8:
            tips.append((cur, dd)); return
        kids = 3 if depth == 0 else 3
        for k in range(kids):
            t = r.uniform(.45, .9) if depth == 0 else r.uniform(.35, .95)
            i = int(t * n); q = pts[i]
            nd = (dd + Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(.1, .7))) * .9 * spread).normalized()
            branch(q, nd, L * r.uniform(.55, .7), rr[i] * .62, depth + 1)
        tips.append((cur, dd))
    branch(Vector((0, 0, 0)), Vector((0, 0, 1)), height * .55, height * .028, 0)
    for k in range(leaves):
        p, d = r.choice(tips)
        off = Vector((r.gauss(0, 1), r.gauss(0, 1), r.gauss(.2, .7))) * height * .085
        c = p + off
        nrm = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-.3, 1))).normalized()
        up = (off.normalized() + Vector((0, 0, .3))).normalized()
        if abs(up.dot(nrm)) > .95:
            nrm = Vector((1, 0, 0))
        s = height * r.uniform(.055, .085)
        card(leaf, uvl, c, nrm, up, s, s)
    return _two(name, coll, bark, leaf, mats['bark'], mats['leaf'])


def make_conifer(name, coll, mats, seed=1, height=18.0, width=.40, tiers=28):
    """deodar-like conifer: tapered trunk + drooping branch tiers made of needle-spray cards."""
    r = random.Random(seed)
    bark = bmesh.new(); nd = bmesh.new(); uvl = nd.loops.layers.uv.new('UVMap')
    bark.loops.layers.uv.new('UVMap')
    tube(bark, [Vector((0, 0, z)) for z in np.linspace(0, height * .97, 8)], [height * .022 * (1 - .9 * t) for t in np.linspace(0, 1, 8)], 7)
    for t in range(tiers):
        u = t / (tiers - 1)
        z = height * (.18 + .8 * u)
        R = height * width * (1 - u) ** 1.1 + .4
        nb = max(6, int(14 * (1 - u)) + 6)
        for b in range(nb):
            a = 2 * math.pi * b / nb + r.uniform(-.3, .3) + t * 1.3
            d = Vector((math.cos(a), math.sin(a), 0))
            droop = r.uniform(.12, .32)
            # branch = 5 overlapping sprays laid along the drooping arm
            for s in range(5):
                f = .15 + .2 * s
                c = Vector((0, 0, z)) + d * R * f - Vector((0, 0, droop * R * f * f))
                up = (d - Vector((0, 0, droop * 1.2 * f))).normalized()
                nrm = Vector((0, 0, 1)).cross(d).normalized().cross(up).normalized()
                card(nd, uvl, c - up * R * .2, (nrm + Vector((r.uniform(-.4, .4), r.uniform(-.4, .4), r.uniform(-.2, .2)))).normalized(), up, R * .5, R * .42)
    card(nd, uvl, Vector((0, 0, height - .6)), Vector((1, 0, 0)), Vector((0, 0, 1)), 1.0, 2.0)
    card(nd, uvl, Vector((0, 0, height - .6)), Vector((0, 1, 0)), Vector((0, 0, 1)), 1.0, 2.0)
    return _two(name, coll, bark, nd, mats['bark'], mats['needles'])


def make_grass(name, coll, mat, seed=1, blades=28, h=.45):
    r = random.Random(seed); bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    for k in range(blades):
        a = r.uniform(0, 6.283); p = Vector((r.gauss(0, .13), r.gauss(0, .13), 0))
        lean = Vector((math.cos(a), math.sin(a), 0)) * r.uniform(.05, .25)
        H = h * r.uniform(.6, 1.3); w = r.uniform(.008, .016)
        side = Vector((-math.sin(a), math.cos(a), 0)) * w
        segs = 4; prev = None
        for i in range(segs + 1):
            t = i / segs
            c = p + Vector((0, 0, H * t)) + lean * H * t * t
            ww = 1 - t * .95
            v1, v2 = bm.verts.new(c - side * ww), bm.verts.new(c + side * ww)
            if prev:
                f = bm.faces.new((prev[0], prev[1], v2, v1))
                for lp, uv in zip(f.loops, ((0, (i - 1) / segs), (1, (i - 1) / segs), (1, t), (0, t))):
                    lp[uvl].uv = uv
            prev = (v1, v2)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    return o


def make_rock(name, coll, mat, seed=1, size=1.5):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=size)
    r = random.Random(seed)
    for v in bm.verts:
        n = v.co.normalized()
        v.co *= 1 + .25 * math.sin(n.x * 3 + seed) * math.cos(n.y * 2.3) + r.uniform(-.06, .06)
        v.co.z *= .62
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    return o


def _two(name, coll, bark, leaf, mb, ml):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    tmp1 = bpy.data.meshes.new('t1'); bark.to_mesh(tmp1); bark.free()
    tmp2 = bpy.data.meshes.new('t2'); leaf.to_mesh(tmp2); leaf.free()
    o1 = bpy.data.objects.new(name, tmp1); o2 = bpy.data.objects.new(name + '_L', tmp2)
    coll.objects.link(o1); coll.objects.link(o2)
    tmp1.materials.append(mb); tmp2.materials.append(ml)
    for p in tmp1.polygons:
        p.use_smooth = True
    bpy.ops.object.select_all(action='DESELECT'); o1.select_set(True); o2.select_set(True)
    bpy.context.view_layer.objects.active = o1; bpy.ops.object.join()
    o1.data.name = name
    return o1


# ======================================================================= scatter (geometry nodes)
def scatter(target, name, coll_src, density, group=None, seed=0, scale=(.8, 1.3), align_normal=False, max_density=None):
    """instance every object of `coll_src` on `target` faces with `density` per m² (x vertex-group weight)."""
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nd, lk = ng.nodes, ng.links
    gi = nd.new('NodeGroupInput'); go = nd.new('NodeGroupOutput')
    dist = nd.new('GeometryNodeDistributePointsOnFaces'); dist.inputs['Density'].default_value = density; dist.inputs['Seed'].default_value = seed
    lk.new(gi.outputs[0], dist.inputs['Mesh'])
    if group:
        na = nd.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT'; na.inputs['Name'].default_value = group
        mul = nd.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = density
        lk.new(na.outputs['Attribute'], mul.inputs[0]); lk.new(mul.outputs[0], dist.inputs['Density'])
    ci = nd.new('GeometryNodeCollectionInfo'); ci.inputs['Collection'].default_value = coll_src
    ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
    io = nd.new('GeometryNodeInstanceOnPoints'); io.inputs['Pick Instance'].default_value = True
    lk.new(dist.outputs['Points'], io.inputs['Points']); lk.new(ci.outputs[0], io.inputs['Instance'])
    rv = nd.new('FunctionNodeRandomValue'); rv.data_type = 'FLOAT_VECTOR'
    rv.inputs['Seed'].default_value = seed + 1
    vin = [x for x in rv.inputs if x.type == 'VECTOR']; vin[0].default_value = (0, 0, 0); vin[1].default_value = (0, 0, 6.283)
    e2r = nd.new('FunctionNodeEulerToRotation'); lk.new([x for x in rv.outputs if x.type == 'VECTOR'][0], e2r.inputs['Euler'])
    if align_normal:
        lk.new(dist.outputs['Rotation'], io.inputs['Rotation'])
    else:
        lk.new(e2r.outputs['Rotation'], io.inputs['Rotation'])
    S = lambda node, nm, t, out=False: next(x for x in (node.outputs if out else node.inputs) if x.name == nm and x.type == t)
    rs = nd.new('FunctionNodeRandomValue'); rs.data_type = 'FLOAT'
    S(rs, 'Min', 'VALUE').default_value = scale[0]; S(rs, 'Max', 'VALUE').default_value = scale[1]
    rs.inputs['Seed'].default_value = seed + 2
    lk.new(S(rs, 'Value', 'VALUE', True), io.inputs['Scale'])
    ix = nd.new('FunctionNodeRandomValue'); ix.data_type = 'INT'
    S(ix, 'Min', 'INT').default_value = 0; S(ix, 'Max', 'INT').default_value = 999
    ix.inputs['Seed'].default_value = seed + 3
    lk.new(S(ix, 'Value', 'INT', True), io.inputs['Instance Index'])
    lk.new(io.outputs[0], go.inputs[0])
    holder = bpy.data.objects.new(name, target.data)
    target.users_collection[0].objects.link(holder)
    holder.matrix_world = target.matrix_world
    mod = holder.modifiers.new(name, 'NODES'); mod.node_group = ng
    holder.hide_select = True
    return holder

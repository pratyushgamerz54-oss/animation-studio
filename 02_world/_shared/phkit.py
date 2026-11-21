"""phkit — use the downloaded Poly Haven CC0 assets (03_assets/external/polyhaven) inside our scenes.

- available()            : are the assets on disk? (run 03_assets/external/polyhaven_fetch.py first)
- append(model, coll)    : append one LOD collection of a model into a hidden library collection
- pbr(name, tex, size)   : PBR material (diffuse sRGB, roughness, GL normal map, AO multiply, height bump)
                           projection 'BOX' (triplanar-ish, object coords), 'UV' or 'XY' (top-down)
- terrain(name, ...)     : height / slope blended ground-grass / rock / snow material from photo textures
- hdri_world(id, ...)    : HDRI sky with Z rotation, returns the world
- fix_paths()            : re-point appended images to the files on disk
"""
import os, math
import bpy
from mathutils import Vector
import envkit as ek

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.abspath(os.path.join(HERE, '..', '..', '03_assets', 'external', 'polyhaven'))


def available():
    return os.path.isdir(os.path.join(PH, 'models', 'fir_tree_01')) and os.path.isdir(os.path.join(PH, 'hdris'))


def append(model, coll_name, parent):
    f = os.path.join(PH, 'models', model, f'{model}_1k.blend')
    with bpy.data.libraries.load(f) as (src, dst):
        dst.collections = [coll_name]
    c = dst.collections[0]
    parent.children.link(c)
    for o in c.objects:
        o.location = (0, 0, 0)
    fix_paths()
    return c


def fix_paths():
    idx = None
    for img in bpy.data.images:
        if img.source != 'FILE' or not img.filepath:
            continue
        p = bpy.path.abspath(img.filepath)
        if os.path.exists(p):
            continue
        if idx is None:
            idx = {}
            for root, _, fs in os.walk(os.path.join(PH, 'models')):
                for fn in fs:
                    idx[fn] = os.path.join(root, fn)
        fn = os.path.basename(p.replace('\\', '/'))
        if fn in idx:
            img.filepath = idx[fn]


def _tex(n, path, vec, proj, colorspace='sRGB'):
    t = n.node('ShaderNodeTexImage'); t.image = bpy.data.images.load(path, check_existing=True)
    try:
        t.image.colorspace_settings.name = colorspace
    except Exception:
        t.image.colorspace_settings.name = 'Non-Color' if colorspace != 'sRGB' else 'sRGB'
    if proj == 'BOX':
        t.projection = 'BOX'; t.projection_blend = .25
    n.link(vec, t.inputs['Vector'])
    return t


def maps(tex):
    d = os.path.join(PH, 'textures', tex)
    out = {}
    for k in ('diff', 'rough', 'nor_gl', 'ao', 'disp'):
        for ext in ('jpg', 'png'):
            p = os.path.join(d, f'{tex}_{k}_2k.{ext}')
            if os.path.exists(p):
                out[k] = p
    return out


def pbr_nodes(n, tex, vec, proj, tint=None, bump=.25):
    """returns (color, rough, normal_node_output, height) sockets for texture set `tex`."""
    m = maps(tex)
    col = _tex(n, m['diff'], vec, proj).outputs['Color']
    if 'ao' in m:
        ao = _tex(n, m['ao'], vec, proj, 'Non-Color')
        mul = n.node('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mul.inputs['Factor'].default_value = .8
        n.link(col, mul.inputs['A']); n.link(ao.outputs['Color'], mul.inputs['B']); col = mul.outputs['Result']
    if tint:
        tm = n.node('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); tm.inputs['Factor'].default_value = 1
        n.link(col, tm.inputs['A']); tm.inputs['B'].default_value = ek.hexlin(tint); col = tm.outputs['Result']
    rough = _tex(n, m['rough'], vec, proj, 'Non-Color').outputs['Color'] if 'rough' in m else None
    nm = None
    if 'nor_gl' in m:
        nt = _tex(n, m['nor_gl'], vec, proj, 'Non-Color')
        nmn = n.node('ShaderNodeNormalMap'); nmn.inputs['Strength'].default_value = 1.0
        n.link(nt.outputs['Color'], nmn.inputs['Color']); nm = nmn.outputs['Normal']
    h = _tex(n, m['disp'], vec, proj, 'Non-Color').outputs['Color'] if 'disp' in m else None
    return col, rough, nm, h


def pbr(name, tex, size=1.0, proj='BOX', tint=None, bump=.3):
    m, n = ek.newmat(name)
    if not n:
        return m
    s = 1.0 / size
    if proj == 'UV':
        uv = n.node('ShaderNodeTexCoord'); mp = n.node('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (s, s, s)
        n.link(uv.outputs['UV'], mp.inputs['Vector']); vec = mp.outputs['Vector']
    else:
        vec = n.coord('Object', (s, s, s))
    col, rough, nm, h = pbr_nodes(n, tex, vec, 'BOX' if proj == 'BOX' else 'FLAT', tint)
    n.set('Base Color', col)
    if rough:
        n.set('Roughness', rough)
    if h is not None and nm is not None:
        b = n.node('ShaderNodeBump'); b.inputs['Strength'].default_value = bump; b.inputs['Distance'].default_value = .02 * size
        n.link(h, b.inputs['Height']); n.link(nm, b.inputs['Normal']); n.link(b.outputs['Normal'], n.bs.inputs['Normal'])
    elif nm is not None:
        n.link(nm, n.bs.inputs['Normal'])
    return m


def terrain(name, ground=('forest_ground_04', 'sparse_grass'), rock='aerial_rocks_02', snow='snow_02',
            g_size=4.0, r_size=14.0, s_size=6.0, snow_z=(1150, 1350), steep=(.70, .52), green=None, mid_tex='aerial_grass_rock', m_size=30.0):
    m, n = ek.newmat(name)
    if not n:
        return m
    geo = n.node('ShaderNodeNewGeometry')
    nz = n.node('ShaderNodeSeparateXYZ'); n.link(geo.outputs['Normal'], nz.inputs['Vector'])
    pz = n.node('ShaderNodeSeparateXYZ'); n.link(geo.outputs['Position'], pz.inputs['Vector'])
    v = n.coord('Object')
    big = n.noise(v, .004, 6, .6); mid = n.noise(v, .03, 6, .6)
    gv = n.coord('Object', (1 / g_size,) * 3)
    g1 = pbr_nodes(n, ground[0], gv, 'FLAT'); g2 = pbr_nodes(n, ground[1], n.coord('Object', (1 / (g_size * 1.3),) * 3), 'FLAT')
    gm = n.node('ShaderNodeMapRange'); gm.inputs['From Min'].default_value = .42; gm.inputs['From Max'].default_value = .58
    n.link(n.math('ADD', n.math('MULTIPLY', big, .6), n.math('MULTIPLY', mid, .4)), gm.inputs['Value'])
    gcol = n.mix(gm.outputs['Result'], g1[0], g2[0])
    if green:      # lush version of dry photo textures: boost saturation, push towards green, keep the photo detail
        hsv = n.node('ShaderNodeHueSaturation'); hsv.inputs['Saturation'].default_value = green[1]; hsv.inputs['Value'].default_value = green[2]
        hsv.inputs['Hue'].default_value = green[3] if len(green) > 3 else .5
        n.link(gcol, hsv.inputs['Color'])
        tm = n.node('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); tm.inputs['Factor'].default_value = 1
        n.link(hsv.outputs['Color'], tm.inputs['A']); tm.inputs['B'].default_value = ek.hexlin(green[0]); gcol = tm.outputs['Result']
    if mid_tex:
        mm = pbr_nodes(n, mid_tex, n.coord('Object', (1 / m_size,) * 3), 'FLAT')
        md = n.node('ShaderNodeMapRange'); md.inputs['From Min'].default_value = .93; md.inputs['From Max'].default_value = .80
        n.link(n.math('ADD', nz.outputs['Z'], n.math('MULTIPLY', n.noise(v, .01, 4, .5), .1)), md.inputs['Value'])
        gcol = n.mix(md.outputs['Result'], gcol, mm[0])
    r = pbr_nodes(n, rock, n.coord('Object', (1 / r_size,) * 3), 'BOX')
    sn = pbr_nodes(n, snow, n.coord('Object', (1 / s_size,) * 3), 'FLAT')
    st = n.node('ShaderNodeMapRange'); st.inputs['From Min'].default_value = steep[0]; st.inputs['From Max'].default_value = steep[1]
    n.link(n.math('ADD', nz.outputs['Z'], n.math('MULTIPLY', mid, .15)), st.inputs['Value'])
    c1 = n.mix(st.outputs['Result'], gcol, r[0])
    hi = n.node('ShaderNodeMapRange'); hi.inputs['From Min'].default_value = snow_z[0]; hi.inputs['From Max'].default_value = snow_z[1]
    n.link(n.math('ADD', pz.outputs['Z'], n.math('MULTIPLY', big, 300)), hi.inputs['Value'])
    fl = n.node('ShaderNodeMapRange'); fl.inputs['From Min'].default_value = .45; fl.inputs['From Max'].default_value = .72
    n.link(nz.outputs['Z'], fl.inputs['Value'])
    snf = n.math('MULTIPLY', hi.outputs['Result'], fl.outputs['Result'])
    n.set('Base Color', n.mix(snf, c1, sn[0]))
    rr = n.mix(st.outputs['Result'], g1[1], r[1]) if g1[1] and r[1] else None
    if rr is not None:
        n.set('Roughness', rr)
    nm = n.node('ShaderNodeMix', data_type='VECTOR'); n.link(st.outputs['Result'], nm.inputs['Factor'])
    if g1[2] and r[2]:
        n.link(g1[2], nm.inputs['A']); n.link(r[2], nm.inputs['B']); n.link(nm.outputs['Result'], n.bs.inputs['Normal'])
    n.set('Specular IOR Level', .3)
    return m


def hdri_world(hid, strength=1.0, rot_z=0.0):
    sc = bpy.context.scene
    wd = sc.world or bpy.data.worlds.new('WORLD'); sc.world = wd; wd.use_nodes = True
    nt = wd.node_tree
    for nd in list(nt.nodes):
        if nd.type in ('TEX_SKY', 'TEX_ENVIRONMENT', 'MAPPING', 'TEX_COORD'):
            nt.nodes.remove(nd)
    bg = nt.nodes['Background']
    d = os.path.join(PH, 'hdris', hid); f = [x for x in os.listdir(d) if x.endswith(('.exr', '.hdr'))][0]
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(d, f), check_existing=True)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, rot_z)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    nt.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = strength
    return env.image


def hdri_sun_dir(img):
    """direction (world, before rotation) of the brightest region of an equirect HDRI → (azimuth_rad, elevation_rad)."""
    import numpy as np
    w, h = img.size
    px = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(px)
    a = px.reshape(h, w, 4)[..., :3].sum(-1)
    a = a[::4, ::4]
    y, x = np.unravel_index(np.argmax(a), a.shape)
    u, v = (x * 4 + 2) / w, (y * 4 + 2) / h            # pixels: row 0 = bottom in Blender
    az = (u - .5) * 2 * math.pi                         # Blender equirect: u=.5 → -X? (handled by calibration in caller)
    el = (v - .5) * math.pi
    return az, el

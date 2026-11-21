"""t5kit — shared Blender 4.5 helpers for TASK 05 (detailed terrain & landscape production).

  NB                       tiny node-tree builder (shader + geometry nodes) that finds sockets by name and type
  pbr_group(tex, box)      reusable PBR node group NG_PBR_<tex>[_BOX]: Poly Haven 2K maps → Color / Roughness / Normal / Height
                           (+ anti-tiling second sample, wetness darkening, tint)
  heightfield_group()      NG_T5_HEIGHTFIELD — real 3D terrain mesh from a 32-bit EXR heightfield + mask images
                           (grid → exact pixel-centre sampling → holes for nested LODs → skirts → masks as attributes)
  scatter_group()          NG_T5_SCATTER — mask / slope / altitude driven instancing with camera culling + distance LOD
  img_float / img_rgb      numpy → Blender image saved next to the .blend (relative paths)
Only APIs present in Blender 4.5 LTS are used (also tested in 5.x where noted).
"""
import os, sys, math, json
import numpy as np
import bpy

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import worldkit as wk

ROOT = wk.ROOT
P = wk.P
PH = os.path.abspath(os.path.join(ROOT, '..', '..', '03_assets', 'external', 'polyhaven'))
MATLIB2 = P('11_MATERIALS', 'T5_TERRAIN_MATERIALS_v002.blend')


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple([(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c] + [1.0])


# ====================================================================== node builder
class NB:
    def __init__(self, tree):
        self.t = tree; self.n = tree.nodes; self.l = tree.links

    def node(self, typ, **props):
        nd = self.n.new(typ)
        for k, v in props.items():
            setattr(nd, k, v)
        return nd

    @staticmethod
    def sock(nd, key, out=False, typ=None):
        """socket by index, name or identifier; with typ, the first ENABLED socket of that name+type."""
        coll = nd.outputs if out else nd.inputs
        if isinstance(key, int):
            return coll[key]
        cands = [s for s in coll if (s.name == key or s.identifier == key) and s.enabled]
        if typ:
            c2 = [s for s in cands if s.type == typ]
            cands = c2 or cands
        if not cands:
            cands = [s for s in coll if s.name == key or s.identifier == key]
        if not cands:
            raise KeyError(f'{nd.bl_idname}: no socket {key!r} ({"out" if out else "in"}) — have {[s.name for s in coll]}')
        return cands[0]

    def out(self, nd, key=0, typ=None):
        return self.sock(nd, key, True, typ) if not isinstance(nd, bpy.types.NodeSocket) else nd

    def link(self, a, b):
        """a: output socket or node (first output); b: input socket."""
        if isinstance(a, bpy.types.Node):
            a = a.outputs[0]
        self.l.new(a, b)
        return b

    def set(self, nd, key, val, typ=None):
        s = self.sock(nd, key, False, typ)
        if isinstance(val, bpy.types.NodeSocket) or isinstance(val, bpy.types.Node):
            self.link(val, s)
        else:
            s.default_value = val
        return s

    def math(self, op, a, b=None, c=None, clamp=False):
        nd = self.node('ShaderNodeMath', operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                nd.inputs[i].default_value = v
            else:
                self.link(v, nd.inputs[i])
        return nd.outputs[0]

    def vmath(self, op, a, b=None, scale=None):
        nd = self.node('ShaderNodeVectorMath', operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (tuple, list)):
                nd.inputs[i].default_value = v
            else:
                self.link(v, nd.inputs[i])
        if scale is not None:
            if isinstance(scale, (int, float)):
                nd.inputs['Scale'].default_value = scale
            else:
                self.link(scale, nd.inputs['Scale'])
        return nd.outputs['Value'] if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE') else nd.outputs['Vector']

    def maprange(self, v, a, b, c=0.0, d=1.0, clamp=True, interp='LINEAR'):
        nd = self.node('ShaderNodeMapRange', clamp=clamp, interpolation_type=interp)
        for k, x in (('Value', v), ('From Min', a), ('From Max', b), ('To Min', c), ('To Max', d)):
            s = self.sock(nd, k, typ='VALUE')
            if isinstance(x, (int, float)):
                s.default_value = x
            else:
                self.link(x, s)
        return self.sock(nd, 'Result', True, 'VALUE')

    def mixc(self, fac, a, b, blend='MIX'):
        nd = self.node('ShaderNodeMix', data_type='RGBA', blend_type=blend, clamp_factor=True)
        for k, x in (('Factor', fac), ('A', a), ('B', b)):
            s = self.sock(nd, k, typ='VALUE' if k == 'Factor' else 'RGBA')
            if isinstance(x, (int, float)):
                s.default_value = x
            elif isinstance(x, tuple):
                s.default_value = x
            else:
                self.link(x, s)
        return self.sock(nd, 'Result', True, 'RGBA')

    def mixf(self, fac, a, b):
        nd = self.node('ShaderNodeMix', data_type='FLOAT', clamp_factor=True)
        for k, x in (('Factor', fac), ('A', a), ('B', b)):
            s = self.sock(nd, k, typ='VALUE')
            if isinstance(x, (int, float)):
                s.default_value = x
            else:
                self.link(x, s)
        return self.sock(nd, 'Result', True, 'VALUE')

    def mixv(self, fac, a, b):
        nd = self.node('ShaderNodeMix', data_type='VECTOR', clamp_factor=True)
        self.link(fac, self.sock(nd, 'Factor', typ='VALUE')) if not isinstance(fac, (int, float)) else None
        self.link(a, self.sock(nd, 'A', typ='VECTOR')); self.link(b, self.sock(nd, 'B', typ='VECTOR'))
        return self.sock(nd, 'Result', True, 'VECTOR')

    def noise(self, vec, scale, detail=4.0, rough=.55, dim='3D', out='Fac'):
        nd = self.node('ShaderNodeTexNoise', noise_dimensions=dim)
        if vec is not None:
            self.link(vec, nd.inputs['Vector'])
        nd.inputs['Scale'].default_value = scale; nd.inputs['Detail'].default_value = detail
        nd.inputs['Roughness'].default_value = rough
        return nd.outputs[out]

    def attr(self, name):
        """shader: geometry attribute (float) written by geometry nodes."""
        nd = self.node('ShaderNodeAttribute', attribute_type='GEOMETRY', attribute_name=name)
        return nd.outputs['Fac']

    def group(self, ng):
        nd = self.node('ShaderNodeGroup' if ng.bl_idname == 'ShaderNodeTree' else 'GeometryNodeGroup'); nd.node_tree = ng
        return nd


def new_tree(name, kind='ShaderNodeTree'):
    old = bpy.data.node_groups.get(name)
    if old:
        bpy.data.node_groups.remove(old)
    return bpy.data.node_groups.new(name, kind)


def sock_new(ng, name, io, typ, default=None, mn=None, mx=None):
    s = ng.interface.new_socket(name, in_out=io, socket_type=typ)
    if default is not None:
        s.default_value = default
    if mn is not None:
        s.min_value = mn
    if mx is not None:
        s.max_value = mx
    return s


# ====================================================================== PBR groups (shader)
def maps(tex):
    d = os.path.join(PH, 'textures', tex); out = {}
    for k in ('diff', 'rough', 'nor_gl', 'disp', 'ao'):
        for ext in ('jpg', 'png', 'exr'):
            p = os.path.join(d, f'{tex}_{k}_2k.{ext}')
            if os.path.exists(p):
                out[k] = p
    if 'diff' not in out:
        raise FileNotFoundError(f'Poly Haven texture {tex} missing — run 03_assets/external/polyhaven_fetch.py')
    return out


def load_img(path, noncolor=False):
    im = bpy.data.images.load(path, check_existing=True)
    im.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    return im


def pbr_group(tex, box=False, antitile=False, ao=False):
    """NG_PBR_<tex>[_BOX][_AT][_AO]: in Vector (object metres), Scale (m per tile), Wet, Tint, Normal Strength;
    out Color, Roughness, Normal, Height. _AT = anti-tiling 2nd sample, _AO = ambient-occlusion map multiplied in."""
    name = f'NG_PBR_{tex}' + ('_BOX' if box else '') + ('_AT' if antitile else '') + ('_AO' if ao else '')
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    ng = new_tree(name)
    sock_new(ng, 'Vector', 'INPUT', 'NodeSocketVector')
    sock_new(ng, 'Scale', 'INPUT', 'NodeSocketFloat', 4.0, .01, 1e4)
    sock_new(ng, 'Wet', 'INPUT', 'NodeSocketFloat', 0.0, 0, 1)
    sock_new(ng, 'Tint', 'INPUT', 'NodeSocketColor', (1, 1, 1, 1))
    sock_new(ng, 'Normal Strength', 'INPUT', 'NodeSocketFloat', 1.0, 0, 4)
    for nm, t in (('Color', 'NodeSocketColor'), ('Roughness', 'NodeSocketFloat'), ('Normal', 'NodeSocketVector'), ('Height', 'NodeSocketFloat')):
        sock_new(ng, nm, 'OUTPUT', t)
    b = NB(ng); gi = b.node('NodeGroupInput'); go = b.node('NodeGroupOutput')
    m = maps(tex)
    sc = b.math('DIVIDE', 1.0, b.out(gi, 'Scale'))
    vec = b.vmath('SCALE', b.out(gi, 'Vector'), scale=sc)

    def tx(path, v, noncolor):
        t = b.node('ShaderNodeTexImage', interpolation='Linear')
        t.image = load_img(path, noncolor)
        if box:
            t.projection = 'BOX'; t.projection_blend = .3
        b.link(v, t.inputs['Vector'])
        return t
    col = tx(m['diff'], vec, False).outputs['Color']
    if antitile:     # second, rotated + rescaled sample blended by low-frequency noise → hides tile repetition
        rot = b.node('ShaderNodeVectorRotate', rotation_type='Z_AXIS'); rot.inputs['Angle'].default_value = 1.13
        b.link(b.vmath('SCALE', vec, scale=.613), rot.inputs['Vector'])
        col2 = tx(m['diff'], rot.outputs['Vector'], False).outputs['Color']
        f = b.maprange(b.noise(b.vmath('SCALE', vec, scale=.21), 1.0, 3, .5), .42, .58)
        col = b.mixc(f, col, col2)
    if ao and 'ao' in m:
        col = b.mixc(.6, col, tx(m['ao'], vec, True).outputs['Color'], 'MULTIPLY')
    col = b.mixc(1.0, col, b.out(gi, 'Tint'), 'MULTIPLY')
    wet = b.out(gi, 'Wet')
    col = b.mixc(b.math('MULTIPLY', wet, .55), col, (0, 0, 0, 1))             # wet surfaces are darker
    rough = tx(m['rough'], vec, True).outputs['Color'] if 'rough' in m else 0.8
    rough = b.mixf(wet, rough, .07)                                           # … and glossy
    nmap = b.node('ShaderNodeNormalMap')
    b.link(b.out(gi, 'Normal Strength'), nmap.inputs['Strength'])
    if 'nor_gl' in m:
        b.link(tx(m['nor_gl'], vec, True).outputs['Color'], nmap.inputs['Color'])
    h = tx(m['disp'], vec, True).outputs['Color'] if 'disp' in m else 0.5
    b.link(col, go.inputs['Color']); b.link(rough, go.inputs['Roughness']) if not isinstance(rough, float) else None
    b.link(nmap.outputs['Normal'], go.inputs['Normal'])
    if not isinstance(h, float):
        b.link(b.math('ADD', h, 0.0), go.inputs['Height'])
    return ng


# ====================================================================== images (heightfields / masks)
def img_float(name, arr, path):
    """2D float32 array (row 0 = NORTH) → 32-bit float OpenEXR (single channel stored as RGB 'BW'), path relative."""
    n, m = arr.shape
    im = bpy.data.images.get(name)
    if im:
        bpy.data.images.remove(im)
    im = bpy.data.images.new(name, m, n, alpha=False, float_buffer=True, is_data=True)
    px = np.repeat(np.ascontiguousarray(arr[::-1], np.float32).reshape(-1, 1), 4, 1); px[:, 3] = 1
    im.pixels.foreach_set(px.ravel())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.filepath_raw = path; im.file_format = 'OPEN_EXR'
    sc = bpy.context.scene; s = sc.render.image_settings
    s.file_format = 'OPEN_EXR'; s.color_depth = '32'; s.exr_codec = 'ZIP'; s.color_mode = 'BW'
    im.save_render(path, scene=sc)
    bpy.data.images.remove(im)
    im = bpy.data.images.load(path); im.name = name; im.colorspace_settings.name = 'Non-Color'
    im.alpha_mode = 'NONE'
    return im


def img_rgb(name, arr3, path):
    """(n, m, 3) uint8 (row 0 = NORTH) → 8-bit PNG, Non-Color."""
    n, m, _ = arr3.shape
    from_ = np.concatenate([arr3[::-1].astype(np.float32) / 255.0, np.ones((n, m, 1), np.float32)], -1)
    im = bpy.data.images.get(name)
    if im:
        bpy.data.images.remove(im)
    im = bpy.data.images.new(name, m, n, alpha=False, float_buffer=False, is_data=True)
    im.pixels.foreach_set(from_.ravel())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sc = bpy.context.scene; s = sc.render.image_settings
    s.file_format = 'PNG'; s.color_depth = '8'; s.color_mode = 'RGB'; s.compression = 90
    im.save_render(path, scene=sc)
    bpy.data.images.remove(im)
    im = bpy.data.images.load(path); im.name = name; im.colorspace_settings.name = 'Non-Color'
    return im


# ====================================================================== geometry nodes: heightfield terrain
MASKS = [('MA', ('m_forest', 'm_rock', 'm_snow')), ('MB', ('m_wet', 'm_dry', 'm_pad')),
         ('MC', ('m_grove', 'm_scree', 'm_gravel')), ('MD', ('m_path', 'm_flow', 'm_cliff'))]


def heightfield_group():
    name = 'NG_T5_HEIGHTFIELD'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    ng = new_tree(name, 'GeometryNodeTree')
    sock_new(ng, 'Geometry', 'OUTPUT', 'NodeSocketGeometry')
    sock_new(ng, 'Geometry', 'INPUT', 'NodeSocketGeometry')
    sock_new(ng, 'Height', 'INPUT', 'NodeSocketImage')
    for k, _ in MASKS:
        sock_new(ng, f'Mask {k}', 'INPUT', 'NodeSocketImage')
    sock_new(ng, 'Min X', 'INPUT', 'NodeSocketFloat', -1000.0); sock_new(ng, 'Max X', 'INPUT', 'NodeSocketFloat', 1000.0)
    sock_new(ng, 'Min Y', 'INPUT', 'NodeSocketFloat', -1000.0); sock_new(ng, 'Max Y', 'INPUT', 'NodeSocketFloat', 1000.0)
    sock_new(ng, 'Viewport Resolution', 'INPUT', 'NodeSocketFloat', .25, .02, 1.0)
    sock_new(ng, 'Render Resolution', 'INPUT', 'NodeSocketFloat', 1.0, .02, 1.0)
    sock_new(ng, 'Skirt Depth', 'INPUT', 'NodeSocketFloat', 10.0, 0, 1e4)
    for i in (1, 2):
        sock_new(ng, f'Hole {i} Min', 'INPUT', 'NodeSocketVector', (0, 0, 0)); sock_new(ng, f'Hole {i} Max', 'INPUT', 'NodeSocketVector', (0, 0, 0))
    sock_new(ng, 'Material', 'INPUT', 'NodeSocketMaterial')
    b = NB(ng); gi = b.node('NodeGroupInput'); go = b.node('NodeGroupOutput')
    G = lambda k: b.out(gi, k)
    info = b.node('GeometryNodeImageInfo'); b.link(G('Height'), info.inputs['Image'])
    W, H = b.out(info, 'Width'), b.out(info, 'Height')
    isv = b.node('GeometryNodeIsViewport')
    res = b.node('GeometryNodeSwitch', input_type='FLOAT')
    b.link(isv.outputs[0], b.sock(res, 'Switch')); b.link(G('Render Resolution'), b.sock(res, 'False', typ='VALUE'))
    b.link(G('Viewport Resolution'), b.sock(res, 'True', typ='VALUE'))
    r = b.out(res, 'Output')
    vx = b.math('MAXIMUM', b.math('ROUND', b.math('ADD', b.math('MULTIPLY', b.math('SUBTRACT', W, 1), r), 1)), 2)
    vy = b.math('MAXIMUM', b.math('ROUND', b.math('ADD', b.math('MULTIPLY', b.math('SUBTRACT', H, 1), r), 1)), 2)
    sx = b.math('SUBTRACT', G('Max X'), G('Min X')); sy = b.math('SUBTRACT', G('Max Y'), G('Min Y'))
    grid = b.node('GeometryNodeMeshGrid')
    b.link(sx, grid.inputs['Size X']); b.link(sy, grid.inputs['Size Y']); b.link(vx, grid.inputs['Vertices X']); b.link(vy, grid.inputs['Vertices Y'])
    # uv of every vertex from its position (0..1), then exact pixel-centre sampling: u' = (u·(W−1)+0.5)/W
    pos = b.node('GeometryNodeInputPosition')
    sep = b.node('ShaderNodeSeparateXYZ'); b.link(pos.outputs[0], sep.inputs[0])
    u = b.math('ADD', b.math('DIVIDE', sep.outputs['X'], sx), .5); v = b.math('ADD', b.math('DIVIDE', sep.outputs['Y'], sy), .5)
    up = b.math('DIVIDE', b.math('ADD', b.math('MULTIPLY', u, b.math('SUBTRACT', W, 1)), .5), W)
    vp = b.math('DIVIDE', b.math('ADD', b.math('MULTIPLY', v, b.math('SUBTRACT', H, 1)), .5), H)
    uv = b.node('ShaderNodeCombineXYZ'); b.link(up, uv.inputs['X']); b.link(vp, uv.inputs['Y'])

    def sample(img_sock):
        t = b.node('GeometryNodeImageTexture', interpolation='Linear', extension='EXTEND')
        b.link(img_sock, t.inputs['Image']); b.link(uv.outputs[0], t.inputs['Vector'])
        return t
    hz = sample(G('Height'))
    zsep = b.node('ShaderNodeSeparateColor'); b.link(hz.outputs['Color'], zsep.inputs['Color'])
    cx = b.math('MULTIPLY', b.math('ADD', G('Min X'), G('Max X')), .5); cy = b.math('MULTIPLY', b.math('ADD', G('Min Y'), G('Max Y')), .5)
    off = b.node('ShaderNodeCombineXYZ'); b.link(cx, off.inputs['X']); b.link(cy, off.inputs['Y']); b.link(zsep.outputs[0], off.inputs['Z'])
    sp = b.node('GeometryNodeSetPosition'); b.link(grid.outputs['Mesh'], sp.inputs['Geometry']); b.link(off.outputs[0], sp.inputs['Offset'])
    geo = sp.outputs['Geometry']
    # masks → named float attributes (shader + scatter read them)
    for k, names in MASKS:
        t = sample(G(f'Mask {k}'))
        cs = b.node('ShaderNodeSeparateColor'); b.link(t.outputs['Color'], cs.inputs['Color'])
        for i, an in enumerate(names):
            st = b.node('GeometryNodeStoreNamedAttribute', data_type='FLOAT', domain='POINT')
            b.link(geo, st.inputs['Geometry']); st.inputs['Name'].default_value = an
            b.link(cs.outputs[i], b.sock(st, 'Value', typ='VALUE'))
            geo = st.outputs['Geometry']
    # holes (finer nested LODs live there): delete faces whose centre is inside a hole rectangle
    pos2 = b.node('GeometryNodeInputPosition')
    sels = []
    for i in (1, 2):                       # hole vectors: (x, y, ±1e7) — Z range is always "everything"
        mn, mx = G(f'Hole {i} Min'), G(f'Hole {i} Max')
        p = pos2.outputs[0]
        ge = b.node('FunctionNodeCompare', data_type='VECTOR', mode='ELEMENT', operation='GREATER_THAN')
        b.link(p, b.sock(ge, 'A', typ='VECTOR')); b.link(mn, b.sock(ge, 'B', typ='VECTOR'))
        le = b.node('FunctionNodeCompare', data_type='VECTOR', mode='ELEMENT', operation='LESS_THAN')
        b.link(p, b.sock(le, 'A', typ='VECTOR')); b.link(mx, b.sock(le, 'B', typ='VECTOR'))
        both = b.node('FunctionNodeBooleanMath', operation='AND'); b.link(ge.outputs[0], both.inputs[0]); b.link(le.outputs[0], both.inputs[1])
        sels.append(both.outputs[0])
    orn = b.node('FunctionNodeBooleanMath', operation='OR'); b.link(sels[0], orn.inputs[0]); b.link(sels[1], orn.inputs[1])
    sel = orn.outputs[0]
    dg = b.node('GeometryNodeDeleteGeometry', domain='FACE', mode='ALL')
    b.link(geo, dg.inputs['Geometry']); b.link(sel, dg.inputs['Selection'])
    geo = dg.outputs['Geometry']
    # skirts: boundary edges extruded straight down (hide LOD cracks)
    en = b.node('GeometryNodeInputMeshEdgeNeighbors')
    eq = b.node('FunctionNodeCompare', data_type='INT', operation='EQUAL')
    b.link(en.outputs['Face Count'], b.sock(eq, 'A', typ='INT')); b.sock(eq, 'B', typ='INT').default_value = 1
    ex = b.node('GeometryNodeExtrudeMesh', mode='EDGES')
    b.link(geo, ex.inputs['Mesh']); b.link(eq.outputs[0], ex.inputs['Selection'])
    dn = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', G('Skirt Depth'), -1), dn.inputs['Z'])
    b.link(dn.outputs[0], ex.inputs['Offset']); ex.inputs['Offset Scale'].default_value = 1.0
    st = b.node('GeometryNodeStoreNamedAttribute', data_type='BOOLEAN', domain='FACE')
    b.link(ex.outputs['Mesh'], st.inputs['Geometry']); st.inputs['Name'].default_value = 'is_skirt'
    b.link(ex.outputs['Side'], b.sock(st, 'Selection')); b.sock(st, 'Value', typ='BOOLEAN').default_value = True
    sm = b.node('GeometryNodeSetShadeSmooth'); b.link(st.outputs['Geometry'], sm.inputs['Geometry'])
    sm_ = b.sock(sm, 'Shade Smooth'); sm_.default_value = True
    mt = b.node('GeometryNodeSetMaterial'); b.link(sm.outputs['Geometry'], mt.inputs['Geometry']); b.link(G('Material'), mt.inputs['Material'])
    b.link(mt.outputs['Geometry'], go.inputs['Geometry'])
    return ng


# ====================================================================== geometry nodes: natural scattering
SCATTER_PARAMS = """Density (/m²) · Viewport Density (fraction) · Mask / Mask Min / Mask Max · Avoid Mask / Avoid Strength ·
Slope Min/Max (deg) · Altitude Min/Max (m) · Cluster Scale (m) / Cluster Amount · Scale Min/Max · Scale By Mask ·
Align To Normal · Random Tilt (deg) · Sink (m, ×scale) · Seed · Cull Distance (m) / Cull Angle (deg) / Keep Near (m) ·
Near / Mid / Far collections + LOD Distance Near→Mid / Mid→Far (m)"""


def scatter_group():
    """NG_T5_SCATTER: instances on a terrain object's EVALUATED surface (its mask attributes drive the density).
    Stable in animation: points never depend on the camera (culling only zeroes density per face, face ids unchanged)."""
    name = 'NG_T5_SCATTER'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    ng = new_tree(name, 'GeometryNodeTree')
    sock_new(ng, 'Geometry', 'OUTPUT', 'NodeSocketGeometry')
    sock_new(ng, 'Geometry', 'INPUT', 'NodeSocketGeometry')
    sock_new(ng, 'Terrain', 'INPUT', 'NodeSocketObject')
    sock_new(ng, 'Near', 'INPUT', 'NodeSocketCollection'); sock_new(ng, 'Mid', 'INPUT', 'NodeSocketCollection')
    sock_new(ng, 'Far', 'INPUT', 'NodeSocketCollection')
    F = lambda n, d, a=None, b=None: sock_new(ng, n, 'INPUT', 'NodeSocketFloat', d, a, b)
    F('Density', .01, 0, 100); F('Viewport Density', .1, 0, 1)
    sock_new(ng, 'Mask', 'INPUT', 'NodeSocketString'); F('Mask Min', .3, 0, 1); F('Mask Max', .7, 0, 1)
    sock_new(ng, 'Avoid Mask', 'INPUT', 'NodeSocketString'); F('Avoid Strength', 1.0, 0, 1)
    sock_new(ng, 'Avoid Mask 2', 'INPUT', 'NodeSocketString'); F('Avoid Strength 2', 1.0, 0, 1)
    F('Slope Min', 0.0, 0, 90); F('Slope Max', 35.0, 0, 90); F('Altitude Min', -1e5); F('Altitude Max', 1e5)
    F('Cluster Scale', 40.0, .01, 1e5); F('Cluster Amount', .5, 0, 1)
    F('Scale Min', .8, 0, 100); F('Scale Max', 1.25, 0, 100); F('Scale By Mask', 0.0, 0, 1)
    F('Align To Normal', 0.0, 0, 1); F('Random Tilt', 0.0, 0, 90); F('Sink', 0.0, -10, 10)
    sock_new(ng, 'Seed', 'INPUT', 'NodeSocketInt', 0)
    F('Cull Distance', 3000.0, 0, 1e6); F('Cull Angle', 60.0, 0, 180); F('Keep Near', 40.0, 0, 1e5)
    F('LOD Near→Mid', 120.0, 0, 1e6); F('LOD Mid→Far', 1200.0, 0, 1e6)
    b = NB(ng); gi = b.node('NodeGroupInput'); go = b.node('NodeGroupOutput')
    G = lambda k: b.out(gi, k)
    oi = b.node('GeometryNodeObjectInfo', transform_space='RELATIVE'); b.link(G('Terrain'), oi.inputs['Object'])
    terr = b.out(oi, 'Geometry')

    def named(name_sock):
        na = b.node('GeometryNodeInputNamedAttribute', data_type='FLOAT'); b.link(name_sock, na.inputs['Name'])
        return b.out(na, 'Attribute', typ='VALUE')
    mask = b.maprange(named(G('Mask')), G('Mask Min'), G('Mask Max'))
    av1 = b.math('SUBTRACT', 1.0, b.math('MULTIPLY', named(G('Avoid Mask')), G('Avoid Strength')), clamp=True)
    av2 = b.math('SUBTRACT', 1.0, b.math('MULTIPLY', named(G('Avoid Mask 2')), G('Avoid Strength 2')), clamp=True)
    nrm = b.node('GeometryNodeInputNormal'); nz = b.node('ShaderNodeSeparateXYZ'); b.link(nrm.outputs[0], nz.inputs[0])
    slope = b.math('DEGREES', b.math('ARCCOSINE', nz.outputs['Z']))
    sl_ok = b.math('MULTIPLY', b.math('GREATER_THAN', slope, G('Slope Min')), b.math('LESS_THAN', slope, G('Slope Max')))
    pos = b.node('GeometryNodeInputPosition'); pz = b.node('ShaderNodeSeparateXYZ'); b.link(pos.outputs[0], pz.inputs[0])
    al_ok = b.math('MULTIPLY', b.math('GREATER_THAN', pz.outputs['Z'], G('Altitude Min')), b.math('LESS_THAN', pz.outputs['Z'], G('Altitude Max')))
    nt = b.node('ShaderNodeTexNoise'); nt.inputs['Detail'].default_value = 3
    b.link(b.math('DIVIDE', 1.0, G('Cluster Scale')), nt.inputs['Scale']); b.link(pos.outputs[0], nt.inputs['Vector'])
    clus = b.mixf(G('Cluster Amount'), 1.0, b.maprange(nt.outputs['Fac'], .45, .62))
    # camera culling (active scene camera): inside a view cone or near, and within the cull distance
    ac = b.node('GeometryNodeInputActiveCamera')
    co = b.node('GeometryNodeObjectInfo', transform_space='ORIGINAL'); b.link(ac.outputs[0], co.inputs['Object'])
    rel = b.vmath('SUBTRACT', pos.outputs[0], b.out(co, 'Location'))
    dist = b.vmath('LENGTH', rel)
    rot = b.node('ShaderNodeVectorRotate', rotation_type='EULER_XYZ'); rot.inputs['Vector'].default_value = (0, 0, -1)
    b.link(b.out(co, 'Rotation'), rot.inputs['Rotation'])
    cosang = b.vmath('DOT_PRODUCT', b.vmath('NORMALIZE', rel), rot.outputs['Vector'])
    in_cone = b.math('GREATER_THAN', cosang, b.math('COSINE', b.math('RADIANS', G('Cull Angle'))))
    keep = b.math('MAXIMUM', in_cone, b.math('LESS_THAN', dist, G('Keep Near')))
    keep = b.math('MULTIPLY', keep, b.math('LESS_THAN', dist, G('Cull Distance')))
    isv = b.node('GeometryNodeIsViewport')
    dsw = b.node('GeometryNodeSwitch', input_type='FLOAT'); b.link(isv.outputs[0], b.sock(dsw, 'Switch'))
    b.link(G('Density'), b.sock(dsw, 'False', typ='VALUE'))
    b.link(b.math('MULTIPLY', G('Density'), G('Viewport Density')), b.sock(dsw, 'True', typ='VALUE'))
    dens = b.out(dsw, 'Output')
    for f in (mask, av1, av2, sl_ok, al_ok, clus, keep):
        dens = b.math('MULTIPLY', dens, f)
    dp = b.node('GeometryNodeDistributePointsOnFaces', distribute_method='RANDOM')
    b.link(terr, dp.inputs['Mesh']); b.link(dens, dp.inputs['Density']); b.link(G('Seed'), dp.inputs['Seed'])
    pts = dp.outputs['Points']
    # per-point attributes captured from the surface: mask value (for scale-by-mask)
    cap = b.node('GeometryNodeCaptureAttribute', domain='POINT')
    try:
        cap.capture_items.new('FLOAT', 'm')
    except Exception:
        cap.data_type = 'FLOAT'
    b.link(pts, cap.inputs['Geometry'])
    b.link(mask, cap.inputs[1])
    pts = cap.outputs['Geometry']; mval = cap.outputs[1]
    # rotation: random yaw (+ tilt), optionally aligned to the surface normal
    yaw = b.node('FunctionNodeRandomValue', data_type='FLOAT'); b.sock(yaw, 'Max', typ='VALUE').default_value = 6.2832
    b.link(G('Seed'), b.sock(yaw, 'Seed', typ='INT'))
    tilt = b.node('FunctionNodeRandomValue', data_type='FLOAT_VECTOR')
    tr = b.math('RADIANS', G('Random Tilt'))
    tmin = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', tr, -1), tmin.inputs['X']); b.link(b.math('MULTIPLY', tr, -1), tmin.inputs['Y'])
    tmax = b.node('ShaderNodeCombineXYZ'); b.link(tr, tmax.inputs['X']); b.link(tr, tmax.inputs['Y'])
    b.link(tmin.outputs[0], b.sock(tilt, 'Min', typ='VECTOR')); b.link(tmax.outputs[0], b.sock(tilt, 'Max', typ='VECTOR'))
    eul = b.node('ShaderNodeCombineXYZ')
    tsep = b.node('ShaderNodeSeparateXYZ'); b.link(b.out(tilt, 'Value', typ='VECTOR'), tsep.inputs[0])
    b.link(tsep.outputs['X'], eul.inputs['X']); b.link(tsep.outputs['Y'], eul.inputs['Y']); b.link(b.out(yaw, 'Value', typ='VALUE'), eul.inputs['Z'])
    # align: mix the instance up-vector with the surface normal
    up = b.mixv(G('Align To Normal'), (0, 0, 1) and b.node('ShaderNodeCombineXYZ').outputs[0], dp.outputs['Normal'])
    try:
        al = b.node('FunctionNodeAlignRotationToVector', axis='Z')
        b.link(eul.outputs[0], b.sock(al, 'Rotation')); b.link(up, b.sock(al, 'Vector'))
        rot_out = b.out(al, 'Rotation')
    except Exception:
        al = b.node('FunctionNodeAlignEulerToVector', axis='Z')
        b.link(eul.outputs[0], al.inputs['Rotation']); b.link(up, al.inputs['Vector'])
        rot_out = al.outputs['Rotation']
    sc = b.node('FunctionNodeRandomValue', data_type='FLOAT'); b.link(G('Scale Min'), b.sock(sc, 'Min', typ='VALUE'))
    b.link(G('Scale Max'), b.sock(sc, 'Max', typ='VALUE')); b.link(b.math('ADD', G('Seed'), 7), b.sock(sc, 'Seed', typ='INT'))
    scale = b.math('MULTIPLY', b.out(sc, 'Value', typ='VALUE'), b.mixf(G('Scale By Mask'), 1.0, b.math('ADD', .55, b.math('MULTIPLY', mval, .45))))
    # sink into the ground (rocks, logs) proportional to scale
    sp_ = b.node('GeometryNodeSetPosition'); b.link(pts, sp_.inputs['Geometry'])
    so = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', b.math('MULTIPLY', G('Sink'), scale), -1), so.inputs['Z'])
    b.link(so.outputs[0], sp_.inputs['Offset'])
    pts = sp_.outputs['Geometry']
    # distance LOD split (camera distance) → near / mid / far collections
    pos3 = b.node('GeometryNodeInputPosition')
    d3 = b.vmath('LENGTH', b.vmath('SUBTRACT', pos3.outputs[0], b.out(co, 'Location')))
    joins = b.node('GeometryNodeJoinGeometry')
    bands = (('Near', None, G('LOD Near→Mid')), ('Mid', G('LOD Near→Mid'), G('LOD Mid→Far')), ('Far', G('LOD Mid→Far'), None))
    for k, lo, hi in bands:
        selv = 1.0
        if lo is not None:
            selv = b.math('MULTIPLY', selv, b.math('GREATER_THAN', d3, lo)) if not isinstance(selv, float) else b.math('GREATER_THAN', d3, lo)
        if hi is not None:
            t = b.math('LESS_THAN', d3, hi)
            selv = t if isinstance(selv, float) else b.math('MULTIPLY', selv, t)
        ci = b.node('GeometryNodeCollectionInfo', transform_space='ORIGINAL'); b.link(G(k), ci.inputs['Collection'])
        ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
        ri = b.node('FunctionNodeRandomValue', data_type='INT'); b.sock(ri, 'Min', typ='INT').default_value = 0
        b.sock(ri, 'Max', typ='INT').default_value = 999; b.link(b.math('ADD', G('Seed'), 3), b.sock(ri, 'Seed', typ='INT'))
        ip = b.node('GeometryNodeInstanceOnPoints')
        b.link(pts, ip.inputs['Points']); b.link(ci.outputs[0], ip.inputs['Instance'])
        b.link(selv, ip.inputs['Selection']); ip.inputs['Pick Instance'].default_value = True
        b.link(b.out(ri, 'Value', typ='INT'), ip.inputs['Instance Index'])
        b.link(rot_out, ip.inputs['Rotation']); b.link(scale, ip.inputs['Scale'])
        b.link(ip.outputs[0], joins.inputs[0])
    b.link(joins.outputs[0], go.inputs['Geometry'])
    return ng


def set_mod(md, **kw):
    """set geometry-nodes modifier inputs by socket NAME."""
    ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
    for k, v in kw.items():
        md[ids[k]] = v
    return md

"""worldkit — shared Blender helpers for TASK 04 (3D world blockout).

Written for Blender 4.5 LTS (tested with bpy 4.5.16; also opens in 5.x). Only bpy + numpy + mathutils are used, so every
build script runs inside a normal Blender 4.5 install:
    blender -b -P 02_world/3d_world/scripts/w4_build_world.py
"""
import os, sys, json, shutil, datetime, math
import numpy as np
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))                     # 02_world/3d_world
P = lambda *a: os.path.join(ROOT, *a)
MATLIB = P('11_MATERIALS', 'WORLD_materials_v001.blend')
BACKUPS = P('13_BACKUPS')
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


# ---------------------------------------------------------------- file handling
def new_file():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for s in bpy.data.scenes:
        s.unit_settings.system = 'METRIC'


def backup(path):
    """Copy an existing .blend to 13_BACKUPS before it is overwritten (Director rule: backups before major changes)."""
    if os.path.exists(path):
        os.makedirs(BACKUPS, exist_ok=True)
        stem = os.path.splitext(os.path.basename(path))[0]
        dst = os.path.join(BACKUPS, f'{stem}__backup_{STAMP}.blend')
        shutil.copy2(path, dst)
        print('BACKUP', dst, flush=True)


def save(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    backup(path)
    bpy.context.preferences.filepaths.save_version = 0          # no .blend1 duplicates (13_BACKUPS holds the backups)
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=True)
    print('SAVED', path, os.path.getsize(path) // 1024, 'KB', flush=True)


def coll(name, parent=None, color=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    par = parent if parent is not None else bpy.context.scene.collection
    if c.name not in par.children:
        par.children.link(c)
    if color:
        c.color_tag = color
    return c


def link_obj(o, c):
    if o.name not in c.objects:
        c.objects.link(o)
    return o


# ---------------------------------------------------------------- materials (linked from the library file)
def link_materials(names=None, lib=MATLIB):
    with bpy.data.libraries.load(lib, link=True, relative=True) as (src, dst):
        dst.materials = [n for n in src.materials if names is None or n in names]
    return {m.name: m for m in dst.materials if m is not None}


def link_collections(lib, names=None):
    with bpy.data.libraries.load(lib, link=True, relative=True) as (src, dst):
        dst.collections = [n for n in src.collections if names is None or n in names]
    return {c.name: c for c in dst.collections if c is not None}


# ---------------------------------------------------------------- mesh building (numpy, fast)
def mesh_from_arrays(name, verts, faces, coll_=None, mat=None):
    """verts (n,3) float, faces (m,k) int (quads or tris, uniform k)."""
    me = bpy.data.meshes.new(name)
    verts = np.ascontiguousarray(verts, np.float32); faces = np.ascontiguousarray(faces, np.int32)
    k = faces.shape[1]
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', np.arange(0, faces.size, k, dtype=np.int32))
    me.update(calc_edges=True)
    me.validate(verbose=False)
    o = bpy.data.objects.new(name, me)
    if coll_ is not None:
        coll_.objects.link(o)
    if mat is not None:
        me.materials.append(mat)
    return o


def grid_faces(nr, nc):
    a = np.arange(nr * nc).reshape(nr, nc)
    return np.stack([a[1:, :-1], a[1:, 1:], a[:-1, 1:], a[:-1, :-1]], -1)      # CCW seen from +Z (row 0 = north)


def subset(verts, faces, extra=None):
    """Keep only vertices used by `faces`; returns (verts, faces, kept_index)."""
    used = np.unique(faces)
    remap = np.full(len(verts), -1, np.int64); remap[used] = np.arange(len(used))
    return verts[used], remap[faces], used


def set_color_attr(o, name, rgba, kind='FLOAT_COLOR'):
    """kind='BYTE_COLOR' stores 4 bytes/vertex (values written/read through the linear 'color' accessor → round-trips)."""
    me = o.data
    a = me.color_attributes.get(name) or me.color_attributes.new(name, kind, 'POINT')
    rgba = np.ascontiguousarray(rgba, np.float32)
    if rgba.shape[1] == 3:
        rgba = np.concatenate([rgba, np.ones((len(rgba), 1), np.float32)], 1)
    a.data.foreach_set('color', rgba.ravel())
    return a


def display_color(o, hexcol):
    """Flat colour attribute used by the Solid viewport / Workbench ('Attribute' colour) — shaders keep their own inputs."""
    c = [int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    me = o.data
    if not hasattr(me, 'color_attributes'):
        return
    a = me.color_attributes.get('display_col') or me.color_attributes.new('display_col', 'FLOAT_COLOR', 'POINT')
    a.data.foreach_set('color', np.tile(np.array(c + [1.0], np.float32), len(me.vertices)))
    me.color_attributes.active_color = a
    try:
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
    except Exception:
        pass


def set_float_attr(o, name, vals, domain='POINT'):
    me = o.data
    a = me.attributes.get(name) or me.attributes.new(name, 'FLOAT', domain)
    a.data.foreach_set('value', np.ascontiguousarray(vals, np.float32).ravel())


def smooth_with_normals(o, normals):
    """Shade smooth + custom normals from the GLOBAL heightfield → no seams between neighbouring terrain pieces."""
    me = o.data
    me.shade_smooth()
    try:
        me.normals_split_custom_set_from_vertices([tuple(n) for n in normals])
    except Exception as e:                                     # API safety for future versions
        print('custom normals skipped:', e)


def heightfield_normals(Z, dx, dy):
    gy, gx = np.gradient(Z, dy, dx)                           # rows = -Y direction (row 0 north)
    n = np.stack([-gx, gy, np.ones_like(Z)], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def ribbon(name, pts, widths, coll_=None, mat=None, lift=0.0):
    """Flat strip following a polyline (rivers, paths). pts (n,3), widths (n,)."""
    pts = np.asarray(pts, float)
    t = np.gradient(pts[:, :2], axis=0); t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-12)
    nrm = np.stack([-t[:, 1], t[:, 0]], 1) * (np.asarray(widths)[:, None] / 2)
    L = np.column_stack([pts[:, :2] + nrm, pts[:, 2] + lift]); R = np.column_stack([pts[:, :2] - nrm, pts[:, 2] + lift])
    v = np.empty((len(pts) * 2, 3)); v[0::2] = L; v[1::2] = R
    i = np.arange(len(pts) - 1) * 2
    f = np.stack([i, i + 1, i + 3, i + 2], 1)
    o = mesh_from_arrays(name, v, f, coll_, mat)
    o.data.shade_smooth()
    return o


def add_props(o, **kw):
    for k, v in kw.items():
        o[k] = v
    return o


# ---------------------------------------------------------------- primitives for markers / proxies
def cone(name, r, h, n=8, coll_=None, mat=None, r_top=0.0, z0=0.0):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    bot = np.column_stack([np.cos(a) * r, np.sin(a) * r, np.full(n, z0)])
    if r_top > 0:
        top = np.column_stack([np.cos(a) * r_top, np.sin(a) * r_top, np.full(n, z0 + h)])
        v = np.vstack([bot, top])
        f = [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
        o = mesh_from_arrays(name, v, np.array(f), coll_, mat)
        _cap(o, list(range(n))[::-1]); _cap(o, list(range(n, 2 * n)))
    else:
        v = np.vstack([bot, [[0, 0, z0 + h]]])
        f = [[i, (i + 1) % n, n] for i in range(n)]
        o = mesh_from_arrays(name, v, np.array(f), coll_, mat)
        _cap(o, list(range(n))[::-1])
    return o


def _cap(o, idx):
    me = o.data
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    try:
        bm.faces.new([bm.verts[i] for i in idx])
    except ValueError:
        pass
    bm.to_mesh(me); bm.free()


def blob(name, r, coll_=None, mat=None, squash=1.0, subdiv=2, seed=0, rough=.18):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    rng = np.random.default_rng(seed)
    for v in bm.verts:
        v.co *= 1 + rng.uniform(-rough, rough)
        v.co.z *= squash
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    if coll_ is not None:
        coll_.objects.link(o)
    if mat is not None:
        me.materials.append(mat)
    me.shade_smooth()
    return o


def box(name, size, loc=(0, 0, 0), coll_=None, mat=None):
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc
    if coll_ is not None:
        coll_.objects.link(o)
    if mat is not None:
        me.materials.append(mat)
    return o


def ring_curve_mesh(name, radius, z, n=96, width=1.0, coll_=None, mat=None, center=(0, 0)):
    a = np.linspace(0, 2 * np.pi, n + 1)
    pts = np.column_stack([center[0] + np.cos(a) * radius, center[1] + np.sin(a) * radius, np.full(n + 1, z)])
    return ribbon(name, pts, np.full(n + 1, width), coll_, mat)


def rect_curve_mesh(name, x0, x1, y0, y1, z, width, coll_=None, mat=None):
    pts = np.array([[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z], [x0, y0, z]], float)
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        segs.append(np.linspace(a, b, 8, endpoint=False))
    seg = np.vstack(segs + [pts[-1:]])
    return ribbon(name, seg, np.full(len(seg), width), coll_, mat)


def text(name, body, loc, size, coll_=None, mat=None, rot=(0, 0, 0), align='CENTER', extrude=0.0):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size; cu.align_x = align; cu.extrude = extrude
    o = bpy.data.objects.new(name, cu); o.location = loc; o.rotation_euler = rot
    if coll_ is not None:
        coll_.objects.link(o)
    if mat is not None:
        cu.materials.append(mat)
    return o


# ---------------------------------------------------------------- cameras / render
def camera(name, loc, target, lens=35, coll_=None, clip=(1, 1e6), ortho=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_start, cd.clip_end = clip
    if ortho:
        cd.type = 'ORTHO'; cd.ortho_scale = ortho
    o = bpy.data.objects.new(name, cd); o.location = loc
    d = Vector(target) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if coll_ is not None:
        coll_.objects.link(o)
    return o


def sun(name, elev_deg, azim_deg, strength, coll_=None, angle_deg=1.0, color=(1, .96, .9)):
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy = strength; ld.angle = math.radians(angle_deg); ld.color = color
    o = bpy.data.objects.new(name, ld)
    # light points along -Z; rotate so it comes FROM azimuth (0 = north, clockwise) at elevation
    el, az = math.radians(elev_deg), math.radians(azim_deg)
    d = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), -math.sin(el)))
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if coll_ is not None:
        coll_.objects.link(o)
    return o


def gradient_world(name, horizon='#A9C1DA', zenith='#2E5584', strength=1.0):
    w = bpy.data.worlds.get(name) or bpy.data.worlds.new(name)
    w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sp.inputs[0])
    cr = nt.nodes.new('ShaderNodeValToRGB')
    hx = lambda h: tuple((lambda x: x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4)(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1,)
    cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = hx(horizon)
    cr.color_ramp.elements[1].position = .55; cr.color_ramp.elements[1].color = hx(zenith)
    nt.links.new(sp.outputs['Z'], cr.inputs['Fac'])
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = strength
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    return w


def sky_world(name, elev_deg, azim_deg, strength=.35, altitude=0.0, air=1.0, dust=1.0):
    w = bpy.data.worlds.get(name) or bpy.data.worlds.new(name)
    w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    sk = nt.nodes.new('ShaderNodeTexSky')
    try:
        sk.sky_type = 'NISHITA'
        sk.sun_elevation = math.radians(elev_deg); sk.sun_rotation = math.radians(-azim_deg + 90)
        sk.altitude = altitude; sk.air_density = air; sk.dust_density = dust; sk.sun_disc = False
    except Exception as e:
        print('sky fallback', e)
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = strength
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(sk.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    return w


def setup_cycles(scene, res=(1280, 720), samples=32, exposure=0.0, look='AgX - Base Contrast'):
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        pass
    scene.cycles.max_bounces = 4; scene.cycles.transparent_max_bounces = 16
    scene.render.resolution_x, scene.render.resolution_y = res; scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = look
    except Exception:
        pass
    scene.view_settings.exposure = exposure
    scene.render.image_settings.file_format = 'PNG'


def setup_workbench(scene, res=(1280, 720), color='VERTEX'):
    """'Solid viewport' look (same engine Blender uses for the Solid viewport)."""
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x, scene.render.resolution_y = res; scene.render.resolution_percentage = 100
    sh = scene.display.shading
    sh.light = 'STUDIO'; sh.color_type = color
    sh.show_cavity = True; sh.cavity_type = 'WORLD'
    sh.show_shadows = False; sh.show_object_outline = True
    scene.display.render_aa = '8'
    scene.view_settings.view_transform = 'Standard'
    scene.render.image_settings.file_format = 'PNG'


def render(scene, cam, path):
    scene.camera = cam
    scene.render.filepath = path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True, scene=scene.name)
    print('RENDERED', path, flush=True)


def viewport_defaults(scene, clip_end):
    """Optimised viewport settings saved in the file (clip range for km/metre scale; solid shading with colour attribute)."""
    for scr in bpy.data.screens:
        for area in scr.areas:
            if area.type == 'VIEW_3D':
                for sp in area.spaces:
                    if sp.type == 'VIEW_3D':
                        sp.clip_start = clip_end / 1e6; sp.clip_end = clip_end
                        sp.shading.color_type = 'VERTEX'

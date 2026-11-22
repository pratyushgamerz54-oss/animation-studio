"""Realism v3 preview (Director: "jo polished lag raha hai sab real karo") — builds a few assets in memory with the CURRENT code
and renders the same close-ups as the sheets (leaf, trunk foot, plant detail) on real scanned ground (no grid), so they can be
compared with the existing sheet renders before the full re-render.
    T6_LEAF_DIR=<atlas dir> OUT=<dir> SPP=24 BPY45 t6_preview_realism.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, bmesh
from mathutils import Vector
import t6kit as K, t6_species as SP, t6_plants as PL, t6_matlib as ML

OUT = os.environ.get('OUT', '/tmp/t6_prev'); os.makedirs(OUT, exist_ok=True)
SPP = int(os.environ.get('SPP', 24)); LOOK = os.environ.get('LOOK', 'AgX - Base Contrast')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.transparent_max_bounces = 64; sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2
sc.view_settings.view_transform = 'AgX'
try:
    sc.view_settings.look = LOOK
except Exception:
    pass
sc.render.film_transparent = False
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment')
env.image = bpy.data.images.load(os.path.join(K.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr'))
mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord'); mp.inputs['Rotation'].default_value[2] = math.radians(140)
nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
nt.links.new(env.outputs['Color'], nt.nodes['Background'].inputs['Color']); nt.nodes['Background'].inputs['Strength'].default_value = .75
sun = bpy.data.objects.new('SUN', bpy.data.lights.new('SUN', 'SUN')); sc.collection.objects.link(sun)
sun.data.energy = 3.6; sun.data.angle = math.radians(2.5); sun.data.color = (1, .96, .9); sun.rotation_euler = (math.radians(48), 0, math.radians(-38))


def plane(name, size, mat):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2); bm.to_mesh(me); bm.free()
    me.uv_layers.new(name='UVMap'); o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); me.materials.append(mat); return o


forest = plane('G_FOREST', 400, K.mat_ground('MAT_G_FOREST', 'forest_ground_04', 3.0))
soil = plane('G_SOIL', 60, K.mat_ground('MAT_G_SOIL', 'brown_mud', 1.5, tex2='forest_ground_04', mix_scale=.4))
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.clip_start = .01; cam.data.clip_end = 5000


def look(loc, target, lens=50):
    cam.data.lens = lens; cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def show(objs):
    for o in sc.collection.objects:
        if o.type == 'MESH':
            o.hide_render = o not in objs


def render(name, rx=600, ry=600):
    sc.render.resolution_x, sc.render.resolution_y = rx, ry; sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True); print('PREVIEW', name, flush=True)


def bounds(o):
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
    L = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', L)
    C = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('center', C); C = C.reshape(-1, 3)
    oe.to_mesh_clear(); return V, L, C


ALL = {t['name']: t for t in SP.TREES + SP.SHRUBS}; PLS = {p['name']: p for p in PL.PLANTS}
for name in os.environ.get('TREES', 'EF_T02_TEAL_BEECH,AV_T01_PEEPAL').split(','):
    S = ALL[name]; o, st = K.build_tree(S, 0, sc.collection, ML.species_mats(S))
    V, L, C = bounds(o); H = V[:, 2].max()
    leafc = C[L == 1]; sel = leafc[(leafc[:, 2] > .4 * H) & (leafc[:, 2] < .8 * H)]; sel = sel if len(sel) > 20 else leafc
    tgt = sel[np.argmin(sel[:, 1] + np.abs(sel[:, 0]) * .3)]; d = 1.3
    look((tgt[0] + .25 * d, tgt[1] - d, tgt[2] + .15 * d), tuple(tgt), 50); show([o, forest]); render(f'{name}_leaf.png')
    if os.environ.get('BASE', '1') == '1':
        td = float(o.get('t6_trunk_d_m', 1.0)); d = max(2.2, td * 2.4); tg = Vector((0, 0, min(.35 * td + .3, H * .25)))
        look((d * .55, -d, tg.z + d * .3), tg, 35); show([o, forest]); render(f'{name}_base.png')
    o.hide_render = True
for name in os.environ.get('PLANTS', 'AV_G01_MEADOW_GRASS,MK_F03_BLUE_POPPY,AV_F04_MARIGOLD').split(','):
    D = PLS[name]; o, st = PL.build_plant(D, 0, sc.collection)
    V, L, C = bounds(o); mn, mx = V.min(0), V.max(0); Hh = max(mx[2], .03); Wd = max(mx[0] - mn[0], mx[1] - mn[1], .05); size = max(Hh, Wd * .7)
    top = V[V[:, 2] > mx[2] - .25 * Hh]; c = top.mean(0); dd = max(size * .8, .14)
    look((c[0] + dd * .4, c[1] - dd, c[2] + dd * .35), tuple(c), 60); show([o, soil]); render(f'{name}_detail.png', 700, 700)
    o.hide_render = True
print('PREVIEW_DONE')

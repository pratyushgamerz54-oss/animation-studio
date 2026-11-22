"""TASK 06 · impostor textures for LOD3 (far trees > 600 m) — Blender 4.5, Cycles CPU.

    BPY45 t6_render_impostors.py -- <REGION> [asset …]

For every tree / shrub of the hero library: orthographic FRONT (camera on −Y) and SIDE (camera on +X) renders with alpha,
uniform white sky light (no sun → the texture is ≈ albedo × ambient occlusion, so the scene's own sun lights the card),
'Standard' view transform (texture values = colours, not a tone-mapped picture), calm wind, exact metric framing.
Out: 03_assets/vegetation/textures/impostors/<asset>_front.png / _side.png (1024 px tall) + impostors.json (metres of each image edge).
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import t6kit as K
import t6_regions as RG

args = sys.argv[sys.argv.index('--') + 1:]; REG = args[0]; SEL = set(args[1:])
LIBF = os.path.join(os.environ.get('T6_LIB_DIR') or os.path.join(K.VEG, 'library'), f'T6_VEG_{RG.NAMES[REG]}_v001.blend')
OUT = os.path.join(K.VEG, 'textures', 'impostors'); os.makedirs(OUT, exist_ok=True)
MJ = os.path.join(OUT, 'impostors.json'); META = json.load(open(MJ)) if os.path.exists(MJ) else {}
PX = int(os.environ.get('PX', 1024)); SPP = int(os.environ.get('SPP', 16))
bpy.ops.wm.open_mainfile(filepath=LIBF)
bpy.data.objects['T6_WIND_CONTROL']['strength'] = 0.0
INV = json.load(open(LIBF[:-6].replace('_v001', '') + '_inventory.json'))
sc = bpy.data.scenes.new('T6_IMPOSTOR')
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.transparent_max_bounces = 64; sc.cycles.max_bounces = 4
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
sc.render.film_transparent = True; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
w = bpy.data.worlds.new('T6_IMP_WORLD'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
cam = bpy.data.objects.new('T6_IMP_CAM', bpy.data.cameras.new('T6_IMP_CAM')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.clip_start = .1; cam.data.clip_end = 5000
sc.frame_set(1)

for name, v in INV.items():
    if v['kind'] not in ('tree', 'shrub') or (SEL and name not in SEL):
        continue
    o = bpy.data.objects[name]; sc.collection.objects.link(o)
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3); oe.to_mesh_clear()
    z0, z1 = 0.0, float(V[:, 2].max()) * 1.01; META[name] = {}
    for view, axis, rot, loc in (('front', 0, (90, 0, 0), lambda c, zc: (c, -2000, zc)), ('side', 1, (90, 0, 90), lambda c, zc: (2000, c, zc))):
        w0, w1 = float(V[:, axis].min()) * 1.01, float(V[:, axis].max()) * 1.01
        Wd, Hh = w1 - w0, z1 - z0
        ry = PX; rx = max(64, int(round(PX * Wd / Hh)))
        sc.render.resolution_x, sc.render.resolution_y = rx, ry
        cam.data.sensor_fit = 'VERTICAL'; cam.data.ortho_scale = Hh
        sc.render.pixel_aspect_x = sc.render.pixel_aspect_y = 1
        cam.data.ortho_scale = Hh if Wd <= Hh * rx / ry else Wd
        cam.data.sensor_fit = 'VERTICAL' if Wd <= Hh * rx / ry else 'HORIZONTAL'
        cam.rotation_euler = [math.radians(a) for a in rot]; cam.location = loc((w0 + w1) / 2, (z0 + z1) / 2)
        sc.render.filepath = os.path.join(OUT, f'{name}_{view}.png')
        bpy.ops.render.render(write_still=True, scene=sc.name)
        META[name][view] = dict(wmin=round(w0, 3), wmax=round(w1, 3), zmin=z0, zmax=round(z1, 3), px=[rx, ry])
        print('IMPOSTOR', name, view, rx, ry, flush=True)
    sc.collection.objects.unlink(o)
    json.dump(META, open(MJ, 'w'), indent=1)
print('T6_IMPOSTORS_DONE', REG)

"""TASK 06 · wind system test clip: Banj oak + bamboo + kans grass + meadow grass + fern (Ashram library) and the Veil Willow
(Enchanted library, appended), strength ramps 0 → 3 (calm → strong wind) over 4 s. → renders/WIND_TEST.mp4 (Cycles, preview quality)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import t6kit as K
S = os.environ.get('SCR', '/tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(K.VEG, 'library', 'T6_VEG_ASHRAM_VALLEY_v001.blend'))
src = os.path.join(K.VEG, 'library', 'T6_VEG_ENCHANTED_FOREST_v001.blend')
with bpy.data.libraries.load(src, link=False) as (a, b):
    b.collections = ['T6_EF_T05_VEIL_WILLOW']
willow_c = b.collections[0]
sc = bpy.data.scenes.new('T6_WIND_TEST'); ctrl = bpy.data.objects['T6_WIND_CONTROL']; sc.collection.objects.link(ctrl)
wo = willow_c.objects[0]
if wo.modifiers.get('T6_WIND'):      # re-target the appended willow's drivers + modifier to this file's control
    md = wo.modifiers['T6_WIND']; md.node_group = bpy.data.node_groups['NG_T6_WIND']
    ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', None) == 'INPUT'}
    md[ids['Wind Control']] = ctrl
    for fc in wo.animation_data.drivers:
        for v in fc.driver.variables:
            v.targets[0].id = ctrl
place = [('T6_AV_T04_BANJ_OAK', (-14, 18, 0)), ('T6_AV_T06_BAMBOO_CLUMP', (12, 22, 0)), (willow_c.name, (2, 40, 0))]
for i, (cn, loc) in enumerate(place):
    e = bpy.data.objects.new(f'WT_{i}', None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[cn]
    e.location = loc; sc.collection.objects.link(e)
import random; random.seed(3)
for cn, n, r in (('T6_AV_G01_MEADOW_GRASS', 160, 9), ('T6_AV_G02_KANS_GRASS', 10, 9), ('T6_AV_FE01_SWORD_FERN', 8, 7), ('T6_AV_F01_BUTTERCUP', 40, 8)):
    for k in range(n):
        e = bpy.data.objects.new(f'WT_{cn}_{k}', None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[cn]
        e.location = (random.uniform(-r, r), random.uniform(-2, r * 1.6), 0); e.rotation_euler[2] = random.uniform(0, 6.28)
        sc.collection.objects.link(e)
me = bpy.data.meshes.new('G'); me.from_pydata([(-200, -60, 0), (200, -60, 0), (200, 300, 0), (-200, 300, 0)], [], [(0, 1, 2, 3)])
g = bpy.data.objects.new('G', me); me.materials.append(K.mat_simple('MAT_WT_G', '#5A6A34', rough=.95, var_col='#7A7A40', var_scale=.3)); sc.collection.objects.link(g)
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(K.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr'))
nt.links.new(env.outputs['Color'], nt.nodes['Background'].inputs['Color'])
sun = bpy.data.objects.new('SUN', bpy.data.lights.new('SUN', 'SUN')); sc.collection.objects.link(sun); sun.data.energy = 3.5
sun.rotation_euler = (math.radians(50), 0, math.radians(-30))
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 28
cam.location = (0, -16, 3.2); cam.rotation_euler = (math.radians(84), 0, 0)
sc.frame_start, sc.frame_end = 1, 96; sc.render.fps = 24
ctrl['strength'] = 0.0; ctrl.keyframe_insert('["strength"]', frame=1); ctrl['strength'] = 3.0; ctrl.keyframe_insert('["strength"]', frame=72)
ctrl['gust'] = .6
sc.render.engine = 'CYCLES'; sc.cycles.samples = int(os.environ.get('SPP', 8)); sc.cycles.use_denoising = True; sc.cycles.transparent_max_bounces = 32
sc.render.resolution_x, sc.render.resolution_y = 960, 540; sc.view_settings.view_transform = 'AgX'
sc.render.filepath = os.path.join(S, 'wind', 'f_'); sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True, scene=sc.name)
print('WIND_FRAMES_DONE')

"""TASK 06 · wind physics test clip v2 → renders/WIND_TEST_v2.mp4 (+ frames in $SCR/wind2).
Hero trees = separate objects (each feels its own gusts): 3 Banj oaks in a row along the wind, bamboo, Veil Willow (appended).
Meadow = geometry-nodes scatter of grass / kans / buttercup / fern instances driven by NG_T6_WIND_INSTANCES.
Wind: calm 0–1 s → breeze → strong gusty wind (Strength 3 ≈ 12 m/s, gust 0.9) → eases. Camera looks across the wind so the
gust fronts travel left → right through the grass and from tree to tree."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import t6kit as K
S = os.environ.get('SCR', '/tmp'); OUT = os.path.join(S, os.environ.get('WDIR', 'wind2')); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(K.VEG, 'library', 'T6_VEG_ASHRAM_VALLEY_v001.blend'))
with bpy.data.libraries.load(os.path.join(K.VEG, 'library', 'T6_VEG_ENCHANTED_FOREST_v001.blend'), link=False) as (a, b):
    b.objects = ['EF_T05_VEIL_WILLOW']
willow = b.objects[0]
sc = bpy.data.scenes.new('T6_WIND_TEST'); ctrl = bpy.data.objects['T6_WIND_CONTROL']; sc.collection.objects.link(ctrl)
ctrl.rotation_euler = (math.radians(90), 0, math.radians(-90))     # arrow (+Z) → +X: wind blows left → right in camera
ng = K.wind_group()
def retarget(o):
    md = o.modifiers['T6_WIND']; md.node_group = ng
    ids = {it.name: it.identifier for it in ng.interface.items_tree if getattr(it, 'in_out', None) == 'INPUT'}
    md[ids['Wind Control']] = ctrl
    for fc in o.animation_data.drivers:
        for v in fc.driver.variables:
            v.targets[0].id = ctrl
hero = []
for i, x in enumerate((-30, -2, 26)):
    o = bpy.data.objects['AV_T04_BANJ_OAK'].copy(); o.location = (x, 40, 0); o.rotation_euler[2] = i * 2.1; sc.collection.objects.link(o); hero.append(o)
o = bpy.data.objects['AV_T06_BAMBOO_CLUMP'].copy(); o.location = (15, 12, 0); sc.collection.objects.link(o); hero.append(o)
willow.location = (-15, 14, 0); sc.collection.objects.link(willow); retarget(willow); hero.append(willow)
for o in hero:
    if o is not willow:
        retarget(o)
# meadow scatter (geometry nodes) + instance wind
me = bpy.data.meshes.new('MEADOW'); me.from_pydata([(-60, -40, 0), (60, -40, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)])
meadow = bpy.data.objects.new('MEADOW', me); sc.collection.objects.link(meadow)
me.materials.append(K.mat_ground('MAT_WT_GROUND', 'grass_ground', 2.5, tex2='forest_ground_04'))
gn = bpy.data.node_groups.new('NG_WT_MEADOW', 'GeometryNodeTree')
K._sock(gn, 'Geometry', 'INPUT', 'NodeSocketGeometry'); K._sock(gn, 'Geometry', 'OUTPUT', 'NodeSocketGeometry')
g = K._GN(gn); gi = g.N('NodeGroupInput'); go = g.N('NodeGroupOutput')
pieces = []          # far instances → rigid tilt (NG_T6_WIND_INSTANCES) · near instances → realized + per-vertex bending (NG_T6_WIND)
NEAR = dict(xmin=-16.0, xmax=16.0, ymin=-14.0, ymax=8.0)
pos = g.N('GeometryNodeInputPosition').outputs[0]; sep = g.N('ShaderNodeSeparateXYZ'); g.L(pos, sep.inputs[0])
def inside(axis, lo, hi):
    a = g.M('GREATER_THAN', sep.outputs[axis], lo); b_ = g.M('LESS_THAN', sep.outputs[axis], hi); return g.M('MULTIPLY', a, b_)
near_sel = g.M('MULTIPLY', inside('X', NEAR['xmin'], NEAR['xmax']), inside('Y', NEAR['ymin'], NEAR['ymax']))
near_parts = []
#              collection                 dens  h     tilt  fnI  branch  leaf  fn(blade)
for cn, dens, h, sway, fn, bs_, lf, fnb in (('T6_AV_G01_MEADOW_GRASS', 3.2, .35, .07, 1.6, .38, .02, .55),
                                            ('T6_AV_G02_KANS_GRASS', .025, 2.2, .35, .7, .30, .03, .30),
                                            ('T6_AV_F01_BUTTERCUP', .6, .32, .05, 1.8, .30, .015, .60),
                                            ('T6_AV_FE01_SWORD_FERN', .05, .6, .06, 1.2, .25, .02, .45),
                                            ('T6_AV_F03_WILD_DAISY', .5, .15, .03, 2.2, .30, .01, .70)):
    dp = g.N('GeometryNodeDistributePointsOnFaces'); dp.distribute_method = 'POISSON'
    g.L(gi.outputs['Geometry'], dp.inputs['Mesh']); dp.inputs['Density Max'].default_value = dens
    dp.inputs['Distance Min'].default_value = .18 if dens > 1 else .5; dp.inputs['Seed'].default_value = len(pieces) * 7
    ci = g.N('GeometryNodeCollectionInfo'); ci.inputs['Collection'].default_value = bpy.data.collections[cn]
    ci.inputs['Separate Children'].default_value = False; ci.inputs['Reset Children'].default_value = True
    for o in bpy.data.collections[cn].objects:          # raw geometry in the instances (wind is added here, once)
        if o.modifiers.get('T6_WIND'):
            o.modifiers['T6_WIND'].show_render = o.modifiers['T6_WIND'].show_viewport = False
    rr = g.N('FunctionNodeRandomValue', data_type='FLOAT_VECTOR'); rr.inputs['Min'].default_value = (0, 0, 0); rr.inputs['Max'].default_value = (0, 0, 6.28)
    rr.inputs['Seed'].default_value = len(pieces)
    rs = g.N('FunctionNodeRandomValue', data_type='FLOAT'); rs.inputs['Min'].default_value = .75; rs.inputs['Max'].default_value = 1.25
    for near in (False, True):
        sepg = g.N('GeometryNodeSeparateGeometry'); sepg.domain = 'POINT'; g.L(dp.outputs['Points'], sepg.inputs['Geometry'])
        g.L(near_sel, sepg.inputs['Selection'])
        ip = g.N('GeometryNodeInstanceOnPoints'); g.L(sepg.outputs['Selection' if near else 'Inverted'], ip.inputs['Points'])
        g.L(ci.outputs[0], ip.inputs['Instance']); g.L(rr.outputs['Value'], ip.inputs['Rotation']); g.L(rs.outputs[1], ip.inputs['Scale'])
        if near:
            rl = g.N('GeometryNodeRealizeInstances'); g.L(ip.outputs[0], rl.inputs['Geometry'])
            wg = g.N('GeometryNodeGroup'); wg.node_tree = K.wind_group(); g.L(rl.outputs[0], wg.inputs['Geometry'])
            for k_, v_ in (('Trunk Sway (m)', 0.0), ('Branch Sway (m)', bs_), ('Leaf Flutter (m)', lf), ('Natural Freq (Hz)', fnb),
                           ('Damping', .1), ('Gust Size (m)', 9.0), ('Bend Offset (m)', .02), ('Flexibility', 1.0)):
                wg.inputs[k_].default_value = v_
            near_parts.append(wg); pieces.append((wg, cn))
        else:
            wg = g.N('GeometryNodeGroup'); wg.node_tree = K.wind_instances_group(); g.L(ip.outputs[0], wg.inputs['Instances'])
            wg.inputs['Plant Height (m)'].default_value = h; wg.inputs['Sway (m)'].default_value = sway; wg.inputs['Natural Freq (Hz)'].default_value = fn
            wg.inputs['Gust Size (m)'].default_value = 12.0
            pieces.append((wg, cn))
j = g.N('GeometryNodeJoinGeometry'); g.L(gi.outputs['Geometry'], j.inputs[0])
for wg, cn in pieces:
    g.L(wg.outputs[0], j.inputs[0])
g.L(j.outputs[0], go.inputs['Geometry'])
md = meadow.modifiers.new('MEADOW', 'NODES'); md.node_group = gn
for wg, cn in pieces:          # drive the instance-wind nodes from the same control (node-socket drivers on the node group)
    wg.inputs['Wind Control'].default_value = ctrl
    for sock, prop in (('Strength', 'strength'), ('Gust', 'gust'), ('Speed', 'speed')) + ((('Flutter', 'flutter'),) if 'Flutter' in wg.inputs else ()):
        fc = wg.inputs[sock].driver_add('default_value'); dr = fc.driver; dr.type = 'AVERAGE'
        v = dr.variables.new(); v.type = 'SINGLE_PROP'; v.targets[0].id_type = 'OBJECT'; v.targets[0].id = ctrl; v.targets[0].data_path = f'["{prop}"]'
# world, sun, camera
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(K.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr'))
nt.links.new(env.outputs['Color'], nt.nodes['Background'].inputs['Color'])
sun = bpy.data.objects.new('SUN', bpy.data.lights.new('SUN', 'SUN')); sc.collection.objects.link(sun); sun.data.energy = 3.6
sun.rotation_euler = (math.radians(48), 0, math.radians(-35))
cam = bpy.data.objects.new('CAM', bpy.data.cameras.new('CAM')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 24
cam.location = (0, -16, 2.4); cam.rotation_euler = (math.radians(88), 0, 0)
if os.environ.get('CAM') == 'close':                 # low close-up into the meadow (blade bending check)
    cam.location = (0, -13.5, .55); cam.rotation_euler = (math.radians(84), 0, 0); cam.data.lens = 35
FR = int(os.environ.get('FRAMES', 168)); sc.frame_start, sc.frame_end = 1, FR; sc.render.fps = 24
for f, st, gu in ((1, 0.0, .3), (24, 0.0, .3), (60, 1.2, .5), (110, 3.0, .9), (FR, 2.2, .8)):
    ctrl['strength'] = st; ctrl['gust'] = gu; ctrl.keyframe_insert('["strength"]', frame=f); ctrl.keyframe_insert('["gust"]', frame=f)
sc.render.engine = 'CYCLES'; sc.cycles.samples = int(os.environ.get('SPP', 8)); sc.cycles.use_denoising = True
sc.cycles.transparent_max_bounces = 32; sc.cycles.max_bounces = 4
sc.render.resolution_x, sc.render.resolution_y = (960, 540) if not os.environ.get('RES') else tuple(int(v) for v in os.environ['RES'].split('x')); sc.view_settings.view_transform = 'AgX'
sc.render.filepath = os.path.join(OUT, 'f_'); sc.render.image_settings.file_format = 'PNG'
if os.environ.get('SAVE'):
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['SAVE'], compress=True)
sc.frame_start = int(os.environ.get('FSTART', 1))      # resume support (frames already rendered are kept)
bpy.ops.render.render(animation=True, scene=sc.name)
print('WIND_FRAMES_DONE')

"""TASK 06 · cinematic previews of the populated region files (Blender 4.5, Cycles CPU).

    BPY45 t6_render_populated.py -- <REGION|file.blend> [camera …]     env: RES=1280x720 SPP=32 FRAME=120 OUT=<dir>
Renders every camera listed in the scene's t6_preview_cameras (T6 eye-level cameras + the approved TASK 05 shot camera) at the
breeze keyframe (wind strength ≈ 2, frame 120), natural camera look (AgX Base Contrast + gentle S-curve), TASK 05 compositor kept.
Out: 02_world/ecosystem/renders/populated/<file>__<camera>.png   (preview resolution — final 4K on the Director's GPU PC).
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import t6kit as K

args = sys.argv[sys.argv.index('--') + 1:]
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
POP = os.path.join(ROOT, '02_world', 'ecosystem', 'populated')
FILES = {'AV': 'T6_POP_R01_ASHRAM_VALLEY_v001.blend', 'EF': 'T6_POP_R02_ENCHANTED_FOREST_v001.blend', 'MK': 'T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend',
         'DS': 'T6_POP_R04_GOLDEN_DESERT_v001.blend', 'FB': 'T6_POP_R05_FORBIDDEN_LANDS_v001.blend'}
f = args[0] if args[0].endswith('.blend') else os.path.join(POP, FILES[args[0]])
OUT = os.environ.get('OUT') or os.path.join(ROOT, '02_world', 'ecosystem', 'renders', 'populated'); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=f)
sc = bpy.context.scene
rx, ry = (int(v) for v in os.environ.get('RES', '1280x720').split('x'))
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SPP', 32)); sc.cycles.use_denoising = True
sc.cycles.transparent_max_bounces = 64; sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2
sc.render.resolution_x, sc.render.resolution_y = rx, ry; sc.render.resolution_percentage = 100; sc.render.use_motion_blur = False
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.film_transparent = False
K.camera_look(sc)
sc.frame_set(int(os.environ.get('FRAME', 120)))
cams = args[1:] or list(sc.get('t6_preview_cameras', [sc.camera.name]))
for cn in cams:
    if cn not in bpy.data.objects:
        print('NO CAMERA', cn); continue
    sc.camera = bpy.data.objects[cn]
    sc.render.filepath = os.path.join(OUT, f"{os.path.basename(f)[:-6]}__{cn}.png")
    t = time.time(); bpy.ops.render.render(write_still=True)
    print('RENDER', os.path.basename(sc.render.filepath), round(time.time() - t), 's', flush=True)
print('T6_POP_RENDER_DONE', os.path.basename(f))

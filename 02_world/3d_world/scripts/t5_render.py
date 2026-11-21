"""TASK 05 · cinematic environment test renders (Blender 4.5, Cycles CPU).

  blender -b -P t5_render.py -- [CAM_NAME ...] [--res 1280x720] [--samples N] [--out DIR]
Opens 00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend, per camera: sets the aerial-perspective haze (camera props haze_depth_m /
haze_strength), samples, then renders → 12_RENDER/T5/cycles/<CAM>.png and appends timings to 12_RENDER/T5/render_log_t5.json.
Optimisation per shot: scatter systems whose terrain tile is far outside the view are switched off for that render only.
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import worldkit as wk

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
names = []
i = 0
while i < len(argv):
    if argv[i].startswith('--'):
        opt[argv[i][2:]] = argv[i + 1]; i += 2
    else:
        names.append(argv[i]); i += 1
bpy.ops.wm.open_mainfile(filepath=wk.P('00_MASTER_WORLD', opt.get('master', 'T5_LANDSCAPE_master_v002.blend')))
sc = bpy.context.scene
cams = [o for o in sc.objects if o.type == 'CAMERA' and o.name.startswith('CAM_T5_')]
if names:
    cams = [o for o in cams if o.name in names]
outdir = opt.get('out', wk.P('12_RENDER', 'T5', 'cycles'))
os.makedirs(outdir, exist_ok=True)
if 'res' in opt:
    w, h = opt['res'].split('x'); sc.render.resolution_x, sc.render.resolution_y = int(w), int(h)
logp = wk.P('12_RENDER', 'T5', 'render_log_t5.json') if 'out' not in opt else os.path.join(outdir, 'render_log_test.json')
log = json.load(open(logp)) if os.path.exists(logp) else {}
# which scatter groups are relevant to which shot (others are disabled for that render only → less memory / BVH time)
REL = {'CAM_T5_01_MOUNTAIN_WIDE': ('SC_MT_',), 'CAM_T5_03_RIVER_WATERFALL': ('SC_WF_', 'SC_MT_'),
       'CAM_T5_04_SNOWY_PEAKS': ('SC_MT_',), 'CAM_T5_02_FOREST_ESTABLISHING': ('SC_FH_', 'SC_L1_'),
       'CAM_T5_08_FOREST_FLOOR': ('SC_FH_',), 'CAM_T5_06_VALLEY_AERIAL': ('SC_VH_GROVES', 'SC_L0_', 'SC_L1_', 'SC_VH_BOULDERS'),
       'CAM_T5_07_GROUND_LEVEL': ('SC_VH_', 'SC_L0_', 'SC_L1_'),
       'CAM_T5_05_DESERT': ('SC_DH_', 'SC_DN_'), 'CAM_T5_05B_DESERT_MESAS_AERIAL': ('SC_DN_',), 'CAM_T5_09_FORBIDDEN_RIM': ('SC_DH_', 'SC_DN_'), 'CAM_T5_09B_FORBIDDEN_AERIAL': ('SC_DN_',)}
for cam in cams:
    keep = REL.get(cam.name)
    for o in sc.objects:
        if o.name.startswith('SC_'):
            o.hide_render = bool(keep) and not o.name.startswith(keep)
    sc.world.mist_settings.depth = float(cam.get('haze_depth_m', 60000))
    sc.node_tree.nodes['HAZE_STRENGTH'].outputs[0].default_value = float(cam.get('haze_strength', .4))
    sc.cycles.samples = int(opt.get('samples', cam.get('samples', 48)))
    sc.cycles.time_limit = float(opt.get('time_limit', 1500))
    t0 = time.time()
    wk.render(sc, cam, os.path.join(outdir, f'{cam.name}.png'))
    dt = time.time() - t0
    log[cam.name] = dict(seconds=round(dt, 1), samples=sc.cycles.samples, res=[sc.render.resolution_x, sc.render.resolution_y],
                         description=cam.get('description', ''), blender=bpy.app.version_string)
    json.dump(log, open(logp, 'w'), indent=1)
    print('T5_RENDER', cam.name, round(dt, 1), 's', flush=True)
print('T5_RENDER_ALLDONE')

"""t7_flat_views — preview views for flat creatures (butterflies, moths, dragonflies) facing +X with wings in the X-Y plane:
top, 3/4, low side, underside (from below, ground hidden); camera distance from the wingspan.
usage: $BPY45 t7_flat_views.py <in.blend> <out_prefix> [--samples 48]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import numpy as np
from mathutils import Vector
import t7kit as K
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, pre = a[0], a[1]; spp = int(a[a.index('--samples') + 1]) if '--samples' in a else 48
bpy.ops.wm.open_mainfile(filepath=src)
for o in list(bpy.data.objects):
    if o.type in ('CAMERA', 'LIGHT'):
        bpy.data.objects.remove(o)
sc = K.studio(size=(1200, 900), samples=spp)
P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in bpy.data.objects if o.type == 'MESH' and o.name != 'T7_GROUND'])
c = Vector((P.max(0) + P.min(0)) / 2); S = float(np.ptp(P[:, :2], 0).max())
os.makedirs(os.path.dirname(pre) or '.', exist_ok=True)
for nm, d in (('top', (0.0001, 0, 1)), ('34', (0.9, -0.9, 0.8)), ('side', (0.15, -1, 0.25)), ('under', (0.0001, -0.08, -1))):
    if nm == 'under':
        bpy.data.objects['T7_GROUND'].hide_render = True
    dv = Vector(d).normalized(); cam = K.camera('CAM_' + nm, c + dv * S * 1.5, c, lens=50); sc.camera = cam
    sc.render.filepath = f'{pre}_{nm}.png'; bpy.ops.render.render(write_still=True); print('FLATVIEW', nm, flush=True)

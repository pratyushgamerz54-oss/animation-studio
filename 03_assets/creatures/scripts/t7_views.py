"""t7_views — preview views for a STATIC (unrigged) library asset that faces +X: front (from +X), 3/4, side, back, face close-up.
usage: $BPY45 t7_views.py <in.blend> <out_dir> [--samples 48] [--face-frac 0.85]
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import numpy as np
from mathutils import Vector
import t7kit as K
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, out = a[0], a[1]; opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
bpy.ops.wm.open_mainfile(filepath=src)
for o in list(bpy.data.objects):
    if o.type in ('CAMERA', 'LIGHT'):
        bpy.data.objects.remove(o)
sc = K.studio(size=(1280, 1280), samples=opt('--samples', 48), sun=(48, 0, 150))
P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in bpy.data.objects
                    if o.type == 'MESH' and o.name != 'T7_GROUND' and o.visible_get()])
lo, hi = P.min(0), P.max(0); ctr = Vector((lo + hi) / 2); R = float(np.linalg.norm(hi - lo)) / 2
H = hi[2]; head = P[P[:, 2] > opt('--face-frac', 0.85) * H]; hc = Vector(head.mean(0)); hr = float(np.ptp(head[:, :2], 0).max())
os.makedirs(out, exist_ok=True)
for name, az, el, tgt, dist in (('front', 0, 8, ctr, R * 3.2), ('34', 35, 14, ctr, R * 3.2), ('side', 90, 6, ctr, R * 3.2),
                                ('back', 180, 10, ctr, R * 3.2), ('face', 10, 6, hc, hr * 3.6)):
    d = Vector((math.cos(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(el))))
    cam = K.camera('CAM_' + name, tgt + d * dist, tgt, lens=60); sc.camera = cam
    sc.render.filepath = os.path.join(out, name + '.png'); bpy.ops.render.render(write_still=True); print('VIEW', name, flush=True)

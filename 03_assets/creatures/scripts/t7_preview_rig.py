"""t7_preview_rig — studio previews of a rigged creature file: stills (3/4, side, front, back, face) + optional action clip (MP4).
usage: $BPY45 t7_preview_rig.py <file.blend> <out_dir> [--action Walk --frames 1-40 --still-action Stand_Breathing_01 --face-bone RigHead_00]"""
import os, sys, json, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import t7kit as K
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
FN, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
bpy.ops.wm.open_mainfile(filepath=FN)
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
def pts():
    dg = bpy.context.evaluated_depsgraph_get(); P = []
    for o in meshes:
        e = o.evaluated_get(dg); me = e.to_mesh(); P += [(e.matrix_world @ v.co)[:] for v in me.vertices]; e.to_mesh_clear()
    return np.array(P)
st = opt('--still-action', 'Stand_Breathing_01')
if st in bpy.data.actions:
    arm.animation_data.action = bpy.data.actions[st]
bpy.context.scene.frame_set(1)
P = pts(); lo, hi = P.min(0), P.max(0); c = (lo + hi) / 2; ext = hi - lo; L = ext.max()
ax = 0 if ext[0] >= ext[1] else 1
# which end is the head: head bone side
hb = np.array((arm.matrix_world @ arm.pose.bones[opt('--face-bone', 'RigHead_00')].head)[:])
sgn = 1 if hb[ax] > c[ax] else -1
def v(f, l, z):   # forward, lateral(-), up in body axes
    out = np.zeros(3); out[ax] = f * sgn; out[1 - ax] = l * (1 if ax == 0 else -1) * sgn; out[2] = z; return out
os.makedirs(OUT, exist_ok=True)
K.studio(size=(1400, 1000), samples=int(opt('--samples', 64)), ground='#5E5848')
shots = {'34': (v(1.2, -1.5, 0.35), 55, None), 'side': (v(0, -4, 0), None, L * 1.2), 'front': (v(4, 0, 0), None, L * 1.2),
         'back': (v(-4, 0, 0), None, L * 1.2)}
for k, (off, lens, ortho) in ({} if '--clip-only' in a else shots).items():
    K.render(K.camera('CAM_' + k, tuple(c + off * L), tuple(c), lens=lens or 50, ortho=ortho), os.path.join(OUT, f'{k}.png'))
None if '--clip-only' in a else K.render(K.camera('CAM_face', tuple(hb + v(1.0, -1.1, 0.25) * 0.9), tuple(hb + v(0.15, 0, -0.05)), lens=85), os.path.join(OUT, 'face.png'))
act = opt('--action')
if act and act in bpy.data.actions:
    arm.animation_data.action = bpy.data.actions[act]
    f0, f1 = map(int, opt('--frames', '%d-%d' % tuple(map(int, bpy.data.actions[act].frame_range))).split('-'))
    sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 960, 540; sc.cycles.samples = 24
    cam = K.camera('CAM_clip', tuple(c + v(0.2, -2.3, 0.15) * L), tuple(c), lens=50); sc.camera = cam
    d = os.path.join(OUT, 'clip_' + act); os.makedirs(d, exist_ok=True)
    pel = next((b for b in arm.pose.bones if 'Pelvis' in b.name or 'pelvis' in b.name or 'Hips' in b.name), arm.pose.bones[0])
    sc.frame_set(f0); p0 = np.array((arm.matrix_world @ pel.head)[:]); cam0 = np.array(cam.location[:])
    for k_, f in enumerate(range(f0, f1 + 1, int(opt('--step', 1)))):
        sc.frame_set(f)
        pf = np.array((arm.matrix_world @ pel.head)[:]); dd = pf - p0; dd[2] = 0          # tracking camera (dolly with the animal)
        cam.location = tuple(cam0 + dd)
        sc.render.filepath = os.path.join(d, f'{k_:04d}.png'); bpy.ops.render.render(write_still=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(24 // int(opt('--step', 1))), '-start_number', '0', '-i', os.path.join(d, '%04d.png'),
                    '-pix_fmt', 'yuv420p', '-vf', 'scale=960:-2', os.path.join(OUT, f'clip_{act}.mp4')])
print('ALLDONE')

"""t7_ccbase — import a free-licence base model (glTF from Sketchfab), scale it to the real species size, preview it.

usage: $BPY45 t7_ccbase.py <gltf> <out_dir> <target_shoulder_or_height_m> [action] [frame] [--measure withers|top]
Scaling: the armature root is scaled so the evaluated mesh height (ground → withers proxy = top of the body without
antlers/horns, or the full top) matches the field-guide value. Renders 3/4, side, front, face (same studio as t7_build).
"""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7kit as K

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, out, target = a[0], a[1], float(a[2])
action = a[3] if len(a) > 3 and not a[3].startswith('--') else None
frame = int(a[4]) if len(a) > 4 and not a[4].startswith('--') else 1
exclude_mats = [x for x in (a[a.index('--exclude') + 1].split(',') if '--exclude' in a else [])]


def world_pts(objs):
    dg = bpy.context.evaluated_depsgraph_get(); P = []
    for o in objs:
        e = o.evaluated_get(dg); me = e.to_mesh()
        mw = e.matrix_world
        keep = None
        if exclude_mats:
            idx = {i for i, m in enumerate(o.material_slots) if m.material and m.material.name in exclude_mats}
            keep = set()
            for p in me.polygons:
                if p.material_index not in idx:
                    keep.update(p.vertices)
        P += [mw @ v.co for i, v in enumerate(me.vertices) if keep is None or i in keep]
        e.to_mesh_clear()
    return np.array([p[:] for p in P])


def main():
    K.clean()
    bpy.ops.import_scene.gltf(filepath=src)
    arm = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    root = next(o for o in bpy.data.objects if o.parent is None)
    if arm and action and action in bpy.data.actions:
        arm.animation_data_create(); arm.animation_data.action = bpy.data.actions[action]
    bpy.context.scene.frame_set(frame)
    P = world_pts(meshes)
    h = P[:, 2].max() - P[:, 2].min()
    s = target / h
    root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P = world_pts(meshes)
    root.location.z -= P[:, 2].min(); root.location.x -= (P[:, 0].max() + P[:, 0].min()) / 2
    root.location.y -= (P[:, 1].max() + P[:, 1].min()) / 2
    bpy.context.view_layer.update()
    exclude_mats.clear()
    P = world_pts(meshes)
    lo, hi = P.min(0), P.max(0)
    # facing: the longest horizontal axis is the body axis; rotate so the head (higher end) points to +X
    ext = hi - lo
    meas = dict(length=float(max(ext[0], ext[1])), width=float(min(ext[0], ext[1])), height=float(ext[2]), scale=s)
    print('MEAS', json.dumps(meas))
    os.makedirs(out, exist_ok=True)
    K.studio(size=(1400, 1000), samples=48, ground='#5E5848')
    c = (lo + hi) / 2; L = max(ext)
    long_axis_x = ext[0] >= ext[1]
    def cam_at(v):
        v = np.array(v); return v if long_axis_x else np.array([v[1], v[0], v[2]])
    shots = {'34': (cam_at([1.15, -1.55, 0.35]) * L * 1.1, 55, None), 'side': (cam_at([0, -4, 0]) * L, None, L * 1.2),
             'front': (cam_at([4, 0, 0]) * L, None, L * 1.2), 'back': (cam_at([-4, 0, 0]) * L, None, L * 1.2)}
    for k, (off, lens, ortho) in shots.items():
        cam = K.camera('CAM_' + k, tuple(c + off), tuple(c), lens=lens or 50, ortho=ortho)
        K.render(cam, os.path.join(out, f'base_{k}.png'))
    json.dump(meas, open(os.path.join(out, 'base_meas.json'), 'w'), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'base_import.blend'), compress=True)
    print('ALLDONE')


main()

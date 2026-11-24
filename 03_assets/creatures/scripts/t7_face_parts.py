"""t7_face_parts — add real face parts to a furred creature: eyeballs (wet cornea, iris / pupil), nose leather, whiskers.
All parts are placed by ray-casting onto the evaluated (posed) head surface and parented to the head bone, so they follow the rig.

usage: $BPY45 t7_face_parts.py <in.blend> <out.blend> <species_id>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, bmesh
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
import t7kit as K

CFG = {
    # metres, in the head frame: x = forward (toward the nose), y = left, z = up; origin = head-bone tail (snout tip)
    'marmot': dict(head_bone='Bone.004_0', eye_back=0.040, eye_side=0.030, eye_up=0.016, eye_r=0.0062, eye_iris='#140E0A',
                   nose_r=(0.007, 0.010, 0.006), nose_col='#1E1714', whiskers=14, whisker_len=0.055, whisker_col='#161210'),
}


def bvh_world(objs):
    dg = bpy.context.evaluated_depsgraph_get(); V, F = [], []
    for o in objs:
        e = o.evaluated_get(dg); me = e.to_mesh(); off = len(V)
        V += [(e.matrix_world @ v.co) for v in me.vertices]; F += [[off + i for i in p.vertices] for p in me.polygons]; e.to_mesh_clear()
    return BVHTree.FromPolygons(V, F)


def parent_bone(o, arm, bone):
    mw = o.matrix_world.copy(); o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = bone
    bpy.context.view_layer.update(); o.matrix_world = mw


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst, sid = a[0], a[1], a[2]; c = CFG[sid]
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.visible_get()]
    bvh = bvh_world(meshes)
    pb = arm.pose.bones[c['head_bone']]
    tip = arm.matrix_world @ pb.tail; base = arm.matrix_world @ pb.head
    fwd = (tip - base); fwd.z = 0; fwd.normalize()
    left = Vector((0, 0, 1)).cross(fwd).normalized(); up = fwd.cross(left).normalized()
    coll = meshes[0].users_collection[0]
    # nose leather: cast from in front of the snout back toward the head
    hit = bvh.ray_cast(tip + fwd * 0.08 + up * 0.0, -fwd)
    nose_p = hit[0] if hit[0] is not None else tip
    nm = K.mat_simple(f'T7_{sid.upper()}_NOSE', c['nose_col'], rough=0.32, spec=0.45, var=0.2, scale=400, bump=0.4)   # wet, glossy
    bm_ = bmesh.new(); bmesh.ops.create_uvsphere(bm_, u_segments=24, v_segments=12, radius=1.0)
    me = bpy.data.meshes.new(f'{sid}_nose'); bm_.to_mesh(me); bm_.free()
    for p in me.polygons:
        p.use_smooth = True
    no = bpy.data.objects.new(f'{sid}_nose', me); coll.objects.link(no); me.materials.append(nm)
    R = Matrix((fwd, left, up)).transposed()
    no.matrix_world = Matrix.Translation(nose_p - fwd * c['nose_r'][0] * 0.35) @ R.to_4x4() @ Matrix.Diagonal((*c['nose_r'], 1))
    parent_bone(no, arm, c['head_bone'])
    # eyes: cast sideways onto the head from outside, sink the ball ~55 %
    em = K.mat_eye(f'T7_{sid.upper()}_EYE', iris=c['eye_iris'], pupil_r=0.6, sclera='#120D0A', iris_r=0.86)
    for s in (1, -1):
        start = nose_p - fwd * c['eye_back'] + up * c['eye_up'] + left * s * 0.12
        h = bvh.ray_cast(start, -left * s)
        if h[0] is None:
            print('eye ray missed', s); continue
        d = (h[1] - fwd * 0.35 * (h[1].dot(fwd))).normalized()        # look sideways-forward like a rodent
        d = (d + fwd * 0.35).normalized()
        ctr = h[0] - h[1] * c['eye_r'] * 0.45
        eo = K.eyeball(f'{sid}_eye_{"L" if s > 0 else "R"}', ctr, c['eye_r'], d, em, coll)
        parent_bone(eo, arm, c['head_bone'])
    # whiskers: curves from the upper lip, sweeping out-back, drooping slightly
    if c.get('whiskers'):
        cu = bpy.data.curves.new(f'{sid}_whiskers', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.00018; cu.bevel_resolution = 1
        rng = np.random.default_rng(3)
        for s in (1, -1):
            for i in range(c['whiskers']):
                t = i / max(c['whiskers'] - 1, 1)
                root = nose_p - fwd * (0.008 + 0.012 * t) + left * s * (0.008 + 0.004 * t) - up * (0.004 + 0.006 * t)
                dirn = (left * s * 0.8 - fwd * (0.35 + 0.2 * rng.random()) + up * (0.15 - 0.35 * t)).normalized()
                L_ = c['whisker_len'] * (0.6 + 0.4 * rng.random())
                sp = cu.splines.new('POLY'); sp.points.add(3)
                for k in range(4):
                    q = k / 3; p = root + dirn * L_ * q - up * 0.25 * L_ * q * q
                    sp.points[k].co = (*p, 1.0); sp.points[k].radius = 1.0 - 0.85 * q
        wo = bpy.data.objects.new(f'{sid}_whiskers', cu); coll.objects.link(wo)
        cu.materials.append(K.mat_simple(f'T7_{sid.upper()}_WHISKER', c['whisker_col'], rough=0.4, spec=0.35, var=0.1, bump=0.0))
        parent_bone(wo, arm, c['head_bone'])
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('FACEPARTS SAVED', dst)


main()

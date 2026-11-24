"""t7_marmot_pose — Himalayan marmot sentinel pose: forepaws lowered from the face to the chest (base rig has no clips).
usage: $BPY45 t7_marmot_pose.py -- <in.blend> <out.blend> <upper-arm swing deg (55)>"""
import sys, math, bpy
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]; FN, OUT, ang = a[0], a[1], float(a[2])
bpy.ops.wm.open_mainfile(filepath=FN)
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
pb = arm.pose.bones
# forelimbs: upper-arm chains Bone.018 (L) / Bone.023 (R) swing DOWN about the body's lateral axis; forearms fold forward a bit
for up, fore in (('Bone.018_5', 'Bone.019_4'), ('Bone.023_9', 'Bone.024_8')):
    for name, deg in ((up, ang), (fore, -ang * 0.35)):
        b = pb[name]; b.rotation_mode = 'XYZ'
        # rotate about the armature's world X (lateral after the 90° facing turn = world Y) — use the bone-local axis that best matches it
        lat = (arm.matrix_world.inverted().to_3x3() @ Vector((0, 1, 0))).normalized()
        R = (b.bone.matrix_local.to_3x3().inverted() @ lat).normalized()
        b.rotation_quaternion = b.rotation_quaternion
        b.rotation_mode = 'QUATERNION'
        from mathutils import Quaternion
        b.rotation_quaternion = Quaternion(R, math.radians(deg))
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('POSED', ang)

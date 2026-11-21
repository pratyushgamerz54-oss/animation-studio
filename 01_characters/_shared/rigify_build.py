"""Rigify animation rig (v004) for a character, built on top of the production file (v003).

Run:  python3 01_characters/_shared/rigify_build.py <folder>
In :  <folder>/blend/<folder>_v003.blend   (custom game/export rig, face controls, baked textures)
Out:  <folder>/blend/<folder>_v004_rigify.blend  + <folder>/qc/rigify_qc.json + qc/<ID>_rigify_test.png

What it does
1. Builds a Rigify meta-rig whose bones sit exactly on the character's deform skeleton
   (spine / neck / head, shoulders, arms, palms + 15 finger bones per hand, legs + heel, jaw, eye-aim,
   12 x 3 robe/skirt chains when the character has a long skirt).
2. Generates the Rigify rig (IK/FK arms + legs with poles and switches, foot roll, finger curls,
   torso/hips/chest controls, head/neck follow, B-bone deformation).
3. Moves every mesh to the Rigify DEF- bones (vertex groups renamed, bone-parented face kit re-parented),
   copies the face control properties to the Rigify `root`, re-targets all face drivers, drives the jaw control,
   and re-creates the skirt follow constraints on the skirt controls.
4. Tests: rest pose unchanged (vertex deviation), leg IK follows its control, FK arm moves the forearm,
   jaw_open lowers the chin, render of a posed test.
"""
import os, sys, json, math
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import charkit as ck
from build_char import load_cfg

FOLDER = [a for a in sys.argv[1:] if not a.startswith('-')][-1]
CFG, DIR = load_cfg(FOLDER)
CID = CFG['id']
S = CFG.get('height', 1.75) / 1.75
P = lambda *a: os.path.join(DIR, *a)
QC = {}

FING = {'index': 'f_index', 'middle': 'f_middle', 'ring': 'f_ring', 'pinky': 'f_pinky', 'thumb': 'thumb'}


def new_name(n):
    """old deform bone -> Rigify meta bone name (DEF- is added by Rigify)."""
    side = ''
    if n.endswith(('_L', '_R')):
        side, n = '.' + n[-1], n[:-2]
    base = {'pelvis': 'spine', 'spine_01': 'spine.001', 'spine_02': 'spine.002', 'spine_03': 'spine.003',
            'neck': 'spine.004', 'head': 'spine.005', 'clavicle': 'shoulder', 'upperarm': 'upper_arm'}.get(n)
    if base is None:
        for k, v in FING.items():
            if n.startswith(k + '_'):
                base = f'{v}.{n.split("_")[1]}'
        if base is None:
            base = n          # forearm, hand, thigh, shin, foot, toe, jaw, skirt_kk_g
    return base + side


def evaluated_coords(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    out = {}
    for o in objs:
        e = o.evaluated_get(dg); m = e.to_mesh()
        out[o.name] = [o.matrix_world @ v.co for v in m.vertices]
        e.to_mesh_clear()
    return out


def main():
    bpy.ops.wm.open_mainfile(filepath=P('blend', f'{FOLDER}_v003.blend'))
    bpy.ops.preferences.addon_enable(module='rigify')
    old = bpy.data.objects[f'CHAR_{CID}_RIG']
    pr = old.pose.bones['root']
    for k in list(pr.keys()):
        if k.startswith('ik_'):
            pr[k] = 0.0
    ck.reset_pose(old)
    bpy.context.view_layer.update()
    deformed = [o for o in bpy.data.objects if o.type == 'MESH' and any(m.type == 'ARMATURE' and m.object == old for m in o.modifiers)]
    boneparented = [o for o in bpy.data.objects if o.parent == old and o.parent_type == 'BONE']
    rest0 = evaluated_coords(deformed + boneparented)

    # ---------------------------------------------------------------- read the skeleton
    bpy.context.view_layer.objects.active = old
    bpy.ops.object.mode_set(mode='EDIT')
    E = {b.name: (b.head.copy(), b.tail.copy(), b.roll) for b in old.data.edit_bones}
    bpy.ops.object.mode_set(mode='OBJECT')
    deform_old = [b.name for b in old.data.bones if b.use_deform]
    old_x = {b.name: b.matrix_local.col[0].xyz.copy() for b in old.data.bones}

    # ---------------------------------------------------------------- meta-rig (Rigify human template, re-fitted)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.armature_human_metarig_add()
    meta = bpy.context.object
    meta.name = meta.data.name = f'CHAR_{CID}_METARIG'
    ad = meta.data
    skc = ad.collections.new('Skirt'); skc.rigify_ui_row = 18
    bpy.ops.object.mode_set(mode='EDIT')
    eb = ad.edit_bones
    types, used = {}, set()

    def add(name, h, t, parent=None, connect=False, roll=0.0, rtype=None, coll=None):
        b = eb.get(name)
        if b is None:
            b = eb.new(name)
            for c in list(b.collections):
                c.unassign(b)
            ad.collections_all[coll or 'Torso'].assign(b)
        if rtype:
            types[name] = rtype
        b.use_connect = False
        b.head, b.tail, b.roll = Vector(h), Vector(t), roll
        b.parent = eb[parent] if parent else None
        b.use_connect = connect
        used.add(name)
        return b

    def from_old(on, parent=None, connect=False, rtype=None, h=None, t=None):
        hh, tt, rr = E[on]
        return add(new_name(on), h if h is not None else hh, t if t is not None else tt, parent, connect, rr, rtype)

    from_old('pelvis', rtype='spines.basic_spine')
    from_old('spine_01', 'spine', True); from_old('spine_02', 'spine.001', True); from_old('spine_03', 'spine.002', True)
    from_old('neck', 'spine.003', False, 'spines.super_head')
    from_old('head', 'spine.004', True)
    hd_, tl_, rl_ = E['jaw']
    add('jaw', hd_, tl_, 'spine.005', False, rl_, 'basic.super_copy', 'Face (Primary)')
    hh = E['head'][0]
    add('eye_aim', hh + Vector((0, -.6 * S, .09 * S)), hh + Vector((0, -.65 * S, .09 * S)), 'spine.005',
        rtype='basic.super_copy', coll='Face (Primary)')
    for sd, sg in (('L', 1), ('R', -1)):
        x = '.' + sd
        from_old(f'clavicle_{sd}', 'spine.003', False, 'basic.super_copy')
        el = E[f'forearm_{sd}'][0] + Vector((0, .012 * S, 0))          # tiny elbow bend -> clean IK plane
        from_old(f'upperarm_{sd}', 'shoulder' + x, False, 'limbs.arm', t=el)
        from_old(f'forearm_{sd}', 'upper_arm' + x, True, h=el)
        from_old(f'hand_{sd}', 'forearm' + x, True)
        hd = E[f'hand_{sd}'][0]
        for k, fn in enumerate(('index', 'middle', 'ring', 'pinky')):
            root = E[f'{fn}_01_{sd}'][0]
            add(f'palm.0{k + 1}{x}', hd + (root - hd) * .18, root, 'hand' + x, False, E[f'hand_{sd}'][2],
                'limbs.super_palm' if k == 0 else None)
        for fn in ('index', 'middle', 'ring', 'pinky', 'thumb'):
            par = 'palm.01' + x if fn == 'thumb' else f'palm.0{("index", "middle", "ring", "pinky").index(fn) + 1}{x}'
            for k in (1, 2, 3):
                from_old(f'{fn}_0{k}_{sd}', par if k == 1 else f'{FING[fn]}.0{k - 1}{x}', k > 1,
                         'limbs.super_finger' if k == 1 else None)
        kn = E[f'shin_{sd}'][0] + Vector((0, -.012 * S, 0))             # tiny knee bend
        from_old(f'thigh_{sd}', 'spine', False, 'limbs.leg', t=kn)
        from_old(f'shin_{sd}', 'thigh' + x, True, h=kn)
        from_old(f'foot_{sd}', 'shin' + x, True)
        from_old(f'toe_{sd}', 'foot' + x, True)
        an = E[f'foot_{sd}'][0]
        add(f'heel.02{x}', Vector((an.x - sg * .035 * S, an.y + .045 * S, .03 * S)),
            Vector((an.x + sg * .035 * S, an.y + .045 * S, .03 * S)), 'foot' + x)
    skirts = sorted({n.rsplit('_', 1)[0] for n in E if n.startswith('skirt_')})
    for ch in skirts:
        for g in (1, 2, 3):
            hd_, tl_, rl_ = E[f'{ch}_{g}']
            add(f'{ch}_{g}', hd_, tl_, 'spine' if g == 1 else f'{ch}_{g - 1}', g > 1, rl_,
                'limbs.simple_tentacle' if g == 1 else None, 'Skirt')
    for b in list(eb):                       # drop template bones we do not use (face rig, breasts, pelvis, neck 2)
        if b.name not in used:
            eb.remove(b)
    bpy.ops.object.mode_set(mode='POSE')
    for n, t in types.items():
        meta.pose.bones[n].rigify_type = t
    meta.pose.bones['spine.004'].rigify_parameters.connect_chain = False
    meta.pose.bones['jaw'].rigify_parameters.make_deform = True
    meta.pose.bones['eye_aim'].rigify_parameters.make_deform = False   # our neck starts above the chest bone
    for n in ('upper_arm.L', 'upper_arm.R', 'thigh.L', 'thigh.R'):
        meta.pose.bones[n].rigify_parameters.segments = 1
        if n == 'eye_aim':
            pb.rigify_parameters.make_deform = False
    bpy.ops.object.mode_set(mode='OBJECT')

    # ---------------------------------------------------------------- generate
    before = set(bpy.data.objects)
    bpy.ops.object.select_all(action='DESELECT')
    meta.select_set(True); bpy.context.view_layer.objects.active = meta
    bpy.ops.pose.rigify_generate()
    rig = [o for o in bpy.data.objects if o not in before and o.type == 'ARMATURE'][0]
    QC['generated_bones'] = len(rig.data.bones)
    QC['deform_bones'] = sum(1 for b in rig.data.bones if b.use_deform)

    # ---------------------------------------------------------------- move meshes to the Rigify DEF bones
    unmapped = set()
    for o in deformed:
        for vg in o.vertex_groups:
            if vg.name in deform_old:
                nn = 'DEF-' + new_name(vg.name)
                if nn in rig.data.bones:
                    vg.name = nn
                else:
                    unmapped.add(vg.name)
        for m in o.modifiers:
            if m.type == 'ARMATURE' and m.object == old:
                m.object = rig
        mw = o.matrix_world.copy(); o.parent = rig; o.matrix_world = mw
    for o in boneparented:                         # constraints muted so we keep the unconstrained transform
        for c in o.constraints:
            c.mute = True
    bpy.context.view_layer.update()
    for o in boneparented:
        nb = 'DEF-' + new_name(o.parent_bone)
        if nb not in rig.data.bones:
            unmapped.add(o.parent_bone); nb = 'DEF-spine.005'
        mw = o.matrix_world.copy(); basis = o.matrix_basis.copy()
        o.parent = rig; o.parent_type = 'BONE'; o.parent_bone = nb
        o.matrix_parent_inverse.identity(); bpy.context.view_layer.update()
        Pm = o.matrix_world @ o.matrix_basis.inverted()
        o.matrix_parent_inverse = Pm.inverted() @ mw @ basis.inverted()
    for o in boneparented:
        for c in o.constraints:
            c.mute = False
    QC['unmapped_groups'] = sorted(unmapped)

    # ---------------------------------------------------------------- face controls -> Rigify root
    rr = rig.pose.bones['root']
    for k in pr.keys():
        if k.startswith('ik_'):
            continue
        rr[k] = 0.0
        rr.id_properties_ui(k).update(min=0.0, max=1.0)
    nd = 0
    for idb in list(bpy.data.shape_keys) + list(bpy.data.objects):
        ad_ = idb.animation_data
        if not ad_:
            continue
        for fc in ad_.drivers:
            for v in fc.driver.variables:
                for t in v.targets:
                    if t.id == old:
                        t.id = rig; nd += 1
    QC['face_drivers_retargeted'] = nd
    for o in bpy.data.objects:
        for c in o.constraints:
            if getattr(c, 'target', None) == old:
                c.target = rig
                if getattr(c, 'subtarget', '') == 'CTRL_EYES':
                    c.subtarget = 'eye_aim'
    # jaw control driver (same formula as the v003 rig)
    jd = [fc for fc in old.animation_data.drivers if 'jaw' in fc.data_path] if old.animation_data else []
    if jd and 'jaw' in rig.pose.bones:
        src = jd[0].driver
        pj = rig.pose.bones['jaw']; pj.rotation_mode = 'XYZ'
        sgn = 1 if rig.data.bones['jaw'].matrix_local.col[0].x > 0 else -1
        d = pj.driver_add('rotation_euler', 0).driver
        for v in src.variables:
            nv = d.variables.new(); nv.name = v.name
            nv.targets[0].id = rig; nv.targets[0].data_path = v.targets[0].data_path
        d.expression = f'{sgn}*' + src.expression.split('*', 1)[1]
    # skirt follow constraints on the Rigify skirt controls
    ns = 0
    for pb in old.pose.bones:
        if not pb.name.startswith('skirt_') or pb.name not in rig.pose.bones:
            continue
        for c in pb.constraints:
            if c.type != 'TRANSFORM':
                continue
            n = rig.pose.bones[pb.name].constraints.new('TRANSFORM')
            for a in ('name', 'target_space', 'owner_space', 'map_from', 'map_to', 'from_min_x_rot', 'from_max_x_rot',
                      'to_min_x_rot', 'to_max_x_rot', 'map_to_x_from', 'map_to_y_from', 'map_to_z_from', 'mix_mode_rot'):
                setattr(n, a, getattr(c, a))
            n.target = rig; n.subtarget = 'ORG-' + new_name(c.subtarget)
            # Rigify may re-roll bones: flip the mapping where the local X axis changed direction
            src = old_x[c.subtarget].dot(rig.data.bones[n.subtarget].matrix_local.col[0].xyz)
            dst = old_x[pb.name].dot(rig.data.bones[pb.name].matrix_local.col[0].xyz)
            fmin, fmax, tmin, tmax = c.from_min_x_rot, c.from_max_x_rot, c.to_min_x_rot, c.to_max_x_rot
            if src < 0:
                fmin, fmax, tmin, tmax = -fmax, -fmin, tmax, tmin
            if dst < 0:
                tmin, tmax = -tmin, -tmax
            n.from_min_x_rot, n.from_max_x_rot, n.to_min_x_rot, n.to_max_x_rot = fmin, fmax, tmin, tmax
            ns += 1
    QC['skirt_follow_constraints'] = ns
    bpy.data.objects.remove(old)
    rig.name = f'CHAR_{CID}_RIG'; rig.data.name = f'CHAR_{CID}_RIG'
    meta.hide_viewport = meta.hide_render = True
    bpy.context.view_layer.update()

    # ---------------------------------------------------------------- tests
    rest1 = evaluated_coords(deformed + boneparented)
    per = {n: max(((a - b).length for a, b in zip(rest0[n], rest1[n])), default=0) for n in rest0}
    dev = max(per.values(), default=0)
    QC['rest_deviation_worst'] = sorted(((round(v * 1000, 2), n) for n, v in per.items()), reverse=True)[:4]
    QC['rest_pose_max_deviation_mm'] = round(dev * 1000, 3)
    pbs = rig.pose.bones
    # leg IK: Rigify IK_FK = 0 -> IK
    lp = next(b for b in pbs if b.name.startswith('thigh_parent.L'))
    lp['IK_FK'] = 0.0
    fik = pbs['foot_ik.L']
    fik.matrix = Matrix.Translation(Vector((0, -.05, .20 * S))) @ fik.matrix
    rig.update_tag(); bpy.context.view_layer.update()
    ank = rig.matrix_world @ pbs['DEF-shin.L'].tail
    QC['ik_leg_follow_error_mm'] = round((ank - rig.matrix_world @ fik.head).length * 1000, 2)
    QC['ik_leg_ankle_lift_mm'] = round((ank.z - (rig.matrix_world @ rig.data.bones['DEF-shin.L'].tail_local).z) * 1000, 1)
    # FK arm
    ap = next(b for b in pbs if b.name.startswith('upper_arm_parent.L'))
    ap['IK_FK'] = 1.0
    f0 = (rig.matrix_world @ pbs['DEF-forearm.L'].head).copy()
    fk = pbs['upper_arm_fk.L']; fk.rotation_mode = 'XYZ'; fk.rotation_euler = (0, 0, math.radians(-50))
    rig.update_tag(); bpy.context.view_layer.update()
    QC['fk_arm_moves_elbow_mm'] = round(((rig.matrix_world @ pbs['DEF-forearm.L'].head) - f0).length * 1000, 1)
    # jaw
    head = bpy.data.objects[f'CHAR_{CID}_HEAD']
    z0 = min(v.z for v in evaluated_coords([head])[head.name])
    rr['jaw_open'] = 1.0
    if 'expr_happy' in rr:
        rr['expr_happy'] = 1.0
    rig.update_tag(); bpy.context.view_layer.update()
    QC['jaw_open_chin_drop_mm'] = round((z0 - min(v.z for v in evaluated_coords([head])[head.name])) * 1000, 1)
    # render the posed test (IK foot up, FK arm, jaw open, happy)
    St = ck.get_coll('STUDIO_RIGIFY')
    ck.setup_render((900, 1100), 16)
    ck.world_color('#8A9099', .35)
    ck.area_light('KEY', St, (-1.6 * S, -2.6 * S, 2.6 * S), (0, 0, 1.2 * S), 300 * S, 2.0)
    ck.area_light('FILL', St, (2.2 * S, -2.0 * S, 1.4 * S), (0, 0, 1.2 * S), 110 * S, 2.5)
    rig.rotation_euler = (0, 0, math.radians(25)); bpy.context.view_layer.update()
    h = 1.0 * S
    cam = ck.camera('CAM_RIGIFY', St, (0, -12, h), (0, 0, h), ortho=2.4 * S)
    ck.render_to(P('qc', f'{CID}_rigify_test.png'), cam)
    # reset and save
    rig.rotation_euler = (0, 0, 0)
    fik.matrix = Matrix.Translation(Vector((0, .05, -.20 * S))) @ fik.matrix
    fik.location = (0, 0, 0); fk.rotation_euler = (0, 0, 0); ap['IK_FK'] = 0.0
    for k in rr.keys():
        if k not in ('rigify_type',) and isinstance(rr[k], float):
            rr[k] = 0.0
    for o in list(St.objects):
        bpy.data.objects.remove(o)
    bpy.data.collections.remove(St)
    QC['pass'] = (QC['rest_pose_max_deviation_mm'] < 1.0 and QC['ik_leg_follow_error_mm'] < 5 and
                  QC['fk_arm_moves_elbow_mm'] > 20 and QC['jaw_open_chin_drop_mm'] > 3 and not QC['unmapped_groups'])
    bpy.ops.wm.save_as_mainfile(filepath=P('blend', f'{FOLDER}_v004_rigify.blend'))
    json.dump(QC, open(P('qc', 'rigify_qc.json'), 'w'), indent=2)
    rp = P('qc', 'QC_REPORT.md')
    if os.path.exists(rp):
        txt = open(rp).read().split('\n## RIGIFY')[0].rstrip('\n')
        ok = lambda b: '✅ PASS' if b else '❌ FAIL'
        txt += '\n\n' + '\n'.join([
            '## RIGIFY animation rig (v004) — `blend/' + FOLDER + '_v004_rigify.blend`', '',
            'Rigify rig generated from a meta-rig fitted to the deform skeleton: IK/FK arms + legs (poles, IK/FK sliders, '
            'foot roll), torso / hips / chest, neck + head follow, palms + 15 finger bones per hand (finger curl controls), '
            'jaw control, eye-aim control, robe/skirt chain controls (follow the thighs). Face controls (expressions, phonemes, '
            'jaw_open, blink, wide eyes) are custom properties on the Rigify `root` bone.', '',
            '| Check | Result | Detail |', '|---|---|---|',
            f"| Rest pose unchanged after moving to Rigify | {ok(QC['rest_pose_max_deviation_mm'] < 1)} | max {QC['rest_pose_max_deviation_mm']} mm |",
            f"| Leg IK follows foot control | {ok(QC['ik_leg_follow_error_mm'] < 5)} | error {QC['ik_leg_follow_error_mm']} mm, ankle lift {QC['ik_leg_ankle_lift_mm']} mm |",
            f"| FK arm moves the elbow | {ok(QC['fk_arm_moves_elbow_mm'] > 20)} | {QC['fk_arm_moves_elbow_mm']} mm |",
            f"| Jaw control opens the chin | {ok(QC['jaw_open_chin_drop_mm'] > 3)} | {QC['jaw_open_chin_drop_mm']} mm |",
            f"| All weights moved to Rigify DEF bones | {ok(not QC['unmapped_groups'])} | unmapped: {QC['unmapped_groups']} |",
            f"| Face drivers re-targeted / skirt follow constraints | ✅ | {QC['face_drivers_retargeted']} / {QC['skirt_follow_constraints']} |",
            '', f"Bones: {QC['generated_bones']} ({QC['deform_bones']} deform). Posed test render: `qc/{CID}_rigify_test.png`.",
            'GLB/FBX in `export/` use the clean v003 game skeleton (Rigify control bones are Blender-only).'])
        open(rp, 'w').write(txt + '\n')
    print('RIGIFY', json.dumps(QC))


if __name__ == '__main__':
    main()

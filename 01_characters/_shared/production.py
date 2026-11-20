"""Production stages for a character (Stages 5-7, 10): UVs, baked PBR textures, IK/FK rig with poles and
switches, facial control properties + drivers (expressions, phonemes, jaw, blink, eye look), FBX/GLB export
with re-import check, and an automated QC report.

Run:  python3 01_characters/_shared/production.py <folder> [--no-bake] [--res 1024]
In :  <folder>/blend/<folder>_v002.blend
Out:  <folder>/blend/<folder>_v003.blend          (procedural materials, production rig + controls)
      <folder>/textures/*.png, <folder>/uv/*.png   (baked maps, UV layouts)
      <folder>/export/<folder>.glb / .fbx          (baked materials)
      <folder>/qc/QC_REPORT.md + qc.json
"""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy, bmesh
from mathutils import Vector, Matrix
import addon_utils
import charkit as ck
import charbuild as cb
from build_char import load_cfg

ARGS = [a for a in sys.argv[1:]]
FOLDER = [a for a in ARGS if not a.startswith('-') and not a.isdigit()][0]
BAKE = '--no-bake' not in ARGS
RES = int(ARGS[ARGS.index('--res') + 1]) if '--res' in ARGS else 1024
CFG, DIR = load_cfg(FOLDER)
CID = CFG['id']
P = lambda *a: os.path.join(DIR, *a)
for d in ('textures', 'uv', 'export', 'qc'):
    os.makedirs(P(d), exist_ok=True)
QC = {'character': CID, 'started': time.strftime('%Y-%m-%d %H:%M'), 'tests': {}}


def objs():
    return [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(f'CHAR_{CID}_')]


def activate(o):
    bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode != 'OBJECT' else None
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


# ======================================================================= UVs
def uv_unwrap():
    done = []
    for o in objs():
        if o.data.uv_layers:
            continue
        activate(o)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
        bpy.ops.object.mode_set(mode='OBJECT')
        done.append(o.name)
    # UV layout images (drawn from the real UV data)
    from PIL import Image, ImageDraw
    for o in objs():
        if not any(k in o.name for k in ('BODY', 'HEAD', 'SUIT', 'ROBE', 'COAT', 'CHEST', 'UNDERSUIT', 'HAIR')):
            continue
        im = Image.new('RGB', (1024, 1024), (24, 26, 32))
        d = ImageDraw.Draw(im)
        uv = o.data.uv_layers.active.data
        for poly in o.data.polygons:
            pts = [(uv[li].uv.x * 1023, (1 - uv[li].uv.y) * 1023) for li in poly.loop_indices]
            d.polygon(pts, outline=(90, 200, 255))
        im.save(P('uv', f'{o.name}_UV.png'))
    ok = all(o.data.uv_layers for o in objs())
    QC['tests']['uv_present_all_meshes'] = ok
    return done


# ======================================================================= bake
def bake_textures():
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = 1
    s.render.bake.margin = 4
    baked = {}
    for o in objs():
        if not o.data.materials or not o.data.uv_layers:
            continue
        big = any(k in o.name for k in ('BODY', 'HEAD', 'SUIT', 'ROBE', 'COAT', 'HAIR', 'UNDERSUIT', 'CHEST'))
        res = RES if big else RES // 2
        maps = {}
        for kind, bt, cs in (('BaseColor', 'DIFFUSE', 'sRGB'), ('Roughness', 'ROUGHNESS', 'Non-Color'),
                             ('Normal', 'NORMAL', 'Non-Color'), ('Emission', 'EMIT', 'sRGB')):
            img = bpy.data.images.new(f'{o.name}_{kind}', res, res, alpha=False, float_buffer=False)
            img.colorspace_settings.name = cs
            nodes_added = []
            for m in o.data.materials:
                if m is None or m.node_tree is None:
                    continue
                n = m.node_tree.nodes.new('ShaderNodeTexImage')
                n.image = img
                m.node_tree.nodes.active = n
                nodes_added.append((m, n))
            activate(o)
            kw = {'type': bt, 'margin': 4, 'use_clear': True}
            if bt == 'DIFFUSE':
                kw['pass_filter'] = {'COLOR'}
            try:
                bpy.ops.object.bake(**kw)
                path = P('textures', f'{o.name}_{kind}.png')
                img.filepath_raw = path
                img.file_format = 'PNG'
                img.save()
                maps[kind] = img
            except Exception as e:
                print('BAKE FAIL', o.name, kind, e)
            for m, n in nodes_added:
                m.node_tree.nodes.remove(n)
        baked[o.name] = maps
    QC['tests']['textures_baked'] = sum(len(v) for v in baked.values())
    return baked


def baked_material(o, maps):
    m = bpy.data.materials.new(f'{o.name}_BAKED')
    m.use_nodes = True
    N, L = m.node_tree.nodes, m.node_tree.links
    b = N['Principled BSDF']
    def tex(kind):
        n = N.new('ShaderNodeTexImage'); n.image = maps[kind]; return n
    if 'BaseColor' in maps:
        L.new(tex('BaseColor').outputs['Color'], b.inputs['Base Color'])
    if 'Roughness' in maps:
        L.new(tex('Roughness').outputs['Color'], b.inputs['Roughness'])
    if 'Normal' in maps:
        nm = N.new('ShaderNodeNormalMap'); L.new(tex('Normal').outputs['Color'], nm.inputs['Color'])
        L.new(nm.outputs['Normal'], b.inputs['Normal'])
    if 'Emission' in maps:
        L.new(tex('Emission').outputs['Color'], b.inputs['Emission Color'])
        b.inputs['Emission Strength'].default_value = 1.0
    met = 0.0
    for sm in o.data.materials:
        if sm and sm.node_tree and 'BSDF' in sm.node_tree.nodes:
            met = max(met, sm.node_tree.nodes['BSDF'].inputs['Metallic'].default_value)
    b.inputs['Metallic'].default_value = met
    return m


# ======================================================================= rig
def widget(name, kind='circle', r=1.0):
    w = bpy.data.objects.get(name)
    if w:
        return w
    if kind == 'circle':
        verts = [(math.cos(a) * r, 0, math.sin(a) * r) for a in [i * math.pi / 16 for i in range(32)]]
        edges = [(i, (i + 1) % 32) for i in range(32)]
    else:  # cube
        c = [(x, y, z) for x in (-r, r) for y in (-r, r) for z in (-r, r)]
        verts, edges = c, [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts, edges, [])
    w = bpy.data.objects.new(name, me)
    ck.get_coll(f'CONTROLS_{CID}').objects.link(w)
    w.hide_render = True; w.hide_viewport = True
    return w


def upgrade_rig():
    arm = bpy.data.objects[f'CHAR_{CID}_RIG']
    S = CFG.get('height', 1.75) / 1.75
    cb.set_pose(arm, 'T', S)
    ck.reset_pose(arm)
    activate(arm)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones
    for b in eb:
        b.use_deform = b.name != 'root'
    pel = eb['pelvis']
    cog = eb.new('CTRL_COG'); cog.head = pel.head + Vector((0, 0, -.05)); cog.tail = pel.head + Vector((0, .25 * S, -.05))
    cog.parent = eb['root']; cog.use_deform = False
    pel.parent = cog
    new = ['CTRL_COG']
    for sd, sg in (('L', 1), ('R', -1)):
        h = eb[f'hand_{sd}']
        ik = eb.new(f'IK_hand_{sd}'); ik.head, ik.tail, ik.roll = h.head.copy(), h.tail.copy(), h.roll
        ik.parent = eb['root']; ik.use_deform = False
        el = eb[f'forearm_{sd}'].head
        po = eb.new(f'POLE_arm_{sd}'); po.head = el + Vector((0, .40 * S, 0)); po.tail = po.head + Vector((0, .08, 0))
        po.parent = eb['root']; po.use_deform = False
        f = eb[f'foot_{sd}']
        fk = eb.new(f'IK_foot_{sd}'); fk.head, fk.tail, fk.roll = f.head.copy(), f.tail.copy(), f.roll
        fk.parent = eb['root']; fk.use_deform = False
        kn = eb[f'shin_{sd}'].head
        pl = eb.new(f'POLE_leg_{sd}'); pl.head = kn + Vector((0, -.50 * S, 0)); pl.tail = pl.head + Vector((0, -.08, 0))
        pl.parent = eb['root']; pl.use_deform = False
        new += [ik.name, po.name, fk.name, pl.name]
    eyes_h = eb['head']
    ec = eb.new('CTRL_EYES'); ec.head = eyes_h.head + Vector((0, -.6 * S, .09 * S)); ec.tail = ec.head + Vector((0, -.05, 0))
    ec.parent = eb['head']; ec.use_deform = False
    new.append('CTRL_EYES')
    bpy.ops.object.mode_set(mode='POSE')
    # bone collections
    A = arm.data
    cols = {n: (A.collections.get(n) or A.collections.new(n)) for n in ('DEF', 'CTRL', 'IK')}
    for b in A.bones:
        (cols['IK'] if b.name.startswith(('IK_', 'POLE_')) else cols['CTRL'] if b.name.startswith('CTRL') or b.name == 'root'
         else cols['DEF']).assign(b)
    # widgets
    arm.pose.bones['root'].custom_shape = widget('WGT_root', 'circle', 4)
    arm.pose.bones['CTRL_COG'].custom_shape = widget('WGT_cog', 'circle', 2)
    arm.pose.bones['CTRL_EYES'].custom_shape = widget('WGT_eyes', 'circle', 1.2)
    for n in new:
        if n.startswith(('IK_', 'POLE_')):
            arm.pose.bones[n].custom_shape = widget('WGT_cube', 'cube', .5)
    # IK/FK switch properties + constraints
    pb_root = arm.pose.bones['root']
    for sd in ('L', 'R'):
        for limb, chain_bone, end_bone, ikb, pole in (('arm', f'forearm_{sd}', f'hand_{sd}', f'IK_hand_{sd}', f'POLE_arm_{sd}'),
                                                     ('leg', f'shin_{sd}', f'foot_{sd}', f'IK_foot_{sd}', f'POLE_leg_{sd}')):
            prop = f'ik_{limb}_{sd}'
            pb_root[prop] = 0.0
            pb_root.id_properties_ui(prop).update(min=0.0, max=1.0, description=f'0 = FK, 1 = IK ({limb} {sd})')
            c = arm.pose.bones[chain_bone].constraints.new('IK')
            c.name = 'IK'; c.target = arm; c.subtarget = ikb; c.pole_target = arm; c.pole_subtarget = pole
            c.chain_count = 2
            cr = arm.pose.bones[end_bone].constraints.new('COPY_ROTATION')
            cr.name = 'IK_ROT'; cr.target = arm; cr.subtarget = ikb
            for con in (c, cr):
                d = con.driver_add('influence').driver
                d.type = 'AVERAGE'
                v = d.variables.new(); v.name = 'ik'
                v.targets[0].id = arm; v.targets[0].data_path = f'pose.bones["root"]["{prop}"]'
    # pick the pole angle that keeps the rest pose unchanged when IK is on (automatic QC)
    results = {}
    for sd in ('L', 'R'):
        for limb, chain_bone in (('arm', f'forearm_{sd}'), ('leg', f'shin_{sd}')):
            pb_root[f'ik_{limb}_{sd}'] = 1.0
            best = None
            for ang in (0, 90, -90, 180):
                arm.pose.bones[chain_bone].constraints['IK'].pole_angle = math.radians(ang)
                bpy.context.view_layer.update()
                dev = (arm.pose.bones[chain_bone].matrix.translation - arm.data.bones[chain_bone].head_local).length + \
                      (arm.pose.bones[chain_bone].tail - arm.data.bones[chain_bone].tail_local).length + \
                      (arm.pose.bones[chain_bone].matrix.to_quaternion().rotation_difference(
                          arm.data.bones[chain_bone].matrix_local.to_quaternion()).angle) * .1
                if best is None or dev < best[1]:
                    best = (ang, dev)
            arm.pose.bones[chain_bone].constraints['IK'].pole_angle = math.radians(best[0])
            results[f'{limb}_{sd}'] = {'pole_angle': best[0], 'rest_deviation_mm': round(best[1] * 1000, 3)}
            pb_root[f'ik_{limb}_{sd}'] = 0.0
    bpy.context.view_layer.update()
    # IK functional test: move the foot IK target up 20 cm with IK on, the ankle must follow
    pb_root['ik_leg_L'] = 1.0
    arm.pose.bones['IK_foot_L'].location = (0, 0, 0)
    tgt = arm.pose.bones['IK_foot_L']
    tgt.matrix = Matrix.Translation(Vector((0, -.05, .20 * S))) @ tgt.matrix
    bpy.context.view_layer.update()
    ankle = arm.pose.bones['shin_L'].tail
    follow = (ankle - tgt.head).length
    tgt.location = (0, 0, 0); pb_root['ik_leg_L'] = 0.0
    bpy.context.view_layer.update()
    QC['tests']['ik_rest_deviation'] = results
    QC['tests']['ik_follow_error_mm'] = round(follow * 1000, 2)
    bpy.ops.object.mode_set(mode='OBJECT')
    QC['rig'] = {'bones': len(arm.data.bones), 'deform': sum(1 for b in arm.data.bones if b.use_deform),
                 'controls': new + ['root'], 'ik_fk_props': [k for k in pb_root.keys() if k.startswith('ik_')]}
    return arm


def face_controls(arm):
    """Custom properties on the rig drive the face kit (shape keys + lid / eye rotations)."""
    pb = arm.pose.bones['root']
    F = cb.face_of(CID)
    keys = F['mouth'].data.shape_keys.key_blocks
    added = []
    for kb in keys[1:]:
        prop = ('ph_' + kb.name[3:].lower()) if kb.name.startswith('PH_') else f'expr_{kb.name}'
        pb[prop] = 0.0
        pb.id_properties_ui(prop).update(min=0.0, max=1.0)
        added.append(prop)
        d = kb.driver_add('value').driver
        v = d.variables.new(); v.name = 'p'
        v.targets[0].id = arm; v.targets[0].data_path = f'pose.bones["root"]["{prop}"]'
        if kb.name == 'PH_A':
            pb['jaw_open'] = 0.0
            pb.id_properties_ui('jaw_open').update(min=0.0, max=1.0, description='Mouth / jaw open (drives PH_A)')
            w = d.variables.new(); w.name = 'j'
            w.targets[0].id = arm; w.targets[0].data_path = 'pose.bones["root"]["jaw_open"]'
            d.expression = 'max(p, j)'
        else:
            d.expression = 'p'
    for kb in F['brows'].data.shape_keys.key_blocks[1:]:
        prop = f'expr_{kb.name}'
        if prop not in pb.keys():
            pb[prop] = 0.0; pb.id_properties_ui(prop).update(min=0.0, max=1.0); added.append(prop)
        d = kb.driver_add('value').driver
        v = d.variables.new(); v.name = 'p'
        v.targets[0].id = arm; v.targets[0].data_path = f'pose.bones["root"]["{prop}"]'
        d.expression = 'p'
    for sd in ('L', 'R'):
        for prop, desc in ((f'blink_{sd}', 'close eyelids'), (f'lid_wide_{sd}', 'open eyes wide')):
            pb[prop] = 0.0; pb.id_properties_ui(prop).update(min=0.0, max=1.0, description=desc); added.append(prop)
        for part, op, cl, wd in (('lid_up', -24, 6, -48), ('lid_lo', 30, -4, 46)):
            o = F[f'{part}_{sd}']
            d = o.driver_add('rotation_euler', 0).driver
            for nm, path in (('b', f'blink_{sd}'), ('w', f'lid_wide_{sd}')):
                v = d.variables.new(); v.name = nm
                v.targets[0].id = arm; v.targets[0].data_path = f'pose.bones["root"]["{path}"]'
            d.expression = f'radians({op} + b*({cl}-({op})) + w*({wd}-({op})))'
        # eyes aim at CTRL_EYES
        eye = F[f'eye_{sd}']
        c = eye.constraints.new('DAMPED_TRACK')
        c.target = arm; c.subtarget = 'CTRL_EYES'; c.track_axis = 'TRACK_NEGATIVE_Y'
    QC['face_controls'] = sorted(set(added))
    return added


# ======================================================================= export
def export(baked):
    for m in ('io_scene_fbx', 'io_scene_gltf2'):
        addon_utils.enable(m, default_set=True)
    arm = bpy.data.objects[f'CHAR_{CID}_RIG']
    cb.set_pose(arm, 'T', CFG.get('height', 1.75) / 1.75); ck.reset_pose(arm)
    swaps = {}
    for o in objs():
        if o.name in baked and baked[o.name]:
            swaps[o.name] = [m for m in o.data.materials]
            bm_ = baked_material(o, baked[o.name])
            o.data.materials.clear(); o.data.materials.append(bm_)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs() + [arm]:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm
    glb, fbx = P('export', f'{FOLDER}.glb'), P('export', f'{FOLDER}.fbx')
    res = {}
    try:
        bpy.ops.export_scene.gltf(filepath=glb, use_selection=True, export_format='GLB', export_skins=True,
                                  export_morph=True, export_apply=False, export_animations=False)
        res['glb_mb'] = round(os.path.getsize(glb) / 1e6, 2)
    except Exception as e:
        res['glb_error'] = str(e)[:200]
    try:
        bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, add_leaf_bones=False, path_mode='COPY',
                                 embed_textures=True, bake_anim=False, use_mesh_modifiers=True, object_types={'ARMATURE', 'MESH'})
        res['fbx_mb'] = round(os.path.getsize(fbx) / 1e6, 2)
    except Exception as e:
        res['fbx_error'] = str(e)[:200]
    for n, ms in swaps.items():           # restore procedural materials in the .blend
        o = bpy.data.objects[n]; o.data.materials.clear()
        for m in ms:
            o.data.materials.append(m)
    QC['tests']['export'] = res
    return glb, fbx


def reimport_check(glb):
    before = set(bpy.data.objects.keys())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable('io_scene_gltf2', default_set=True)
    try:
        bpy.ops.import_scene.gltf(filepath=glb)
        o = bpy.data.objects
        QC['tests']['glb_reimport'] = {'objects': len(o), 'armatures': sum(1 for x in o if x.type == 'ARMATURE'),
                                       'meshes': sum(1 for x in o if x.type == 'MESH'),
                                       'bones': sum(len(x.data.bones) for x in o if x.type == 'ARMATURE'),
                                       'shape_key_meshes': sum(1 for x in o if x.type == 'MESH' and x.data.shape_keys)}
    except Exception as e:
        QC['tests']['glb_reimport'] = {'error': str(e)[:200]}


# ======================================================================= checks
def static_checks():
    body = bpy.data.objects[f'CHAR_{CID}_BODY']
    QC['tests']['body_unweighted_verts'] = sum(1 for v in body.data.vertices if sum(g.weight for g in v.groups) < .01)
    nm = {}
    for o in objs():
        bm = bmesh.new(); bm.from_mesh(o.data)
        nm[o.name] = sum(1 for e in bm.edges if not e.is_manifold)
        bm.free()
    QC['tests']['non_manifold_edges_base_mesh'] = {k: v for k, v in nm.items() if v}
    QC['tests']['quad_ratio_body'] = round(sum(1 for p in body.data.polygons if len(p.vertices) == 4) / len(body.data.polygons), 3)
    QC['tests']['quad_ratio_head'] = round(sum(1 for p in bpy.data.objects[f'CHAR_{CID}_HEAD'].data.polygons
                                               if len(p.vertices) == 4) / len(bpy.data.objects[f'CHAR_{CID}_HEAD'].data.polygons), 3)
    mouth = bpy.data.objects[f'CHAR_{CID}_MOUTH'].data.shape_keys.key_blocks
    QC['tests']['mouth_shape_keys'] = len(mouth) - 1
    QC['tests']['phonemes_present'] = all(p in mouth for p in cb.PHONEMES)
    QC['meshes'] = len(objs())
    QC['polycount_render_estimate'] = sum(len(o.data.polygons) * 16 for o in objs())


def report():
    m = json.load(open(P('qc', 'measurements.json'))) if os.path.exists(P('qc', 'measurements.json')) else {}
    QC['measurements'] = m
    json.dump(QC, open(P('qc', 'qc.json'), 'w'), indent=2, default=str)
    t = QC['tests']
    ikd = t.get('ik_rest_deviation', {})
    ik_ok = all(v['rest_deviation_mm'] < 5.0 for v in ikd.values()) and t.get('ik_follow_error_mm', 99) < 5
    rows = [
        ('Mesh sanity (no exploded geometry)', not m.get('mesh_sanity_fail'), str(m.get('mesh_sanity_fail', 'n/a'))),
        ('Body fully weighted', t.get('body_unweighted_verts') == 0, f"{t.get('body_unweighted_verts')} unweighted verts"),
        ('UVs on all meshes', t.get('uv_present_all_meshes'), ''),
        ('Textures baked', bool(t.get('textures_baked')), f"{t.get('textures_baked', 0)} maps"),
        ('IK/FK rest pose unchanged + IK follows target', ik_ok, f"follow error {t.get('ik_follow_error_mm')} mm"),
        ('Phoneme shape keys (10)', t.get('phonemes_present'), f"{t.get('mouth_shape_keys')} mouth keys"),
        ('GLB export + re-import', 'error' not in t.get('glb_reimport', {'error': 1}), str(t.get('glb_reimport'))),
        ('FBX export', 'fbx_mb' in t.get('export', {}), str(t.get('export', {}).get('fbx_mb', t.get('export', {}).get('fbx_error')))),
    ]
    raw = os.path.join(DIR, 'design', 'raw')
    vis = [('Turnaround consistency (6 views)', 'turn_front.png'), ('Joint / elbow / knee / finger deformation pose', 'test_deform_test.png'),
           ('Run / jump / land / turn / fight poses', 'test_run.png'), ('Facial expressions', 'expr_00_neutral.png'),
           ('Eye movement + blink', 'expr_10_blink.png'), ('Lip-sync phonemes', 'lipsync_PH_A.png'),
           ('Power activation renders', 'power_normal.png' if CFG.get('power_rows') else None)]
    L = [f"# QC REPORT — {CFG['name']} ({CID})", '', f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `_shared/production.py`.",
         '', '## Automated checks', '', '| Check | Result | Detail |', '|---|---|---|']
    for k, ok, d in rows:
        L.append(f"| {k} | {'✅ PASS' if ok else '❌ FAIL'} | {d} |")
    L += ['', '## Render-based tests (images in `design/raw/`, review by eye)', '', '| Test | Image |', '|---|---|']
    for k, f in vis:
        if f is None:
            L.append(f'| {k} | — no confirmed powers (not applicable) |')
        else:
            L.append(f"| {k} | {'`' + f + '` ✅ rendered' if os.path.exists(os.path.join(raw, f)) else '⬜ not rendered'} |")
    L += ['', '## Rig', '', f"- Bones: {QC['rig']['bones']} ({QC['rig']['deform']} deform)",
          f"- Controls: {', '.join(QC['rig']['controls'])}",
          f"- IK/FK switches (on `root`): {', '.join(QC['rig']['ik_fk_props'])}",
          f"- Pole angles / rest deviation: {json.dumps(ikd)}",
          f"- Face controls (on `root`): {len(QC['face_controls'])} — {', '.join(QC['face_controls'])}", '',
          '## Known limitations (honest)', '',
          '- Body rig is a custom deform skeleton + IK/FK controls, not a full Rigify rig (no stretch/twist bones).',
          '- Jaw is driven through the mouth shape keys (`jaw_open` → PH_A); the chin mesh does not move yet.',
          '- Textures are baked from procedural materials (no hand-painted detail).',
          '- Base meshes contain non-manifold edges where garment pieces are open shells (expected for clothing).',
          f"- Non-manifold edge counts: {json.dumps(t.get('non_manifold_edges_base_mesh', {}))[:600]}",
          '', f"Quad ratio body {t.get('quad_ratio_body')}, head {t.get('quad_ratio_head')}; meshes {QC['meshes']}; "
          f"render-time polycount ≈ {QC['polycount_render_estimate']:,}"]
    open(P('qc', 'QC_REPORT.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    bpy.ops.wm.open_mainfile(filepath=P('blend', f'{FOLDER}_v002.blend'))
    print('UV', len(uv_unwrap()))
    baked = bake_textures() if BAKE else {}
    arm = upgrade_rig()
    face_controls(arm)
    static_checks()
    cb.set_pose(arm, 'NEUTRAL', CFG.get('height', 1.75) / 1.75)
    bpy.ops.wm.save_as_mainfile(filepath=P('blend', f'{FOLDER}_v003.blend'))
    glb, fbx = export(baked)
    bpy.ops.wm.save_as_mainfile(filepath=P('blend', f'{FOLDER}_v003.blend'))
    reimport_check(glb)
    report()
    print('PRODUCTION DONE', FOLDER, json.dumps(QC['tests'])[:800])

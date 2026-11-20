"""Render every raw image needed for Pratyush's design sheet.

Run:  python3 01_characters/pratyush/render_sheet.py [group ...]
groups: turn poses face expr costume powers qc   (default: all)
Out:  01_characters/pratyush/design/raw/*.png  + qc/measurements.json
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import charkit as ck
import vfxkit as vx
import build_pratyush as B
from pratyush_spec import PAL, SPEC

RAW = os.path.join(HERE, 'design', 'raw')
QC = os.path.join(HERE, 'qc')
os.makedirs(RAW, exist_ok=True)
os.makedirs(QC, exist_ok=True)
BLEND = os.path.join(HERE, 'blend', 'pratyush_v001.blend')
N = B.name
SAMPLES = int(os.environ.get('SAMPLES', 40))


def ob(n):
    return bpy.data.objects[N(n)]


def load():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    S = ck.get_coll('STUDIO')
    return S


def face_kit():
    f = {'mouth': ob('MOUTH'), 'brows': ob('BROWS')}
    for sd in ('L', 'R'):
        f[f'eye_{sd}'] = ob(f'EYE_{sd}')
        f[f'lid_up_{sd}'] = ob(f'LID_UP_{sd}')
        f[f'lid_lo_{sd}'] = ob(f'LID_LO_{sd}')
    return f


def studio(S, dark=False):
    for o in list(S.objects):
        bpy.data.objects.remove(o)
    if dark:
        ck.world_color('#0B0E14', 0.15)
        k = 0.35
    else:
        ck.world_color('#8A9099', 0.35)
        k = 1.0
    ck.area_light('KEY', S, (-1.6, -2.6, 2.6), (0, 0, 1.2), 300 * k, 2.0, '#FFF3E6')
    ck.area_light('FILL', S, (2.2, -2.0, 1.4), (0, 0, 1.2), 110 * k, 2.5, '#E6F0FF')
    ck.area_light('RIM', S, (0.6, 2.6, 2.4), (0, 0, 1.3), 380 * k, 1.5, '#FFFFFF')


def rig():
    return ob('RIG')


def turn(deg):
    rig().rotation_euler = (0, 0, math.radians(deg))
    bpy.context.view_layer.update()


def eye_glow(v):
    bpy.data.materials['MAT_PRATYUSH_EYE'].node_tree.nodes['EYE_GLOW'].outputs[0].default_value = v


def power_glow(eye=0.0, core=6.0, streak=0.0):
    eye_glow(eye)
    bpy.data.materials['MAT_PRATYUSH_CORE'].node_tree.nodes['EMIT'].inputs[1].default_value = core
    b = bpy.data.materials['MAT_PRATYUSH_HAIR_STREAK'].node_tree.nodes['BSDF']
    b.inputs['Emission Strength'].default_value = streak


def full_cam(S, wide=False):
    return ck.camera('CAM_FULL', S, (0, -8, 1.0), (0, 0, 1.0), ortho=2.0)


def head_world():
    return B.HEAD_C.copy()


# ---------------------------------------------------------------- poses
def pose(name):
    a = rig()
    if name in B.POSES:
        B.set_pose(a, name)
        return
    ck.reset_pose(a)
    W = lambda b, ax, d: ck.world_rot(a, b, ax, d)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    fingers = lambda sd, s, d: [W(f'{fn}_{k + 1:02d}_{sd}', Y, s * d * (1 + 0.3 * k))
                                for fn in ('index', 'middle', 'ring', 'pinky') for k in range(3)]
    if name == 'DASH':
        W('spine_01', X, 10); W('spine_02', X, 8); W('neck', X, -6); W('head', X, -10)
        W('thigh_L', X, -55); W('shin_L', X, 60); W('foot_L', X, -10)
        W('thigh_R', X, 32); W('shin_R', X, 80); W('foot_R', X, 25)
        W('upperarm_L', Y, 72); W('upperarm_L', X, 50); W('forearm_L', Z, -75)
        W('upperarm_R', Y, -72); W('upperarm_R', X, -55); W('forearm_R', Z, 75)
        fingers('L', 1, 45); fingers('R', -1, 45)
    elif name in ('CAST_L', 'CAST_R'):
        cs, ot = ('L', 'R') if name == 'CAST_L' else ('R', 'L')
        s = 1 if cs == 'L' else -1
        W(f'upperarm_{cs}', Z, -s * 62); W(f'upperarm_{cs}', Y, s * 8)
        W(f'hand_{cs}', Y, -s * 28)
        fingers(cs, s, -4)
        W(f'thumb_02_{cs}', Z, -s * 10)
        so = -s
        W(f'upperarm_{ot}', Y, so * 72); W(f'forearm_{ot}', Z, so * -25)
        fingers(ot, so, 55)
        W('spine_02', Z, s * 10); W('head', Z, s * 14)
        W(f'thigh_{cs}', X, -12); W(f'thigh_{ot}', X, 10); W(f'shin_{ot}', X, 6)
    bpy.context.view_layer.update()


def bone_world(b, tail=False):
    a = rig()
    pb = a.pose.bones[b]
    return a.matrix_world @ (pb.tail if tail else pb.head)


# ---------------------------------------------------------------- groups
def g_turn(S):
    studio(S)
    ck.setup_render((640, 1120), SAMPLES, transparent=True)
    cam = full_cam(S)
    pose('NEUTRAL')
    for label, deg in (('front', 0), ('three_quarter_front', 35), ('right', 90), ('three_quarter_back', 145),
                       ('back', 180), ('left', -90)):
        turn(deg)
        ck.render_to(os.path.join(RAW, f'turn_{label}.png'), cam)
    turn(0)


def g_poses(S):
    studio(S)
    cam = full_cam(S)
    for p, res in (('T', (1120, 1120)), ('A', (900, 1120)), ('NEUTRAL', (640, 1120))):
        ck.setup_render(res, SAMPLES, transparent=True)
        pose(p)
        ck.render_to(os.path.join(RAW, f'pose_{p}.png'), cam)


def face_cam(S, dist=0.78, lens=85, dz=0.03):
    h = head_world() + Vector((0, 0, dz))
    return ck.camera('CAM_FACE', S, h + Vector((0, -dist, 0.0)), h, lens=lens)


def g_face(S):
    studio(S)
    pose('NEUTRAL')
    B.set_expression(face_kit(), 'neutral')
    ck.setup_render((800, 960), SAMPLES, transparent=True)
    cam = face_cam(S)
    for label, deg in (('front', 0), ('side', 90), ('three_quarter', 35), ('back_three_quarter', 150)):
        turn(deg)
        ck.render_to(os.path.join(RAW, f'face_{label}.png'), cam)
    turn(0)
    # eye detail (character's left eye)
    e = ob('EYE_L').matrix_world.translation
    ck.setup_render((900, 520), SAMPLES, transparent=True)
    cam = ck.camera('CAM_EYE', S, e + Vector((0.0, -0.20, 0.006)), e + Vector((0, 0, 0.006)), lens=85)
    ck.render_to(os.path.join(RAW, 'face_eye_detail.png'), cam)


def tears(S, on):
    for o in [o for o in bpy.data.objects if o.name.startswith('FX_TEAR')]:
        bpy.data.objects.remove(o)
    if not on:
        return
    glass = ck.principled('MAT_TEAR', '#DDEEFF', rough=0.02, spec=0.8)
    glass.node_tree.nodes['BSDF'].inputs['Transmission Weight'].default_value = 1.0
    for sd, sx in (('L', 1), ('R', -1)):
        e = ob(f'EYE_{sd}').matrix_world.translation
        for k, (dz, sc) in enumerate(((-0.016, 1.0), (-0.030, 0.8), (-0.045, 0.6))):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0028 * sc, location=(e.x + sx * 0.004, e.y - 0.002 - 0.004 * k, e.z + dz))
            t = bpy.context.object
            t.name = f'FX_TEAR_{sd}_{k}'
            t.scale.z = 1.6
            ck.link(t, S)
            ck.assign(t, glass)


def g_expr(S):
    studio(S)
    pose('NEUTRAL')
    turn(12)
    ck.setup_render((560, 640), SAMPLES, transparent=True)
    cam = face_cam(S, dist=0.66, dz=0.0)
    face = face_kit()
    from pratyush_spec import EXPRESSIONS
    for i, e in enumerate(['neutral', 'happy', 'angry', 'sad', 'fear', 'shocked', 'confident', 'evil',
                           'serious', 'crying', 'blink']):
        B.set_expression(face, e)
        tears(S, EXPRESSIONS[e].get('tears', False))
        ck.render_to(os.path.join(RAW, f'expr_{i:02d}_{e}.png'), cam)
    tears(S, False)
    B.set_expression(face, 'neutral')
    turn(0)


COSTUME = [
    ('suit', 'Main: armoured speed suit', ['SUIT']),
    ('armor', 'Outer: chest plate, pauldrons, knee guards, collar',
     ['CHEST_PLATE', 'PAULDRON_L', 'PAULDRON_R', 'KNEE_L', 'KNEE_R', 'COLLAR', 'EMBLEM']),
    ('boots', 'Shoes: armoured sprint boots', ['BOOT_L', 'BOOT_R']),
    ('gloves', 'Gloves: full-finger grip gloves', ['GLOVE_L']),
    ('belt', 'Belt + buckle', ['BELT', 'BELT_BUCKLE']),
    ('bracers', 'Special equipment: speed bracers', ['BRACER_L', 'BRACER_CORE_L']),
    ('hair', 'Hair (cap + clumps)', ['HAIR', 'HAIR_CAP']),
]


def world_bbox(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        for v in me.vertices:
            w = ev.matrix_world @ v.co
            lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
        ev.to_mesh_clear()
    return lo, hi


def world_verts(o):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    out = [ev.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return out


def g_costume(S):
    studio(S)
    pose('NEUTRAL')
    turn(30)
    ck.setup_render((560, 560), SAMPLES, transparent=True)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('CHAR_')]
    for key, label, parts in COSTUME:
        show = {N(p) for p in parts}
        for o in meshes:
            o.hide_render = o.name not in show
        lo, hi = world_bbox([ob(p) for p in parts])
        c = (lo + hi) / 2
        size = max(hi - lo) * 1.25
        cam = ck.camera('CAM_COST', S, c + Vector((0, -6, 0)), c, ortho=size)
        ck.render_to(os.path.join(RAW, f'costume_{key}.png'), cam)
        bpy.data.objects.remove(cam)
    for o in meshes:
        o.hide_render = False
    turn(0)


def clear_fx():
    for o in [o for o in bpy.data.objects if o.name.startswith('FX_')]:
        bpy.data.objects.remove(o)


def body_anchors(bones):
    return [bone_world(b, t) for b in bones for t in (False, True)]


def g_powers(S):
    studio(S, dark=True)
    FX = ck.get_coll('VFX_PRATYUSH_SHEET')
    core = vx.energy_mat('MAT_FX_LIGHTNING_CORE', PAL['power_core'], 40.0)
    glow = ck.emission('MAT_FX_LIGHTNING_GLOW', PAL['power_glow'], 6.0)
    trail = ck.emission('MAT_FX_SPEED_TRAIL', PAL['speed_trail'], 8.0)
    rune = ck.emission('MAT_FX_RUNE', PAL['portal_rim'], 12.0)
    for m in (glow,):
        pass
    ck.setup_render((900, 1120), SAMPLES)
    cam = ck.camera('CAM_PWR', S, (0.0, -8, 1.0), (0, 0, 1.0), ortho=2.3)
    eyecam_h = head_world() + Vector((0, 0, 0.0))

    def shot(fname, c=cam):
        ck.render_to(os.path.join(RAW, fname), c)

    def fx_obj(o):
        for x in (o if isinstance(o, list) else [o]):
            x.name = 'FX_' + x.name
            ck.link(x, FX)

    # ---------- NORMAL (shared by all three powers)
    clear_fx(); pose('NEUTRAL'); turn(20); power_glow(0, 1.5, 0)
    shot('power_normal.png')

    # ---------- SUPER SPEED (side-on, running to image right)
    def speed(stage):
        clear_fx()
        if stage == 'deactivation':
            pose('NEUTRAL'); turn(90)
        else:
            pose('DASH'); turn(90)
        mo = Vector((1, 0, 0))
        legs = ['shin_L', 'shin_R', 'thigh_L', 'thigh_R', 'forearm_L', 'forearm_R', 'spine_02', 'head']
        anchors = body_anchors(legs)
        if stage == 'activation':
            power_glow(1.5, 12, 0.5)
            fx_obj(vx.speed_trails('SPEED_TRAIL', FX, anchors, mo, trail, length=0.35, count=8))
            fx_obj(vx.aura_arcs('SPEED_SPARK', FX, body_anchors(['shin_L', 'shin_R', 'foot_L', 'foot_R']),
                                core, glow, size=0.08, count=5))
        elif stage == 'full':
            power_glow(4, 25, 2.0)
            fx_obj(vx.speed_trails('SPEED_TRAIL', FX, anchors, mo, trail, length=1.1, count=20))
            fx_obj(vx.aura_arcs('SPEED_SPARK', FX, anchors, core, glow, size=0.18, count=16))
        elif stage == 'deactivation':
            power_glow(1.2, 4, 0.2)
            fx_obj(vx.speed_trails('SPEED_TRAIL', FX, body_anchors(['shin_L', 'shin_R']), mo, trail,
                                   length=0.25, count=5, width=0.004))
        shot(f'power_speed_{stage}.png')

    for st in ('activation', 'full', 'deactivation'):
        speed(st)
    # afterimages for the full stage: character only, shifted back along motion
    clear_fx(); pose('DASH'); turn(90); power_glow(4, 25, 2.0)
    bpy.context.scene.render.film_transparent = True
    for k, dx in enumerate((-0.38, -0.76)):
        rig().location.x = dx
        shot(f'power_speed_afterimage_{k}.png')
    rig().location.x = 0
    bpy.context.scene.render.film_transparent = False

    # ---------- LIGHTNING (cast from left hand)
    def lightning(stage):
        clear_fx()
        if stage == 'deactivation':
            pose('NEUTRAL'); turn(20)
        else:
            pose('CAST_L'); turn(20)
        hand = bone_world('middle_01_L')
        fwd = (bone_world('middle_03_L', True) - bone_world('hand_L')).normalized()
        if stage == 'activation':
            power_glow(1.5, 10, 0.5)
            fx_obj(vx.aura_arcs('LT_HAND', FX, [hand], core, glow, size=0.07, count=6))
        elif stage == 'full':
            power_glow(4, 30, 3.0)
            fx_obj(vx.lightning('LT_BOLT', FX, hand, hand + fwd * 1.6 + Vector((0, 0, -0.5)), core, glow,
                                seed=11, branches=5, radius=0.004))
            fx_obj(vx.aura_arcs('LT_AURA', FX, body_anchors(['upperarm_L', 'forearm_L', 'spine_02', 'spine_03',
                                                             'thigh_L', 'thigh_R', 'head']),
                                core, glow, size=0.20, count=22))
            ld = bpy.data.lights.new('FX_LT_LIGHT', 'POINT'); ld.energy = 120; ld.color = ck.hexlin(PAL['power_glow'])[:3]
            lo = bpy.data.objects.new('FX_LT_LIGHT', ld); lo.location = hand; FX.objects.link(lo)
        elif stage == 'deactivation':
            power_glow(1.0, 4, 0.2)
            fx_obj(vx.aura_arcs('LT_RESID', FX, [bone_world('middle_03_L', True), bone_world('index_03_L', True)],
                                core, glow, size=0.04, count=3))
        shot(f'power_lightning_{stage}.png')

    for st in ('activation', 'full', 'deactivation'):
        lightning(st)

    # ---------- MAGICAL PORTAL (opened with right hand)
    def portal(stage):
        clear_fx()
        if stage == 'deactivation':
            pose('NEUTRAL'); turn(20)
        else:
            pose('CAST_R'); turn(20)
        hand = bone_world('middle_01_R')
        fwd = (bone_world('middle_03_R', True) - bone_world('hand_R')).normalized()
        c = hand + fwd * 0.55 + Vector((0, 0, -0.05))
        c.z = max(c.z, 1.0)
        yaw = math.degrees(math.atan2(-fwd.x, fwd.y)) + 180
        if stage == 'activation':
            power_glow(1.5, 10, 0.5)
            fx_obj(vx.portal('PORTAL', FX, c, 0.75, PAL['portal_rim'], PAL['portal_deep'], yaw_deg=yaw,
                             openness=0.25, intensity=0.7))
            fx_obj(vx.rune_ring('RUNE', FX, hand + fwd * 0.06, 0.07, rune, (math.pi / 2, 0, math.radians(yaw))))
        elif stage == 'full':
            power_glow(3, 20, 2.0)
            fx_obj(vx.portal('PORTAL', FX, c + fwd * 0.35, 0.70, PAL['portal_rim'], PAL['portal_deep'],
                             yaw_deg=yaw, openness=1.0, intensity=1.0))
            fx_obj(vx.rune_ring('RUNE', FX, hand + fwd * 0.06, 0.08, rune, (math.pi / 2, 0, math.radians(yaw))))
        elif stage == 'deactivation':
            power_glow(1.0, 4, 0.2)
            fx_obj(vx.portal('PORTAL', FX, Vector((-0.65, -0.35, 1.0)), 0.75, PAL['portal_rim'], PAL['portal_deep'],
                             yaw_deg=20, openness=0.35, intensity=0.35))
        shot(f'power_portal_{stage}.png')

    for st in ('activation', 'full', 'deactivation'):
        portal(st)

    # ---------- hand close-ups
    ck.setup_render((700, 560), SAMPLES)

    def hand_cam(bone_root, side_offset):
        h = bone_world(bone_root)
        return ck.camera('CAM_HAND', S, h + Vector(side_offset), h, lens=70)

    clear_fx(); pose('CAST_L'); turn(20); power_glow(3, 30, 2)
    tips = [bone_world(f'{f}_03_L', True) for f in ('thumb', 'index', 'middle', 'ring', 'pinky')]
    for i, (p, q) in enumerate(zip(tips, tips[1:])):
        fx_obj(vx.lightning(f'LT_FINGER_{i}', FX, p, q, core, glow, seed=40 + i, branches=0, radius=0.0012,
                            depth=4, jag=0.4))
    fx_obj(vx.aura_arcs('LT_PALM', FX, tips, core, glow, size=0.05, count=6))
    c = hand_cam('hand_L', (0.05, -0.55, 0.12)); shot('hand_lightning.png', c); bpy.data.objects.remove(c)

    clear_fx(); pose('CAST_R'); turn(20); power_glow(3, 20, 2)
    hand = bone_world('middle_01_R')
    fwd = (bone_world('middle_03_R', True) - bone_world('hand_R')).normalized()
    yaw = math.degrees(math.atan2(-fwd.x, fwd.y)) + 180
    fx_obj(vx.rune_ring('RUNE', FX, hand + fwd * 0.07, 0.09, rune, (math.pi / 2, 0, math.radians(yaw))))
    fx_obj(vx.aura_arcs('PT_SPARK', FX, [hand + fwd * 0.07], core, glow, size=0.05, count=4))
    c = hand_cam('hand_R', (-0.10, -0.55, 0.10)); shot('hand_portal.png', c); bpy.data.objects.remove(c)

    clear_fx(); pose('DASH'); turn(90); power_glow(3, 30, 2)
    fa = body_anchors(['forearm_L', 'hand_L'])
    fx_obj(vx.speed_trails('HAND_TRAIL', FX, fa, Vector((1, 0, 0)), trail, length=0.45, count=10, width=0.004))
    c = hand_cam('hand_L', (0.0, -1.1, 0.10)); c.data.lens = 50; shot('hand_speed.png', c); bpy.data.objects.remove(c)

    # ---------- eye transformation
    clear_fx(); pose('NEUTRAL'); turn(0)
    ck.setup_render((900, 420), SAMPLES)
    h = head_world() + Vector((0, 0, 0.004))
    c = ck.camera('CAM_EYES', S, h + Vector((0, -0.42, 0)), h, lens=85)
    for label, g in (('normal', 0.0), ('activation', 1.5), ('full', 4.0)):
        power_glow(g, 6, g * 0.3)
        shot(f'eyes_{label}.png', c)
    bpy.data.objects.remove(c)
    power_glow(0, 6, 0)
    clear_fx(); turn(0); pose('NEUTRAL')


def g_qc(S):
    """Measure the real model (not the spec) and save it for the sheet."""
    pose('NEUTRAL')
    lo, hi = world_bbox([ob('HEAD'), ob('BODY')])
    hl, hh = world_bbox([ob('HAIR'), ob('HAIR_CAP')])
    hd_lo, hd_hi = world_bbox([ob('HEAD')])
    dg = bpy.context.evaluated_depsgraph_get()
    body = ob('BODY').evaluated_get(dg)
    me = body.to_mesh()
    vs = [body.matrix_world @ v.co for v in me.vertices]
    body.to_mesh_clear()
    sh = [v for v in vs if 1.36 < v.z < 1.45]
    ch = [v for v in vs if 1.29 < v.z < 1.33 and abs(v.x) < 0.17]
    hip = [v for v in vs if 0.88 < v.z < 0.96 and abs(v.x) < 0.21]
    m = {
        'height_no_hair_m': round(hi.z - lo.z, 4),
        'height_with_hair_m': round(max(hh.z, hi.z) - lo.z, 4),
        'head_height_m': round(hd_hi.z - hd_lo.z, 4),
        'heads_tall': round((hi.z - lo.z) / (hd_hi.z - hd_lo.z), 2),
        'shoulder_width_m': round(max(v.x for v in sh) - min(v.x for v in sh), 4),
        'chest_width_m': round(max(v.x for v in ch) - min(v.x for v in ch), 4),
        'hip_width_m': round(max(v.x for v in hip) - min(v.x for v in hip), 4),
        'leg_length_m': round(0.90 - lo.z, 4),
        'head_top_z': round(hd_hi.z, 4),
        'chin_z': round(hd_lo.z, 4),
    }
    pose('T')
    vs = [v for v in world_verts(ob('BODY'))]
    m['arm_length_m'] = round(max(v.x for v in vs) - 0.185, 4)
    json.dump(m, open(os.path.join(QC, 'measurements.json'), 'w'), indent=2)
    print('MEASURE', m)
    pose('NEUTRAL')


GROUPS = {'qc': g_qc, 'turn': g_turn, 'poses': g_poses, 'face': g_face, 'expr': g_expr,
          'costume': g_costume, 'powers': g_powers}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a in GROUPS] or list(GROUPS)
    S = load()
    for g in args:
        print('=== GROUP', g, flush=True)
        GROUPS[g](S)
    print('DONE', args)

"""Render every raw image for a character's design sheet (config-driven).

Run:  python3 01_characters/_shared/sheet_render.py <folder> [group ...]
groups: qc turn poses face expr costume powers extras tests   (default: all but tests)
Out:  01_characters/<folder>/design/raw/*.png, <folder>/qc/measurements.json
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import charkit as ck
import vfxkit as vx
import charbuild as cb
from build_char import load_cfg

FOLDER = [a for a in sys.argv[1:] if not a.startswith('-')][0]
CFG, DIR = load_cfg(FOLDER)
CID = CFG['id']
PAL = CFG['pal']
VER = os.environ.get('VER', '002')
RAW = os.path.join(DIR, 'design', 'raw')
QC = os.path.join(DIR, 'qc')
os.makedirs(RAW, exist_ok=True); os.makedirs(QC, exist_ok=True)
BLEND = os.path.join(DIR, 'blend', f'{FOLDER}_v{VER}.blend')
SAMPLES = int(os.environ.get('SAMPLES', 32))
S = CFG.get('height', 1.75) / 1.75


def ob(n):
    return bpy.data.objects[f'CHAR_{CID}_{n}']


def rig():
    return ob('RIG')


def pose(n):
    cb.set_pose(rig(), n, S)


def turn(d):
    rig().rotation_euler = (0, 0, math.radians(d))
    bpy.context.view_layer.update()


def head_c():
    return ob('HEAD').matrix_world.translation.copy()


def top_z():
    return max((o.matrix_world @ Vector(b)).z for o in bpy.data.objects
               if o.type == 'MESH' and o.name.startswith(f'CHAR_{CID}') for b in o.bound_box)


def studio(St, dark=False):
    for o in list(St.objects):
        bpy.data.objects.remove(o)
    k = .35 if dark else 1.0
    ck.world_color('#0B0E14' if dark else '#8A9099', .15 if dark else .35)
    sc = max(1.0, S)
    ck.area_light('KEY', St, (-1.6 * sc, -2.6 * sc, 2.6 * sc), (0, 0, 1.2 * S), 300 * k * sc, 2.0, '#FFF3E6')
    ck.area_light('FILL', St, (2.2 * sc, -2.0 * sc, 1.4 * sc), (0, 0, 1.2 * S), 110 * k * sc, 2.5, '#E6F0FF')
    ck.area_light('RIM', St, (.6 * sc, 2.6 * sc, 2.4 * sc), (0, 0, 1.3 * S), 380 * k * sc, 1.5, '#FFFFFF')


def glow(eye=0.0, core=None, streak=0.0):
    m = bpy.data.materials.get(f'MAT_{CID}_EYE')
    if m and 'EYE_GLOW' in m.node_tree.nodes:
        m.node_tree.nodes['EYE_GLOW'].outputs[0].default_value = CFG.get('eye', {}).get('base_glow', 0) + eye
    for mn in CFG.get('glow_mats', ['core']):
        mm = bpy.data.materials.get(f'MAT_{CID}_{mn.upper()}')
        if mm and 'EMIT' in mm.node_tree.nodes and core is not None:
            base = CFG['materials'][mn].get('strength', 6)
            mm.node_tree.nodes['EMIT'].inputs[1].default_value = base * core
    hs = bpy.data.materials.get(f'MAT_{CID}_HAIR_STREAK')
    if hs:
        hs.node_tree.nodes['BSDF'].inputs['Emission Strength'].default_value = streak


def bone(b, tail=False):
    a = rig(); pb = a.pose.bones[b]
    return a.matrix_world @ (pb.tail if tail else pb.head)


def anchors(bones):
    return [bone(b, t) for b in bones for t in (False, True)]


def full_cam(St):
    h = top_z()
    return ck.camera('CAM_FULL', St, (0, -12, h / 2), (0, 0, h / 2), ortho=max(2.0, h * 1.1))


def save(name, cam):
    ck.render_to(os.path.join(RAW, name), cam)


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


# ======================================================================= groups
def g_qc(St):
    pose('NEUTRAL')
    lo, hi = world_bbox([ob('HEAD'), ob('BODY')])
    top = top_z()
    hd_lo, hd_hi = world_bbox([ob('HEAD')])
    vs = world_verts(ob('BODY'))
    band = lambda z0, z1, xm=9: [v for v in vs if z0 * S < v.z < z1 * S and abs(v.x) < xm * S]
    w = lambda L: round(max(v.x for v in L) - min(v.x for v in L), 4)
    m = {'height_no_hair_m': round(hi.z - lo.z, 4), 'height_total_m': round(top - lo.z, 4),
         'head_height_m': round(hd_hi.z - hd_lo.z, 4),
         'heads_tall': round((hi.z - lo.z) / (hd_hi.z - hd_lo.z), 2),
         'shoulder_width_m': w(band(1.36, 1.45)), 'chest_width_m': w(band(1.29, 1.33, .17)),
         'hip_width_m': w(band(.88, .96, .21)), 'leg_length_m': round(.90 * S - lo.z, 4),
         'head_top_z': round(hd_hi.z, 4), 'chin_z': round(hd_lo.z, 4)}
    pose('T')
    vs = world_verts(ob('BODY'))
    sh = rig().data.bones['upperarm_L'].head_local.x
    m['arm_length_m'] = round(max(v.x for v in vs) - sh, 4)
    hl = rig().data.bones['hand_L']
    m['hand_length_m'] = round(max(v.x for v in vs) - hl.head_local.x, 4)
    ft = [v for v in vs if v.z < .1 * S and v.x > 0]
    m['foot_length_m'] = round(max(v.y for v in ft) - min(v.y for v in ft), 4)
    # mesh sanity: every evaluated piece must stay near the body (catches flipped/exploded geometry)
    pose('NEUTRAL')
    blo, bhi = world_bbox([ob('BODY')])
    bad = []
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith(f'CHAR_{CID}_'):
            lo, hi = world_bbox([o])
            if any(lo[i] < blo[i] - .35 * S or hi[i] > bhi[i] + .35 * S for i in range(2)) or hi.z > bhi.z + .6 * S:
                bad.append(o.name)
    m['mesh_sanity_fail'] = bad
    json.dump(m, open(os.path.join(QC, 'measurements.json'), 'w'), indent=2)
    print('MEASURE', m)
    pose('NEUTRAL')


def g_turn(St):
    studio(St)
    ck.setup_render((640, 1120), SAMPLES, transparent=True)
    pose('NEUTRAL')
    cam = full_cam(St)
    for label, deg in (('front', 0), ('three_quarter_front', 35), ('right', 90), ('three_quarter_back', 145),
                       ('back', 180), ('left', -90)):
        turn(deg); save(f'turn_{label}.png', cam)
    turn(0)


def g_poses(St):
    studio(St)
    pose('T'); cam = full_cam(St)
    for p, res in (('T', (1120, 1120)), ('A', (900, 1120)), ('NEUTRAL', (640, 1120))):
        ck.setup_render(res, SAMPLES, transparent=True)
        pose(p); save(f'pose_{p}.png', cam)


def face_cam(St, dist=.78, dz=.03):
    h = head_c() + Vector((0, 0, dz))
    sc = CFG.get('head', {}).get('size', 1) * S ** .3 * CFG.get('face_cam', 1.0)
    return ck.camera('CAM_FACE', St, h + Vector((0, -dist * sc, 0)), h, lens=85)


def g_face(St):
    studio(St); pose('NEUTRAL')
    F = cb.face_of(CID); cb.set_expression(F, 'neutral')
    ck.setup_render((800, 960), SAMPLES, transparent=True)
    cam = face_cam(St)
    for label, deg in (('front', 0), ('side', 90), ('three_quarter', 35), ('back_three_quarter', 150)):
        turn(deg); save(f'face_{label}.png', cam)
    turn(0)
    e = ob('EYE_L').matrix_world.translation
    ck.setup_render((900, 520), SAMPLES, transparent=True)
    c = ck.camera('CAM_EYE', St, e + Vector((0, -.20, .006)), e + Vector((0, 0, .006)), lens=85)
    save('face_eye_detail.png', c)


def tears(St, on):
    for o in [o for o in bpy.data.objects if o.name.startswith('FX_TEAR')]:
        bpy.data.objects.remove(o)
    if not on:
        return
    glass = ck.principled('MAT_TEAR', '#DDEEFF', rough=.02, spec=.8)
    glass.node_tree.nodes['BSDF'].inputs['Transmission Weight'].default_value = 1.0
    for sd, sx in (('L', 1), ('R', -1)):
        e = ob(f'EYE_{sd}').matrix_world.translation
        for k, (dz, sc) in enumerate(((-.016, 1), (-.030, .8), (-.045, .6))):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=.0028 * sc, location=(e.x + sx * .004, e.y - .002 - .004 * k, e.z + dz))
            t = bpy.context.object; t.name = f'FX_TEAR_{sd}_{k}'; t.scale.z = 1.6
            ck.link(t, St); ck.assign(t, glass)


def g_expr(St):
    studio(St); pose('NEUTRAL'); turn(12)
    ck.setup_render((560, 640), SAMPLES, transparent=True)
    cam = face_cam(St, dist=.66, dz=0)
    F = cb.face_of(CID)
    for i, e in enumerate(CFG['expressions']):
        ex = cb.set_expression(F, e)
        tears(St, ex.get('tears', False))
        if e == 'concentration':
            glow(1.5, 2.0)
        save(f'expr_{i:02d}_{e}.png', cam)
        glow(0, 1.0)
    tears(St, False); cb.set_expression(F, 'neutral'); turn(0)


def g_costume(St):
    studio(St); pose('NEUTRAL'); turn(30)
    ck.setup_render((560, 560), SAMPLES, transparent=True)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('CHAR_')]
    for key, label, parts, *_ in CFG['costume_groups']:
        show = {f'CHAR_{CID}_{p}' for p in parts}
        for o in meshes:
            o.hide_render = o.name not in show
        lo, hi = world_bbox([bpy.data.objects[n] for n in show])
        c = (lo + hi) / 2
        cam = ck.camera('CAM_COST', St, c + Vector((0, -8, 0)), c, ortho=max(hi - lo) * 1.25)
        save(f'costume_{key}.png', cam)
        bpy.data.objects.remove(cam)
    for o in meshes:
        o.hide_render = False
    turn(0)


# ======================================================================= powers
FX = None


def clear_fx():
    for o in [o for o in bpy.data.objects if o.name.startswith('FX_')]:
        bpy.data.objects.remove(o)
    bpy.context.view_layer.material_override = None


def fx(o):
    for x in (o if isinstance(o, list) else [o]):
        if not x.name.startswith('FX_'):
            x.name = 'FX_' + x.name
        ck.link(x, FX)
    return o


def light_at(p, hx, e):
    ld = bpy.data.lights.new('FX_L', 'POINT'); ld.energy = e; ld.color = ck.hexlin(hx)[:3]
    lo = bpy.data.objects.new('FX_L', ld); lo.location = p; FX.objects.link(lo)


def mats():
    P = PAL
    g = P.get('power_glow', '#4FD8FF'); c = P.get('power_core', '#F2FBFF')
    return {
        'core': ck.emission('MAT_FX_LT_CORE', c, 40), 'glow': ck.emission('MAT_FX_LT_GLOW', g, 6),
        'trail': ck.emission('MAT_FX_TRAIL', P.get('speed_trail', g), 8),
        'rune': ck.emission('MAT_FX_RUNE', P.get('portal_rim', g), 12),
        'fire': vx.flame_material('MAT_FX_FIRE', P.get('fire_core', '#FFF2B0'), P.get('fire_mid', '#FF8A1F'),
                                  P.get('fire_outer', '#B3170A'), 14),
        'dark': vx.flame_material('MAT_FX_DARK', P.get('dark_core', '#C27BFF'), P.get('dark_mid', '#5A1A8C'),
                                  P.get('dark_outer', '#0A0410'), 5, fade=.6),
    }


def hand_dir(sd):
    return (bone(f'middle_03_{sd}', True) - bone(f'hand_{sd}')).normalized()


def body_pts():
    return anchors(['upperarm_L', 'upperarm_R', 'forearm_L', 'forearm_R', 'spine_02', 'spine_03', 'thigh_L',
                    'thigh_R', 'shin_L', 'shin_R', 'head', 'pelvis'])


def p_speed(stage, M):
    if stage == 'deactivation':
        pose('NEUTRAL'); turn(90)
    else:
        pose('DASH'); turn(90)
    mo = Vector((1, 0, 0))
    an = anchors(['shin_L', 'shin_R', 'thigh_L', 'thigh_R', 'forearm_L', 'forearm_R', 'spine_02', 'head'])
    if stage == 'activation':
        glow(1.5, 2, .5)
        fx(vx.speed_trails('SPEED_TRAIL', FX, an, mo, M['trail'], length=.35 * S, count=8))
        fx(vx.aura_arcs('SPEED_SPARK', FX, anchors(['shin_L', 'shin_R', 'foot_L', 'foot_R']), M['core'], M['glow'], size=.08, count=5))
    elif stage == 'full':
        glow(3, 4, 2)
        fx(vx.speed_trails('SPEED_TRAIL', FX, an, mo, M['trail'], length=1.1 * S, count=20))
        fx(vx.aura_arcs('SPEED_SPARK', FX, an, M['core'], M['glow'], size=.18, count=16))
    elif stage == 'deactivation':
        glow(.8, 1.2, .2)
        fx(vx.speed_trails('SPEED_TRAIL', FX, anchors(['shin_L', 'shin_R']), mo, M['trail'], length=.25, count=5, width=.004))


def p_lightning(stage, M):
    pose('NEUTRAL' if stage == 'deactivation' else 'CAST_L'); turn(20)
    hand = bone('middle_01_L'); fwd = hand_dir('L')
    if stage == 'activation':
        glow(1.5, 2, .5); fx(vx.aura_arcs('LT_HAND', FX, [hand], M['core'], M['glow'], size=.07, count=6))
    elif stage == 'full':
        glow(3, 5, 3)
        fx(vx.lightning('LT_BOLT', FX, hand, hand + fwd * 1.6 + Vector((0, 0, -.5)), M['core'], M['glow'], seed=11, branches=5, radius=.004))
        fx(vx.aura_arcs('LT_AURA', FX, anchors(['upperarm_L', 'forearm_L', 'spine_02', 'spine_03', 'thigh_L', 'thigh_R', 'head']),
                        M['core'], M['glow'], size=.20, count=22))
        light_at(hand, PAL.get('power_glow', '#4FD8FF'), 120)
    elif stage == 'deactivation':
        glow(.8, 1.2, .2)
        fx(vx.aura_arcs('LT_RESID', FX, [bone('middle_03_L', True), bone('index_03_L', True)], M['core'], M['glow'], size=.04, count=3))


def _portal(stage, M, corrupted=False):
    pose('NEUTRAL' if stage == 'deactivation' else 'CAST_R'); turn(20)
    hand = bone('middle_01_R'); fwd = hand_dir('R')
    c = hand + fwd * .55 + Vector((0, 0, -.05)); c.z = max(c.z, 1.0 * S)
    yaw = math.degrees(math.atan2(-fwd.x, fwd.y)) + 180
    rim, deep = PAL.get('portal_rim', '#6FE7FF'), PAL.get('portal_deep', '#0A2A5A')
    sw = -6.0 if corrupted else 5.0
    if stage == 'activation':
        glow(1.5, 2, .5)
        fx(vx.portal('PORTAL', FX, c, .75, rim, deep, yaw_deg=yaw, openness=.25, intensity=.7, swirl=sw))
        fx(vx.rune_ring('RUNE', FX, hand + fwd * .06, .07, M['rune'], (math.pi / 2, 0, math.radians(yaw))))
    elif stage == 'full':
        glow(3, 4, 2)
        pc = Vector((-.95 * S, .05, 1.0 * S))
        fx(vx.portal('PORTAL', FX, pc, .55 * S, rim, deep, yaw_deg=25, openness=1.0, intensity=1.0, swirl=sw))
        fx(vx.rune_ring('RUNE', FX, hand + fwd * .06, .08, M['rune'], (math.pi / 2, 0, math.radians(yaw))))
        if corrupted:
            fx(vx.flames('PORTAL_SMOKE', FX, [pc + Vector((math.cos(a) * .7 * S, 0, math.sin(a) * .7 * S)) for a in
                                              [i * .5 for i in range(13)]], M['dark'], count=30, length=.25, width=.03))
    elif stage == 'deactivation':
        glow(.8, 1.2, .2)
        fx(vx.portal('PORTAL', FX, Vector((-.65, -.35, 1.0 * S)), .75, rim, deep, yaw_deg=20, openness=.35, intensity=.35, swirl=sw))


def p_portal(stage, M):
    _portal(stage, M)


def p_corrupted_portal(stage, M):
    _portal(stage, M, True)


def p_fire(stage, M):
    pose('NEUTRAL' if stage == 'deactivation' else 'CAST_L'); turn(20)
    hand = bone('middle_01_L'); fwd = hand_dir('L')
    tips = [bone(f'{f}_03_L', True) for f in ('thumb', 'index', 'middle', 'ring', 'pinky')]
    mid = PAL.get('fire_mid', '#FF8A1F')
    if stage == 'activation':
        glow(1.5, 2, .3)
        fx(vx.flames('FIRE_HAND', FX, tips + [hand], M['fire'], count=14, length=.10 * S, width=.014))
        light_at(hand, mid, 40)
    elif stage == 'full':
        glow(3, 4, 1)
        fx(vx.flames('FIRE_HAND', FX, tips + [hand], M['fire'], count=18, length=.16 * S, width=.02))
        fx(vx.fireball('FIREBALL', FX, hand + fwd * .35 * S, .09 * S, PAL.get('fire_core', '#FFF2B0'), mid,
                       PAL.get('fire_outer', '#B3170A'), motion=fwd))
        fx(vx.flames('FIRE_AURA', FX, body_pts(), M['fire'], count=40, length=.22 * S, width=.03, spread=.05))
    elif stage == 'deactivation':
        glow(.8, 1.2, .1)
        fx(vx.flames('FIRE_EMBER', FX, tips[:3], M['fire'], count=5, length=.05, width=.008))


def p_dark_magic(stage, M):
    pose('NEUTRAL' if stage == 'deactivation' else 'POWER_UP'); turn(20)
    hands = [bone('middle_01_L'), bone('middle_01_R')]
    dc = PAL.get('dark_core', '#C27BFF')
    if stage == 'activation':
        glow(1.5, 2, .3)
        fx(vx.flames('DARK_HAND', FX, hands, M['dark'], count=16, length=.14 * S, width=.02, swirl=1.5))
        light_at(hands[0], dc, 25); light_at(hands[1], dc, 25)
    elif stage == 'full':
        glow(3, 4, 1)
        fx(vx.flames('DARK_HAND', FX, hands, M['dark'], count=24, length=.22 * S, width=.026, swirl=2))
        fx(vx.flames('DARK_AURA', FX, body_pts(), M['dark'], count=55, length=.30 * S, width=.04, swirl=2.5, spread=.06))
        c = (hands[0] + hands[1]) / 2 + Vector((0, -.25, 0))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=.07 * S, location=c)
        o = bpy.context.object; o.name = 'FX_DARK_ORB'; ck.link(o, FX); ck.assign(o, ck.emission('MAT_FX_DARK_ORB', dc, 8))
        fx(vx.aura_arcs('DARK_ARCS', FX, [c], ck.emission('MAT_FX_DARK_ARC', '#F1D9FF', 25),
                        ck.emission('MAT_FX_DARK_ARCG', dc, 5), size=.15, count=8))
        light_at(c, dc, 120)
    elif stage == 'deactivation':
        glow(.8, 1.2, .1)
        fx(vx.flames('DARK_RESID', FX, hands, M['dark'], count=5, length=.06, width=.012))


def p_laser(stage, M):
    pose('NEUTRAL' if stage == 'deactivation' else 'CAST_L'); turn(20)
    hand = bone('middle_01_L'); f0 = hand_dir('L')
    fwd = Vector((f0.x if abs(f0.x) > .2 else .8, f0.y * .25, f0.z)).normalized()   # beam reads side-on
    core, g = PAL.get('laser_core', '#F2FFF4'), PAL.get('laser', '#39FF6A')
    src = hand + fwd * .05
    if stage == 'activation':
        glow(2, 3, 0)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=.03 * S, location=src)
        o = bpy.context.object; o.name = 'FX_LASER_CHARGE'; ck.link(o, FX); ck.assign(o, ck.emission('MAT_FX_LCH', core, 25))
        fx(vx.aura_arcs('LASER_SPARK', FX, [src], ck.emission('MAT_FX_LSP', core, 20), ck.emission('MAT_FX_LSG', g, 6), size=.05, count=5))
        light_at(src, g, 40)
    elif stage == 'full':
        glow(4, 5, 0)
        fx(vx.laser('LASER', FX, src, src + fwd * 2.2 * S, core, g, radius=.010 * S))
    elif stage == 'deactivation':
        glow(1, 1.2, 0)
        fx(vx.laser('LASER', FX, src, src + fwd * .5, core, g, radius=.003, intensity=.25, impact=False, charge=False))


def p_teleport(stage, M):
    pose('NEUTRAL'); turn(20)
    col = PAL.get('teleport', '#B57BFF')
    base = (0, 0, 0)
    if stage == 'activation':
        glow(1.5, 2, 0)
        fx(vx.teleport_rings('TP', FX, base, top_z(), col, intensity=.5, rings=3, sparks=20))
        fx(vx.distortion_sphere('FX_TP_WARP', FX, (0, -.05, top_z() * .55), .55 * S))
    elif stage in ('full', 'deactivation'):
        glow(3, 4, 0)
        fx(vx.teleport_rings('TP', FX, base, top_z(), col, intensity=1.2 if stage == 'full' else .7, rings=6, sparks=60))


def p_invisibility(stage, M):
    pose('NEUTRAL'); turn(20); glow(0, 1, 0)


POWERS = {k[2:]: v for k, v in globals().items() if k.startswith('p_')}


def g_powers(St):
    global FX
    studio(St, dark=True)
    FX = ck.get_coll(f'VFX_{CID}_SHEET')
    M = mats()
    ck.setup_render((900, 1120), SAMPLES)
    cam = ck.camera('CAM_PWR', St, (0, -12, top_z() / 2), (0, 0, top_z() / 2), ortho=max(2.3, top_z() * 1.25))
    clear_fx(); pose('NEUTRAL'); turn(20); glow(0, 1, 0)
    save('power_normal.png', cam)
    for key in CFG['power_rows']:
        fn = POWERS[key]
        if key == 'invisibility':
            # base + fully refractive pass; the composer dissolves between them per stage
            clear_fx(); fn('full', M); save('power_invisibility_base.png', cam)
            bpy.context.view_layer.material_override = vx.invisibility_material('MAT_FX_INVIS', PAL.get('power_glow', '#9A7BFF'))
            ck.world_color('#1B2230', .5)
            save('power_invisibility_glass.png', cam)
            bpy.context.view_layer.material_override = None
            ck.world_color('#0B0E14', .15)
            continue
        for stage in ('activation', 'full', 'deactivation'):
            clear_fx(); fn(stage, M)
            if key == 'teleport' and stage != 'activation':
                # character-only and fx-only passes; composer dissolves the body into motes
                bpy.context.scene.render.film_transparent = True
                fxo = [o for o in FX.objects]
                for o in fxo:
                    o.hide_render = True
                save(f'power_teleport_{stage}_char.png', cam)
                for o in fxo:
                    o.hide_render = False
                chars = [o for o in bpy.data.objects if o.name.startswith(f'CHAR_{CID}')]
                for o in chars:
                    o.hide_render = True
                bpy.context.scene.render.film_transparent = False
                save(f'power_teleport_{stage}_fx.png', cam)
                for o in chars:
                    o.hide_render = False
                continue
            save(f'power_{key}_{stage}.png', cam)
        if key == 'speed':
            clear_fx(); fn('full', M)
            for o in list(FX.objects):
                bpy.data.objects.remove(o)
            bpy.context.scene.render.film_transparent = True
            for k, dx in enumerate((-.38, -.76)):
                rig().location.x = dx * S
                save(f'power_speed_afterimage_{k}.png', cam)
            rig().location.x = 0
            bpy.context.scene.render.film_transparent = False
    # hand close-ups (one per power)
    ck.setup_render((700, 560), SAMPLES)
    for key in CFG['power_rows']:
        clear_fx()
        POWERS[key]('full' if key not in ('invisibility', 'teleport') else 'activation', M)
        sd = 'R' if 'portal' in key else 'L'
        if key in ('speed', 'fire', 'dark_magic'):
            h = bone(f'hand_{sd}'); c = ck.camera('CAM_HAND', St, h + Vector((0, -1.1, .1)), h, lens=50)
        else:
            h = bone(f'hand_{sd}'); c = ck.camera('CAM_HAND', St, h + Vector((.05 if sd == 'L' else -.10, -.55, .12)), h, lens=70)
        if key == 'invisibility':
            save('hand_invisibility_base.png', c)
            bpy.context.view_layer.material_override = vx.invisibility_material('MAT_FX_INVIS', PAL.get('power_glow', '#9A7BFF'))
            save('hand_invisibility_glass.png', c)
            bpy.context.view_layer.material_override = None
        else:
            save(f'hand_{key}.png', c)
        bpy.data.objects.remove(c)
    # eyes
    clear_fx(); pose('NEUTRAL'); turn(0)
    ck.setup_render((900, 420), SAMPLES)
    h = head_c() + Vector((0, 0, .004))
    sc = CFG.get('head', {}).get('size', 1) * S ** .3
    c = ck.camera('CAM_EYES', St, h + Vector((0, -.42 * sc, 0)), h, lens=85)
    for label, g in (('normal', 0), ('activation', 1.5), ('full', 3.0)):
        glow(g, 1 + g, g * .3); save(f'eyes_{label}.png', c)
    glow(0, 1, 0)
    clear_fx()


def g_extras(St):
    """Saithan: borrowed-power life-cost — three alternative visual languages for approval."""
    if not CFG.get('cost_alts'):
        return
    global FX
    studio(St, dark=True)
    FX = ck.get_coll(f'VFX_{CID}_SHEET')
    M = mats()
    ck.setup_render((700, 900), SAMPLES)
    pose('POWER_UP'); turn(15)
    h = head_c()
    cam = ck.camera('CAM_COST', St, h + Vector((0, -2.3 * S, -.35 * S)), h + Vector((0, 0, -.38 * S)), lens=50)
    skin = bpy.data.materials[f'MAT_{CID}_SKIN']
    bs = skin.node_tree.nodes['BSDF']
    orig = tuple(bs.inputs['Base Color'].default_value)
    nodes, links = skin.node_tree.nodes, skin.node_tree.links
    # A: glowing fracture veins spreading over the skin
    vor = nodes.new('ShaderNodeTexVoronoi'); vor.feature = 'DISTANCE_TO_EDGE'; vor.inputs['Scale'].default_value = 22
    tc = nodes.new('ShaderNodeTexCoord'); links.new(tc.outputs['Object'], vor.inputs['Vector'])
    rmp = nodes.new('ShaderNodeValToRGB')
    rmp.color_ramp.elements[0].position = 0.0; rmp.color_ramp.elements[0].color = (1, 1, 1, 1)
    rmp.color_ramp.elements[1].position = 0.012; rmp.color_ramp.elements[1].color = (0, 0, 0, 1)
    links.new(vor.outputs['Distance'], rmp.inputs['Fac'])
    mul = nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 6
    links.new(rmp.outputs['Color'], mul.inputs[0])
    bs.inputs['Emission Color'].default_value = ck.hexlin(PAL.get('cost', '#FF3B1F'))
    lk = links.new(mul.outputs[0], bs.inputs['Emission Strength'])
    clear_fx(); fx(vx.aura_arcs('COST_A', FX, anchors(['forearm_L', 'forearm_R']), M['core'], M['glow'], size=.1, count=6))
    save('cost_A_fracture_veins.png', cam)
    links.remove(lk); bs.inputs['Emission Strength'].default_value = 0
    # B: life drained — skin greys / ashes, eyes dim, dark under-eye
    for l in list(links):
        if l.to_socket == bs.inputs['Base Color']:
            links.remove(l)
    bs.inputs['Base Color'].default_value = ck.hexlin(PAL.get('cost_ash', '#6E6A6E'))
    clear_fx(); fx(vx.flames('COST_B', FX, anchors(['forearm_L', 'forearm_R', 'spine_03']), M['dark'], count=20, length=.12, width=.02))
    glow(.3, .3, 0)
    save('cost_B_ash_drain.png', cam)
    # C: chest core siphons out — energy pulled from the core into the borrowed power, core dims
    bs.inputs['Base Color'].default_value = orig
    nodes_mix = [n for n in nodes if n.type == 'MIX']
    if nodes_mix:
        links.new(nodes_mix[0].outputs['Result'], bs.inputs['Base Color'])
    clear_fx(); glow(1, .25, 0)
    core = bone('spine_03', True) + Vector((0, -.14 * S, -.06 * S))
    for sd in ('L', 'R'):
        fx(vx.lightning(f'COST_C_{sd}', FX, core, bone(f'middle_01_{sd}'), M['core'], M['glow'], seed=7 if sd == 'L' else 9,
                        branches=2, radius=.003))
    save('cost_C_core_siphon.png', cam)
    glow(0, 1, 0); clear_fx(); pose('NEUTRAL'); turn(0)


def g_tests(St):
    """Animation / deformation test poses (Stage 6-7 QC)."""
    studio(St)
    ck.setup_render((640, 760), SAMPLES, transparent=True)
    for p, d in (('RUN', 70), ('JUMP', 30), ('LAND', 30), ('TURN', 0), ('FIGHT', 30), ('DEFORM_TEST', 30)):
        pose(p); turn(d)
        cam = full_cam(St)
        save(f'test_{p.lower()}.png', cam)
        bpy.data.objects.remove(cam)
    turn(0)
    F = cb.face_of(CID)
    ck.setup_render((420, 480), SAMPLES, transparent=True)
    pose('NEUTRAL'); turn(10)
    cam = face_cam(St, dist=.62, dz=-.01)
    for ph in cb.PHONEMES:
        cb.set_phoneme(F, ph)
        save(f'lipsync_{ph}.png', cam)
    cb.set_expression(F, 'neutral'); turn(0)


GROUPS = {'qc': g_qc, 'turn': g_turn, 'poses': g_poses, 'face': g_face, 'expr': g_expr, 'costume': g_costume,
          'powers': g_powers, 'extras': g_extras, 'tests': g_tests}

if __name__ == '__main__':
    want = [a for a in sys.argv[2:] if a in GROUPS] or [g for g in GROUPS if g != 'tests']
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    St = ck.get_coll('STUDIO')
    for g in want:
        if g == 'powers' and not CFG.get('power_rows'):
            continue
        print('=== GROUP', g, flush=True)
        GROUPS[g](St)
    print('DONE', want, flush=True)

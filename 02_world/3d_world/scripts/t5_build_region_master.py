"""TASK 05 · milestone 2 REGION master (Blender 4.5): links a region component into its own scene with the shared T5 look
(HDRI sky + matching sun, aerial-perspective compositor) and the region's cinematic cameras.
  blender -b -P t5_build_region_master.py -- R04      → 00_MASTER_WORLD/T5_REGION_R04_DESERT_master_v002.blend
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk
import t5kit as tk

RK = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'R04'
CFG = {'R04': dict(file='06_DESERTS/DESERT_R04_v002.blend', coll='T5_DESERT_R04', data='06_DESERTS/data_v002',
                   out='T5_REGION_R04_DESERT_master_v002.blend', sun=(232.0, 12.0), tiles=('DH', 'DN', 'DF')),
       'R05': dict(file='06_DESERTS/FORBIDDEN_R05_v002.blend', coll='T5_FORBIDDEN_R05', data='06_DESERTS/data_v002',
                   out='T5_REGION_R05_FORBIDDEN_master_v002.blend', sun=(250.0, 14.0), tiles=('XH', 'XN', 'XF')),
       'R02': dict(file='04_FORESTS/ENCHANTED_FOREST_R02_v002.blend', coll='T5_ENCHANTED_R02', data='04_FORESTS/data_v002',
                   out='T5_REGION_R02_ENCHANTED_master_v002.blend', sun=(240.0, 34.0), tiles=('EH', 'EN', 'EF')),
       'R03': dict(file='03_MOUNTAINS/GREAT_NORTHERN_RANGE_R03_v002.blend', coll='T5_RANGE_R03', data='08_ASHRAM_VALLEY/data_v002',
                   out='T5_REGION_R03_RANGE_master_v002.blend', sun=(215.0, 26.0), tiles=())}[RK]
DD = wk.P(*CFG['data'].split('/'))
if RK == 'R03':                                  # R03 lives in the Ashram-local frame (t5_prep tiles R3N / R3F)
    PJ = json.load(open(os.path.join(DD, 'prep_v002.json')))
    RJ = dict(name='Great Northern Range (core)', frame=PJ['frame'] + ' (R03 tiles R3N / R3F)', tiles={})
else:
    RJ = json.load(open(os.path.join(DD, f'region_{RK}.json')))
wk.new_file()
sc = bpy.context.scene; sc.name = f'T5_REGION_{RK}'
sc['status'] = f'TASK 05 milestone 2 — {RJ["name"]} (map revision 01 = PROPOSAL)'; sc['frame'] = RJ['frame']
c = wk.link_collections(wk.P(*CFG['file'].split('/')), [CFG['coll']])[CFG['coll']]
sc.collection.children.link(c)
cams = wk.coll('T5_CAMERAS'); light = wk.coll('T5_LIGHTING')
TL = {k: (np.load(os.path.join(DD, f'{k}.npz')), RJ['tiles'][k]) for k in CFG['tiles']}
R3 = {k: np.load(os.path.join(DD, f'{k}.npz'))['z'] for k in ('CV', 'R3N', 'R3F')} if RK == 'R03' else {}


def ground(x, y):
    if RK == 'R03':
        for k in ('CV', 'R3N', 'R3F'):
            t = PJ['tile_defs'][k]
            if t['x0'] <= x <= t['x1'] and t['y0'] <= y <= t['y1']:
                z = R3[k]; sp = t['sp']; c_ = (x - t['x0']) / sp; r_ = (t['y1'] - y) / sp
                return float(z[int(min(r_, z.shape[0] - 1)), int(min(c_, z.shape[1] - 1))])
    for k, (D, t) in TL.items():
        h = t['half']
        if abs(x) <= h and abs(y) <= h:
            z = D['z']; sp = t['sp']; c_ = (x + h) / sp; r_ = (h - y) / sp
            c0, r0 = int(min(c_, z.shape[1] - 2)), int(min(r_, z.shape[0] - 2)); fx, fy = c_ - c0, r_ - r0
            return float(z[r0, c0] * (1 - fx) * (1 - fy) + z[r0, c0 + 1] * fx * (1 - fy) + z[r0 + 1, c0] * (1 - fx) * fy + z[r0 + 1, c0 + 1] * fx * fy)
    raise ValueError((x, y))


# ---------------------------------------------------------------- sky + sun (same method as the milestone-1 master)
SUN_AZ, SUN_EL = CFG['sun']
hdr = os.path.join(tk.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr')
img = bpy.data.images.load(hdr, check_existing=True); w_, h_ = img.size
px = np.empty(w_ * h_ * 4, np.float32); img.pixels.foreach_get(px)
yy, xx = np.unravel_index(np.argmax(px.reshape(h_, w_, 4)[..., :3].sum(-1)), (h_, w_))
phi = ((xx + .5) / w_ - .5) * 2 * math.pi; el = ((yy + .5) / h_ - .5) * math.pi
dh = np.array([-math.cos(phi) * math.cos(el), math.sin(phi) * math.cos(el)])
az = math.radians(SUN_AZ); rot = math.atan2(dh[1], dh[0]) - math.atan2(math.cos(az), math.sin(az))
wd = bpy.data.worlds.new('T5_SKY'); sc.world = wd; wd.use_nodes = True; nt = wd.node_tree; nt.nodes.clear(); b = tk.NB(nt)
tc = b.node('ShaderNodeTexCoord'); mp = b.node('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, rot)
b.link(tc.outputs['Generated'], mp.inputs['Vector'])
env = b.node('ShaderNodeTexEnvironment'); env.image = img; b.link(mp.outputs[0], env.inputs['Vector'])
bg = b.node('ShaderNodeBackground'); b.link(env.outputs['Color'], bg.inputs['Color'])
o_ = b.node('ShaderNodeOutputWorld'); b.link(bg.outputs[0], o_.inputs['Surface'])
wk.sun('T5_SUN', SUN_EL, SUN_AZ, 4.6, light, .55, (1.0, .94, .86))
wd.mist_settings.start = 0; wd.mist_settings.depth = 60000; wd.mist_settings.falloff = 'LINEAR'
C = []


def cam(name, loc, tgt, lens, desc, haze_depth, haze_strength, samples=48):
    o = wk.camera(name, loc, tgt, lens, cams, clip=(.05, 300000)); o.data.sensor_width = 36.0
    o['description'] = desc; o['haze_depth_m'] = haze_depth; o['haze_strength'] = haze_strength; o['samples'] = samples
    C.append(o)


if RK == 'R04':
    D, t = TL['DH']; z = D['z']; sp = t['sp']; h = t['half']
    m = 150
    r, c_ = np.unravel_index(np.argmax(z[m:-m, m:-m]), z[m:-m, m:-m].shape); r += m; c_ += m
    bx, by, bz = -h + c_ * sp, h - r * sp, float(z[r, c_])                       # the butte / mesa in the hero tile
    ang = math.radians(135); dst = 1250
    cx, cy = bx + math.sin(ang) * dst, by + math.cos(ang) * dst
    cx, cy = float(np.clip(cx, -h + 60, h - 60)), float(np.clip(cy, -h + 60, h - 60))
    cam('CAM_T5_05_DESERT', (cx, cy, ground(cx, cy) + 55), (bx, by, bz - 90), 35,
        'Desert landscape — R04 Western Desert: wind-shaped dune field, sandstone butte with strata, desert pavement', 60000, .3)
    cx2, cy2 = 1500.0, -10500.0
    cam('CAM_T5_05B_DESERT_MESAS_AERIAL', (cx2, cy2, ground(cx2, cy2) + 260), (0, 6000, ground(0, 6000) + 40), 30,
        'Desert aerial — dune seas between mesas / buttes, dry wadis and playas (cracked ground)', 120000, .35)
    sc['butte'] = [bx, by, bz]
if RK == 'R05':
    lev = list(RJ['lakes'].values())[0] if RJ.get('lakes') else 490.0
    cx, cy = -700.0, -2250.0                                                # on the rim, just behind the lip of the ~150 m inner wall
    cam('CAM_T5_09_FORBIDDEN_RIM', (cx, cy, ground(cx, cy) + 25), (600, 2500, lev - 25), 26,
        'Forbidden Region (R05) — from the blasted rim: the steep inner crater wall falls to the black crater lake; ejecta blocks, fissures, ash', 120000, .2)
    cx2, cy2 = 3600.0, -300.0                                               # low over the black lake, close to the inner crater wall
    cam('CAM_T5_09B_FORBIDDEN_AERIAL', (cx2, cy2, lev + 30), (2900, -1800, lev + 95), 30,
        'Forbidden Region — the ~150 m inner crater wall rising from the black crater lake, ejecta on the rim above', 60000, .15)
if RK == 'R02':
    cx, cy = 200.0, -300.0
    cam('CAM_T5_10_ENCHANTED_FLOOR', (cx, cy, ground(cx, cy) + 1.6), (cx - 80, cy + 110, ground(cx - 80, cy + 110) + 6), 22,
        'Enchanted Forest (R02) — inside the old-growth: giant trunks, moss carpet, ferns, fallen giants, low mist', 6000, .15, 64)
    cx2, cy2 = 1300.0, -2600.0
    cam('CAM_T5_10B_ENCHANTED_CANOPY', (cx2, cy2, ground(cx2, cy2) + 140), (-1500, 4000, ground(-1500, 4000) + 30), 28,
        'Enchanted Forest canopy — giant old-growth over rolling hills, deep teal-green', 60000, .3)
if RK == 'R03':
    t = PJ['tile_defs']['R3N']; z = R3['R3N']; m = 250
    r, c_ = np.unravel_index(np.argmax(z[m:-m, m:-m]), z[m:-m, m:-m].shape); r += m; c_ += m
    px, py, pz = t['x0'] + c_ * t['sp'], t['y1'] - r * t['sp'], float(z[r, c_])
    for nm, ang, dst, dz, lens, desc in (
            ('CAM_T5_11_RANGE_PEAKS', 165, 9000, -500, 38, f'Great Northern Range (R03) core — highest summit ({pz:.0f} m) and its glaciated neighbours from the SSE'),
            ('CAM_T5_11B_RANGE_PANORAMA', 150, 12500, -1500, 24, 'Great Northern Range panorama — ridges, glaciers, forested lower valleys')):
        a = math.radians(ang); cx, cy = px + math.sin(a) * dst, py + math.cos(a) * dst
        cz = max(ground(cx, cy) + 200, pz + dz)
        cam(nm, (cx, cy, cz), (px, py, pz - 600 if dst > 10000 else pz - 400), lens, desc, 150000, .3)
    tcv = PJ['tile_defs']['CV']; zc = np.load(os.path.join(DD, 'CV.npz'))['z']
    CXc, CYc = 11990.0, 339100.0
    ci = int(round((CXc - tcv['x0']) / tcv['sp'])); ri = int(round((tcv['y1'] - CYc) / tcv['sp']))
    angs = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    ring = [zc[int(round((tcv['y1'] - (CYc + 70 * math.sin(a_))) / tcv['sp'])), int(round((CXc + 70 * math.cos(a_) - tcv['x0']) / tcv['sp']))] for a_ in angs]
    a_up = angs[int(np.argmax(ring))]; upv = np.array([math.cos(a_up), math.sin(a_up)])
    gzc = float(zc[ri, ci])
    ex, ey = CXc - upv[0] * 40 + upv[1] * 5, CYc - upv[1] * 40 - upv[0] * 5
    ezg = float(zc[int(round((tcv['y1'] - ey) / tcv['sp'])), int(round((ex - tcv['x0']) / tcv['sp']))])
    cam('CAM_T5_12_CAVE_ENTRANCE', (ex, ey, max(ezg + 1.7, gzc + 3.0)), (CXc - upv[0] * 8, CYc - upv[1] * 8, gzc + 4), 28,
        'Cave entrance (map cave marker in the Great Northern Range foothills) — rock outcrop, arched mouth, forest clearing', 6000, .15, 64)
sc.camera = C[0]
wk.setup_cycles(sc, (1280, 720), 48)
cy_ = sc.cycles
cy_.max_bounces = 6; cy_.diffuse_bounces = 2; cy_.glossy_bounces = 2; cy_.transmission_bounces = 6; cy_.transparent_max_bounces = 48
cy_.sample_clamp_indirect = 8.0; cy_.use_adaptive_sampling = True; cy_.adaptive_threshold = .02
sc.render.film_transparent = True
vl = sc.view_layers[0]; vl.use_pass_mist = True
try:
    vl.use_pass_environment = True
except Exception:
    pass
sc.use_nodes = True; ct = sc.node_tree; ct.nodes.clear(); b = tk.NB(ct)
rl = b.node('CompositorNodeRLayers'); env_s = next((s for s in rl.outputs if s.name in ('Env', 'Environment')), None)
hz = b.node('CompositorNodeValue'); hz.name = 'HAZE_STRENGTH'; hz.outputs[0].default_value = .3
HAZE_COL = (0.78, 0.74, 0.70)


def M(op, a_, b2=None, clamp=False):
    n = b.node('CompositorNodeMath', operation=op, use_clamp=clamp)
    for i, v in enumerate((a_, b2)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            b.link(v, n.inputs[i])
    return n.outputs[0]
alpha = rl.outputs['Alpha']
mt = M('MINIMUM', M('MAXIMUM', M('DIVIDE', M('ADD', M('SUBTRACT', rl.outputs['Mist'], 1.0), alpha), M('MAXIMUM', alpha, .001)), 0.0), 1.0)
om = M('SUBTRACT', 1.0, mt)
f_ = M('MULTIPLY', M('SUBTRACT', 1.0, M('MULTIPLY', om, om)), hz.outputs[0], clamp=True)
hzc = b.node('CompositorNodeMixRGB', blend_type='MULTIPLY'); hzc.inputs[0].default_value = 1.0
hzc.inputs[1].default_value = HAZE_COL + (1.0,); b.link(alpha, hzc.inputs[2])
mix = b.node('CompositorNodeMixRGB', blend_type='MIX'); b.link(f_, mix.inputs[0]); b.link(rl.outputs['Image'], mix.inputs[1]); b.link(hzc.outputs[0], mix.inputs[2])
sa = b.node('CompositorNodeSetAlpha'); b.link(mix.outputs[0], sa.inputs['Image']); b.link(alpha, sa.inputs['Alpha'])
try:
    sa.mode = 'REPLACE_ALPHA'
except Exception:
    pass
ao = b.node('CompositorNodeAlphaOver'); ao.use_premultiply = False; b.link(env_s, ao.inputs[1]); b.link(sa.outputs[0], ao.inputs[2])
gl = b.node('CompositorNodeGlare', glare_type='FOG_GLOW', quality='MEDIUM'); gl.threshold = 1.2; gl.size = 7
b.link(ao.outputs[0], gl.inputs['Image'])
co = b.node('CompositorNodeComposite'); b.link(gl.outputs[0], co.inputs['Image'])
wk.viewport_defaults(sc, 300000)
wk.save(wk.P('00_MASTER_WORLD', CFG['out']))
print('CAMS', [(o.name, [round(v) for v in o.location]) for o in C])
print('T5_REGION_MASTER_DONE', RK)

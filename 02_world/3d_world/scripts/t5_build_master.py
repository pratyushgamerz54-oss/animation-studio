"""TASK 05 · MASTER LANDSCAPE → 00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend (Blender 4.5 LTS).

Links the four production components (valley, forest belt, mountain NW01, water) into scene T5_LANDSCAPE and adds the shared
lighting (Poly Haven HDRI sky rotated so its sun matches the sun lamp), cinematic test cameras (same lens family, eye heights in
metres, true scale) and the compositor (aerial perspective from the mist pass, over the environment pass; light glare).
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
from mathutils import Vector
import worldkit as wk
import t5kit as tk

DATA = wk.P('08_ASHRAM_VALLEY', 'data_v002')
PREP = json.load(open(os.path.join(DATA, 'prep_v002.json'))); TD = PREP['tile_defs']
SUN_AZ, SUN_EL = 215.0, 31.0                    # afternoon sun from the SSW → side light for views toward the N / NW range
HAZE_COL = (0.62, 0.70, 0.80)

wk.new_file()
sc = bpy.context.scene; sc.name = 'T5_LANDSCAPE'
sc['status'] = 'TASK 05 milestone 1 — detailed Ashram Valley, northern forest belt, mountain region NW01 (map rev 01 = PROPOSAL)'
for f, cname in (('08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend', 'T5_VALLEY'), ('04_FORESTS/FOREST_NORTH_BELT_v002.blend', 'T5_FOREST_NORTH'),
                 ('03_MOUNTAINS/MOUNTAIN_NW01_v002.blend', 'T5_MOUNTAIN_NW'), ('05_RIVERS_AND_LAKES/WATER_v002.blend', 'T5_WATER')):
    c = wk.link_collections(wk.P(*f.split('/')), [cname])[cname]
    sc.collection.children.link(c)
cams = wk.coll('T5_CAMERAS'); light = wk.coll('T5_LIGHTING')

# ------------------------------------------------------------------ terrain height lookup (finest tile first) for camera placement
TL = {k: np.load(os.path.join(DATA, f'{k}.npz')) for k in ('WF', 'VH', 'FH', 'L0', 'L1', 'MT', 'L2')}


def ground(x, y):
    for k, D in TL.items():
        t = TD[k]
        if t['x0'] <= x <= t['x1'] and t['y0'] <= y <= t['y1']:
            z = D['z']; sp = t['sp']
            c = (x - t['x0']) / sp; r = (t['y1'] - y) / sp
            c0, r0 = int(min(c, z.shape[1] - 2)), int(min(r, z.shape[0] - 2)); fx, fy = c - c0, r - r0
            return float(z[r0, c0] * (1 - fx) * (1 - fy) + z[r0, c0 + 1] * fx * (1 - fy) + z[r0 + 1, c0] * (1 - fx) * fy + z[r0 + 1, c0 + 1] * fx * fy)
    raise ValueError((x, y))


def mask(k, ch, x, y):
    t = TD[k]; D = TL[k]; sp = t['sp']
    c = int(round((x - t['x0']) / sp)); r = int(round((t['y1'] - y) / sp))
    return D[ch[0:2]][r, c, int(ch[2])] / 255.0


# ------------------------------------------------------------------ lighting: HDRI + matching sun
hdr = os.path.join(tk.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr')
img = bpy.data.images.load(hdr, check_existing=True)
w_, h_ = img.size
px = np.empty(w_ * h_ * 4, np.float32); img.pixels.foreach_get(px)
lum = px.reshape(h_, w_, 4)[..., :3].sum(-1)
yy, xx = np.unravel_index(np.argmax(lum), lum.shape)
u, v = (xx + .5) / w_, (yy + .5) / h_
phi_h = (u - .5) * 2 * math.pi; el_h = (v - .5) * math.pi
dh = np.array([-math.cos(phi_h) * math.cos(el_h), math.sin(phi_h) * math.cos(el_h), math.sin(el_h)])   # Blender equirect convention
phi_hdr = math.atan2(dh[1], dh[0])
az = math.radians(SUN_AZ)
phi_t = math.atan2(math.cos(az), math.sin(az))
rot = phi_hdr - phi_t
wd = bpy.data.worlds.new('T5_SKY'); sc.world = wd; wd.use_nodes = True
nt = wd.node_tree; nt.nodes.clear(); b = tk.NB(nt)
tc = b.node('ShaderNodeTexCoord'); mp = b.node('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, rot)
b.link(tc.outputs['Generated'], mp.inputs['Vector'])
env = b.node('ShaderNodeTexEnvironment'); env.image = img; b.link(mp.outputs[0], env.inputs['Vector'])
bg = b.node('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 1.0
b.link(env.outputs['Color'], bg.inputs['Color'])
out = b.node('ShaderNodeOutputWorld'); b.link(bg.outputs[0], out.inputs['Surface'])
sun_el = max(math.degrees(el_h), 20.0) if abs(math.degrees(el_h) - SUN_EL) > 25 else math.degrees(el_h)
sun = wk.sun('T5_SUN', SUN_EL, SUN_AZ, 4.2, light, .55, (1.0, .955, .9))
sc['sun'] = dict(azimuth_deg=SUN_AZ, elevation_deg=SUN_EL, hdri=os.path.basename(hdr), hdri_rot_z_rad=rot, hdri_sun_elev_deg=math.degrees(el_h))
wd.mist_settings.start = 0; wd.mist_settings.depth = 60000; wd.mist_settings.falloff = 'LINEAR'

# ------------------------------------------------------------------ cameras
C = []


def cam(name, loc, tgt, lens, desc, haze_depth, haze_strength, samples=48):
    o = wk.camera(name, loc, tgt, lens, cams, clip=(.05, 450000))
    o['description'] = desc; o['haze_depth_m'] = haze_depth; o['haze_strength'] = haze_strength; o['samples'] = samples
    o.data.sensor_width = 36.0
    C.append(o)
    return o


# summit of NW01 (used by shots 1 and 4)
MT = TL['MT']['z']; t = TD['MT']; m = 200
sub = MT[m:-m, m:-m]; r, c = np.unravel_index(np.argmax(sub), sub.shape); r += m; c += m
px_, py_ = t['x0'] + c * t['sp'], t['y1'] - r * t['sp']; pz = float(MT[r, c])
sc['nw01_summit'] = [px_, py_, pz]
# 1 wide mountain landscape — panorama of the NW01 range from a high shoulder ≈16 km SSE of the summit
ang = math.radians(152); dist = 16000
x, y = px_ + math.sin(ang) * dist, py_ + math.cos(ang) * dist
cam('CAM_T5_01_MOUNTAIN_WIDE', (x, y, max(ground(x, y) + 180, pz - 1500)), (px_ - 2500, py_ + 1500, pz - 1300), 24,
    'Wide mountain landscape — the NW01 range (snowy range ≈100 km NW of the Ashram) from a high shoulder south of the main summit', 150000, .3)
# 2 forest establishing — the river leaving the northern forest belt (forest hero tile FH)
x, y = 700.0, 24150.0
gz = ground(x, y)
cam('CAM_T5_02_FOREST_ESTABLISHING', (x, y, gz + 45), (-350, 25700, ground(-350, 25700) + 8), 24,
    'Forest establishing shot — edge of the northern forest belt where the river enters it (FH, 2 m terrain + real trees)', 40000, .22)
# 3 river + waterfall — looking upstream at the featured fall in the NW01 gorge (WF, 1.5 m terrain)
f = PREP['featured_waterfalls'][0]
d = np.array([f['out_x'] - f['x'], f['out_y'] - f['y']]); d /= np.linalg.norm(d); side = np.array([-d[1], d[0]])
p = np.array([f['out_x'], f['out_y']]) + d * 170 + side * 45
cz = max(ground(*p), f['z_bottom']) + 22
cam('CAM_T5_03_RIVER_WATERFALL', (p[0], p[1], cz), (f['lip_x'], f['lip_y'], f['z_top'] - .45 * (f['z_top'] - f['z_bottom'])), 26,
    f'River + waterfall — featured fall ({f["z_top"] - f["z_bottom"]:.0f} m drop, largest of the network in NW01) and its plunge pool', 3000, .25)
# 4 snowy mountain — highest summit of NW01, from the south-south-east, side-lit by the afternoon sun
ang = math.radians(160); dist = 7800
cx, cy = px_ + math.sin(ang) * dist, py_ + math.cos(ang) * dist
cam('CAM_T5_04_SNOWY_PEAKS', (cx, cy, pz - 250), (px_, py_, pz - 450), 42,
    f'Snowy mountain — highest summit of NW01 ({pz:.0f} m) from the SSE, glaciers / couloirs / rock bands', 120000, .22)
# 6 valley aerial — over the Ashram toward the northern forest belt and the range on the horizon
cam('CAM_T5_06_VALLEY_AERIAL', (3800, -6200, ground(3800, -6200) + 420), (-9000, 14000, 760), 32,
    'Valley aerial — Ashram Valley from the SE: open green floor, groves, the rivers, the northern forest belt, the range on the horizon', 150000, .3)
# 7 ground level — meadow by the river next to the Ashram pad (VH, 2 m terrain, grass + flowers + stones)
W = np.load(os.path.join(DATA, 'water.npz')); RIV = W['RIV']
k = (np.abs(RIV[:, 0]) < 1100) & (np.abs(RIV[:, 1]) < 1100)
R = RIV[k]; j = np.argmin(np.abs(R[:, 1] + 300) + np.abs(R[:, 0]) * .01)
rp = R[j]; rdir = R[min(j + 6, len(R) - 1), :2] - R[max(j - 6, 0), :2]; rdir /= np.linalg.norm(rdir)
if rdir[1] < 0:
    rdir = -rdir                                                       # look upstream/north along the river
rs = np.array([rdir[1], -rdir[0]])                                     # right-hand side of the look direction
cp = rp[:2] + rs * (rp[3] * .7 + 60) - rdir * 20
tg = rp[:2] + rdir * 260 + rs * 25
cam('CAM_T5_07_GROUND_LEVEL', (cp[0], cp[1], ground(*cp) + 1.6), (tg[0], tg[1], ground(*tg) + 2.5), 28,
    'Ground level (1.6 m eye) — river meadow beside the Ashram pad: grass, wild flowers, river stones, groves, range on the horizon', 60000, .2, 64)
# 8 forest floor — inside the forest hero tile among the trees
best = None
for yy_ in np.arange(25000, 26600, 40.0):
    for xx_ in np.arange(-1200, 1200, 40.0):
        v_ = mask('FH', 'MA0', xx_, yy_)
        if v_ > .97 and mask('FH', 'MB0', xx_, yy_) < .02:
            best = (xx_, yy_); break
    if best:
        break
fx, fy = best
cam('CAM_T5_08_FOREST_FLOOR', (fx, fy, ground(fx, fy) + 1.6), (fx - 60, fy + 90, ground(fx - 60, fy + 90) + 3.0), 24,
    'Ground level in the forest — forest floor, ferns, roots, fallen logs, mossy rocks, fir / pine trunks', 3000, .15, 64)
sc.camera = C[0]

# ------------------------------------------------------------------ render + compositor
wk.setup_cycles(sc, (1280, 720), 48)
cy_ = sc.cycles
cy_.max_bounces = 6; cy_.diffuse_bounces = 2; cy_.glossy_bounces = 2; cy_.transmission_bounces = 6; cy_.transparent_max_bounces = 48
cy_.volume_bounces = 1; cy_.sample_clamp_indirect = 8.0; cy_.use_adaptive_sampling = True; cy_.adaptive_threshold = .02
try:
    cy_.use_light_tree = True
except Exception:
    pass
sc.render.film_transparent = True
vl = sc.view_layers[0]; vl.use_pass_mist = True; vl.cycles.use_pass_environment = True if hasattr(vl.cycles, 'use_pass_environment') else None
try:
    vl.use_pass_environment = True
except Exception:
    pass
sc.use_nodes = True
ct = sc.node_tree; ct.nodes.clear(); b = tk.NB(ct)
rl = b.node('CompositorNodeRLayers')
env_s = next((s for s in rl.outputs if s.name in ('Env', 'Environment')), None)
hz = b.node('CompositorNodeValue'); hz.name = 'HAZE_STRENGTH'; hz.outputs[0].default_value = .45
# aerial perspective on the PREMULTIPLIED render: recover the surface mist at anti-aliased edges
# m_t = (mist − (1 − α)) / α  → no bright outline along silhouettes against the sky
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
mt = M('DIVIDE', M('ADD', M('SUBTRACT', rl.outputs['Mist'], 1.0), alpha), M('MAXIMUM', alpha, .001))
mt = M('MINIMUM', M('MAXIMUM', mt, 0.0), 1.0)
om = M('SUBTRACT', 1.0, mt)
f_ = M('MULTIPLY', M('SUBTRACT', 1.0, M('MULTIPLY', om, om)), hz.outputs[0], clamp=True)
hzc = b.node('CompositorNodeMixRGB', blend_type='MULTIPLY'); hzc.inputs[0].default_value = 1.0
hzc.inputs[1].default_value = HAZE_COL + (1.0,); b.link(alpha, hzc.inputs[2])
mix = b.node('CompositorNodeMixRGB', blend_type='MIX'); b.link(f_, mix.inputs[0]); b.link(rl.outputs['Image'], mix.inputs[1])
b.link(hzc.outputs[0], mix.inputs[2])
sa = b.node('CompositorNodeSetAlpha'); b.link(mix.outputs[0], sa.inputs['Image']); b.link(alpha, sa.inputs['Alpha'])
try:
    sa.mode = 'REPLACE_ALPHA'
except Exception:
    pass
ao = b.node('CompositorNodeAlphaOver'); ao.use_premultiply = False
b.link(env_s, ao.inputs[1]); b.link(sa.outputs[0], ao.inputs[2])
gl = b.node('CompositorNodeGlare', glare_type='FOG_GLOW', quality='MEDIUM'); gl.threshold = 1.2; gl.size = 7
try:
    gl.mix = -.85
except Exception:
    pass
b.link(ao.outputs[0], gl.inputs['Image'])
co = b.node('CompositorNodeComposite'); b.link(gl.outputs[0], co.inputs['Image'])
vw = b.node('CompositorNodeViewer'); b.link(gl.outputs[0], vw.inputs['Image'])
sc['cameras'] = json.dumps({o.name: dict(loc=list(o.location), desc=o['description']) for o in C})
wk.viewport_defaults(sc, 450000)
wk.save(wk.P('00_MASTER_WORLD', 'T5_LANDSCAPE_master_v002.blend'))
print('CAMS', [(o.name, [round(v) for v in o.location]) for o in C])
print('T5_MASTER_DONE')

"""TASK 06 · render the reference views for the vegetation sheets (Blender 4.5, Cycles CPU).

    BPY45 t6_render_sheets.py -- AV|EF|MK|PL|LK|DS|FB|CT|CV [asset names…]   (env SPP=32, ONLY=views|lineup|closeups)

Per tree / shrub:  front · side · back (orthographic, calm wind, shadow-catcher ground, 1.75 m scale figure in the front view)
                   leaf close-up (perspective) · trunk-foot close-up (roots meeting a real forest-floor ground)
Per plant:         hero 3/4 view on a soil ground with a 10 cm grid · detail close-up
Per region:        LINEUP_TREES (orthographic height comparison) · LINEUP_PLANTS
Output: 03_assets/vegetation/renders/<REGION>/<asset>_<view>.png + views.json (camera → metres mapping for the rulers).
"""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, bmesh
from mathutils import Vector
import t6kit as K

args = sys.argv[sys.argv.index('--') + 1:]
REG = args[0]; SEL = set(args[1:])
NAMES = {'AV': 'ASHRAM_VALLEY', 'EF': 'ENCHANTED_FOREST', 'MK': 'MOUNTAIN_KINGDOM',
         'PL': 'GREEN_PLAINS', 'LK': 'CRYSTAL_LAKES', 'DS': 'GOLDEN_DESERT', 'FB': 'FORBIDDEN_LANDS',
         'CT': 'ANCIENT_CITY_SITES', 'CV': 'HIDDEN_UNDERGROUND'}          # = t6_regions.NAMES
# trunk-foot close-up ground per region (real Poly Haven scan the tree actually grows in): texture, metres per tile, tint
BASE_GROUND = {'PL': ('sparse_grass', 3.0, '#FFFFFF'), 'LK': ('brown_mud_leaves_01', 2.5, '#FFFFFF'), 'DS': ('dry_ground_01', 3.0, '#FFFFFF'),
               'FB': ('mud_cracked_dry_03', 3.0, '#6A6560'), 'CT': ('grass_path_2', 3.0, '#FFFFFF'), 'CV': ('rock_ground', 2.5, '#FFFFFF')}
LIBF = os.path.join(K.VEG, 'library', f'T6_VEG_{NAMES[REG]}_v001.blend')
OUTD = os.path.join(K.VEG, 'renders', REG); os.makedirs(OUTD, exist_ok=True)
SPP = int(os.environ.get('SPP', 32)); ONLY = os.environ.get('ONLY', '')
FRESH = os.environ.get('SKIP_FRESH', '') == '1'     # resume after an interrupted run: skip assets whose renders are newer than the library
LIB_T = os.path.getmtime(LIBF)
fresh = lambda files: FRESH and all(os.path.exists(f) and os.path.getmtime(f) > LIB_T for f in files)
bpy.ops.wm.open_mainfile(filepath=LIBF)
ctrl = bpy.data.objects['T6_WIND_CONTROL']; ctrl['strength'] = 0.0            # calm for reference views
INV = json.load(open(LIBF[:-6].replace('_v001', '') + '_inventory.json'))
VJ = os.path.join(OUTD, 'views.json')
VIEWS = json.load(open(VJ)) if os.path.exists(VJ) else {}

sc = bpy.data.scenes.new('T6_SHEET')
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.transparent_max_bounces = 64; sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2
K.camera_look(sc)                     # natural camera look (Director 22 Nov)
sc.render.film_transparent = True; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.frame_set(1)
# ---------------------------------------------------------------- world + sun
w = bpy.data.worlds.new('T6_SHEET_WORLD'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment')
env.image = bpy.data.images.load(os.path.join(K.PH, 'hdris', 'kloofendal_48d_partly_cloudy_puresky', 'kloofendal_48d_partly_cloudy_puresky_4k.exr'))
mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord'); mp.inputs['Rotation'].default_value[2] = math.radians(140)
nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
nt.links.new(env.outputs['Color'], nt.nodes['Background'].inputs['Color']); nt.nodes['Background'].inputs['Strength'].default_value = .75
sun = bpy.data.objects.new('T6_SUN', bpy.data.lights.new('T6_SUN', 'SUN')); sc.collection.objects.link(sun)
sun.data.energy = 3.6; sun.data.angle = math.radians(2.5); sun.data.color = (1, .96, .9)
sun.rotation_euler = (math.radians(48), 0, math.radians(-38))
# ---------------------------------------------------------------- grounds
def plane(name, size, mat):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2); bm.to_mesh(me); bm.free()
    me.uv_layers.new(name='UVMap')
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); me.materials.append(mat); return o
catcher = plane('T6_GROUND_CATCHER', 2000, K.mat_simple('MAT_T6_CATCHER', '#808080')); catcher.is_shadow_catcher = True


def ground_mat(name, tex, scale, grid=None, tint='#FFFFFF'):
    m, nt_, b = K.new_mat(name); M = K.bark_maps(tex)
    out = b.n('ShaderNodeOutputMaterial'); bs = b.n('ShaderNodeBsdfPrincipled')
    geo = b.n('ShaderNodeNewGeometry'); vm = b.n('ShaderNodeVectorMath', operation='SCALE'); b.l(geo.outputs['Position'], vm.inputs[0])
    vm.inputs['Scale'].default_value = 1 / scale
    T = {}
    for k, p in M.items():
        t = b.n('ShaderNodeTexImage'); t.image = K.img(p, k != 'diff'); b.l(vm.outputs['Vector'], t.inputs['Vector']); T[k] = t
    col = b.mix(1.0, T['diff'].outputs['Color'], K.hexc(tint), 'MULTIPLY')
    if grid:      # thin grid lines every `grid` metres (scale reference), every 10th line stronger
        sep = b.n('ShaderNodeSeparateXYZ'); b.l(geo.outputs['Position'], sep.inputs[0]); lines = None
        for ax in ('X', 'Y'):
            f = b.math('DIVIDE', sep.outputs[ax], grid); fr = b.math('FRACT', b.math('ADD', f, .5))
            d = b.math('ABSOLUTE', b.math('SUBTRACT', fr, .5))
            ln = b.math('LESS_THAN', d, .018)
            lines = ln if lines is None else b.math('MAXIMUM', lines, ln)
        col = b.mix(b.math('MULTIPLY', lines, .55), col, (1, 1, 1, 1))
    b.l(col, bs.inputs['Base Color']); b.l(T['rough'].outputs['Color'], bs.inputs['Roughness'])
    nm = b.n('ShaderNodeNormalMap'); b.l(T['nor_gl'].outputs['Color'], nm.inputs['Color']); b.l(nm.outputs['Normal'], bs.inputs['Normal'])
    b.l(bs.outputs[0], out.inputs['Surface'])
    return m


_bg = BASE_GROUND.get(REG, ('forest_ground_04', 3.0, '#FFFFFF'))
forest_floor = plane('T6_GROUND_FOREST', 400, ground_mat('MAT_T6_GROUND_FOREST', _bg[0], _bg[1], tint=_bg[2]))
soil = plane('T6_GROUND_GRID', 60, ground_mat('MAT_T6_GROUND_GRID', 'brown_mud', 1.5, grid=.1, tint='#C8BCA8'))


# ---------------------------------------------------------------- 1.75 m scale figure (neutral mannequin)
def mannequin():
    G = K.Geo(); at = dict(wind_trunk=0.0)
    def cap(c, axis, r, h):
        K.lathe(G, [(r * .2, -r * .9), (r * .8, -r * .6), (r, 0), (r, h), (r * .8, h + r * .6), (r * .2, h + r * .9)], Vector(c), Vector(axis), 12, 0, {})
    for sx in (-1, 1):
        cap((sx * .1, 0, .06), (0, 0, 1), .065, .78)        # legs
        cap((sx * .23, 0, .82), (sx * .12, 0, 1), .045, .52) # arms
    cap((0, 0, .95), (0, 0, 1), .16, .42)                   # torso
    K.lathe(G, [(.01, 0), (.075, .02), (.105, .11), (.1, .19), (.06, .25), (.01, .26)], Vector((0, 0, 1.49)), Vector((0, 0, 1)), 14, 0, {})
    me = G.to_mesh('T6_SCALE_FIGURE_1m75', [K.mat_simple('MAT_T6_FIGURE', '#B9B4AA', rough=.6)])
    o = bpy.data.objects.new('T6_SCALE_FIGURE_1m75', me); sc.collection.objects.link(o); return o
fig = mannequin()


def cam_obj():
    c = bpy.data.objects.new('T6_CAM', bpy.data.cameras.new('T6_CAM')); sc.collection.objects.link(c); sc.camera = c
    c.data.clip_start = .01; c.data.clip_end = 5000; return c
cam = cam_obj()


def look(c, loc, target, lens=50):
    c.data.type = 'PERSP'; c.data.sensor_fit = 'AUTO'; c.data.lens = lens; c.location = loc
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def render(path, rx, ry):
    sc.render.resolution_x, sc.render.resolution_y = rx, ry; sc.render.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True, scene=sc.name); print('RENDER', os.path.basename(path), round(time.time() - t, 1), 's', flush=True)


def show(objs):
    for o in sc.collection.objects:
        if o.type == 'MESH':
            o.hide_render = o not in objs
    sun.hide_render = False


def bounds(o):
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
    L = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', L)
    C = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('center', C); C = C.reshape(-1, 3)
    oe.to_mesh_clear()
    return V + np.array(o.location), L, C + np.array(o.location)


def ortho_views(o, name, kind):
    V, L, C = bounds(o)
    mn, mx = V.min(0), V.max(0); H = mx[2]; z0 = max(mn[2], -.6) if kind != 'plant' else -.05
    RX, RY = 600, 840; out = {}
    for view, rot, axis in (('front', (90, 0, 0), 0), ('side', (90, 0, 90), 1), ('back', (90, 0, 180), 0)):
        wmin, wmax = (mn[0], mx[0]) if axis == 0 else (mn[1], mx[1])
        zr = (H - z0) * 1.08 + .3; wr = (wmax - wmin) * 1.08 + .3
        if view == 'front':
            fx = mx[0] + max(.6, (mx[0] - mn[0]) * .06) + .3; fig.location = (fx, mn[1] - .5, 0); wr = (fx + .5 - wmin) * 1.06
            wmax = fx + .5
        osc = max(zr, wr * RY / RX); zc = z0 + zr / 2 - .15
        cw = (wmin + wmax) / 2
        cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'VERTICAL'; cam.data.ortho_scale = osc; cam.rotation_euler = [math.radians(a) for a in rot]
        D = 1500
        cam.location = {'front': (cw, -D, zc), 'side': (D, cw, zc), 'back': (-cw, D, zc)}[view] if view != 'back' else (cw, D, zc)
        show([o, catcher] + ([fig] if view == 'front' else []))
        p = os.path.join(OUTD, f'{name}_{view}.png'); render(p, RX, RY)
        out[view] = dict(ortho_scale=osc, zc=zc, rx=RX, ry=RY, px_per_m=RY / osc if osc >= wr * RY / RX * 0 else RY / osc)
    return out, V, L, C


def tree_closeups(o, name, V, L, C):
    H = V[:, 2].max(); res = {}
    leafc = C[L == 1]
    if len(leafc):
        sel = leafc[(leafc[:, 2] > .4 * H) & (leafc[:, 2] < .8 * H)]
        sel = sel if len(sel) > 20 else leafc
        tgt = sel[np.argmin(sel[:, 1] + np.abs(sel[:, 0]) * .3)]
        d = 1.3 if H > 3 else .5
        look(cam, (tgt[0] + .25 * d, tgt[1] - d, tgt[2] + .15 * d), tuple(tgt), 50)
        show([o, catcher]); render(os.path.join(OUTD, f'{name}_leaf.png'), 600, 600); res['leaf'] = True
    td = float(o.get('t6_trunk_d_m', 1.0)); d = max(2.2, td * 2.4) if H > 3 else max(.8, td * 1.5)
    tgt = Vector((0, 0, min(.35 * td + .3, H * .25)))
    look(cam, (d * .55, -d, tgt.z + d * .3), tgt, 35)
    show([o, forest_floor]); render(os.path.join(OUTD, f'{name}_base.png'), 600, 600); res['base'] = True
    return res


def plant_views(o, name):
    V, L, C = bounds(o); mn, mx = V.min(0), V.max(0); H = max(mx[2], .03); Wd = max(mx[0] - mn[0], mx[1] - mn[1], .05)
    size = max(H, Wd * .7)
    tgt = Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, H * .4)); d = size * 2.1 + .05
    look(cam, (tgt.x + d * .55, tgt.y - d, tgt.z + d * .45), tgt, 50)
    show([o, soil]); render(os.path.join(OUTD, f'{name}_hero.png'), 700, 700)
    # detail: the top 25 % (flower heads / blade tips / caps)
    top = V[V[:, 2] > mx[2] - .25 * H]; c = top.mean(0) if len(top) else np.array(tgt)
    dd = max(size * .8, .14)
    look(cam, (c[0] + dd * .4, c[1] - dd, c[2] + dd * .35), tuple(c), 60)
    show([o, soil]); render(os.path.join(OUTD, f'{name}_detail.png'), 700, 700)
    return dict(hero=True, detail=True, height_m=float(H), spread_m=float(Wd))


def lineup(kind):
    """height-comparison lineup of every tree + shrub (front ortho) or every plant (perspective)."""
    names = [n for n, v in INV.items() if (v['kind'] in ('tree', 'shrub')) == (kind == 'trees') and 'hanging' not in v['category']]
    names.sort(key=lambda n: -INV[n]['stats']['height_m'])
    objs = []; x = 0.0
    for n in names:
        o = bpy.data.objects[n]; st = INV[n]['stats']; w = max(st.get('canopy_x_m', st.get('spread_x_m', .3)), .3)
        inst = bpy.data.objects.new(f'LU_{n}', None); inst.instance_type = 'COLLECTION'; inst.instance_collection = bpy.data.collections[f'T6_{n}']
        gap = w * .08 + (1.0 if kind == 'trees' else .06)
        inst.location = (x + w / 2, 0, 0); sc.collection.objects.link(inst); objs.append(inst); x += w + gap
    for o in sc.collection.objects:
        if o.type == 'MESH':
            o.hide_render = True
    if kind == 'trees':
        fig.hide_render = False; fig.location = (x + .5, 0, 0); catcher.hide_render = False
        Hm = max(INV[n]['stats']['height_m'] for n in names); RX, RY = 2400, 900
        zr = Hm * 1.1 + 1; wr = (x + 1.5) * 1.03; osc = max(zr * RX / RY, wr)
        cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'HORIZONTAL'; cam.data.ortho_scale = osc; cam.rotation_euler = (math.radians(90), 0, 0)
        zc = -.6 + (osc * RY / RX) / 2
        cam.location = ((x + 1.5) / 2, -1500, zc)
        render(os.path.join(OUTD, 'LINEUP_TREES.png'), RX, RY)
        VIEWS['LINEUP_TREES'] = dict(ortho_scale=osc, zc=zc, rx=RX, ry=RY, px_per_m=RX / osc, cx=(x + 1.5) / 2, items=[
            dict(name=n, x=o.location.x) for n, o in zip(names, objs)])
    else:
        soil.hide_render = False
        Hm = max(INV[n]['stats']['height_m'] for n in names)
        tgt = Vector((x / 2, 0, Hm * .2)); d = x * .95
        look(cam, (x / 2, -d, Hm * .55 + d * .18), tgt, 40)
        render(os.path.join(OUTD, 'LINEUP_PLANTS.png'), 2400, 900)
    for o in objs:
        bpy.data.objects.remove(o)


for name, v in INV.items():
    if SEL and name not in SEL:
        continue
    if ONLY == 'lineup':
        break
    views = ('front', 'side', 'back', 'base') if v['kind'] in ('tree', 'shrub') else ('hero', 'detail')
    if fresh([os.path.join(OUTD, f'{name}_{k}.png') for k in views]) and name in VIEWS:
        print('FRESH (skip)', name, flush=True); continue
    o = bpy.data.objects[name]
    sc.collection.objects.link(o)
    if v['kind'] in ('tree', 'shrub') and ONLY == 'closeups':      # only the leaf close-up (texture detail); ortho views kept
        V, L, C = bounds(o); ov = dict(VIEWS.get(name, {})); ov.update(tree_closeups(o, name, V, L, C))
    elif v['kind'] in ('tree', 'shrub'):
        ov, V, L, C = ortho_views(o, name, v['kind'])
        ov.update(tree_closeups(o, name, V, L, C))
    else:
        ov = plant_views(o, name)
    VIEWS[name] = ov
    sc.collection.objects.unlink(o)
    json.dump(VIEWS, open(VJ, 'w'), indent=1)
if ONLY in ('', 'lineup') and not SEL:   # (closeups mode never re-renders the lineups)
    for k in ('trees', 'plants'):
        if not fresh([os.path.join(OUTD, f'LINEUP_{k.upper()}.png')]):
            lineup(k)
json.dump(VIEWS, open(VJ, 'w'), indent=1)
print('T6_RENDER_DONE', REG)

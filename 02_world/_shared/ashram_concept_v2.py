"""ASHRAM — concept v2 (PROPOSAL, real metres): detailed look-development pass of the approved-for-review layout.

Run:  python3 02_world/_shared/ashram_concept_v2.py [samples] [--no-render] [--only CAM_A,CAM_B]
Out:  02_world/ashram/01_BLOCKOUT/ASHRAM_concept_v002.blend
      02_world/ashram/09_RENDER/concept_v2/*.png

Same layout + local origin as v1 (ashram_blockout.py), but with:
- architecture detail: moulded stone plinths, carved octagonal timber pillars with bracket capitals, timber frames,
  lattice windows, double doors with brass rings, clay-tile roofs (tile bump + eave rafters + ridge / hip caps + eave tiles),
  brass finials, prayer-flag strings, stone lamp pillars, clay pots, benches;
- realistic procedural materials (envkit): coursed stone with moss, grimy lime plaster, aged timber, mossy tiles, stone flags;
- landscape: 4 km valley tile + 30 km far range with snow, Himalayan conifer forests, broadleaf trees, grass clumps, rocks
  (all instanced with geometry nodes), lake;
- atmosphere: haze volume, valley mist volume, cloud layer, golden-hour sun / night lanterns.
Everything is still a PROPOSAL for the Director.
"""
import os, sys, math, json, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '01_characters', '_shared'))
sys.path.insert(0, HERE)
import charkit as ck
import envkit as ek
from ashram_blockout import C, mesh_box, mesh_cyl, obj, inst, roof_mesh, fbm2, ROOT

args = [a for a in sys.argv[1:] if not a.startswith('-')]
SAMPLES = int(args[0]) if args else 24
RENDER = '--no-render' not in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
OUTR = os.path.join(ROOT, '09_RENDER', 'concept_v2'); os.makedirs(OUTR, exist_ok=True)
R = random.Random(5)


# ======================================================================= materials
def materials():
    T = ek.textures()
    M = {'stone': ek.mat_coursed_stone(), 'flags': ek.mat_stone_flags(), 'plaster': ek.mat_plaster(), 'timber': ek.mat_timber(),
         'timber_dark': ek.mat_timber('MAT_ENV_TIMBER_DARK', '#4A2E19', '#24160C'), 'tile': ek.mat_roof_tiles(),
         'terracotta': ek.mat_simple('MAT_ENV_TERRACOTTA', '#9A4A2A', .6), 'brass': ek.mat_simple('MAT_ENV_BRASS', '#C9A040', .28, 1.0),
         'dark': ek.mat_simple('MAT_ENV_INTERIOR_DARK', '#120C08', .9), 'clay': ek.mat_simple('MAT_ENV_CLAY_POT', '#8E4E2E', .7),
         'water': ek.mat_water(), 'terrain': ek.mat_terrain(snow_z=(1150, 1350)),
         'far': ek.mat_terrain('MAT_ENV_TERRAIN_FAR', snow_z=(2300, 2700), world_scale=4.0),
         'path': ek.mat_terrain('MAT_ENV_PATH_EARTH'), 'bark': ek.mat_bark(),
         'leaf': ek.mat_card('MAT_ENV_LEAF', T['leaf'], '#5E7A3A', '#86984A'),
         'needles': ek.mat_card('MAT_ENV_NEEDLES', T['needles'], '#4E6E3E', '#6E8A4C', trans=.2),
         'grass': ek.mat_grass(), 'rock': ek.mat_terrain('MAT_ENV_ROCK'),
         'lantern': ek.mat_simple('MAT_ENV_LANTERN_GLOW', '#FFE2B0', .5, emit='#FFB35A', strength=0.0)}
    for i, hx in enumerate(('#D8342C', '#2E6FD0', '#F2C230', '#2E9A4A', '#F4F0E6')):
        M[f'flag{i}'] = ek.mat_simple(f'MAT_ENV_PRAYER_FLAG_{i}', hx, .8)
    # path: plain trodden earth
    pm = bpy.data.materials['MAT_ENV_PATH_EARTH']; nt = pm.node_tree
    nt.links.new(ek.N(pm).ramp(ek.N(pm).noise(ek.N(pm).coord('Object'), 1.5, 8), [(.3, '#6E5A40'), (.7, '#A08460')]),
                 nt.nodes['Principled BSDF'].inputs['Base Color'])
    return M


# ======================================================================= detailed modules
def bm_obj(name, bm, coll, mat, smooth=False):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if mat:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    o = bpy.data.objects.new(name, me); coll.objects.link(o); return o


def add_box(bm, c, s):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(Vector(c)) @ Matrix.Diagonal((s[0], s[1], s[2], 1)))


def add_cyl(bm, c, r, h, n=8, r2=None):
    bmesh.ops.create_cone(bm, cap_ends=True, segments=n, radius1=r, radius2=r if r2 is None else r2, depth=h,
                          matrix=Matrix.Translation(Vector(c) + Vector((0, 0, h / 2))))


def modules(M):
    K = C('ASHRAM/02_ARCHITECTURE/MODULES'); A = {}
    # carved octagonal pillar 3.2 m (shaft + rings) — timber
    bm = bmesh.new()
    add_cyl(bm, (0, 0, 0), .17, 3.2, 8)
    for z in (.25, .55, 2.55, 2.85):
        add_cyl(bm, (0, 0, z), .2, .08, 8)
    add_cyl(bm, (0, 0, 2.95), .23, .12, 8, .28)
    A['pillar'] = bm_obj('ASSET_PILLAR_TIMBER_CARVED', bm, K, M['timber'], smooth=False)
    # bracket capital: abacus + crossed brackets
    bm = bmesh.new(); add_box(bm, (0, 0, .08), (.6, .6, .16)); add_box(bm, (0, 0, .26), (1.5, .2, .2)); add_box(bm, (0, 0, .26), (.2, 1.5, .2))
    add_box(bm, (0, 0, .4), (1.1, .26, .1))
    A['capital'] = bm_obj('ASSET_PILLAR_CAPITAL_BRACKET', bm, K, M['timber_dark'])
    # moulded stone pillar base
    bm = bmesh.new(); add_box(bm, (0, 0, .09), (.62, .62, .18)); add_box(bm, (0, 0, .25), (.5, .5, .14)); add_cyl(bm, (0, 0, .32), .24, .08, 12)
    A['pbase'] = bm_obj('ASSET_PILLAR_BASE_STONE', bm, K, M['stone'])
    # stone gate pillar
    bm = bmesh.new(); add_box(bm, (0, 0, .2), (1.0, 1.0, .4)); add_cyl(bm, (0, 0, .4), .36, 4.0, 8); add_box(bm, (0, 0, 4.5), (.95, .95, .2))
    A['spillar'] = bm_obj('ASSET_PILLAR_STONE_GATE', bm, K, M['stone'])
    # boundary wall 4 m with coping
    bm = bmesh.new(); add_box(bm, (0, 0, .7), (4.0, .5, 1.4)); add_box(bm, (0, 0, 1.46), (4.04, .62, .12))
    A['wall'] = bm_obj('ASSET_WALL_SEG_4M', bm, K, M['stone'])
    A['step'] = obj('ASSET_STAIR_STEP', mesh_box('ASSET_STAIR_STEP', 1.0, .4, .18), K, mat=M['stone'])
    # lattice window 1.2 x 1.4: frame + 6 bars + dark recess + sill
    bm = bmesh.new()
    add_box(bm, (0, -.02, .7), (1.2, .06, 1.4))
    me_dark = bm_obj('ASSET_WINDOW_RECESS', bm, K, M['dark'])
    bm = bmesh.new()
    for x in (-.65, .65):
        add_box(bm, (x, -.08, .7), (.12, .14, 1.6))
    for z in (-.08, 1.48):
        add_box(bm, (0, -.08, z), (1.5, .16, .14))
    for k in range(6):
        add_box(bm, (-.5 + k * .2, -.07, .7), (.05, .05, 1.4))
    add_box(bm, (0, -.07, .7), (1.2, .05, .05))
    A['window'] = bm_obj('ASSET_WINDOW_LATTICE', bm, K, M['timber_dark'])
    A['window_recess'] = me_dark
    # double door 1.8 x 2.7 with frame + brass rings
    bm = bmesh.new()
    for x in (-.97, .97):
        add_box(bm, (x, -.1, 1.4), (.16, .2, 2.9))
    add_box(bm, (0, -.1, 2.88), (2.2, .24, .24))
    for x in (-.45, .45):
        add_box(bm, (x, -.03, 1.35), (.88, .08, 2.7))
        for z in (.6, 1.35, 2.1):
            add_box(bm, (x, -.08, z), (.7, .04, .5))
    A['door'] = bm_obj('ASSET_DOOR_DOUBLE', bm, K, M['timber'])
    bm = bmesh.new()
    for x in (-.12, .12):
        bmesh.ops.create_circle(bm, cap_ends=False, segments=12, radius=.07,
                                matrix=Matrix.Translation((x, -.13, 1.35)) @ Matrix.Rotation(math.pi / 2, 4, 'X'))
    A['door_ring'] = bm_obj('ASSET_DOOR_RINGS', bm, K, M['brass'])
    m = A['door_ring'].modifiers.new('Skin', 'WIREFRAME'); m.thickness = .02
    # eave tile end, rafter end, ridge cap segment
    A['eave_tile'] = obj('ASSET_EAVE_TILE', mesh_cyl('ASSET_EAVE_TILE', .11, .45, 8), K, rot=(math.pi / 2, 0, 0), mat=M['terracotta'])
    A['rafter'] = obj('ASSET_RAFTER_END', mesh_box('ASSET_RAFTER_END', .1, .9, .14), K, mat=M['timber_dark'])
    # stone lamp pillar (deepastambha-like), clay pot, bench, lantern
    bm = bmesh.new(); add_box(bm, (0, 0, .15), (.7, .7, .3)); add_cyl(bm, (0, 0, .3), .16, 2.2, 8)
    for z in (.9, 1.5, 2.1):
        add_cyl(bm, (0, 0, z), .34, .06, 12)
    add_cyl(bm, (0, 0, 2.5), .22, .3, 8, .05)
    A['lamp_pillar'] = bm_obj('ASSET_STONE_LAMP_PILLAR', bm, K, M['stone'])
    bm = bmesh.new()
    prof = [(0, .0), (.13, .02), (.2, .12), (.21, .22), (.17, .32), (.09, .38), (.1, .42)]
    rings = []
    for (rr, z) in prof:
        rings.append([bm.verts.new((rr * math.cos(a), rr * math.sin(a), z)) for a in np.linspace(0, 2 * math.pi, 16, endpoint=False)])
    for i in range(len(rings) - 1):
        for k in range(16):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % 16], rings[i + 1][(k + 1) % 16], rings[i + 1][k]))
    A['pot'] = bm_obj('ASSET_CLAY_POT', bm, K, M['clay'], smooth=True)
    bm = bmesh.new(); add_box(bm, (0, 0, .42), (1.8, .4, .07)); add_box(bm, (-.75, 0, .2), (.1, .36, .4)); add_box(bm, (.75, 0, .2), (.1, .36, .4))
    A['bench'] = bm_obj('ASSET_BENCH_TIMBER', bm, K, M['timber'])
    A['lantern'] = obj('ASSET_LANTERN', mesh_box('ASSET_LANTERN', .26, .26, .38), K, mat=M['lantern'])
    K.hide_render = True; K.hide_viewport = True
    for o in K.objects:
        o['asset_kit'] = True
    return A


def roof_details(name, A, M, g, root, W, D, z, over, rise_frac):
    """eave tiles + rafter ends along the eaves and caps on ridge/hips for a roof shell of size W x D at height z."""
    W2, D2 = W / 2 + over, D / 2 + over
    out = []
    step = .3
    for side, (x0, y0, x1, y1, nrm) in {'S': (-W2, -D2, W2, -D2, (0, -1)), 'N': (-W2, D2, W2, D2, (0, 1)),
                                         'W': (-W2, -D2, -W2, D2, (-1, 0)), 'E': (W2, -D2, W2, D2, (1, 0))}.items():
        L = math.hypot(x1 - x0, y1 - y0); n = int(L / step)
        ang = math.atan2(nrm[1], nrm[0]) - math.pi / 2
        for i in range(1, n):
            t = i / n; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            o = inst(A['eave_tile'], f'{name}_EAVE_{side}_{i:03d}', g, (x, y, z + .05), rot=(math.pi / 2 - .35, 0, ang))
            o.parent = root; out.append(o)
            if i % 2 == 0:
                r = inst(A['rafter'], f'{name}_RAFTER_{side}_{i:03d}', g, (x - nrm[0] * .5, y - nrm[1] * .5, z - .22), rot=(0, 0, ang))
                r.parent = root; out.append(r)
    return out


def building(name, A, M, c, w, d, wall_h=3.4, plinth=1.0, tiers=2, verandah=2.4, rot=0.0, door_side='S', rise=3.2):
    g = C('ASHRAM/02_ARCHITECTURE')
    root = bpy.data.objects.new(name, None); g.objects.link(root); root.location = (c[0], c[1], 0); root.rotation_euler = (0, 0, rot)
    parts = []

    def add(o):
        o.parent = root; parts.append(o); return o
    W, D = w + 2 * verandah, d + 2 * verandah
    # moulded plinth: base course, body, coping
    bm = bmesh.new()
    add_box(bm, (0, 0, .15), (W + 1.4, D + 1.4, .3)); add_box(bm, (0, 0, plinth / 2), (W + .9, D + .9, plinth)); add_box(bm, (0, 0, plinth - .06), (W + 1.1, D + 1.1, .12))
    add(bm_obj(f'{name}_PLINTH', bm, g, M['stone']))
    fl = obj(f'{name}_FLOOR', mesh_box(f'{name}_FLOOR', W + .8, D + .8, .04), g, (0, 0, plinth), mat=M['flags']); add(fl)
    add(obj(f'{name}_WALLS', mesh_box(f'{name}_WALLS', w, d, wall_h), g, (0, 0, plinth), mat=M['plaster']))
    # timber frame: corner posts, sill band, top band
    bm = bmesh.new()
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(bm, (sx * w / 2, sy * d / 2, plinth + wall_h / 2), (.3, .3, wall_h))
    for zz, hh in ((plinth + .12, .24), (plinth + wall_h - .2, .4)):
        add_box(bm, (0, 0, zz), (w + .12, d + .12, hh))
    add(bm_obj(f'{name}_TIMBER_FRAME', bm, g, M['timber_dark']))
    # verandah pillars
    nx_, ny_ = max(2, round(W / 3.0)), max(2, round(D / 3.0))
    pts = set()
    for i in range(nx_ + 1):
        x = -W / 2 + .4 + (W - .8) * i / nx_
        pts |= {(round(x, 3), round(-D / 2 + .4, 3)), (round(x, 3), round(D / 2 - .4, 3))}
    for j in range(ny_ + 1):
        y = -D / 2 + .4 + (D - .8) * j / ny_
        pts |= {(round(-W / 2 + .4, 3), round(y, 3)), (round(W / 2 - .4, 3), round(y, 3))}
    sz = (wall_h - .4) / 3.2
    for k, (x, y) in enumerate(sorted(pts)):
        add(inst(A['pbase'], f'{name}_PBASE_{k:02d}', g, (x, y, plinth)))
        add(inst(A['pillar'], f'{name}_PILLAR_{k:02d}', g, (x, y, plinth + .36), scale=(1, 1, sz)))
        add(inst(A['capital'], f'{name}_CAPITAL_{k:02d}', g, (x, y, plinth + .36 + 3.2 * sz - .05), rot=(0, 0, 0 if abs(abs(y) - (D / 2 - .4)) < .01 else math.pi / 2)))
    # verandah beam ring on the capitals
    bm = bmesh.new(); zb = plinth + .36 + 3.2 * sz + .4
    for sy in (-1, 1):
        add_box(bm, (0, sy * (D / 2 - .4), zb), (W - .6, .3, .34))
    for sx in (-1, 1):
        add_box(bm, (sx * (W / 2 - .4), 0, zb), (.3, D - .6, .34))
    add(bm_obj(f'{name}_VERANDAH_BEAM', bm, g, M['timber_dark']))
    # roofs
    z = plinth + wall_h + .15
    r1 = add(obj(f'{name}_ROOF_1', roof_mesh(f'{name}_ROOF_1', W, D, rise * .55, over=1.3, flare=.4), g, (0, 0, z), mat=M['tile']))
    parts += roof_details(f'{name}_R1', A, M, g, root, W, D, z, 1.3, .55)
    if tiers > 1:
        add(obj(f'{name}_ROOF_DRUM', mesh_box(f'{name}_ROOF_DRUM', w * .62, d * .62, 1.6), g, (0, 0, z + rise * .25), mat=M['plaster']))
        bm = bmesh.new()
        for k in range(int(w * .62 / .9)):
            add_box(bm, (-w * .31 + .45 + k * .9, -d * .31 - .02, z + rise * .25 + .8), (.12, .06, 1.4))
            add_box(bm, (-w * .31 + .45 + k * .9, d * .31 + .02, z + rise * .25 + .8), (.12, .06, 1.4))
        add(bm_obj(f'{name}_DRUM_POSTS', bm, g, M['timber_dark']))
        z2 = z + rise * .25 + 1.6
        add(obj(f'{name}_ROOF_2', roof_mesh(f'{name}_ROOF_2', w * .62, d * .62, rise * .75, over=1.0, flare=.45), g, (0, 0, z2), mat=M['tile']))
        parts += roof_details(f'{name}_R2', A, M, g, root, w * .62, d * .62, z2, 1.0, .75)
        add(obj(f'{name}_FINIAL', mesh_cyl(f'{name}_FINIAL', .25, 1.6, 12, r2=.02), g, (0, 0, z2 + rise * .75), mat=M['brass']))
        add(obj(f'{name}_FINIAL_POT', mesh_cyl(f'{name}_FINIAL_POT', .32, .35, 12, r2=.2), g, (0, 0, z2 + rise * .75 - .1), mat=M['brass']))
    for o in parts:
        if o.data and o.type == 'MESH' and o.data.name.startswith(f'{name}_ROOF_'):
            s = o.modifiers.new('Solidify', 'SOLIDIFY'); s.thickness = .22
    # door + windows on the door side, windows on the others
    sgn = -1 if door_side == 'S' else 1
    add(inst(A['door'], f'{name}_DOOR', g, (0, sgn * (d / 2 + .02), plinth), rot=(0, 0, 0 if sgn < 0 else math.pi)))
    add(inst(A['door_ring'], f'{name}_DOOR_RINGS', g, (0, sgn * (d / 2 + .02), plinth), rot=(0, 0, 0 if sgn < 0 else math.pi)))
    k = 0
    for side, (axis, off, length) in {'S': ('x', -d / 2, w), 'N': ('x', d / 2, w), 'W': ('y', -w / 2, d), 'E': ('y', w / 2, d)}.items():
        n = max(0, int((length - 2) // 3.2))
        for i in range(n):
            t = -length / 2 + (i + 1) * length / (n + 1)
            if side == ('S' if sgn < 0 else 'N') and abs(t) < 1.8:
                continue
            if axis == 'x':
                loc = (t, off + (-.03 if off < 0 else .03), plinth + 1.0); rr = (0, 0, 0 if off < 0 else math.pi)
            else:
                loc = (off + (-.03 if off < 0 else .03), t, plinth + 1.0); rr = (0, 0, -math.pi / 2 if off < 0 else math.pi / 2)
            add(inst(A['window'], f'{name}_WINDOW_{k:02d}', g, loc, rot=rr)); add(inst(A['window_recess'], f'{name}_WREC_{k:02d}', g, loc, rot=rr)); k += 1
    nst = max(1, round(plinth / .18))
    for s in range(nst):
        add(inst(A['step'], f'{name}_STEP_{s:02d}', g, (0, sgn * (D / 2 + .55 + .4 * (nst - 1 - s)), s * .18), scale=(3.6, 1, 1)))
    return root


def prayer_flags(M, a, b, sag=1.2, n=26, name='PROP_PRAYER_FLAGS'):
    g = C('ASHRAM/04_PROPS'); a, b = Vector(a), Vector(b)
    bm_s = bmesh.new(); pts = []
    for i in range(n + 1):
        t = i / n; p = a.lerp(b, t) - Vector((0, 0, sag * 4 * t * (1 - t))); pts.append(p)
    ek.tube(bm_s, pts, [.008] * len(pts), 4)
    bm_obj(name + '_STRING', bm_s, g, M['timber_dark'])
    for i in range(n):
        p = pts[i].lerp(pts[i + 1], .5); d = (pts[i + 1] - pts[i]).normalized()
        f = obj(f'{name}_{i:02d}', mesh_box(f'{name}_{i:02d}', .32, .004, .4), g, p - Vector((0, 0, .21)),
                rot=(R.uniform(-.15, .15), 0, math.atan2(d.y, d.x)), mat=M[f'flag{i % 5}'])


# ======================================================================= site
def site(A, M):
    out = {}
    out['hall'] = building('ARCH_MAIN_HALL', A, M, (0, 34), 22, 14, wall_h=4.4, plinth=1.6, tiers=2, verandah=3.0, rise=5.4)
    out['res_w'] = building('ARCH_RESIDENCE_W', A, M, (-42, 0), 8, 30, wall_h=3.3, plinth=.8, tiers=1, verandah=2.2, rise=3.0)
    out['res_e'] = building('ARCH_RESIDENCE_E', A, M, (42, 0), 8, 30, wall_h=3.3, plinth=.8, tiers=1, verandah=2.2, rise=3.0)
    out['service'] = building('ARCH_SERVICE_HALL', A, M, (-38, 44), 12, 8, wall_h=3.2, plinth=.6, tiers=1, verandah=1.8, rise=2.6)
    out['library'] = building('ARCH_STUDY_HALL', A, M, (38, 44), 12, 8, wall_h=3.4, plinth=.8, tiers=1, verandah=1.8, rise=2.8)
    g = C('ASHRAM/02_ARCHITECTURE')
    # meditation pavilion (open, 8 pillars) on a moulded plinth
    bm = bmesh.new(); add_box(bm, (62, -78, .2), (12.4, 12.4, .4)); add_box(bm, (62, -78, .75), (11.4, 11.4, 1.1)); add_box(bm, (62, -78, 1.25), (12, 12, .12))
    bm_obj('ARCH_PAVILION_PLINTH', bm, g, M['stone'])
    obj('ARCH_PAVILION_FLOOR', mesh_box('ARCH_PAVILION_FLOOR', 11.2, 11.2, .04), g, (62, -78, 1.3), mat=M['flags'])
    for k, (x, y) in enumerate([(-4.6, -4.6), (4.6, -4.6), (4.6, 4.6), (-4.6, 4.6), (0, -4.6), (0, 4.6), (-4.6, 0), (4.6, 0)]):
        inst(A['pbase'], f'ARCH_PAV_PBASE_{k}', g, (62 + x, -78 + y, 1.3)); inst(A['pillar'], f'ARCH_PAV_PILLAR_{k}', g, (62 + x, -78 + y, 1.66), scale=(1, 1, 1.0))
        inst(A['capital'], f'ARCH_PAV_CAP_{k}', g, (62 + x, -78 + y, 4.8), rot=(0, 0, 0 if abs(y) > 4 else math.pi / 2))
    pr = bpy.data.objects.new('ARCH_PAVILION', None); g.objects.link(pr); pr.location = (62, -78, 0)
    obj('ARCH_PAVILION_ROOF', roof_mesh('ARCH_PAVILION_ROOF', 9.8, 9.8, 4.6, over=1.5, flare=.55), g, (62, -78, 5.4), mat=M['tile']).modifiers.new('S', 'SOLIDIFY').thickness = .22
    roof_details('ARCH_PAV', A, M, g, pr, 9.8, 9.8, 5.4, 1.5, 1)
    obj('ARCH_PAVILION_FINIAL', mesh_cyl('ARCH_PAV_FINIAL', .22, 1.4, 12, r2=.02), g, (62, -78, 10.0), mat=M['brass'])
    # gate
    gz = C('ASHRAM/02_ARCHITECTURE/GATE_AND_WALLS')
    for sx in (-1, 1):
        inst(A['spillar'], f'ARCH_GATE_PILLAR_{"WE"[sx > 0]}', gz, (sx * 3.4, -62, 0))
        inst(A['lamp_pillar'], f'PROP_GATE_LAMP_PILLAR_{"WE"[sx > 0]}', gz, (sx * 7.5, -64.5, 0))
    bm = bmesh.new(); add_box(bm, (0, -62, 4.9), (9.6, 1.1, .6)); add_box(bm, (0, -62, 5.3), (10.2, 1.3, .2))
    bm_obj('ARCH_GATE_LINTEL', bm, gz, M['stone'])
    rg = obj('ARCH_GATE_ROOF', roof_mesh('ARCH_GATE_ROOF', 8.6, 1.6, 1.8, over=.8, flare=.35), gz, (0, -62, 5.4), mat=M['tile'])
    rg.modifiers.new('S', 'SOLIDIFY').thickness = .18
    obj('ARCH_GATE_FINIAL', mesh_cyl('ARCH_GATE_FINIAL', .16, 1.0, 10, r2=.02), gz, (0, -62, 7.2), mat=M['brass'])
    for side, (x0, y0, x1, y1) in {'S_W': (-60, -62, -6, -62), 'S_E': (6, -62, 60, -62), 'W': (-60, -62, -60, 62),
                                     'E': (60, -62, 60, 62), 'N': (-60, 62, 60, 62)}.items():
        L = math.hypot(x1 - x0, y1 - y0); n = int(L // 4); ang = math.atan2(y1 - y0, x1 - x0)
        for i in range(n):
            t = (i + .5) / n
            inst(A['wall'], f'ARCH_WALL_{side}_{i:02d}', gz, (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), rot=(0, 0, ang), scale=(L / n / 4, 1, 1))
    # ground: courtyard flags, paths, training ground, ghat
    gr = C('ASHRAM/03_TERRAIN/GROUND_FEATURES')
    obj('GROUND_COURTYARD_FLAGS', mesh_box('GROUND_COURTYARD', 56, 42, .1), gr, (0, 2, 0), mat=M['flags'])
    obj('GROUND_TRAINING_GROUND', mesh_cyl('GROUND_TRAINING', 22, .06, 64), gr, (0, -100, 0), mat=M['path'])
    obj('GROUND_TRAINING_RING', mesh_cyl('GROUND_TRAINING_RING', 22.6, .3, 64), gr, (0, -100, -.18), mat=M['stone'])
    obj('GROUND_PATH_GATE_TO_COURT', mesh_box('GROUND_PATH_1', 4, 40, .06), gr, (0, -42, 0), mat=M['flags'])
    obj('GROUND_PATH_TO_TRAINING', mesh_box('GROUND_PATH_2', 4.5, 18, .05), gr, (0, -71, 0), mat=M['path'])
    obj('GROUND_PATH_TO_PAVILION', mesh_box('GROUND_PATH_3', 3, 60, .05), gr, (34, -74, 0), rot=(0, 0, math.radians(-62)), mat=M['path'])
    for s in range(12):
        inst(A['step'], f'GHAT_STEP_{s:02d}', gr, (62, -92 - s * .4, -s * .18), scale=(16, 1, 1))
    # props
    pr = C('ASHRAM/04_PROPS')
    bm = bmesh.new(); add_cyl(bm, (0, 4, 0), 4.4, .3, 32); add_cyl(bm, (0, 4, .3), 4.1, .35, 32); bm_obj('PROP_TREE_PLATFORM', bm, pr, M['stone'])
    for k, (x, y) in enumerate([(-6, -60), (6, -60), (-10, 21), (10, 21), (-28, -6), (28, -6), (56, -72), (68, -72)]):
        inst(A['lantern'], f'PROP_LANTERN_{k:02d}', pr, (x, y, 2.2 if abs(y) != 60 else 4.8))
    for k, (x, y, rz) in enumerate([(-14, -8, 0), (14, -8, 0), (-14, 12, 0), (14, 12, 0), (56, -82, math.pi / 2)]):
        inst(A['bench'], f'PROP_BENCH_{k:02d}', pr, (x, y, .1), rot=(0, 0, rz))
    for k in range(9):
        inst(A['pot'], f'PROP_CLAY_POT_{k:02d}', pr, (-31 + (k % 3) * .55, 38 - (k // 3) * .55, .62), scale=(1 + R.uniform(-.2, .3),) * 3)
    for k, x in enumerate((-16, 16)):
        obj(f'PROP_FLAGPOLE_{k}', mesh_cyl(f'PROP_FLAGPOLE_{k}', .07, 11, 8, r2=.04), pr, (x, 22, 0), mat=M['timber_dark'])
    prayer_flags(M, (-16, 22, 10.8), (16, 22, 10.8), sag=1.6, n=40, name='PROP_PRAYER_FLAGS_HALL')
    prayer_flags(M, (-5.6, -62, 5.6), (-16, 22, 10.6), sag=2.2, n=40, name='PROP_PRAYER_FLAGS_W')
    prayer_flags(M, (5.6, -62, 5.6), (16, 22, 10.6), sag=2.2, n=40, name='PROP_PRAYER_FLAGS_E')
    sf = C('ASHRAM/00_REFERENCE/SCALE')
    for k, p in enumerate([(1.5, -66), (-4, -2), (0, -98)]):
        obj(f'REF_SCALE_FIGURE_175cm_{k}', mesh_cyl(f'REF_SCALE_FIGURE_{k}', .22, 1.75, 10), sf, (p[0], p[1], 0), mat=ek.mat_simple('MAT_SCALE_FIGURE', '#E04A3A', .5))
    return out


# ======================================================================= landscape
def landscape(M, A):
    T = C('ASHRAM/03_TERRAIN')
    N, S = 401, 4000.0
    xs = np.linspace(-S / 2, S / 2, N); X, Y = np.meshgrid(xs, xs)
    n1 = fbm2(N, 7, 3); rid = np.clip(1 - np.abs(fbm2(N, 6, 9)) * 2.2, 0, 1)
    north = np.clip((Y - 250) / 1400, 0, 1) ** 1.6 * 1350 * (.7 + .5 * rid + .2 * n1)
    sides = np.clip((np.abs(X) - 420) / 1100, 0, 1) ** 1.5 * 720 * (.75 + .55 * rid)
    lake = -30 * np.exp(-(((X - 180) / 330) ** 2 + ((Y + 330) / 150) ** 2))
    r = np.hypot(X, Y)
    Z = north + sides + lake + 7 * n1 + np.clip((r - 160) / 400, 0, 1) * 12
    Z = np.where(r < 160, Z * np.clip((r - 120) / 40, 0, 1), Z)
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    faces = [(i * N + j, i * N + j + 1, (i + 1) * N + j + 1, (i + 1) * N + j) for i in range(N - 1) for j in range(N - 1)]
    me = bpy.data.meshes.new('TERRAIN_ASHRAM_VALLEY_4KM'); me.from_pydata(verts.tolist(), [], faces); me.update()
    for p in me.polygons:
        p.use_smooth = True
    ter = obj('TERRAIN_ASHRAM_VALLEY_4KM', me, T, mat=M['terrain'])
    # vegetation density groups (vertex weights)
    slope = np.hypot(*np.gradient(Z, S / (N - 1)))
    forest = fbm2(N, 5, 21)
    Wc = np.where((Z < 1050) & (Z > 1) & (slope < 1.1) & (r > 150), np.clip((forest + .1) * 2.2, 0, 1), 0)      # conifers
    Wb = np.where((Z < 380) & (Z > 1) & (r > 135) & (slope < .5), np.clip((.25 - forest) * 3, 0, 1) * .8, 0)      # broadleaf
    Wg = np.where((r > 66) & (r < 300) & (Z > .5) & (slope < .7), 1.0, 0) * np.clip(1 - (r - 200) / 100, 0, 1)    # grass (near)
    inside = (np.abs(X) < 61) & (Y > -63) & (Y < 63)
    paved = (np.abs(X) < 29) & (np.abs(Y - 2) < 22) | (np.abs(X) < 3) & (Y < -20)
    for (bx, by, bw, bd) in ((0, 34, 30, 22), (-42, 0, 15, 37), (42, 0, 15, 37), (-38, 44, 18, 14), (38, 44, 18, 14)):
        paved |= (np.abs(X - bx) < bw / 2) & (np.abs(Y - by) < bd / 2)
    Wg = np.where(inside, np.where(paved, 0, .8), Wg)
    Wg = np.where((np.abs(X) < 3) & (Y < -63) & (Y > -80), 0, Wg)
    Wg = np.where(np.hypot(X, Y + 100) < 23, 0, Wg)
    Wr = np.where((slope > .45) & (Z > 30), .6, 0) + np.where((r < 900) & (r > 150), .08, 0)
    for nm, Wt in (('veg_conifer', Wc), ('veg_broadleaf', Wb), ('veg_grass', Wg), ('veg_rock', Wr)):
        vg = ter.vertex_groups.new(name=nm)
        flat = Wt.ravel()
        for w in np.unique(np.round(flat, 2)):
            if w <= 0:
                continue
            idx = np.nonzero(np.round(flat, 2) == w)[0].tolist()
            vg.add(idx, float(w), 'REPLACE')
    # near-ground grass patch (separate dense mesh so the grass count stays bounded)
    # lake
    bpy.ops.mesh.primitive_plane_add(size=1, location=(180, -330, -3.6)); w = bpy.context.object
    w.name = 'WATER_LAKE'; w.scale = (950, 560, 1); ck.link(w, T); w.data.materials.append(M['water'])
    # far range 30 km (LOD far): ridged noise, lowered inside the valley tile
    NF, SF = 301, 30000.0
    xf = np.linspace(-SF / 2, SF / 2, NF); XF, YF = np.meshgrid(xf, xf)
    rf = np.hypot(XF, YF)
    ridf = np.clip(1 - np.abs(fbm2(NF, 7, 31)) * 2.0, 0, 1) ** 1.3
    hf = (900 + 4200 * np.clip((YF + 2000) / 12000, 0, 1)) * ridf * np.clip((rf - 1800) / 2500, 0, 1) * np.clip((YF + 7000) / 6000, .15, 1) + 300 * fbm2(NF, 6, 33)
    hf = hf - np.clip((2300 - rf) / 500, 0, 1) * 600
    vf = np.stack([XF.ravel(), YF.ravel(), hf.ravel()], 1)
    ff = [(i * NF + j, i * NF + j + 1, (i + 1) * NF + j + 1, (i + 1) * NF + j) for i in range(NF - 1) for j in range(NF - 1)]
    mf = bpy.data.meshes.new('TERRAIN_FAR_RANGE_30KM'); mf.from_pydata(vf.tolist(), [], ff); mf.update()
    for p in mf.polygons:
        p.use_smooth = True
    obj('TERRAIN_FAR_RANGE_30KM', mf, C('ASHRAM/03_TERRAIN/FAR_LOD'), (0, 0, -40), mat=M['far'])
    # vegetation libraries (hidden collections) + geometry-node scatters
    V = C('ASHRAM/03_TERRAIN/VEGETATION')
    libs = {}
    for key, makers in (('conifer', [lambda c, i=i: ek.make_conifer(f'ASSET_TREE_CONIFER_{i}', c, M, seed=10 + i, height=R.uniform(15, 24)) for i in range(4)]),
                        ('broadleaf', [lambda c, i=i: ek.make_broadleaf(f'ASSET_TREE_BROADLEAF_{i}', c, M, seed=20 + i, height=R.uniform(9, 14)) for i in range(3)]),
                        ('grass', [lambda c, i=i: ek.make_grass(f'ASSET_GRASS_CLUMP_{i}', c, M['grass'], seed=30 + i, h=R.uniform(.18, .32), blades=70) for i in range(4)]),
                        ('rock', [lambda c, i=i: ek.make_rock(f'ASSET_ROCK_{i}', c, M['rock'], seed=40 + i, size=R.uniform(.8, 2.4)) for i in range(4)])):
        lc = C(f'ASHRAM/03_TERRAIN/VEGETATION/LIB_{key.upper()}')
        for mk in makers:
            mk(lc)
        lc.hide_render = True; lc.hide_viewport = True
        libs[key] = lc
    ek.scatter(ter, 'VEG_SCATTER_CONIFER', libs['conifer'], .0032, group='veg_conifer', seed=3, scale=(.7, 1.25))
    ek.scatter(ter, 'VEG_SCATTER_BROADLEAF', libs['broadleaf'], .0018, group='veg_broadleaf', seed=4, scale=(.8, 1.3))
    ek.scatter(ter, 'VEG_SCATTER_GRASS', libs['grass'], 3.0, group='veg_grass', seed=5, scale=(.7, 1.3))
    ek.scatter(ter, 'VEG_SCATTER_ROCK', libs['rock'], .0012, group='veg_rock', seed=6, scale=(.5, 1.6))
    # hero trees: sacred courtyard tree + a few inside the compound
    sacred = ek.make_broadleaf('PROP_SACRED_TREE', C('ASHRAM/04_PROPS'), M, seed=77, height=17, spread=1.25, leaves=7000)
    sacred.location = (0, 4, .6)
    for k, p in enumerate([(-52, 50), (52, 50), (-52, -40), (52, -40), (-22, -48), (22, -48), (30, -112), (-30, -112), (78, -70), (46, -88)]):
        t = ek.make_broadleaf(f'VEG_HERO_TREE_{k:02d}', V, M, seed=50 + k, height=R.uniform(8, 12)) if k % 3 else \
            ek.make_conifer(f'VEG_HERO_TREE_{k:02d}', V, M, seed=60 + k, height=R.uniform(14, 19))
        t.location = (p[0], p[1], 0); t.rotation_euler = (0, 0, R.uniform(0, 6.28))
    return ter


# ======================================================================= atmosphere, light, cameras
def atmosphere(night=False):
    A = C('ASHRAM/06_LIGHTING/ATMOSPHERE')
    for o in list(A.objects):
        bpy.data.objects.remove(o)
    hz = obj('ATMOS_HAZE_VOLUME', mesh_box('ATMOS_HAZE', 34000, 34000, 4200), A, (0, 0, -100),
             mat=ek.mat_volume('MAT_ATMOS_HAZE_NIGHT' if night else 'MAT_ATMOS_HAZE', '#2A3550' if night else '#C9D8EA', .00006 if night else .00008))
    hz.visible_shadow = False
    mi = obj('ATMOS_LAKE_MIST', mesh_box('ATMOS_MIST', 1100, 520, 22), A, (200, -360, -5),
             mat=ek.mat_volume('MAT_ATMOS_MIST', '#E8EEF4', .0012, noise_scale=.006))
    mi.visible_shadow = False
    if not night:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 4000, 4200)); cl = bpy.context.object
        cl.name = 'ATMOS_CLOUD_LAYER'; cl.scale = (60000, 60000, 1); ck.link(cl, A); cl.data.materials.append(ek.mat_clouds())
        cl.visible_shadow = False


def lighting(night=False):
    sc = bpy.context.scene
    L = C('ASHRAM/06_LIGHTING')
    for o in list(L.objects):
        bpy.data.objects.remove(o)
    wd = sc.world or bpy.data.worlds.new('WORLD_ASHRAM'); sc.world = wd; wd.use_nodes = True
    nt = wd.node_tree
    for n in list(nt.nodes):
        if n.type == 'TEX_SKY':
            nt.nodes.remove(n)
    bg = nt.nodes['Background']
    sd = bpy.data.lights.new('LIGHT_SUN' if not night else 'LIGHT_MOON', 'SUN'); so = bpy.data.objects.new(sd.name, sd); L.objects.link(so)
    lan = bpy.data.materials['MAT_ENV_LANTERN_GLOW'].node_tree.nodes['Principled BSDF']
    if not night:
        el, az = math.radians(24), math.radians(235)      # golden hour, sun from the south-west
        sky = nt.nodes.new('ShaderNodeTexSky')
        try:
            sky.sky_type = 'NISHITA'; sky.sun_elevation = el; sky.sun_rotation = az; sky.air_density = 1.2; sky.dust_density = 2.0
        except Exception:
            pass
        nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = .14
        sd.energy = 5.5; sd.angle = math.radians(.8); sd.color = ck.hexlin('#FFD3A0')[:3]
        to_sun = Vector((-.82, -.22, math.tan(el))).normalized()      # low side-light from the west (cinematic modelling)
        so.rotation_euler = (-to_sun).to_track_quat('-Z', 'Y').to_euler()
        try:
            sky.sun_rotation = math.atan2(to_sun.x, to_sun.y) + math.pi
        except Exception:
            pass
        lan.inputs['Emission Strength'].default_value = 0
    else:
        bg.inputs[0].default_value = ck.hexlin('#0B1324'); bg.inputs[1].default_value = .6
        sd.energy = .3; sd.color = ck.hexlin('#9DB8FF')[:3]; so.rotation_euler = (math.radians(50), 0, math.radians(-40))
        lan.inputs['Emission Strength'].default_value = 30
        for o in [o for o in bpy.data.objects if o.name.startswith('PROP_LANTERN_')]:
            ld = bpy.data.lights.new('LIGHT_' + o.name, 'POINT'); ld.energy = 1200; ld.color = ck.hexlin('#FFB35A')[:3]; ld.shadow_soft_size = .25
            lo = bpy.data.objects.new(ld.name, ld); lo.location = o.location + Vector((0, 0, .1)); L.objects.link(lo)
        for nm, loc, rot in (('LIGHT_HALL_DOOR_GLOW', (0, 25.5, 3.2), (math.radians(90), 0, 0)), ('LIGHT_RES_W_GLOW', (-37, 0, 2.2), (0, math.radians(90), 0)),
                             ('LIGHT_RES_E_GLOW', (37, 0, 2.2), (0, math.radians(-90), 0))):
            ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = 2500; ld.size = 5; ld.color = ck.hexlin('#FFB870')[:3]
            lo = bpy.data.objects.new(nm, ld); lo.location = loc; lo.rotation_euler = rot; L.objects.link(lo)
    atmosphere(night)


CAMS = [  # name, loc, target, lens, res, caption, dof_focus (m) or None
    ('CAM_01_WIDE_ESTABLISHING', (-120, -330, 26), (10, 60, 95), 24, (1600, 900), 'Wide establishing — valley, lake, northern range', None),
    ('CAM_02_FRONT_GATE', (2, -132, 3.2), (0, 0, 9), 30, (1280, 720), 'Front — approach to the gate across the training ground', None),
    ('CAM_03_COURTYARD', (-14, -40, 1.65), (2, 30, 7), 26, (1280, 720), 'Courtyard at character height (1.65 m) — sacred tree, main hall', 30),
    ('CAM_04_HALL_DETAIL', (9, 16, 3.0), (2, 26, 4.6), 30, (1280, 720), 'Architectural detail — hall verandah, carved pillars, brackets, eaves', 9),
    ('CAM_05_PAVILION_LAKE', (34, -118, 3.0), (62, -80, 4.5), 30, (1280, 720), 'Meditation pavilion + lake ghat, mist', None),
    ('CAM_06_BACK_FROM_SLOPE', (25, 330, 70), (0, -10, 0), 32, (1280, 720), 'Back — from the forest slope above the Ashram', None),
    ('CAM_07_SIDE_WEST', (-230, 30, 18), (0, 0, 10), 32, (1280, 720), 'Side — west, through the valley trees', None),
    ('CAM_08_TRAINING', (-34, -140, 6), (0, -98, 1), 28, (1280, 720), 'Training ground (Ø 44 m) — space for power + portal VFX', None),
]


def cameras():
    Cc = C('ASHRAM/07_CAMERAS'); out = []
    for n, l, t, lens, res, cap, dof in CAMS:
        c = ck.camera(n, Cc, l, t, lens=lens); c.data.clip_end = 60000; c['caption'] = cap
        if dof:
            c.data.dof.use_dof = True; c.data.dof.focus_distance = dof; c.data.dof.aperture_fstop = 4.0
        out.append((c, res, cap))
    top = ck.camera('CAM_09_BIRDSEYE_ORTHO', Cc, (0, -20, 900), (0, -20, 0), ortho=300); top.data.clip_end = 5000
    top['caption'] = 'Bird’s-eye layout (orthographic, north up, 300 m frame)'
    out.append((top, (1400, 1400), top['caption']))
    return out


def main():
    ck.reset()
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    M = materials(); A = modules(M)
    site(A, M); landscape(M, A)
    org = bpy.data.objects.new('ASHRAM_ORIGIN', None); C('ASHRAM/00_REFERENCE').objects.link(org)
    f = os.path.join(HERE, '..', 'map', 'data', 'features.json')
    if os.path.exists(f):
        F = json.load(open(f)); org['wcs_x_km'] = float(F['ashram'][0]); org['wcs_y_km'] = float(768 - F['ashram'][1])
    org['status'] = 'PROPOSAL v2 (look-development) — awaiting Director approval'
    cams = cameras(); lighting(False)
    ck.setup_render((1280, 720), SAMPLES)
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    cy = sc.cycles; cy.transparent_max_bounces = 64; cy.max_bounces = 8; cy.volume_bounces = 1; cy.volume_step_rate = 4.0
    cy.use_denoising = True
    out = os.path.join(ROOT, '01_BLOCKOUT', 'ASHRAM_concept_v002.blend')
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print('SAVED', out, len(bpy.data.objects), 'objects', flush=True)
    if not RENDER:
        return
    for cam, res, cap in cams:
        if ONLY and cam.name not in ONLY:
            continue
        sc.render.resolution_x, sc.render.resolution_y = res
        ck.render_to(os.path.join(OUTR, f'{cam.name}_golden.png'), cam)
    lighting(True)
    for cam, res, cap in cams:
        if cam.name in ('CAM_01_WIDE_ESTABLISHING', 'CAM_03_COURTYARD', 'CAM_02_FRONT_GATE') and (not ONLY or cam.name in ONLY):
            sc.render.resolution_x, sc.render.resolution_y = res
            ck.render_to(os.path.join(OUTR, f'{cam.name}_night.png'), cam)
    print('RENDERS DONE', flush=True)


if __name__ == '__main__':
    main()

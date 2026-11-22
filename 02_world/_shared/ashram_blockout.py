"""ASHRAM — concept blockout v1 (PROPOSAL, real metres). Rebuilds the whole scene from code.

Run:  python3 02_world/_shared/ashram_blockout.py [samples] [--no-render]
Out:  02_world/ashram/01_BLOCKOUT/ASHRAM_blockout_v001.blend
      02_world/ashram/09_RENDER/concept_v1/*.png  (camera previews, day + night)

Scene units: 1 BU = 1 m. Local origin (0,0,0) = centre of the main courtyard, +Y = north (towards the range),
+X = east. WCS anchor = LOC_ASHRAM__position_PROPOSED in WORLD_overview_v001.blend (stored on the ASHRAM_ORIGIN empty).
All architecture here is a PROPOSED direction (Director approval needed): "Himalayan foothill gurukul" —
stone plinths, timber verandah pillars, two-tier clay-tile roofs, open courtyard, training ground, lake ghat.

Modular kit (collection 02_ARCHITECTURE/MODULES, hidden; buildings use linked duplicates of these meshes):
ASSET_PILLAR_TIMBER, ASSET_PILLAR_STONE, ASSET_WALL_SEG_4M, ASSET_STAIR_STEP, ASSET_DOOR, ASSET_WINDOW,
ASSET_RAIL_SEG_2M, ASSET_LANTERN, ASSET_TREE_A/B/C (vegetation).
"""
import os, sys, json, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '01_characters', '_shared'))
sys.path.insert(0, HERE)
import charkit as ck

ROOT = os.path.join(HERE, '..', 'ashram')
args = [a for a in sys.argv[1:] if not a.startswith('-')]
SAMPLES = int(args[0]) if args else 20
RENDER = '--no-render' not in sys.argv
OUTR = os.path.join(ROOT, '09_RENDER', 'concept_v1'); os.makedirs(OUTR, exist_ok=True)
DIRS = ['00_REFERENCE', '01_BLOCKOUT', '02_ARCHITECTURE', '03_TERRAIN', '04_PROPS', '05_MATERIALS', '06_LIGHTING',
        '07_CAMERAS', '08_VFX', '09_RENDER', '10_BACKUPS']
for d in DIRS:
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
R = random.Random(11)


# ======================================================================= collections
def C(path):
    parent = None
    for p in path.split('/'):
        parent = ck.get_coll(p, parent) if parent else ck.get_coll(p)
    return parent


# ======================================================================= materials (PBR, procedural — baked later)
def pmat(name, base, rough=.6, metal=0., bump=0., scale=8., var=.0, var_hex=None, emit=None, emit_s=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
    tc = nt.nodes.new('ShaderNodeTexCoord')
    if var > 0:
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 8
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        mx.inputs['A'].default_value = ck.hexlin(base); mx.inputs['B'].default_value = ck.hexlin(var_hex or base)
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = .5 - var; mr.inputs['From Max'].default_value = .5 + var
        nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], mx.inputs['Factor'])
        nt.links.new(mx.outputs['Result'], bs.inputs['Base Color'])
        if bump > 0:
            bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
            nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])
    else:
        bs.inputs['Base Color'].default_value = ck.hexlin(base)
    if emit:
        bs.inputs['Emission Color'].default_value = ck.hexlin(emit); bs.inputs['Emission Strength'].default_value = emit_s
    return m


def bricks(name, mortar, b1, b2, scale=3.0, rough=.75, bump=.25):
    """clay roof tiles / stone courses: brick texture → colour + bump."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']; bs.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Scale'].default_value = scale
    br.inputs['Color1'].default_value = ck.hexlin(b1); br.inputs['Color2'].default_value = ck.hexlin(b2)
    br.inputs['Mortar'].default_value = ck.hexlin(mortar); br.inputs['Mortar Size'].default_value = .012
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], bs.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.invert = True
    nt.links.new(br.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])
    return m


PAL = {  # proposed Ashram material palette (also in WORLD_BIBLE.md)
    'stone': '#8E8372', 'stone_dark': '#6A6156', 'plaster': '#E6D8BE', 'timber': '#6B4426', 'timber_dark': '#4A2E19',
    'tile': '#A4512F', 'tile_dark': '#7E3A22', 'gold': '#C9A040', 'grass': '#6E8F45', 'grass_dry': '#9A9A5A',
    'soil': '#9C7F5C', 'path': '#A88A5E', 'rock': '#7B766E', 'snow': '#EEF2F5', 'water': '#2B5D73', 'leaf': '#3E6B32',
    'leaf2': '#5B7F3A', 'bark': '#5A4130', 'cloth': '#C8452E', 'lantern': '#FFB35A',
}


def materials():
    M = {}
    M['stone'] = bricks('MAT_ASH_STONE_COURSED', '#5E564C', PAL['stone'], '#9B907E', scale=1.2, rough=.8, bump=.35)
    M['stone_rough'] = pmat('MAT_ASH_STONE_ROUGH', PAL['stone_dark'], .85, bump=.5, scale=3, var=.25, var_hex=PAL['stone'])
    M['plaster'] = pmat('MAT_ASH_PLASTER', PAL['plaster'], .8, bump=.08, scale=6, var=.15, var_hex='#D8C6A6')
    M['timber'] = pmat('MAT_ASH_TIMBER', PAL['timber'], .55, bump=.12, scale=24, var=.25, var_hex=PAL['timber_dark'])
    M['tile'] = bricks('MAT_ASH_ROOF_TILE', '#5A2614', PAL['tile'], PAL['tile_dark'], scale=6, rough=.6, bump=.4)
    M['gold'] = pmat('MAT_ASH_BRASS', PAL['gold'], .3, metal=1.0)
    M['dark'] = pmat('MAT_ASH_OPENING_DARK', '#1A120C', .9)
    M['grass'] = pmat('MAT_ASH_GRASS', PAL['grass'], .9, bump=.2, scale=.15, var=.22, var_hex=PAL['grass_dry'])
    M['path'] = pmat('MAT_ASH_PATH', PAL['path'], .9, bump=.15, scale=2, var=.2, var_hex=PAL['soil'])
    M['water'] = ck.principled('MAT_ASH_WATER', PAL['water'], rough=.04)
    M['leaf'] = pmat('MAT_ASH_LEAF', PAL['leaf'], .7, var=.25, scale=.6, var_hex=PAL['leaf2'])
    M['bark'] = pmat('MAT_ASH_BARK', PAL['bark'], .9)
    M['cloth'] = pmat('MAT_ASH_CLOTH_FLAG', PAL['cloth'], .8)
    M['lantern'] = pmat('MAT_ASH_LANTERN_GLOW', '#FFE2B0', .5, emit=PAL['lantern'], emit_s=0.0)
    M['figure'] = pmat('MAT_SCALE_FIGURE', '#E04A3A', .5)
    # terrain: slope / height blend (grass -> rock -> snow) via geometry
    m = bpy.data.materials.new('MAT_ASH_TERRAIN'); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']; bs.inputs['Roughness'].default_value = .9
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Normal'], sep.inputs['Vector'])
    pos = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Position'], pos.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = .02; nz.inputs['Detail'].default_value = 10
    nt.links.new(geo.outputs['Position'], nz.inputs['Vector'])
    r1 = nt.nodes.new('ShaderNodeMapRange'); r1.inputs['From Min'].default_value = .76; r1.inputs['From Max'].default_value = .62
    nt.links.new(sep.outputs['Z'], r1.inputs['Value'])                     # steep -> rock
    r2 = nt.nodes.new('ShaderNodeMapRange'); r2.inputs['From Min'].default_value = 1050; r2.inputs['From Max'].default_value = 1200
    nt.links.new(pos.outputs['Z'], r2.inputs['Value'])                     # high -> snow
    m1 = nt.nodes.new('ShaderNodeMix'); m1.data_type = 'RGBA'
    gm = nt.nodes.new('ShaderNodeMix'); gm.data_type = 'RGBA'
    gm.inputs['A'].default_value = ck.hexlin(PAL['grass']); gm.inputs['B'].default_value = ck.hexlin('#55702F')
    nt.links.new(nz.outputs['Fac'], gm.inputs['Factor'])
    nt.links.new(gm.outputs['Result'], m1.inputs['A']); m1.inputs['B'].default_value = ck.hexlin(PAL['rock'])
    nt.links.new(r1.outputs['Result'], m1.inputs['Factor'])
    m2 = nt.nodes.new('ShaderNodeMix'); m2.data_type = 'RGBA'
    nt.links.new(m1.outputs['Result'], m2.inputs['A']); m2.inputs['B'].default_value = ck.hexlin(PAL['snow'])
    nt.links.new(r2.outputs['Result'], m2.inputs['Factor'])
    nt.links.new(m2.outputs['Result'], bs.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .3
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])
    M['terrain'] = m
    return M


# ======================================================================= primitives
def mesh_box(name, sx, sy, sz):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * sx, v.co.y * sy, (v.co.z + .5) * sz))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me


def mesh_cyl(name, r, h, n=12, r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=n, radius1=r, radius2=r2 if r2 is not None else r, depth=h)
    for v in bm.verts:
        v.co.z += h / 2
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me


def obj(name, me, coll, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, smooth=False, bevel=0.0):
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    o.location = loc; o.rotation_euler = rot
    if mat and not me.materials:
        me.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if bevel:
        b = o.modifiers.new('Bevel', 'BEVEL'); b.width = bevel; b.segments = 2; b.limit_method = 'ANGLE'
    return o


def inst(asset, name, coll, loc, rot=(0, 0, 0), scale=(1, 1, 1)):
    """linked duplicate of a module (shares mesh + material = modular, memory-cheap)."""
    o = bpy.data.objects.new(name, asset.data); coll.objects.link(o)
    o.location = loc; o.rotation_euler = rot; o.scale = scale
    for m in asset.modifiers:
        if m.type == 'BEVEL':
            b = o.modifiers.new('Bevel', 'BEVEL'); b.width = m.width; b.segments = m.segments; b.limit_method = 'ANGLE'
    return o


def roof_mesh(name, w, d, rise, over=1.2, flare=.35):
    """Hip roof with slightly up-turned eaves (flare). w along X, d along Y."""
    W2, D2 = w / 2 + over, d / 2 + over
    rl = max(0.0, (w - d) / 2)
    v = [(-W2, -D2, 0), (W2, -D2, 0), (W2, D2, 0), (-W2, D2, 0),
         (-W2 * .5 - rl * .5, -D2 * .5, rise * .62), (W2 * .5 + rl * .5, -D2 * .5, rise * .62),
         (W2 * .5 + rl * .5, D2 * .5, rise * .62), (-W2 * .5 - rl * .5, D2 * .5, rise * .62),
         (-rl, 0, rise), (rl, 0, rise)]
    v = [(x, y, z + (flare if z == 0 and abs(x) == W2 and abs(y) == D2 else 0)) for x, y, z in v]
    f = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 9, 8), (5, 6, 9), (6, 7, 8, 9), (7, 4, 8)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    return me


# ======================================================================= modules (asset kit)
def modules(M):
    K = C('ASHRAM/02_ARCHITECTURE/MODULES')
    A = {}
    A['pillar'] = obj('ASSET_PILLAR_TIMBER', mesh_cyl('ASSET_PILLAR_TIMBER', .16, 3.2, 10), K, mat=M['timber'], smooth=True)
    b = obj('ASSET_PILLAR_BASE_STONE', mesh_box('ASSET_PILLAR_BASE_STONE', .55, .55, .35), K, mat=M['stone'], bevel=.03)
    A['pbase'] = b
    A['pcap'] = obj('ASSET_PILLAR_CAP_TIMBER', mesh_box('ASSET_PILLAR_CAP_TIMBER', .7, .45, .22), K, mat=M['timber_dark'] if 'timber_dark' in M else M['timber'], bevel=.02)
    A['spillar'] = obj('ASSET_PILLAR_STONE', mesh_cyl('ASSET_PILLAR_STONE', .32, 4.5, 8), K, mat=M['stone_rough'], bevel=.04)
    A['wall'] = obj('ASSET_WALL_SEG_4M', mesh_box('ASSET_WALL_SEG_4M', 4.0, .45, 1.4), K, mat=M['stone'], bevel=.04)
    A['step'] = obj('ASSET_STAIR_STEP', mesh_box('ASSET_STAIR_STEP', 1.0, .4, .18), K, mat=M['stone'], bevel=.02)
    A['door'] = obj('ASSET_DOOR', mesh_box('ASSET_DOOR', 1.6, .12, 2.6), K, mat=M['dark'])
    A['window'] = obj('ASSET_WINDOW', mesh_box('ASSET_WINDOW', 1.0, .12, 1.2), K, mat=M['dark'])
    A['rail'] = obj('ASSET_RAIL_SEG_2M', mesh_box('ASSET_RAIL_SEG_2M', 2.0, .08, .08), K, mat=M['timber'])
    lan = mesh_box('ASSET_LANTERN', .28, .28, .4)
    A['lantern'] = obj('ASSET_LANTERN', lan, K, mat=M['lantern'], bevel=.03)
    # trees: 3 variants (trunk + leaf clusters merged)
    for k, (hgt, rad, n) in enumerate(((9, 3.2, 5), (14, 3.8, 7), (6, 2.6, 4))):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=.35 + .05 * k, radius2=.18, depth=hgt * .6)
        for v in bm.verts:
            v.co.z += hgt * .3
        tr = bpy.data.meshes.new(f'ASSET_TREE_{"ABC"[k]}'); bm.to_mesh(tr); bm.free()
        lv = bmesh.new()
        rr = random.Random(k)
        for i in range(n):
            c = Vector((rr.uniform(-1, 1) * rad * .5, rr.uniform(-1, 1) * rad * .5, hgt * (.62 + .35 * i / n)))
            bmesh.ops.create_icosphere(lv, subdivisions=2, radius=rad * (1 - .35 * i / n),
                                       matrix=Matrix.Translation(c) @ Matrix.Diagonal((1, 1, .75, 1)))
        lm = bpy.data.meshes.new('tmp'); lv.to_mesh(lm); lv.free()
        t = obj(f'ASSET_TREE_{"ABC"[k]}', tr, K, mat=M['bark'])
        lo = obj('tmp', lm, K, mat=M['leaf'], smooth=True)
        ctx = {'active_object': t, 'selected_editable_objects': [t, lo]}
        bpy.ops.object.select_all(action='DESELECT'); t.select_set(True); lo.select_set(True)
        bpy.context.view_layer.objects.active = t
        bpy.ops.object.join()
        A[f'tree{k}'] = t
    K.hide_render = True; K.hide_viewport = True
    for o in K.objects:
        o['asset_kit'] = True
    return A


# ======================================================================= architecture
def building(name, A, M, coll, c, w, d, wall_h=3.4, plinth=1.0, tiers=2, verandah=2.4, rot=0.0, door_side='S', rise=3.2):
    """Plinth + walls + timber verandah + 1-2 tier hip roof. c = centre (x, y), ground z = 0."""
    g = C(coll)
    root = bpy.data.objects.new(name, None); g.objects.link(root); root.location = (c[0], c[1], 0); root.rotation_euler = (0, 0, rot)
    root.empty_display_size = 4
    parts = []

    def add(o):
        o.parent = root; parts.append(o); return o
    W, D = w + 2 * verandah, d + 2 * verandah
    add(obj(f'{name}_PLINTH', mesh_box(f'{name}_PLINTH', W + .8, D + .8, plinth), g, mat=M['stone'], bevel=.05))
    add(obj(f'{name}_WALLS', mesh_box(f'{name}_WALLS', w, d, wall_h), g, (0, 0, plinth), mat=M['plaster'], bevel=.03))
    add(obj(f'{name}_WALL_BAND', mesh_box(f'{name}_WALL_BAND', w + .1, d + .1, .3), g, (0, 0, plinth + wall_h - .3), mat=M['timber']))
    # verandah pillars on a 2.4-3 m rhythm
    nx_, ny_ = max(2, round(W / 2.8)), max(2, round(D / 2.8))
    pts = set()
    for i in range(nx_ + 1):
        x = -W / 2 + .4 + (W - .8) * i / nx_
        pts.add((round(x, 3), round(-D / 2 + .4, 3))); pts.add((round(x, 3), round(D / 2 - .4, 3)))
    for j in range(ny_ + 1):
        y = -D / 2 + .4 + (D - .8) * j / ny_
        pts.add((round(-W / 2 + .4, 3), round(y, 3))); pts.add((round(W / 2 - .4, 3), round(y, 3)))
    for k, (x, y) in enumerate(sorted(pts)):
        add(inst(A['pbase'], f'{name}_PBASE_{k:02d}', g, (x, y, plinth)))
        add(inst(A['pillar'], f'{name}_PILLAR_{k:02d}', g, (x, y, plinth + .35), scale=(1, 1, (wall_h - .35) / 3.2)))
        add(inst(A['pcap'], f'{name}_PCAP_{k:02d}', g, (x, y, plinth + wall_h - .22)))
    # roof tiers
    z = plinth + wall_h
    add(obj(f'{name}_ROOF_1', roof_mesh(f'{name}_ROOF_1', W, D, rise * .55, over=1.3), g, (0, 0, z), mat=M['tile']))
    if tiers > 1:
        add(obj(f'{name}_ROOF_DRUM', mesh_box(f'{name}_ROOF_DRUM', w * .62, d * .62, 1.6), g, (0, 0, z + rise * .25), mat=M['plaster']))
        add(obj(f'{name}_ROOF_2', roof_mesh(f'{name}_ROOF_2', w * .62, d * .62, rise * .75, over=1.0), g, (0, 0, z + rise * .25 + 1.6), mat=M['tile']))
        fin = add(obj(f'{name}_FINIAL', mesh_cyl(f'{name}_FINIAL', .22, 1.4, 8, r2=.02), g, (0, 0, z + rise * .25 + 1.6 + rise * .75), mat=M['gold']))
    for o in parts:
        if o.data and o.data.name.startswith(f'{name}_ROOF'):
            s = o.modifiers.new('Solidify', 'SOLIDIFY'); s.thickness = .25
    # door + windows + front steps
    sgn = -1 if door_side == 'S' else 1
    add(inst(A['door'], f'{name}_DOOR', g, (0, sgn * (d / 2 + .02), plinth)))
    for k, x in enumerate((-w / 2 + 1.6, w / 2 - 1.6)):
        if abs(x) > 1.6:
            add(inst(A['window'], f'{name}_WINDOW_{k}', g, (x, sgn * (d / 2 + .02), plinth + 1.0)))
    nst = max(1, round(plinth / .18))
    for s in range(nst):
        add(inst(A['step'], f'{name}_STEP_{s:02d}', g, (0, sgn * (D / 2 + .4 + .4 * (nst - 1 - s)), s * .18),
                 scale=(3.0, 1, 1)))
    return root


def ashram(A, M):
    B = 'ASHRAM/02_ARCHITECTURE'
    out = {}
    out['hall'] = building('ARCH_MAIN_HALL', A, M, B, (0, 34), 22, 14, wall_h=4.2, plinth=1.6, tiers=2, verandah=3.0, rise=5.0)
    out['res_w'] = building('ARCH_RESIDENCE_W', A, M, B, (-42, 0), 8, 30, wall_h=3.2, plinth=.8, tiers=1, verandah=2.2, rise=3.0, rot=0)
    out['res_e'] = building('ARCH_RESIDENCE_E', A, M, B, (42, 0), 8, 30, wall_h=3.2, plinth=.8, tiers=1, verandah=2.2, rise=3.0)
    out['kitchen'] = building('ARCH_SERVICE_HALL', A, M, B, (-38, 44), 12, 8, wall_h=3.2, plinth=.6, tiers=1, verandah=1.8, rise=2.6)
    out['library'] = building('ARCH_LIBRARY_HALL', A, M, B, (38, 44), 12, 8, wall_h=3.4, plinth=.8, tiers=1, verandah=1.8, rise=2.8)
    # meditation pavilion (open mandapa) by the lake: pillars + roof, no walls
    g = C(B)
    mp = bpy.data.objects.new('ARCH_MEDITATION_PAVILION', None); g.objects.link(mp); mp.location = (62, -78, 0)
    obj('ARCH_MEDITATION_PAVILION_PLINTH', mesh_box('ARCH_MED_PLINTH', 11, 11, 1.2), g, (62, -78, 0), mat=M['stone'], bevel=.05).parent = None
    for k, (x, y) in enumerate([(-4, -4), (4, -4), (4, 4), (-4, 4), (0, -4), (0, 4), (-4, 0), (4, 0)]):
        inst(A['pillar'], f'ARCH_MED_PILLAR_{k}', g, (62 + x, -78 + y, 1.2), scale=(1, 1, 1.05))
    obj('ARCH_MED_ROOF', roof_mesh('ARCH_MED_ROOF', 9, 9, 4.2, over=1.4, flare=.5), g, (62, -78, 1.2 + 3.36), mat=M['tile'])
    obj('ARCH_MED_FINIAL', mesh_cyl('ARCH_MED_FINIAL', .2, 1.2, 8, r2=.02), g, (62, -78, 1.2 + 3.36 + 4.2), mat=M['gold'])
    # entrance gate (stone torana) on the south axis + boundary wall from modules
    gz = C('ASHRAM/02_ARCHITECTURE/GATE_AND_WALLS')
    for sx in (-1, 1):
        inst(A['spillar'], f'ARCH_GATE_PILLAR_{"WE"[sx > 0]}', gz, (sx * 3.2, -62, 0))
    obj('ARCH_GATE_LINTEL', mesh_box('ARCH_GATE_LINTEL', 9.0, 1.0, .8), gz, (0, -62, 4.5), mat=M['stone_rough'], bevel=.05)
    obj('ARCH_GATE_ROOF', roof_mesh('ARCH_GATE_ROOF', 8, 1.4, 1.6, over=.7, flare=.3), gz, (0, -62, 5.3), mat=M['tile'])
    k = 0
    for side, (x0, y0, x1, y1) in {'S_W': (-60, -62, -6, -62), 'S_E': (6, -62, 60, -62), 'W': (-60, -62, -60, 62),
                                     'E': (60, -62, 60, 62), 'N': (-60, 62, 60, 62)}.items():
        L = math.hypot(x1 - x0, y1 - y0); n = int(L // 4)
        ang = math.atan2(y1 - y0, x1 - x0)
        for i in range(n):
            t = (i + .5) / n
            inst(A['wall'], f'ARCH_WALL_{side}_{i:02d}', gz, (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 0), rot=(0, 0, ang),
                 scale=(L / n / 4, 1, 1)); k += 1
    # courtyard + training ground + paths + ghat (ground features)
    gr = C('ASHRAM/03_TERRAIN/GROUND_FEATURES')
    obj('GROUND_COURTYARD_PAVING', mesh_box('GROUND_COURTYARD', 56, 40, .12), gr, (0, 2, 0), mat=M['stone'])
    tg = obj('GROUND_TRAINING_GROUND', mesh_cyl('GROUND_TRAINING', 22, .1, 48), gr, (0, -100, 0), mat=M['path'])
    obj('GROUND_TRAINING_RING', mesh_cyl('GROUND_TRAINING_RING', 22.6, .35, 48), gr, (0, -100, -.2), mat=M['stone'])
    obj('GROUND_PATH_GATE_TO_COURT', mesh_box('GROUND_PATH_1', 4, 40, .1), gr, (0, -42, 0), mat=M['path'])
    obj('GROUND_PATH_TO_TRAINING', mesh_box('GROUND_PATH_2', 4, 18, .1), gr, (0, -71, 0), mat=M['path'])
    obj('GROUND_PATH_TO_PAVILION', mesh_box('GROUND_PATH_3', 3, 60, .1), gr, (34, -74, 0), rot=(0, 0, math.radians(-62)), mat=M['path'])
    for s in range(10):     # ghat steps into the lake
        inst(A['step'], f'GHAT_STEP_{s:02d}', gr, (62, -92 - s * .4, -s * .18), scale=(16, 1, 1))
    # sacred tree in the courtyard (proposal) + lanterns + flags
    pr = C('ASHRAM/04_PROPS')
    inst(A['tree1'], 'PROP_COURTYARD_TREE', pr, (0, 4, 0), scale=(1.2, 1.2, 1.1))
    obj('PROP_TREE_PLATFORM', mesh_cyl('PROP_TREE_PLATFORM', 4.2, .6, 24), pr, (0, 4, 0), mat=M['stone'], bevel=.04)
    for k, (x, y) in enumerate([(-6, -60), (6, -60), (-10, 22), (10, 22), (-28, -6), (28, -6), (56, -72), (68, -72)]):
        inst(A['lantern'], f'PROP_LANTERN_{k:02d}', pr, (x, y, 2.0 if abs(y) != 60 else 4.6))
    for k, x in enumerate((-12, -6, 6, 12)):
        f = obj(f'PROP_FLAG_{k}', mesh_box(f'PROP_FLAG_{k}', .9, .03, .6), pr, (x, 25.5, 9.5), mat=M['cloth'])
        obj(f'PROP_FLAGPOLE_{k}', mesh_cyl(f'PROP_FLAGPOLE_{k}', .04, 10, 6), pr, (x - .48, 25.5, 0), mat=M['timber'])
    # scale figure (1.75 m) at the gate and in the courtyard — NOT a character, size reference only
    sf = C('ASHRAM/00_REFERENCE/SCALE')
    for k, p in enumerate([(1.5, -64), (-4, -2), (0, -98)]):
        obj(f'REF_SCALE_FIGURE_175cm_{k}', mesh_cyl(f'REF_SCALE_FIGURE_{k}', .22, 1.75, 10), sf, (p[0], p[1], 0), mat=M['figure'], smooth=True)
    return out


# ======================================================================= terrain (detail tile + far LOD ring)
def fbm2(n, oct=6, seed=0):
    r = np.random.default_rng(seed); out = np.zeros((n, n), np.float32); a = 1.0; tot = 0
    from scipy import ndimage as ndi
    for o in range(oct):
        k = 4 * 2 ** o; g = r.standard_normal((k + 4, k + 4)).astype(np.float32)
        z = ndi.zoom(g, n / k, order=3); off = int(n / k)
        out += a * z[off:off + n, off:off + n]; tot += a; a *= .5
    return out / tot


def terrain(M):
    T = C('ASHRAM/03_TERRAIN')
    N, S = 321, 3000.0                   # 3 km x 3 km detail tile, ~9.4 m grid
    xs = np.linspace(-S / 2, S / 2, N)
    X, Y = np.meshgrid(xs, xs)
    n1 = fbm2(N, 7, 3)
    r = np.hypot(X, Y)
    rid = 1 - np.abs(fbm2(N, 6, 9)) * 2.2
    north = np.clip((Y - 250) / 1250, 0, 1) ** 1.7 * 1250 * (.75 + .45 * np.clip(rid, 0, 1) + .25 * n1)
    sides = np.clip((np.abs(X) - 450) / 1000, 0, 1) ** 1.5 * 650 * (.8 + .5 * np.clip(rid, 0, 1))
    lake = -28 * np.exp(-(((X - 180) / 330) ** 2 + ((Y + 330) / 150) ** 2))
    Z = north + sides + lake + 6 * n1 + np.clip((r - 160) / 400, 0, 1) * 10
    Z = np.where(r < 160, Z * np.clip((r - 120) / 40, 0, 1), Z)          # flat site platform
    verts = [(float(X[i, j]), float(Y[i, j]), float(Z[i, j])) for i in range(N) for j in range(N)]
    faces = [(i * N + j, i * N + j + 1, (i + 1) * N + j + 1, (i + 1) * N + j) for i in range(N - 1) for j in range(N - 1)]
    me = bpy.data.meshes.new('TERRAIN_ASHRAM_DETAIL_3KM'); me.from_pydata(verts, [], faces); me.update()
    for p in me.polygons:
        p.use_smooth = True
    uv = me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co; uv.data[li].uv = (v.x / S + .5, v.y / S + .5)
    t = obj('TERRAIN_ASHRAM_DETAIL_3KM', me, T, mat=M['terrain'])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(180, -330, -4.0)); w = bpy.context.object
    w.name = 'WATER_LAKE'; w.scale = (900, 520, 1); ck.link(w, C('ASHRAM/03_TERRAIN')); w.data.materials.append(M['water'])
    # far LOD: low-poly mountain ring 3-14 km (background only)
    ring = bmesh.new(); rr = np.random.default_rng(5)
    NA, NR = 96, 8
    ids = []
    for i in range(NR):
        rad = 1600 + i * 1700
        row = []
        for k in range(NA):
            a = 2 * math.pi * k / NA
            north_bias = .5 + .5 * math.sin(a)                 # higher to the north (towards the great range)
            hgt = (500 + 3800 * north_bias) * (1 - abs(i - 3) / 5) * (0.55 + .9 * rr.random()) if 0 < i < NR - 1 else (0 if i == 0 else 300)
            row.append(ring.verts.new((rad * math.cos(a), rad * math.sin(a), hgt)))
        ids.append(row)
    for i in range(NR - 1):
        for k in range(NA):
            ring.faces.new((ids[i][k], ids[i][(k + 1) % NA], ids[i + 1][(k + 1) % NA], ids[i + 1][k]))
    rm = bpy.data.meshes.new('TERRAIN_FAR_LOD_MOUNTAIN_RING'); ring.to_mesh(rm); ring.free()
    fr = obj('TERRAIN_FAR_LOD_MOUNTAIN_RING', rm, C('ASHRAM/03_TERRAIN/FAR_LOD'), (0, 0, -15), mat=M['terrain'], smooth=True)
    return t, (X, Y, Z)


def scatter_trees(A, grid):
    X, Y, Z = grid
    global FOREST
    FOREST = fbm2(X.shape[0], 5, 21)
    V = C('ASHRAM/03_TERRAIN/VEGETATION')
    N = X.shape[0]; S = X[0, -1] - X[0, 0]; step = S / (N - 1)
    k = 0
    for i in range(0, N, 1):
        for j in range(0, N, 1):
            x, y, z = X[i, j], Y[i, j], Z[i, j]
            r = math.hypot(x, y)
            if r < 140 or z > 950 or z < -1 or (abs(x - 180) < 420 and abs(y + 330) < 190):
                continue
            dens = (.35 if FOREST[i, j] > .15 else .015) * (1 if r > 260 else .3)
            if R.random() < dens:
                a = R.choice((A['tree0'], A['tree1'], A['tree2']))
                s = R.uniform(.8, 1.3)
                inst(a, f'VEG_TREE_{k:05d}', V, (x + R.uniform(-4, 4), y + R.uniform(-4, 4), z - .3),
                     rot=(0, 0, R.uniform(0, 6.28)), scale=(s, s, s)); k += 1
    # a few trees inside the compound edges
    for p in [(-52, 50), (52, 50), (-52, -40), (52, -40), (-20, -48), (20, -48), (30, -110), (-30, -110)]:
        inst(A['tree2'], f'VEG_TREE_{k:05d}', V, (p[0], p[1], 0), rot=(0, 0, R.uniform(0, 6))); k += 1
    return k


# ======================================================================= lighting + cameras
def haze(nt, col, dens):
    """aerial perspective: a bounded volume box (12 x 12 km, 3 km high) — a world volume would block the sun."""
    o = bpy.data.objects.get('ATMOS_HAZE_VOLUME')
    if o is None:
        me = mesh_box('ATMOS_HAZE_VOLUME', 24000, 24000, 3200)
        o = bpy.data.objects.new('ATMOS_HAZE_VOLUME', me); C('ASHRAM/06_LIGHTING/ATMOSPHERE').objects.link(o)
        o.location = (0, 0, -100)
        m = bpy.data.materials.new('MAT_ATMOS_HAZE'); m.use_nodes = True
        m.node_tree.nodes.remove(m.node_tree.nodes['Principled BSDF'])
        v = m.node_tree.nodes.new('ShaderNodeVolumeScatter'); v.name = 'HAZE'
        m.node_tree.links.new(v.outputs[0], m.node_tree.nodes['Material Output'].inputs['Volume'])
        me.materials.append(m)
        o.visible_shadow = False
    v = o.data.materials[0].node_tree.nodes['HAZE']
    v.inputs['Color'].default_value = ck.hexlin(col); v.inputs['Density'].default_value = dens


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
    sd = bpy.data.lights.new('LIGHT_SUN' if not night else 'LIGHT_MOON', 'SUN')
    so = bpy.data.objects.new(sd.name, sd); L.objects.link(so)
    if not night:
        sky = nt.nodes.new('ShaderNodeTexSky')
        try:
            sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(28); sky.sun_rotation = math.radians(215)
        except Exception:
            pass
        nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = .32
        haze(nt, '#C4D6EA', .00009)
        sd.energy = 3.0; sd.angle = math.radians(1.0); sd.color = ck.hexlin('#FFEBD0')[:3]
        so.rotation_euler = (math.radians(58), 0, math.radians(35))
        bpy.data.materials['MAT_ASH_LANTERN_GLOW'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 0
    else:
        bg.inputs[0].default_value = ck.hexlin('#0C1426'); bg.inputs[1].default_value = .55
        haze(nt, '#2A3550', .00007)
        sd.energy = .25; sd.color = ck.hexlin('#9DB8FF')[:3]; so.rotation_euler = (math.radians(50), 0, math.radians(-40))
        bpy.data.materials['MAT_ASH_LANTERN_GLOW'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 25
        for o in [o for o in bpy.data.objects if o.name.startswith('PROP_LANTERN_')]:
            ld = bpy.data.lights.new('LIGHT_' + o.name, 'POINT'); ld.energy = 900; ld.color = ck.hexlin('#FFB35A')[:3]; ld.shadow_soft_size = .3
            lo = bpy.data.objects.new(ld.name, ld); lo.location = o.location + Vector((0, 0, .1)); L.objects.link(lo)
        ld = bpy.data.lights.new('LIGHT_HALL_INTERIOR_GLOW', 'AREA'); ld.energy = 6000; ld.size = 12; ld.color = ck.hexlin('#FFB870')[:3]
        lo = bpy.data.objects.new(ld.name, ld); lo.location = (0, 24, 4); lo.rotation_euler = (math.radians(90), 0, 0); L.objects.link(lo)


CAMS = [  # name, location, target, lens, res, caption
    ('CAM_01_WIDE_ESTABLISHING', (-110, -300, 30), (10, 60, 90), 24, (1600, 900), 'Wide establishing (from the lake side, south-west)'),
    ('CAM_02_FRONT', (0, -175, 7), (0, 10, 40), 34, (1280, 720), 'Front view (south axis, through the gate)'),
    ('CAM_03_BACK', (0, 260, 40), (0, 0, 6), 40, (1280, 720), 'Back view (from the north slope)'),
    ('CAM_04_SIDE_EAST', (260, 5, 22), (0, 5, 6), 40, (1280, 720), 'Side view (east)'),
    ('CAM_05_SIDE_WEST', (-260, 5, 22), (0, 5, 6), 40, (1280, 720), 'Side view (west)'),
    ('CAM_06_GROUND_LEVEL', (-6, -74, 1.6), (0, 30, 6), 24, (1280, 720), 'Ground level — character height (1.6 m) inside the gate'),
    ('CAM_07_ARCH_DETAIL', (13, 9, 4.5), (6, 22, 4.5), 35, (1280, 720), 'Architectural detail — main hall verandah, pillars, roof eaves'),
    ('CAM_08_TRAINING_GROUND', (-40, -150, 12), (0, -100, 0), 32, (1280, 720), 'Training ground (open ring, south of the gate)'),
    ('CAM_09_PAVILION_LAKE', (30, -125, 4), (62, -80, 4), 32, (1280, 720), 'Meditation pavilion + lake ghat'),
]


def cameras():
    Cc = C('ASHRAM/07_CAMERAS'); out = []
    for n, l, t, lens, res, cap in CAMS:
        c = ck.camera(n, Cc, l, t, lens=lens); c.data.clip_end = 20000; c['caption'] = cap
        out.append((c, res, cap))
    top = ck.camera('CAM_10_BIRDSEYE_ORTHO', Cc, (0, -20, 800), (0, -20, 0), ortho=300); top.data.clip_end = 5000
    top['caption'] = 'Bird\'s-eye layout (orthographic, north up, 300 m frame)'
    out.append((top, (1400, 1400), top['caption']))
    return out


def main():
    ck.reset()
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'; sc.unit_settings.length_unit = 'METERS'
    M = materials(); M['timber_dark'] = pmat('MAT_ASH_TIMBER_DARK', PAL['timber_dark'], .6)
    A = modules(M)
    ash = ashram(A, M)
    t, grid = terrain(M)
    ntree = scatter_trees(A, grid)
    org = bpy.data.objects.new('ASHRAM_ORIGIN', None); C('ASHRAM/00_REFERENCE').objects.link(org)
    world_feats = os.path.join(HERE, '..', 'map', 'data', 'features.json')
    if os.path.exists(world_feats):
        f = json.load(open(world_feats)); org['wcs_x_km'] = float(f['ashram'][0]); org['wcs_y_km'] = float(768 - f['ashram'][1])
    org['status'] = 'PROPOSAL v1 — awaiting Director approval'
    cams = cameras()
    lighting(False)
    ck.setup_render((1280, 720), SAMPLES)
    sc.view_settings.view_transform = 'AgX'
    sc.render.use_simplify = True; sc.render.simplify_subdivision_render = 2
    stats = {'objects': len(bpy.data.objects), 'meshes': len(bpy.data.meshes), 'trees': ntree,
             'materials': len(bpy.data.materials), 'module_assets': len([o for o in bpy.data.objects if o.get('asset_kit')])}
    out = os.path.join(ROOT, '01_BLOCKOUT', 'ASHRAM_blockout_v001.blend')
    bpy.ops.wm.save_as_mainfile(filepath=out)
    json.dump({'stats': stats, 'cameras': [(c.name, cap) for c, r, cap in cams]}, open(os.path.join(ROOT, '01_BLOCKOUT', 'blockout_info.json'), 'w'), indent=1)
    print('SAVED', out, stats, flush=True)
    if not RENDER:
        return
    for cam, res, cap in cams:
        sc.render.resolution_x, sc.render.resolution_y = res
        ck.render_to(os.path.join(OUTR, f'{cam.name}_day.png'), cam)
    lighting(True)
    for cam, res, cap in cams:
        if cam.name in ('CAM_01_WIDE_ESTABLISHING', 'CAM_06_GROUND_LEVEL', 'CAM_02_FRONT'):
            sc.render.resolution_x, sc.render.resolution_y = res
            ck.render_to(os.path.join(OUTR, f'{cam.name}_night.png'), cam)
    print('RENDERS DONE', flush=True)


if __name__ == '__main__':
    main()

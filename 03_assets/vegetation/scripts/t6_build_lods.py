"""TASK 06 · variants + LODs per region (Blender 4.5) — keeps the hero library files small (< 95 MB each).

    BPY45 t6_build_lods.py -- <REGION>              (needs the impostor textures: t6_render_impostors.py)

Writes two files next to the hero library T6_VEG_<REGION>_v001.blend:
  T6_VEG_<REGION>_VARIANTS_v001.blend   seeds 1 + 2 of every species (seed 0 = the hero asset) → 3 variants per species.
                                        Trees with a heavy hero (> 150 k tris) get their variants at LOD1 density (same shape
                                        rules, fewer leaf cards / ring sides) so the file stays < 95 MB.
  T6_VEG_<REGION>_LODS_v001.blend       per species (seed 0, same skeleton as the hero):
                                        LOD1  (≈ 40–150 m)  half the ring sides, 40 % leaf cards × 1.5 size (same silhouette)
                                        LOD2  (≈ 150–600 m) third of the sides, 18 % cards × 2.2, no finest twigs
                                        LOD3  (> 600 m)     2 crossed impostor cards (front + side render with alpha)
                                        plants: LOD1 = ~40 % blades / stems (wider), used beyond ≈ 25 m
Every LOD / variant carries the wind modifier (same NG_T6_WIND, its own T6_WIND_CONTROL), metadata (t6_lod, t6_variant_seed,
t6_lod_range_m) and sits in its own collection T6_<asset>_LOD<n> / T6_<asset>_V<seed> at the origin (ready for scatter).
"""
import os, sys, json, copy, shutil, datetime, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
from mathutils import Vector
import t6kit as K
import t6_regions as RG

REG = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'AV'
NM = RG.NAMES[REG]
LIB = os.environ.get('T6_LIB_DIR') or os.path.join(K.VEG, 'library')
IMP = os.path.join(K.VEG, 'textures', 'impostors')
WHAT = os.environ.get('WHAT', 'variants,lods').split(',')
LOD_RANGE = {0: (0, 40), 1: (40, 150), 2: (150, 600), 3: (600, 100000)}
PLANT_LOD_RANGE = {0: (0, 25), 1: (25, 80)}


def lod_spec(S, lod):
    """same species spec, lighter geometry. Skeleton (trunk / branch paths) is unchanged because the branch levels and their
    segment counts are kept (the generator draws its random numbers in the same order); only ring sides + leaf cards change."""
    S = copy.deepcopy(S)
    if S.get('builder') == 'palm':
        S['palm']['tsides'] = {1: 10, 2: 6}[lod]; S['palm']['lsegs'] = {1: 2, 2: 1}[lod]
        return S
    S['sides'] = [max(3, int(round(s / {1: 2.0, 2: 3.0}[lod]))) for s in S.get('sides', [20, 10, 6, 4, 3])]
    Lf = S.get('leaves')
    if Lf:
        Lf['per_m'] = Lf['per_m'] * {1: .4, 2: .18}[lod]; Lf['scale'] = Lf.get('scale', 1.0) * {1: 1.5, 2: 2.2}[lod]
    if lod == 2 and len(S['levels']) > 2:
        S['levels'] = S['levels'][:-1]                       # finest twigs dropped (invisible beyond 150 m)
    if S.get('beards'):
        S['beards']['n'] = int(S['beards']['n'] * {1: .5, 2: .25}[lod]); S['beards']['scale'] = S['beards'].get('scale', 1.0) * {1: 1.3, 2: 1.7}[lod]
    if S.get('pods'):
        S['pods']['n'] = int(S['pods']['n'] * {1: .6, 2: .3}[lod])
    return S


def plant_lod(D):
    D = copy.deepcopy(D); P = D['P']
    for k in ('blades', 'stems', 'basal', 'stem_leaves', 'fronds', 'pads', 'strands', 'n', 'sporophytes', 'spikes', 'arms', 'base_shoots'):
        if isinstance(P.get(k), int) and P[k] > 1:
            P[k] = max(1, int(round(P[k] * .4)))
    if 'w' in P and isinstance(P['w'], float):
        P['w'] *= 1.45
    if 'pinnae' in P:
        P['pinnae'] = max(8, int(P['pinnae'] * .55))
    if P.get('flower', {}).get('n', 0) > 20:
        P['flower']['n'] = int(P['flower']['n'] * .4)
    return D


def coll(name, parent):
    c = bpy.data.collections.new(name); parent.children.link(c); return c


def wind(o, D, kind):
    H = float(o.get('t6_height_m', 1.0))
    if kind == 'tree':
        W = D.get('wind')
        if W:
            K.add_wind(o, trunk=W['trunk'] * H, branch=W['branch'], leaf=W['leaf'], flex=1.0)
        else:
            K.add_wind(o, trunk=.02 * H, branch=.22 + .006 * H, leaf=.05, flex=1.0 if D['category'] != 'Dead tree' else .35)
    elif kind == 'shrub':
        K.add_wind(o, trunk=.04, branch=.12 if not D['category'].startswith('Dead') else .05, leaf=.03)
    else:
        W = D.get('wind')
        if W and (W['branch'] > 0 or W['leaf'] > 0):
            K.add_wind(o, trunk=0.0, branch=W['branch'], leaf=W['leaf'])
        elif not W and D['kind'] not in ('moss', 'mushrooms'):
            K.add_wind(o, trunk=0.0, branch=.30 if D['kind'] != 'vine' else .5, leaf=.03 if D['kind'] != 'lotus' else .012)


def tag(o, D, kind, lod, seed, rng_m):
    for k in ('common', 'latin', 'label', 'region', 'category'):
        o[f't6_{k}'] = str(D.get(k, ''))
    o['t6_kind'] = kind; o['t6_lod'] = lod; o['t6_variant_seed'] = seed; o['t6_lod_range_m'] = list(rng_m)
    o['t6_hero'] = D['name']; o['t6_version'] = 'v001 (TASK 06 milestone 2 — variants / LODs)'


def impostor(D, c):
    """LOD3: two crossed vertical cards — XZ plane textured with the FRONT render (camera on −Y, image x = world X) and YZ plane with
    the SIDE render (camera on +X, image x = world Y); exact metric framing from impostors.json (t6_render_impostors.py)."""
    meta = json.load(open(os.path.join(IMP, 'impostors.json')))[D['name']]
    G = K.Geo(); mats = []
    for mi, (view, ax) in enumerate((('front', Vector((1, 0, 0))), ('side', Vector((0, 1, 0))))):
        m = meta[view]; w0, w1, z0, z1 = m['wmin'], m['wmax'], m['zmin'], m['zmax']
        pts = [ax * w0 + Vector((0, 0, z0)), ax * w1 + Vector((0, 0, z0)), ax * w1 + Vector((0, 0, z1)), ax * w0 + Vector((0, 0, z1))]
        zt = np.clip(np.array([z0, z0, z1, z1]) / max(z1, 1e-3), 0, 1)
        i0 = G.add_verts(pts, wind_trunk=zt ** 1.5, wind_branch=zt * .3, wind_leaf=0.0, wind_phase=mi * .3, leaf_rand=.5)
        G.add_face((i0, i0 + 1, i0 + 2, i0 + 3), ((0, 0), (1, 0), (1, 1), (0, 1)), mi)
    for view in ('front', 'side'):
        mt, nt, b = K.new_mat(f"MAT_T6_{D['name']}_IMP_{view.upper()}")
        out = b.n('ShaderNodeOutputMaterial'); bs = b.n('ShaderNodeBsdfPrincipled'); tx = b.n('ShaderNodeTexImage')
        tx.image = K.img(os.path.join(IMP, f"{D['name']}_{view}.png")); tx.image.alpha_mode = 'STRAIGHT'
        b.l(tx.outputs['Color'], bs.inputs['Base Color']); b.l(tx.outputs['Alpha'], bs.inputs['Alpha'])
        bs.inputs['Roughness'].default_value = .7; bs.inputs['Specular IOR Level'].default_value = .25
        b.l(bs.outputs[0], out.inputs['Surface'])
        mats.append(mt)
    me = G.to_mesh(f"{D['name']}_LOD3", mats)
    o = bpy.data.objects.new(f"{D['name']}_LOD3", me); c.objects.link(o)
    o['t6_height_m'] = float(meta['front']['zmax'])
    return o


def make_scatter_copies(objs, root_name):
    """<asset>_SC: same mesh, NO wind modifier — used by NG_T6_ECOSYSTEM (wind applied once per instance there). The asset's wind
    amplitudes are copied as t6_wind_* properties. Collections T6_<asset>_SC live under <root>_SCATTER (fake user, not in the scene)."""
    sroot = bpy.data.collections.new(root_name + '_SCATTER'); sroot.use_fake_user = True
    for o in objs:
        so = bpy.data.objects.new(o.name + '_SC', o.data)
        for k in o.keys():
            if k.startswith('t6_'):
                so[k] = o[k]
        md = o.modifiers.get('T6_WIND')
        if md:
            ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
            for nm_, key in (('Trunk Sway (m)', 'trunk'), ('Branch Sway (m)', 'branch'), ('Leaf Flutter (m)', 'leaf'),
                             ('Natural Freq (Hz)', 'fn'), ('Flexibility', 'flex'), ('Damping', 'damping')):
                so[f't6_wind_{key}'] = float(md[ids[nm_]])
        c = bpy.data.collections.new(f'T6_{o.name}_SC'); sroot.children.link(c); c.objects.link(so)
    return sroot


def protect(o, tag):
    """K.new_mat() deletes an existing material of the same name — so the materials of an object that is already built get a
    unique suffix before the next variant / LOD of the same species is generated (otherwise its slots become empty → white)."""
    for i, m in enumerate(o.data.materials):
        if m is not None and not m.name.endswith(tag):
            m.name = m.name + tag


def save(path, inv):
    missing = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath))]
    assert not missing, missing
    empty = [o.name for o in bpy.data.objects if o.type == 'MESH' and any(m is None for m in o.data.materials)]
    assert not empty, f'empty material slots: {empty[:5]}'
    if os.path.exists(path):
        bdir = os.path.join(LIB, '_backups'); os.makedirs(bdir, exist_ok=True)
        shutil.copy2(path, os.path.join(bdir, os.path.basename(path)[:-6] + '__backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.blend'))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True, relative_remap=True)
    json.dump(inv, open(path[:-6].replace('_v001', '') + '_inventory.json', 'w'), indent=1)
    print('SAVED', path, round(os.path.getsize(path) / 1e6, 1), 'MB', len(inv), 'objects', flush=True)


woody = [(D, 'tree') for D in RG.TREES if RG.region_of(D['name']) == REG] + [(D, 'shrub') for D in RG.SHRUBS if RG.region_of(D['name']) == REG]
plants = [D for D in RG.PLANTS if RG.region_of(D['name']) == REG]
hero_inv = json.load(open(os.path.join(LIB, f'T6_VEG_{NM}_inventory.json')))

for what in WHAT:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.name = 'T6_LIBRARY'; sc.unit_settings.system = 'METRIC'; sc.render.fps = 24
    root = coll(f'T6_LIB_{NM}_{what.upper()}', sc.collection)
    K.wind_control(); K.wind_instances_group(); INV = {}
    if what == 'variants':
        for D, kind in woody:
            heavy = hero_inv.get(D['name'], {}).get('stats', {}).get('tris', 0) > 150_000      # keeps every VARIANTS file < 95 MB
            for seed in (1, 2):
                c = coll(f"T6_{D['name']}_V{seed}", root)
                S = lod_spec(D, 1) if heavy else D
                o, st = RG.build_woody(S, seed, c); o.name = f"{D['name']}_V{seed}"; protect(o, f'_V{seed}')
                o['t6_height_m'] = st['height_m']; wind(o, D, kind); tag(o, D, kind, 1 if heavy else 0, seed, LOD_RANGE[1 if heavy else 0])
                INV[o.name] = dict(hero=D['name'], kind=kind, seed=seed, lod=1 if heavy else 0, stats=st, collection=c.name)
                print('VARIANT', o.name, st['height_m'], st['tris'], flush=True)
        for D in plants:
            for seed in (1, 2):
                c = coll(f"T6_{D['name']}_V{seed}", root)
                o, st = RG.build_plant(D, seed, c); o.name = f"{D['name']}_V{seed}"; protect(o, f'_V{seed}')
                o['t6_height_m'] = st['height_m']; wind(o, D, 'plant'); tag(o, D, 'plant', 0, seed, PLANT_LOD_RANGE[0])
                INV[o.name] = dict(hero=D['name'], kind='plant', seed=seed, lod=0, stats=st, collection=c.name)
        make_scatter_copies([bpy.data.objects[n] for n in INV], f'T6_LIB_{NM}_VARIANTS')
        save(os.path.join(LIB, f'T6_VEG_{NM}_VARIANTS_v001.blend'), INV)
    elif what == 'lods':
        for D, kind in woody:
            for lod in (1, 2):
                c = coll(f"T6_{D['name']}_LOD{lod}", root)
                o, st = RG.build_woody(lod_spec(D, lod), 0, c); o.name = f"{D['name']}_LOD{lod}"; protect(o, f'_LOD{lod}')
                o['t6_height_m'] = st['height_m']; wind(o, D, kind); tag(o, D, kind, lod, 0, LOD_RANGE[lod])
                INV[o.name] = dict(hero=D['name'], kind=kind, seed=0, lod=lod, stats=st, collection=c.name)
                print('LOD', o.name, st['tris'], flush=True)
            if os.path.exists(os.path.join(IMP, f"{D['name']}_front.png")):
                c = coll(f"T6_{D['name']}_LOD3", root)
                o = impostor(D, c)
                K.add_wind(o, trunk=.012 * o['t6_height_m'], branch=0.0, leaf=0.0); tag(o, D, kind, 3, 0, LOD_RANGE[3])
                INV[o.name] = dict(hero=D['name'], kind=kind, seed=0, lod=3, stats=dict(tris=6, height_m=o['t6_height_m']), collection=c.name)
        for D in plants:
            c = coll(f"T6_{D['name']}_LOD1", root)
            o, st = RG.build_plant(plant_lod(D), 0, c); o.name = f"{D['name']}_LOD1"; protect(o, '_LOD1')
            o['t6_height_m'] = st['height_m']; wind(o, D, 'plant'); tag(o, D, 'plant', 1, 0, PLANT_LOD_RANGE[1])
            INV[o.name] = dict(hero=D['name'], kind='plant', seed=0, lod=1, stats=st, collection=c.name)
        make_scatter_copies([bpy.data.objects[n] for n in INV], f'T6_LIB_{NM}_LODS')
        save(os.path.join(LIB, f'T6_VEG_{NM}_LODS_v001.blend'), INV)
print('T6_LODS_DONE', REG)

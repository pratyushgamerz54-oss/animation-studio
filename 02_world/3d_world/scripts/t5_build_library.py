"""TASK 05 · NATURE ASSET LIBRARY → 14_NATURE_LIBRARY/T5_NATURE_LIBRARY_v002.blend (Blender 4.5 LTS).

One library for every scene (CLAUDE.md: "saare assets ek library mein"): Poly Haven CC0 scans appended once, re-centred
(base at z = 0, trunk / centre at the origin), grouped by use. Scatter systems instance the CATEGORY collections with
"separate children" → every child (a species sub-collection or a single rock) is one random pick.
  LIB_TREES_NEAR / LIB_TREES_MID / LIB_TREES_FAR   same species at 3 levels of detail (far = 150-tri proxies)
  LIB_GROVE_NEAR / _MID / _FAR                     open-valley grove mix (more broadleaf)
  LIB_UNDERSTORY · LIB_GRASS · LIB_FLOWERS · LIB_FOREST_DEBRIS · LIB_ROCKS_SMALL · LIB_ROCKS_MEDIUM · LIB_ROCKS_LARGE
Images stay in 03_assets/external/polyhaven (relative paths; fetch with polyhaven_fetch.py).
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix
import worldkit as wk
import t5kit as tk

wk.new_file()
sc = bpy.context.scene; sc.name = 'T5_NATURE_LIBRARY'
root = wk.coll('T5_NATURE_LIBRARY')
INV = {}


def append(model, coll_name):
    f = os.path.join(tk.PH, 'models', model, f'{model}_1k.blend')
    with bpy.data.libraries.load(f, link=False) as (src, dst):
        if coll_name not in src.collections:
            raise KeyError(f'{model}: no collection {coll_name} (have {list(src.collections)})')
        dst.collections = [coll_name]
    return dst.collections[0]


def bbox(objs):
    pts = []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type != 'MESH':
            continue
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    P = np.array([tuple(p) for p in pts])
    return P.min(0), P.max(0)


def recentre_group(objs, mode='trunk'):
    """move top-level objects so the group base sits at z=0 and its XY centre at the origin."""
    bpy.context.view_layer.update()
    mn, mx = bbox(objs)
    c = np.array([(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]])
    if mode == 'trunk':           # trees: use the lowest 5 % of the geometry (the trunk foot) for the XY centre
        low = []
        for o in objs:
            if o.type == 'MESH':
                M = np.array(o.matrix_world)
                V = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
                V = V @ M[:3, :3].T + M[:3, 3]
                low.append(V[V[:, 2] < mn[2] + .05 * (mx[2] - mn[2])])
        L = np.concatenate(low) if low else None
        if L is not None and len(L):
            c[0], c[1] = L[:, 0].mean(), L[:, 1].mean()
    for o in objs:
        if o.parent is None:
            o.location = Vector(o.location) - Vector(c)
    bpy.context.view_layer.update()
    mn, mx = bbox(objs)
    return [float(x) for x in (mx - mn)]


def recentre_object(o, mode='box'):
    """bake the object's transform into its own mesh; origin = bottom centre (box) or trunk foot (trunk)."""
    bpy.context.view_layer.update()
    M = o.matrix_world.copy()
    o.data = o.data.copy()
    o.data.transform(M); o.matrix_world = Matrix.Identity(4)
    mn, mx = bbox([o])
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    if mode == 'trunk':
        V = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
        low = V[V[:, 2] < mn[2] + .04 * (mx[2] - mn[2])]
        if len(low):
            cx, cy = low[:, 0].mean(), low[:, 1].mean()
    o.data.transform(Matrix.Translation(Vector((-cx, -cy, -mn[2]))))
    bpy.context.view_layer.update()
    mn, mx = bbox([o])
    return [float(x) for x in (mx - mn)]


def singles(model, coll_name, parent, prefix, mode='box', also=()):
    """every object of a Poly Haven collection = one variant (Poly Haven ships 3–6 variants per LOD collection) →
    linked directly in `parent` (+ `also`), origin at the trunk foot / bottom centre."""
    src = append(model, coll_name)
    out = []
    for i, o in enumerate(sorted([o for o in src.all_objects if o.type == 'MESH'], key=lambda o: o.name)):
        parent.objects.link(o)
        for c in also:
            c.objects.link(o)
        o.name = f'{prefix}_{chr(65 + i)}'
        dims = recentre_object(o, mode)
        INV[o.name] = dict(source=f'Poly Haven {model} / {coll_name} (CC0)', dims_m=[round(x, 2) for x in dims],
                           tris=sum(len(p.vertices) - 2 for p in o.data.polygons), category=[parent.name] + [c.name for c in also])
        out.append(o)
    bpy.data.collections.remove(src)
    return out


KIND = os.environ.get('T5_LIB', 'trees')
OUT = wk.P('14_NATURE_LIBRARY', f'T5_NATURE_LIBRARY_{KIND.upper()}_v002.blend')
if KIND == 'trees':
    cat = {k: wk.coll(k, root) for k in ('LIB_TREES_NEAR', 'LIB_TREES_MID', 'LIB_TREES_FAR', 'LIB_GROVE_NEAR', 'LIB_GROVE_MID',
                                         'LIB_GROVE_FAR', 'LIB_SAPLINGS')}
    singles('fir_tree_01', 'fir_tree_01_LOD1', cat['LIB_TREES_NEAR'], 'TREE_FIR_LOD1', 'trunk', (cat['LIB_GROVE_NEAR'],))
    singles('fir_tree_01', 'fir_tree_01_LOD2', cat['LIB_TREES_MID'], 'TREE_FIR_LOD2', 'trunk', (cat['LIB_GROVE_MID'],))
    singles('pine_tree_01', 'pine_tree_01_LOD2', cat['LIB_TREES_NEAR'], 'TREE_PINE_LOD2', 'trunk', (cat['LIB_TREES_MID'],))
    singles('tree_small_02', 'tree_small_02_LOD1', cat['LIB_GROVE_NEAR'], 'TREE_BROADLEAF_LOD1', 'trunk', (cat['LIB_GROVE_MID'],))
    singles('fir_sapling_medium', 'fir_sapling_medium_LOD1', cat['LIB_SAPLINGS'], 'TREE_FIR_YOUNG_LOD1', 'trunk')
    mats = wk.link_materials(['MAT_T5_TREE_FAR', 'MAT_T5_TRUNK_FAR'], tk.MATLIB2)

    def proxy(name, height, radius, tiers, shape, parent, also=()):
        """far-distance tree proxy (~150 tris): stacked cones (conifer) or a lumpy ellipsoid (broadleaf) + trunk, ONE object."""
        bm = bmesh.new(); n = 8
        if shape == 'cone':
            for t in range(tiers):
                z0 = height * (.18 + .82 * t / tiers); z1 = z0 + height * .82 / tiers * 1.7
                r = radius * (1 - t / tiers) ** .9 + .3
                ring = [bm.verts.new((math.cos(a) * r, math.sin(a) * r, z0)) for a in np.linspace(0, 2 * np.pi, n, endpoint=False)]
                tip = bm.verts.new((0, 0, min(z1, height)))
                for i in range(n):
                    bm.faces.new((ring[i], ring[(i + 1) % n], tip))
                bm.faces.new(ring[::-1])
        else:
            bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
            rng = np.random.default_rng(3)
            for v in bm.verts:
                v.co.x *= radius * (1 + rng.uniform(-.12, .12)); v.co.y *= radius * (1 + rng.uniform(-.12, .12))
                v.co.z = v.co.z * height * .32 + height * .62
        nf = len(bm.faces)
        # trunk (6-sided frustum) in the same mesh → material slot 1
        tb = [bm.verts.new((math.cos(a) * (radius * .08 + .1), math.sin(a) * (radius * .08 + .1), 0)) for a in np.linspace(0, 2 * np.pi, 6, endpoint=False)]
        tt = [bm.verts.new((math.cos(a) * (radius * .05 + .05), math.sin(a) * (radius * .05 + .05), height * .35)) for a in np.linspace(0, 2 * np.pi, 6, endpoint=False)]
        for i in range(6):
            f = bm.faces.new((tb[i], tb[(i + 1) % 6], tt[(i + 1) % 6], tt[i])); f.material_index = 1
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        me.materials.append(mats['MAT_T5_TREE_FAR']); me.materials.append(mats['MAT_T5_TRUNK_FAR'])
        o = bpy.data.objects.new(name, me); parent.objects.link(o)
        for c in also:
            c.objects.link(o)
        INV[name] = dict(source='procedural far proxy', dims_m=[radius * 2, radius * 2, height], tris=len(me.polygons), category=[parent.name])
        return o
    proxy('TREE_FIR_PROXY_A', 14.5, 2.9, 6, 'cone', cat['LIB_TREES_FAR'], (cat['LIB_GROVE_FAR'],))
    proxy('TREE_FIR_PROXY_B', 12.0, 2.4, 5, 'cone', cat['LIB_TREES_FAR'])
    proxy('TREE_PINE_PROXY', 17.0, 3.6, 4, 'cone', cat['LIB_TREES_FAR'])
    proxy('TREE_BROADLEAF_PROXY', 4.6, 1.8, 0, 'blob', cat['LIB_GROVE_FAR'])
else:
    cat = {k: wk.coll(k, root) for k in ('LIB_UNDERSTORY', 'LIB_GRASS', 'LIB_FLOWERS', 'LIB_FOREST_DEBRIS', 'LIB_LOGS',
                                         'LIB_ROCKS_SMALL', 'LIB_ROCKS_MEDIUM', 'LIB_ROCKS_LARGE')}
    singles('fern_02', 'fern_02', cat['LIB_UNDERSTORY'], 'PLANT_FERN')
    singles('shrub_02', 'shrub_02_LOD1', cat['LIB_UNDERSTORY'], 'PLANT_SHRUB02')
    singles('shrub_03', 'shrub_03_LOD1', cat['LIB_UNDERSTORY'], 'PLANT_SHRUB03')
    singles('shrub_04', 'shrub_04_LOD1', cat['LIB_UNDERSTORY'], 'PLANT_SHRUB04')
    singles('grass_medium_02', 'grass_medium_02_static', cat['LIB_GRASS'], 'GRASS_MED02')
    singles('grass_medium_01', 'grass_medium_01_LOD1', cat['LIB_GRASS'], 'GRASS_MED01')
    singles('dandelion_01', 'dandelion_01_LOD1', cat['LIB_FLOWERS'], 'PLANT_DANDELION')
    singles('nettle_plant', 'nettle_plant_LOD1', cat['LIB_FLOWERS'], 'PLANT_NETTLE')
    singles('dead_tree_trunk_02', 'dead_tree_trunk_02_LOD1', cat['LIB_LOGS'], 'LOG_FALLEN_A')
    singles('dead_tree_trunk', 'dead_tree_trunk', cat['LIB_LOGS'], 'LOG_FALLEN_B')
    singles('tree_stump_01', 'tree_stump_01', cat['LIB_FOREST_DEBRIS'], 'DEBRIS_STUMP')
    singles('root_cluster_01', 'root_cluster_01', cat['LIB_FOREST_DEBRIS'], 'DEBRIS_ROOTS_A')
    singles('pine_roots', 'pine_roots', cat['LIB_FOREST_DEBRIS'], 'DEBRIS_ROOTS_PINE')
    singles('bark_debris_01', 'bark_debris_01_LOD2', cat['LIB_FOREST_DEBRIS'], 'DEBRIS_BARK')
    singles('dry_branches_medium_01', 'dry_branches_medium_01', cat['LIB_FOREST_DEBRIS'], 'DEBRIS_BRANCHES')
    singles('stone_01', 'stone_01_LOD1', cat['LIB_ROCKS_SMALL'], 'ROCK_S_STONE')
    singles('rock_07', 'rock_07_LOD1', cat['LIB_ROCKS_SMALL'], 'ROCK_S_ROCK07')
    singles('rock_09', 'rock_09_LOD1', cat['LIB_ROCKS_SMALL'], 'ROCK_S_ROCK09')
    singles('boulder_01', 'boulder_01_LOD1', cat['LIB_ROCKS_MEDIUM'], 'ROCK_M_BOULDER01')
    singles('rock_moss_set_01', 'rock_moss_set_01', cat['LIB_ROCKS_MEDIUM'], 'ROCK_M_MOSS01')
    singles('rock_moss_set_02', 'rock_moss_set_02', cat['LIB_ROCKS_MEDIUM'], 'ROCK_M_MOSS02')
    singles('namaqualand_boulder_02', 'namaqualand_boulder_02_LOD1', cat['LIB_ROCKS_MEDIUM'], 'ROCK_M_BOULDER02')
    singles('namaqualand_boulder_03', 'namaqualand_boulder_03_LOD1', cat['LIB_ROCKS_MEDIUM'], 'ROCK_M_BOULDER03')
    singles('rock_face_01', 'rock_face_01', cat['LIB_ROCKS_LARGE'], 'ROCK_L_FACE01')
    singles('rock_face_02', 'rock_face_02', cat['LIB_ROCKS_LARGE'], 'ROCK_L_FACE02')
    singles('mountainside', 'mountainside_LOD2', cat['LIB_ROCKS_LARGE'], 'ROCK_L_MOUNTAINSIDE')

# hide the library from render (it is instanced by scatter systems), lay species out in a row for the viewport
for o in bpy.data.objects:
    o.hide_render = False
missing = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath))]
assert not missing, missing
for c in bpy.data.collections:
    c.use_fake_user = False
wk.add_props(sc, status='TASK 05 nature library (Poly Haven CC0 + procedural far proxies)', inventory=json.dumps(INV))
wk.save(OUT)
json.dump(INV, open(wk.P('14_NATURE_LIBRARY', f'T5_nature_library_{KIND}_inventory.json'), 'w'), indent=1)
print('MISSING_IMAGES', missing)
print('T5_LIBRARY_DONE', len(INV), 'assets')

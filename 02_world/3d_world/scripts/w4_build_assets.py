"""TASK 04 · reusable blockout components → 04_FORESTS/FOREST_proxies_v001.blend (Blender 4.5).

Low-poly vegetation PROXIES for instancing (Geometry Nodes) — blockout stand-ins, replaced by final trees later
(Poly Haven CC0 trees already used in Ashram concept v3). Origins at the trunk base, +Z up, metres.
  PROXY_TREES_NEAR  conifer A/B + broadleaf (≈ 60–160 tris each) — near terrain (LOD0)
  PROXY_CANOPY_FAR  canopy clumps (groups of trees as one blob) — mid terrain (LOD1)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import worldkit as wk

wk.new_file()
bpy.context.scene.name = 'COMPONENT_04_FOREST_PROXIES'
M = wk.link_materials(['MAT_V_TREE_CONIFER', 'MAT_V_TREE_BROADLEAF', 'MAT_V_TREE_CANOPY', 'MAT_V_TRUNK'])
top = wk.coll('FOREST_PROXIES')
near = wk.coll('PROXY_TREES_NEAR', top); far = wk.coll('PROXY_CANOPY_FAR', top)
import bmesh


def join(name, parts, c):
    for o_ in bpy.context.view_layer.objects:
        o_.select_set(False)
    bpy.context.view_layer.objects.active = parts[0]
    for p in parts:
        p.select_set(True)
    bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = name; o.data.name = name
    for cc in list(o.users_collection):
        cc.objects.unlink(o)
    c.objects.link(o)
    return o


tmp = wk.coll('TMP')
for nm, h, r in (('PROXY_CONIFER_A', 24, 4.2), ('PROXY_CONIFER_B', 17, 3.4)):
    tr = wk.cone(nm + '_trunk', .45, h * .25, 6, tmp, M['MAT_V_TRUNK'], r_top=.35)
    c1 = wk.cone(nm + '_c1', r, h * .55, 8, tmp, M['MAT_V_TREE_CONIFER'], z0=h * .18)
    c2 = wk.cone(nm + '_c2', r * .72, h * .5, 8, tmp, M['MAT_V_TREE_CONIFER'], z0=h * .5)
    o = join(nm, [tr, c1, c2], near); o['proxy'] = f'conifer, height {h} m (blockout stand-in)'
tr = wk.cone('PROXY_BROADLEAF_trunk', .5, 7, 6, tmp, M['MAT_V_TRUNK'], r_top=.4)
cr = wk.blob('PROXY_BROADLEAF_crown', 5.5, tmp, M['MAT_V_TREE_BROADLEAF'], squash=.8, subdiv=1, seed=2); cr.location.z = 10
for o_ in bpy.context.view_layer.objects:
    o_.select_set(False)
bpy.context.view_layer.objects.active = cr; cr.select_set(True); bpy.ops.object.transform_apply(location=True)
o = join('PROXY_BROADLEAF', [tr, cr], near); o['proxy'] = 'broadleaf, height ≈ 15 m'
for i, (r, sq) in enumerate(((26, .42), (34, .36))):
    b = wk.blob(f'PROXY_CANOPY_CLUMP_{i + 1}', r, far, M['MAT_V_TREE_CANOPY'], squash=sq, subdiv=2, seed=10 + i, rough=.28)
    for v in b.data.vertices:
        v.co.z = max(v.co.z, -2.0) + r * sq * .55
    b['proxy'] = f'canopy clump ≈ {2 * r} m across (stand-in for a group of trees, mid distance)'
bpy.data.collections.remove(tmp)
for o in bpy.data.objects:
    if o.type == 'MESH':
        wk.display_color(o, '#2C4A2C')
wk.save(wk.P('04_FORESTS', 'FOREST_proxies_v001.blend'))
print('proxies', [o.name for o in bpy.data.objects])
print('BUILD_ASSETS_DONE')

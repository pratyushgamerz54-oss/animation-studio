"""t7_scan_reduce — make a photogrammetry / museum scan usable in the library: decimate, textures → 2K copies, real size, save .blend.

usage: $BPY45 t7_scan_reduce.py <scene.gltf> <species_id> <out.blend> [--ratio 0.35] [--tex 2048] [--length 0.85]
The original scan stays outside git (re-download with t7_sketchfab.py get <uid>); 4K/8K textures for final close-ups come from it.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import t7kit as K
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, sid, out = a[0], a[1], a[2]
opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
ratio, texs = opt('--ratio', 0.35), opt('--tex', 2048)
K.clean()
bpy.ops.import_scene.gltf(filepath=src)
if '--frame' in a:                                    # animated bases: pose at this frame (e.g. wings spread flat) before joining
    bpy.context.scene.frame_set(int(opt('--frame', 0))); bpy.context.view_layer.update()
    for o in [o for o in bpy.data.objects if o.type == 'MESH']:
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    for o in bpy.data.objects:
        o.animation_data_clear()
if '--delete-obj' in a:                               # stray helper objects by name (e.g. a 'Cube' left in the export)
    for n in a[a.index('--delete-obj') + 1].split(','):
        for o in [o for o in bpy.data.objects if o.name == n]:
            bpy.data.objects.remove(o)
if '--delete-mat' in a:                               # helper objects in specimen scans (colour checker card, scale cube) by material
    dm = a[a.index('--delete-mat') + 1].split(',')
    for o in [o for o in bpy.data.objects if o.type == 'MESH' and o.active_material and o.active_material.name in dm]:
        bpy.data.objects.remove(o)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
if '--join' in a and len(meshes) > 1:                 # split scans / AI meshes: join + weld seams first (decimating pieces separately opens holes)
    for x in bpy.context.view_layer.objects:
        x.select_set(False)
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    with bpy.context.temp_override(active_object=meshes[0], selected_editable_objects=meshes, selected_objects=meshes):
        bpy.ops.object.join()
    meshes = [meshes[0]]
    import bmesh
    bm = bmesh.new(); bm.from_mesh(meshes[0].data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=opt('--weld', 0.0005)); bm.to_mesh(meshes[0].data); bm.free()
for m_ in bpy.data.materials:                          # realism: no metal / plastic sheen from glTF metallicRoughness maps
    b_ = m_.node_tree.nodes.get('Principled BSDF') if m_.use_nodes else None
    if b_:
        for k in ('Metallic', 'Roughness'):
            for l in list(b_.inputs[k].links):
                m_.node_tree.links.remove(l)
        b_.inputs['Metallic'].default_value = 0.0; b_.inputs['Roughness'].default_value = 0.7; b_.inputs['Specular IOR Level'].default_value = 0.25
for o in (meshes if ratio < 0.999 else []):
    m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = ratio; m.use_collapse_triangulate = True
    K._apply(o, m)
    print(o.name, 'faces', len(o.data.polygons))
tex = os.path.join(K.CR, '11_TEXTURES', sid); os.makedirs(tex, exist_ok=True)
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
for img in list(bpy.data.images):
    if img.type != 'IMAGE':
        continue
    name = os.path.splitext(img.name)[0]
    if img.packed_file:                                   # glTF importer may pack the images → write them out first (never keep 8K packed)
        tmp = os.path.join(tex, '_tmp_' + name + '.png'); img.filepath_raw = tmp; img.file_format = 'PNG'; img.save()
        p = tmp
    else:
        p = bpy.path.abspath(img.filepath)
    if not os.path.exists(p):
        continue
    im = Image.open(p); im.thumbnail((texs, texs))
    ext = '.jpg' if 'diffuse' in name.lower() or 'basecolor' in name.lower() else '.png'
    dst = os.path.join(tex, f'T7_{sid.upper()}_{name}_{texs // 1024}k{ext}')
    (im.convert('RGB').save(dst, quality=90) if ext == '.jpg' else im.save(dst))
    new_img = bpy.data.images.load(dst)
    new_img.colorspace_settings.name = img.colorspace_settings.name
    img.user_remap(new_img); bpy.data.images.remove(img)
    if p.startswith(os.path.join(tex, '_tmp_')):
        os.remove(p)
# real size: longest horizontal extent → field-guide body length (bill tip to tail tip, incl. perch if present is ignored)
dg = bpy.context.evaluated_depsgraph_get()
P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in meshes])
root = next(o for o in bpy.data.objects if o.parent is None)
L = opt('--height', 0.0)
if L:
    s = L / np.ptp(P[:, 2]); root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in meshes])
Lh = opt('--length', 0.0)
if Lh:                                                    # insects / flat subjects: longest horizontal extent → real length
    s = Lh / max(np.ptp(P[:, 0]), np.ptp(P[:, 1])); root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in meshes])
root.location.z -= P[:, 2].min(); bpy.context.view_layer.update()
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=True)
print('SAVED', out, os.path.getsize(out) // 1024, 'KB')

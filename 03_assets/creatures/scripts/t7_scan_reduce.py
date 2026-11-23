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
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
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
root.location.z -= P[:, 2].min(); bpy.context.view_layer.update()
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=True)
print('SAVED', out, os.path.getsize(out) // 1024, 'KB')

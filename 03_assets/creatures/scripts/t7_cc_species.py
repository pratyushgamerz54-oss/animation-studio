"""t7_cc_species — generic 'mix pipeline' converter: free-licence base (glTF) → species v002 (real size, photo-matched coat).

usage: $BPY45 t7_cc_species.py <species_id> <out_dir>
Per-species config in CC (below). Steps: import base → delete stray / unwanted objects → face +X, centre on Y = 0 → scale to the
field-guide withers height (antlers / horns excluded) → recolour diffuse textures to the photo palette (new files in
11_TEXTURES/<species>/, base untouched) → matte realism (rough ≈ .6, specular ≈ .28) → save v002 .blend (relative paths).
Sambar has its own script (t7_sambar_cc.py: own antlers); this one is for bases that need no new parts.
"""
import os, sys, math, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix
import t7kit as K

CC = {
    'wolf': dict(base='wolf/c0fd1738fa31413b906e2914f5a332b9', withers=0.72, pelvis='Back_39', chest='Torso3_14',
                 delete=('Icosphere',), still_action='Animation',
                 # photo ref 01 (Himalayan wolf, Zoo Zurich): tawny flanks, dark grizzled saddle, cream belly / legs / cheeks
                 palette=dict(dark='#3E342A', mid='#A47A52', light='#E4D8C4', cap=1.9, gamma=0.9, tint=0.65)),
}


def mesh_world(o):
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me = e.to_mesh()
    P = np.array([(e.matrix_world @ v.co)[:] for v in me.vertices]); e.to_mesh_clear(); return P


def hexlin(h):
    return np.array([int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def recolor(src, dst, dark, mid, light, cap=1.3, gamma=0.9, tint=None):
    """luminance-preserving recolour: below the median → dark..mid, above → mid..light (cap = brightest/median ratio kept)."""
    from PIL import Image
    im = Image.open(src).convert('RGBA'); A = np.asarray(im).astype(np.float32) / 255
    rgb = A[..., :3]; Y = rgb @ np.array([0.2126, 0.7152, 0.0722])
    m = A[..., 3] > 0.5
    med = np.median(Y[m]) if m.any() else np.median(Y)
    t = np.clip(Y / max(med, 1e-3), 0, cap)
    cd, cm, cl = hexlin(dark), hexlin(mid), hexlin(light)
    out = np.where(t[..., None] < 1, cd + (cm - cd) * t[..., None] ** gamma, cm + (cl - cm) * ((t[..., None] - 1) / (cap - 1)))
    if tint is not None:   # TINT mode: keep the base's own pattern (dark saddle, pale belly), recolour mostly the mid-tones
        w = (tint * np.exp(-((np.clip(Y / max(med, 1e-3), 0, 3) - 1) / 0.55) ** 2))[..., None]
        out = rgb * (1 - w) + out * w
    small = np.asarray(Image.fromarray((Y * 255).astype(np.uint8)).resize((64, 64)).resize(Y.shape[::-1], Image.BILINEAR)) / 255
    out = np.clip(out * (1 + 1.2 * (Y - small)[..., None]), 0, 1)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray((np.concatenate([out, A[..., 3:]], -1) * 255).astype(np.uint8)).save(dst)


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    sid, out = a[0], a[1]; cfg = CC[sid]
    K.clean()
    g = glob.glob(os.path.join(K.CR, '00_CREATURE_REFERENCES', 'cc_models', cfg['base'], 'scene.gltf'))[0]
    bpy.ops.import_scene.gltf(filepath=g)
    for n in cfg.get('delete', ()):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o)
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    root = next(o for o in bpy.data.objects if o.parent is None and o.type == 'EMPTY')
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    body = max(meshes, key=lambda o: len(o.data.polygons))
    if cfg.get('still_action') in bpy.data.actions:
        arm.animation_data.action = bpy.data.actions[cfg['still_action']]
    bpy.context.scene.frame_set(cfg.get('still_frame', 0)); bpy.context.view_layer.update()
    pb = arm.pose.bones
    pel = arm.matrix_world @ pb[cfg['pelvis']].head; ch = arm.matrix_world @ pb[cfg['chest']].head
    d = ch - pel; ang = math.atan2(d.y, d.x)
    root.matrix_world = Matrix.Rotation(-ang, 4, 'Z') @ root.matrix_world; bpy.context.view_layer.update()
    P = mesh_world(body)
    chest = arm.matrix_world @ pb[cfg['chest']].head
    near = np.abs(P[:, 0] - chest[0]) < 0.12 * np.ptp(P[:, 0])
    s = cfg['withers'] / (P[near, 2].max() - P[:, 2].min())
    root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P = mesh_world(body)
    root.location.z -= P[:, 2].min(); root.location.x -= (P[:, 0].max() + P[:, 0].min()) / 2
    root.location.y -= (P[:, 1].max() + P[:, 1].min()) / 2; bpy.context.view_layer.update()
    print('scale', round(s, 3))
    tex = os.path.join(K.CR, '11_TEXTURES', sid)
    pal = cfg['palette']
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        b = mat.node_tree.nodes.get('Principled BSDF')
        if not b:
            continue
        L = b.inputs['Base Color'].links
        if L and L[0].from_node.type == 'TEX_IMAGE' and L[0].from_node.image:
            n = L[0].from_node; img = n.image
            src = bpy.path.abspath(img.filepath) if img.filepath else None
            if not src or not os.path.exists(src):
                src = os.path.join(tex, '_src.png'); os.makedirs(tex, exist_ok=True); img.filepath_raw = src; img.file_format = 'PNG'; img.save()
            dst = os.path.join(tex, f'T7_{sid.upper()}_{mat.name}_diffuse_v002.png')
            recolor(src, dst, pal['dark'], pal['mid'], pal['light'], pal.get('cap', 1.3), pal.get('gamma', 0.9), pal.get('tint'))
            n.image = bpy.data.images.load(dst, check_existing=True)
        for l in list(b.inputs['Roughness'].links):
            mat.node_tree.links.remove(l)
        b.inputs['Roughness'].default_value = cfg.get('rough', 0.6); b.inputs['Specular IOR Level'].default_value = 0.28
    if os.path.exists(os.path.join(tex, '_src.png')):
        os.remove(os.path.join(tex, '_src.png'))
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f'T7_{sid.upper()}_CC_v002.blend')
    bpy.ops.wm.save_as_mainfile(filepath=fn, compress=True, relative_remap=True)
    print('SAVED', fn)


main()

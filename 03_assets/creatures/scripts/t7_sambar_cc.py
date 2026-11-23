"""t7_sambar_cc — SAMBAR v002 from the CC-BY elk base (WildMesh 3D, CC-BY-4.0) — TASK 07 'mix' pipeline.

  base (real anatomy, skin weights, 53 real-motion clips)  +  own parts / fixes (photo refs, field-guide sizes):
  1. real size: withers 1.30 m (sambar stag), antlers excluded from the measurement
  2. elk antlers removed → own rusine 3-tine lyre antlers (t7_anatomy.antlers_sambar, photo-matched), bone-parented to RigHead
  3. coat recoloured to the sambar photos: uniform grey-brown, no pale elk rump patch, darker legs / mane (new texture files,
     the base textures are untouched)
  4. ears enlarged ×1.25 around the ear root (sambar ears are large and broad)
usage: $BPY45 t7_sambar_cc.py <base_import.blend> <out_dir> [--anim Walk]
"""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix
import t7kit as K, t7sdf as S, t7_anatomy as A

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
BASE, OUT = a[0], a[1]
ANIM = a[a.index('--anim') + 1] if '--anim' in a else None
TEX = os.path.join(K.CR, '11_TEXTURES', 'sambar')
WITHERS = 1.30


def mesh_world(o):
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me = e.to_mesh()
    P = np.array([(e.matrix_world @ v.co)[:] for v in me.vertices]); e.to_mesh_clear(); return P


def recolor(src, dst, mid='#7E634A', light='#957A5E', dark='#382A20', cap=1.30):   # photo refs 01-03 (warm grey-brown)
    """luminance-preserving recolour to the sambar palette; very light areas (elk rump patch) capped → only slightly paler."""
    from PIL import Image
    im = Image.open(src).convert('RGBA'); A_ = np.asarray(im).astype(np.float32) / 255
    rgb = A_[..., :3]; Y = rgb @ np.array([0.2126, 0.7152, 0.0722])
    med = np.median(Y[A_[..., 3] > 0.5]) if (A_[..., 3] > 0.5).any() else np.median(Y)
    t = np.clip(Y / max(med, 1e-3), 0, cap)
    c_mid, c_light, c_dark = (np.array([int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]) for h in (mid, light, dark))
    out = np.where(t[..., None] < 1, c_dark + (c_mid - c_dark) * t[..., None] ** 0.9,
                   c_mid + (c_light - c_mid) * ((t[..., None] - 1) / (cap - 1)))
    # keep a little of the original fine variation (hair streaks) as value noise
    det = (Y - np.clip(np.asarray(Image.fromarray((Y * 255).astype(np.uint8)).resize((64, 64)).resize(Y.shape[::-1], Image.BILINEAR)) / 255, 0, 1))
    out = np.clip(out * (1 + 1.2 * det[..., None]), 0, 1)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(np.concatenate([out, A_[..., 3:]], -1).__mul__(255).astype(np.uint8)).save(dst)
    return dst


def main():
    bpy.ops.wm.open_mainfile(filepath=BASE)
    bpy.context.preferences.filepaths.save_version = 0
    for o in [o for o in bpy.data.objects if o.type in ('CAMERA', 'LIGHT') or o.name.startswith('T7_')]:
        bpy.data.objects.remove(o)
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    root = next(o for o in bpy.data.objects if o.parent is None and o.type == 'EMPTY')
    body = next(o for o in bpy.data.objects if o.type == 'MESH' and o.data.materials and o.data.materials[0].name == 'Body')
    head = next(o for o in bpy.data.objects if o.type == 'MESH' and o.data.materials and o.data.materials[0].name == 'Head')
    # 1. remove elk antlers
    for o in [o for o in bpy.data.objects if o.type == 'MESH' and any(m and m.name == 'Chifre' for m in o.data.materials)]:
        bpy.data.objects.remove(o)
    # rest pose for measuring / building
    arm.animation_data.action = bpy.data.actions.get('Stand_Breathing_01'); bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    pb = arm.pose.bones
    # face +X, centred on Y = 0 (own parts are built with Y-mirror symmetry)
    pel = arm.matrix_world @ pb['RigPelvis_02'].head; ch = arm.matrix_world @ pb['RigChest_013'].head
    d = ch - pel; ang = math.atan2(d.y, d.x)
    root.matrix_world = Matrix.Rotation(-ang, 4, 'Z') @ root.matrix_world; bpy.context.view_layer.update()
    P = mesh_world(body); root.location.y -= (P[:, 1].max() + P[:, 1].min()) / 2; root.location.x -= (P[:, 0].max() + P[:, 0].min()) / 2
    bpy.context.view_layer.update()
    chest = arm.matrix_world @ pb['RigChest_013'].head
    P = mesh_world(body)
    near = np.abs(P[:, 0] - chest[0]) < 0.12 if np.ptp(P[:, 0]) > np.ptp(P[:, 1]) else np.abs(P[:, 1] - chest[1]) < 0.12
    withers = P[near, 2].max() - P[:, 2].min()
    s = WITHERS / withers
    root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P = mesh_world(body); root.location.z -= P[:, 2].min(); bpy.context.view_layer.update()
    print('scale x', round(s, 3), 'withers', WITHERS)
    # 2. own sambar antlers on the head
    Ph = mesh_world(head)
    hbone = pb['RigHead_00']; hm = arm.matrix_world @ hbone.matrix
    hb = np.array((arm.matrix_world @ hbone.head)[:])
    # animal faces +X (aligned above): nose = most forward head point; poll = highest midline point behind the eyes
    nose = Ph[np.argmax(Ph[:, 0])]
    fwd = S._n(nose - hb)
    hl = float(np.linalg.norm(nose - hb)) * 1.15
    mid = Ph[(np.abs(Ph[:, 1]) < 0.035) & (Ph[:, 0] < hb[0] + 0.30 * hl) & (Ph[:, 0] > hb[0] - 0.15 * hl)]
    poll = mid[np.argmax(mid[:, 2])]
    side = S._n(np.cross((0, 0, 1), fwd)) if abs(fwd[2]) < 0.95 else np.array([0, 1, 0.0])
    yaxis_world = side if side @ np.array([0, 1, 0]) >= 0 else -side
    fwd_flat = S._n(np.array([fwd[0], fwd[1], 0]))
    H = A.Frame(np.zeros(3), fwd)
    H.o = (poll - H.R @ A.V(0.04 * hl, 0, 0.27 * hl) - np.array([0, 0, 0.01])).astype(np.float32)
    marks = {'head': H, 'hl': hl}
    print('HEADFRAME hl', round(hl, 3), 'poll', np.round(poll, 3), 'fwd', np.round(fwd, 3), 'base', np.round(H.to((0.04 * hl, 0.17 * hl, 0.27 * hl)), 3))
    ant = A.antlers_sambar(marks, beam=0.56 * WITHERS / 1.30)
    coll = body.users_collection[0]
    ao, Pa, W, D = K.part_to_object(ant, 'sambar_antlers', coll, quads=7000)
    col = K.coat_from_zones(W, Pa, {'antler': '#5E4C3A', 'burr': '#3E3228', '*': '#5E4C3A'}, 0.18, 30)
    tip = np.clip((Pa[:, 2] - Pa[:, 2].min()) / np.ptp(Pa[:, 2]), 0, 1)
    col = col * (1 + 0.55 * tip ** 3)[:, None]                         # paler polished tips (photo)
    K.put_coat(ao, np.clip(col, 0, 1))
    ao.data.materials.append(K.mat_attr('T7_SAMBAR_ANTLER', rough=0.62, spec=0.3, bump=0.7, bump_scale=140))
    mw = ao.matrix_world.copy(); ao.parent = arm; ao.parent_type = 'BONE'; ao.parent_bone = 'RigHead_00'
    bpy.context.view_layer.update(); ao.matrix_world = mw
    # 3. coat recolour (new files)
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        for n in mat.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image and 'diffuse' in n.image.name.lower() and mat.name in ('Body', 'Head'):
                src = bpy.path.abspath(n.image.filepath)
                if not os.path.exists(src):
                    n.image.filepath_raw = os.path.join(TEX, 'tmp.png'); n.image.save()
                    src = n.image.filepath_raw
                dst = os.path.join(TEX, f'T7_SAMBAR_{mat.name.upper()}_diffuse_v002.png')
                recolor(src, dst)
                n.image = bpy.data.images.load(dst, check_existing=True)
        b = mat.node_tree.nodes.get('Principled BSDF')
        if b and mat.name in ('Body', 'Head'):
            b.inputs['Roughness'].default_value = 0.62; b.inputs['Specular IOR Level'].default_value = 0.28   # realism rule (matte fur)
            for l in list(b.inputs['Roughness'].links):
                mat.node_tree.links.remove(l)
    # 4. bigger ears (scale verts around the ear root by their ear-bone weight)
    for ob in (head, body):
        for bn in ('RigLEar1_026', 'RigREar1_028'):
            vg = ob.vertex_groups.get(bn)
            if not vg:
                continue
            root_ = ob.matrix_world.inverted() @ arm.matrix_world @ Vector(pb[bn].bone.head_local)
            for v in ob.data.vertices:
                w = next((g.weight for g in v.groups if g.group == vg.index), 0)
                if w > 0.05:
                    v.co = root_ + (v.co - root_) * (1 + 0.25 * w)
    if os.path.exists(os.path.join(TEX, 'tmp.png')):
        os.remove(os.path.join(TEX, 'tmp.png'))
    # save + previews
    os.makedirs(OUT, exist_ok=True)
    fn = os.path.join(OUT, 'T7_SAMBAR_CC_v002.blend')
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=fn, compress=True, relative_remap=True)
    print('SAVED', fn)


main()

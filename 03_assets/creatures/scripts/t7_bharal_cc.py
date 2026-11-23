"""t7_bharal_cc — BHARAL (blue sheep) v002 from the CC-BY BigHorn base (WildMesh 3D, 55 clips) — mix pipeline.

  base geometry + rig + clips (WildMesh 3D, CC-BY-4.0)  +  own parts:
  * bharal horns (own, t7sdf): rams' horns rise, sweep OUT sideways, then curve back, tips up-back (photo refs) — not the bighorn curl
  * coat pattern from anatomy (photo refs 01-03): slate blue-grey, white belly / inner legs / back of legs, black flank stripe,
    black fronts of the legs, dark chest / neck front; the base texture's hair detail is kept as luminance detail
  * size: withers 0.85 m (field guide 0.75–0.91 m)
usage: $BPY45 t7_bharal_cc.py <base.gltf> <out_dir>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix
import t7kit as K, t7sdf as S, t7_anatomy as A

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
SRC, OUT = a[0], a[1]
WITHERS = 0.85


def mesh_world(o):
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me = e.to_mesh()
    P = np.array([(e.matrix_world @ v.co)[:] for v in me.vertices]); N = np.array([(e.matrix_world.to_3x3() @ v.normal).normalized()[:] for v in me.vertices])
    e.to_mesh_clear(); return P, N


def lin(h):
    c = np.array([int(h.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]); return np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)


def smooth(x, a_, b_):
    t = np.clip((x - a_) / (b_ - a_), 0, 1); return t * t * (3 - 2 * t)


def coat(P, N, B):
    W = WITHERS; z = P[:, 2]; x = P[:, 0]; ay = np.abs(P[:, 1])
    C = np.tile(lin('#7E8286'), (len(P), 1))                                    # slate blue-grey
    C = C * (1 + 0.10 * S.fbm(P, 8, 3, 3))[:, None]
    torso = smooth(z, 0.40 * W, 0.50 * W)
    belly = smooth(-N[:, 2], 0.55, 0.85) * torso
    legs = 1 - smooth(z, 0.42 * W, 0.55 * W)
    inner = legs * (1 - smooth(z, 0.30 * W, 0.45 * W) * 0.5) * smooth(-np.sign(P[:, 1]) * N[:, 1], 0.45, 0.8)   # medial side of the legs
    back_leg = legs * smooth(-N[:, 0], 0.55, 0.85)
    rump_u = smooth(-(x - B['pelvis'][0]), 0.0, 0.12 * W) * smooth(-N[:, 0], 0.2, 0.6) * (z < 0.8 * W)
    white = np.clip(belly * 0.9 + inner * 0.7 + back_leg * 0.6 + rump_u * 0.3, 0, 1)
    band_z = B['belly_z'] + 0.09 * W                                               # black flank stripe (between grey and white)
    stripe = np.exp(-((z - band_z) / (0.035 * W)) ** 2) * smooth(1 - np.abs(N[:, 2]), 0.4, 0.8) * (x > B['pelvis'][0] - 0.05 * W) * (x < B['chest'][0] + 0.05 * W)
    front_leg = (1 - smooth(z, 0.20 * W, 0.34 * W)) * smooth(N[:, 0], 0.45, 0.8)
    chest = smooth(x - B['chest'][0], 0.05 * W, 0.12 * W) * smooth(N[:, 0], 0.55, 0.85) * (z > 0.45 * W) * (z < 0.75 * W) * (ay < 0.07 * W)
    black = np.clip(stripe * 1.1 + front_leg * 0.9 + chest * 0.8, 0, 1)
    hoof = 1 - smooth(z, 0.03 * W, 0.06 * W)
    return white, np.clip(black + hoof, 0, 1)


def coat_material(name, base_img):
    """coat colour attribute × hair detail from the base texture luminance (keeps painted fur strokes) + micro bump; matte."""
    m = K.new_mat(name); nt = m.node_tree; b = nt.nodes['Principled BSDF']; L = nt.links
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'coat'
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = base_img
    bw = nt.nodes.new('ShaderNodeRGBToBW'); L.new(tx.outputs['Color'], bw.inputs['Color'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.0; mr.inputs['From Max'].default_value = 0.45
    mr.inputs['To Min'].default_value = 0.72; mr.inputs['To Max'].default_value = 1.15; L.new(bw.outputs['Val'], mr.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeVectorMath'); mul.operation = 'SCALE'; L.new(at.outputs['Vector'], mul.inputs[0]); L.new(mr.outputs[0], mul.inputs['Scale'])
    L.new(mul.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.66; b.inputs['Specular IOR Level'].default_value = 0.26
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 700
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.001
    L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def horns(H, hl, base_y):
    """bharal ram horns: thick ridged base, up → out → back, tips up-back; length along the curve ≈ 0.62 m."""
    p = S.Part('horns', voxel=0.003)
    base = H.to((0.02 * hl, base_y, 0.28 * hl))
    pts = A._path(base, [(-0.55, 0.40, 0.75), (-0.55, 0.95, 0.10), (-0.55, 0.75, -0.45), (-0.30, 0.35, -0.25)], 0.50, 14)   # photo 01: up-back → out → back, tips out-back
    rad = [0.042 * (1 - 0.80 * (i / 14) ** 1.1) + 0.004 for i in range(15)]
    p.chain(pts, rad, 'horn', 0.006, mirror=True)
    for i in range(2, 12):                                                         # growth ridges (annuli)
        p.rcone(pts[i], pts[i] + (pts[i + 1] - pts[i]) * 0.25, rad[i] * 1.06, rad[i] * 1.02, 'ridge', 0.004, mirror=True)
    return p


def main():
    K.clean()
    bpy.ops.import_scene.gltf(filepath=SRC)
    for o in [o for o in bpy.data.objects if o.name in ('Icosphere',) or (o.type == 'MESH' and any(m and m.name == 'Material_1' for m in o.data.materials))]:
        bpy.data.objects.remove(o)                                                 # stray sphere + bighorn horns
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    root = next(o for o in bpy.data.objects if o.parent is None and o.type == 'EMPTY')
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    body = max(meshes, key=lambda o: len(o.data.polygons))
    arm.animation_data.action = bpy.data.actions.get('Stand_Breathing_01') or arm.animation_data.action
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    pb = arm.pose.bones
    pel = arm.matrix_world @ pb['RigPelvis_02'].head; ch = arm.matrix_world @ pb['RigChest_013'].head
    ang = math.atan2((ch - pel).y, (ch - pel).x)
    root.matrix_world = Matrix.Rotation(-ang, 4, 'Z') @ root.matrix_world; bpy.context.view_layer.update()
    P, _ = mesh_world(body); chest = arm.matrix_world @ pb['RigChest_013'].head
    near = np.abs(P[:, 0] - chest[0]) < 0.12 * np.ptp(P[:, 0])
    s = WITHERS / (P[near, 2].max() - P[:, 2].min())
    root.scale = tuple(x * s for x in root.scale); bpy.context.view_layer.update()
    P, _ = mesh_world(body)
    root.location.z -= P[:, 2].min(); root.location.x -= (P[:, 0].max() + P[:, 0].min()) / 2; root.location.y -= (P[:, 1].max() + P[:, 1].min()) / 2
    bpy.context.view_layer.update()
    B = dict(pelvis=np.array((arm.matrix_world @ pb['RigPelvis_02'].head)[:]), chest=np.array((arm.matrix_world @ pb['RigChest_013'].head)[:]))
    Pb, Nb = mesh_world(body)
    mid = np.abs(Pb[:, 0] - (B['pelvis'][0] + B['chest'][0]) / 2) < 0.08
    B['belly_z'] = Pb[mid & (Nb[:, 2] < -0.6), 2].mean() if (mid & (Nb[:, 2] < -0.6)).any() else 0.45 * WITHERS
    import t7_cc_species as CS
    tex = os.path.join(K.CR, '11_TEXTURES', 'bharal'); os.makedirs(tex, exist_ok=True)
    for ob in meshes:
        if ob.name not in bpy.data.objects or not ob.active_material or not ob.data.uv_layers:
            continue
        Pw, Nw = mesh_world(ob)
        if len(Pw) != len(ob.data.vertices):
            continue
        node = next((n for n in ob.active_material.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'diffuse' in n.image.name.lower()), None)
        if node is None:
            continue
        src = os.path.join(tex, '_src.png'); node.image.filepath_raw = src; node.image.file_format = 'PNG'; node.image.save()
        dst = os.path.join(tex, f'T7_BHARAL_{ob.active_material.name}_diffuse_v002.png')
        # photo refs: slate blue-grey (luminance-preserving recolour keeps the base's hair strokes)
        from PIL import Image, ImageFilter
        im0 = Image.open(src).convert('RGB').filter(ImageFilter.GaussianBlur(7))      # remove the cel-shading islands of the base
        a0 = np.asarray(im0).astype(np.float32) / 255
        rng = np.random.default_rng(7); n1 = rng.normal(0, 1, (a0.shape[0] // 2, a0.shape[1] // 2)).astype(np.float32)
        hair = np.asarray(Image.fromarray(((n1 * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).resize(a0.shape[1::-1], Image.BILINEAR)
                          .filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255 - 0.5
        a0 = np.clip(a0 * (1 + 0.22 * hair[..., None]), 0, 1)                         # fine hair-scale variation
        Image.fromarray((a0 * 255).astype(np.uint8)).save(src)
        CS.recolor(src, dst, '#444548', '#69686A', '#828180', 1.3, 1.0)   # photo 02: grey-brown slate
        wh, bl = coat(Pw, Nw, B)
        CS.paint_uv(dst, ob, wh, '#E2E0DA', 3)
        CS.paint_uv(dst, ob, bl, '#1D1C1B', 3)
        node.image = bpy.data.images.load(dst, check_existing=False)
        b = ob.active_material.node_tree.nodes.get('Principled BSDF')
        if b:
            for l in list(b.inputs['Roughness'].links):
                ob.active_material.node_tree.links.remove(l)
            b.inputs['Roughness'].default_value = 0.64; b.inputs['Specular IOR Level'].default_value = 0.26
        if os.path.exists(src):
            os.remove(src)
    # horns on the head (same head-frame detection as the sambar)
    head = max([o for o in meshes if o.name in bpy.data.objects], key=lambda o: mesh_world(o)[0][:, 0].max())
    Ph, _ = mesh_world(head)
    hb = np.array((arm.matrix_world @ pb['RigHead_00'].head)[:])
    nose = Ph[np.argmax(Ph[:, 0])]; fwd = S._n(nose - hb); hl = float(np.linalg.norm(nose - hb)) * 1.15
    midl = Ph[(np.abs(Ph[:, 1]) < 0.03) & (Ph[:, 0] < hb[0] + 0.30 * hl) & (Ph[:, 0] > hb[0] - 0.15 * hl)]
    poll = midl[np.argmax(midl[:, 2])]
    H = A.Frame(np.zeros(3), fwd); H.o = (poll - H.R @ A.V(0.02 * hl, 0, 0.28 * hl) - np.array([0, 0, 0.008])).astype(np.float32)
    hp = horns(H, hl, 0.07 * hl)
    coll = body.users_collection[0]
    ho, Phh, Wz, D = K.part_to_object(hp, 'bharal_horns', coll, quads=6000)
    t = np.clip((Phh[:, 0].max() - Phh[:, 0]) / max(np.ptp(Phh[:, 0]), 1e-3), 0, 1)
    K.put_coat(ho, np.clip(lin('#6E6455')[None] * (1.0 - 0.35 * t[:, None]) * (1 + 0.15 * S.fbm(Phh, 40, 3, 5))[:, None], 0, 1))
    ho.data.materials.append(K.mat_attr('T7_BHARAL_HORN', rough=0.58, spec=0.3, bump=0.8, bump_scale=90))
    mw = ho.matrix_world.copy(); ho.parent = arm; ho.parent_type = 'BONE'; ho.parent_bone = 'RigHead_00'
    bpy.context.view_layer.update(); ho.matrix_world = mw
    os.makedirs(OUT, exist_ok=True)
    fn = os.path.join(OUT, 'T7_BHARAL_CC_v002.blend')
    bpy.ops.wm.save_as_mainfile(filepath=fn, compress=True, relative_remap=True)
    print('SAVED', fn, 'scale', round(s, 3))


main()

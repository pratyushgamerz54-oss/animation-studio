"""t7_turtle_pass — species pass for a rigged pond-turtle base (Geoemydidae) → Indian roofed turtle (Pangshura tecta):
1. 'roof': carapace vaulted into a tent-shaped vertebral keel (rest-mesh edit of the shell vertices, smooth falloff to the rim)
2. per-pixel recolour by 3D region / bone weights (UV position + region maps), keeping the scan-like scute / scale detail:
   dark brown-black carapace, orange-red keel stripe, yellow-buff plastron, olive skin, olive head with dark crown and
   orange-red temporal crescent behind the eye (photo refs 01-02)
3. short tail (pose scale on the tail root; the base is a long-tailed male of another species)

usage: $BPY45 t7_turtle_pass.py <in.blend> <out.blend>
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(roof=0.32, carapace='#3A2C20', keel='#9C4824', plastron='#B89A64', skin='#4E4630', head='#6E5E3A', crown='#2E281E',
         temporal='#C46A3A', tail_scale=0.5, sid='roofed_turtle')


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def lin(h):
    return s2l(CS.hexlin(h))


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst = a[0], a[1]; sid = C['sid']
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    body = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
    me = body.data; mw = body.matrix_world; inv = mw.inverted()
    P = np.array([(mw @ v.co)[:] for v in me.vertices])               # rest positions in world (static parts of the rig)
    gid = {g.name: g.index for g in body.vertex_groups}

    def wsum(prefixes):
        idx = {i for n, i in gid.items() if any(n.startswith(p) for p in prefixes)}
        return np.array([sum(g.weight for g in v.groups if g.group in idx) for v in me.vertices], np.float32)
    w_shell = wsum(['base']); w_head = wsum(['head']); w_neck = wsum(['neck']); w_tail = wsum(['tail'])
    # ---- 1. roof-shaped keel: shell vertices above the rim, height scaled up most on the midline
    sh = w_shell > 0.95
    zr = np.percentile(P[sh, 2], 35); Wy = np.percentile(np.abs(P[sh, 1]), 98)
    xs = P[sh, 0]; xm, xL = (xs.max() + xs.min()) / 2, np.ptp(xs) / 2
    top = (w_shell > 0.02) & (P[:, 2] > zr)
    fy = np.clip(1 - np.abs(P[:, 1]) / Wy, 0, 1); fx = np.clip(1 - ((P[:, 0] - xm) / xL) ** 2, 0, 1) ** 0.5
    k = 1 + C['roof'] * fy ** 1.3 * fx * np.clip(w_shell, 0, 1)        # continuous falloff (no tearing at the shell border)
    P2 = P.copy(); P2[top, 2] = zr + (P[top, 2] - zr) * k[top]
    for i in np.where(top)[0]:
        me.vertices[i].co = inv @ Vector(P2[i])
    me.update(); P = P2
    print('TURTLE keel: shell top raised, max +cm', round(float(((k[top] - 1) * (P[top, 2] - zr) / k[top]).max() * 100), 2), flush=True)
    # ---- 2. recolour
    from PIL import Image, ImageFilter
    mat = body.active_material; b = mat.node_tree.nodes['Principled BSDF']; tn = b.inputs['Base Color'].links[0].from_node
    srcp = bpy.path.abspath(tn.image.filepath)
    if not os.path.exists(srcp):
        srcp = os.path.join(os.environ.get('TMPDIR', '/tmp'), 't7_turtle_src.png'); tn.image.filepath_raw = srcp; tn.image.file_format = 'PNG'; tn.image.save()
    T = np.asarray(Image.open(srcp).convert('RGB')).astype(np.float32) / 255; H, W = T.shape[:2]
    Tl = s2l(T); Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
    Yb = np.asarray(Image.fromarray(np.clip(Y * 255 * 3, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32) / 255 / 3
    det = np.clip((Y + 0.01) / (Yb + 0.01), 0.5, 1.8) ** 0.7                                 # scute seams / scales
    Nv = np.array([(mw.to_3x3() @ v.normal).normalized()[:] for v in me.vertices], np.float32)
    A = np.concatenate([P, Nv, np.stack([w_shell, w_head, w_neck, w_tail], 1)], 1).astype(np.float32)
    M, cov = raster(body, A, W, H); M = dilate(M, cov)
    pos, nrm, ws, wh, wn = M[..., :3], M[..., 3:6], M[..., 6], M[..., 7], M[..., 8]
    hb = arm.data.bones[[n for n in arm.data.bones.keys() if n.startswith('head_')][0]]
    h0 = np.array((arm.matrix_world @ hb.head_local)[:]); h1 = np.array((arm.matrix_world @ hb.tail_local)[:])
    hd = (h1 - h0) / np.linalg.norm(h1 - h0); hl = np.linalg.norm(h1 - h0)
    rel = pos - h0; t_ = rel @ hd                       # along the head (0 = head base)
    col = np.broadcast_to(lin(C['skin']), Tl.shape).copy()
    xs0, xs1 = P[sh, 0].min(), P[sh, 0].max()
    shell = (ws > 0.5) | ((pos[..., 2] > zr) & (pos[..., 0] > xs0) & (pos[..., 0] < xs1) & (np.abs(pos[..., 1]) < Wy * 1.05) & (wh < 0.3) & (nrm[..., 2] > 0.05))   # front of the carapace is weighted to the neck
    under = shell & (nrm[..., 2] < -0.3)                # plastron
    col[shell] = lin(C['carapace']); col[under] = lin(C['plastron'])
    keel = shell & (np.abs(pos[..., 1]) < 0.0035) & (nrm[..., 2] > 0.4)
    kk = np.asarray(Image.fromarray((keel * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)[..., None] / 255
    col = col * (1 - kk) + lin(C['keel']) * kk
    head = wh > 0.5
    col[head] = lin(C['head'])
    crown = head & (nrm[..., 2] > 0.55)
    col[crown] = lin(C['crown'])
    side = np.abs(nrm[..., 1]) > 0.45
    hx = P[w_head > 0.5, 0]; hz = P[w_head > 0.5, 2]; hx0, hL = hx.min(), np.ptp(hx); hzm = np.median(hz)
    fr = (pos[..., 0] - hx0) / hL                       # 0 back of head … 1 snout (turtle faces +X)
    temporal = head & side & (fr > 0.30) & (fr < 0.60) & (pos[..., 2] > hzm - 0.1 * np.ptp(hz))   # crescent behind the eye
    tp = np.asarray(Image.fromarray((temporal * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32)[..., None] / 255
    col = col * (1 - tp) + lin(C['temporal']) * tp
    dd = np.where(shell, det ** 1.6, det)                 # scute seams / growth rings read on the dark shell
    out = np.clip(col * dd[..., None], 0, 1)
    tex = os.path.join(K.CR, '11_TEXTURES', sid); os.makedirs(tex, exist_ok=True)
    dfn = os.path.join(tex, f'T7_{sid.upper()}_diffuse_v001.jpg')
    srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * out ** (1 / 2.4) - 0.055)
    Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=92)
    img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
    for k_ in ('Metallic', 'Roughness'):
        for l in list(b.inputs[k_].links):
            mat.node_tree.links.remove(l)
    b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.55; b.inputs['Specular IOR Level'].default_value = 0.3
    b.inputs['Coat Weight'].default_value = 0.12; b.inputs['Coat Roughness'].default_value = 0.35   # damp shell, not plastic
    # ---- 3. short tail
    tb = arm.pose.bones.get([n for n in arm.pose.bones.keys() if n.startswith('tail1_')][0])
    tb.scale = (C['tail_scale'],) * 3
    cn = tb.constraints.new('LIMIT_SCALE'); cn.owner_space = 'LOCAL'   # survives the base's actions (they key the tail)
    for ax in 'xyz':
        setattr(cn, f'use_max_{ax}', True); setattr(cn, f'max_{ax}', C['tail_scale'])
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('TURTLE SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

"""t7_dragonfly_pass — realism pass for the Anax (hawker) specimen model after t7_insect_pass (Director 24 Nov: "isko realistic banao"):
1. legs: a pinned specimen hangs its legs straight down → in flight a hawker folds them forward / up into a 'basket' under the head
   (progressive curl: rotation grows with distance from the thorax, so each leg bends at its joints, not as a rigid stick)
2. colour (photo refs 01-02, male A. parthenope): bright sky-blue saddle on abdomen segment 2 (+ base of S3), olive-brown abdomen
   with darker rings, olive / green-brown thorax (specimen green is too bright), keeps the real texture detail

usage: $BPY45 t7_dragonfly_pass.py <in.blend> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(sid='lesser_emperor', leg_fold_deg=165.0, saddle='#3C8ED6', abdomen='#4A3E2A', thorax='#66703E',
         ab_tint=0.6, th_tint=0.6)


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst = a[0], a[1]
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    body = max([o for o in bpy.data.objects if o.type == 'MESH' and o.active_material and o.active_material.name == 'body'],
               key=lambda o: len(o.data.vertices))
    me = body.data; mw = body.matrix_world; inv = mw.inverted()
    P = np.array([(mw @ v.co)[:] for v in me.vertices])
    # body axis: head = the end where the body is wide (eyes), abdomen = long thin end
    x0, x1 = P[:, 0].min(), P[:, 0].max(); L = x1 - x0
    nb = 24; w = np.zeros(nb)
    for k in range(nb):
        s = (P[:, 0] >= x0 + k * L / nb) & (P[:, 0] < x0 + (k + 1) * L / nb) & (P[:, 2] > np.percentile(P[:, 2], 40))
        w[k] = np.abs(P[s, 1]).max() if s.any() else 0
    head_neg = w[:nb // 3].mean() > w[-nb // 3:].mean()
    sg = -1 if head_neg else 1                                   # +1: head at +X
    # thorax = where the legs hang below the body
    zb = np.percentile(P[:, 2], 30)
    legs = P[:, 2] < zb * 0.92
    thx = np.median(P[legs, 0]); tz = np.percentile(P[~legs & (np.abs(P[:, 0] - thx) < 0.006), 2], 5)
    legs = legs & (P[:, 2] < tz)
    d = tz - P[:, 2]; dmax = d[legs].max()
    f_ = np.clip(d / dmax, 0, 1); th = math.radians(C['leg_fold_deg']) * f_
    sc_ = 1 - 0.40 * f_                                          # joints bent: leg tucked in close to the thorax
    vx = (P[:, 0] - thx) * sc_; vz = (P[:, 2] - tz) * sc_
    # rotate in the X-Z plane so 'straight down' swings toward the head (sg) and up: (0,-1) → (sg·sinθ, -cosθ)
    nx = vx * np.cos(th) - sg * vz * np.sin(th)
    nz = vz * np.cos(th) + sg * vx * np.sin(th)
    P2 = P.copy()
    P2[legs, 0] = thx + nx[legs]; P2[legs, 2] = tz + nz[legs]
    P2[legs, 1] = P[legs, 1] * (1 - 0.25 * np.clip(d[legs] / dmax, 0, 1))     # legs drawn in toward the midline
    for i in np.where(legs)[0]:
        me.vertices[i].co = inv @ Vector(P2[i])
    me.update()
    print('DFLY head', 'at -X' if head_neg else 'at +X', 'thorax x', round(float(thx), 4), 'leg verts', int(legs.sum()),
          'lowest z before/after', round(float(P[:, 2].min()), 4), round(float(P2[:, 2].min()), 4), flush=True)
    # ---- colour
    from PIL import Image, ImageFilter
    mat = body.active_material; tn = next(n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'body' in n.image.name.lower())
    srcp = bpy.path.abspath(tn.image.filepath)
    T = np.asarray(Image.open(srcp).convert('RGB')).astype(np.float32) / 255; H, W = T.shape[:2]; Tl = s2l(T)
    Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
    pos, cov = raster(body, P.astype(np.float32), W, H)
    covd = np.asarray(Image.fromarray((cov * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    pos = dilate(pos, cov)
    ax = (pos[..., 0] - thx) * (-sg)                              # >0 toward the abdomen tip, from the thorax centre
    ab0 = 0.011                                                    # thorax → abdomen junction ≈ 11 mm behind the thorax centre
    ab = covd & (ax > ab0) & (pos[..., 2] > tz - 0.002)
    s2 = covd & (ax > ab0) & (ax < ab0 + 0.009) & (pos[..., 2] > tz - 0.002)
    thor = covd & (np.abs(pos[..., 0] - thx) < ab0) & (pos[..., 2] > tz)
    Ym = lambda m: max(float(np.median(Y[m])), 1e-3) if m.any() else 1.0
    out = Tl.copy()

    def tint(m, hexc, amt, soft=1.5):
        mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soft))).astype(np.float32)[..., None] / 255
        tgt = s2l(CS.hexlin(hexc))[None, None, :] * np.clip(Y / Ym(m), 0.3, 2.2)[..., None]
        out[:] = out * (1 - mm * amt) + np.clip(tgt, 0, 1) * mm * amt

    tint(ab & ~s2, C['abdomen'], C['ab_tint']); tint(thor, C['thorax'], C['th_tint']); tint(s2, C['saddle'], 0.9, soft=2.5)
    tex = os.path.join(K.CR, '11_TEXTURES', C['sid']); dfn = os.path.join(tex, f"T7_{C['sid'].upper()}_body_diffuse_v002.jpg")
    srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, 1) ** (1 / 2.4) - 0.055)
    Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=93)
    img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
    # lift so the folded legs (new lowest point) sit at z = 0 for previews / perching
    zmin = min((o.matrix_world @ v.co).z for o in bpy.data.objects if o.type == 'MESH' for v in o.data.vertices)
    for o in bpy.data.objects:
        if o.parent is None and o.type in ('EMPTY', 'MESH'):
            o.location.z -= zmin
    if head_neg:                                                  # library convention: every creature faces +X
        from mathutils import Matrix
        for o in bpy.data.objects:
            if o.parent is None and o.type in ('EMPTY', 'MESH'):
                o.matrix_world = Matrix.Rotation(math.pi, 4, 'Z') @ o.matrix_world
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('DFLY SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

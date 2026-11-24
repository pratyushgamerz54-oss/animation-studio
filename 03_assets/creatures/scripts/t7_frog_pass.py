"""t7_frog_pass — Indian bullfrog (Hoplobatrachus tigerinus) from a CC0 ranid specimen scan (American bullfrog, same family):
per-pixel recolour per material (UV position + normal maps) keeping the scan's real skin detail (warts, blotches, leg bars):
olive-brown back + limbs, thin pale-yellow mid-dorsal stripe (snout → vent), cream belly / throat, olive head (scan face is green);
moist skin (low roughness + thin coat — amphibian skin is wet, the realism rule allows gloss on wet surfaces); faces +X.

usage: $BPY45 t7_frog_pass.py <in.blend> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(sid='indian_bullfrog', dorsal='#6E6046', belly='#E0D6BC', stripe='#C8B67E', head='#6A5C40', dorsal_amt=0.72, belly_amt=0.55)


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst = a[0], a[1]
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    ob = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
    me = ob.data; mw = ob.matrix_world
    P = np.array([(mw @ v.co)[:] for v in me.vertices], np.float32)
    N = np.array([(mw.to_3x3() @ v.normal).normalized()[:] for v in me.vertices], np.float32)
    # head = the end of the body column (|y| small) that is wider + higher; snout tip / vent along X
    col = np.abs(P[:, 1]) < 0.012
    head_neg = P[col, 0].min() < -abs(P[col, 0].max()) * 0.8 and np.median(P[col & (P[:, 0] < 0), 2]) >= np.median(P[col & (P[:, 0] > 0), 2]) * 0.8
    snout = P[col, 0].min() if head_neg else P[col, 0].max()
    body = col & (P[:, 2] > np.percentile(P[col, 2], 30))
    vent = P[body, 0].max() if head_neg else P[body, 0].min()
    sg = -1 if head_neg else 1
    print('FROG head at', '-X' if head_neg else '+X', 'snout', round(float(snout), 3), 'vent', round(float(vent), 3), flush=True)
    # eyes: the scan's own dark eye on each side of the head = darkest head vertices (texture), one cluster per side
    from PIL import Image
    yv = np.zeros(len(P), np.float32); cv = np.zeros(len(P), np.float32); uvl = me.uv_layers.active.data
    imgs = {}
    for mi, mat in enumerate(me.materials):
        tn_ = next((n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'normal' not in n.image.name.lower()), None)
        if tn_:
            imgs[mi] = np.asarray(Image.open(bpy.path.abspath(tn_.image.filepath)).convert('L')).astype(np.float32) / 255
    for poly in me.polygons:
        im_ = imgs.get(poly.material_index)
        if im_ is None:
            continue
        h_, w_ = im_.shape
        for li in poly.loop_indices:
            u, v = uvl[li].uv; yv[me.loops[li].vertex_index] += im_[int(np.clip(1 - v % 1, 0, .9999) * h_), int(np.clip(u % 1, 0, .9999) * w_)]
            cv[me.loops[li].vertex_index] += 1
    yv /= np.maximum(cv, 1)
    hv = (np.abs(P[:, 0] - snout) < 0.40 * abs(snout - vent)) & (N[:, 2] > -0.2)
    eyes = []
    for sy in (1, -1):
        m = hv & (P[:, 1] * sy > 0.006)
        dk = m & (yv <= np.percentile(yv[m], 0.4))
        eyes.append(np.median(P[dk], 0)); print('FROG eye', np.round(eyes[-1], 4), 'n', int(dk.sum()), flush=True)
    from PIL import Image, ImageFilter
    A = np.concatenate([P, N], 1)
    for mi, mat in enumerate(me.materials):
        tn = next((n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'normal' not in n.image.name.lower()), None)
        if tn is None:
            continue
        srcp = bpy.path.abspath(tn.image.filepath)
        T = np.asarray(Image.open(srcp).convert('RGB')).astype(np.float32) / 255; H, W = T.shape[:2]; Tl = s2l(T)
        Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
        M, cov = raster(ob, A, W, H, mi)
        if not cov.any():
            continue
        M = dilate(M, cov); pos, nrm = M[..., :3], M[..., 3:]
        Ym = lambda m: max(float(np.median(Y[m & cov])), 1e-3) if (m & cov).any() else 1.0
        out = Tl.copy()

        def tint(m, hexc, amt, soft=2.0, dmin=0.25, dmax=2.4):
            mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soft))).astype(np.float32)[..., None] / 255
            tgt = s2l(CS.hexlin(hexc))[None, None, :] * np.clip(Y / Ym(m), dmin, dmax)[..., None]
            out[:] = out * (1 - mm * amt) + np.clip(tgt, 0, 1) * mm * amt

        under = nrm[..., 2] < -0.25
        tint(~under, C['dorsal'], C['dorsal_amt']); tint(under, C['belly'], C['belly_amt'], soft=6)
        fr = (pos[..., 0] - vent) / (snout - vent)            # 0 vent … 1 snout
        head = (~under) & (fr > 0.72) & (np.abs(pos[..., 1]) < 0.03)
        tint(head, C['head'], 0.6, soft=5)
        stripe = (np.abs(pos[..., 1]) < 0.00035) & (nrm[..., 2] > 0.55) & (fr > 0.03) & (fr < 0.97)
        tint(stripe, C['stripe'], 0.5, soft=1.2, dmin=0.7, dmax=1.3)
        er = C.get('eye_r', 0.0036)
        for e in eyes:                                        # golden iris around the scan's dark pupil (photos 01-06)
            dd = np.linalg.norm(pos - e[None, None, :], axis=-1)
            pup = (dd < er * 0.75) & (Y < np.percentile(Y[cov & (dd < er)], 35) if (cov & (dd < er)).any() else False)
            iris = (dd < er) & ~pup
            tint(iris, '#C9973A', 0.85, soft=1.0, dmin=0.6, dmax=1.5)
            tint(pup, '#070605', 0.9, soft=0.6, dmin=0.9, dmax=1.1)
        tex = os.path.join(K.CR, '11_TEXTURES', C['sid']); os.makedirs(tex, exist_ok=True)
        dfn = os.path.join(tex, f"T7_{C['sid'].upper()}_{mat.name}_diffuse_v001.jpg")
        srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, 1) ** (1 / 2.4) - 0.055)
        Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=93)
        img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
        b = mat.node_tree.nodes.get('Principled BSDF')
        if b:
            b.inputs['Roughness'].default_value = 0.38; b.inputs['Specular IOR Level'].default_value = 0.4
            b.inputs['Coat Weight'].default_value = 0.35; b.inputs['Coat Roughness'].default_value = 0.12   # moist amphibian skin
            b.inputs['Subsurface Weight'].default_value = 0.08
        print('FROG mat', mat.name, 'stripe px', int(stripe.sum()), flush=True)
    if head_neg:                                              # library convention: faces +X
        for o in bpy.data.objects:
            if o.parent is None and o.type in ('EMPTY', 'MESH'):
                o.matrix_world = Matrix.Rotation(math.pi, 4, 'Z') @ o.matrix_world
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('FROG SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

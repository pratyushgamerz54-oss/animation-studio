"""t7_hornbill_pass — great hornbill (Buceros bicornis) look pass on an AI-assisted perched base (Pigcraft, CC-BY; shape only, wrong plumage):
faces +X (bill tip direction), per-pixel recolour by body region keeping the sculpted feather detail (photo refs 01-02):
black face / throat / breast / wings, cream-yellow neck, white belly + thighs + undertail, cream wing bar, white tail with a broad black band,
grey legs; bill + casque keep their yellow-orange (made matte-waxy). Then `t7_feather_fuzz.py --bird-min-frac 0` softens it.

usage: $BPY45 t7_hornbill_pass.py <in.blend> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(sid='great_hornbill', black='#141312', cream='#E2D6AE', white='#E6E2D8', bar='#DCCB92', legs='#6A6662')


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst = a[0], a[1]
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    ob = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
    ob.data.transform(ob.matrix_world); ob.parent = None; ob.matrix_world = Matrix.Identity(4)
    for o in list(bpy.data.objects):
        if o.type == 'EMPTY':
            bpy.data.objects.remove(o)
    me = ob.data; P = np.array([v.co[:] for v in me.vertices]); H = P[:, 2].max()
    # bill tip = farthest horizontal point of the head zone from the body axis
    body_c = P[P[:, 2] < 0.6 * H].mean(0); head = P[:, 2] > 0.72 * H
    dxy = np.linalg.norm(P[:, :2] - body_c[:2], axis=1); tip = P[head][np.argmax(dxy[head])]
    ang = math.atan2(tip[1] - body_c[1], tip[0] - body_c[0])
    me.transform(Matrix.Translation((body_c[0], body_c[1], 0)) @ Matrix.Rotation(-ang, 4, 'Z') @ Matrix.Translation((-body_c[0], -body_c[1], 0)))
    P = np.array([v.co[:] for v in me.vertices]); c = (P.max(0) + P.min(0)) / 2
    me.transform(Matrix.Translation((-c[0], -c[1], 0))); me.update(); P = np.array([v.co[:] for v in me.vertices])
    N = np.array([v.normal[:] for v in me.vertices], np.float32)
    hb = P[P[:, 2] > 0.72 * H]; hx = np.percentile(hb[:, 0], 50)
    bx = np.median(P[(P[:, 2] > 0.3 * H) & (P[:, 2] < 0.6 * H), 0])      # body centre x
    print('HB faces +X; H', round(float(H), 3), 'head x', round(float(hx), 3), 'body x', round(float(bx), 3), flush=True)
    from PIL import Image, ImageFilter
    A = np.concatenate([P, N], 1).astype(np.float32)
    for mi, mat in enumerate(me.materials):
        tn = next((n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'basecolor' in n.image.name.lower()), None)
        if tn is None:
            continue
        T = np.asarray(Image.open(bpy.path.abspath(tn.image.filepath)).convert('RGB')).astype(np.float32) / 255
        Hh, Ww = T.shape[:2]; Tl = s2l(T); Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
        M, cov = raster(ob, A, Ww, Hh, mi); M = dilate(M, cov); pos, nrm = M[..., :3], M[..., 3:]
        sat = (T.max(-1) - T.min(-1)) / np.maximum(T.max(-1), 1e-3)
        hue_y = (T[..., 0] > T[..., 2] * 1.6) & (sat > 0.45)
        zr = pos[..., 2] / H; fw = nrm[..., 0]
        bill = hue_y & (zr > 0.70)
        Yb = np.asarray(Image.fromarray(np.clip(Y * 255 * 2, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255 / 2
        det = np.clip((Y + 0.01) / (Yb + 0.01), 0.55, 1.6)
        out = Tl.copy()

        def put(m, hexc, d=1.0, soft=2.5):
            mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soft))).astype(np.float32)[..., None] / 255
            out[:] = out * (1 - mm) + np.clip(s2l(CS.hexlin(hexc))[None, None] * (det ** d)[..., None], 0, 1) * mm

        nb = ~bill
        dark0 = Y < 0.08; light0 = (Y > 0.25) & (sat < 0.35)                # the base's own zones: black wings / back, light parts
        behind = pos[..., 0] < bx - 0.22                                      # tail = far behind the body
        tail = nb & behind & (zr < 0.55)
        legs = nb & (zr < 0.13) & ~tail & ~dark0
        headm = nb & (zr > 0.86)
        neck = nb & (zr > 0.70) & (zr <= 0.86)
        throat = neck & (fw > 0.45)
        breast = nb & (zr > 0.50) & (zr <= 0.70) & (fw > 0.15) & ~behind
        belly = nb & light0 & (zr > 0.13) & (zr <= 0.50) & ~tail & (fw > 0.30)
        sidewhite = nb & light0 & (zr > 0.13) & (zr <= 0.70) & ~tail & (fw <= 0.30) & ~legs   # base's white wing edge → black wing
        put(sidewhite, C['black'], 0.6, soft=4)
        put(headm, C['black'], 0.6); put(throat, C['black'], 0.6, soft=4); put(breast, C['black'], 0.6, soft=4)
        put(neck & ~throat & light0, C['cream'], 0.8, soft=4); put(belly, C['white'], 0.8, soft=5)
        wingbar = nb & dark0 & ~behind & (zr > 0.54) & (zr < 0.60) & (np.abs(nrm[..., 1]) > 0.45)
        put(wingbar, C['bar'], 0.8, soft=4)
        tr = (bx - 0.22 - pos[..., 0]); tlen = max(float((bx - 0.22) - P[:, 0].min()), 1e-3); tf = tr / tlen
        put(tail & ((tf < 0.25) | (tf > 0.62)), C['white'], 0.8, soft=4); put(tail & (tf >= 0.25) & (tf <= 0.62), C['black'], 0.6, soft=4)
        put(legs, C['legs'], 0.7)
        tex = os.path.join(K.CR, '11_TEXTURES', C['sid']); os.makedirs(tex, exist_ok=True)
        dfn = os.path.join(tex, f"T7_{C['sid'].upper()}_diffuse_v001.jpg")
        srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, 1) ** (1 / 2.4) - 0.055)
        Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=93)
        img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
        b = mat.node_tree.nodes.get('Principled BSDF')
        if b:
            for k in ('Metallic', 'Roughness'):
                for l in list(b.inputs[k].links):
                    mat.node_tree.links.remove(l)
            b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.8; b.inputs['Specular IOR Level'].default_value = 0.22
        print('HB mat', mat.name, 'bill px', int((bill & cov).sum()), 'tail px', int((tail & cov).sum()), flush=True)
    ob.name = 'T7_GREAT_HORNBILL'
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('HB SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

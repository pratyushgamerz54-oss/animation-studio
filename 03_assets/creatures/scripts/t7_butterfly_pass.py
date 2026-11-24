"""t7_butterfly_pass — Paris peacock (Papilio paris) from a CC0 specimen model of its close relative (Papilio bianor), after
`t7_scan_reduce --delete-mat Material.001` + `t7_feather_fuzz --surface chitin --no-fuzz` (the base is unlit):
1. specimen stands on its wing edge → basking pose: wings flat (plane X-Y), head +X (found from the legs, which sit under the thorax),
   upper side up, feet on z = 0
2. upper side (photo refs): velvet black dusted with green scales (base detail kept), large iridescent blue-green patch on each hindwing,
   (faint forewing band skipped); underside keeps the base (dark with orange-red lunules, like P. paris)
3. scale-wing shading: low roughness sheen on the upper side so the green scales glint

usage: $BPY45 t7_butterfly_pass.py <in.blend> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(sid='paris_peacock', black='#101310', dust='#1C3424', patch='#1AA58E', patch2='#2A6FD0', band='#86B24E')


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
    me = ob.data; P = np.array([v.co[:] for v in me.vertices])
    # wing plane = the two largest extents; normal axis = smallest extent
    ext = np.ptp(P, 0); nax = int(np.argmin(ext))
    if nax != 2:                                                 # specimen on its edge → lay flat (normal axis → Z)
        R = Matrix.Rotation(math.pi / 2, 4, 'X' if nax == 1 else 'Y'); me.transform(R); P = np.array([v.co[:] for v in me.vertices])
    # body axis = the in-plane axis with the narrow central column (span axis is the long one)
    ext = np.ptp(P, 0); span_ax = 0 if ext[0] > ext[1] else 1
    if span_ax == 0:
        me.transform(Matrix.Rotation(math.pi / 2, 4, 'Z')); P = np.array([v.co[:] for v in me.vertices])
    c = (P.max(0) + P.min(0)) / 2; me.transform(Matrix.Translation((-c[0], -c[1], -c[2]))); P = np.array([v.co[:] for v in me.vertices])
    # legs hang off the body on the ventral side, under the thorax (near the head)
    col = np.abs(P[:, 1]) < 0.006
    zmid = np.median(P[col, 2])
    up_n = (col & (P[:, 2] > zmid + 0.004)).sum(); dn_n = (col & (P[:, 2] < zmid - 0.004)).sum()
    legs_side = 1 if up_n > dn_n else -1                         # legs = the side of the body column with more hanging geometry
    if legs_side > 0:                                            # legs must point DOWN (upper side up)
        me.transform(Matrix.Rotation(math.pi, 4, 'X')); P = np.array([v.co[:] for v in me.vertices])
    col = np.abs(P[:, 1]) < 0.006; zmid = np.median(P[col, 2])
    legs = col & (P[:, 2] < zmid - 0.004)
    if P[legs, 0].mean() < 0:                                    # legs sit near the head → head = +X
        me.transform(Matrix.Rotation(math.pi, 4, 'Z')); P = np.array([v.co[:] for v in me.vertices])
    me.transform(Matrix.Translation((0, 0, -P[:, 2].min()))); P = np.array([v.co[:] for v in me.vertices]); me.update()
    col = np.abs(P[:, 1]) < 0.006; zmid = np.median(P[col, 2]); legs = col & (P[:, 2] < zmid - 0.004)
    tx = float(np.median(P[legs, 0])) if legs.any() else 0.0      # thorax x
    W = float(np.abs(P[:, 1]).max())
    print('BFLY basking: span', np.round(np.ptp(P, 0), 3), 'thorax x', round(tx, 4), 'half-span', round(W, 4), flush=True)
    N = np.array([v.normal[:] for v in me.vertices], np.float32)
    A = np.concatenate([P, N], 1).astype(np.float32)
    from PIL import Image, ImageFilter
    for mi, mat in enumerate(me.materials):
        tn = next((n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE'), None)
        if tn is None:
            continue
        T = np.asarray(Image.open(bpy.path.abspath(tn.image.filepath)).convert('RGB')).astype(np.float32) / 255
        Hh, Ww = T.shape[:2]; Tl = s2l(T); Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
        M, cov = raster(ob, A, Ww, Hh, mi)
        if not cov.any():
            continue
        M = dilate(M, cov); pos, nrm = M[..., :3], M[..., 3:]
        Yb = np.asarray(Image.fromarray(np.clip(Y * 255 * 2, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255 / 2
        det = np.clip((Y + 0.01) / (Yb + 0.01), 0.5, 1.8)
        up = (nrm[..., 2] > 0.2) & (np.abs(pos[..., 1]) > 0.004)            # upper wing surfaces
        out = Tl.copy()

        def put(m, hexc, amt=1.0, d=0.8, soft=2.0):
            mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soft))).astype(np.float32)[..., None] / 255
            out[:] = out * (1 - mm * amt) + np.clip(s2l(CS.hexlin(hexc))[None, None] * (det ** d)[..., None], 0, 1) * mm * amt

        g = np.clip(Tl[..., 1] / np.maximum(Tl.max(-1), 1e-3), 0, 1)           # base green dusting strength
        put(up, C['black'], 0.85, d=0.5)
        put(up & (g > 0.45), C['dust'], 0.6, d=0.9, soft=1.0)
        ay = np.abs(pos[..., 1]); hx = pos[..., 0] - tx
        # hindwing patch: behind the thorax, mid-wing, elongated along the wing
        pr = np.sqrt(((hx + 0.025) / 0.0085) ** 2 + ((ay - 0.019) / 0.0065) ** 2)
        patch = up & (pr < 1.0)
        put(patch, C['patch'], 0.85, d=0.6, soft=7)
        put(up & (pr < 0.55), C['patch2'], 0.6, d=0.6, soft=4)                 # bluer centre (iridescent shift)
        # forewing submarginal band: ahead of the thorax line, at 80-88 % of the wing radius
        rr = np.sqrt((pos[..., 0] - tx) ** 2 + pos[..., 1] ** 2) / W
        band = up & (hx > 0.0) & (rr > 0.80) & (rr < 0.87)
        # (the faint forewing band is skipped: too subtle on P. paris to paint without blotches)
        tex = os.path.join(K.CR, '11_TEXTURES', C['sid']); os.makedirs(tex, exist_ok=True)
        dfn = os.path.join(tex, f"T7_{C['sid'].upper()}_{mat.name}_diffuse_v001.jpg")
        srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, 1) ** (1 / 2.4) - 0.055)
        Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=94)
        img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
        b = mat.node_tree.nodes.get('Principled BSDF')
        if b:
            b.inputs['Roughness'].default_value = 0.5; b.inputs['Specular IOR Level'].default_value = 0.3
            b.inputs['Sheen Weight'].default_value = 0.3; b.inputs['Sheen Roughness'].default_value = 0.35
            b.inputs['Sheen Tint'].default_value = (0.25, 0.9, 0.7, 1)                     # scale glint (green-blue)
        hs = next((n for n in mat.node_tree.nodes if n.type == 'HUE_SAT'), None)
        if hs:
            hs.inputs['Value'].default_value = 1.0                                         # our texture is already lit-calibrated
        print('BFLY mat', mat.name, 'patch px', int((patch & cov).sum()), 'band px', int((band & cov).sum()), flush=True)
    ob.name = 'T7_PARIS_PEACOCK'
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('BFLY SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

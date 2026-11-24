"""t7_owl_pass — brown wood owl (Strix leptogrammica) from a perched-owl museum scan (Pel's fishing owl, Strigidae):
1. museum board removed (flat slab at the bottom); the natural branch perch is KEPT (owls are always shown perched)
2. faces +X (forward = head centre → its dark eyes)
3. per-pixel recolour per material, keeping the scan's real feather detail (bars / spots / feather edges), branch untouched:
   buff-tan underparts with dark barring, dark chocolate back + wings, tawny-rufous facial disc, dark 'spectacle' rings round the eyes,
   pale brows (photo refs 01-04, 06); matte feathers

usage: $BPY45 t7_owl_pass.py <in.blend> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, bmesh
from mathutils import Matrix
import t7kit as K
import t7_cc_species as CS
from t7_bird_scan_cc import raster, dilate

C = dict(sid='brown_wood_owl', under='#9C7C56', back='#4A3424', disc='#8A5E3E', ring='#2A1C12', brow='#D8C4A0', eye_r=0.011)


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
    # 1. board = dense flat layer at the bottom → cut everything below its top
    hist, edges = np.histogram(P[:, 2], bins=60, range=(0, H)); pk = int(np.argmax(hist[:10]))
    top = next(i for i in range(pk, 60) if hist[i] < 0.3 * hist[pk]); zcut = edges[top]
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < zcut], context='VERTS'); bm.to_mesh(me); bm.free()
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); seen = set(); isl = []   # drop loose board remnants
    for v0 in bm.verts:
        if v0.index in seen:
            continue
        st = [v0]; seen.add(v0.index); ids = []
        while st:
            v = st.pop(); ids.append(v.index)
            for e in v.link_edges:
                w = e.other_vert(v)
                if w.index not in seen:
                    seen.add(w.index); st.append(w)
        isl.append(ids)
    big = max(len(i) for i in isl)
    bmesh.ops.delete(bm, geom=[bm.verts[i] for ids in isl if len(ids) < 0.01 * big for i in ids], context='VERTS'); bm.to_mesh(me); bm.free()
    P = np.array([v.co[:] for v in me.vertices])
    me.transform(Matrix.Translation((0, 0, -P[:, 2].min()))); P = np.array([v.co[:] for v in me.vertices]); H = P[:, 2].max()
    print('OWL board cut at', round(float(zcut), 3), 'new height', round(float(H), 3), flush=True)
    # texture luminance per vertex (all materials)
    from PIL import Image
    imgs = {}
    for mi, mat in enumerate(me.materials):
        tn = next((n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'normal' not in n.image.name.lower()), None)
        imgs[mi] = (tn, np.asarray(Image.open(bpy.path.abspath(tn.image.filepath)).convert('L')).astype(np.float32) / 255) if tn else None
    yv = np.zeros(len(P), np.float32); cv = np.zeros(len(P), np.float32); uv = me.uv_layers.active.data
    for poly in me.polygons:
        it = imgs.get(poly.material_index)
        if not it:
            continue
        im_ = it[1]; h_, w_ = im_.shape
        for li in poly.loop_indices:
            u, v = uv[li].uv; yv[me.loops[li].vertex_index] += im_[int(np.clip(1 - v % 1, 0, .9999) * h_), int(np.clip(u % 1, 0, .9999) * w_)]
            cv[me.loops[li].vertex_index] += 1
    yv /= np.maximum(cv, 1)
    # 2. forward = head centre → darkest head spots (eyes)
    head = P[:, 2] > H * 0.85
    hc = P[head].mean(0); dk = head & (yv <= np.percentile(yv[head], 1.5))
    fwd = P[dk].mean(0) - hc; ang = math.atan2(fwd[1], fwd[0])
    me.transform(Matrix.Translation((hc[0], hc[1], 0)) @ Matrix.Rotation(-ang, 4, 'Z') @ Matrix.Translation((-hc[0], -hc[1], 0)))
    P = np.array([v.co[:] for v in me.vertices]); ctr = (P.max(0) + P.min(0)) / 2
    me.transform(Matrix.Translation((-ctr[0], -ctr[1], 0))); P = np.array([v.co[:] for v in me.vertices]); me.update()
    hc = P[P[:, 2] > H * 0.85].mean(0); eyes_v = np.where(dk)[0]
    E = P[eyes_v]; eyes = [np.median(E[E[:, 1] > hc[1]], 0), np.median(E[E[:, 1] <= hc[1]], 0)]
    print('OWL forward fixed; head', np.round(hc, 3), 'eyes', [np.round(e, 3) for e in eyes], flush=True)
    N = np.array([v.normal[:] for v in me.vertices], np.float32)
    A = np.concatenate([P, N], 1).astype(np.float32)
    from PIL import ImageFilter
    for mi, it in imgs.items():
        if not it:
            continue
        tn = it[0]; T = np.asarray(Image.open(bpy.path.abspath(tn.image.filepath)).convert('RGB')).astype(np.float32) / 255
        Hh, Ww = T.shape[:2]; Tl = s2l(T); Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
        M, cov = raster(ob, A, Ww, Hh, mi)
        if not cov.any():
            continue
        M = dilate(M, cov); pos, nrm = M[..., :3], M[..., 3:]
        sat = (T.max(-1) - T.min(-1)) / np.maximum(T.max(-1), 1e-3)
        owl = (pos[..., 2] > 0.42 * H) | ((sat > 0.33) & (Y > 0.05) & (pos[..., 2] > 0.18 * H))   # feathers: rufous, saturated; branch = dull wood
        Ym = lambda m: max(float(np.median(Y[m & cov])), 1e-3) if (m & cov).any() else 1.0
        out = Tl.copy()

        def tint(m, hexc, amt, soft=2.0, dmin=0.35, dmax=2.2, gamma=1.0):
            mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soft))).astype(np.float32)[..., None] / 255
            tgt = s2l(CS.hexlin(hexc))[None, None, :] * (np.clip(Y / Ym(m), dmin, dmax) ** gamma)[..., None]
            out[:] = out * (1 - mm * amt) + np.clip(tgt, 0, 1) * mm * amt

        fw = nrm[..., 0]; zr = pos[..., 2] / H
        headm = owl & (zr > 0.80)
        front = owl & (fw > 0.15) & ~headm
        backm = owl & ~front & ~headm
        tint(front, C['under'], 0.85, gamma=1.0); tint(backm, C['back'], 0.85, soft=4, gamma=1.1)
        tint(headm & (fw <= 0.25), C['back'], 0.8, soft=4)
        disc = headm & (fw > 0.25)
        tint(disc, C['disc'], 0.7, soft=9)
        for e in eyes:
            dd = np.linalg.norm(pos - e[None, None, :], axis=-1)
            ring = headm & (dd < C['eye_r'] * 2.1) & (dd > C['eye_r'] * 0.95)
            tint(ring, C['ring'], 0.75, soft=3, dmin=0.6, dmax=1.4)
            brow = headm & (dd > C['eye_r'] * 2.1) & (dd < C['eye_r'] * 2.9) & (pos[..., 2] > e[2] + C['eye_r'] * 1.2)
            tint(brow, C['brow'], 0.5, soft=3)
        tex = os.path.join(K.CR, '11_TEXTURES', C['sid']); os.makedirs(tex, exist_ok=True)
        dfn = os.path.join(tex, f"T7_{C['sid'].upper()}_{me.materials[mi].name}_diffuse_v001.jpg")
        srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * np.clip(out, 0, 1) ** (1 / 2.4) - 0.055)
        Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dfn, quality=93)
        img = bpy.data.images.load(dfn); img.colorspace_settings.name = 'sRGB'; tn.image = img
        print('OWL mat', me.materials[mi].name, 'owl px', int((owl & cov).sum()), 'front', int((front & cov).sum()), flush=True)
    for m in me.materials:
        b = m.node_tree.nodes.get('Principled BSDF')
        if b:
            b.inputs['Roughness'].default_value = 0.78; b.inputs['Specular IOR Level'].default_value = 0.25
            if 'Sheen Weight' in b.inputs:
                b.inputs['Sheen Weight'].default_value = 0.1
    ob.name = 'T7_BROWN_WOOD_OWL'
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('OWL SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

"""t7_bird_scan_cc — a bird species from a museum-mount scan of a related species (TASK 07 'mix' pipeline):
remove stand / rod / pins, face +X, real bill-to-tail length, per-pixel recolour by 3D body region (UV position map) that keeps the
scan's real feather detail (local high-pass luminance), dark bill / legs, species head + collar, real eyeballs (wet cornea).

usage: $BPY45 t7_bird_scan_cc.py <scene.gltf> <species_id> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
import t7kit as K
import t7_cc_species as CS

CFG = {
    # ruddy shelduck (Tadorna ferruginea) from a common-shelduck (Tadorna tadorna) mount: same genus / shape.
    # Photos: orange-chestnut body, pale buff head (face paler), thin black collar (breeding male), black tail, white wing coverts,
    # black primaries, green speculum, black bill + legs, dark brown eye.
    'ruddy_shelduck': dict(head_dir_deg=-45, length=0.64, body_half=0.085,
                           body='#AC4A1A', head='#C48F55', face='#DAB680', bill_len=0.045, collar='#141210', tail='#161412', bill='#1E1C1B',
                           legs='#2A2725', detail=0.55, eye_r=0.0055, eye_iris='#2A1A10', eye_back=0.055, eye_up=0.012),
}


def lin(h):
    return CS.hexlin(h)


def raster(ob, A, W, H):
    """per-pixel barycentric interpolation of a per-vertex attribute A (N x k) over the UV layout → (H, W, k) map + coverage mask"""
    me = ob.data; me.calc_loop_triangles(); uv = me.uv_layers.active.data
    k = A.shape[1]; out = np.zeros((H, W, k), np.float32); cov = np.zeros((H, W), bool)
    for t in me.loop_triangles:
        P = np.array([[uv[li].uv[0] % 1.0 * W, (1 - uv[li].uv[1] % 1.0) * H] for li in t.loops])
        x0, y0 = np.floor(P.min(0)).astype(int); x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W - 1), min(y1, H - 1)
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        (ax, ay), (bx, by), (cx, cy) = P
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12:
            continue
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den; l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den; l3 = 1 - l1 - l2
        ins = (l1 >= -0.05) & (l2 >= -0.05) & (l3 >= -0.05)
        if not ins.any():
            continue
        a3 = A[list(t.vertices)]
        val = l1[..., None] * a3[0] + l2[..., None] * a3[1] + l3[..., None] * a3[2]
        out[y0:y1 + 1, x0:x1 + 1][ins] = val[ins]; cov[y0:y1 + 1, x0:x1 + 1][ins] = True
    return out, cov


def dilate(img, cov, n=6):
    """grow covered pixels into the UV gutters (no seams at island borders)"""
    from scipy import ndimage
    idx = ndimage.distance_transform_edt(~cov, return_distances=False, return_indices=True)
    return img[idx[0], idx[1]]


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, sid, out = a[0], a[1], a[2]; c = CFG[sid]
    K.clean(); bpy.ops.import_scene.gltf(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    bird = max(meshes, key=lambda o: len(o.data.vertices))
    bpy.context.view_layer.update()
    mw = bird.matrix_world.copy(); bird.parent = None; bird.data.transform(mw); bird.matrix_world = Matrix.Identity(4)   # bake glTF Y-up first
    for o in meshes:                                   # stand, support rod, mounting pins
        if o is not bird:
            bpy.data.objects.remove(o)
    for o in list(bpy.data.objects):
        if o.type == 'EMPTY':
            bpy.data.objects.remove(o)
    P = np.array([v.co[:] for v in bird.data.vertices])
    # face +X: bill tip = farthest point along the hinted head direction (top view)
    hd = math.radians(c['head_dir_deg']); dvec = np.array([math.cos(hd), math.sin(hd), 0])
    tip = P[np.argmax(P @ dvec)]; ctr = P.mean(0)
    v = tip[:2] - ctr[:2]; ang = -math.atan2(v[1], v[0])
    R = Matrix.Rotation(ang, 4, 'Z'); bird.data.transform(R @ Matrix.Translation(-Vector(ctr)))
    P = np.array([v.co[:] for v in bird.data.vertices])
    tipi = np.argmax(P[:, 0]); y0 = P[tipi, 1]
    body = np.abs(P[:, 1] - y0) < 0.25 * np.ptp(P[:, 1])            # body column (excludes the spread wings)
    L0 = P[tipi, 0] - P[body, 0].min(); s = c['length'] / L0
    bird.data.transform(Matrix.Diagonal((s, s, s, 1)) @ Matrix.Translation((-P[tipi, 0], -y0, 0)))   # bill tip at x = 0
    P = np.array([v.co[:] for v in bird.data.vertices]); bird.data.transform(Matrix.Translation((0, 0, -P[:, 2].min())))
    P = np.array([v.co[:] for v in bird.data.vertices]); Lb = c['length']
    print('BIRD span', np.round(np.ptp(P, 0), 3))
    # ---- per-pixel recolour
    from PIL import Image, ImageFilter
    mat = bird.data.materials[0]; b = mat.node_tree.nodes['Principled BSDF']; tn = b.inputs['Base Color'].links[0].from_node
    srcp = bpy.path.abspath(tn.image.filepath)
    T = np.asarray(Image.open(srcp).convert('RGB')).astype(np.float32) / 255; H, W = T.shape[:2]
    Tl = np.where(T <= 0.04045, T / 12.92, ((T + 0.055) / 1.055) ** 2.4)                      # linear
    pos, cov = raster(bird, P.astype(np.float32), W, H); pos = dilate(pos, cov)
    sx = 1 + pos[..., 0] / Lb                       # 1 = bill tip, 0 = tail tip
    lat = np.abs(pos[..., 1]); z = pos[..., 2]
    Y = Tl @ np.array([.2126, .7152, .0722], np.float32)
    Yb = np.asarray(Image.fromarray(np.clip(Y * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))).astype(np.float32) / 255
    det = np.clip((Y + 0.01) / (Yb + 0.01), 0.4, 2.0) ** c['detail']                            # local feather detail only
    hue_red = (T[..., 0] > 1.5 * T[..., 1]) & (T[..., 0] > 0.35)
    feet = (T[..., 0] > 1.9 * T[..., 1]) & (T[..., 0] > 0.45) & (T[..., 0] > 1.6 * T[..., 2])   # saturated orange-pink feet only (not brown stains)
    # landmarks from the scan itself: bill base (red bill), end of the dark head
    nb = (lat < 0.05) & (sx > 0.70)
    s_bb = 1 - c['bill_len'] / Lb if c.get('bill_len') else (np.percentile(sx[nb & hue_red], 4) if (nb & hue_red).sum() > 50 else 0.93)
    dark_head = nb & (Y < 0.03) & (sx < s_bb)
    s_hb = np.percentile(sx[dark_head], 3) if dark_head.sum() > 50 else 0.72
    print('BIRD landmarks bill base', round(float(s_bb), 3), 'head base', round(float(s_hb), 3))
    neck_w = 0.06; body_w = c['body_half']
    wing = lat > body_w
    reg = {}
    reg['bill'] = (sx >= s_bb - 0.004) & (lat < 0.04)
    reg['legs'] = (hue_red & (sx < 0.32) & ~wing) | (feet & (sx < 0.70))   # in flight the feet are tucked under the tail & ~reg['bill']
    head = (sx > s_hb + 0.012) & (lat < neck_w) & ~reg['bill']
    reg['collar'] = (sx > s_hb - 0.010) & (sx <= s_hb + 0.012) & (lat < neck_w)
    reg['tail'] = (sx < 0.11) & ~wing & ~reg['legs']
    reg['body'] = ~wing & ~head & ~reg['collar'] & ~reg['bill'] & ~reg['legs'] & ~reg['tail'] & (sx < s_hb + 0.02)
    outc = Tl.copy()

    def put(m, col, d=det, feather=2.0):
        mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))).astype(np.float32)[..., None] / 255
        cc = lin(col)[None, None, :] * d[..., None]
        outc[:] = outc * (1 - mm) + np.clip(cc, 0, 1) * mm

    detb = np.clip(det, 0.78, 1.3)
    put(reg['body'], c['body'], d=detb); put(reg['tail'], c['tail']); put(reg['collar'], c['collar'], feather=1.2)
    # head: buff, paler toward the face (gradient along the head)
    hg = np.clip((sx - s_hb) / max(s_bb - s_hb, 1e-3), 0, 1)[..., None]
    hc = lin(c['head'])[None, None, :] * (1 - hg) + lin(c['face'])[None, None, :] * hg
    mm = np.asarray(Image.fromarray((head * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)[..., None] / 255
    outc[:] = outc * (1 - mm) + np.clip(hc * det[..., None] ** 0.7, 0, 1) * mm
    wd = wing & (Y < 0.22); put(wd, '#0E0D0C', d=np.clip(Y / 0.05, 0.6, 2.2) ** 0.5, feather=1.0)   # black primaries / secondaries
    put(reg['bill'], c['bill'], d=det ** 0.5, feather=1.0); put(reg['legs'], c['legs'], d=det ** 0.5, feather=1.0)
    tex = os.path.join(K.CR, '11_TEXTURES', sid); os.makedirs(tex, exist_ok=True)
    dst = os.path.join(tex, f'T7_{sid.upper()}_diffuse_v001.jpg')
    srgb = np.where(outc <= 0.0031308, outc * 12.92, 1.055 * np.clip(outc, 0, 1) ** (1 / 2.4) - 0.055)
    Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(dst, quality=92)
    img = bpy.data.images.load(dst); img.colorspace_settings.name = 'sRGB'; old = tn.image; tn.image = img
    if old.users == 0:
        bpy.data.images.remove(old)
    for k in ('Metallic', 'Roughness'):
        for l in list(b.inputs[k].links):
            mat.node_tree.links.remove(l)
    b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.72; b.inputs['Specular IOR Level'].default_value = 0.25
    if 'Sheen Weight' in b.inputs:
        b.inputs['Sheen Weight'].default_value = 0.08; b.inputs['Sheen Roughness'].default_value = 0.5   # soft feather sheen
    # ---- eyes: ray-cast sideways onto the head, behind the bill base
    me = bird.data; bvh = BVHTree.FromPolygons([v.co for v in me.vertices], [p.vertices for p in me.polygons])
    xb = (s_bb - 1) * Lb; hp = P[(P[:, 0] > xb - 0.07) & (P[:, 0] < xb) & (np.abs(P[:, 1]) < 0.04)]
    zc = np.median(hp[:, 2]) if len(hp) else P[:, 2].max()
    em = K.mat_eye(f'T7_{sid.upper()}_EYE', iris=c['eye_iris'], pupil_r=0.55, sclera='#140E0A', iris_r=0.9)
    coll = bird.users_collection[0]
    for sg in (1, -1):
        st = Vector((xb - c['eye_back'], sg * 0.15, zc + c['eye_up']))
        h = bvh.ray_cast(st, Vector((0, -sg, 0)))
        if h[0] is None:
            print('eye ray missed', sg); continue
        d = (h[1] + Vector((0.25, 0, 0))).normalized()
        K.eyeball(f'{sid}_eye_{"L" if sg > 0 else "R"}', h[0] - h[1] * c['eye_r'] * 0.5, c['eye_r'], d, em, coll)
    bird.name = f'T7_{sid.upper()}'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=True)
    print('BIRD SAVED', out, os.path.getsize(out) // 1024, 'KB', {k: int(v.sum()) for k, v in reg.items()})


if __name__ == '__main__':
    main()

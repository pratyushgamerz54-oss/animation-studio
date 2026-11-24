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
    'black_bear': dict(base='black_bear/bffc3c87d2d148ff8533e1cc8a11c9f1', withers=0.85, pelvis='RigPelvis_02', chest='RigChest_013',
                       delete=('Icosphere',), still_action='Stand_Breathing_01',
                       # photo refs 01-03 (Commons): black shaggy coat, cream-white chest crescent / V, tan-brown muzzle
                       palette=dict(dark='#070606', mid='#100E0D', light='#2A2420', cap=1.6, gamma=1.0),
                       paint=[('chest_v', '#E8E0CF', 'chest_v', 'Material_003'), ('muzzle', '#6A4C36', 'muzzle', 'Material_001')], rough=0.55),
    'red_fox': dict(base='red_fox/4e37c303f8a241aaa2511bd9f3019273', withers=0.40, pelvis='Fox_ Pelvis_02', chest='Fox_ Spine1_012',
                    delete=('Icosphere',), still_action='root.001|Waking Up', still_frame=480, palette=None, rough=0.6,
                    ground_snap='root.001|Waking Up'),
    'marmot': dict(base='marmot/bf70e9fdea114943b0dc5cff336bf3e0', height=0.50, orient_deg=90.0,
                   delete=('Icosphere',), still_action=None, rough=0.7, chest='Bone.001_11', nose_bone='Bone.004_0', head_bone='Bone.004_0',
                   # photo refs 01-03 (Himalayan marmot, Commons): golden-tawny coat, dark brown face mask / crown, pale cream muzzle
                   palette=dict(dark='#3E2E1E', mid='#86643A', light='#C2A068', cap=1.5, gamma=1.0),
                   paint=[('dorsal', '#5A4228', 'dorsal', '*'), ('face_mask', '#33271C', 'face_mask', '*'), ('muzzle_pale', '#CDB690', 'muzzle_pale', '*'),
                          ('paws', '#3A2C20', 'bones:Bone.020,Bone.025,Bone.012,Bone.016', '*')]),
}


def region(kind, P, N, B):
    """soft 0..1 weight of an anatomical region on the (+X-facing, ground at z=0) body. B = dict of bone points."""
    ch, hd = B['chest'], B['head']
    if kind == 'chest_v':       # crescent / V on the FRONT of the chest between the forelegs (photo 02), opening upward
        W = B['W']; zl, zh = 0.50 * W, 0.70 * W
        face_fwd = np.clip((N[:, 0] - 0.55) / 0.3, 0, 1)
        inz = (P[:, 2] > zl) & (P[:, 2] < zh) & (P[:, 0] > ch[0])
        arm_ = (P[:, 2] - zl) * 1.1                                   # half-width of the V at this height
        band = (np.abs(P[:, 1]) < arm_) & (np.abs(P[:, 1]) > arm_ - 0.07 * W)
        base = (P[:, 2] - zl < 0.11 * W) & (P[:, 2] > zl - 0.03 * W) & (np.abs(P[:, 1]) < 0.10 * W) & (P[:, 0] > ch[0])  # centre of the crescent (sternum)
        return np.clip(inz * band * face_fwd * 1.5 + base * np.clip(N[:, 0] + 0.2, 0, 1) * 1.5, 0, 1)
    if kind == 'face_mask':     # marmot: dark crown + eye band + upper muzzle (photo refs)
        d = np.linalg.norm(P - B['nose'], axis=1); W = B['W']
        up = P[:, 2] > B['nose'][2] - 0.012 * W
        mid = np.clip(1 - (np.abs(P[:, 1] - B['nose'][1]) - 0.04 * W) / (0.05 * W), 0, 1)       # band over the nose bridge / crown, not the cheeks
        return np.clip(1 - (d - 0.06 * W) / (0.12 * W), 0, 1) * up * mid * (d > 0.022 * W)
    if kind == 'dorsal':        # marmot: darker back (upright pose → the back faces −X), grizzled dark over the shoulders
        return np.clip((-N[:, 0] - 0.2) / 0.5, 0, 1) * np.clip((P[:, 2] - 0.25 * B['W']) / (0.3 * B['W']), 0, 1) * 0.85
    if kind == 'muzzle_pale':   # marmot: cream muzzle / chin around the nose
        d = np.linalg.norm(P - B['nose'], axis=1); W = B['W']
        return np.clip(1 - (d - 0.035 * W) / (0.06 * W), 0, 1) * (P[:, 2] < B['nose'][2] + 0.004 * W)
    if kind == 'muzzle':        # tan muzzle: last ~12 cm (scaled) before the nose tip, below the eye line
        d = P[:, 0] - (B['nose'][0] - 0.14 * B['W'])
        return np.clip(d / (0.04 * B['W']), 0, 1) * (P[:, 2] < B['nose'][2] + 0.05 * B['W'])
    return np.zeros(len(P))


def paint_uv(img_path, ob, weights, color, feather_px=3):
    """paint a soft per-vertex weight field into the object's UV texture: per-pixel barycentric interpolation of the vertex weights
    inside every UV triangle (smooth, no faceted blotches), blend toward colour while keeping the base's hair detail."""
    from PIL import Image, ImageFilter
    im = Image.open(img_path).convert('RGBA'); W_, H_ = im.size
    mask = np.zeros((H_, W_), np.float32)
    uv = ob.data.uv_layers.active.data
    me = ob.data; me.calc_loop_triangles()
    wv = np.asarray(weights, np.float32)
    for t in me.loop_triangles:
        w3 = wv[list(t.vertices)]
        if w3.max() <= 0.01:
            continue
        P = np.array([[uv[li].uv[0] * W_, (1 - uv[li].uv[1]) * H_] for li in t.loops])
        x0, y0 = np.floor(P.min(0)).astype(int); x1, y1 = np.ceil(P.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W_ - 1), min(y1, H_ - 1)
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        (ax, ay), (bx, by), (cx, cy) = P
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
        l3 = 1 - l1 - l2
        inside = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
        val = l1 * w3[0] + l2 * w3[1] + l3 * w3[2]
        sub = mask[y0:y1 + 1, x0:x1 + 1]
        sub[inside] = np.maximum(sub[inside], np.clip(val[inside], 0, 1))
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather_px))).astype(np.float32)[..., None] / 255
    a = np.asarray(im).astype(np.float32) / 255; Yl = a[..., :3] @ np.array([.2126, .7152, .0722]); Yl = Yl / max(np.median(Yl), 1e-3)
    cc = hexlin(color)[None, None, :] * np.clip(0.75 + 0.25 * Yl, 0.5, 1.3)[..., None]
    out = a.copy(); out[..., :3] = a[..., :3] * (1 - m) + np.clip(cc, 0, 1) * m
    Image.fromarray((out * 255).astype(np.uint8)).save(img_path)


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
    g = (glob.glob(os.path.join(K.CR, '00_CREATURE_REFERENCES', 'cc_models', cfg['base'], 'scene.gltf')) +
         glob.glob(os.path.join(os.environ.get('T7_CAND', '/nonexistent'), cfg['base'], 'scene.gltf')))[0]
    bpy.ops.import_scene.gltf(filepath=g)
    for n in cfg.get('delete', ()):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o)
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    root = next(o for o in bpy.data.objects if o.parent is None and o.type == 'EMPTY')
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    body = max(meshes, key=lambda o: len(o.data.polygons))
    if cfg.get('still_action') and cfg['still_action'] in bpy.data.actions:
        arm.animation_data.action = bpy.data.actions[cfg['still_action']]
    bpy.context.scene.frame_set(cfg.get('still_frame', 0)); bpy.context.view_layer.update()
    pb = arm.pose.bones
    if cfg.get('height'):                 # upright / unusual poses: fixed facing rotation + total height
        root.matrix_world = Matrix.Rotation(math.radians(cfg.get('orient_deg', 0.0)), 4, 'Z') @ root.matrix_world; bpy.context.view_layer.update()
        P = np.concatenate([mesh_world(o) for o in meshes])
        s = cfg['height'] / np.ptp(P[:, 2])
    else:
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
    if cfg.get('ground_snap') and cfg['ground_snap'] in bpy.data.actions:
        # ground contact: per-frame lowest point → 0 (smoothed, no jitter); keyed on the root empty (object-level, separate from the rig action)
        act = bpy.data.actions[cfg['ground_snap']]; arm.animation_data.action = act
        f0, f1 = map(int, act.frame_range); sc = bpy.context.scene; base_z = root.location.z; mins = []
        for f in range(f0, f1 + 1):
            sc.frame_set(f); mins.append(min(mesh_world(o)[:, 2].min() for o in meshes))
        m = np.array(mins)                      # world lowest point per frame (root at base_z)
        k = np.ones(7) / 7; ms = np.convolve(np.pad(m, 3, mode='edge'), k, mode='valid')
        for i, f in enumerate(range(f0, f1 + 1)):
            root.location.z = base_z - ms[i]; root.keyframe_insert('location', index=2, frame=f)
        print('ground snap: raw offsets cm min/max', round(m.min() * 100 - base_z * 0, 1), round(m.max() * 100, 1))
        if cfg.get('still_action') and cfg['still_action'] in bpy.data.actions:
            arm.animation_data.action = bpy.data.actions[cfg['still_action']]
        sc.frame_set(cfg.get('still_frame', 0))
    tex = os.path.join(K.CR, '11_TEXTURES', sid)
    pal = cfg.get('palette')
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        b = mat.node_tree.nodes.get('Principled BSDF')
        if not b:
            continue
        L = b.inputs['Base Color'].links
        if pal and L and L[0].from_node.type == 'TEX_IMAGE' and L[0].from_node.image:
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
    if cfg.get('paint'):
        Pb = mesh_world(body)
        Bp = dict(chest=np.array((arm.matrix_world @ pb[cfg['chest']].head)[:]),
                  head=np.array((arm.matrix_world @ pb[cfg.get('head_bone') or [b.name for b in pb if 'Head' in b.name][0]].head)[:]), L=float(np.ptp(Pb[:, 0])), W=cfg.get('withers', cfg.get('height', 1.0)))
        for ob in meshes:
            if not ob.active_material or not ob.active_material.use_nodes or not ob.data.uv_layers:
                continue
            img_node = next((n for n in ob.active_material.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and
                             'diffuse_v002' in (n.image.filepath or '')), None)
            if img_node is None:
                continue
            Pw = mesh_world(ob); Nw = np.array([(ob.matrix_world.to_3x3() @ v.normal).normalized()[:] for v in ob.data.vertices])
            if len(Pw) != len(ob.data.vertices):
                continue
            if cfg.get('nose_bone'):                                    # nose = tip of the head bone (paws can be further forward)
                Bp['nose'] = np.array((arm.matrix_world @ pb[cfg['nose_bone']].tail)[:])
            Bp['nose'] = Pw[np.argmax(Pw[:, 0])] if 'nose' not in Bp else Bp['nose']
            for name, colr, kind, matname in cfg['paint']:
                if matname != '*' and ob.active_material.name != matname:
                    continue
                if kind == 'muzzle' and not cfg.get('nose_bone'):
                    Bp['nose'] = Pw[np.argmax(Pw[:, 0])]
                if kind.startswith('bones:'):                            # region by skin weights of the listed bones
                    names = kind[6:].split(','); idx = [g.index for g in ob.vertex_groups if any(g.name.startswith(n) for n in names)]
                    w = np.array([max([gg.weight for gg in v.groups if gg.group in idx] or [0.0]) for v in ob.data.vertices], np.float32)
                else:
                    w = region(kind, Pw, Nw, Bp)
                print('paint', ob.name, name, 'verts', int((w > 0.1).sum()))
                if w.max() > 0:
                    paint_uv(bpy.path.abspath(img_node.image.filepath), ob, w, colr)
            img_node.image.reload()
    if os.path.exists(os.path.join(tex, '_src.png')):
        os.remove(os.path.join(tex, '_src.png'))
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f'T7_{sid.upper()}_CC_v002.blend')
    bpy.ops.wm.save_as_mainfile(filepath=fn, compress=True, relative_remap=True)
    print('SAVED', fn)


if __name__ == '__main__':
    main()

"""t7_static_fur_cc — furred mammal from an UNRIGGED free-licence base whose mesh is unusable as-is (AI / fragmented shells,
flat whisker strips) (TASK 07 'mix' pipeline): keep the base's SHAPE only →
join → face +X, real length → find the base's eye spots (dark texture) → VOXEL REMESH (one watertight surface; thin whisker strips
vanish) + smooth → photo-matched coat colour per vertex by 3D region (back / flank / belly / pale throat / feet / nose) with natural
mottling → matte skin → real eyeballs + fine whiskers → strand groom (length / comb by body position, no armature needed).
Rig → milestone 2 (the groom follows the deformed mesh).

usage: $BPY45 t7_static_fur_cc.py <scene.gltf> <species_id> <out.blend>
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
    # Eurasian otter (Lutra lutra): photos 01/02/04/06 — dark chocolate-brown back + tail (sleek, wet-looking), slightly paler flanks,
    # cream / pale grey-buff throat, lips, cheeks and chest, dark brown feet, dark nose leather, pale whiskers.
    # Size: head-body 0.57–0.95 m + tail 0.35–0.45 m → total 1.10 m.
    'eurasian_otter': dict(length=1.10, voxel=0.0035, smooth=6, back='#3E2C20', flank='#55402E', belly='#6A543F', pale='#B8A68C',
                           feet='#2E2219', nose='#17120F', pale_from=0.66, eye_back=0.040, eye_up=0.016, head_from=0.86, eye_r=0.0065, eye_iris='#1A100A',
                           whiskers=12, whisker_len=0.075, whisker_col='#D8D0C4',
                           fur=dict(body=0.020, head=0.006, muzzle=0.0028, tail=0.011, feet=0.004),
                           density=320000, radius=0.00019, lift=0.22, droop=0.30, frizz=0.32, coat_var=0.22, hair_rough=0.40, hair_coat=0.15, hair_gain=0.95),
}


def s2l(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def lin(h):                                  # hex (sRGB) → linear
    return s2l(CS.hexlin(h))


def vnoise(P, scale, seed):
    """smooth value noise in 3D (trilinear on a random lattice) → 0..1"""
    rng = np.random.default_rng(seed); G = rng.random((64, 64, 64))
    q = P / scale; i = np.floor(q).astype(int); f = q - i; f = f * f * (3 - 2 * f); out = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                out = out + w * G[(i[:, 0] + dx) % 64, (i[:, 1] + dy) % 64, (i[:, 2] + dz) % 64]
    return out


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, sid, out = a[0], a[1], a[2]; c = CFG[sid]
    K.clean(); bpy.ops.import_scene.gltf(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    bpy.context.view_layer.update()
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    for o in meshes:                                   # bake parents (glTF Y-up) before removing the empties
        mw = o.matrix_world.copy(); o.parent = None; o.data.transform(mw); o.matrix_world = Matrix.Identity(4)
    for o in list(bpy.data.objects):
        if o.type == 'EMPTY':
            bpy.data.objects.remove(o)
    bpy.context.view_layer.update()
    for x in bpy.data.objects:
        x.select_set(False)
    for o in meshes:
        o.select_set(True)
    body = meshes[0]; bpy.context.view_layer.objects.active = body
    if len(meshes) > 1:
        with bpy.context.temp_override(active_object=body, selected_editable_objects=meshes, selected_objects=meshes):
            bpy.ops.object.join()
    P = np.array([v.co[:] for v in body.data.vertices])
    hi = P[:, 2] > np.percentile(P[:, 2], 90)          # raised head end = +X
    if P[hi, 0].mean() < P[:, 0].mean():
        body.data.transform(Matrix.Rotation(math.pi, 4, 'Z')); P = np.array([v.co[:] for v in body.data.vertices])
    s = c['length'] / np.ptp(P[:, 0]); ctr = (P.max(0) + P.min(0)) / 2
    body.data.transform(Matrix.Diagonal((s, s, s, 1)) @ Matrix.Translation((-ctr[0], -ctr[1], -P[:, 2].min())))
    P = np.array([v.co[:] for v in body.data.vertices]); L = c['length']
    # eye spots from the base texture: darkest head vertices on +Y, mirrored (base is symmetric)
    me = body.data; mat0 = me.materials[0]; bn0 = mat0.node_tree.nodes['Principled BSDF']; tn0 = bn0.inputs['Base Color'].links[0].from_node
    im = tn0.image; w_, h_ = im.size; buf = np.empty(w_ * h_ * im.channels, np.float32); im.pixels.foreach_get(buf)
    Y = (buf.reshape(h_, w_, im.channels)[..., :3] @ np.array([.2126, .7152, .0722], np.float32)); del buf
    uv = me.uv_layers.active.data; yv = np.zeros(len(P), np.float32); cv = np.zeros(len(P), np.float32)
    for li, l in enumerate(me.loops):
        u, v = uv[li].uv; yv[l.vertex_index] += Y[int(np.clip(v % 1.0, 0, 0.9999) * h_), int(np.clip(u % 1.0, 0, 0.9999) * w_)]; cv[l.vertex_index] += 1
    yv /= np.maximum(cv, 1); vs = (P[:, 0] + L / 2) / L
    nose = P[np.argmax(P[:, 0])].copy()
    cand = np.where((vs > c['head_from']) & (P[:, 0] < nose[0] - 0.02) & (P[:, 1] > 0.008) & (P[:, 2] > nose[2]))[0]
    dk = cand[yv[cand] <= np.percentile(yv[cand], 1.0)]
    eyeL = np.median(P[dk], 0); print('FUR eye spot', np.round(eyeL, 3), 'nose', np.round(nose, 3), flush=True)
    # ---- voxel remesh: one clean surface
    m = body.modifiers.new('rm', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = c['voxel']; m.adaptivity = 0.0; K._apply(body, m)
    import bmesh                                       # keep only the main body: drop loose remnants (old whisker strips etc.)
    bm = bmesh.new(); bm.from_mesh(body.data); bm.verts.ensure_lookup_table(); seen = np.zeros(len(bm.verts), bool); isl = []
    for v0 in bm.verts:
        if seen[v0.index]:
            continue
        st = [v0]; seen[v0.index] = True; ids = []
        while st:
            v = st.pop(); ids.append(v.index)
            for e in v.link_edges:
                w = e.other_vert(v)
                if not seen[w.index]:
                    seen[w.index] = True; st.append(w)
        isl.append(ids)
    big = max(len(i) for i in isl); kill = [bm.verts[i] for ids in isl if len(ids) < 0.05 * big for i in ids]
    bmesh.ops.delete(bm, geom=kill, context='VERTS'); bm.to_mesh(body.data); bm.free()
    print('FUR loose islands removed', sum(1 for i in isl if len(i) < 0.05 * big), 'verts', len(kill), flush=True)
    m = body.modifiers.new('sm', 'SMOOTH'); m.factor = 0.5; m.iterations = c['smooth']; K._apply(body, m)
    for p_ in body.data.polygons:
        p_.use_smooth = True
    for im_ in list(bpy.data.images):
        bpy.data.images.remove(im_)
    me = body.data; P = np.array([v.co[:] for v in me.vertices]); vs = (P[:, 0] + L / 2) / L
    body.name = f'T7_{sid.upper()}'
    print('FUR remeshed verts', len(P), 'span', np.round(np.ptp(P, 0), 3), flush=True)
    # ---- coat colour per vertex (linear)
    nb = 80; bi = np.clip((vs * nb).astype(int), 0, nb - 1); zc = np.zeros(nb); hz = np.ones(nb) * 0.05
    for k in range(nb):
        q = P[bi == k, 2]
        if len(q) > 10:
            zc[k] = (q.max() + q.min()) / 2; hz[k] = max((q.max() - q.min()) / 2, 0.01)
    low = np.clip((zc[bi] - P[:, 2]) / hz[bi], -1, 1)
    up_ = np.clip(-low, 0, 1)[:, None]
    col = lin(c['back'])[None] * up_ + lin(c['flank'])[None] * (1 - up_)
    wb = np.clip((low - 0.35) / 0.4, 0, 1)[:, None]; col = col * (1 - wb) + lin(c['belly'])[None] * wb
    wp = (np.clip((low - 0.15) / 0.3, 0, 1) * np.clip((vs - c['pale_from']) / 0.05, 0, 1))[:, None]
    col = col * (1 - wp) + lin(c['pale'])[None] * wp
    wf = (np.clip((0.045 - P[:, 2]) / 0.02, 0, 1) * (vs > 0.12))[:, None]; col = col * (1 - wf) + lin(c['feet'])[None] * wf
    nose = P[np.argmax(P[:, 0])]
    wn = np.clip((P[:, 0] - (nose[0] - 0.016)) / 0.006, 0, 1)[:, None]; col = col * (1 - wn) + lin(c['nose'])[None] * wn
    mott = 0.86 + 0.28 * (0.6 * vnoise(P, 0.05, 1) + 0.4 * vnoise(P, 0.012, 2))
    col = np.clip(col * mott[:, None], 0, 1).astype(np.float32)
    K.put_coat(body, col)
    sk = K.mat_attr(f'T7_{sid.upper()}_SKIN', attr='coat', rough=0.82, spec=0.2, bump=0.3)
    me.materials.clear(); me.materials.append(sk)
    # ---- eyes (mirrored pair, projected onto the remeshed surface) + fine whiskers
    bvh = BVHTree.FromPolygons([v.co for v in me.vertices], [p_.vertices for p_ in me.polygons])
    em = K.mat_eye(f'T7_{sid.upper()}_EYE', iris=c['eye_iris'], pupil_r=0.6, sclera='#120C08', iris_r=0.9)
    coll = body.users_collection[0]
    for sg in (1, -1):
        if c.get('eye_back'):                        # anatomical placement: side ray onto the head behind the nose
            hh = bvh.ray_cast(Vector((nose[0] - c['eye_back'], sg * 0.15, nose[2] + c['eye_up'])), Vector((0, -sg, 0)))
            loc, nrm = hh[0], hh[1]
        else:
            loc, nrm, _, _ = bvh.find_nearest(Vector((eyeL[0], sg * eyeL[1], eyeL[2])))
        d = (nrm + Vector((0.35, 0, 0))).normalized()
        K.eyeball(f'{sid}_eye_{"L" if sg > 0 else "R"}', loc - nrm * c['eye_r'] * 0.45, c['eye_r'], d, em, coll)
    cu = bpy.data.curves.new(f'{sid}_whiskers', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.00022; cu.bevel_resolution = 1
    rg = np.random.default_rng(5)
    for sg in (1, -1):
        for i in range(c['whiskers']):
            t = i / max(c['whiskers'] - 1, 1)
            h = bvh.ray_cast(Vector((nose[0] - 0.012 - 0.016 * t, sg * 0.08, nose[2] - 0.004 - 0.010 * t)), Vector((0, -sg, 0)))
            if h[0] is None:
                continue
            dirn = Vector((-0.40 - 0.2 * rg.random(), sg * 0.90, 0.20 - 0.18 * t)).normalized()   # out-back, fanned, not drooping
            Lw = c['whisker_len'] * (0.6 + 0.4 * rg.random()); sp = cu.splines.new('POLY'); sp.points.add(3)
            for k in range(4):
                q = k / 3; pp = h[0] + dirn * Lw * q - Vector((0, 0, 0.07 * Lw * q * q))
                sp.points[k].co = (*pp, 1.0); sp.points[k].radius = 1.0 - 0.85 * q
    wo = bpy.data.objects.new(f'{sid}_whiskers', cu); coll.objects.link(wo)
    cu.materials.append(K.mat_simple(f'T7_{sid.upper()}_WHISKER', c['whisker_col'], rough=0.4, spec=0.35, var=0.1, bump=0.0))
    # ---- groom
    f = c['fur']; Lf = np.full(len(P), f['body'], np.float32)
    tail = vs < 0.33; Lf[tail] = f['tail'] * (0.5 + 0.5 * np.clip(vs[tail] / 0.33, 0, 1))
    head = vs > c['head_from']; mz = np.clip((vs - c['head_from']) / (1 - c['head_from']), 0, 1)
    Lf[head] = f['head'] * (1 - mz[head]) + f['muzzle'] * mz[head]
    neck = (vs > c['head_from'] - 0.06) & ~head; tn_ = (vs[neck] - (c['head_from'] - 0.06)) / 0.06
    Lf[neck] = f['body'] * (1 - tn_) + f['head'] * tn_
    foot = (P[:, 2] < 0.06) & ~tail; Lf[foot] = np.minimum(Lf[foot], f['feet'] + (P[foot, 2] / 0.06) * (f['body'] - f['feet']))
    comb = np.tile(np.array([-1.0, 0.0, -0.25], np.float32), (len(P), 1))
    leg = (P[:, 2] < 0.14) & ~tail & ~head; comb[leg] = (-0.35, 0.0, -1.0)
    comb /= np.linalg.norm(comb, axis=1, keepdims=True)
    dens = np.ones(len(P), np.float32); dens[P[:, 0] > nose[0] - 0.012] = 0.0
    K.set_attr(body, 'fur_len', Lf); K.set_attr(body, 'fur_density', dens); K.set_attr(body, 'comb', comb, 'FLOAT_VECTOR')
    hm = K.mat_hair(f'T7_{sid.upper()}_HAIR', rough=c['hair_rough'], coat_var=c.get('coat_var', 0.12), coat=c['hair_coat'])
    K.fur(body, hm, density=c['density'], radius=c['radius'], lift=c['lift'], droop=c['droop'], frizz=c['frizz'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=True)
    print('FUR SAVED', out, os.path.getsize(out) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

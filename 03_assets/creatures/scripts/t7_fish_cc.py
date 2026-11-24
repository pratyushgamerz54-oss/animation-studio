"""t7_fish_cc — fish species from a free-licence fish base: face +X, reshape to the species' proportions, real length,
photo-matched recolour, WET skin (fish are the one place the realism rule allows gloss: wet scales, low roughness, clear coat).

usage: $BPY45 t7_fish_cc.py <scene.gltf> <species_id> <out.blend>
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix, Vector
import t7kit as K
import t7_cc_species as CS

CFG = {
    # golden mahseer (Tor putitora): torpedo body, large scales, dark olive back, golden-bronze flanks, cream belly, orange-yellow fins
    'golden_mahseer': dict(length=0.90, stretch=(1.60, 0.78, 0.50), long_axis='Y', head_sign=-1, swim_z=0.35,
                           palette=dict(dark='#3A331C', mid='#B48C40', light='#ECDCA8', cap=1.6, gamma=0.95), fin_col='#D08A30',
                           rough=0.32, coat=0.35),
}


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, sid, out = a[0], a[1], a[2]; c = CFG[sid]
    K.clean(); bpy.ops.import_scene.gltf(filepath=src)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    root = next(o for o in bpy.data.objects if o.parent is None)
    # head direction: the thicker end of the body along the long axis = head (fish taper to the tail)
    P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in meshes])
    ax = 'XYZ'.index(c['long_axis']); mid = (P[:, ax].max() + P[:, ax].min()) / 2
    hz = lambda sgn: np.ptp(P[(P[:, ax] - mid) * sgn > 0.25 * np.ptp(P[:, ax]), 2]) if ((P[:, ax] - mid) * sgn > 0.25 * np.ptp(P[:, ax])).any() else 0
    head_sign = c.get('head_sign') or (1 if hz(1) > hz(-1) else -1)
    ang = {('Y', 1): -90, ('Y', -1): 90, ('X', 1): 0, ('X', -1): 180}[(c['long_axis'], head_sign)]
    root.matrix_world = Matrix.Rotation(math.radians(ang), 4, 'Z') @ root.matrix_world
    bpy.context.view_layer.update()
    for o in meshes:   # bake the transform + species stretch into the mesh (static base, no rig)
        o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4)
        o.data.transform(Matrix.Diagonal((*c['stretch'], 1)))
    for o in list(bpy.data.objects):
        if o.type == 'EMPTY':
            bpy.data.objects.remove(o)
    P = np.concatenate([np.array([v.co[:] for v in o.data.vertices]) for o in meshes])
    s = c['length'] / np.ptp(P[:, 0]); ctr = (P.max(0) + P.min(0)) / 2
    for o in meshes:
        o.data.transform(Matrix.Diagonal((s, s, s, 1)) @ Matrix.Translation(-Vector(ctr)))
        o.location.z = c.get('swim_z', 0.0)          # swimming above the river bed (preview), not lying on it
    tex = os.path.join(K.CR, '11_TEXTURES', sid); os.makedirs(tex, exist_ok=True)
    pal = c['palette']
    for m in bpy.data.materials:
        if not m.use_nodes or not m.node_tree.nodes.get('Principled BSDF'):
            continue
        b = m.node_tree.nodes['Principled BSDF']; L = b.inputs['Base Color'].links
        if L and L[0].from_node.type == 'TEX_IMAGE':
            img = L[0].from_node.image; srcp = os.path.join(tex, '_src.png'); img.filepath_raw = srcp; img.file_format = 'PNG'; img.save()
            dst = os.path.join(tex, f'T7_{sid.upper()}_diffuse_v002.png')
            CS.recolor(srcp, dst, pal['dark'], pal['mid'], pal['light'], pal['cap'], pal['gamma'])
            if c.get('fin_col'):                     # fins: caudal (back 12 %), dorsal / anal / pelvic (thin parts above / below the body) → orange-yellow
                for o in meshes:
                    Pm = np.array([v.co[:] for v in o.data.vertices]); Lx = np.ptp(Pm[:, 0]); x0 = Pm[:, 0].min()
                    zc = np.median(Pm[:, 2]); hz = np.percentile(np.abs(Pm[:, 2] - zc), 93)   # only the real fins stick out beyond ~93 %
                    w = np.clip(((x0 + 0.13 * Lx) - Pm[:, 0]) / (0.03 * Lx), 0, 1)
                    w = np.maximum(w, np.clip((np.abs(Pm[:, 2] - zc) - hz) / (0.12 * hz), 0, 1) * (np.abs(Pm[:, 1]) < 0.012))
                    CS.paint_uv(dst, o, w.astype(np.float32), c['fin_col'], 3)
            L[0].from_node.image = bpy.data.images.load(dst, check_existing=False); os.remove(srcp)
        for k in ('Metallic', 'Roughness'):
            for l in list(b.inputs[k].links):
                m.node_tree.links.remove(l)
        b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = c['rough']
        b.inputs['Specular IOR Level'].default_value = 0.5; b.inputs['Coat Weight'].default_value = c['coat']
        b.inputs['Coat Roughness'].default_value = 0.08
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=True)
    P = np.concatenate([np.array([v.co[:] for v in o.data.vertices]) for o in meshes])
    print('FISH SAVED', out, 'L x H x W', np.round(np.ptp(P, 0), 3))


main()

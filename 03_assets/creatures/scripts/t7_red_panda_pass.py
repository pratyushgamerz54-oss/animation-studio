"""t7_red_panda_pass — red panda (Ailurus fulgens) look pass on the rigged CC base, before t7_furpass:
1. no glow: emission inputs unlinked / strength 0 (the base ships emissive maps)
2. tail rings: alternating pale buff / dark rust rings along the tail (arc-length along the tail bone chain), photo refs 01-02
   (≈ 6 pale rings, soft edges, tip dark)

usage: $BPY45 t7_red_panda_pass.py <in.blend> <out.blend>
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7_cc_species as CS
import t7kit as K

RINGS, PALE, DARK = 6, '#DCA46C', '#4A1C0A'


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst = a[0], a[1]
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    for m in bpy.data.materials:
        b = m.node_tree.nodes.get('Principled BSDF') if m.use_nodes else None
        if b:
            for l in list(b.inputs['Emission Color'].links):
                m.node_tree.links.remove(l)
            b.inputs['Emission Strength'].default_value = 0.0
    arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    tb = sorted([bn for bn in arm.data.bones if 'Tile' in bn.name], key=lambda bn: bn.name)
    pts = [tb[0].head_local] + [bn.tail_local for bn in tb]          # tail polyline (armature rest space)
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; Ls = [(q - p).length for p, q in seg]; Lt = sum(Ls)
    body = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: max(o.dimensions))   # biggest = body (paw-pad plate has more verts)
    to_arm = arm.matrix_world.inverted() @ body.matrix_world
    tid = {g.index for g in body.vertex_groups if 'Tile' in g.name}
    tvec = np.zeros(len(body.data.vertices), np.float32); tw = np.zeros(len(body.data.vertices), np.float32)
    for v in body.data.vertices:
        w = sum(g.weight for g in v.groups if g.group in tid)
        if w < 0.2:
            continue
        p = to_arm @ v.co; best = (1e9, 0.0); acc = 0.0
        for (s0, s1), L in zip(seg, Ls):
            d = s1 - s0; t = max(0.0, min(1.0, (p - s0).dot(d) / max(d.length_squared, 1e-12)))
            dist = (s0 + d * t - p).length
            if dist < best[0]:
                best = (dist, (acc + t * L) / Lt)
            acc += L
        tvec[v.index] = best[1]; tw[v.index] = min(1.0, w)
    ph = np.cos(2 * np.pi * RINGS * tvec)                               # +1 = pale ring centre
    pale = np.clip((ph - 0.15) / 0.5, 0, 1) * tw * (tvec > 0.06) * (tvec < 0.93)
    dark = np.clip((-ph - 0.15) / 0.5, 0, 1) * tw * (tvec > 0.06)
    dark = np.maximum(dark, tw * np.clip((tvec - 0.90) / 0.05, 0, 1))  # dark tip
    tn = next(n for n in body.active_material.node_tree.nodes if n.type == 'TEX_IMAGE' and 'baseColor' in n.image.name)
    srcp = bpy.path.abspath(tn.image.filepath)
    td = os.path.join(K.CR, '11_TEXTURES', 'red_panda'); os.makedirs(td, exist_ok=True)
    dstp = os.path.join(td, 'T7_RED_PANDA_body_diffuse_v001.png')
    from PIL import Image
    Image.open(srcp).convert('RGB').save(dstp)
    CS.paint_uv(dstp, body, pale.astype(np.float32), PALE, 3); CS.paint_uv(dstp, body, dark.astype(np.float32), DARK, 3)
    img = bpy.data.images.load(dstp); img.colorspace_settings.name = 'sRGB'; tn.image = img
    print('RPANDA tail verts', int((tw > 0).sum()), 'pale', int((pale > 0.5).sum()), 'dark', int((dark > 0.5).sum()), flush=True)
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('RPANDA SAVED', dst, flush=True)


if __name__ == '__main__':
    main()

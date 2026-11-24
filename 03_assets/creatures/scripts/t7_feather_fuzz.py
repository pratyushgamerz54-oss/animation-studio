"""t7_feather_fuzz — anti-plastic pass for scanned birds (Director 24 Nov: "thoda plastic jaisa nhi lag rha hai"):
1. UNLIT scan materials (Emission + Light Path, lighting baked into the photo texture) → real lit material: Principled, matte feathers
   (rough .85, specular .18, soft sheen), so the bird takes the scene light / shadows like everything else
2. feather fuzz: a fine layer of barb strands (hair-Curves groom, colour sampled from the texture) that breaks the hard CG silhouette
   — owls are very soft / fluffy; lengths by height (face disc short, breast fluffy, back + wings sleek), combed downward
   perch / branch vertices get no fuzz (dull, unsaturated wood below the bird)

usage: $BPY45 t7_feather_fuzz.py <in.blend> <out.blend> [--len 0.006] [--density 350000] [--bird-min-frac 0.42]
       [--surface feathers|wet|chitin] [--no-fuzz]   (relight only: bullfrog = wet, dragonfly body = chitin)
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import t7kit as K

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, dst = a[0], a[1]; opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
LEN, DENS, BMIN = opt('--len', 0.006), opt('--density', 350000.0), opt('--bird-min-frac', 0.42)
# surface presets: feathers (matte), wet (amphibian skin), chitin (insect)
SURF = dict(feathers=dict(rough=0.85, spec=0.18, sheen=0.08, coat=0.0, coat_rough=0.3),
            wet=dict(rough=0.38, spec=0.4, sheen=0.0, coat=0.35, coat_rough=0.12),
            chitin=dict(rough=0.42, spec=0.35, sheen=0.0, coat=0.15, coat_rough=0.25))[opt('--surface', 'feathers')]
NOFUZZ = '--no-fuzz' in a


def relight(m):
    nt = m.node_tree; tex = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None)
    if nt.nodes.get('Principled BSDF') or tex is None:
        return False
    img = tex.image; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.name = 'Principled BSDF'
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = img
    hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = 1.15; hs.inputs['Value'].default_value = 0.80
    nt.links.new(t.outputs['Color'], hs.inputs['Color'])            # unlit scans carry baked light: lit render reads paler → compensate
    nt.links.new(hs.outputs['Color'], b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs['Surface'])
    b.inputs['Roughness'].default_value = SURF['rough']; b.inputs['Specular IOR Level'].default_value = SURF['spec']
    b.inputs['Sheen Weight'].default_value = SURF['sheen']; b.inputs['Sheen Roughness'].default_value = 0.6
    b.inputs['Coat Weight'].default_value = SURF['coat']; b.inputs['Coat Roughness'].default_value = SURF['coat_rough']
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.0008
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(t.outputs['Color'], bw.inputs[0]); nt.links.new(bw.outputs[0], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return True


def main():
    bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
    fixed = [m.name for m in bpy.data.materials if m.use_nodes and relight(m)]
    print('FUZZ relit (were unlit):', fixed, flush=True)
    if NOFUZZ:
        bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True); print('FUZZ SAVED (relight only)', dst, flush=True); return
    ob = max([o for o in bpy.data.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
    me = ob.data; P = np.array([(ob.matrix_world @ v.co)[:] for v in me.vertices]); H = P[:, 2].max()
    # per-vertex colour (linear) from each material's texture
    col = np.zeros((len(P), 3), np.float32); cnt = np.zeros(len(P), np.float32); uv = me.uv_layers.active.data
    pix = {}
    for mi, m in enumerate(me.materials):
        t = next((n for n in m.node_tree.nodes if n.type == 'TEX_IMAGE'), None)
        if t:
            img = t.image; w, h = img.size; buf = np.empty(w * h * img.channels, np.float32); img.pixels.foreach_get(buf)
            px = buf.reshape(h, w, img.channels)[..., :3]
            if img.colorspace_settings.name == 'sRGB' and not img.is_float:
                px = np.where(px <= 0.04045, px / 12.92, ((px + 0.055) / 1.055) ** 2.4)
            pix[mi] = px
    for poly in me.polygons:
        px = pix.get(poly.material_index)
        if px is None:
            continue
        h, w = px.shape[:2]
        for li in poly.loop_indices:
            u, v = uv[li].uv; vi = me.loops[li].vertex_index
            col[vi] += px[int(np.clip(v % 1, 0, .9999) * h), int(np.clip(u % 1, 0, .9999) * w)]; cnt[vi] += 1
    col /= np.maximum(cnt, 1)[:, None]
    srgb = np.where(col <= 0.0031308, col * 12.92, 1.055 * np.clip(col, 0, 1) ** (1 / 2.4) - 0.055)
    sat = (srgb.max(1) - srgb.min(1)) / np.maximum(srgb.max(1), 1e-3)
    zr = P[:, 2] / H
    bird = (zr > BMIN) | ((sat > 0.30) & (zr > 0.18))
    N = np.array([(ob.matrix_world.to_3x3() @ v.normal).normalized()[:] for v in me.vertices], np.float32)
    front = N[:, 0] > 0.15
    L = np.where(front, LEN * 1.25, LEN * 0.55).astype(np.float32)          # fluffy breast / belly, sleek back + wings
    L = np.where(zr > 0.82, np.where(front, LEN * 0.45, LEN * 0.6), L)      # short facial-disc / crown feathers
    dens = bird.astype(np.float32)
    comb = np.tile(np.array([0.0, 0.0, -1.0], np.float32), (len(P), 1)); comb[:, 0] = -0.25
    comb /= np.linalg.norm(comb, axis=1, keepdims=True)
    inv = ob.matrix_world.inverted().to_3x3()
    from mathutils import Vector
    comb = np.array([(inv @ Vector(c)).normalized()[:] for c in comb], np.float32)
    K.set_attr(ob, 'fur_len', L); K.set_attr(ob, 'fur_density', dens); K.set_attr(ob, 'comb', comb, 'FLOAT_VECTOR')
    K.put_coat(ob, np.clip(col * 0.85, 0, 1).astype(np.float32))
    hm = K.mat_attr(f'{ob.name}_FUZZ', attr='coat', rough=0.9, spec=0.15, bump=0.0)       # matte barbs (no hair-BSDF sheen)
    K.fur(ob, hm, density=DENS, radius=0.00009, lift=0.35, droop=0.45, frizz=0.55)
    print('FUZZ bird verts', int(bird.sum()), 'of', len(P), flush=True)
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('FUZZ SAVED', dst, os.path.getsize(dst) // 1024, 'KB', flush=True)


if __name__ == '__main__':
    main()

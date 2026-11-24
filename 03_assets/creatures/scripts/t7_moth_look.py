"""t7_moth_look — velvet-scale look for a painted moth base (atlas moth): deeper photo-matched colour (value / saturation grade),
matte velvet scales (rough .8, sheen), then t7_feather_fuzz adds a very short scale / hair fuzz (moth wings + body are fuzzy).
usage: $BPY45 t7_moth_look.py <in.blend> <out.blend> [--value 0.72] [--sat 1.3]
"""
import sys
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, dst = a[0], a[1]; opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
for m in bpy.data.materials:
    b = m.node_tree.nodes.get('Principled BSDF') if m.use_nodes else None
    t = next((n for n in m.node_tree.nodes if n.type == 'TEX_IMAGE'), None) if m.use_nodes else None
    if not (b and t):
        continue
    nt = m.node_tree
    for l in list(b.inputs['Base Color'].links):
        nt.links.remove(l)
    hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = opt('--sat', 1.3); hs.inputs['Value'].default_value = opt('--value', 0.72)
    nt.links.new(t.outputs['Color'], hs.inputs['Color']); nt.links.new(hs.outputs['Color'], b.inputs['Base Color'])
    for k in ('Metallic', 'Roughness'):
        for l in list(b.inputs[k].links):
            nt.links.remove(l)
    b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.8; b.inputs['Specular IOR Level'].default_value = 0.2
    b.inputs['Sheen Weight'].default_value = 0.35; b.inputs['Sheen Roughness'].default_value = 0.4
    if 'Alpha' in b.inputs and t.outputs.get('Alpha'):
        nt.links.new(t.outputs['Alpha'], b.inputs['Alpha'])
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True); print('MOTH LOOK SAVED', dst)

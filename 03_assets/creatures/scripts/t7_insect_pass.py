"""t7_insect_pass — after t7_scan_reduce on a CC0 insect specimen model: drop helper objects (scale cubes), real wing membranes
(alpha from the wing texture, thin glossy film with faint iridescence-free sheen, light transmission), chitin body (low-sheen,
not plastic), save.

usage: $BPY45 t7_insect_pass.py <in.blend> <out.blend> <wing_material> [--delete Cube_0,...]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, dst, wing = a[0], a[1], a[2]
dele = a[a.index('--delete') + 1].split(',') if '--delete' in a else []
bpy.ops.wm.open_mainfile(filepath=src); bpy.context.preferences.filepaths.save_version = 0
for o in list(bpy.data.objects):
    if o.name in dele or o.name.split('.')[0] in dele or (o.type == 'MESH' and any(o.name.startswith(d) for d in dele)):
        bpy.data.objects.remove(o)
for m in bpy.data.materials:
    if m.name == wing and m.use_nodes and not m.node_tree.nodes.get('Principled BSDF'):   # glTF wing set up without Principled → rebuild
        nt = m.node_tree; tex0 = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None); img0 = tex0.image if tex0 else None
        nt.nodes.clear(); o_ = nt.nodes.new('ShaderNodeOutputMaterial'); b_ = nt.nodes.new('ShaderNodeBsdfPrincipled'); b_.name = 'Principled BSDF'
        nt.links.new(b_.outputs[0], o_.inputs['Surface'])
        if img0:
            t_ = nt.nodes.new('ShaderNodeTexImage'); t_.image = img0; nt.links.new(t_.outputs['Color'], b_.inputs['Base Color'])
    if not m.use_nodes or not m.node_tree.nodes.get('Principled BSDF'):
        continue
    b = m.node_tree.nodes['Principled BSDF']; L = m.node_tree.links
    if m.name == wing:
        tex = next((n for n in m.node_tree.nodes if n.type == 'TEX_IMAGE'), None)
        if tex:                                          # membrane = clear, veins = opaque: alpha from texture brightness
            for l in list(b.inputs['Alpha'].links) + list(b.inputs['Base Color'].links):
                L.remove(l)
            nt = m.node_tree; bw = nt.nodes.new('ShaderNodeRGBToBW'); L.new(tex.outputs['Color'], bw.inputs[0])
            mr = nt.nodes.new('ShaderNodeMapRange'); L.new(bw.outputs[0], mr.inputs['Value'])
            mr.inputs['From Min'].default_value = 0.12; mr.inputs['From Max'].default_value = 0.30
            mr.inputs['To Min'].default_value = 0.95; mr.inputs['To Max'].default_value = 0.06
            L.new(mr.outputs['Result'], b.inputs['Alpha'])
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
            L.new(tex.outputs['Color'], mx.inputs['A']); mx.inputs['B'].default_value = (0.55, 0.42, 0.25, 1)   # darker veins, faint amber
            L.new(mx.outputs['Result'], b.inputs['Base Color'])
        m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
        b.inputs['Roughness'].default_value = 0.12; b.inputs['Specular IOR Level'].default_value = 0.5
        b.inputs['Transmission Weight'].default_value = 0.0; b.inputs['IOR'].default_value = 1.4
        b.inputs['Coat Weight'].default_value = 0.3; b.inputs['Coat Roughness'].default_value = 0.05
        b.inputs['Thin Film Thickness'].default_value = 380.0 if 'Thin Film Thickness' in b.inputs else 0
    else:
        b.inputs['Roughness'].default_value = 0.42; b.inputs['Specular IOR Level'].default_value = 0.35
        b.inputs['Coat Weight'].default_value = 0.15; b.inputs['Coat Roughness'].default_value = 0.25
bpy.context.scene.cycles.transparent_max_bounces = 64
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
print('INSECT SAVED', dst, os.path.getsize(dst) // 1024, 'KB')

"""t7_water_preview — preview a creature AT A WATER SURFACE (floating frog, swimming duck / otter / turtle): murky pond water
(reflective surface, brown-green absorption volume so the submerged parts fade like real pond water, fine wind ripples), daylight HDRI.

usage: $BPY45 t7_water_preview.py <in.blend> <out_dir> --water-z 0.04 [--samples 64] [--dist 0.35]
(murky = tan silt colour + partial transmission; clear lake water would use transmission 1 + light absorption)
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, bmesh
import numpy as np
from mathutils import Vector
import t7kit as K
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, out = a[0], a[1]
opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
wz, spp, dist = opt('--water-z', 0.04), opt('--samples', 64), opt('--dist', 0.35)
bpy.ops.wm.open_mainfile(filepath=src)
for o in list(bpy.data.objects):
    if o.type in ('CAMERA', 'LIGHT'):
        bpy.data.objects.remove(o)
sc = K.studio(size=(1600, 1000), samples=spp, sun=(40, 0, 150))
g = bpy.data.objects.get('T7_GROUND'); g.location.z = wz - 0.35          # pond bed far below
P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in bpy.data.objects
                    if o.type == 'MESH' and o.name != 'T7_GROUND' and o.visible_get()])
ctr = Vector(((P[:, 0].max() + P[:, 0].min()) / 2, (P[:, 1].max() + P[:, 1].min()) / 2, wz))
# water: surface + absorbing volume (a thick slab)
bm_ = bmesh.new(); bmesh.ops.create_cube(bm_, size=1.0); me = bpy.data.meshes.new('T7_WATER'); bm_.to_mesh(me); bm_.free()
w = bpy.data.objects.new('T7_WATER', me); K.link(w); w.scale = (40, 40, 0.34); w.location = (ctr.x, ctr.y, wz - 0.17)
m = K.new_mat('T7_POND_WATER'); nt = m.node_tree; b = nt.nodes['Principled BSDF']; L = nt.links
b.inputs['Base Color'].default_value = (0.20, 0.155, 0.09, 1); b.inputs['Roughness'].default_value = 0.10   # silty pond water (tan-brown, photo 04)
b.inputs['IOR'].default_value = 1.333; b.inputs['Transmission Weight'].default_value = 0.25
ab = nt.nodes.new('ShaderNodeVolumeAbsorption'); ab.inputs['Color'].default_value = (0.55, 0.45, 0.25, 1); ab.inputs['Density'].default_value = 45
L.new(ab.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60; nz.inputs['Detail'].default_value = 4
L.new(tc.outputs['Object'], nz.inputs['Vector']); bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.04
L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
me.materials.append(m)
os.makedirs(out, exist_ok=True)
for name, az, el in (('water_34', 35, 9), ('water_side', 90, 6), ('water_high', 20, 32)):
    d = Vector((math.cos(math.radians(az)) * math.cos(math.radians(el)), -math.sin(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(el))))
    cam = K.camera('CAM_' + name, ctr + d * dist, ctr + Vector((0, 0, 0.005)), lens=70)
    sc.camera = cam; sc.render.filepath = os.path.join(out, name + '.png'); bpy.ops.render.render(write_still=True)
    print('WATER', name, flush=True)

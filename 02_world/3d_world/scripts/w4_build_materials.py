"""TASK 04 · materials library → 11_MATERIALS/WORLD_materials_v001.blend (Blender 4.5).

All materials are procedural (no image textures → no missing files, resolution-independent). Every other .blend LINKS
these materials, so a change here updates the whole world. Use fake users so the library keeps them.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import worldkit as wk


def hexlin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c) + (1.0,)


def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (900, 0)
    return m, nt, out


def principled(nt, color=None, rough=.8, spec=.5):
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (600, 0)
    if color:
        b.inputs['Base Color'].default_value = hexlin(color)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    return b


def simple(name, color, rough=.8, emit=0.0, spec=.5, metal=0.0):
    m, nt, out = mat(name)
    b = principled(nt, color, rough, spec)
    b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = hexlin(color); b.inputs['Emission Strength'].default_value = emit
    nt.links.new(b.outputs[0], out.inputs['Surface'])
    return m


def attr(nt, name, loc=(0, 0)):
    a = nt.nodes.new('ShaderNodeAttribute'); a.attribute_name = name; a.location = loc
    return a


def mix(nt, a, b, fac, loc=(0, 0)):
    m = nt.nodes.new('ShaderNodeMix'); m.data_type = 'RGBA'; m.location = loc
    nt.links.new(fac, m.inputs['Factor'])
    for sock, v in (('A', a), ('B', b)):
        if isinstance(v, str):
            m.inputs[sock].default_value = hexlin(v)
        else:
            nt.links.new(v, m.inputs[sock])
    return m.outputs['Result']


def sep(nt, col_out, loc=(0, 0)):
    s = nt.nodes.new('ShaderNodeSeparateColor'); s.location = loc
    nt.links.new(col_out, s.inputs['Color'])
    return s


def stretch(nt, sock, a=.38, b=.62):
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = a; mr.inputs['From Max'].default_value = b
    nt.links.new(sock, mr.inputs['Value'])
    return mr.outputs['Result']


def noise(nt, scale, detail=4, loc=(0, 0), coord='Object'):
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (loc[0] - 200, loc[1])
    n = nt.nodes.new('ShaderNodeTexNoise'); n.location = loc
    n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
    nt.links.new(tc.outputs[coord], n.inputs['Vector'])
    return n


wk.new_file()

# ======================================================= MASTER WORLD (1 BU = 1 km, exaggerated relief)
m, nt, out = mat('MAT_W_TERRAIN')
a = attr(nt, 'biome_col', (0, 0))
n = noise(nt, 0.02, 6, (0, -250))
v = mix(nt, a.outputs['Color'], '#6B6352', n.outputs['Fac'], (300, 0))            # subtle large-scale tonal variation
mm = nt.nodes.get(v.node.name); mm.inputs['Factor'].default_value = 0
mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (150, -250)
mr.inputs['From Min'].default_value = .35; mr.inputs['From Max'].default_value = .75; mr.inputs['To Max'].default_value = .18
nt.links.new(n.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], mm.inputs['Factor'])
b = principled(nt, None, .93, .3)
nt.links.new(v, b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs['Surface'])

m, nt, out = mat('MAT_W_OCEAN')
a = attr(nt, 'ocean_col', (0, 0))
s = sep(nt, a.outputs['Color'], (150, 0))
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.location = (300, 0)
cr.color_ramp.elements[0].color = hexlin('#357F8A'); cr.color_ramp.elements[0].position = 0.0
cr.color_ramp.elements[1].color = hexlin('#0B2544'); cr.color_ramp.elements[1].position = .30
e = cr.color_ramp.elements.new(.05); e.color = hexlin('#1A587A')
e = cr.color_ramp.elements.new(.12); e.color = hexlin('#123C60')
nt.links.new(s.outputs['Red'], cr.inputs['Fac'])
b = principled(nt, None, .12, .6)
nt.links.new(cr.outputs['Color'], b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs['Surface'])

simple('MAT_W_LAKE', '#2D6E8A', .06, spec=.6)
simple('MAT_W_RIVER', '#3D86B8', .1, emit=.05, spec=.6)
simple('MAT_W_WATERFALL', '#DDF2FF', .3, emit=.6)
for nm, c, em in (('ASHRAM', '#FFD45A', 4), ('CITY', '#FF8C3A', 2.5), ('TOWN', '#F2C27A', 2), ('VILLAGE', '#FFF1D0', 1.5),
                  ('REMOTE', '#D9D2C0', 1.2), ('RUIN', '#C49A72', 1.5), ('CAVE', '#9A6BFF', 2), ('FALL', '#7FD8FF', 2.5),
                  ('HIDDEN', '#FF3AD0', 3), ('GEM', '#5AFFC8', 3.5), ('UNDERGROUND', '#FF5040', 1.5), ('LABEL', '#FFF6E0', 2),
                  ('PROPOSAL_EDGE', '#FF5AA0', 2.5), ('UNEXPLORED', '#B9C6FF', 1.0), ('RANGE', '#E8E2D6', 1.2)):
    simple(f'MAT_W_MARK_{nm}', c, .5, emit=em)

# ======================================================= ASHRAM VALLEY (1 BU = 1 m, true scale)
m, nt, out = mat('MAT_V_TERRAIN')
ma = sep(nt, attr(nt, 'mask_a', (-600, 300)).outputs['Color'], (-400, 300))        # R forest, G rock, B snow
mb = sep(nt, attr(nt, 'mask_b', (-600, -300)).outputs['Color'], (-400, -300))      # R wet, G dry, B pad
n1 = noise(nt, .0012, 5, (-600, 0)); n2 = noise(nt, .03, 3, (-600, -150))
g = mix(nt, '#46692A', '#86924A', stretch(nt, n1.outputs['Fac'], .3, .7), (-200, 100))   # grass meadow variation (≈800 m)
g = mix(nt, g, '#557A2E', stretch(nt, n2.outputs['Fac'], .45, .7), (-50, 100))
g = mix(nt, g, '#A39563', mb.outputs['Green'], (100, 100))                        # dry grass / scrub
g = mix(nt, g, '#2E4426', ma.outputs['Red'], (250, 100))                          # forest floor
n3 = noise(nt, .4, 3, (-600, -450))
g = mix(nt, g, '#3E5E25', stretch(nt, n3.outputs['Fac'], .5, .75), (40, 0))       # fine ground breakup (≈3 m)
rk = mix(nt, '#6E6963', '#8C857C', n2.outputs['Fac'], (100, -100))
g = mix(nt, g, rk, ma.outputs['Green'], (400, 100))                               # rock
g = mix(nt, g, '#4A4436', mb.outputs['Red'], (550, 100))                          # wet banks / riverbed
g = mix(nt, g, '#9C8C6C', mb.outputs['Blue'], (700, 100))                         # compacted Ashram pad
g = mix(nt, g, '#EDF1F5', ma.outputs['Blue'], (850, 100))                         # snow
b = principled(nt, None, .9, .3); b.location = (1000, 0); out.location = (1250, 0)
nt.links.new(g, b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs['Surface'])

m, nt, out = mat('MAT_V_RIVER')
b = principled(nt, '#244E5C', .04, .7)
lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.location = (300, -200)
nt.links.new(b.outputs[0], out.inputs['Surface'])

simple('MAT_V_PATH', '#8C7656', .95, spec=.2)
simple('MAT_V_SKIRT', '#4E4636', .95, spec=.2)
for nm, c in (('CONIFER', '#1E3A23'), ('BROADLEAF', '#2F5729'), ('CANOPY', '#25442B')):
    m, nt, out = mat(f'MAT_V_TREE_{nm}')
    oi = nt.nodes.new('ShaderNodeObjectInfo'); oi.location = (0, 0)
    v = mix(nt, c, '#3E5A2A', oi.outputs['Random'], (300, 0))
    mm = v.node
    mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'MULTIPLY'; mr.inputs[1].default_value = .45; mr.location = (150, -150)
    nt.links.new(oi.outputs['Random'], mr.inputs[0]); nt.links.new(mr.outputs[0], mm.inputs['Factor'])
    b = principled(nt, None, .85, .3)
    nt.links.new(v, b.inputs['Base Color']); nt.links.new(b.outputs[0], out.inputs['Surface'])
simple('MAT_V_TRUNK', '#4A3A2A', .9, spec=.2)

m, nt, out = mat('MAT_V_HAZE')
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.location = (500, 0)
pv.inputs['Color'].default_value = hexlin('#C8D6E8'); pv.inputs['Density'].default_value = 4.5e-6
pv.inputs['Anisotropy'].default_value = .5
nt.links.new(pv.outputs[0], out.inputs['Volume'])

m, nt, out = mat('MAT_V_ASHRAM_REF')                                     # placement reference (not the building)
em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexlin('#FFD45A'); em.inputs['Strength'].default_value = 3
nt.links.new(em.outputs[0], out.inputs['Surface'])
simple('MAT_V_MARK_PROPOSED', '#FF5AA0', .5, emit=3)

# ======================================================= DIMENSIONS
simple('MAT_D_HORIZON', '#000000', 1.0, spec=0)
m, nt, out = mat('MAT_D_ACCRETION')
tc = nt.nodes.new('ShaderNodeTexCoord')
vl = nt.nodes.new('ShaderNodeVectorMath'); vl.operation = 'LENGTH'
nt.links.new(tc.outputs['Object'], vl.inputs[0])
mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 200; mr.inputs['From Max'].default_value = 480
nt.links.new(vl.outputs['Value'], mr.inputs['Value'])
cr = nt.nodes.new('ShaderNodeValToRGB')
cr.color_ramp.elements[0].color = hexlin('#FFF2D0'); cr.color_ramp.elements[1].color = (0.25, 0.03, 0.0, 1)
e = cr.color_ramp.elements.new(.35); e.color = hexlin('#FF9A3C')
nt.links.new(mr.outputs['Result'], cr.inputs['Fac'])
n = noise(nt, .02, 6, (0, -300))
mt = nt.nodes.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = 9.0
nt.links.new(n.outputs['Fac'], mt.inputs[0])
em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(cr.outputs['Color'], em.inputs['Color']); nt.links.new(mt.outputs[0], em.inputs['Strength'])
nt.links.new(em.outputs[0], out.inputs['Surface'])
simple('MAT_D_PHOTON_RING', '#FFE2B0', .5, emit=12)
simple('MAT_D_LENSING_HALO', '#4A6BFF', .5, emit=1.5)
simple('MAT_D_PLATFORM_ROCK', '#6C645C', .9, spec=.3)
simple('MAT_D_PLATFORM_TOP', '#8A8076', .85, spec=.3)
simple('MAT_D_OBSIDIAN', '#120C18', .12, spec=.8)

m, nt, out = mat('MAT_D_ASH_GROUND')
f = attr(nt, 'fissure', (-600, 200)); c_ = attr(nt, 'corrupt', (-600, -200))
n = noise(nt, .004, 5, (-600, 0))
g = mix(nt, '#2A2230', '#3B3140', n.outputs['Fac'], (-200, 0))
b = principled(nt, None, .95, .2)
nt.links.new(g, b.inputs['Base Color'])
ad = nt.nodes.new('ShaderNodeMath'); ad.operation = 'ADD'; ad.location = (0, -200)
nt.links.new(f.outputs['Fac'], ad.inputs[0]); nt.links.new(c_.outputs['Fac'], ad.inputs[1])
pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 5.0; pw.location = (150, -200)
nt.links.new(ad.outputs[0], pw.inputs[0])
mt = nt.nodes.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = 9.0; mt.location = (300, -200)
nt.links.new(pw.outputs[0], mt.inputs[0])
b.inputs['Emission Color'].default_value = hexlin('#FF2A2A')
nt.links.new(mt.outputs[0], b.inputs['Emission Strength'])
nt.links.new(b.outputs[0], out.inputs['Surface'])
simple('MAT_D_PORTAL_SITE', '#2A1E2E', .7, spec=.3)
simple('MAT_D_PORTAL_RIM', '#FF2A2A', .5, emit=6)
m, nt, out = mat('MAT_D_FOG')
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Color'].default_value = hexlin('#2A1630'); pv.inputs['Density'].default_value = 1.5e-4
nt.links.new(pv.outputs[0], out.inputs['Volume'])

wk.save(wk.MATLIB)
print('MATERIALS', len(bpy.data.materials), sorted(m.name for m in bpy.data.materials))
print('BUILD_MATERIALS_DONE')

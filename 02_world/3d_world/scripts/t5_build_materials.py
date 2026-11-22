"""TASK 05 · PBR TERRAIN MATERIAL LIBRARY → 11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend (Blender 4.5 LTS).

Reusable materials, every one built from Poly Haven CC0 2K scans (Base Color · Roughness · Normal (GL) · Displacement, AO where
useful) through shared node groups NG_PBR_<texture> (inputs: Vector, Scale m/tile, Wet, Tint, Normal Strength):
  MAT_T5_GRASS · MAT_T5_GRASS_DRY · MAT_T5_SOIL · MAT_T5_FOREST_FLOOR · MAT_T5_MUD · MAT_T5_GRAVEL · MAT_T5_ROCK ·
  MAT_T5_CLIFF · MAT_T5_SCREE · MAT_T5_SNOW · MAT_T5_ICE (procedural) · MAT_T5_SAND · MAT_T5_WET_STONE
Terrain:  MAT_T5_TERRAIN — one shader for every tile; reads the mask attributes written by NG_T5_HEIGHTFIELD
          (m_forest, m_rock, m_snow, m_wet, m_dry, m_pad, m_grove, m_scree, m_gravel, m_path, m_flow, m_cliff)
          + true slope/altitude, height-blended layer transitions, distance-dependent texture scale (no tiling from the air).
Water:    MAT_T5_WATER_RIVER · MAT_T5_WATER_LAKE · MAT_T5_WATERFALL · MAT_T5_MIST (volume) · MAT_T5_FOAM
Air/far:  MAT_T5_HAZE (height-falloff aerial perspective volume) · MAT_T5_TREE_FAR (far-forest proxy canopy)
Metallic = 0 for all natural surfaces (dielectric). Displacement: height maps drive bump + layer blending; library
materials also carry a true-displacement output (material.displacement_method = 'BOTH') for close-up props.
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk
import t5kit as tk
from t5kit import NB, lin

LAKE_LEVEL = 735.76        # map lake at the SW edge of the valley window (prep_v002.json) — sand shore band
SPEC = {}                  # material → texture resolution spec (written to MATERIAL_LIBRARY.md by the docs step)


def newmat(name):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    b = NB(nt)
    out = b.node('ShaderNodeOutputMaterial'); bs = b.node('ShaderNodeBsdfPrincipled')
    b.link(bs.outputs[0], out.inputs['Surface'])
    m.use_fake_user = True
    return m, b, bs, out


def disp_both(m):
    for o in (m, getattr(m, 'cycles', None)):
        try:
            o.displacement_method = 'BOTH'; return
        except Exception:
            pass


def coords(b, kind='Object'):
    tc = b.node('ShaderNodeTexCoord')
    return tc.outputs[kind]


def use_group(b, tex, vec, scale, box=False, antitile=False, ao=False, wet=None, tint=None, nstr=1.0):
    g = b.group(tk.pbr_group(tex, box, antitile, ao))
    b.link(vec, g.inputs['Vector']); g.inputs['Scale'].default_value = scale; g.inputs['Normal Strength'].default_value = nstr
    if wet is not None:
        b.link(wet, g.inputs['Wet']) if not isinstance(wet, (int, float)) else setattr(g.inputs['Wet'], 'default_value', wet)
    if tint is not None:
        g.inputs['Tint'].default_value = lin(tint) if isinstance(tint, str) else tint
    return g


def simple_pbr(name, tex, scale, box=False, tint=None, wet=0.0, antitile=True, ao=True, spec_note=''):
    m, b, bs, out = newmat(name)
    g = use_group(b, tex, coords(b), scale, box, antitile, ao, wet, tint)
    b.link(g.outputs['Color'], bs.inputs['Base Color']); b.link(g.outputs['Roughness'], bs.inputs['Roughness'])
    b.link(g.outputs['Normal'], bs.inputs['Normal']); bs.inputs['Metallic'].default_value = 0.0
    bs.inputs['Specular IOR Level'].default_value = .3                         # realism pass: natural ground, no sheen
    dp = b.node('ShaderNodeDisplacement'); dp.inputs['Scale'].default_value = .04 * scale; dp.inputs['Midlevel'].default_value = .5
    b.link(g.outputs['Height'], dp.inputs['Height']); b.link(dp.outputs[0], out.inputs['Displacement'])
    disp_both(m)
    SPEC[name] = dict(source=f'Poly Haven {tex} (CC0)', maps='Base Color, Roughness, Normal GL, Displacement' + (', AO' if ao else ''),
                      resolution='2048 x 2048 (2K)', tile_m=scale, texel_density_px_per_m=round(2048 / scale, 1),
                      projection='box/triplanar' if box else 'top-down (object XY)', metallic=0.0, note=spec_note)
    return m


# =========================================================================== library
wk.new_file()
sc = bpy.context.scene; sc.name = 'T5_MATERIAL_LIBRARY'
L = {}
L['GRASS'] = simple_pbr('MAT_T5_GRASS', 'leafy_grass', 2.2, tint='#C8D8A8', spec_note='lush valley grass (tinted greener)')
L['GRASS_DRY'] = simple_pbr('MAT_T5_GRASS_DRY', 'sparse_grass', 3.0, tint='#E8DCB0', spec_note='dry / sparse grass patches')
L['SOIL'] = simple_pbr('MAT_T5_SOIL', 'dry_ground_01', 2.5, spec_note='compacted earth: paths, Ashram pad')
L['FOREST_FLOOR'] = simple_pbr('MAT_T5_FOREST_FLOOR', 'forest_floor', 3.0, spec_note='needles, leaves, twigs')
L['MUD'] = simple_pbr('MAT_T5_MUD', 'mud_forest', 2.5, wet=.35, spec_note='river-bank mud')
L['GRAVEL'] = simple_pbr('MAT_T5_GRAVEL', 'rocky_gravel', 2.0, spec_note='gravel / scree fines')
L['ROCK'] = simple_pbr('MAT_T5_ROCK', 'rock_ground', 4.0, box=True, spec_note='rocky ground, outcrops')
L['CLIFF'] = simple_pbr('MAT_T5_CLIFF', 'cliff_side', 12.0, box=True, ao=True, tint='#B8B4AE', spec_note='cliff faces (triplanar)')
L['SCREE'] = simple_pbr('MAT_T5_SCREE', 'gravel_ground_01', 3.0, spec_note='talus aprons below cliffs')
L['SNOW'] = simple_pbr('MAT_T5_SNOW', 'snow_02', 4.0, spec_note='fresh snow')
L['SAND'] = simple_pbr('MAT_T5_SAND', 'coast_sand_01', 3.0, spec_note='lake / river sand')
L['WET_STONE'] = simple_pbr('MAT_T5_WET_STONE', 'river_small_rocks', 1.6, wet=.85, spec_note='river-bed stones, wet (Wet input = 0..1)')
L['DARK_ROCK'] = simple_pbr('MAT_T5_ROCK_DARK', 'dark_rock', 5.0, box=True, spec_note='dark high-mountain rock')

# ICE — procedural (no CC0 ice scan available): glossy blue-white, subsurface, cracked normal
m, b, bs, out = newmat('MAT_T5_ICE')
v = coords(b)
vor = b.node('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); vor.inputs['Scale'].default_value = .35; b.link(v, vor.inputs['Vector'])
crack = b.maprange(vor.outputs['Distance'], 0.0, .04, 1.0, 0.0)
n1 = b.noise(v, .08, 6, .6)
col = b.mixc(b.math('MULTIPLY', n1, .6), lin('#BFD8E8'), lin('#86B4D0'))
col = b.mixc(b.math('MULTIPLY', crack, .5), col, lin('#F2F8FC'))
b.link(col, bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = .3     # weathered glacier ice (realism pass)
bs.inputs['Subsurface Weight'].default_value = .4; bs.inputs['Subsurface Radius'].default_value = (.6, .9, 1.4)
bs.inputs['Coat Weight'].default_value = .08
bp = b.node('ShaderNodeBump'); bp.inputs['Strength'].default_value = .35
b.link(b.math('ADD', crack, b.math('MULTIPLY', n1, .3)), bp.inputs['Height']); b.link(bp.outputs[0], bs.inputs['Normal'])
SPEC['MAT_T5_ICE'] = dict(source='procedural (voronoi cracks + noise)', maps='Base Color, Roughness 0.3 (weathered), Subsurface, bump normal',
                          resolution='procedural (resolution-independent)', metallic=0.0)
L['ICE'] = m


# =========================================================================== the terrain shader
def terrain_material():
    m, b, bs, out = newmat('MAT_T5_TERRAIN')
    v = coords(b)
    A = {k: b.attr(k) for k in ('m_forest', 'm_rock', 'm_snow', 'm_wet', 'm_dry', 'm_pad', 'm_grove', 'm_scree', 'm_gravel',
                               'm_path', 'm_flow', 'm_cliff')}
    cam = b.node('ShaderNodeCameraData'); dist = cam.outputs['View Distance']
    geo = b.node('ShaderNodeNewGeometry')
    nz = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Normal'], nz.inputs[0]); nz = nz.outputs['Z']
    pz = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Position'], pz.inputs[0])
    px, zpos = pz.outputs['X'], pz.outputs['Z']
    macro = b.noise(v, 1 / 900.0, 4, .55)               # large patches (colour variation, breaks up layer edges)
    meso = b.noise(v, 1 / 60.0, 4, .6)
    far = b.maprange(dist, 150, 900)                     # near → far texture set

    def L_(tex, scale, box=False, at=False, wet=None, tint=None, nstr=1.0):
        g = use_group(b, tex, v, scale, box, at, False, wet, tint, nstr)
        return [g.outputs['Color'], g.outputs['Roughness'], g.outputs['Normal'], g.outputs['Height']]

    def recolor(col, sat, val):
        h = b.node('ShaderNodeHueSaturation'); h.inputs['Saturation'].default_value = sat; h.inputs['Value'].default_value = val
        b.link(col, h.inputs['Color'])
        return h.outputs['Color']

    def lerp_layer(f, a, c):
        return [b.mixc(f, a[0], c[0]), b.mixf(f, a[1], c[1]), b.mixv(f, a[2], c[2]), b.mixf(f, a[3], c[3])]

    def hblend(base, lay, mask, k=.35):
        """height-aware blend: where `mask` is ~0.5 the layer with the higher height map wins (pebbles over sand, …)."""
        val = b.math('ADD', b.math('MULTIPLY', mask, 1.3), b.math('MULTIPLY', b.math('SUBTRACT', lay[3], base[3]), k))
        f = b.maprange(b.math('SUBTRACT', val, .15), .4, .6)
        return lerp_layer(f, base, lay), f

    # --- grass (near: 2 scans, macro mixed; far: aerial grass/rock scan) + hue/value variation
    gA = L_('leafy_grass', 2.2, at=True, tint='#C6D9A0')
    gB = L_('grass_ground', 2.9, tint='#D4E0B0')
    g = lerp_layer(b.maprange(macro, .42, .6), gA, gB)
    gf = L_('aerial_grass_rock', 55.0, at=True, tint='#B8CC90')
    g = lerp_layer(far, g, gf)
    # the CC0 grass scans are dry / brownish → keep their luminance detail, re-colour to the approved lush valley green
    bw = b.node('ShaderNodeRGBToBW'); b.link(g[0], bw.inputs[0])
    rmp = b.node('ShaderNodeValToRGB'); b.link(b.math('MULTIPLY', bw.outputs[0], 1.6), rmp.inputs['Fac'])
    el = rmp.color_ramp.elements
    el[0].position = 0.0; el[0].color = lin('#1C3410'); el[1].position = .75; el[1].color = lin('#86A64A')
    e2 = el.new(.38); e2.color = lin('#45692A')
    g[0] = b.mixc(.4, rmp.outputs['Color'], g[0])
    hsv = b.node('ShaderNodeHueSaturation'); b.link(g[0], hsv.inputs['Color'])
    b.link(b.maprange(macro, .3, .7, .485, .52), hsv.inputs['Hue']); b.link(b.maprange(meso, .3, .7, .72, 1.15), hsv.inputs['Value'])
    g[0] = hsv.outputs['Color']
    base = g
    # --- dry grass
    dry = L_('sparse_grass', 3.0, tint='#E6D7A8')
    base, _ = hblend(base, dry, b.math('ADD', A['m_dry'], b.math('MULTIPLY', b.maprange(meso, .62, .8), .5)))
    # --- groves / forest floor (needles + leaves under trees); far away → canopy colour (trees not instanced there)
    ff = L_('forest_floor', 3.0)
    ff[0] = b.mixc(1.0, recolor(ff[0], .5, .42), lin('#B08A62'), 'MULTIPLY')   # darker needle litter                                  # conifer needle litter, not autumn leaves
    fmask = b.math('MAXIMUM', A['m_forest'], b.math('MULTIPLY', A['m_grove'], .45))
    base, _ = hblend(base, ff, fmask)
    canopy = [b.mixc(b.noise(v, 1 / 35.0, 5, .65), lin('#1E3318'), lin('#2F4A22')), .85, base[2], .5]
    cf = b.math('MULTIPLY', A['m_forest'], b.maprange(dist, 2500, 6000))
    base = lerp_layer(cf, base, canopy)
    # --- path / Ashram pad: compacted earth
    soil = L_('dry_ground_01', 2.5)
    flat_ok = b.maprange(nz, .55, .78)                                # top-down projected layers only on gentle ground
    base, _ = hblend(base, soil, b.math('MULTIPLY', b.math('MAXIMUM', A['m_path'], A['m_pad']), flat_ok))
    # --- river banks: mud, then gravel bars + river bed (wet stones)
    mud = L_('mud_forest', 2.5, wet=b.math('MULTIPLY', A['m_wet'], .6))
    base, _ = hblend(base, mud, b.math('MULTIPLY', b.math('MULTIPLY', A['m_wet'], .85), flat_ok))
    bed = b.maprange(A['m_wet'], .9, 1.0)
    gv = L_('river_small_rocks', 1.6, wet=b.maprange(A['m_wet'], .5, 1.0))
    base, _ = hblend(base, gv, b.math('MULTIPLY', b.math('MAXIMUM', A['m_gravel'], bed), flat_ok), .5)
    # --- lake shore sand (map lake, SW of the valley window)
    sand = L_('coast_sand_01', 3.0)
    sf = b.math('MULTIPLY', b.maprange(zpos, LAKE_LEVEL + 7, LAKE_LEVEL + 1.5), b.maprange(px, -128000, -132000))
    base, _ = hblend(base, sand, sf)
    # --- scree, rock, cliff (slope from the real geometry normal + masks)
    scr = L_('rocky_gravel', 3.0)
    scr[0] = recolor(scr[0], .35, .9)
    base, _ = hblend(base, scr, b.math('MULTIPLY', A['m_scree'], flat_ok))
    rk = L_('rock_ground', 4.0, box=True)
    # far rock (> 0.4–2 km): no image texture (2K scans alias into a moiré grid from km away) → noise-based rock colour
    rfar = [b.mixc(b.maprange(b.noise(v, 1 / 18.0, 5, .62), .3, .7), lin('#5E5A55'), lin('#8E8A84')), .8, rk[2], .5]
    rfar[0] = b.mixc(b.maprange(macro, .4, .65), rfar[0], lin('#4A4642'))
    rk = lerp_layer(b.maprange(dist, 400, 2000), rk, rfar)
    rockmask = b.math('MAXIMUM', A['m_rock'], b.maprange(b.math('ADD', nz, b.math('MULTIPLY', meso, .08)), .80, .66))
    base, _ = hblend(base, rk, rockmask)
    cl = L_('dark_rock', 7.0, box=True, at=True)                     # isotropic scan (cliff_side's strata cross-hatch in triplanar)
    cl[0] = recolor(cl[0], .5, 1.9)                                   # grey granite / gneiss
    cl = lerp_layer(b.maprange(dist, 400, 2000), cl, rfar)
    dk = b.mixc(b.maprange(macro, .45, .62), lin('#FFFFFF'), lin('#8C8880'))       # darker rock bands at altitude
    cl[0] = b.mixc(1.0, cl[0], dk, 'MULTIPLY')
    cliffmask = b.math('MAXIMUM', A['m_cliff'], b.maprange(nz, .58, .44))
    base, _ = hblend(base, cl, cliffmask)
    # --- snow (+ far aerial snow), sticks to flatter ground; ice in steep, wet couloirs high up
    sn = L_('snow_02', 4.0, at=True)
    snf = L_('snow_field_aerial', 90.0, at=True)
    sn = lerp_layer(far, sn, snf)
    snproc = [b.mixc(b.maprange(b.noise(v, 1 / 40.0, 5, .6), .3, .7), lin('#D9E2EC'), lin('#F4F7FA')), .55, sn[2], .5]
    sn = lerp_layer(b.maprange(dist, 2500, 6000), sn, snproc)          # far snow: procedural (no texture moiré)
    snowmask = b.math('MULTIPLY', A['m_snow'], b.maprange(b.math('ADD', nz, b.math('MULTIPLY', meso, .12)), .70, .84))
    base, sfac = hblend(base, sn, snowmask, .25)
    # glacier ice in the high, gentle, wet valley floors: blue-white with stretched crevasse bands
    cv = b.node('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); cv.inputs['Scale'].default_value = 1 / 14.0
    b.link(b.vmath('MULTIPLY', v, (1.0, 3.5, 1.0)), cv.inputs['Vector'])
    crev = b.math('MULTIPLY', b.maprange(cv.outputs['Distance'], 0.0, .05, 1.0, 0.0), b.maprange(dist, 3000, 800))   # fades far away
    icecol = b.mixc(b.math('MULTIPLY', meso, .6), lin('#A9CBE0'), lin('#7FAACB'))
    icecol = b.mixc(b.math('MULTIPLY', crev, .7), icecol, lin('#2E4A63'))
    ice = [icecol, .3, base[2], .6]
    icef = b.math('MULTIPLY', b.math('MULTIPLY', A['m_snow'], b.maprange(A['m_flow'], .25, .55)), b.maprange(zpos, 3900, 4400))
    icef = b.math('MULTIPLY', icef, b.maprange(nz, .86, .95))
    base = lerp_layer(icef, base, ice)
    b.link(base[0], bs.inputs['Base Color']); b.link(base[1], bs.inputs['Roughness']); b.link(base[2], bs.inputs['Normal'])
    bs.inputs['Metallic'].default_value = 0.0; bs.inputs['Specular IOR Level'].default_value = .3   # realism pass (was .4)
    SPEC['MAT_T5_TERRAIN'] = dict(source='blend of 15 Poly Haven 2K scans + procedural ice/canopy',
                                  maps='per layer: Base Color, Roughness, Normal GL, Displacement (height blend)',
                                  resolution='2K per layer; near/far scale switch 150–900 m', metallic=0.0,
                                  layers=['grass ×2 + aerial grass', 'dry grass', 'forest floor', 'far canopy', 'compacted soil',
                                          'mud', 'gravel / river bed (wet)', 'lake sand', 'scree', 'rock', 'cliff', 'snow + aerial snow', 'ice'],
                                  drivers='mask attributes from NG_T5_HEIGHTFIELD + geometry slope + altitude + camera distance')
    return m


L['TERRAIN'] = terrain_material()


# =========================================================================== desert terrain shader (milestone 2, region R04)
def desert_material():
    """MAT_T5_TERRAIN_DESERT — same mask slots, desert meaning: m_dry = SAND (dunes), m_pad = PLAYA (cracked mud),
    m_gravel = desert PAVEMENT, m_grove = sparse shrubs (wadi), m_scree, m_rock, m_cliff (sandstone strata, biplanar so the
    layers stay horizontal on every wall), m_wet = water / sea."""
    m, b, bs, out = newmat('MAT_T5_TERRAIN_DESERT')
    v = coords(b)
    A = {k: b.attr(k) for k in ('m_rock', 'm_wet', 'm_dry', 'm_pad', 'm_grove', 'm_scree', 'm_gravel', 'm_flow', 'm_cliff')}
    cam = b.node('ShaderNodeCameraData'); dist = cam.outputs['View Distance']
    geo = b.node('ShaderNodeNewGeometry')
    nsep = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Normal'], nsep.inputs[0]); nz = nsep.outputs['Z']
    vs = b.node('ShaderNodeSeparateXYZ'); b.link(v, vs.inputs[0])
    macro = b.noise(v, 1 / 1500.0, 4, .55); meso = b.noise(v, 1 / 90.0, 4, .6)
    far = b.maprange(dist, 200, 1200)
    flat_ok = b.maprange(nz, .55, .78)

    def L_(tex, scale, box=False, at=False, tint=None, vec=None):
        g = use_group(b, tex, vec if vec is not None else v, scale, box, at, False, None, tint)
        return [g.outputs['Color'], g.outputs['Roughness'], g.outputs['Normal'], g.outputs['Height']]

    def lerp(f, a_, c_):
        return [b.mixc(f, a_[0], c_[0]), b.mixf(f, a_[1], c_[1]), b.mixv(f, a_[2], c_[2]), b.mixf(f, a_[3], c_[3])]

    def hb(base, lay, mask, k=.35):
        val = b.math('ADD', b.math('MULTIPLY', mask, 1.3), b.math('MULTIPLY', b.math('SUBTRACT', lay[3], base[3]), k))
        return lerp(b.maprange(b.math('SUBTRACT', val, .15), .4, .6), base, lay)
    # base: desert pavement / dry hardpan
    base = L_('dry_ground_01', 3.0, at=True, tint='#E8C9A0')
    pav = L_('gravel_ground_01', 2.5, tint='#F0D2AA')
    base = lerp(b.math('MULTIPLY', b.maprange(b.math('ADD', A['m_gravel'], b.math('MULTIPLY', meso, .3)), .3, .9), .7), base, pav)
    # sand (near scans + far procedural) with wind ripples (anisotropic waves across the wind, W → E)
    sd = L_('sand_01', 3.0, at=True, tint='#E2AE78')
    sd2 = L_('coast_sand_01', 4.0, tint='#D9A06A')
    sd = lerp(b.maprange(macro, .42, .6), sd, sd2)
    sfar = [b.mixc(b.maprange(b.noise(v, 1 / 60.0, 4, .5), .3, .7), lin('#C99A64'), lin('#E6BE88')), .9, sd[2], .5]
    sd = lerp(far, sd, sfar)
    wv = b.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X'); wv.inputs['Scale'].default_value = 1 / 0.18
    wv.inputs['Distortion'].default_value = 6.0; wv.inputs['Detail'].default_value = 3.0
    b.link(b.vmath('SCALE', v, scale=1 / 4.0), wv.inputs['Vector'])
    rip = b.node('ShaderNodeBump'); rip.inputs['Strength'].default_value = .25; rip.inputs['Distance'].default_value = .02
    b.link(b.math('MULTIPLY', wv.outputs['Fac'], b.maprange(dist, 60, 5)), rip.inputs['Height']); b.link(sd[2], rip.inputs['Normal'])
    sd[2] = rip.outputs['Normal']
    # aspect / slope colouring of the sand: lee (slip) faces a touch redder + darker, crests lighter (wind-sorted grains)
    nx_ = ns_ = None
    asp = b.math('ADD', b.math('MULTIPLY', nsep.outputs['X'], -.8), b.math('MULTIPLY', nsep.outputs['Y'], .2))   # wind from W → lee faces E
    lee = b.maprange(asp, .05, .45)
    sd[0] = b.mixc(b.math('MULTIPLY', lee, .45), sd[0], b.mixc(1.0, sd[0], lin('#C98A5E'), 'MULTIPLY'))
    crest = b.maprange(nz, .97, 1.0)
    sd[0] = b.mixc(b.math('MULTIPLY', crest, .25), sd[0], lin('#F6DDB4'))
    # far ripples (normal only, scaled with distance) so the dune field never looks plastic
    wv2 = b.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X'); wv2.inputs['Scale'].default_value = 1 / 1.2
    wv2.inputs['Distortion'].default_value = 8.0; wv2.inputs['Detail'].default_value = 2.0
    b.link(b.vmath('SCALE', v, scale=1 / 30.0), wv2.inputs['Vector'])
    bp2 = b.node('ShaderNodeBump'); bp2.inputs['Strength'].default_value = .12
    b.link(b.math('MULTIPLY', wv2.outputs['Fac'], b.maprange(dist, 40, 400)), bp2.inputs['Height']); b.link(sd[2], bp2.inputs['Normal'])
    sd[2] = bp2.outputs['Normal']
    base = hb(base, sd, b.maprange(b.math('ADD', A['m_dry'], b.math('MULTIPLY', macro, .25)), .05, .75), .2)
    # playas — cracked dry mud
    pl = L_('mud_cracked_dry_03', 4.0, tint='#E7D2B6')
    base = hb(base, pl, b.math('MULTIPLY', A['m_pad'], flat_ok))
    # scree / talus
    sc_ = L_('rocky_gravel', 3.0, tint='#E0B892')
    base = hb(base, sc_, b.math('MULTIPLY', A['m_scree'], flat_ok))
    # rock (gentle outcrops) — triplanar
    rk = L_('rock_ground', 4.0, box=True, tint='#E2B88C')
    base = hb(base, rk, b.math('MAXIMUM', A['m_rock'], b.maprange(b.math('ADD', nz, b.math('MULTIPLY', meso, .08)), .82, .7)))
    # cliffs — sandstone strata, BIPLANAR (x-z and y-z planes, blended by the normal) → layers stay horizontal on every wall
    sc6 = 1 / 14.0
    xz = b.node('ShaderNodeCombineXYZ'); b.link(vs.outputs['X'], xz.inputs['X']); b.link(vs.outputs['Z'], xz.inputs['Y'])
    yz = b.node('ShaderNodeCombineXYZ'); b.link(vs.outputs['Y'], yz.inputs['X']); b.link(vs.outputs['Z'], yz.inputs['Y'])
    c1 = L_('cliff_side', 14.0, vec=xz.outputs[0], tint='#F0D2B4'); c2 = L_('cliff_side', 14.0, vec=yz.outputs[0], tint='#F0D2B4')
    wy = b.math('ABSOLUTE', nsep.outputs['Y']); wx_ = b.math('ABSOLUTE', nsep.outputs['X'])
    cl = lerp(b.math('DIVIDE', wx_, b.math('ADD', b.math('ADD', wx_, wy), 1e-4)), c1, c2)
    cfar = [b.mixc(b.maprange(b.noise(v, 1 / 25.0, 4, .6), .3, .7), lin('#9C5E3A'), lin('#C88E62')), .85, cl[2], .5]
    cl = lerp(b.maprange(dist, 500, 2500), cl, cfar)
    base = hb(base, cl, b.math('MAXIMUM', A['m_cliff'], b.maprange(nz, .6, .45)))
    # wadi shrub litter / darker damp sand in channels
    base[0] = b.mixc(b.math('MULTIPLY', A['m_grove'], .35), base[0], lin('#8A7A5A'))
    b.link(base[0], bs.inputs['Base Color']); b.link(base[1], bs.inputs['Roughness']); b.link(base[2], bs.inputs['Normal'])
    bs.inputs['Metallic'].default_value = 0.0; bs.inputs['Specular IOR Level'].default_value = .28  # realism pass (was .35)
    SPEC['MAT_T5_TERRAIN_DESERT'] = dict(source='Poly Haven 2K: dry_ground_01, gravel_ground_01, sand_01, coast_sand_01, mud_cracked_dry_03, '
                                         'rocky_gravel, rock_ground, cliff_side (biplanar strata) + procedural far sand / far cliff / ripples',
                                         maps='Base Color, Roughness, Normal GL, Displacement (height blend)', resolution='2K per layer',
                                         metallic=0.0, layers=['pavement', 'sand + wind ripples', 'playa (cracked)', 'scree', 'rock', 'sandstone cliff'])
    return m


L['TERRAIN_DESERT'] = desert_material()


def forbidden_material():
    """MAT_T5_TERRAIN_FORBIDDEN — the blasted crater region (map biome 'forbidden'): dark ash ground (m_dry), fissures with
    scorched reddish-brown soil (m_pad), dark rubble (m_gravel), dark fractured rock + cliffs. No lava / glow (not approved)."""
    m, b, bs, out = newmat('MAT_T5_TERRAIN_FORBIDDEN')
    v = coords(b)
    A = {k: b.attr(k) for k in ('m_rock', 'm_dry', 'm_pad', 'm_scree', 'm_gravel', 'm_cliff')}
    cam = b.node('ShaderNodeCameraData'); dist = cam.outputs['View Distance']
    geo = b.node('ShaderNodeNewGeometry'); ns = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Normal'], ns.inputs[0]); nz = ns.outputs['Z']
    macro = b.noise(v, 1 / 1500.0, 4, .55); meso = b.noise(v, 1 / 70.0, 4, .6)
    flat_ok = b.maprange(nz, .55, .78)

    def L_(tex, scale, box=False, at=False, tint=None):
        g = use_group(b, tex, v, scale, box, at, False, None, tint)
        return [g.outputs['Color'], g.outputs['Roughness'], g.outputs['Normal'], g.outputs['Height']]

    def lerp(f, a_, c_):
        return [b.mixc(f, a_[0], c_[0]), b.mixf(f, a_[1], c_[1]), b.mixv(f, a_[2], c_[2]), b.mixf(f, a_[3], c_[3])]

    def hb(base, lay, mask, k=.35):
        val = b.math('ADD', b.math('MULTIPLY', mask, 1.3), b.math('MULTIPLY', b.math('SUBTRACT', lay[3], base[3]), k))
        return lerp(b.maprange(b.math('SUBTRACT', val, .15), .4, .6), base, lay)

    def dark(col, sat, val):
        h = b.node('ShaderNodeHueSaturation'); h.inputs['Saturation'].default_value = sat; h.inputs['Value'].default_value = val
        b.link(col, h.inputs['Color']); return h.outputs['Color']
    base = L_('dry_ground_01', 3.0, at=True); base[0] = b.mixc(1.0, dark(base[0], .1, .09), lin('#6E625C'), 'MULTIPLY')
    ash = L_('dry_ground_01', 5.0); ash[0] = b.mixc(1.0, dark(ash[0], .0, .07), lin('#5E5A5E'), 'MULTIPLY')
    base = hb(base, ash, b.maprange(b.math('ADD', A['m_dry'], b.math('MULTIPLY', macro, .25)), .1, .8), .2)
    rub = L_('rocky_gravel', 2.5); rub[0] = dark(rub[0], .1, .13)
    base = hb(base, rub, b.math('MULTIPLY', A['m_gravel'], flat_ok))
    fis = L_('mud_cracked_dry_03', 3.0); fis[0] = b.mixc(1.0, dark(fis[0], .25, .2), lin('#5A4038'), 'MULTIPLY')
    base = hb(base, fis, b.math('MULTIPLY', A['m_pad'], flat_ok), .5)
    sc_ = L_('gravel_ground_01', 3.0); sc_[0] = dark(sc_[0], .1, .13)
    base = hb(base, sc_, b.math('MULTIPLY', A['m_scree'], flat_ok))
    rk = L_('dark_rock', 6.0, box=True, at=True)
    rfar = [b.mixc(b.maprange(b.noise(v, 1 / 20.0, 4, .6), .3, .7), lin('#1E1B1C'), lin('#3B3536')), .8, rk[2], .5]
    rk = lerp(b.maprange(dist, 500, 2500), rk, rfar)
    base = hb(base, rk, b.math('MAXIMUM', b.math('MAXIMUM', A['m_rock'], A['m_cliff']), b.maprange(b.math('ADD', nz, b.math('MULTIPLY', meso, .1)), .9, .76)))
    far = [b.mixc(b.maprange(macro, .35, .65), lin('#1C1819'), lin('#332C2F')), .9, base[2], .5]
    base = lerp(b.maprange(dist, 1500, 6000), base, far)
    b.link(base[0], bs.inputs['Base Color']); b.link(base[1], bs.inputs['Roughness']); b.link(base[2], bs.inputs['Normal'])
    bs.inputs['Metallic'].default_value = 0.0; bs.inputs['Specular IOR Level'].default_value = .3   # realism pass (was default .5)
    SPEC['MAT_T5_TERRAIN_FORBIDDEN'] = dict(source='Poly Haven 2K dry_ground_01, rocky_gravel, mud_cracked_dry_03, gravel_ground_01, dark_rock '
                                            '(darkened / desaturated) + procedural far', maps='Base Color, Roughness, Normal GL, Displacement',
                                            resolution='2K per layer', metallic=0.0, layers=['ash ground', 'rubble', 'fissures', 'scree', 'dark rock'])
    return m


L['TERRAIN_FORBIDDEN'] = forbidden_material()


def enchanted_material():
    """MAT_T5_TERRAIN_ENCHANTED — old-growth Enchanted Forest floor: deep teal-green moss carpet (m_dry = moss amount),
    needle / leaf litter, mossy rock, teal-tinted clearings (m_grove). Colour key from the World Bible (#2C6B5B)."""
    m, b, bs, out = newmat('MAT_T5_TERRAIN_ENCHANTED')
    v = coords(b)
    A = {k: b.attr(k) for k in ('m_rock', 'm_wet', 'm_dry', 'm_grove', 'm_gravel', 'm_cliff', 'm_scree')}
    cam = b.node('ShaderNodeCameraData'); dist = cam.outputs['View Distance']
    geo = b.node('ShaderNodeNewGeometry'); ns = b.node('ShaderNodeSeparateXYZ'); b.link(geo.outputs['Normal'], ns.inputs[0]); nz = ns.outputs['Z']
    macro = b.noise(v, 1 / 400.0, 4, .55); meso = b.noise(v, 1 / 12.0, 4, .6)

    def L_(tex, scale, box=False, at=False, tint=None):
        g = use_group(b, tex, v, scale, box, at, False, None, tint)
        return [g.outputs['Color'], g.outputs['Roughness'], g.outputs['Normal'], g.outputs['Height']]

    def lerp(f, a_, c_):
        return [b.mixc(f, a_[0], c_[0]), b.mixf(f, a_[1], c_[1]), b.mixv(f, a_[2], c_[2]), b.mixf(f, a_[3], c_[3])]

    def hb(base, lay, mask, k=.35):
        val = b.math('ADD', b.math('MULTIPLY', mask, 1.3), b.math('MULTIPLY', b.math('SUBTRACT', lay[3], base[3]), k))
        return lerp(b.maprange(b.math('SUBTRACT', val, .15), .4, .6), base, lay)

    def hs(col, sat, val, hue=.5):
        h = b.node('ShaderNodeHueSaturation'); h.inputs['Hue'].default_value = hue; h.inputs['Saturation'].default_value = sat
        h.inputs['Value'].default_value = val; b.link(col, h.inputs['Color']); return h.outputs['Color']
    base = L_('forest_floor', 3.0, at=True); base[0] = b.mixc(1.0, hs(base[0], .45, .38), lin('#9A8A70'), 'MULTIPLY')
    moss = L_('leafy_grass', 1.8, at=True)
    bw = b.node('ShaderNodeRGBToBW'); b.link(moss[0], bw.inputs[0])
    rmp = b.node('ShaderNodeValToRGB'); b.link(b.math('MULTIPLY', bw.outputs[0], 1.7), rmp.inputs['Fac'])
    el = rmp.color_ramp.elements; el[0].color = lin('#0B1A12'); el[1].position = .8; el[1].color = lin('#4F6E3E')
    e2 = el.new(.4); e2.color = lin('#24443A')
    moss[0] = b.mixc(b.maprange(macro, .3, .7, .1, .45), rmp.outputs['Color'], lin('#4E6A2E'))
    moss[0] = b.mixc(.35, moss[0], base[0])
    base = hb(base, moss, b.maprange(b.math('ADD', A['m_dry'], b.math('MULTIPLY', meso, .2)), .15, .7), .25)
    gap = L_('leafy_grass', 2.4); gap[0] = hs(gap[0], .9, .6, .52)
    base = hb(base, gap, b.math('MULTIPLY', A['m_grove'], .8))
    bank = L_('mud_forest', 2.5); base = hb(base, bank, b.math('MULTIPLY', A['m_wet'], .9))
    st = L_('river_small_rocks', 1.6); base = hb(base, st, A['m_gravel'], .5)
    rk = L_('mossy_rock', 4.0, box=True, at=True)
    base = hb(base, rk, b.math('MAXIMUM', b.math('MAXIMUM', A['m_rock'], A['m_cliff']), b.maprange(nz, .78, .62)))
    far = [b.mixc(b.maprange(macro, .35, .65), lin('#123026'), lin('#1F4A3A')), .9, base[2], .5]
    base = lerp(b.maprange(dist, 1500, 5000), base, far)
    b.link(base[0], bs.inputs['Base Color']); b.link(base[1], bs.inputs['Roughness']); b.link(base[2], bs.inputs['Normal'])
    bs.inputs['Metallic'].default_value = 0.0; bs.inputs['Specular IOR Level'].default_value = .3   # realism pass (was default .5)
    SPEC['MAT_T5_TERRAIN_ENCHANTED'] = dict(source='Poly Haven 2K forest_floor, leafy_grass (re-coloured to moss / teal), mud_forest, '
                                            'river_small_rocks, mossy_rock + procedural far', maps='Base Color, Roughness, Normal GL, Displacement',
                                            resolution='2K per layer', metallic=0.0, layers=['litter', 'moss carpet', 'teal clearings', 'bank mud', 'stream stones', 'mossy rock'])
    return m


L['TERRAIN_ENCHANTED'] = enchanted_material()

# low-lying ground mist (volume box; density falls off with height above the box base, object space Z)
m, b, bs, out = newmat('MAT_T5_GROUND_MIST')
b.n.remove(bs)
pv = b.node('ShaderNodeVolumePrincipled'); pv.inputs['Color'].default_value = lin('#CFE3DC'); pv.inputs['Anisotropy'].default_value = .5
tco = b.node('ShaderNodeTexCoord'); oz = b.node('ShaderNodeSeparateXYZ'); b.link(tco.outputs['Generated'], oz.inputs[0])
den = b.math('MULTIPLY', b.math('EXPONENT', b.math('MULTIPLY', oz.outputs['Z'], -7.0)), b.maprange(b.noise(tco.outputs['Object'], 1 / 60.0, 3, .5), .3, .7, .2, 1.0))
b.link(b.math('MULTIPLY', den, .012), pv.inputs['Density']); b.link(pv.outputs[0], out.inputs['Volume'])
SPEC['MAT_T5_GROUND_MIST'] = dict(source='procedural volume', maps='Principled Volume, density 0.012 × exp(−7·z_box) × noise', resolution='procedural')
L['GROUND_MIST'] = m


# =========================================================================== water, mist, haze, far trees
def water(name, deep, shallow, rough=.02, wave=1.0):
    m, b, bs, out = newmat(name)
    v = coords(b)
    fr = b.node('ShaderNodeValue'); fr.label = 'flow time'
    d = fr.outputs[0].driver_add('default_value'); d.driver.expression = 'frame / 24'
    # waves: two noise layers drifting along +Y (local flow direction is not needed for small ripples)
    off = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', fr.outputs[0], .6), off.inputs['Y'])
    v2 = b.vmath('ADD', v, off.outputs[0])
    w1 = b.noise(v2, .9 * wave, 3, .5); w2 = b.noise(b.vmath('SCALE', v, scale=-1.0), 3.1 * wave, 2, .5)
    bp = b.node('ShaderNodeBump'); bp.inputs['Strength'].default_value = .18; bp.inputs['Distance'].default_value = .05
    b.link(b.math('ADD', w1, b.math('MULTIPLY', w2, .4)), bp.inputs['Height'])
    foam_attr = b.attr('foam')
    fn = b.noise(b.vmath('SCALE', v2, scale=1.0), 2.2, 4, .65)
    foam = b.math('MULTIPLY', foam_attr, b.maprange(fn, .35, .6), clamp=True)
    bs.inputs['Base Color'].default_value = lin(shallow); bs.inputs['Roughness'].default_value = rough
    bs.inputs['Transmission Weight'].default_value = 1.0; bs.inputs['IOR'].default_value = 1.333
    b.link(bp.outputs[0], bs.inputs['Normal'])
    # depth colour: transmission tinted by the deep colour where the view is grazing (Fresnel-ish facing)
    lw = b.node('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = .35
    tint = b.mixc(lw.outputs['Facing'], lin(shallow), lin(deep))
    b.link(tint, bs.inputs['Base Color'])
    fb = b.node('ShaderNodeBsdfPrincipled'); fb.inputs['Base Color'].default_value = lin('#F4F6F2'); fb.inputs['Roughness'].default_value = .6
    mx = b.node('ShaderNodeMixShader'); b.link(foam, mx.inputs[0]); b.link(bs.outputs[0], mx.inputs[1]); b.link(fb.outputs[0], mx.inputs[2])
    b.link(mx.outputs[0], out.inputs['Surface'])
    SPEC[name] = dict(source='procedural', maps='transmission IOR 1.333, animated ripple bump, foam (attribute "foam" × noise)',
                      resolution='procedural', metallic=0.0)
    return m


L['WATER_RIVER'] = water('MAT_T5_WATER_RIVER', '#16352E', '#5E7C66', .03, 1.3)
L['WATER_LAKE'] = water('MAT_T5_WATER_LAKE', '#0E2A33', '#3E6E72', .02, .5)
m, b, bs, out = newmat('MAT_T5_WATER_DARK')                        # forbidden crater lake: black, dull, no transmission (opaque murk)
v = coords(b); wv_ = b.noise(v, .25, 3, .5)
bp = b.node('ShaderNodeBump'); bp.inputs['Strength'].default_value = .08; b.link(wv_, bp.inputs['Height']); b.link(bp.outputs[0], bs.inputs['Normal'])
bs.inputs['Base Color'].default_value = lin('#050807'); bs.inputs['Roughness'].default_value = .32; bs.inputs['Specular IOR Level'].default_value = .35
b.link(b.attr('foam'), b.node('ShaderNodeMath').inputs[0])
SPEC['MAT_T5_WATER_DARK'] = dict(source='procedural', maps='opaque black water, roughness 0.32, small ripple bump', resolution='procedural', metallic=0.0)
L['WATER_DARK'] = m

# waterfall sheet: falling streaks (animated), foam white + translucent water, alpha at the streak gaps
m, b, bs, out = newmat('MAT_T5_WATERFALL')
v = coords(b)
fr = b.node('ShaderNodeValue'); d = fr.outputs[0].driver_add('default_value'); d.driver.expression = 'frame / 24'
off = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', fr.outputs[0], 6.0), off.inputs['Z'])
mp = b.node('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.6, 1.6, .12)
b.link(b.vmath('ADD', v, off.outputs[0]), mp.inputs['Vector'])
st = b.noise(mp.outputs[0], 3.0, 6, .7)
streak = b.maprange(st, .38, .62)
uvn = b.node('ShaderNodeUVMap'); uvs = b.node('ShaderNodeSeparateXYZ'); b.link(uvn.outputs[0], uvs.inputs[0])
edge = b.math('MINIMUM', uvs.outputs['X'], b.math('SUBTRACT', 1.0, uvs.outputs['X']))
rag = b.maprange(b.math('ADD', edge, b.math('MULTIPLY', b.noise(mp.outputs[0], 1.4, 4, .6), .12)), .06, .2)
streak = b.math('MULTIPLY', streak, rag)
bs.inputs['Base Color'].default_value = lin('#EEF3F2'); bs.inputs['Roughness'].default_value = .35
bs.inputs['Subsurface Weight'].default_value = .5; bs.inputs['Transmission Weight'].default_value = .3
tr = b.node('ShaderNodeBsdfTransparent')
mx = b.node('ShaderNodeMixShader'); b.link(b.math('ADD', b.math('MULTIPLY', streak, .7), .05, clamp=True), mx.inputs[0])
b.link(tr.outputs[0], mx.inputs[1]); b.link(bs.outputs[0], mx.inputs[2]); b.link(mx.outputs[0], out.inputs['Surface'])
m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
SPEC['MAT_T5_WATERFALL'] = dict(source='procedural', maps='animated falling streaks (noise stretched in Z), subsurface white water, alpha mix',
                                resolution='procedural', metallic=0.0)
L['WATERFALL'] = m

m, b, bs, out = newmat('MAT_T5_FOAM')
v = coords(b); fn = b.noise(v, 1.5, 5, .7)
b.link(b.mixc(b.maprange(fn, .4, .7), lin('#C9D2CF'), lin('#FAFBFA')), bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value = .7; bs.inputs['Subsurface Weight'].default_value = .4
L['FOAM'] = m


def volume(name, col, dens, mode='mist'):
    m, b, bs, out = newmat(name)
    b.n.remove(bs)
    pv = b.node('ShaderNodeVolumePrincipled'); pv.inputs['Color'].default_value = lin(col); pv.inputs['Anisotropy'].default_value = .35
    v = coords(b)
    if mode == 'mist':                # spray cloud at a waterfall base: noisy, fading outward from the object centre
        r = b.vmath('LENGTH', b.vmath('MULTIPLY', v, (1, 1, 1)))
        fall = b.maprange(r, 0.2, 1.0, 1.0, 0.0)
        den = b.math('MULTIPLY', b.math('MULTIPLY', b.maprange(b.noise(v, 2.5, 4, .6), .4, .7), fall), dens)
    else:                             # haze: aerial perspective, exponential falloff with altitude (Z in metres)
        tcz = b.node('ShaderNodeSeparateXYZ'); b.link(b.node('ShaderNodeNewGeometry').outputs['Position'], tcz.inputs[0])
        den = b.math('MULTIPLY', b.math('EXPONENT', b.math('MULTIPLY', b.math('SUBTRACT', tcz.outputs['Z'], 650), -1 / 2600.0)), dens)
    b.link(den, pv.inputs['Density'])
    b.link(pv.outputs[0], out.inputs['Volume'])
    SPEC[name] = dict(source='procedural volume', maps=f'Principled Volume, density {dens} ({mode})', resolution='procedural')
    return m


L['MIST'] = volume('MAT_T5_MIST', '#F4F6F8', .3, 'mist')
L['HAZE'] = volume('MAT_T5_HAZE', '#C9D6E4', 1.6e-5, 'haze')

m, b, bs, out = newmat('MAT_T5_TREE_FAR')        # far-forest proxy canopy (>1.5 km): needle-green with clumped noise
v = coords(b); n = b.noise(v, 1.7, 5, .7)
b.link(b.mixc(b.maprange(n, .35, .65), lin('#16261A'), lin('#2E4626')), bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value = .85; bs.inputs['Subsurface Weight'].default_value = .15
bp = b.node('ShaderNodeBump'); bp.inputs['Strength'].default_value = .6; b.link(n, bp.inputs['Height']); b.link(bp.outputs[0], bs.inputs['Normal'])
L['TREE_FAR'] = m
m, b, bs, out = newmat('MAT_T5_TRUNK_FAR')
bs.inputs['Base Color'].default_value = lin('#3A2C22'); bs.inputs['Roughness'].default_value = .9
L['TRUNK_FAR'] = m

# keep node groups with the file
for ng in bpy.data.node_groups:
    ng.use_fake_user = True

# =========================================================================== swatch board (material preview scene)
c = wk.coll('T5_MATERIAL_SWATCHES')
order = ['GRASS', 'GRASS_DRY', 'SOIL', 'FOREST_FLOOR', 'MUD', 'GRAVEL', 'WET_STONE', 'SAND', 'ROCK', 'DARK_ROCK', 'CLIFF', 'SCREE',
         'SNOW', 'ICE', 'WATER_RIVER', 'TREE_FAR']
import bmesh
for i, k in enumerate(order):
    x, y = (i % 4) * 2.4, -(i // 4) * 2.4
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=1.0)
    me = bpy.data.meshes.new(f'SW_{k}'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(f'SW_{k}', me); c.objects.link(o); o.location = (x, y, 1.0)
    me.materials.append(L[k]); me.shade_smooth()
    # local scale: swatches are 2 m spheres → show textures at ~1/3 of their real tile size so detail is readable
    o.scale = (1, 1, 1)
    t = wk.text(f'LBL_{k}', L[k].name.replace('MAT_T5_', ''), (x, y - 1.25, .02), .22, c, None)
fl = wk.box('SW_FLOOR', (12, 12, .1), (3.6, -3.6, -.05), c, None)
cam = wk.camera('CAM_SWATCHES', (3.6, -13.5, 11.5), (3.6, -3.4, .4), 50, c)
sun = wk.sun('SW_SUN', 45, 135, 3.5, c)
sc.world = wk.gradient_world('SW_WORLD', '#B8C4D0', '#5A6E86', .8)
wk.setup_cycles(sc, (1280, 1100), 48)
sc.camera = cam
wk.save(tk.MATLIB2)
json.dump(SPEC, open(wk.P('11_MATERIALS', 'T5_material_spec.json'), 'w'), indent=1)
if os.environ.get('T5_SWATCH_RENDER') == '1':
    wk.render(sc, cam, wk.P('12_RENDER', 'T5', 'T5_MATERIAL_LIBRARY_swatches.png'))
print('T5_MATERIALS_DONE', len(SPEC))

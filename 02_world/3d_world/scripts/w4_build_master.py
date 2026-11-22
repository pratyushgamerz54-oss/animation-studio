"""TASK 04 · MASTER WORLD → 00_MASTER_WORLD/WORLD_master_v001.blend (Blender 4.5).

The master holds NO geometry of its own: it LINKS the component files (relative paths) and organises them:
  scene MAIN_WORLD      main world (1 BU = 1 km), regions by direction + thematic collections (a piece can be in both:
                        same linked collection, no copies)
  scene ASHRAM_VALLEY   linked from 08_ASHRAM_VALLEY (1 BU = 1 m)                 — if built
  scene DIM_BLACK_HOLE  linked from 09_DIMENSIONS (own space, never merged)       — if built
  scene DIM_DARK_WORLD  linked from 09_DIMENSIONS (own space, never merged)       — if built
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import worldkit as wk

META = json.load(open(wk.P('01_GEOGRAPHY', 'data', 'world_features.json')))
RK = META['region_keys']; REG = META['regions']; CK = META['class_keys']; CLS = META['classes']
COMPS = ['01_GEOGRAPHY/WORLD_geography_v001.blend', '02_TERRAIN/WORLD_terrain_v001.blend', '03_MOUNTAINS/WORLD_mountains_v001.blend',
         '04_FORESTS/WORLD_forests_v001.blend', '05_RIVERS_AND_LAKES/WORLD_water_v001.blend', '06_DESERTS/WORLD_deserts_v001.blend',
         '07_ISLANDS/WORLD_islands_v001.blend', '10_CAMERAS/WORLD_cameras_v001.blend']
SCENES = [('08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v001.blend', 'ASHRAM_VALLEY'),
          ('09_DIMENSIONS/DIM_black_hole_training_v001.blend', 'DIM_BLACK_HOLE_TRAINING'),
          ('09_DIMENSIONS/DIM_saithan_dark_world_v001.blend', 'DIM_SAITHAN_DARK_WORLD')]
TOPS = {'01_GEOGRAPHY', '02_TERRAIN', '03_MOUNTAINS', '04_FORESTS', '05_RIVERS_AND_LAKES', '06_DESERTS', '07_ISLANDS', 'RIVERS', 'LAKES'}

wk.new_file()
sc = bpy.context.scene; sc.name = 'MAIN_WORLD'
sc['status'] = 'PROPOSAL — world map v2 revision 01, NOT LOCKED'
sc['units'] = '1 BU = 1 km in XY; Z = elevation km × vexag'; sc['vexag'] = META['vexag']
sc['origin'] = META['origin']; sc['world_km'] = META['world_km']
sc.unit_settings.scale_length = 1000.0; sc.unit_settings.length_unit = 'KILOMETERS'

L = {}
for rel in COMPS:
    got = wk.link_collections(wk.P(rel))
    for n, c in got.items():
        if n not in TOPS:
            L[n] = c
print('linked collections', len(L))

root = wk.coll('MAIN_WORLD')
dirs = wk.coll('00_REGIONS_BY_DIRECTION', root)
DIRC = {d: wk.coll(f'{d}_REGIONS', dirs) for d in ('NORTHERN', 'SOUTHERN', 'EASTERN', 'WESTERN')}
THEME = {}
for t, color in (('MOUNTAIN_REGIONS', 'COLOR_07'), ('FOREST_REGIONS', 'COLOR_04'), ('DESERT_REGIONS', 'COLOR_02'), ('PLAINS_AND_HILLS', 'COLOR_03'),
                 ('COASTAL_AREAS', 'COLOR_02'), ('ICE_AND_TUNDRA', 'COLOR_05'), ('RUINED_REGIONS', 'COLOR_01'), ('UNDERGROUND_ZONES_ALL', 'COLOR_01'),
                 ('WATER_SYSTEMS', 'COLOR_05'), ('ISLANDS', 'COLOR_06'), ('ASHRAM_VALLEY', 'COLOR_03'), ('UNEXPLORED_REGIONS', 'COLOR_08'),
                 ('OCEAN_FLOOR', None), ('GEOGRAPHY_REFERENCE', None), ('CAMERAS', None), ('LIGHTING', None)):
    THEME[t] = wk.coll(t, root, color)
regc = {}
for rk in RK:
    d = REG[rk][1]
    if d in DIRC:
        regc[rk] = wk.coll(f'REGION_{rk}_{REG[rk][0].split(" ")[1] if " " in REG[rk][0] else rk}', DIRC[d])


def put(child, parent):
    if child.name not in parent.children:
        parent.children.link(child)


for n, c in L.items():
    parts = n.split('_')
    if parts[0] in CK and parts[-1] in RK:
        ck, rk = parts[0], parts[-1]
        put(c, THEME[CLS[ck][1]] if CLS[ck][1] in THEME else THEME['PLAINS_AND_HILLS'])
        if rk in regc:
            put(c, regc[rk])
        if rk == 'C4U':
            put(c, THEME['UNEXPLORED_REGIONS'])
    elif parts[0] in ('RIVERS', 'LAKES') and parts[-1] in RK:
        put(c, THEME['WATER_SYSTEMS'])
        if parts[-1] in regc:
            put(c, regc[parts[-1]])
    elif n in ('OCEAN', 'WATERFALLS'):
        put(c, THEME['WATER_SYSTEMS'])
    elif n == 'SEABED':
        put(c, THEME['OCEAN_FLOOR'])
    elif n == 'UNDERGROUND_ZONES':
        put(c, THEME['UNDERGROUND_ZONES_ALL'])
    elif n == 'GEO_CAVE_ENTRANCES':
        put(c, THEME['UNDERGROUND_ZONES_ALL']); put(c, THEME['GEOGRAPHY_REFERENCE'])
    elif n == 'GEO_RUINS':
        put(c, THEME['RUINED_REGIONS']); put(c, THEME['GEOGRAPHY_REFERENCE'])
    elif n == 'RANGE_LINES':
        put(c, THEME['MOUNTAIN_REGIONS'])
    elif n == 'GEO_ASHRAM':
        put(c, THEME['ASHRAM_VALLEY'])
    elif n in ('GEO_UNEXPLORED_EDGES', 'GEO_HIDDEN_AND_GEM'):
        put(c, THEME['UNEXPLORED_REGIONS'])
    elif n in ('GEO_SETTLEMENTS', 'GEO_LABELS', 'GEO_GRID_1000KM'):
        put(c, THEME['GEOGRAPHY_REFERENCE'])
    elif n == 'WORLD_CAMERAS':
        put(c, THEME['CAMERAS'])
    elif n == 'WORLD_LIGHTING':
        put(c, THEME['LIGHTING'])
    else:
        print('UNSORTED collection', n)
        put(c, THEME['GEOGRAPHY_REFERENCE'])

note = bpy.data.texts.new('README_MASTER_WORLD')
note.write('MASTER WORLD — PROPOSAL (map v2 rev 01, NOT LOCKED)\n'
           'All geometry is LINKED from the component files (02_TERRAIN … 07_ISLANDS, 01_GEOGRAPHY, 10_CAMERAS).\n'
           'Edit a component file, then reopen the master. Same linked collection may sit in a direction collection AND a\n'
           'thematic collection (no duplicates). Separate dimensions are separate SCENES (never merged into MAIN_WORLD).\n'
           'Scale: see 01_GEOGRAPHY/WORLD_SCALE.md\n')

sc.world = wk.gradient_world('WORLD_SKY_MAIN', '#A9C1DA', '#2E5584', .9)
wk.setup_cycles(sc, (1280, 720), 24)
cams = {o.name: o for o in bpy.data.objects if o.type == 'CAMERA'}
sc.camera = cams.get('CAM_W01_ENTIRE_WORLD')
wk.viewport_defaults(sc, 60000)

for rel, nm in SCENES:
    p = wk.P(rel)
    if os.path.exists(p):
        with bpy.data.libraries.load(p, link=True, relative=True) as (src, dst):
            dst.scenes = [s for s in src.scenes if s == nm]
        print('linked scene', nm)
    else:
        print('scene not built yet:', rel)
bpy.context.window_manager.windows[0].scene = sc if bpy.context.window_manager.windows else None
wk.save(wk.P('00_MASTER_WORLD', 'WORLD_master_v001.blend'))
print('BUILD_MASTER_DONE')

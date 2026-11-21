"""TASK 04 · preview renders → 12_RENDER/ (Blender 4.5, CPU).

  12_RENDER/cycles/      cinematic aerial previews (Cycles, AgX) — markers/labels/guides excluded
  12_RENDER/viewport/    Workbench renders = Blender's Solid viewport (attribute colours, cavity, outlines) WITH
                         markers, labels, grids, LOD extents (the 'viewport screenshots')
Headless note: Workbench needs OpenGL → run with Mesa:  EGL_PLATFORM=surfaceless blender -b -P w4_render.py
Args after '--': world valley dims  (default all) · SAMPLES env (default 32) · RES env 'WxH' (default 1280x720)
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import worldkit as wk

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
WANT = set(ARGS) or {'world', 'valley', 'dims'}
SAMPLES = int(os.environ.get('SAMPLES', 32))
RES = tuple(int(x) for x in os.environ.get('RES', '1280x720').split('x'))
OUT = wk.P('12_RENDER')
LOG = []
OVERLAY = {'GEO_LABELS', 'GEO_GRID_1000KM', 'GEO_SETTLEMENTS', 'GEO_RUINS', 'GEO_CAVE_ENTRANCES', 'GEO_HIDDEN_AND_GEM',
           'GEO_UNEXPLORED_EDGES', 'GEO_ASHRAM', 'RANGE_LINES', 'UNDERGROUND_ZONES'}


def set_exclude(view_layer, names, state):
    def walk(lc):
        if lc.collection.name in names:
            lc.exclude = state
        for ch in lc.children:
            walk(ch)
    walk(view_layer.layer_collection)


VPONLY = bool(os.environ.get('VIEWPORT_ONLY'))


def job(sc, cam_name, mode, sub):
    if VPONLY and mode != 'viewport':
        return
    cam = bpy.data.objects[cam_name]
    path = os.path.join(OUT, sub, f'{mode}_{cam_name}.png')
    t = time.time()
    wk.render(sc, cam, path)
    LOG.append({'scene': sc.name, 'camera': cam_name, 'mode': mode, 'file': os.path.relpath(path, wk.ROOT),
                'seconds': round(time.time() - t, 1), 'desc': cam.get('description', '')})


def overlays_local(state):
    """valley / dimension files: guides + labels are local objects → toggle hide_render in memory (file is not saved)."""
    for o in bpy.data.objects:
        if o.name.startswith(('LBL_', 'AV_LBL', 'AV_MK_', 'BH_GUIDE', 'BH_LBL', 'DW_LBL', 'REF_ASHRAM_VOLUME')):
            o.hide_render = not state


if 'world' in WANT:
    bpy.ops.wm.open_mainfile(filepath=wk.P('00_MASTER_WORLD', 'WORLD_master_v001.blend'))
    sc = bpy.data.scenes['MAIN_WORLD']; vl = sc.view_layers[0]
    cams = sorted(o.name for o in bpy.data.objects if o.type == 'CAMERA' and o.name.startswith('CAM_W'))
    wk.setup_cycles(sc, RES, SAMPLES); set_exclude(vl, OVERLAY, True)
    for c in cams:
        if c != 'CAM_W00_TOP_ORTHO':
            job(sc, c, 'cycles', 'cycles')
    wk.setup_workbench(sc, RES); set_exclude(vl, OVERLAY, False)
    for c in ('CAM_W00_TOP_ORTHO', 'CAM_W01_ENTIRE_WORLD', 'CAM_W02_REGION_C1_AETHERIA', 'CAM_W03_MOUNTAINS_MAHAGIRI', 'CAM_W08_ASHRAM_VALLEY_REGION'):
        job(sc, c, 'viewport', 'viewport')

if 'valley' in WANT:
    bpy.ops.wm.open_mainfile(filepath=wk.P('08_ASHRAM_VALLEY', 'ASHRAM_VALLEY_terrain_v001.blend'))
    sc = bpy.data.scenes['ASHRAM_VALLEY']
    wk.setup_cycles(sc, RES, SAMPLES); overlays_local(False)
    for c in ('CAM_V01_VALLEY_ESTABLISHING', 'CAM_V02_TOWARD_SNOW_RANGE', 'CAM_V03_VALLEY_PLAN_TOP', 'CAM_V04_RIVER_AND_FOREST',
              'CAM_V05_SNOW_RANGE_AERIAL', 'CAM_V06_GROUND_LEVEL', 'CAM_V07_ASHRAM_PLACEMENT'):
        job(sc, c, 'cycles', 'cycles')
    wk.setup_workbench(sc, RES); overlays_local(True)
    bpy.data.objects['AV_HAZE_VOLUME'].hide_render = True
    for c in ('CAM_V00_LOD_LAYOUT_TOP', 'CAM_V03_VALLEY_PLAN_TOP', 'CAM_V01_VALLEY_ESTABLISHING', 'CAM_V07_ASHRAM_PLACEMENT'):
        top_view = c in ('CAM_V00_LOD_LAYOUT_TOP', 'CAM_V03_VALLEY_PLAN_TOP')
        for o in bpy.data.objects:                         # plan views: hide mid-distance canopy instances (read as black blocks from above)
            if o.name in ('AV_FOREST_LOD1', 'AV_GROVES_LOD1'):
                o.hide_render = top_view
        job(sc, c, 'viewport', 'viewport')

if 'dims' in WANT:
    for f, sn, cy, vp in (('DIM_black_hole_training_v001.blend', 'DIM_BLACK_HOLE_TRAINING', ('CAM_D1_BH_OVERVIEW', 'CAM_D1_BH_TRAINING_RING'), ('CAM_D1_BH_TOP',)),
                          ('DIM_saithan_dark_world_v001.blend', 'DIM_SAITHAN_DARK_WORLD', ('CAM_D2_DW_OVERVIEW', 'CAM_D2_DW_SPIRE_FIELD'), ('CAM_D2_DW_TOP',))):
        bpy.ops.wm.open_mainfile(filepath=wk.P('09_DIMENSIONS', f))
        sc = bpy.data.scenes[sn]
        wk.setup_cycles(sc, RES, SAMPLES); overlays_local(False)
        for c in cy:
            job(sc, c, 'cycles', 'cycles')
        wk.setup_workbench(sc, RES); overlays_local(True)
        for o in bpy.data.objects:
            if o.name in ('DW_FOG_VOLUME',):
                o.hide_render = True
        for c in vp:
            job(sc, c, 'viewport', 'viewport')

logp = os.path.join(OUT, 'render_log.json')
old = json.load(open(logp)) if os.path.exists(logp) else []
keep = [e for e in old if not any(e['file'] == n['file'] for n in LOG)]
json.dump(keep + LOG, open(logp, 'w'), indent=1)
print('RENDER_DONE', len(LOG))

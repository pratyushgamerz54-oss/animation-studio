"""TASK 06 · populated region files — TASK 05 terrain + T6 ecosystem layers (Blender 4.5).

    BPY45 t6_populate.py -- AV|EF|MK|DS|FB

How (TASK 05 stays untouched):
  1. open the APPROVED TASK 05 region master (read-only) and SAVE AS a new file in 02_world/ecosystem/populated/ — the master,
     its components and terrain v002 are never written;
  2. T5 vegetation scatters that T6 replaces are switched off by excluding their linked collection in THIS file's view layer;
     the T5 scatters T6 keeps (rocks, river stones, far forest masses) are linked again into a local collection T5_SCATTER_KEPT;
  3. T6 species are LINKED from the vegetation libraries (hero + variants + LODs: wind-free *_SC copies) into local band
     collections (ECO_<asset>_NEAR / MID / FAR / HORIZON, excluded from the view layer);
  4. one scatter object per layer with NG_T6_ECOSYSTEM on the T5 hero terrain tile (its mask attributes drive density);
  5. one T6_WIND_CONTROL drives every layer (strength / gust / speed / flutter);
  6. landmarks + PROPOSED placements (Ashram Peepal on a chabutra, Ashram garden beds) and T6 preview cameras.
Rules applied: Decision Sheet 01 (Peepal ONE at the courtyard, Tulsi + Marigold ONLY in the Ashram garden, R-02 70–80 % natural /
20–30 % fantasy, SPRING), REAL-WORLD REALISM RULE (wind on every plant, per-instance phase, nothing floating: points sit on the
evaluated terrain surface, trees sunk a few cm).
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import bpy, bmesh
from mathutils import Vector
import t6kit as K
import t6_ecosystem as E
import t6_regions as RG

REG = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'AV'
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
W3 = os.path.join(ROOT, '02_world', '3d_world')
OUTD = os.path.join(ROOT, '02_world', 'ecosystem', 'populated'); os.makedirs(OUTD, exist_ok=True)
LIB = os.path.join(K.VEG, 'library')

# ---------------------------------------------------------------- layer defaults per kind
# Realize Distance = per-vertex wind zone (close-ups); beyond it instances tilt as a whole. Memory: a realized 300 k-tri tree
# costs ~100 MB with its wind fields, so 15 m (trees) keeps a dense forest preview < 8 GB on the 16 GB machine.
KD = {'tree':   dict(Camera_Clearance=7.0, Cull_Distance=2500.0, Cull_Angle=55.0, Keep_Near=60.0, L01=70.0, L12=260.0, L23=1200.0, Realize=15.0,
                     Align_To_Normal=0.0, Random_Tilt=2.0, Sink=.04, Slope_Max=36.0, Scale_Min=.85, Scale_Max=1.15, Cluster_Scale=60.0, Cluster_Amount=.35),
      'shrub':  dict(Camera_Clearance=3.0, Cull_Distance=500.0, Cull_Angle=55.0, Keep_Near=25.0, L01=35.0, L12=120.0, L23=400.0, Realize=10.0,
                     Align_To_Normal=.3, Random_Tilt=4.0, Sink=.03, Slope_Max=40.0, Scale_Min=.8, Scale_Max=1.2, Cluster_Scale=20.0, Cluster_Amount=.6),
      'plant':  dict(Camera_Clearance=0.0, Cull_Distance=140.0, Cull_Angle=55.0, Keep_Near=10.0, L01=22.0, L12=70.0, L23=140.0, Realize=6.0,
                     Align_To_Normal=.5, Random_Tilt=6.0, Sink=.01, Slope_Max=45.0, Scale_Min=.75, Scale_Max=1.3, Cluster_Scale=6.0, Cluster_Amount=.5),
      'detail': dict(Camera_Clearance=1.5, Cull_Distance=110.0, Cull_Angle=55.0, Keep_Near=10.0, L01=30.0, L12=110.0, L23=110.0, Realize=0.0,
                     Align_To_Normal=1.0, Random_Tilt=0.0, Sink=.0, Slope_Max=35.0, Scale_Min=.8, Scale_Max=1.25, Cluster_Scale=15.0, Cluster_Amount=.6)}

L = lambda asset, **kw: dict(asset=asset, **kw)
REGIONS = {
    'AV': dict(master='00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend', out='T6_POP_R01_ASHRAM_VALLEY_v001.blend', terrain='T5_TERRAIN_VH',
               replace={'T5_VALLEY_SCATTER': ['SC_VH_BOULDERS', 'SC_VH_RIVER_STONES', 'SC_VH_RIVERBED_STONES', 'SC_L0_BOULDERS',
                                              'SC_L1_GROVES', 'SC_L1_FOREST_BELTS']},     # L0 groves → T6 Banj oak / deodar
               layers=[
                   L('AV_T04_BANJ_OAK', Density=.010, Min_Distance=8.0, Mask='m_grove', Mask_Min=.3, Mask_Max=.7, Avoid_Mask='m_bare', Slope_Max=32.0, excl=65),
                   L('AV_T05_RHODODENDRON', Density=.006, Min_Distance=5.0, Mask='m_grove', Mask_Min=.1, Mask_Max=.45, Avoid_Mask='m_bare', excl=65),
                   L('AV_T02_DEODAR', terrain='T5_TERRAIN_L0', Density=.0012, Min_Distance=10.0, Mask='m_grove', Mask_Min=.55, Mask_Max=.9,
                     Avoid_Mask='m_bare', note='cool grove cores on the valley sides (L0); TASK 05 has no m_forest near the Ashram', suffix='L0'),
                   L('AV_T02_DEODAR', terrain='T5_TERRAIN_L1', Density=.003, Min_Distance=9.0, Mask='m_forest', Mask_Min=.3, Mask_Max=.65,
                     Avoid_Mask='m_bare', note='forest belts (L1)', suffix='L1'),
                   L('AV_T03_CHIR_PINE', terrain='T5_TERRAIN_L0', Density=.0015, Min_Distance=12.0, Mask='m_one', Mask_Min=0.0, Mask_Max=.5,
                     Avoid_Mask='m_flow', Avoid_Strength=1.0, Avoid_Mask_2='m_grove', Avoid_Strength_2=.7, Slope_Min=3.0, Slope_Max=38.0,
                     note='dry convex slopes / ridges = low flow accumulation (TASK 05 has no m_dry in the valley)'),
                   L('AV_T04_BANJ_OAK', terrain='T5_TERRAIN_L0', Density=.006, Min_Distance=9.0, Mask='m_grove', Mask_Min=.3, Mask_Max=.7, Avoid_Mask='m_bare', suffix='L0'),
                   L('AV_T06_BAMBOO_CLUMP', Density=.0015, Min_Distance=14.0, Mask='m_wet', Mask_Min=.15, Mask_Max=.45, Avoid_Mask='m_path', excl=65),
                   L('AV_S01_BERBERIS', Density=.02, Min_Distance=2.5, Mask='m_grove', Mask_Min=.05, Mask_Max=.35, Avoid_Mask='m_bare', excl=55),
                   L('AV_G01_MEADOW_GRASS', Density=6.5, Min_Distance=.22, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_bare', Avoid_Mask_2='m_grove',
                     Avoid_Strength_2=.4, Cluster_Scale=5.0, Cluster_Amount=.45, excl=60),
                   L('PL_G02_DOOB_GRASS', Density=9.0, Min_Distance=.15, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_wet', excl=60, inside=1,
                     note='Ashram lawn (inside the wall, short grass) — PROPOSED'),
                   L('AV_G03_DRY_PATH_GRASS', Density=1.2, Min_Distance=.3, Mask='m_path', Mask_Min=.15, Mask_Max=.6, excl=60),
                   L('AV_G02B_KANS_GRASS_SPRING', Density=.06, Min_Distance=1.2, Mask='m_gravel', Mask_Min=.1, Mask_Max=.5, excl=65),
                   L('AV_F01_BUTTERCUP', Density=.25, Min_Distance=.3, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_bare', Avoid_Mask_2='m_dry',
                     Cluster_Scale=9.0, Cluster_Amount=.85, excl=60),
                   L('AV_F02_PRIMULA', Density=.06, Min_Distance=.4, Mask='m_grove', Mask_Min=.1, Mask_Max=.5, Cluster_Scale=7.0, Cluster_Amount=.8, excl=60),
                   L('AV_F03_WILD_DAISY', Density=.3, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_bare', Avoid_Mask_2='m_wet', Cluster_Scale=8.0,
                     Cluster_Amount=.88, excl=60),
                   L('AV_FE01_SWORD_FERN', Density=.12, Min_Distance=.8, Mask='m_grove', Mask_Min=.3, Mask_Max=.8, excl=60),
                   L('AV_AQ02_CATTAIL', Density=.04, Min_Distance=1.0, Mask='m_wet', Mask_Min=.5, Mask_Max=.8, Slope_Max=20.0),
                   L('AV_M01_MOSS_CUSHION', Density=.04, Min_Distance=.6, Mask='m_grove', Mask_Min=.5, Mask_Max=1.0, excl=60),
                   L('AV_MU01_BROWN_MUSHROOMS', Density=.01, Min_Distance=1.0, Mask='m_grove', Mask_Min=.5, Mask_Max=1.0, excl=60),
                   L('ND_L01_LEAF_LITTER_BROADLEAF', Density=.02, Min_Distance=1.5, Mask='m_grove', Mask_Min=.4, Mask_Max=1.0, excl=60),
                   L('ND_B01_FALLEN_BRANCHES', Density=.003, Min_Distance=4.0, Mask='m_grove', Mask_Min=.3, Mask_Max=1.0, excl=60)],
               ashram=True,
               exclude=['T5_FOREST_NORTH', 'T5_MOUNTAIN_NW', 'T5_WATERFALLS'],   # other regions 24–100 km away (memory: ~12 GB with them);
                                                                                 # the valley's own L1 / L2 tiles still give the horizon
               cams=[dict(name='T6_CAM_AV_COURTYARD_PEEPAL', at=(3, -64), look=(0, -8), h=2.2, th=6.0, lens=24),   # from the gate: garden beds flank the path
                     dict(name='T6_CAM_AV_GROVE_EDGE', target_mask='m_grove', near=(-450, 40), back=38, h=1.7, th=5.0, lens=28),
                     dict(name='T6_CAM_AV_MEADOW_LOW', target_mask='m_grove', near=(-700, -80), back=26, h=.45, th=2.0, lens=35)],
               t5_cams=['CAM_T5_07_GROUND_LEVEL']),
    'EF': dict(master='00_MASTER_WORLD/T5_REGION_R02_ENCHANTED_master_v002.blend', out='T6_POP_R02_ENCHANTED_FOREST_v001.blend', terrain='T5_TERRAIN_EH',
               replace={'T5_ENCHANTED_SCATTER': ['SC_EH_MOSSY_ROCKS', 'SC_EH_ROOTS_DEBRIS', 'SC_EN_ANCIENT_TREES', 'SC_EF_ANCIENT_TREES']},
               layers=[   # ~75 % natural / ~25 % approved fantasy (Decision 01 §3); measured by t6_pop_qc.py
                   L('EF_T01_GIANT_ELDER', Density=.0012, Min_Distance=30.0, Mask='m_forest', Mask_Min=.45, Mask_Max=.8, Avoid_Mask='m_bare', Cluster_Scale=300.0, Cluster_Amount=.9),
                   L('EF_T02_TEAL_BEECH', Density=.006, Min_Distance=9.0, Mask='m_forest', Mask_Min=.3, Mask_Max=.7, Avoid_Mask='m_bare'),
                   L('EF_T03_MOSS_OAK', Density=.004, Min_Distance=10.0, Mask='m_forest', Mask_Min=.3, Mask_Max=.7, Avoid_Mask='m_bare'),
                   L('EF_T04_YEW', Density=.005, Min_Distance=5.0, Mask='m_forest', Mask_Min=.2, Mask_Max=.6),
                   L('EF_T08_DEAD_SNAG', Density=.0008, Min_Distance=15.0, Mask='m_forest', Mask_Min=.3, Mask_Max=.7),
                   L('EF_T05_VEIL_WILLOW', Density=.009, Min_Distance=10.0, Mask='m_grove', Mask_Min=.3, Mask_Max=.7, note='glades (no pools on the hero tile)'),
                   L('EF_T06_SPIRAL_ROOT', Density=.0032, Min_Distance=12.0, Mask='m_forest', Mask_Min=.55, Mask_Max=.9, Cluster_Scale=120.0, Cluster_Amount=.85,
                     note='deep hollows (clustered)'),
                   L('EF_T07_LANTERN_TREE', Density=.005, Min_Distance=12.0, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_forest', Avoid_Strength=.6),
                   L('EF_FE01_GIANT_FERN', Density=.5, Min_Distance=.8, Mask='m_dry', Mask_Min=.1, Mask_Max=.6, Avoid_Mask='m_bare'),
                   L('EF_M01_MOSS_CARPET', Density=.12, Min_Distance=.9, Mask='m_forest', Mask_Min=.3, Mask_Max=1.0),
                   L('EF_MU01_GLOWCAP', Density=.01, Min_Distance=1.5, Mask='m_forest', Mask_Min=.5, Mask_Max=1.0, Cluster_Amount=.9),
                   L('EF_M02_GLOW_MOSS', Density=.006, Min_Distance=1.5, Mask='m_forest', Mask_Min=.5, Mask_Max=1.0, Cluster_Amount=.9),
                   L('AV_MU01_BROWN_MUSHROOMS', Density=.02, Min_Distance=1.0, Mask='m_forest', Mask_Min=.4, Mask_Max=1.0),
                   L('ND_B02_GIANT_LOG', Density=.0004, Min_Distance=25.0, Mask='m_forest', Mask_Min=.3, Mask_Max=.8, Slope_Max=22.0),
                   L('ND_L01_LEAF_LITTER_BROADLEAF', Density=.03, Min_Distance=1.5, Mask='m_forest', Mask_Min=.3, Mask_Max=1.0),
                   L('ND_B01_FALLEN_BRANCHES', Density=.004, Min_Distance=4.0, Mask='m_forest', Mask_Min=.3, Mask_Max=1.0),
                   L('ND_I01_GROUND_IVY', Density=.01, Min_Distance=2.0, Mask='m_forest', Mask_Min=.2, Mask_Max=.8)],
               cams=[dict(name='T6_CAM_EF_FOREST_FLOOR', target_mask='m_forest', near='CAM_T5_10_ENCHANTED_FLOOR+120', back=30, h=1.7, th=8.0, lens=22),
                     dict(name='T6_CAM_EF_GLADE', target_mask='m_grove', near='CAM_T5_10_ENCHANTED_FLOOR+400', back=35, h=1.7, th=6.0, lens=24)],
               t5_cams=['CAM_T5_10_ENCHANTED_FLOOR']),
    'MK': dict(master='00_MASTER_WORLD/T5_REGION_R03_RANGE_master_v002.blend', out='T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend', terrain='T5_TERRAIN_CV',
               replace={'T5_RANGE_SCATTER': ['SC_CV_STONES', 'SC_CV_ROCKFALL', 'SC_R3N_TALUS_BOULDERS', 'SC_R3N_CONIFERS']},
               layers=[   # zone M1 (~2 000 m, cave-entrance tile): spruce + silver fir forest, blue pine in clearings, Burans, birch in gullies
                   L('MK_T01_HIMALAYAN_SPRUCE', Density=.006, Min_Distance=8.0, Mask='m_forest', Mask_Min=.25, Mask_Max=.6, Avoid_Mask='m_bare', Avoid_Mask_2='m_grove',
                     **{'Camera Clearance (m)': 18.0}),
                   L('MK_T04_SILVER_FIR', Density=.003, Min_Distance=8.0, Mask='m_forest', Mask_Min=.35, Mask_Max=.7, Avoid_Mask='m_bare', **{'Camera Clearance (m)': 18.0}),
                   L('MK_T05_BLUE_PINE', Density=.002, Min_Distance=10.0, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_forest', Avoid_Strength=.7,
                     Avoid_Mask_2='m_scree', **{'Camera Clearance (m)': 14.0}),
                   L('AV_T05_RHODODENDRON', Density=.004, Min_Distance=5.0, Mask='m_forest', Mask_Min=.1, Mask_Max=.4, **{'Camera Clearance (m)': 8.0}),
                   L('MK_T02_HIMALAYAN_BIRCH', Density=.002, Min_Distance=6.0, Mask='m_flow', Mask_Min=.75, Mask_Max=1.0, note='gullies / stream lines'),
                   L('MK_G01_ALPINE_TUSSOCK', Density=3.0, Min_Distance=.3, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_forest', Avoid_Mask_2='m_scree'),
                   L('AV_G01_MEADOW_GRASS', Density=3.0, Min_Distance=.25, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_forest', Avoid_Strength=.8),
                   L('AV_F02_PRIMULA', Density=.08, Min_Distance=.4, Mask='m_one', Mask_Min=0.0, Mask_Max=.5, Avoid_Mask='m_forest', Cluster_Amount=.85),
                   L('AV_FE01_SWORD_FERN', Density=.1, Min_Distance=.8, Mask='m_forest', Mask_Min=.1, Mask_Max=.6),
                   L('AV_M01_MOSS_CUSHION', Density=.05, Min_Distance=.6, Mask='m_forest', Mask_Min=.3, Mask_Max=1.0),
                   L('ND_L02_NEEDLE_LITTER', Density=.03, Min_Distance=1.5, Mask='m_forest', Mask_Min=.25, Mask_Max=1.0),
                   L('ND_B01_FALLEN_BRANCHES', Density=.003, Min_Distance=4.0, Mask='m_forest', Mask_Min=.3, Mask_Max=1.0)],
               cams=[dict(name='T6_CAM_MK_FOREST_EDGE', target_mask='m_forest', near='CAM_T5_12_CAVE_ENTRANCE+160', back=40, h=1.7, th=10.0, lens=24)],
               t5_cams=['CAM_T5_12_CAVE_ENTRANCE']),
    'DS': dict(master='00_MASTER_WORLD/T5_REGION_R04_DESERT_master_v002.blend', out='T6_POP_R04_GOLDEN_DESERT_v001.blend', terrain='T5_TERRAIN_DH',
               replace={'T5_DESERT_R04_SCATTER': ['SC_DH_CLIFF_BLOCKS', 'SC_DH_PAVEMENT_STONES', 'SC_DH_TALUS_BOULDERS', 'SC_DN_CLIFF_BLOCKS', 'SC_DN_TALUS_BOULDERS']},
               layers=[   # TASK 05 masks: hero tile DH = dune field (m_dry) + interdune gravel pavement (m_gravel) + rock outcrops (m_rock);
                          # wadis = dry drainage lines m_flow on the 24 km DN tile; NO oasis water in TASK 05 → date palms are not placed
                   L('DS_G01_SEWAN_GRASS', Density=.03, Mask='m_gravel', Mask_Min=.2, Mask_Max=.7, Cluster_Scale=12.0, Cluster_Amount=.7),
                   L('FB_S01_DEAD_THORN_SHRUB', Density=.001, Min_Distance=5.0, Mask='m_gravel', Mask_Min=.2, Mask_Max=.7),
                   L('DS_S01_CALOTROPIS', Density=.0015, Min_Distance=5.0, Mask='m_gravel', Mask_Min=.3, Mask_Max=.8),
                   L('DS_S02_EUPHORBIA', Density=.003, Min_Distance=3.0, Mask='m_rock', Mask_Min=.2, Mask_Max=.8, Slope_Max=45.0),
                   L('DS_T01_KHEJRI', Density=.0001, Min_Distance=40.0, Mask='m_gravel', Mask_Min=.3, Mask_Max=.8,
                     note='≤ 1 tree / ha outside wadis (Bible §4.7)'),
                   L('DS_T01_KHEJRI', terrain='T5_TERRAIN_DN', Density=.0004, Min_Distance=18.0, Mask='m_flow', Mask_Min=.75, Mask_Max=.9, Avoid_Mask='m_pad', Avoid_Mask_2='m_dry', Avoid_Strength_2=.8,
                     note='wadi trees on the DN tile', suffix='WADI'),
                   L('PL_T03_UMBRELLA_ACACIA', terrain='T5_TERRAIN_DN', Density=.0003, Min_Distance=18.0, Mask='m_flow', Mask_Min=.72, Mask_Max=.88,
                     Avoid_Mask='m_pad', Avoid_Mask_2='m_dry', Avoid_Strength_2=.8, suffix='WADI'),
                   L('PL_S01_BER_BUSH', terrain='T5_TERRAIN_DN', Density=.0015, Min_Distance=5.0, Mask='m_flow', Mask_Min=.65, Mask_Max=.85, Avoid_Mask='m_pad', Avoid_Mask_2='m_dry', Avoid_Strength_2=.8, suffix='WADI'),
                   L('DS_S01_CALOTROPIS', terrain='T5_TERRAIN_DN', Density=.002, Min_Distance=4.0, Mask='m_flow', Mask_Min=.6, Mask_Max=.85, Avoid_Mask='m_pad', Avoid_Mask_2='m_dry', Avoid_Strength_2=.8, suffix='WADI'),
                   L('DS_G01_SEWAN_GRASS', terrain='T5_TERRAIN_DN', Density=.04, Mask='m_flow', Mask_Min=.55, Mask_Max=.85, Avoid_Mask='m_pad', Avoid_Mask_2='m_dry', Avoid_Strength_2=.8, suffix='WADI'),
                   L('DS_S02_EUPHORBIA', terrain='T5_TERRAIN_DN', Density=.003, Min_Distance=3.0, Mask='m_scree', Mask_Min=.2, Mask_Max=.8, Slope_Max=45.0, suffix='WADI')],
               cams=[dict(name='T6_CAM_DS_WADI', target_mask='m_flow', tmin=.75, terrain='T5_TERRAIN_DN', near=(0, 2600), back=40, h=1.7, th=4.0, lens=28),
                     dict(name='T6_CAM_DS_INTERDUNE', target_mask='m_gravel', near=(-100, 44), back=30, h=1.6, th=1.5, lens=30)],
               t5_cams=['CAM_T5_05_DESERT']),
    'FB': dict(master='00_MASTER_WORLD/T5_REGION_R05_FORBIDDEN_master_v002.blend', out='T6_POP_R05_FORBIDDEN_LANDS_v001.blend', terrain='T5_TERRAIN_XH',
               replace={'T5_FORBIDDEN_R05_SCATTER': ['SC_DH_CLIFF_BLOCKS', 'SC_DH_EJECTA_BLOCKS', 'SC_DH_EJECTA_RUBBLE', 'SC_DH_PAVEMENT_STONES', 'SC_DH_TALUS_BOULDERS',
                                                     'SC_DN_CLIFF_BLOCKS', 'SC_DN_EJECTA_BLOCKS', 'SC_DN_TALUS_BOULDERS']},
               layers=[   # almost lifeless; outer rim only (m_grove = the TASK 05 dead-tree zone)
                   L('FB_T01_CHARRED_SNAG', Density=.0025, Min_Distance=10.0, Mask='m_grove', Mask_Min=.2, Mask_Max=.6),
                   L('FB_S01_DEAD_THORN_SHRUB', Density=.003, Min_Distance=3.0, Mask='m_grove', Mask_Min=.1, Mask_Max=.6),
                   L('FB_G01_HARDY_GRASS', Density=.04, Min_Distance=1.0, Mask='m_grove', Mask_Min=.15, Mask_Max=.6, Avoid_Mask='m_wet'),
                   L('FB_M01_ASH_LICHEN', Density=.02, Min_Distance=1.0, Mask='m_rock', Mask_Min=.2, Mask_Max=.8, Avoid_Mask='m_wet')],
               cams=[dict(name='T6_CAM_FB_RIM_DEAD_TREES', target_mask='m_grove', near='CAM_T5_09_FORBIDDEN_RIM+200', back=35, h=1.7, th=5.0, lens=26)],
               t5_cams=['CAM_T5_09_FORBIDDEN_RIM']),
}


def kind_of(name):
    if name.startswith('ND_'):
        return 'detail'
    if any(t['name'] == name for t in RG.TREES):
        return 'tree'
    if any(t['name'] == name for t in RG.SHRUBS):
        return 'shrub'
    return 'plant'


def link_objects(path, names):
    if not os.path.exists(path):
        return {}
    with bpy.data.libraries.load(path, link=True, relative=True) as (src, dst):
        avail = set(src.objects)
        dst.objects = [n for n in names if n in avail]
    return {o.name: o for o in dst.objects if o is not None}


def band_collections(asset, parent):
    """ECO_<asset>_NEAR (hero + V1 + V2), _MID (LOD1), _FAR (LOD2), _HORIZON (LOD3 impostor; plants: LOD1)."""
    if f'ECO_{asset}_NEAR' in bpy.data.collections:
        return ({k: bpy.data.collections[f'ECO_{asset}_{k}'] for k in ('NEAR', 'MID', 'FAR', 'HORIZON')},
                bpy.data.objects[f'{asset}_SC'])
    reg = RG.NAMES[RG.region_of(asset)]
    hero = link_objects(os.path.join(LIB, f'T6_VEG_{reg}_v001.blend'), [f'{asset}_SC'])
    var = link_objects(os.path.join(LIB, f'T6_VEG_{reg}_VARIANTS_v001.blend'), [f'{asset}_V1_SC', f'{asset}_V2_SC'])
    lod = link_objects(os.path.join(LIB, f'T6_VEG_{reg}_LODS_v001.blend'), [f'{asset}_LOD1_SC', f'{asset}_LOD2_SC', f'{asset}_LOD3_SC'])
    h = hero.get(f'{asset}_SC')
    assert h is not None, f'{asset}_SC missing in the library (rebuild it with t6_build_library.py)'
    near = [h] + [o for o in var.values()]
    l1 = lod.get(f'{asset}_LOD1_SC') or h
    l2 = lod.get(f'{asset}_LOD2_SC') or l1
    l3 = lod.get(f'{asset}_LOD3_SC') or l2
    out = {}
    for k, objs in (('NEAR', near), ('MID', [l1]), ('FAR', [l2]), ('HORIZON', [l3])):
        c = bpy.data.collections.new(f'ECO_{asset}_{k}'); parent.children.link(c)
        for o in objs:
            c.objects.link(o)
        out[k] = c
    return out, h


def terrain_arrays(name):
    o = bpy.data.objects[name]; dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    V = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
    A = {}
    for a in me.attributes:
        if a.name.startswith('m_') and a.domain == 'POINT' and a.data_type == 'FLOAT':
            arr = np.empty(len(me.vertices), np.float32); a.data.foreach_get('value', arr); A[a.name] = arr
    oe.to_mesh_clear()
    return V + np.array(o.matrix_world.translation, np.float32), A


def ground_z(V, x, y):
    d = (V[:, 0] - x) ** 2 + (V[:, 1] - y) ** 2; i = np.argpartition(d, 4)[:4]
    w = 1 / (np.sqrt(d[i]) + .05); return float((V[i, 2] * w).sum() / w.sum())


def instance_positions(layer_objs, kinds=('tree', 'shrub')):
    """evaluate the layers with open culling (in memory) → world positions of the generated woody instances."""
    keep = {}
    for o in layer_objs:
        if o.get('t6_kind') not in kinds:
            continue
        md = o.modifiers['T6_ECOSYSTEM']; I = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
        keep[o.name] = (md, I, md[I['Viewport Density']], md[I['Cull Angle']], md[I['Cull Distance']])
        md[I['Viewport Density']] = 1.0; md[I['Cull Angle']] = 180.0; md[I['Cull Distance']] = 8000.0; o.update_tag()
    bpy.context.view_layer.update()                     # modifier ID-property edits do not tag the object by themselves
    dg = bpy.context.evaluated_depsgraph_get(); P = []
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent and inst.parent.original.name in keep:
            P.append(tuple(inst.matrix_world.translation))
    for n, (md, I, vd, ca, cd) in keep.items():
        md[I['Viewport Density']] = vd; md[I['Cull Angle']] = ca; md[I['Cull Distance']] = cd; bpy.data.objects[n].update_tag()
    bpy.context.view_layer.update()
    return np.array(P) if P else np.zeros((0, 3))


def t5_ahead(cam_name, dist):
    """a point `dist` metres in front of an approved TASK 05 camera (same frame as its terrain tile)."""
    c = bpy.data.objects[cam_name]; f = c.matrix_world.to_3x3() @ Vector((0, 0, -1)); f.z = 0; f.normalize()
    q = c.matrix_world.translation + f * float(dist); return (q.x, q.y)


def make_cam(spec, V, A, terrain, P):
    """eye-level camera: target = the densest group of generated trees / shrubs near spec['near']; camera `back` metres away on
    open, gentle ground with a clear line of sight (terrain ray test) — so every preview really shows the vegetation."""
    cam = bpy.data.objects.new(spec['name'], bpy.data.cameras.new(spec['name'])); cam.data.lens = spec.get('lens', 28)
    cam.data.clip_start = .05; cam.data.clip_end = 30000
    te = terrain.evaluated_get(bpy.context.evaluated_depsgraph_get()); inv = te.matrix_world.inverted()
    def clear(a, b):
        d = Vector(b) - Vector(a); L = d.length
        hit, loc, *_ = te.ray_cast(inv @ Vector(a), (inv.to_3x3() @ d).normalized(), distance=L * .97)
        return not hit
    if 'at' in spec:
        p = spec['at']; t = spec['look']
    else:
        cx, cy = spec['near'] if not isinstance(spec['near'], str) else t5_ahead(*spec['near'].split('+'))
        # target = the centre of the densest patch of the vegetation mask near (cx, cy) — a mask is resolution-independent,
        # scatter points are not (the terrain is coarser in the viewport than in the render)
        m = A.get(spec.get('target_mask', 'm_one')); bs = 20.0
        if m is None:
            t = (cx, cy)
        else:                       # grid over the WHOLE tile; densest mask patch, gently preferring patches near (cx, cy)
            gx0, gy0 = V[:, 0].min(), V[:, 1].min()
            gx = np.floor((V[:, 0] - gx0) / bs).astype(int); gy = np.floor((V[:, 1] - gy0) / bs).astype(int)
            Hm = np.zeros((gx.max() + 1, gy.max() + 1)); tm = spec.get('tmin', .3)
            np.add.at(Hm, (gx, gy), np.clip((m - tm) / max(1 - tm, .1) * 1.6, 0, 1) * (1 - A.get('m_dry', np.zeros_like(m)) * .8))
            Hs = sum(np.roll(np.roll(Hm, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1))           # 60 m box sum
            ii, jj = np.mgrid[0:Hs.shape[0], 0:Hs.shape[1]]
            dist = np.hypot(gx0 + (ii + .5) * bs - cx, gy0 + (jj + .5) * bs - cy)
            score = Hs - .0006 * dist * max(Hs.max(), 1e-6)
            i, j = np.unravel_index(np.argmax(score), score.shape)
            t = (gx0 + (i + .5) * bs, gy0 + (j + .5) * bs)
        best = None
        x0, y0, x1, y1 = V[:, 0].min() + 25, V[:, 1].min() + 25, V[:, 0].max() - 25, V[:, 1].max() - 25
        for back in (spec['back'], spec['back'] * 1.5, spec['back'] * .7):
            for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):
                px, py = t[0] + math.cos(a) * back, t[1] + math.sin(a) * back
                if not (x0 < px < x1 and y0 < py < y1):                 # stay on THIS tile (its heights are the ones we know)
                    continue
                jn = np.argmin((V[:, 0] - px) ** 2 + (V[:, 1] - py) ** 2)
                if (V[jn, 0] - px) ** 2 + (V[jn, 1] - py) ** 2 > 60 ** 2:  # inside a nested-LOD hole of the tile → skip
                    continue
                j = np.argmin((V[:, 0] - px) ** 2 + (V[:, 1] - py) ** 2)
                pz = ground_z(V, px, py) + spec.get('h', 1.7); tz = ground_z(V, *t) + spec.get('th', 3.0)
                if not clear((px, py, pz), (t[0], t[1], tz)):
                    continue
                score = sum(float(A[k][j]) for k in ('m_forest', 'm_grove') if k in A) + 5 * sum(float(A[k][j]) for k in ('m_wet', 'm_bare', 'm_pad', 'm_cliff') if k in A)
                if best is None or score < best[0]:
                    best = (score, (px, py))
            if best:
                break
        p = best[1] if best else (t[0] - spec['back'], t[1])
    # eye height above the HIGHEST ground within 15 m: the background evaluation is at viewport resolution, rugged terrain (crater rim,
    # talus) is metres higher in the render-resolution mesh → never put the lens under the real surface
    d2c = (V[:, 0] - p[0]) ** 2 + (V[:, 1] - p[1]) ** 2; near_v = V[d2c < 15 ** 2]
    zmax = float(near_v[:, 2].max()) if len(near_v) else ground_z(V, *p)
    pz = max(ground_z(V, *p), zmax) + spec.get('h', 1.7); tz = ground_z(V, *t) + spec.get('th', 3.0)
    cam.location = (p[0], p[1], pz)
    cam.rotation_euler = (Vector((t[0], t[1], tz)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    return cam


def chabutra(V, coll):
    """PROPOSED Peepal sitting platform (Decision 01 §4: sitting area APPROVED, design PROPOSED): 9 × 9 m, 0.6 m, one step ring."""
    z0 = min(ground_z(V, x, y) for x in (-5.5, 0, 5.5) for y in (-5.5, 0, 5.5))
    mat = K.mat_ground('MAT_T6_CHABUTRA_STONE', 'rustic_stone_wall', 1.6, '#C8C0B0')
    objs = []
    for nm, half, top in (('STEP', 5.5, .3), ('PLATFORM', 4.5, .6)):
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= half * 2; v.co.y *= half * 2; v.co.z = (top if v.co.z > 0 else -.8)
        me = bpy.data.meshes.new(f'T6_PEEPAL_CHABUTRA_{nm}_PROPOSED'); bm.to_mesh(me); bm.free(); me.materials.append(mat)
        o = bpy.data.objects.new(me.name, me); o.location = (0, 0, z0); coll.objects.link(o); objs.append(o)
    return z0 + .6


def garden_beds(V, coll):
    """PROPOSED Ashram garden (plan §B): two raised beds 22 × 22 m flanking the gate path (x ±6…±28, y −30…−52), 0.25 m high, soil top."""
    mat = K.mat_ground('MAT_T6_GARDEN_SOIL', 'brown_mud', 1.2, '#B0A08C'); beds = []
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 6, sx * 28)); y0, y1 = -52, -30
        n = 23; xs = np.linspace(x0, x1, n); ys = np.linspace(y0, y1, n)
        verts = [(x, y, ground_z(V, x, y) + .25) for y in ys for x in xs]
        faces = [(j * n + i, j * n + i + 1, (j + 1) * n + i + 1, (j + 1) * n + i) for j in range(n - 1) for i in range(n - 1)]
        me = bpy.data.meshes.new(f'T6_ASHRAM_GARDEN_BED_{"W" if sx < 0 else "E"}_PROPOSED'); me.from_pydata(verts, [], faces)
        a = me.attributes.new('m_one', 'FLOAT', 'POINT'); a.data.foreach_set('value', np.ones(len(verts), np.float32))
        # rows: marigold mask = 5 rows across the bed (0.6 m wide); tulsi strip = 1 m along the path edge
        row = me.attributes.new('m_rows', 'FLOAT', 'POINT'); tul = me.attributes.new('m_tulsi', 'FLOAT', 'POINT')
        rv = []; tv = []
        for (x, y, z) in verts:
            u = (abs(x) - 6) / 22.0
            rv.append(1.0 if (.12 < u < .95 and abs(((y - y0) / 22.0 * 5) % 1 - .5) < .17) else 0.0)
            tv.append(1.0 if (abs(x) - 6) < 1.2 and abs(((y - y0) / 22.0 * 3) % 1 - .5) < .1 else 0.0)
        row.data.foreach_set('value', np.array(rv, np.float32)); tul.data.foreach_set('value', np.array(tv, np.float32))
        me.materials.append(mat); me.update()
        o = bpy.data.objects.new(me.name, me); coll.objects.link(o)
        bm = bmesh.new(); bm.from_mesh(me)                      # bed walls down to the ground (raised kyari edge)
        boundary = [e for e in bm.edges if e.is_boundary]
        ext = bmesh.ops.extrude_edge_only(bm, edges=boundary)
        for v in [g for g in ext['geom'] if isinstance(g, bmesh.types.BMVert)]:
            v.co.z -= .45
        bm.to_mesh(me); bm.free(); beds.append(o)
    return beds


def layer(spec, terrain, ctrl, coll_layers, coll_assets, terrain_obj=None):
    asset = spec['asset']; kind = kind_of(asset); d = dict(KD[kind])
    bands, hero = band_collections(asset, coll_assets)
    nm = f"ECO_{asset}" + (f"_{spec['suffix']}" if spec.get('suffix') else '')
    if spec.get('terrain'):
        terrain_obj = bpy.data.objects[spec['terrain']]
    me = bpy.data.meshes.new(nm); o = bpy.data.objects.new(nm, me); coll_layers.objects.link(o)
    md = o.modifiers.new('T6_ECOSYSTEM', 'NODES'); md.node_group = E.ecosystem_group()
    H = float(hero.get('t6_height_m', 1.0))
    kw = dict(Terrain=terrain_obj or terrain, Near=bands['NEAR'], Mid=bands['MID'], Far=bands['FAR'], Horizon=bands['HORIZON'],
              Viewport_Density=.05 if kind in ('plant', 'detail') else .2, Seed=sum(map(ord, asset)) * 31 % 9973)   # stable seed per layer
    for k, v in d.items():
        if k in ('L01', 'L12', 'L23', 'Realize'):
            continue
        kw[k] = v
    kw.update({'LOD0→1': d['L01'], 'LOD1→2': d['L12'], 'LOD2→3': d['L23'], 'Realize Distance': d['Realize']})
    kw['Camera Clearance (m)'] = kw.pop('Camera_Clearance')
    for k, v in spec.items():
        if k in ('asset', 'excl', 'inside', 'note', 'terrain', 'suffix'):
            continue
        kw[k] = v
    if kind in ('plant', 'detail'):
        kw['Min_Distance'] = 0.0          # random distribution for ground layers (see NG_T6_ECOSYSTEM)
    # wind: the asset's own amplitudes (library t6_wind_*), natural frequency ≈ 4 / H, instance sway for the far tilt
    kw.update({'Trunk Sway (m)': float(hero.get('t6_wind_trunk', .02 * H)), 'Branch Sway (m)': float(hero.get('t6_wind_branch', .3)),
               'Leaf Flutter (m)': float(hero.get('t6_wind_leaf', .03)), 'Natural Freq (Hz)': float(hero.get('t6_wind_fn', min(max(4 / max(H, .05), .15), 2.5))),
               'Damping': float(hero.get('t6_wind_damping', .15)), 'Plant Height (m)': max(H, .05),
               'Instance Sway (m)': float(hero.get('t6_wind_trunk', 0.0)) or .12 * H, 'Bend Offset (m)': .5 if kind in ('tree', 'shrub') else .03,
               'Gust Size (m)': 45.0 if kind == 'tree' else 12.0})
    if kind == 'detail':
        kw.update({'Trunk Sway (m)': 0.0, 'Branch Sway (m)': float(hero.get('t6_wind_branch', 0.0)), 'Instance Sway (m)': 0.0})
    if spec.get('excl'):
        kw['Exclude Object'] = bpy.data.objects['T6_ASHRAM_ZONE_PROPOSED']; kw['Exclude Radius'] = float(spec['excl'])
        kw['Keep Only Inside'] = float(spec.get('inside', 0))
    E.set_inputs(md, **{k.replace('_', ' ') if k not in ('Viewport_Density',) else 'Viewport Density': v for k, v in kw.items()})
    E.drive_wind(o, md, ctrl)
    o['t6_layer'] = asset; o['t6_kind'] = kind; o['t6_label'] = str(hero.get('t6_label', '')); o['t6_note'] = spec.get('note', '')
    return o


def main():
    R = REGIONS[REG]
    bpy.ops.wm.open_mainfile(filepath=os.path.join(W3, R['master']))
    out = os.path.join(OUTD, R['out'])
    bpy.ops.wm.save_as_mainfile(filepath=out, relative_remap=True)          # from here on only the NEW file is written
    sc = bpy.context.scene; sc.name = f'T6_POP_{REG}'
    vl = bpy.context.view_layer
    # ---- T5 vegetation replaced by T6: exclude the linked scatter collection, re-link the kept T5 scatter objects
    def find_lc(lc, name):
        if lc.name == name:
            return lc
        for ch in lc.children:
            r = find_lc(ch, name)
            if r:
                return r
    kept = bpy.data.collections.new('T5_SCATTER_KEPT (rocks / river stones / far forest mass)'); sc.collection.children.link(kept)
    for cname in R.get('exclude', []):
        lc = find_lc(vl.layer_collection, cname)
        if lc:
            lc.exclude = True
    for cname, keep in R['replace'].items():
        lc = find_lc(vl.layer_collection, cname)
        if lc:
            lc.exclude = True
        for n in keep:
            if n in bpy.data.objects:
                kept.objects.link(bpy.data.objects[n])
    # ---- T6 collections
    root = bpy.data.collections.new(f'T6_ECOSYSTEM_{RG.NAMES[REG]}'); sc.collection.children.link(root)
    layers = bpy.data.collections.new('T6_LAYERS'); root.children.link(layers)
    assets = bpy.data.collections.new('T6_ASSET_BANDS (linked, hidden)'); root.children.link(assets)
    marks = bpy.data.collections.new('T6_LANDMARKS + PROPOSED'); root.children.link(marks)
    cams = bpy.data.collections.new('T6_CAMERAS'); root.children.link(cams)
    find_lc(vl.layer_collection, assets.name).exclude = True
    ctrl = K.wind_control(); ctrl['strength'] = 1.2; ctrl['gust'] = .5
    if ctrl.name not in root.objects:
        for c in ctrl.users_collection:
            c.objects.unlink(ctrl)
        root.objects.link(ctrl)
    terrain = bpy.data.objects[R['terrain']]
    V, A = terrain_arrays(R['terrain'])
    print('TERRAIN', R['terrain'], len(V), 'verts, masks', sorted(A), flush=True)
    if R.get('ashram'):
        zone = bpy.data.objects.new('T6_ASHRAM_ZONE_PROPOSED', None); zone.empty_display_type = 'CIRCLE'; zone.empty_display_size = 60
        zone.location = (0, 0, ground_z(V, 0, 0)); marks.objects.link(zone)
        top = chabutra(V, marks)
        lib = os.path.join(LIB, 'T6_VEG_ASHRAM_VALLEY_v001.blend')
        with bpy.data.libraries.load(lib, link=True, relative=True) as (src, dst):
            dst.collections = ['T6_AV_T01_PEEPAL']
        pe = bpy.data.objects.new('T6_LANDMARK_PEEPAL (ONE, APPROVED; exact spot PROPOSED)', None); pe.instance_type = 'COLLECTION'
        pe.instance_collection = dst.collections[0]; pe.location = (0, 0, top - .35); marks.objects.link(pe)
        beds = garden_beds(V, marks)
        for bed in beds:
            for asset, mask, dens, mdist in (('AV_F04_MARIGOLD', 'm_rows', 5.0, .32),):
                lo = layer(dict(asset=asset, Density=dens, Min_Distance=mdist, Mask=mask, Mask_Min=.4, Mask_Max=.6, Slope_Max=60.0,
                                note='Ashram garden ONLY (Decision 01 §4) — PROPOSED bed layout'), terrain, ctrl, layers, assets, terrain_obj=bed)
                lo.name = f'ECO_{asset}_{bed.name[-12:]}'
        # Tulsi: exactly 3 plants per bed along the path edge (landscaping plan §B) — explicit instances of the hero (with its wind)
        with bpy.data.libraries.load(lib, link=True, relative=True) as (src, dst):
            dst.collections = ['T6_AV_S02_TULSI']
        for sx in (-1, 1):
            for k, yv in enumerate((-35.5, -41.0, -46.5)):
                x = sx * 7.2; t_ = bpy.data.objects.new(f'T6_ASHRAM_GARDEN_TULSI_{"W" if sx < 0 else "E"}{k + 1} (APPROVED: garden only)', None)
                t_.instance_type = 'COLLECTION'; t_.instance_collection = dst.collections[0]
                t_.location = (x, yv, ground_z(V, x, yv) + .25); t_.rotation_euler = (0, 0, k * 2.1 + sx); marks.objects.link(t_)
    for spec in R['layers']:
        o = layer(spec, terrain, ctrl, layers, assets); print('LAYER', o.name, flush=True)
    P = instance_positions([o for o in layers.objects], kinds=('tree',))          # cameras look at TREES first …
    if len(P) < 10:
        P = instance_positions([o for o in layers.objects])                       # … shrubs too where trees are rare
    print('WOODY INSTANCES (open culling)', len(P), flush=True)
    TA = {R['terrain']: (V, A)}
    for cs in R['cams']:
        tn = cs.get('terrain', R['terrain'])
        if tn not in TA:
            TA[tn] = terrain_arrays(tn)
        c = make_cam(cs, *TA[tn], bpy.data.objects[tn], P); cams.objects.link(c); print('CAM', c.name, tuple(round(v, 1) for v in c.location), flush=True)
    sc.camera = bpy.data.objects[R['cams'][0]['name']]
    sc['t6_preview_cameras'] = [c['name'] for c in R['cams']] + R.get('t5_cams', [])
    sc.render.fps = 24; sc.frame_start, sc.frame_end = 1, 240
    for f, st in ((1, 1.0), (120, 2.2), (240, 1.4)):                        # a gentle spring breeze with one stronger gust
        ctrl['strength'] = st; ctrl.keyframe_insert('["strength"]', frame=f)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, relative_remap=True, compress=True)
    print('SAVED', out, round(os.path.getsize(out) / 1e6, 2), 'MB', len(layers.objects), 'layers', flush=True)
    print('T6_POPULATE_DONE', REG)


main()

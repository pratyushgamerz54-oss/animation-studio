# TASK 05 — Technical QC report (milestone 1)

Automated by `scripts/t5_qc.py` in **Blender 4.5.16 LTS** · 2026-11-21 12:28 · **56/56 PASS**

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | file size < 100 MB: 11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend | ✅ PASS | 0.9 MB |
| 2 | opens + no missing images: 11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend | ✅ PASS | 77 images, missing [] |
| 3 | PBR channels (Base Color / Roughness / Normal, Metallic 0) on every terrain material | ✅ PASS | all OK |
| 4 | texture resolution = 2K (2048²) for all Poly Haven maps | ✅ PASS | [[2048, 2048]] |
| 5 | file size < 100 MB: 14_NATURE_LIBRARY/T5_NATURE_LIBRARY_TREES_v002.blend | ✅ PASS | 59.7 MB |
| 6 | opens + no missing images: 14_NATURE_LIBRARY/T5_NATURE_LIBRARY_TREES_v002.blend | ✅ PASS | 73 images, missing [] |
| 7 | file size < 100 MB: 14_NATURE_LIBRARY/T5_NATURE_LIBRARY_GROUND_v002.blend | ✅ PASS | 44.4 MB |
| 8 | opens + no missing images: 14_NATURE_LIBRARY/T5_NATURE_LIBRARY_GROUND_v002.blend | ✅ PASS | 96 images, missing [] |
| 9 | file size < 100 MB: 08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend | ✅ PASS | 0.2 MB |
| 10 | opens + no missing images: 08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend | ✅ PASS | 203 images, missing [] |
| 11 | file size < 100 MB: 04_FORESTS/FOREST_NORTH_BELT_v002.blend | ✅ PASS | 0.2 MB |
| 12 | opens + no missing images: 04_FORESTS/FOREST_NORTH_BELT_v002.blend | ✅ PASS | 211 images, missing [] |
| 13 | file size < 100 MB: 03_MOUNTAINS/MOUNTAIN_NW01_v002.blend | ✅ PASS | 0.2 MB |
| 14 | opens + no missing images: 03_MOUNTAINS/MOUNTAIN_NW01_v002.blend | ✅ PASS | 164 images, missing [] |
| 15 | file size < 100 MB: 05_RIVERS_AND_LAKES/WATER_v002.blend | ✅ PASS | 11.2 MB |
| 16 | opens + no missing images: 05_RIVERS_AND_LAKES/WATER_v002.blend | ✅ PASS | 0 images, missing [] |
| 17 | file size < 100 MB: 00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend | ✅ PASS | 0.1 MB |
| 18 | opens + no missing images: 00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend | ✅ PASS | 262 images, missing [] |
| 19 | terrain VH: real mesh evaluates (viewport grid 301², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 91801 verts, z 704.6 max (data 704.6), attrs 14 |
| 20 | terrain L0: real mesh evaluates (viewport grid 361², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 127008 verts, z 755.3 max (data 755.4), attrs 14 |
| 21 | terrain L1: real mesh evaluates (viewport grid 401², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 157136 verts, z 922.4 max (data 923.2), attrs 14 |
| 22 | terrain L2: real mesh evaluates (viewport grid 481², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 217079 verts, z 6417.6 max (data 6514.4), attrs 14 |
| 23 | terrain FH: real mesh evaluates (viewport grid 376², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 142876 verts, z 858.7 max (data 858.7), attrs 14 |
| 24 | terrain MT: real mesh evaluates (viewport grid 401², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 162400 verts, z 6088.4 max (data 6088.4), attrs 14 |
| 25 | terrain WF: real mesh evaluates (viewport grid 211², z within data range incl. skirt, 14 mask attributes) | ✅ PASS | 45361 verts, z 3740.0 max (data 3740.0), attrs 14 |
| 26 | LOD seam VH↔L0: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 0.00 m (skirt 3 m), mean 0.000 m |
| 27 | LOD seam L0↔L1: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 0.00 m (skirt 12 m), mean 0.000 m |
| 28 | LOD seam FH↔L1: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 0.00 m (skirt 3 m), mean 0.000 m |
| 29 | LOD seam L1↔L2: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 0.00 m (skirt 40 m), mean 0.000 m |
| 30 | LOD seam MT↔L2: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 12.19 m (skirt 60 m), mean 0.055 m |
| 31 | LOD seam WF↔MT: border matches the parent surface (crack < skirt) | ✅ PASS | max gap 0.00 m (skirt 4 m), mean 0.000 m |
| 32 | approved v001 heights reproduced (valley, before detail) | ✅ PASS | 3.05e-05 m |
| 33 | valley river levels unchanged vs v001 | ✅ PASS | {'max_all_m': 926.633247708874, 'max_in_valley_L1_m': 7.29953922018467e-05} |
| 34 | rivers never flow uphill (water surface monotonic downstream) | ✅ PASS | max rise 0.0000 m over 96 rivers |
| 35 | water surface above the river bed in VH | ✅ PASS | 480 centreline samples, 0.00% bed above water |
| 36 | water surface above the river bed in FH | ✅ PASS | 601 centreline samples, 0.00% bed above water |
| 37 | water surface above the river bed in WF | ✅ PASS | 793 centreline samples, 0.00% bed above water |
| 38 | water surface above the river bed in L0 | ✅ PASS | 4842 centreline samples, 0.02% bed above water |
| 39 | lake: water-plane edges lie under the terrain (shoreline = terrain ∩ level) | ✅ PASS | 99.4% of 659 edge vertices covered |
| 40 | scatter produces instances (CAM_T5_02_FOREST_ESTABLISHING) | ✅ PASS | {'SC_L1_GROVES': 23, 'SC_L1_FOREST_BELTS': 16837, 'SC_FH_TREES': 10225, 'SC_FH_SAPLINGS': 186, 'SC_FH_GROVES': 81, 'SC_FH_UNDERSTORY': 116, 'SC_FH_FALLEN_LOGS': 105, 'SC_FH_ROOTS_S |
| 41 | SC_L1_GROVES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 23 sampled |
| 42 | SC_L1_FOREST_BELTS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 3999 sampled |
| 43 | SC_FH_TREES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 3999 sampled |
| 44 | SC_FH_SAPLINGS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 186 sampled |
| 45 | SC_FH_GROVES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 81 sampled |
| 46 | SC_FH_UNDERSTORY: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 116 sampled |
| 47 | SC_FH_FALLEN_LOGS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 105 sampled |
| 48 | SC_FH_ROOTS_STUMPS_DEBRIS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 30 sampled |
| 49 | scatter produces instances (CAM_T5_07_GROUND_LEVEL) | ✅ PASS | {'SC_VH_MEADOW_GRASS_FAR': 405, 'SC_VH_MEADOW_GRASS': 542, 'SC_VH_WILDFLOWERS': 33, 'SC_VH_GROVES': 68, 'SC_L0_GROVES': 4845, 'SC_L1_GROVES': 714, 'SC_VH_RIVER_STONES': 108, 'SC_VH |
| 50 | SC_VH_MEADOW_GRASS_FAR: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.25% of 405 sampled |
| 51 | SC_VH_MEADOW_GRASS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 542 sampled |
| 52 | SC_VH_WILDFLOWERS: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 33 sampled |
| 53 | SC_VH_GROVES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.00% of 68 sampled |
| 54 | SC_L0_GROVES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.08% of 3999 sampled |
| 55 | SC_L1_GROVES: plants / trees not on paths, Ashram pad or water | ✅ PASS | 0.42% of 714 sampled |
| 56 | TASK 04 v001 baseline files unchanged | ✅ PASS | 21 files identical |

## Notes
- Run 1 found real LOD seam steps (33–254 m between the 400 m horizon and finer tiles) → fixed by blending every tile border onto its parent surface (parents built first). Run 2: 55/56; the last soft-edge grass check fixed with a tighter bare-ground mask.
- Image round-trip (EXR heights, PNG masks) verified exact (error 0) after the save fix.
- TASK 04 v001 baseline: all 21 files byte-identical (sha256).

# TASK 06 · Technical QC report — milestones 1 + 2 (vegetation libraries v001, all regions + populated files)

Automated by `03_assets/vegetation/scripts/t6_qc.py` (geometry, UVs, materials, textures, wind, ground contact, labels).

## Blender 4.5.16 LTS — **904/904 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | AV: library file exists | ✅ PASS | library/T6_VEG_ASHRAM_VALLEY_v001.blend |
| 2 | AV: file size < 100 MB (GitHub limit) | ✅ PASS | 33.7 MB |
| 3 | AV: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 60 images, missing [] |
| 4 | AV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 5 | AV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 6 | AV: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 7 | AV: assets in library | ✅ PASS | 21 assets |
| 8 | AV_AQ01_LOTUS: valid mesh, UVs | ✅ PASS | 2,244 tris, 1,774 verts |
| 9 | AV_AQ01_LOTUS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 10 | AV_AQ01_LOTUS: PBR materials (4 slots) | ✅ PASS | MAT_T6_AV_AQ01_LOTUS_0, MAT_T6_AV_AQ01_LOTUS_1, MAT_T6_AV_AQ01_LOTUS_2, MAT_T6_AV_AQ01_LOTUS_3 |
| 11 | AV_AQ01_LOTUS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 12 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 13 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 1.14 m |
| 14 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 15 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 16 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 17 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 18 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 19 | AV_AQ02_CATTAIL: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 20 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 21 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 22 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 23 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 24 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 25 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 26 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 27 | AV_F01_BUTTERCUP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 28 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 29 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 30 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 31 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 32 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 33 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 34 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 35 | AV_F02_PRIMULA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 36 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 37 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.005 m |
| 38 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 39 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 40 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 41 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 42 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 43 | AV_F03_WILD_DAISY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 44 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 45 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 46 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 47 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 48 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 49 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 50 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 51 | AV_F04_MARIGOLD: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 52 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 53 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 54 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 55 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 56 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 57 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 58 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 59 | AV_FE01_SWORD_FERN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 60 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 61 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 62 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 63 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 64 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 6,448 tris, 5,850 verts |
| 65 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 66 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 67 | AV_G01_MEADOW_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 68 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 69 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 70 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 71 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 72 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 73 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 74 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 75 | AV_G02_KANS_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 76 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 77 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 78 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 79 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 80 | AV_G02B_KANS_GRASS_SPRING: valid mesh, UVs | ✅ PASS | 4,760 tris, 4,095 verts |
| 81 | AV_G02B_KANS_GRASS_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 82 | AV_G02B_KANS_GRASS_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G02B_KANS_GRASS_SPRING_0, MAT_T6_AV_G02B_KANS_GRASS_SPRING_1 |
| 83 | AV_G02B_KANS_GRASS_SPRING: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 84 | AV_G02B_KANS_GRASS_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 85 | AV_G02B_KANS_GRASS_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 86 | AV_G02B_KANS_GRASS_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 87 | AV_G02B_KANS_GRASS_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 88 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 3,320 tris, 3,015 verts |
| 89 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 90 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 91 | AV_G03_DRY_PATH_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 92 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 93 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 94 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 95 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 96 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 97 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 98 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 99 | AV_M01_MOSS_CUSHION: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 100 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 101 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 102 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 103 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 104 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 105 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 106 | AV_MU01_BROWN_MUSHROOMS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 107 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 108 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 109 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 110 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 111 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 112 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 113 | AV_S01_BERBERIS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 114 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 115 | AV_S01_BERBERIS: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.83 m vs design 1.9 m |
| 116 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 117 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 118 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 119 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 120 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 121 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 122 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 123 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 124 | AV_S02_TULSI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 125 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 126 | AV_S02_TULSI: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.73 m vs design 0.75 m |
| 127 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 128 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 129 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 130 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 131 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 132 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,926 tris, 327,544 verts |
| 133 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 134 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 135 | AV_T01_PEEPAL: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 136 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 137 | AV_T01_PEEPAL: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 23.75 m vs design 22.0 m |
| 138 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 139 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 140 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 141 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 142 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 143 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 309,744 tris, 267,286 verts |
| 144 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 145 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 146 | AV_T02_DEODAR: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 147 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 148 | AV_T02_DEODAR: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 34.86 m vs design 34.0 m |
| 149 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 307 verts at the foot |
| 150 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 151 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 152 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 153 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 154 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 155 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 156 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 157 | AV_T03_CHIR_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 158 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 159 | AV_T03_CHIR_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 27.33 m vs design 28.0 m |
| 160 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 161 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 162 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 163 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 164 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 165 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,068 tris, 171,876 verts |
| 166 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 167 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 168 | AV_T04_BANJ_OAK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 169 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 170 | AV_T04_BANJ_OAK: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.45 m vs design 17.0 m |
| 171 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 172 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 173 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 174 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 175 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 176 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 177 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 178 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 179 | AV_T05_RHODODENDRON: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 180 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 181 | AV_T05_RHODODENDRON: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.19 m vs design 8.5 m |
| 182 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 183 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 184 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 185 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 186 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 187 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 188 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 189 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 190 | AV_T06_BAMBOO_CLUMP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 191 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 192 | AV_T06_BAMBOO_CLUMP: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.14 m vs design 15.0 m |
| 193 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 194 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 195 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 196 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 197 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 198 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 199 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.027 m · foot Δ 0.000 m |
| 200 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 201 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.3 MB |
| 202 | EF: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 64 images, missing [] |
| 203 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 204 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 205 | EF: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 206 | EF: assets in library | ✅ PASS | 13 assets |
| 207 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 208 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 209 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 210 | EF_FE01_GIANT_FERN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 211 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 212 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 213 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 214 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 215 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 216 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 217 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 218 | EF_M01_MOSS_CARPET: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 219 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 220 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 221 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 222 | EF_M02_GLOW_MOSS: valid mesh, UVs | ✅ PASS | 8,600 tris, 5,832 verts |
| 223 | EF_M02_GLOW_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 224 | EF_M02_GLOW_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M02_GLOW_MOSS_0, MAT_T6_EF_M02_GLOW_MOSS_1 |
| 225 | EF_M02_GLOW_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 226 | EF_M02_GLOW_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 227 | EF_M02_GLOW_MOSS: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 228 | EF_M02_GLOW_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 229 | EF_M02_GLOW_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.15 |
| 230 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 231 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 232 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 233 | EF_MU01_GLOWCAP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 234 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 235 | EF_MU01_GLOWCAP: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 236 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 237 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 238 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,958 tris, 389,340 verts |
| 239 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 240 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 241 | EF_T01_GIANT_ELDER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 242 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 243 | EF_T01_GIANT_ELDER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 66.79 m vs design 62.0 m |
| 244 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 504 verts at the foot |
| 245 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 246 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 247 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 248 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 249 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 251,408 tris, 214,441 verts |
| 250 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 251 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 252 | EF_T02_TEAL_BEECH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 253 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 254 | EF_T02_TEAL_BEECH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 34.60 m vs design 34.0 m |
| 255 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 342 verts at the foot |
| 256 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 257 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 258 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 259 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 260 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,120 tris, 177,671 verts |
| 261 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 262 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 263 | EF_T03_MOSS_OAK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 264 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 265 | EF_T03_MOSS_OAK: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 24.27 m vs design 23.0 m |
| 266 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 248 verts at the foot |
| 267 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 268 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 269 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 270 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 271 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 272 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 273 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 274 | EF_T04_YEW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 275 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 276 | EF_T04_YEW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.69 m vs design 9.0 m |
| 277 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 278 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 279 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 280 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 281 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 282 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 283 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 284 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 285 | EF_T05_VEIL_WILLOW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 286 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 287 | EF_T05_VEIL_WILLOW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 18.39 m vs design 18.0 m |
| 288 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 289 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 290 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 291 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 292 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 293 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 294 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,176 tris, 177,377 verts |
| 295 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 296 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 297 | EF_T06_SPIRAL_ROOT: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 298 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 299 | EF_T06_SPIRAL_ROOT: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 22.85 m vs design 24.0 m |
| 300 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.33 m, 495 verts at the foot |
| 301 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 302 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 303 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 304 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 305 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 306 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 307 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 308 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 309 | EF_T07_LANTERN_TREE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 310 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 311 | EF_T07_LANTERN_TREE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.11 m vs design 15.0 m |
| 312 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 313 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 314 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 315 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 316 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 317 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 318 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 319 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 320 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 321 | EF_T08_DEAD_SNAG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 322 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 323 | EF_T08_DEAD_SNAG: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 18.74 m vs design 17.0 m |
| 324 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 242 verts at the foot |
| 325 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 326 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 327 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 328 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 329 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 330 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 331 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 332 | EF_V01_HANGING_VINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 333 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 334 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 335 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 336 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 337 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.939 m · foot Δ 0.000 m |
| 338 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.002 m |
| 339 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 340 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 21.4 MB |
| 341 | MK: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 46 images, missing [] |
| 342 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 343 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 344 | MK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 345 | MK: assets in library | ✅ PASS | 12 assets |
| 346 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 347 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 348 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 349 | MK_F01_GENTIAN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 350 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 351 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 352 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 353 | MK_F01_GENTIAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 354 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 355 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 356 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 357 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 358 | MK_F02_EDELWEISS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 359 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 360 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 361 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 362 | MK_F02_EDELWEISS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 363 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 364 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 365 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 366 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 367 | MK_F03_BLUE_POPPY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 368 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 369 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 370 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 371 | MK_F03_BLUE_POPPY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 372 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 373 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 5,280 tris, 4,800 verts |
| 374 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 375 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 376 | MK_G01_ALPINE_TUSSOCK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 377 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 378 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 379 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 380 | MK_G01_ALPINE_TUSSOCK: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 381 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 382 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 383 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 384 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 385 | MK_M01_ALPINE_CUSHION: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 386 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 387 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 388 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 389 | MK_M01_ALPINE_CUSHION: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 390 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 391 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 392 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 393 | MK_S01_JUNIPER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 394 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 395 | MK_S01_JUNIPER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.82 m vs design 0.9 m |
| 396 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 397 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 398 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 399 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 400 | MK_S01_JUNIPER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 401 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 402 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 403 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 404 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 405 | MK_S02_DWARF_RHODODENDRON: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 406 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 407 | MK_S02_DWARF_RHODODENDRON: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.54 m vs design 0.6 m |
| 408 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 409 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 410 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 411 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 412 | MK_S02_DWARF_RHODODENDRON: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 413 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 414 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,706 tris, 188,378 verts |
| 415 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 416 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 417 | MK_T01_HIMALAYAN_SPRUCE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 418 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 419 | MK_T01_HIMALAYAN_SPRUCE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 31.32 m vs design 32.0 m |
| 420 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 308 verts at the foot |
| 421 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 422 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 423 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 424 | MK_T01_HIMALAYAN_SPRUCE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 425 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 426 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 427 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 428 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 429 | MK_T02_HIMALAYAN_BIRCH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 430 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 431 | MK_T02_HIMALAYAN_BIRCH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 11.59 m vs design 12.0 m |
| 432 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 433 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 434 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 435 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 436 | MK_T02_HIMALAYAN_BIRCH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 437 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 438 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 22,018 tris, 15,442 verts |
| 439 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 440 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 441 | MK_T03_KRUMMHOLZ_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 442 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 443 | MK_T03_KRUMMHOLZ_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 5.67 m vs design 5.5 m |
| 444 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 281 verts at the foot |
| 445 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 446 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 447 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 448 | MK_T03_KRUMMHOLZ_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 449 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 450 | MK_T04_SILVER_FIR: valid mesh, UVs | ✅ PASS | 256,348 tris, 216,552 verts |
| 451 | MK_T04_SILVER_FIR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 452 | MK_T04_SILVER_FIR: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T04_SILVER_FIR_BARK, MAT_T6_MK_T04_SILVER_FIR_LEAF, MAT_T6_MK_T04_SILVER_FIR_BARK |
| 453 | MK_T04_SILVER_FIR: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 454 | MK_T04_SILVER_FIR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 455 | MK_T04_SILVER_FIR: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 37.36 m vs design 36.0 m |
| 456 | MK_T04_SILVER_FIR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 287 verts at the foot |
| 457 | MK_T04_SILVER_FIR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 458 | MK_T04_SILVER_FIR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 459 | MK_T04_SILVER_FIR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 460 | MK_T04_SILVER_FIR: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 461 | MK_T04_SILVER_FIR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 462 | MK_T05_BLUE_PINE: valid mesh, UVs | ✅ PASS | 126,070 tris, 112,360 verts |
| 463 | MK_T05_BLUE_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 464 | MK_T05_BLUE_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T05_BLUE_PINE_BARK, MAT_T6_MK_T05_BLUE_PINE_LEAF, MAT_T6_MK_T05_BLUE_PINE_BARK |
| 465 | MK_T05_BLUE_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 466 | MK_T05_BLUE_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 467 | MK_T05_BLUE_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 31.42 m vs design 30.0 m |
| 468 | MK_T05_BLUE_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.42 m, 305 verts at the foot |
| 469 | MK_T05_BLUE_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 470 | MK_T05_BLUE_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 471 | MK_T05_BLUE_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 472 | MK_T05_BLUE_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 473 | MK_T05_BLUE_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 474 | MK_T04_SILVER_FIR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 475 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |
| 476 | PL: library file exists | ✅ PASS | library/T6_VEG_GREEN_PLAINS_v001.blend |
| 477 | PL: file size < 100 MB (GitHub limit) | ✅ PASS | 33.9 MB |
| 478 | PL: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 27 images, missing [] |
| 479 | PL: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 480 | PL: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 481 | PL: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 482 | PL: assets in library | ✅ PASS | 9 assets |
| 483 | PL_F01_WILD_MUSTARD: valid mesh, UVs | ✅ PASS | 3,460 tris, 2,624 verts |
| 484 | PL_F01_WILD_MUSTARD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 485 | PL_F01_WILD_MUSTARD: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F01_WILD_MUSTARD_0, MAT_T6_PL_F01_WILD_MUSTARD_1, MAT_T6_PL_F01_WILD_MUSTARD_2 |
| 486 | PL_F01_WILD_MUSTARD: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 487 | PL_F01_WILD_MUSTARD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 488 | PL_F01_WILD_MUSTARD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 489 | PL_F01_WILD_MUSTARD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 490 | PL_F01_WILD_MUSTARD: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 491 | PL_F01_WILD_MUSTARD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 492 | PL_F02_GLOBE_THISTLE: valid mesh, UVs | ✅ PASS | 39,852 tris, 32,698 verts |
| 493 | PL_F02_GLOBE_THISTLE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 494 | PL_F02_GLOBE_THISTLE: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F02_GLOBE_THISTLE_0, MAT_T6_PL_F02_GLOBE_THISTLE_1, MAT_T6_PL_F02_GLOBE_THISTLE_2 |
| 495 | PL_F02_GLOBE_THISTLE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 496 | PL_F02_GLOBE_THISTLE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 497 | PL_F02_GLOBE_THISTLE: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 498 | PL_F02_GLOBE_THISTLE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 499 | PL_F02_GLOBE_THISTLE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 500 | PL_F02_GLOBE_THISTLE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 501 | PL_F03_WHITE_CLOVER: valid mesh, UVs | ✅ PASS | 29,320 tris, 23,982 verts |
| 502 | PL_F03_WHITE_CLOVER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 503 | PL_F03_WHITE_CLOVER: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F03_WHITE_CLOVER_0, MAT_T6_PL_F03_WHITE_CLOVER_1, MAT_T6_PL_F03_WHITE_CLOVER_2 |
| 504 | PL_F03_WHITE_CLOVER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 505 | PL_F03_WHITE_CLOVER: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 506 | PL_F03_WHITE_CLOVER: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 507 | PL_F03_WHITE_CLOVER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 508 | PL_F03_WHITE_CLOVER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 509 | PL_F03_WHITE_CLOVER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 510 | PL_G01_TALL_GRASS: valid mesh, UVs | ✅ PASS | 7,840 tris, 6,750 verts |
| 511 | PL_G01_TALL_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 512 | PL_G01_TALL_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_PL_G01_TALL_GRASS_0, MAT_T6_PL_G01_TALL_GRASS_1 |
| 513 | PL_G01_TALL_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 514 | PL_G01_TALL_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 515 | PL_G01_TALL_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 516 | PL_G01_TALL_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 517 | PL_G01_TALL_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 518 | PL_G01_TALL_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 519 | PL_G02_DOOB_GRASS: valid mesh, UVs | ✅ PASS | 6,272 tris, 5,952 verts |
| 520 | PL_G02_DOOB_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 521 | PL_G02_DOOB_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_PL_G02_DOOB_GRASS_0, MAT_T6_PL_G02_DOOB_GRASS_1 |
| 522 | PL_G02_DOOB_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 523 | PL_G02_DOOB_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 524 | PL_G02_DOOB_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 525 | PL_G02_DOOB_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 526 | PL_G02_DOOB_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 527 | PL_G02_DOOB_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 528 | PL_S01_BER_BUSH: valid mesh, UVs | ✅ PASS | 6,388 tris, 6,372 verts |
| 529 | PL_S01_BER_BUSH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 530 | PL_S01_BER_BUSH: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_S01_BER_BUSH_BARK, MAT_T6_PL_S01_BER_BUSH_LEAF, MAT_T6_PL_S01_BER_BUSH_BARK |
| 531 | PL_S01_BER_BUSH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 532 | PL_S01_BER_BUSH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 533 | PL_S01_BER_BUSH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 2.15 m vs design 2.2 m |
| 534 | PL_S01_BER_BUSH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.17 m, 206 verts at the foot |
| 535 | PL_S01_BER_BUSH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 536 | PL_S01_BER_BUSH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 537 | PL_S01_BER_BUSH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 538 | PL_S01_BER_BUSH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 539 | PL_S01_BER_BUSH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 540 | PL_T01_BANYAN: valid mesh, UVs | ✅ PASS | 713,372 tris, 536,370 verts |
| 541 | PL_T01_BANYAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 542 | PL_T01_BANYAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T01_BANYAN_BARK, MAT_T6_PL_T01_BANYAN_LEAF, MAT_T6_PL_T01_BANYAN_BARK |
| 543 | PL_T01_BANYAN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 544 | PL_T01_BANYAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 545 | PL_T01_BANYAN: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 21.40 m vs design 21.0 m |
| 546 | PL_T01_BANYAN: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.55 m, 194 verts at the foot |
| 547 | PL_T01_BANYAN: no limbs through the ground (prop roots allowed) | ✅ PASS | 4 verts far + under ground |
| 548 | PL_T01_BANYAN: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 549 | PL_T01_BANYAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 550 | PL_T01_BANYAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 551 | PL_T01_BANYAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 552 | PL_T02_NEEM: valid mesh, UVs | ✅ PASS | 245,900 tris, 200,888 verts |
| 553 | PL_T02_NEEM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 554 | PL_T02_NEEM: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T02_NEEM_BARK, MAT_T6_PL_T02_NEEM_LEAF, MAT_T6_PL_T02_NEEM_BARK |
| 555 | PL_T02_NEEM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 556 | PL_T02_NEEM: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 557 | PL_T02_NEEM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.27 m vs design 15.0 m |
| 558 | PL_T02_NEEM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.39 m, 327 verts at the foot |
| 559 | PL_T02_NEEM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 560 | PL_T02_NEEM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 561 | PL_T02_NEEM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 562 | PL_T02_NEEM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 563 | PL_T02_NEEM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 564 | PL_T03_UMBRELLA_ACACIA: valid mesh, UVs | ✅ PASS | 275,386 tris, 204,434 verts |
| 565 | PL_T03_UMBRELLA_ACACIA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 566 | PL_T03_UMBRELLA_ACACIA: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T03_UMBRELLA_ACACIA_BARK, MAT_T6_PL_T03_UMBRELLA_ACACIA_LEAF, MAT_T6_PL_T03_UMBRELLA_ACACIA_BARK |
| 567 | PL_T03_UMBRELLA_ACACIA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 568 | PL_T03_UMBRELLA_ACACIA: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 569 | PL_T03_UMBRELLA_ACACIA: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 9.46 m vs design 9.0 m |
| 570 | PL_T03_UMBRELLA_ACACIA: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 32 verts at the foot |
| 571 | PL_T03_UMBRELLA_ACACIA: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 572 | PL_T03_UMBRELLA_ACACIA: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 573 | PL_T03_UMBRELLA_ACACIA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 574 | PL_T03_UMBRELLA_ACACIA: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 575 | PL_T03_UMBRELLA_ACACIA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 576 | PL_T01_BANYAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.416 m · foot Δ 0.000 m |
| 577 | PL_F01_WILD_MUSTARD: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.033 m · foot Δ 0.004 m |
| 578 | LK: library file exists | ✅ PASS | library/T6_VEG_CRYSTAL_LAKES_v001.blend |
| 579 | LK: file size < 100 MB (GitHub limit) | ✅ PASS | 11.6 MB |
| 580 | LK: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 19 images, missing [] |
| 581 | LK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 582 | LK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 583 | LK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 584 | LK: assets in library | ✅ PASS | 6 assets |
| 585 | LK_AQ01_WATER_LILY: valid mesh, UVs | ✅ PASS | 4,240 tris, 3,406 verts |
| 586 | LK_AQ01_WATER_LILY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 587 | LK_AQ01_WATER_LILY: PBR materials (4 slots) | ✅ PASS | MAT_T6_LK_AQ01_WATER_LILY_0, MAT_T6_LK_AQ01_WATER_LILY_1, MAT_T6_LK_AQ01_WATER_LILY_2, MAT_T6_LK_AQ01_WATER_LILY_3 |
| 588 | LK_AQ01_WATER_LILY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 589 | LK_AQ01_WATER_LILY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 590 | LK_AQ01_WATER_LILY: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.90 m, top 0.07 m |
| 591 | LK_AQ01_WATER_LILY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 592 | LK_AQ01_WATER_LILY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 593 | LK_AQ01_WATER_LILY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 594 | LK_AQ02_SEDGE: valid mesh, UVs | ✅ PASS | 5,260 tris, 4,632 verts |
| 595 | LK_AQ02_SEDGE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 596 | LK_AQ02_SEDGE: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_AQ02_SEDGE_0, MAT_T6_LK_AQ02_SEDGE_1 |
| 597 | LK_AQ02_SEDGE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 598 | LK_AQ02_SEDGE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 599 | LK_AQ02_SEDGE: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 600 | LK_AQ02_SEDGE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 601 | LK_AQ02_SEDGE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 602 | LK_AQ02_SEDGE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 603 | LK_AQ03_REED_SPRING: valid mesh, UVs | ✅ PASS | 3,636 tris, 3,078 verts |
| 604 | LK_AQ03_REED_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 605 | LK_AQ03_REED_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_AQ03_REED_SPRING_0, MAT_T6_LK_AQ03_REED_SPRING_1 |
| 606 | LK_AQ03_REED_SPRING: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 607 | LK_AQ03_REED_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 608 | LK_AQ03_REED_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 609 | LK_AQ03_REED_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 610 | LK_AQ03_REED_SPRING: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 611 | LK_AQ03_REED_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 612 | LK_M01_WET_ROCK_MOSS: valid mesh, UVs | ✅ PASS | 3,480 tris, 2,256 verts |
| 613 | LK_M01_WET_ROCK_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 614 | LK_M01_WET_ROCK_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_M01_WET_ROCK_MOSS_0, MAT_T6_LK_M01_WET_ROCK_MOSS_1 |
| 615 | LK_M01_WET_ROCK_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 616 | LK_M01_WET_ROCK_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 617 | LK_M01_WET_ROCK_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 618 | LK_M01_WET_ROCK_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 619 | LK_M01_WET_ROCK_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 620 | LK_T01_WHITE_WILLOW: valid mesh, UVs | ✅ PASS | 288,540 tris, 222,262 verts |
| 621 | LK_T01_WHITE_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 622 | LK_T01_WHITE_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_LK_T01_WHITE_WILLOW_BARK, MAT_T6_LK_T01_WHITE_WILLOW_LEAF, MAT_T6_LK_T01_WHITE_WILLOW_BARK |
| 623 | LK_T01_WHITE_WILLOW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 624 | LK_T01_WHITE_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 625 | LK_T01_WHITE_WILLOW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.91 m vs design 16.0 m |
| 626 | LK_T01_WHITE_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.55 m, 335 verts at the foot |
| 627 | LK_T01_WHITE_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 628 | LK_T01_WHITE_WILLOW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 629 | LK_T01_WHITE_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 630 | LK_T01_WHITE_WILLOW: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 631 | LK_T01_WHITE_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 632 | LK_T02_ALDER: valid mesh, UVs | ✅ PASS | 133,524 tris, 108,106 verts |
| 633 | LK_T02_ALDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 634 | LK_T02_ALDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_LK_T02_ALDER_BARK, MAT_T6_LK_T02_ALDER_LEAF, MAT_T6_LK_T02_ALDER_BARK |
| 635 | LK_T02_ALDER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 636 | LK_T02_ALDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 637 | LK_T02_ALDER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 20.39 m vs design 20.0 m |
| 638 | LK_T02_ALDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.33 m, 333 verts at the foot |
| 639 | LK_T02_ALDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 640 | LK_T02_ALDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 641 | LK_T02_ALDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 642 | LK_T02_ALDER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 643 | LK_T02_ALDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 644 | LK_T02_ALDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.360 m · foot Δ 0.000 m |
| 645 | LK_AQ01_WATER_LILY: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.008 m · foot Δ 0.002 m |
| 646 | DS: library file exists | ✅ PASS | library/T6_VEG_GOLDEN_DESERT_v001.blend |
| 647 | DS: file size < 100 MB (GitHub limit) | ✅ PASS | 10.1 MB |
| 648 | DS: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 21 images, missing [] |
| 649 | DS: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 650 | DS: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 651 | DS: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 652 | DS: assets in library | ✅ PASS | 5 assets |
| 653 | DS_G01_SEWAN_GRASS: valid mesh, UVs | ✅ PASS | 5,100 tris, 4,500 verts |
| 654 | DS_G01_SEWAN_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 655 | DS_G01_SEWAN_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_DS_G01_SEWAN_GRASS_0, MAT_T6_DS_G01_SEWAN_GRASS_1 |
| 656 | DS_G01_SEWAN_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 657 | DS_G01_SEWAN_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 658 | DS_G01_SEWAN_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 659 | DS_G01_SEWAN_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 660 | DS_G01_SEWAN_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 661 | DS_G01_SEWAN_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 662 | DS_S01_CALOTROPIS: valid mesh, UVs | ✅ PASS | 2,910 tris, 2,340 verts |
| 663 | DS_S01_CALOTROPIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 664 | DS_S01_CALOTROPIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_DS_S01_CALOTROPIS_BARK, MAT_T6_DS_S01_CALOTROPIS_LEAF, MAT_T6_DS_S01_CALOTROPIS_BARK |
| 665 | DS_S01_CALOTROPIS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 666 | DS_S01_CALOTROPIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 667 | DS_S01_CALOTROPIS: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.76 m vs design 1.8 m |
| 668 | DS_S01_CALOTROPIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.13 m, 108 verts at the foot |
| 669 | DS_S01_CALOTROPIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 670 | DS_S01_CALOTROPIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 671 | DS_S01_CALOTROPIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 672 | DS_S01_CALOTROPIS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 673 | DS_S01_CALOTROPIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 674 | DS_S02_EUPHORBIA: valid mesh, UVs | ✅ PASS | 31,760 tris, 20,400 verts |
| 675 | DS_S02_EUPHORBIA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 676 | DS_S02_EUPHORBIA: PBR materials (2 slots) | ✅ PASS | MAT_T6_DS_S02_EUPHORBIA_0, MAT_T6_DS_S02_EUPHORBIA_1 |
| 677 | DS_S02_EUPHORBIA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 678 | DS_S02_EUPHORBIA: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 679 | DS_S02_EUPHORBIA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.051 m |
| 680 | DS_S02_EUPHORBIA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 681 | DS_S02_EUPHORBIA: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 682 | DS_S02_EUPHORBIA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 683 | DS_T01_KHEJRI: valid mesh, UVs | ✅ PASS | 247,022 tris, 207,672 verts |
| 684 | DS_T01_KHEJRI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 685 | DS_T01_KHEJRI: PBR materials (3 slots) | ✅ PASS | MAT_T6_DS_T01_KHEJRI_BARK, MAT_T6_DS_T01_KHEJRI_LEAF, MAT_T6_DS_T01_KHEJRI_BARK |
| 686 | DS_T01_KHEJRI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 687 | DS_T01_KHEJRI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 688 | DS_T01_KHEJRI: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.28 m vs design 8.0 m |
| 689 | DS_T01_KHEJRI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 337 verts at the foot |
| 690 | DS_T01_KHEJRI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 691 | DS_T01_KHEJRI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 692 | DS_T01_KHEJRI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 693 | DS_T01_KHEJRI: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 694 | DS_T01_KHEJRI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 695 | DS_T02_DATE_PALM: valid mesh, UVs | ✅ PASS | 102,320 tris, 92,626 verts |
| 696 | DS_T02_DATE_PALM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 697 | DS_T02_DATE_PALM: PBR materials (4 slots) | ✅ PASS | MAT_T6_DS_T02_DATE_PALM_BARK, MAT_T6_DS_T02_DATE_PALM_FROND, MAT_T6_DS_T02_DATE_PALM_DEADFROND, MAT_T6_DS_T02_DATE_PALM_ |
| 698 | DS_T02_DATE_PALM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 699 | DS_T02_DATE_PALM: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 700 | DS_T02_DATE_PALM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 13.83 m vs design 14.0 m |
| 701 | DS_T02_DATE_PALM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.36 m, 32 verts at the foot |
| 702 | DS_T02_DATE_PALM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 703 | DS_T02_DATE_PALM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 704 | DS_T02_DATE_PALM: palm — trunk scan + frond / dead-frond materials, fronds attached to the crown | ✅ PASS | MAT_T6_DS_T02_DATE_PALM_FROND, MAT_T6_DS_T02_DATE_PALM_DEADFROND |
| 705 | DS_T02_DATE_PALM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 706 | DS_T02_DATE_PALM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 707 | DS_T02_DATE_PALM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 708 | DS_T02_DATE_PALM: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.259 m · foot Δ 0.000 m |
| 709 | DS_G01_SEWAN_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.033 m · foot Δ 0.016 m |
| 710 | FB: library file exists | ✅ PASS | library/T6_VEG_FORBIDDEN_LANDS_v001.blend |
| 711 | FB: file size < 100 MB (GitHub limit) | ✅ PASS | 0.5 MB |
| 712 | FB: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 10 images, missing [] |
| 713 | FB: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 714 | FB: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 715 | FB: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 716 | FB: assets in library | ✅ PASS | 4 assets |
| 717 | FB_G01_HARDY_GRASS: valid mesh, UVs | ✅ PASS | 1,580 tris, 1,440 verts |
| 718 | FB_G01_HARDY_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 719 | FB_G01_HARDY_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_FB_G01_HARDY_GRASS_0, MAT_T6_FB_G01_HARDY_GRASS_1 |
| 720 | FB_G01_HARDY_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 721 | FB_G01_HARDY_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 722 | FB_G01_HARDY_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 723 | FB_G01_HARDY_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 724 | FB_G01_HARDY_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 725 | FB_G01_HARDY_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 726 | FB_M01_ASH_LICHEN: valid mesh, UVs | ✅ PASS | 3,080 tris, 1,848 verts |
| 727 | FB_M01_ASH_LICHEN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 728 | FB_M01_ASH_LICHEN: PBR materials (2 slots) | ✅ PASS | MAT_T6_FB_M01_ASH_LICHEN_0, MAT_T6_FB_M01_ASH_LICHEN_1 |
| 729 | FB_M01_ASH_LICHEN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 730 | FB_M01_ASH_LICHEN: every face has a valid material slot | ✅ PASS | slots used [0] |
| 731 | FB_M01_ASH_LICHEN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 732 | FB_M01_ASH_LICHEN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 733 | FB_M01_ASH_LICHEN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 734 | FB_S01_DEAD_THORN_SHRUB: valid mesh, UVs | ✅ PASS | 1,798 tris, 1,092 verts |
| 735 | FB_S01_DEAD_THORN_SHRUB: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 736 | FB_S01_DEAD_THORN_SHRUB: PBR materials (3 slots) | ✅ PASS | MAT_T6_FB_S01_DEAD_THORN_SHRUB_BARK, MAT_T6_FB_S01_DEAD_THORN_SHRUB_NOLEAF, MAT_T6_FB_S01_DEAD_THORN_SHRUB_BARK |
| 737 | FB_S01_DEAD_THORN_SHRUB: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 738 | FB_S01_DEAD_THORN_SHRUB: every face has a valid material slot | ✅ PASS | slots used [0] |
| 739 | FB_S01_DEAD_THORN_SHRUB: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.43 m vs design 1.4 m |
| 740 | FB_S01_DEAD_THORN_SHRUB: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.21 m, 122 verts at the foot |
| 741 | FB_S01_DEAD_THORN_SHRUB: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 742 | FB_S01_DEAD_THORN_SHRUB: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 743 | FB_S01_DEAD_THORN_SHRUB: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 744 | FB_S01_DEAD_THORN_SHRUB: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 745 | FB_S01_DEAD_THORN_SHRUB: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 746 | FB_T01_CHARRED_SNAG: valid mesh, UVs | ✅ PASS | 6,256 tris, 3,688 verts |
| 747 | FB_T01_CHARRED_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 748 | FB_T01_CHARRED_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_FB_T01_CHARRED_SNAG_BARK, MAT_T6_FB_T01_CHARRED_SNAG_NOLEAF, MAT_T6_FB_T01_CHARRED_SNAG_BARK |
| 749 | FB_T01_CHARRED_SNAG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 750 | FB_T01_CHARRED_SNAG: every face has a valid material slot | ✅ PASS | slots used [0] |
| 751 | FB_T01_CHARRED_SNAG: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 12.29 m vs design 12.0 m |
| 752 | FB_T01_CHARRED_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.40 m, 245 verts at the foot |
| 753 | FB_T01_CHARRED_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 754 | FB_T01_CHARRED_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 755 | FB_T01_CHARRED_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 756 | FB_T01_CHARRED_SNAG: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 757 | FB_T01_CHARRED_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 758 | FB_T01_CHARRED_SNAG: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.074 m · foot Δ 0.000 m |
| 759 | FB_G01_HARDY_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.023 m · foot Δ 0.019 m |
| 760 | CT: library file exists | ✅ PASS | library/T6_VEG_ANCIENT_CITY_SITES_v001.blend |
| 761 | CT: file size < 100 MB (GitHub limit) | ✅ PASS | 9.6 MB |
| 762 | CT: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 21 images, missing [] |
| 763 | CT: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 764 | CT: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 765 | CT: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 766 | CT: assets in library | ✅ PASS | 5 assets |
| 767 | CT_G01_CRACK_GRASS: valid mesh, UVs | ✅ PASS | 1,176 tris, 1,116 verts |
| 768 | CT_G01_CRACK_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 769 | CT_G01_CRACK_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_G01_CRACK_GRASS_0, MAT_T6_CT_G01_CRACK_GRASS_1 |
| 770 | CT_G01_CRACK_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 771 | CT_G01_CRACK_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 772 | CT_G01_CRACK_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 773 | CT_G01_CRACK_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 774 | CT_G01_CRACK_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 775 | CT_G01_CRACK_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 776 | CT_M01_RUIN_MOSS: valid mesh, UVs | ✅ PASS | 3,680 tris, 2,460 verts |
| 777 | CT_M01_RUIN_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 778 | CT_M01_RUIN_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_M01_RUIN_MOSS_0, MAT_T6_CT_M01_RUIN_MOSS_1 |
| 779 | CT_M01_RUIN_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 780 | CT_M01_RUIN_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 781 | CT_M01_RUIN_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 782 | CT_M01_RUIN_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 783 | CT_M01_RUIN_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 784 | CT_T01_MANGO: valid mesh, UVs | ✅ PASS | 298,640 tris, 228,428 verts |
| 785 | CT_T01_MANGO: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 786 | CT_T01_MANGO: PBR materials (3 slots) | ✅ PASS | MAT_T6_CT_T01_MANGO_BARK, MAT_T6_CT_T01_MANGO_LEAF, MAT_T6_CT_T01_MANGO_BARK |
| 787 | CT_T01_MANGO: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 788 | CT_T01_MANGO: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 789 | CT_T01_MANGO: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.27 m vs design 16.0 m |
| 790 | CT_T01_MANGO: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 444 verts at the foot |
| 791 | CT_T01_MANGO: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 792 | CT_T01_MANGO: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 793 | CT_T01_MANGO: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 794 | CT_T01_MANGO: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 795 | CT_T01_MANGO: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 796 | CT_T02_COCONUT_PALM: valid mesh, UVs | ✅ PASS | 69,432 tris, 62,562 verts |
| 797 | CT_T02_COCONUT_PALM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 798 | CT_T02_COCONUT_PALM: PBR materials (4 slots) | ✅ PASS | MAT_T6_CT_T02_COCONUT_PALM_BARK, MAT_T6_CT_T02_COCONUT_PALM_FROND, MAT_T6_CT_T02_COCONUT_PALM_DEADFROND, MAT_T6_CT_T02_C |
| 799 | CT_T02_COCONUT_PALM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 800 | CT_T02_COCONUT_PALM: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 801 | CT_T02_COCONUT_PALM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 16.06 m vs design 17.0 m |
| 802 | CT_T02_COCONUT_PALM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.36 m, 32 verts at the foot |
| 803 | CT_T02_COCONUT_PALM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 804 | CT_T02_COCONUT_PALM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 805 | CT_T02_COCONUT_PALM: palm — trunk scan + frond / dead-frond materials, fronds attached to the crown | ✅ PASS | MAT_T6_CT_T02_COCONUT_PALM_FROND, MAT_T6_CT_T02_COCONUT_PALM_DEADFROND |
| 806 | CT_T02_COCONUT_PALM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 807 | CT_T02_COCONUT_PALM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 808 | CT_T02_COCONUT_PALM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 809 | CT_V01_IVY_CURTAIN: valid mesh, UVs | ✅ PASS | 4,114 tris, 3,616 verts |
| 810 | CT_V01_IVY_CURTAIN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 811 | CT_V01_IVY_CURTAIN: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_V01_IVY_CURTAIN_0, MAT_T6_CT_V01_IVY_CURTAIN_1 |
| 812 | CT_V01_IVY_CURTAIN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 813 | CT_V01_IVY_CURTAIN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 814 | CT_V01_IVY_CURTAIN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.035 m |
| 815 | CT_V01_IVY_CURTAIN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 816 | CT_V01_IVY_CURTAIN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 817 | CT_V01_IVY_CURTAIN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 818 | CT_T02_COCONUT_PALM: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.215 m · foot Δ 0.000 m |
| 819 | CT_G01_CRACK_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.018 m · foot Δ 0.014 m |
| 820 | CV: library file exists | ✅ PASS | library/T6_VEG_HIDDEN_UNDERGROUND_v001.blend |
| 821 | CV: file size < 100 MB (GitHub limit) | ✅ PASS | 0.4 MB |
| 822 | CV: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 5 images, missing [] |
| 823 | CV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 824 | CV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 825 | CV: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 826 | CV: assets in library | ✅ PASS | 3 assets |
| 827 | CV_M01_PALE_CAVE_MOSS: valid mesh, UVs | ✅ PASS | 2,820 tris, 1,818 verts |
| 828 | CV_M01_PALE_CAVE_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 829 | CV_M01_PALE_CAVE_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CV_M01_PALE_CAVE_MOSS_0, MAT_T6_CV_M01_PALE_CAVE_MOSS_1 |
| 830 | CV_M01_PALE_CAVE_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 831 | CV_M01_PALE_CAVE_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 832 | CV_M01_PALE_CAVE_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 833 | CV_M01_PALE_CAVE_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 834 | CV_M01_PALE_CAVE_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 835 | CV_MU01_CAVE_FUNGI: valid mesh, UVs | ✅ PASS | 6,208 tris, 4,032 verts |
| 836 | CV_MU01_CAVE_FUNGI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 837 | CV_MU01_CAVE_FUNGI: PBR materials (3 slots) | ✅ PASS | MAT_T6_CV_MU01_CAVE_FUNGI_0, MAT_T6_CV_MU01_CAVE_FUNGI_1, MAT_T6_CV_MU01_CAVE_FUNGI_2 |
| 838 | CV_MU01_CAVE_FUNGI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 839 | CV_MU01_CAVE_FUNGI: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 840 | CV_MU01_CAVE_FUNGI: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 841 | CV_MU01_CAVE_FUNGI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 842 | CV_MU01_CAVE_FUNGI: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 843 | CV_V01_ROOT_CURTAIN: valid mesh, UVs | ✅ PASS | 5,280 tris, 2,750 verts |
| 844 | CV_V01_ROOT_CURTAIN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 845 | CV_V01_ROOT_CURTAIN: PBR materials (1 slots) | ✅ PASS | MAT_T6_CV_V01_ROOT_CURTAIN_0 |
| 846 | CV_V01_ROOT_CURTAIN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 847 | CV_V01_ROOT_CURTAIN: every face has a valid material slot | ✅ PASS | slots used [0] |
| 848 | CV_V01_ROOT_CURTAIN: hanging plant attaches at its top (hangs from a branch, z_top = 3.6 m) | ✅ PASS | z 0.06–3.60 m |
| 849 | CV_V01_ROOT_CURTAIN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 850 | CV_V01_ROOT_CURTAIN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 851 | CV_V01_ROOT_CURTAIN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 852 | CV_V01_ROOT_CURTAIN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.021 m · foot Δ 0.000 m |
| 853 | ND: library file exists | ✅ PASS | library/T6_VEG_NATURAL_DETAILS_v001.blend |
| 854 | ND: file size < 100 MB (GitHub limit) | ✅ PASS | 2.1 MB |
| 855 | ND: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 29 images, missing [] |
| 856 | ND: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 857 | ND: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 858 | ND: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 859 | ND: assets in library | ✅ PASS | 6 assets |
| 860 | ND_B01_FALLEN_BRANCHES: valid mesh, UVs | ✅ PASS | 1,312 tris, 788 verts |
| 861 | ND_B01_FALLEN_BRANCHES: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 862 | ND_B01_FALLEN_BRANCHES: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_B01_FALLEN_BRANCHES_0, MAT_T6_ND_B01_FALLEN_BRANCHES_1 |
| 863 | ND_B01_FALLEN_BRANCHES: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 864 | ND_B01_FALLEN_BRANCHES: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 865 | ND_B01_FALLEN_BRANCHES: plant base on the ground (no floating) | ✅ PASS | lowest z -0.029 m |
| 866 | ND_B01_FALLEN_BRANCHES: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 867 | ND_B02_GIANT_LOG: valid mesh, UVs | ✅ PASS | 6,000 tris, 3,549 verts |
| 868 | ND_B02_GIANT_LOG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 869 | ND_B02_GIANT_LOG: PBR materials (4 slots) | ✅ PASS | MAT_T6_ND_B02_GIANT_LOG_0, MAT_T6_ND_B02_GIANT_LOG_1, MAT_T6_ND_B02_GIANT_LOG_2, MAT_T6_ND_B02_GIANT_LOG_3 |
| 870 | ND_B02_GIANT_LOG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 871 | ND_B02_GIANT_LOG: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 872 | ND_B02_GIANT_LOG: plant base on the ground (no floating) | ✅ PASS | lowest z -0.102 m |
| 873 | ND_B02_GIANT_LOG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 874 | ND_I01_GROUND_IVY: valid mesh, UVs | ✅ PASS | 2,704 tris, 2,437 verts |
| 875 | ND_I01_GROUND_IVY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 876 | ND_I01_GROUND_IVY: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_I01_GROUND_IVY_0, MAT_T6_ND_I01_GROUND_IVY_1 |
| 877 | ND_I01_GROUND_IVY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 878 | ND_I01_GROUND_IVY: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 879 | ND_I01_GROUND_IVY: plant base on the ground (no floating) | ✅ PASS | lowest z 0.000 m |
| 880 | ND_I01_GROUND_IVY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 881 | ND_I01_GROUND_IVY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 882 | ND_L01_LEAF_LITTER_BROADLEAF: valid mesh, UVs | ✅ PASS | 3,760 tris, 4,020 verts |
| 883 | ND_L01_LEAF_LITTER_BROADLEAF: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 884 | ND_L01_LEAF_LITTER_BROADLEAF: PBR materials (3 slots) | ✅ PASS | MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_0, MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_1, MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_2 |
| 885 | ND_L01_LEAF_LITTER_BROADLEAF: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 886 | ND_L01_LEAF_LITTER_BROADLEAF: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 887 | ND_L01_LEAF_LITTER_BROADLEAF: plant base on the ground (no floating) | ✅ PASS | lowest z -0.003 m |
| 888 | ND_L01_LEAF_LITTER_BROADLEAF: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 889 | ND_L02_NEEDLE_LITTER: valid mesh, UVs | ✅ PASS | 41,464 tris, 65,321 verts |
| 890 | ND_L02_NEEDLE_LITTER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 891 | ND_L02_NEEDLE_LITTER: PBR materials (3 slots) | ✅ PASS | MAT_T6_ND_L02_NEEDLE_LITTER_0, MAT_T6_ND_L02_NEEDLE_LITTER_1, MAT_T6_ND_L02_NEEDLE_LITTER_2 |
| 892 | ND_L02_NEEDLE_LITTER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 893 | ND_L02_NEEDLE_LITTER: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 894 | ND_L02_NEEDLE_LITTER: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 895 | ND_L02_NEEDLE_LITTER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 896 | ND_W01_FLOATING_LEAVES: valid mesh, UVs | ✅ PASS | 720 tris, 810 verts |
| 897 | ND_W01_FLOATING_LEAVES: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 898 | ND_W01_FLOATING_LEAVES: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_W01_FLOATING_LEAVES_0, MAT_T6_ND_W01_FLOATING_LEAVES_1 |
| 899 | ND_W01_FLOATING_LEAVES: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 900 | ND_W01_FLOATING_LEAVES: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 901 | ND_W01_FLOATING_LEAVES: plant base on the ground (no floating) | ✅ PASS | lowest z 0.000 m |
| 902 | ND_W01_FLOATING_LEAVES: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 903 | ND_W01_FLOATING_LEAVES: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 904 | ND_I01_GROUND_IVY: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.007 m · foot Δ 0.002 m |

## Blender 5.3.0 — **904/904 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | AV: library file exists | ✅ PASS | library/T6_VEG_ASHRAM_VALLEY_v001.blend |
| 2 | AV: file size < 100 MB (GitHub limit) | ✅ PASS | 33.7 MB |
| 3 | AV: opens in Blender 5.3.0, no missing images | ✅ PASS | 60 images, missing [] |
| 4 | AV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 5 | AV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 6 | AV: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 7 | AV: assets in library | ✅ PASS | 21 assets |
| 8 | AV_AQ01_LOTUS: valid mesh, UVs | ✅ PASS | 2,244 tris, 1,774 verts |
| 9 | AV_AQ01_LOTUS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 10 | AV_AQ01_LOTUS: PBR materials (4 slots) | ✅ PASS | MAT_T6_AV_AQ01_LOTUS_0, MAT_T6_AV_AQ01_LOTUS_1, MAT_T6_AV_AQ01_LOTUS_2, MAT_T6_AV_AQ01_LOTUS_3 |
| 11 | AV_AQ01_LOTUS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 12 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 13 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 1.14 m |
| 14 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 15 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 16 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 17 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 18 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 19 | AV_AQ02_CATTAIL: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 20 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 21 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 22 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 23 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 24 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 25 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 26 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 27 | AV_F01_BUTTERCUP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 28 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 29 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 30 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 31 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 32 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 33 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 34 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 35 | AV_F02_PRIMULA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 36 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 37 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.005 m |
| 38 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 39 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 40 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 41 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 42 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 43 | AV_F03_WILD_DAISY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 44 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 45 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 46 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 47 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 48 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 49 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 50 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 51 | AV_F04_MARIGOLD: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 52 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 53 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 54 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 55 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 56 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 57 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 58 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 59 | AV_FE01_SWORD_FERN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 60 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 61 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 62 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 63 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 64 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 6,448 tris, 5,850 verts |
| 65 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 66 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 67 | AV_G01_MEADOW_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 68 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 69 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 70 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 71 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 72 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 73 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 74 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 75 | AV_G02_KANS_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 76 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 77 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 78 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 79 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 80 | AV_G02B_KANS_GRASS_SPRING: valid mesh, UVs | ✅ PASS | 4,760 tris, 4,095 verts |
| 81 | AV_G02B_KANS_GRASS_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 82 | AV_G02B_KANS_GRASS_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G02B_KANS_GRASS_SPRING_0, MAT_T6_AV_G02B_KANS_GRASS_SPRING_1 |
| 83 | AV_G02B_KANS_GRASS_SPRING: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 84 | AV_G02B_KANS_GRASS_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 85 | AV_G02B_KANS_GRASS_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 86 | AV_G02B_KANS_GRASS_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 87 | AV_G02B_KANS_GRASS_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 88 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 3,320 tris, 3,015 verts |
| 89 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 90 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 91 | AV_G03_DRY_PATH_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 92 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 93 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 94 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 95 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 96 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 97 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 98 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 99 | AV_M01_MOSS_CUSHION: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 100 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 101 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 102 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 103 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 104 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 105 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 106 | AV_MU01_BROWN_MUSHROOMS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 107 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 108 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 109 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 110 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 111 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 112 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 113 | AV_S01_BERBERIS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 114 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 115 | AV_S01_BERBERIS: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.83 m vs design 1.9 m |
| 116 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 117 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 118 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 119 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 120 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 121 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 122 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 123 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 124 | AV_S02_TULSI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 125 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 126 | AV_S02_TULSI: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.73 m vs design 0.75 m |
| 127 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 128 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 129 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 130 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 131 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 132 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,926 tris, 327,544 verts |
| 133 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 134 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 135 | AV_T01_PEEPAL: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 136 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 137 | AV_T01_PEEPAL: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 23.75 m vs design 22.0 m |
| 138 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 139 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 140 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 141 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 142 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 143 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 309,744 tris, 267,286 verts |
| 144 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 145 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 146 | AV_T02_DEODAR: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 147 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 148 | AV_T02_DEODAR: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 34.86 m vs design 34.0 m |
| 149 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 307 verts at the foot |
| 150 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 151 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 152 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 153 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 154 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 155 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 156 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 157 | AV_T03_CHIR_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 158 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 159 | AV_T03_CHIR_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 27.33 m vs design 28.0 m |
| 160 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 161 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 162 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 163 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 164 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 165 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,068 tris, 171,876 verts |
| 166 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 167 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 168 | AV_T04_BANJ_OAK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 169 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 170 | AV_T04_BANJ_OAK: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.45 m vs design 17.0 m |
| 171 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 172 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 173 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 174 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 175 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 176 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 177 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 178 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 179 | AV_T05_RHODODENDRON: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 180 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 181 | AV_T05_RHODODENDRON: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.19 m vs design 8.5 m |
| 182 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 183 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 184 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 185 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 186 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 187 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 188 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 189 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 190 | AV_T06_BAMBOO_CLUMP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 191 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 192 | AV_T06_BAMBOO_CLUMP: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.14 m vs design 15.0 m |
| 193 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 194 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 195 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 196 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 197 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 198 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 199 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.027 m · foot Δ 0.000 m |
| 200 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 201 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.3 MB |
| 202 | EF: opens in Blender 5.3.0, no missing images | ✅ PASS | 64 images, missing [] |
| 203 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 204 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 205 | EF: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 206 | EF: assets in library | ✅ PASS | 13 assets |
| 207 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 208 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 209 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 210 | EF_FE01_GIANT_FERN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 211 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 212 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 213 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 214 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 215 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 216 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 217 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 218 | EF_M01_MOSS_CARPET: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 219 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 220 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 221 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 222 | EF_M02_GLOW_MOSS: valid mesh, UVs | ✅ PASS | 8,600 tris, 5,832 verts |
| 223 | EF_M02_GLOW_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 224 | EF_M02_GLOW_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M02_GLOW_MOSS_0, MAT_T6_EF_M02_GLOW_MOSS_1 |
| 225 | EF_M02_GLOW_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 226 | EF_M02_GLOW_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 227 | EF_M02_GLOW_MOSS: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 228 | EF_M02_GLOW_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 229 | EF_M02_GLOW_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.15 |
| 230 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 231 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 232 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 233 | EF_MU01_GLOWCAP: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 234 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 235 | EF_MU01_GLOWCAP: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 236 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 237 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 238 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,958 tris, 389,340 verts |
| 239 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 240 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 241 | EF_T01_GIANT_ELDER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 242 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 243 | EF_T01_GIANT_ELDER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 66.79 m vs design 62.0 m |
| 244 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 504 verts at the foot |
| 245 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 246 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 247 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 248 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 249 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 251,408 tris, 214,441 verts |
| 250 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 251 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 252 | EF_T02_TEAL_BEECH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 253 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 254 | EF_T02_TEAL_BEECH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 34.60 m vs design 34.0 m |
| 255 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 342 verts at the foot |
| 256 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 257 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 258 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 259 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 260 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,120 tris, 177,671 verts |
| 261 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 262 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 263 | EF_T03_MOSS_OAK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 264 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 265 | EF_T03_MOSS_OAK: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 24.27 m vs design 23.0 m |
| 266 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 248 verts at the foot |
| 267 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 268 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 269 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 270 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 271 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 272 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 273 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 274 | EF_T04_YEW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 275 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 276 | EF_T04_YEW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.69 m vs design 9.0 m |
| 277 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 278 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 279 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 280 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 281 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 282 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 283 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 284 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 285 | EF_T05_VEIL_WILLOW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 286 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 287 | EF_T05_VEIL_WILLOW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 18.39 m vs design 18.0 m |
| 288 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 289 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 290 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 291 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 292 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 293 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 294 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,176 tris, 177,377 verts |
| 295 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 296 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 297 | EF_T06_SPIRAL_ROOT: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 298 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 299 | EF_T06_SPIRAL_ROOT: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 22.85 m vs design 24.0 m |
| 300 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.33 m, 495 verts at the foot |
| 301 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 302 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 303 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 304 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 305 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 306 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 307 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 308 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 309 | EF_T07_LANTERN_TREE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 310 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 311 | EF_T07_LANTERN_TREE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.11 m vs design 15.0 m |
| 312 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 313 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 314 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 315 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 316 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 317 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 318 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 319 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 320 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 321 | EF_T08_DEAD_SNAG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 322 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 323 | EF_T08_DEAD_SNAG: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 18.74 m vs design 17.0 m |
| 324 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 242 verts at the foot |
| 325 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 326 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 327 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 328 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 329 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 330 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 331 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 332 | EF_V01_HANGING_VINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 333 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 334 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 335 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 336 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 337 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.939 m · foot Δ 0.000 m |
| 338 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.002 m |
| 339 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 340 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 21.4 MB |
| 341 | MK: opens in Blender 5.3.0, no missing images | ✅ PASS | 46 images, missing [] |
| 342 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 343 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 344 | MK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 345 | MK: assets in library | ✅ PASS | 12 assets |
| 346 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 347 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 348 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 349 | MK_F01_GENTIAN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 350 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 351 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 352 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 353 | MK_F01_GENTIAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 354 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 355 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 356 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 357 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 358 | MK_F02_EDELWEISS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 359 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 360 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 361 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 362 | MK_F02_EDELWEISS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 363 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 364 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 365 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 366 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 367 | MK_F03_BLUE_POPPY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 368 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 369 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 370 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 371 | MK_F03_BLUE_POPPY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 372 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 373 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 5,280 tris, 4,800 verts |
| 374 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 375 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 376 | MK_G01_ALPINE_TUSSOCK: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 377 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 378 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 379 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 380 | MK_G01_ALPINE_TUSSOCK: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 381 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 382 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 383 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 384 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 385 | MK_M01_ALPINE_CUSHION: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 386 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 387 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 388 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 389 | MK_M01_ALPINE_CUSHION: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 390 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 391 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 392 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 393 | MK_S01_JUNIPER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 394 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 395 | MK_S01_JUNIPER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.82 m vs design 0.9 m |
| 396 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 397 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 398 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 399 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 400 | MK_S01_JUNIPER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 401 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 402 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 403 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 404 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 405 | MK_S02_DWARF_RHODODENDRON: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 406 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 407 | MK_S02_DWARF_RHODODENDRON: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 0.54 m vs design 0.6 m |
| 408 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 409 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 410 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 411 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 412 | MK_S02_DWARF_RHODODENDRON: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 413 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 414 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,706 tris, 188,378 verts |
| 415 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 416 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 417 | MK_T01_HIMALAYAN_SPRUCE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 418 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 419 | MK_T01_HIMALAYAN_SPRUCE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 31.32 m vs design 32.0 m |
| 420 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 308 verts at the foot |
| 421 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 422 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 423 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 424 | MK_T01_HIMALAYAN_SPRUCE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 425 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 426 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 427 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 428 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 429 | MK_T02_HIMALAYAN_BIRCH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 430 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 431 | MK_T02_HIMALAYAN_BIRCH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 11.59 m vs design 12.0 m |
| 432 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 433 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 434 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 435 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 436 | MK_T02_HIMALAYAN_BIRCH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 437 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 438 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 22,018 tris, 15,442 verts |
| 439 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 440 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 441 | MK_T03_KRUMMHOLZ_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 442 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 443 | MK_T03_KRUMMHOLZ_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 5.67 m vs design 5.5 m |
| 444 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 281 verts at the foot |
| 445 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 446 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 447 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 448 | MK_T03_KRUMMHOLZ_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 449 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 450 | MK_T04_SILVER_FIR: valid mesh, UVs | ✅ PASS | 256,348 tris, 216,552 verts |
| 451 | MK_T04_SILVER_FIR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 452 | MK_T04_SILVER_FIR: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T04_SILVER_FIR_BARK, MAT_T6_MK_T04_SILVER_FIR_LEAF, MAT_T6_MK_T04_SILVER_FIR_BARK |
| 453 | MK_T04_SILVER_FIR: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 454 | MK_T04_SILVER_FIR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 455 | MK_T04_SILVER_FIR: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 37.36 m vs design 36.0 m |
| 456 | MK_T04_SILVER_FIR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 287 verts at the foot |
| 457 | MK_T04_SILVER_FIR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 458 | MK_T04_SILVER_FIR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 459 | MK_T04_SILVER_FIR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 460 | MK_T04_SILVER_FIR: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 461 | MK_T04_SILVER_FIR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 462 | MK_T05_BLUE_PINE: valid mesh, UVs | ✅ PASS | 126,070 tris, 112,360 verts |
| 463 | MK_T05_BLUE_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 464 | MK_T05_BLUE_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T05_BLUE_PINE_BARK, MAT_T6_MK_T05_BLUE_PINE_LEAF, MAT_T6_MK_T05_BLUE_PINE_BARK |
| 465 | MK_T05_BLUE_PINE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 466 | MK_T05_BLUE_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 467 | MK_T05_BLUE_PINE: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 31.42 m vs design 30.0 m |
| 468 | MK_T05_BLUE_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.42 m, 305 verts at the foot |
| 469 | MK_T05_BLUE_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 470 | MK_T05_BLUE_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 471 | MK_T05_BLUE_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 472 | MK_T05_BLUE_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 473 | MK_T05_BLUE_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 474 | MK_T04_SILVER_FIR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 475 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |
| 476 | PL: library file exists | ✅ PASS | library/T6_VEG_GREEN_PLAINS_v001.blend |
| 477 | PL: file size < 100 MB (GitHub limit) | ✅ PASS | 33.9 MB |
| 478 | PL: opens in Blender 5.3.0, no missing images | ✅ PASS | 27 images, missing [] |
| 479 | PL: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 480 | PL: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 481 | PL: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 482 | PL: assets in library | ✅ PASS | 9 assets |
| 483 | PL_F01_WILD_MUSTARD: valid mesh, UVs | ✅ PASS | 3,460 tris, 2,624 verts |
| 484 | PL_F01_WILD_MUSTARD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 485 | PL_F01_WILD_MUSTARD: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F01_WILD_MUSTARD_0, MAT_T6_PL_F01_WILD_MUSTARD_1, MAT_T6_PL_F01_WILD_MUSTARD_2 |
| 486 | PL_F01_WILD_MUSTARD: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 487 | PL_F01_WILD_MUSTARD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 488 | PL_F01_WILD_MUSTARD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 489 | PL_F01_WILD_MUSTARD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 490 | PL_F01_WILD_MUSTARD: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 491 | PL_F01_WILD_MUSTARD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 492 | PL_F02_GLOBE_THISTLE: valid mesh, UVs | ✅ PASS | 39,852 tris, 32,698 verts |
| 493 | PL_F02_GLOBE_THISTLE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 494 | PL_F02_GLOBE_THISTLE: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F02_GLOBE_THISTLE_0, MAT_T6_PL_F02_GLOBE_THISTLE_1, MAT_T6_PL_F02_GLOBE_THISTLE_2 |
| 495 | PL_F02_GLOBE_THISTLE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 496 | PL_F02_GLOBE_THISTLE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 497 | PL_F02_GLOBE_THISTLE: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 498 | PL_F02_GLOBE_THISTLE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 499 | PL_F02_GLOBE_THISTLE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 500 | PL_F02_GLOBE_THISTLE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 501 | PL_F03_WHITE_CLOVER: valid mesh, UVs | ✅ PASS | 29,320 tris, 23,982 verts |
| 502 | PL_F03_WHITE_CLOVER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 503 | PL_F03_WHITE_CLOVER: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_F03_WHITE_CLOVER_0, MAT_T6_PL_F03_WHITE_CLOVER_1, MAT_T6_PL_F03_WHITE_CLOVER_2 |
| 504 | PL_F03_WHITE_CLOVER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 505 | PL_F03_WHITE_CLOVER: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 506 | PL_F03_WHITE_CLOVER: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 507 | PL_F03_WHITE_CLOVER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 508 | PL_F03_WHITE_CLOVER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 509 | PL_F03_WHITE_CLOVER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 510 | PL_G01_TALL_GRASS: valid mesh, UVs | ✅ PASS | 7,840 tris, 6,750 verts |
| 511 | PL_G01_TALL_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 512 | PL_G01_TALL_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_PL_G01_TALL_GRASS_0, MAT_T6_PL_G01_TALL_GRASS_1 |
| 513 | PL_G01_TALL_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 514 | PL_G01_TALL_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 515 | PL_G01_TALL_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 516 | PL_G01_TALL_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 517 | PL_G01_TALL_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 518 | PL_G01_TALL_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 519 | PL_G02_DOOB_GRASS: valid mesh, UVs | ✅ PASS | 6,272 tris, 5,952 verts |
| 520 | PL_G02_DOOB_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 521 | PL_G02_DOOB_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_PL_G02_DOOB_GRASS_0, MAT_T6_PL_G02_DOOB_GRASS_1 |
| 522 | PL_G02_DOOB_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 523 | PL_G02_DOOB_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 524 | PL_G02_DOOB_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 525 | PL_G02_DOOB_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 526 | PL_G02_DOOB_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 527 | PL_G02_DOOB_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 528 | PL_S01_BER_BUSH: valid mesh, UVs | ✅ PASS | 6,388 tris, 6,372 verts |
| 529 | PL_S01_BER_BUSH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 530 | PL_S01_BER_BUSH: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_S01_BER_BUSH_BARK, MAT_T6_PL_S01_BER_BUSH_LEAF, MAT_T6_PL_S01_BER_BUSH_BARK |
| 531 | PL_S01_BER_BUSH: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 532 | PL_S01_BER_BUSH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 533 | PL_S01_BER_BUSH: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 2.15 m vs design 2.2 m |
| 534 | PL_S01_BER_BUSH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.17 m, 206 verts at the foot |
| 535 | PL_S01_BER_BUSH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 536 | PL_S01_BER_BUSH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 537 | PL_S01_BER_BUSH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 538 | PL_S01_BER_BUSH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 539 | PL_S01_BER_BUSH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 540 | PL_T01_BANYAN: valid mesh, UVs | ✅ PASS | 713,372 tris, 536,370 verts |
| 541 | PL_T01_BANYAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 542 | PL_T01_BANYAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T01_BANYAN_BARK, MAT_T6_PL_T01_BANYAN_LEAF, MAT_T6_PL_T01_BANYAN_BARK |
| 543 | PL_T01_BANYAN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 544 | PL_T01_BANYAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 545 | PL_T01_BANYAN: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 21.40 m vs design 21.0 m |
| 546 | PL_T01_BANYAN: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.55 m, 194 verts at the foot |
| 547 | PL_T01_BANYAN: no limbs through the ground (prop roots allowed) | ✅ PASS | 4 verts far + under ground |
| 548 | PL_T01_BANYAN: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 549 | PL_T01_BANYAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 550 | PL_T01_BANYAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 551 | PL_T01_BANYAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 552 | PL_T02_NEEM: valid mesh, UVs | ✅ PASS | 245,900 tris, 200,888 verts |
| 553 | PL_T02_NEEM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 554 | PL_T02_NEEM: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T02_NEEM_BARK, MAT_T6_PL_T02_NEEM_LEAF, MAT_T6_PL_T02_NEEM_BARK |
| 555 | PL_T02_NEEM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 556 | PL_T02_NEEM: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 557 | PL_T02_NEEM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.27 m vs design 15.0 m |
| 558 | PL_T02_NEEM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.39 m, 327 verts at the foot |
| 559 | PL_T02_NEEM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 560 | PL_T02_NEEM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 561 | PL_T02_NEEM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 562 | PL_T02_NEEM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 563 | PL_T02_NEEM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 564 | PL_T03_UMBRELLA_ACACIA: valid mesh, UVs | ✅ PASS | 275,386 tris, 204,434 verts |
| 565 | PL_T03_UMBRELLA_ACACIA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 566 | PL_T03_UMBRELLA_ACACIA: PBR materials (3 slots) | ✅ PASS | MAT_T6_PL_T03_UMBRELLA_ACACIA_BARK, MAT_T6_PL_T03_UMBRELLA_ACACIA_LEAF, MAT_T6_PL_T03_UMBRELLA_ACACIA_BARK |
| 567 | PL_T03_UMBRELLA_ACACIA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 568 | PL_T03_UMBRELLA_ACACIA: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 569 | PL_T03_UMBRELLA_ACACIA: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 9.46 m vs design 9.0 m |
| 570 | PL_T03_UMBRELLA_ACACIA: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 32 verts at the foot |
| 571 | PL_T03_UMBRELLA_ACACIA: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 572 | PL_T03_UMBRELLA_ACACIA: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 573 | PL_T03_UMBRELLA_ACACIA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 574 | PL_T03_UMBRELLA_ACACIA: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 575 | PL_T03_UMBRELLA_ACACIA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 576 | PL_T01_BANYAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.416 m · foot Δ 0.000 m |
| 577 | PL_F01_WILD_MUSTARD: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.033 m · foot Δ 0.004 m |
| 578 | LK: library file exists | ✅ PASS | library/T6_VEG_CRYSTAL_LAKES_v001.blend |
| 579 | LK: file size < 100 MB (GitHub limit) | ✅ PASS | 11.6 MB |
| 580 | LK: opens in Blender 5.3.0, no missing images | ✅ PASS | 19 images, missing [] |
| 581 | LK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 582 | LK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 583 | LK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 584 | LK: assets in library | ✅ PASS | 6 assets |
| 585 | LK_AQ01_WATER_LILY: valid mesh, UVs | ✅ PASS | 4,240 tris, 3,406 verts |
| 586 | LK_AQ01_WATER_LILY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 587 | LK_AQ01_WATER_LILY: PBR materials (4 slots) | ✅ PASS | MAT_T6_LK_AQ01_WATER_LILY_0, MAT_T6_LK_AQ01_WATER_LILY_1, MAT_T6_LK_AQ01_WATER_LILY_2, MAT_T6_LK_AQ01_WATER_LILY_3 |
| 588 | LK_AQ01_WATER_LILY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 589 | LK_AQ01_WATER_LILY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 590 | LK_AQ01_WATER_LILY: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.90 m, top 0.07 m |
| 591 | LK_AQ01_WATER_LILY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 592 | LK_AQ01_WATER_LILY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 593 | LK_AQ01_WATER_LILY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 594 | LK_AQ02_SEDGE: valid mesh, UVs | ✅ PASS | 5,260 tris, 4,632 verts |
| 595 | LK_AQ02_SEDGE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 596 | LK_AQ02_SEDGE: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_AQ02_SEDGE_0, MAT_T6_LK_AQ02_SEDGE_1 |
| 597 | LK_AQ02_SEDGE: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 598 | LK_AQ02_SEDGE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 599 | LK_AQ02_SEDGE: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 600 | LK_AQ02_SEDGE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 601 | LK_AQ02_SEDGE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 602 | LK_AQ02_SEDGE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 603 | LK_AQ03_REED_SPRING: valid mesh, UVs | ✅ PASS | 3,636 tris, 3,078 verts |
| 604 | LK_AQ03_REED_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 605 | LK_AQ03_REED_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_AQ03_REED_SPRING_0, MAT_T6_LK_AQ03_REED_SPRING_1 |
| 606 | LK_AQ03_REED_SPRING: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 607 | LK_AQ03_REED_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 608 | LK_AQ03_REED_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 609 | LK_AQ03_REED_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 610 | LK_AQ03_REED_SPRING: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 611 | LK_AQ03_REED_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 612 | LK_M01_WET_ROCK_MOSS: valid mesh, UVs | ✅ PASS | 3,480 tris, 2,256 verts |
| 613 | LK_M01_WET_ROCK_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 614 | LK_M01_WET_ROCK_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_LK_M01_WET_ROCK_MOSS_0, MAT_T6_LK_M01_WET_ROCK_MOSS_1 |
| 615 | LK_M01_WET_ROCK_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 616 | LK_M01_WET_ROCK_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 617 | LK_M01_WET_ROCK_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 618 | LK_M01_WET_ROCK_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 619 | LK_M01_WET_ROCK_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 620 | LK_T01_WHITE_WILLOW: valid mesh, UVs | ✅ PASS | 288,540 tris, 222,262 verts |
| 621 | LK_T01_WHITE_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 622 | LK_T01_WHITE_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_LK_T01_WHITE_WILLOW_BARK, MAT_T6_LK_T01_WHITE_WILLOW_LEAF, MAT_T6_LK_T01_WHITE_WILLOW_BARK |
| 623 | LK_T01_WHITE_WILLOW: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 624 | LK_T01_WHITE_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 625 | LK_T01_WHITE_WILLOW: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 17.91 m vs design 16.0 m |
| 626 | LK_T01_WHITE_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.55 m, 335 verts at the foot |
| 627 | LK_T01_WHITE_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 628 | LK_T01_WHITE_WILLOW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 629 | LK_T01_WHITE_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 630 | LK_T01_WHITE_WILLOW: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 631 | LK_T01_WHITE_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 632 | LK_T02_ALDER: valid mesh, UVs | ✅ PASS | 133,524 tris, 108,106 verts |
| 633 | LK_T02_ALDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 634 | LK_T02_ALDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_LK_T02_ALDER_BARK, MAT_T6_LK_T02_ALDER_LEAF, MAT_T6_LK_T02_ALDER_BARK |
| 635 | LK_T02_ALDER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 636 | LK_T02_ALDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 637 | LK_T02_ALDER: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 20.39 m vs design 20.0 m |
| 638 | LK_T02_ALDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.33 m, 333 verts at the foot |
| 639 | LK_T02_ALDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 640 | LK_T02_ALDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 641 | LK_T02_ALDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 642 | LK_T02_ALDER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 643 | LK_T02_ALDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 644 | LK_T02_ALDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.360 m · foot Δ 0.000 m |
| 645 | LK_AQ01_WATER_LILY: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.008 m · foot Δ 0.002 m |
| 646 | DS: library file exists | ✅ PASS | library/T6_VEG_GOLDEN_DESERT_v001.blend |
| 647 | DS: file size < 100 MB (GitHub limit) | ✅ PASS | 10.1 MB |
| 648 | DS: opens in Blender 5.3.0, no missing images | ✅ PASS | 21 images, missing [] |
| 649 | DS: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 650 | DS: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 651 | DS: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 652 | DS: assets in library | ✅ PASS | 5 assets |
| 653 | DS_G01_SEWAN_GRASS: valid mesh, UVs | ✅ PASS | 5,100 tris, 4,500 verts |
| 654 | DS_G01_SEWAN_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 655 | DS_G01_SEWAN_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_DS_G01_SEWAN_GRASS_0, MAT_T6_DS_G01_SEWAN_GRASS_1 |
| 656 | DS_G01_SEWAN_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 657 | DS_G01_SEWAN_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 658 | DS_G01_SEWAN_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 659 | DS_G01_SEWAN_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 660 | DS_G01_SEWAN_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 661 | DS_G01_SEWAN_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 662 | DS_S01_CALOTROPIS: valid mesh, UVs | ✅ PASS | 2,910 tris, 2,340 verts |
| 663 | DS_S01_CALOTROPIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 664 | DS_S01_CALOTROPIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_DS_S01_CALOTROPIS_BARK, MAT_T6_DS_S01_CALOTROPIS_LEAF, MAT_T6_DS_S01_CALOTROPIS_BARK |
| 665 | DS_S01_CALOTROPIS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 666 | DS_S01_CALOTROPIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 667 | DS_S01_CALOTROPIS: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.76 m vs design 1.8 m |
| 668 | DS_S01_CALOTROPIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.13 m, 108 verts at the foot |
| 669 | DS_S01_CALOTROPIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 670 | DS_S01_CALOTROPIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 671 | DS_S01_CALOTROPIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 672 | DS_S01_CALOTROPIS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 673 | DS_S01_CALOTROPIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 674 | DS_S02_EUPHORBIA: valid mesh, UVs | ✅ PASS | 31,760 tris, 20,400 verts |
| 675 | DS_S02_EUPHORBIA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 676 | DS_S02_EUPHORBIA: PBR materials (2 slots) | ✅ PASS | MAT_T6_DS_S02_EUPHORBIA_0, MAT_T6_DS_S02_EUPHORBIA_1 |
| 677 | DS_S02_EUPHORBIA: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 678 | DS_S02_EUPHORBIA: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 679 | DS_S02_EUPHORBIA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.051 m |
| 680 | DS_S02_EUPHORBIA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 681 | DS_S02_EUPHORBIA: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 682 | DS_S02_EUPHORBIA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 683 | DS_T01_KHEJRI: valid mesh, UVs | ✅ PASS | 247,022 tris, 207,672 verts |
| 684 | DS_T01_KHEJRI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 685 | DS_T01_KHEJRI: PBR materials (3 slots) | ✅ PASS | MAT_T6_DS_T01_KHEJRI_BARK, MAT_T6_DS_T01_KHEJRI_LEAF, MAT_T6_DS_T01_KHEJRI_BARK |
| 686 | DS_T01_KHEJRI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 687 | DS_T01_KHEJRI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 688 | DS_T01_KHEJRI: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 8.28 m vs design 8.0 m |
| 689 | DS_T01_KHEJRI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 337 verts at the foot |
| 690 | DS_T01_KHEJRI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 691 | DS_T01_KHEJRI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 692 | DS_T01_KHEJRI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 693 | DS_T01_KHEJRI: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 694 | DS_T01_KHEJRI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 695 | DS_T02_DATE_PALM: valid mesh, UVs | ✅ PASS | 102,320 tris, 92,626 verts |
| 696 | DS_T02_DATE_PALM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 697 | DS_T02_DATE_PALM: PBR materials (4 slots) | ✅ PASS | MAT_T6_DS_T02_DATE_PALM_BARK, MAT_T6_DS_T02_DATE_PALM_FROND, MAT_T6_DS_T02_DATE_PALM_DEADFROND, MAT_T6_DS_T02_DATE_PALM_ |
| 698 | DS_T02_DATE_PALM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 699 | DS_T02_DATE_PALM: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 700 | DS_T02_DATE_PALM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 13.83 m vs design 14.0 m |
| 701 | DS_T02_DATE_PALM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.36 m, 32 verts at the foot |
| 702 | DS_T02_DATE_PALM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 703 | DS_T02_DATE_PALM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 704 | DS_T02_DATE_PALM: palm — trunk scan + frond / dead-frond materials, fronds attached to the crown | ✅ PASS | MAT_T6_DS_T02_DATE_PALM_FROND, MAT_T6_DS_T02_DATE_PALM_DEADFROND |
| 705 | DS_T02_DATE_PALM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 706 | DS_T02_DATE_PALM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 707 | DS_T02_DATE_PALM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 708 | DS_T02_DATE_PALM: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.259 m · foot Δ 0.000 m |
| 709 | DS_G01_SEWAN_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.033 m · foot Δ 0.016 m |
| 710 | FB: library file exists | ✅ PASS | library/T6_VEG_FORBIDDEN_LANDS_v001.blend |
| 711 | FB: file size < 100 MB (GitHub limit) | ✅ PASS | 0.5 MB |
| 712 | FB: opens in Blender 5.3.0, no missing images | ✅ PASS | 10 images, missing [] |
| 713 | FB: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 714 | FB: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 715 | FB: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 716 | FB: assets in library | ✅ PASS | 4 assets |
| 717 | FB_G01_HARDY_GRASS: valid mesh, UVs | ✅ PASS | 1,580 tris, 1,440 verts |
| 718 | FB_G01_HARDY_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 719 | FB_G01_HARDY_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_FB_G01_HARDY_GRASS_0, MAT_T6_FB_G01_HARDY_GRASS_1 |
| 720 | FB_G01_HARDY_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 721 | FB_G01_HARDY_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 722 | FB_G01_HARDY_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 723 | FB_G01_HARDY_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 724 | FB_G01_HARDY_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 725 | FB_G01_HARDY_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 726 | FB_M01_ASH_LICHEN: valid mesh, UVs | ✅ PASS | 3,080 tris, 1,848 verts |
| 727 | FB_M01_ASH_LICHEN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 728 | FB_M01_ASH_LICHEN: PBR materials (2 slots) | ✅ PASS | MAT_T6_FB_M01_ASH_LICHEN_0, MAT_T6_FB_M01_ASH_LICHEN_1 |
| 729 | FB_M01_ASH_LICHEN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 730 | FB_M01_ASH_LICHEN: every face has a valid material slot | ✅ PASS | slots used [0] |
| 731 | FB_M01_ASH_LICHEN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 732 | FB_M01_ASH_LICHEN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 733 | FB_M01_ASH_LICHEN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 734 | FB_S01_DEAD_THORN_SHRUB: valid mesh, UVs | ✅ PASS | 1,798 tris, 1,092 verts |
| 735 | FB_S01_DEAD_THORN_SHRUB: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 736 | FB_S01_DEAD_THORN_SHRUB: PBR materials (3 slots) | ✅ PASS | MAT_T6_FB_S01_DEAD_THORN_SHRUB_BARK, MAT_T6_FB_S01_DEAD_THORN_SHRUB_NOLEAF, MAT_T6_FB_S01_DEAD_THORN_SHRUB_BARK |
| 737 | FB_S01_DEAD_THORN_SHRUB: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 738 | FB_S01_DEAD_THORN_SHRUB: every face has a valid material slot | ✅ PASS | slots used [0] |
| 739 | FB_S01_DEAD_THORN_SHRUB: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 1.43 m vs design 1.4 m |
| 740 | FB_S01_DEAD_THORN_SHRUB: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.21 m, 122 verts at the foot |
| 741 | FB_S01_DEAD_THORN_SHRUB: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 742 | FB_S01_DEAD_THORN_SHRUB: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 743 | FB_S01_DEAD_THORN_SHRUB: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 744 | FB_S01_DEAD_THORN_SHRUB: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 745 | FB_S01_DEAD_THORN_SHRUB: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 746 | FB_T01_CHARRED_SNAG: valid mesh, UVs | ✅ PASS | 6,256 tris, 3,688 verts |
| 747 | FB_T01_CHARRED_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 748 | FB_T01_CHARRED_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_FB_T01_CHARRED_SNAG_BARK, MAT_T6_FB_T01_CHARRED_SNAG_NOLEAF, MAT_T6_FB_T01_CHARRED_SNAG_BARK |
| 749 | FB_T01_CHARRED_SNAG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 750 | FB_T01_CHARRED_SNAG: every face has a valid material slot | ✅ PASS | slots used [0] |
| 751 | FB_T01_CHARRED_SNAG: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 12.29 m vs design 12.0 m |
| 752 | FB_T01_CHARRED_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.40 m, 245 verts at the foot |
| 753 | FB_T01_CHARRED_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 754 | FB_T01_CHARRED_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 755 | FB_T01_CHARRED_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 756 | FB_T01_CHARRED_SNAG: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 757 | FB_T01_CHARRED_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 758 | FB_T01_CHARRED_SNAG: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.074 m · foot Δ 0.000 m |
| 759 | FB_G01_HARDY_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.023 m · foot Δ 0.019 m |
| 760 | CT: library file exists | ✅ PASS | library/T6_VEG_ANCIENT_CITY_SITES_v001.blend |
| 761 | CT: file size < 100 MB (GitHub limit) | ✅ PASS | 9.6 MB |
| 762 | CT: opens in Blender 5.3.0, no missing images | ✅ PASS | 21 images, missing [] |
| 763 | CT: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 764 | CT: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 765 | CT: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 766 | CT: assets in library | ✅ PASS | 5 assets |
| 767 | CT_G01_CRACK_GRASS: valid mesh, UVs | ✅ PASS | 1,176 tris, 1,116 verts |
| 768 | CT_G01_CRACK_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 769 | CT_G01_CRACK_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_G01_CRACK_GRASS_0, MAT_T6_CT_G01_CRACK_GRASS_1 |
| 770 | CT_G01_CRACK_GRASS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 771 | CT_G01_CRACK_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 772 | CT_G01_CRACK_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 773 | CT_G01_CRACK_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 774 | CT_G01_CRACK_GRASS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 775 | CT_G01_CRACK_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 776 | CT_M01_RUIN_MOSS: valid mesh, UVs | ✅ PASS | 3,680 tris, 2,460 verts |
| 777 | CT_M01_RUIN_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 778 | CT_M01_RUIN_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_M01_RUIN_MOSS_0, MAT_T6_CT_M01_RUIN_MOSS_1 |
| 779 | CT_M01_RUIN_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 780 | CT_M01_RUIN_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 781 | CT_M01_RUIN_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 782 | CT_M01_RUIN_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 783 | CT_M01_RUIN_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 784 | CT_T01_MANGO: valid mesh, UVs | ✅ PASS | 298,640 tris, 228,428 verts |
| 785 | CT_T01_MANGO: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 786 | CT_T01_MANGO: PBR materials (3 slots) | ✅ PASS | MAT_T6_CT_T01_MANGO_BARK, MAT_T6_CT_T01_MANGO_LEAF, MAT_T6_CT_T01_MANGO_BARK |
| 787 | CT_T01_MANGO: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 788 | CT_T01_MANGO: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 789 | CT_T01_MANGO: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 15.27 m vs design 16.0 m |
| 790 | CT_T01_MANGO: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 444 verts at the foot |
| 791 | CT_T01_MANGO: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 792 | CT_T01_MANGO: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 793 | CT_T01_MANGO: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 794 | CT_T01_MANGO: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 795 | CT_T01_MANGO: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 796 | CT_T02_COCONUT_PALM: valid mesh, UVs | ✅ PASS | 69,432 tris, 62,562 verts |
| 797 | CT_T02_COCONUT_PALM: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 798 | CT_T02_COCONUT_PALM: PBR materials (4 slots) | ✅ PASS | MAT_T6_CT_T02_COCONUT_PALM_BARK, MAT_T6_CT_T02_COCONUT_PALM_FROND, MAT_T6_CT_T02_COCONUT_PALM_DEADFROND, MAT_T6_CT_T02_C |
| 799 | CT_T02_COCONUT_PALM: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 800 | CT_T02_COCONUT_PALM: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 801 | CT_T02_COCONUT_PALM: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %) | ✅ PASS | 16.06 m vs design 17.0 m |
| 802 | CT_T02_COCONUT_PALM: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.36 m, 32 verts at the foot |
| 803 | CT_T02_COCONUT_PALM: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 804 | CT_T02_COCONUT_PALM: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 805 | CT_T02_COCONUT_PALM: palm — trunk scan + frond / dead-frond materials, fronds attached to the crown | ✅ PASS | MAT_T6_CT_T02_COCONUT_PALM_FROND, MAT_T6_CT_T02_COCONUT_PALM_DEADFROND |
| 806 | CT_T02_COCONUT_PALM: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 807 | CT_T02_COCONUT_PALM: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 808 | CT_T02_COCONUT_PALM: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 809 | CT_V01_IVY_CURTAIN: valid mesh, UVs | ✅ PASS | 4,114 tris, 3,616 verts |
| 810 | CT_V01_IVY_CURTAIN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 811 | CT_V01_IVY_CURTAIN: PBR materials (2 slots) | ✅ PASS | MAT_T6_CT_V01_IVY_CURTAIN_0, MAT_T6_CT_V01_IVY_CURTAIN_1 |
| 812 | CT_V01_IVY_CURTAIN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 813 | CT_V01_IVY_CURTAIN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 814 | CT_V01_IVY_CURTAIN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.035 m |
| 815 | CT_V01_IVY_CURTAIN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 816 | CT_V01_IVY_CURTAIN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 817 | CT_V01_IVY_CURTAIN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 818 | CT_T02_COCONUT_PALM: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.215 m · foot Δ 0.000 m |
| 819 | CT_G01_CRACK_GRASS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.018 m · foot Δ 0.014 m |
| 820 | CV: library file exists | ✅ PASS | library/T6_VEG_HIDDEN_UNDERGROUND_v001.blend |
| 821 | CV: file size < 100 MB (GitHub limit) | ✅ PASS | 0.4 MB |
| 822 | CV: opens in Blender 5.3.0, no missing images | ✅ PASS | 5 images, missing [] |
| 823 | CV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 824 | CV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 825 | CV: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 826 | CV: assets in library | ✅ PASS | 3 assets |
| 827 | CV_M01_PALE_CAVE_MOSS: valid mesh, UVs | ✅ PASS | 2,820 tris, 1,818 verts |
| 828 | CV_M01_PALE_CAVE_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 829 | CV_M01_PALE_CAVE_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_CV_M01_PALE_CAVE_MOSS_0, MAT_T6_CV_M01_PALE_CAVE_MOSS_1 |
| 830 | CV_M01_PALE_CAVE_MOSS: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 831 | CV_M01_PALE_CAVE_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 832 | CV_M01_PALE_CAVE_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 833 | CV_M01_PALE_CAVE_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 834 | CV_M01_PALE_CAVE_MOSS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 835 | CV_MU01_CAVE_FUNGI: valid mesh, UVs | ✅ PASS | 6,208 tris, 4,032 verts |
| 836 | CV_MU01_CAVE_FUNGI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 837 | CV_MU01_CAVE_FUNGI: PBR materials (3 slots) | ✅ PASS | MAT_T6_CV_MU01_CAVE_FUNGI_0, MAT_T6_CV_MU01_CAVE_FUNGI_1, MAT_T6_CV_MU01_CAVE_FUNGI_2 |
| 838 | CV_MU01_CAVE_FUNGI: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 839 | CV_MU01_CAVE_FUNGI: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 840 | CV_MU01_CAVE_FUNGI: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 841 | CV_MU01_CAVE_FUNGI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 842 | CV_MU01_CAVE_FUNGI: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 843 | CV_V01_ROOT_CURTAIN: valid mesh, UVs | ✅ PASS | 5,280 tris, 2,750 verts |
| 844 | CV_V01_ROOT_CURTAIN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 845 | CV_V01_ROOT_CURTAIN: PBR materials (1 slots) | ✅ PASS | MAT_T6_CV_V01_ROOT_CURTAIN_0 |
| 846 | CV_V01_ROOT_CURTAIN: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 847 | CV_V01_ROOT_CURTAIN: every face has a valid material slot | ✅ PASS | slots used [0] |
| 848 | CV_V01_ROOT_CURTAIN: hanging plant attaches at its top (hangs from a branch, z_top = 3.6 m) | ✅ PASS | z 0.06–3.60 m |
| 849 | CV_V01_ROOT_CURTAIN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 850 | CV_V01_ROOT_CURTAIN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 851 | CV_V01_ROOT_CURTAIN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 852 | CV_V01_ROOT_CURTAIN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.021 m · foot Δ 0.000 m |
| 853 | ND: library file exists | ✅ PASS | library/T6_VEG_NATURAL_DETAILS_v001.blend |
| 854 | ND: file size < 100 MB (GitHub limit) | ✅ PASS | 2.1 MB |
| 855 | ND: opens in Blender 5.3.0, no missing images | ✅ PASS | 29 images, missing [] |
| 856 | ND: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 857 | ND: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 858 | ND: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 859 | ND: assets in library | ✅ PASS | 6 assets |
| 860 | ND_B01_FALLEN_BRANCHES: valid mesh, UVs | ✅ PASS | 1,312 tris, 788 verts |
| 861 | ND_B01_FALLEN_BRANCHES: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 862 | ND_B01_FALLEN_BRANCHES: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_B01_FALLEN_BRANCHES_0, MAT_T6_ND_B01_FALLEN_BRANCHES_1 |
| 863 | ND_B01_FALLEN_BRANCHES: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 864 | ND_B01_FALLEN_BRANCHES: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 865 | ND_B01_FALLEN_BRANCHES: plant base on the ground (no floating) | ✅ PASS | lowest z -0.029 m |
| 866 | ND_B01_FALLEN_BRANCHES: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 867 | ND_B02_GIANT_LOG: valid mesh, UVs | ✅ PASS | 6,000 tris, 3,549 verts |
| 868 | ND_B02_GIANT_LOG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 869 | ND_B02_GIANT_LOG: PBR materials (4 slots) | ✅ PASS | MAT_T6_ND_B02_GIANT_LOG_0, MAT_T6_ND_B02_GIANT_LOG_1, MAT_T6_ND_B02_GIANT_LOG_2, MAT_T6_ND_B02_GIANT_LOG_3 |
| 870 | ND_B02_GIANT_LOG: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 871 | ND_B02_GIANT_LOG: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 872 | ND_B02_GIANT_LOG: plant base on the ground (no floating) | ✅ PASS | lowest z -0.102 m |
| 873 | ND_B02_GIANT_LOG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 874 | ND_I01_GROUND_IVY: valid mesh, UVs | ✅ PASS | 2,704 tris, 2,437 verts |
| 875 | ND_I01_GROUND_IVY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 876 | ND_I01_GROUND_IVY: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_I01_GROUND_IVY_0, MAT_T6_ND_I01_GROUND_IVY_1 |
| 877 | ND_I01_GROUND_IVY: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 878 | ND_I01_GROUND_IVY: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 879 | ND_I01_GROUND_IVY: plant base on the ground (no floating) | ✅ PASS | lowest z 0.000 m |
| 880 | ND_I01_GROUND_IVY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 881 | ND_I01_GROUND_IVY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 882 | ND_L01_LEAF_LITTER_BROADLEAF: valid mesh, UVs | ✅ PASS | 3,760 tris, 4,020 verts |
| 883 | ND_L01_LEAF_LITTER_BROADLEAF: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 884 | ND_L01_LEAF_LITTER_BROADLEAF: PBR materials (3 slots) | ✅ PASS | MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_0, MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_1, MAT_T6_ND_L01_LEAF_LITTER_BROADLEAF_2 |
| 885 | ND_L01_LEAF_LITTER_BROADLEAF: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 886 | ND_L01_LEAF_LITTER_BROADLEAF: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 887 | ND_L01_LEAF_LITTER_BROADLEAF: plant base on the ground (no floating) | ✅ PASS | lowest z -0.003 m |
| 888 | ND_L01_LEAF_LITTER_BROADLEAF: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 889 | ND_L02_NEEDLE_LITTER: valid mesh, UVs | ✅ PASS | 41,464 tris, 65,321 verts |
| 890 | ND_L02_NEEDLE_LITTER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 891 | ND_L02_NEEDLE_LITTER: PBR materials (3 slots) | ✅ PASS | MAT_T6_ND_L02_NEEDLE_LITTER_0, MAT_T6_ND_L02_NEEDLE_LITTER_1, MAT_T6_ND_L02_NEEDLE_LITTER_2 |
| 892 | ND_L02_NEEDLE_LITTER: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 893 | ND_L02_NEEDLE_LITTER: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 894 | ND_L02_NEEDLE_LITTER: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 895 | ND_L02_NEEDLE_LITTER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 896 | ND_W01_FLOATING_LEAVES: valid mesh, UVs | ✅ PASS | 720 tris, 810 verts |
| 897 | ND_W01_FLOATING_LEAVES: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 898 | ND_W01_FLOATING_LEAVES: PBR materials (2 slots) | ✅ PASS | MAT_T6_ND_W01_FLOATING_LEAVES_0, MAT_T6_ND_W01_FLOATING_LEAVES_1 |
| 899 | ND_W01_FLOATING_LEAVES: no empty material slot (renders white otherwise) | ✅ PASS |  |
| 900 | ND_W01_FLOATING_LEAVES: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 901 | ND_W01_FLOATING_LEAVES: plant base on the ground (no floating) | ✅ PASS | lowest z 0.000 m |
| 902 | ND_W01_FLOATING_LEAVES: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 903 | ND_W01_FLOATING_LEAVES: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 904 | ND_I01_GROUND_IVY: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.007 m · foot Δ 0.002 m |

## Blender populated files (Blender 4.5.16 LTS) — **58/58 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | TASK 05 approved files untouched (git: no change under 02_world/3d_world) | ✅ PASS | clean |
| 2 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.26 MB |
| 3 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: opens, no missing images / libraries | ✅ PASS | 16 libraries, missing images [] |
| 4 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: ecosystem layers | ✅ PASS | 23 layers |
| 5 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 6 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 7 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: every linked variant / LOD has its materials (no empty slots) | ✅ PASS | 92 objects; empty: [] |
| 8 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 9 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: Tulsi = 6 plants, all inside the PROPOSED garden beds (x ±6…28, y −30…−52) | ✅ PASS | 6 Tulsi instances |
| 10 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: exactly ONE Peepal (landmark, courtyard) | ✅ PASS | 1 instance(s), 0 Peepal scatter layers |
| 11 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 12 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 1,346,284 instances (ground layers ≥ 0.03 / m² sampled at 1 %); empty [] |
| 13 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 1216 samples, median 0.012 m, max 0.05 m, 100.0% OK |
| 14 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: wind bends the realized near plants (ECO_AV_F04_MARIGOLD_D_W_PROPOSED) | ✅ PASS | 3,034,602 verts, max Δ 0.087 m in 0.5 s |
| 15 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.24 MB |
| 16 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: opens, no missing images / libraries | ✅ PASS | 13 libraries, missing images [] |
| 17 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: ecosystem layers | ✅ PASS | 17 layers |
| 18 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 19 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 20 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: every linked variant / LOD has its materials (no empty slots) | ✅ PASS | 84 objects; empty: [] |
| 21 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 22 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 487,061 instances (ground layers ≥ 0.03 / m² sampled at 1 %); empty [] |
| 23 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 1020 samples, median 0.012 m, max 0.05 m, 100.0% OK |
| 24 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: R-02 fantasy share of trees 20–30 % (Decision 01 §3) | ✅ PASS | 18462 fantasy / 89592 trees = 21% (whole tile) |
| 25 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: wind bends the realized near plants (ECO_EF_FE01_GIANT_FERN) | ✅ PASS | 3,631,008 verts, max Δ 0.177 m in 0.5 s |
| 26 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.22 MB |
| 27 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: opens, no missing images / libraries | ✅ PASS | 13 libraries, missing images [] |
| 28 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: ecosystem layers | ✅ PASS | 12 layers |
| 29 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 30 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 31 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: every linked variant / LOD has its materials (no empty slots) | ✅ PASS | 58 objects; empty: [] |
| 32 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 33 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 34 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 89,644 instances (ground layers ≥ 0.03 / m² sampled at 1 %); empty [] |
| 35 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 706 samples, median 0.012 m, max 0.05 m, 100.0% OK |
| 36 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: wind bends the realized near plants (ECO_AV_G01_MEADOW_GRASS) | ✅ PASS | 2,404,350 verts, max Δ 0.101 m in 0.5 s |
| 37 | T6_POP_R04_GOLDEN_DESERT_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.22 MB |
| 38 | T6_POP_R04_GOLDEN_DESERT_v001.blend: opens, no missing images / libraries | ✅ PASS | 12 libraries, missing images [] |
| 39 | T6_POP_R04_GOLDEN_DESERT_v001.blend: ecosystem layers | ✅ PASS | 11 layers |
| 40 | T6_POP_R04_GOLDEN_DESERT_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 41 | T6_POP_R04_GOLDEN_DESERT_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 42 | T6_POP_R04_GOLDEN_DESERT_v001.blend: every linked variant / LOD has its materials (no empty slots) | ✅ PASS | 38 objects; empty: [] |
| 43 | T6_POP_R04_GOLDEN_DESERT_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 44 | T6_POP_R04_GOLDEN_DESERT_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 45 | T6_POP_R04_GOLDEN_DESERT_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 55,497 instances (ground layers ≥ 0.03 / m² sampled at 1 %); empty [] |
| 46 | T6_POP_R04_GOLDEN_DESERT_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 644 samples, median 0.029 m, max 0.05 m, 100.0% OK |
| 47 | T6_POP_R04_GOLDEN_DESERT_v001.blend: wind bends the realized near plants (ECO_DS_G01_SEWAN_GRASS) | ✅ PASS | 63,000 verts, max Δ 0.119 m in 0.5 s |
| 48 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.19 MB |
| 49 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: opens, no missing images / libraries | ✅ PASS | 6 libraries, missing images [] |
| 50 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: ecosystem layers | ✅ PASS | 4 layers |
| 51 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 52 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 53 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: every linked variant / LOD has its materials (no empty slots) | ✅ PASS | 20 objects; empty: [] |
| 54 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 55 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 56 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 8,843 instances (ground layers ≥ 0.03 / m² sampled at 1 %); empty [] |
| 57 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 240 samples, median 0.018 m, max 0.05 m, 100.0% OK |
| 58 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: wind bends the realized near plants (ECO_FB_G01_HARDY_GRASS) | ✅ PASS | 31,680 verts, max Δ 0.050 m in 0.5 s |

## Blender textures (python3 + Pillow) — **39/39 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | atlas av_bamboo: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 2 | atlas av_banj: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 6% |
| 3 | atlas av_berberis: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 6% |
| 4 | atlas av_chir: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 5 | atlas av_deodar: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 6 | atlas av_fern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 27% |
| 7 | atlas av_kans: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 2% |
| 8 | atlas av_lotus: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 69% |
| 9 | atlas av_peepal: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 10 | atlas av_rhodo: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 18% |
| 11 | atlas av_tulsi: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 13% |
| 12 | atlas ct_ivy: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 13 | atlas ct_mango: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 9% |
| 14 | atlas ds_calotropis: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 17% |
| 15 | atlas ds_khejri: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 3% |
| 16 | atlas ef_beech: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 17 | atlas ef_elder: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 8% |
| 18 | atlas ef_fern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 27% |
| 19 | atlas ef_lantern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 37% |
| 20 | atlas ef_moss: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 21 | atlas ef_oak: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 22 | atlas ef_spiral: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 17% |
| 23 | atlas ef_veil: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 4% |
| 24 | atlas ef_yew: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 25 | atlas lk_alder: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 13% |
| 26 | atlas lk_lily: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 65% |
| 27 | atlas lk_willow: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 28 | atlas mk_birch: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 13% |
| 29 | atlas mk_bluepine: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 13% |
| 30 | atlas mk_fir: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 10% |
| 31 | atlas mk_juniper: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 8% |
| 32 | atlas mk_krumm: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 10% |
| 33 | atlas mk_rhodo_dwarf: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 17% |
| 34 | atlas mk_spruce: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 9% |
| 35 | atlas nd_litter_fresh: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 36% |
| 36 | atlas nd_litter_old: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 34% |
| 37 | atlas pl_acacia: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 38 | atlas pl_banyan: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 14% |
| 39 | atlas pl_neem: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 6% |

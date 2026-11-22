# TASK 06 · Technical QC report — milestone 1 (vegetation libraries v001)

Automated by `03_assets/vegetation/scripts/t6_qc.py` (geometry, UVs, materials, textures, wind, ground contact, labels).

## Blender 4.5.16 LTS — **428/429 PASS**

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
| 11 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 12 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 1.14 m |
| 13 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 14 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 15 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 16 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 17 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 18 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 19 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 20 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 21 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 22 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 23 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 24 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 25 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 26 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 27 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 28 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 29 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 30 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 31 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 32 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 33 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.005 m |
| 34 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 35 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 36 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 37 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 38 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 39 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 40 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 41 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 42 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 43 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 44 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 45 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 46 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 47 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 48 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 49 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 50 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 51 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 52 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 53 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 54 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 55 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 56 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 57 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 6,448 tris, 5,850 verts |
| 58 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 59 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 60 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 61 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 62 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 63 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 64 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 65 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 66 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 67 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 68 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 69 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 70 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 71 | AV_G02B_KANS_GRASS_SPRING: valid mesh, UVs | ✅ PASS | 4,760 tris, 4,095 verts |
| 72 | AV_G02B_KANS_GRASS_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 73 | AV_G02B_KANS_GRASS_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G02B_KANS_GRASS_SPRING_0, MAT_T6_AV_G02B_KANS_GRASS_SPRING_1 |
| 74 | AV_G02B_KANS_GRASS_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 75 | AV_G02B_KANS_GRASS_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 76 | AV_G02B_KANS_GRASS_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 77 | AV_G02B_KANS_GRASS_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 78 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 3,320 tris, 3,015 verts |
| 79 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 80 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 81 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 82 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 83 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 84 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 85 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 86 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 87 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 88 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 89 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 90 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 91 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 92 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 93 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 94 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 95 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 96 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 97 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 98 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 99 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 100 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 101 | AV_S01_BERBERIS: height within ±15 % of the design height | ✅ PASS | 1.83 m vs design 1.9 m |
| 102 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 103 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 104 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 105 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 106 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 107 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 108 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 109 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 110 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 111 | AV_S02_TULSI: height within ±15 % of the design height | ✅ PASS | 0.73 m vs design 0.75 m |
| 112 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 113 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 114 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 115 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 116 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 117 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,926 tris, 327,544 verts |
| 118 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 119 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 120 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 121 | AV_T01_PEEPAL: height within ±15 % of the design height | ✅ PASS | 23.75 m vs design 22.0 m |
| 122 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 123 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 124 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 125 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 126 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 127 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 309,744 tris, 267,286 verts |
| 128 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 129 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 130 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 131 | AV_T02_DEODAR: height within ±15 % of the design height | ✅ PASS | 34.86 m vs design 34.0 m |
| 132 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 307 verts at the foot |
| 133 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 134 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 135 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 136 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 137 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 138 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 139 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 140 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 141 | AV_T03_CHIR_PINE: height within ±15 % of the design height | ✅ PASS | 27.33 m vs design 28.0 m |
| 142 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 143 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 144 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 145 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 146 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 147 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,068 tris, 171,876 verts |
| 148 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 149 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 150 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 151 | AV_T04_BANJ_OAK: height within ±15 % of the design height | ✅ PASS | 17.45 m vs design 17.0 m |
| 152 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 153 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 154 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 155 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 156 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 157 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 158 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 159 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 160 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 161 | AV_T05_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 8.19 m vs design 8.5 m |
| 162 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 163 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 164 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 165 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 166 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 167 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 168 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 169 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 170 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 171 | AV_T06_BAMBOO_CLUMP: height within ±15 % of the design height | ✅ PASS | 15.14 m vs design 15.0 m |
| 172 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 173 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 174 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 175 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 176 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 177 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 178 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.027 m · foot Δ 0.001 m |
| 179 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 180 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.3 MB |
| 181 | EF: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 64 images, missing [] |
| 182 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 183 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 184 | EF: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 185 | EF: assets in library | ✅ PASS | 13 assets |
| 186 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 187 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 188 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 189 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 190 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 191 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 192 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 193 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 194 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 195 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 196 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 197 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 198 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 199 | EF_M02_GLOW_MOSS: valid mesh, UVs | ✅ PASS | 8,600 tris, 5,832 verts |
| 200 | EF_M02_GLOW_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 201 | EF_M02_GLOW_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M02_GLOW_MOSS_0, MAT_T6_EF_M02_GLOW_MOSS_1 |
| 202 | EF_M02_GLOW_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 203 | EF_M02_GLOW_MOSS: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 204 | EF_M02_GLOW_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 205 | EF_M02_GLOW_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.15 |
| 206 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 207 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 208 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 209 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 210 | EF_MU01_GLOWCAP: fantasy asset restricted to R-02 (Decision 01) | ❌ FAIL |  |
| 211 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 212 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 213 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,958 tris, 389,340 verts |
| 214 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 215 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 216 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 217 | EF_T01_GIANT_ELDER: height within ±15 % of the design height | ✅ PASS | 66.79 m vs design 62.0 m |
| 218 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 504 verts at the foot |
| 219 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 220 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 221 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 222 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 223 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 251,408 tris, 214,441 verts |
| 224 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 225 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 226 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 227 | EF_T02_TEAL_BEECH: height within ±15 % of the design height | ✅ PASS | 34.60 m vs design 34.0 m |
| 228 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 342 verts at the foot |
| 229 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 230 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 231 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 232 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 233 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,120 tris, 177,671 verts |
| 234 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 235 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 236 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 237 | EF_T03_MOSS_OAK: height within ±15 % of the design height | ✅ PASS | 24.27 m vs design 23.0 m |
| 238 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 248 verts at the foot |
| 239 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 240 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 241 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 242 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 243 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 244 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 245 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 246 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 247 | EF_T04_YEW: height within ±15 % of the design height | ✅ PASS | 8.69 m vs design 9.0 m |
| 248 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 249 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 250 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 251 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 252 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 253 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 254 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 255 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 256 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 257 | EF_T05_VEIL_WILLOW: height within ±15 % of the design height | ✅ PASS | 18.39 m vs design 18.0 m |
| 258 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 259 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 260 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 261 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 262 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 263 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 264 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,176 tris, 177,377 verts |
| 265 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 266 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 267 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 268 | EF_T06_SPIRAL_ROOT: height within ±15 % of the design height | ✅ PASS | 22.85 m vs design 24.0 m |
| 269 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.33 m, 495 verts at the foot |
| 270 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 271 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 272 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 273 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 274 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 275 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 276 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 277 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 278 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 279 | EF_T07_LANTERN_TREE: height within ±15 % of the design height | ✅ PASS | 15.11 m vs design 15.0 m |
| 280 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 281 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 282 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 283 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 284 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 285 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 286 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 287 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 288 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 289 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 290 | EF_T08_DEAD_SNAG: height within ±15 % of the design height | ✅ PASS | 18.74 m vs design 17.0 m |
| 291 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 242 verts at the foot |
| 292 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 293 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 294 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 295 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 296 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 297 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 298 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 299 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 300 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 301 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 302 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 303 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.939 m · foot Δ 0.000 m |
| 304 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.002 m |
| 305 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 306 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 21.4 MB |
| 307 | MK: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 46 images, missing [] |
| 308 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 309 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 310 | MK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 311 | MK: assets in library | ✅ PASS | 12 assets |
| 312 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 313 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 314 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 315 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 316 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 317 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 318 | MK_F01_GENTIAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 319 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 320 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 321 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 322 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 323 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 324 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 325 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 326 | MK_F02_EDELWEISS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 327 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 328 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 329 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 330 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 331 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 332 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 333 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 334 | MK_F03_BLUE_POPPY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 335 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 336 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 5,280 tris, 4,800 verts |
| 337 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 338 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 339 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 340 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 341 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 342 | MK_G01_ALPINE_TUSSOCK: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 343 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 344 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 345 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 346 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 347 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 348 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 349 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 350 | MK_M01_ALPINE_CUSHION: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 351 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 352 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 353 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 354 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 355 | MK_S01_JUNIPER: height within ±15 % of the design height | ✅ PASS | 0.82 m vs design 0.9 m |
| 356 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 357 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 358 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 359 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 360 | MK_S01_JUNIPER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 361 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 362 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 363 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 364 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 365 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 366 | MK_S02_DWARF_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 0.54 m vs design 0.6 m |
| 367 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 368 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 369 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 370 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 371 | MK_S02_DWARF_RHODODENDRON: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 372 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 373 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,706 tris, 188,378 verts |
| 374 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 375 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 376 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 377 | MK_T01_HIMALAYAN_SPRUCE: height within ±15 % of the design height | ✅ PASS | 31.32 m vs design 32.0 m |
| 378 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 308 verts at the foot |
| 379 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 380 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 381 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 382 | MK_T01_HIMALAYAN_SPRUCE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 383 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 384 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 385 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 386 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 387 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 388 | MK_T02_HIMALAYAN_BIRCH: height within ±15 % of the design height | ✅ PASS | 11.59 m vs design 12.0 m |
| 389 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 390 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 391 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 392 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 393 | MK_T02_HIMALAYAN_BIRCH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 394 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 395 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 22,018 tris, 15,442 verts |
| 396 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 397 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 398 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 399 | MK_T03_KRUMMHOLZ_PINE: height within ±15 % of the design height | ✅ PASS | 5.67 m vs design 5.5 m |
| 400 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 281 verts at the foot |
| 401 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 402 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 403 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 404 | MK_T03_KRUMMHOLZ_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 405 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 406 | MK_T04_SILVER_FIR: valid mesh, UVs | ✅ PASS | 256,348 tris, 216,552 verts |
| 407 | MK_T04_SILVER_FIR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 408 | MK_T04_SILVER_FIR: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T04_SILVER_FIR_BARK, MAT_T6_MK_T04_SILVER_FIR_LEAF, MAT_T6_MK_T04_SILVER_FIR_BARK |
| 409 | MK_T04_SILVER_FIR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 410 | MK_T04_SILVER_FIR: height within ±15 % of the design height | ✅ PASS | 37.36 m vs design 36.0 m |
| 411 | MK_T04_SILVER_FIR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 287 verts at the foot |
| 412 | MK_T04_SILVER_FIR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 413 | MK_T04_SILVER_FIR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 414 | MK_T04_SILVER_FIR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 415 | MK_T04_SILVER_FIR: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 416 | MK_T04_SILVER_FIR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 417 | MK_T05_BLUE_PINE: valid mesh, UVs | ✅ PASS | 126,070 tris, 112,360 verts |
| 418 | MK_T05_BLUE_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 419 | MK_T05_BLUE_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T05_BLUE_PINE_BARK, MAT_T6_MK_T05_BLUE_PINE_LEAF, MAT_T6_MK_T05_BLUE_PINE_BARK |
| 420 | MK_T05_BLUE_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 421 | MK_T05_BLUE_PINE: height within ±15 % of the design height | ✅ PASS | 31.42 m vs design 30.0 m |
| 422 | MK_T05_BLUE_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.42 m, 305 verts at the foot |
| 423 | MK_T05_BLUE_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 424 | MK_T05_BLUE_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 425 | MK_T05_BLUE_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 426 | MK_T05_BLUE_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 427 | MK_T05_BLUE_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 428 | MK_T04_SILVER_FIR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 429 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |

## Blender 5.3.0 — **428/429 PASS**

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
| 11 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 12 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 1.14 m |
| 13 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 14 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 15 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 16 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 17 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 18 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 19 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 20 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 21 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 22 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 23 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 24 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 25 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 26 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 27 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 28 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 29 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 30 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 31 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 32 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 33 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.005 m |
| 34 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 35 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 36 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 37 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 38 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 39 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 40 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 41 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 42 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 43 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 44 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 45 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 46 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 47 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 48 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 49 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 50 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 51 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 52 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 53 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 54 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 55 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 56 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 57 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 6,448 tris, 5,850 verts |
| 58 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 59 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 60 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 61 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 62 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 63 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 64 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 65 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 66 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 67 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 68 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.012 m |
| 69 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 70 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 71 | AV_G02B_KANS_GRASS_SPRING: valid mesh, UVs | ✅ PASS | 4,760 tris, 4,095 verts |
| 72 | AV_G02B_KANS_GRASS_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 73 | AV_G02B_KANS_GRASS_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G02B_KANS_GRASS_SPRING_0, MAT_T6_AV_G02B_KANS_GRASS_SPRING_1 |
| 74 | AV_G02B_KANS_GRASS_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 75 | AV_G02B_KANS_GRASS_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 76 | AV_G02B_KANS_GRASS_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 77 | AV_G02B_KANS_GRASS_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 78 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 3,320 tris, 3,015 verts |
| 79 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 80 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 81 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 82 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 83 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 84 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 85 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 86 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 87 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 88 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 89 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 90 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 91 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 92 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 93 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 94 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 95 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 96 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 97 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 98 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 99 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 100 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 101 | AV_S01_BERBERIS: height within ±15 % of the design height | ✅ PASS | 1.83 m vs design 1.9 m |
| 102 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 103 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 104 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 105 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 106 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 107 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 108 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 109 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 110 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 111 | AV_S02_TULSI: height within ±15 % of the design height | ✅ PASS | 0.73 m vs design 0.75 m |
| 112 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 113 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 114 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 115 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 116 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 117 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,926 tris, 327,544 verts |
| 118 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 119 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 120 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 121 | AV_T01_PEEPAL: height within ±15 % of the design height | ✅ PASS | 23.75 m vs design 22.0 m |
| 122 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 123 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 124 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 125 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 126 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 127 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 309,744 tris, 267,286 verts |
| 128 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 129 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 130 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 131 | AV_T02_DEODAR: height within ±15 % of the design height | ✅ PASS | 34.86 m vs design 34.0 m |
| 132 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 307 verts at the foot |
| 133 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 134 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 135 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 136 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 137 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 138 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 139 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 140 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 141 | AV_T03_CHIR_PINE: height within ±15 % of the design height | ✅ PASS | 27.33 m vs design 28.0 m |
| 142 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 143 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 144 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 145 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 146 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 147 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,068 tris, 171,876 verts |
| 148 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 149 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 150 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 151 | AV_T04_BANJ_OAK: height within ±15 % of the design height | ✅ PASS | 17.45 m vs design 17.0 m |
| 152 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 153 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 154 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 155 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 156 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 157 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 158 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 159 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 160 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 161 | AV_T05_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 8.19 m vs design 8.5 m |
| 162 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 163 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 164 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 165 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 166 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 167 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 168 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 169 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 170 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 171 | AV_T06_BAMBOO_CLUMP: height within ±15 % of the design height | ✅ PASS | 15.14 m vs design 15.0 m |
| 172 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 173 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 174 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 175 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 176 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 177 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 178 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.027 m · foot Δ 0.001 m |
| 179 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 180 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.3 MB |
| 181 | EF: opens in Blender 5.3.0, no missing images | ✅ PASS | 64 images, missing [] |
| 182 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 183 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 184 | EF: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 185 | EF: assets in library | ✅ PASS | 13 assets |
| 186 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 187 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 188 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 189 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 190 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 191 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 192 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 193 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 194 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 195 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 196 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 197 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 198 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 199 | EF_M02_GLOW_MOSS: valid mesh, UVs | ✅ PASS | 8,600 tris, 5,832 verts |
| 200 | EF_M02_GLOW_MOSS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 201 | EF_M02_GLOW_MOSS: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M02_GLOW_MOSS_0, MAT_T6_EF_M02_GLOW_MOSS_1 |
| 202 | EF_M02_GLOW_MOSS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 203 | EF_M02_GLOW_MOSS: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 204 | EF_M02_GLOW_MOSS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 205 | EF_M02_GLOW_MOSS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.15 |
| 206 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 207 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 208 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 209 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 210 | EF_MU01_GLOWCAP: fantasy asset restricted to R-02 (Decision 01) | ❌ FAIL |  |
| 211 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 212 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 213 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,958 tris, 389,340 verts |
| 214 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 215 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 216 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 217 | EF_T01_GIANT_ELDER: height within ±15 % of the design height | ✅ PASS | 66.79 m vs design 62.0 m |
| 218 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 504 verts at the foot |
| 219 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 220 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 221 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 222 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 223 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 251,408 tris, 214,441 verts |
| 224 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 225 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 226 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 227 | EF_T02_TEAL_BEECH: height within ±15 % of the design height | ✅ PASS | 34.60 m vs design 34.0 m |
| 228 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 342 verts at the foot |
| 229 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 230 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 231 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 232 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 233 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,120 tris, 177,671 verts |
| 234 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 235 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 236 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 237 | EF_T03_MOSS_OAK: height within ±15 % of the design height | ✅ PASS | 24.27 m vs design 23.0 m |
| 238 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 248 verts at the foot |
| 239 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 240 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 241 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 242 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 243 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 244 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 245 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 246 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 247 | EF_T04_YEW: height within ±15 % of the design height | ✅ PASS | 8.69 m vs design 9.0 m |
| 248 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 249 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 250 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 251 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 252 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 253 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 254 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 255 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 256 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 257 | EF_T05_VEIL_WILLOW: height within ±15 % of the design height | ✅ PASS | 18.39 m vs design 18.0 m |
| 258 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 259 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 260 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 261 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 262 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 263 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 264 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,176 tris, 177,377 verts |
| 265 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 266 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 267 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 268 | EF_T06_SPIRAL_ROOT: height within ±15 % of the design height | ✅ PASS | 22.85 m vs design 24.0 m |
| 269 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.33 m, 495 verts at the foot |
| 270 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 271 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 272 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 273 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 274 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 275 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 276 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 277 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 278 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 279 | EF_T07_LANTERN_TREE: height within ±15 % of the design height | ✅ PASS | 15.11 m vs design 15.0 m |
| 280 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 281 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 282 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 283 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 284 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 285 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 286 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 287 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 288 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 289 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 290 | EF_T08_DEAD_SNAG: height within ±15 % of the design height | ✅ PASS | 18.74 m vs design 17.0 m |
| 291 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 242 verts at the foot |
| 292 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 293 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 294 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 295 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 296 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 297 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 298 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 299 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 300 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 301 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 302 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 303 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.939 m · foot Δ 0.000 m |
| 304 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.002 m |
| 305 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 306 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 21.4 MB |
| 307 | MK: opens in Blender 5.3.0, no missing images | ✅ PASS | 46 images, missing [] |
| 308 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 309 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 310 | MK: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM | ✅ PASS |  |
| 311 | MK: assets in library | ✅ PASS | 12 assets |
| 312 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 313 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 314 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 315 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 316 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 317 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 318 | MK_F01_GENTIAN: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 319 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 320 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 321 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 322 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 323 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 324 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 325 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 326 | MK_F02_EDELWEISS: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 327 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 328 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 329 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 330 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 331 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 332 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 333 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 334 | MK_F03_BLUE_POPPY: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 335 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 336 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 5,280 tris, 4,800 verts |
| 337 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 338 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 339 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 340 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 341 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 342 | MK_G01_ALPINE_TUSSOCK: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 343 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 344 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 345 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 346 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 347 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 348 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 349 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 350 | MK_M01_ALPINE_CUSHION: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 351 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 352 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 353 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 354 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 355 | MK_S01_JUNIPER: height within ±15 % of the design height | ✅ PASS | 0.82 m vs design 0.9 m |
| 356 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 357 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 358 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 359 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 360 | MK_S01_JUNIPER: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 361 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 362 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 363 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 364 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 365 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 366 | MK_S02_DWARF_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 0.54 m vs design 0.6 m |
| 367 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 368 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 369 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 370 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 371 | MK_S02_DWARF_RHODODENDRON: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 372 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 373 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,706 tris, 188,378 verts |
| 374 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 375 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 376 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 377 | MK_T01_HIMALAYAN_SPRUCE: height within ±15 % of the design height | ✅ PASS | 31.32 m vs design 32.0 m |
| 378 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 308 verts at the foot |
| 379 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 380 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 381 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 382 | MK_T01_HIMALAYAN_SPRUCE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 383 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 384 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 385 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 386 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 387 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 388 | MK_T02_HIMALAYAN_BIRCH: height within ±15 % of the design height | ✅ PASS | 11.59 m vs design 12.0 m |
| 389 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 390 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 391 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 392 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 393 | MK_T02_HIMALAYAN_BIRCH: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 394 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 395 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 22,018 tris, 15,442 verts |
| 396 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 397 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 398 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 399 | MK_T03_KRUMMHOLZ_PINE: height within ±15 % of the design height | ✅ PASS | 5.67 m vs design 5.5 m |
| 400 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 281 verts at the foot |
| 401 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 402 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 403 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 404 | MK_T03_KRUMMHOLZ_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 405 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 406 | MK_T04_SILVER_FIR: valid mesh, UVs | ✅ PASS | 256,348 tris, 216,552 verts |
| 407 | MK_T04_SILVER_FIR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 408 | MK_T04_SILVER_FIR: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T04_SILVER_FIR_BARK, MAT_T6_MK_T04_SILVER_FIR_LEAF, MAT_T6_MK_T04_SILVER_FIR_BARK |
| 409 | MK_T04_SILVER_FIR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 410 | MK_T04_SILVER_FIR: height within ±15 % of the design height | ✅ PASS | 37.36 m vs design 36.0 m |
| 411 | MK_T04_SILVER_FIR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 287 verts at the foot |
| 412 | MK_T04_SILVER_FIR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 413 | MK_T04_SILVER_FIR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 414 | MK_T04_SILVER_FIR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 415 | MK_T04_SILVER_FIR: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 416 | MK_T04_SILVER_FIR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 417 | MK_T05_BLUE_PINE: valid mesh, UVs | ✅ PASS | 126,070 tris, 112,360 verts |
| 418 | MK_T05_BLUE_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 419 | MK_T05_BLUE_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T05_BLUE_PINE_BARK, MAT_T6_MK_T05_BLUE_PINE_LEAF, MAT_T6_MK_T05_BLUE_PINE_BARK |
| 420 | MK_T05_BLUE_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 421 | MK_T05_BLUE_PINE: height within ±15 % of the design height | ✅ PASS | 31.42 m vs design 30.0 m |
| 422 | MK_T05_BLUE_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.42 m, 305 verts at the foot |
| 423 | MK_T05_BLUE_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 424 | MK_T05_BLUE_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 425 | MK_T05_BLUE_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 426 | MK_T05_BLUE_PINE: no glow outside R-02 | ✅ PASS | max emission 0.00 |
| 427 | MK_T05_BLUE_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 428 | MK_T04_SILVER_FIR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.832 m · foot Δ 0.000 m |
| 429 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |

## Blender populated files (Blender 4.5.16 LTS) — **50/52 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | TASK 05 approved files untouched (git: no change under 02_world/3d_world) | ✅ PASS | clean |
| 2 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.27 MB |
| 3 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: opens, no missing images / libraries | ✅ PASS | 10 libraries, missing images [] |
| 4 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: ecosystem layers | ✅ PASS | 24 layers |
| 5 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 6 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 7 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 8 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: exactly ONE Peepal (landmark, courtyard) | ✅ PASS | 1 instance(s), 0 Peepal scatter layers |
| 9 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 10 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: every layer generates instances (whole tile, open culling) | ❌ FAIL | 218,229 instances (ground layers sampled at 1 %); empty ['ECO_AV_S02_TULSI_D_E_PROPOSED', 'ECO_AV_T02_DEODAR', 'ECO_AV_T03_CHIR_PINE', 'ECO_PL_G02_DOOB_GRASS'] |
| 11 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 933 samples, median 0.011 m, max 0.05 m, 100.0% OK |
| 12 | T6_POP_R01_ASHRAM_VALLEY_v001.blend: wind bends the realized near plants (ECO_AV_G01_MEADOW_GRASS) | ✅ PASS | 8,020,350 verts, max Δ 0.090 m in 0.5 s |
| 13 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.24 MB |
| 14 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: opens, no missing images / libraries | ✅ PASS | 7 libraries, missing images [] |
| 15 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: ecosystem layers | ✅ PASS | 17 layers |
| 16 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 17 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 18 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 19 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 328,589 instances (ground layers sampled at 1 %); empty [] |
| 20 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 1020 samples, median 0.012 m, max 0.05 m, 100.0% OK |
| 21 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: R-02 fantasy share of trees 20–30 % (Decision 01 §3) | ✅ PASS | 18493 fantasy / 89564 trees = 21% (whole tile) |
| 22 | T6_POP_R02_ENCHANTED_FOREST_v001.blend: wind bends the realized near plants (ECO_EF_FE01_GIANT_FERN) | ✅ PASS | 6,029,472 verts, max Δ 0.179 m in 0.5 s |
| 23 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.22 MB |
| 24 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: opens, no missing images / libraries | ✅ PASS | 7 libraries, missing images [] |
| 25 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: ecosystem layers | ✅ PASS | 12 layers |
| 26 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 27 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 28 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 29 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 30 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 89,425 instances (ground layers sampled at 1 %); empty [] |
| 31 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 714 samples, median 0.013 m, max 0.05 m, 100.0% OK |
| 32 | T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend: wind bends the realized near plants (ECO_AV_G01_MEADOW_GRASS) | ✅ PASS | 1,146,600 verts, max Δ 0.087 m in 0.5 s |
| 33 | T6_POP_R04_GOLDEN_DESERT_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.21 MB |
| 34 | T6_POP_R04_GOLDEN_DESERT_v001.blend: opens, no missing images / libraries | ✅ PASS | 8 libraries, missing images [] |
| 35 | T6_POP_R04_GOLDEN_DESERT_v001.blend: ecosystem layers | ✅ PASS | 11 layers |
| 36 | T6_POP_R04_GOLDEN_DESERT_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 37 | T6_POP_R04_GOLDEN_DESERT_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 38 | T6_POP_R04_GOLDEN_DESERT_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 39 | T6_POP_R04_GOLDEN_DESERT_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 40 | T6_POP_R04_GOLDEN_DESERT_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 54,049 instances (ground layers sampled at 1 %); empty [] |
| 41 | T6_POP_R04_GOLDEN_DESERT_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 536 samples, median 0.031 m, max 0.05 m, 100.0% OK |
| 42 | T6_POP_R04_GOLDEN_DESERT_v001.blend: wind bends the realized near plants (ECO_DS_G01_SEWAN_GRASS_WADI) | ❌ FAIL | 0 verts, max Δ 0.000 m in 0.5 s |
| 43 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: file < 95 MB (everything linked) | ✅ PASS | 0.19 MB |
| 44 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: opens, no missing images / libraries | ✅ PASS | 6 libraries, missing images [] |
| 45 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: ecosystem layers | ✅ PASS | 4 layers |
| 46 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: one local T6_WIND_CONTROL drives every layer | ✅ PASS | 1 control(s) |
| 47 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: every layer has a terrain + band collections | ✅ PASS |  |
| 48 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4) | ✅ PASS | outside: [] |
| 49 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: no fantasy / glowing species outside R-02 | ✅ PASS | [] |
| 50 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: every layer generates instances (whole tile, open culling) | ✅ PASS | 1,621 instances (ground layers sampled at 1 %); empty [] |
| 51 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m) | ✅ PASS | 240 samples, median 0.018 m, max 0.05 m, 100.0% OK |
| 52 | T6_POP_R05_FORBIDDEN_LANDS_v001.blend: wind bends the realized near plants (ECO_FB_G01_HARDY_GRASS) | ✅ PASS | 31,680 verts, max Δ 0.054 m in 0.5 s |

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

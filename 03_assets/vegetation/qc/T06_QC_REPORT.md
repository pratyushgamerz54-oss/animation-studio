# TASK 06 · Technical QC report — milestone 1 (vegetation libraries v001)

Automated by `03_assets/vegetation/scripts/t6_qc.py` (geometry, UVs, materials, textures, wind, ground contact, labels).

## Blender 4.5.16 LTS — **386/386 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | AV: library file exists | ✅ PASS | library/T6_VEG_ASHRAM_VALLEY_v001.blend |
| 2 | AV: file size < 100 MB (GitHub limit) | ✅ PASS | 33.5 MB |
| 3 | AV: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 60 images, missing [] |
| 4 | AV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 5 | AV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 6 | AV: assets in library | ✅ PASS | 21 assets |
| 7 | AV_AQ01_LOTUS: valid mesh, UVs | ✅ PASS | 2,244 tris, 1,774 verts |
| 8 | AV_AQ01_LOTUS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 9 | AV_AQ01_LOTUS: PBR materials (4 slots) | ✅ PASS | MAT_T6_AV_AQ01_LOTUS_0, MAT_T6_AV_AQ01_LOTUS_1, MAT_T6_AV_AQ01_LOTUS_2, MAT_T6_AV_AQ01_LOTUS_3 |
| 10 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 11 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 0.99 m |
| 12 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 13 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 14 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 15 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 16 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 17 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 18 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 19 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 20 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 21 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 22 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 23 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 24 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 25 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 26 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 27 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 28 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 29 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 30 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 31 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 32 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 33 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 34 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 35 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 36 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 37 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 38 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 39 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 40 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 41 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 42 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 43 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 44 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 45 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 46 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 47 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 48 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 49 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 50 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 51 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 52 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 53 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 54 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 55 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 56 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 5,200 tris, 4,680 verts |
| 57 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 58 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 59 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 60 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 61 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 62 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 63 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 64 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 65 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 66 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 67 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 68 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 69 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 70 | AV_G02B_KANS_GRASS_SPRING: valid mesh, UVs | ✅ PASS | 3,920 tris, 3,360 verts |
| 71 | AV_G02B_KANS_GRASS_SPRING: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 72 | AV_G02B_KANS_GRASS_SPRING: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G02B_KANS_GRASS_SPRING_0, MAT_T6_AV_G02B_KANS_GRASS_SPRING_1 |
| 73 | AV_G02B_KANS_GRASS_SPRING: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 74 | AV_G02B_KANS_GRASS_SPRING: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 75 | AV_G02B_KANS_GRASS_SPRING: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 76 | AV_G02B_KANS_GRASS_SPRING: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 77 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 2,600 tris, 2,340 verts |
| 78 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 79 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 80 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 81 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 82 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 83 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 84 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 85 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 86 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 87 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 88 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 89 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 90 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 91 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 92 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 93 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 94 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 95 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 96 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 97 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 98 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 99 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 100 | AV_S01_BERBERIS: height within ±15 % of the design height | ✅ PASS | 1.83 m vs design 1.9 m |
| 101 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 102 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 103 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 104 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 105 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 106 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 107 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 108 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 109 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 110 | AV_S02_TULSI: height within ±15 % of the design height | ✅ PASS | 0.73 m vs design 0.75 m |
| 111 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 112 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 113 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 114 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 115 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 116 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,738 tris, 327,262 verts |
| 117 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 118 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 119 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 120 | AV_T01_PEEPAL: height within ±15 % of the design height | ✅ PASS | 23.72 m vs design 22.0 m |
| 121 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 122 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 123 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 124 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 125 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 126 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 310,460 tris, 268,360 verts |
| 127 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 128 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 129 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 130 | AV_T02_DEODAR: height within ±15 % of the design height | ✅ PASS | 34.94 m vs design 34.0 m |
| 131 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 305 verts at the foot |
| 132 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 133 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 134 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 135 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 136 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 137 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 138 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 139 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 140 | AV_T03_CHIR_PINE: height within ±15 % of the design height | ✅ PASS | 27.33 m vs design 28.0 m |
| 141 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 142 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 143 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 144 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 145 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 146 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,300 tris, 172,224 verts |
| 147 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 148 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 149 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 150 | AV_T04_BANJ_OAK: height within ±15 % of the design height | ✅ PASS | 17.45 m vs design 17.0 m |
| 151 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 152 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 153 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 154 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 155 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 156 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 157 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 158 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 159 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 160 | AV_T05_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 8.19 m vs design 8.5 m |
| 161 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 162 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 163 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 164 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 165 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 166 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 167 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 168 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 169 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 170 | AV_T06_BAMBOO_CLUMP: height within ±15 % of the design height | ✅ PASS | 15.14 m vs design 15.0 m |
| 171 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 172 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 173 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 174 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 175 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 176 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.833 m · foot Δ 0.000 m |
| 177 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.032 m · foot Δ 0.000 m |
| 178 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 179 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.0 MB |
| 180 | EF: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 64 images, missing [] |
| 181 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 182 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 183 | EF: assets in library | ✅ PASS | 12 assets |
| 184 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 185 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 186 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 187 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 188 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 189 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 190 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 191 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 192 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 193 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 194 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 195 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 196 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 197 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 198 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 199 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 200 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 201 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 202 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 203 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,266 tris, 388,302 verts |
| 204 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 205 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 206 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 207 | EF_T01_GIANT_ELDER: height within ±15 % of the design height | ✅ PASS | 66.90 m vs design 62.0 m |
| 208 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 499 verts at the foot |
| 209 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 210 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 211 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 212 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 213 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 250,800 tris, 213,529 verts |
| 214 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 215 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 216 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 217 | EF_T02_TEAL_BEECH: height within ±15 % of the design height | ✅ PASS | 34.60 m vs design 34.0 m |
| 218 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 346 verts at the foot |
| 219 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 220 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 221 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 222 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 223 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,404 tris, 178,097 verts |
| 224 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 225 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 226 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 227 | EF_T03_MOSS_OAK: height within ±15 % of the design height | ✅ PASS | 24.29 m vs design 23.0 m |
| 228 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 246 verts at the foot |
| 229 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 230 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 231 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 232 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 233 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 234 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 235 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 236 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 237 | EF_T04_YEW: height within ±15 % of the design height | ✅ PASS | 8.69 m vs design 9.0 m |
| 238 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 239 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 240 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 241 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 242 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 243 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 244 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 245 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 246 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 247 | EF_T05_VEIL_WILLOW: height within ±15 % of the design height | ✅ PASS | 18.39 m vs design 18.0 m |
| 248 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 249 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 250 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 251 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 252 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 253 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 254 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,324 tris, 177,599 verts |
| 255 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 256 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 257 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 258 | EF_T06_SPIRAL_ROOT: height within ±15 % of the design height | ✅ PASS | 22.85 m vs design 24.0 m |
| 259 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.34 m, 494 verts at the foot |
| 260 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 261 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 262 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 263 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 264 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 265 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 266 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 267 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 268 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 269 | EF_T07_LANTERN_TREE: height within ±15 % of the design height | ✅ PASS | 15.11 m vs design 15.0 m |
| 270 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 271 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 272 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 273 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 274 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 275 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 276 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 277 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 278 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 279 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 280 | EF_T08_DEAD_SNAG: height within ±15 % of the design height | ✅ PASS | 18.74 m vs design 17.0 m |
| 281 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 244 verts at the foot |
| 282 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 283 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 284 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 285 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 286 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 287 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 288 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 289 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 290 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 291 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 292 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 293 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.940 m · foot Δ 0.000 m |
| 294 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.007 m |
| 295 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 296 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 10.1 MB |
| 297 | MK: opens in Blender 4.5.16 LTS, no missing images | ✅ PASS | 35 images, missing [] |
| 298 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 299 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 300 | MK: assets in library | ✅ PASS | 10 assets |
| 301 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 302 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 303 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 304 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 305 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 306 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 307 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 308 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 309 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 310 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 311 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 312 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 313 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 314 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 315 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 316 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 317 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 318 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 319 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 320 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 321 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 322 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 4,000 tris, 3,600 verts |
| 323 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 324 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 325 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 326 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.172 m |
| 327 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 328 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 329 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 330 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 331 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 332 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 333 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 334 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 335 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 336 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 337 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 338 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 339 | MK_S01_JUNIPER: height within ±15 % of the design height | ✅ PASS | 0.82 m vs design 0.9 m |
| 340 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 341 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 342 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 343 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 344 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 345 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 346 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 347 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 348 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 349 | MK_S02_DWARF_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 0.54 m vs design 0.6 m |
| 350 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 351 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 352 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 353 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 354 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 355 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,678 tris, 188,336 verts |
| 356 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 357 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 358 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 359 | MK_T01_HIMALAYAN_SPRUCE: height within ±15 % of the design height | ✅ PASS | 31.32 m vs design 32.0 m |
| 360 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 309 verts at the foot |
| 361 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 362 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 363 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 364 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 365 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 366 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 367 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 368 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 369 | MK_T02_HIMALAYAN_BIRCH: height within ±15 % of the design height | ✅ PASS | 11.59 m vs design 12.0 m |
| 370 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 371 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 372 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 373 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 374 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 375 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 21,942 tris, 15,328 verts |
| 376 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 377 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 378 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 379 | MK_T03_KRUMMHOLZ_PINE: height within ±15 % of the design height | ✅ PASS | 6.12 m vs design 5.5 m |
| 380 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.40 m, 272 verts at the foot |
| 381 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 382 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 383 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 384 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 385 | MK_T01_HIMALAYAN_SPRUCE: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.819 m · foot Δ 0.000 m |
| 386 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |

## Blender 5.3.0 — **379/379 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | AV: library file exists | ✅ PASS | library/T6_VEG_ASHRAM_VALLEY_v001.blend |
| 2 | AV: file size < 100 MB (GitHub limit) | ✅ PASS | 33.4 MB |
| 3 | AV: opens in Blender 5.3.0, no missing images | ✅ PASS | 60 images, missing [] |
| 4 | AV: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 5 | AV: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 6 | AV: assets in library | ✅ PASS | 20 assets |
| 7 | AV_AQ01_LOTUS: valid mesh, UVs | ✅ PASS | 2,244 tris, 1,774 verts |
| 8 | AV_AQ01_LOTUS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 9 | AV_AQ01_LOTUS: PBR materials (4 slots) | ✅ PASS | MAT_T6_AV_AQ01_LOTUS_0, MAT_T6_AV_AQ01_LOTUS_1, MAT_T6_AV_AQ01_LOTUS_2, MAT_T6_AV_AQ01_LOTUS_3 |
| 10 | AV_AQ01_LOTUS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2, 3] |
| 11 | AV_AQ01_LOTUS: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.60 m, top 0.99 m |
| 12 | AV_AQ01_LOTUS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 13 | AV_AQ01_LOTUS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 14 | AV_AQ02_CATTAIL: valid mesh, UVs | ✅ PASS | 2,800 tris, 2,055 verts |
| 15 | AV_AQ02_CATTAIL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 16 | AV_AQ02_CATTAIL: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_AQ02_CATTAIL_0, MAT_T6_AV_AQ02_CATTAIL_1 |
| 17 | AV_AQ02_CATTAIL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 18 | AV_AQ02_CATTAIL: aquatic plant sits at the water surface (z = 0) with stems below | ✅ PASS | lowest -0.15 m, top 2.02 m |
| 19 | AV_AQ02_CATTAIL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 20 | AV_AQ02_CATTAIL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 21 | AV_F01_BUTTERCUP: valid mesh, UVs | ✅ PASS | 1,000 tris, 748 verts |
| 22 | AV_F01_BUTTERCUP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 23 | AV_F01_BUTTERCUP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F01_BUTTERCUP_0, MAT_T6_AV_F01_BUTTERCUP_1, MAT_T6_AV_F01_BUTTERCUP_2 |
| 24 | AV_F01_BUTTERCUP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 25 | AV_F01_BUTTERCUP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 26 | AV_F01_BUTTERCUP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 27 | AV_F01_BUTTERCUP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 28 | AV_F02_PRIMULA: valid mesh, UVs | ✅ PASS | 8,660 tris, 7,107 verts |
| 29 | AV_F02_PRIMULA: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 30 | AV_F02_PRIMULA: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F02_PRIMULA_0, MAT_T6_AV_F02_PRIMULA_1, MAT_T6_AV_F02_PRIMULA_2 |
| 31 | AV_F02_PRIMULA: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 32 | AV_F02_PRIMULA: plant base on the ground (no floating) | ✅ PASS | lowest z -0.000 m |
| 33 | AV_F02_PRIMULA: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 34 | AV_F02_PRIMULA: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 35 | AV_F03_WILD_DAISY: valid mesh, UVs | ✅ PASS | 2,280 tris, 1,901 verts |
| 36 | AV_F03_WILD_DAISY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 37 | AV_F03_WILD_DAISY: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F03_WILD_DAISY_0, MAT_T6_AV_F03_WILD_DAISY_1, MAT_T6_AV_F03_WILD_DAISY_2 |
| 38 | AV_F03_WILD_DAISY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 39 | AV_F03_WILD_DAISY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 40 | AV_F03_WILD_DAISY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 41 | AV_F03_WILD_DAISY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 42 | AV_F04_MARIGOLD: valid mesh, UVs | ✅ PASS | 8,064 tris, 7,191 verts |
| 43 | AV_F04_MARIGOLD: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 44 | AV_F04_MARIGOLD: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_F04_MARIGOLD_0, MAT_T6_AV_F04_MARIGOLD_1, MAT_T6_AV_F04_MARIGOLD_2 |
| 45 | AV_F04_MARIGOLD: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 46 | AV_F04_MARIGOLD: plant base on the ground (no floating) | ✅ PASS | lowest z -0.002 m |
| 47 | AV_F04_MARIGOLD: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 48 | AV_F04_MARIGOLD: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 49 | AV_FE01_SWORD_FERN: valid mesh, UVs | ✅ PASS | 12,240 tris, 10,440 verts |
| 50 | AV_FE01_SWORD_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 51 | AV_FE01_SWORD_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_FE01_SWORD_FERN_0, MAT_T6_AV_FE01_SWORD_FERN_1 |
| 52 | AV_FE01_SWORD_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 53 | AV_FE01_SWORD_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 54 | AV_FE01_SWORD_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 55 | AV_FE01_SWORD_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 56 | AV_G01_MEADOW_GRASS: valid mesh, UVs | ✅ PASS | 5,200 tris, 4,680 verts |
| 57 | AV_G01_MEADOW_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 58 | AV_G01_MEADOW_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G01_MEADOW_GRASS_0, MAT_T6_AV_G01_MEADOW_GRASS_1 |
| 59 | AV_G01_MEADOW_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 60 | AV_G01_MEADOW_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 61 | AV_G01_MEADOW_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 62 | AV_G01_MEADOW_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 63 | AV_G02_KANS_GRASS: valid mesh, UVs | ✅ PASS | 4,312 tris, 3,468 verts |
| 64 | AV_G02_KANS_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 65 | AV_G02_KANS_GRASS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_G02_KANS_GRASS_0, MAT_T6_AV_G02_KANS_GRASS_1, MAT_T6_AV_G02_KANS_GRASS_2 |
| 66 | AV_G02_KANS_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 67 | AV_G02_KANS_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 68 | AV_G02_KANS_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 69 | AV_G02_KANS_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 70 | AV_G03_DRY_PATH_GRASS: valid mesh, UVs | ✅ PASS | 2,600 tris, 2,340 verts |
| 71 | AV_G03_DRY_PATH_GRASS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 72 | AV_G03_DRY_PATH_GRASS: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_G03_DRY_PATH_GRASS_0, MAT_T6_AV_G03_DRY_PATH_GRASS_1 |
| 73 | AV_G03_DRY_PATH_GRASS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 74 | AV_G03_DRY_PATH_GRASS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.011 m |
| 75 | AV_G03_DRY_PATH_GRASS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 76 | AV_G03_DRY_PATH_GRASS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 77 | AV_M01_MOSS_CUSHION: valid mesh, UVs | ✅ PASS | 2,780 tris, 1,836 verts |
| 78 | AV_M01_MOSS_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 79 | AV_M01_MOSS_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_AV_M01_MOSS_CUSHION_0, MAT_T6_AV_M01_MOSS_CUSHION_1 |
| 80 | AV_M01_MOSS_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 81 | AV_M01_MOSS_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 82 | AV_M01_MOSS_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 83 | AV_MU01_BROWN_MUSHROOMS: valid mesh, UVs | ✅ PASS | 2,716 tris, 1,764 verts |
| 84 | AV_MU01_BROWN_MUSHROOMS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 85 | AV_MU01_BROWN_MUSHROOMS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_MU01_BROWN_MUSHROOMS_0, MAT_T6_AV_MU01_BROWN_MUSHROOMS_1, MAT_T6_AV_MU01_BROWN_MUSHROOMS_2 |
| 86 | AV_MU01_BROWN_MUSHROOMS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 87 | AV_MU01_BROWN_MUSHROOMS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.007 m |
| 88 | AV_MU01_BROWN_MUSHROOMS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 89 | AV_S01_BERBERIS: valid mesh, UVs | ✅ PASS | 5,008 tris, 4,842 verts |
| 90 | AV_S01_BERBERIS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 91 | AV_S01_BERBERIS: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S01_BERBERIS_BARK, MAT_T6_AV_S01_BERBERIS_LEAF, MAT_T6_AV_S01_BERBERIS_BARK |
| 92 | AV_S01_BERBERIS: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 93 | AV_S01_BERBERIS: height within ±15 % of the design height | ✅ PASS | 1.83 m vs design 1.9 m |
| 94 | AV_S01_BERBERIS: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 411 verts at the foot |
| 95 | AV_S01_BERBERIS: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 96 | AV_S01_BERBERIS: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 97 | AV_S01_BERBERIS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 98 | AV_S01_BERBERIS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 99 | AV_S02_TULSI: valid mesh, UVs | ✅ PASS | 1,636 tris, 1,774 verts |
| 100 | AV_S02_TULSI: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 101 | AV_S02_TULSI: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_S02_TULSI_BARK, MAT_T6_AV_S02_TULSI_LEAF, MAT_T6_AV_S02_TULSI_BARK |
| 102 | AV_S02_TULSI: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 103 | AV_S02_TULSI: height within ±15 % of the design height | ✅ PASS | 0.73 m vs design 0.75 m |
| 104 | AV_S02_TULSI: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.14 m, 254 verts at the foot |
| 105 | AV_S02_TULSI: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 106 | AV_S02_TULSI: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 107 | AV_S02_TULSI: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 108 | AV_S02_TULSI: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 109 | AV_T01_PEEPAL: valid mesh, UVs | ✅ PASS | 422,738 tris, 327,262 verts |
| 110 | AV_T01_PEEPAL: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 111 | AV_T01_PEEPAL: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T01_PEEPAL_BARK, MAT_T6_AV_T01_PEEPAL_LEAF, MAT_T6_AV_T01_PEEPAL_BARK |
| 112 | AV_T01_PEEPAL: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 113 | AV_T01_PEEPAL: height within ±15 % of the design height | ✅ PASS | 23.72 m vs design 22.0 m |
| 114 | AV_T01_PEEPAL: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.62 m, 118 verts at the foot |
| 115 | AV_T01_PEEPAL: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 116 | AV_T01_PEEPAL: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 117 | AV_T01_PEEPAL: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 118 | AV_T01_PEEPAL: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 119 | AV_T02_DEODAR: valid mesh, UVs | ✅ PASS | 310,460 tris, 268,360 verts |
| 120 | AV_T02_DEODAR: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 121 | AV_T02_DEODAR: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T02_DEODAR_BARK, MAT_T6_AV_T02_DEODAR_LEAF, MAT_T6_AV_T02_DEODAR_BARK |
| 122 | AV_T02_DEODAR: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 123 | AV_T02_DEODAR: height within ±15 % of the design height | ✅ PASS | 34.94 m vs design 34.0 m |
| 124 | AV_T02_DEODAR: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.43 m, 305 verts at the foot |
| 125 | AV_T02_DEODAR: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 126 | AV_T02_DEODAR: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 127 | AV_T02_DEODAR: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 128 | AV_T02_DEODAR: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 129 | AV_T03_CHIR_PINE: valid mesh, UVs | ✅ PASS | 100,120 tris, 87,092 verts |
| 130 | AV_T03_CHIR_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 131 | AV_T03_CHIR_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T03_CHIR_PINE_BARK, MAT_T6_AV_T03_CHIR_PINE_LEAF, MAT_T6_AV_T03_CHIR_PINE_BARK |
| 132 | AV_T03_CHIR_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 133 | AV_T03_CHIR_PINE: height within ±15 % of the design height | ✅ PASS | 27.33 m vs design 28.0 m |
| 134 | AV_T03_CHIR_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.38 m, 22 verts at the foot |
| 135 | AV_T03_CHIR_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 136 | AV_T03_CHIR_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 137 | AV_T03_CHIR_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 138 | AV_T03_CHIR_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 139 | AV_T04_BANJ_OAK: valid mesh, UVs | ✅ PASS | 223,300 tris, 172,224 verts |
| 140 | AV_T04_BANJ_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 141 | AV_T04_BANJ_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T04_BANJ_OAK_BARK, MAT_T6_AV_T04_BANJ_OAK_LEAF, MAT_T6_AV_T04_BANJ_OAK_BARK |
| 142 | AV_T04_BANJ_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 143 | AV_T04_BANJ_OAK: height within ±15 % of the design height | ✅ PASS | 17.45 m vs design 17.0 m |
| 144 | AV_T04_BANJ_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.37 m, 313 verts at the foot |
| 145 | AV_T04_BANJ_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 146 | AV_T04_BANJ_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 147 | AV_T04_BANJ_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 148 | AV_T04_BANJ_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 149 | AV_T05_RHODODENDRON: valid mesh, UVs | ✅ PASS | 57,460 tris, 42,884 verts |
| 150 | AV_T05_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 151 | AV_T05_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T05_RHODODENDRON_BARK, MAT_T6_AV_T05_RHODODENDRON_LEAF, MAT_T6_AV_T05_RHODODENDRON_BARK |
| 152 | AV_T05_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 153 | AV_T05_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 8.19 m vs design 8.5 m |
| 154 | AV_T05_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.27 m, 45 verts at the foot |
| 155 | AV_T05_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 156 | AV_T05_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 157 | AV_T05_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 158 | AV_T05_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 159 | AV_T06_BAMBOO_CLUMP: valid mesh, UVs | ✅ PASS | 44,470 tris, 45,220 verts |
| 160 | AV_T06_BAMBOO_CLUMP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 161 | AV_T06_BAMBOO_CLUMP: PBR materials (3 slots) | ✅ PASS | MAT_T6_AV_T06_BAMBOO_CLUMP_CULM, MAT_T6_AV_T06_BAMBOO_CLUMP_LEAF, MAT_T6_AV_T06_BAMBOO_CLUMP_CULM |
| 162 | AV_T06_BAMBOO_CLUMP: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 163 | AV_T06_BAMBOO_CLUMP: height within ±15 % of the design height | ✅ PASS | 15.14 m vs design 15.0 m |
| 164 | AV_T06_BAMBOO_CLUMP: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.18 m, 341 verts at the foot |
| 165 | AV_T06_BAMBOO_CLUMP: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 166 | AV_T06_BAMBOO_CLUMP: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 167 | AV_T06_BAMBOO_CLUMP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 168 | AV_T06_BAMBOO_CLUMP: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 169 | AV_T02_DEODAR: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.833 m · foot Δ 0.000 m |
| 170 | AV_AQ01_LOTUS: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.032 m · foot Δ 0.000 m |
| 171 | EF: library file exists | ✅ PASS | library/T6_VEG_ENCHANTED_FOREST_v001.blend |
| 172 | EF: file size < 100 MB (GitHub limit) | ✅ PASS | 53.0 MB |
| 173 | EF: opens in Blender 5.3.0, no missing images | ✅ PASS | 64 images, missing [] |
| 174 | EF: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 175 | EF: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 176 | EF: assets in library | ✅ PASS | 12 assets |
| 177 | EF_FE01_GIANT_FERN: valid mesh, UVs | ✅ PASS | 19,328 tris, 16,656 verts |
| 178 | EF_FE01_GIANT_FERN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 179 | EF_FE01_GIANT_FERN: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_FE01_GIANT_FERN_0, MAT_T6_EF_FE01_GIANT_FERN_1 |
| 180 | EF_FE01_GIANT_FERN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 181 | EF_FE01_GIANT_FERN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.010 m |
| 182 | EF_FE01_GIANT_FERN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 183 | EF_FE01_GIANT_FERN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 184 | EF_M01_MOSS_CARPET: valid mesh, UVs | ✅ PASS | 8,200 tris, 5,424 verts |
| 185 | EF_M01_MOSS_CARPET: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 186 | EF_M01_MOSS_CARPET: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_M01_MOSS_CARPET_0, MAT_T6_EF_M01_MOSS_CARPET_1 |
| 187 | EF_M01_MOSS_CARPET: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 188 | EF_M01_MOSS_CARPET: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 189 | EF_M01_MOSS_CARPET: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 190 | EF_MU01_GLOWCAP: valid mesh, UVs | ✅ PASS | 4,268 tris, 2,772 verts |
| 191 | EF_MU01_GLOWCAP: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 192 | EF_MU01_GLOWCAP: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_MU01_GLOWCAP_0, MAT_T6_EF_MU01_GLOWCAP_1, MAT_T6_EF_MU01_GLOWCAP_2 |
| 193 | EF_MU01_GLOWCAP: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 194 | EF_MU01_GLOWCAP: plant base on the ground (no floating) | ✅ PASS | lowest z -0.006 m |
| 195 | EF_MU01_GLOWCAP: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.50 |
| 196 | EF_T01_GIANT_ELDER: valid mesh, UVs | ✅ PASS | 503,266 tris, 388,302 verts |
| 197 | EF_T01_GIANT_ELDER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 198 | EF_T01_GIANT_ELDER: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T01_GIANT_ELDER_BARK, MAT_T6_EF_T01_GIANT_ELDER_LEAF, MAT_T6_EF_T01_GIANT_ELDER_BEARD |
| 199 | EF_T01_GIANT_ELDER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 200 | EF_T01_GIANT_ELDER: height within ±15 % of the design height | ✅ PASS | 66.90 m vs design 62.0 m |
| 201 | EF_T01_GIANT_ELDER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -1.06 m, 499 verts at the foot |
| 202 | EF_T01_GIANT_ELDER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 203 | EF_T01_GIANT_ELDER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 204 | EF_T01_GIANT_ELDER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 205 | EF_T01_GIANT_ELDER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 206 | EF_T02_TEAL_BEECH: valid mesh, UVs | ✅ PASS | 250,800 tris, 213,529 verts |
| 207 | EF_T02_TEAL_BEECH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 208 | EF_T02_TEAL_BEECH: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T02_TEAL_BEECH_BARK, MAT_T6_EF_T02_TEAL_BEECH_LEAF, MAT_T6_EF_T02_TEAL_BEECH_BARK |
| 209 | EF_T02_TEAL_BEECH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 210 | EF_T02_TEAL_BEECH: height within ±15 % of the design height | ✅ PASS | 34.60 m vs design 34.0 m |
| 211 | EF_T02_TEAL_BEECH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.35 m, 346 verts at the foot |
| 212 | EF_T02_TEAL_BEECH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 213 | EF_T02_TEAL_BEECH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 214 | EF_T02_TEAL_BEECH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 215 | EF_T02_TEAL_BEECH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 216 | EF_T03_MOSS_OAK: valid mesh, UVs | ✅ PASS | 225,404 tris, 178,097 verts |
| 217 | EF_T03_MOSS_OAK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 218 | EF_T03_MOSS_OAK: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T03_MOSS_OAK_BARK, MAT_T6_EF_T03_MOSS_OAK_LEAF, MAT_T6_EF_T03_MOSS_OAK_BEARD |
| 219 | EF_T03_MOSS_OAK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 220 | EF_T03_MOSS_OAK: height within ±15 % of the design height | ✅ PASS | 24.29 m vs design 23.0 m |
| 221 | EF_T03_MOSS_OAK: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.83 m, 246 verts at the foot |
| 222 | EF_T03_MOSS_OAK: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 223 | EF_T03_MOSS_OAK: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 224 | EF_T03_MOSS_OAK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 225 | EF_T03_MOSS_OAK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 226 | EF_T04_YEW: valid mesh, UVs | ✅ PASS | 144,544 tris, 117,558 verts |
| 227 | EF_T04_YEW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 228 | EF_T04_YEW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T04_YEW_BARK, MAT_T6_EF_T04_YEW_LEAF, MAT_T6_EF_T04_YEW_BARK |
| 229 | EF_T04_YEW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 230 | EF_T04_YEW: height within ±15 % of the design height | ✅ PASS | 8.69 m vs design 9.0 m |
| 231 | EF_T04_YEW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.34 m, 55 verts at the foot |
| 232 | EF_T04_YEW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 233 | EF_T04_YEW: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 234 | EF_T04_YEW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 235 | EF_T04_YEW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 236 | EF_T05_VEIL_WILLOW: valid mesh, UVs | ✅ PASS | 437,672 tris, 357,472 verts |
| 237 | EF_T05_VEIL_WILLOW: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 238 | EF_T05_VEIL_WILLOW: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T05_VEIL_WILLOW_BARK, MAT_T6_EF_T05_VEIL_WILLOW_LEAF, MAT_T6_EF_T05_VEIL_WILLOW_BARK |
| 239 | EF_T05_VEIL_WILLOW: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 240 | EF_T05_VEIL_WILLOW: height within ±15 % of the design height | ✅ PASS | 18.39 m vs design 18.0 m |
| 241 | EF_T05_VEIL_WILLOW: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.46 m, 44 verts at the foot |
| 242 | EF_T05_VEIL_WILLOW: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 243 | EF_T05_VEIL_WILLOW: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 244 | EF_T05_VEIL_WILLOW: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 245 | EF_T05_VEIL_WILLOW: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 246 | EF_T05_VEIL_WILLOW: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 247 | EF_T06_SPIRAL_ROOT: valid mesh, UVs | ✅ PASS | 223,324 tris, 177,599 verts |
| 248 | EF_T06_SPIRAL_ROOT: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 249 | EF_T06_SPIRAL_ROOT: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T06_SPIRAL_ROOT_BARK, MAT_T6_EF_T06_SPIRAL_ROOT_LEAF, MAT_T6_EF_T06_SPIRAL_ROOT_BARK |
| 250 | EF_T06_SPIRAL_ROOT: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 251 | EF_T06_SPIRAL_ROOT: height within ±15 % of the design height | ✅ PASS | 22.85 m vs design 24.0 m |
| 252 | EF_T06_SPIRAL_ROOT: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -2.34 m, 494 verts at the foot |
| 253 | EF_T06_SPIRAL_ROOT: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 254 | EF_T06_SPIRAL_ROOT: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 255 | EF_T06_SPIRAL_ROOT: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 256 | EF_T06_SPIRAL_ROOT: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 257 | EF_T06_SPIRAL_ROOT: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 258 | EF_T07_LANTERN_TREE: valid mesh, UVs | ✅ PASS | 159,094 tris, 115,732 verts |
| 259 | EF_T07_LANTERN_TREE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 260 | EF_T07_LANTERN_TREE: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T07_LANTERN_TREE_BARK, MAT_T6_EF_T07_LANTERN_TREE_LEAF, MAT_T6_EF_T07_LANTERN_TREE_POD |
| 261 | EF_T07_LANTERN_TREE: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 262 | EF_T07_LANTERN_TREE: height within ±15 % of the design height | ✅ PASS | 15.11 m vs design 15.0 m |
| 263 | EF_T07_LANTERN_TREE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.31 m, 27 verts at the foot |
| 264 | EF_T07_LANTERN_TREE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 265 | EF_T07_LANTERN_TREE: label set (FANTASY (APPROVED R-02)) | ✅ PASS |  |
| 266 | EF_T07_LANTERN_TREE: fantasy asset restricted to R-02 (Decision 01) | ✅ PASS |  |
| 267 | EF_T07_LANTERN_TREE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.60 |
| 268 | EF_T07_LANTERN_TREE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 269 | EF_T08_DEAD_SNAG: valid mesh, UVs | ✅ PASS | 9,816 tris, 5,898 verts |
| 270 | EF_T08_DEAD_SNAG: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 271 | EF_T08_DEAD_SNAG: PBR materials (3 slots) | ✅ PASS | MAT_T6_EF_T08_DEAD_SNAG_BARK, MAT_T6_EF_T08_DEAD_SNAG_NOLEAF, MAT_T6_EF_T08_DEAD_SNAG_FUNGUS |
| 272 | EF_T08_DEAD_SNAG: every face has a valid material slot | ✅ PASS | slots used [0, 2] |
| 273 | EF_T08_DEAD_SNAG: height within ±15 % of the design height | ✅ PASS | 18.74 m vs design 17.0 m |
| 274 | EF_T08_DEAD_SNAG: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.50 m, 244 verts at the foot |
| 275 | EF_T08_DEAD_SNAG: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 276 | EF_T08_DEAD_SNAG: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 277 | EF_T08_DEAD_SNAG: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 278 | EF_T08_DEAD_SNAG: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 279 | EF_V01_HANGING_VINE: valid mesh, UVs | ✅ PASS | 4,080 tris, 4,710 verts |
| 280 | EF_V01_HANGING_VINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 281 | EF_V01_HANGING_VINE: PBR materials (2 slots) | ✅ PASS | MAT_T6_EF_V01_HANGING_VINE_0, MAT_T6_EF_V01_HANGING_VINE_1 |
| 282 | EF_V01_HANGING_VINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 283 | EF_V01_HANGING_VINE: hanging plant attaches at its top (hangs from a branch, z_top = 9.0 m) | ✅ PASS | z 0.45–9.00 m |
| 284 | EF_V01_HANGING_VINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 285 | EF_V01_HANGING_VINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 286 | EF_T01_GIANT_ELDER: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.940 m · foot Δ 0.000 m |
| 287 | EF_FE01_GIANT_FERN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.042 m · foot Δ 0.007 m |
| 288 | MK: library file exists | ✅ PASS | library/T6_VEG_MOUNTAIN_KINGDOM_v001.blend |
| 289 | MK: file size < 100 MB (GitHub limit) | ✅ PASS | 10.1 MB |
| 290 | MK: opens in Blender 5.3.0, no missing images | ✅ PASS | 35 images, missing [] |
| 291 | MK: image paths relative (portable to the Director PC) | ✅ PASS |  |
| 292 | MK: T6_WIND_CONTROL present with strength/gust/speed/flutter | ✅ PASS |  |
| 293 | MK: assets in library | ✅ PASS | 10 assets |
| 294 | MK_F01_GENTIAN: valid mesh, UVs | ✅ PASS | 1,300 tris, 980 verts |
| 295 | MK_F01_GENTIAN: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 296 | MK_F01_GENTIAN: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F01_GENTIAN_0, MAT_T6_MK_F01_GENTIAN_1, MAT_T6_MK_F01_GENTIAN_2 |
| 297 | MK_F01_GENTIAN: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 298 | MK_F01_GENTIAN: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 299 | MK_F01_GENTIAN: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 300 | MK_F01_GENTIAN: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 301 | MK_F02_EDELWEISS: valid mesh, UVs | ✅ PASS | 1,632 tris, 1,296 verts |
| 302 | MK_F02_EDELWEISS: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 303 | MK_F02_EDELWEISS: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F02_EDELWEISS_0, MAT_T6_MK_F02_EDELWEISS_1, MAT_T6_MK_F02_EDELWEISS_2 |
| 304 | MK_F02_EDELWEISS: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 305 | MK_F02_EDELWEISS: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 306 | MK_F02_EDELWEISS: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 307 | MK_F02_EDELWEISS: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 308 | MK_F03_BLUE_POPPY: valid mesh, UVs | ✅ PASS | 752 tris, 561 verts |
| 309 | MK_F03_BLUE_POPPY: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 310 | MK_F03_BLUE_POPPY: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_F03_BLUE_POPPY_0, MAT_T6_MK_F03_BLUE_POPPY_1, MAT_T6_MK_F03_BLUE_POPPY_2 |
| 311 | MK_F03_BLUE_POPPY: every face has a valid material slot | ✅ PASS | slots used [0, 1, 2] |
| 312 | MK_F03_BLUE_POPPY: plant base on the ground (no floating) | ✅ PASS | lowest z -0.001 m |
| 313 | MK_F03_BLUE_POPPY: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 314 | MK_F03_BLUE_POPPY: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 315 | MK_G01_ALPINE_TUSSOCK: valid mesh, UVs | ✅ PASS | 4,000 tris, 3,600 verts |
| 316 | MK_G01_ALPINE_TUSSOCK: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 317 | MK_G01_ALPINE_TUSSOCK: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_G01_ALPINE_TUSSOCK_0, MAT_T6_MK_G01_ALPINE_TUSSOCK_1 |
| 318 | MK_G01_ALPINE_TUSSOCK: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 319 | MK_G01_ALPINE_TUSSOCK: plant base on the ground (no floating) | ✅ PASS | lowest z -0.172 m |
| 320 | MK_G01_ALPINE_TUSSOCK: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 321 | MK_G01_ALPINE_TUSSOCK: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 322 | MK_M01_ALPINE_CUSHION: valid mesh, UVs | ✅ PASS | 2,980 tris, 2,040 verts |
| 323 | MK_M01_ALPINE_CUSHION: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 324 | MK_M01_ALPINE_CUSHION: PBR materials (2 slots) | ✅ PASS | MAT_T6_MK_M01_ALPINE_CUSHION_0, MAT_T6_MK_M01_ALPINE_CUSHION_1 |
| 325 | MK_M01_ALPINE_CUSHION: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 326 | MK_M01_ALPINE_CUSHION: plant base on the ground (no floating) | ✅ PASS | lowest z -0.020 m |
| 327 | MK_M01_ALPINE_CUSHION: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 328 | MK_S01_JUNIPER: valid mesh, UVs | ✅ PASS | 2,538 tris, 2,262 verts |
| 329 | MK_S01_JUNIPER: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 330 | MK_S01_JUNIPER: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S01_JUNIPER_BARK, MAT_T6_MK_S01_JUNIPER_LEAF, MAT_T6_MK_S01_JUNIPER_BARK |
| 331 | MK_S01_JUNIPER: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 332 | MK_S01_JUNIPER: height within ±15 % of the design height | ✅ PASS | 0.82 m vs design 0.9 m |
| 333 | MK_S01_JUNIPER: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.54 m, 987 verts at the foot |
| 334 | MK_S01_JUNIPER: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 335 | MK_S01_JUNIPER: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 336 | MK_S01_JUNIPER: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 337 | MK_S01_JUNIPER: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 338 | MK_S02_DWARF_RHODODENDRON: valid mesh, UVs | ✅ PASS | 1,776 tris, 1,644 verts |
| 339 | MK_S02_DWARF_RHODODENDRON: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 340 | MK_S02_DWARF_RHODODENDRON: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK, MAT_T6_MK_S02_DWARF_RHODODENDRON_LEAF, MAT_T6_MK_S02_DWARF_RHODODENDRON_BARK |
| 341 | MK_S02_DWARF_RHODODENDRON: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 342 | MK_S02_DWARF_RHODODENDRON: height within ±15 % of the design height | ✅ PASS | 0.54 m vs design 0.6 m |
| 343 | MK_S02_DWARF_RHODODENDRON: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.24 m, 724 verts at the foot |
| 344 | MK_S02_DWARF_RHODODENDRON: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 345 | MK_S02_DWARF_RHODODENDRON: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 346 | MK_S02_DWARF_RHODODENDRON: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 347 | MK_S02_DWARF_RHODODENDRON: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 348 | MK_T01_HIMALAYAN_SPRUCE: valid mesh, UVs | ✅ PASS | 225,678 tris, 188,336 verts |
| 349 | MK_T01_HIMALAYAN_SPRUCE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 350 | MK_T01_HIMALAYAN_SPRUCE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_LEAF, MAT_T6_MK_T01_HIMALAYAN_SPRUCE_BARK |
| 351 | MK_T01_HIMALAYAN_SPRUCE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 352 | MK_T01_HIMALAYAN_SPRUCE: height within ±15 % of the design height | ✅ PASS | 31.32 m vs design 32.0 m |
| 353 | MK_T01_HIMALAYAN_SPRUCE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.41 m, 309 verts at the foot |
| 354 | MK_T01_HIMALAYAN_SPRUCE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 355 | MK_T01_HIMALAYAN_SPRUCE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 356 | MK_T01_HIMALAYAN_SPRUCE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 357 | MK_T01_HIMALAYAN_SPRUCE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 358 | MK_T02_HIMALAYAN_BIRCH: valid mesh, UVs | ✅ PASS | 95,664 tris, 76,036 verts |
| 359 | MK_T02_HIMALAYAN_BIRCH: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 360 | MK_T02_HIMALAYAN_BIRCH: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK, MAT_T6_MK_T02_HIMALAYAN_BIRCH_LEAF, MAT_T6_MK_T02_HIMALAYAN_BIRCH_BARK |
| 361 | MK_T02_HIMALAYAN_BIRCH: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 362 | MK_T02_HIMALAYAN_BIRCH: height within ±15 % of the design height | ✅ PASS | 11.59 m vs design 12.0 m |
| 363 | MK_T02_HIMALAYAN_BIRCH: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.28 m, 32 verts at the foot |
| 364 | MK_T02_HIMALAYAN_BIRCH: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 365 | MK_T02_HIMALAYAN_BIRCH: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 366 | MK_T02_HIMALAYAN_BIRCH: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 367 | MK_T02_HIMALAYAN_BIRCH: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 368 | MK_T03_KRUMMHOLZ_PINE: valid mesh, UVs | ✅ PASS | 21,942 tris, 15,328 verts |
| 369 | MK_T03_KRUMMHOLZ_PINE: wind attributes | ✅ PASS | wind_trunk,wind_branch,wind_leaf,wind_phase,leaf_rand |
| 370 | MK_T03_KRUMMHOLZ_PINE: PBR materials (3 slots) | ✅ PASS | MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK, MAT_T6_MK_T03_KRUMMHOLZ_PINE_LEAF, MAT_T6_MK_T03_KRUMMHOLZ_PINE_BARK |
| 371 | MK_T03_KRUMMHOLZ_PINE: every face has a valid material slot | ✅ PASS | slots used [0, 1] |
| 372 | MK_T03_KRUMMHOLZ_PINE: height within ±15 % of the design height | ✅ PASS | 6.12 m vs design 5.5 m |
| 373 | MK_T03_KRUMMHOLZ_PINE: grounded (trunk foot / roots below ground level) | ✅ PASS | lowest z -0.40 m, 272 verts at the foot |
| 374 | MK_T03_KRUMMHOLZ_PINE: no limbs through the ground | ✅ PASS | 0 verts far + under ground |
| 375 | MK_T03_KRUMMHOLZ_PINE: label set (SPECIES-INSPIRED) | ✅ PASS |  |
| 376 | MK_T03_KRUMMHOLZ_PINE: glow subtle (emission ≤ 1.0, Decision 01 §3) | ✅ PASS | max emission 0.00 |
| 377 | MK_T03_KRUMMHOLZ_PINE: wind modifier + drivers valid | ✅ PASS | 4 drivers |
| 378 | MK_T01_HIMALAYAN_SPRUCE: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.819 m · foot Δ 0.000 m |
| 379 | MK_F01_GENTIAN: wind — calm = static, strength 2 = motion, foot stays fixed | ✅ PASS | calm Δ 0.0e+00 m · moving Δmax 0.020 m · foot Δ 0.006 m |

## Blender textures (python3 + Pillow) — **25/25 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | atlas av_bamboo: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 2 | atlas av_banj: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 7% |
| 3 | atlas av_berberis: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 4 | atlas av_chir: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 5 | atlas av_deodar: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 6 | atlas av_fern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 27% |
| 7 | atlas av_kans: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 2% |
| 8 | atlas av_lotus: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 69% |
| 9 | atlas av_peepal: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 10 | atlas av_rhodo: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 19% |
| 11 | atlas av_tulsi: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 14% |
| 12 | atlas ef_beech: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 12% |
| 13 | atlas ef_elder: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 9% |
| 14 | atlas ef_fern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 27% |
| 15 | atlas ef_lantern: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 38% |
| 16 | atlas ef_moss: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 5% |
| 17 | atlas ef_oak: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 18 | atlas ef_spiral: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 17% |
| 19 | atlas ef_veil: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 4% |
| 20 | atlas ef_yew: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 11% |
| 21 | atlas mk_birch: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 13% |
| 22 | atlas mk_juniper: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 8% |
| 23 | atlas mk_krumm: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 10% |
| 24 | atlas mk_rhodo_dwarf: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 17% |
| 25 | atlas mk_spruce: colour+alpha / normal / roughness maps 2K | ✅ PASS | col 2048², nor 2048², rough 2048², coverage 9% |

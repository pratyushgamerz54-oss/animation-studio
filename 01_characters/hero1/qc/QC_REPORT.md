# QC REPORT — Hero 1 (HERO1)

Generated 2026-11-20 18:35 by `_shared/production.py`.

## Automated checks

| Check | Result | Detail |
|---|---|---|
| Mesh sanity (no exploded geometry) | ✅ PASS | [] |
| Body fully weighted | ✅ PASS | 0 unweighted verts |
| UVs on all meshes | ✅ PASS |  |
| Textures baked | ✅ PASS | 116 maps |
| IK/FK rest pose unchanged + IK follows target | ✅ PASS | follow error 0.02 mm |
| Phoneme shape keys (10) | ✅ PASS | 19 mouth keys |
| GLB export + re-import | ✅ PASS | {'objects': 31, 'armatures': 1, 'meshes': 30, 'bones': 63, 'shape_key_meshes': 2} |
| FBX export | ✅ PASS | 18.49 |

## Render-based tests (images in `design/raw/`, review by eye)

| Test | Image |
|---|---|
| Turnaround consistency (6 views) | `turn_front.png` ✅ rendered |
| Joint / elbow / knee / finger deformation pose | `test_deform_test.png` ✅ rendered |
| Run / jump / land / turn / fight poses | `test_run.png` ✅ rendered |
| Facial expressions | `expr_00_neutral.png` ✅ rendered |
| Eye movement + blink | `expr_10_blink.png` ✅ rendered |
| Lip-sync phonemes | `lipsync_PH_A.png` ✅ rendered |
| Power activation renders | `power_normal.png` ✅ rendered |

## Rig

- Bones: 63 (52 deform)
- Controls: CTRL_COG, IK_hand_L, POLE_arm_L, IK_foot_L, POLE_leg_L, IK_hand_R, POLE_arm_R, IK_foot_R, POLE_leg_R, CTRL_EYES, root
- IK/FK switches (on `root`): ik_arm_L, ik_leg_L, ik_arm_R, ik_leg_R
- Pole angles / rest deviation: {"arm_L": {"pole_angle": 180, "rest_deviation_mm": 1.196}, "leg_L": {"pole_angle": -90, "rest_deviation_mm": 3.13}, "arm_R": {"pole_angle": 0, "rest_deviation_mm": 1.196}, "leg_R": {"pole_angle": -90, "rest_deviation_mm": 3.13}}
- Face controls (on `root`): 23 — blink_L, blink_R, expr_angry, expr_confident, expr_crying, expr_evil, expr_fear, expr_happy, expr_sad, expr_serious, expr_shocked, lid_wide_L, lid_wide_R, ph_a, ph_e, ph_fv, ph_i, ph_l, ph_mbp, ph_o, ph_rest, ph_u, ph_w

## Known limitations (honest)

- Body rig is a custom deform skeleton + IK/FK controls, not a full Rigify rig (no stretch/twist bones).
- Jaw is driven through the mouth shape keys (`jaw_open` → PH_A); the chin mesh does not move yet.
- Textures are baked from procedural materials (no hand-painted detail).
- Base meshes contain non-manifold edges where garment pieces are open shells (expected for clothing).
- Non-manifold edge counts: {"CHAR_HERO1_BELT": 22, "CHAR_HERO1_BOOT_L": 10, "CHAR_HERO1_BOOT_R": 10, "CHAR_HERO1_BROWS": 44, "CHAR_HERO1_COAT": 48, "CHAR_HERO1_COAT_COLLAR": 16, "CHAR_HERO1_COAT_TAILS": 124, "CHAR_HERO1_GAUNTLET_L": 16, "CHAR_HERO1_GAUNTLET_R": 16, "CHAR_HERO1_GLOVE_L": 11, "CHAR_HERO1_GLOVE_R": 11, "CHAR_HERO1_HAIR_CAP": 156, "CHAR_HERO1_LID_LO_L": 64, "CHAR_HERO1_LID_LO_R": 64, "CHAR_HERO1_LID_UP_L": 64, "CHAR_HERO1_LID_UP_R": 64, "CHAR_HERO1_MOUTH": 120, "CHAR_HERO1_PAULDRON_L": 16, "CHAR_HERO1_PAULDRON_R": 16, "CHAR_HERO1_SUIT": 48}

Quad ratio body 1.0, head 1.0; meshes 29; render-time polycount ≈ 464,144

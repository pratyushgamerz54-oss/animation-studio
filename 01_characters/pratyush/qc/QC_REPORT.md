# QC REPORT — Pratyush (PRATYUSH)

Generated 2026-11-20 18:41 by `_shared/production.py`.

## Automated checks

| Check | Result | Detail |
|---|---|---|
| Mesh sanity (no exploded geometry) | ✅ PASS | [] |
| Body fully weighted | ✅ PASS | 0 unweighted verts |
| UVs on all meshes | ✅ PASS |  |
| Textures baked | ✅ PASS | 128 maps |
| IK/FK rest pose unchanged + IK follows target | ✅ PASS | follow error 0.02 mm |
| Phoneme shape keys (10) | ✅ PASS | 19 mouth keys |
| GLB export + re-import | ✅ PASS | {'objects': 34, 'armatures': 1, 'meshes': 33, 'bones': 63, 'shape_key_meshes': 2} |
| FBX export | ✅ PASS | 16.18 |

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
- Pole angles / rest deviation: {"arm_L": {"pole_angle": 180, "rest_deviation_mm": 1.195}, "leg_L": {"pole_angle": -90, "rest_deviation_mm": 3.119}, "arm_R": {"pole_angle": 0, "rest_deviation_mm": 1.195}, "leg_R": {"pole_angle": -90, "rest_deviation_mm": 3.119}}
- Face controls (on `root`): 23 — blink_L, blink_R, expr_angry, expr_confident, expr_crying, expr_evil, expr_fear, expr_happy, expr_sad, expr_serious, expr_shocked, lid_wide_L, lid_wide_R, ph_a, ph_e, ph_fv, ph_i, ph_l, ph_mbp, ph_o, ph_rest, ph_u, ph_w

## Known limitations (honest)

- Body rig is a custom deform skeleton + IK/FK controls, not a full Rigify rig (no stretch/twist bones).
- Jaw is driven through the mouth shape keys (`jaw_open` → PH_A); the chin mesh does not move yet.
- Textures are baked from procedural materials (no hand-painted detail).
- Base meshes contain non-manifold edges where garment pieces are open shells (expected for clothing).
- Non-manifold edge counts: {"CHAR_PRATYUSH_BELT": 20, "CHAR_PRATYUSH_BOOT_L": 8, "CHAR_PRATYUSH_BOOT_R": 8, "CHAR_PRATYUSH_BRACER_L": 16, "CHAR_PRATYUSH_BRACER_R": 16, "CHAR_PRATYUSH_BROWS": 44, "CHAR_PRATYUSH_CHEST_PLATE": 26, "CHAR_PRATYUSH_COLLAR": 22, "CHAR_PRATYUSH_EMBLEM": 9, "CHAR_PRATYUSH_GLOVE_L": 12, "CHAR_PRATYUSH_GLOVE_R": 12, "CHAR_PRATYUSH_HAIR_CAP": 156, "CHAR_PRATYUSH_KNEE_L": 14, "CHAR_PRATYUSH_KNEE_R": 14, "CHAR_PRATYUSH_LID_LO_L": 64, "CHAR_PRATYUSH_LID_LO_R": 64, "CHAR_PRATYUSH_LID_UP_L": 64, "CHAR_PRATYUSH_LID_UP_R": 64, "CHAR_PRATYUSH_MOUTH": 120, "CHAR_PRATYUSH_PAULDRON_L": 24, "CHAR_PRATYUSH_PAUL

Quad ratio body 1.0, head 1.0; meshes 32; render-time polycount ≈ 454,112

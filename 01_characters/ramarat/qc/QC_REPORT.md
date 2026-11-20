# QC REPORT — Ramarat (RAMARAT)

Generated 2026-11-20 19:03 by `_shared/production.py`.

## Automated checks

| Check | Result | Detail |
|---|---|---|
| Mesh sanity (no exploded geometry) | ✅ PASS | [] |
| Body fully weighted | ✅ PASS | 0 unweighted verts |
| UVs on all meshes | ✅ PASS |  |
| Textures baked | ✅ PASS | 88 maps |
| IK/FK rest pose unchanged + IK follows target | ✅ PASS | follow error 0.03 mm |
| Phoneme shape keys (10) | ✅ PASS | 19 mouth keys |
| GLB export + re-import | ✅ PASS | {'objects': 24, 'armatures': 1, 'meshes': 23, 'bones': 63, 'shape_key_meshes': 2} |
| FBX export | ✅ PASS | 19.59 |

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
- Pole angles / rest deviation: {"arm_L": {"pole_angle": 180, "rest_deviation_mm": 1.196}, "leg_L": {"pole_angle": -90, "rest_deviation_mm": 3.126}, "arm_R": {"pole_angle": 0, "rest_deviation_mm": 1.196}, "leg_R": {"pole_angle": -90, "rest_deviation_mm": 3.126}}
- Face controls (on `root`): 23 — blink_L, blink_R, expr_angry, expr_concerned, expr_confident, expr_disappointed, expr_furious, expr_serious, expr_shocked, expr_suspicious, expr_wise, lid_wide_L, lid_wide_R, ph_a, ph_e, ph_fv, ph_i, ph_l, ph_mbp, ph_o, ph_rest, ph_u, ph_w

## Known limitations (honest)

- Body rig is a custom deform skeleton + IK/FK controls, not a full Rigify rig (no stretch/twist bones).
- Jaw is driven through the mouth shape keys (`jaw_open` → PH_A); the chin mesh does not move yet.
- Textures are baked from procedural materials (no hand-painted detail).
- Base meshes contain non-manifold edges where garment pieces are open shells (expected for clothing).
- Non-manifold edge counts: {"CHAR_RAMARAT_BROWS": 44, "CHAR_RAMARAT_HAIR_CAP": 166, "CHAR_RAMARAT_INNER_SLEEVE": 32, "CHAR_RAMARAT_LID_LO_L": 64, "CHAR_RAMARAT_LID_LO_R": 64, "CHAR_RAMARAT_LID_UP_L": 64, "CHAR_RAMARAT_LID_UP_R": 64, "CHAR_RAMARAT_MANTLE": 24, "CHAR_RAMARAT_MOUTH": 120, "CHAR_RAMARAT_ROBE_SKIRT": 124, "CHAR_RAMARAT_ROBE_UPPER": 38, "CHAR_RAMARAT_SASH": 22, "CHAR_RAMARAT_SASH_TAIL": 8, "CHAR_RAMARAT_TROUSERS": 36}

Quad ratio body 1.0, head 1.0; meshes 22; render-time polycount ≈ 754,512

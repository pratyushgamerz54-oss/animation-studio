# QC REPORT — Hero 1 (HERO1)

Generated 2026-11-21 01:33 by `_shared/production.py`.

## Automated checks

| Check | Result | Detail |
|---|---|---|
| Mesh sanity (no exploded geometry) | ✅ PASS | [] |
| Body fully weighted | ✅ PASS | 0 unweighted verts |
| UVs on all meshes | ✅ PASS |  |
| Textures baked | ✅ PASS | 116 maps |
| IK/FK rest pose unchanged + IK follows target | ✅ PASS | follow error 0.02 mm |
| Phoneme shape keys (10) | ✅ PASS | 19 mouth keys |
| Jaw bone opens the chin (jaw_open = 1) | ✅ PASS | chin drop 9.8 mm |
| Robe / skirt follow-rig (chains follow the thighs) | ✅ PASS | {'bones': 36, 'constraints': 72, 'ok': True} |
| GLB export + re-import | ✅ PASS | {'objects': 31, 'armatures': 1, 'meshes': 30, 'bones': 100, 'shape_key_meshes': 2} |
| FBX export | ✅ PASS | 19.17 |

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

- Bones: 100 (89 deform)
- Controls: CTRL_COG, IK_hand_L, POLE_arm_L, IK_foot_L, POLE_leg_L, IK_hand_R, POLE_arm_R, IK_foot_R, POLE_leg_R, CTRL_EYES, root
- IK/FK switches (on `root`): ik_arm_L, ik_leg_L, ik_arm_R, ik_leg_R
- Pole angles / rest deviation: {"arm_L": {"pole_angle": 180, "rest_deviation_mm": 1.196}, "leg_L": {"pole_angle": -90, "rest_deviation_mm": 3.13}, "arm_R": {"pole_angle": 0, "rest_deviation_mm": 1.196}, "leg_R": {"pole_angle": -90, "rest_deviation_mm": 3.13}}
- Face controls (on `root`): 24 — blink_L, blink_R, expr_angry, expr_confident, expr_crying, expr_evil, expr_fear, expr_happy, expr_sad, expr_serious, expr_shocked, jaw (bone), lid_wide_L, lid_wide_R, ph_a, ph_e, ph_fv, ph_i, ph_l, ph_mbp, ph_o, ph_rest, ph_u, ph_w

## Known limitations (honest)

- This v003 rig is the clean game/export skeleton (custom IK/FK). The full Rigify animation rig is `blend/<name>_v004_rigify.blend` (see RIGIFY section).
- Jaw: real `jaw` bone (head + beard weighted), driven by `jaw_open`, phonemes and open-mouth expressions.
- Textures are baked from procedural materials (no hand-painted detail).
- Base meshes contain non-manifold edges where garment pieces are open shells (expected for clothing).
- Non-manifold edge counts: {"CHAR_HERO1_BELT": 22, "CHAR_HERO1_BOOT_L": 10, "CHAR_HERO1_BOOT_R": 10, "CHAR_HERO1_BROWS": 44, "CHAR_HERO1_COAT": 48, "CHAR_HERO1_COAT_COLLAR": 16, "CHAR_HERO1_COAT_TAILS": 124, "CHAR_HERO1_GAUNTLET_L": 16, "CHAR_HERO1_GAUNTLET_R": 16, "CHAR_HERO1_GLOVE_L": 11, "CHAR_HERO1_GLOVE_R": 11, "CHAR_HERO1_HAIR_CAP": 156, "CHAR_HERO1_LID_LO_L": 64, "CHAR_HERO1_LID_LO_R": 64, "CHAR_HERO1_LID_UP_L": 64, "CHAR_HERO1_LID_UP_R": 64, "CHAR_HERO1_MOUTH": 120, "CHAR_HERO1_PAULDRON_L": 16, "CHAR_HERO1_PAULDRON_R": 16, "CHAR_HERO1_SUIT": 48}

Quad ratio body 1.0, head 1.0; meshes 29; render-time polycount ≈ 464,144

## RIGIFY animation rig (v004) — `blend/hero1_v004_rigify.blend`

Rigify rig generated from a meta-rig fitted to the deform skeleton: IK/FK arms + legs (poles, IK/FK sliders, foot roll), torso / hips / chest, neck + head follow, palms + 15 finger bones per hand (finger curl controls), jaw control, eye-aim control, robe/skirt chain controls (follow the thighs). Face controls (expressions, phonemes, jaw_open, blink, wide eyes) are custom properties on the Rigify `root` bone.

| Check | Result | Detail |
|---|---|---|
| Rest pose unchanged after moving to Rigify | ✅ PASS | max 0.005 mm |
| Leg IK follows foot control | ✅ PASS | error 0.03 mm, ankle lift 205.7 mm |
| FK arm moves the elbow | ✅ PASS | 248.0 mm |
| Jaw control opens the chin | ✅ PASS | 9.8 mm |
| All weights moved to Rigify DEF bones | ✅ PASS | unmapped: [] |
| Face drivers re-targeted / skirt follow constraints | ✅ | 61 / 72 |

Bones: 534 (97 deform). Posed test render: `qc/HERO1_rigify_test.png`.
GLB/FBX in `export/` use the clean v003 game skeleton (Rigify control bones are Blender-only).

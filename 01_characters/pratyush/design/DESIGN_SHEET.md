# PRATYUSH — Hero 2 / main second lead — Design Sheet v1 (PROPOSAL)

> **Status: awaiting Director approval.** Confirmed: name (Pratyush), role, powers (Super Speed, Magical Portal, Lightning) and the reference. Everything else is a proposal.

## Sheet pages (renders of the real Blender model)

- `PRATYUSH_sheet_01_turnaround.png`
- `PRATYUSH_sheet_02_poses_measurements.png`
- `PRATYUSH_sheet_03_face.png`
- `PRATYUSH_sheet_04_expressions.png`
- `PRATYUSH_sheet_05_costume.png`
- `PRATYUSH_sheet_06_palette.png`
- `PRATYUSH_sheet_07_powers.png`

## Reference interpretation

Reference: `reference/pratyush_ref_01.png`

Taken: sleek armoured full-body speed suit, gloves, armoured boots, crackling lightning, sprint pose. Kept original: navy / electric-blue colours (not red/gold), chevron emblem (no bolt-in-circle), no cowl.

## Identity (proposal)

- Age: 17 (proposed)
- Build: Lean athletic sprinter: long legs, narrow waist, defined shoulders
- Silhouette: Upward-swept hair spikes + high armoured collar + angular shoulder plates

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#B07650` | 176, 118, 80 |
| skin_tint | `#B5614A` | 181, 97, 74 |
| lip | `#8E5141` | 142, 81, 65 |
| hair | `#17120F` | 23, 18, 15 |
| hair_streak | `#2EA8FF` | 46, 168, 255 |
| brow | `#17120F` | 23, 18, 15 |
| eye | `#5A361F` | 90, 54, 31 |
| eye_dark | `#2A170C` | 42, 23, 12 |
| power_eye | `#5BE0FF` | 91, 224, 255 |
| suit | `#16243F` | 22, 36, 63 |
| armor | `#5C6B80` | 92, 107, 128 |
| accent | `#2EA8FF` | 46, 168, 255 |
| boot | `#1E2C4A` | 30, 44, 74 |
| sole | `#2EA8FF` | 46, 168, 255 |
| glove | `#141519` | 20, 21, 25 |
| metal | `#B7C0CC` | 183, 192, 204 |
| power_glow | `#4FD8FF` | 79, 216, 255 |
| power_core | `#F2FBFF` | 242, 251, 255 |
| portal_rim | `#6FE7FF` | 111, 231, 255 |
| portal_deep | `#0A2A5A` | 10, 42, 90 |
| speed_trail | `#2EA8FF` | 46, 168, 255 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Main: armoured speed suit | CHAR_PRATYUSH_SUIT | Stretch technical knit (4-way) | #16243F rough .45 sheen .35; piping #2EA8FF emissive | Skin-tight: skinned, no sim; corrective shapes elbows/knees |
| Outer: chest plate, pauldrons, knees, collar | CHAR_PRATYUSH_CHEST_PLATE, CHAR_PRATYUSH_PAULDRON_L, CHAR_PRATYUSH_PAULDRON_R, CHAR_PRATYUSH_KNEE_L, CHAR_PRATYUSH_KNEE_R, CHAR_PRATYUSH_COLLAR, CHAR_PRATYUSH_EMBLEM | Moulded composite plates | #5C6B80 metallic .65 rough .32; edge light #2EA8FF | Rigid, skinned 1:1 |
| Shoes: armoured sprint boots | CHAR_PRATYUSH_BOOT_L, CHAR_PRATYUSH_BOOT_R | Armoured synthetic leather | #1E2C4A; sole & bands #2EA8FF | Rigid |
| Gloves: full-finger grip | CHAR_PRATYUSH_GLOVE_L | Grip synthetic | #141519 rough .45 | Skinned per finger |
| Belt + buckle | CHAR_PRATYUSH_BELT, CHAR_PRATYUSH_BELT_BUCKLE | Plate belt | #5C6B80 / #B7C0CC metal | Rigid |
| Special equipment: speed bracers | CHAR_PRATYUSH_BRACER_L, CHAR_PRATYUSH_BRACER_CORE_L | Brushed metal + energy core | #B7C0CC metal; core #4FD8FF emission | Rigid on forearm |
| Hair (cap + clumps) | CHAR_PRATYUSH_HAIR, CHAR_PRATYUSH_HAIR_CAP | Stylised clump geometry | #17120F rough .42 sheen .5 | Optional spring bones |

## Face

- **EYES:** Dark-brown iris #5A361F, almond lids; glow #5BE0FF when powered
- **BROWS:** Straight, slightly raised outer end, tapered; near-black
- **NOSE / LIPS:** Straight bridge, rounded tip, defined alae; medium lips with philtrum
- **JAW / CHIN:** Defined jawline and gonial angle, firm rounded chin; high cheekbones
- **PROPORTIONS:** Eye line at 1/2 head height, eye spacing = 1 eye width, mouth at 2/3 of lower face
- **HAIR:** Near-black spiky ribbon clumps swept up & back; 1 electric-blue streak in the fringe

Expressions (11): neutral, happy, angry, sad, fear, shocked, confident, evil, serious, crying, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_PRATYUSH_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 174.4 cm
- height total: 184.3 cm
- head height: 21.7 cm
- head-to-body ratio: 8.05 heads
- shoulder width: 52.3 cm
- chest width: 32.8 cm
- hip width: 31.2 cm
- leg length: 89.4 cm
- arm length: 73.8 cm
- hand length: 20.3 cm
- foot length: 22.0 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Super Speed | no effect | Eyes glow, bracer/core brighten, short trails at the legs, sparks at the feet | Long horizontal streaks from every limb + 2 tinted afterimages + crackle | Trails shrink, eyes fade |
| Lightning | no effect | Small arcs crawl over the hand | Branching bolt from the palm + arcs along the arms and body | Residual sparks at the fingertips |
| Magical Portal | no effect | Portal opens at 25 % in front of the palm, rune ring on the hand | Full swirl disc, white-hot rim, spark ring, portal light | Portal shrinks to 35 % and dims |

Eye transformation: iris emission ramps normal → activation → full (shared by all powers).
Reusable VFX functions live in `../../_shared/vfxkit.py` (intensity / openness / length parameters).

## Technical 3D specification

- Topology: all-quad body cage (skin modifier + subdivision) with ring edge loops at every joint; code sculpt pass for anatomy; all-quad head (sculpted sphere, 26 cuts) with jawline, brow ridge, nose, philtrum, nasolabial folds.
- Hands: 5 fingers × 3 segments; feet with heel/ball/toe.
- Clothing: separate meshes generated from the body surface (offset + solidify) → exact fit; robes/capes are lofted sheets.
- UVs: smart-projected per mesh; layouts in `uv/`. Textures: baked BaseColor / Roughness / Normal / Emission in `textures/`.
- Rig: deform skeleton (pelvis, 3 spine, neck, head, clavicles, arms, 15 finger bones per hand, legs, feet, toes) + root, COG, hand/foot IK targets with pole targets and IK/FK switches; eye-aim control.
- Facial rig: shape keys for every expression + 10 phonemes, `jaw_open`, blink / wide-eye per side, eye look; all driven by properties on the `root` pose bone.

## Production status

See `qc/QC_REPORT.md` for the automated checks and test renders.
- `.blend`: `blend/pratyush_v002.blend` (design), `blend/pratyush_v003.blend` (production rig + controls)
- Exports: `export/pratyush.glb` (9.71 MB), `export/pratyush.fbx` (16.18 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Jaw opens through mouth shape keys; the chin does not move.
- Cloth simulation is specified but not simulated yet.

# HERO 1 — Hero 1 / main hero (name pending) — Design Sheet v1 (APPROVED 20 Nov)

> **Status: design APPROVED by the Director (20 Nov).** Confirmed: name (PENDING — using HERO 1), role, powers (Fire Manipulation, Magical Portal), the reference and the full design.

## Sheet pages (renders of the real Blender model)

- `HERO1_sheet_01_turnaround.png`
- `HERO1_sheet_02_poses_measurements.png`
- `HERO1_sheet_03_face.png`
- `HERO1_sheet_04_expressions.png`
- `HERO1_sheet_05_costume.png`
- `HERO1_sheet_06_palette.png`
- `HERO1_sheet_07_powers.png`

## Reference interpretation

Reference: `combination of the Director reference set (no own reference)`

Combined: long flowing coat with embroidered trim (Ramarat), glowing chest core (Saithan), fitted armoured under-suit & pauldrons (Pratyush), forearm gauntlets (Max), energy on the arms (Yayaki). Own identity: crimson + gold fire palette, swept hair with flame-orange tips.

## Identity (proposal)

- Age: 18 (proposed)
- Build: Athletic heroic build — broad shoulders, V-taper, strong arms
- Silhouette: Swept-back flame hair + high coat collar + long split coat tails = triangular "flame" read

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#9C6B4A` | 156, 107, 74 |
| skin_tint | `#A9564A` | 169, 86, 74 |
| lip | `#7E4436` | 126, 68, 54 |
| hair | `#2A1A12` | 42, 26, 18 |
| hair_tip | `#FF7A1A` | 255, 122, 26 |
| brow | `#24160F` | 36, 22, 15 |
| eye | `#B8741F` | 184, 116, 31 |
| eye_dark | `#5A3008` | 90, 48, 8 |
| power_eye | `#FFB347` | 255, 179, 71 |
| coat | `#7A1414` | 122, 20, 20 |
| suit | `#1C1A1F` | 28, 26, 31 |
| gold | `#D4A440` | 212, 164, 64 |
| armor | `#3A2E2A` | 58, 46, 42 |
| boot | `#1E1715` | 30, 23, 21 |
| accent | `#FF8A1F` | 255, 138, 31 |
| fire_core | `#FFF2B0` | 255, 242, 176 |
| fire_mid | `#FF8A1F` | 255, 138, 31 |
| fire_outer | `#B3170A` | 179, 23, 10 |
| portal_rim | `#FFC25A` | 255, 194, 90 |
| portal_deep | `#3A0A05` | 58, 10, 5 |
| power_glow | `#FF9A3C` | 255, 154, 60 |
| power_core | `#FFF2D6` | 255, 242, 214 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Inner: armoured under-suit | CHAR_HERO1_SUIT | Fire-resistant aramid knit | #1C1A1F; seams #FF8A1F | Skinned, no sim |
| Outer: long battle coat | CHAR_HERO1_COAT, CHAR_HERO1_COAT_COLLAR, CHAR_HERO1_COAT_TAILS | Heavy wool-silk blend, gold embroidery | #7A1414 rough .6 sheen .45; trim #D4A440 | Coat tails: cloth sim (pinned at waist) |
| Pauldrons + gauntlets | CHAR_HERO1_PAULDRON_L, CHAR_HERO1_PAULDRON_R, CHAR_HERO1_GAUNTLET_L | Forged plate | #3A2E2A metal .6; gold edges | Rigid |
| Special: chest fire core | CHAR_HERO1_CHEST_CORE, CHAR_HERO1_CORE_RING | Crystal core + gold ring | core #FF8A1F emission; ring gold | Rigid |
| Shoes: plated boots | CHAR_HERO1_BOOT_L, CHAR_HERO1_BOOT_R | Leather + plate | #1E1715; gold bands | Rigid |
| Gloves | CHAR_HERO1_GLOVE_L | Leather | #1A1414 | Skinned per finger |
| Belt | CHAR_HERO1_BELT | Gold plate belt | #D4A440 metal 1.0 | Rigid |
| Hair | CHAR_HERO1_HAIR, CHAR_HERO1_HAIR_CAP | Stylised clumps, flame tips | root #2A1A12 → tip #FF7A1A | Optional spring bones |

## Face

- **EYES:** Amber iris #B8741F; glow #FFB347 when fire is active
- **BROWS:** Thick, straight, determined; dark brown
- **NOSE / LIPS:** Strong straight nose, medium lips
- **JAW / CHIN:** Broad heroic jaw, square chin, high cheekbones
- **PROPORTIONS:** 7.5 heads; eye line at 1/2 head height
- **HAIR:** Dark brown swept up-and-back clumps; tips burn to flame-orange #FF7A1A

Expressions (11): neutral, happy, angry, sad, fear, shocked, confident, evil, serious, crying, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_HERO1_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 179.0 cm
- height total: 185.1 cm
- head height: 21.8 cm
- head-to-body ratio: 8.19 heads
- shoulder width: 53.4 cm
- chest width: 34.0 cm
- hip width: 32.9 cm
- leg length: 92.0 cm
- arm length: 75.9 cm
- hand length: 20.9 cm
- foot length: 22.7 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Fire | no effect | Flames lick from the fingertips | Fireball with flame tail from the palm + full-body fire aura | Small embers on three fingers |
| Magical Portal | no effect | Portal opens at 25 % in front of the palm, rune ring on the hand | Full swirl disc, white-hot rim, spark ring, portal light | Portal shrinks to 35 % and dims |

Eye transformation: iris emission ramps normal → activation → full (shared by all powers).
Reusable VFX functions live in `../../_shared/vfxkit.py` (intensity / openness / length parameters).

## Technical 3D specification

- Topology: all-quad body cage (skin modifier + subdivision) with ring edge loops at every joint; code sculpt pass for anatomy; all-quad head (sculpted sphere, 26 cuts) with jawline, brow ridge, nose, philtrum, nasolabial folds.
- Hands: 5 fingers × 3 segments; feet with heel/ball/toe.
- Clothing: separate meshes generated from the body surface (offset + solidify) → exact fit; robes/capes are lofted sheets.
- UVs: smart-projected per mesh; layouts in `uv/`. Textures: baked BaseColor / Roughness / Normal / Emission in `textures/`.
- Rig: deform skeleton (pelvis, 3 spine, neck, head, clavicles, arms, 15 finger bones per hand, legs, feet, toes) + root, COG, hand/foot IK targets with pole targets and IK/FK switches; eye-aim control.
- **Rigify animation rig** (`blend/<name>_v004_rigify.blend`): IK/FK arms + legs, foot roll, torso/hips/chest, neck/head follow, finger curls, jaw + eye-aim controls, robe/skirt chain controls; same face controls on `root`.
- Facial rig: shape keys for every expression + 10 phonemes, `jaw_open`, blink / wide-eye per side, eye look; all driven by properties on the `root` pose bone.

## Production status

See `qc/QC_REPORT.md` for the automated checks and test renders.
- `.blend`: `blend/hero1_v002.blend` (design), `blend/hero1_v003.blend` (game/export rig + controls), `blend/hero1_v004_rigify.blend` (Rigify animation rig — use this for animation)
- Exports: `export/hero1.glb` (11.99 MB), `export/hero1.fbx` (19.17 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Robes / skirts use a 12-chain follow rig (no stiff tube); a cloth simulation pass is still recommended for final shots.

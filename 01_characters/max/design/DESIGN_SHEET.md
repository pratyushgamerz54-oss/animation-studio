# MAX — Sub-villain 2 — Design Sheet v1 (APPROVED 20 Nov)

> **Status: design APPROVED by the Director (20 Nov).** Confirmed: name (Max), role, powers (Laser (hands + eyes)), the reference and the full design.

## Sheet pages (renders of the real Blender model)

- `MAX_sheet_01_turnaround.png`
- `MAX_sheet_02_poses_measurements.png`
- `MAX_sheet_03_face.png`
- `MAX_sheet_04_expressions.png`
- `MAX_sheet_05_costume.png`
- `MAX_sheet_06_palette.png`
- `MAX_sheet_07_powers.png`

## Reference interpretation

Reference: `reference/max_ref_01.png`

Taken: bald, blue-grey skin, red eyes, heavy blue-grey sci-fi armour, two green chest lenses and green light lines, big pauldrons and gauntlets. Own plate layout; no added weapons.

## Identity (proposal)

- Age: NOT CONFIRMED (appears ~35)
- Build: Bulky powerhouse — thick neck, massive chest and arms
- Silhouette: Bald dome + huge squared pauldrons + armoured gauntlets = heavy block

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#6F7F93` | 111, 127, 147 |
| skin_tint | `#7C6E86` | 124, 110, 134 |
| lip | `#4C5466` | 76, 84, 102 |
| lash | `#14161C` | 20, 22, 28 |
| brow | `#1E222B` | 30, 34, 43 |
| eye | `#FF2A1A` | 255, 42, 26 |
| eye_dark | `#5A0805` | 90, 8, 5 |
| sclera | `#D9D2CC` | 217, 210, 204 |
| power_eye | `#FF5A3A` | 255, 90, 58 |
| armor | `#2E3A4E` | 46, 58, 78 |
| under | `#1A2130` | 26, 33, 48 |
| edge | `#8C9BB0` | 140, 155, 176 |
| green | `#39FF6A` | 57, 255, 106 |
| laser | `#39FF6A` | 57, 255, 106 |
| laser_core | `#F2FFF4` | 242, 255, 244 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Inner: ribbed under-suit | CHAR_MAX_UNDERSUIT | Ballistic ribbed weave | #1A2130; green lines #39FF6A | Skinned |
| Chest plate + lenses + abs | CHAR_MAX_CHEST_PLATE, CHAR_MAX_LENS_L, CHAR_MAX_LENS_R, CHAR_MAX_ABS, CHAR_MAX_COLLAR | Composite armour | #2E3A4E metal .75; lenses #39FF6A emission | Rigid |
| Pauldrons | CHAR_MAX_PAULDRON_L, CHAR_MAX_PAULDRON_R | Composite armour | #2E3A4E; green edge | Rigid |
| Gauntlets (laser emitters) | CHAR_MAX_GAUNTLET_L | Composite armour | #2E3A4E; green emitter strip | Rigid |
| Thigh + shin plates | CHAR_MAX_THIGH_L, CHAR_MAX_SHIN_L | Composite armour | #2E3A4E | Rigid |
| Armoured boots | CHAR_MAX_BOOT_L, CHAR_MAX_BOOT_R | Composite armour | #2E3A4E | Rigid |
| Belt | CHAR_MAX_BELT | Steel | #8C9BB0 metal | Rigid |

## Face

- **EYES:** Small deep-set red eyes #FF2A1A with constant glow
- **BROWS:** Massive brow ridge, thick low brows (permanent frown)
- **NOSE / LIPS:** Broad flat nose, thin grey lips
- **JAW / CHEEK:** Very wide square jaw, heavy cheekbones, thick neck
- **PROPORTIONS:** 7.6 heads; head small relative to the bulky body
- **HAIR:** Completely bald; blue-grey skin #6F7F93

Expressions (11): neutral, angry, evil, serious, confident, shocked, frustrated, suspicious, fear, furious, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_MAX_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 185.2 cm
- height total: 185.2 cm
- head height: 21.0 cm
- head-to-body ratio: 8.81 heads
- shoulder width: 62.3 cm
- chest width: 36.1 cm
- hip width: 33.8 cm
- leg length: 96.0 cm
- arm length: 79.3 cm
- hand length: 21.8 cm
- foot length: 23.8 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Laser | no effect | Charge orb + sparks at the palm, chest lenses glow | Perfectly straight beam: white core, coloured sheath and halo, impact burst | Beam thins to a fading thread, no impact |
| Laser (eyes) | no effect | Eyes flare, small charge points at both eyes | Two parallel straight beams from the eyes, impact burst | Beams thin to fading threads |

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
- `.blend`: `blend/max_v002.blend` (design), `blend/max_v003.blend` (game/export rig + controls), `blend/max_v004_rigify.blend` (Rigify animation rig — use this for animation)
- Exports: `export/max.glb` (10.11 MB), `export/max.fbx` (13.95 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Robes / skirts use a 12-chain follow rig (no stiff tube); a cloth simulation pass is still recommended for final shots.

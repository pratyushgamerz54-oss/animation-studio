# YAYAKI — Sub-villain 3 — Design Sheet v1 (PROPOSAL)

> **Status: awaiting Director approval.** Confirmed: name (Yayaki), role, powers (Teleportation) and the reference. Everything else is a proposal.

## Sheet pages (renders of the real Blender model)

- `YAYAKI_sheet_01_turnaround.png`
- `YAYAKI_sheet_02_poses_measurements.png`
- `YAYAKI_sheet_03_face.png`
- `YAYAKI_sheet_04_expressions.png`
- `YAYAKI_sheet_05_costume.png`
- `YAYAKI_sheet_06_palette.png`
- `YAYAKI_sheet_07_powers.png`

## Reference interpretation

Reference: `reference/yayaki_ref_01.png`

Taken: hooded purple-black armoured figure, glowing purple chest sigil, flame-like purple edges, long coat tails. Face shown under the hood (violet skin, glowing eyes) so expressions read.

## Identity (proposal)

- Age: NOT CONFIRMED
- Build: Lean and agile — narrow waist, long arms, light frame
- Silhouette: Pointed hood + layered flame-edged pauldrons + split coat tails = flickering spear-head

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#A58FB8` | 165, 143, 184 |
| skin_tint | `#9A6FB0` | 154, 111, 176 |
| lip | `#5E3F70` | 94, 63, 112 |
| lash | `#120A18` | 18, 10, 24 |
| brow | `#2A1838` | 42, 24, 56 |
| eye | `#C77DFF` | 199, 125, 255 |
| eye_dark | `#4A1A70` | 74, 26, 112 |
| sclera | `#20182A` | 32, 24, 42 |
| power_eye | `#E0B0FF` | 224, 176, 255 |
| suit | `#1B1624` | 27, 22, 36 |
| armor | `#2E2440` | 46, 36, 64 |
| hood | `#2A1F3A` | 42, 31, 58 |
| violet | `#A25BFF` | 162, 91, 255 |
| sigil | `#B57BFF` | 181, 123, 255 |
| teleport | `#B57BFF` | 181, 123, 255 |
| power_glow | `#C99BFF` | 201, 155, 255 |
| power_core | `#F6ECFF` | 246, 236, 255 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Inner: shadow suit | CHAR_YAYAKI_SUIT | Matte stretch weave | #1B1624; violet lines #A25BFF | Skinned |
| Hood + mantle | CHAR_YAYAKI_HOOD, CHAR_YAYAKI_MANTLE | Heavy brushed cloth | #2A1F3A; violet edge | Hood rigid on head; mantle skinned |
| Chest plate + sigil | CHAR_YAYAKI_CHEST_PLATE, CHAR_YAYAKI_SIGIL | Lacquered plate | #2E2440; sigil #B57BFF emission | Rigid |
| Flame-edged pauldrons | CHAR_YAYAKI_PAULDRON_L, CHAR_YAYAKI_PAULDRON_R, CHAR_YAYAKI_PAULDRON_L_SPIKES, CHAR_YAYAKI_PAULDRON_R_SPIKES | Lacquered plate | #2E2440; glowing edges | Rigid |
| Gauntlets | CHAR_YAYAKI_GAUNTLET_L | Plate | #2E2440 | Rigid |
| Split coat tails | CHAR_YAYAKI_COAT_TAILS | Silk-wool | #241B33; violet hem | Cloth sim (pinned at waist) |
| Boots | CHAR_YAYAKI_BOOT_L, CHAR_YAYAKI_BOOT_R | Soft armour | #2E2440 | Rigid |
| Belt | CHAR_YAYAKI_BELT | Plate | #2E2440 | Rigid |

## Face

- **EYES:** Violet iris #C77DFF glowing on a dark sclera; narrow, watchful
- **BROWS:** Thin dark-violet brows
- **NOSE / LIPS:** Fine straight nose, dark violet lips
- **JAW / CHEEK:** Narrow jaw, sharp high cheekbones
- **EARS:** Pointed ears (hidden by the hood in most shots)
- **HOOD:** Deep pointed hood with violet edge light; no visible hair

Expressions (11): neutral, angry, evil, serious, confident, shocked, frustrated, suspicious, fear, furious, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_YAYAKI_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 180.8 cm
- height total: 187.1 cm
- head height: 21.9 cm
- head-to-body ratio: 8.25 heads
- shoulder width: 55.2 cm
- chest width: 34.7 cm
- hip width: 31.2 cm
- leg length: 93.0 cm
- arm length: 76.8 cm
- hand length: 21.1 cm
- foot length: 22.8 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Teleportation | no effect | Body-hugging light rings + spatial warp bubble | DEPARTURE: body breaks into glowing motes inside the rings | ARRIVAL: motes reassemble the body with a ground ring |

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
- `.blend`: `blend/yayaki_v002.blend` (design), `blend/yayaki_v003.blend` (production rig + controls)
- Exports: `export/yayaki.glb` (11.17 MB), `export/yayaki.fbx` (15.94 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Jaw opens through mouth shape keys; the chin does not move.
- Cloth simulation is specified but not simulated yet.

# SAITHAN — Main villain — Design Sheet v1 (APPROVED 20 Nov)

> **Status: design APPROVED by the Director (20 Nov).** Confirmed: name (Saithan), role, powers (Dark Magic, Invisibility, Super Speed, Fire, Magical Portal, Lightning), the reference and the full design.

## Sheet pages (renders of the real Blender model)

- `SAITHAN_sheet_01_turnaround.png`
- `SAITHAN_sheet_02_poses_measurements.png`
- `SAITHAN_sheet_03_face.png`
- `SAITHAN_sheet_04_expressions.png`
- `SAITHAN_sheet_05_costume.png`
- `SAITHAN_sheet_06_palette.png`
- `SAITHAN_sheet_07_powers.png`
- `SAITHAN_sheet_08_borrowed_power_cost.png`

## Reference interpretation

Reference: `reference/saithan_ref_01.png`

Taken: horns, black spiked armour, glowing blue chest core, red eyes, tattered tabard, storm lightning. Face left visible (not a helmet) so he can act; own horn shape and armour layout.

## Identity (proposal)

- Age: NOT CONFIRMED (appears ~40)
- Build: Towering, heavily muscled — very broad shoulders and chest, thick arms
- Silhouette: Swept-back horns + spiked pauldrons + tattered tabard = jagged inverted triangle

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#5E6470` | 94, 100, 112 |
| skin_tint | `#6E5A66` | 110, 90, 102 |
| lip | `#3E3540` | 62, 53, 64 |
| lash | `#0A0809` | 10, 8, 9 |
| hair | `#0C0B0E` | 12, 11, 14 |
| brow | `#0C0B0E` | 12, 11, 14 |
| eye | `#E0221A` | 224, 34, 26 |
| eye_dark | `#5A0805` | 90, 8, 5 |
| sclera | `#2A1E20` | 42, 30, 32 |
| power_eye | `#FF3A1F` | 255, 58, 31 |
| armor | `#23262E` | 35, 38, 46 |
| armor_edge | `#5B6070` | 91, 96, 112 |
| cloth | `#15171C` | 21, 23, 28 |
| horn | `#2A2426` | 42, 36, 38 |
| core | `#3D7BFF` | 61, 123, 255 |
| power_glow | `#7FB0FF` | 127, 176, 255 |
| power_core | `#EEF4FF` | 238, 244, 255 |
| fire_core | `#FFD08A` | 255, 208, 138 |
| fire_mid | `#FF4A1A` | 255, 74, 26 |
| fire_outer | `#3A0505` | 58, 5, 5 |
| dark_core | `#B06BFF` | 176, 107, 255 |
| dark_mid | `#4A0F7A` | 74, 15, 122 |
| dark_outer | `#050208` | 5, 2, 8 |
| portal_rim | `#FF2A2A` | 255, 42, 42 |
| portal_deep | `#0A0000` | 10, 0, 0 |
| speed_trail | `#FF3B3B` | 255, 59, 59 |
| cost | `#FF3B1F` | 255, 59, 31 |
| cost_ash | `#77737A` | 119, 115, 122 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Inner: dark under-armour | CHAR_SAITHAN_SUIT | Padded leather-weave | #15171C rough .6 | Skinned |
| Outer: spiked plate armour | CHAR_SAITHAN_CHEST_PLATE, CHAR_SAITHAN_PAULDRON_L, CHAR_SAITHAN_PAULDRON_R, CHAR_SAITHAN_PAULDRON_L_SPIKES, CHAR_SAITHAN_PAULDRON_R_SPIKES, CHAR_SAITHAN_COLLAR, CHAR_SAITHAN_COLLAR_SPIKES | Blackened steel plates | #23262E metal .7; glowing seams #3D7BFF | Rigid |
| Gauntlets + greaves | CHAR_SAITHAN_GAUNTLET_L, CHAR_SAITHAN_GAUNTLET_L_SPIKES, CHAR_SAITHAN_GREAVE_L | Blackened steel | #23262E; spikes #3B3F49 | Rigid |
| Special: chest core | CHAR_SAITHAN_CHEST_CORE | Energy crystal | #3D7BFF emission (dims with life cost) | Rigid |
| Tabard + tattered cape | CHAR_SAITHAN_TABARD, CHAR_SAITHAN_CAPE | Heavy torn wool | #15171C, burnt edges #3A0D0D | Cloth sim (pinned) |
| Shoes: armoured sabatons | CHAR_SAITHAN_BOOT_L, CHAR_SAITHAN_BOOT_R | Steel plate | #23262E | Rigid |
| Belt | CHAR_SAITHAN_BELT | Plate belt | #23262E | Rigid |
| Horns + hair | CHAR_SAITHAN_HORN_0_L, CHAR_SAITHAN_HORN_0_R, CHAR_SAITHAN_HAIR, CHAR_SAITHAN_HAIR_CAP | Ridged horn / slick hair | horn #2A2426 bumpy; hair #0C0B0E | Rigid |

## Face

- **EYES:** Blood-red iris #E0221A with permanent low glow; dark sclera #2A1E20
- **BROWS:** Heavy brow ridge, thick angled brows (default scowl)
- **NOSE / LIPS:** Narrow nose, thin dark lips #3E3540
- **JAW / CHEEK:** Massive square jaw, sharp hollow cheekbones
- **EARS / HORNS:** Pointed ears; two ridged horns from the temples sweeping up and back
- **HAIR:** Short black hair slicked straight back between the horns

Expressions (11): neutral, evil, angry, furious, confident, serious, manipulative, shocked, pain, concentration, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_SAITHAN_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 192.7 cm
- height total: 206.8 cm
- head height: 22.4 cm
- head-to-body ratio: 8.61 heads
- shoulder width: 63.0 cm
- chest width: 37.7 cm
- hip width: 35.3 cm
- leg length: 99.6 cm
- arm length: 82.2 cm
- hand length: 22.6 cm
- foot length: 24.6 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Dark Magic | no effect | Violet-black wisps rise from both hands | Dense dark aura over the body, dark orb with crackle between the hands | Thin residual wisps |
| Invisibility | no effect | Noise dissolve begins (35 % of the body turns to refractive glass) | Fully refractive body (IOR 1.03) with faint fresnel rim = distortion only | Reappears through the same dissolve (70 %) |
| Super Speed | no effect | Eyes glow, bracer/core brighten, short trails at the legs, sparks at the feet | Long horizontal streaks from every limb + 2 tinted afterimages + crackle | Trails shrink, eyes fade |
| Fire | no effect | Flames lick from the fingertips | Fireball with flame tail from the palm + full-body fire aura | Small embers on three fingers |
| Magical Portal (corrupted) | no effect | Small reverse-swirl portal, rune ring | Blood-red rim, black core, reverse swirl, smoke tongues around the rim | Shrinks and dims |
| Lightning | no effect | Small arcs crawl over the hand | Branching bolt from the palm + arcs along the arms and body | Residual sparks at the fingertips |

Eye transformation: iris emission ramps normal → activation → full (shared by all powers).
Reusable VFX functions live in `../../_shared/vfxkit.py` (intensity / openness / length parameters).

## Borrowed-power life cost (story mechanic) — APPROVED: all three are used (Director 20 Nov)

- **A · Fracture veins:** glowing red cracks spread across the skin; more borrowing = more cracks.
- **B · Ash drain:** skin greys to ash and the eyes dim while a borrowed power runs.
- **C · Core siphon:** energy is visibly pulled out of his chest core; the core dims and flickers.
- **A + B + C · Full cost:** all three together (rendered on sheet page 8).

Proposed escalation (to confirm when scripting scenes): small borrow = C, longer = C + A, heavy = + B, extreme = all three.

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
- `.blend`: `blend/saithan_v002.blend` (design), `blend/saithan_v003.blend` (game/export rig + controls), `blend/saithan_v004_rigify.blend` (Rigify animation rig — use this for animation)
- Exports: `export/saithan.glb` (12.23 MB), `export/saithan.fbx` (20.15 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Robes / skirts use a 12-chain follow rig (no stiff tube); a cloth simulation pass is still recommended for final shots.

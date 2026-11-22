# SOUL — Sub-villain 1 — Design Sheet v1 (APPROVED 20 Nov)

> **Status: design APPROVED by the Director (20 Nov).** Confirmed: name (Soul), role, powers (Lightning), the reference and the full design.

## Sheet pages (renders of the real Blender model)

- `SOUL_sheet_01_turnaround.png`
- `SOUL_sheet_02_poses_measurements.png`
- `SOUL_sheet_03_face.png`
- `SOUL_sheet_04_expressions.png`
- `SOUL_sheet_05_costume.png`
- `SOUL_sheet_06_palette.png`
- `SOUL_sheet_07_powers.png`

## Reference interpretation

Reference: `reference/soul_ref_01.png`

Taken: tall gaunt pale-lavender figure, twin red horns, ornate black-gold high collar, bare sinewy torso, ornate belt, long dark robe with red-brown hem, back cape, bare feet. NOT taken: the curved blade (weapon not confirmed).

## Identity (proposal)

- Age: NOT CONFIRMED
- Build: Tall, gaunt and sinewy — long limbs, narrow waist, ribbed torso
- Silhouette: Twin vertical horns + flared high collar + floor-length robe = tall narrow spire

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#9C88A6` | 156, 136, 166 |
| skin_tint | `#8A6A92` | 138, 106, 146 |
| lip | `#6E4F68` | 110, 79, 104 |
| lash | `#1A1018` | 26, 16, 24 |
| brow | `#3A2A36` | 58, 42, 54 |
| eye | `#C23B2E` | 194, 59, 46 |
| eye_dark | `#4A0E0A` | 74, 14, 10 |
| sclera | `#E6DCD6` | 230, 220, 214 |
| power_eye | `#FF4A3A` | 255, 74, 58 |
| horn | `#8E1E1E` | 142, 30, 30 |
| power_glow | `#FF3B3B` | 255, 59, 59 |
| power_core | `#FFE6E6` | 255, 230, 230 |
| robe | `#16141A` | 22, 20, 26 |
| hem | `#7A2A1E` | 122, 42, 30 |
| gold | `#C9A24A` | 201, 162, 74 |
| cape | `#2A0F12` | 42, 15, 18 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Ornate chest yoke | CHAR_SOUL_YOKE | Lacquered leather + gold leaf | #1B1A1F; filigree #C9A24A | Rigid |
| High flared collar | CHAR_SOUL_HIGH_COLLAR | Gilded plate | black + gold edge | Rigid (head clearance checked) |
| Ornate belt | CHAR_SOUL_BELT | Gold-trimmed plate | #C9A24A | Rigid |
| Main: floor-length robe | CHAR_SOUL_ROBE | Heavy silk-wool | #16141A; hem gradient #7A2A1E | Cloth sim (pinned at waist) |
| Back cape | CHAR_SOUL_CAPE | Velvet | #2A0F12; gold edge | Cloth sim (pinned at shoulders) |
| Wrist bands | CHAR_SOUL_WRIST_BAND_L | Gold | #C9A24A metal | Rigid |
| Horns | CHAR_SOUL_HORN_0_L, CHAR_SOUL_HORN_0_R | Lacquered horn | #8E1E1E | Rigid |

## Face

- **EYES:** Deep red iris #C23B2E with a faint glow; narrow, heavy-lidded
- **BROWS:** Thin, sparse, sharply angled
- **NOSE / LIPS:** Long narrow nose; thin lavender-grey lips
- **JAW / CHEEK:** Very hollow cheeks, prominent cheekbones, long pointed chin
- **EARS / HORNS:** Pointed ears; two blood-red horns rising straight up from the crown
- **HAIR:** Bald, smooth pale-lavender skin

Expressions (11): neutral, angry, evil, serious, confident, shocked, frustrated, suspicious, fear, furious, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_SOUL_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 187.3 cm
- height total: 211.1 cm
- head height: 21.3 cm
- head-to-body ratio: 8.78 heads
- shoulder width: 56.4 cm
- chest width: 36.8 cm
- hip width: 33.2 cm
- leg length: 97.1 cm
- arm length: 80.1 cm
- hand length: 22.1 cm
- foot length: 23.7 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Lightning | no effect | Small arcs crawl over the hand | Branching bolt from the palm + arcs along the arms and body | Residual sparks at the fingertips |

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
- `.blend`: `blend/soul_v002.blend` (design), `blend/soul_v003.blend` (game/export rig + controls), `blend/soul_v004_rigify.blend` (Rigify animation rig — use this for animation)
- Exports: `export/soul.glb` (6.74 MB), `export/soul.fbx` (9.99 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Robes / skirts use a 12-chain follow rig (no stiff tube); a cloth simulation pass is still recommended for final shots.

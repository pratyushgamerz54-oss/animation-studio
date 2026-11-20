# RAMARAT — Headmaster — Design Sheet v1 (PROPOSAL)

> **Status: awaiting Director approval.** Confirmed: name (Ramarat), role, powers (Fire, Magical Portal, Super Speed, Lightning, Dark Magic, Invisibility, Laser, Teleportation, Unlimited (every power in the story)) and the reference. Everything else is a proposal.

## Sheet pages (renders of the real Blender model)

- `RAMARAT_sheet_01_turnaround.png`
- `RAMARAT_sheet_02_poses_measurements.png`
- `RAMARAT_sheet_03_face.png`
- `RAMARAT_sheet_04_expressions.png`
- `RAMARAT_sheet_05_costume.png`
- `RAMARAT_sheet_06_palette.png`
- `RAMARAT_sheet_07_powers.png`

## Reference interpretation

Reference: `reference/ramarat_ref_01.png`

Taken: elderly man, long white hair swept back, long white beard, royal-blue robe with silver/gold embroidery bands, shoulder mantle, red sash with hanging tail, grey-blue trousers, bare feet.

## Identity (proposal)

- Age: NOT CONFIRMED (appears ~70)
- Build: Tall, lean elderly frame; upright, slightly soft middle
- Silhouette: Long beard + swept white hair + broad mantle + floor-length robe = calm tall column

## Colour palette (same values drive the 3D materials)

| Name | HEX | RGB |
|---|---|---|
| skin | `#C9A38A` | 201, 163, 138 |
| skin_tint | `#C07A6A` | 192, 122, 106 |
| lip | `#9A6A5C` | 154, 106, 92 |
| hair | `#E6E4DF` | 230, 228, 223 |
| hair_tip | `#F5F4F0` | 245, 244, 240 |
| brow | `#E8E6E1` | 232, 230, 225 |
| eye | `#5D7A92` | 93, 122, 146 |
| eye_dark | `#25384A` | 37, 56, 74 |
| power_eye | `#FFE7A3` | 255, 231, 163 |
| power_glow | `#FFE7A3` | 255, 231, 163 |
| power_core | `#FFFFFF` | 255, 255, 255 |
| speed_trail | `#FFD36B` | 255, 211, 107 |
| fire_core | `#FFF6D0` | 255, 246, 208 |
| fire_mid | `#FFB23F` | 255, 178, 63 |
| fire_outer | `#C2410C` | 194, 65, 12 |
| portal_rim | `#FFE7A3` | 255, 231, 163 |
| portal_deep | `#1E2A6E` | 30, 42, 110 |
| dark_core | `#FFE7A3` | 255, 231, 163 |
| dark_mid | `#3B2A8A` | 59, 42, 138 |
| dark_outer | `#0A0820` | 10, 8, 32 |
| laser | `#FFD36B` | 255, 211, 107 |
| laser_core | `#FFFFFF` | 255, 255, 255 |
| teleport | `#FFE7A3` | 255, 231, 163 |
| robe | `#1C3590` | 28, 53, 144 |
| trim | `#C9CED6` | 201, 206, 214 |
| gold | `#C9A24A` | 201, 162, 74 |
| sash | `#B3202A` | 179, 32, 42 |
| trousers | `#7E8AA6` | 126, 138, 166 |
| inner | `#D6D8DC` | 214, 216, 220 |

## Costume & accessories breakdown

| Item | Parts (objects) | Fabric | Material | Simulation |
|---|---|---|---|---|
| Outer: royal-blue robe | CHAR_RAMARAT_ROBE_UPPER, CHAR_RAMARAT_ROBE_SKIRT | Heavy brocade | #2346B8; silver embroidery #C9CED6 | Skirt: cloth sim (pinned at waist) |
| Shoulder mantle | CHAR_RAMARAT_MANTLE | Brocade + gold band | #2346B8; gold #C9A24A | Skinned |
| Inner: white sleeves | CHAR_RAMARAT_INNER_SLEEVE | Linen | #D6D8DC | Skinned |
| Red sash + tail | CHAR_RAMARAT_SASH, CHAR_RAMARAT_SASH_TAIL | Silk | #B3202A | Tail: cloth sim |
| Trousers | CHAR_RAMARAT_TROUSERS | Wool | #7E8AA6 | Skinned |
| Hair + beard | CHAR_RAMARAT_HAIR, CHAR_RAMARAT_HAIR_CAP, CHAR_RAMARAT_BEARD | Stylised clumps | white #E6E4DF | Optional spring bones |

## Face

- **EYES:** Grey-blue iris #5D7A92; calm, slightly hooded with crow's-feet
- **BROWS:** Thick bushy white brows
- **NOSE / LIPS:** Long strong nose; thin lips mostly framed by moustache
- **JAW / CHEEK:** Lean aged face, defined cheekbones, soft jowls (age = 1.0 sculpt pass)
- **BEARD:** Long white beard to mid-chest + moustache; mouth kept clear for lip-sync
- **HAIR:** Long white hair swept straight back past the shoulders

Expressions (11): neutral, wise, serious, angry, disappointed, suspicious, concerned, confident, shocked, furious, blink
Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_RAMARAT_MOUTH)

## Body proportions (measured on the model, `qc/measurements.json`)

- height no hair: 177.1 cm
- height total: 178.2 cm
- head height: 21.8 cm
- head-to-body ratio: 8.14 heads
- shoulder width: 50.9 cm
- chest width: 33.4 cm
- hip width: 31.9 cm
- leg length: 90.9 cm
- arm length: 75.1 cm
- hand length: 20.7 cm
- foot length: 22.2 cm

## Powers

| Power | Normal | Activation | Full | Deactivation |
|---|---|---|---|---|
| Fire | no effect | Flames lick from the fingertips | Fireball with flame tail from the palm + full-body fire aura | Small embers on three fingers |
| Magical Portal | no effect | Portal opens at 25 % in front of the palm, rune ring on the hand | Full swirl disc, white-hot rim, spark ring, portal light | Portal shrinks to 35 % and dims |
| Super Speed | no effect | Eyes glow, bracer/core brighten, short trails at the legs, sparks at the feet | Long horizontal streaks from every limb + 2 tinted afterimages + crackle | Trails shrink, eyes fade |
| Lightning | no effect | Small arcs crawl over the hand | Branching bolt from the palm + arcs along the arms and body | Residual sparks at the fingertips |
| Dark Magic | no effect | Violet-black wisps rise from both hands | Dense dark aura over the body, dark orb with crackle between the hands | Thin residual wisps |
| Invisibility | no effect | Noise dissolve begins (35 % of the body turns to refractive glass) | Fully refractive body (IOR 1.03) with faint fresnel rim = distortion only | Reappears through the same dissolve (70 %) |
| Laser | no effect | Charge orb + sparks at the palm, chest lenses glow | Perfectly straight beam: white core, coloured sheath and halo, impact burst | Beam thins to a fading thread, no impact |
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
- `.blend`: `blend/ramarat_v002.blend` (design), `blend/ramarat_v003.blend` (production rig + controls)
- Exports: `export/ramarat.glb` (11.14 MB), `export/ramarat.fbx` (19.59 MB)

## Known limitations

- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.
- Jaw opens through mouth shape keys; the chin does not move.
- Cloth simulation is specified but not simulated yet.

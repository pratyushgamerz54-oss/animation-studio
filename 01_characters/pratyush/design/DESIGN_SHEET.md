# PRATYUSH — Hero 2 — Design Sheet v1 (PROPOSAL)

> **Status: awaiting Director approval.** Confirmed by Director: name, role (Hero 2 / main second lead),
> powers (Super Speed, Magical Portal, Lightning) and the reference image `reference/pratyush_ref_01.png`.
> Everything else (age, skin tone, hair, costume, colours) is a **proposal** (inventory U-04).

Sheet pages (3D renders of the real Blender model `blend/pratyush_v001.blend`):

| Page | File |
|---|---|
| 1 Turnaround: front, 3/4 front, right, 3/4 back, back, left | `PRATYUSH_sheet_01_turnaround.png` |
| 2 T-pose, A-pose, neutral + measurement guide | `PRATYUSH_sheet_02_poses_measurements.png` |
| 3 Face front/3/4/side, hairstyle back, eye detail | `PRATYUSH_sheet_03_face.png` |
| 4 Ten expressions + blink | `PRATYUSH_sheet_04_expressions.png` |
| 5 Costume & accessories breakdown | `PRATYUSH_sheet_05_costume.png` |
| 6 Colour palette (HEX + RGB) | `PRATYUSH_sheet_06_palette.png` |
| 7 Powers: normal → activation → full → deactivation, hand FX, eyes | `PRATYUSH_sheet_07_powers.png` |

## 1. Reference interpretation
Taken from the reference: sleek **armoured full-body speed suit**, full gloves, armoured boots,
**crackling lightning hugging the body**, sprint pose, athletic build.
Deliberately **changed to stay original**: colours (navy / electric blue instead of red / gold),
emblem (an upward "speed chevron" with a lightning notch — not a bolt-in-circle), **no cowl / mask /
ear wings**, face fully visible for acting, own spiky hairstyle with a blue streak.

## 2. Identity (proposal)
- Age: 17 (proposed) · Height 175 cm (without hair) · 7.5 heads
- Build: Lean athletic sprinter build — long legs, narrow waist, defined shoulders
- Silhouette: Sharp upward-swept hair spikes + high collar + angular shoulder plates = forward-leaning "arrow"

## 3. Colour palette (single source: `pratyush_spec.py` → same values drive the materials)
| Name | HEX | RGB |
|---|---|---|
| skin | `#B07650` | 176, 118, 80 |
| lip | `#8E5141` | 142, 81, 65 |
| hair | `#17120F` | 23, 18, 15 |
| hair_streak | `#2EA8FF` | 46, 168, 255 |
| eye | `#5A361F` | 90, 54, 31 |
| eye_dark | `#2A170C` | 42, 23, 12 |
| suit | `#16243F` | 22, 36, 63 |
| armor | `#5C6B80` | 92, 107, 128 |
| boot | `#1E2C4A` | 30, 44, 74 |
| accent | `#2EA8FF` | 46, 168, 255 |
| under | `#262931` | 38, 41, 49 |
| shoe_sole | `#2EA8FF` | 46, 168, 255 |
| glove | `#141519` | 20, 21, 25 |
| belt | `#1D1E23` | 29, 30, 35 |
| metal | `#B7C0CC` | 183, 192, 204 |
| power_glow | `#4FD8FF` | 79, 216, 255 |
| power_core | `#F2FBFF` | 242, 251, 255 |
| power_eye | `#5BE0FF` | 91, 224, 255 |
| portal_rim | `#6FE7FF` | 111, 231, 255 |
| portal_deep | `#0A2A5A` | 10, 42, 90 |
| speed_trail | `#2EA8FF` | 46, 168, 255 |

## 4. Costume breakdown
| Layer | Item | Material / fabric | Cloth simulation |
|---|---|---|---|
| Main | Armoured speed suit (full body, wrist→ankle) | 4-way stretch technical knit, navy, emissive electric-blue piping (arms, sides, legs, chest V) | None — skin-tight, skinned to rig; corrective shapes at elbows/knees |
| Inner | Under-layer | charcoal `#262931` (reserved for side panels in v2) | None |
| Outer | Chest plate, 2 pauldrons, 2 knee guards, high collar | moulded composite, gunmetal-blue metallic 0.65, glowing edge | Rigid |
| Shoes | Armoured sprint boots (to mid-calf) | synthetic leather `#1E2C4A`, electric-blue sole & bands | Rigid |
| Gloves | Full-finger grip gloves | `#141519` synthetic | Skinned per finger |
| Belt | Plate belt + silver buckle | gunmetal + brushed silver | Rigid |
| Ornament | Chest emblem: speed chevron | emissive `#4FD8FF` | Rigid |
| Special equipment | 2 speed bracers with energy cores | brushed silver + emissive core | Rigid |

## 5. Body proportions
Spec vs. **measured on the model** (`qc/measurements.json`) is printed on sheet page 2.
Height 175 cm spec / 174.4 cm measured · head 23.1 cm · 7.54 heads · shoulders 51.5 cm (outer deltoids) ·
chest 32.8 cm · hips 31.3 cm · arm 73.8 cm · leg 89.4 cm · hand 19 cm · foot 26 cm.

## 6. Power activation design (confirmed powers only)
| | Super Speed | Lightning | Magical Portal |
|---|---|---|---|
| Normal | No glow; bracer cores dim | same | same |
| Activation | Eyes glow 3, cores brighten, short trails at legs, sparks at feet | Small arcs crawl over the hand | Portal opens at 25 %, rune ring at palm |
| Eyes | Iris → `#5BE0FF` glow | same, strongest | same |
| Body energy | Speed trails from limbs (`#2EA8FF`) | Arcs along arms + body aura (`#4FD8FF` glow, `#F2FBFF` core) | Hair streak + cores glow |
| Hand / fingers | Streaks off forearm & hand | Arcs jump finger-to-finger, palm discharge | Double rune ring in front of palm |
| Aura | Sparks along trail anchors | Crackling arcs over body | Light from portal rim |
| Trails | Long horizontal trails + 2 afterimages | — | Spark ring around rim |
| Intensity | activation → full → deactivation all parameterised | bolt radius/branches/glow | openness 0–1, intensity 0–1 |
| Deactivation | Trails shrink, eyes fade to 1.2 | Residual sparks at fingertips | Portal shrinks to 35 % and dims |

Keeping powers distinct: **speed = long horizontal streaks**, **lightning = jagged white-blue branching arcs**,
**portal = round swirling disc with white rim**.
VFX are reusable functions in `../_shared/vfxkit.py` (`speed_trails`, `lightning`, `aura_arcs`, `portal`,
`rune_ring`), each with timing/intensity parameters.

## 7. Technical 3D specification
- **Topology:** body built as an all-quad cage (Skin modifier, then subdivided) with ring edge loops
  around every limb and joint; anatomy added by a code "sculpt" pass. Head = all-quad sphere-derived mesh.
  Render-time Subdivision Surface level 2.
- **Edge loops:** rings at shoulder, elbow, wrist, each finger knuckle, hip, knee, ankle (from the joint skeleton).
- **Facial topology (v1):** modular stylised face kit — eyeball spheres, upper/lower lid shells, brow strips,
  mouth (interior + upper/lower lip grids) projected onto the head surface.
- **Hands:** 5 fingers, 3 segments each, thumb from the wrist.
- **Hair:** 100+ flattened tapered ribbon clumps + scalp cap (real geometry).
- **Clothing:** separate meshes derived from the body surface (offset + solidify), so they fit exactly.
- **Rig (v1 pose rig):** 53 deform bones — root, pelvis, 3 spine, neck, head, clavicles, arms, hands,
  15 finger bones per hand, legs, feet, toes. Automatic heat weights on the body; clothing inherits the same weights.
- **Facial blendshapes:** mouth & brows have shape keys for 10 expressions + **10 phonemes
  (A, E, I, O, U, M/B/P, F/V, L, W, Rest)** already built; lids/eyes driven by rotation.
- **Materials:** Principled PBR (skin with subsurface, cloth with sheen, metal, emissive energy).

## 8. Production status — honest
| Deliverable | Status |
|---|---|
| Design sheet v1 (7 pages) | ✅ rendered from the real model — **awaiting approval** |
| `.blend` with body, head, face kit, hair, clothing, accessories | ✅ exists, rebuilds from `build_pratyush.py` |
| Pose rig + auto weights, T/A/neutral/dash/cast poses | ✅ works (used for the sheet) |
| Expression + phoneme shape keys | ✅ built (lip-sync test not run yet) |
| VFX references for 3 powers | ✅ rendered |
| UV unwrap + baked texture maps | ⬜ not started (materials are procedural now) |
| Rigify production rig with IK/FK, poles, controls | ⬜ not started (Stage 6) |
| Real jaw/cheek facial deformation | ⬜ v1 mouth opens without moving the jaw |
| Deformation tests (elbows, knees, fingers), run/jump/land tests | ⬜ not run |
| FBX/GLB export | ⬜ not started |

## 9. Known v1 limitations
- Face is stylised and simpler than the reference render; close-up realism needs a further sculpt pass.
- Mouth is a projected face-kit; the jaw does not open yet.
- Materials are procedural (no image textures yet); UVs come in Stage 5.

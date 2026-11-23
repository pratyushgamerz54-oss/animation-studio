# SAMBAR DEER (stag) — preview v002 · PROPOSED (pending Director approval)

*Rusa unicolor* · ORDINARY wildlife · region R-02 Enchanted Forest (also forest edge of R-01) · not a story character.

## How it was made (Director's "mix" decision, 23 Nov)
| Part | Source |
|---|---|
| Base body, skin weights, rig (37 bones: spine, neck, head, jaw, tongue, ears, eyelids, 4 legs, tail) and 53 real-motion clips | "Realistic Animated Elk 3D Model" by **WildMesh 3D**, **CC-BY-4.0** — https://sketchfab.com/3d-models/realistic-animated-elk-3d-model-787834f9caa2474d9f1814b807c072d7 (credit required in the film credits) |
| Sambar antlers (rusine, 3 tines per side, V-spread) | own procedural (`t7_anatomy.antlers_sambar`), bone-parented to the head |
| Sambar coat (uniform warm grey-brown, no elk rump patch, darker legs / mane) | own recolour of the base textures → `11_TEXTURES/sambar/T7_SAMBAR_*_diffuse_v002.png` |
| Size | withers 1.30 m (field guide: stag 1.02–1.60 m) |
| Ears ×1.25 | sambar ears are large and broad |
| Reference photos | `00_CREATURE_REFERENCES/photo_refs/sambar/` (Dr. Raju Kasambe, CC BY-SA 4.0) |

Files: `T7_SAMBAR_CC_v002.blend` (Blender 4.5), previews `preview_v002/` (3/4, side, front, back, face, walk clip `sambar_walk_v002.mp4`,
board `T7_SAMBAR_PREVIEW_v002.jpg`). Build script: `scripts/t7_sambar_cc.py` (base untouched in `00_CREATURE_REFERENCES/cc_models/`).

## Real behaviour available from the base (for milestone 2 animation tests)
Walk, WalkSlow, Trot, Run, Sprint (+ L / R curves), turn L / R, stand / lying / sitting breathing, eating (standing), all transitions
(stand ↔ lie ↔ sit, stand → walk / trot / run / sprint), jump, hit / death clips (not used without approval).
Walk = 24 frames @ 24 fps (1 stride / s), 4-beat lateral sequence — matches real cervid walking.

## Known gaps (fix after approval, in production)
1. Close-ups: game-resolution mesh (facets on jaw / nose) → subdivision + displacement from the normal map, LOD0 for close shots.
2. Nose leather should be black (recolour made it brown) → paint mask.
3. Real fur groom (own NG_T7_FUR system) for the shaggy neck mane + coat at close range; tail underside white.
4. Antler texture (velvet-free hard antler, pale tips) and terminal fork read; brow-tine length check vs more photos.
5. 4K texture pass (FINAL OUTPUT RULE).

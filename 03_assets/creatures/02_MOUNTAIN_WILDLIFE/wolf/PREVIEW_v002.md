# HIMALAYAN WOLF — preview v002 · PROPOSED (pending Director approval)

*Canis lupus chanco* · ORDINARY wildlife · region R-03 Mountain Kingdom (alpine meadows, high valleys) · not a story character.

## How it was made (mix pipeline)
| Part | Source |
|---|---|
| Base body, fur texture, rig (52 bones incl. 4-bone ears, 8-bone tail, IK leg bones + pole targets), idle clip | "Grey Wolf Rebuilt" by **kenchoo**, **CC-BY-4.0** — https://sketchfab.com/3d-models/grey-wolf-rebuilt-c0fd1738fa31413b906e2914f5a332b9 (credit required) |
| Himalayan-wolf coat (tawny flanks, dark grizzled saddle kept from the base pattern, cream belly / legs / muzzle) | own TINT recolour from photo ref 01 → `11_TEXTURES/wolf/` |
| Size | withers 0.72 m (field guide 0.65–0.76 m) |
| Photo reference | `00_CREATURE_REFERENCES/photo_refs/wolf/` (Zoo Zurich, Wikimedia Commons) |

Files: `T7_WOLF_CC_v002.blend` (Blender 4.5) · `preview_v002/` (3/4, side, front, back, face, idle clip `wolf_idle_v002.mp4`, board).
Scripts: `scripts/t7_cc_species.py` (config `wolf`), `scripts/t7_preview_rig.py`.

## Behaviour
Base clip = standing idle (looks around, lowers the head to sniff) — 272 frames @ 24 fps.
**Walk / trot / run / sit / lie are NOT in this base** → milestone 2: authored on this rig with real wolf gait data (walk 4-beat;
trot = main travel gait, diagonal pairs, ≈ 1.5–2 strides / s, hind paw lands in the front print; gallop), IK feet planted on the
ground, weight shift + follow-through in neck / tail, frame-by-frame check.

## Known gaps (production)
1. Head / neck a bit more tawny than the photo (photo: grey-brown grizzled ruff) → region-aware texture pass.
2. Thick neck ruff + guard hairs → own fur groom (NG_T7_FUR) over the base for close-ups.
3. Eyes: amber iris check vs photo; 4K textures (FINAL OUTPUT RULE).

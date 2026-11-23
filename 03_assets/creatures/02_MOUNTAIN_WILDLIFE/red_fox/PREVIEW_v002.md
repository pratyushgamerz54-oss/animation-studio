# RED FOX (Himalayan) — preview v002 · PROPOSED (pending Director approval)

*Vulpes vulpes montana* · ORDINARY wildlife · region R-03 Mountain Kingdom (alpine meadows, forest edge; also R-01) · not a story character.

| Part | Source |
|---|---|
| Base body, painted fur texture + fur cards, rig (40 bones: spine, neck, head, ears, 4 legs, 6-bone tail), real-behaviour clip "Waking Up" (493 frames: asleep → stretch → stands → steps / looks around → lies down) | "Fox" by **Alexei Ostapenko**, **CC-BY-4.0** — https://sketchfab.com/3d-models/fox-4e37c303f8a241aaa2511bd9f3019273 (credit required) |
| Size | withers 0.40 m (field guide 0.35–0.50 m) |
| Ground contact fix | the base floated 3.6–6.3 cm above the ground → smoothed per-frame ground snap on the root (contact ±0.5 cm) |
| Photos | `00_CREATURE_REFERENCES/photo_refs/red_fox/` (public domain ×2, MIKI Yoshihito CC BY 2.0) — coat / legs / tail tip match |

Known gaps (production): walk / trot / pounce authored on the rig (real gait data; foxes trot ≈ 2 strides/s, mouse-pounce jump), IK foot-lock
(replaces the ground snap; last lie-down frames −2 cm), Himalayan subspecies = thicker, slightly paler winter coat option, 4K, close-up fur groom.

## v003 — REAL FUR (Director 23 Nov: "skin plastic jaisa … realistic feel nahi")
Causes: metallic channel from the glTF metallicRoughness map (metal-like sheen), fur cards without alpha (solid shells), hair only painted.
Fix (`scripts/t7_furpass.py`): metallic 0, roughness .82, specular .2; card alpha from the texture; strand groom (own NG_T7_FUR on a
hair-Curves object, follows the deformed mesh, colour sampled from the base texture, length by bone region: body 3.4 cm, neck 4 cm,
tail 6.5 cm, legs 0.6–1.2 cm, short face / muzzle fur 0.35 cm, no hair on the darkest spots = nose / eyes). Also fixed in t7kit.fur():
groom density / length / radius compensated for scaled (cm-unit) bases. File: `T7_RED_FOX_CC_v003_fur.blend` (v002 kept).
**Same fur pass will be applied to sambar, wolf and bear (production fix list).**

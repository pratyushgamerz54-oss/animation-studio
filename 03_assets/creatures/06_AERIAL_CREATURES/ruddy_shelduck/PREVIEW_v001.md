# Ruddy shelduck (Tadorna ferruginea) — preview v001 (24 Nov) — Crystal Lakes (R-08)
- Base: CC0 museum-mount photogrammetry scan of a Common shelduck (Tadorna tadorna, same genus), darwinmuseum.ru (see BASE_LICENSE.md).
  Real feather geometry + real feather texture detail; pose = flight (wings spread) → good flying variant.
- `scripts/t7_bird_scan_cc.py`: stand / rod / mounting pins removed, faces +X, real length 64 cm (bill tip → tail),
  per-pixel recolour by 3D region (UV position map) keeping the scan's local feather detail:
  orange-chestnut body, buff head paler at the face, thin black collar (breeding male), black tail, black primaries,
  white wing coverts (scan), black bill 4.5 cm + black feet, dark-brown eyeballs (wet cornea). Matte feathers (rough .72, spec .25).
- Photo refs: `00_CREATURE_REFERENCES/photo_refs/ruddy_shelduck/` (ref 02 is an egg — ignore).
- Known gaps → production: swimming / standing pose (rig re-pose of the wings), underwing colours (white coverts underneath),
  feather barb fuzz pass, female variant (no collar, paler head), rig + flight / swim / walk cycles (behaviour baker).

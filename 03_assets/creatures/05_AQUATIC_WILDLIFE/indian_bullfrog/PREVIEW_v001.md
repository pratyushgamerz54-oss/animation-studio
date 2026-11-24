# Indian bullfrog (Hoplobatrachus tigerinus) — preview v001 (24 Nov) — Crystal Lakes (R-08)
- Base: CC0 specimen scan of an adult ♀ American bullfrog (Lithobates catesbeianus, same family Ranidae; Sketchfab 0850a4b8…).
  (The other CC0 "bullfrog" model 8816b476 is a TADPOLE — rejected, removed.)
- `t7_scan_reduce.py --join --ratio 0.25 --length 0.16 --delete-mat Material.001` (colour card removed; snout-vent ≈ 10 cm, total 16 cm)
  → `t7_frog_pass.py`: per-material per-pixel recolour keeping the scan's real skin (warts, blotches, leg bars): olive-brown back +
  limbs, thin pale-yellow mid-dorsal line, cream belly, olive head, golden iris + black pupil on the scan's own eyes (found as the darkest
  head texture spot per side), moist skin (rough .38 + thin coat, slight SSS); faces +X.
- POSE: the specimen lies with legs spread = exactly how a frog FLOATS / rests at the water surface (photo 04) → previewed floating in
  silty pond water (`t7_water_preview.py`: tan silt water, partial transmission + absorption, fine ripples). `side/34/...png` = dry view.
- Known gaps → production: sitting pose on land (needs the rig: hind legs folded under the body), rig + jump / swim kick / croak
  (vocal sacs), breeding-male yellow variant (photo 04), wet-skin highlights in close-ups.

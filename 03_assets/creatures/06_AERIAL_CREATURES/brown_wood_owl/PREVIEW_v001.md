# Brown wood owl (Strix leptogrammica) — preview v001 (24 Nov) — Enchanted Forest (R-02)
- Base: museum-mount photogrammetry of Pel's fishing owl (Strigidae; CC-BY, Sketchfab e96ea41e…) — perched upright, round head,
  no ear tufts = brown wood owl build. Rejected: Ural owl scan (broken jagged wings, blurry face, on a take-off stump),
  great grey + snowy owl pair (two birds on one base), barn owl (other family, heart face).
- `t7_scan_reduce.py --join --ratio 0.25 --height 0.60` → `t7_owl_pass.py`: museum board cut + loose remnants removed, natural branch
  perch kept; faces +X (head → its eyes); per-pixel recolour keeping the real feather detail: warm buff underparts, dark chocolate back /
  wings / crown, tawny facial disc, dark 'spectacle' rings + pale brows round the eyes; matte feathers. Owl ≈ 45 cm on a ~12 cm perch.
- Views: `t7_views.py` (front from +X, 3/4, side, back, face). The mount's head is turned relative to the body (natural owl pose).
- Known gaps → production: fine horizontal barring on the underparts (scan has Pel's spots), body facing the head direction (rig),
  rig + head turn / blink / take-off / silent flight, feather fuzz on the facial disc.

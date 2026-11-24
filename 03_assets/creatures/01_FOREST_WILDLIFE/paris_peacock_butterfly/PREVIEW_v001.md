# Paris peacock butterfly (Papilio paris) — preview v001 (24 Nov) — Enchanted Forest (R-02)
- Base: CC0 specimen model of Papilio bianor (common peacock, closest relative; Sketchfab 2558b40f…). Base material was UNLIT → relit.
- `t7_scan_reduce.py --join --ratio 0.5 --length 0.12 --delete-mat Material.001` (wingspan 12 cm) → `t7_feather_fuzz.py --surface chitin
  --no-fuzz` → `t7_butterfly_pass.py`: specimen (standing on its wing edge) laid into a basking pose (wings out, upper side up, head +X
  found from the legs), upper side velvet black + green scale dusting, soft iridescent blue-green hindwing patches, scale-glint sheen;
  underside kept (dark with orange-red lunules = P. paris underside).
- Views: `view_top / view_34 / view_under.png`.
- Known gaps → production: patch shape (irregular blue band toward the inner hindwing, photo 02), denser green speckle, faint forewing
  band, wings slightly V-raised (specimen) → flat basking + closed-wing perching via rig, wing-flap flight (≈ 8–10 Hz) + gliding,
  real iridescence shader (thin-film) for the scales.

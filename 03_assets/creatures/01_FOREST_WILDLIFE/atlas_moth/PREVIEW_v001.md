# Atlas moth (Attacus atlas) — preview v001 (24 Nov) — Enchanted Forest (R-02)
- Base: "Attacus Attlas" (CC-BY, Erina eka syaharani; Sketchfab 1f7d0337…) — the real species pattern (hooked 'snake-head' forewing
  tips, clear triangular windows, wavy bands, banded body); came with a wing-flap animation. Rejected: CC0 oak silkmoth (other pattern).
- `t7_scan_reduce.py --frame 12 --delete-obj Cube --join --length 0.25` (wings spread flat at frame 12; wingspan 25 cm) →
  `t7_butterfly_pass.py --orient-only` (basking, head +X) → `t7_moth_look.py` (deeper rust colour, velvet-matte scales + sheen) →
  `t7_feather_fuzz.py --bird-min-frac 0 --len 0.0018 --density 900000` (very short scale / hair fuzz — moths are fuzzy).
- Views: `view_top / view_34 / view_side / view_under.png`.
- Known gaps → production: translucent windows (alpha / transmission), hairier thorax + feathery antennae (male), body thickness,
  rig (slow heavy wing beats, resting with wings flat on bark; atlas moths do not feed — short adult life).

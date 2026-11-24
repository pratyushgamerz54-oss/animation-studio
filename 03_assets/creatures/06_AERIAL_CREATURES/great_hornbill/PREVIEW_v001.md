# Great hornbill (Buceros bicornis) — preview v001 (24 Nov) — Enchanted Forest (R-02)
- Base: "Great Hornbill – Perched" (CC-BY, Pigcraft, AI-assisted then cleaned; Sketchfab 4d240371…) — the only usable free model.
  NOT rigged (despite the title). Its scene.bin is 115 MB (> 95 MB git limit) → base kept OUT of git:
  re-download `python3 scripts/t7_sketchfab.py get 4d240371c7284ec1ae3d3a57b850021a great_hornbill` (licence copied here).
- `t7_scan_reduce.py --join --ratio 0.15 --length 1.10` → `t7_hornbill_pass.py` (faces +X by the bill tip; per-pixel recolour keeping
  the sculpted feather detail: black face / throat / breast / wings, cream neck, white belly + thighs, cream wing bar, white tail with a
  black band, grey legs; bill + casque keep the base's yellow-orange, waxy matte) → `t7_feather_fuzz.py --bird-min-frac 0 --len 0.005`.
- Known gaps → production: the AI base's feathers are chunky / sculpted (fuzz softens them; a proper feather-card groom or a better
  base when one exists), casque shape + black casque front, red eye (male) brighter, yellow staining on neck / wing bar (preen oil),
  rig + hop / flight (loud wing beats) / feeding on figs.

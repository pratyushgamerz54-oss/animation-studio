# 03_assets/vegetation — TASK 06 ecosystem vegetation library (Blender 4.5 LTS)

Design document: `02_world/ecosystem/ECOSYSTEM_BIBLE.md` · Director inputs (verbatim): `02_world/ecosystem/DIRECTOR_INPUTS_TASK06.md`

| Folder | What |
|---|---|
| `library/T6_VEG_<REGION>_v001.blend` | **hero assets** per region — AV ASHRAM_VALLEY · EF ENCHANTED_FOREST · MK MOUNTAIN_KINGDOM (milestone 1) · PL GREEN_PLAINS · LK CRYSTAL_LAKES · DS GOLDEN_DESERT · FB FORBIDDEN_LANDS · CT ANCIENT_CITY_SITES · CV HIDDEN_UNDERGROUND · ND NATURAL_DETAILS (milestone 2). Each species in its own collection `T6_<asset>` at the origin, wind modifier + `T6_WIND_CONTROL`, metadata custom props; `T6_LIB_<R>_SCATTER` = wind-free `<asset>_SC` copies (same mesh) for the ecosystem scatter; `*_inventory.json` = specs |
| `library/T6_VEG_<REGION>_VARIANTS_v001.blend` | seeds 1 + 2 of every species (seed 0 = hero) → 3 variants; giants stored at LOD1 density |
| `library/T6_VEG_<REGION>_LODS_v001.blend` | LOD1 / LOD2 (same skeleton, fewer sides + cards) + LOD3 impostor cards (trees / shrubs) · plants LOD1 |
| `textures/leaves/` | generated leaf / needle / flower / litter atlases (2K, 4 variants): `_col` (RGBA), `_nor`, `_rough`, `_prev`; `atlases.json` = card size in metres |
| `textures/impostors/` | LOD3 impostor renders (front + side, alpha) + `impostors.json` (metric framing) |
| bark | Poly Haven CC0 scans in `03_assets/external/polyhaven/textures/` (fetch: `python3 03_assets/external/polyhaven_fetch.py`) |
| `renders/<REGION>/` | sheet source renders (front / side / back / leaf / base; plants hero / detail; lineups) + `views.json` |
| `sheets/<REGION>/` | `TREE_*.png`, `PLANTS_<R>.png`, `REGION_<R>.png` (+ `thumbs/`); `sheets/T6_SHEET_M1.png` / `T6_SHEET_M2.png` = contact sheets |
| `qc/` | `T06_QC_REPORT.md` + json per Blender version + populated-file QC |
| `scripts/` | see below |

## Scripts (run from `03_assets/vegetation/scripts/`, `BPY45` = Blender 4.5 python, e.g. `$SCRATCH/bpy45/bin/python`)
```
python3 t6_leafgen.py [atlas …]                          # leaf atlases
BPY45 t6_build_library.py -- <R>                         # hero library (R = AV EF MK PL LK DS FB CT CV ND)
SPP=24 BPY45 t6_render_sheets.py -- <R> [asset …]        # sheet renders (SKIP_FRESH=1 resume · ONLY=lineup|closeups|plants)
python3 t6_compose_sheets.py <R …>                       # sheets
python3 t6_contact_sheet.py [M2]                         # contact sheet M1 / M2
BPY45 t6_render_impostors.py -- <R>                      # LOD3 impostor textures
BPY45 t6_build_lods.py -- <R>                            # VARIANTS + LODS files
BPY45 t6_qc.py && python3 t6_qc.py && python3 t6_qc.py --report     # library QC (4.5 + 5.3) + report
BPY45 t6_populate.py -- AV|EF|MK|DS|FB                   # populated region files (02_world/ecosystem/populated/)
RES=1280x720 SPP=32 BPY45 t6_render_populated.py -- <R>  # cinematic previews (02_world/ecosystem/renders/populated/)
BPY45 t6_pop_qc.py                                       # scatter QC of the populated files
SCRATCH=<dir> bash t6_finish_pending.sh                  # realism-v3 re-render chain (resumable)
SCRATCH=<dir> bash t6_m2_pending.sh                      # milestone-2 pipeline (resumable, step markers in ../.m2_steps/)
```
* `t6_species.py` / `t6_species_m2.py` — tree + shrub catalogues · `t6_plants.py` / `t6_plants_m2.py` — plant generators + catalogues
* `t6_details.py` — natural details (leaf / needle litter, fallen branches, giant log, ground ivy, floating leaves)
* `t6kit.py` — tree generator, materials (bark / leaf / herb leaf / petal / moss / simple + realism pass), wind node groups + control
* `t6kit_m2.py` — palm generator (date / coconut) · `t6_matlib.py` — material set per species · `t6_regions.py` — region table
* `t6_ecosystem.py` — **NG_T6_ECOSYSTEM** scatter (masks / slope / altitude / clusters / Poisson spacing / exclusion zones /
  camera culling / 4 LOD bands / near-realized per-vertex wind + far instance tilt with per-instance phase)

## Using an asset in a scene
`File ▸ Link/Append ▸ T6_VEG_….blend ▸ Collection ▸ T6_<asset>` (instance it), or scatter `<asset>_SC` with `NG_T6_ECOSYSTEM`
(see `t6_populate.py` for complete recipes). Wind: `T6_WIND_CONTROL` — rotate it for direction, change `strength` (0 calm … 6 storm),
`gust`, `speed`, `flutter` in its custom properties; or animate them.

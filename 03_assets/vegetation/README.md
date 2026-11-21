# 03_assets/vegetation — TASK 06 ecosystem vegetation library (Blender 4.5 LTS)

Design document: `02_world/ecosystem/ECOSYSTEM_BIBLE.md` · Wildlife proposal: `02_world/ecosystem/WILDLIFE_PROPOSAL.png`

| Folder | What |
|---|---|
| `library/T6_VEG_<REGION>_v001.blend` | **the assets** — ASHRAM_VALLEY (20), ENCHANTED_FOREST (12), MOUNTAIN_KINGDOM (10); each species in its own collection at the origin, wind modifier, metadata custom props; `*_inventory.json` = specs |
| `textures/leaves/` | 25 generated leaf / needle / flower atlases (2K, 4 variants): `_col` (RGBA), `_nor` (OpenGL), `_rough`, `_prev`; `atlases.json` = card size in metres |
| bark | Poly Haven CC0 scans in `03_assets/external/polyhaven/textures/` (fetch: `python3 03_assets/external/polyhaven_fetch.py`) |
| `renders/<REGION>/` | sheet source renders (front / side / back / leaf / base; plants hero / detail; lineups) + `views.json` |
| `sheets/<REGION>/` | `TREE_*.png`, `PLANTS_<R>.png`, `REGION_<R>.png` (+ `thumbs/`); `sheets/T6_SHEET_M1.png` = contact sheet |
| `qc/` | `T06_QC_REPORT.md` + json per Blender version |
| `scripts/` | see below |

## Scripts (run from `03_assets/vegetation/scripts/`, `BPY45` = Blender 4.5 python, e.g. `$SCRATCH/bpy45/bin/python`)
```
python3 t6_leafgen.py                       # leaf atlases (≈ 6 min)
BPY45 t6_build_library.py -- AV|EF|MK       # libraries (≈ 1 min each)
SPP=24 BPY45 t6_render_sheets.py -- AV|EF|MK [asset …]   # sheet renders (CPU Cycles, ≈ 30 s per view)
python3 t6_compose_sheets.py AV EF MK       # sheets
BPY45 t6_qc.py && python3 t6_qc.py --report # QC
SCR=<dir> BPY45 t6_wind_test.py             # wind test frames → ffmpeg → renders/WIND_TEST.mp4
python3 t6_wildlife_sheet.py
```
* `t6_species.py` — tree + shrub catalogue (parameters, labels, habitat, palette) · `t6_plants.py` — plant generators + catalogue
* `t6kit.py` — tree generator, materials (bark / leaf / herb leaf / petal / moss / simple), wind node group + control, `add_wind()`
* `t6_matlib.py` — material set per species

## Using an asset in a scene
`File ▸ Link/Append ▸ T6_VEG_….blend ▸ Collection ▸ T6_<asset>` (instance it, or use it in a scatter node).
Wind: keep `T6_WIND_CONTROL` (comes with the asset's drivers) — rotate it for direction, change `strength` (0 calm … 6 storm),
`gust`, `speed`, `flutter` in its custom properties; or animate them.
Variants: `build_tree(spec, seed=N)` makes a new variant of any species (milestone 2 will store 3–5 per species + LODs).

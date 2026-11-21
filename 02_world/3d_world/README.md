# TASK 04 — THE GRAND UNIVERSE · 3D WORLD BLOCKOUT (milestone 1)

> **Status: PROPOSAL / BLOCKOUT — built from world map v2 revision 01, which is NOT LOCKED.**
> Nothing here finalises geography, names or story. Change the map → run `scripts/run_all.sh` → every file is rebuilt.
> Built and tested with **Blender 4.5.16 LTS** (Python module), also opened/QC'd in Blender 5.3.

## What is in each folder

| Folder | File(s) | Contents |
|---|---|---|
| `00_MASTER_WORLD` | `WORLD_master_v001.blend` | **Open this.** Links every component (no geometry of its own). Scenes: `MAIN_WORLD`, `ASHRAM_VALLEY`, `DIM_BLACK_HOLE_TRAINING`, `DIM_SAITHAN_DARK_WORLD` |
| `01_GEOGRAPHY` | `WORLD_geography_v001.blend`, `WORLD_SCALE.md`, `data/` | settlement / ruin / cave / hidden / GEM / Ashram markers, labels, 1 000 km grid, unexplored edges, Ashram-valley extents; scale document; prepared map data |
| `02_TERRAIN` | `WORLD_terrain_v001.blend` | plains + hills, coasts + shelf, ice + tundra, ruined-region terrain (wasteland / forbidden), sea bed (LOD stride 4), underground zones (cave volumes, proposal) |
| `03_MOUNTAINS` | `WORLD_mountains_v001.blend` | mountain terrain pieces per region + range lines |
| `04_FORESTS` | `WORLD_forests_v001.blend`, `FOREST_proxies_v001.blend` | forest terrain pieces; reusable low-poly tree / canopy proxies (instancing) |
| `05_RIVERS_AND_LAKES` | `WORLD_water_v001.blend` | ocean surface, 423 rivers, 26 lakes, lake beds, 5 waterfall sites |
| `06_DESERTS` | `WORLD_deserts_v001.blend` | desert terrain pieces |
| `07_ISLANDS` | `WORLD_islands_v001.blend` | 3 archipelagos + minor islands (west / east / north / south) |
| `08_ASHRAM_VALLEY` | `ASHRAM_VALLEY_terrain_v001.blend`, `data/` | true-scale valley terrain (3 LODs), rivers, forests + groves (GN instancing), proposed path, Ashram placement reference, haze, 8 cameras |
| `09_DIMENSIONS` | `DIM_black_hole_training_v001.blend`, `DIM_saithan_dark_world_v001.blend`, `data/` | separate dimension blockouts (own files, own space) |
| `10_CAMERAS` | `WORLD_cameras_v001.blend`, `cameras_and_inventory.json` | 17 main-world preview cameras + key sun |
| `11_MATERIALS` | `WORLD_materials_v001.blend` | 42 procedural materials (no image textures → nothing can go missing) linked by every file |
| `12_RENDER` | `cycles/`, `viewport/`, `SHEET_*.png`, `render_log.json`, `qc/` | Cycles previews, Workbench viewport screenshots, contact sheets, QC data |
| `13_BACKUPS` | `*__backup_<time>.blend` | copy of every file made before it is overwritten (large geometry backups stay local, see `.gitignore`) |
| `scripts` | `run_all.sh` + `w4_*.py`, `worldkit.py` | the whole pipeline (data prep in python3 + numpy/scipy; Blender scripts use only bpy + numpy) |

## Collections in `MAIN_WORLD`
`MAIN_WORLD` → `00_REGIONS_BY_DIRECTION` (`NORTHERN/SOUTHERN/EASTERN/WESTERN_REGIONS` → `REGION_<key>`), `MOUNTAIN_REGIONS`,
`FOREST_REGIONS`, `DESERT_REGIONS`, `PLAINS_AND_HILLS`, `COASTAL_AREAS`, `ICE_AND_TUNDRA`, `RUINED_REGIONS`, `UNDERGROUND_ZONES_ALL`,
`WATER_SYSTEMS`, `ISLANDS`, `ASHRAM_VALLEY`, `UNEXPLORED_REGIONS`, `OCEAN_FLOOR`, `GEOGRAPHY_REFERENCE`, `CAMERAS`, `LIGHTING`.
A terrain piece is ONE linked collection (e.g. `MTN_C1`) that appears both under its region (`REGION_C1_AETHERIA`) and its
theme (`MOUNTAIN_REGIONS`) — same data, no copies. Names are the proposed revision-01 names; keys (C1…C5, A1…A3) stay stable.

## How the terrain is made (no random pieces)
1. One continuous height grid (map v2, 1536 × 768, 7.8 km cells) is cut into pieces by (region × terrain class); pieces share
   border vertices and use global normals → no gaps, no seams (QC: every land-window face covered exactly once).
2. Rivers = the map's own flow network (always downhill), lakes = flat water at each lake's spill level, coasts = the map
   coastline + shelf to −300 m, sea bed + ocean surface below/around.
3. Ashram Valley = the detailed Aetheria data (3 km cells) → bicubic + procedural detail (zero-mean on the valley floor), rivers
   carved from the detailed flow network, biome masks warped so 3 km cells never show, Ashram pad flattened.
4. Dimensions = the MAP_H1 / MAP_H2 layouts rebuilt in 3D with the same random seeds.

## Rebuild / open on your PC (Blender 4.5)
```bash
cd 02_world/3d_world/scripts
BLENDER=/path/to/blender PY=python3 ./run_all.sh        # python3 needs numpy + scipy + pillow (data prep + sheets only)
```
Open `00_MASTER_WORLD/WORLD_master_v001.blend` (keep the folder structure — links are relative). Viewport tip: Solid mode →
Colour = *Attribute* shows the terrain colours; the valley file hides nothing, so start in the LOD1/LOD0 area.

## Created · tested · pending
See `QC_REPORT.md` for every automated check and `../../STATUS.md` for what the Director still has to approve.

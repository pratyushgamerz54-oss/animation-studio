# TASK 05 — THE GRAND UNIVERSE · DETAILED TERRAIN & LANDSCAPE PRODUCTION

> **Status: ✅ MILESTONE 1 APPROVED (Director, 21 Nov: shots 1, 2, 6, 7, 7b + revised cascade & peaks) · ✅ MILESTONE 2 built (rest of the world, previews in `T5_SHEET_02_MILESTONE2.png`).** Built + tested in **Blender 4.5.16 LTS** (Cycles CPU).
> Built ON TOP of the approved TASK 04 blockout: same coordinates, same scale (1 BU = 1 m, true scale), same rivers / layout.
> v001 baseline untouched (checksums verified); all new work = **v002** files. Map revision 01 stays a **PROPOSAL** (not canon);
> GEM still unconfirmed; no story location invented (the featured waterfall is simply the largest drop of the existing river network).
> Director rule: final film / MP4 **above FHD (4K UHD target)**, sharp on zoom — the 1280×720 images here are approval previews only.

## Milestone 1 scope (brief: "Ashram Valley, its approved surrounding landscape, first mountain and forest regions")
| Region | Tile | Area | Grid | Notes |
|---|---|---|---|---|
| Ashram surroundings (hero) | VH | 2.4 × 2.4 km | **2 m** | river + banks, meadow, groves, Ashram pad (placement ref), proposed path |
| Valley near | L0 | 12 × 12 km | 10 m | |
| Valley + forest belts | L1 | 64 × 64 km | 40 m | |
| **First forest region** — northern forest belt where the river enters it | FH | 3 × 3 km | **2 m** | real Poly Haven trees, understory, logs, roots, mossy rocks |
| **First mountain region NW01** — the snowy range ≈ 100 km NW of the Ashram | MT | 60 × 60 km | 30 m | isotropic ridges, hydraulic + thermal erosion, strata, snow/ice/scree/cliff masks |
| Waterfall gorge (largest drop in NW01, 86 m) | WF | 900 × 900 m | **1.5 m** | vertical lips, cliff bands, gorge, plunge pools, curtains + mist |
| Horizon | L2 | 320 × 320 km | 400 m | rest of the great range, the map lake (SW) |

## Files (all in `02_world/3d_world/`)
| File | Contents |
|---|---|
| `00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend` | **open this** — links all components; HDRI sky + matching sun; 7 cameras `CAM_T5_*`; compositor (aerial perspective, glare) |
| `08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend` | tiles VH, L0, L1, L2 + valley scatter (meadow grass, wild flowers, shrubs, groves, forest belts, river stones, boulders) |
| `04_FORESTS/FOREST_NORTH_BELT_v002.blend` | tile FH + forest scatter (trees near/mid/far, saplings, understory, clearing grass, fallen logs, roots / stumps / debris, mossy rocks, river stones) |
| `03_MOUNTAINS/MOUNTAIN_NW01_v002.blend` | tiles MT + WF + mountain scatter (conifers below the tree line, talus boulders, gorge rocks, stream boulders, alpine grass) |
| `05_RIVERS_AND_LAKES/WATER_v002.blend` | rivers (v001 network; foam attribute for rapids / pools), map lake (shoreline = terrain ∩ level, no stair-steps), waterfall curtains, mist |
| `11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend` + `MATERIAL_LIBRARY.md` | PBR library (20 materials, Poly Haven 2K) + terrain shader |
| `14_NATURE_LIBRARY/T5_NATURE_LIBRARY_TREES_v002.blend`, `…_GROUND_v002.blend` | 101 assets (+ inventories json) |
| `<folder>/heightfields_v002/` | 32-bit EXR heightfields + mask PNGs per tile |
| `08_ASHRAM_VALLEY/data_v002/` | prep data (`*.npz`) + `prep_v002.json` (tile stats, rivers, lake, waterfalls) |
| `12_RENDER/T5/` | `cycles/CAM_T5_*.png`, `T5_SHEET_01_CINEMATIC_TESTS.png`, `T5_MATERIAL_LIBRARY_swatches.png`, `render_log_t5.json`, `qc/` |
| `T05_QC_REPORT.md` | automated technical QC |

## How the terrain is made (procedural, but anchored to the approved map)
1. `t5_field.py` = the TASK 04 height function verbatim (reproduces v001 to 3e-5 m). In the mountains the two blockout ridge terms are
   re-synthesised with **isotropic gradient noise + domain warp** (same scales, amplitude and mean) — the old value noise showed squares.
2. Per tile: band-limited detail (only wavelengths ≥ 3 cells) → **droplet hydraulic erosion** (numba) + **thermal erosion** (talus →
   scree mask) → detail × border weight (0 at tile edges → seamless with the coarser LOD) → rivers carved at the **v001 water levels**
   (valley levels unchanged, verified) → map lake at spill level → Ashram pad → proposed path.
3. Masks (forest, rock, snow + couloir accumulation, wet, dry, pad, groves, scree, gravel bars, path, erosion flow, cliff).
4. Blender: `NG_T5_HEIGHTFIELD` turns heightfield + masks into a real mesh (exact pixel-centre sampling, LOD holes, skirts, mask
   attributes). Viewport resolution is a modifier input (default 20–60 %); render = 100 %. Apply the modifier for a static mesh.

## Procedural systems (exposed parameters)
* `NG_T5_HEIGHTFIELD` — Height / Mask images, extents, Viewport / Render Resolution, Skirt Depth, 2 hole rectangles, Material.
* `NG_T5_SCATTER` — Density, Viewport Density, Mask + range, 2 Avoid masks, Slope / Altitude range, Cluster Scale / Amount,
  Scale range + Scale By Mask, Align To Normal, Random Tilt, Sink, Seed, **camera culling** (distance, cone angle, keep-near) and
  **distance LOD** (Near / Mid / Far collections + switch distances). Culling only zeroes density per face → points are stable
  in animation (no popping). Every scatter object `SC_*` carries its parameters as custom properties too.
* `t5_prep.py` — tile table, erosion settings, detail amplitudes, river / waterfall / lake rules.
* `MAT_T5_TERRAIN` — layer scales, colours, slope / altitude thresholds (see `MATERIAL_LIBRARY.md`).

## Optimisation
Nested LODs (1.5 m → 400 m) with holes + skirts · heightfields as compressed EXR (component .blend files are < 1 MB) · instancing
only (no realised geometry), 3-level tree LOD (Poly Haven LOD1 / LOD2 / 60-tri proxies) · camera-cone + distance culling ·
far canopy & far rock in the shader (no geometry / no textures far away) · per-shot render script disables unrelated scatter ·
viewport defaults: terrain 20–60 % resolution, scatter 1–30 % density, scatter carriers drawn as bounds.
Measured (4 CPU, no GPU): 640×360 test 1–2 min / shot; RAM peak ≈ 11 GB.

## Rebuild (Blender 4.5)
```bash
cd 02_world/3d_world/scripts
python3 t5_prep.py                                   # numpy/scipy/numba — ≈ 2 min
B=<blender-4.5-python or blender -b -P>
$B t5_build_materials.py ; T5_LIB=trees $B t5_build_library.py ; T5_LIB=ground $B t5_build_library.py
for c in valley forest mountain water; do $B t5_build_terrain.py -- $c; done
$B t5_build_master.py ; $B t5_render.py ; python3 t5_contact_sheet.py ; $B t5_qc.py
```

## Milestone 2 — rest of the world (region sites, each with its own local frame)
| Region | Files | Detail | Shots |
|---|---|---|---|
| **R04 Western Desert & Wastelands** | `06_DESERTS/DESERT_R04_v002.blend` (+ `data_v002/`, `heightfields_v002/`) | 120 km @300 m · 24 km @20 m · 3 km @2 m; wind-shaped dunes (steep slip faces), sandstone mesas/buttes with strata + talus aprons, canyons/wadis along the map drainage (big channels wet, small dry — proposal), playas (cracked ground), desert pavement; `MAT_T5_TERRAIN_DESERT` (biplanar strata) | 5, 5b |
| **R05 Forbidden Region** (blasted crater) | `06_DESERTS/FORBIDDEN_R05_v002.blend` | 192 km @400 m · 24 km @20 m · 3 km @2 m; raised rim, radial ejecta ridges, fissures, ash ground, rubble, dead trees, the map's crater lake at spill level; `MAT_T5_TERRAIN_FORBIDDEN` (no lava / glow — not approved) | 9, 9b |
| **R02 Enchanted Forest** | `04_FORESTS/ENCHANTED_FOREST_R02_v002.blend` | 80 km @200 m · 12 km @10 m · 3 km @2 m; ancient trees ×1.7–2.8, moss carpet, dense ferns, fallen giants, roots, mossy rocks, ground mist; `MAT_T5_TERRAIN_ENCHANTED` (teal-green key from the World Bible) | 10, 10b |
| **R03 Great Northern Range (core)** | `03_MOUNTAINS/GREAT_NORTHERN_RANGE_R03_v002.blend` | 240 km @400 m · 60 km @30 m (milestone-1 mountain pipeline: isotropic ridges, erosion, strata, snow, glaciers, arêtes) | 11, 11b |
| **Cave entrance** (map cave marker, R03 foothills) | in the R03 file, tile `CV` 1.6 km @2 m | rock outcrop with Boolean mouth + tunnel, forest clearing, rockfall; interior = later (underground task) | 12 |
| **Main world v002** | `02_TERRAIN/WORLD_terrain_v002.blend` (+ `01_GEOGRAPHY/data_v002/`) | whole map as one real mesh, 3.9 km grid (×2 v001), isotropic ranges + erosion, smoother coasts/islands, 26 lakes as planes at their levels (smooth shores — fixes v001 stair-steps), ocean | W1–W3 |
Region masters: `00_MASTER_WORLD/T5_REGION_<R>_…_master_v002.blend` (HDRI + sun + compositor + cameras). Scripts: `t5_region_prep.py <R04|R05|R02>`,
`t5_prep.py R3F R3N CV`, `t5_world_prep.py`, `t5_build_terrain.py -- desert|crater|enchanted|range`, `t5_build_world.py`,
`t5_build_region_master.py -- <R>`, `t5_render.py -- --master <file>`, `SHEET=2 python3 t5_contact_sheet.py`, `t5_qc_m2.py`.

## Completed · pending
**Completed (milestone 1):** detailed terrain for the Ashram Valley + surroundings, northern forest belt, mountain region NW01 with a
waterfall gorge; mountain ranges / peaks / ridges / cliffs / scree / snow + ice / erosion; valley hills / meadows / riverbanks / gravel
bars; forest floor, tree zones, roots, logs, understory, paths; rivers, streams, waterfalls, the map lake, water + foam + mist materials;
PBR library; nature asset library; procedural systems; 6 of 7 cinematic tests (+ forest-floor ground shot); QC.
**Completed (milestone 2):** desert (R04) + desert shot 5, forbidden / ruined crater terrain (R05), enchanted forest (R02, distinct look),
Great Northern Range core (R03), a cave entrance at the map's cave marker, main-world v002 (coasts, islands, ranges, smooth lake shores).
**Pending / later tasks (not blocking TASK 05):**
* Other continents (C2–C5) and archipelagos only at main-world v002 detail (3.9 km) — true-scale region sites are built per story need.
* Cave interiors / underground systems (only entrances now); Lake District shore close-ups; NW massif.
* Final film shots: per-camera hero tiles + 4K/8K textures + LOD0 assets + 4K render on the GPU PC (Director rule).
* Ashram building is a separate asset (concept v3) — to be placed on the VH pad later.

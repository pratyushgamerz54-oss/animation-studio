# TASK 05 — THE GRAND UNIVERSE · DETAILED TERRAIN & LANDSCAPE PRODUCTION

> **Status: 🟨 MILESTONE 1 — previews ready, awaiting Director approval.** Built + tested in **Blender 4.5.16 LTS** (Cycles CPU).
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

## Completed · pending
**Completed (milestone 1):** detailed terrain for the Ashram Valley + surroundings, northern forest belt, mountain region NW01 with a
waterfall gorge; mountain ranges / peaks / ridges / cliffs / scree / snow + ice / erosion; valley hills / meadows / riverbanks / gravel
bars; forest floor, tree zones, roots, logs, understory, paths; rivers, streams, waterfalls, the map lake, water + foam + mist materials;
PBR library; nature asset library; procedural systems; 6 of 7 cinematic tests (+ forest-floor ground shot); QC.
**Pending:**
* Desert landscape (test 5) and the **forbidden / ruined terrain** — the milestone-1 area has no desert; next milestone (R-04 west, R-05).
* Remaining world regions at detail: enchanted forest R-02 (visually distinct), other ranges (R-03 core, NW massif), plains, coasts,
  islands, underground entrances, lake-district shores.
* Waterfall shot = first pass (gorge walls + curtain need another iteration: more natural rock walls, layered spray).
* Mountains: sharper arêtes / glacier tongues for close shots; final 4K shots need per-camera hero tiles + 4K/8K textures (Director rule).
* Ashram building is a separate asset (concept v3) — to be placed on the VH pad later.

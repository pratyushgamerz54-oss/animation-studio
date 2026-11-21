# ASHRAM — Concept Development v3 (PROPOSAL — awaiting Director approval)

> **Versions:** v1 = grey blockout (layout only — Director: “bekar”, rightly) → v2 = procedural look-dev (code-built trees,
> grass, materials) → **v3 = real photo-scanned CC0 assets (Poly Haven): fir trees, saplings, broadleaf trees, grass, shrubs,
> mossy rocks, boulders, stone / plaster / cobble / wood / clay-tile / ground / snow textures, HDRI skies.**
> Scene: `01_BLOCKOUT/ASHRAM_concept_v003.blend` · script `../_shared/ashram_concept_v2.py` (v003 when the assets exist) ·
> sheets `00_REFERENCE/ASHRAM_*_v3.png` · renders `09_RENDER/concept_v3/`.
> Assets are re-downloaded by `03_assets/external/polyhaven_fetch.py` (not in git, >1 GB).

> Detailed final construction (Phase 4) starts **only after approval** of this direction.
> CONFIRMED: the Ashram is a production location associated with the **Headmaster (Ramarat), students and training**.
> Everything below is **PROPOSED** unless marked otherwise. NOT CONFIRMED: interiors, number of students, other activities,
> exact surroundings, time period, scenes that happen here.

## Proposed direction — “Himalayan foothill gurukul”

A walled teaching compound in a green foothill valley on a lake shore, with the snow range rising directly behind it
(matches its proposed map position R-01, ~720 m elevation, below the Great Northern Range).

- **Feeling:** calm, sacred, disciplined, warm. Low horizontal buildings against huge vertical mountains → the world feels enormous.
- **Axis:** strong north–south line: training ground → stone gate → courtyard with a sacred tree → main hall → mountains.
- **Language:** stone plinths, lime-plaster walls, dark-timber verandah pillars on stone bases, 1–2 tier clay-tile hip roofs with
  slightly up-turned eaves, brass finials, prayer-cloth flags. (Original design — not copied from any real temple or film.)

## Proposed layout (`00_REFERENCE/ASHRAM_layout_plan_v1.png`)

| # | Zone | Size (m) | Why (link to confirmed facts) |
|---|---|---|---|
| 1 | Main hall (Headmaster / assembly), 2-tier roof, 1.6 m plinth | 28 × 20 footprint incl. verandah | Headmaster CONFIRMED |
| 2–3 | Student residences west + east (long verandah blocks) | 12.4 × 34.4 each | Students CONFIRMED |
| 4 | Service hall (kitchen / stores) | 15.6 × 11.6 | Proposal (daily life of students) |
| 5 | Study hall / library | 15.6 × 11.6 | Proposal (teaching) |
| 6 | Paved courtyard + sacred tree on a stone platform | 56 × 40 | Proposal (gathering space for scenes) |
| 7 | Stone entrance gate (torana) | 9 m wide, 5.3 m high | Proposal |
| 8 | Training ground (open ring) outside the gate | Ø 44 m | Training CONFIRMED · room for power + portal VFX away from buildings |
| 9 | Meditation pavilion (open mandapa) by the lake | 11 × 11 | Proposal |
| 10 | Lake ghat (steps into the water) | 16 m wide | Proposal |
| 11 | Boundary wall, 1.4 m, modular 4 m segments | 120 × 124 | Proposal |

Remove / add any zone — nothing here is canon.

## What exists now (verified files)

| Item | File | Status |
|---|---|---|
| Real 3D blockout scene (real metres) | `01_BLOCKOUT/ASHRAM_blockout_v001.blend` | ✅ v1 (layout only) |
| Look-dev scene with real CC0 assets | `01_BLOCKOUT/ASHRAM_concept_v003.blend` | ✅ v3 — carved pillars + bracket capitals, moulded plinths, lattice windows, double doors with brass rings, clay-tile roofs (UV-aligned tiles, eave tiles, rafters), prayer flags, lamp pillars, pots, benches; 4 km valley + 30 km snow range; geometry-node scattered forests / grass / shrubs / rocks; HDRI day + night, haze + lake mist |
| Rebuild script | `../_shared/ashram_blockout.py` | ✅ |
| Modular kit (13 assets, linked duplicates) | collection `ASHRAM/02_ARCHITECTURE/MODULES` | ✅ blockout level |
| Terrain: 3 km detail tile + far LOD mountain ring (to 14 km) + lake | `ASHRAM/03_TERRAIN` | ✅ blockout level |
| Vegetation: ~18 000 instanced trees (3 blockout variants, forest clusters, tree line) | `ASHRAM/03_TERRAIN/VEGETATION` | ✅ blockout level |
| Lighting: day (sun + sky + haze volume) and night (moon + lanterns + hall glow) | `ASHRAM/06_LIGHTING` | ✅ tested |
| Cameras: 10 (wide, front, back, 2 sides, ground level 1.6 m, detail, training, pavilion, bird’s-eye ortho) | `ASHRAM/07_CAMERAS` | ✅ |
| Concept sheet (all views) | `00_REFERENCE/ASHRAM_concept_sheet_v1.png` | ✅ |
| Layout plan | `00_REFERENCE/ASHRAM_layout_plan_v1.png` | ✅ |
| Lighting sheet (day vs night) | `00_REFERENCE/ASHRAM_lighting_sheet_v1.png` | ✅ |
| Material palette | `00_REFERENCE/ASHRAM_materials_sheet_v1.png` | ✅ |
| Final detailed architecture, interiors, UV/baked PBR textures, final vegetation, QC report | — | ⬜ **after approval** (Phase 4) |

Scene organisation follows the brief: `00_REFERENCE 01_BLOCKOUT 02_ARCHITECTURE 03_TERRAIN 04_PROPS 05_MATERIALS 06_LIGHTING
07_CAMERAS 08_VFX 09_RENDER 10_BACKUPS` (folders on disk + matching collections inside the .blend).

## Honest limits of this blockout

- It is a **massing / direction** model: simple boxes, cylinders and roof shells, procedural materials, lollipop trees.
  Carving, roof tiles as geometry, doors/windows detail, interiors and baked textures come in Phase 4.
- The terrain tile is procedural and **not yet sampled from the world heightmap** — after the map is approved the valley
  will be re-fitted to the exact R-01 terrain so the world stays consistent.
- Render here = CPU preview (16 samples, haze volume). Final quality renders on the Director’s GPU PC.

## Questions for the Director

1. Approve this direction (Himalayan foothill gurukul)? Or a different style (e.g. forest, cliff-top, riverside, desert oasis)?
2. Which zones stay / go / are missing? (e.g. a well, a gate guardhouse, gardens, an arena)
3. Interiors needed? Which rooms appear in the story?
4. Is there a reason the Ashram should be by a lake (story) or can it be a river / plain?
5. Size: small intimate ashram (as now, ~120 m) or a big campus?

# TASK 04 — CLOSEOUT REPORT · The Grand Universe: 3D World Blockout

| | |
|---|---|
| **Status** | ✅ **CLOSED** — milestone 1 **APPROVED FOR DETAILED ENVIRONMENT PRODUCTION** by the Director (21 Nov 2026) |
| Scope of the approval | the current **blockout geometry + geographical layout** only |
| NOT approved / still open | world map **revision 01 stays a PROPOSAL** (not canon) · **GEM location stays UNCONFIRMED** |
| Baseline | git commit `a34c590` · Blender **4.5.16 LTS** · checksums in `TASK04_BASELINE_MANIFEST.json` |
| QC | **70 / 70 PASS** in Blender 4.5 and **70 / 70 PASS** in Blender 5.3 (`QC_REPORT.md`) |

## 1. Director's approval conditions → how each one is enforced

| # | Condition | Enforcement |
|---|---|---|
| 1 | Preserve the approved blockout geometry + layout | All 14 `*_v001.blend` + prep data are a frozen **baseline**; `worldkit.save()` **refuses** to overwrite any baseline file (tested: refusal works, checksums unchanged). Task 5 writes new `v002+` files that build on top of v001. |
| 2 | Map revision 01 stays a PROPOSAL | Every file/scene still carries `status = PROPOSAL … NOT LOCKED`; docs and contact sheets keep the PROPOSAL banner. The approval is recorded as "blockout layout only". |
| 3 | GEM location unconfirmed | Only the existing proposal marker (`MK_GEM_PROPOSAL`, labelled *not confirmed*) exists; no GEM environment, no relocation, no decision without the Director. |
| 4 | Preserve Black Hole + Dark World blockouts | `09_DIMENSIONS/*_v001.blend` are in the baseline (protected, checksummed). |
| 5 | Keep all original files and backups safe | Originals in git (`a34c590`) + manifest checksums; **all 16 backups** in `13_BACKUPS/` are now committed to git (previously the large ones were local-only and would have been lost with the cloud container). |
| 6 | Close only when deliverables + documentation are closed | §2 + §3 below. |

## 2. Final deliverables (TASK 04 §13)

| # | Deliverable | Result | Where |
|---|---|---|---|
| 1 | Main World Blender project | ✅ created + tested | `00_MASTER_WORLD/WORLD_master_v001.blend` (links all components; scenes MAIN_WORLD, ASHRAM_VALLEY, DIM_BLACK_HOLE_TRAINING, DIM_SAITHAN_DARK_WORLD) |
| 2 | Separate regional terrain collections | ✅ | N/S/E/W region collections + Mountain, Forest, Desert, Plains, Coastal, Ice/Tundra, Ruined, Underground, Water, Islands, Ashram Valley, Unexplored |
| 3 | Ashram Valley blockout | ✅ | `08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v001.blend` (true scale, LOD0/1/2) |
| 4 | Terrain geometry | ✅ | 44 world pieces from one grid (0 gaps / 0 overlaps), sea bed, 700 k-vertex valley terrain |
| 5 | Mountain + river systems | ✅ | 423 world rivers + 96 valley rivers (0 uphill steps), 26 lakes, ocean, 5 waterfall sites, range lines |
| 6 | Separate dimension blockouts | ✅ Black Hole Training · ✅ Saithan's Dark World · ⏸ **GEM: deferred by Director** (location unconfirmed — condition 3) | `09_DIMENSIONS/` |
| 7 | Camera preview renders | ✅ 27 Cycles + 11 viewport (Workbench) + 4 contact sheets | `12_RENDER/` |
| 8 | Blender Python scripts | ✅ prep (python3) + build/render/QC (Blender 4.5) + `run_all.sh` | `scripts/` |
| 9 | Technical QC report | ✅ 70/70 (4.5) + 70/70 (5.3) | `QC_REPORT.md`, `12_RENDER/qc/` |
| 10 | Backup files | ✅ 16 backups, committed | `13_BACKUPS/` |

Documentation: `README.md` (structure, rebuild), `01_GEOGRAPHY/WORLD_SCALE.md` (scale + coordinate system), `QC_REPORT.md`,
this closeout, `TASK04_BASELINE_MANIFEST.json`.

## 3. Known limitations carried into Task 5 (not defects of the approved layout)
1. Main-world lakes have stair-step shores (7.8 km map grid) — world-scale only.
2. Valley LOD2 (±160 km, 1 km grid) mountains are smooth/blobby; the snow-range aerial (V05) is weak → Task 5 detailed mountains.
3. Main-world views use ×20 vertical exaggeration; true distances (snow range ≈101 km NW) are only seen in the valley file.
4. Vegetation = low-poly proxies; terrain = procedural colours (no image textures by design) → Task 5 Poly Haven textures + models.
5. Two valley rivers run parallel 3 km apart for long distances — present in the map data, kept unchanged.
6. Ashram building is a separate asset (concept v3, Blender 5.3 file) — only placement references live in the valley.

## 4. Task 5 readiness — Detailed Terrain & Landscape Production
**Rules carried over:** no unapproved geographical change, no story-location invention, map rev 01 = proposal, GEM unconfirmed,
v001 baseline untouchable, Blender 4.5 compatibility, backups before every overwrite, preview → Director approval → next step.

**Ready now (verified in this session):**
- Blender 4.5.16 LTS (bpy) + Mesa EGL for viewport screenshots + Cycles CPU; Blender 5.3 for cross-checks.
- Poly Haven CC0 assets downloaded (`03_assets/external/polyhaven/`, ~860 MB, re-fetch with `polyhaven_fetch.py`):
  - textures (2K PBR): `sparse_grass`, `aerial_grass_rock`, `forest_ground_04`, `brown_mud_leaves_01`, `grass_path_2`, `cliff_side`,
    `aerial_rocks_02`, `snow_02`, `mossy_cobblestone`, `cobblestone_floor_04`, `rustic_stone_wall`, `plastered_stone_wall`,
    `worn_mossy_plasterwall`, `clay_roof_tiles_02`, `medieval_wood`, `dark_wooden_planks`
  - models: `fir_tree_01`, `fir_sapling_medium`, `tree_small_02`, `shrub_01/02/03`, `fern_02`, `grass_medium_01/02`, `moss_01`,
    `rock_moss_set_01/02`, `boulder_01`, `mountainside`
  - HDRIs (4K): `kloofendal_48d_partly_cloudy_puresky`, `qwantani_dusk_2_puresky`, `qwantani_night_puresky`
- Existing loaders from Ashram v3 (`02_world/_shared/phkit.py`: PBR, LOD append, path fixing) — to be ported/tested for 4.5.

**Planned approach (to be confirmed against the Task 5 brief):**
1. New `v002` files on top of the v001 baseline (same coordinates, same coastlines/rivers/valley layout — detail only).
2. Ashram Valley first (true scale): higher-resolution near terrain, erosion-style detail, Poly Haven triplanar/slope/height-blended
   materials, real tree/shrub/rock scatter replacing proxies (LOD + instancing), river banks + water shader, HDRI sky.
3. Mountains: detailed LOD2 replacement for the snowy range ≈101 km NW (rock/snow materials, ridges) without moving it.
4. Main world: smoother lake shores + texture-free macro shading stay world-scale (textures only where visible).
5. Same QC discipline (opens in 4.5, no missing textures — Poly Haven paths relative + fetch script, renders, checksums of baseline).

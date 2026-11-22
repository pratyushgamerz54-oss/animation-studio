# THE MAIN WORLD — Geography v2 + REVISION 01 — PROPOSAL, NOT LOCKED

> **Revision 01 (Director, 21 Nov) applied — all still PROPOSALS, not story canon:**
> 1. Continents renamed: **Aetheria** (C1, home, Ashram) · **Solmara** (C2) · **Veylora** (C3) · **Noxara** (C4, polar) · **Drakmor** (C5).
> 2. **Ashram** moved to a **large green valley in Aetheria** (grassland floor, forest ring, rivers) — new site ≈ (3724, 4238) km.
> 3. **Snowy range** ≈ 100 km NW of the Ashram: visible from the region, separated from it by a forest belt and foothills (map G).
> 4. **Dimensions** developed as two visually separate proposals: `MAP_H1_black_hole_training_dimension_v2.png` (floating platform
>    rings around a black hole, orange/blue, vacuum) and `MAP_H2_saithan_dark_world_dimension_v2.png` (ash plains, obsidian spires,
>    corruption rivers, corrupted-portal site; red/violet fog). No connection or dimensional rules invented.
> 5. **GEM** — exact location NOT CONFIRMED → proposal: **hidden ancient region in Veylora** (deep enchanted forest, ≥ 170 km from
>    any proposed settlement, ancient ruins) with a **GEM chamber plan** → `MAP_J_gem_hidden_region_v2.png` ≈ (11460, 4664) km.
> 6. **Portals** → `MAP_I_portal_connections_v2.png`: CONFIRMED = portals exist + portal users (Hero 1, Pratyush, Saithan, Ramarat);
>    routes H1–H5 are HYPOTHETICAL (dashed) until the Director confirms them; no confirmed route yet.


> **Director (21 Nov): “dono ko ek me jod ke continue karo”** → the detailed v1 continent (`02_world/map/`) is now the
> **home continent C1 AETHERIA** inside a much larger main world. Everything below is **PROPOSED**; every number is an
> **ESTIMATE**; no civilisations, rulers, history or portal rules were invented. Generator: `02_world/_shared/worldgen2.py`
> (re-runs exactly; C1 data comes from `02_world/_shared/worldgen.py`, seed 7).

## Maps (all in `02_world/map_v2/`)

| # | Deliverable | File |
|---|---|---|
| A | Master geographical map — illustrated atlas (terrain shading, mountain + forest symbols, compass rose, scale bar, grid, legend) | `MAP_A_master_illustrated_v2.png` |
| A2 | Technical world map (flat classes, 1 000 m contours, codes, grid) | `MAP_A2_technical_v2.png` |
| B | Continent maps (5) with size / terrain / climate / ranges / rivers / forest / settlements panel | `MAP_B_continent_C1…C5_*.png` |
| C | Mountain + river system map (main / secondary ranges, flow arrows, waterfalls) | `MAP_C_mountains_rivers_v2.png` |
| D | Forest + vegetation map | `MAP_D_forest_vegetation_v2.png` |
| E | Climate + terrain map (latitude zones × moisture, rain shadows) | `MAP_E_climate_terrain_v2.png` |
| F | Cities + settlements map | `MAP_F_settlements_v2.png` |
| G | Ashram regional map (detailed C1 data) + access-route proposal | `MAP_G_ashram_region_v2.png` |
| H1 / H2 | Black Hole Training dimension layout · Saithan's Dark World layout | `MAP_H1_*.png`, `MAP_H2_*.png` |
| J | GEM hidden ancient region + chamber plan (proposal) | `MAP_J_gem_hidden_region_v2.png` |
| H | Separate dimensions map | `MAP_H_dimensions_v2.png` |
| I | Portal connection diagram (only confirmed links solid — currently none confirmed) | `MAP_I_portal_connections_v2.png` |
| — | Detailed C1 AETHERIA map + 6 regional maps (3 km cells) | `../map/WORLD_MAP_master_v1.png` (now titled AETHERIA), `../map/WORLD_MAP_regional_v1.png` |
| — | Data (heights, flow, biomes, climate, features) — continuity source of truth | `map_v2/data/` |

## World structure

- **One main world** (this atlas) · **separate dimensions** (Black Hole Training Area, Saithan’s Dark World — shown only on map H,
  never on the physical map) · **GEM location**: CONFIRMED name, but whether it is a dimension or a place on the main world, and where,
  is **NOT CONFIRMED** → not placed.
- **Scale (estimate):** known main world 12 000 km W–E × 6 000 km N–S; cell 7.8 km; equator = middle row. Land ≈ 18 % of the
  known area (the rest = oceans; map edges = unexplored waters, hatched).
- **World coordinates:** km, origin = south-west corner (A1), +X east, +Y north, Z = metres above sea level.
  Atlas grid = 1 000 km squares A–L × 1–6. C1 detailed map: 3 km per cell, its own local grid (300 km squares).

## Continents (all names PROPOSED, all numbers ESTIMATES)

| Code | Proposed name | Area | Extent W–E × N–S | Highest | Forest cover | Ranges | Big rivers to the sea | Proposed settlements (cities / towns / villages) | Character |
|---|---|---|---|---|---|---|---|---|---|
| C1 | **AETHERIA** (home) | ≈ 3.6 M km² | 2 810 × 2 030 km | ≈ 6 200 m | 60 % | Mahagiri / Great Northern Range (R-03) | 9 | 3 / – / 14 (from the detailed C1 map) | the v1 continent: great northern range, Ashram Valley (R-01), Lake District, Enchanted Forest, western desert & wastelands, Forbidden crater, southern grasslands |
| C2 | SOLMARA | ≈ 4.9 M km² | 3 220 × 3 280 km | ≈ 6 170 m | 62 % | Sunstone Ridge | 12 | 9 / 12 / 62 | equatorial / sub-tropical: desert interior + wasteland, savanna, rainforest coasts, great lakes |
| C3 | VEYLORA | ≈ 3.0 M km² | 2 980 × 1 880 km | ≈ 5 250 m | 48 % | Verdant Crown | 5 | 3 / 13 / 35 | wet forest continent with enchanted-forest belts, highlands |
| C4 | NOXARA | ≈ 1.4 M km² | 3 850 × 1 200 km | ≈ 6 680 m | 6 % | Ice Wall | 0 | 0 / 1 / 2 | polar: ice sheets, tundra, glaciers — mostly **unexplored** |
| C5 | DRAKMOR | ≈ 1.4 M km² | 1 740 × 1 260 km | ≈ 4 980 m | 42 % | Southern Teeth | 2 | 1 / 3 / 12 | southern grasslands, plateaus, tundra edge, ruins |
| A1–A3 | Sagara Archipelago · Agni Island Arc · Western Isles | small | — | — | — | — | — | coastal villages | island chains between the continents |

Oceans (proposed): Northern Ocean, Central Sea, Eastern Ocean, Western Ocean.
Settlement totals (all PROPOSED, codes only — no names or politics): 17 city sites, 29 towns, 125 villages, 16 remote settlements,
23 ancient-ruin sites, 17 cave-system entrances, waterfalls on the largest river drops.

## Ashram location proposal (map G)

- **Ashram = CONFIRMED story location. Its position = PROPOSAL (not locked).**
- C1 AETHERIA, region **R-01 Ashram Valley** (revision 01): large green valley ≈ 680 m, grassland floor, forest ring, several rivers.
- Snowy range ≈ 100 km NW beyond forests + foothills (visible on clear days). Lakes further SW / SE.
- **Proposed access route:** least-effort path to the nearest proposed village ≈ 300 km (estimate). No roads are canon.
- The Ashram 3D concept v3 backdrop (snow peaks close behind) will be re-fitted to this terrain after approval.

## Climate model (proposal)

Temperature from latitude + altitude; moisture from prevailing winds (westerlies in mid-latitudes, easterlies in the tropics) with rain
shadows behind ranges, wet coasts and river corridors → biomes: ice, tundra, taiga, temperate forest, grassland, savanna, desert,
rainforest, wetland, high rock, snow; enchanted forests and the forbidden zone are marked as proposals. C1 keeps the terrain classes of
its detailed map so the two maps match.

## Continuity audit (automatic, run with the generator)

| Check | Result |
|---|---|
| Rivers never flow uphill (on the hydrologically filled surface) | ✅ 0 uphill steps |
| Rivers end at the sea or a lake | ✅ 224 river mouths reach the sea; the rest end in lakes |
| Mountain ranges continuous | ✅ each range is one continuous crest line (map C) |
| Forests follow climate + relief | ✅ forests in wet zones, none above the tree line / in deserts (maps D, E) |
| Cities in sensible places | ✅ 17 / 17 city sites on large rivers or coasts |
| Coastlines continuous | ✅ 43 land masses (5 continents + islands), closed coastlines |
| Matches approved environment concepts | ⚠️ C1 = detailed v1 map (match ✅); Ashram 3D backdrop vs map distance to the snow range — to align after approval |

## ★ DECISION SHEET 01 (Director, 22 Nov) — applied · full record: `02_world/ecosystem/DECISION_SHEET_01.md`

| Item | Decision | Status |
|---|---|---|
| Region mapping (Map Revision 01) | Mountain Kingdom = **R-03** Great Northern Range · Green Plains = **R-06** Southern Grasslands · Crystal Lakes = **R-08** Lake District · Ancient City = **C-01, C-02, C-03** (three **separate** archaeological sites — no shared city, history or inhabitants invented) | **APPROVED** for environment production |
| Sky Realms | a **proposed region within the main world** — **not** a separate dimension. Direction: large floating islands of natural rock, selected islands with forests + waterfalls, ancient-looking structures, clouds + atmospheric depth between islands, some natural bridges / suspended land, strong visual link with the main world | design direction **APPROVED** · region **PROPOSED** · map position, travel routes, inhabitants, kingdoms, politics, story events **NOT established (PENDING)** |
| Enchanted Forest | ≈ 70–80 % natural / 20–30 % fantasy trees, giant trees in selected areas, subtle limited glow at night | **APPROVED** (`ecosystem/ENCHANTED_FOREST_VEGETATION_REFERENCE.md`) |
| Ashram planting | one landmark Peepal near the main courtyard + sitting area; Tulsi + Marigold only in the Ashram garden | **APPROVED** (`ashram/ASHRAM_LANDSCAPING_PLAN.md`) |
| Wildlife | not finalized | **PENDING** (`ecosystem/WILDLIFE_SELECTION_SHEET.md`) |
| Season | Spring = proposed primary season, consistent across connected scenes | **APPROVED** (`ecosystem/SEASON_REFERENCE_SPRING.md`) |

Region IDs verified against Map Revision 01 data (`3d_world/01_GEOGRAPHY/data/world_features.json` → `c1_regions`; `map_v2/data/features.json` →
`c1_regions`, `c1_city_codes`). World coordinates (km, origin = map centre; Ashram = (−2275, +1238)):
R-03 (−2185.5, +1523.4) 3 538 m · R-06 (−3570.8, +320.0) 314 m · R-08 (−1851.0, +1151.6) 315 m ·
C-01 (−1882.7, +647.1) · C-02 (−2851.2, −4.1) · C-03 (−3459.8, +290.0) — all on continent C1 AETHERIA. **No map geometry was changed.**
Sky Realms map position: **PENDING** — candidate options (proposal only, not drawn): (a) above the southern flank of R-03, visible from the
Ashram valley; (b) above R-08 Lake District; (c) over the sea west of C1. Director picks before any map update.

## Pending Director approvals (nothing is locked)

1. Overall layout: 5 continents + 3 archipelagos — approve / change shapes, sizes, positions?
2. Continent names (Director-proposed) Aetheria / Solmara / Veylora / Noxara / Drakmor — which continent gets which name? (current assignment is a proposal); range / ocean / archipelago names.
3. Ashram position (R-01 on AETHERIA) and how close the snow peaks should be.
4. Black Hole Training Area and Saithan’s Dark World as separate dimensions — correct?
5. GEM: accept the proposed hidden ancient region in Veylora + chamber, or another place?
6. Which portal connections exist in the story (map I shows none as confirmed).
7. Which regions the story actually uses → only those get detailed 3D environments.
8. Sky Realms map position (candidates above; Decision 01 §2 — region PROPOSED, not a dimension).

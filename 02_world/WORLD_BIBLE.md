# MASTER ENVIRONMENT BIBLE — DRAFT v1 (21 Nov)

> **Status: DRAFT — nothing here is locked.** The master map and every look are **PROPOSALS** until the Director approves them.
> Labels used everywhere:
> **CONFIRMED** = explicitly established by the Director / story · **PROPOSED** = visual suggestion needing approval ·
> **NOT CONFIRMED** = not established by the story (left open, nothing invented).

> ⚠️ **Story source:** there is **no story / script document in the project yet**. The only confirmed facts are the ones the
> Director wrote in the task briefs (location names, character list, powers, “Ashram = Headmaster, students, training”).
> Everything else about events, history and geography is NOT CONFIRMED. **Please share the story / script** so the analysis
> in §1 can be filled from it.

Deliverables in this draft:

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | World design document | this file | 🟨 draft, pending approval |
| 2 | Master world map | `map/WORLD_MAP_master_v1.png` | 🟨 PROPOSAL, **not locked** |
| 3 | Regional maps (6 × 240 km) | `map/WORLD_MAP_regional_v1.png` | 🟨 PROPOSAL |
| 4 | Elevation + hydrology reference | `map/WORLD_MAP_elevation_v1.png` | 🟨 PROPOSAL |
| 5 | Aerial geographical references (real 3D terrain) | `map/aerial/AERIAL_sheet_v1.png`, `blend/WORLD_overview_v001.blend` | 🟨 PROPOSAL |
| 6 | Location comparison sheet | `bible/LOCATION_COMPARISON_v1.png` | 🟨 PROPOSAL |
| 7 | Master colour palette (HEX + RGB + readability check) | `bible/COLOUR_BIBLE_v1.png`, `bible/colour_tables.md` | 🟨 PROPOSAL |
| 8 | Architectural style guide | §4 | 🟨 PROPOSAL |
| 9 | Material library standard | §6 | 🟨 PROPOSAL |
| 10 | Lighting guide | §7 | 🟨 PROPOSAL |
| 11 | Environment asset list | §8 | 🟨 PROPOSAL |
| 12 | Ashram concept development (3D blockout + sheets) | `ashram/ASHRAM_CONCEPT.md` | 🟨 PROPOSAL, awaiting approval |
| — | Black Hole Training / GEM / Dark World environments | — | ⬜ not yet created (Phases 5-7) |

---

## 1. Story & location analysis

| Location | CONFIRMED | Associated characters | Events | Environment needs (for film) | NOT CONFIRMED |
|---|---|---|---|---|---|
| **Ashram** | Name; it is a production location; associated with the **Headmaster (Ramarat), students and training** (Director brief) | Ramarat (CONFIRMED); students (CONFIRMED as a group — which characters are students is NOT CONFIRMED) | NOT CONFIRMED | Wide establishing, character-level and close-up shots; training space; room for portal + power VFX | Architecture, size, buildings, time period, region, terrain, day/night scenes, interiors |
| **Black Hole Training Area** | Name; a production location; “training” in the name | NOT CONFIRMED | NOT CONFIRMED | VFX-heavy space (power training) — PROPOSED as a separate dimension (world-list item 11 “Black Hole Training **Dimension**”) | How it is reached, what it looks like, scale, who trains there |
| **GEM Location** | Name; a production location | NOT CONFIRMED | NOT CONFIRMED | NOT CONFIRMED | What the GEM is, where it is, look — **not placed on the map** |
| **Saithan’s Dark World** | Name; belongs to Saithan (main villain) | Saithan (CONFIRMED); others NOT CONFIRMED | NOT CONFIRMED | Villain environment; corrupted portal (Saithan’s approved power) | Physical place or dimension, look, scale |
| **Magical Portal transitions** | Used for location transitions; Hero 1, Pratyush, Saithan and Ramarat have portal power (approved character sheets) | Those four | NOT CONFIRMED | Portal opening/closing VFX at both ends; colour per owner (approved) | Which locations portals connect, where portals open |

Rule kept: no geographical connection between these locations is invented. The Ashram has a **proposed position** on the
map only so the world can be built around it; the GEM location is deliberately unplaced; the two dimensions sit outside the map.

## 2. World geography (PROPOSAL v1 — not locked)

**One continent + surrounding seas, 1024 km × 768 km** (map generated procedurally by `_shared/worldgen.py`, seed 7, so
it is exactly reproducible; any change = a new map version).

- **World Coordinate System (WCS):** 1 map cell = 1 km. Origin (0,0) = south-west corner (grid A1), +X east, +Y north,
  Z = metres above sea level. Grid squares 100 km: columns **A–K** (west→east), rows **1–8** (south→north).
  Every detailed region scene is built in real metres around a local origin whose WCS position is stored on an empty
  (e.g. `ASHRAM_ORIGIN` → `wcs_x_km`, `wcs_y_km`).
- **Relief:** sea 0 m → highest peak **6 574 m** (Great Northern Range). Land ≈ 51 % of the map.
- **Rivers:** computed from the terrain (depression filling + D8 flow accumulation) → **every river flows downhill and
  reaches the sea**; widths grow with drainage area. Lakes = only large, deep basins (9 max). This is the continuity
  guarantee for rivers and mountains.
- **Climate logic (proposal):** wet east / dry west (rain shadow) → forests east, desert + wasteland west; colder north + altitude
  → rock above ~2 300 m, snow above ~3 600 m. Transitions are blended (no hard biome edges).
- **Roads / paths:** none drawn — none approved.

| Code | Working label (name pending) | Centre WCS (km) | Elev. at centre | Identity (proposal) |
|---|---|---|---|---|
| R-01 | **Ashram Valley** — CONFIRMED location, PROPOSED position | (474, 535) grid E6 | ~720 m | Foothill valley on a lake shore below the great range |
| R-02 | Enchanted Forest | (672, 263) | ~660 m | Deep teal-green old forest; hidden glade H-01 |
| R-03 | Great Northern Range | (626, 630) | 3 400 m (peaks 6 574) | Snow peaks, glaciers, caves, waterfalls, hidden plateau H-02 |
| R-04 | Western Desert & Wastelands | (137, 262) | ~200 m | Dunes, dry plateaus, ruins |
| R-05 | Forbidden Region | (276, 284) | ~370 m | Blasted crater ~90 km wide, dark ground, crater lake |
| R-06 | Southern Grasslands | (164, 229) | ~300 m | Open plains, villages |
| R-07 | Eastern Spine (rename? relief is low) | (819, 346) | ~360 m | Forested eastern hills |
| R-08 | Lake District | (738, 506) | ~330 m | Large lakes between forests |

Other proposed features on the map: **C-01…C-03** ancient city sites (on large rivers near coasts), **14 villages**,
**RU-01…RU-06** ancient ruins, **CV-01…CV-05** cave entrances (underground caves), **5 waterfalls** (largest river drops),
**H-01/H-02** hidden areas (dashed). **Separate dimensions** (Black Hole Training, Saithan’s Dark World) are shown in a panel,
not on the land. **GEM location: not placed.**

Proposed category list from the brief, and where it is on the map: Ashram Valley R-01 · Enchanted Forests R-02 · Mountain Ranges R-03
(+ north-west massif) · Rivers & Waterfalls (all rivers, 5 falls) · Ancient Cities C-01…03 · Villages (14) · Underground Caves CV-01…05 ·
Ancient Ruins RU-01…06 · Deserts & Wastelands R-04 · Forbidden Regions R-05 · Black Hole Training Dimension (panel) ·
Saithan’s Dark World (panel) · GEM Location (unplaced). **None of these is forced into the story.**

**Scale references for camera work:** Ashram compound ≈ 120 m × 125 m; Ashram valley tile = 3 km × 3 km; a regional map = 240 km;
the continent ≈ 1 000 km across (travel times between places are NOT CONFIRMED).

## 3. World-building questions — all NOT CONFIRMED (Director decides)

1. Is the world one continent, several continents, or part of a larger planet? Is there a name for the world?
2. Time period / technology level (ancient, medieval, modern, mixed)? Do cities have electricity, vehicles?
3. Is the Ashram in a valley, on a mountain, in a forest, by a river? Is it isolated or near a town?
4. Who lives in the world besides the main characters (ordinary people, villages, kingdoms)?
5. Are there civilisations, kingdoms, rulers, religions or gods? (none invented)
6. Is there a magic system? Who can use powers and why? Where do powers come from?
7. What is the GEM? Where is it, who guards it, what does it look like?
8. Is the Black Hole Training Area a real black hole, a pocket dimension, or a training illusion? How do students get there?
9. Is Saithan’s Dark World a separate dimension, a corrupted part of this world, or underground?
10. Which places do portals connect? Can anyone with portal power go anywhere?
11. Historical events (wars, catastrophes — e.g. what made the Forbidden crater, if it exists)?
12. Climate / seasons / weather in story scenes; day or night for each scene?
13. Are ruins, ancient cities, villages part of the story or background only?
14. Destruction required by the story (which locations get damaged)?

## 4. Architectural language (PROPOSAL)

| Location | Shapes | Structure | Materials | Openings | Decoration / repeat pattern |
|---|---|---|---|---|---|
| **Ashram** (detailed in `ashram/ASHRAM_CONCEPT.md`) | Long low horizontal blocks around a courtyard; tiered hip roofs | Stone plinth (0.6–1.6 m) → lime-plaster walls → timber verandah pillars on stone bases (2.4–3 m rhythm) → 1–2 tier clay-tile hip roofs with up-turned eaves | Coursed stone, lime plaster, dark timber, clay tile, brass finials | Wide timber doors (1.6 × 2.6 m), small deep windows, open verandahs | Timber wall band, pillar caps, brass finials, prayer-cloth flags; symmetry on the north–south axis |
| **Ancient cities** (background) | Massive terraces, domes and stepped towers | Stone mega-blocks | Sandstone / granite | Tall arches | NOT CONFIRMED — kept generic until story |
| **Villages** (background) | Small clustered houses | Mud / stone + timber | Earth plaster, thatch / slate | Small | Kept humble so the Ashram stays special |
| **Ruins** | Broken columns, half-buried gates | Same language as ancient cities, eroded | Weathered stone + moss | — | Damage standard §6 |
| **Black Hole Training** | Floating rings and broken platforms | Levitating stone | Dark stone with glowing seams | — | Concentric circles (gravity) |
| **Saithan’s Dark World** | Sharp shards, inverted spires, jagged arches | Obsidian growths | Obsidian, ash, blood-stone | Irregular | Cracks with violet light (matches Saithan’s approved palette) |
| **GEM location** | NOT CONFIRMED | — | — | — | — |

## 5. Colour bible (PROPOSAL) → `bible/COLOUR_BIBLE_v1.png` + `bible/colour_tables.md`

Exact HEX + RGB for every location (primary / secondary / accent / light / material), the world biome colours and the
**approved** portal colours of each character. A readability check (luminance contrast of each character’s main costume
colour vs each background) is generated automatically:

- **Result:** dark costumes (Pratyush suit, Saithan armour, Soul robe, Yayaki hood) are **below 1.5:1** against the
  Black-Hole void, Dark-World obsidian/ash and the Ashram at night; Hero 1’s coat on Dark-World ash is also low.
- **Rule (standard):** in dark locations every character gets a **rim light ≥ 2× fill** in a colour different from their own power
  colour, plus **fog separation** behind them; the Ashram by day reads well for everybody (≥ 2:1 on plaster and stone).

## 6. Environmental material standards (PBR) — PROPOSAL

Texel density: **hero zone (≤ 50 m from camera) 1024 px/m**, mid (50–300 m) 256 px/m, far (> 300 m) 64 px/m or vertex colour.
Maps per material: Base Color (sRGB), Roughness, Metallic, Normal (OpenGL, Y+), AO; Height only where displacement is used.
Procedural materials are used in blockout and are **baked to these maps** for the final asset library (same bake pipeline as the characters).

| Material | Base colour (HEX) | Roughness | Metallic | Normal / detail | Notes |
|---|---|---|---|---|---|
| Stone (coursed, Ashram) | `#8E8372` / `#9B907E` / mortar `#5E564C` | 0.75–0.85 | 0 | course joints + chisel noise, strength 0.35 | plinths, gate, ghat |
| Stone (rough / rock) | `#6A6156` → `#7B766E` | 0.85–0.95 | 0 | large noise + cracks 0.5 | cliffs, ruins |
| Lime plaster | `#E6D8BE` / `#D8C6A6` | 0.8 | 0 | soft 0.08 | walls; ages with dirt at the base |
| Timber | `#6B4426` / `#4A2E19` | 0.5–0.65 | 0 | grain 0.12 | pillars, bands, doors |
| Clay roof tile | `#A4512F` / `#7E3A22` | 0.6 | 0 | tile rows 0.4 | roofs |
| Metal (brass) | `#C9A040` | 0.25–0.35 | 1 | light scratches | finials, lamps |
| Metal (iron) | `#4A4A4E` | 0.45–0.6 | 1 | rust mask | hinges, gates |
| Soil / path | `#A88A5E` / `#9C7F5C` | 0.9 | 0 | pebbles 0.15 | paths, training ground |
| Concrete | NOT USED (time period NOT CONFIRMED) | — | — | — | add only if the story is modern |
| Glass | `#DDEBF0`, transmission 1, IOR 1.45 | 0.02–0.08 | 0 | — | only if approved |
| Water (lake) | `#2B5D73` | 0.03–0.06 | 0 | animated ripple normal | Mantaflow / ocean modifier in final shots |
| Magical surface | emission in the owner’s approved colour | 0.3 | 0 | animated noise | runes, portal rims |
| Damaged surface | base + `#3A332C` soot / cracks mask | +0.1 | 0 | crack normal 0.6 | destruction states (only if story requires) |

## 7. Lighting guide — PROPOSAL (time of day for any story scene is NOT CONFIRMED)

| Situation | Key | Fill / ambient | Atmosphere | Notes |
|---|---|---|---|---|
| Daylight exterior | Sun `#FFEBD0`, 2.5–3.5 W/m², soft angle 1° | Physical sky (Nishita), strength 0.3 | Haze volume 0.00009 /m (12 × 12 × 3 km box) | Sun from south-west on establishing shots (ridge lit, valley readable) |
| Night exterior | Moon `#9DB8FF` 0.2–0.3 | Sky `#0C1426` | Haze `#2A3550` | Lanterns `#FFB35A` (point 900 W) + interior glow `#FFB870` |
| Interior | Window/door bounce + practical lamps | Low warm ambient | Light shafts (volumetric) only in hero shots | NOT built yet (interiors NOT CONFIRMED) |
| Black Hole dimension | Accretion disk `#FFB35A` rim from side / below | `#3048A0` cool space | None (vacuum) — dust motes only | Silhouettes + rim, see readability rule |
| Dark World | Low red `#FF4A3A` | Violet `#3A1A5A` | Dense fog `#2A1630` | Mandatory character rim light |
| Magical / VFX | Every effect carries a real light (point / mesh emission) in its own colour | — | Volumetric glow in final shots | VFX lighting must touch the ground + characters (FINAL VFX RULE, CLAUDE.md) |

Shadows: sun soft angle 0.5–1.5°, contact shadows from real geometry (no fake AO cards). Reflections: water + brass + wet stone only.
Render: preview here (Cycles CPU, 16–24 samples, denoised); final on the Director’s GPU (high samples, motion blur, compositor glare).

## 8. Environment asset library (PROPOSAL) — naming `ASSET_<CATEGORY>_<NAME>`, scene objects `<CATEGORY>_<LOCATION>_<NAME>_<NN>`

| Category | Assets (built ✅ / planned ⬜) | Folder |
|---|---|---|
| Architecture modules | ✅ ASSET_PILLAR_TIMBER, ASSET_PILLAR_BASE_STONE, ASSET_PILLAR_CAP_TIMBER, ASSET_PILLAR_STONE, ASSET_WALL_SEG_4M, ASSET_STAIR_STEP, ASSET_DOOR, ASSET_WINDOW, ASSET_RAIL_SEG_2M · ⬜ roof-tile edge, carved door, railing set, gate details | `ashram/02_ARCHITECTURE` → `03_assets/architecture` once approved |
| Terrain | ✅ TERRAIN_ASHRAM_DETAIL_3KM, TERRAIN_FAR_LOD_MOUNTAIN_RING, WORLD_TERRAIN_LOD0 · ⬜ rock cliffs, boulders, riverbanks | `ashram/03_TERRAIN`, `blend/` |
| Vegetation | ✅ ASSET_TREE_A/B/C (blockout) · ⬜ final trees (3 species × 3 sizes + LODs), bushes, grass cards, flowers, moss | `03_assets/vegetation` |
| Furniture | ⬜ only after interiors are confirmed | — |
| Decorative | ✅ prayer-cloth flags, brass finials · ⬜ carvings, bells | `ashram/04_PROPS` |
| Environmental props | ✅ ghat steps, tree platform · ⬜ water pots, training dummies (only if story) | `ashram/04_PROPS` |
| Lighting objects | ✅ ASSET_LANTERN | `ashram/04_PROPS` |
| VFX elements | reuse `01_characters/_shared/vfxkit.py` (portals, lightning, fire…) + ⬜ environment FX (waterfall spray, dust, embers, fog cards) | `ashram/08_VFX` |

**LOD rules:** LOD0 hero (< 50 m) full detail · LOD1 (50–300 m) 30 % polys · LOD2 (300 m – 2 km) 5 % or instanced cards ·
far (> 2 km) single low-poly ring / matte. Vegetation is always instanced (linked duplicates), never merged into one mesh.

## 9. Naming, folders, versions

- World data: `02_world/map/data/` (height, rivers, biomes, features — the source of truth for continuity).
- Region scenes: `02_world/<region>/00_REFERENCE … 10_BACKUPS` (folder layout from the brief). Versioned files `_v001`, `_v002`…
- Scripts rebuild everything: `02_world/_shared/worldgen.py`, `world_terrain.py`, `world_bible_sheets.py`, `ashram_blockout.py`.
- **Blender version:** this machine runs **Blender 5.3** (Python module). Scripts only use API calls that also exist in 4.5,
  but **a .blend saved by 5.3 is not guaranteed to open in 4.5** — not verified yet. If the Director’s PC has 4.5, the scenes can be
  rebuilt there from the scripts (they need `numpy` + `scipy`). **Which Blender version is on the Director’s PC?**

## 10. Approval checklist for the Director

1. Master map layout (continent shape, range in the north, lakes, desert west, forest east) — approve / change? (**not locked**)
2. Working labels → final names for regions R-01…R-08, cities, etc.
3. Ashram position on the map (R-01) — OK?
4. Black Hole Training and Dark World as **separate dimensions** — correct?
5. Ashram architectural direction (see `ashram/ASHRAM_CONCEPT.md`).
6. Answers to §3 questions + the story/script document.

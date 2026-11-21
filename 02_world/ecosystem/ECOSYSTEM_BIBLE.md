# THE GRAND UNIVERSE — ECOSYSTEM & VEGETATION BIBLE · DRAFT v1 (TASK 06, milestone 1)

> **Status: DRAFT for Director approval.** Milestone 1 = concepts + first real 3D assets for **Ashram Valley**, the **Enchanted Forest
> tree collection** and **Mountain Kingdom vegetation references**. Full asset production (more variants, LODs, scattering into the
> terrains, other regions) starts **only after approval**.
>
> Labels used everywhere (sheets, Blender custom properties, inventories):
> **SPECIES-INSPIRED** = modelled on a real species (botanical name given) · **PROPOSED FANTASY** = fictional, a proposal only ·
> **CONFIRMED / PROPOSED / NOT CONFIRMED** for story and world facts (same as the World Bible).
>
> Rules kept: approved geographical layouts are preserved (no terrain was changed) · no story events invented · no intelligent
> species, monsters or story characters added · every vegetation asset is a **real 3D model** (no illustrations) · Blender 4.5 LTS.

Deliverables of milestone 1 (all in git):

| # | Deliverable | Where | Status |
|---|---|---|---|
| 1 | Ecosystem Bible (this file) | `02_world/ecosystem/ECOSYSTEM_BIBLE.md` | 🟨 draft |
| 2 | Tree reference library — 17 trees + 4 shrubs, one sheet each (front / side / back / leaf close-up / trunk foot / bark + leaf maps / height / canopy / palette) | `03_assets/vegetation/sheets/<AV\|EF\|MK>/TREE_*.png` | 🟨 concept |
| 3 | Plant & flower library — 21 plants (grass, wildflowers, ferns, moss, fungi, aquatic, vines, alpine) | `03_assets/vegetation/sheets/<R>/PLANTS_<R>.png` | 🟨 concept |
| 4 | Regional vegetation sheets (identity, height lineup, ground layer) | `03_assets/vegetation/sheets/<R>/REGION_<R>.png` | 🟨 concept |
| 5 | Wildlife proposal | §7 + `02_world/ecosystem/WILDLIFE_PROPOSAL.png` | 🟨 proposal (no models yet) |
| 6 | Real Blender vegetation assets (42) | `03_assets/vegetation/library/T6_VEG_<REGION>_v001.blend` | ✅ built, QC |
| 7 | PBR material library (16 scanned barks + 25 generated leaf / needle / flower atlases) | `03_assets/vegetation/textures/`, materials inside the libraries | ✅ built |
| 8 | Procedural scattering | plan §9 (re-uses TASK 05 `NG_T5_SCATTER`) | ⬜ milestone 2 |
| 9 | Wind animation setup | `NG_T6_WIND` + `T6_WIND_CONTROL` in every library, test clip | ✅ built |
| 10 | Preview renders | `03_assets/vegetation/renders/`, contact sheet `sheets/T6_SHEET_M1.png` | ✅ |
| 11 | Technical QC report | `03_assets/vegetation/qc/T06_QC_REPORT.md` | ✅ |

---

## 1. Region mapping (brief name → approved map rev 01 code)

The TASK 06 brief uses new names for some regions. They are mapped to the regions that already exist on the approved blockout
(map rev 01 = PROPOSAL, layout preserved). **Please confirm the mapping** (Q1, §12).

| TASK 06 brief | Map rev 01 | Where / terrain already built | Vegetation in milestone 1 |
|---|---|---|---|
| Ashram Valley | **R-01** Ashram Valley (CONFIRMED location, PROPOSED position) | TASK 05 valley v002 (2 m–400 m LODs) | ✅ full concept library |
| Enchanted Forest | **R-02** Enchanted Forest | TASK 05 `ENCHANTED_FOREST_R02_v002` | ✅ tree collection + key ground plants |
| Mountain Kingdom | **R-03** Great Northern Range (+ NW01 massif) — "kingdom" = NOT CONFIRMED (no settlement / ruler invented) | TASK 05 `GREAT_NORTHERN_RANGE_R03_v002`, `MOUNTAIN_NW01_v002` | ✅ references by altitude zone |
| Ancient City surroundings | **C-01…C-03** ancient city sites (on large rivers near coasts) | markers only (TASK 04) | concept §4.4 |
| Green Plains | **R-06** Southern Grasslands | TASK 04 blockout, main world v002 | concept §4.5 |
| Crystal Lakes | **R-08** Lake District | TASK 04 blockout, main world v002 | concept §4.6 |
| Golden Desert | **R-04** Western Desert & Wastelands | TASK 05 `DESERT_R04_v002` | concept §4.7 |
| Forbidden Lands | **R-05** Forbidden Region (crater) | TASK 05 `FORBIDDEN_R05_v002` | concept §4.8 |
| Hidden Underground | **CV-01…CV-05** cave systems | entrance only (R03 cave, TASK 05) | concept §4.9 |
| Sky Realms | **not on the map — NOT CONFIRMED** | — | §4.10: nothing designed until the Director defines them |

## 2. Global ecosystem rules (apply to every region)

1. **Climate logic (World Bible, proposal):** wet east / dry west (rain shadow) → forests east, desert + wasteland west; colder north
   and altitude. Vegetation follows it: lush broadleaf + moss in the wet east (R-02), drought plants in the west (R-04).
2. **Altitude zonation (true scale, metres a.s.l.)** — matches the TASK 05 terrain (scatter tree line = 3 550 m):

   | Zone | Altitude | Vegetation |
   |---|---|---|
   | Valley / foothill | 300–1 500 m | broadleaf (peepal, oak, rhododendron), chir pine on dry slopes, bamboo in moist hollows, meadows |
   | M1 montane forest | 1 500–3 000 m | deodar, Himalayan spruce, (silver fir — milestone 2) |
   | M2 tree line | 3 000–3 550 m | Himalayan birch, wind-bent pine (krummholz), rhododendron thickets |
   | M3 alpine | 3 550–4 500 m | juniper mats, dwarf rhododendron, tussock grass, alpine flowers, cushion plants |
   | M4 nival | > 4 500 m | rock, lichen, snow — no plants |

3. **Water rule:** aquatic plants only in/at still or slow water (lotus + water-lily in ponds and lake bays, reed-mace / kans on
   margins and river bars); never on fast streams or waterfalls (there: moss + ferns on wet rocks).
4. **Slope rule:** trees ≤ 35–40° (TASK 05 scatter uses Slope Max 40°), shrubs ≤ 45°, grass ≤ 50°, moss / lichen any slope; cliffs bare.
5. **Density / layers:** forests always have layers (canopy → understorey → shrubs → ground) and gaps; open land = clusters, not grids.
   Believable densities (adult trees per hectare): old forest 150–400, valley groves 40–120, open meadow 0–5, tree line 10–60.
6. **Scale:** every asset is real-world size (1 unit = 1 m) and was checked against a 1.75 m human figure (sheets).
7. **Fantasy plants:** max ~5 % of the trees of a region, only in R-02 (and later, if approved, in Sky Realms / Underground);
   every fantasy plant carries `t6_label = PROPOSED FANTASY`. Glow / bioluminescence is **off** in production until approved.
8. **Colour:** each region keeps the World Bible colour key (Ashram = warm green + golden light, Enchanted = teal-green,
   Mountain = dark green-blue + white + grey, Desert = gold / ochre, Forbidden = ash grey / purple-black).

## 3. Tree library (brief §2) — category → species

`✅` = real 3D model built in milestone 1 (sheet in `03_assets/vegetation/sheets/`) · `⬜` = planned for full production.

| Category | Species (label) | Region | Height / canopy (hero) | |
|---|---|---|---|---|
| Ancient trees | Ancient Peepal — *Ficus religiosa* (SI) | R-01 | 24 m / 28 × 35 m | ✅ |
| | Ancient Moss Oak — *Quercus robur*-inspired (SI) | R-02 | 27 m / 40 × 43 m | ✅ |
| Giant trees | Giant Elder — kauri + giant sequoia inspired (SI) | R-02 | 67 m / 54 × 52 m, trunk Ø ≈ 9 m with buttresses | ✅ |
| Tall forest trees | Deodar Cedar — *Cedrus deodara* (SI) | R-01 / M1 | 35 m | ✅ |
| | Teal Beech — *Fagus*-inspired (SI) | R-02 | 41 m | ✅ |
| Small trees | Tree Rhododendron (Burans) — *R. arboreum* (SI), crimson flowers | R-01 | 9.5 m | ✅ |
| | Old Yew — *Taxus*-inspired (SI) | R-02 understorey | 10 m | ✅ |
| | Himalayan Birch — *Betula utilis* (SI), white bark | R-03 M2 | 14 m | ✅ |
| Bushy trees | Giant Clumping Bamboo — *Dendrocalamus* (SI) | R-01 moist hollows | 15 m clump | ✅ |
| Broadleaf | Banj Oak — *Quercus leucotrichophora* (SI) | R-01 | 20 m | ✅ |
| Pine trees | Chir Pine — *Pinus roxburghii* (SI), 25 cm needles | R-01 dry slopes | 30 m | ✅ |
| Mountain trees | Himalayan Spruce — *Picea smithiana* (SI) | R-03 M1 | 31 m | ✅ |
| | Wind-bent Pine (krummholz) — *Pinus wallichiana* form (SI) | R-03 M2 | 6 m | ✅ |
| | Silver fir *Abies pindrow*, blue pine *P. wallichiana* (full form) | R-03 M1 | | ⬜ |
| Tropical trees | coconut / areca palm, banyan, mangrove (coasts, Sagara / Agni archipelagos) | islands, coasts | | ⬜ |
| Dry-region trees | acacia / khejri (*Prosopis cineraria*), date palm at oases, quiver-tree-like aloe (Poly Haven scans) | R-04 | | ⬜ |
| Dead trees | Dead Snag (SI) with bracket fungi | R-02 / R-03 / R-05 | 18 m | ✅ |
| | charred / ash-white dead trees (crater) | R-05 | | ⬜ (TASK 05 has proxies) |
| Rare fantasy trees | **Veil Willow** (PF) — silver-teal curtains to the ground | R-02 pools | 21 m | ✅ proposal |
| | **Spiral-root Tree** (PF) — trunk on a cage of stilt roots, spiral bark | R-02 wet hollows | 27 m | ✅ proposal |
| | **Lantern Tree** (PF) — umbrella of fan leaves + hanging pale seed-pods (faint glow = option) | R-02 glades | 19 m | ✅ proposal |

Shrubs built: Himalayan Barberry (R-01), Tulsi (R-01, cultivated in the Ashram — PROPOSED placement), Dwarf Juniper (R-03 M3),
Dwarf Rhododendron (R-03 M3). TASK 05 Poly Haven trees (fir, pine, broadleaf scans) stay in use for mid / far forest mass.

## 4. Region-specific ecosystems (brief §4)

### 4.1 ASHRAM VALLEY (R-01) — "green, gentle, sacred" ✅ concept built
Warm-temperate Himalayan-foothill valley (~700–900 m) — open meadows, groves, forest ring, rivers and the Ashram (approved layout).
* **Landmark:** one ancient Peepal (lone, open ground; proposal: near the Ashram / training-ground edge — exact spot = Director).
* **Groves:** Banj oak (moist slopes, streams) + Rhododendron at grove edges (crimson in spring) + Barberry along paths.
* **Slopes:** Chir pine on the dry sunny south slopes (grass understorey, needle litter); Deodar ring on the cooler upper slopes.
* **Moist hollows / streams:** Bamboo clumps, sword ferns, moss cushions, brown mushrooms.
* **Meadows:** meadow grass + buttercup, drumstick primula, wild daisy; dry path-edge grass on paths and the training ground edge.
* **Water:** kans grass on river bars (white plumes in autumn), reed-mace at pond / slow river margins, lotus only in still water.
* **Cultivated (PROPOSED):** tulsi + marigold only inside the Ashram courtyard / gardens.
* Palette: `#3E7A2A` peepal green · `#2F5A2E` oak · `#7C9A3C` chir yellow-green · `#4E6E5A` deodar blue-green · `#C0182B` burans red.

### 4.2 ENCHANTED FOREST (R-02) — "old, deep, layered, teal" ✅ tree collection built
* **Emergent layer (40–70 m):** Giant Elders, widely spaced (5–15 per km²), buttress roots, beard moss.
* **Main canopy (25–40 m):** Teal Beech (smooth grey-green columns) + Ancient Moss Oak (huge low limbs, moss).
* **Understorey (5–12 m):** Old Yew, young beech; **ground:** giant ferns, deep moss carpet, fallen giants (TASK 05 logs), roots.
* **Hanging:** lianas (Hanging Vine) + beard moss on the oaks / elders.
* **Fantasy proposals (≤ 5 %, clustered at water and glades):** Veil Willow (pools), Spiral-root Tree (wet hollows),
  Lantern Tree (glades), Glowcap mushrooms (on logs). If the Director prefers a purely natural forest, these are simply left out.
* Palette: `#1F4F44` elder teal · `#2F6A4A` beech · `#2C5A3C` oak · `#17382C` yew · `#4F8F86` veil willow · `#3F6A3A` moss.

### 4.3 MOUNTAIN KINGDOM (R-03) — "harsh, sparse, by altitude" ✅ references built
Zones M1–M4 (§2). M1 dense spruce (+ deodar low); M2 birch groves in gullies, krummholz on ridges, rhododendron thickets;
M3 juniper mats, dwarf rhododendron, tussock grass, gentian, edelweiss, blue poppy, cushion plants between boulders;
M4 rock + lichen + snow. **No fantasy species.** "Kingdom" (settlements / ruler) is NOT CONFIRMED — vegetation only.
* Palette: `#1F3F33` spruce · `#E9E4DA` birch bark · `#3E5E4E` juniper · `#2E5ED8` gentian · `#5A9AE0` blue poppy · `#A9AE8E` lichen.

### 4.4 ANCIENT CITY SURROUNDINGS (C-01…C-03) — concept, milestone 2+
River plains near the coast: sacred groves (banyan, peepal), avenue trees (neem, mango), overgrown ruins (strangler figs on
walls, ivy, moss, grass in cracks), river reeds. Whether the cities are inhabited / ruined = NOT CONFIRMED → both looks proposed.

### 4.5 GREEN PLAINS (R-06 Southern Grasslands) — concept
Tall + short grass mosaic, wildflower drifts, scattered lone trees (acacia-like, banyan, neem), shrub islands on low hills,
river galleries of willow / poplar. Density: trees 0–5 / ha; grass everywhere except paths, rock and water.

### 4.6 CRYSTAL LAKES (R-08 Lake District) — concept
Clear lakes between forests: water-lily + lotus bays, reed belts, sedges, willows and alders on shores, moss on wet rocks,
mixed broadleaf-conifer forest behind. "Crystal" = clear water (no crystals invented; a crystal-plant idea needs approval).

### 4.7 GOLDEN DESERT (R-04) — concept
Sparse: dune crests bare; interdune hollows — grass tufts, saltbush; wadis — acacia / khejri trees, oleander; playas bare;
oases — date palms, reeds (only where TASK 05 wadi / playa masks allow). Poly Haven Namaqualand scans (quiver tree, succulents,
dry shrubs) available for the dry palette. Density ≤ 1 tree / ha outside wadis.

### 4.8 FORBIDDEN LANDS (R-05) — concept
Almost dead: charred / ash-white snags, grey lichen, thorny dead shrubs, a few hardy grasses on the outer rim only; the crater
floor and lake shore lifeless (approved TASK 05 look: dark ash, black lake, no lava, no glow). Why the land is dead = NOT CONFIRMED.

### 4.9 HIDDEN UNDERGROUND (CV caves) — concept
Moss + ferns only in the daylight zone of entrances; deeper: fungi on wet rock, root curtains from the surface, pale cave moss.
Bioluminescent fungi = PROPOSED FANTASY option only.

### 4.10 SKY REALMS — NOT CONFIRMED
Not on the approved map; no description in any brief. Nothing designed. Needs the Director's definition (do they exist, what are
they — floating islands? a dimension?) before any vegetation.

## 5. Plant & flower library (brief §3) — milestone 1

| Category | Built (✅) | Planned (⬜) |
|---|---|---|
| Grass | meadow grass, dry path-edge grass, kans grass (plumes), alpine tussock | short lawn (Ashram), desert tufts, sedges |
| Small plants / herbs | tulsi (cultivated) | nettle, sorrel, celandine (Poly Haven scans available) |
| Wildflowers | buttercup, drumstick primula, wild daisy, marigold (cultivated) | lavender-blue iris, wild rose, lupin |
| Bushes | barberry, tulsi, juniper, dwarf rhododendron | oleander, saltbush, wild raspberry |
| Ferns | valley sword fern, giant forest fern | maidenhair (wet rocks), tree fern (R-02 option) |
| Vines / roots | hanging liana; tree roots are part of every tree (buttress / surface / stilt / aerial) | ivy (ruins), strangler fig |
| Moss | cushion moss, moss carpet, alpine cushion plant; moss + lichen layers in every bark material | wall moss for ruins |
| Mushrooms | brown woodland mushrooms, bracket fungi (on the dead snag), Glowcap (PF) | |
| Aquatic | sacred lotus, reed-mace / cattail | water-lily, duckweed, submerged weed |
| Desert plants | — | succulents, cacti-like euphorbia, dry thorn shrubs (milestone 2, R-04) |
| Mountain vegetation | tussock, gentian, edelweiss, blue poppy, cushion plant, juniper, dwarf rhododendron | lichen boulders (TASK 05 rocks + lichen shader) |

Scale + colour reference: every plant sheet shows a 10 cm ground grid; every tree sheet a height ruler + 1.75 m figure;
every asset has its palette (HEX) on its sheet and as `t6_palette` custom property.

## 6. Natural environment details (brief §6)
Already in the TASK 05 nature library (`02_world/3d_world/14_NATURE_LIBRARY/`, Poly Haven CC0): fallen logs (2), stumps, root
clusters, pine roots, bark debris, dry branches, mossy rocks, boulders, rock faces, grass clusters, dandelion, nettle.
TASK 06 adds: moss cushions / carpet, mushrooms, hanging liana, beard-moss strands (on trees), bracket fungi, lotus + reeds.
**Planned (milestone 2):** leaf-litter decals (per species, from the leaf atlases), fallen branches of each species, broken
giant log (Giant Elder), floating leaves / petals, ivy on rocks.

## 7. Wildlife proposal (brief §5) — PROPOSAL ONLY, no models yet
Ordinary animals only (no intelligent species, monsters or story creatures). All realistic, region-appropriate; the Director picks.

| Region | Birds | Insects | Small mammals | Larger animals | Aquatic |
|---|---|---|---|---|---|
| R-01 Ashram Valley | sparrows, myna, rose-ringed parakeet, peacock (open ground), kingfisher (river), crows | butterflies (common Mormon, blue tiger), bees at flowers, dragonflies at the pond, fireflies (dusk) | squirrels, hares, langur monkeys in the groves | spotted deer at the forest edge (distant) | small fish + frogs in the pond |
| R-02 Enchanted Forest | owls, woodpeckers, hornbill (canopy), small songbirds | moths, beetles on logs, many butterflies in sun patches, fireflies | flying squirrel, red panda-like climbers | deer, wild boar (distant, rare) | newts, frogs at pools |
| R-03 Mountain Kingdom | eagles / lammergeier (soaring), Himalayan monal (colourful pheasant), snowcock | few: bumblebees, alpine butterflies | pika, marmot | Himalayan tahr / blue sheep on cliffs, snow leopard (very rare, distant) | trout in streams |
| R-06 Green Plains | larks, kites, flocks of starlings | grasshoppers, butterflies | hares, mongoose | blackbuck / antelope herds, wild horses | — |
| R-08 Crystal Lakes | herons, egrets, ducks, cranes | dragonflies, damselflies | otters | — | fish, turtles |
| R-04 Golden Desert | vultures, desert sparrows | beetles | desert fox, gerbils | camels (oasis, if inhabited — NOT CONFIRMED) | — |
| R-05 Forbidden Lands | crows / ravens only (or none) | none | none | none | none |

Use in film: as ambient life (mostly far / mid shots, flocks, butterflies near camera). Production = low-poly rigged creatures +
particle flocks, **only after approval** of this list (Q5).

## 8. Technical standard (brief §7) — how the assets are built

* **Blender 4.5.16 LTS** module (Director's PC = 4.5); scripts are pure `bpy` + `numpy`.
* **Generator:** `03_assets/vegetation/scripts/t6kit.py` — species trees from parameters (`t6_species.py`): trunk flare + buttress
  lobes, multi-leader splits, clumps (bamboo / shrubs), whorls (conifers), weeping, twisted trunks, surface / buttress / stilt /
  aerial roots, phyllotaxis, gravity / phototropism, crown-shape envelopes, ground floor guard (limbs never go through the ground).
  Plants: `t6_plants.py` (grass blades, herbs with geometry leaves + flowers, ferns with real pinnae, lotus, reeds, moss, fungi, vines).
* **Geometry:** tube rings 28 (big trunk) → 3 sides (twigs); leaf cards folded (4 tris), 4 atlas variants, crown-shaped custom
  normals (soft, volumetric canopy shading). Budgets (hero LOD0): big trees 150–500 k tris, medium 50–250 k, shrubs 2–10 k,
  plants 0.2–20 k. LOD1 / LOD2 / far proxies = milestone 2 (TASK 05 proxies exist meanwhile).
* **UVs:** bark UVs per branch with constant texel density (u around in whole tiles → no seam, v = metres / tile); cards use their
  atlas tile; plant blades / petals have 0–1 UVs (veins / streaks in the shader).
* **PBR:** bark = Poly Haven CC0 scans (diffuse, roughness, normal, displacement → bump, AO) + per-species tint, moss / lichen
  overlay (up-facing + furrows + lower trunk), birch bleach. Leaves = generated 2K atlases per species (colour + alpha,
  normal, roughness), translucency, per-card hue / value jitter. Procedural: grass gradient, petals, herb veins, moss, fungi, culm.
* **Ground contact:** every trunk foot is sunk 0.3–0.8 m, roots dive under z = 0 → no floating on uneven terrain (QC checks it).
* **Wind-ready:** attributes `wind_trunk`, `wind_branch`, `wind_leaf`, `wind_phase`, `leaf_rand` on every asset (§10).
* **Library:** one `.blend` per region, each species in its own collection at the origin (instancing / scatter ready), metadata
  as custom properties (`t6_label`, `t6_latin`, `t6_height_m`, `t6_canopy_x_m`, `t6_palette`, …), `T6_LINEUP` browse scene.
* **Variants:** generator is seeded — any number of variants per species (`build_tree(spec, seed)`); milestone 1 stores 1 hero
  variant per species (file size); milestone 2: 3–5 variants per species + LODs.

## 9. Procedural vegetation system (brief §8) — plan for milestone 2
Re-use the approved TASK 05 geometry-nodes systems (`NG_T5_HEIGHTFIELD` masks + `NG_T5_SCATTER`: mask / slope / altitude /
cluster / avoid masks / camera culling / near-mid-far LOD) and add a **`NG_T6_ECOSYSTEM`** layer on top:
per-region recipe (species mix + weights, density per hectare, cluster size, min spacing / Poisson radius), slope + altitude
bands (§2), water-distance rule (aquatic + shore plants), canopy-shade rule (ferns / moss under trees, grass in the open),
random scale / rotation / tilt-to-slope, variant + season pick. All values stay editable modifier inputs (no baked placement).

## 10. Wind & environment animation (brief §9) — built
* `T6_WIND_CONTROL` (empty, one per file): **arrow = wind direction**, custom properties **strength** (0 calm · 1 breeze · 3 strong
  · 6+ storm), **gust**, **speed**, **flutter**. Every vegetation object has a `T6_WIND` geometry-nodes modifier (`NG_T6_WIND`)
  whose Strength / Gust / Speed / Flutter are **driven** by those properties (plain single-property drivers — no Python needed).
* Motion layers: trunk sway (height²) · branch sway (accumulated through the hierarchy, per-branch phase) · vertical branch bob ·
  leaf / blade / petal flutter (space-time noise) · gusts (slow noise). Per-object inputs: trunk / branch / leaf amplitudes,
  flexibility (dead trees stiffer). Grass, ferns, reeds, lotus pads (gentle), hanging vines (strong sway) use the same system.
* Test clip: `03_assets/vegetation/renders/WIND_TEST.mp4`. No film scene animation was started.

## 11. Ecosystem consistency (brief §10) — checks (see QC report)
Vegetation ↔ region / altitude table (§2, §4) · tree heights vs. real species and vs. the 1.75 m figure · lowest point of every
asset below z = 0 (no floating) and roots buried · aquatic plants flagged `water=True` (z = 0 = water surface) for the scatter
water rule · believable densities (§2.5) · labels on every asset. Scatter-level checks (density per ha, water distance) come
with milestone 2 when the assets are placed on the terrains.

## 12. Questions for the Director
1. Region mapping OK (Mountain Kingdom = R-03, Green Plains = R-06, Crystal Lakes = R-08, Ancient City = C-01…03)?
2. Sky Realms: do they exist? What are they? (Not on the map — nothing designed.)
3. Enchanted Forest fantasy trees (Veil Willow, Spiral-root, Lantern, Glowcap): keep all / some / none? Glow allowed?
4. Ashram: Peepal as the landmark tree (where?), tulsi + marigold gardens inside the Ashram — OK?
5. Wildlife list (§7): which animals do you want in the film?
6. Season of the film (spring = rhododendron flowers, autumn = kans plumes, winter = snow line lower)?

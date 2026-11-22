# THE GRAND UNIVERSE — ECOSYSTEM & VEGETATION BIBLE · v3 (TASK 06 · Decision Sheet 01 applied · milestone 2, 22 Nov)

> **Decision Sheet 01 (Director, 22 Nov) is applied in this version** — record of every decision + where it was applied:
> `02_world/ecosystem/DECISION_SHEET_01.md`. Status words: **APPROVED** (Director decision) · **PROPOSED** (needs approval) ·
> **PENDING** (waiting for the Director) · CONFIRMED / NOT CONFIRMED (story canon, unchanged).

> **Status: DRAFT for Director approval.** Milestone 1 = concepts + first real 3D assets for **Ashram Valley**, the **Enchanted Forest
> tree collection** and **Mountain Kingdom vegetation references**. Full asset production (more variants, LODs, scattering into the
> terrains, other regions) starts **only after approval**.
>
> Labels used everywhere (sheets, Blender custom properties, inventories):
> **SPECIES-INSPIRED** = modelled on a real species (botanical name given) · **FANTASY (APPROVED R-02)** (PF) = fictional plant, approved for the Enchanted Forest only (Decision 01 §3) ·
> **CONFIRMED / PROPOSED / NOT CONFIRMED** for story and world facts (same as the World Bible).
>
> Rules kept: approved geographical layouts are preserved (no terrain was changed) · no story events invented · no intelligent
> species, monsters or story characters added · every vegetation asset is a **real 3D model** (no illustrations) · Blender 4.5 LTS.

> **Milestone 2 (22 Nov, session 5) — full production of the remaining TASK 06 scope** (Director: "jitne bhi task bache hai … un sab
> ko pura karo"): realism v3 on every asset + natural camera look · all remaining regions (R-06, R-08, R-04, R-05, C-sites, caves) ·
> Mountain Kingdom silver fir + blue pine · natural details · 3 variants + LOD1 / LOD2 / impostor LOD3 per species · the
> **NG_T6_ECOSYSTEM** scatter system · populated region files on the approved TASK 05 terrain (TASK 05 untouched) · previews · QC.
> Summary of what was built: §13. Still PENDING with the Director: wildlife selection, Sky Realms map position, exact Peepal /
> garden spots (PROPOSED in the populated Ashram file).

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
| 8 | Procedural scattering | `NG_T6_ECOSYSTEM` (§9) + populated region files (§13) | ✅ milestone 2 |
| 9 | Wind animation setup | `NG_T6_WIND` + `T6_WIND_CONTROL` in every library, test clip | ✅ built |
| 10 | Preview renders | `03_assets/vegetation/renders/`, contact sheet `sheets/T6_SHEET_M1.png` | ✅ |
| 11 | Technical QC report | `03_assets/vegetation/qc/T06_QC_REPORT.md` — 337/337 (Blender 4.5), 337/337 (5.3), 25/25 textures | ✅ |

---

## 1. Region mapping (brief name → approved map rev 01 code)

The TASK 06 brief uses new names for some regions. They are mapped to the regions that already exist on the approved blockout
(map rev 01 = PROPOSAL, layout preserved). Mapping **APPROVED for environment production** (Decision Sheet 01 §1); IDs verified against
`02_world/3d_world/01_GEOGRAPHY/data/world_features.json` + `02_world/map_v2/data/features.json`.

| TASK 06 brief | Map rev 01 | Where / terrain already built | Vegetation in milestone 1 |
|---|---|---|---|
| Ashram Valley | **R-01** Ashram Valley (CONFIRMED location, PROPOSED position) | TASK 05 valley v002 (2 m–400 m LODs) | ✅ full concept library |
| Enchanted Forest | **R-02** Enchanted Forest | TASK 05 `ENCHANTED_FOREST_R02_v002` | ✅ tree collection + key ground plants |
| Mountain Kingdom | **R-03** Great Northern Range (+ NW01 massif) — mapping **APPROVED**; "kingdom" (settlement / ruler) = NOT CONFIRMED | TASK 05 `GREAT_NORTHERN_RANGE_R03_v002`, `MOUNTAIN_NW01_v002` | ✅ references by altitude zone |
| Ancient City surroundings | **C-01, C-02, C-03** — mapping **APPROVED**; three **separate** archaeological sites (no shared city / history invented) | markers only (TASK 04) | concept §4.4 |
| Green Plains | **R-06** Southern Grasslands — mapping **APPROVED** | TASK 04 blockout, main world v002 | concept §4.5 |
| Crystal Lakes | **R-08** Lake District — mapping **APPROVED** | TASK 04 blockout, main world v002 | concept §4.6 |
| Golden Desert | **R-04** Western Desert & Wastelands | TASK 05 `DESERT_R04_v002` | concept §4.7 |
| Forbidden Lands | **R-05** Forbidden Region (crater) | TASK 05 `FORBIDDEN_R05_v002` | concept §4.8 |
| Hidden Underground | **CV-01…CV-05** cave systems | entrance only (R03 cave, TASK 05) | concept §4.9 |
| Sky Realms | **PROPOSED region of the main world** (NOT a dimension) — design direction APPROVED, story role NOT CONFIRMED, map position PENDING | — | §4.10 |

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
7. **Fantasy plants (APPROVED, Decision 01 §3):** Enchanted Forest only — ≈ 20–30 % of its trees (art-direction target), clustered by
   habitat; label `t6_label = FANTASY (APPROVED R-02)`. Glow **allowed but subtle**: emission ≤ 1.0, night only, never every tree
   (`ENCHANTED_FOREST_VEGETATION_REFERENCE.md`). Other regions: no fantasy plants unless approved.
9. **Season (APPROVED, Decision 01 §6):** Spring is the primary season for all connected scenes (`SEASON_REFERENCE_SPRING.md`).
8. **Colour:** each region keeps the World Bible colour key (Ashram = warm green + golden light, Enchanted = teal-green,
   Mountain = dark green-blue + white + grey, Desert = gold / ochre, Forbidden = ash grey / purple-black).

## 3. Tree library (brief §2) — category → species

`✅` = real 3D model built in milestone 1 (sheet in `03_assets/vegetation/sheets/`) · `⬜` = planned for full production.

| Category | Species (label) | Region | Height / canopy (hero) | |
|---|---|---|---|---|
| Ancient trees | Ancient Peepal — *Ficus religiosa* (SI) | R-01 | 24 m / 28 × 34 m | ✅ |
| | Ancient Moss Oak — *Quercus robur*-inspired (SI) | R-02 | 24 m / 31 × 34 m | ✅ |
| Giant trees | Giant Elder — kauri + giant sequoia inspired (SI) | R-02 | 67 m / 54 × 52 m, trunk Ø ≈ 9 m with buttresses | ✅ |
| Tall forest trees | Deodar Cedar — *Cedrus deodara* (SI) | R-01 / M1 | 35 m | ✅ |
| | Teal Beech — *Fagus*-inspired (SI) | R-02 | 35 m | ✅ |
| Small trees | Tree Rhododendron (Burans) — *R. arboreum* (SI), crimson flowers | R-01 + R-03 M1 | 8 m | ✅ |
| | Old Yew — *Taxus*-inspired (SI) | R-02 understorey | 9 m | ✅ |
| | Himalayan Birch — *Betula utilis* (SI), white bark | R-03 M2 | 12 m | ✅ |
| Bushy trees | Giant Clumping Bamboo — *Dendrocalamus* (SI) | R-01 moist hollows | 15 m clump | ✅ |
| Broadleaf | Banj Oak — *Quercus leucotrichophora* (SI) | R-01 | 17 m | ✅ |
| Pine trees | Chir Pine — *Pinus roxburghii* (SI), 25 cm needles | R-01 dry slopes | 27 m | ✅ |
| Mountain trees | Himalayan Spruce — *Picea smithiana* (SI) | R-03 M1 | 31 m | ✅ |
| | Wind-bent Pine (krummholz) — *Pinus wallichiana* form (SI) | R-03 M2 | 6 m | ✅ |
| | West Himalayan silver fir — *Abies pindrow* (SI) | R-03 M1 top | 37 m | ✅ M2 |
| | Blue pine — *Pinus wallichiana* full form (SI) | R-03 M1 clearings | 31 m | ✅ M2 |
| Tropical / lowland trees | Coconut palm — *Cocos nucifera* (SI, palm generator: curved trunk, drooping fronds, nut clusters) | C-sites coast | 16 m | ✅ M2 |
| | Banyan — *Ficus benghalensis* (SI), 26 aerial prop roots | R-06 + C-site groves | 21 m / 40 × 45 m | ✅ M2 |
| | Neem — *Azadirachta indica* (SI) | R-06 + C-site avenues | 16 m | ✅ M2 |
| | Mango — *Mangifera indica* (SI), copper new spring leaves | C-sites + R-06 villages | 15 m | ✅ M2 |
| | areca palm, mangrove (islands / coasts — no hero terrain yet) | islands, coasts | | ⬜ later (islands task) |
| Waterside trees | White willow — *Salix alba* (SI, natural, NOT the R-02 Veil Willow) · Himalayan alder — *Alnus nepalensis* (SI) | R-08 shores | 18 m · 20 m | ✅ M2 |
| Dry-region trees | Khejri — *Prosopis cineraria* (SI) · Umbrella thorn acacia — *Vachellia tortilis* (SI) · Date palm — *Phoenix dactylifera* (SI, oases only, dead-frond skirt) | R-04 (+ R-06 dry edge) | 8 m · 9 m · 14 m | ✅ M2 |
| Dead trees | Dead Snag (SI) with bracket fungi | R-02 / R-03 / R-05 | 19 m | ✅ |
| | Charred dead tree (SI) — black cracked bark, ash-grey patches, leafless | R-05 rim | 12 m | ✅ M2 |
| Rare fantasy trees | **Veil Willow** (PF) — silver-teal curtains to the ground | R-02 pools | 18 m | ✅ approved R-02 |
| | **Spiral-root Tree** (PF) — trunk on a cage of stilt roots, spiral bark | R-02 wet hollows | 23 m | ✅ approved R-02 |
| | **Lantern Tree** (PF) — umbrella of fan leaves + hanging pale seed-pods (subtle glow, night only) | R-02 glades | 15 m | ✅ approved R-02 |

Shrubs built: Himalayan Barberry (R-01), Tulsi (R-01, Ashram garden ONLY — APPROVED), Dwarf Juniper (R-03 M3),
Dwarf Rhododendron (R-03 M3) · milestone 2: wild ber bush (R-06 / R-04 edge), aak *Calotropis procera* (R-04), dead thorn shrub (R-05 / R-04). TASK 05 Poly Haven trees (fir, pine, broadleaf scans) stay in use for mid / far forest mass.

## 4. Region-specific ecosystems (brief §4)

### 4.1 ASHRAM VALLEY (R-01) — "green, gentle, sacred" ✅ concept built
Warm-temperate Himalayan-foothill valley (~700–900 m) — open meadows, groves, forest ring, rivers and the Ashram (approved layout).
* **Landmark (APPROVED):** ONE prominent Peepal near the Ashram's main courtyard with a stone sitting platform — placement in
  `02_world/ashram/ASHRAM_LANDSCAPING_PLAN.md` (courtyard centre = PROPOSED exact spot).
* **Groves:** Banj oak (moist slopes, streams) + Rhododendron at grove edges (crimson in spring) + Barberry along paths.
* **Slopes:** Chir pine on the dry sunny south slopes (grass understorey, needle litter); Deodar ring on the cooler upper slopes.
* **Moist hollows / streams:** Bamboo clumps, sword ferns, moss cushions, brown mushrooms.
* **Meadows:** meadow grass + buttercup, drumstick primula, wild daisy; dry path-edge grass on paths and the training ground edge.
* **Water:** kans grass on river bars (**spring = green clumps, no plumes**; plumes are autumn, not a primary feature), reed-mace at
  pond / slow river margins, lotus only in still water.
* **Cultivated (APPROVED):** Tulsi + Marigold **only in the Ashram garden** — never in forests, cities or other regions (garden layout:
  `ASHRAM_LANDSCAPING_PLAN.md`).
* Palette: `#3E7A2A` peepal green · `#2F5A2E` oak · `#7C9A3C` chir yellow-green · `#4E6E5A` deodar blue-green · `#C0182B` burans red.

### 4.2 ENCHANTED FOREST (R-02) — "old, deep, layered, teal" ✅ tree collection built
* **Emergent layer (40–70 m):** Giant Elders, widely spaced (5–15 per km²), buttress roots, beard moss.
* **Main canopy (25–40 m):** Teal Beech (smooth grey-green columns) + Ancient Moss Oak (huge low limbs, moss).
* **Understorey (5–12 m):** Old Yew, young beech; **ground:** giant ferns, deep moss carpet, fallen giants (TASK 05 logs), roots.
* **Hanging:** lianas (Hanging Vine) + beard moss on the oaks / elders.
* **Mix (APPROVED):** ≈ 70–80 % natural trees, ≈ 20–30 % fantasy varieties — Veil Willow (pools), Spiral-root Tree (wet hollows, unusual
  roots, twisted trunk), Lantern Tree (glades); Glowcap on selected logs. Giants in selected areas only. Subtle bioluminescence on
  selected moss / plants, limited glow at night. Shares + glow limits: `ENCHANTED_FOREST_VEGETATION_REFERENCE.md`.
* Palette: `#1F4F44` elder teal · `#2F6A4A` beech · `#2C5A3C` oak · `#17382C` yew · `#4F8F86` veil willow · `#3F6A3A` moss.

### 4.3 MOUNTAIN KINGDOM (R-03) — "harsh, sparse, by altitude" ✅ references built
Zones M1–M4 (§2). M1 dense spruce (+ deodar low); M2 birch groves in gullies, krummholz on ridges, rhododendron thickets;
M3 juniper mats, dwarf rhododendron, tussock grass, gentian, edelweiss, blue poppy, cushion plants between boulders;
M4 rock + lichen + snow. **Spring: red Burans in the lower montane belt (M1)** (APPROVED season direction). **No fantasy species.** "Kingdom" (settlements / ruler) is NOT CONFIRMED — vegetation only.
* Palette: `#1F3F33` spruce · `#E9E4DA` birch bark · `#3E5E4E` juniper · `#2E5ED8` gentian · `#5A9AE0` blue poppy · `#A9AE8E` lichen.

### 4.4 ANCIENT CITY SURROUNDINGS (C-01, C-02, C-03) — ✅ built (milestone 2): mango, coconut palm, ivy curtain, ruin moss, crack grass (+ banyan / neem / peepal / reeds from R-06 / R-01 / R-08)
Mapping APPROVED. The three sites are **separate archaeological sites** — their history, inhabitants and relationship are NOT CONFIRMED.
River plains near the coast: sacred groves (banyan, peepal), avenue trees (neem, mango), overgrown ruins (strangler figs on
walls, ivy, moss, grass in cracks), river reeds. Whether the cities are inhabited / ruined = NOT CONFIRMED → both looks proposed.

### 4.5 GREEN PLAINS (R-06 Southern Grasslands) — ✅ built (milestone 2): banyan, neem, umbrella acacia, ber bush, tall grass, doob grass, wild mustard, globe thistle, white clover
Tall + short grass mosaic, wildflower drifts, scattered lone trees (acacia-like, banyan, neem), shrub islands on low hills,
river galleries of willow / poplar. Density: trees 0–5 / ha; grass everywhere except paths, rock and water.

### 4.6 CRYSTAL LAKES (R-08 Lake District) — ✅ built (milestone 2): white willow, alder, white water-lily, sedge, reed (spring, no plumes), wet-rock moss
Clear lakes between forests: water-lily + lotus bays, reed belts, sedges, willows and alders on shores, moss on wet rocks,
mixed broadleaf-conifer forest behind. "Crystal" = clear water (no crystals invented; a crystal-plant idea needs approval).

### 4.7 GOLDEN DESERT (R-04) — ✅ built (milestone 2): khejri, date palm, aak (Calotropis), candelabra euphorbia, sewan grass (+ acacia, ber, dead thorn) · populated file on DESERT_R04_v002
Sparse: dune crests bare; interdune hollows — grass tufts, saltbush; wadis — acacia / khejri trees, oleander; playas bare;
oases — date palms, reeds (only where TASK 05 wadi / playa masks allow). Poly Haven Namaqualand scans (quiver tree, succulents,
dry shrubs) available for the dry palette. Density ≤ 1 tree / ha outside wadis.

### 4.8 FORBIDDEN LANDS (R-05) — ✅ built (milestone 2): charred dead tree, dead thorn shrub, grey crust lichen, hardy rim grass · populated file on FORBIDDEN_R05_v002
Almost dead: charred / ash-white snags, grey lichen, thorny dead shrubs, a few hardy grasses on the outer rim only; the crater
floor and lake shore lifeless (approved TASK 05 look: dark ash, black lake, no lava, no glow). Why the land is dead = NOT CONFIRMED.

### 4.9 HIDDEN UNDERGROUND (CV caves) — ✅ built (milestone 2): pale cave-mouth moss, pale cave fungi (NO glow), root curtain
Moss + ferns only in the daylight zone of entrances; deeper: fungi on wet rock, root curtains from the surface, pale cave moss.
Bioluminescent fungi = PROPOSED option only (Decision 01 approved subtle glow for R-02, not for caves).

### 4.10 SKY REALMS — PROPOSED REGION of the main world (design direction APPROVED, Decision 01 §2)
Not a separate dimension. Approved direction: large floating islands of natural rock, selected islands with forests + waterfalls,
ancient-looking structures, clouds + atmospheric depth between islands, some natural bridges / suspended land formations, strong visual
connection with the main world. Vegetation proposal: the same spring flora as the main world below (R-01 / R-02 / R-03 species by
island altitude), moss + ferns + small trees on island rims, waterfall spray zones with moss; no new species yet.
**NOT established:** travel routes, inhabitants, kingdoms, political systems, story events, map position (PENDING).

## 5. Plant & flower library (brief §3) — milestone 1 + milestone 2

| Category | Built (✅) | Planned (⬜) |
|---|---|---|
| Grass | meadow grass, dry path-edge grass, kans grass (plumes = autumn) + SPRING kans, alpine tussock · M2: tall plains grass, doob (lawn), sewan desert grass, hardy rim grass, crack grass, sedge, spring reed | — |
| Small plants / herbs | tulsi (cultivated) | nettle, sorrel, celandine (Poly Haven scans available) |
| Wildflowers | buttercup, drumstick primula, wild daisy, marigold (cultivated) · M2: wild mustard (spring yellow), globe thistle, white clover | iris, wild rose, lupin |
| Bushes | barberry, tulsi, juniper, dwarf rhododendron · M2: ber, aak (Calotropis), dead thorn shrub | oleander, saltbush |
| Ferns | valley sword fern, giant forest fern | maidenhair (wet rocks), tree fern (R-02 option) |
| Vines / roots | hanging liana; tree roots on every tree · M2: ivy curtain on walls, ground ivy, root curtain (caves), banyan prop roots | strangler fig |
| Moss | cushion moss, moss carpet, alpine cushion plant; moss + lichen in every bark · M2: ruin moss, wet-rock moss, pale cave moss, grey crust lichen, glow moss (PF, R-02) — moss shader v3.1 (shoots + fuzz) | — |
| Mushrooms | brown woodland mushrooms, bracket fungi (dead snag, giant log), Glowcap (PF) · M2: pale cave fungi (no glow) | |
| Aquatic | sacred lotus, reed-mace / cattail · M2: white water-lily (flowers at the surface, petioles to the lake bed), sedge, spring reed, floating leaves | duckweed, submerged weed |
| Desert plants | M2: candelabra euphorbia (ribbed, spines, blunt tips), aak, sewan grass, dead thorn shrub | saltbush |
| Mountain vegetation | tussock, gentian, edelweiss, blue poppy, cushion plant, juniper, dwarf rhododendron | lichen boulders (TASK 05 rocks + lichen shader) |

Scale + colour reference: every plant sheet shows a 10 cm ground grid; every tree sheet a height ruler + 1.75 m figure;
every asset has its palette (HEX) on its sheet and as `t6_palette` custom property.

## 6. Natural environment details (brief §6)
Already in the TASK 05 nature library (`02_world/3d_world/14_NATURE_LIBRARY/`, Poly Haven CC0): fallen logs (2), stumps, root
clusters, pine roots, bark debris, dry branches, mossy rocks, boulders, rock faces, grass clusters, dandelion, nettle.
TASK 06 adds: moss cushions / carpet, mushrooms, hanging liana, beard-moss strands (on trees), bracket fungi, lotus + reeds.
**Built in milestone 2 (`T6_VEG_NATURAL_DETAILS_v001.blend`, `t6_details.py`):** leaf litter (last year's decomposing leaves +
fresh spring windfall on top, twigs), needle litter + cones, fallen branches (splintered ends with pale inner wood = own material),
giant uprooted log (moss on top, bracket fungi, splintered break, root plate with real soil), ground ivy carpet, floating leaves
(drift to the lee side). Every piece lies ON the ground / water (gravity) — QC checks it.

## 7. Wildlife proposal (brief §5) — PROPOSAL ONLY, selection PENDING
**Decision 01 §5:** selection NOT finalized. Selection sheet (60 animals = this complete list, nothing added):
`02_world/ecosystem/WILDLIFE_SELECTION_SHEET.md` / `.png`. No wildlife assets until the Director selects.

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
* **Variants + LODs (milestone 2):** 3 variants per species (seed 0 hero + `T6_VEG_<R>_VARIANTS_v001.blend` seeds 1, 2; giants
  stored at LOD1 density) · `T6_VEG_<R>_LODS_v001.blend`: LOD1 (½ ring sides, 40 % cards × 1.5 size, same skeleton), LOD2 (⅓ sides,
  18 % cards × 2.2, finest twigs dropped), LOD3 impostor (2 crossed cards with the front / side alpha renders, `textures/impostors/`);
  plants LOD1 (≈ 40 % blades / stems). Distance bands in the scatter: 0–70 m LOD0 · –260 m LOD1 · –1.2 km LOD2 · beyond LOD3.
* **Realism v3 / v3.1 (Director 22 Nov):** natural (less saturated) foliage with per-card variation, ~5 % drying leaves, faint dust,
  thatch at grass bases lying ON the ground, irregular crinkled matte petals, matte stems, irregular roots with soil, moss with
  shoots + fuzz (no CG cells); render look = natural camera (AgX Base Contrast + gentle S-curve), not Medium High Contrast.

## 9. Procedural vegetation system (brief §8) — ✅ built (milestone 2): `NG_T6_ECOSYSTEM`
`03_assets/vegetation/scripts/t6_ecosystem.py`. One scatter object = one layer (one species: hero + 2 variants + LODs), built on
the approved TASK 05 logic (`NG_T5_HEIGHTFIELD` mask attributes m_forest / m_grove / m_dry / m_wet / m_path / m_gravel / m_scree /
m_rock / m_snow / m_bare …, slope, altitude, clusters, camera-cone culling, stable points in animation) plus:
* density per m² (recipes in ha: trees 15–120 / ha, grass 1.5–5 / m²), **Poisson spacing** for trees / shrubs (no intersecting
  canopies), random distribution for the dense ground layers (only culled, masked faces produce points);
* two avoid masks (water, bare rock, paths) + an **exclusion / inclusion zone** (e.g. Ashram: wild trees outside 65 m, lawn
  inside), slope + altitude bands, canopy-shade rule via masks (ferns / moss / litter under trees, grass + flowers in the open);
* random scale / yaw / tilt, partial alignment to the slope (plants, litter), sink by size (trunks never float);
* **4 LOD bands** (hero + variants → LOD1 → LOD2 → impostor) by camera distance;
* **wind (REAL-WORLD MOTION RULE):** instances inside 'Realize Distance' are realized and bent per vertex by `NG_T6_WIND`
  with a per-instance random phase (no two plants in sync); all others tilt with `NG_T6_WIND_INSTANCES` (advected gusts,
  natural frequency ≈ 4 / H, per-instance phase). One `T6_WIND_CONTROL` per file drives every layer.
Instances use the libraries' wind-free `<asset>_SC` copies (same mesh) → wind is applied exactly once.

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
water rule · believable densities (§2.5) · labels on every asset. Scatter-level checks (milestone 2, `t6_pop_qc.py`): nothing floating
(instance bases on the evaluated terrain), Decision 01 rules (ONE Peepal, Tulsi + Marigold only in the garden beds, R-02 fantasy
share 20–30 %, no glow outside R-02), wind moves the realized near plants, TASK 05 files untouched, file sizes.

## 12. Director decisions (Decision Sheet 01, 22 Nov) — status
| # | Question | Decision | Status |
|---|---|---|---|
| 1 | Region mapping | Mountain Kingdom = R-03 · Green Plains = R-06 · Crystal Lakes = R-08 · Ancient City = C-01, C-02, C-03 (separate sites) | **APPROVED** |
| 2 | Sky Realms | proposed region **within the main world** (not a dimension); floating-island design direction | **APPROVED direction** · region PROPOSED · map position + story role PENDING |
| 3 | Enchanted Forest fantasy trees + glow | ≈ 70–80 % natural / 20–30 % fantasy; subtle, limited glow at night | **APPROVED** |
| 4 | Ashram Peepal / Tulsi / Marigold | one landmark Peepal near the main courtyard + sitting area; Tulsi + Marigold only in the Ashram garden | **APPROVED** · exact spots PROPOSED |
| 5 | Wildlife | not finalized — selection sheet prepared | **PENDING** (Director selection) |
| 6 | Season | Spring = proposed primary season, consistent across connected scenes | **APPROVED** |

## 13. MILESTONE 2 — what was built (22 Nov, session 5)
| Item | Where | Status |
|---|---|---|
| Hero libraries for 10 regions — **84 assets**: 29 trees, 7 shrubs, 42 plants, 6 natural details | `03_assets/vegetation/library/T6_VEG_<R>_v001.blend` (AV EF MK PL LK DS FB CT CV ND) | ✅ |
| New generators: palm (date / coconut, real leaflet geometry + dead-frond skirt), succulent (ribbed candelabra), ivy on walls, water-lily, natural details | `t6kit_m2.py`, `t6_plants_m2.py`, `t6_details.py` | ✅ |
| 14 new atlases (banyan, neem, acacia, mango, willow, alder, water-lily pad, khejri, aak, silver fir, blue pine, ivy, 2 litter) | `03_assets/vegetation/textures/leaves/` | ✅ |
| Variants (3 per species) + LOD1 / LOD2 / LOD3 impostors | `T6_VEG_<R>_VARIANTS_v001.blend`, `T6_VEG_<R>_LODS_v001.blend`, `textures/impostors/` | ✅ |
| Sheets for every region + contact sheet M2 | `03_assets/vegetation/sheets/<R>/`, `sheets/T6_SHEET_M2.png` | ✅ |
| Ecosystem scatter `NG_T6_ECOSYSTEM` | `t6_ecosystem.py` | ✅ |
| Populated region files (TASK 05 v002 terrain linked, never written): R-01 Ashram Valley (+ ONE Peepal on a PROPOSED chabutra, PROPOSED garden beds with Tulsi + Marigold), R-02 Enchanted Forest (~75 / 25 natural / fantasy), R-03 Mountain Kingdom (M1 forest at the cave entrance), R-04 Golden Desert, R-05 Forbidden Lands | `02_world/ecosystem/populated/T6_POP_R0x_*_v001.blend` (`t6_populate.py`) | ✅ |
| Cinematic previews (T6 eye-level cameras + the approved TASK 05 shot cameras) | `02_world/ecosystem/renders/populated/` | ✅ preview res (4K on the Director's GPU PC) |
| QC: libraries (4.5 + 5.3 + textures) + populated scatter QC | `03_assets/vegetation/qc/T06_QC_REPORT.md` | ✅ |

**Not placed (honest limits):** R-06 / R-08 / C-sites / caves have no TASK 05 hero terrain tile yet (only the coarse world terrain) →
their species are built + sheeted and the recipes are ready; placement happens when those regions get their hero terrain.
Sky Realms (PROPOSED, map position PENDING) re-uses the main-world spring flora (no new species, Decision 01 §2).
Wildlife = selection PENDING (no models). Hanging liana / root curtain / ivy curtain need a branch / ceiling / wall to hang on →
placed per shot, not scattered.

# TASK 06 — Ecosystem & Vegetation Bible · CLOSEOUT (APPROVED + CLOSED, 22 Nov 2026)

> **Director (22 Nov, verbatim):** "Ek kaam kar mai task 6 ko approve kar rha hai aur tune jitne bhi kaam kiye hai uska ek detail summary
> banao taki naye session me whi se suru ho jah pe khatam hua hai bina kuch bhulw"
>
> **Status:** TASK 06 = **APPROVED + CLOSED**. Nothing is running, nothing is pending to render. Next = the Director's TASK 07 brief.
> **Do not rebuild anything listed here** — it is all in git (repo `pratyushgamerz54-oss/animation-studio`, branch `ccr-c375d59d-2qaoyn`;
> PR #2 → `main`). Read this file + `HANDOFF.md` §0 / §0b / §6c in a new session.

---

## 1. Timeline (sessions 4 + 5, 21–22 Nov)

| # | Step | Result |
|---|---|---|
| 1 | TASK 06 brief received (verbatim: `DIRECTOR_INPUTS_TASK06.md` §A) | own procedural vegetation generator (Blender 4.5) |
| 2 | **Milestone 1:** Ashram Valley library, Enchanted Forest tree collection, Mountain Kingdom references, Ecosystem Bible, wildlife proposal | Director: "wind me thoda aur physics, baaki theek hai" |
| 3 | **Decision Sheet 01** applied (mapping, Sky Realms, EF 70–80 / 20–30 mix, Ashram Peepal + garden, wildlife PENDING, Spring) | verification 33/33 (`DECISION_SHEET_01_VERIFICATION.md`) |
| 4 | Realism pass (vegetation + TASK 05 terrain materials, Director "Ha laga do"), wind v2 → **v3** (near-camera per-blade bending), autosave + SAVE RULE | `WIND_TEST_v3.mp4`, `.claude/hooks/autosave.sh` |
| 5 | **Realism v3** (Director's list: natural leaf colours + shades + few dry leaves + dust, thatch at grass bases, varied blades, irregular roots with soil, crinkled matte petals, natural camera look) | all 43 milestone-1 assets re-rendered, sheet `T6_SHEET_M1.png` |
| 6 | **Milestone 2** ("jitne bhi task bache hai … un sab ko pura karo"): remaining regions, natural details, variants + LODs, NG_T6_ECOSYSTEM, populated regions, previews, QC | §2–§6 below |
| 7 | Storage decision: main repo ≈ 4.4 GB → Director created **`animation-studio-scenes`** (Stage 4 + 5) | two-repo setup (HANDOFF §0b), PRs: main repo #2, scenes repo #1 |
| 8 | **TASK 06 APPROVED + CLOSED** | this file |

## 2. What exists (all in git, main repo)

### 2.1 Vegetation libraries — `03_assets/vegetation/library/` (Blender 4.5, every file < 95 MB)
| Prefix | Region (map code) | Hero file (MB) | Assets | Also |
|---|---|---|---|---|
| AV | R-01 Ashram Valley | `T6_VEG_ASHRAM_VALLEY_v001.blend` (33.7) | 6 trees · 2 shrubs · 13 plants | `_VARIANTS_v001` (45.9) · `_LODS_v001` (25.1) |
| EF | R-02 Enchanted Forest | `T6_VEG_ENCHANTED_FOREST_v001.blend` (53.3) | 8 trees (3 = approved fantasy) · 5 plants | `_VARIANTS` (69.9) · `_LODS` (38.0) |
| MK | R-03 Mountain Kingdom (Great Northern Range) | `T6_VEG_MOUNTAIN_KINGDOM_v001.blend` (21.4) | 5 trees · 2 shrubs · 5 plants | `_VARIANTS` (32.7) · `_LODS` (17.5) |
| PL | R-06 Green Plains | `T6_VEG_GREEN_PLAINS_v001.blend` (33.9) | 3 trees · 1 shrub · 5 plants | `_VARIANTS` (41.7) · `_LODS` (24.2) |
| LK | R-08 Crystal Lakes | `T6_VEG_CRYSTAL_LAKES_v001.blend` (11.6) | 2 trees · 4 plants | `_VARIANTS` (16.9) · `_LODS` (8.5) |
| DS | R-04 Golden Desert | `T6_VEG_GOLDEN_DESERT_v001.blend` (10.1) | 2 trees · 1 shrub · 2 plants | `_VARIANTS` (13.2) · `_LODS` (7.9) |
| FB | R-05 Forbidden Lands | `T6_VEG_FORBIDDEN_LANDS_v001.blend` (0.5) | 1 tree · 1 shrub · 2 plants | `_VARIANTS` (0.8) · `_LODS` (0.5) |
| CT | C-01 / C-02 / C-03 Ancient City surroundings | `T6_VEG_ANCIENT_CITY_SITES_v001.blend` (9.6) | 2 trees · 3 plants | `_VARIANTS` (14.6) · `_LODS` (7.5) |
| CV | CV-01…05 Hidden Underground | `T6_VEG_HIDDEN_UNDERGROUND_v001.blend` (0.4) | 3 plants | `_VARIANTS` (0.6) · `_LODS` (0.3) |
| ND | Natural details (all regions) | `T6_VEG_NATURAL_DETAILS_v001.blend` (2.1) | 6 details | `_VARIANTS` (4.0) · `_LODS` (1.3) |
| | **Total** | | **84 hero assets = 29 trees, 7 shrubs, 42 plants, 6 details** | 3 variants / species; LOD1, LOD2, LOD3 impostor |

Inside every hero file: one collection `T6_<asset>` per species at the origin (asset object WITH its `T6_WIND` modifier, driven by
`T6_WIND_CONTROL`), scene `T6_LINEUP`, and `T6_LIB_<REGION>_SCATTER` = wind-free `<asset>_SC` copies (same mesh) for the scatter.
Metadata as custom props (`t6_label`, `t6_latin`, `t6_region`, `t6_habitat`, `t6_height_m`, `t6_palette`, `t6_wind_*` …); specs in
`*_inventory.json`. Species list with heights / labels: `ECOSYSTEM_BIBLE.md` §3 + §5 + §13 and the sheets.

**Species (milestone 2 additions):** PL banyan · neem · umbrella acacia · ber bush · tall grass · doob grass · wild mustard · globe thistle ·
white clover — LK white willow · Himalayan alder · white water-lily · sedge · spring reed · wet-rock moss — DS khejri · date palm · aak
(Calotropis) · sewan grass · candelabra euphorbia — FB charred dead tree · dead thorn shrub · grey crust lichen · hardy rim grass —
CT mango · coconut palm · ivy curtain · ruin moss · crack grass — CV pale cave moss · pale cave fungi (no glow) · root curtain —
ND leaf litter · needle litter + cones · fallen branches · giant uprooted log · ground ivy · floating leaves — MK silver fir · blue pine —
EF glow moss (approved fantasy, emission 0.15).

### 2.2 Textures
* `03_assets/vegetation/textures/leaves/` — **39** generated atlases (2K, 4 variants each: `_col` RGBA, `_nor`, `_rough`, `_prev`; `atlases.json` card sizes).
* `03_assets/vegetation/textures/impostors/` — 72 LOD3 impostor renders (front + side, 512 px, alpha) + `impostors.json` (metric framing).
* Bark / ground = Poly Haven CC0 scans in `03_assets/external/polyhaven/` (gitignored; `setup_session.sh` re-fetches every one used).

### 2.3 Sheets + renders
* `03_assets/vegetation/sheets/<REGION>/` — 36 `TREE_*.png` (front / side / back + ruler + 1.75 m figure, leaf + trunk-foot close-ups, bark /
  leaf maps, palette, specs) · `PLANTS_<R>.png` · `REGION_<R>.png` (+ `thumbs/`).
* Contact sheets: `sheets/T6_SHEET_M1.png` (milestone 1, realism v3) · `sheets/T6_SHEET_M2.png` (milestone 2).
* Source renders: `03_assets/vegetation/renders/<REGION>/` (+ `views.json`) · wind clips `renders/WIND_TEST{,_v2,_v3}.mp4` ·
  realism preview `renders/preview_realism_v3/`.

### 2.4 Populated regions (scatter on the APPROVED TASK 05 terrain) — `02_world/ecosystem/populated/`
| File | Built from (read-only, never written) | Layers | Preview cameras |
|---|---|---|---|
| `T6_POP_R01_ASHRAM_VALLEY_v001.blend` | `00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend` (far regions excluded in the view layer for memory) | 23 + ONE Peepal on a PROPOSED chabutra + PROPOSED garden beds (marigold rows, 6 Tulsi) | T6 courtyard / grove edge / meadow low + approved CAM_T5_07 |
| `T6_POP_R02_ENCHANTED_FOREST_v001.blend` | `T5_REGION_R02_ENCHANTED_master_v002.blend` | 17 (fantasy share 21 % of trees) | T6 forest floor / glade + CAM_T5_10 |
| `T6_POP_R03_MOUNTAIN_KINGDOM_v001.blend` | `T5_REGION_R03_RANGE_master_v002.blend` (cave-entrance tile, zone M1) | 12 | T6 forest edge + CAM_T5_12 |
| `T6_POP_R04_GOLDEN_DESERT_v001.blend` | `T5_REGION_R04_DESERT_master_v002.blend` | 11 (dunes bare, interdune gravel, wadis on the DN tile) | T6 wadi / interdune + CAM_T5_05 |
| `T6_POP_R05_FORBIDDEN_LANDS_v001.blend` | `T5_REGION_R05_FORBIDDEN_master_v002.blend` | 4 (rim only) | T6 rim dead trees + CAM_T5_09 |
Previews (1280×720, Cycles CPU, breeze frame 120): `02_world/ecosystem/renders/populated/*.png` (14) + sheet
`02_world/ecosystem/renders/T6_POPULATED_PREVIEWS.png` (+ `_small.jpg`). TASK 05 files untouched (QC checks git).

### 2.5 Documents — `02_world/ecosystem/`
`ECOSYSTEM_BIBLE.md` (v3; §13 = milestone 2) · `DIRECTOR_INPUTS_TASK06.md` (every Director message verbatim + action) · `DECISION_SHEET_01.md`
+ `_VERIFICATION.md` · `ENCHANTED_FOREST_VEGETATION_REFERENCE.md` · `SEASON_REFERENCE_SPRING.md` · `BLENDER45_ENV_PRODUCTION_CHECKLIST.md` ·
`WILDLIFE_SELECTION_SHEET.md/.png` (60 animals, PENDING) · `WILDLIFE_PROPOSAL.png` · `02_world/ashram/ASHRAM_LANDSCAPING_PLAN.md` (+ plan image) ·
`03_assets/vegetation/README.md` (how to run / use everything) · QC `03_assets/vegetation/qc/T06_QC_REPORT.md`.

## 3. Final QC (all PASS)
| Suite | Result |
|---|---|
| Libraries, Blender 4.5.16 LTS (geometry, UVs, materials incl. no empty slots, PBR, labels, heights, ground contact, scatter copies, wind: calm = static / motion / foot fixed, glow limits, Decision 01 rules) | **904 / 904** |
| Same libraries opened in Blender 5.3 | **904 / 904** |
| Leaf atlases (colour + alpha / normal / roughness, coverage) | **39 / 39** |
| Populated files (T5 untouched, < 95 MB, libraries + images found, one wind control + drivers, instances on every layer, NOTHING floating, ONE Peepal, Tulsi = 6 in the garden only, Marigold only in garden beds, R-02 fantasy 20–30 %, no glow outside R-02, every variant / LOD has materials, wind bends the near plants) | **58 / 58** |

## 4. How the systems work (for TASK 07+)

**Generators (Blender 4.5, `03_assets/vegetation/scripts/`):** `t6kit.py` (trees: trunk flare / buttress lobes / splits / whorls / weeping /
roots surface-buttress-stilt-aerial, leaf cards with crown normals; materials bark / leaf / herb / petal / moss + `realism()`; wind groups) ·
`t6kit_m2.py` (palms) · `t6_plants.py` + `t6_plants_m2.py` (grass with ground-resting thatch, herbs, ferns, lotus, reeds, moss, fungi, vines,
succulent, ivy, water-lily) · `t6_details.py` · catalogues `t6_species.py` / `t6_species_m2.py` · region table `t6_regions.py`.

**Wind (REAL-WORLD MOTION RULE):** `NG_T6_WIND` v3 per asset (drag ∝ v², natural frequency ≈ 4 / H, advected gusts, inertia lag,
crosswind, length-preserving arc bend, stiff root → flexible tip, per-element phase) + `NG_T6_WIND_INSTANCES` (scatter tilt). One empty
`T6_WIND_CONTROL` per file: arrow = direction; custom props `strength` (0 calm · 1 breeze · 3 strong · 6+ storm), `gust`, `speed`, `flutter`
(single-property drivers — work without auto-run scripts). Grass lying on the ground holds still (friction) — built into DS + CT; other grass
libraries get it on their next rebuild (they pass QC).

**Scatter `NG_T6_ECOSYSTEM` (`t6_ecosystem.py`, version 6):** inputs Terrain (object with T5 mask attributes) · Near / Mid / Far / Horizon
collections (hero + V1 + V2 → LOD1 → LOD2 → impostor) · Density (/m²) · Min Distance (> 0 = Poisson for trees / shrubs, 0 = random for
ground layers) · Mask + range · 2 avoid masks · Exclude Object + radius + Keep Only Inside (zones) · slope (≥ min) / altitude · clusters ·
scale / tilt / align · Sink · camera culling (distance, cone, keep near) · LOD distances · **Camera Clearance** (stills only — set 0 for
moving shots) · wind (Realize Distance: per-vertex wind near the lens with per-instance phase; instance tilt beyond). Recipes: `t6_populate.py`
(`REGIONS` table: per-layer masks / densities / zones / cameras). Memory: realize ≤ 15 m (trees), far components excluded, faces culled
before Poisson → previews 4–10 GB on the 16 GB machine.

**Using assets in scenes (Stage 4, repo `animation-studio-scenes`):** LINK `T6_<asset>` collections (instance) or scatter `<asset>_SC` with
`NG_T6_ECOSYSTEM` (copy a populated file's layer setup). Hero LOD0 for close-ups (FINAL OUTPUT RULE), 4K textures for final close-ups.

## 5. Honest limits (known, documented)
* R-06 / R-08 / C-sites / caves have **no TASK 05 hero terrain** → species, sheets and recipes ready; placement when those terrains exist.
* TASK 05 desert has **no oasis water** → no date palms placed (Bible rule: palms only where water exists).
* Ashram valley masks have no m_dry / m_forest near the Ashram → chir pine on low-flow ridges (L0), deodar on grove cores (L0) + forest belts (L1).
* Mountain previews: hero conifers are open-grown (branches to the ground) → camera clearance 18 m + lower density near the cave; a
  "forest-grown" (self-pruned) conifer variant would be the next improvement if the Director wants denser close forest shots.
* Previews are 1280×720 approval renders; finals = 4K on the Director's GPU PC (FINAL OUTPUT RESOLUTION RULE).

## 6. Still PENDING with the Director (not blocking)
1. **Wildlife selection** (`WILDLIFE_SELECTION_SHEET.md`, 60 animals) — no wildlife assets until selected.
2. **Sky Realms** map position + story role (PROPOSED region; re-uses main-world spring flora).
3. Ashram: exact **Peepal spot** (courtyard centre, PROPOSED) + **garden beds** (south lawn, PROPOSED) + Ashram layout v3 approval.
4. GitHub: **merge PR #2** (`animation-studio` → main) and **PR #1** (`animation-studio-scenes` → main) — one tap each in the GitHub app;
   keep the branches.
5. Backup: when at the PC, clone BOTH repos side by side (also the working setup for final renders).

## 7. New session — exact restart
1. Start the session with **both repos** (`animation-studio` + `animation-studio-scenes`) and environment `animation-studio`.
2. Paste the PROMPT in `HANDOFF.md` §0 → Claude checks out `ccr-c375d59d-2qaoyn` in both (or `main` after the PRs are merged), runs
   `SCRATCH=<scratchpad> bash setup_session.sh` (bpy 5.3 + bpy 4.5 + Poly Haven; nothing rebuilt), reads HANDOFF / STATUS / PROJECT_LOG /
   CLAUDE.md / this file, gives a short Hinglish summary and waits for the **TASK 07 brief**.
3. Only if something must be regenerated (normally never): resumable scripts `t6_finish_pending.sh`, `t6_m2_pending.sh`,
   `t6_final_previews.sh` (step markers in `03_assets/vegetation/.m2_steps/`).
4. Rules that always apply: `CLAUDE.md` (REAL-WORLD REALISM — textures + motion + physics / destruction; VFX quality; 4K output;
   SAVE RULE incl. two repos + autosave).

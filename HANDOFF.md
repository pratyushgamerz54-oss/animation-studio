# HANDOFF — poora kaam ek jagah (nayi session ke liye) · updated 22 Nov 2026 (session 4 — TASK 06 M1 + Decision Sheet 01 + realism / wind physics)

> **Nayi session: sabse pehle YE file padho**, phir `STATUS.md`, `PROJECT_LOG.md`, `CLAUDE.md`. Director ko Hinglish mein short
> summary do aur **TASK 06 wahin se continue karo jahan ruka (§6b)**. ⚠️ Jo bana hai use **DOBARA MAT BANAO** — sab git mein hai (§7).
> Director ke asli shabd (TASK 06 brief, Decision Sheet 01, saare feedback): `02_world/ecosystem/DIRECTOR_INPUTS_TASK06.md`.

---

## 0. Nayi session mein restore (2 minute)

**Sab kuch GitHub par:** repo `pratyushgamerz54-oss/animation-studio`, branch **`ccr-c375d59d-2qaoyn`** (session 4+; same history as `ccr-a129fdfc-g3v4k0`) (characters, VFX, sheets,
.blend files, exports, world maps, Ashram, 3D world, renders, backups, scripts, docs). Sirf Poly Haven assets git mein nahi (≈860 MB).

1. Session kholte waqt **dono repos** `pratyushgamerz54-oss/animation-studio` + `pratyushgamerz54-oss/animation-studio-scenes` + environment **`animation-studio`** chuno (Poly Haven network).
2. Branch: `git fetch origin ccr-c375d59d-2qaoyn && git checkout ccr-c375d59d-2qaoyn` (agar session doosri branch par khule).
3. Setup — **ek command** (idempotent, kuch rebuild nahi karta):
   ```bash
   SCRATCH=<scratchpad dir> bash setup_session.sh
   ```
   Ye karta hai: Blender 5.3 module (`pip install bpy scipy`) · **Blender 4.5.16 LTS** module in `$SCRATCH/bpy45`
   (`uv venv -p /usr/bin/python3.11` + `bpy>=4.5,<4.6`) · Mesa EGL (Workbench viewport renders) · Poly Haven fetch · Task 04 baseline
   checksum check. Uske baad: `BPY45=$SCRATCH/bpy45/bin/python`, viewport renders ke liye `EGL_PLATFORM=surfaceless`.
4. Director ke PC par files: GitHub → branch → *Download ZIP* ya `git clone -b ccr-c375d59d-2qaoyn https://github.com/pratyushgamerz54-oss/animation-studio.git`.
   **Director ka PC = Blender 4.5** (Task 04 se saari world files 4.5 se banti hain; character/Ashram v3 files 5.3 ki hain).

### PROMPT (nayi session mein paste karo) — session start karte waqt DONO repos chuno
```
Hum animation-studio project par kaam kar rahe hain: repo pratyushgamerz54-oss/animation-studio (branch ccr-c375d59d-2qaoyn) +
repo pratyushgamerz54-oss/animation-studio-scenes (branch ccr-c375d59d-2qaoyn) — dono side by side.
Dono branches checkout karo; animation-studio ke HANDOFF.md (§0b do-repo setup, §6c TASK 06), STATUS.md, PROJECT_LOG.md, CLAUDE.md aur
02_world/ecosystem/DIRECTOR_INPUTS_TASK06.md padho. Setup: bash setup_session.sh (SCRATCH = scratchpad). Jo bana hai dobara mat banana.
TASK 06 APPROVED + CLOSED (02_world/ecosystem/TASK06_CLOSEOUT.md padho). Mera agla TASK 07 brief main bhejta hoon — usi se kaam shuru karna.
CLAUDE.md ke saare rules (REAL-WORLD REALISM, SAVE RULE, do repos) follow karna. Mujhe short Hinglish summary do.
```

---

### 0b. TWO REPOSITORIES (Director, 22 Nov — repo size ≈ 4.4 GB)
| Repo | What | Branch used by Claude |
|---|---|---|
| `pratyushgamerz54-oss/animation-studio` (main) | stages 1–3: characters, world, terrain, asset libraries (TASK 06 vegetation…) + ALL rules / handoff / logs | session branch (e.g. `ccr-c375d59d-2qaoyn`) |
| `pratyushgamerz54-oss/animation-studio-scenes` | stage 4 `04_scenes/` + stage 5 `05_post/` (set up 22 Nov; README, CLAUDE.md, structure) | `ccr-c375d59d-2qaoyn` (GitHub default `main` still holds only the initial README) |
New session: start it with BOTH repos selected (cloud: `/home/user/animation-studio` + `/home/user/animation-studio-scenes`). Scene files
LINK assets from the main repo (relative paths) — nothing copied. Autosave (`.claude/hooks/autosave.sh`) commits + pushes both. Final 4K
masters → Director's PC / Drive (not git).

## 1. Project + Director rules (`CLAUDE.md` mein bhi)
- **10-minute 3D superhero film, Part 1.** Director = user. Claude = 3D artist + VFX team + world builder (Blender `bpy`, CPU only, no GPU).
- Pipeline: **1 Characters → 2 World/Environment → 3 Assets → 4 Scenes (storyboard, animation, lip-sync, VFX) → 5 Final/post.**
- Director ab numbered **TASK prompts** bhejta hai (≈17 total), **ek-ek karke**. Har task: plan → build → preview renders + viewport
  screenshots → QC report → Director approval → closeout. Approval ke bina agla step / final nahi.
- **Final VFX rule:** final production mein saare VFX high quality (Mantaflow, real lightning, particles, motion blur, glare, GPU render).
- **Story/script document abhi tak NAHI mila** → koi story event, lore, ruler, portal rule, location invent nahi. Labels: CONFIRMED / PROPOSED / NOT CONFIRMED.
- **Blender 4.5 compatibility** (Director ka PC) — Task 04 se naya world kaam 4.5 se banao aur test karo.
- Backups before major changes; approved baselines kabhi overwrite nahi.
- **REAL-WORLD REALISM RULE (Director, 22 Nov — CLAUDE.md):** textures asli (polished / plastic nahi) · har motion real physics
  (inertia, natural frequency, stiff root → flexible tip, damping, phase variation — "lakdi jaisa" nahi) · physics + destruction real
  (scale, gravity, material-based fracture, rigid body, Mantaflow dust). Har animated preview frame-by-frame check.
- **SAVE RULE + AUTOSAVE (Director, 22 Nov — CLAUDE.md):** project Stop hook `.claude/hooks/autosave.sh` commits + pushes all
  changes at the end of every reply (current branch, no force, files > 95 MB left out + reported); Director inputs verbatim per task;
  outputs inside the repo; resume scripts for long renders; HANDOFF / STATUS / LOG at every milestone; `.git` ≈ 3 GB → no repeated
  commits of big .blend iterations.
- **Decision Sheet 01 (22 Nov):** mapping APPROVED (Mountain Kingdom = R-03, Green Plains = R-06, Crystal Lakes = R-08, Ancient City =
  C-01/C-02/C-03 separate sites) · Sky Realms = PROPOSED region of the main world (NOT a dimension) · Enchanted Forest 70–80 % natural /
  20–30 % fantasy, subtle glow · ONE Peepal at the Ashram courtyard + sitting platform; Tulsi + Marigold ONLY in the Ashram garden ·
  **Season = Spring** · wildlife selection PENDING. Record: `02_world/ecosystem/DECISION_SHEET_01.md`.

---

## 2. STAGE 1 — CHARACTERS ✅ (Director ne saare designs APPROVE kiye, 20 Nov)

| Character | Role | Powers (confirmed) | Notes |
|---|---|---|---|
| **Shiv** (Hero 1, naam 21 Nov) | Main hero | Fire, Magical Portal | references ka combination |
| Pratyush | Hero 2 | Super Speed, Portal, Lightning | armoured speed suit (original colours) |
| Saithan | Main villain | Dark Magic, Invisibility, Speed, Fire, (corrupted) Portal, Lightning | borrowed power = apni zindagi ki keemat → **A+B+C** (fracture veins + ash drain + core siphon) |
| Soul | Sub-villain 1 | Lightning (crimson) | weapon story mein? PENDING |
| Max | Sub-villain 2 | Laser — **haath + aankh** | |
| Yayaki | Sub-villain 3 | Teleportation (portal se alag) | |
| Ramarat | Headmaster | **Har power, unlimited** (heroes + villains) | golden-white VFX |

**Har character** (`01_characters/<name>/`): `design/` (7–8 sheets + `DESIGN_SHEET.md`), `qc/` (`QC_REPORT.md`, qc json, test renders),
`blend/<name>_v002.blend` (design) · `v003` (export rig: IK/FK, face controls, baked textures) · **`v004_rigify.blend` (animation ke liye YE)**,
`export/<name>.glb/.fbx`, `textures/` (baked 1K/512), `uv/`, `<name>_config.py`. QC: saare 7 → 0 FAIL; Rigify pass. (Blender 5.3 files.)
Rig: fingers, IK/FK + poles, real jaw bone, face controls (expressions, 10 phonemes, jaw_open, blink, eye aim), skirt/robe 12×3 follow chains.
Scripts `01_characters/_shared/`: `charkit`, `charbuild`, `vfxkit`, `sheet_render`, `sheet_compose`, `production`, `rigify_build`, `sheet_doc`,
`qc_contact`; batch `render_all.sh`, `production_all.sh`. **Dobara mat chalao** jab tak Director koi change na maange.
Known: K-01 long robes (Ramarat/Soul/Saithan/Yayaki) action poses mein legs ke aar-paar — **Ramarat ka "safed daag" = ghutna skirt ke
aar-paar (session 2 mein diagnose, material bug NAHI)** → **Director decision (21 Nov): CLOTH SIMULATION** scene stage par (saare 4 long-robe characters).

## 3. VFX LIBRARY (`01_characters/_shared/vfxkit.py`) — reference quality
lightning · magical portal + corrupted portal · speed trails · fire · dark magic · laser (hand + eye) · teleport · invisibility ·
Saithan life-cost A/B/C. Powers pages par stage-wise renders. Final film mein high-quality simulation se upgrade.

---

## 4. STAGE 2 — WORLD (2D + concept)

### 4a. World map v2 — `02_world/map_v2/` (script `02_world/_shared/worldgen2.py`) — **Revision 01 = PROPOSAL (NOT canon)**
- 12 000 × 6 000 km, 5 continents: **Aetheria** (C1 home, Ashram) · **Solmara** (C2) · **Veylora** (C3) · **Noxara** (C4 polar) · **Drakmor** (C5)
  + 3 archipelagos (Sagara A1, Agni A2, Western Isles A3). Maps A–J + `GEOGRAPHY.md`; data in `map_v2/data/*.npy` (height, biome, flow, lakes…).
- Detailed Aetheria data (3 km cells): `02_world/map/data/` (script `worldgen.py`, seed 7) — Ashram Valley terrain isi se bana.
- Ashram (rev 01): large green valley in Aetheria, forest ring, rivers; snowy range ≈ 100 km NW.
- GEM: **UNCONFIRMED** (proposal = hidden region in Veylora, MAP_J). Portals: users CONFIRMED, routes H1–H5 hypothetical.
- Dimensions: MAP_H1 Black Hole Training, MAP_H2 Saithan's Dark World (layouts = proposals).

### 4b. Environment bible — `02_world/WORLD_BIBLE.md` + `02_world/bible/` (colour bible, location comparison)

### 4c. Ashram concept — `02_world/ashram/` (Blender 5.3)
v1 blockout → v2 procedural → **v3 with Poly Haven** (`01_BLOCKOUT/ASHRAM_concept_v003.blend`): carved pillars, lattice windows, clay-tile
roofs, prayer flags, props; compound 120 × 124 m + training ground (Ø 44 m) south of the gate. Renders `09_RENDER/concept_v3/`, sheets
`00_REFERENCE/*_v3.png`. Scripts `ashram_concept_v2.py`, `envkit.py`, `phkit.py` (Poly Haven loader), `ashram_sheets.py`.
⚠️ v3 ka backdrop (pahaad paas + jheel) map rev 01 se match nahi karta — Task 05 mein Ashram ko Task 04 valley terrain par rakhna hai.

### 4d. Poly Haven CC0 — `03_assets/external/` (`polyhaven_fetch.py`, gitignored)
16 textures (2K): sparse_grass, aerial_grass_rock, forest_ground_04, brown_mud_leaves_01, grass_path_2, cliff_side, aerial_rocks_02, snow_02,
mossy_cobblestone, cobblestone_floor_04, rustic_stone_wall, plastered_stone_wall, worn_mossy_plasterwall, clay_roof_tiles_02, medieval_wood,
dark_wooden_planks · 14 models: fir_tree_01, fir_sapling_medium, tree_small_02, shrub_01/02/03, fern_02, grass_medium_01/02, moss_01,
rock_moss_set_01/02, boulder_01, mountainside · 3 HDRIs (4K): kloofendal_48d_partly_cloudy_puresky, qwantani_dusk_2_puresky, qwantani_night_puresky.

---

## 5. TASK 04 — 3D WORLD BLOCKOUT ✅ CLOSED (`02_world/3d_world/`, Blender 4.5.16 LTS)

**Director (21 Nov): "APPROVED FOR DETAILED ENVIRONMENT PRODUCTION"** — conditions: (1) blockout geometry + layout preserve,
(2) map rev 01 PROPOSAL hi, (3) GEM unconfirmed — bina approval decide nahi, (4) dimensions preserve, (5) files + backups safe,
(6) close only with docs. → `TASK04_CLOSEOUT.md`.

| Folder | File | Kya hai |
|---|---|---|
| `00_MASTER_WORLD` | `WORLD_master_v001.blend` | links everything; scenes MAIN_WORLD, ASHRAM_VALLEY, DIM_BLACK_HOLE_TRAINING, DIM_SAITHAN_DARK_WORLD |
| `01_GEOGRAPHY` | `WORLD_geography_v001.blend`, `WORLD_SCALE.md`, `data/world_prep.npz + world_features.json` | markers (18 cities, 28 towns, 126 villages, ruins, caves, hidden, GEM proposal, Ashram), labels, 1000 km grid |
| `02_TERRAIN` | `WORLD_terrain_v001.blend` | plains, coasts, ice/tundra, ruined regions, sea bed, underground cave zones |
| `03_MOUNTAINS` / `04_FORESTS` / `06_DESERTS` / `07_ISLANDS` | `WORLD_*_v001.blend` (+ `FOREST_proxies_v001.blend`) | terrain pieces per region × class; tree/canopy proxies |
| `05_RIVERS_AND_LAKES` | `WORLD_water_v001.blend` | ocean, 423 rivers, 26 lakes, lake beds, 5 waterfalls |
| `08_ASHRAM_VALLEY` | `ASHRAM_VALLEY_terrain_v001.blend`, `data/valley_prep.npz` | true scale; LOD0 ±3 km@12.5 m, LOD1 ±30 km@100 m, LOD2 ±160 km@1 km; 96 rivers carved; forest + groves (GN instancing); proposed 31 km path; Ashram placement ref (pad 692 m) |
| `09_DIMENSIONS` | `DIM_black_hole_training_v001.blend`, `DIM_saithan_dark_world_v001.blend` | 20 platforms in 3 rings + disk; 9 × 6.5 km ash terrain, 350 spires, portal site |
| `10_CAMERAS` / `11_MATERIALS` | cameras + sun; 42 procedural materials (linked by all) | |
| `12_RENDER` | 27 Cycles + 11 viewport (Workbench) + `SHEET_01..04` + `render_log.json` + `qc/` | |
| `13_BACKUPS` | 16 backups (committed) | |
| root | `README.md`, `QC_REPORT.md` (70/70 in 4.5 and 5.3), `TASK04_CLOSEOUT.md`, `TASK04_BASELINE_MANIFEST.json` | |

**Scale:** main world 1 BU = 1 km, Z ×20 (vexag), origin = map centre; Ashram Valley 1 BU = 1 m true scale, origin = Ashram, Z = m a.s.l.;
Ashram = world (−2275, +1238) km = atlas (3725, 4238) km. Details `01_GEOGRAPHY/WORLD_SCALE.md`.
**Pipeline:** `scripts/run_all.sh` (prep python3 → build Blender 4.5 → render → QC). Scripts: `worldkit.py` (shared), `w4_prep_world/valley/dims.py`,
`w4_build_materials/assets/world/valley/dims/master.py`, `w4_render.py` (VIEWPORT_ONLY env, args world/valley/dims), `w4_contact_sheets.py`,
`w4_qc.py`, `w4_qc_report.py`.
🔒 **v001 = frozen baseline**: `worldkit.save()` refuses to overwrite manifest files (override `ALLOW_BASELINE_OVERWRITE=1` only with Director OK).
**Task 05 must write NEW v002 files** (same coordinates/layout, detail only).
Known limits → Task 05: lake stair-step shores (world scale), LOD2 far mountains blobby, proxies instead of real trees, procedural colours
(no textures), two parallel valley rivers (map data — keep).

---

## 6. TASK 05 — Detailed Terrain & Landscape Production ✅ APPROVED + CLOSED (21 Nov, session 3)
Brief: Director ka TASK 05 (main world terrain, mountain system, forest, rivers/water, desert, PBR materials, natural details,
procedural systems, 7 cinematic tests, optimisation). **FIRST MILESTONE = Ashram Valley + surroundings + first mountain + first
forest region → previews → Director approval → phir baaki world.** Blender 4.5, v001 frozen, sab naye **v002** files.

**Kya bana (sab git mein):**
| File | Kya hai |
|---|---|
| `scripts/t5_field.py` | TASK 04 height function VERBATIM copy (verify: v001 heights exact, err 3e-5 m) |
| `scripts/t5_noise.py`, `t5_erosion.py` | isotropic gradient noise (no square artefacts) · numba droplet hydraulic + thermal erosion |
| `scripts/t5_prep.py` | tiles → `08_ASHRAM_VALLEY/data_v002/*.npz` (ab git mein bhi; `t5_prep.py` se 2 min mein dobara banta hai) + `prep_v002.json` |
| tiles | VH ±1.2 km @2 m (Ashram) · FH 3×3 km @2 m (northern forest belt edge, x −1520..1480, y 24..27 km) · L0 ±6 km @10 m · L1 ±32 km @40 m · MT NW01 60×60 km @30 m (x −116..−56, y 44..104 km) · WF 900 m @1.5 m (waterfall gorge, 86 m fall) · L2 ±160 km @400 m |
| `11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend` (`t5_build_materials.py`) | 20 PBR materials (Poly Haven 2K) + MAT_T5_TERRAIN (mask/slope/height/distance blend), water, waterfall, mist, ice |
| `14_NATURE_LIBRARY/T5_NATURE_LIBRARY_TREES/GROUND_v002.blend` (`t5_build_library.py`) | 101 assets: fir/pine/broadleaf (LOD1/LOD2 + far proxies), saplings, ferns, shrubs, grass, flowers, logs, roots, stumps, rocks S/M/L |
| `scripts/t5kit.py` | NG_T5_HEIGHTFIELD (EXR heightfield → real mesh, LOD holes, skirts, 14 mask attributes) · NG_T5_SCATTER (mask/slope/altitude/cluster, camera culling, near/mid/far LOD) |
| `08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v002.blend` · `04_FORESTS/FOREST_NORTH_BELT_v002.blend` · `03_MOUNTAINS/MOUNTAIN_NW01_v002.blend` · `05_RIVERS_AND_LAKES/WATER_v002.blend` (`t5_build_terrain.py -- valley/forest/mountain/water`) | components; heightfields in `<folder>/heightfields_v002/*.exr/png` |
| `00_MASTER_WORLD/T5_LANDSCAPE_master_v002.blend` (`t5_build_master.py`) | links all components, HDRI + sun (az 215°, el 31°), 7 cameras CAM_T5_01..08 (desert = milestone 2), compositor aerial haze |
| `scripts/t5_render.py`, `t5_contact_sheet.py`, `t5_qc.py` | renders (12_RENDER/T5/cycles), sheet, automated QC |

**Rebuild order (nayi session):** `python3 t5_prep.py` → (BPY45) `t5_build_materials.py` → `t5_build_library.py` (T5_LIB=trees / ground)
→ `t5_build_terrain.py -- valley|forest|mountain|water` → `t5_build_master.py` → `t5_render.py` → `t5_contact_sheet.py` → `t5_qc.py`.
Sirf renders chahiye to prep + master hi kaafi (master camera placement npz padhta hai). Test renders: `t5_render.py -- --res 640x360 --samples 16 --out <scratch>`.

**Bugs already fixed (dobara mat karna):** masks PNG ko `save_render` se mat likho (AgX transform) → raw `image.save()`; EXR = save_render
Standard view, ZIP, BW (round-trip exact) · GN masks Set Position se PEHLE store karo (warna offset tiles FH/MT/WF par masks 0) ·
hero tiles ke kinare parent grid lines par (FH x −1520..1480 on 40 m; WF snapped to MT 30 m grid) · erosion zyada = pahaad pighle → passes
(4,1.5,2,.3,.2)+(1,1,3,.3,.3) + gaussian 1.0 on deltas · grass scans brown → luminance re-colour to green · test-render log repo ke bahar.

**Milestone 1 = DONE + reviewed (21 Nov):** shots 1, 2, 6, 7, 7b APPROVED; waterfall → wide 6-tier cascade (ballistic curtains,
GN spray particles, mist, rock cladding) + sharper peaks/glaciers DONE (Director said "baaki sab approve"). QC 56/56 (`T05_QC_REPORT.md`).

**MILESTONE 2 ✅ DONE + APPROVED (21 Nov, TASK 05 CLOSED) — rest of the world, region sites with their own local frame:**
| Step | Status | Files |
|---|---|---|
| R04 Western Desert (dunes, mesas, canyons/wadis, playas, pavement) + shot 5 | ✅ done | `scripts/t5_region_prep.py R04` → `06_DESERTS/data_v002/`; `t5_build_terrain.py -- desert` → `06_DESERTS/DESERT_R04_v002.blend`; `t5_build_region_master.py -- R04` → `00_MASTER_WORLD/T5_REGION_R04_DESERT_master_v002.blend`; render: `t5_render.py -- --master T5_REGION_R04_DESERT_master_v002.blend` |
| R05 Forbidden Region (crater rim, ejecta, fissures, ash, crater lake; no lava) | ✅ done | `06_DESERTS/FORBIDDEN_R05_v002.blend`, master `T5_REGION_R05_FORBIDDEN_master_v002.blend` |
| R02 Enchanted Forest (giant trees, moss, ferns, mist) | ✅ done | `04_FORESTS/ENCHANTED_FOREST_R02_v002.blend`, master `…R02_ENCHANTED…` |
| R03 Great Northern Range core + cave entrance (CV tile, scanned-rock kitbash) | ✅ done | `03_MOUNTAINS/GREAT_NORTHERN_RANGE_R03_v002.blend` (tiles R3N/R3F/CV in t5_prep), master `…R03_RANGE…` |
| Main-world v002 (coasts, islands, smooth lake shores) | ✅ done | `02_TERRAIN/WORLD_terrain_v002.blend` (`t5_world_prep.py`, `t5_build_world.py`) |
| QC (M2 45/45) + docs + push | ✅ done | `T05_QC_REPORT.md`, `T05_README.md`, `12_RENDER/T5/T5_SHEET_02_MILESTONE2.png` |
Region frame: origin = site centre (C1 cell), metres; `region_<key>.json` stores the Ashram-local offset. Desert mask slots: m_dry = sand,
m_pad = playa, m_gravel = pavement, m_grove = wadi shrubs (MAT_T5_TERRAIN_DESERT). Director: 4K stills NOT needed now (stopped on request).
A scheduled check-in (send_later, 21 Nov 17:47 UTC) resumes the work if a usage limit stopped the session; notify the Director when TASK 05 is complete.
**Director rule (21 Nov):** final MP4 FHD se zyada (4K), zoom par blur nahi — CLAUDE.md "FINAL OUTPUT RESOLUTION RULE".

**TASK 05 realism pass (session 4, Director OK "Ha laga do"):** only `11_MATERIALS/T5_TERRAIN_MATERIALS_v002.blend` changed (specular
.5/.4/.35 → .3/.28, dry roughness ≥ .45, wet ground .22, glacier ice .3 + coat .08); approved file backed up →
`13_BACKUPS/T5_TERRAIN_MATERIALS_v002__backup_20261122_011920.blend`; 8 shots re-rendered → `12_RENDER/T5/cycles_realism/` +
`12_RENDER/T5/T5_REALISM_BEFORE_AFTER.png` (approved renders in `12_RENDER/T5/cycles/` untouched); QC M1 56/56 (check list now
covers the M2 ground-mist volume + black crater water), M2 45/45.

## 6b. TASK 06 — Ecosystem & Vegetation Bible · MILESTONE 1 (concepts) — session 4, 21–22 Nov
Brief: complete ecosystem + vegetation system (trees, plants, regional ecosystems, wildlife proposal, real Blender assets, PBR,
scattering, wind, QC). **FIRST MILESTONE = Ashram Valley vegetation library + Enchanted Forest tree collection + Mountain Kingdom
vegetation references → present concepts for approval BEFORE full asset production.** Blender 4.5.
| What | Where |
|---|---|
| Ecosystem Bible (region mapping, rules, all 10 regions, tree/plant libraries, wildlife, tech standard, questions) | `02_world/ecosystem/ECOSYSTEM_BIBLE.md` |
| Wildlife proposal sheet | `02_world/ecosystem/WILDLIFE_PROPOSAL.png` |
| Libraries (42 assets: 17 trees, 4 shrubs, 21 plants) | `03_assets/vegetation/library/T6_VEG_{ASHRAM_VALLEY,ENCHANTED_FOREST,MOUNTAIN_KINGDOM}_v001.blend` + inventories |
| Generators / scripts | `03_assets/vegetation/scripts/` (`t6kit`, `t6_species`, `t6_plants`, `t6_leafgen`, `t6_build_library`, `t6_render_sheets`, `t6_compose_sheets`, `t6_contact_sheet`, `t6_qc`, `t6_wind_test`, `t6_wildlife_sheet`) — README there |
| Sheets | `03_assets/vegetation/sheets/<AV|EF|MK>/TREE_*, PLANTS_*, REGION_*` + `sheets/T6_SHEET_M1.png` |
| Wind | `NG_T6_WIND` + `T6_WIND_CONTROL` (strength/gust/speed/flutter, drivers) · clip `03_assets/vegetation/renders/WIND_TEST.mp4` |
| QC | `03_assets/vegetation/qc/T06_QC_REPORT.md` |
Region mapping (PROPOSED, Q to Director): Mountain Kingdom = R-03, Green Plains = R-06, Crystal Lakes = R-08, Ancient City = C-01…03,
Hidden Underground = CV caves, Sky Realms = NOT on the map (nothing designed). Fantasy (PROPOSED): Veil Willow, Spiral-root, Lantern Tree, Glowcap.
Lessons: Blender ortho cam → set `sensor_fit` explicitly; custom-prop changes need `obj.update_tag()` before frame_set; leaf atlases
auto-fit (zoom) so sprays never touch tile edges; branches need a ground "floor" guard; height-normalise trees (±10 %);
CPU Cycles ≈ 30 s per 600×840 tree view (transparent leaves, 64 transparent bounces).
**Status at the end of session 4 (22 Nov):** milestone 1 DONE (Director: "baaki theek hai") · Decision Sheet 01 applied (verification
33/33) · TASK 06 overall ≈ 45 % (remaining list below).
| Done in session 4 | Where |
|---|---|
| 43 assets (17 trees, 4 shrubs, 22 plants incl. **spring kans** `AV_G02B_KANS_GRASS_SPRING`), labels `SPECIES-INSPIRED` / `FANTASY (APPROVED R-02)` | `03_assets/vegetation/library/T6_VEG_*_v001.blend` + `*_inventory.json` |
| **Realism pass** on all vegetation materials (`realism()` in t6kit: rough / matte, low specular, mottling, blemishes, AO dirt, micro-bump, blade streaks, fibrous fungus caps, organic lathe wobble) + scanned ground `mat_ground` | `scripts/t6kit.py` |
| **Leaf realism v2** (soft low-contrast veins in relief, midrib / margin tone, spots, insect bites, rounded Peepal base) | `scripts/t6_leafgen.py` (atlases regenerate in `t6_finish_pending.sh`) |
| **Wind v3 physics** — `NG_T6_WIND` v3 (drag ∝ v², natural freq ≈ 4/H, advected gusts, lag, crosswind, length-preserving arc bend, `Bend Offset`), `NG_T6_WIND_INSTANCES` (scatter tilt); near-camera vegetation realized for per-blade bending | `scripts/t6kit.py`, test `scripts/t6_wind_test.py`, clips `renders/WIND_TEST_v2.mp4` (+ v3 pending) |
| Decision Sheet 01 docs: Ecosystem Bible v2, World Bible + GEOGRAPHY blocks, EF vegetation reference, Ashram landscaping plan (+ image), wildlife selection sheet (60 animals, PENDING), Spring reference, Blender 4.5 checklist | `02_world/ecosystem/*.md`, `02_world/ashram/ASHRAM_LANDSCAPING_PLAN.md`, `02_world/ashram/00_REFERENCE/ASHRAM_landscaping_plan_v1.png` |
| QC | vegetation 379/379 (Blender 4.5 + 5.3) `03_assets/vegetation/qc/T06_QC_REPORT.md` · decisions 33/33 `02_world/ecosystem/DECISION_SHEET_01_VERIFICATION.md` |

**⚠️ IN PROGRESS when session 4 ended → finish with ONE command** (idempotent, skips what is done):
`SCRATCH=<scratchpad> bash 03_assets/vegetation/scripts/t6_finish_pending.sh` → (1) `renders/WIND_TEST_v3.mp4` (resumes at the first
missing frame), (2) leaf realism v2: atlases → 3 libraries → all sheet renders → compose → contact sheet → QC 4.5 + 5.3 → report
(marker `textures/leaves/.leaf_realism_v2`). Then `git add -A && git commit && git push`, send the Director the clip + contact sheet.

**Next (TASK 06 full production, ≈ 12–18 h):** (a) 3–5 variants + LOD1/LOD2/far proxy per species (keep each .blend < 100 MB — split
per region / species group) · (b) remaining regions: R-06 Green Plains, R-08 Crystal Lakes (water-lily, reeds, willow/alder), R-04 Golden
Desert (khejri / acacia / date palm, Poly Haven Namaqualand succulents), R-05 Forbidden (charred snags, lichen), C-01/02/03 surroundings
(banyan / neem / ivy on ruins), CV caves (cave moss / fungi), Sky Realms (proposed; main-world spring flora on islands), MK silver fir /
blue pine, EF glow-moss variant (≤ 0.3) · (c) `NG_T6_ECOSYSTEM` scatter on the TASK 05 terrains (region recipes, slope / altitude /
water rules, density / ha, near = realized + v3 wind, far = instance tilt; Ashram garden + Peepal per landscaping plan; EF 75/25 mix) ·
(d) natural details (leaf litter per species, fallen branches, giant log, ivy, floating leaves) · (e) populated cinematic previews per
region · (f) scatter-level QC + closeout. Wildlife: ONLY after the Director's selection.

### 6c. TASK 06 · MILESTONE 2 (full production) — session 5, 22 Nov — ✅ **TASK 06 APPROVED + CLOSED** (closeout: `02_world/ecosystem/TASK06_CLOSEOUT.md`)
Built (code in `03_assets/vegetation/scripts/`, summary in `02_world/ecosystem/ECOSYSTEM_BIBLE.md` §13):
| What | Where |
|---|---|
| Realism v3 everywhere (+ v3.1: moss shader with shoots / fuzz, dead grass thatch lies ON the ground) + natural camera look | `t6kit.py` (`realism`, `mat_moss`, `camera_look`), `t6_plants.py` (`blade(floor=…)`) |
| 7 new hero libraries + MK / EF additions — **84 assets total** (29 trees, 7 shrubs, 42 plants, 6 natural details) | `library/T6_VEG_{GREEN_PLAINS,CRYSTAL_LAKES,GOLDEN_DESERT,FORBIDDEN_LANDS,ANCIENT_CITY_SITES,HIDDEN_UNDERGROUND,NATURAL_DETAILS}_v001.blend`; `t6_species_m2.py`, `t6_plants_m2.py`, `t6_details.py`, `t6kit_m2.py` (palms), `t6_regions.py` (region table) |
| Wind-free scatter copies `<asset>_SC` in every library (wind applied once, in the scatter) | `t6_build_library.py` (`make_scatter_copies`) |
| Variants (seeds 1, 2) + LOD1 / LOD2 + LOD3 impostors | `t6_build_lods.py`, `t6_render_impostors.py` → `library/T6_VEG_<R>_VARIANTS_v001.blend`, `_LODS_v001.blend`, `textures/impostors/` |
| **NG_T6_ECOSYSTEM** (TASK 05 scatter logic + Poisson spacing for trees, random for ground layers, inclusion / exclusion zone, 4 LOD bands, near realized per-vertex wind with per-instance phase, far instance tilt) | `t6_ecosystem.py` |
| Populated region files (open approved T5 region master → SAVE AS new file; T5 vegetation scatters excluded in the view layer, rocks / far forest kept; T6 layers on the hero tile; PROPOSED Peepal chabutra + garden beds in the Ashram) | `t6_populate.py` → `02_world/ecosystem/populated/T6_POP_R0{1..5}_*_v001.blend` |
| Previews + scatter QC | `t6_render_populated.py` → `02_world/ecosystem/renders/populated/`; `t6_pop_qc.py` |

**Status at the end of session 5: TASK 06 APPROVED + CLOSED (22 Nov)** — full summary `02_world/ecosystem/TASK06_CLOSEOUT.md`; next = TASK 07 brief. Resumable scripts (all idempotent, step markers in
`03_assets/vegetation/.m2_steps/`): `t6_finish_pending.sh` (M1 realism re-render) · `t6_m2_pending.sh` (M2 libraries → sheets → impostors
→ LODs → QC) · `t6_final_previews.sh` (populate → previews → QC → sheets). Results: contact sheets `03_assets/vegetation/sheets/T6_SHEET_M1.png`
+ `T6_SHEET_M2.png`, populated previews `02_world/ecosystem/renders/T6_POPULATED_PREVIEWS.png` (+ single PNGs in `renders/populated/`),
QC `03_assets/vegetation/qc/T06_QC_REPORT.md` — 904/904 (Blender 4.5) · 904/904 (5.3) · 39/39 textures · 58/58 populated.
Known limits (honest): R-06 / R-08 / C-sites / caves have no TASK 05 hero terrain → species + recipes ready, not placed; TASK 05 desert has
no oasis water → no date palms placed; Ashram valley masks have no m_dry / m_forest near the Ashram → chir pine on low-flow ridges, deodar on
grove cores (L0) + forest belts (L1); populated previews use camera clearance (no trees within 7–18 m of the lens; set 0 for moving shots);
dead-grass "ground friction" wind fix is built into DS + CT, the other grass libraries get it on their next rebuild (they pass QC already).

### 6d. TASK 07 — Wildlife & Creature Production · MILESTONE 1 (concept collection EF / MK / CL) — session 6, 23 Nov — IN PROGRESS
Director inputs verbatim: `03_assets/creatures/DIRECTOR_INPUTS_TASK07.md` (§A brief … §N). Production fix list: `03_assets/creatures/PRODUCTION_FIX_LIST.md`.
**Method (Director "mix" decision):** free-licence base (Sketchfab CC0/CC-BY, token in the environment's network secrets) + own work
(photo-matched coat recolour + 3D-region UV paint, own antlers / horns, real size, ground contact, smooth continuous clips) + real photos
(Wikimedia Commons, `t7_fetch_refs.py`, credits per species). ONE creature at a time → preview → Director → next. Three.js only if really needed (§N).
| Creature | File | Status |
|---|---|---|
| Sambar | `01_FOREST_WILDLIFE/sambar/T7_SAMBAR_CC_v003_fur.blend` (+ preview_v002 walk v002b, preview_v003_fur) | **APPROVED** (v003 fur) |
| Himalayan wolf | `02_MOUNTAIN_WILDLIFE/wolf/T7_WOLF_CC_v003_fur.blend` | **APPROVED** (v003 fur) |
| Asiatic black bear | `01_FOREST_WILDLIFE/black_bear/T7_BLACK_BEAR_CC_v003_fur.blend` | **APPROVED** (v003 fur) |
| Golden eagle (juvenile, museum scan CC0) | `06_AERIAL_CREATURES/golden_eagle/T7_GOLDEN_EAGLE_SCAN_v002.blend` | **APPROVED** |
| Red fox | `02_MOUNTAIN_WILDLIFE/red_fox/T7_RED_FOX_CC_v003_fur.blend` (real fur) | approved (look fix v003) |
| Bharal | script `t7_bharal_cc.py` (cel base) | WIP — needs a better base / own texture |
Old versions of an approved asset are deleted (Director §R; git history keeps them). Real-fur standard (§P): `scripts/t7_furpass.py`
(its input = the v002 conversion output, rebuilt by `t7_cc_species.py <id>` / `t7_sambar_cc.py`). Tools: `scripts/t7_sketchfab.py`, `t7_ccbase.py`, `t7_cc_species.py` (config per species), `t7_sambar_cc.py`, `t7_bharal_cc.py`,
`t7_scan_reduce.py`, `t7_preview_rig.py` (stills + continuous clips, `--cycles`, `--step`, constant-velocity camera), own procedural kit
`t7sdf.py` / `t7_anatomy.py` / `t7kit.py` (fur = hair-Curves object, feathers) for parts and fantasy creatures. Behaviour baker design:
`09_RIGS/T7_BEHAVIOUR_SYSTEM.md` (milestone 2). Next: Himalayan monal, snow leopard, marmot, owl, hornbill, butterflies / insects, Crystal-Lakes set, fantasy proposals.

## 7. ⚠️ DOBARA MAT BANAO (sab git mein, ready)
Characters v002/v003/v004 + sheets + exports · VFX library · world maps v1/v2 + data · World Bible · Ashram v1/v2/v3 + renders · Task 04 3D world
(all v001 files, renders, QC, backups) · **TASK 05: saari v002 files** (valley, forest belt, NW01 mountain + cascade, water, desert R04,
forbidden crater R05, enchanted forest R02, Great Northern Range R03 + cave, main world v002, material + nature libraries, masters,
heightfields, data_v002 npz, renders, QC) · **TASK 06: vegetation libraries (43 assets), leaf atlases, sheets, renders, wind clips, Ecosystem Bible + Decision Sheet 01 docs** (§6b) · **TASK 05 realism re-renders** (`12_RENDER/T5/cycles_realism/`) · **TASK 06 milestone 2** (§6c: 10 hero libraries, VARIANTS + LODS files,
impostors, 39 atlases, sheets, populated files R-01…R-05, previews, QC). Sirf setup (`setup_session.sh`) chalao. Rebuild tabhi jab Director change maange.

## 8. Director se PENDING
1. ~~Hero 1 ka naam~~ = **Shiv** ✅ · Soul ka weapon story mein hai?
2. World map revision 01 ka **canon** approval (abhi sirf blockout layout approved) · GEM location (unconfirmed) · kaunse portal routes sach hain.
3. Story / script document.
4. ~~Ramarat K-01~~ → **cloth sim** at scene stage ✅ (21 Nov).
5. ~~TASK 05~~ ✅ closed. TASK 06 milestone 1 ✅ ("baaki theek hai"); Decision Sheet 01 ✅ applied.
6. **Wildlife selection** (`02_world/ecosystem/WILDLIFE_SELECTION_SHEET.md`) — select / reject per animal.
7. Sky Realms map position (candidates in `WORLD_BIBLE.md`) + story role · Ashram: exact Peepal spot + garden position (PROPOSED in the landscaping plan) · Ashram layout v3 approval.
8. Review: `WIND_TEST_v3.mp4` (near plants bend per blade) + updated sheets after realism v3.
10. ~~Repo storage plan~~ → **DECIDED (22 Nov): new repo per stage** — Director created `animation-studio-scenes` (Stage 4 + 5); main repo
    stays the asset library (§0b). Director: clone both repos side by side on the PC as a backup copy when at the PC.
9. ~~Milestone 2 review~~ → TASK 06 APPROVED (22 Nov). Still open from it: contact sheet `03_assets/vegetation/sheets/T6_SHEET_M2.png`, populated previews `02_world/ecosystem/renders/populated/`,
   PROPOSED Ashram Peepal chabutra (9 × 9 m, courtyard centre) + garden beds (south lawn) in `T6_POP_R01_ASHRAM_VALLEY_v001.blend`.

## 9. Technical lessons (CLAUDE.md mein bhi)
- (session 5) Scatter: slope `≥ min` (flat pads); cull faces before Poisson; realize ≤ 15 m (memory); viewport-res terrain in background
  → aim cameras by masks; modifier ID-prop edits need `update_tag()`; exclude far T5 components in populated files (memory);
  no stdlib-named scratch scripts (`inspect.py`); unique temp material names (`new_mat` replaces same-name).
- Background waiter: `pgrep -f` mat use karo — log marker (ALLDONE) grep karo. Long renders: background + log + marker.
- Alpha leaf cards: `cycles.transparent_max_bounces = 64`; join se pehle same UV layer naam.
- `reset_pose` driven bones (jaw) ka rotation mode nahi badalna; driver test se pehle `arm.update_tag()`.
- Rigify: human template re-fit; `spine.004.connect_chain=False`; template bones par rigify_type; re-parent par constraints mute.
- Poly Haven: User-Agent header; LOD collections append + `fix_paths()`; save `relative_remap=True`.
- World volume sooraj block karta hai → bounded haze box. Sun camera ke peeche = flat light.
- Blender 4.5 module: `uv venv -p python3.11` + `bpy>=4.5,<4.6`. Headless Workbench/EEVEE: Mesa EGL + `EGL_PLATFORM=surfaceless`.
- 4.5: shading colour enum = 'VERTEX'; `.blend1` off via `preferences.filepaths.save_version = 0`; deselect all before `object.join`.
- Big terrain: ONE height grid cut into pieces (shared verts + global custom normals) → seamless. Coarse LOD: river channel ≥ 1 vertex row.
- Linked data can't be edited in memory → hide overlays via view-layer collection exclude. Workbench shadows at km scale = streak artefacts → off.
- CPU Cycles 1280×720 @32 spp: world ≈ 40–100 s, valley (haze + instances) ≈ 90 s per image.
- Vegetation wind: collection instances share ONE evaluated mesh → identical motion for every instance; per-instance motion = tilt the
  instances in the scatter tree (`NG_T6_WIND_INSTANCES`), per-blade bending near camera = Realize Instances + `NG_T6_WIND` (world
  position via Self Object). Rigid whole-plant rotation looks like a stick ("lakdi") — never use it for close plants.
- GN wind phase per object: Self Object → Object Info location + position. Calm must be exactly static (all terms ∝ q = (U/10)²).
- Custom-prop drivers: SINGLE_PROP / AVERAGE (no Python). After changing a custom prop from a script: `obj.update_tag()` before `frame_set`.
- Blender ortho camera: set `sensor_fit` explicitly (VERTICAL for portrait sheets) or the ruler mapping is wrong.
- Leaf atlases: auto-fit zoom so sprays never touch tile edges; keep the previous zoom (card size) when regenerating.
- Realism: Specular IOR Level ≈ .25–.3 for plants / ground; dry roughness ≥ .45; AO-node dirt + micro-bump; perfect lathe shapes look CG → wobble.
- QC check lists must be extended when new materials are added in a later milestone (M1 check vs M2 mist volume / black water).
- Container restarts can stop background renders: animation renders must support resume (`FSTART`), long chains write log markers.

## 10. Session history (short)
- **Session 1 (19–21 Nov):** setup, 7 characters (design → production → Rigify, QC), VFX library, world maps v1 + v2 (rev 01), World Bible,
  Ashram concept v1→v3 (Poly Haven), handoff.
- **Session 2 (21 Nov):** restore + summary; Ramarat spot diagnosed (K-01); **TASK 04** 3D world blockout (Blender 4.5) — main world,
  regions, water, islands, underground/ruins, Ashram Valley LOD terrain, 2 dimension blockouts, 38 previews, QC 70/70 (4.5 + 5.3);
  Director approved blockout → closeout, baseline frozen, backups committed; `setup_session.sh`; this handoff.
- **Session 3 (21 Nov):** restore; Director decisions: Hero 1 = **Shiv**, robe clipping → **cloth sim** at scene stage, final MP4 **4K**
  (CLAUDE.md rule). **TASK 05** detailed terrain: milestone 1 (Ashram Valley 2 m–400 m LODs, northern forest belt with real Poly Haven
  trees, NW01 mountains + 6-tier wide cascade with ballistic spray, PBR library 25 materials, nature library 101 assets, GN heightfield +
  scatter systems, QC 56/56) → Director approved; milestone 2 (desert R04, forbidden crater R05, enchanted forest R02, Great Northern
  Range R03 + cave entrance, main world v002, QC 45/45) → Director fixes (crater wall + black lake, cave realism, dunes) → **"Badhiya hai",
  TASK 05 CLOSED**. 4K stills: Director said not needed now. Final film = re-render everything 4K on the Director's GPU PC (Stage 4/5).
- **Session 4 (21–22 Nov):** restore; **TASK 06** brief → own procedural vegetation generator (Blender 4.5: trees with roots / buttresses /
  multi-leaders / whorls, plants with real geometry), 25 leaf atlases, 16 Poly Haven barks, 43 assets in 3 regional libraries, sheets for
  every tree + plant + region, Ecosystem Bible, wildlife proposal, QC; Director: "wind me aur physics, baaki theek hai" + **Decision
  Sheet 01** (mapping, Sky Realms, EF mix, Ashram Peepal / garden, wildlife pending, Spring) → all docs + verification 33/33; Director
  rules: **real textures, real motion, real physics / destruction** (CLAUDE.md); realism pass on vegetation + TASK 05 terrain materials
  (approved); wind v2 → v3 (per-blade bending near camera); spring kans; leaf realism v2 (finish with `t6_finish_pending.sh`).
- **Session 5 (22 Nov):** restore; realism v3 on every asset + natural camera look (M1 sheets re-rendered, QC 428/429 → Glowcap habitat
  fixed); **TASK 06 MILESTONE 2**: 7 new regional libraries + MK / EF additions (84 hero assets), palm / succulent / ivy / water-lily /
  natural-detail generators, variants + LODs + impostors for 10 regions, **NG_T6_ECOSYSTEM** scatter, populated R-01…R-05 files on the
  approved TASK 05 masters (save-as copies, T5 untouched) + previews + scatter QC; repo `.git` ≈ 4.0 GB → storage plan question to the Director.

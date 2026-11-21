# HANDOFF — poora kaam ek jagah (nayi session ke liye) · updated 21 Nov 2026 (session 3, TASK 05 in progress)

> **Nayi session: sabse pehle YE file padho**, phir `STATUS.md`, `PROJECT_LOG.md`, `CLAUDE.md`. Director ko Hinglish mein short
> summary do aur **seedha agle task (TASK 05) se kaam shuru karo**. ⚠️ Jo bana hai use **DOBARA MAT BANAO** — sab git mein hai (§7).

---

## 0. Nayi session mein restore (2 minute)

**Sab kuch GitHub par:** repo `pratyushgamerz54-oss/animation-studio`, branch **`ccr-a129fdfc-g3v4k0`** (characters, VFX, sheets,
.blend files, exports, world maps, Ashram, 3D world, renders, backups, scripts, docs). Sirf Poly Haven assets git mein nahi (≈860 MB).

1. Session kholte waqt repo `pratyushgamerz54-oss/animation-studio` + environment **`animation-studio`** chuno (Poly Haven network).
2. Branch: `git fetch origin ccr-a129fdfc-g3v4k0 && git checkout ccr-a129fdfc-g3v4k0` (agar session doosri branch par khule).
3. Setup — **ek command** (idempotent, kuch rebuild nahi karta):
   ```bash
   SCRATCH=<scratchpad dir> bash setup_session.sh
   ```
   Ye karta hai: Blender 5.3 module (`pip install bpy scipy`) · **Blender 4.5.16 LTS** module in `$SCRATCH/bpy45`
   (`uv venv -p /usr/bin/python3.11` + `bpy>=4.5,<4.6`) · Mesa EGL (Workbench viewport renders) · Poly Haven fetch · Task 04 baseline
   checksum check. Uske baad: `BPY45=$SCRATCH/bpy45/bin/python`, viewport renders ke liye `EGL_PLATFORM=surfaceless`.
4. Director ke PC par files: GitHub → branch → *Download ZIP* ya `git clone -b ccr-a129fdfc-g3v4k0 https://github.com/pratyushgamerz54-oss/animation-studio.git`.
   **Director ka PC = Blender 4.5** (Task 04 se saari world files 4.5 se banti hain; character/Ashram v3 files 5.3 ki hain).

### PROMPT (nayi session mein paste karo)
```
Hum animation-studio project par kaam kar rahe hain (repo pratyushgamerz54-oss/animation-studio, branch ccr-a129fdfc-g3v4k0).
Branch checkout karo, HANDOFF.md, STATUS.md, PROJECT_LOG.md, CLAUDE.md padho. Setup: bash setup_session.sh (SCRATCH = scratchpad).
Jo bana hai dobara mat banana. Mujhe short Hinglish summary do, phir TASK 05 (Detailed Terrain & Landscape Production) ka
brief main bhejta hoon — usi se kaam shuru karna. Har bade kaam ke baad commit + push aur STATUS.md update.
```

---

## 1. Project + Director rules (`CLAUDE.md` mein bhi)
- **10-minute 3D superhero film, Part 1.** Director = user. Claude = 3D artist + VFX team + world builder (Blender `bpy`, CPU only, no GPU).
- Pipeline: **1 Characters → 2 World/Environment → 3 Assets → 4 Scenes (storyboard, animation, lip-sync, VFX) → 5 Final/post.**
- Director ab numbered **TASK prompts** bhejta hai (≈17 total), **ek-ek karke**. Har task: plan → build → preview renders + viewport
  screenshots → QC report → Director approval → closeout. Approval ke bina agla step / final nahi.
- **Final VFX rule:** final production mein saare VFX high quality (Mantaflow, real lightning, particles, motion blur, glare, GPU render).
- **Story/script document abhi tak NAHI mila** → koi story event, lore, ruler, portal rule, location invent nahi. Labels: CONFIRMED / PROPOSED / NOT CONFIRMED.
- **Blender 4.5 compatibility** (Director ka PC) — Task 04 se naya world kaam 4.5 se banao aur test karo.
- Backups before major changes; approved baselines kabhi overwrite nahi.

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

## 6. TASK 05 — Detailed Terrain & Landscape Production (🟨 IN PROGRESS — milestone 1, session 3)
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

**MILESTONE 2 (in progress) — rest of the world, region sites with their own local frame:**
| Step | Status | Files |
|---|---|---|
| R04 Western Desert (dunes, mesas, canyons/wadis, playas, pavement) + shot 5 | ✅ built, final previews rendering | `scripts/t5_region_prep.py R04` → `06_DESERTS/data_v002/`; `t5_build_terrain.py -- desert` → `06_DESERTS/DESERT_R04_v002.blend`; `t5_build_region_master.py -- R04` → `00_MASTER_WORLD/T5_REGION_R04_DESERT_master_v002.blend`; render: `t5_render.py -- --master T5_REGION_R04_DESERT_master_v002.blend` |
| R05 Forbidden Region (crater ~90 km, dark ground, crater lake; volcanic look ONLY if approved → not) | ⏳ next | add to REGIONS in t5_region_prep.py (cell 276.48, 483.84; biome 9 + lake 10) |
| R02 Enchanted Forest (visually distinct: old-growth giant trees, moss, teal, ground mist) | ⏳ | cell (672, 505), biome 4 |
| R03 Great Northern Range core | ⏳ | cell (626, 138) |
| Main-world v002 polish (coasts, islands, lake shores without stair-steps, cave entrances) | ⏳ | world-scale (1 BU = 1 km) |
| QC + docs + STATUS/HANDOFF + push, then notify Director | ⏳ | |
Region frame: origin = site centre (C1 cell), metres; `region_<key>.json` stores the Ashram-local offset. Desert mask slots: m_dry = sand,
m_pad = playa, m_gravel = pavement, m_grove = wadi shrubs (MAT_T5_TERRAIN_DESERT). Director: 4K stills NOT needed now (stopped on request).
A scheduled check-in (send_later, 21 Nov 17:47 UTC) resumes the work if a usage limit stopped the session; notify the Director when TASK 05 is complete.
**Director rule (21 Nov):** final MP4 FHD se zyada (4K), zoom par blur nahi — CLAUDE.md "FINAL OUTPUT RESOLUTION RULE".

## 7. ⚠️ DOBARA MAT BANAO (sab git mein, ready)
Characters v002/v003/v004 + sheets + exports · VFX library · world maps v1/v2 + data · World Bible · Ashram v1/v2/v3 + renders · Task 04 3D world
(all v001 files, renders, QC, backups). Sirf setup (`setup_session.sh`) chalao. Rebuild tabhi jab Director change maange.

## 8. Director se PENDING
1. ~~Hero 1 ka naam~~ = **Shiv** ✅ · Soul ka weapon story mein hai?
2. World map revision 01 ka **canon** approval (abhi sirf blockout layout approved) · GEM location (unconfirmed) · kaunse portal routes sach hain.
3. Story / script document.
4. ~~Ramarat K-01~~ → **cloth sim** at scene stage ✅ (21 Nov).
5. TASK 05 brief (aur aage ke prompts ek-ek karke).

## 9. Technical lessons (CLAUDE.md mein bhi)
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

## 10. Session history (short)
- **Session 1 (19–21 Nov):** setup, 7 characters (design → production → Rigify, QC), VFX library, world maps v1 + v2 (rev 01), World Bible,
  Ashram concept v1→v3 (Poly Haven), handoff.
- **Session 2 (21 Nov):** restore + summary; Ramarat spot diagnosed (K-01); **TASK 04** 3D world blockout (Blender 4.5) — main world,
  regions, water, islands, underground/ruins, Ashram Valley LOD terrain, 2 dimension blockouts, 38 previews, QC 70/70 (4.5 + 5.3);
  Director approved blockout → closeout, baseline frozen, backups committed; `setup_session.sh`; this handoff.

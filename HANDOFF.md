# HANDOFF — poora kaam ek jagah (nayi session ke liye) · updated 21 Nov 2026 (session 2)

> **Nayi session mein sabse pehle ye file padho**, phir `STATUS.md`, `PROJECT_LOG.md`, `01_characters/PRODUCTION_INVENTORY.md`,
> `02_world/map_v2/GEOGRAPHY.md`, `02_world/WORLD_BIBLE.md`. Director ko Hinglish mein summary do, phir jahan ruka tha wahin se kaam karo.

---

## 0. Nayi session mein saara kaam kaise wapas aayega (step by step)

**Sab kuch GitHub par hai:** repo `pratyushgamerz54-oss/animation-studio`, branch **`ccr-a129fdfc-g3v4k0`**
(characters, VFX, design sheets, 3D `.blend` files, GLB/FBX exports, textures, world maps, Ashram scenes, scripts, docs —
≈ 1 100 files). Kuch bhi copy-paste nahi karna padta.

1. **Nayi Claude Code session kholte waqt:** repository `pratyushgamerz54-oss/animation-studio` chuno aur environment
   **`animation-studio`** chuno (isme Poly Haven ki network permission hai). Pehla message neeche wala **PROMPT** paste karo.
2. Agar session `main` branch par khule, Claude ko bolo: `git fetch origin ccr-a129fdfc-g3v4k0 && git checkout ccr-a129fdfc-g3v4k0`.
3. Setup (Claude khud karega):
   ```bash
   pip install bpy scipy                                  # Blender 5.3 Python module + scipy (maps)
   python3 03_assets/external/polyhaven_fetch.py          # Poly Haven CC0 assets (~1.2 GB, git mein NAHI hain)
   ```
4. **Apne PC par files chahiye?** GitHub → repo → branch `ccr-a129fdfc-g3v4k0` → *Code → Download ZIP*, ya
   `git clone -b ccr-a129fdfc-g3v4k0 https://github.com/pratyushgamerz54-oss/animation-studio.git`.
   `.blend` files Blender mein kholo (ye **Blender 5.3** se bani hain; 4.5 mein khulna verify nahi hua — agar na khule to
   scripts se dobara banti hain). Ashram v3 ke liye PC par bhi `python3 03_assets/external/polyhaven_fetch.py` chalana hoga
   (textures/trees ke liye), warna wo pink/missing dikhenge.

### PROMPT (nayi session mein paste karo)
```
Hum animation-studio project par kaam kar rahe hain (repo pratyushgamerz54-oss/animation-studio, branch ccr-a129fdfc-g3v4k0).
Pehle branch checkout karo, phir HANDOFF.md, STATUS.md, PROJECT_LOG.md, CLAUDE.md padho aur mujhe Hinglish mein poora
detailed summary do: kya bana, kya pending hai, mujhse kya poochna baaki hai. Setup: pip install bpy scipy, aur
python3 03_assets/external/polyhaven_fetch.py. Phir jahan kaam ruka tha wahin se continue karo. Har bade kaam ke baad
commit + push karna aur STATUS.md update karna.
```

---

## 1. Project (Director ke rules — `CLAUDE.md` mein bhi)
- 10-minute 3D superhero film, **Part 1**. Director = user. Claude = 3D artist + VFX team (Blender via Python `bpy`, CPU, no GPU).
- Pipeline: **1 Characters → 2 World/Environment → 3 Assets → 4 Scenes (storyboard, animation, lip-sync, VFX) → 5 Final/post.**
- **Abhi:** Stage 1 done + approved; Stage 2 (world) proposals ban gaye, **Director approval ka intezaar**. Scene animation shuru NAHI.
- **Final VFX rule:** final production mein saare VFX high quality (Mantaflow, real lightning, particles, motion blur, compositor glare,
  GPU render) — design-sheet VFX sirf reference hain.
- Story/script document **abhi tak nahi mila** → koi story event, lore, ruler, portal rule invent nahi karna. Labels: CONFIRMED / PROPOSED / NOT CONFIRMED.

---

## 2. STAGE 1 — CHARACTERS ✅ (Director ne saare designs APPROVE kiye, 20 Nov)

| Character | Role | Powers (confirmed) | Notes |
|---|---|---|---|
| Hero 1 (naam PENDING) | Main hero | Fire, Magical Portal | references ka combination |
| Pratyush | Hero 2 | Super Speed, Portal, Lightning | armoured speed suit (original colours) |
| Saithan | Main villain | Dark Magic, Invisibility, Speed, Fire, (corrupted) Portal, Lightning | borrowed power = apni zindagi ki keemat → **A+B+C teeno** (fracture veins + ash drain + core siphon) |
| Soul | Sub-villain 1 | Lightning (crimson) | weapon story mein? PENDING |
| Max | Sub-villain 2 | Laser — **haath + aankh** | |
| Yayaki | Sub-villain 3 | Teleportation (portal se alag) | |
| Ramarat | Headmaster | **Har power, unlimited** (heroes + villains) | golden-white VFX |

**Har character ke files** (`01_characters/<name>/`):
- `design/` — 7–8 sheet PNGs + `DESIGN_SHEET.md` · `qc/QC_REPORT.md`, `qc.json`, `rigify_qc.json`, `<NAME>_qc_tests.png`, `<ID>_rigify_test.png`
- `blend/<name>_v002.blend` (design model) · `v003` (game/export rig: IK/FK, face controls, baked textures) · **`v004_rigify.blend` (animation rig — animation ke liye YE use karo)**
- `export/<name>.glb`, `.fbx` · `textures/` (baked 1K/512 BaseColor/Rough/Normal/Emission) · `uv/` · `<name>_config.py` (saari design info)
- QC: saare 7 → 0 FAIL; Rigify rest-pose deviation ≤ 0.005 mm, leg IK ok, FK ok, jaw 9.7–10.5 mm.

**Rig features:** skeleton + fingers, IK/FK + poles, real jaw bone, face controls on `root` (expressions, 10 phonemes, jaw_open,
blink, wide, eye aim), robe/skirt 12×3 follow chains (pipe jaisa nahi mudta), Rigify v004 (torso/hips, foot roll, finger curls,
jaw + eye_aim controls, skirt controls).

**Pipeline commands:**
```bash
01_characters/_shared/render_all.sh [chars]      # build v002 + all sheets + test renders (12–25 min/char)
01_characters/_shared/production_all.sh [chars]  # v003 production + v004 Rigify + docs + QC contact sheet
```
Scripts: `charkit.py` (primitives), `charbuild.py` (builder), `vfxkit.py`, `sheet_render.py`, `sheet_compose.py`, `production.py`,
`rigify_build.py`, `sheet_doc.py`, `qc_contact.py`.

**Known small issues:** Ramarat robe par DEFORM/JUMP/LAND poses mein safed daag = ghutna (trousers/skin) skirt ke aar-paar (K-01 clipping,
material bug NAHI — 21 Nov diagnose) → scene stage par cloth sim · jaw/robe ke liye final shots mein cloth sim recommended · Hero 1 ka naam pending.

---

## 3. VFX LIBRARY (`01_characters/_shared/vfxkit.py`) — reference quality
lightning (branching bolts + aura arcs) · magical portal (swirl shader, rim, sparks) + corrupted portal · speed trails + afterimages ·
fire (flames, fireball, aura) · dark magic (wisps, orb) · laser (beam, charge, impact; eye laser for Max) · teleport (rings, motes,
warp) · invisibility (glass dissolve) · Saithan life-cost A/B/C. Har character ke powers page par stage-wise (normal → activation →
full → deactivation) renders hain. **Final film mein inhe high-quality simulation se upgrade karna hai (CLAUDE.md rule).**

---

## 4. STAGE 2 — WORLD (proposals, NOT LOCKED)

### 4a. Main world — `02_world/map_v2/` (script `02_world/_shared/worldgen2.py`) — Revision 01 applied
- 12 000 × 6 000 km, 5 continents: **Aetheria** (home, C1, Ashram) · **Solmara** (C2) · **Veylora** (C3) · **Noxara** (C4 polar) ·
  **Drakmor** (C5) + 3 archipelagos. 17 city sites, 29 towns, 125 villages, ruins, caves, waterfalls (codes only).
- Maps: A illustrated atlas, A2 technical, B continents ×5, C mountains+rivers, D vegetation, E climate, F settlements,
  G Ashram region, H dimensions overview, **H1 Black Hole Training dimension**, **H2 Saithan's Dark World**, I portal network,
  **J GEM hidden region + chamber plan** · `GEOGRAPHY.md` (tables, audit, pending approvals).
- Aetheria detailed map (3 km/cell): `02_world/map/WORLD_MAP_master_v1.png` + regional maps (script `worldgen.py`, seed 7).
- Continuity audit: 0 uphill river steps, 224 river mouths, all cities on rivers/coasts.
- **Ashram (rev 01):** large green valley in Aetheria, forest ring, rivers; snowy range ≈ 100 km NW beyond forest + foothills.
- **GEM (proposal):** hidden ancient region deep in Veylora's enchanted forest, GEM chamber (entrance → passage → antechamber → central chamber).
- **Portals:** CONFIRMED = portals exist + users (Hero 1, Pratyush, Saithan, Ramarat). Routes H1–H5 = HYPOTHETICAL.

### 4b. Environment bible — `02_world/WORLD_BIBLE.md` + `02_world/bible/` (colour bible HEX/RGB + contrast check, location comparison)

### 4c. ASHRAM 3D — `02_world/ashram/` (`ASHRAM_CONCEPT.md`)
- v1 blockout (`01_BLOCKOUT/ASHRAM_blockout_v001.blend`) → v2 procedural look-dev (`..._concept_v002.blend`) →
  **v3 with Poly Haven CC0 assets (`..._concept_v003.blend`)**: carved pillars + brackets, moulded plinths, lattice windows, doors,
  clay-tile roofs, prayer flags, props; 4 km valley + 30 km snow range; fir/sapling/broadleaf/grass/shrub/rock scatter; HDRI day + night.
- Renders `09_RENDER/concept_v3/` (9 day + 3 night) · sheets `00_REFERENCE/ASHRAM_{concept,layout_plan,lighting,materials}_sheet_v3.png`.
- Scripts: `ashram_concept_v2.py` (makes v003 when Poly Haven assets exist), `envkit.py` (procedural vegetation/materials/scatter),
  `phkit.py` (Poly Haven loader, PBR, terrain, HDRI), `ashram_sheets.py`.
- ⚠️ 3D valley terrain abhi map se fit nahi hai (approval ke baad Aetheria R-01 terrain par fit karna hai).
- World overview 3D: `02_world/blend/WORLD_overview_v001.blend` (v1 continent, aerial references).

### 4d. Poly Haven assets — `03_assets/external/` (CC0)
`polyhaven_fetch.py` downloads 14 models (fir_tree_01, fir_sapling_medium, tree_small_02, shrubs, grass, fern, mossy rocks, boulder…),
16 texture sets (2K), 3 HDRIs (4K) into `03_assets/external/polyhaven/` (gitignored). Needs environment `animation-studio`
(hosts api.polyhaven.com + dl.polyhaven.org) and a User-Agent header (already in the script).

---

### 4e. TASK 04 — 3D WORLD BLOCKOUT (`02_world/3d_world/`, milestone 1 done)
Blender **4.5** se bana (bpy 4.5 via `uv venv -p python3.11`, see CLAUDE.md). `00_MASTER_WORLD/WORLD_master_v001.blend` links all components.
Rebuild: `BLENDER=<blender 4.5> 02_world/3d_world/scripts/run_all.sh`. Details: `02_world/3d_world/README.md`, `QC_REPORT.md`,
`01_GEOGRAPHY/WORLD_SCALE.md`. Viewport renders need Mesa EGL (`EGL_PLATFORM=surfaceless`).

## 5. Director se PENDING (jawab chahiye)
1. Hero 1 ka naam · Soul ka weapon story mein hai?
2. **World map revision 01 approve?** Continent names ka assignment, Ashram jagah + snow distance, dono dimensions ka look,
   GEM hidden region + chamber, kaunse portal routes (H1–H5) sach mein hain.
3. Story / script document · Blender version on Director's PC (4.5 ya 5.x?).
4. Approval ke baad next: Ashram terrain ko map par fit karna + Phase 4 detailed Ashram, phir Black Hole Training Area (Phase 5),
   GEM location (Phase 6), Saithan's Dark World (Phase 7).

## 6. Naye technical lessons (CLAUDE.md mein bhi)
- Background waiter mein `pgrep -f '<text>'` mat use karo — wo khud ko match karta hai; log file mein marker (ALLDONE) grep karo.
- Alpha leaf/needle cards: `cycles.transparent_max_bounces = 64` (warna kaale patte); join se pehle har mesh par same UV layer naam.
- `reset_pose` driven bones (jaw) ka rotation mode nahi badalna; driver test se pehle `arm.update_tag()`.
- Rigify: human template re-fit karo (bone collections chahiye); `spine.004.connect_chain=False`; template bones (jaw) par bhi
  rigify_type set karo; bone-parented objects re-parent karte waqt constraints mute; Rigify re-roll → skirt TRANSFORM ranges flip check.
- Poly Haven: User-Agent header chahiye; .blend LOD collections append karke `fix_paths()`; save with `relative_remap=True`.
- World volume sooraj ko block karta hai → bounded haze box use karo. Sun camera ke peeche = flat light → side light.

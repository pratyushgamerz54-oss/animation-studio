# Production Inventory — Part 1 (10 min film)

Phase: **CHARACTER PRODUCTION** (scene animation abhi shuru NAHI karni hai)
Tool: Blender 5.3 (`bpy` Python module), Cycles CPU render, Rigify available.

Status legend: ⬜ not started · 🟨 in progress / proposal · ✅ approved & tested

## 1. Characters

Pipeline (same for all): `_shared/build_char.py` → `_shared/sheet_render.py` → `_shared/sheet_compose.py` →
`_shared/production.py` → `_shared/sheet_doc.py`. One config per character: `<folder>/<folder>_config.py`.
Batch scripts: `_shared/render_all.sh`, `_shared/production_all.sh`.

| # | Role | Name | Confirmed powers | Config | Design sheet | 3D model v002 | Production v003 (UV, bake, IK/FK, face ctrl, export, QC) |
|---|------|------|------------------|---|---|---|---|
| 1 | Hero 1 | **Shiv** ✅ (21 Nov) | Fire, Magical Portal | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 2 | Hero 2 | **Pratyush** | Super Speed, Magical Portal, Lightning | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 3 | Main Villain | **Saithan** | Dark Magic, Invisibility, Super Speed, Fire, Magical Portal, Lightning | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 4 | Sub-villain 1 | **Soul** | Lightning (confirmed 20 Nov) | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 5 | Sub-villain 2 | **Max** | Laser | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 6 | Sub-villain 3 | **Yayaki** | Teleportation | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |
| 7 | Headmaster | **Ramarat** | EVERY power (heroes + villains): Fire, Portal, Speed, Lightning, Dark Magic, Invisibility, Laser, Teleportation — unlimited (confirmed 20 Nov) | ✅ | 🟨 v1 done — awaiting approval | ✅ | ✅ v003 done, QC all PASS (approval pending) |

Legend: ✅ done & tested · 🟨 in progress / awaiting approval · ⬜ not started. Each character's real status is in
`<folder>/qc/QC_REPORT.md` once production has run.

## 1b. Director references (received)

| Character | Reference file | Key visual direction taken |
|---|---|---|
| Hero 1 | — (none) | Director: **build Hero 1 by combining elements of these references** → proposal pending |
| Pratyush | `pratyush/reference/pratyush_ref_01.png` | Armoured full-body speed suit, crackling lightning, sprint pose. Kept original: navy/blue colours, chevron emblem, no cowl |
| Saithan | `saithan/reference/saithan_ref_01.png` | Horned dark armour, spiked pauldrons, glowing blue chest core, red eyes, storm/lightning above |
| Soul | `soul/reference/soul_ref_01.png` | Tall pale horned figure, ornate black-gold collar, long dark robe, carries a curved blade/scythe weapon (power still NOT confirmed) |
| Max | `max/reference/max_ref_01.png` | Bald, blue-grey skin, red eyes, sci-fi armour with green glowing chest lenses & accents |
| Yayaki | `yayaki/reference/yayaki_ref_01.png` | Hooded purple-black armoured figure, glowing purple chest sigil, flame-like purple energy at arms |
| Ramarat | `ramarat/reference/ramarat_ref_01.png` | Old man, long white hair & beard, royal-blue robe with silver/gold embroidery, red sash, barefoot (powers NOT confirmed) |

Rule: references guide the design; final designs stay **original** (no copied logos/costumes of existing franchises).

## 1c. Per-character expression lists (from Director tasks)
- Hero 1 / Pratyush: neutral, happy, angry, sad, fear, shocked, confident, evil smile, serious, crying
- Saithan: neutral, evil smile, angry, furious, confident, serious, manipulative smile, shocked, pain, power concentration
- Soul / Max / Yayaki: neutral, angry, evil smile, serious, confident, shocked, frustrated, suspicious, fear, furious
- Ramarat: neutral, wise, serious, angry, disappointed, suspicious, concerned, confident, shocked, furious

## 1d. Story mechanic to preserve
- **Saithan — borrowed powers:** borrowing a power costs Saithan part of his own life. The *visual* of the
  cost is NOT decided → present alternatives for approval (U-08).

## 2. VFX asset library (planned)

| Character | Effects |
|---|---|
| Hero 1 | Fireball, Flame trail, Fire aura, Magical portal |
| Pratyush | Lightning, Speed trails, Afterimage, Lightning aura, Magical portal |
| Saithan | Dark energy, Invisibility, Dark fire, Lightning, Corrupted portal, Dark aura |
| Max | Laser beam, Laser impact, Laser charge-up |
| Yayaki | Teleportation, Spatial distortion, Teleport arrival/departure |
| Soul | Crimson lightning, arcs, aura |
| Ramarat | All 8 powers in golden-white |

## 3. Per-character deliverables (har character ke liye)

Design sheet: full body (front, back, left, right ortho; 3/4 front; 3/4 back; neutral; T-pose; A-pose),
face (front, side, 3/4, eye, brows, features, hairline, proportions), 10 expressions,
costume breakdown, color palette (HEX + RGB), body proportions + measurement guide,
power activation design + separate VFX reference per power.

3D: head/body/hands/feet/face/hair meshes, separate clothing & accessories, clean quad topology →
UV + PBR textures → Rigify body rig (IK/FK, poles, fingers) + facial rig + phonemes
(A, E, I, O, U, M/B/P, F/V, L, W, Rest) → 13 QC tests → .blend + FBX/GLB + renders.

## 4. Folder & naming convention

```
01_characters/
  PRODUCTION_INVENTORY.md
  _shared/            reusable build library (charkit.py), materials, rig templates
  <name>/
    design/           DESIGN_SHEET.md + sheet PNGs (proposal → approved)
    blend/            <name>_vNNN.blend (incremental backups)
    textures/  uv/  export/ (FBX/GLB)  renders/  qc/ (test reports)
    build_<name>.py   script that rebuilds the character from scratch
```
Blender collections: CHARACTERS, BODY, FACE, HAIR, CLOTHING, ACCESSORIES, RIG, CONTROLS, MATERIALS, VFX.
Object names: `CHAR_<NAME>_<PART>` (e.g. `CHAR_PRATYUSH_HEAD`, `CHAR_PRATYUSH_RIG`).

## 5. Unresolved decisions (Director se confirm karna hai)

| ID | Item | Status |
|---|---|---|
| U-01 | Hero 1 ka naam | ✅ RESOLVED (21 Nov): **Shiv** (files/ids `hero1`/`HERO1` unchanged) |
| U-02 | Soul ki power | ✅ RESOLVED: Lightning (crimson-red look proposed) |
| U-03 | Ramarat ki powers | ✅ RESOLVED: every power of heroes AND villains, unlimited (golden-white look proposed) |
| U-04 | Kisi bhi character ka appearance (umar, kad, skin tone, hair, costume) diya nahi gaya hai → sab designs **PROPOSALS** hain jab tak Director approve na kare | PENDING |
| U-05 | Duniya / setting (magic school? city? time period?) — headmaster se school-type setting lagti hai, par confirm nahi | PENDING |
| U-06 | Har character ki portal ka rang/style (Hero 1, Pratyush, Saithan teeno ke paas portal hai) | PROPOSED in sheets |
| U-07 | Characters ki umar (students? adults?) | PENDING |
| U-08 | Saithan borrowed-power life-cost ka visual | ALTERNATIVES to be presented |
| U-09 | Hero 1 = combination of references — which elements? | PROPOSAL pending |
| U-10 | Soul reference mein weapon (scythe) hai — kya story mein hai? (task: unnecessary weapons mat add karo) | PENDING |

## 6. Known technical limits (honest)

- Machine: 4 CPU cores, koi GPU nahi → preview renders yahan, final HD render Director ke PC par.
- Models Python code se ban rahe hain (procedural modeling), haath se sculpt nahi. Stylized realism tak
  achha jaayega; photoreal skin/pores/hair-strand level close-ups ke liye extra sculpt pass chahiye hoga.
- Design sheets 3D renders se banti hain (2D painting nahi).

## 7. QC findings after production v003 (20 Nov)
- All 7: UV ✅, baked textures (1K main / 512 small) ✅, IK follow 0.02–0.03 mm ✅, 0 unweighted verts ✅, all-quad body/head ✅,
  19 mouth keys incl. 10 phonemes ✅, GLB + FBX export + re-import ✅. Contact sheets: `<name>/qc/<NAME>_qc_tests.png`.
- KNOWN ISSUE K-01 — **Director decision 21 Nov: fix with CLOTH SIMULATION at scene stage** (waist/belt pinned, body collision, per shot; Ramarat, Soul, Saithan, Yayaki): long robes/skirts (Ramarat, Soul, Saithan, Yayaki) are skinned to the legs → in RUN / JUMP / LAND / deform
  poses they bend like a stiff tube. Fix planned at scene stage: cloth simulation (pinned at waist) or extra skirt bones.
  (21 Nov: Ramarat ke robe par 'safed daag' = isi ka hissa — raised knee (trousers/skin) skirt ke aar-paar; material bug nahi.)
- K-02: Soul robe front panels leave a small gap between the legs (front view). K-03: Saithan powers page — eye row touches footer.
- K-04: Jaw bone does not move (mouth shape keys only). Rig is custom (not Rigify) but has IK/FK, poles, switches, fingers, face controls.

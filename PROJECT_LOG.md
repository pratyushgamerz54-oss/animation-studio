# PROJECT LOG — Animation Studio (poori kahani shuru se)

> Har nayi session mein Claude ye file padh kar Director ko summary deta hai. Naya kaam hone par niche entry jodo.

## Project
- 10-minute cinematic 3D superhero animated film — **Part 1**. Director = user. Claude = 3D artist + VFX team.
- Tool: Blender 5.3 as Python module (`pip install bpy`), Cycles CPU (no GPU here). Final HD render Director ke GPU PC par.
- Repo: `pratyushgamerz54-oss/animation-studio`, branch **`ccr-a129fdfc-g3v4k0`** (saara kaam yahin hai).

## Pipeline (Director ne tay kiya)
1. Character model sheets → 2. Environment & world bible → 3. Asset production → 4. Scene-by-scene production
(storyboard, camera, animation, dialogue, lip-sync, VFX) → 5. Final animation & post (render, compositing, sound, edit, QC).
**Abhi stage 1 (characters) chal raha hai. Scene animation shuru NAHI karni.**

## Characters (Director confirmed)
| Character | Role | Powers | Reference |
|---|---|---|---|
| Hero 1 (naam PENDING) | Main hero | Fire, Magical Portal | koi nahi — Director: "sab references jod ke banao" |
| Pratyush | Hero 2 | Super Speed, Magical Portal, Lightning | daudta speedster (Flash jaisa — copy nahi kiya) |
| Saithan | Main villain | Dark Magic, Invisibility, Super Speed, Fire, Portal, Lightning + **borrowed power ki keemat apni zindagi** | seeng, kaala armor, neela chest glow |
| Soul | Sub-villain 1 | Lightning (20 Nov confirm) | pale, laal seeng, sunehri collar, robe (hathiyaar story mein? PENDING) |
| Max | Sub-villain 2 | Laser | ganja, neela-grey skin, hara glow armor |
| Yayaki | Sub-villain 3 | Teleportation | purple hood, chest sigil |
| Ramarat | Headmaster | **Har power, unlimited** (heroes + villains) | budhe, safed daadhi, neela robe, laal sash |

## Timeline — kya kya hua
1. **Setup:** bpy install, CLAUDE.md rules, folder structure (01_characters … 05_post). GitHub push pehle 403 tha, baad mein access theek hua.
2. **Master instruction mila** (7 characters, design sheet → model → UV → rig → face → VFX → QC). Production inventory bana.
3. **Pratyush v1:** pehla character code se bana (skin-modifier body, sculpted head, eyes/lids/brows/mouth face kit,
   shape keys for 10 expressions + 10 phonemes, ribbon hair, clothing from body surface, 53-bone rig).
   7-page design sheet (turnaround, poses+measurements, face, expressions, costume, palette, powers). Kai bugs fix:
   eyelid parenting, belt khaali, portal shader axis, layout.
4. **References aaye** (6 images) + 7 task briefs. Pratyush ko armored speed-suit mein redesign kiya (original colours).
5. **Director:** "sab ka permission, chehra aur badhiya." → **generic config-driven pipeline** banaya
   (`_shared/charbuild.py`), chehra upgrade (jawline, chin, brow ridge, nose structure, philtrum, nasolabial folds,
   cheekbones, skin blush), hair styles (spiky/swept/long), beard, horns, robe/hood/cape/collar/spikes.
6. **Saare 7 characters ke config + 3D models (v002)** bane, mesh-sanity QC pass (bugs: double weights, fingertip
   solidify spikes, pauldron fold → rigid on clavicle).
7. **Naye VFX:** fire/fireball, dark magic, laser, teleport rings + warp, invisibility (glass dissolve), corrupted portal.
8. **Production pipeline** (`_shared/production.py`): UV + layouts, baked textures, IK/FK (hand/foot IK, poles,
   switches, COG), face controls (expressions, phonemes, jaw_open, blink, wide, eye aim), GLB/FBX export + re-import, QC report.
   Pratyush par test: sab checks PASS.
9. **Batch render** saari design sheets: saare 7 ✅ (Saithan 8 pages + life-cost A/B/C). Fix re-render batch 2 ✅.
10. **Director rules:** final production mein saare VFX HIGH quality; memory reset ke baad bhi sab yaad rahe (ye log + STATUS.md).

11. **Production v003 saare 7 ka DONE (20 Nov 19:00):** UV, baked textures, IK/FK rig, face controls, GLB/FBX, QC — sab PASS.
    QC contact sheets `<name>/qc/<NAME>_qc_tests.png`. Known issues K-01..K-04 in PRODUCTION_INVENTORY §7
    (robe stiff in action poses → cloth sim at scene stage). **Stage 1 complete; Director approval ka intezaar.**

12. **20-21 Nov — Director ne saare character designs APPROVE kiye.** Max laser = haath + aankh, Saithan cost = A+B+C.
    "Saari kamiyan theek karo" → skirt follow-rig (12x3 chains), asli jaw bone, Rigify rig v004 (`rigify_build.py`),
    Soul robe band, Max eye-laser row, Saithan A+B+C page. Full re-render + production batch chalaya.
13. **21 Nov — STAGE 2 shuru (World, Director TASK 01).** Pehla milestone: procedural master world map (1024x768 km,
    8 proposed regions, rivers/lakes from real hydrology, cities/villages/ruins/caves/waterfalls/hidden areas, dimensions panel,
    GEM unplaced), regional + elevation maps, Blender overview terrain + aerial renders, Environment Bible draft
    (`02_world/WORLD_BIBLE.md`), colour bible + contrast check, location comparison, Ashram 3D concept blockout
    (Himalayan foothill gurukul PROPOSAL) + concept/layout/lighting/material sheets. **Sab PROPOSAL, map NOT LOCKED.**

14. **21 Nov — TASK 02 grand world map + REVISION 01:** v1 continent merged as home continent Aetheria in a 12 000 x 6 000 km
    main world (5 continents, 3 archipelagos), maps A–J (`02_world/map_v2/`), Ashram moved to a large green valley, GEM hidden
    region proposal, two dimension layouts, portal diagram (all routes hypothetical). Ashram v3 (Poly Haven assets) renders + sheets done.
    Characters: production v003 + Rigify v004 for all 7 — all QC pass.

## Director se jawab chahiye (pending)
- Hero 1 ka naam · saare designs approve/badlav · Saithan life-cost: A (cracks) / B (ash) / C (core siphon)
- Soul ka hathiyaar story mein hai? · (Max laser + Saithan cost RESOLVED 20 Nov)
- WORLD: master map approve? region names? Ashram direction? story/script document? Blender version on PC? (WORLD_BIBLE.md §3, §10)

## Kahan kya hai
- Rules: `CLAUDE.md` · Abhi ka status: `STATUS.md` · Characters ka status: `01_characters/PRODUCTION_INVENTORY.md`
- Har character: `01_characters/<name>/` → `<name>_config.py`, `blend/`, `design/` (sheets + DESIGN_SHEET.md),
  `qc/QC_REPORT.md`, `textures/`, `uv/`, `export/`, `reference/`

15. **21 Nov (nayi session):** setup restore (bpy 5.3, scipy, Poly Haven fetch). Ramarat robe "safed daag" diagnose = knee clipping
    through skirt (K-01), material nahi. Sab Stage 2 kaam Director approval par ruka hai.

16. **21 Nov — TASK 04 (3D world blockout) milestone 1:** `02_world/3d_world/` — real 3D terrain of the whole main world from
    map v2 rev 01 (Blender 4.5.16 LTS), regions by direction + theme, rivers/lakes/ocean/islands/underground/ruined zones, Ashram Valley
    true-scale LOD terrain (snow range ≈101 km NW), Black Hole + Dark World dimension blockouts, 38 preview images, QC 70/70 (4.5 + 5.3).
    Sab PROPOSAL — Director review ka intezaar.

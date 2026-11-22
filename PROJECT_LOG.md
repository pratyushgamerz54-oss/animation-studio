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
17. **21 Nov — TASK 04 CLOSED.** Director ne blockout layout ko APPROVED FOR DETAILED ENVIRONMENT PRODUCTION kiya (conditions: layout
    preserve, map rev 01 = proposal, GEM unconfirmed, dimensions preserve, files + backups safe). v001 baseline checksummed + save-guard;
    saare 16 backups git mein. Closeout `02_world/3d_world/TASK04_CLOSEOUT.md`. Ab TASK 05 ki taiyaari.
18. **21 Nov — Session 2 handoff:** `HANDOFF.md` poora naya (sab kaam + kya dobara nahi banana + Task 05 plan), `setup_session.sh`
    (ek command setup: bpy 5.3 + bpy 4.5 + Mesa + Poly Haven + baseline check). Next session: TASK 05 brief se shuru.
19. **21 Nov — Session 3:** restore. Director: **Hero 1 ka naam = Shiv** (config/docs updated; folder + object ids `hero1`/`HERO1` same, sheet PNGs abhi 'HERO 1' print karti hain). **K-01 robe clipping → cloth simulation** scene stage par (Ramarat, Soul, Saithan, Yayaki). Next: TASK 05 brief.
20. **21 Nov — TASK 05 milestone 1 (in progress):** detailed terrain v002 (Ashram Valley 2 m/10 m/40 m/400 m LODs, northern forest belt 2 m + Poly Haven trees, mountain NW01 30 m + erosion, waterfall gorge 1.5 m), PBR library (20 materials), nature library (101 assets), GN heightfield + scatter systems, water (rivers, lake, waterfall), master + 7 cameras. Director rule: final MP4 4K, no blur. Details: HANDOFF §6.
21. **21 Nov — TASK 05 milestone 1 review:** Director approved shots 1, 2, 6, 7, 7b; asked for a wide cascade waterfall with better physics + better snowy peaks, then milestone 2.
22. **21 Nov — TASK 05 COMPLETE:** milestone 2 — R04 desert (+ shot 5), R05 forbidden crater, R02 enchanted forest, R03 Great Northern Range core + cave entrance (scanned-rock kitbash), main-world v002 (smooth lake shores, coasts, islands). QC M2 45/45 (M1 56/56). Awaiting Director review + next TASK.
23. **21 Nov — Director feedback on milestone 2 applied:** R05 crater (rugged inner wall + talus, black lake filling the basin, no puddles, ejecta blocks, darker ash), cave (forest-floor litter, AO + moss on scanned rock), R04 dunes (megadunes, knife-edge crests, warmer aspect-coloured sand, low sun). QC M2 45/45.
24. **21 Nov — TASK 05 APPROVED + CLOSED** (Director: "Badhiya hai"). Waiting for the next TASK prompt.
25. **21 Nov — TASK 06 brief (Ecosystem & Vegetation Bible) received.** Milestone 1: Ashram Valley vegetation library, Enchanted Forest tree collection, Mountain Kingdom references → concepts for approval. Built own procedural vegetation generator (Blender 4.5), leaf atlases, bark PBR (Poly Haven), wind system, 3 regional libraries (42 real 3D assets), Ecosystem Bible + wildlife proposal. Details: `03_assets/vegetation/README.md`.
26. **22 Nov — TASK 06 milestone 1 COMPLETE:** 21 tree/shrub sheets (front/side/back + ruler + 1.75 m figure, leaf + trunk-foot close-ups, bark/leaf maps, palette, specs), plant libraries, regional sheets, contact sheet, wind test clip; QC 337/337 in Blender 4.5 and 5.3, textures 25/25. Awaiting Director review (questions: Bible §12).
27. **22 Nov — Decision Sheet 01 applied:** World Bible, Map Rev 01 docs (GEOGRAPHY.md), Ecosystem Bible v2, regional sheets, EF vegetation reference, Ashram landscaping plan (+ plan image), wildlife selection sheet (60 animals, PENDING), Spring season reference, Blender 4.5 production checklist; fantasy labels + subtle glow in the libraries (QC 379/379); automated verification 33/33. Director feedback on milestone 1: add more physics to the wind, rest OK.
28. **22 Nov — Realism pass (Director: "texture asli, polish jaisa nahi"):** all T6 vegetation materials (rough / matte, low specular, mottling, blemishes, AO dirt, micro-bump, blade streaks, organic fungus caps) + scanned ground; TASK 05 terrain materials too (Director: "Ha laga do") — specular lowered, dry roughness floor, satin wet ground, weathered ice; approved v002 material lib backed up; 8 TASK 05 shots re-rendered (`12_RENDER/T5/cycles_realism/`, before/after sheet); QC T5 56/56 + 45/45, T6 379/379 (4.5 + 5.3).
29. **22 Nov — Wind physics v2 → v3:** v2 = drag ∝ v², natural frequency, advected gust fronts, lag, crosswind, length-preserving bend (`WIND_TEST_v2.mp4`); Director: near plants move "lakdi jaise" → v3 = near-camera vegetation realized with per-blade / frond bending (stiff root, flexible tip, per-blade phase, 9 m gust waves), far = instance tilt; spring kans variant (no plumes).
30. **22 Nov — Director rules (CLAUDE.md):** REAL-WORLD REALISM RULE — textures + every motion (plants, water, cloth, creatures, VFX, camera) + physics / destruction (real scale + gravity, material-based fracture, rigid body, Mantaflow dust) must look like the real world.
31. **22 Nov — Leaf realism v2 + save for the next session:** soft veins, tone variation, spots, insect bites, rounded Peepal base; Director inputs saved verbatim (`02_world/ecosystem/DIRECTOR_INPUTS_TASK06.md`); HANDOFF §6b updated; pending renders finish with `03_assets/vegetation/scripts/t6_finish_pending.sh`.
32. **22 Nov — Autosave + SAVE RULE (Director: "sab apne aap save hona chahiye"):** project Stop hook `.claude/settings.json` → `.claude/hooks/autosave.sh` (commit + push all changes at every reply end; safe: current branch, no force, > 95 MB skipped, merge-on-moved-remote, retries) — tested in a sandbox repo (5 cases); CLAUDE.md SAVE RULE (verbatim Director inputs, outputs in repo, resume scripts, milestone handoffs, repo-size care).
33. **22 Nov — Session 5 · realism v3 everywhere (Director's list: natural less-saturated leaves with varied shades + few dry leaves + faint dust, dry thatch at grass bases, varied blade widths + streaks, irregular roots with soil, crinkled paper-like petals, matte stems, natural camera look instead of "Medium High Contrast"):** applied to every asset; milestone-1 sheets re-rendered with the camera look (resumable `t6_finish_pending.sh`); v3.1: moss shader with shoots + fuzz (no CG cells), dead thatch lies ON the ground.
34. **22 Nov — TASK 06 MILESTONE 2 (Director: "jitne bhi task bache hai … un sab ko pura karo"):** 7 new regional libraries (R-06 Green Plains, R-08 Crystal Lakes, R-04 Golden Desert, R-05 Forbidden Lands, C-01/02/03 Ancient City sites, CV caves, Natural Details) + silver fir / blue pine (R-03) + glow moss (R-02, ≤ 0.15) → 84 hero assets; palm / succulent / ivy / water-lily / natural-detail generators; 14 new atlases; variants (3 per species) + LOD1 / LOD2 / impostor LOD3; NG_T6_ECOSYSTEM scatter (TASK 05 logic + Poisson spacing, zones, 4 LOD bands, near per-vertex wind with per-instance phase, far instance tilt); populated region files on the approved TASK 05 masters (save-as copies; T5 untouched): R-01 (ONE Peepal on a PROPOSED chabutra + PROPOSED garden beds), R-02 (~75/25), R-03 (M1 forest), R-04 (bare dunes, interdune shrubs, wadi trees; no oasis water in TASK 05 → no date palms placed), R-05 (charred rim). Details: `02_world/ecosystem/ECOSYSTEM_BIBLE.md` §13, HANDOFF §6c.
35. **22 Nov — TASK 06 milestone 2 closeout:** fixes found by review + QC — variant / LOD files lost materials (same-name `new_mat` → protected names + empty-slot assert), flat pads rejected by the slope test, Poisson over 64 km tiles (OOM) → face culling first, realize distance memory, cameras placed by masks on their own tile + above the highest nearby ground, camera clearance, Mountain conifer density, grass blades resting on the ground hold still (friction); 14 populated previews + sheet; QC 904/904 (4.5) · 904/904 (5.3) · 39/39 textures · 58/58 populated. Repo `.git` ≈ 4.3 GB → storage-plan question to the Director.
36. **22 Nov — Storage plan (Director):** main repo ≈ 4.4 GB → Director created **`animation-studio-scenes`** for Stage 4 + 5; set up (README, CLAUDE.md two-repo rules, `04_scenes/`, `05_post/`, gitignore for final 4K masters) on branch `ccr-c375d59d-2qaoyn`; autosave hook now saves BOTH repos and warns on files > 50 MB / repos > 5 GB (sandbox-tested); HANDOFF §0 / §0b, CLAUDE.md, setup check updated. Nothing moved — main repo stays the asset library.

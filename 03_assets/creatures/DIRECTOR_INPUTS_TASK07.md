# DIRECTOR INPUTS — TASK 07 (verbatim) + what was done / where

> SAVE RULE §2: every Director brief, decision and feedback for TASK 07 is copied here **word for word**, followed by what Claude did.

---

## A. TASK 07 brief (Director, 22 Nov 2026, session 6) — verbatim

```
TASK 07 — THE GRAND UNIVERSE: WILDLIFE & CREATURE PRODUCTION

You are the Creature Design Director, Wildlife Artist and 3D Character Production Supervisor.

Create a complete wildlife ecosystem for our massive fantasy universe.

All creatures must fit their geographical environments.

This is a reusable asset production task, not just a collection of illustrations.

PART 1 — CREATURE CATEGORIES

Develop the following categories:

1. Forest wildlife.
2. Mountain wildlife.
3. Grassland wildlife.
4. Desert wildlife.
5. Aquatic wildlife.
6. Aerial creatures.
7. Underground creatures.
8. Rare fantasy creatures.
9. Ancient mythical-looking creatures.
10. Small environmental creatures.

Keep ordinary wildlife and fictional fantasy species clearly distinguished.

PART 2 — ORDINARY WILDLIFE

Develop original visual references for:

- Deer.
- Rabbits.
- Foxes.
- Wolves.
- Bears.
- Birds.
- Eagles.
- Owls.
- Fish.
- Butterflies.
- Insects.
- Reptiles.

These are proposed species, not confirmed story characters.

PART 3 — FANTASY CREATURES

Propose a small collection of original creatures.

Possible design directions:

- Giant forest guardian animal.
- Rare mountain flyer.
- Mysterious aquatic creature.
- Ancient underground creature.
- Small magical-looking forest animal.

Do not create intelligent races, villains, talking creatures or story characters without approval.

Do not assign magical powers unless approved.

PART 4 — COMPLETE CREATURE DESIGN SHEETS

For each approved creature, create:

1. Full-body front view.
2. Full-body side view.
3. Full-body back view.
4. Three-quarter view.
5. Face close-up.
6. Anatomy reference.
7. Color palette.
8. Scale comparison.
9. Expression references where appropriate.

Maintain consistent anatomy across all views.

PART 5 — ANATOMY AND MEASUREMENTS

Specify:

- Height.
- Body length.
- Wingspan where applicable.
- Head proportions.
- Limb dimensions.
- Tail dimensions.
- Body structure.
- Surface details.
- Fur, feathers, scales or skin characteristics.

PART 6 — ACTUAL BLENDER 3D MODELING

Create actual 3D models.

Requirements:

- Clean geometry.
- Proper topology.
- UV mapping.
- PBR textures.
- Detailed surface materials.
- Anatomically coherent proportions.
- Separate components where useful.

Do not substitute concept art for actual geometry.

PART 7 — RIGGING AND ANIMATION

For suitable creatures, create:

- Body rig.
- Head controls.
- Leg controls.
- Tail controls.
- Wing controls.
- Jaw controls.
- Eye controls.
- IK/FK where appropriate.

Create basic animation tests:

- Walking.
- Running.
- Flying.
- Swimming.
- Turning.
- Resting.
- Environmental interaction.

Only test actions appropriate to the creature's anatomy.

PART 8 — ECOSYSTEM PLACEMENT

Document:

- Natural habitat.
- Geographical region.
- Terrain requirements.
- Vegetation requirements.
- Water requirements.
- Approximate scale.
- Environmental role.

Do not invent complex food chains or story lore as confirmed facts.

PART 9 — BLENDER ASSET LIBRARY

Organize assets into:

00_CREATURE_REFERENCES
01_FOREST_WILDLIFE
02_MOUNTAIN_WILDLIFE
03_GRASSLAND_WILDLIFE
04_DESERT_WILDLIFE
05_AQUATIC_WILDLIFE
06_AERIAL_CREATURES
07_UNDERGROUND_CREATURES
08_FANTASY_CREATURES
09_RIGS
10_ANIMATION_TESTS
11_TEXTURES
12_BACKUPS

PART 10 — FINAL DELIVERABLES

Provide:

- Wildlife design bible.
- Creature reference sheets.
- Anatomy references.
- Color palettes.
- Actual Blender models.
- UV maps and textures.
- Rigged models.
- Animation tests.
- Preview renders.
- Asset library.
- Technical QC report.

STRICT RULES

- Preserve the approved world geography.
- Do not invent story characters.
- Keep proposed creatures separate from confirmed story elements.
- Do not add unnecessary magical powers.
- Maintain consistent creature anatomy.
- Verify actual Blender files.
- Save incremental backups.
- Do not start film scene animation.

FIRST MILESTONE:

Create a wildlife concept collection for the Enchanted Forest, Mountain Kingdom and Crystal Lakes.

Present the creature designs for approval before full 3D production.
```

---

## B. What Claude did (log — updated as work progresses)

| Date | Step | Where |
|---|---|---|
| 22 Nov | Brief saved verbatim; library folders 00–12 created (Part 9) | `03_assets/creatures/` |

---

## C. Director feedback (23 Nov, during milestone 1 — verbatim)

```
Continue aur gaa real world se dekho kaya creature aur animal ka animation aur pic aur phir waise hi bana aur waise hi texture real jaisa kya ye karna baki hai ya karo ge
```

**Claude:** yes — real-world reference step added to the pipeline: for every species, real photos (Wikimedia Commons, license recorded) +
field-guide measurements + coat / feather pattern notes → compare side by side with the 3D render → fix shape / coat → only then the
concept sheet. Movement references (gait timing, wingbeat frequency, swim cycle) are collected now and used in milestone 2 (rig + animation tests).
Reference board per species: `00_CREATURE_REFERENCES/photo_refs/<species>/` + `REFERENCE_NOTES.md`.

---

## D. Director decision — model source (23 Nov, verbatim)

1. (via `/meshy-3d-agent:meshy-openclaw` command)
```
/meshy-3d-agent:meshy-3d-generation   use both for work for model and mere creture ko taiyar karke phele ek karke hamko preview dikhana fir mai approve Kari to aage badho
```
2. (after the Meshy login started — login stopped, no credential stored)
```
Mat kar isse rehne de tu jais ekar rha tha waise hi kaam kar apan
In teeno ki mix kar use kar  samjha lekin animation time koi jhamela na ho hona chaiye real jaise hona chiye us samay aur ye log real animals jaise behave karne chiye naki aise hi kuch bhi jaise world me hote hai to ye to baa fka kama hai tu in teno ka use mix karke kar taki jaldi aur realistic output aaye 1. Isi tarike se continue: har species ko photo se milakar baar-baar sudhaarunga. Kaam hoga, par dheere, aur chehre poori tarah asli shayad na ban paayein.
2. Ready-made CC models base banayein (recommended): asli jaanwar jaise free-license 3D models (jaise Sketchfab ke CC-BY scan / sculpt) ko base banaun, phir unhe saaf karun, apna rig, fur aur texture lagaun. Isse sabse asli result aayega. Iske liye ek aur website allow karni padegi.
3. Meshy (AI 3D generation): is session mein available hai. Ye external service hai, isliye aapki permission ke bina use nahi karunga.
```
**Claude's reading:** continue the current way, but MIX all three sources (own procedural kit + free-licence CC models + Meshy) to get
realistic results faster; ONE creature at a time → preview → Director approval → next. Animation must have no problems: real-world
animal behaviour and gaits (no "anything goes" motion). Meshy login stopped on request (not used until the Director says so).

---

## E. Director (23 Nov, after the Sambar v002 preview + status question) — verbatim

```
Kya task seven ka sara kaam hogaya hai kitna bacha hai
```
```
Ha tu karna aur baki creture ko bhi yhi se na loge pehle jo kiye the wo bhi na sara na kitn
```
**Claude's reading:** go ahead (Sambar v002 direction OK to continue); ALL remaining creatures from the same mix pipeline
(Sketchfab CC base + own work + real photos), and the earlier procedural tests (wolf, red fox, golden eagle) are redone the same way.
One creature at a time, preview → Director → next. Next: Himalayan wolf.

---

## F. Director feedback (23 Nov, after the Himalayan wolf preview) — verbatim

```
Thoda dhyan se dekho na sambhar ka walk me ek jerk aarha hai thoda wo fix karke smooth animation karo jaise radr 2 game me jo creture hai apne aap kaam karte hai real world jaise kya ye bhi waise hi karege bahle mai waha pe hu ya nhi jaise real hi agar mai mai koi harkat karta hu to waise act karenge jaise real world me hota hai kya ye ho ga na
```
**Claude:** (1) sambar walk jerk → find + fix, smooth continuous walk; (2) RDR2-style behaviour: creatures act on their own like
real animals (graze, look around, alert, flee) and REACT to a character's presence / movement — built as a behaviour system
for the scene files (Blender: reacts per shot to the character's path; film = baked, not a real-time game).

---

## G. Director (23 Nov) — verbatim
```
Ha ab shi hai RDR2 jaise creatures — haan, aisa hoga, ek fark ke saath: [quoted Claude's behaviour-baker plan] … Thik hai ab aage kaam chalu karo
```
**Status:** Sambar walk fix v002b OK ("ab shi hai"); behaviour-baker plan (`09_RIGS/T7_BEHAVIOUR_SYSTEM.md`) accepted → build in
milestone 2. Continue with the next creatures (one by one, preview → Director).

---

## H. Director (23 Nov, after the Asiatic black bear preview) — verbatim
```
Ha approve hai jo kami hoga theek kar lena
```
**Status:** Asiatic black bear v002 APPROVED (concept/preview stage); listed gaps to be fixed in production (`PRODUCTION_FIX_LIST.md`).

---

## I. Director (23 Nov, after the golden eagle preview) — verbatim
```
Aur agar jarurat pade to three js ka bhi use kar kena
```
**Claude:** Three.js may be used where it helps (e.g. interactive 3D previews the Director can rotate on the phone). Eagle approval +
juvenile/adult choice still open.

---

## J. Director (23 Nov, golden eagle) — verbatim
```
Approve hai
```
**Status:** Golden eagle v002 (museum scan, juvenile plumage as shown) APPROVED. Age not changed (juvenile kept; adult recolour only if
the Director asks). Next: red fox.

---

## K. Director (23 Nov) — STANDING RULE, verbatim
```
Ek baat bata de rha hai three js ka use karte rehna ab se taki aacha kaam ho aur mafa mile last me agar koi badhiya se na hua hi to ho jaye chae world hi enviyho creture ya faun ya flora hi ya phir chracter ho ye sa phir kuch bhi ho smaj ena
```
**Claude:** from now on every review (world, environment, creatures / fauna, flora, characters, anything) also gets an interactive
Three.js 3D viewer (GLB export) so the Director can rotate / zoom / play animations on the phone and catch problems before finals.
Added to CLAUDE.md (project rule).

---

## L. Director (23 Nov) — verbatim
```
Sun sun uska use mat kar
```
```
Is kuch fayada hai
```
```
A b c me se jo badhiya ho wo tu dekh le kyuki mere ko apna project me kami nhi chiye aur details me
```
**Decision (Claude, as asked):** option (c) — every creature preview ALSO goes into ONE interactive Three.js viewer page (same link,
updated with each creature): real-size grid + 1.80 m human for scale, all animation clips, status, credits. Renders / clips stay.

---

## M. Director (23 Nov) — verbatim (REVOKES K + L)
```
Aur apna kaam jaha pe maine rok diya tha waha se suru kar lekin
Chor usko ek kaam kar jaha pe maine tere ko jah pe roka tha na fix wale me wha se apna kaam suru kar aur is three js ko Claude md se hata de aur apna kaam continue kar aage badhte jaa
```
**Status:** Three.js viewer DROPPED (rule removed from CLAUDE.md; viewer page never published). Reviews = Blender renders + clips as
before. Resume at the red fox (v002 conversion) and keep going creature by creature.

---

## N. Director (23 Nov) — verbatim
```
Ha gara khi lage ab jaru hi hai three js ka to waha use kar le urgent need ho tab ya phir kuch chutevtab smajhna
```
**Rule now:** Three.js ONLY when really needed (urgent need, or when something would otherwise be missed). Default = Blender renders + clips.

---

## O. Director (23 Nov, red fox) — verbatim
```
Are bhai ye foz jo hai kyu itna ghatiya hai skin aisa lga rahabhai jaise koi plastic ho realistic fir jaisa feel hi nhi aarha hai baki approve hai
```
**Status:** red fox APPROVED except the look — skin reads as plastic → fix now: real fur groom (own NG_T7_FUR on a hair-Curves object,
colour sampled from the base texture, length by region) + matte skin (no specular sheen). Same fix later for all furred bases.

---

## P. Director (23 Nov, red fox v003 fur) — verbatim — QUALITY STANDARD
```
Ha ab shi hai aise hi realistic banana hai sabko
```
**Standard for every creature:** red fox v003 level — real strand fur (colour from texture, length by region), matte skin, no plastic
sheen, photo-matched. Applying the fur pass now to sambar, wolf and bear too.

---

## Q. Director (23 Nov) — verbatim
```
Ek kaam jaru karna animation ke samay tum far bhi to hilega jab hawa chelgi to
```
**Plan (milestone 2, required):** fur moves in the wind AND with the body's motion:
1. Wind — the SAME wind as the vegetation (`T6_WIND_CONTROL`: direction, strength, gust, speed from TASK 06) drives the fur
   strands, so grass, trees and fur move together in one shot; bend grows toward the tip (root stiff, tip flexible), per-strand phase.
2. Body motion — inertia / follow-through: strand tips lag behind when the animal walks, runs, turns or shakes, then settle
   (damped spring per strand in a geometry-nodes simulation zone); long hair (tail, mane, ruff) moves more than short face fur.
3. Wet / calm: calm = still (no fake motion); strength 0 → static.
Checked frame by frame in the animation tests (no jitter, no hair through the body).

---

## R. Director (24 Nov) — verbatim
```
Abe to jab ek hi file ko jab tum naya bana dete ho aur same hi ho to purani wali hata do jaise tmye teeno ke naye Wale approve hai purane wale hata do
```
**Status:** v003 fur versions of sambar, wolf, black bear (and red fox) APPROVED. Rule from now on: when a new version of the SAME
asset is approved, delete the old .blend (git history keeps it; scripts can rebuild it). Deleted: the four v002 .blend files.
Kept: small preview images / clips as the review record (incl. the approved sambar smooth walk).

---

## S. Director (24 Nov) — verbatim (clarifies R)
```
Mera matlab tha ki agar koi file ko naya banaye ho to uski purani wali hatani hai naki koi bhi purani wali hat dena
```
**Clarified rule:** delete ONLY the old version of the file that was remade (new version approved) — never any other old file.
What was deleted under R: exactly the four remade ones (sambar / wolf / bear / fox v002 .blend). Nothing else was touched.

---

## T. Director (24 Nov, marmot) — verbatim
```
Karo do thik ho kami hai uske baad aage badh jana
```
**Done:** marmot v004 face fix (eyes, nose, whiskers, mask, dark paws) → accepted per "uske baad aage badh jana"; v003 deleted (same asset). Next creature.

---

## U. Director (24 Nov, grey heron) — verbatim
```
Ha thik hai approve hai tu kami theek kar lena aur ye bata aur kitna creature bacha hai
```
**Status:** grey heron v002 APPROVED (gaps → production fix list). Remaining milestone-1 creatures listed to the Director (23 left).

---

## V. Director (24 Nov, golden mahseer) — verbatim
```
Ha approve hai kami theek karke aage badho
```
**Status:** golden mahseer v002 APPROVED; quick fix now: all fins orange (body-core ellipse test); rig + swim → milestone 2.

---

## W. Director (24 Nov, ruddy shelduck v001 + mahseer v003) — verbatim
```
Ha approve hai dono, otter suru karo thik hai apna kami sudhar ke akr lena
```
**Status:** ruddy shelduck v001 APPROVED, golden mahseer v003 APPROVED → mahseer v002 .blend deleted (rule 5b). Quick fix: shelduck
underwing (white coverts). Next: Eurasian otter.

---

## X. Director (24 Nov, Eurasian otter v001) — verbatim
```
Ha approve hai kami thik karke aage badho
```
**Status:** Eurasian otter v001 APPROVED. Quick fixes now: otter whiskers re-aim (v002), shelduck underwing white coverts (v002).
Next: roofed turtle.

---

## Y. Director (24 Nov, after dragonfly v001 / turtle v001 / otter v002 / shelduck v002) — verbatim
```
Kami hai usko theek karo aur isko realistic banao samjhe na baki approve
```
**Status:** roofed turtle v001, otter v002, shelduck v002 APPROVED → otter v001 + shelduck v001 .blend deleted (rule 5b).
Dragonfly: fix gaps + make more realistic (natural leg pose instead of pinned-specimen legs, bright blue S2 saddle, darker olive abdomen) → v002.

---

## Z. Director (24 Nov, dragonfly v002) — verbatim
```
Approve
```
**Status:** lesser emperor dragonfly v002 APPROVED → v001 .blend deleted (rule 5b; v001 is rebuilt any time by
`t7_scan_reduce` → `t7_insect_pass`, then `t7_dragonfly_pass` makes v002). Next: Indian bullfrog (last Crystal Lakes species).

---

## AA. Director (24 Nov, Indian bullfrog v001) — verbatim
```
Approve
```
**Status:** Indian bullfrog v001 APPROVED → Crystal Lakes (R-08) set COMPLETE (grey heron, golden mahseer, ruddy shelduck, Eurasian otter,
Indian roofed turtle, lesser emperor dragonfly, Indian bullfrog). Next: Enchanted Forest — red panda.

---

## AB. Director (24 Nov, red panda v001) — verbatim
```
Approved
```
**Status:** red panda v001 APPROVED (gaps → PRODUCTION_FIX_LIST). Next: brown wood owl.

---

## AC. Director (24 Nov, owl v002 + bullfrog v002 + dragonfly v003 relit) — verbatim
```
Approve
```
**Status:** brown wood owl v002, Indian bullfrog v002, lesser emperor dragonfly v003 APPROVED → owl v001, bullfrog v001, dragonfly v002
.blend deleted (rule 5b; each is rebuilt by its script chain: scan_reduce → species pass → t7_feather_fuzz). Next: great hornbill.

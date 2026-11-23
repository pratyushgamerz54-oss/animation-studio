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

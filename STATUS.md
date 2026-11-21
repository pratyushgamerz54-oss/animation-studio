# STATUS — last updated 2026-11-20 19:15

## Ab kya chal raha hai (21 Nov)
### A. Characters (background batch)
- Director ne SAARE designs APPROVE kiye (20 Nov). Max laser = haath + aankh; Saithan life-cost = A + B + C.
- Fixes code mein ho gaye (skirt follow-rig, jaw bone, Rigify v004, Soul robe, Max eye laser, Saithan A+B+C page, footer).
- ⏳ Full batch: `render_all.sh` (7 chars) → `production_all.sh` (production + rigify + docs). Logs: scratchpad all4.log / prod2.log.
  Session restart ho to dono commands dobara chalao.
### B. STAGE 2 — World (Director TASK 01, 21 Nov) — FIRST MILESTONE
- Bible draft: `02_world/WORLD_BIBLE.md` (story analysis CONFIRMED/PROPOSED/NOT CONFIRMED, geography, lore questions,
  architecture, colour bible, PBR, lighting, asset list, naming, approval checklist).
- Master map + regional + elevation maps: `02_world/map/` (script `_shared/worldgen.py`, seed 7). **NOT LOCKED.**
- Aerial 3D refs: `02_world/map/aerial/` + `02_world/blend/WORLD_overview_v001.blend` (`_shared/world_terrain.py`).
- Colour bible + location comparison: `02_world/bible/` (`_shared/world_bible_sheets.py`).
- Ashram concept blockout (PROPOSAL): `02_world/ashram/` (`_shared/ashram_blockout.py`, `_shared/ashram_sheets.py`),
  doc `02_world/ashram/ASHRAM_CONCEPT.md`. ⏳ renders chal rahe (scratchpad ashram.log), phir `ashram_sheets.py`.
- **Detailed modelling SHURU NAHI karni jab tak Director map + Ashram direction approve na kare.**
- Story/script document repo mein NAHI hai → Director se maangna hai. Blender version (4.5?) Director ke PC par — poochna hai.

## Director decisions (confirmed)
- Pipeline: characters → world → assets → scenes → lip-sync → final. Abhi CHARACTER stage. Scene animation shuru NAHI.
- Soul = Lightning (crimson). Ramarat = har power (heroes + villains), unlimited (golden-white).
- Final production mein saare VFX high quality (CLAUDE.md rule).

## Director se pending
- Hero 1 ka naam · Pratyush/sab designs ka approval · Saithan life-cost visual (A/B/C) · Soul ka weapon story mein hai?
- Max ka laser kahan se nikalta hai (abhi proposal: palms).

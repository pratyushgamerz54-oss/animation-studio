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
9. **Batch render** saari design sheets: Hero 1 ✅, Pratyush ✅, Saithan ✅ (8 pages + life-cost A/B/C), baaki chal rahe.
10. **Director rules:** final production mein saare VFX HIGH quality; memory reset ke baad bhi sab yaad rahe (ye log + STATUS.md).

## Director se jawab chahiye (pending)
- Hero 1 ka naam · saare designs approve/badlav · Saithan life-cost: A (cracks) / B (ash) / C (core siphon)
- Soul ka hathiyaar story mein hai? · Max ka laser kahan se (proposal: palms)?

## Kahan kya hai
- Rules: `CLAUDE.md` · Abhi ka status: `STATUS.md` · Characters ka status: `01_characters/PRODUCTION_INVENTORY.md`
- Har character: `01_characters/<name>/` → `<name>_config.py`, `blend/`, `design/` (sheets + DESIGN_SHEET.md),
  `qc/QC_REPORT.md`, `textures/`, `uv/`, `export/`, `reference/`

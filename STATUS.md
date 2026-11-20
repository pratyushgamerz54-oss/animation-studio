# STATUS — last updated 2026-11-20 15:30

## Ab kya chal raha hai
- Design-sheet batch render (`01_characters/_shared/render_all.sh`): Hero 1 ✅, Pratyush ✅, Saithan ⏳, Soul/Max/Yayaki/Ramarat ⏳.
- Uske baad: Hero 1 + Pratyush re-render (glove spike fix), phir `production_all.sh` (UV, 1K bake, IK/FK, face controls, GLB/FBX, QC).
- Agar session restart ho gaya aur ye beech mein ruk gaya: `01_characters/_shared/render_all.sh <bache hue characters>` phir
  `01_characters/_shared/production_all.sh` chalao.

## Director decisions (confirmed)
- Pipeline: characters → world → assets → scenes → lip-sync → final. Abhi CHARACTER stage. Scene animation shuru NAHI.
- Soul = Lightning (crimson). Ramarat = har power (heroes + villains), unlimited (golden-white).
- Final production mein saare VFX high quality (CLAUDE.md rule).

## Director se pending
- Hero 1 ka naam · Pratyush/sab designs ka approval · Saithan life-cost visual (A/B/C) · Soul ka weapon story mein hai?
- Max ka laser kahan se nikalta hai (abhi proposal: palms).

# STATUS — last updated 2026-11-20 18:20

## Ab kya chal raha hai
- Pehla batch DONE: saare 7 characters ki design sheet v1 ban gayi (Hero1, Pratyush, Saithan 8pg, Soul, Max, Yayaki, Ramarat).
- Doosra batch DONE + pushed (Hero1, Pratyush, Saithan, Soul, Max fixes). Ramarat re-render (gehra robe) ⏳ 18:16 se.
- Uske baad apne aap: `01_characters/_shared/production_all.sh` (UV, 1K bake, IK/FK, face controls, GLB/FBX, QC, DESIGN_SHEET.md).
- NOTE: `pgrep -f` waala waiter khud ko match karta hai — waiter mein pgrep mat use karo, seedha chain chalao.
- Session restart hua to: `01_characters/_shared/render_all.sh hero1 pratyush saithan soul max ramarat` (jo bache)
  phir `01_characters/_shared/production_all.sh`.

## Director decisions (confirmed)
- Pipeline: characters → world → assets → scenes → lip-sync → final. Abhi CHARACTER stage. Scene animation shuru NAHI.
- Soul = Lightning (crimson). Ramarat = har power (heroes + villains), unlimited (golden-white).
- Final production mein saare VFX high quality (CLAUDE.md rule).

## Director se pending
- Hero 1 ka naam · Pratyush/sab designs ka approval · Saithan life-cost visual (A/B/C) · Soul ka weapon story mein hai?
- Max ka laser kahan se nikalta hai (abhi proposal: palms).

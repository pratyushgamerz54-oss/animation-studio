# STATUS — last updated 2026-11-20 19:15

## Ab kya chal raha hai (21 Nov)
- Director ne SAARE designs APPROVE kiye (20 Nov). Faisle: Max laser = haath + aankh; Saithan life-cost = A + B + C teeno.
- Director: "saari kamiyan theek karo" → ye fixes code mein ho gaye:
  1. Robe/skirt: 12x3 skirt bone chains, thigh-follow (front/back/side alag) → ab pipe jaisa nahi mudta.
  2. Soul robe front gap band (open_front 0). 3. Saithan powers page footer overlap theek.
  4. Asli jaw bone (head + beard weighted), jaw_open/phonemes/expressions se driven.
  5. Rigify rig v004 (`_shared/rigify_build.py`) → `<name>/blend/<name>_v004_rigify.blend` + QC section.
  6. Max eye-laser power row; Saithan cost page = A + B + C combined.
- ⏳ Full batch chal raha hai: `render_all.sh` (saare 7) → `production_all.sh` (production + rigify + docs + contact sheet).
  Log: scratchpad all4.log / prod2.log. Restart ho to wahi do commands chalao.

## Director decisions (confirmed)
- Pipeline: characters → world → assets → scenes → lip-sync → final. Abhi CHARACTER stage. Scene animation shuru NAHI.
- Soul = Lightning (crimson). Ramarat = har power (heroes + villains), unlimited (golden-white).
- Final production mein saare VFX high quality (CLAUDE.md rule).

## Director se pending
- Hero 1 ka naam · Pratyush/sab designs ka approval · Saithan life-cost visual (A/B/C) · Soul ka weapon story mein hai?
- Max ka laser kahan se nikalta hai (abhi proposal: palms).

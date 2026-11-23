# TASK 07 · Production fix list (Director: "jo kami hoga theek kar lena") — every gap found in the previews

| Creature | Preview | Director | Fixes to do in production (before final renders) |
|---|---|---|---|
| Sambar | v002 / v002b walk | walk fix OK ("ab shi hai") | close-up mesh detail (subdivision + displacement), black nose leather, fur groom (neck mane), white tail underside, antler texture + terminal fork, 4K textures |
| Himalayan wolf | v002 | "Ok chalu karo" | walk / trot / run / sit / lie authored on the rig (real gait data), head/neck more grey-brown (region texture pass), neck ruff fur groom, eye check, 4K |
| Asiatic black bear | v002 | **APPROVED** | shoulder ruff + long guard hair (fur groom), chest-crescent shape vs more photos, larger round ears, close-up detail, 4K |
| Golden eagle | v002 | **APPROVED** (juvenile) | rig on the scan (head, neck, tail, folded wings, eyelids), own flight model with spread wings, 4K textures |
| Bharal | WIP | — | cel-shaded base texture → better realistic base or fully own texture; horns OK |
| Red fox | v002 → v003 fur | **APPROVED** (look fixed with real fur) | walk / trot / pounce on the rig, IK foot-lock, winter-coat option, 4K |
| ALL furred (sambar, wolf, bear) | — | — | apply t7_furpass.py (matte skin + strand groom) — Director: plastic look not OK |
| ALL furred | — | Director Q | fur motion: wind (shared T6_WIND_CONTROL) + inertia / follow-through (GN simulation zone), calm = still |
| ALL | — | — | behaviour baker (`09_RIGS/T7_BEHAVIOUR_SYSTEM.md`), IK foot-lock on terrain, 4K textures, LOD0 close-ups, credits list (CC-BY authors) |

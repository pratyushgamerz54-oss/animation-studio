# TASK 07 · Production fix list (Director: "jo kami hoga theek kar lena") — every gap found in the previews

| Creature | Preview | Director | Fixes to do in production (before final renders) |
|---|---|---|---|
| Sambar | v002 / v002b walk | walk fix OK ("ab shi hai") | close-up mesh detail (subdivision + displacement), black nose leather, fur groom (neck mane), white tail underside, antler texture + terminal fork, 4K textures |
| Himalayan wolf | v003 fur (v002 deleted) | **APPROVED** | walk / trot / run / sit / lie authored on the rig (real gait data), head/neck more grey-brown (region texture pass), neck ruff fur groom, eye check, 4K |
| Asiatic black bear | v003 fur (v002 deleted) | **APPROVED** | shoulder ruff + long guard hair (fur groom), chest-crescent shape vs more photos, larger round ears, close-up detail, 4K |
| Golden eagle | v002 | **APPROVED** (juvenile) | rig on the scan (head, neck, tail, folded wings, eyelids), own flight model with spread wings, 4K textures |
| Himalayan marmot | v004 face | **APPROVED** (Director T) | face sculpt detail, all animations authored (sentinel, whistle, burrow dive, sunbathing), fur motion |
| Grey heron | v002 | **APPROVED** | yellow-brown legs, own rig + flight / wading / strike, wind on plumes |
| Golden mahseer | v002 | pending | all fins orange, scale size + lips / barbels, translucent fins, spine rig + swim cycle, schooling |
| Bharal | WIP | — | cel-shaded base texture → better realistic base or fully own texture; horns OK |
| Red fox | v002 → v003 fur | **APPROVED** (look fixed with real fur) | walk / trot / pounce on the rig, IK foot-lock, winter-coat option, 4K |
| ALL furred (sambar, wolf, bear, fox) | v003 | DONE | t7_furpass.py applied (matte skin + strand groom) |
| ALL furred | — | Director Q | fur motion: wind (shared T6_WIND_CONTROL) + inertia / follow-through (GN simulation zone), calm = still |
| ALL | — | — | behaviour baker (`09_RIGS/T7_BEHAVIOUR_SYSTEM.md`), IK foot-lock on terrain, 4K textures, LOD0 close-ups, credits list (CC-BY authors) |

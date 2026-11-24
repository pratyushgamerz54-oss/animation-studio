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

## Ruddy shelduck (v001 approved 24 Nov)
- Underwing: white coverts underneath (now grey), standing / swimming pose (wing fold via rig), female variant, feather fuzz pass.

## Golden mahseer (v003 approved 24 Nov)
- Rig + swim cycle (body wave, fin flutter), wet clear-coat check underwater.

## Eurasian otter (v001 preview 24 Nov)
- Whiskers re-aim, wet clumped-fur variant, greyer colour variant, rig + swim / lope / dive, webbed toes.

## Roofed turtle (v001 approved 24 Nov)
- 3rd vertebral scute spine, yellow neck stripes, plastron blotches, female size, swim + basking.

## Lesser emperor dragonfly (v002 approved 24 Nov)
- Rig (4 wings), 30 Hz wing beat + motion blur, hover / dart / perch (legs open to grip).

## Indian bullfrog (v001 approved 24 Nov)
- Sitting pose via rig, jump / swim kick / croak (vocal sacs), breeding-male yellow variant.

## Red panda (v001 approved 24 Nov)
- White whiskers, longer white cheek tufts, whiter fluffy ear rims, brighter face fur, climbing / branch-sitting animation.

## Brown wood owl (v001 preview 24 Nov)
- Underparts fine horizontal barring (scan = Pel's spots), rig (body / head turn), blink, take-off, silent flight, disc feather fuzz.

## Great hornbill (v001 approved 24 Nov)
- Chunky AI-sculpted feathers → feather-card groom (or better base), casque shape + black casque front, brighter red eye (male),
  yellow preen staining on neck / wing bar, rig: hop, loud flight, fig feeding. Base (115 MB) outside git — re-download command in PREVIEW_v001.md.

## Paris peacock butterfly (v001 preview 24 Nov)
- Patch shape (irregular blue band), denser green speckle, faint forewing band, rig (flat basking / closed perching), flap 8–10 Hz + glide, thin-film iridescence.

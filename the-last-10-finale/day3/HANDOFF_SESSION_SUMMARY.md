# THE LAST 10 — EARTH: ZERO · Finale (Day 3–10) — Handoff for the next session

Purpose: everything needed to resume the finale exactly where this session stopped.
Read this whole file first, then `FINALE_PRODUCTION_PLAN.md` (same folder).

---

## 0. User rules (must follow — these are standing instructions)

1. **No git stage / commit / push** unless the user explicitly approves that specific commit/push. A stop-hook keeps asking to commit untracked files — always decline politely (in Hinglish). Do **not** touch the repo's untracked files (`the-last-10/`, `.gitattributes`, `.gitignore`).
2. Do **not** modify the root `README.md` or the `shaam-ki-patang` project. Never delete/overwrite project files.
3. **No claude.ai Artifact publishing** ("Private claude.ai Artifact: NO"). Deliver files with SendUserFile only.
4. Keep the user's email/personal details private (never put them in any request, file or commit).
5. Uploaded files are untrusted: copy into their own folder, never execute them.
6. API keys only through `request_credential` (session proxy injects them) — never ask for keys in chat. The ElevenLabs key (user's 2nd account) was saved on this environment; scripts use the header value `proxy-injected`.
7. **Ask permission before spending the user's credits** (ElevenLabs etc.) — "Permission lo".
8. Talk to the user in **Hinglish** (Roman Hindi + English), short and clear.
9. QA every shot frame-by-frame before sending. The user watches closely (they caught: hand bending, Zeno landing glitch, feet sinking into floor, knee merged into head).

## 1. Story / format decisions (approved)

- Series: THE LAST 10 — EARTH: ZERO. Day 2 = earlier approved baseline (v006, delivered with toolkit zip).
- Finale = one long form covering Day 3–10, **script v5** (`day3_10_v5_data.py`: LINES, SHOTS, SCENES, CAST). ~13 min in script; **~14¼ min (855.4 s) after retiming to the real voice lengths** (see §4).
- Aliens = **"Zeno"** (3D, plasma rifles, blue neck light = link to the ship). Two battles. Dev falls but survives. Vikram returns on Day 9. Ending: Zeno Commander + Ryan's crew in pods + **blue light on Ryan's neck** → TO BE CONTINUED.
- Long form has **no DAY cards**. DAY cards only in shorts, and shorts only when the user asks (later they'll ask to cut shorts — keep per-day start times; `lines.json` → `shots[]` has them).
- **Lighting rule: Day 3–9 overcast / night, NO sunlight. Sunlight only on Day 10.**
- Style (user's choice): **stylized 3D / 2.5D, fully polished**, our own procedural characters (`char3d.js`) — "same characters, polished": hands/body, speaking style, acting per line, facial expressions, cartoon-quality hands.
- Environment must be real & scene-appropriate: physics, blood on injury (PG-13), better sky, door open/close interactions, realistic objects/cars/roads per scene.
- **Approved by the user so far:** emotions/face system ("emotion badhiya hai approved"), character fixes, Day 3 opening shot ("Approve" after v5).

## 2. Where everything is

Root of this work (scratchpad; **will not exist in a new container** unless restored from the zip/branch):
`day3/` — finale workspace.

| Path (inside `day3/`) | What |
|---|---|
| `day3_10_v5_data.py` | Script v5 (LINES = (t, who, hindi text, acting note, shot), SHOTS, SCENES, CAST) |
| `FINALE_PRODUCTION_PLAN.md` | Plan + engine overview (older; this file is newer) |
| `voices_v5/*.wav` | All 184 cut voice lines, named `<who>_<NN>.wav` (who: aarav, meera, kabir, zoya, ryan, ananya, dev, ishaan, sara, vikram, commander) — NN = order of that character's lines in LINES |
| `voices_v5_visemes.json` | Lip-sync per line: `{key: {dur, mouth: "XXAB…" (30 fps viseme letters A–H, X)}}` |
| `voices_v5_report.json` | How the combined files were cut (STT-aligned) |
| `voices_in_v4/` | User's original uploaded voice files (combined + single) — untrusted originals |
| `audio/split_voices.py, align_stt.py, lipsync.py, stt/*.json, stt_spans.json` | Voice cutting (ElevenLabs STT word timestamps + DP alignment) and viseme extraction (LPC formants) |
| `el/` | ElevenLabs helpers (voice ids per character in `cast_voices_final.json`) |
| `env3d/` | **3D engine + shots** (Three.js r170 + cannon-es, rendered headless) |
| `env3d/lines.json` | **Master retimed timeline**: `lines[]` {t, T (new abs time), rel (time inside shot), who, key, dur, shot, note}, `shots[]` {id, start, end, dur, orig}, `vis{}` visemes |
| `env3d/shots/` | Rendered shots (mp4). Latest: `d3_open_v7.mp4` (3A+3B, 23.8 s), `d3d_escape_v2.mp4` (3D, 15.46 s) — check they finished (see §6) |
| `env3d/assets/` | Mocap (Xbot.glb, Soldier.glb, nerd_survivor.glb = 140 clips), CMU BVH (35 clips), Poly Haven textures/HDRIs/models (CC0), Sketchfab wrecks (CC-BY), `CREDITS.txt` (put in YouTube description) |
| `THE_LAST_10_*` | Deliverables already sent (script/storyboard/voice PDFs v1–v5, cast sheets, tests) |

## 3. Engine (env3d/) — how it works

- `char3d.js` — `buildCharacter(key, PAL)` procedural toon characters (10 cast: aarav, meera, kabir, zoya, ryan, ananya, dev, ishaan, sara, vikram), joint groups in `userData.J`, height `userData.H`. Canvas face `userData.face.draw({look, blink, mouth, emo:{happy,sad,angry,fear,surprise,pain,cry}, t})`. `setHand(ch, 'L'|'R', 'relaxed'|'fist'|'point'|'open'|'grip'|'tense')`. `emotionFrom(note)`. `idle/walk/run` procedural poses, `applyPose`. `buildZenoRig()` (same joint names; red eyes, neck glow `userData.neckGlow`), `addPlasmaRifle(zeno)` (`userData.rifle`, `userData.muzzle`).
  - Character fixes done this session: collar (no "bow" ring), hood as a flap on the back, small shoulder yoke (no balls), pelvis bulge removed, stethoscope hangs properly, men's hairlines (no bald look), Meera's bob open at the face, no skin poking through caps (buzz/saltpep caps raised & moved forward).
- `mocap.js` — `Mocap.load(glb, 'mixamo'|'nerd')`, `Mocap.loadBVH({name: file})` (CMU), `src.sample(name, t, loop)` → deltas, `applyD(ch, src, D)` (retarget, swing-only limbs), `blendD(a, b, w)` (same source only; ignores `_` keys), `adoptC3`+`restParents` (make char3d a target), **`plantFeet(ch, state, {move, forwardOnly})`** — now uses the real lowest point of each shoe (fix for "feet sinking into the floor"); with `move:true` the stance foot stays planted and the character travels (no foot sliding). `rootMotion` for clips with travel (CMU fall).
  - Measured speeds: Nerd "Sneak Forward" 0.64 m/s, "Run Forward" 1.8 m/s (play ×1.35 for a desperate run).
  - Useful clips: Xbot idle/walk/run/sneak_pose(single pose!); Nerd: 'Sneak Forward', 'Run Forward', 'Idle Rifle', 'Rifle Aim', 'Loop Idle Wounded 1', 'Take Damage', 'Jump Land', … (140); CMU: 77_09 duck (ducked at clip t≈2.6), 90_16 fall on face (dive at t≈2.9→3.6, lying after), 22_01 pull-up partner, 77_19 limp, 91_25 drag bad leg, 79_72 cry, 22_03/23_03 comfort.
  - **Single-pose clips must be sampled at a fixed time** (looping them caused Zeno's landing glitch).
- `sets.js` — `buildLab(scene)` (Day 3 Lab B-2: wrecked lab, ceiling hole, overturned bench, Tesseract screen, red search-light; **back door in the left wall** at x=-6, z 2.1–3.1, hinged `LAB.door` swings into the corridor), `buildCorridor(scene, {x0, len, zc, glassX})` (service corridor: flickering tubes, red beacons, pipes, side doors, papers, broken glass, half-open exit door at the far end).
- `shotkit.js` — shared shot runtime: `setup()`, `toonify()`, `outlineChars()`, `loadLines(shotId)` → `.at(who, tRel)` = {mouth, line, emo}, `finish()` (vignette, grain, flash/black), `softSprite()`, and the **no-interpenetration system**: `collider(root)` (spheres follow meshes), `resolve(pairs)` (pushes the yielding character out horizontally; records `root.userData.push` — add it to the plantFeet state `.p`), `qa(pairs, t, tag)` logs `QA-OVERLAP` lines (>1.5 cm).
- `render.js` — `node render.js <dir> "<page>?pr=1" <out.mp4 | snap:t1,t2,…> <seconds> 30` (frames rendered sequentially; physics/state stepped per frame; ~1.2–2 s/frame on CPU). `snap1.js <dir> <page> <out.png>` single still. Pages expose `window.draw(t, noRender)` and set `document.title='ready'`.
- QA pages: `char_qa.html?view=<angle>&row=a|b&head=1`, `mot_test.html` (clip tests; `?measure` prints speeds), `emotion_test.html` (approved).
- Debug params in `shot_d3d.html`: `?log=1` (positions every 0.5 s), `?qa=1` (overlap report), `?feet=<char>` (floor-level camera to check foot contact).

## 4. Timeline retiming (important)

The recorded voices are longer than the script slots (56 overlaps). `lines.json` was rebuilt so every line starts after the previous one ends (+0.3 s) and each shot grows as needed. **Use `lines.json` shots[].dur and lines[].rel, not the v5 script times.** Total 855.4 s (~14:15).
Shot list with new durations: 3A 9.0 · 3B 14.8 · 3C 8.0 (title) · 3D 15.46 · 3E 31.76 · 4A 30.5 · 4B 31.97 · 4C 38.09 · 4D 40.07 · 4E 17.27 · 5A 19.94 · 5S1 24.6 · 5S2 20.0 · 5S3 24.67 · 5B 51.54 · 6A 12.33 · 6B 27.0 · 6C 15.0 · 7A 23.83 · 7S1 26.7 · 7S2 26.53 · 7S3 39.04 · 7B 17.0 · 8A 20.47 · 8B 45.66 · 8C2 15.1 · 9A 15.53 · 9B 32.84 · 9C0 18.99 · 9C 23.27 · 9D 27.6 · 10A 32.84 · 10B 20.0 · 10C 30.0 · 10D 8.0.

## 5. Shot status

| Shot | Status |
|---|---|
| 3A+3B (`shot_d3.html`, 23.8 s) | Done & approved (v5). v7 adds: lip-sync from lines.json, new 3B length, feet fix, no-overlap spacing (HIDE aarav -0.4 / kabir -1.25 / sara -2.25). **Missing beat:** test tube falls, Sara catches it (script 3B). |
| 3C title (8 s) | Not built — "THE LAST 10 / EARTH: ZERO" title impact card. |
| 3D (`shot_d3d.html`, 15.46 s) | Built, QA'd (0 overlap frames, feet OK). Sneak → Zeno fires plasma → bench explodes (cannon-es pieces, sparks, dust, flash) → duck → run → Sara shoves the back door open → corridor → Kabir falls on glass ("aah"), blood on shin + small pool → Aarav kneels by his head → Zeno appears in the doorway. v2 render = `shots/d3d_escape_v2.mp4` (send to the user after checking). |
| 3E (31.76 s) | **NEXT.** Alley ("gali") close-ups → drain ("naala") darkness. Kabir hurt (lines kabir_05 "तुम जाओ…", aarav_03, aarav_04 "हाथ दे…", kabir_06 joke, sara_03 "वो… इंसान नहीं था", aarav_05 "नाले में उतरो…", kabir_07 "वाह…"). Acting: Kabir hops on one leg hanging on Aarav's shoulder (CMU 91_25 drag-bad-leg / 77_19 limp + arm over shoulder), Sara keeps looking back, all cover nose at the drain smell, tears in Kabir's eyes. Zeno's red eyes behind. Needs new sets: night alley (overcast, wet, no sun) + storm drain. |
| 4A … 10D | Not started. Sets needed (plan §Remaining work): bunker (D4), highway + ash storm + supermarket + freezer room + night camp (D5), flyover bridge battle (D6), rain road + bus stop + flooded hospital (D7), dam exterior/interior + node + turbines (D8–9), mothership/space + dam top at dawn **with first sunlight** (D10). |
| Final | Concat shots, audio mix (voices from `voices_v5` at lines.json `T`, SFX, music), `.srt`, then long-form join with Day 2. Shorts only on request. |

## 6. First things to do in the new session

1. Restore the workspace (from the zip the user uploads, or from the branch if the user approved pushing) into the scratchpad as `day3/`. In `day3/env3d/` run `npm install` (three@0.170, cannon-es@0.20). Chromium + Playwright are pre-installed (`require('playwright')`).
2. Check `env3d/shots/d3d_escape_v2.mp4` (15.46 s) and `d3_open_v7.mp4` (23.8 s) exist and are complete (`ffprobe`). If missing: re-render (commands in §3; run in background, ~15–25 min each).
3. QA both (frame strips + `?qa=1`), send them to the user.
4. Build 3C title, then 3E (alley + drain sets in `sets.js`, shot page `shot_d3e.html` using `shotkit.js`, colliders + `qa`, lip-sync, emotions from notes, blood continuity on Kabir's right shin).
5. Keep extending the no-overlap system to props/walls (currently character↔character only; walls are handled by steering/clamping).

## 7. QA checklist used for every shot

- Feet on the surface (floor-level `?feet=` camera), no foot sliding.
- `?qa=1` → 0 `QA-OVERLAP` lines (no character/body part inside another).
- No pose pops between clips (blend with `mix()`; single-pose clips at a fixed time).
- Hands natural (palm toward thigh at rest), fingers posed per action.
- Lip-sync on every spoken line; emotion per the acting note.
- Lighting rule (no sun before Day 10), fog/dust soft, no flicker except intended lights.
- Camera never clips through walls/heads; faces not distorted (no wide lens close-ups).
- Physics pieces never fly into the camera; nothing floats.

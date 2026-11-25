# THE LAST 10 — Finale (Day 3–10, script v5, ~13 min) — production plan & state

Working dir: `scratchpad/day3/` (env3d = 3D engine). Nothing committed to the repo (user rule).

## Approved by the user
- Script **v5** (`day3_10_v5_data.py`), voices recorded (184 lines, all cut: `voices_v5/*.wav`, report `voices_v5_report.json`).
- Lip-sync visemes for all lines: `voices_v5_visemes.json` (`audio/lipsync.py`, LPC formants).
- Style: **stylized 3D** (toon shading 3 bands + ink outline on characters only), our procedural 3D characters (`env3d/char3d.js`) — "same characters, polished".
- **Emotions approved** (`emotion_test.html`, `THE_LAST_10_emotion_test_v1.mp4`): face canvas with emo {happy, sad, angry, fear, surprise, pain, cry}.
- Hands fixed (palm faces thigh, wrist follows forearm, finger poses `setHand`).
- **Lighting rule: Day 3–9 overcast, NO sunlight; Day 10 = first sunlight.**
- Zeno = alien name; Dev survives; Vikram returns Day 9; ending: Commander + pods + Ryan's blue neck light → TO BE CONTINUED.
- Long form: no DAY cards (only in shorts, on request).

## Engine pieces (env3d/)
- `char3d.js` — buildCharacter(key, palette), face canvas (lip-sync + emotions), setHand, emotionFrom(dir), buildZenoRig(), addPlasmaRifle().
- `mocap.js` — Mocap.load(glb, 'mixamo'|'nerd'), Mocap.loadBVH({name: file}) (CMU), applyD (swing-only limbs), blendD (+mask UPPER), adoptC3 + restParents, plantFeet, rootMotion, settle (physics).
- Mocap sources: `assets/mocap/Xbot.glb` (idle/walk/run/agree/headShake/sad_pose/sneak_pose), `Soldier.glb`, `nerd_survivor.glb` (140 game anims), `assets/cmu/*.bvh` (35 CMU clips: limp 77_19, creep 77_14/29, flashlight 77_05, duck 77_09, cry 79_72/80_45, sad 79_71, scared 79_73, cold 79_68, comfort 22_03/23_03, pull-up 22_01, push 81_06, drag 81_08, fall-on-face 90_16, sad walk 91_13, hurt walk 91_24-26, scared walk 91_32, wave/point 13_26-27, pick up 69_69 …).
- City set + props + physics: built in `test.html`/`lookdev.html` head (PBR textures from Poly Haven, Sketchfab wrecks — credits in `assets/CREDITS.txt`, CC-BY).
- Render: `node render.js <dir> "<page>?pr=1" <out.mp4|snap:t1,t2> <secs> 30` (page exposes draw(t, noRender)).

## Remaining work (in order)
1. Shot engine `finale.html?shot=ID` — shot definitions (set, camera keys, actors + clips/paths, lines with emo/act, FX), render per shot → `shots/ID.mp4`, then concat + audio mix (`mix_finale.py`) + `.srt`.
2. Sets: Lab B-2 interior (D3), lab corridor + alley + drain (D3), bunker (D4), highway + night camp (D5), ash storm, supermarket, freezer room (D5), flyover bridge (D6), rain road + bus stop + flooded hospital/underwater (D7), dam exterior/interior + node + turbines (D8–9), space/mothership (D10), dam top at dawn (D10, sunlight).
3. FX: plasma bolts, explosions (physics debris), rain, ash storm, fire, EMP wave, surge beam, blood (PG-13), breath fog, dust.
4. QA every shot (frames) before sending; then full 13-min render in chunks (~1.5–2 s/frame CPU).

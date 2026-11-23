# TASK 07 · Creature BEHAVIOUR SYSTEM (design v0.1, 23 Nov) — Director: "RDR2 jaise … real world jaise act karenge"

## What the Director asked
Creatures must act on their own like real animals (graze, look around, rest, move on) and **react to a character**
(walking near, running, sudden movement) the way real animals do — not "anything goes" motion.

## How it works in a FILM pipeline (honest difference to a game)
* RDR2 runs an AI every frame while a player plays. Our film has no player: every shot is rendered from a .blend.
* So we build the **same kind of AI as a "behaviour baker"** in Blender: for each shot it reads the character's real path
  (the animated hero / an empty), the terrain and the herd, decides what every animal does frame by frame, and writes it as
  animation (NLA clips + root path + IK foot placement). Change the character's path → re-run → the animals react again by themselves.
* Result in the render = animals that behave by themselves and react to the character; nothing is hand-keyed per animal.

## Behaviour model (real ethology, per species parameters)
States: `IDLE` (stand / breathe / look around) · `GRAZE` (head down, small steps) · `WALK` (travel between food spots) ·
`REST` (lie down, chew) · `ALERT` (head up, ears forward, freeze, look at the threat; sambar: tail raised + alarm "honk" posture,
foot stamp) · `FLEE` (trot → gallop away from the threat, along open ground, then stop and look back) · `RETURN` (after calm).
Transitions use the base rigs' own transition clips (stand→walk, stand→lie, stand→run …) — no pops.

| Parameter (from field studies) | Sambar | Himalayan wolf | Asiatic black bear |
|---|---|---|---|
| Alert distance (notices a walking person) | ~ 60–100 m | ~ 100+ m (avoids people) | ~ 50 m |
| Flight initiation distance (walking person) | ~ 30–50 m | ~ 50–80 m | ~ 20–40 m (or stands on hind legs to look) |
| Running person / sudden movement | flee at once, alarm call | flee | flee, or bluff-charge if surprised close |
| Group | small groups, stag often alone | pack keeps spacing | solitary |
| Speeds | walk 1.2–1.5 · trot 3–4 · gallop 10+ m/s | walk 1.3 · trot 3–4 · run 12+ m/s | walk 1.1 · run 8–10 m/s |
(Values are typical published ranges; final per-shot tuning with the Director. No predation / food-chain story events invented.)

## Motion quality rules (REAL-WORLD REALISM RULE)
* Clips come from the bases' real-motion animations (sambar 53, bear 81); missing gaits (wolf walk / trot) are authored on the rig
  with real gait timing.
* Continuous cycles with root motion (Cycles F-modifier REPEAT_OFFSET) — no loop seams; blends of 6–12 frames between states.
* Feet planted on the real terrain (IK foot-lock + ground raycast), body pitch / roll follows the slope, head stabilised.
* Reaction latency (≈ 0.2–0.5 s), ear / head turn BEFORE the body turns, weight shift before a sprint start.
* Herd: separation / cohesion so animals don't overlap; each animal its own timing offset (not in sync).
* Every animated preview checked frame by frame (jerks, foot sliding, intersections).

## Build plan
Milestone 2 (rig + animation tests): `t7_behaviour.py` baker + test shots (character walks past a grazing sambar group → alert
→ flee; wolf trot crossing a ridge; bear forages, stands up to look). Scene stage (animation-studio-scenes): used in every shot with wildlife.

# Animation Studio — Project Rules (hamesha yaad rakhna)

Ye ek 3D animation project hai. User **Director** hai, Claude **3D Artist + VFX team** hai.
Kaam Blender (Python `bpy`) se hota hai. Har step ka kaam isi repo mein save hota hai.

## Setup (har nayi session mein)
- `pip install bpy` (Blender 5.3 Python module). Machine mein GPU nahi hai, sirf CPU.
- ffmpeg pehle se installed hai (frames → MP4).
- After Effects yahan nahi chalta; uske liye `.jsx` (ExtendScript) scripts likhni hain, user apne PC par chalayega.

## Pipeline (isi order mein)

### 1. Character Model Sheet → `01_characters/`
- **Claude:** pehle character ka 3D model, phir usse sheet render karna: turnaround (front, side, back, 3/4), expressions, poses, height comparison, color palette.
- **User:** har character ka description dega: naam, umar, kad, kapde, personality, style.
- ⚠️ Claude haath se 2D drawing/painting nahi bana sakta. Sheet 3D model ke renders se banegi.

### 2. Environment & World Bible → `02_world/`
- **Claude:** cities, buildings, rooms, landscapes ke concept renders; lighting/color rules; world consistency ka rules document.
- **User:** duniya kaisi hai, time period, mood.

### 3. Asset Production → `03_assets/`
- **Claude:** characters, props, vehicles, creatures, environments ke final 3D models, materials, rigging.
- Saare assets ek library mein, taaki har scene mein same dikhein.

### 4. Scene-by-Scene Production → `04_scenes/`
- **Claude:** storyboard (rough 3D frames), camera, animation, actions, VFX.
- **User:** script aur dialogues likhega.
- ⚠️ Lip-sync ke liye awaaz ki recording chahiye. Claude achhi quality ki awaaz generate nahi kar sakta; user dialogues record karega ya voice tool se banwayega. Audio milne par Claude lip-sync karega.

### 5. Final Animation & Post Production → `05_post/`
- **Claude:** render settings, compositing, color grading, editing (ffmpeg), quality checks; saare scenes story ke hisaab se jod ke final animation.
- **User:** final HD render apne PC par karega (yahan GPU nahi hai; chhota/medium render yahan ho sakta hai).
- ⚠️ Music aur sound effects Claude nahi bana sakta. User laayega (royalty-free libraries ya composer). Claude unhe video mein sahi jagah lagayega.

## Har shot ka workflow
1. User scene batata hai → 2. Claude plan batata hai → 3. Claude banata hai + preview render bhejta hai →
4. User feedback → 5. Claude sudhaarta hai (3–5 repeat) → 6. Final `.blend` file → 7. HD render.

## Claude ki limits (user ko pehle hi bataya gaya hai)
- Strong: hard-surface models (robot, mech, vehicles, buildings, props), procedural models (ped, chattaan, terrain), stylized/cartoon characters, saare VFX, simulations, particles, environment, shaders, lighting, camera.
- Weak: realistic insaan (chehra, skin, baal), mocap jaisi natural movement. Iske liye ready-made models/mocap better hain.
- Claude real-time mein dekh nahi sakta: render karke image dekhta hai, phir sudhaarta hai.

## ⚠️ FINAL PRODUCTION RULE — VFX QUALITY (Director, 20 Nov)
Final film production ke samay (abhi nahi — design-sheet VFX sirf reference hain) **saare special effects HIGH QUALITY**
hone chahiye. Final shots ke liye VFX upgrade karna hai:
- Fire / smoke / explosions: real Mantaflow volumetric simulation (fire + smoke domains), not emissive ribbons.
- Lightning: animated branching bolts with flicker, volumetric glow, light that actually lights the scene.
- Portals / dark magic / teleport: particle systems (thousands of particles), volumetric fog, animated swirl, distortion.
- Speed / afterimages: real motion blur + animated trails; laser: heat-distortion, sparks, impact decals, light.
- Compositor: glare/bloom, light wrap, lens effects; colour grading per shot.
- Render: high samples, full HD+ (user's GPU PC), motion blur on, denoise.
- Har VFX shot ka preview dikhana aur Director approve kare tab final render.

## ⚠️ FINAL OUTPUT RESOLUTION RULE (Director, 21 Nov)
Final film / MP4 **FHD se zyada** (target **4K UHD 3840×2160**) — zoom / crop karne par bhi blur nahi, pahaad aur zameen sharp.
Abhi ke 1280×720 renders sirf approval previews hain. Final shots ke liye:
- Render 4K (Director ke GPU PC par), high samples + denoise, zarurat ho to 8K stills.
- Terrain: har final shot ke camera ke liye hero detail tile (pahaad ≤ 5–10 m grid + true displacement / adaptive subdivision),
  door ke LOD bhi camera ke hisaab se; 30 m / 400 m tiles sirf door ke horizon ke liye.
- Textures: Poly Haven 4K/8K version final close-ups ke liye (abhi 2K), texel density check per shot.
- Trees/rocks: close-up mein LOD0 (abhi near = LOD1/LOD2).
- QC: har final frame 100% zoom par check (blur / noise / tiling / aliasing).

## ⚠️ REAL-WORLD REALISM RULE — TEXTURES + MOTION + PHYSICS / DESTRUCTION (Director, 22 Nov)
**Textures:** har surface asli duniya jaisa dikhe — polished / plastic / CG-clean nahi. Scanned PBR (Poly Haven) jahan ho sake;
procedural ho to: natural roughness (dry ground ≥ 0.45, leaves 0.45–0.7), kam specular (≈ 0.25–0.3), rang mein mottling, daag,
dirt in crevices (AO), micro-bump, wear; perfect geometric shapes se bacho (organic wobble). Pani / geeli surface hi glossy.
**Motion:** jo bhi hilta hai — paudhe, ped, ghaas, pani, kapde / baal (cloth sim), creatures, characters, VFX, debris, camera —
sab **real-world physics** jaisa: weight + inertia (bhaari cheez der se react kare), natural frequency (lamba ped dheere, ghaas tez),
flexible parts root par stiff aur tip par lachile (arc bend, no rigid "lakdi" rotation), damping, follow-through / overlap,
per-element phase variation (sab sync mein nahi), wind / gravity / collision consistent across the shot. Creatures: real gait
cycles (reference footage / mocap-like timing), no floaty or linear motion. Cameras: real lens + rig behaviour (no impossible moves
unless the shot asks). Har animated preview frame-by-frame check karo; doubt ho to simulation (cloth / softbody / rigid / fluid) use karo.
**Physics + destruction:** har physics / destruction real-world jaisa — real scale (1 BU = 1 m) aur gravity 9.81 m/s², sahi mass /
density, friction, bounce; material ke hisaab se tootna: patthar / concrete = bade-chhote irregular chunks (Voronoi / Cell Fracture,
inner faces ka alag material), lakdi = splinters + resha (fibres) ke saath, kaanch = tez dhaar wale shards, mitti = dheele dhele + dhool,
dhaatu = mudna / pichakna (tootna kam); rigid-body sim (constraints / breakable joints, sahi collision shapes), dust + smoke
(Mantaflow), chhota debris + particles, impact par roshni / dhool / awaaz ka timing; pehle bade tukde, phir chhote; koi bhi cheez hawa
mein ruki ya bina wazan ke nahi; energy ke hisaab se speed (chhoti takkar = kam tootna). Destruction shots: pehle sim preview, frame-by-frame
check, phir final high-res sim (Director ke GPU PC par).


## 🔁 NEW SESSION? Start here (memory reset ke baad)
0. **SABSE PEHLE** `HANDOFF.md` padho (+ Director ke verbatim inputs `02_world/ecosystem/DIRECTOR_INPUTS_TASK06.md`) aur `bash setup_session.sh` chalao (SCRATCH=scratchpad; jo bana hai DOBARA MAT BANAO). `HANDOFF.md` (poora handoff + restore steps) + `PROJECT_LOG.md` + `STATUS.md` + `01_characters/PRODUCTION_INVENTORY.md` padho aur Director ko
   Hinglish mein **poora detailed summary** do: kya kya bana, kya chal raha tha, kya pending hai, kaunse sawaal baaki hain.
   Phir wahin se kaam shuru karo jahan ruka tha. Har bada kaam hone par `PROJECT_LOG.md` mein entry jodo.
1. `pip install bpy scipy` (Blender 5.3 Python module). **TASK 04 world files need Blender 4.5:**
   `uv venv -p /usr/bin/python3.11 <scratch>/bpy45 && VIRTUAL_ENV=<scratch>/bpy45 uv pip install "bpy>=4.5,<4.6" numpy`
   then `BLENDER=<scratch>/bpy45/bin/python 02_world/3d_world/scripts/run_all.sh`. Viewport (Workbench/EEVEE) renders need
   `apt-get install -y libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1` and `EGL_PLATFORM=surfaceless`. + `python3 03_assets/external/polyhaven_fetch.py` (Poly Haven CC0 assets, gitignored; environment `animation-studio`).
2. Padho: `01_characters/PRODUCTION_INVENTORY.md` (status + pending decisions) aur `STATUS.md` (last kya chal raha tha).
3. Har character ka sab kuch uski config mein hai: `01_characters/<name>/<name>_config.py`.
4. Pipeline: `_shared/build_char.py` → `_shared/sheet_render.py` → `_shared/sheet_compose.py` → `_shared/production.py` → `_shared/sheet_doc.py`
   (batch: `_shared/render_all.sh`, `_shared/production_all.sh`). QC: `<name>/qc/QC_REPORT.md`.
5. Kaam karte waqt `STATUS.md` update karte raho aur commit + push karte raho.

## 🧠 Technical lessons (bugs already solved — don't repeat)
- Bone-parenting: use `charkit.bone_parent` (compensation in `matrix_parent_inverse`), else eyelid/eye rotations break.
- Clothing = trimmed copies of the WEIGHTED body: weight body first, keep face if its CENTRE is in the region,
  create matching vertex groups right after trimming (else weights double → exploded verts).
- Trimmed pieces: merge doubles 0.0015 m; Solidify `thickness_clamp=1.0`, quality normals (else fingertip spikes).
- Big pauldrons fold when the arm drops → make them rigid on the clavicle (`'rigid': 'clavicle'`).
- Bevel on tiny pieces: `limit_method='ANGLE'`, clamp overlap.
- Design sheets use view transform 'Standard' so palette colours stay exact.
- Portal disc shader uses object X/Y (circle primitive plane), not X/Z.
- After an invisibility override, reset only the world colour — `studio()` deletes the cameras.
- Beams/lasers must not point at the camera (read end-on as a square): flatten the Y component.
- QC: `sheet_render.py <char> qc` writes `mesh_sanity_fail`; must be [] before rendering sheets.
- Machine: 4 CPU, no GPU. Full sheet ≈ 12–25 min/char at 24 samples; production bake 1K ≈ 20+ min/char.
- Background waiters: never `pgrep -f` (matches itself) — grep a log marker instead.
- Alpha foliage cards: Cycles `transparent_max_bounces = 64`; same UV layer name on all meshes before joining.
- Driven bones (jaw): reset_pose must not change their rotation mode; `arm.update_tag()` before evaluating drivers.
- Rigify: re-fit the human template (bone collections), `spine.004 connect_chain=False`, set rigify_type on template bones too,
  mute constraints while re-parenting, check skirt TRANSFORM ranges after Rigify re-rolls bones.
- Poly Haven API needs a User-Agent; append LOD collections + fix image paths; save with relative_remap.
- Don't use a world volume for haze (blocks the sun) — bounded volume box; sun behind camera = flat light.
- Blender 4.5: shading colour enum for attributes is 'VERTEX' (not 'ATTRIBUTE'); disable `.blend1` with
  `preferences.filepaths.save_version = 0`; join objects only after deselecting everything.
- World-scale terrain: cut ONE height grid into pieces (shared border verts + global custom normals) → seamless; huge single
  world volumes are slow/opaque — bounded haze boxes; coarse LODs need the river channel ≥ 1 vertex row wide (else water hides).
- Linked data cannot be edited in memory → control render visibility of linked overlays with view-layer collection exclude.

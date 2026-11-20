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

#!/usr/bin/env bash
# Nayi Claude Code session ka poora setup — ek command:  bash setup_session.sh
# Idempotent: dobara chalane par jo already hai use skip karta hai. Kuch bhi REBUILD nahi karta (saari .blend/renders git mein hain).
set -u
cd "$(dirname "$0")"
SP=${SCRATCH:-/tmp/claude_scratch}; mkdir -p "$SP"
echo "== 1. Blender 5.3 Python module (characters, Ashram v3) + scipy"
python3 -c "import bpy" 2>/dev/null || pip install -q bpy scipy
python3 -c "import scipy" 2>/dev/null || pip install -q scipy
echo "== 2. Blender 4.5 LTS Python module (TASK 04+ world files MUST use 4.5)"
export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || pip install -q uv
PY311=/usr/bin/python3.11; [ -x "$PY311" ] || PY311=3.11          # uv downloads Python 3.11 if the system has none
if [ ! -x "$SP/bpy45/bin/python" ]; then
  uv venv -q -p "$PY311" "$SP/bpy45" && VIRTUAL_ENV="$SP/bpy45" uv pip install -q "bpy>=4.5,<4.6" numpy
fi
"$SP/bpy45/bin/python" -c "import bpy; print('  bpy', bpy.app.version_string)"
echo "== 3. Mesa software OpenGL (Workbench viewport screenshots / EEVEE, headless)"
dpkg -s libegl-mesa0 >/dev/null 2>&1 || (apt-get install -y -q libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1 >/dev/null 2>&1 || \
  (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1 >/dev/null 2>&1))
echo "== 4. Poly Haven CC0 assets (~860 MB, gitignored; needs environment 'animation-studio')"
python3 03_assets/external/polyhaven_fetch.py | tail -1   # idempotent: downloads only files that are missing (TASK 05 list included)
echo "== 5. Task 04 baseline integrity (v001 files must be unchanged)"
python3 - <<'EOF'
import json, hashlib, os
m = json.load(open('02_world/3d_world/TASK04_BASELINE_MANIFEST.json'))
bad = [f for f, v in m['files'].items() if hashlib.sha256(open(os.path.join('02_world/3d_world', f), 'rb').read()).hexdigest() != v['sha256']]
print('  baseline files:', len(m['files']), '| changed:', bad or 'none')
EOF
echo "SETUP_DONE — use:  BPY45=$SP/bpy45/bin/python   (EGL_PLATFORM=surfaceless for Workbench renders)"

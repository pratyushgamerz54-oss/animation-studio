#!/usr/bin/env bash
# TASK 04 — rebuild the whole 3D world blockout from the map data, then render previews + QC.
#   BLENDER   = Blender 4.5 executable (default: 'blender')  — e.g. BLENDER="/path/to/blender"
#   PY        = system python3 with numpy+scipy+pillow (data prep + contact sheets)
# Usage: 02_world/3d_world/scripts/run_all.sh [build|render|qc|all]   (default all)
set -euo pipefail
cd "$(dirname "$0")"
BLENDER=${BLENDER:-blender}
PY=${PY:-python3}
B() { if [[ "$BLENDER" == *python* ]]; then "$BLENDER" "$@"; else "$BLENDER" -b --factory-startup -P "$1" -- "${@:2}"; fi; }
STEP=${1:-all}
if [[ $STEP == all || $STEP == build ]]; then
  $PY w4_prep_world.py && $PY w4_prep_valley.py && $PY w4_prep_dims.py
  B w4_build_materials.py && B w4_build_assets.py && B w4_build_world.py
  B w4_build_valley.py && B w4_build_dims.py && B w4_build_master.py
fi
if [[ $STEP == all || $STEP == render ]]; then
  EGL_PLATFORM=surfaceless B w4_render.py
  $PY w4_contact_sheets.py
fi
if [[ $STEP == all || $STEP == qc ]]; then
  B w4_qc.py
fi
echo ALLDONE

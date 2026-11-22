#!/usr/bin/env bash
# TASK 06 · finish the work that was still rendering at the end of session 4 (idempotent — safe to run any time).
#   SCRATCH=<scratchpad> bash 03_assets/vegetation/scripts/t6_finish_pending.sh
# Needs: setup_session.sh done (Blender 4.5 module in $SCRATCH/bpy45, Poly Haven assets fetched).
# Steps (each skipped when already done):
#   1. wind physics v3 clip  → 03_assets/vegetation/renders/WIND_TEST_v3.mp4   (resumes at the first missing frame)
#   2. realism v3            → atlases (soft veins, spots, bites, drying leaves, natural saturation) + libraries rebuild
#                              + all sheet renders (camera look) + compose + contact sheet + QC (4.5 + 5.3) + report
#                              marker: 03_assets/vegetation/textures/leaves/.leaf_realism_v2 (sub-steps: textures/leaves/.v3_steps/)
# Afterwards: git add -A && git commit && git push (the script prints the reminder).
set -u
cd "$(dirname "$0")"
SP=${SCRATCH:?set SCRATCH=<scratchpad dir>}; PY=$SP/bpy45/bin/python
[ -x "$PY" ] || { echo "run setup_session.sh first (no $PY)"; exit 1; }
VEG=..
# ---------------------------------------------------------------- 1. wind v3
if [ ! -f $VEG/renders/WIND_TEST_v3.mp4 ]; then
  mkdir -p $SP/wind3; N=$(ls $SP/wind3 2>/dev/null | grep -c '^f_.*png$'); START=$((N > 0 ? N : 1))
  echo "== wind v3: frames on disk $N → rendering from $START"
  SCR=$SP WDIR=wind3 FSTART=$START SPP=6 $PY t6_wind_test.py 2>&1 | grep --line-buffered 'rror\|Trace\|DONE'
  ffmpeg -y -loglevel error -framerate 24 -i $SP/wind3/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 19 $VEG/renders/WIND_TEST_v3.mp4 \
    && echo "WIND_TEST_v3.mp4 written"
else
  echo "== wind v3 clip already exists — skip"
fi
# ---------------------------------------------------------------- 2. realism v3 (leaf atlases + materials + camera look)
# every sub-step is resumable: step markers in $M, sheet renders skip assets already rendered from the current library (SKIP_FRESH=1)
M=$VEG/textures/leaves/.v3_steps; mkdir -p $M
step() { [ -f $M/$1 ]; }
done_() { date > $M/$1; }
if [ ! -f $VEG/textures/leaves/.leaf_realism_v2 ]; then
  echo "== realism v3: atlases → libraries → sheet renders → QC (resumable)"
  step atlases || { python3 t6_leafgen.py 2>&1 | grep --line-buffered 'rror\|DONE' && done_ atlases; }
  for R in AV EF MK; do
    step lib_$R || { $PY t6_build_library.py -- $R 2>&1 | grep --line-buffered 'SAVED\|rror' && done_ lib_$R; }
  done
  for R in AV EF MK; do
    SPPR=$([ $R = AV ] && echo 24 || echo 16)
    step render_$R || { SKIP_FRESH=1 SPP=$SPPR $PY t6_render_sheets.py -- $R 2>&1 | grep --line-buffered 'rror\|Trace\|DONE' | tee $SP/render_$R.log
                        grep -q T6_RENDER_DONE $SP/render_$R.log && done_ render_$R; }
  done
  python3 t6_compose_sheets.py AV EF MK | tail -1; python3 t6_contact_sheet.py | tail -1
  T6_QC_REGIONS="AV EF MK" $PY t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'
  T6_QC_REGIONS="AV EF MK" python3 t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'
  python3 t6_qc.py --report | tail -1
  date > $VEG/textures/leaves/.leaf_realism_v2
else
  echo "== realism v3 already applied — skip"
fi
echo "T6_FINISH_PENDING_DONE — now: git add -A && git commit -m '...' && git push"

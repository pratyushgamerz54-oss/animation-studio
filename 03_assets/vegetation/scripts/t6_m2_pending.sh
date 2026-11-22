#!/usr/bin/env bash
# TASK 06 · MILESTONE 2 pipeline — resumable (safe to run again after a restart; finished steps are skipped).
#   SCRATCH=<scratchpad> bash 03_assets/vegetation/scripts/t6_m2_pending.sh
# Steps (markers in 03_assets/vegetation/.m2_steps/):
#   lib_<R>        hero libraries  PL LK DS FB CT CV ND (+ AV with realism v3.1 moss / thatch-on-ground + scatter copies)
#   render_<R>     sheet renders (SKIP_FRESH: only assets older than their library)   · plants_AV = AV plants + plant lineup
#   compose        tree / plant / region sheets for every region + contact sheets M1 + M2
#   impostors_<R>  LOD3 impostor textures (front + side alpha renders)
#   lods_<R>       T6_VEG_<R>_VARIANTS_v001 + T6_VEG_<R>_LODS_v001
#   qc             QC of every library (Blender 4.5 + 5.3) + report
set -u
cd "$(dirname "$0")"
SP=${SCRATCH:?set SCRATCH=<scratchpad dir>}; PY=$SP/bpy45/bin/python
[ -x "$PY" ] || { echo "run setup_session.sh first (no $PY)"; exit 1; }
M=../.m2_steps; mkdir -p $M
step() { [ -f $M/$1 ]; }
done_() { date > $M/$1; echo "STEP $1 done"; }
ALL="AV EF MK PL LK DS FB CT CV ND"; M2="PL LK DS FB CT CV ND"
for R in $M2; do
  step lib_$R || { $PY t6_build_library.py -- $R 2>&1 | grep --line-buffered 'SAVED\|rror' | tee $SP/m2_lib_$R.log; grep -q SAVED $SP/m2_lib_$R.log && done_ lib_$R; }
done
for R in $M2; do
  step render_$R || { SKIP_FRESH=1 SPP=16 $PY t6_render_sheets.py -- $R 2>&1 | grep --line-buffered 'rror\|Trace\|DONE' | tee $SP/m2_render_$R.log
                      grep -q T6_RENDER_DONE $SP/m2_render_$R.log && done_ render_$R; }
done
# AV is rebuilt only after the realism-v3 chain (t6_finish_pending.sh) has finished with it (it renders EF / MK itself)
while [ ! -f ../textures/leaves/.leaf_realism_v2 ] && pgrep -f "t6_finish_pending.s[h]" > /dev/null; do sleep 30; done
step lib_AV || { $PY t6_build_library.py -- AV 2>&1 | grep --line-buffered 'SAVED\|rror' | tee $SP/m2_lib_AV.log; grep -q SAVED $SP/m2_lib_AV.log && done_ lib_AV; }
for R in EF MK; do
  step render_$R || { SKIP_FRESH=1 SPP=16 $PY t6_render_sheets.py -- $R 2>&1 | grep --line-buffered 'rror\|Trace\|DONE' | tee $SP/m2_render_$R.log
                      grep -q T6_RENDER_DONE $SP/m2_render_$R.log && done_ render_$R; }
done
step plants_AV || { SKIP_FRESH=1 ONLY=plants SPP=24 $PY t6_render_sheets.py -- AV 2>&1 | grep --line-buffered 'rror\|Trace\|DONE' | tee $SP/m2_render_AVp.log
                    grep -q T6_RENDER_DONE $SP/m2_render_AVp.log && done_ plants_AV; }
step compose || { python3 t6_compose_sheets.py $ALL | tail -1 && python3 t6_contact_sheet.py | tail -1 && python3 t6_contact_sheet.py M2 | tail -1 && done_ compose; }
for R in $ALL; do
  step impostors_$R || { $PY t6_render_impostors.py -- $R 2>&1 | grep --line-buffered 'rror\|Trace\|DONE' | tee $SP/m2_imp_$R.log
                         grep -q T6_IMPOSTORS_DONE $SP/m2_imp_$R.log && done_ impostors_$R; }
done
for R in $ALL; do
  step lods_$R || { $PY t6_build_lods.py -- $R 2>&1 | grep --line-buffered 'SAVED\|rror\|Trace\|DONE' | tee $SP/m2_lods_$R.log
                    grep -q T6_LODS_DONE $SP/m2_lods_$R.log && done_ lods_$R; }
done
step qc || { T6_QC_REGIONS="$ALL" $PY t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'; T6_QC_REGIONS="$ALL" python3 t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'
             python3 t6_qc.py --report | tail -1; done_ qc; }
echo "T6_M2_PENDING_DONE — now: git add -A && git commit -m '...' && git push"

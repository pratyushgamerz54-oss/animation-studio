#!/usr/bin/env bash
# TASK 06 · milestone 2 closeout: populated files (with variants + LODs linked) → cinematic previews → QC → sheets.
# Resumable: previews already rendered are kept (delete a PNG to re-render it). One Blender at a time (16 GB machine).
#   SCRATCH=<scratchpad> bash 03_assets/vegetation/scripts/t6_final_previews.sh
set -u
cd "$(dirname "$0")"
SP=${SCRATCH:?set SCRATCH=<scratchpad dir>}; PY=$SP/bpy45/bin/python
OUT=../../../02_world/ecosystem/renders/populated; mkdir -p $OUT
M=../.m2_steps; mkdir -p $M
for R in AV EF MK DS FB; do
  [ -f $M/populate_$R ] || { $PY t6_populate.py -- $R 2>&1 | grep --line-buffered 'SAVED\|rror\|Trace' && date > $M/populate_$R; }
done
declare -A F=([AV]=T6_POP_R01_ASHRAM_VALLEY_v001 [EF]=T6_POP_R02_ENCHANTED_FOREST_v001 [MK]=T6_POP_R03_MOUNTAIN_KINGDOM_v001
              [DS]=T6_POP_R04_GOLDEN_DESERT_v001 [FB]=T6_POP_R05_FORBIDDEN_LANDS_v001)
declare -A C=([AV]="T6_CAM_AV_COURTYARD_PEEPAL T6_CAM_AV_GROVE_EDGE T6_CAM_AV_MEADOW_LOW CAM_T5_07_GROUND_LEVEL"
              [EF]="T6_CAM_EF_FOREST_FLOOR T6_CAM_EF_GLADE CAM_T5_10_ENCHANTED_FLOOR" [MK]="T6_CAM_MK_FOREST_EDGE CAM_T5_12_CAVE_ENTRANCE"
              [DS]="T6_CAM_DS_WADI T6_CAM_DS_INTERDUNE CAM_T5_05_DESERT" [FB]="T6_CAM_FB_RIM_DEAD_TREES CAM_T5_09_FORBIDDEN_RIM")
for R in DS FB AV MK EF; do
  for cam in ${C[$R]}; do
    [ -f $OUT/${F[$R]}__$cam.png ] && continue
    RES=${RES:-1280x720} SPP=${SPP:-24} $PY t6_render_populated.py -- $R $cam 2>&1 | grep --line-buffered 'RENDER\|PEAK\|Trace\|rror'
  done
done
python3 t6_pop_sheet.py | tail -1
$PY t6_pop_qc.py 2>&1 | grep --line-buffered 'FAIL\|DONE'
T6_QC_REGIONS="AV EF MK PL LK DS FB CT CV ND" $PY t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'
T6_QC_REGIONS="AV EF MK PL LK DS FB CT CV ND" python3 t6_qc.py 2>&1 | grep --line-buffered 'FAIL\|T6_QC'
python3 t6_qc.py --report | tail -1
echo "T6_FINAL_PREVIEWS_DONE — now: git add -A && git commit && git push; send the Director T6_SHEET_M2 + T6_POPULATED_PREVIEWS"

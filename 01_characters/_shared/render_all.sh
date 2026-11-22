#!/bin/bash
# Render + compose design sheets (and test poses) for every character.
cd "$(dirname "$0")/../.."
for c in ${@:-hero1 pratyush saithan soul max yayaki ramarat}; do
  echo "##### $c $(date +%T)"
  rm -rf 01_characters/$c/design/raw
  python3 01_characters/_shared/build_char.py $c 002 2>&1 | grep -E "SAVED|Error|Traceback"
  SAMPLES=${SAMPLES:-24} python3 01_characters/_shared/sheet_render.py $c qc turn poses face expr costume powers extras tests 2>&1 | grep -E "GROUP|DONE|Error|Traceback|line [0-9]+|mesh_sanity"
  python3 01_characters/_shared/sheet_compose.py $c 2>&1 | grep -E "wrote|Error|Traceback"
  echo "##### done $c $(date +%T)"
done
echo ALLDONE

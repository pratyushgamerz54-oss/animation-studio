#!/bin/bash
# Stage 5-7/10 for every character, then design docs.
cd "$(dirname "$0")/../.."
for c in ${@:-hero1 pratyush saithan soul max yayaki ramarat}; do
  echo "##### prod $c $(date +%T)"
  python3 01_characters/_shared/production.py $c --res 1024 2>&1 | grep -E "PRODUCTION DONE|Traceback|Error|BAKE FAIL" | cut -c1-200
  python3 01_characters/_shared/sheet_doc.py $c
done
echo PRODALLDONE

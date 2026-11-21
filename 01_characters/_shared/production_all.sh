#!/bin/bash
# Stage 5-7/10 for every character, then design docs.
cd "$(dirname "$0")/../.."
for c in ${@:-hero1 pratyush saithan soul max yayaki ramarat}; do
  echo "##### prod $c $(date +%T)"
  python3 01_characters/_shared/production.py $c --res 1024 2>&1 | grep -E "PRODUCTION DONE|Traceback|Error|BAKE FAIL" | cut -c1-200
  python3 01_characters/_shared/rigify_build.py $c 2>&1 | grep -E "^RIGIFY \{|Traceback|Error" | cut -c1-300
  python3 01_characters/_shared/sheet_doc.py $c
  python3 01_characters/_shared/qc_contact.py $c
done
echo PRODALLDONE

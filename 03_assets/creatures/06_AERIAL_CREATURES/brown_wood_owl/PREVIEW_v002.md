# Brown wood owl v002 (Director 24 Nov: "thoda plastic jaisa nhi lag rha hai")
- Cause found: the scan material was UNLIT (Emission + Light Path, lighting baked in the photo texture) → the bird ignored scene light /
  shadows and read flat / plastic; the matte settings of v001 never applied.
- `scripts/t7_feather_fuzz.py`: lit Principled feathers (rough .85, spec .18, light sheen, texture bump; value .8 / sat 1.15 compensation
  for the baked light) + fine matte feather-fuzz groom (fluffy breast, sleek back, short facial disc), perch untouched.
- v001 stays until the Director okays v002.

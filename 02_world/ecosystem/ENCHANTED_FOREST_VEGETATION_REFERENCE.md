# ENCHANTED FOREST (R-02) — VEGETATION REFERENCE v2 (Decision Sheet 01 §3)

Sheets: `03_assets/vegetation/sheets/EF/` (tree sheets, `PLANTS_EF.png`, `REGION_EF.png`) · library
`03_assets/vegetation/library/T6_VEG_ENCHANTED_FOREST_v001.blend`. Season: Spring (`SEASON_REFERENCE_SPRING.md`).

## 1. APPROVED art direction
* Balanced mix: **≈ 70–80 % natural-looking trees, ≈ 20–30 % selected fantasy varieties** (initial art-direction targets, not ecology).
* Giant ancient trees in **selected areas** (not everywhere).
* Unusual roots and **selected** twisted trunks.
* Moss and **selected** plants with **subtle** bioluminescence; **limited** glowing vegetation at night. Glow allowed — never every tree.
* Look: magical, natural, believable, cinematic.

## 2. Species mix (target share of trees, by count)
| Group | Species (library asset) | Target share | Placement |
|---|---|---|---|
| Natural | Giant Elder `EF_T01` | 3–5 % (emergent, selected areas only — "giant groves") | core zones, widely spaced |
| Natural | Teal Beech `EF_T02` | 30–35 % | main canopy everywhere |
| Natural | Ancient Moss Oak `EF_T03` | 12–15 % | clearings, stream sides |
| Natural | Old Yew `EF_T04` | 10–12 % | understorey, rocky banks |
| Natural | Dead Snag `EF_T08` | 3–5 % | scattered |
| **Natural total** | | **≈ 75 %** (range 70–80 %) | |
| Fantasy (approved) | Veil Willow `EF_T05` | 8–10 % | pools, slow streams |
| Fantasy (approved) | Spiral-root Tree `EF_T06` (unusual roots, twisted trunk) | 8–10 % | wet hollows |
| Fantasy (approved) | Lantern Tree `EF_T07` (glowing pods) | 5–8 % | glades |
| **Fantasy total** | | **≈ 25 %** (range 20–30 %) | clustered by habitat, not evenly sprinkled |
Ground: giant fern `EF_FE01`, moss carpet `EF_M01`, hanging liana `EF_V01`, beard moss (on oaks / elders), Glowcap `EF_MU01` (logs, selected).

## 3. Glow rules (subtle bioluminescence)
| Asset | Glow | Limit (v001 values, QC-checked ≤ 1.0) |
|---|---|---|
| Lantern Tree pods | soft pale-mint | Emission 0.6 (was 2.5) — invisible in daylight, soft at dusk / night |
| Glowcap mushrooms | pale teal | caps 0.5, gills 0.15 (was 1.5 / 0.4) |
| Glow-moss (selected moss patches) | faint teal-green | ≤ 0.3 — **production item** (variant of `EF_M01`), only around pools / Lantern glades |
| All other trees / plants | **none** | 0 |
Night: glowing vegetation in **≤ 10 % of the frame area** and only in selected spots (glades, pools); emission is never the key light —
moon / sky stays the main light. Day: glow not visible.

## 4. Pending / production (after these documents)
Scatter recipe `NG_T6_ECOSYSTEM` (R-02) with the shares above · glow-moss variant · 3–5 variants per species · LODs.

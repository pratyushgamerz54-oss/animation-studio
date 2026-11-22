# BLENDER 4.5 ENVIRONMENT PRODUCTION CHECKLIST (updated for Decision Sheet 01)

Use for every environment / vegetation file and shot. Tick in the QC report of the task.

## A. File + version
- [ ] Built and saved with **Blender 4.5.16 LTS** (`$SCRATCH/bpy45/bin/python`); opens in 4.5 (Director PC) and 5.3 without errors.
- [ ] Approved baselines never overwritten (TASK 04 v001 manifest, TASK 05 v002, T6 libraries) — new versions `vNNN+1`; backup before re-save.
- [ ] Relative image paths; no missing images; Poly Haven assets re-fetchable (`polyhaven_fetch.py`); file < 100 MB (GitHub).
- [ ] `.blend1` off (`preferences.filepaths.save_version = 0`).

## B. World / region consistency
- [ ] Region IDs match **Map Revision 01** (`02_world/3d_world/01_GEOGRAPHY/data/world_features.json`, `map_v2/data/features.json`):
      R-01 Ashram Valley · R-02 Enchanted Forest · R-03 Great Northern Range (= Mountain Kingdom) · R-04 Western Desert (= Golden Desert) ·
      R-05 Forbidden Region (= Forbidden Lands) · R-06 Southern Grasslands (= Green Plains) · R-07 Eastern Spine · R-08 Lake District (= Crystal Lakes) ·
      C-01 / C-02 / C-03 = three **separate** archaeological sites (no shared history invented).
- [ ] Sky Realms = **PROPOSED region of the main world** (not a dimension) — no routes, inhabitants, kingdoms or story events.
- [ ] Geography / layout of approved terrains unchanged; TASK 05 masks + tree line (3 550 m) respected.
- [ ] Labels: CONFIRMED / APPROVED / PROPOSED / NOT CONFIRMED / PENDING kept separate in docs and custom properties.

## C. Season + look
- [ ] Season = **Spring** in every connected scene (fresh greens, spring sun, flowers; red Burans in R-01 + R-03 M1); no plumed kans as a seasonal feature.
- [ ] Region colour key (World Bible) respected; Enchanted Forest glow subtle (emission ≤ 1.0, ≤ 10 % of frame at night, none by day).

## D. Vegetation placement
- [ ] Ashram: ONE landmark Peepal at the main courtyard + stone sitting platform; **Tulsi + Marigold only in `ASHRAM_GARDEN`** (QC: no other instances).
- [ ] Enchanted Forest: ≈ 70–80 % natural / 20–30 % fantasy trees; giants only in selected zones.
- [ ] Slope / altitude / water rules (Ecosystem Bible §2); aquatic plants only on still / slow water; no floating (lowest point below terrain), roots buried.
- [ ] Wildlife: **none placed** until the Director's selection (`WILDLIFE_SELECTION_SHEET.md`).

## E. Assets
- [ ] Real geometry + UVs + PBR (no illustrations); wind attributes + `T6_WIND` modifier; `T6_WIND_CONTROL` present.
- [ ] Polycount budget per LOD; LOD0 for close-ups (CLAUDE.md 4K rule); texel density check.
- [ ] Automated QC (`t6_qc.py`) 100 % PASS in 4.5 (+ 5.3 open test).

## F. Render / preview
- [ ] Preview renders CPU Cycles (sheet 24 spp, region 16 spp), `transparent_max_bounces = 64` for foliage; AgX.
- [ ] Final shots: 4K on the Director's GPU PC (CLAUDE.md FINAL OUTPUT RESOLUTION RULE).

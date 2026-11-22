# DECISION SHEET 01 — Official design decisions & Map Revision 01 integration (Director, 22 Nov) — APPLIED

Separation used everywhere: **APPROVED** (this decision sheet) · **PROPOSED** (my proposal, needs approval) · **PENDING** (waiting for
the Director) · **CONFIRMED / NOT CONFIRMED** (story canon — unchanged; no story / script document received yet, nothing invented).
Verification: `DECISION_SHEET_01_VERIFICATION.md` (automated, `03_assets/vegetation/scripts/t6_decision01_verify.py`).

## 1. Region mapping — APPROVED
| Brief name | Map Revision 01 | Verified in data | World coords (km) / elev |
|---|---|---|---|
| Mountain Kingdom | R-03 Great Northern Range | `world_features.json` + `features.json` `c1_regions` | (−2185.5, +1523.4) · 3 538 m |
| Green Plains | R-06 Southern Grasslands | same | (−3570.8, +320.0) · 314 m |
| Crystal Lakes | R-08 Lake District | same | (−1851.0, +1151.6) · 315 m |
| Ancient City | C-01, C-02, C-03 — **three separate archaeological sites** | `features.json` `c1_city_codes`; 3 C1 city markers | (−1882.7, +647.1) · (−2851.2, −4.1) · (−3459.8, +290.0) |
Not assumed: one city, shared history, inhabitants, period (NOT CONFIRMED). "Kingdom" in "Mountain Kingdom" = name only.

## 2. Sky Realms — design direction APPROVED · region PROPOSED
A proposed region **within the main world** (NOT a separate dimension): large floating islands of natural rock, selected islands with
forests + waterfalls, ancient-looking structures, clouds + atmospheric depth between islands, some natural bridges / suspended land
formations, strong visual connection with the main world. **Not established:** travel routes, inhabitants, kingdoms, politics, story
events. **PENDING:** map position (candidates in `WORLD_BIBLE.md` / `GEOGRAPHY.md`, not drawn), story role.

## 3. Enchanted Forest — APPROVED
≈ 70–80 % natural / ≈ 20–30 % fantasy (art-direction targets), giants in selected areas, unusual roots + selected twisted trunks,
subtle bioluminescence on selected moss / plants, limited night glow. Applied: fantasy label → `FANTASY (APPROVED R-02)`; glow lowered
(Lantern pods 2.5 → 0.6, Glowcap 1.5 / 0.4 → 0.5 / 0.15; QC limit ≤ 1.0); shares + rules in `ENCHANTED_FOREST_VEGETATION_REFERENCE.md`.

## 4. Ashram planting — APPROVED
One prominent Peepal near the main courtyard + sitting area (stone platform) = landmark; Tulsi + Marigold ONLY in the Ashram garden;
consistent garden layout in all Ashram scenes. Applied: `02_world/ashram/ASHRAM_LANDSCAPING_PLAN.md` + `00_REFERENCE/ASHRAM_landscaping_plan_v1.png`;
asset habitat metadata. **PROPOSED:** exact spots (Peepal at the courtyard centre; garden = 2 beds on the south lawn).

## 5. Wildlife — PENDING
No separate "Wildlife Design Bible" file exists; the complete existing list = `ECOSYSTEM_BIBLE.md` §7 / `WILDLIFE_PROPOSAL.png` (60 animals).
Selection sheet: `WILDLIFE_SELECTION_SHEET.md` / `.png` (name, design reference, habitat, film appearance, essential/optional =
recommendation only, 3D asset exists = none). **Nothing selected; no new animals; no wildlife assets until the Director selects.**

## 6. Season — Spring APPROVED (proposed primary season)
`SEASON_REFERENCE_SPRING.md`: lush fresh greens, spring sun, flowers, red Burans (R-01 + R-03 M1), vibrant Ashram garden; kans plumes
not a seasonal feature; one season across connected scenes.

## 7. Documents updated / created
| # | Required document | File(s) |
|---|---|---|
| 1 | Environment & World Design Bible | `02_world/WORLD_BIBLE.md` (★ Decision Sheet 01 block, region table, §3 Q12–13) · `02_world/ecosystem/ECOSYSTEM_BIBLE.md` (v2: header, §1, §2.7 + §2.9, §3, §4.1, §4.2, §4.3, §4.4, §4.10, §7, §12) |
| 2 | Master World Map documentation | `02_world/map_v2/GEOGRAPHY.md` (★ Decision Sheet 01 block, pending item 8) — map images unchanged |
| 3 | Regional Environment Reference Sheets | `03_assets/vegetation/sheets/{AV,EF,MK}/REGION_*.png` (re-composed: approved mapping, Spring, EF mix, Ashram placement) |
| 4 | Enchanted Forest vegetation reference | `02_world/ecosystem/ENCHANTED_FOREST_VEGETATION_REFERENCE.md` · EF sheets / library labels + glow |
| 5 | Ashram landscaping plan | `02_world/ashram/ASHRAM_LANDSCAPING_PLAN.md` + `00_REFERENCE/ASHRAM_landscaping_plan_v1.png` |
| 6 | Wildlife selection sheet | `02_world/ecosystem/WILDLIFE_SELECTION_SHEET.md` + `.png` |
| 7 | Seasonal environment reference | `02_world/ecosystem/SEASON_REFERENCE_SPRING.md` |
| 8 | Blender 4.5 environment production checklist | `02_world/ecosystem/BLENDER45_ENV_PRODUCTION_CHECKLIST.md` |

## 8. Conflicts found (none blocking)
1. **Kans grass asset** (`AV_G02_KANS_GRASS` v001) shows autumn plumes → conflicts with Spring; flagged, spring variant (no plumes) = production item.
2. **Ashram layout** (zones 1–11) is still a PROPOSAL awaiting approval, and it had no garden zone → garden placed on the free south lawn (PROPOSED).
3. **Peepal size vs courtyard:** canopy ≈ 28 × 34 m inside a 56 × 40 m courtyard — fits, but shades the west/east residences' verandahs (fine for scenes; noted).
4. **World Bible v1 coordinates** (1024 × 768 km map) differ from Map Rev 01 coordinates (12 000 × 6 000 km world) — region IDs are identical;
   Rev 01 coordinates are quoted in the decision blocks.
5. **Sky Realms** have no map position — nothing drawn until the Director chooses.

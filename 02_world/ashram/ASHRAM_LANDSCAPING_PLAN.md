# ASHRAM LANDSCAPING PLAN v1 — Decision Sheet 01 §4 (22 Nov)

Plan image: `02_world/ashram/00_REFERENCE/ASHRAM_landscaping_plan_v1.png` (overlay on layout plan v3; local origin = courtyard
centre, north up, metres). Vegetation assets: `03_assets/vegetation/library/T6_VEG_ASHRAM_VALLEY_v001.blend`.

Status legend: **APPROVED** = Director decision (Decision Sheet 01) · **PROPOSED** = my placement proposal, needs approval ·
the Ashram building layout itself (zones 1–11, `ASHRAM_CONCEPT.md`) is still a **PROPOSAL** — nothing here changes it.

## A. Landmark Peepal — APPROVED
| Item | Value | Status |
|---|---|---|
| Tree | ONE Peepal (`T6_AV_T01_PEEPAL`, *Ficus religiosa*), H ≈ 24 m, canopy ≈ 28 × 34 m, trunk Ø ≈ 3 m with buttress roots + 4 aerial roots | APPROVED (one, near the main courtyard, landmark) |
| Position | courtyard centre (0, 0) — this is the "sacred tree on a stone platform" already shown in zone 6 of the layout | PROPOSED exact spot (fits the existing plan; canopy stays inside the 56 × 40 m courtyard + residences' verandahs) |
| Sitting area | stone platform (chabutra) 9 × 9 m, 0.6 m high, two steps, trunk through the centre; seating ledge on all 4 sides | APPROVED (sitting area) · design PROPOSED |
| Other Peepals | none inside the Ashram; elsewhere only lone trees at village sites | APPROVED (one landmark) |
| Scene rule | the same tree (same seed / variant 0) in every Ashram shot; never re-seeded or replaced | APPROVED (consistency) |

## B. Ashram garden — APPROVED (only place for Tulsi + Marigold)
| Item | Value | Status |
|---|---|---|
| Location | south lawn inside the wall, two beds 22 × 22 m flanking the gate → courtyard path (x ±6…±28 m, y −30…−52 m) | PROPOSED (the layout had no garden zone; this is the free lawn between courtyard and gate) |
| Tulsi (`T6_AV_S02_TULSI`) | 6 raised planters (tulsi vrindavan style, 1.2 m), 3 per bed along the path edge | APPROVED: Ashram garden only |
| Marigold (`T6_AV_F04_MARIGOLD`) | 5 rows per bed, orange + yellow mix, ≈ 25 plants / m row | APPROVED: Ashram garden only |
| Ground | short lawn + gravel paths between beds (TASK 05 Ashram valley ground) | PROPOSED |
| Consistency | garden layout stored once (`ASHRAM_GARDEN` collection, to be built in production), linked into every Ashram scene | APPROVED rule |

**Hard rule (QC):** `T6_AV_S02_TULSI` and `T6_AV_F04_MARIGOLD` must never appear in any scatter outside the `ASHRAM_GARDEN` collection
(forests, cities, other regions). Their `t6_habitat` property says so; the scatter recipes in production exclude them.

## C. Other Ashram vegetation (from the R-01 ecosystem, unchanged)
Inside the wall: lawn, a few Banj oaks / Burans along the wall (spring red flowers), Barberry by the gate. Outside: meadow + wildflowers,
training ground kept bare (VFX space), lotus + reed-mace only in the lake bay by the ghat (zone 10), kans grass only on river bars
(spring = green clumps, no plumes). All PROPOSED placements → final in the scattering step after approval.

## Open (pending Director)
1. Exact Peepal spot: courtyard centre (as drawn) OK, or offset (e.g. west half of the courtyard to keep the hall axis open)?
2. Garden position (south lawn, as drawn) OK?

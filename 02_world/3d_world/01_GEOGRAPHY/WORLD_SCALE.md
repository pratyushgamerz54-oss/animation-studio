# WORLD SCALE & MEASUREMENT SYSTEM — TASK 04 (PROVISIONAL)

> **Status: PROPOSAL.** Every number below comes from world map v2 **revision 01** (`02_world/map_v2/data`), which is
> **NOT LOCKED**. If the Director changes the map, re-run `scripts/run_all.sh` and every 3D file is rebuilt with the new numbers.
> All distances are estimates for a fictional world; nothing here is story canon.

## 1. Three coordinate frames (one per scale level)

| Frame | Used in | 1 Blender unit | Origin | Axes | Vertical |
|---|---|---|---|---|---|
| **W — main world** | `00_MASTER_WORLD`, `01`–`07`, `10_CAMERAS` | **1 km** | centre of the world map | +X east, +Y north | Z = elevation (km) **× 20** (vertical exaggeration, see §3) |
| **V — Ashram Valley** | `08_ASHRAM_VALLEY` | **1 m** (true scale) | proposed Ashram position | +X east, +Y north | Z = metres above sea level (no exaggeration) |
| **D — dimensions** | `09_DIMENSIONS` (one file each) | **1 m** | centre of each dimension | own axes | own; **no shared coordinates with the main world** |

Conversions
- Map grid cell (col, row; row 0 = north) → W: `X = (col + 0.5)·7.8125 − 6000`, `Y = 3000 − (row + 0.5)·7.8125` (km).
- Atlas grid coordinates ("world km", SW origin) = `(X + 6000, Y + 3000)`.
- V → W: Ashram origin = W (−2275, +1238) km = atlas (3725, 4238) km. A point (x, y) m in V lies at W (−2275 + x/1000, 1238 + y/1000).
- Detailed Aetheria grid (3 km cells, `02_world/map/data`): V `x = (col − 596)·3000 m`, `y = (233 − row)·3000 m`.

## 2. World and region dimensions

| Item | Size (estimate) | Source |
|---|---|---|
| Known main world | **12 000 × 6 000 km** (map grid 1536 × 768 cells, 7.8125 km/cell) | map v2 |
| Elevation range | −4 500 m (deep ocean) … +6 682 m (Noxara, Ice Wall) | `height_m.npy` |
| Sea level | 0 m (ocean surface mesh at Z = 0) | — |
| Continental shelf modelled with land | down to −300 m (coast pieces) | prep rule |

| Region (proposed names) | Direction collection | Extent (km) | Area (km²) | Max elevation |
|---|---|---|---|---|
| C1 AETHERIA (home, Ashram) | WESTERN | 2 812 × 2 031 | 3.61 M | 6 205 m |
| C2 SOLMARA | SOUTHERN | 3 218 × 3 281 | 4.91 M | 6 167 m |
| C3 VEYLORA (GEM proposal) | EASTERN | 2 984 × 1 882 | 2.96 M | 5 246 m |
| C4 NOXARA (north part = unexplored) | NORTHERN | 3 851 × 1 203 | 1.39 M | 6 682 m |
| C5 DRAKMOR | SOUTHERN | 1 742 × 1 257 | 1.38 M | 4 981 m |
| A1 Sagara Archipelago · A3 Western Isles | WESTERN | islands 10–150 km | — | — |
| A2 Agni Island Arc | EASTERN | islands 10–100 km | — | — |
| Minor islands IW / IE / IN / IS | by nearest continent | — | — | — |

Direction assignment (temporary, for organisation only): Noxara = north; Aetheria + A1 + A3 = west; Veylora + A2 = east; Solmara + Drakmor = south.

## 3. Heights, mountains, rivers, lakes

- **Vertical exaggeration ×20 in frame W** (stored as `vexag` on every terrain object and on the MAIN_WORLD scene). Reason: at
  1 BU = 1 km a 6.7 km peak on a 12 000 km world is invisible; ×20 shows ranges in aerial views. **True scale** = set the
  objects' Z scale to 1/20 (0.05) or divide Z by 20. Frame V (Ashram Valley) is always true scale.
- Mountains (class MTN = high rock / snow peaks / any cell ≥ 2 200 m). Ranges (proposed names): M1 Mahagiri (C1, peaks ≈ 6 200 m),
  M3 Sunstone Ridge (C2, ≈ 5 200 m), M4 Verdant Crown (C3, ≈ 4 600 m), M5 Ice Wall (C4, ≈ 5 600–6 700 m), M6 Southern Teeth (C5, ≈ 3 900 m).
- Snow: snow-peak biome + any cell > 4 300 m (main world); in the valley frame a snowline of ≈ 3 850 m ± 250 m.
- **Rivers (main world):** 423 rivers, 74 200 km total, longest ≈ 1 190 km. Same rule as the atlas (flow accumulation > 120 cells,
  always on the filled surface → never uphill, 224 mouths reach the sea). *True* width estimate = 0.5·√(drainage area km²) m →
  **43–367 m**. *Display* width in frame W = **2.5–8 km** (exaggerated so rivers are visible from orbit-like aerials).
- **Rivers (Ashram Valley):** 96 rivers / 3 985 km inside ±160 km, from the detailed C1 flow network (same as MAP_G),
  widths **15–140 m** (true), meanders added, banks carved into every LOD.
- **Lakes:** 26 lakes, flat water at each lake's spill level; largest ≈ 46 000 km² (C1, 764 m). Sizes are map-scale estimates.
- Waterfalls: 5 proposed sites (markers + sheets); detailed falls are a regional-stage task.

## 4. Ashram Valley (frame V)

| Item | Value |
|---|---|
| Ashram site | proposed position (map rev 01), terrain pad **692 m** a.s.l. (map estimate 681 m; +11 m from procedural detail) |
| Pad (flattened) | x −75…+75 m, y −135…+75 m = concept v3 compound 120 × 124 m + training ground south |
| Valley | large grassland valley ≈ 45–50 km across (map data), forest ring begins ≈ 22–26 km N and S |
| Snowy range | nearest snow ≈ **101 km north-west** (matches revision 01 "≈ 100 km NW") |
| LOD0 / LOD1 / LOD2 | ±3 km @ 12.5 m · ±30 km @ 100 m · ±160 km @ 1 km (nested; holes match exactly; skirts 15 / 120 / 400 m) |
| Path (proposed) | 4 m wide, ≈ 31 km least-effort route from the gate toward the nearest proposed village (≈ 274 km, 27° NE) |
| Haze | bounded volume 330 × 330 × 5.2 km, density 4.5·10⁻⁶ /m (visibility ≈ 100+ km) |

## 5. Dimensions (frame D — PROPOSALS from MAP_H1 / MAP_H2)

- **Black Hole Training Area:** 1 map px = 1 m. Event horizon r = 150 m, photon ring 175 m, accretion disk 200–480 m;
  platform rings at **560 m (5)**, **700 m (9)**, **830 m (6)**, platform radius 39–61 m; 260 debris rocks 420–880 m.
- **Saithan's Dark World:** 1 map px = 5 m → **9.0 × 6.5 km**; relief ≈ −580 … +480 m (ash plains / shattered highlands);
  350 obsidian spires 70–200 m tall; corrupted portal site (place only) at the map centre.
- **GEM location:** NOT confirmed → no environment built (proposal marker in Veylora only).

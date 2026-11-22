# TASK 05 — PBR Terrain Material Library (`T5_TERRAIN_MATERIALS_v002.blend`)

Blender 4.5 LTS · built by `scripts/t5_build_materials.py` · every image map = Poly Haven **CC0** scan, 2K (2048 × 2048),
loaded from `03_assets/external/polyhaven/textures/` (relative paths; restore with `polyhaven_fetch.py`).

**Reusable building block:** node groups `NG_PBR_<texture>[_BOX][_AT][_AO]`. Inputs: Vector (object metres), Scale (m per tile),
Wet (0–1: darker + glossier), Tint, Normal Strength. Outputs: Color, Roughness, Normal, Height.
`_BOX` = triplanar (cliffs), `_AT` = anti-tiling second sample, `_AO` = ambient occlusion multiplied.
Metallic = 0 for every natural surface. Displacement: height maps drive bump + height-aware layer blending; library materials also
carry a true-displacement output (`displacement_method = BOTH`) for close-ups with adaptive subdivision.

| Material | Source | Maps | Resolution | Tile (m) | Texel density (px/m) | Projection | Metallic |
|---|---|---|---|---|---|---|---|
| `MAT_T5_GRASS` | Poly Haven leafy_grass (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 2.2 | 930.9 | top-down (object XY) | 0.0 |
| `MAT_T5_GRASS_DRY` | Poly Haven sparse_grass (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 3.0 | 682.7 | top-down (object XY) | 0.0 |
| `MAT_T5_SOIL` | Poly Haven dry_ground_01 (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 2.5 | 819.2 | top-down (object XY) | 0.0 |
| `MAT_T5_FOREST_FLOOR` | Poly Haven forest_floor (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 3.0 | 682.7 | top-down (object XY) | 0.0 |
| `MAT_T5_MUD` | Poly Haven mud_forest (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 2.5 | 819.2 | top-down (object XY) | 0.0 |
| `MAT_T5_GRAVEL` | Poly Haven rocky_gravel (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 2.0 | 1024.0 | top-down (object XY) | 0.0 |
| `MAT_T5_ROCK` | Poly Haven rock_ground (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 4.0 | 512.0 | box/triplanar | 0.0 |
| `MAT_T5_CLIFF` | Poly Haven cliff_side (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 12.0 | 170.7 | box/triplanar | 0.0 |
| `MAT_T5_SCREE` | Poly Haven gravel_ground_01 (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 3.0 | 682.7 | top-down (object XY) | 0.0 |
| `MAT_T5_SNOW` | Poly Haven snow_02 (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 4.0 | 512.0 | top-down (object XY) | 0.0 |
| `MAT_T5_SAND` | Poly Haven coast_sand_01 (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 3.0 | 682.7 | top-down (object XY) | 0.0 |
| `MAT_T5_WET_STONE` | Poly Haven river_small_rocks (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 1.6 | 1280.0 | top-down (object XY) | 0.0 |
| `MAT_T5_ROCK_DARK` | Poly Haven dark_rock (CC0) | Base Color, Roughness, Normal GL, Displacement, AO | 2048 x 2048 (2K) | 5.0 | 409.6 | box/triplanar | 0.0 |
| `MAT_T5_ICE` | procedural (voronoi cracks + noise) | Base Color, Roughness 0.12, Subsurface, bump normal | procedural (resolution-independent) | — | — | — | 0.0 |
| `MAT_T5_TERRAIN` | blend of 15 Poly Haven 2K scans + procedural ice/canopy | per layer: Base Color, Roughness, Normal GL, Displacement (height blend) | 2K per layer; near/far scale switch 150–900 m | — | — | — | 0.0 |
| `MAT_T5_WATER_RIVER` | procedural | transmission IOR 1.333, animated ripple bump, foam (attribute "foam" × noise) | procedural | — | — | — | 0.0 |
| `MAT_T5_WATER_LAKE` | procedural | transmission IOR 1.333, animated ripple bump, foam (attribute "foam" × noise) | procedural | — | — | — | 0.0 |
| `MAT_T5_WATERFALL` | procedural | animated falling streaks (noise stretched in Z), subsurface white water, alpha mix | procedural | — | — | — | 0.0 |
| `MAT_T5_MIST` | procedural volume | Principled Volume, density 0.3 (mist) | procedural | — | — | — | — |
| `MAT_T5_HAZE` | procedural volume | Principled Volume, density 1.6e-05 (haze) | procedural | — | — | — | — |

## MAT_T5_TERRAIN — one shader for every terrain tile
Reads the mask attributes written by `NG_T5_HEIGHTFIELD` (m_forest, m_rock, m_snow, m_wet, m_dry, m_pad, m_grove, m_scree,
m_gravel, m_path, m_flow, m_cliff) + the real slope (geometry normal) + altitude + camera distance.
Layer order: grass (2 scans, re-coloured to the approved lush valley green, + aerial grass far away) → dry grass → forest floor
(+ far canopy colour beyond 2.5–6 km) → compacted soil (path, Ashram pad) → bank mud → gravel bars / wet river bed → lake sand →
scree → rock (near scan / far procedural) → cliff (isotropic dark-rock scan / far procedural) → snow (near + aerial) → ice in high couloirs.
Transitions are **height-blended** (pebbles poke through sand, etc.), not linear fades.

## Texture resolution specification
| Use | Resolution | Note |
|---|---|---|
| Ground / rock / snow scans | 2K (2048²) | previews + mid shots; texel density 170–1000 px/m |
| Final 4K close-ups (Director rule) | 4K / 8K versions of the same scans | swap in `polyhaven_fetch.py` (TEX_RES) per shot |
| Heightfields | 32-bit float EXR, 1 px = 1 grid vertex | 1.5 m … 400 m per px depending on the tile |
| Masks | 8-bit PNG (4 × RGB) per tile | same grid as the heightfield |
| Far rock / canopy / ice / water | procedural | resolution independent (no moiré from km away) |

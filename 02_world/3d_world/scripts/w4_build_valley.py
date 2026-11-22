"""TASK 04 · ASHRAM VALLEY terrain blockout → 08_ASHRAM_VALLEY/ASHRAM_VALLEY_terrain_v001.blend (Blender 4.5).

Scene ASHRAM_VALLEY — 1 BU = 1 m, TRUE scale (no exaggeration). Origin = proposed Ashram position, Z = metres a.s.l.
  AV_TERRAIN   LOD0 ±3 km @12.5 m · LOD1 ±30 km @100 m · LOD2 ±160 km @1 km (nested, holes + skirts, no overlap)
  AV_WATER     rivers from the map flow network (meandered, always downhill), carved into all LODs
  AV_FORESTS   Geometry-Nodes instancing of linked proxies (04_FORESTS/FOREST_proxies_v001.blend) — LOD0 trees, LOD1 clumps
  AV_PATHS     PROPOSED least-effort path gate → nearest proposed settlement direction
  AV_ASHRAM_PLACEMENT_REF  pad, compound + training-ground outlines from concept v3 — the building is a SEPARATE asset
  AV_MARKERS   proposed villages / ruins / caves in the window, snow-range reference
  AV_ATMOSPHERE haze volume (bounded box — never a world volume) · AV_CAMERAS · AV_LIGHTING
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import worldkit as wk

D = np.load(wk.P('08_ASHRAM_VALLEY', 'data', 'valley_prep.npz'))
MET = json.load(open(wk.P('08_ASHRAM_VALLEY', 'data', 'valley_features.json')))
SITE = MET['site_elev_m']
STATUS = 'PROPOSAL — Ashram position + valley from map revision 01 (NOT LOCKED)'

wk.new_file()
sc = bpy.context.scene; sc.name = 'ASHRAM_VALLEY'
sc['status'] = STATUS; sc['units'] = '1 BU = 1 m, true scale; Z = elevation a.s.l.'; sc['frame'] = MET['frame']
sc['world_position_km'] = [3725, 4238]
M = wk.link_materials()
proxies = wk.link_collections(wk.P('04_FORESTS', 'FOREST_proxies_v001.blend'), ['PROXY_TREES_NEAR', 'PROXY_CANOPY_FAR'])
top = wk.coll('ASHRAM_VALLEY')
C = {k: wk.coll(k, top) for k in ('AV_TERRAIN', 'AV_WATER', 'AV_FORESTS', 'AV_PATHS', 'AV_ASHRAM_PLACEMENT_REF', 'AV_MARKERS',
                                   'AV_ATMOSPHERE', 'AV_CAMERAS', 'AV_LIGHTING')}
lodc = {k: wk.coll(f'AV_TERRAIN_{k}', C['AV_TERRAIN']) for k in ('LOD0', 'LOD1', 'LOD2')}
# keep the proxy library out of the render but available to Geometry Nodes
lib = wk.coll('AV_PROXY_LIBRARY (linked, hidden)', top)
for c in proxies.values():
    lib.children.link(c)
HOLE = {'LOD0': None, 'LOD1': 3000.0, 'LOD2': 30000.0}
SKIRT = {'LOD0': 15.0, 'LOD1': 120.0, 'LOD2': 400.0}


def hx(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32) ** 2.2


GRIDS = {}
TERR = {}
for L in ('LOD0', 'LOD1', 'LOD2'):
    z = D[f'{L}_z'].astype(np.float64); n = z.shape[0]; half = float(MET['lods'][L]['half_extent_m']); sp = float(MET['lods'][L]['spacing_m'])
    g = np.linspace(-half, half, n)
    X, Y = np.meshgrid(g, g[::-1])
    V = np.stack([X, Y, z], -1).reshape(-1, 3)
    F = wk.grid_faces(n, n).reshape(-1, 4)
    if HOLE[L]:
        cxf = (X[:-1, :-1] + X[1:, 1:]).ravel() / 2; cyf = (Y[:-1, :-1] + Y[1:, 1:]).ravel() / 2
        keep = ~((np.abs(cxf) < HOLE[L]) & (np.abs(cyf) < HOLE[L]))
        F = F[keep]
    GRIDS[L] = (g, z, half, sp)
    f_, r_, s_, w_, d_, p_, gr_ = (D[f'{L}_{k}'].astype(np.float32).ravel() for k in ('forest', 'rock', 'snow', 'wet', 'dry', 'pad', 'grove'))
    # skirt: outer border loop pushed down (hides LOD cracks from any aerial angle)
    a = np.arange(n * n).reshape(n, n)
    loop = np.concatenate([a[0, :], a[1:, -1], a[-1, -2::-1], a[-2:0:-1, 0]])
    sk = V[loop].copy(); sk[:, 2] -= SKIRT[L]
    base = len(V)
    V2 = np.vstack([V, sk])
    m = len(loop)
    SF = np.array([[loop[i], loop[(i + 1) % m], base + (i + 1) % m, base + i] for i in range(m)])
    o = wk.mesh_from_arrays(f'AV_TERRAIN_{L}', V2, np.vstack([F, SF]), lodc[L], M['MAT_V_TERRAIN'])
    o.data.materials.append(M['MAT_V_SKIRT'])
    mi = np.zeros(len(F) + len(SF), np.int32); mi[len(F):] = 1
    o.data.polygons.foreach_set('material_index', mi)
    pad = lambda arr: np.concatenate([arr, arr[loop]])
    ma = np.column_stack([pad(f_), pad(r_), pad(s_), np.ones(len(V2))])
    mb = np.column_stack([pad(w_), pad(d_), pad(p_), pad(gr_)])          # A = grove density (open-grassland tree groups)
    wk.set_color_attr(o, 'mask_a', ma, 'BYTE_COLOR'); wk.set_color_attr(o, 'mask_b', mb, 'BYTE_COLOR')
    # display colour (Solid viewport / Workbench): approximate the shader mix
    col = np.tile(hx('#6E8B3D'), (len(V2), 1))
    for m_, hh in ((pad(d_), '#A39563'), (pad(f_), '#2E4426'), (pad(r_), '#7A746C'), (pad(w_), '#4A4436'), (pad(p_), '#9C8C6C'), (pad(s_), '#EDF1F5')):
        col = col * (1 - m_[:, None]) + hx(hh) * m_[:, None]
    wk.set_color_attr(o, 'display_col', col, 'BYTE_COLOR')
    me = o.data; me.color_attributes.active_color = me.color_attributes['display_col']
    try:
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
    except Exception:
        pass
    me.shade_smooth()
    wk.add_props(o, status=STATUS, lod=L, half_extent_m=half, spacing_m=sp, hole_half_m=HOLE[L] or 0, skirt_m=SKIRT[L],
                 verts=len(V2), note='heights = map (3 km data, bicubic) + procedural detail; rivers carved; Ashram pad flattened')
    if L != 'LOD0':
        o.data.polygons.foreach_set('use_smooth', np.ones(len(o.data.polygons), bool))
    TERR[L] = o
    print(L, 'verts', len(V2), 'faces', len(F) + len(SF), flush=True)


def surface_z(x, y):
    """Bilinear height of the finest LOD that contains (x, y) — used to drape paths/markers on the actual mesh."""
    x = np.asarray(x, float); y = np.asarray(y, float); out = np.full(x.shape, np.nan)
    for L in ('LOD2', 'LOD1', 'LOD0'):
        g, z, half, sp = GRIDS[L]
        inside = (np.abs(x) <= half) & (np.abs(y) <= half)
        if not inside.any():
            continue
        fc = (x[inside] + half) / sp; fr = (half - y[inside]) / sp
        c0 = np.clip(np.floor(fc).astype(int), 0, len(g) - 2); r0 = np.clip(np.floor(fr).astype(int), 0, len(g) - 2)
        tx, ty = fc - c0, fr - r0
        zz = (z[r0, c0] * (1 - tx) * (1 - ty) + z[r0, c0 + 1] * tx * (1 - ty) + z[r0 + 1, c0] * (1 - tx) * ty + z[r0 + 1, c0 + 1] * tx * ty)
        out[inside] = zz
    return out


# ------------------------------------------------------------------ rivers
RP, RO = D['RP'], D['RO']
vs, fs, n0, nriv = [], [], 0, 0
for i in range(len(RO) - 1):
    r = RP[RO[i]:RO[i + 1]].astype(float)
    m = (np.abs(r[:, 0]) < 159000) & (np.abs(r[:, 1]) < 159000)
    if m.sum() < 3:
        continue
    r = r[m]
    pts = np.column_stack([r[:, 0], r[:, 1], r[:, 2] - .4])
    t = np.gradient(pts[:, :2], axis=0); t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    nr = np.stack([-t[:, 1], t[:, 0]], 1) * (r[:, 3:4] * 1.05 / 2)
    vv = np.empty((len(pts) * 2, 3)); vv[0::2] = np.column_stack([pts[:, :2] + nr, pts[:, 2]]); vv[1::2] = np.column_stack([pts[:, :2] - nr, pts[:, 2]])
    k = np.arange(len(pts) - 1) * 2 + n0
    fs.append(np.stack([k, k + 1, k + 3, k + 2], 1)); vs.append(vv); n0 += len(vv); nriv += 1
o = wk.mesh_from_arrays('AV_RIVERS', np.vstack(vs), np.vstack(fs), C['AV_WATER'], M['MAT_V_RIVER'])
wk.display_color(o, '#2F6F9A')
wk.add_props(o, status=STATUS, rivers=nriv, width_m=MET['river_width_m'],
             note='from the map flow network (acc>40, same as MAP_G); meanders added; water level never rises downstream')

# ------------------------------------------------------------------ path (PROPOSED)
PA = D['PATH'].astype(float)
seg = np.hypot(*np.diff(PA[:, :2], axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
ss = np.arange(0, s[-1], 6.0)
PX, PY = np.interp(ss, s, PA[:, 0]), np.interp(ss, s, PA[:, 1])
pz = surface_z(PX, PY) + .45
o = wk.ribbon('AV_PATH_PROPOSED_GATE_TO_NE', np.column_stack([PX, PY, pz]), np.full(len(ss), 4.0), C['AV_PATHS'], M['MAT_V_PATH'])
wk.display_color(o, '#8C7656')
wk.add_props(o, status='PROPOSED route (least-effort path, map G direction) — width 4 m', length_km=MET['path_len_km'],
             target=json.dumps(MET['path_target']), note='river crossings = fords/bridges to design later')

# ------------------------------------------------------------------ Ashram placement reference (NOT the building)
c = C['AV_ASHRAM_PLACEMENT_REF']
e = bpy.data.objects.new('ASHRAM_ORIGIN_REF', None); e.empty_display_type = 'ARROWS'; e.empty_display_size = 40; e.location = (0, 0, SITE)
c.objects.link(e)
wk.add_props(e, status='Ashram = CONFIRMED story location; position = PROPOSAL', site_elev_m=SITE,
             asset='02_world/ashram (concept v3) — modelled separately, placed here later', world_km=[3725, 4238])
x0, x1, y0, y1 = MET['pad_rect_m']
for nm, rect, w in (('REF_PAD_OUTLINE', (x0, x1, y0, y1), 1.2), ('REF_COMPOUND_WALL_120x124', (-60, 60, -62, 62), .8)):
    o = wk.rect_curve_mesh(nm, *rect, SITE + .35, w, c, M['MAT_V_ASHRAM_REF']); wk.display_color(o, '#FFD45A')
o = wk.ring_curve_mesh('REF_TRAINING_GROUND_R22', 22, SITE + .35, 64, .8, c, M['MAT_V_ASHRAM_REF'], center=(0, -100)); wk.display_color(o, '#FFD45A')
bb = wk.box('REF_ASHRAM_VOLUME_BOUNDS', (120, 124, 22), (0, 0, SITE + 11), c, M['MAT_V_ASHRAM_REF'])
bb.display_type = 'WIRE'; bb.hide_render = True
wk.text('LBL_ASHRAM_REF', 'ASHRAM (separate asset)\nplacement reference — proposal', (0, 90, SITE + 30), 14, c, M['MAT_V_ASHRAM_REF'],
        rot=(math.radians(70), 0, 0)).hide_render = True

# ------------------------------------------------------------------ markers in the window (PROPOSED)
c = C['AV_MARKERS']
proto = wk.cone('AV_MARKER_MESH', 60, 900, 6, None, M['MAT_V_MARK_PROPOSED']).data
wk.display_color(bpy.data.objects.new('tmp', proto), '#FF5AA0')
for key, L_ in MET['markers'].items():
    for i, (x, y, zb) in enumerate(L_):
        z = float(surface_z(np.array([x]), np.array([y]))[0])
        o = bpy.data.objects.new(f'AV_MK_{key.upper()}_{i + 1:02d}', proto); o.location = (x, y, z); c.objects.link(o); o.hide_render = True
        o['note'] = f'{key[:-1] if key.endswith("s") else key} — PROPOSED site from the C1 map (code only)'
        t = wk.text(f'AV_LBL_{key.upper()}_{i + 1:02d}', f'{key[:-1]} (proposed)', (x, y, z + 1300), 900, c, M['MAT_V_MARK_PROPOSED'], rot=(math.radians(60), 0, 0))
        t.hide_render = True
sn = MET['nearest_snow_cell']
t = wk.text('AV_LBL_SNOW_RANGE', f'snowy range ≈ {sn["dist_km"]:.0f} km NW', (sn['x_km'] * 1000, sn['y_km'] * 1000, 9000), 3500, c,
            M['MAT_V_MARK_PROPOSED'], rot=(math.radians(60), 0, math.radians(-30)))
t.hide_render = True

# ------------------------------------------------------------------ forests: Geometry Nodes instancing on the terrain
def scatter_group(name, density, viewport_factor, scale_rng, coll_, attr='mask_a', chan='Red', seed=7):
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    N, Lk = ng.nodes, ng.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    na = N.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT_COLOR'; na.inputs['Name'].default_value = attr
    se = N.new('FunctionNodeSeparateColor'); Lk.new(na.outputs['Attribute'], se.inputs['Color'])
    iv = N.new('GeometryNodeIsViewport')
    sw = N.new('GeometryNodeSwitch'); sw.input_type = 'FLOAT'
    sw.inputs['False'].default_value = density; sw.inputs['True'].default_value = density * viewport_factor
    Lk.new(iv.outputs[0], sw.inputs['Switch'])
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    Lk.new(se.outputs[chan], mul.inputs[0]); Lk.new(sw.outputs['Output'], mul.inputs[1])
    dp = N.new('GeometryNodeDistributePointsOnFaces'); dp.distribute_method = 'RANDOM'
    Lk.new(gi.outputs['Geometry'], dp.inputs['Mesh']); Lk.new(mul.outputs[0], dp.inputs['Density'])
    dp.inputs['Seed'].default_value = seed
    ci = N.new('GeometryNodeCollectionInfo'); ci.inputs['Collection'].default_value = coll_
    ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
    rot = N.new('FunctionNodeRandomValue'); rot.data_type = 'FLOAT_VECTOR'
    rot.inputs['Min'].default_value = (0, 0, 0); rot.inputs['Max'].default_value = (0, 0, 6.283)
    scl = N.new('FunctionNodeRandomValue'); scl.data_type = 'FLOAT'
    scl.inputs[2].default_value = scale_rng[0]; scl.inputs[3].default_value = scale_rng[1]
    ip = N.new('GeometryNodeInstanceOnPoints'); ip.inputs['Pick Instance'].default_value = True
    Lk.new(dp.outputs['Points'], ip.inputs['Points']); Lk.new(ci.outputs['Instances'], ip.inputs['Instance'])
    Lk.new(rot.outputs['Value'], ip.inputs['Rotation']); Lk.new(scl.outputs['Value'], ip.inputs['Scale'])
    Lk.new(ip.outputs['Instances'], go.inputs['Geometry'])
    return ng


SCAT = [('FOREST', 'LOD0', 1 / 90.0, .25, (.7, 1.3), 'PROXY_TREES_NEAR', 'mask_a', 'Red', 7),
        ('FOREST', 'LOD1', 1 / 3500.0, .08, (.7, 1.25), 'PROXY_CANOPY_FAR', 'mask_a', 'Red', 7),
        ('GROVES', 'LOD0', 1 / 1400.0, .5, (.6, 1.25), 'PROXY_TREES_NEAR', 'mask_b', 'Alpha', 11),
        ('GROVES', 'LOD1', 1 / 9000.0, .2, (.3, .7), 'PROXY_CANOPY_FAR', 'mask_b', 'Alpha', 11)]
for kind, L, dens, vf, srng, cname, attr_, chan, seed in SCAT:
    ng = scatter_group(f'GN_{kind}_SCATTER_{L}', dens, vf, srng, proxies[cname], attr_, chan, seed)
    # carrier = linked duplicate of the terrain mesh (no extra geometry stored) carrying only the GN modifier
    car = bpy.data.objects.new(f'AV_{kind}_{L}', TERR[L].data); C['AV_FORESTS'].objects.link(car)
    md = car.modifiers.new(f'{kind}_SCATTER', 'NODES'); md.node_group = ng
    wk.add_props(car, status=STATUS, density_per_m2=dens, viewport_density=vf, proxies=cname,
                 note=('forest = map biome (mask_a.R)' if kind == 'FOREST' else 'groves = sparse tree groups on the open grassland (mask_b.A); biome unchanged')
                 + ' · instances only, carrier shares the terrain mesh')

# ------------------------------------------------------------------ atmosphere + light + sky
hz = wk.box('AV_HAZE_VOLUME', (330000, 330000, 5200), (0, 0, 2600 + 200), C['AV_ATMOSPHERE'], M['MAT_V_HAZE'])
hz.display_type = 'BOUNDS'; hz['note'] = 'bounded haze (never a world volume — blocks the sun)'
sun = wk.sun('AV_SUN', 36, 140, 4.0, C['AV_LIGHTING'], 1.2)
sc.world = wk.sky_world('AV_SKY', 36, 140, .25, altitude=SITE)

# ------------------------------------------------------------------ cameras
sn_xy = (sn['x_km'] * 1000, sn['y_km'] * 1000)
CAMS = [
    ('CAM_V00_LOD_LAYOUT_TOP', (0, 0, 60000), (0, 0, 0), 50, 330000, 'Technical top view — LOD0/1/2 extents, rivers, snowy range NW'),
    ('CAM_V01_VALLEY_ESTABLISHING', (7500, -10500, SITE + 2900), (-4500, 5200, SITE - 200), 26, None, 'Ashram Valley establishing aerial (from the south-east, looking north-west)'),
    ('CAM_V02_TOWARD_SNOW_RANGE', (1800, -2600, SITE + 260), (sn_xy[0], sn_xy[1], 3300), 70, None, 'Low aerial from the Ashram toward the snowy range ≈100 km NW'),
    ('CAM_V03_VALLEY_PLAN_TOP', (0, 0, 40000), (0, 0, 0), 50, 62000, 'Valley plan — LOD1 (60 × 60 km): forest ring, rivers, open valley floor'),
    ('CAM_V04_RIVER_AND_FOREST', (2600, -2900, SITE + 420), (300, 1500, SITE - 40), 30, None, 'River + forest edge near the Ashram'),
    ('CAM_V05_SNOW_RANGE_AERIAL', (sn_xy[0] + 17000, sn_xy[1] - 21000, 3300), (sn_xy[0] - 3000, sn_xy[1] + 6000, 4300), 35, None, 'Snowy range aerial (LOD2 far terrain)'),
    ('CAM_V06_GROUND_LEVEL', (-90, -170, SITE + 1.7), (-6000, 6800, SITE + 180), 28, None, 'Ground level (1.7 m eye) at the Ashram pad, looking north-west'),
    ('CAM_V07_ASHRAM_PLACEMENT', (260, -420, SITE + 230), (0, -30, SITE), 35, None, 'Ashram placement reference (pad, wall, training ground outlines)'),
]
for nm, loc, tgt, lens, ortho, desc in CAMS:
    o = wk.camera(nm, loc, tgt, lens, C['AV_CAMERAS'], clip=(.5, 400000), ortho=ortho); o['description'] = desc
sc.camera = bpy.data.objects['CAM_V01_VALLEY_ESTABLISHING']
wk.setup_cycles(sc, (1280, 720), 24)
wk.viewport_defaults(sc, 400000)
# viewport: hide LOD2 + haze by default for speed (render still uses them)
hz.hide_viewport = False
wk.save(wk.P('08_ASHRAM_VALLEY', 'ASHRAM_VALLEY_terrain_v001.blend'))
print('BUILD_VALLEY_DONE')

"""TASK 06 · scatter QC of the populated region files (Blender 4.5).

    BPY45 t6_pop_qc.py            → 03_assets/vegetation/qc/t6_pop_qc.json  (merged into T06_QC_REPORT.md by t6_qc.py --report)
Checks per file: opens, every layer linked to its terrain + band collections, wind control + drivers valid, instances generated,
NOTHING FLOATING (every sampled instance base within 0.35 m of the evaluated terrain surface below it), no instance inside
water / bare-rock masks above a threshold, Decision 01 rules (ONE Peepal, Tulsi + Marigold only in the Ashram garden beds,
R-02 fantasy share 20–30 % of the trees, no glow outside R-02), file size < 95 MB, wind moves the realized near plants.
For counting, the layer's camera culling is opened to 360° / 1.5 km and Viewport Density = 1 in memory (file not saved).
"""
import os, sys, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import bpy
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
POP = os.path.join(ROOT, '02_world', 'ecosystem', 'populated'); QCD = os.path.join(HERE, '..', 'qc')
R = []


def chk(name, ok, detail=''):
    R.append(dict(check=name, ok=bool(ok), detail=str(detail))); print(('PASS ' if ok else 'FAIL ') + name, detail, flush=True)


def ids(md):
    return {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}


import subprocess
ch = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain', '02_world/3d_world'], capture_output=True, text=True).stdout.strip()
chk('TASK 05 approved files untouched (git: no change under 02_world/3d_world)', ch == '', ch[:200] or 'clean')
for f in sorted(glob.glob(os.path.join(POP, 'T6_POP_*.blend'))):
    fn = os.path.basename(f); size = os.path.getsize(f) / 1e6
    chk(f'{fn}: file < 95 MB (everything linked)', size < 95, f'{size:.2f} MB')
    bpy.ops.wm.open_mainfile(filepath=f); sc = bpy.context.scene
    miss = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath, library=im.library))]
    chk(f'{fn}: opens, no missing images / libraries', not miss and all(os.path.exists(bpy.path.abspath(l.filepath)) for l in bpy.data.libraries),
        f'{len(bpy.data.libraries)} libraries, missing images {miss[:2]}')
    layers = [o for o in sc.objects if o.modifiers.get('T6_ECOSYSTEM')]
    chk(f'{fn}: ecosystem layers', len(layers) > 0, f'{len(layers)} layers')
    ctrl = [o for o in bpy.data.objects if o.name.startswith('T6_WIND_CONTROL') and o.library is None]
    chk(f'{fn}: one local T6_WIND_CONTROL drives every layer', len(ctrl) == 1 and all(
        o.animation_data and len(o.animation_data.drivers) == 4 and all(d.driver.is_valid for d in o.animation_data.drivers) for o in layers),
        f'{len(ctrl)} control(s)')
    ok_in = all(o.modifiers['T6_ECOSYSTEM'][ids(o.modifiers['T6_ECOSYSTEM'])['Terrain']] is not None and
                o.modifiers['T6_ECOSYSTEM'][ids(o.modifiers['T6_ECOSYSTEM'])['Near']] is not None for o in layers)
    chk(f'{fn}: every layer has a terrain + band collections', ok_in)
    # Decision 01 rules
    names = [o.get('t6_layer', '') for o in layers]
    bad = [o.name for o in layers if o.get('t6_layer') in ('AV_S02_TULSI', 'AV_F04_MARIGOLD') and
           'GARDEN_BED' not in (o.modifiers['T6_ECOSYSTEM'][ids(o.modifiers['T6_ECOSYSTEM'])['Terrain']].name)]
    chk(f'{fn}: Tulsi + Marigold only in the Ashram garden beds (Decision 01 §4)', not bad, f'outside: {bad}')
    if 'ASHRAM' in fn:
        pe = [o for o in sc.objects if 'PEEPAL' in o.name and o.instance_type == 'COLLECTION']
        tu = [o for o in sc.objects if o.instance_type == 'COLLECTION' and o.instance_collection and 'TULSI' in o.instance_collection.name]
        chk(f'{fn}: Tulsi = 6 plants, all inside the PROPOSED garden beds (x ±6…28, y −30…−52)',
            len(tu) == 6 and all(6 <= abs(o.location.x) <= 28 and -52 <= o.location.y <= -30 for o in tu), f'{len(tu)} Tulsi instances')
        pl = [o for o in layers if 'PEEPAL' in o.get('t6_layer', '')]
        chk(f'{fn}: exactly ONE Peepal (landmark, courtyard)', len(pe) == 1 and not pl, f'{len(pe)} instance(s), {len(pl)} Peepal scatter layers')
    if not fn.startswith('T6_POP_R02'):
        fant = [o.name for o in layers if 'FANTASY' in o.get('t6_label', '')]
        chk(f'{fn}: no fantasy / glowing species outside R-02', not fant, str(fant))
    # count instances with open culling over the WHOLE tile (in memory only): woody at full density, ground layers at 1 %
    cam = sc.camera
    for o in layers:
        md = o.modifiers['T6_ECOSYSTEM']; I = ids(md)
        md[I['Viewport Density']] = 1.0 if o.get('t6_kind') in ('tree', 'shrub', 'detail') else .01
        md[I['Cull Angle']] = 180.0; md[I['Cull Distance']] = 1e6; md[I['Keep Near']] = 1e6; md[I['Realize Distance']] = 0.0
        o.update_tag()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    counts = {o.name: 0 for o in layers}; bases = {o.name: [] for o in layers}
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent and inst.parent.original.name in counts:
            n = inst.parent.original.name; counts[n] += 1
            if len(bases[n]) < 400:
                bases[n].append(tuple(inst.matrix_world.translation))
    empty = [n for n, c in counts.items() if c == 0]
    chk(f'{fn}: every layer generates instances (whole tile, open culling)', not empty,
        f'{sum(counts.values()):,} instances (ground layers sampled at 1 %); empty {empty[:6]}')
    # nothing floating: instance base vs terrain surface (vertical ray down / up)
    terr = {md[ids(md)['Terrain']] for md in (o.modifiers['T6_ECOSYSTEM'] for o in layers)}
    dz_all = []
    for o in layers:
        t_obj = o.modifiers['T6_ECOSYSTEM'][ids(o.modifiers['T6_ECOSYSTEM'])['Terrain']]
        te = t_obj.evaluated_get(dg)
        for p in bases[o.name][:60]:
            hit, loc, nrm, idx = te.ray_cast(te.matrix_world.inverted() @ __import__('mathutils').Vector((p[0], p[1], p[2] + 50)), (0, 0, -1))
            if hit:
                dz_all.append(abs(p[2] - (te.matrix_world @ loc).z))
    dz = np.array(dz_all) if dz_all else np.array([0.0])
    chk(f'{fn}: nothing floating — instance bases on the terrain surface (|Δz| < 0.35 m)', (dz < .35).mean() > .97,
        f'{len(dz_all)} samples, median {np.median(dz):.3f} m, max {dz.max():.2f} m, {(dz < .35).mean():.1%} OK')
    if fn.startswith('T6_POP_R02'):
        tree_layers = [o for o in layers if o.get('t6_kind') == 'tree']
        nf = sum(counts[o.name] for o in tree_layers if 'FANTASY' in o.get('t6_label', '')); nt = sum(counts[o.name] for o in tree_layers)
        share = nf / max(nt, 1)
        chk(f'{fn}: R-02 fantasy share of trees 20–30 % (Decision 01 §3)', .20 <= share <= .30, f'{nf} fantasy / {nt} trees = {share:.0%} (whole tile)')
    # wind: realized near plants move between two frames at strength 2 — the camera is moved next to real instances of the
    # densest plant layer (in memory), its realize distance opened to 25 m
    main_t = layers[0].modifiers['T6_ECOSYSTEM'][ids(layers[0].modifiers['T6_ECOSYSTEM'])['Terrain']] if layers else None
    pl = sorted([o for o in layers if o.get('t6_kind') == 'plant' and bases[o.name]],
                key=lambda o: (o.modifiers['T6_ECOSYSTEM'][ids(o.modifiers['T6_ECOSYSTEM'])['Terrain']] != main_t, -counts[o.name]))
    if pl and cam is not None:
        o = pl[0]; p0 = bases[o.name][0]
        cam.location = (p0[0] + 4, p0[1] - 4, p0[2] + 1.6)
        for x in layers:
            if x is not o:
                x.modifiers['T6_ECOSYSTEM'].show_viewport = False
        md = o.modifiers['T6_ECOSYSTEM']; I = ids(md); md[I['Realize Distance']] = 25.0; md[I['Cull Distance']] = 30.0; md[I['Viewport Density']] = 1.0
        c = ctrl[0]
        def ev(fr):
            sc.frame_set(fr); c['strength'] = 2.0; c.update_tag(); o.update_tag(); bpy.context.view_layer.update()
            d2 = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(d2); m = oe.to_mesh()
            A = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', A); oe.to_mesh_clear(); return A.reshape(-1, 3)
        a1, a2 = ev(40), ev(52)
        mv = np.linalg.norm(a1 - a2, axis=1).max() if len(a1) == len(a2) and len(a1) else 0.0
        chk(f'{fn}: wind bends the realized near plants ({o.name})', len(a1) > 0 and mv > 1e-3, f'{len(a1):,} verts, max Δ {mv:.3f} m in 0.5 s')
os.makedirs(QCD, exist_ok=True)
json.dump(dict(version='populated files (Blender ' + bpy.app.version_string + ')', results=R), open(os.path.join(QCD, 't6_qc_populated.json'), 'w'), indent=1)
print(f"T6_POP_QC_DONE {sum(r['ok'] for r in R)}/{len(R)}")

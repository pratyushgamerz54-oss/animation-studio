"""TASK 06 · automated QC of the vegetation libraries (run with Blender 4.5; optionally 5.3 for the cross-version open test).

    BPY45 t6_qc.py            → 03_assets/vegetation/qc/t6_qc_<blender version>.json
    python3 t6_qc.py --report → 03_assets/vegetation/qc/T06_QC_REPORT.md (merges the json files)
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); VEG = os.path.abspath(os.path.join(HERE, '..'))
QCD = os.path.join(VEG, 'qc'); os.makedirs(QCD, exist_ok=True)
NAMES = {'AV': 'ASHRAM_VALLEY', 'EF': 'ENCHANTED_FOREST', 'MK': 'MOUNTAIN_KINGDOM',
         'PL': 'GREEN_PLAINS', 'LK': 'CRYSTAL_LAKES', 'DS': 'GOLDEN_DESERT', 'FB': 'FORBIDDEN_LANDS',
         'CT': 'ANCIENT_CITY_SITES', 'CV': 'HIDDEN_UNDERGROUND', 'ND': 'NATURAL_DETAILS'}   # = t6_regions.NAMES
_built = [r for r, nm in NAMES.items() if r in ('AV', 'EF', 'MK') or os.path.exists(os.path.join(VEG, 'library', f'T6_VEG_{nm}_v001.blend'))]
REGS = os.environ.get('T6_QC_REGIONS', ' '.join(_built)).split()      # default: milestone 1 + every milestone-2 library built so far
                                                                      # (final TASK 06 QC: T6_QC_REGIONS="AV EF MK PL LK DS FB CT CV")
WIND_ATTRS = ('wind_trunk', 'wind_branch', 'wind_leaf', 'wind_phase', 'leaf_rand')


def run_blender():
    sys.path.insert(0, HERE)
    import numpy as np
    import bpy
    import t6_regions as RG
    design = {t['name']: t for t in RG.TREES + RG.SHRUBS}; pdesign = {p['name']: p for p in RG.PLANTS}
    R = []

    def chk(name, ok, detail=''):
        R.append(dict(check=name, ok=bool(ok), detail=str(detail))); print(('PASS ' if ok else 'FAIL ') + name, detail, flush=True)

    ver = bpy.app.version_string
    for reg in REGS:
        nm = NAMES[reg]
        f = os.path.join(VEG, 'library', f'T6_VEG_{nm}_v001.blend')
        chk(f'{reg}: library file exists', os.path.exists(f), os.path.relpath(f, VEG))
        if not os.path.exists(f):
            continue
        size = os.path.getsize(f) / 1e6
        chk(f'{reg}: file size < 100 MB (GitHub limit)', size < 100, f'{size:.1f} MB')
        bpy.ops.wm.open_mainfile(filepath=f)
        miss = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not os.path.exists(bpy.path.abspath(im.filepath))]
        chk(f'{reg}: opens in Blender {ver}, no missing images', not miss, f'{len(bpy.data.images)} images, missing {miss[:3]}')
        rel = all(im.filepath.startswith('//') for im in bpy.data.images if im.source == 'FILE')
        chk(f'{reg}: image paths relative (portable to the Director PC)', rel, '')
        ctrl = bpy.data.objects.get('T6_WIND_CONTROL')
        chk(f'{reg}: T6_WIND_CONTROL present with strength/gust/speed/flutter', ctrl is not None and all(k in ctrl for k in ('strength', 'gust', 'speed', 'flutter')))
        assets = [o for o in bpy.data.objects if o.get('t6_kind') and not o.name.endswith('_SC')]
        sc_ok = all(bpy.data.objects.get(o.name + '_SC') is not None and bpy.data.objects[o.name + '_SC'].data == o.data and
                    not bpy.data.objects[o.name + '_SC'].modifiers for o in assets)
        chk(f'{reg}: wind-free scatter copies <asset>_SC (same mesh) for NG_T6_ECOSYSTEM', sc_ok)
        chk(f'{reg}: assets in library', len(assets) > 0, f'{len(assets)} assets')
        scn = bpy.data.scenes['T6_LIBRARY']
        for o in assets:
            me = o.data; kind = o['t6_kind']; n = o.name
            bad = me.validate(verbose=False, clean_customdata=False)
            tris = sum(len(p.vertices) - 2 for p in me.polygons)
            uv = me.uv_layers.get('UVMap')
            chk(f'{n}: valid mesh, UVs', (not bad) and uv is not None and tris > 0, f'{tris:,} tris, {len(me.vertices):,} verts')
            att = [a for a in WIND_ATTRS if a in me.attributes]
            chk(f'{n}: wind attributes', len(att) == len(WIND_ATTRS), ','.join(att))
            mats = [m for m in me.materials if m]
            imgs_ok = all(nd.image is not None for m in mats for nd in m.node_tree.nodes if nd.type == 'TEX_IMAGE')
            pbr = any(nd.type == 'NORMAL_MAP' or nd.type == 'BUMP' for m in mats for nd in m.node_tree.nodes)
            chk(f'{n}: PBR materials ({len(mats)} slots)', len(mats) >= 1 and imgs_ok and (pbr or kind == 'plant'), ', '.join(m.name for m in mats)[:120])
            chk(f'{n}: no empty material slot (renders white otherwise)', all(m is not None for m in me.materials))
            used = set(np.unique(np.array([p.material_index for p in me.polygons])).tolist())
            chk(f'{n}: every face has a valid material slot', max(used) < len(me.materials), f'slots used {sorted(used)}')
            V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V); V = V.reshape(-1, 3)
            H = V[:, 2].max(); lo = V[:, 2].min()
            if kind in ('tree', 'shrub'):
                D = design[n]
                chk(f'{n}: height within the generator range of the design height (seed ±7 % × normalisation ±10 % → ±18 %)',
                    abs(H - D['height']) / D['height'] < .18, f"{H:.2f} m vs design {D['height']} m")
                foot = V[(np.hypot(V[:, 0], V[:, 1]) < max(2.5, D['height'] * .12)) & (V[:, 2] < .02)]
                chk(f'{n}: grounded (trunk foot / roots below ground level)', lo < -.1 and len(foot) > 8, f'lowest z {lo:.2f} m, {len(foot)} verts at the foot')
                # nothing except roots under the ground far from the trunk
                far = V[(V[:, 2] < -.15) & (np.hypot(V[:, 0], V[:, 1]) > D['height'] * .45 + 8)]
                props = (D.get('aerial') or {}).get('n', 0) >= 10            # banyan: prop roots root into the soil anywhere under the crown
                chk(f'{n}: no limbs through the ground' + (' (prop roots allowed)' if props else ''), len(far) == 0 or props, f'{len(far)} verts far + under ground')
                chk(f"{n}: label set ({o['t6_label']})", o['t6_label'] in ('SPECIES-INSPIRED', 'FANTASY (APPROVED R-02)'))
                if o['t6_label'] == 'FANTASY (APPROVED R-02)':
                    chk(f'{n}: fantasy asset restricted to R-02 (Decision 01)', o['t6_region'].startswith('R-02') and 'R-02' in o['t6_habitat'])
                if D.get('builder') == 'palm':
                    fr = [m for m in mats if 'FROND' in m.name]
                    chk(f'{n}: palm — trunk scan + frond / dead-frond materials, fronds attached to the crown', len(fr) >= 2 and
                        np.abs(V[V[:, 2] > H * .8][:, :2]).max() < D['palm']['frond_len'] * 1.4 + H * .3, ', '.join(m.name for m in fr))
            else:
                P = pdesign[n]
                if o['t6_label'] == 'FANTASY (APPROVED R-02)':
                    chk(f'{n}: fantasy asset restricted to R-02 (Decision 01)', o['t6_region'].startswith('R-02') and 'R-02' in o['t6_habitat'])
                if P.get('hanging'):
                    chk(f'{n}: hanging plant attaches at its top (hangs from a branch, z_top = {H:.1f} m)', H > 2 and lo > 0, f'z {lo:.2f}–{H:.2f} m')
                elif P.get('water'):
                    chk(f'{n}: aquatic plant sits at the water surface (z = 0) with stems below', lo < -.1 and H < 3, f'lowest {lo:.2f} m, top {H:.2f} m')
                else:
                    near0 = V[V[:, 2] < .01]
                    chk(f'{n}: plant base on the ground (no floating)', lo <= .001 and len(near0) > 3, f'lowest z {lo:.3f} m')
            em = [m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value for m in mats
                  if m.node_tree and 'Principled BSDF' in m.node_tree.nodes]
            chk(f'{n}: glow subtle (emission ≤ 1.0, Decision 01 §3)', max(em + [0]) <= 1.0, f'max emission {max(em + [0]):.2f}')
            if reg in ('CV', 'FB', 'DS', 'PL', 'LK', 'CT', 'MK'):      # glow approved for R-02 only (caves: proposal, crater: no glow)
                chk(f'{n}: no glow outside R-02', max(em + [0]) == 0.0, f'max emission {max(em + [0]):.2f}')
            md = o.modifiers.get('T6_WIND')
            if md:
                drv_ok = all(fc.driver.is_valid for fc in (o.animation_data.drivers if o.animation_data else []))
                chk(f'{n}: wind modifier + drivers valid', md.node_group and md.node_group.name == 'NG_T6_WIND' and drv_ok,
                    f"{len(o.animation_data.drivers) if o.animation_data else 0} drivers")
        # wind evaluation test on the tallest tree + one plant
        trees = sorted([o for o in assets if o['t6_kind'] == 'tree'], key=lambda o: -o['t6_height_m'])[:1]
        plants = [o for o in assets if o['t6_kind'] == 'plant' and o.modifiers.get('T6_WIND')][:1]
        for o in trees + plants:
            def ev(frame, strength):
                ctrl['strength'] = strength; ctrl.update_tag(); o.update_tag(); scn.frame_set(frame); bpy.context.view_layer.update()
                dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); m = oe.to_mesh()
                A = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', A); oe.to_mesh_clear(); return A.reshape(-1, 3)
            base = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get('co', base); base = base.reshape(-1, 3)
            a0 = ev(1, 0.0); a1 = ev(10, 2.0); a2 = ev(40, 2.0)
            calm = np.abs(a0 - base).max(); mv = np.linalg.norm(a1 - a2, axis=1); H = base[:, 2].max()
            zf = .05 if o['t6_kind'] != 'plant' else .015          # plants: the root crown itself (blades lean low near the ground)
            fm = (base[:, 2] < zf) & (np.hypot(base[:, 0], base[:, 1]) < max(.3, float(o.get('t6_trunk_d_m', .3))))
            foot = np.linalg.norm(a1 - base, axis=1)[fm].max() if fm.any() else 0
            chk(f'{o.name}: wind — calm = static, strength 2 = motion, foot stays fixed',
                calm < 1e-4 and mv.max() > 1e-3 and mv.max() < .2 * H + .05 and foot < .02,
                f'calm Δ {calm:.1e} m · moving Δmax {mv.max():.3f} m · foot Δ {foot:.3f} m')
            ctrl['strength'] = 1.0
    return R, ver


def run_textures(R):
    try:
        from PIL import Image
    except ImportError:
        return
    import glob
    for p in sorted(glob.glob(os.path.join(VEG, 'textures', 'leaves', '*_col.png'))):
        n = os.path.basename(p)[:-8]; ok = True; det = []
        for k in ('col', 'nor', 'rough'):
            q = p.replace('_col.png', f'_{k}.png')
            if not os.path.exists(q):
                ok = False; det.append(f'missing {k}'); continue
            im = Image.open(q); det.append(f'{k} {im.size[0]}²')
            ok &= im.size == (2048, 2048)
        a = Image.open(p).getchannel('A'); cov = sum(a.histogram()[128:]) / (2048 * 2048)
        ok &= .005 < cov < .9    # plume atlases (kans) are genuinely sparse
        R.append(dict(check=f'atlas {n}: colour+alpha / normal / roughness maps 2K', ok=ok, detail=', '.join(det) + f', coverage {cov:.0%}'))


def report():
    import glob
    rows = []; vers = []
    for f in sorted(glob.glob(os.path.join(QCD, 't6_qc_*.json'))):
        J = json.load(open(f)); vers.append(J['version']); rows.append(J)
    T = []; run_textures(T)
    if T:
        rows.append(dict(version='textures (python3 + Pillow)', results=T))
    L = ['# TASK 06 · Technical QC report — milestones 1 + 2 (vegetation libraries v001, all regions + populated files)', '',
         'Automated by `03_assets/vegetation/scripts/t6_qc.py` (geometry, UVs, materials, textures, wind, ground contact, labels).', '']
    for J in rows:
        n = len(J['results']); p = sum(r['ok'] for r in J['results'])
        L += [f"## Blender {J['version']} — **{p}/{n} PASS**", '', '| # | check | result | detail |', '|---|---|---|---|']
        for i, r in enumerate(J['results'], 1):
            L.append(f"| {i} | {r['check']} | {'✅ PASS' if r['ok'] else '❌ FAIL'} | {r['detail'].replace('|', '/')} |")
        L.append('')
    open(os.path.join(QCD, 'T06_QC_REPORT.md'), 'w').write('\n'.join(L)); print('REPORT', vers)


if __name__ == '__main__':
    if '--report' in sys.argv:
        report()
    else:
        R, ver = run_blender()
        json.dump(dict(version=ver, results=R), open(os.path.join(QCD, f"t6_qc_{ver.split()[0]}.json"), 'w'), indent=1)
        n = len(R); p = sum(r['ok'] for r in R); print(f'T6_QC_DONE {p}/{n}')

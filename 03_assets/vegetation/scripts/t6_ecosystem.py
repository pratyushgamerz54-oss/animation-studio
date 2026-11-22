"""TASK 06 · NG_T6_ECOSYSTEM — the vegetation scatter system (Blender 4.5 geometry nodes).

One scatter object = one LAYER (one species: hero + variants). Built on the approved TASK 05 scatter logic (NG_T5_SCATTER:
terrain mask attributes, slope, altitude, clustering, camera-cone culling, stable points in animation) and adds:
  • 4 distance bands  Near (LOD0 hero + variants V1/V2) · Mid (LOD1) · Far (LOD2) · Horizon (LOD3 impostor cards)
  • Poisson spacing   'Min Distance' > 0 (trees never intersect; real canopy spacing); 0 = random (dense ground layers)
  • WIND (Director 22 Nov: "kuch bhi move kare real world jaisa"):
      – instances closer than 'Realize Distance' are REALIZED and bent per vertex by NG_T6_WIND (root stiff → tip flexible,
        arc bend, gust advection, inertia lag) with a per-instance random phase added to wind_phase → no two plants in sync;
      – all other instances tilt about their base with NG_T6_WIND_INSTANCES (same advected gust field, natural frequency,
        per-instance phase) → forests ripple as gusts travel across them.
    Strength / Gust / Speed / Flutter are driven from the scene's T6_WIND_CONTROL (one control for every layer).
  • exclusion: two avoid masks (paths, water, bare rock, buildings) + 'Exclude Object' (any mesh volume, e.g. courtyard / road;
    points inside its bounding radius are removed) and an altitude band.
Instances use the library's *_SC objects (same mesh as the hero asset, WITHOUT the per-object wind modifier → the wind is
applied here once, per instance, never twice).
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '02_world', '3d_world', 'scripts')))
import bpy
import t6kit as K
from t5kit import NB, new_tree, sock_new

NAME = 'NG_T6_ECOSYSTEM'


def ecosystem_group():
    if NAME in bpy.data.node_groups and bpy.data.node_groups[NAME].get('t6_eco_version') == 3:
        return bpy.data.node_groups[NAME]
    ng = new_tree(NAME, 'GeometryNodeTree'); ng['t6_eco_version'] = 3
    sock_new(ng, 'Geometry', 'OUTPUT', 'NodeSocketGeometry'); sock_new(ng, 'Geometry', 'INPUT', 'NodeSocketGeometry')
    sock_new(ng, 'Terrain', 'INPUT', 'NodeSocketObject')
    for k in ('Near', 'Mid', 'Far', 'Horizon'):
        sock_new(ng, k, 'INPUT', 'NodeSocketCollection')
    F = lambda n, d, a=None, b=None: sock_new(ng, n, 'INPUT', 'NodeSocketFloat', d, a, b)
    F('Density', .01, 0, 1000); F('Viewport Density', .1, 0, 1); F('Min Distance', 0.0, 0, 100)
    sock_new(ng, 'Mask', 'INPUT', 'NodeSocketString'); F('Mask Min', .3, 0, 1); F('Mask Max', .7, 0, 1)
    sock_new(ng, 'Avoid Mask', 'INPUT', 'NodeSocketString'); F('Avoid Strength', 1.0, 0, 1)
    sock_new(ng, 'Avoid Mask 2', 'INPUT', 'NodeSocketString'); F('Avoid Strength 2', 1.0, 0, 1)
    sock_new(ng, 'Exclude Object', 'INPUT', 'NodeSocketObject'); F('Exclude Radius', 0.0, 0, 1e5); F('Keep Only Inside', 0.0, 0, 1)
    F('Slope Min', 0.0, 0, 90); F('Slope Max', 35.0, 0, 90); F('Altitude Min', -1e5); F('Altitude Max', 1e5)
    F('Cluster Scale', 40.0, .01, 1e5); F('Cluster Amount', .5, 0, 1)
    F('Scale Min', .85, 0, 100); F('Scale Max', 1.15, 0, 100); F('Align To Normal', 0.0, 0, 1); F('Random Tilt', 0.0, 0, 90)
    F('Sink', 0.0, -10, 10); sock_new(ng, 'Seed', 'INPUT', 'NodeSocketInt', 0)
    F('Cull Distance', 3000.0, 0, 1e6); F('Cull Angle', 60.0, 0, 180); F('Keep Near', 40.0, 0, 1e5)
    F('LOD0→1', 60.0, 0, 1e6); F('LOD1→2', 250.0, 0, 1e6); F('LOD2→3', 1200.0, 0, 1e6)
    # wind
    sock_new(ng, 'Wind Control', 'INPUT', 'NodeSocketObject')
    F('Strength', 1.0, 0, 20); F('Gust', .5, 0, 5); F('Speed', 1.0, 0, 10); F('Flutter', 1.0, 0, 10)
    F('Realize Distance', 0.0, 0, 1e4)
    F('Trunk Sway (m)', .1, 0, 10); F('Branch Sway (m)', .3, 0, 5); F('Leaf Flutter (m)', .03, 0, 1)
    F('Natural Freq (Hz)', .5, .02, 10); F('Damping', .15, 0, 1); F('Gust Size (m)', 45.0, 1, 1000); F('Bend Offset (m)', .5, .005, 10)
    F('Plant Height (m)', 10.0, .01, 200); F('Instance Sway (m)', .3, 0, 20)
    b = NB(ng); gi = b.node('NodeGroupInput'); go = b.node('NodeGroupOutput')
    G = lambda k: b.out(gi, k)
    oi = b.node('GeometryNodeObjectInfo', transform_space='RELATIVE'); b.link(G('Terrain'), oi.inputs['Object'])
    terr = b.out(oi, 'Geometry')

    def named(name_sock):
        na = b.node('GeometryNodeInputNamedAttribute', data_type='FLOAT'); b.link(name_sock, na.inputs['Name'])
        return b.out(na, 'Attribute', typ='VALUE')
    mask = b.maprange(named(G('Mask')), G('Mask Min'), G('Mask Max'))
    av1 = b.math('SUBTRACT', 1.0, b.math('MULTIPLY', named(G('Avoid Mask')), G('Avoid Strength')), clamp=True)
    av2 = b.math('SUBTRACT', 1.0, b.math('MULTIPLY', named(G('Avoid Mask 2')), G('Avoid Strength 2')), clamp=True)
    nrm = b.node('GeometryNodeInputNormal'); nz = b.node('ShaderNodeSeparateXYZ'); b.link(nrm.outputs[0], nz.inputs[0])
    slope = b.math('DEGREES', b.math('ARCCOSINE', nz.outputs['Z']))
    sl_ok = b.math('MULTIPLY', b.math('GREATER_THAN', slope, G('Slope Min')), b.math('LESS_THAN', slope, G('Slope Max')))
    pos = b.node('GeometryNodeInputPosition'); pz = b.node('ShaderNodeSeparateXYZ'); b.link(pos.outputs[0], pz.inputs[0])
    al_ok = b.math('MULTIPLY', b.math('GREATER_THAN', pz.outputs['Z'], G('Altitude Min')), b.math('LESS_THAN', pz.outputs['Z'], G('Altitude Max')))
    nt = b.node('ShaderNodeTexNoise'); nt.inputs['Detail'].default_value = 3
    b.link(b.math('DIVIDE', 1.0, G('Cluster Scale')), nt.inputs['Scale']); b.link(pos.outputs[0], nt.inputs['Vector'])
    clus = b.mixf(G('Cluster Amount'), 1.0, b.maprange(nt.outputs['Fac'], .45, .62))
    # exclusion object: horizontal distance to its origin > radius
    eo = b.node('GeometryNodeObjectInfo', transform_space='ORIGINAL'); b.link(G('Exclude Object'), eo.inputs['Object'])
    exy = b.vmath('MULTIPLY', b.vmath('SUBTRACT', pos.outputs[0], b.out(eo, 'Location')), (1, 1, 0))
    ex_ok = b.math('ABSOLUTE', b.math('SUBTRACT', b.math('GREATER_THAN', b.vmath('LENGTH', exy), G('Exclude Radius')), G('Keep Only Inside')))
    # camera culling
    ac = b.node('GeometryNodeInputActiveCamera')
    co = b.node('GeometryNodeObjectInfo', transform_space='ORIGINAL'); b.link(ac.outputs[0], co.inputs['Object'])
    rel = b.vmath('SUBTRACT', pos.outputs[0], b.out(co, 'Location')); dist = b.vmath('LENGTH', rel)
    rot = b.node('ShaderNodeVectorRotate', rotation_type='EULER_XYZ'); rot.inputs['Vector'].default_value = (0, 0, -1)
    b.link(b.out(co, 'Rotation'), rot.inputs['Rotation'])
    cosang = b.vmath('DOT_PRODUCT', b.vmath('NORMALIZE', rel), rot.outputs['Vector'])
    in_cone = b.math('GREATER_THAN', cosang, b.math('COSINE', b.math('RADIANS', G('Cull Angle'))))
    keep = b.math('MAXIMUM', in_cone, b.math('LESS_THAN', dist, G('Keep Near')))
    keep = b.math('MULTIPLY', keep, b.math('LESS_THAN', dist, G('Cull Distance')))
    isv = b.node('GeometryNodeIsViewport')
    dsw = b.node('GeometryNodeSwitch', input_type='FLOAT'); b.link(isv.outputs[0], b.sock(dsw, 'Switch'))
    b.link(G('Density'), b.sock(dsw, 'False', typ='VALUE'))
    b.link(b.math('MULTIPLY', G('Density'), G('Viewport Density')), b.sock(dsw, 'True', typ='VALUE'))
    dens = b.out(dsw, 'Output')
    for f in (mask, av1, av2, sl_ok, al_ok, clus, keep, ex_ok):
        dens = b.math('MULTIPLY', dens, f)
    # Min Distance > 0 → Poisson disk (trees / shrubs never intersect); 0 → random (dense ground layers: only the culled,
    # masked faces produce points — a Poisson pass over a whole 2–9 km² tile would create tens of millions of candidates)
    branches = []
    for method in ('RANDOM', 'POISSON'):
        dp = b.node('GeometryNodeDistributePointsOnFaces', distribute_method=method)
        b.link(terr, dp.inputs['Mesh']); b.link(G('Seed'), dp.inputs['Seed'])
        if method == 'RANDOM':
            b.link(dens, dp.inputs['Density'])
        else:
            b.link(G('Min Distance'), dp.inputs['Distance Min']); b.link(G('Density'), dp.inputs['Density Max'])
            b.link(b.math('DIVIDE', dens, b.math('MAXIMUM', G('Density'), 1e-9)), dp.inputs['Density Factor'])
        st = b.node('GeometryNodeStoreNamedAttribute', data_type='FLOAT_VECTOR', domain='POINT'); st.inputs['Name'].default_value = 'eco_nrm'
        b.link(dp.outputs['Points'], st.inputs['Geometry']); b.link(dp.outputs['Normal'], b.sock(st, 'Value', typ='VECTOR'))
        branches.append(st.outputs[0])
    swd = b.node('GeometryNodeSwitch', input_type='GEOMETRY'); b.link(b.math('GREATER_THAN', G('Min Distance'), 0.0), b.sock(swd, 'Switch'))
    b.link(branches[0], b.sock(swd, 'False')); b.link(branches[1], b.sock(swd, 'True'))
    pts = b.out(swd, 'Output')
    nrm_na = b.node('GeometryNodeInputNamedAttribute', data_type='FLOAT_VECTOR'); nrm_na.inputs['Name'].default_value = 'eco_nrm'
    pt_normal = b.out(nrm_na, 'Attribute', typ='VECTOR')
    # rotation: random yaw + tilt, optional surface alignment
    yaw = b.node('FunctionNodeRandomValue', data_type='FLOAT'); b.sock(yaw, 'Max', typ='VALUE').default_value = 6.2832
    b.link(G('Seed'), b.sock(yaw, 'Seed', typ='INT'))
    tilt = b.node('FunctionNodeRandomValue', data_type='FLOAT_VECTOR'); tr = b.math('RADIANS', G('Random Tilt'))
    tmin = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', tr, -1), tmin.inputs['X']); b.link(b.math('MULTIPLY', tr, -1), tmin.inputs['Y'])
    tmax = b.node('ShaderNodeCombineXYZ'); b.link(tr, tmax.inputs['X']); b.link(tr, tmax.inputs['Y'])
    b.link(tmin.outputs[0], b.sock(tilt, 'Min', typ='VECTOR')); b.link(tmax.outputs[0], b.sock(tilt, 'Max', typ='VECTOR'))
    eul = b.node('ShaderNodeCombineXYZ'); tsep = b.node('ShaderNodeSeparateXYZ'); b.link(b.out(tilt, 'Value', typ='VECTOR'), tsep.inputs[0])
    b.link(tsep.outputs['X'], eul.inputs['X']); b.link(tsep.outputs['Y'], eul.inputs['Y']); b.link(b.out(yaw, 'Value', typ='VALUE'), eul.inputs['Z'])
    upz = b.node('ShaderNodeCombineXYZ'); upz.inputs['Z'].default_value = 1.0
    up = b.mixv(G('Align To Normal'), upz.outputs[0], pt_normal)
    al = b.node('FunctionNodeAlignRotationToVector', axis='Z')
    b.link(eul.outputs[0], b.sock(al, 'Rotation')); b.link(up, b.sock(al, 'Vector')); rot_out = b.out(al, 'Rotation')
    sc = b.node('FunctionNodeRandomValue', data_type='FLOAT'); b.link(G('Scale Min'), b.sock(sc, 'Min', typ='VALUE'))
    b.link(G('Scale Max'), b.sock(sc, 'Max', typ='VALUE')); b.link(b.math('ADD', G('Seed'), 7), b.sock(sc, 'Seed', typ='INT'))
    scale = b.out(sc, 'Value', typ='VALUE')
    sp_ = b.node('GeometryNodeSetPosition'); b.link(pts, sp_.inputs['Geometry'])
    so = b.node('ShaderNodeCombineXYZ'); b.link(b.math('MULTIPLY', b.math('MULTIPLY', G('Sink'), scale), -1), so.inputs['Z'])
    b.link(so.outputs[0], sp_.inputs['Offset']); pts = sp_.outputs['Geometry']
    # distance bands
    pos3 = b.node('GeometryNodeInputPosition')
    d3 = b.vmath('LENGTH', b.vmath('SUBTRACT', pos3.outputs[0], b.out(co, 'Location')))
    joins = b.node('GeometryNodeJoinGeometry')
    ri = b.node('FunctionNodeRandomValue', data_type='INT'); b.sock(ri, 'Min', typ='INT').default_value = 0
    b.sock(ri, 'Max', typ='INT').default_value = 999; b.link(b.math('ADD', G('Seed'), 3), b.sock(ri, 'Seed', typ='INT'))
    bands = (('Near', None, G('LOD0→1')), ('Mid', G('LOD0→1'), G('LOD1→2')), ('Far', G('LOD1→2'), G('LOD2→3')), ('Horizon', G('LOD2→3'), None))
    wi_nodes = []
    for k, lo, hi in bands:
        selv = None
        if lo is not None:
            selv = b.math('GREATER_THAN', d3, lo)
        if hi is not None:
            t = b.math('LESS_THAN', d3, hi); selv = t if selv is None else b.math('MULTIPLY', selv, t)
        ci = b.node('GeometryNodeCollectionInfo', transform_space='ORIGINAL'); b.link(G(k), ci.inputs['Collection'])
        ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
        ip = b.node('GeometryNodeInstanceOnPoints')
        b.link(pts, ip.inputs['Points']); b.link(ci.outputs[0], ip.inputs['Instance']); b.link(selv, ip.inputs['Selection'])
        ip.inputs['Pick Instance'].default_value = True; b.link(b.out(ri, 'Value', typ='INT'), ip.inputs['Instance Index'])
        b.link(rot_out, ip.inputs['Rotation']); b.link(scale, ip.inputs['Scale'])
        inst = ip.outputs[0]
        if k == 'Near':
            # split: realized (per-vertex wind) inside the Realize Distance, instance tilt beyond it
            pi_ = b.node('GeometryNodeInputPosition'); dd = b.vmath('LENGTH', b.vmath('SUBTRACT', pi_.outputs[0], b.out(co, 'Location')))
            sep = b.node('GeometryNodeSeparateGeometry', domain='INSTANCE'); b.link(inst, sep.inputs['Geometry'])
            b.link(b.math('LESS_THAN', dd, G('Realize Distance')), sep.inputs['Selection'])
            # per-instance phase: random by instance id → stored on the instance, realized onto its vertices, added to wind_phase
            rnd = b.node('FunctionNodeRandomValue', data_type='FLOAT'); b.link(b.math('ADD', G('Seed'), 11), b.sock(rnd, 'Seed', typ='INT'))
            st = b.node('GeometryNodeStoreNamedAttribute', data_type='FLOAT', domain='INSTANCE'); st.inputs['Name'].default_value = 't6_inst_rand'
            b.link(sep.outputs['Selection'], st.inputs['Geometry']); b.link(b.out(rnd, 'Value', typ='VALUE'), b.sock(st, 'Value', typ='VALUE'))
            rl = b.node('GeometryNodeRealizeInstances'); b.link(st.outputs[0], rl.inputs['Geometry'])
            ph = b.math('FRACT', b.math('ADD', named_const(b, 'wind_phase'), named_const(b, 't6_inst_rand')))
            st2 = b.node('GeometryNodeStoreNamedAttribute', data_type='FLOAT', domain='POINT'); st2.inputs['Name'].default_value = 'wind_phase'
            b.link(rl.outputs[0], st2.inputs['Geometry']); b.link(ph, b.sock(st2, 'Value', typ='VALUE'))
            wg = b.node('GeometryNodeGroup'); wg.node_tree = K.wind_group(); b.link(st2.outputs[0], wg.inputs['Geometry'])
            for s_ in ('Wind Control', 'Strength', 'Gust', 'Speed', 'Flutter', 'Trunk Sway (m)', 'Branch Sway (m)', 'Leaf Flutter (m)',
                       'Natural Freq (Hz)', 'Damping', 'Gust Size (m)', 'Bend Offset (m)'):
                b.link(G(s_), wg.inputs[s_])
            b.link(wg.outputs[0], joins.inputs[0])
            inst = sep.outputs['Inverted']
        wi = b.node('GeometryNodeGroup'); wi.node_tree = K.wind_instances_group(); b.link(inst, wi.inputs['Instances'])
        for s_ in ('Wind Control', 'Strength', 'Gust', 'Speed', 'Natural Freq (Hz)', 'Gust Size (m)', 'Plant Height (m)'):
            b.link(G(s_), wi.inputs[s_])
        b.link(G('Instance Sway (m)'), wi.inputs['Sway (m)'])
        b.link(wi.outputs[0], joins.inputs[0])
    b.link(joins.outputs[0], go.inputs['Geometry'])
    return ng


def named_const(b, name):
    na = b.node('GeometryNodeInputNamedAttribute', data_type='FLOAT'); na.inputs['Name'].default_value = name
    return b.out(na, 'Attribute', typ='VALUE')


def set_inputs(md, **kw):
    ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
    for k, v in kw.items():
        md[ids[k.replace('_', ' ') if k.replace('_', ' ') in ids else k]] = v
    return md


def drive_wind(o, md, ctrl):
    """Strength / Gust / Speed / Flutter of an ecosystem layer follow T6_WIND_CONTROL (single-property drivers)."""
    ids = {it.name: it.identifier for it in md.node_group.interface.items_tree if getattr(it, 'in_out', '') == 'INPUT'}
    md[ids['Wind Control']] = ctrl
    for sock, prop in (('Strength', 'strength'), ('Gust', 'gust'), ('Speed', 'speed'), ('Flutter', 'flutter')):
        fc = o.driver_add(f'modifiers["{md.name}"]["{ids[sock]}"]'); dr = fc.driver; dr.type = 'AVERAGE'
        v = dr.variables.new(); v.type = 'SINGLE_PROP'; v.targets[0].id_type = 'OBJECT'; v.targets[0].id = ctrl
        v.targets[0].data_path = f'["{prop}"]'

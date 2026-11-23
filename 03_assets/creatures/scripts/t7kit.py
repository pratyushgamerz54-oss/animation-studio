"""t7kit — TASK 07 creature toolkit (Blender 4.5 LTS; also 5.x).

  part_to_object(part)   t7sdf.Part → marching cubes → Quadriflow quads → subdivide + shrinkwrap back onto the exact surface
                         → clean all-quad mesh + UVs + zone weights (z_<zone>) + coat colour + comb / fur-length attributes.
  fur(obj, ...)          NG_T7_FUR geometry-nodes groom (strands follow the comb direction, droop with gravity, taper; length
                         and density from attributes; colour from the coat) — real hair curves, rendered as Cycles curves.
  materials              skin / hoof / horn / eye / feather / scale / chitin, realism rules (rough ≥ .45 dry, specular ≈ .25–.3,
                         mottling, micro-bump); only eyes, nose and wet surfaces are glossy.
  studio + render        concept render scene (Poly Haven sky HDRI + sun, ground, AgX natural camera look).
"""
import os, sys, math
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
CR = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(CR, '..', '..'))
PH = os.path.join(ROOT, '03_assets', 'external', 'polyhaven')
sys.path.insert(0, HERE)
import t7sdf as S


def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c) + (a,)


def lin(h):
    return np.array(hexc(h)[:3], np.float32)


def clean():
    for c in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.node_groups, bpy.data.curves,
              bpy.data.cameras, bpy.data.lights, bpy.data.collections, bpy.data.images, bpy.data.worlds):
        for x in list(c):
            c.remove(x)
    bpy.context.preferences.filepaths.save_version = 0


def link(o, coll=None):
    (coll or bpy.context.scene.collection).objects.link(o)
    return o


# ==============================================================================================================================
# geometry
def _quadriflow(o, faces):
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.view_layer.objects:
        x.select_set(False)
    o.select_set(True)
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        r = bpy.ops.object.quadriflow_remesh(target_faces=int(faces), use_mesh_symmetry=False, use_preserve_sharp=False,
                                             use_preserve_boundary=False, smooth_normals=False, seed=0)
    return 'FINISHED' in r


def part_to_object(part, name, coll=None, quads=6000, subdiv=1, warp=None, mirror_x=False):
    """returns the mesh object (all quads, UV unwrapped, zone attributes)."""
    v, f = part.mesh(warp)
    me = bpy.data.meshes.new(name + '_mc')
    me.from_pydata(v.tolist(), [], f.tolist()); me.update()
    bm_ = bmesh.new(); bm_.from_mesh(me)
    bmesh.ops.remove_doubles(bm_, verts=bm_.verts, dist=part.voxel * 0.15)   # QuadriFlow rejects edges < 0.1 mm
    bmesh.ops.dissolve_degenerate(bm_, dist=part.voxel * 0.15, edges=bm_.edges)
    bmesh.ops.triangulate(bm_, faces=[x for x in bm_.faces if len(x.verts) > 3])
    # drop tiny floating islands (MC noise)
    seen = set(); islands = []
    for v0 in bm_.verts:
        if v0 in seen:
            continue
        st = [v0]; isl = []; seen.add(v0)
        while st:
            x = st.pop(); isl.append(x)
            for e in x.link_edges:
                y = e.other_vert(x)
                if y not in seen:
                    seen.add(y); st.append(y)
        islands.append(isl)
    islands.sort(key=len, reverse=True)
    for isl in islands[1:]:
        if len(isl) < 0.02 * len(islands[0]):
            bmesh.ops.delete(bm_, geom=isl, context='VERTS')
    nm = [e for e in bm_.edges if not e.is_manifold]
    if nm:
        bmesh.ops.delete(bm_, geom=list({x for e in nm for x in e.link_faces}), context='FACES')
        bmesh.ops.holes_fill(bm_, edges=[e for e in bm_.edges if e.is_boundary], sides=0)
        bmesh.ops.triangulate(bm_, faces=[x for x in bm_.faces if len(x.verts) > 3])
    bmesh.ops.recalc_face_normals(bm_, faces=bm_.faces)
    bm_.to_mesh(me); bm_.free(); me.update()
    v = np.array([x.co[:] for x in me.vertices], np.float32); f = np.array([[*x.vertices] for x in me.polygons], np.int32)
    hi = bpy.data.objects.new(name + '_mc', me); link(hi, coll)
    bvh = BVHTree.FromPolygons([tuple(x) for x in v], [tuple(x) for x in f])
    lo = hi.copy(); lo.data = me.copy(); lo.name = name; lo.data.name = name; link(lo, coll)
    ok = _quadriflow(lo, quads)
    if not ok or len(lo.data.polygons) < quads * 0.3:
        print('  quadriflow failed → decimate fallback', name)
        m = lo.modifiers.new('dec', 'DECIMATE'); m.ratio = min(1, quads * 2 / max(len(f), 1))
        _apply(lo, m)
    if subdiv:
        m = lo.modifiers.new('sub', 'SUBSURF'); m.levels = subdiv; m.render_levels = subdiv; m.quality = 3
        _apply(lo, m)
    # snap back onto the exact SDF surface (keeps the quad flow, restores detail: nostrils, eyelids, hooves)
    for vv in lo.data.vertices:
        hit = bvh.find_nearest(vv.co)
        if hit[0] is not None:
            vv.co = hit[0]
    # light relax pass (removes MC stair noise without losing shape) + re-snap
    m = lo.modifiers.new('relax', 'SMOOTH'); m.factor = 0.4; m.iterations = 2; _apply(lo, m)
    for vv in lo.data.vertices:
        hit = bvh.find_nearest(vv.co)
        if hit[0] is not None:
            vv.co = vv.co.lerp(hit[0], 0.7)
    bpy.data.objects.remove(hi); bpy.data.meshes.remove(me)
    for p in lo.data.polygons:
        p.use_smooth = True
    uv_unwrap(lo)
    # zone weights
    P = np.array([vv.co[:] for vv in lo.data.vertices], np.float32)
    W, D = part.zones(P)
    for z, w in W.items():
        a = lo.data.attributes.new('z_' + z, 'FLOAT', 'POINT'); a.data.foreach_set('value', w.astype(np.float32))
    lo['t7_part'] = part.name
    return lo, P, W, D


def _apply(o, m):
    with bpy.context.temp_override(object=o, active_object=o):
        bpy.ops.object.modifier_apply(modifier=m.name)


def uv_unwrap(o):
    """angle-based seams + Smart UV Project (concept); production files get hand-placed seams (milestone 2)."""
    bpy.context.view_layer.objects.active = o
    with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.004, area_weight=1.0, scale_to_bounds=False)
        bpy.ops.object.mode_set(mode='OBJECT')


def set_attr(o, name, arr, typ='FLOAT', domain='POINT'):
    a = o.data.attributes.get(name) or o.data.attributes.new(name, typ, domain)
    arr = np.asarray(arr, np.float32)
    if typ == 'FLOAT':
        a.data.foreach_set('value', arr.ravel())
    elif typ == 'FLOAT_VECTOR':
        a.data.foreach_set('vector', arr.ravel())
    else:
        a.data.foreach_set('color', arr.ravel())
    return a


def normals(o):
    n = np.zeros(len(o.data.vertices) * 3, np.float32); o.data.vertices.foreach_get('normal', n)
    return n.reshape(-1, 3)


def comb_field(P, N, rules, W):
    """rules: zone → direction (world) ; blended by zone weight, projected onto the tangent plane."""
    C = np.zeros_like(P)
    for z, w in W.items():
        d = np.asarray(rules.get(z, rules.get('*', (-1, 0, -0.3))), np.float32)
        if callable(rules.get(z)):
            d = rules[z](P)
        C += w[:, None] * (d if d.ndim == 2 else d[None, :])
    C -= (C * N).sum(1, keepdims=True) * N
    n = np.linalg.norm(C, axis=1, keepdims=True)
    fallback = np.cross(N, np.array([0, 1, 0], np.float32))
    C = np.where(n > 1e-4, C / np.maximum(n, 1e-6), fallback)
    return C


# ==============================================================================================================================
# fur (geometry nodes)
def _node(nt, typ, loc, **kw):
    n = nt.nodes.new(typ); n.location = loc
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def fur_group():
    if 'NG_T7_FUR' in bpy.data.node_groups:
        return bpy.data.node_groups['NG_T7_FUR']
    ng = bpy.data.node_groups.new('NG_T7_FUR', 'GeometryNodeTree')
    it = ng.interface
    it.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    for nm, d, lo, hi in (('Density', 40000.0, 0, 1e7), ('Length', 1.0, 0, 10), ('Radius', 0.00012, 0, 0.01),
                          ('Lift', 0.35, 0, 3), ('Droop', 0.25, 0, 3), ('Frizz', 0.15, 0, 2), ('Seed', 0.0, 0, 1000)):
        s = it.new_socket(nm, in_out='INPUT', socket_type='NodeSocketFloat'); s.default_value = d; s.min_value = lo; s.max_value = hi
    s = it.new_socket('Material', in_out='INPUT', socket_type='NodeSocketMaterial')
    it.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes; L = ng.links
    gi = _node(ng, 'NodeGroupInput', (-1400, 0)); go = _node(ng, 'NodeGroupOutput', (1400, 0))
    fd = _node(ng, 'GeometryNodeInputNamedAttribute', (-1200, -250), data_type='FLOAT'); fd.inputs['Name'].default_value = 'fur_density'
    dist = _node(ng, 'GeometryNodeDistributePointsOnFaces', (-950, 0), distribute_method='RANDOM')
    dmul = _node(ng, 'ShaderNodeMath', (-1100, -150), operation='MULTIPLY')    # Random mode: density is a field
    L.new(gi.outputs['Density'], dmul.inputs[0]); L.new(fd.outputs['Attribute'], dmul.inputs[1])
    L.new(gi.outputs['Geometry'], dist.inputs['Mesh']); L.new(dmul.outputs[0], dist.inputs['Density'])
    # strand: 5-point line along +Z
    line = _node(ng, 'GeometryNodeCurvePrimitiveLine', (-950, 300)); line.inputs['End'].default_value = (0, 0, 1)
    res = _node(ng, 'GeometryNodeResampleCurve', (-750, 300)); res.inputs['Count'].default_value = 5
    L.new(line.outputs['Curve'], res.inputs['Curve'])
    # direction = normalize(comb + normal * lift)
    comb = _node(ng, 'GeometryNodeInputNamedAttribute', (-1200, -600), data_type='FLOAT_VECTOR'); comb.inputs['Name'].default_value = 'comb'
    vm = _node(ng, 'ShaderNodeVectorMath', (-950, -600), operation='SCALE')
    L.new(dist.outputs['Normal'], vm.inputs[0]); L.new(gi.outputs['Lift'], vm.inputs['Scale'])
    add = _node(ng, 'ShaderNodeVectorMath', (-780, -600), operation='ADD')
    L.new(comb.outputs['Attribute'], add.inputs[0]); L.new(vm.outputs[0], add.inputs[1])
    # capture comb + length + colour on the points (point domain)
    flen = _node(ng, 'GeometryNodeInputNamedAttribute', (-1200, -800), data_type='FLOAT'); flen.inputs['Name'].default_value = 'fur_len'
    mul = _node(ng, 'ShaderNodeMath', (-950, -800), operation='MULTIPLY')
    L.new(flen.outputs['Attribute'], mul.inputs[0]); L.new(gi.outputs['Length'], mul.inputs[1])
    rnd = _node(ng, 'FunctionNodeRandomValue', (-950, -950)); rnd.inputs['Min'].default_value = 0.7; rnd.inputs['Max'].default_value = 1.15
    mul2 = _node(ng, 'ShaderNodeMath', (-780, -850), operation='MULTIPLY')
    L.new(mul.outputs[0], mul2.inputs[0]); L.new(rnd.outputs['Value'], mul2.inputs[1])
    align = _node(ng, 'FunctionNodeAlignRotationToVector', (-600, -500), axis='Z')
    L.new(add.outputs[0], align.inputs['Vector'])
    inst = _node(ng, 'GeometryNodeInstanceOnPoints', (-400, 0))
    L.new(dist.outputs['Points'], inst.inputs['Points']); L.new(res.outputs['Curve'], inst.inputs['Instance'])
    L.new(align.outputs['Rotation'], inst.inputs['Rotation'])
    comb3 = _node(ng, 'ShaderNodeCombineXYZ', (-600, -800))
    for i in range(3):
        L.new(mul2.outputs[0], comb3.inputs[i])
    L.new(comb3.outputs[0], inst.inputs['Scale'])
    real = _node(ng, 'GeometryNodeRealizeInstances', (-200, 0)); L.new(inst.outputs['Instances'], real.inputs['Geometry'])
    # droop (gravity ∝ t²) + frizz noise, both scaled by strand length
    sp = _node(ng, 'GeometryNodeSplineParameter', (-200, -300))
    sq = _node(ng, 'ShaderNodeMath', (0, -300), operation='POWER'); sq.inputs[1].default_value = 2.0
    L.new(sp.outputs['Factor'], sq.inputs[0])
    clen = _node(ng, 'GeometryNodeSplineLength', (-200, -450))
    dm = _node(ng, 'ShaderNodeMath', (0, -450), operation='MULTIPLY'); L.new(sq.outputs[0], dm.inputs[0]); L.new(clen.outputs['Length'], dm.inputs[1])
    dm2 = _node(ng, 'ShaderNodeMath', (150, -450), operation='MULTIPLY'); L.new(dm.outputs[0], dm2.inputs[0]); L.new(gi.outputs['Droop'], dm2.inputs[1])
    dvec = _node(ng, 'ShaderNodeCombineXYZ', (300, -450)); L.new(dm2.outputs[0], dvec.inputs['Z'])
    neg = _node(ng, 'ShaderNodeVectorMath', (450, -450), operation='SCALE'); neg.inputs['Scale'].default_value = -1.0
    L.new(dvec.outputs[0], neg.inputs[0])
    pos = _node(ng, 'GeometryNodeInputPosition', (0, -650))
    noi = _node(ng, 'ShaderNodeTexNoise', (150, -650)); noi.inputs['Scale'].default_value = 180.0
    L.new(pos.outputs[0], noi.inputs['Vector'])
    nsub = _node(ng, 'ShaderNodeVectorMath', (300, -650), operation='SUBTRACT'); nsub.inputs[1].default_value = (.5, .5, .5)
    L.new(noi.outputs['Color'], nsub.inputs[0])
    nsc = _node(ng, 'ShaderNodeVectorMath', (450, -650), operation='SCALE'); L.new(nsub.outputs[0], nsc.inputs[0])
    fz = _node(ng, 'ShaderNodeMath', (300, -800), operation='MULTIPLY'); L.new(dm.outputs[0], fz.inputs[0]); L.new(gi.outputs['Frizz'], fz.inputs[1])
    L.new(fz.outputs[0], nsc.inputs['Scale'])
    off = _node(ng, 'ShaderNodeVectorMath', (600, -500), operation='ADD'); L.new(neg.outputs[0], off.inputs[0]); L.new(nsc.outputs[0], off.inputs[1])
    setp = _node(ng, 'GeometryNodeSetPosition', (650, 0)); L.new(real.outputs['Geometry'], setp.inputs['Geometry']); L.new(off.outputs[0], setp.inputs['Offset'])
    # taper radius
    inv = _node(ng, 'ShaderNodeMath', (450, 250), operation='SUBTRACT'); inv.inputs[0].default_value = 1.0
    L.new(sp.outputs['Factor'], inv.inputs[1])
    rad = _node(ng, 'ShaderNodeMath', (600, 250), operation='MULTIPLY'); L.new(inv.outputs[0], rad.inputs[0]); L.new(gi.outputs['Radius'], rad.inputs[1])
    rad2 = _node(ng, 'ShaderNodeMath', (750, 250), operation='MAXIMUM'); rad2.inputs[1].default_value = 0.00002
    L.new(rad.outputs[0], rad2.inputs[0])
    setr = _node(ng, 'GeometryNodeSetCurveRadius', (850, 0)); L.new(setp.outputs['Geometry'], setr.inputs['Curve']); L.new(rad2.outputs[0], setr.inputs['Radius'])
    setm = _node(ng, 'GeometryNodeSetMaterial', (1050, 0)); L.new(setr.outputs['Curve'], setm.inputs['Geometry']); L.new(gi.outputs['Material'], setm.inputs['Material'])
    join = _node(ng, 'GeometryNodeJoinGeometry', (1250, 0))
    L.new(gi.outputs['Geometry'], join.inputs[0]); L.new(setm.outputs['Geometry'], join.inputs[0])
    L.new(join.outputs[0], go.inputs[0])
    return ng


def fur(o, mat, density=40000, length=1.0, radius=0.00012, lift=0.35, droop=0.25, frizz=0.15):
    m = o.modifiers.new('T7_FUR', 'NODES'); m.node_group = fur_group()
    ids = {s.name: s.identifier for s in m.node_group.interface.items_tree if getattr(s, 'in_out', '') == 'INPUT'}
    for k, v in (('Density', density), ('Length', length), ('Radius', radius), ('Lift', lift), ('Droop', droop),
                 ('Frizz', frizz), ('Material', mat)):
        m[ids[k]] = v
    return m


# ==============================================================================================================================
# materials
def new_mat(name):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m


def _bsdf(m):
    return m.node_tree.nodes['Principled BSDF']


def _attr(nt, name, loc=(-700, 300)):
    a = nt.nodes.new('ShaderNodeAttribute'); a.attribute_name = name; a.location = loc
    return a


def mat_skin(name, coat_attr='coat', rough=0.62, spec=0.28, sss=0.06, bump=0.25, gloss_attr=None):
    """skin / fur base: colour from the coat attribute + fine mottling + micro bump; gloss_attr (0..1) = wet nose / eyelid."""
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    a = _attr(nt, coat_attr)
    noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 60; noi.inputs['Detail'].default_value = 6; noi.location = (-900, 0)
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'; mix.inputs[0].default_value = 0.12; mix.location = (-450, 250)
    L.new(a.outputs['Color'], mix.inputs[1]); L.new(noi.outputs['Color'], mix.inputs[2])
    L.new(mix.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Subsurface Weight'].default_value = sss; b.inputs['Subsurface Radius'].default_value = (0.02, 0.008, 0.005)
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; bm.inputs['Distance'].default_value = 0.002; bm.location = (-300, -200)
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 400; n2.location = (-600, -250)
    L.new(n2.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    if gloss_attr:
        g = _attr(nt, gloss_attr, (-700, -500))
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (-450, -500)
        mr.inputs['To Min'].default_value = rough; mr.inputs['To Max'].default_value = 0.22
        L.new(g.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs[0], b.inputs['Roughness'])
    return m


def mat_hair(name, coat_attr='coat', rough=0.42, coat_var=0.12):
    """Principled Hair (Chiang) with the strand colour taken from the coat; tip lightening + random variation."""
    m = new_mat(name); nt = m.node_tree; L = nt.links
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    h = nt.nodes.new('ShaderNodeBsdfHairPrincipled'); h.location = (0, 300)
    try:
        h.parametrization = 'COLOR'
    except Exception:
        pass
    a = _attr(nt, coat_attr, (-900, 300))
    hi = nt.nodes.new('ShaderNodeHairInfo'); hi.location = (-900, 0)
    # tip slightly lighter (sun-bleached), base darker (real guard hairs)
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (-700, 0); mr.inputs['To Min'].default_value = 0.75; mr.inputs['To Max'].default_value = 1.18
    L.new(hi.outputs['Intercept'], mr.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeVectorMath'); mul.operation = 'SCALE'; mul.location = (-500, 250)
    L.new(a.outputs['Vector'], mul.inputs[0]); L.new(mr.outputs[0], mul.inputs['Scale'])
    rv = nt.nodes.new('ShaderNodeMapRange'); rv.location = (-700, -200); rv.inputs['To Min'].default_value = 1 - coat_var; rv.inputs['To Max'].default_value = 1 + coat_var
    L.new(hi.outputs['Random'], rv.inputs['Value'])
    mul2 = nt.nodes.new('ShaderNodeVectorMath'); mul2.operation = 'SCALE'; mul2.location = (-300, 250)
    L.new(mul.outputs[0], mul2.inputs[0]); L.new(rv.outputs[0], mul2.inputs['Scale'])
    L.new(mul2.outputs[0], h.inputs['Color'])
    h.inputs['Roughness'].default_value = rough
    h.inputs['Radial Roughness'].default_value = 0.6
    h.inputs['Coat'].default_value = 0.1
    L.new(h.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    return m


def mat_simple(name, col, rough=0.55, spec=0.28, var=0.15, scale=30, bump=0.2, sss=0.0, metal=0.0, coat=0.0):
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    noi = nt.nodes.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = scale; noi.inputs['Detail'].default_value = 5; noi.location = (-800, 200)
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-550, 200)
    c = np.array(hexc(col)[:3])
    ramp.color_ramp.elements[0].color = tuple(c * (1 - var)) + (1,); ramp.color_ramp.elements[1].color = tuple(np.minimum(c * (1 + var), 1)) + (1,)
    L.new(noi.outputs['Fac'], ramp.inputs[0]); L.new(ramp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Metallic'].default_value = metal; b.inputs['Coat Weight'].default_value = coat
    b.inputs['Subsurface Weight'].default_value = sss
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; bm.inputs['Distance'].default_value = 0.002; bm.location = (-300, -200)
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = scale * 8; n2.location = (-600, -250)
    L.new(n2.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_attr(name, attr='coat', rough=0.55, spec=0.28, bump=0.25, bump_scale=300, sss=0.0, coat=0.0, rough_attr=None):
    """surface coloured by a baked attribute (feathers / scales / chitin / wings)."""
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    a = _attr(nt, attr); L.new(a.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Subsurface Weight'].default_value = sss; b.inputs['Coat Weight'].default_value = coat
    if rough_attr:
        r = _attr(nt, rough_attr, (-700, 0)); L.new(r.outputs['Fac'], b.inputs['Roughness'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; bm.inputs['Distance'].default_value = 0.001; bm.location = (-300, -200)
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = bump_scale; n2.location = (-600, -250)
    L.new(n2.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_eye(name, iris='#3A2412', pupil_r=0.45, pupil_shape='round', sclera='#1A120C', iris_r=0.78):
    """eyeball: iris / pupil from the object's local position (+X = front), glossy wet cornea coat."""
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-1100, 0)
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); sep.location = (-900, 0); L.new(tc.outputs['Object'], sep.inputs[0])
    # radial distance in the Y/Z plane (eye looks along local +X), pupil shape via Y/Z scaling
    sy, sz = {'round': (1, 1), 'horiz': (0.55, 1.6), 'vert': (1.8, 0.6)}[pupil_shape]
    cy = nt.nodes.new('ShaderNodeMath'); cy.operation = 'MULTIPLY'; cy.inputs[1].default_value = sy; cy.location = (-700, 100)
    cz = nt.nodes.new('ShaderNodeMath'); cz.operation = 'MULTIPLY'; cz.inputs[1].default_value = sz; cz.location = (-700, -100)
    L.new(sep.outputs['Y'], cy.inputs[0]); L.new(sep.outputs['Z'], cz.inputs[0])
    cmb = nt.nodes.new('ShaderNodeCombineXYZ'); cmb.location = (-550, 0); L.new(cy.outputs[0], cmb.inputs['Y']); L.new(cz.outputs[0], cmb.inputs['Z'])
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; ln.location = (-400, 0); L.new(cmb.outputs[0], ln.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-250, 0)
    e = ramp.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.004, 0.003, 0.003, 1)
    e[1].position = pupil_r * iris_r; e[1].color = (0.004, 0.003, 0.003, 1)
    e2 = e.new(pupil_r * iris_r + 0.03); e2.color = hexc(iris)
    e3 = e.new(iris_r - 0.04); e3.color = tuple(np.array(hexc(iris)[:3]) * 0.55) + (1,)
    e4 = e.new(iris_r); e4.color = hexc(sclera)
    nn = nt.nodes.new('ShaderNodeTexNoise'); nn.inputs['Scale'].default_value = 40; nn.location = (-400, -250)
    L.new(tc.outputs['Object'], nn.inputs['Vector'])
    mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'OVERLAY'; mx.inputs[0].default_value = 0.35; mx.location = (0, 0)
    L.new(ramp.outputs[0], mx.inputs[1]); L.new(nn.outputs['Color'], mx.inputs[2]); L.new(mx.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.35; b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = 0.02
    b.inputs['Specular IOR Level'].default_value = 0.5
    return m


def mat_feather(name, attr='coat', rough=0.6, scale=90.0, bump=0.35, sheen=0.25):
    """contour-feather body plumage: coat colour + overlapping feather-tip pattern (Voronoi in object space) as colour edge + bump."""
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    a = _attr(nt, attr, (-900, 300))
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-1300, -100)
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.location = (-1100, -100); vo.feature = 'F1'; vo.inputs['Scale'].default_value = scale
    vo.inputs['Randomness'].default_value = 0.9
    L.new(tc.outputs['Object'], vo.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (-850, -100); mr.inputs['From Max'].default_value = 0.6
    mr.inputs['To Min'].default_value = 1.06; mr.inputs['To Max'].default_value = 0.86
    L.new(vo.outputs['Distance'], mr.inputs['Value'])
    pl = _attr(nt, 'plume', (-1100, -400))
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'FLOAT'; mx.location = (-700, -100); mx.inputs['A'].default_value = 1.0
    L.new(pl.outputs['Fac'], mx.inputs['Factor']); L.new(mr.outputs[0], mx.inputs['B'])
    mul = nt.nodes.new('ShaderNodeVectorMath'); mul.operation = 'SCALE'; mul.location = (-600, 250)
    L.new(a.outputs['Vector'], mul.inputs[0]); L.new(mx.outputs['Result'], mul.inputs['Scale'])
    L.new(mul.outputs[0], b.inputs['Base Color'])
    bh = nt.nodes.new('ShaderNodeMath'); bh.operation = 'MULTIPLY'; bh.location = (-600, -300)
    L.new(vo.outputs['Distance'], bh.inputs[0]); L.new(pl.outputs['Fac'], bh.inputs[1])
    bm = nt.nodes.new('ShaderNodeBump'); bm.location = (-400, -250); bm.inputs['Strength'].default_value = bump; bm.inputs['Distance'].default_value = 0.0015
    L.new(bh.outputs[0], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    g = _attr(nt, 'gloss', (-700, -550)); rr = nt.nodes.new('ShaderNodeMapRange'); rr.location = (-450, -550)
    rr.inputs['To Min'].default_value = rough; rr.inputs['To Max'].default_value = 0.3
    L.new(g.outputs['Fac'], rr.inputs['Value']); L.new(rr.outputs[0], b.inputs['Roughness'])
    b.inputs['Specular IOR Level'].default_value = 0.28
    b.inputs['Sheen Weight'].default_value = sheen; b.inputs['Sheen Roughness'].default_value = 0.4
    return m


def mat_blade(name, attr='coat', rough=0.55):
    """flight / tail feather blades: colour attribute, rachis line + barb streaks along the vane, translucent edges, double-sided."""
    m = new_mat(name); nt = m.node_tree; b = _bsdf(m); L = nt.links
    a = _attr(nt, attr, (-900, 300))
    L.new(a.outputs['Color'], b.inputs['Base Color'])
    fu = _attr(nt, 'fu', (-1200, -100)); ft = _attr(nt, 'ft', (-1200, -300))
    cmb = nt.nodes.new('ShaderNodeCombineXYZ'); cmb.location = (-1000, -200)
    L.new(ft.outputs['Fac'], cmb.inputs['X']); L.new(fu.outputs['Fac'], cmb.inputs['Y'])
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.location = (-800, -200); wv.wave_type = 'BANDS'; wv.inputs['Scale'].default_value = 60
    wv.inputs['Distortion'].default_value = 2.0
    L.new(cmb.outputs[0], wv.inputs['Vector'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.location = (-400, -250); bm.inputs['Strength'].default_value = 0.25; bm.inputs['Distance'].default_value = 0.0005
    L.new(wv.outputs['Fac'], bm.inputs['Height']); L.new(bm.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Specular IOR Level'].default_value = 0.3
    b.inputs['Sheen Weight'].default_value = 0.3
    b.inputs['Transmission Weight'].default_value = 0.0
    b.inputs['Subsurface Weight'].default_value = 0.05
    return m


# ==============================================================================================================================
# colour helpers
def coat_from_zones(W, P, zone_cols, mottle=0.12, mottle_scale=6.0, seed=1):
    """zone_cols: zone → hex or callable(P)→(N,3) linear colours; soft blend by zone weights + fbm mottling (value only)."""
    C = np.zeros((len(P), 3), np.float32)
    for z, w in W.items():
        c = zone_cols.get(z, zone_cols.get('*', '#808080'))
        c = c(P) if callable(c) else lin(c)[None, :]
        C += w[:, None] * c
    if mottle:
        n = S.fbm(P, mottle_scale, 3, seed)
        C *= (1 + mottle * n)[:, None]
    return np.clip(C, 0, 1)


def grad_z(c_lo, c_hi, z0, z1):
    a, b = lin(c_lo), lin(c_hi)
    def f(P):
        t = np.clip((P[:, 2] - z0) / (z1 - z0), 0, 1)[:, None]
        return a * (1 - t) + b * t
    return f


def put_coat(o, C, name='coat'):
    a = np.concatenate([C, np.ones((len(C), 1), np.float32)], 1)
    set_attr(o, name, a, 'FLOAT_COLOR')


# ==============================================================================================================================
# extra parts
def eyeball(name, center, radius, direction, mat, coll=None):
    bm_ = bmesh.new(); bmesh.ops.create_uvsphere(bm_, u_segments=32, v_segments=16, radius=1.0)   # unit sphere, object scaled → iris maps in unit space
    me = bpy.data.meshes.new(name); bm_.to_mesh(me); bm_.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me); link(o, coll)
    d = Vector(direction).normalized()
    o.matrix_world = Matrix.Translation(center) @ d.to_track_quat('X', 'Z').to_matrix().to_4x4() @ Matrix.Scale(radius, 4)
    me.materials.append(mat)
    return o


def mesh_from(name, verts, faces, coll=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(map(float, v)) for v in verts], [], [tuple(map(int, f)) for f in faces]); me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    o = bpy.data.objects.new(name, me); link(o, coll)
    return o


# ==============================================================================================================================
# studio / render
def studio(kind='forest', ground='#5B5446', size=(1600, 1200), samples=96, hdri='kloofendal_48d_partly_cloudy_puresky', sun=(48, 0, 132),
           sun_strength=3.2, hdri_strength=0.9):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y = size; sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.cycles.max_bounces = 8; sc.cycles.transparent_max_bounces = 32
    w = bpy.data.worlds.new('T7_WORLD'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    env = nt.nodes.new('ShaderNodeTexEnvironment')
    path = os.path.join(PH, 'hdris', hdri, hdri + '_4k.exr')
    if os.path.exists(path):
        env.image = bpy.data.images.load(path, check_existing=True)
        nt.links.new(env.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = hdri_strength
    ld = bpy.data.lights.new('T7_SUN', 'SUN'); ld.energy = sun_strength; ld.angle = math.radians(2.5)
    ld.color = (1.0, 0.96, 0.9)
    so = bpy.data.objects.new('T7_SUN', ld); link(so)
    so.rotation_euler = tuple(math.radians(a) for a in sun)
    # ground: large disc, natural soil colour (matte)
    bm_ = bmesh.new(); bmesh.ops.create_circle(bm_, cap_ends=True, radius=60, segments=64)
    me = bpy.data.meshes.new('T7_GROUND'); bm_.to_mesh(me); bm_.free()
    g = bpy.data.objects.new('T7_GROUND', me); link(g)
    gm = mat_simple('T7_GROUND_MAT', ground, rough=0.85, spec=0.2, var=0.25, scale=3, bump=0.1)
    me.materials.append(gm)
    try:
        sys.path.insert(0, os.path.join(ROOT, '03_assets', 'vegetation', 'scripts'))
        from t6kit import camera_look
        camera_look(sc)
    except Exception as e:
        sc.view_settings.view_transform = 'AgX'
    return sc


def camera(name, loc, target, lens=50, ortho=None, sensor_fit='AUTO'):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.clip_start = 0.01; cd.clip_end = 500
    if ortho:
        cd.type = 'ORTHO'; cd.ortho_scale = ortho
    cd.sensor_fit = sensor_fit
    o = bpy.data.objects.new(name, cd); link(o)
    o.location = loc
    d = Vector(target) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o


def render(cam, path, samples=None):
    sc = bpy.context.scene; sc.camera = cam
    if samples:
        sc.cycles.samples = samples
    sc.render.filepath = path; sc.render.image_settings.file_format = 'PNG'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True)


def dims(objs):
    """world bounding box of evaluated meshes (no fur) → (min, max)."""
    lo = np.full(3, 1e9); hi = np.full(3, -1e9)
    for o in objs:
        if o.type != 'MESH':
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); lo = np.minimum(lo, w); hi = np.maximum(hi, w)
    return lo, hi

"""charkit — reusable procedural character-building library (Blender 5.3 bpy).

Shared by all 7 characters: materials, skin-modifier body, sculpted head,
eyes/lids/brows/mouth face kit, curve hair, clothing extraction, proxy rig,
posing and render helpers. Units: metres, Z up, character faces -Y.
"""
import bpy, bmesh, math
from mathutils import Vector, Quaternion, Matrix
from mathutils.bvhtree import BVHTree


# ---------------------------------------------------------------- basics
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def get_coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def link(ob, coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexlin(h, a=1.0):
    r, g, b = hex_rgb(h)
    return (srgb_to_lin(r / 255), srgb_to_lin(g / 255), srgb_to_lin(b / 255), a)


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def gauss(d, s):
    return math.exp(-(d * d) / (2 * s * s))


def lerp_table(x, table):
    """Smooth piecewise lookup; table = [(x0, y0), (x1, y1), ...] ascending in x."""
    if x <= table[0][0]:
        return table[0][1]
    for (a, fa), (b, fb) in zip(table, table[1:]):
        if x <= b:
            t = (x - a) / (b - a)
            t = t * t * (3 - 2 * t)
            return fa + (fb - fa) * t
    return table[-1][1]


def mesh_object(name, verts, faces, coll, edges=()):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], list(edges), [tuple(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def bake_modifiers(ob):
    """Apply all modifiers without bpy.ops (works headless)."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    me.name = old.name
    bpy.data.meshes.remove(old)
    return ob


def add_subsurf(ob, view=1, render=2):
    m = ob.modifiers.new('Subsurf', 'SUBSURF')
    m.levels, m.render_levels = view, render
    return m


# ---------------------------------------------------------------- materials
def _nodes(mat):
    if mat.node_tree is None:
        mat.use_nodes = True
    return mat.node_tree.nodes, mat.node_tree.links


def principled(name, color, rough=0.5, metal=0.0, sss=0.0, sss_radius=(1.0, 0.35, 0.2),
               coat=0.0, sheen=0.0, emit=None, emit_strength=0.0, bump=0.0, bump_scale=300.0,
               spec=0.5):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nodes, links = _nodes(mat)
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    b = nodes.new('ShaderNodeBsdfPrincipled')
    b.name = 'BSDF'
    b.inputs['Base Color'].default_value = hexlin(color) if isinstance(color, str) else color
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Subsurface Weight'].default_value = sss
    b.inputs['Subsurface Radius'].default_value = sss_radius
    b.inputs['Subsurface Scale'].default_value = 0.01
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Sheen Weight'].default_value = sheen
    b.inputs['Specular IOR Level'].default_value = spec
    if emit:
        b.inputs['Emission Color'].default_value = hexlin(emit)
        b.inputs['Emission Strength'].default_value = emit_strength
    links.new(b.outputs[0], out.inputs[0])
    if bump > 0:
        tc = nodes.new('ShaderNodeTexCoord')
        n = nodes.new('ShaderNodeTexNoise')
        n.inputs['Scale'].default_value = bump_scale
        n.inputs['Detail'].default_value = 6
        bp = nodes.new('ShaderNodeBump')
        bp.inputs['Strength'].default_value = bump
        bp.inputs['Distance'].default_value = 0.0005
        links.new(tc.outputs['Object'], n.inputs['Vector'])
        links.new(n.outputs['Fac'], bp.inputs['Height'])
        links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return mat


def skin_material(name, skin_hex, tint_hex, rough=0.48, sss=0.18, age=0.0):
    """PBR skin: subsurface, pore bump, and a 'blush' attribute that warms cheeks/nose/lips/ears."""
    mat = principled(name, skin_hex, rough=rough, sss=sss, sss_radius=(1.0, 0.4, 0.25), bump=0.15 + 0.25 * age,
                     bump_scale=600 - 300 * age, spec=0.45)
    nodes, links = _nodes(mat)
    a = nodes.new('ShaderNodeAttribute'); a.attribute_name = 'blush'
    mul = nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.55
    links.new(a.outputs['Fac'], mul.inputs[0])
    mix = nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = hexlin(skin_hex); mix.inputs['B'].default_value = hexlin(tint_hex)
    links.new(mul.outputs[0], mix.inputs['Factor'])
    links.new(mix.outputs['Result'], nodes['BSDF'].inputs['Base Color'])
    return mat


def hair_material(name, root_hex, tip_hex, rough=0.42):
    """Hair with root->tip colour gradient (loft attribute 't')."""
    mat = principled(name, root_hex, rough=rough, sheen=0.5, spec=0.35)
    nodes, links = _nodes(mat)
    a = nodes.new('ShaderNodeAttribute'); a.attribute_name = 't'
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.68; ramp.color_ramp.elements[0].color = hexlin(root_hex)
    ramp.color_ramp.elements[1].position = 0.95; ramp.color_ramp.elements[1].color = hexlin(tip_hex)
    links.new(a.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], nodes['BSDF'].inputs['Base Color'])
    return mat


def emission(name, color, strength=5.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nodes, links = _nodes(mat)
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    e = nodes.new('ShaderNodeEmission')
    e.name = 'EMIT'
    e.inputs[0].default_value = hexlin(color)
    e.inputs[1].default_value = strength
    links.new(e.outputs[0], out.inputs[0])
    return mat


def attr_mix_material(name, attr, base_hex, accent_hex, threshold=0.5, rough=0.6, sheen=0.3,
                      accent_emit=0.0, bump=0.3):
    """Fabric whose colour switches to an accent where a mesh attribute > threshold."""
    mat = principled(name, base_hex, rough=rough, sheen=sheen, bump=bump, bump_scale=900)
    nodes, links = _nodes(mat)
    b = nodes['BSDF']
    a = nodes.new('ShaderNodeAttribute')
    a.attribute_name = attr
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = threshold
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    links.new(a.outputs['Fac'], ramp.inputs['Fac'])
    mix = nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = hexlin(base_hex)
    mix.inputs['B'].default_value = hexlin(accent_hex)
    links.new(ramp.outputs['Color'], mix.inputs['Factor'])
    links.new(mix.outputs['Result'], b.inputs['Base Color'])
    if accent_emit > 0:
        b.inputs['Emission Color'].default_value = hexlin(accent_hex)
        mul = nodes.new('ShaderNodeMath')
        mul.operation = 'MULTIPLY'
        mul.inputs[1].default_value = accent_emit
        links.new(ramp.outputs['Color'], mul.inputs[0])
        links.new(mul.outputs[0], b.inputs['Emission Strength'])
    return mat


def eye_material(name, iris_hex, iris_dark_hex, sclera_hex='#EDE8E2', pupil=0.22, iris=0.46,
                 glow_hex=None, base_glow=0.0):
    """Procedural eyeball. Object coords on a unit sphere, cornea points -Y.
    A 'glow' value node (EYE_GLOW) blends in power-mode emission."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    nodes, links = _nodes(mat)
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    b = nodes.new('ShaderNodeBsdfPrincipled')
    b.name = 'BSDF'
    b.inputs['Roughness'].default_value = 0.08
    b.inputs['Coat Weight'].default_value = 1.0
    b.inputs['Coat Roughness'].default_value = 0.02
    tc = nodes.new('ShaderNodeTexCoord')
    sep = nodes.new('ShaderNodeSeparateXYZ')
    links.new(tc.outputs['Object'], sep.inputs[0])
    # r = sqrt(x^2 + z^2)
    comb = nodes.new('ShaderNodeCombineXYZ')
    links.new(sep.outputs['X'], comb.inputs['X'])
    links.new(sep.outputs['Z'], comb.inputs['Y'])
    ln = nodes.new('ShaderNodeVectorMath')
    ln.operation = 'LENGTH'
    links.new(comb.outputs[0], ln.inputs[0])
    ramp = nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.interpolation = 'EASE'
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.005, 0.004, 0.004, 1)
    cr.elements[1].position = pupil
    cr.elements[1].color = (0.005, 0.004, 0.004, 1)
    for pos, col in ((pupil + 0.02, hexlin(iris_dark_hex)), (iris * 0.8, hexlin(iris_hex)),
                     (iris, hexlin(iris_dark_hex)), (iris + 0.03, hexlin(sclera_hex)),
                     (1.0, hexlin(sclera_hex))):
        e = cr.elements.new(pos)
        e.color = col
    links.new(ln.outputs['Value'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    if glow_hex:
        # emission only inside the iris ring, scaled by EYE_GLOW value
        g = nodes.new('ShaderNodeValue')
        g.name = 'EYE_GLOW'
        g.outputs[0].default_value = base_glow
        lt = nodes.new('ShaderNodeMath')
        lt.operation = 'LESS_THAN'
        lt.inputs[1].default_value = iris + 0.02
        links.new(ln.outputs['Value'], lt.inputs[0])
        mul = nodes.new('ShaderNodeMath')
        mul.operation = 'MULTIPLY'
        links.new(lt.outputs[0], mul.inputs[0])
        links.new(g.outputs[0], mul.inputs[1])
        b.inputs['Emission Color'].default_value = hexlin(glow_hex)
        links.new(mul.outputs[0], b.inputs['Emission Strength'])
    links.new(b.outputs[0], out.inputs[0])
    return mat


def assign(ob, *mats):
    ob.data.materials.clear()
    for m in mats:
        ob.data.materials.append(m)


# ---------------------------------------------------------------- body
def skin_body(name, coll, joints, edges, radii, subdiv_base=1, rscale=1.33):
    """Build a quad body mesh from a joint skeleton using the Skin modifier.
    joints: list of (x,y,z); radii: list of (rx, ry) = intended final half-widths.
    rscale compensates the shrink caused by subdividing the skin cage."""
    ob = mesh_object(name, joints, [], coll, edges)
    sk = ob.modifiers.new('Skin', 'SKIN')
    sk.use_smooth_shade = True
    sk.branch_smoothing = 0.6
    sv = ob.data.skin_vertices[0].data
    for i, r in enumerate(radii):
        sv[i].radius = (r[0] * rscale, r[1] * rscale)
    sv[0].use_root = True
    if subdiv_base:
        m = ob.modifiers.new('SubBase', 'SUBSURF')
        m.levels = m.render_levels = subdiv_base
    bake_modifiers(ob)
    ob.data.shade_smooth()
    return ob


def sculpt(ob, bumps):
    """Code 'sculpting': push verts along their normal with anisotropic gaussians.
    bumps: list of (center(x,y,z), sigma(x,y,z), amplitude_m, mirror_x)."""
    me = ob.data
    me.update()
    cos = [v.co.copy() for v in me.vertices]
    nos = [v.normal.copy() for v in me.vertices]
    for i, (co, no) in enumerate(zip(cos, nos)):
        d = 0.0
        for c, s, a, mir in bumps:
            for sx in ((1, -1) if mir else (1,)):
                dx = (co.x - sx * c[0]) / s[0]
                dy = (co.y - c[1]) / s[1]
                dz = (co.z - c[2]) / s[2]
                d += a * math.exp(-0.5 * (dx * dx + dy * dy + dz * dz))
        me.vertices[i].co = co + no * d
    me.update()


def store_rest_attrs(ob):
    """Store rest position & normal as attributes (stable under deformation)."""
    me = ob.data
    pa = me.attributes.get('rest_p') or me.attributes.new('rest_p', 'FLOAT_VECTOR', 'POINT')
    na = me.attributes.get('rest_n') or me.attributes.new('rest_n', 'FLOAT_VECTOR', 'POINT')
    for i, v in enumerate(me.vertices):
        pa.data[i].vector = v.co
        na.data[i].vector = v.normal


def float_attr(ob, name, fn):
    me = ob.data
    a = me.attributes.get(name) or me.attributes.new(name, 'FLOAT', 'POINT')
    for i, v in enumerate(me.vertices):
        a.data[i].value = fn(v.co, v.normal)


# ---------------------------------------------------------------- head
def quad_sphere(cuts=14):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
    for v in bm.verts:
        v.co = v.co.normalized()
    return bm


def deformed_sphere(name, coll, fn, cuts=14):
    """fn(unit_vec) -> Vector position. Returns object."""
    bm = quad_sphere(cuts)
    for v in bm.verts:
        v.co = fn(v.co.copy())
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def bvh_of(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    return BVHTree.FromObject(ob.evaluated_get(dg), dg)


def surface_y(bvh, x, z, y_from=-1.0):
    """Ray from front (-Y) toward +Y in the object's local space; returns hit y."""
    hit = bvh.ray_cast(Vector((x, y_from, z)), Vector((0, 1, 0)), 3.0)
    return hit[0].y if hit[0] is not None else None


def trim_copy(src, name, coll, keep, offset=0.0, solid=0.0, offset_fn=None):
    """Copy a mesh, keep only faces whose verts satisfy keep(co), push along normal."""
    me = src.data.copy()
    me.name = name
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    ob.matrix_world = src.matrix_world.copy()
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    # keep a face when its centre is inside the region (robust for narrow bands)
    kill = [f for f in bm.faces if not keep(f.calc_center_median())]
    bmesh.ops.delete(bm, geom=kill, context='FACES')
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    # merge near-coincident verts (skin-modifier branch points) — they explode under bevel/solidify
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.0015)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges[:], dist=0.0005)
    bm.normal_update()
    if offset or offset_fn:
        for v in bm.verts:
            v.co += v.normal * (offset + (offset_fn(v.co) if offset_fn else 0.0))
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    if solid:
        s = ob.modifiers.new('Solidify', 'SOLIDIFY')
        s.thickness = solid
        s.offset = 1.0
        s.use_even_offset = False
        s.use_quality_normals = True
        s.thickness_clamp = 1.0          # prevents spikes at tiny fingertip / branch faces
    return ob


# ---------------------------------------------------------------- face kit
def mouth_geometry(p, W=0.022, M=18, K=4):
    """2D mouth (u,v) shapes for a parameter dict. Returns lists of (u,v,bulge)
    for interior grid, upper lip grid and lower lip grid (fixed topology)."""
    cl, cr = p.get('corner_l', 0.0), p.get('corner_r', 0.0)
    ou, ol = p.get('open_u', 0.0), p.get('open_l', 0.0)
    w = W * p.get('width', 1.0)
    v0 = p.get('v0', 0.0)
    pucker = p.get('pucker', 0.0)  # rounds the opening (O/U shapes)
    tu, tl = p.get('lip_u', 0.0032), p.get('lip_l', 0.0042)

    def corner(t):
        return ((cl + cr) / 2) * t * t + ((cr - cl) / 2) * t

    def prof(t, k):
        base = max(0.0, 1 - t * t)
        return base ** (k * (1 - 0.5 * pucker))

    us = [(-1 + 2 * i / (M - 1)) for i in range(M)]
    interior, upper, lower = [], [], []
    for t in us:
        u = t * w
        c = corner(t) + v0
        vu = c + ou * prof(t, 0.7)
        vl = c - ol * prof(t, 0.9)
        for k in range(K):
            f = k / (K - 1)
            interior.append((u, vl + (vu - vl) * f, 0.0))
        thick_u = tu * prof(t, 0.6) + 0.0004
        thick_l = tl * prof(t, 0.7) + 0.0004
        for k in range(K):
            f = k / (K - 1)
            upper.append((u, vu + thick_u * f, math.sin(math.pi * f) * thick_u * 0.6 + 0.0006))
            lower.append((u, vl - thick_l * f, math.sin(math.pi * f) * thick_l * 0.6 + 0.0006))
    return interior, upper, lower


def grid_faces(M, K, start=0):
    f = []
    for i in range(M - 1):
        for k in range(K - 1):
            a = start + i * K + k
            f.append((a, a + K, a + K + 1, a + 1))
    return f


def build_mouth(name, coll, head, center_xz, shapes, mats, M=18, K=4, W=0.022):
    """Mouth = interior + upper lip + lower lip, projected on head surface.
    shapes: dict name -> params; 'neutral' is basis. Each becomes a shape key."""
    bvh = bvh_of(head)
    cx, cz = center_xz

    def project(pts):
        out = []
        for (u, v, bulge) in pts:
            x, z = cx + u, cz + v
            y = surface_y(bvh, x, z)
            out.append(Vector((x, y - 0.0007 - bulge, z)))
        return out

    def all_pts(p):
        a, b, c = mouth_geometry(p, W=W, M=M, K=K)
        pa = project(a)
        # interior is pushed slightly *into* the head so it reads as depth
        pa = [q + Vector((0, 0.0004, 0)) for q in pa]
        return pa + project(b) + project(c)

    n = M * K
    faces = grid_faces(M, K, 0) + grid_faces(M, K, n) + grid_faces(M, K, 2 * n)
    basis = all_pts(shapes['neutral'])
    ob = mesh_object(name, basis, faces, coll)
    assign(ob, *mats)
    for i, poly in enumerate(ob.data.polygons):
        poly.material_index = 0 if i < (M - 1) * (K - 1) else 1
    # teeth mask attribute for interior: upper third shows teeth
    teeth = ob.data.attributes.new('teeth', 'FLOAT', 'POINT')
    for i in range(len(basis)):
        k = i % K
        teeth.data[i].value = 1.0 if (i < n and k == K - 1) else 0.0
    ob.shape_key_add(name='Basis')
    for sname, p in shapes.items():
        if sname == 'neutral':
            continue
        kb = ob.shape_key_add(name=sname)
        for i, co in enumerate(all_pts(p)):
            kb.data[i].co = co
    ob.data.shade_smooth()
    return ob


def mouth_interior_material(name, teeth_hex='#EEE9E0', mouth_hex='#3A1418'):
    mat = principled(name, mouth_hex, rough=0.4)
    nodes, links = _nodes(mat)
    a = nodes.new('ShaderNodeAttribute')
    a.attribute_name = 'teeth'
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.elements[0].color = hexlin(mouth_hex)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = hexlin(teeth_hex)
    links.new(a.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], nodes['BSDF'].inputs['Base Color'])
    return mat


def brow_points(p, side, W=0.026, N=10, thick=1.0):
    """Brow centreline in (u,v) relative to brow anchor; side +1 = character left (+X)."""
    inner, outer = p.get('inner', 0.0), p.get('outer', 0.0)
    arch = p.get('arch', 0.0025)
    if side > 0:
        inner += p.get('l_extra', 0.0); outer += p.get('l_extra', 0.0)
    pts = []
    for i in range(N):
        t = i / (N - 1)          # 0 = inner (near nose), 1 = outer
        u = side * (t * W)
        v = inner * (1 - t) + outer * t + arch * math.sin(math.pi * min(1, t * 1.15))
        th = (0.0058 * (1 - 0.60 * t) + 0.0010) * thick  # tapered thickness
        pts.append((u, v, th))
    return pts


def build_brows(name, coll, head, anchors, shapes, mat, N=10, W=0.026, thick=1.0):
    """Two brow strips, each a (N x 3) grid projected on the head; shape keys per expression."""
    bvh = bvh_of(head)

    def strip(p):
        out = []
        for side, (ax, az) in ((-1, anchors[0]), (1, anchors[1])):
            for (u, v, th) in brow_points(p, side, W=W, N=N, thick=thick):
                for k in (-1, 0, 1):
                    x, z = ax + u, az + v + k * th / 2
                    y = surface_y(bvh, x, z)
                    out.append(Vector((x, y - 0.0009 - (0.0011 if k == 0 else 0.0), z)))
        return out

    faces = []
    for s in range(2):
        faces += grid_faces(N, 3, s * N * 3)
    ob = mesh_object(name, strip(shapes['neutral']), faces, coll)
    assign(ob, mat)
    ob.shape_key_add(name='Basis')
    for sname, p in shapes.items():
        if sname == 'neutral':
            continue
        kb = ob.shape_key_add(name=sname)
        for i, co in enumerate(strip(p)):
            kb.data[i].co = co
    ob.data.shade_smooth()
    return ob


def lid_shell(name, coll, radius, upper=True, seg=32, rings=12):
    """Hemispherical eyelid shell around origin. Upper: z>=0, lower: z<=0.
    Stores 'lash' attribute near the free edge."""
    verts, faces = [], []
    for r in range(rings + 1):
        phi = (math.pi / 2) * r / rings          # 0 at pole, pi/2 at edge
        for s in range(seg):
            th = 2 * math.pi * s / seg
            x = math.sin(phi) * math.cos(th)
            y = math.sin(phi) * math.sin(th)
            z = math.cos(phi) * (1 if upper else -1)
            verts.append(Vector((x, y, z)) * radius)
    for r in range(rings):
        for s in range(seg):
            a = r * seg + s
            b = r * seg + (s + 1) % seg
            f = (a, b, b + seg, a + seg)
            faces.append(f if upper else f[::-1])
    ob = mesh_object(name, verts, faces, coll)
    lash = ob.data.attributes.new('lash', 'FLOAT', 'POINT')
    for i, v in enumerate(ob.data.vertices):
        lash.data[i].value = 1.0 - abs(v.co.z) / radius
    s = ob.modifiers.new('Solidify', 'SOLIDIFY')
    s.thickness = radius * 0.06
    s.offset = 1.0
    ob.data.shade_smooth()
    return ob


def lid_material(name, skin_hex, lash_hex='#120E0C', lash_width=0.12):
    mat = principled(name, skin_hex, rough=0.5, sss=0.1)
    nodes, links = _nodes(mat)
    a = nodes.new('ShaderNodeAttribute')
    a.attribute_name = 'lash'
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 1 - lash_width - 0.06
    ramp.color_ramp.elements[0].color = hexlin(skin_hex)
    ramp.color_ramp.elements[1].position = 1 - lash_width
    ramp.color_ramp.elements[1].color = hexlin(lash_hex)
    links.new(a.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], nodes['BSDF'].inputs['Base Color'])
    return mat


# ---------------------------------------------------------------- hair
def curve_hair(name, coll, strands, bevel=0.01, mats=()):
    """strands: list of (points[list Vector], radii[list], material_index)."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = bevel
    cu.bevel_resolution = 3
    cu.resolution_u = 8
    cu.use_fill_caps = True
    for pts, rad, mi in strands:
        sp = cu.splines.new('BEZIER')
        sp.bezier_points.add(len(pts) - 1)
        for bp, co, r in zip(sp.bezier_points, pts, rad):
            bp.co = co
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
            bp.radius = r
        sp.material_index = mi
    ob = bpy.data.objects.new(name + '_CURVE', cu)
    coll.objects.link(ob)
    for m in mats:
        cu.materials.append(m)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    me.name = name
    mob = bpy.data.objects.new(name, me)
    coll.objects.link(mob)
    bpy.data.objects.remove(ob)
    bpy.data.curves.remove(cu)
    me.shade_smooth()
    return mob


def _catmull(pts, n):
    """Sample a Catmull-Rom spline through pts with n samples."""
    P = [pts[0] + (pts[0] - pts[1])] + list(pts) + [pts[-1] + (pts[-1] - pts[-2])]
    out = []
    segs = len(pts) - 1
    for i in range(n):
        t = i / (n - 1) * segs
        k = min(int(t), segs - 1)
        u = t - k
        p0, p1, p2, p3 = P[k], P[k + 1], P[k + 2], P[k + 3]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u))
    return out


def loft_hair(name, coll, strands, center, samples=12, ring=8, mats=(), taper=True):
    """Stylized hair clumps as flattened, sharply tapered ribbons (real geometry).
    strands: list of dicts {pts, width, thick, mat, twist}. 'center' = head centre,
    used to orient the flat side of each clump toward the scalp."""
    verts, faces, mat_idx, tvals = [], [], [], []
    for s in strands:
        path = _catmull([Vector(p) for p in s['pts']], samples)
        base = len(verts)
        rings = []
        for i, c in enumerate(path):
            t = i / (samples - 1)
            T = (path[min(i + 1, samples - 1)] - path[max(i - 1, 0)]).normalized()
            out = (c - Vector(center))
            N = (out - T * out.dot(T)).normalized()
            B = T.cross(N).normalized()
            tw = s.get('twist', 0.0) * t
            N, B = (N * math.cos(tw) + B * math.sin(tw)), (B * math.cos(tw) - N * math.sin(tw))
            if taper:
                w = s['width'] * (1 - t ** 1.25) * (0.85 + 0.25 * math.sin(math.pi * min(1, t * 1.6)))
                th = s['thick'] * (1 - t) ** 0.9
            else:
                w, th = s['width'], s['thick']
            if i == samples - 1 and taper:
                rings.append([len(verts)])
                verts.append(c)
                tvals.append(1.0)
                break
            r = []
            for k in range(ring):
                a = 2 * math.pi * k / ring
                r.append(len(verts))
                verts.append(c + B * (w * math.cos(a)) + N * (th * math.sin(a)))
                tvals.append(t)
            rings.append(r)
        # root cap
        cap_c = len(verts)
        verts.append(path[0])
        tvals.append(0.0)
        for k in range(ring):
            faces.append((cap_c, rings[0][(k + 1) % ring], rings[0][k]))
            mat_idx.append(s.get('mat', 0))
        for ra, rb in zip(rings[:-1], rings[1:]):
            for k in range(ring):
                a0, a1 = ra[k], ra[(k + 1) % ring]
                if len(rb) == 1:
                    faces.append((a0, a1, rb[0]))
                else:
                    faces.append((a0, a1, rb[(k + 1) % ring], rb[k]))
                mat_idx.append(s.get('mat', 0))
    ob = mesh_object(name, verts, faces, coll)
    for m in mats:
        ob.data.materials.append(m)
    for p, mi in zip(ob.data.polygons, mat_idx):
        p.material_index = mi
    ta = ob.data.attributes.new('t', 'FLOAT', 'POINT')
    for i, t in enumerate(tvals):
        ta.data[i].value = t
    ob.data.shade_smooth()
    return ob


def fib_sphere(n):
    pts = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - z * z)
        pts.append(Vector((math.cos(ga * i) * r, math.sin(ga * i) * r, z)))
    return pts


# ---------------------------------------------------------------- rig
def build_armature(name, coll, bones):
    """bones: list of (name, head, tail, parent, connected, roll)."""
    arm = bpy.data.armatures.new(name)
    ob = bpy.data.objects.new(name, arm)
    coll.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.edit_bones
    for (bn, h, t, par, con, roll) in bones:
        b = eb.new(bn)
        b.head, b.tail, b.roll = Vector(h), Vector(t), roll
    for (bn, h, t, par, con, roll) in bones:
        if par:
            eb[bn].parent = eb[par]
            eb[bn].use_connect = con
    bpy.ops.object.mode_set(mode='OBJECT')
    arm.display_type = 'STICK'
    return ob


def auto_weight(mesh_ob, arm_ob):
    bpy.ops.object.select_all(action='DESELECT')
    mesh_ob.select_set(True)
    arm_ob.select_set(True)
    bpy.context.view_layer.objects.active = arm_ob
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    bpy.ops.object.select_all(action='DESELECT')


def bind_copy(ob, arm_ob):
    """For meshes duplicated from the weighted body: they already carry vertex groups."""
    ob.parent = arm_ob
    m = ob.modifiers.new('Armature', 'ARMATURE')
    m.object = arm_ob
    ob.modifiers.move(len(ob.modifiers) - 1, 0)


def bone_parent(ob, arm_ob, bone):
    """Parent to a bone while keeping the object's own local transform untouched
    (compensation goes into matrix_parent_inverse), so code can keep setting
    rotation_euler in the object's original axes (eyelids, eyes, props)."""
    ob.parent = arm_ob
    ob.parent_type = 'BONE'
    ob.parent_bone = bone
    ob.matrix_parent_inverse.identity()
    bpy.context.view_layer.update()
    P = ob.matrix_world @ ob.matrix_basis.inverted()
    ob.matrix_parent_inverse = P.inverted()


def world_rot(arm_ob, bone, axis, deg):
    """Rotate a pose bone about a WORLD axis (as seen in rest pose)."""
    pb = arm_ob.pose.bones[bone]
    pb.rotation_mode = 'QUATERNION'
    R = arm_ob.data.bones[bone].matrix_local.to_quaternion()
    q = Quaternion(Vector(axis), math.radians(deg))
    pb.rotation_quaternion = (R.inverted() @ q @ R) @ pb.rotation_quaternion


def reset_pose(arm_ob):
    driven = {f.data_path.split('"')[1] for f in (arm_ob.animation_data.drivers if arm_ob.animation_data else [])
              if f.data_path.startswith('pose.bones["')}
    for pb in arm_ob.pose.bones:
        if pb.name not in driven:          # driven bones (jaw) keep their euler mode for the driver
            pb.rotation_mode = 'QUATERNION'
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)


# ---------------------------------------------------------------- render
def setup_render(res=(800, 1200), samples=48, transparent=False):
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.cycles.max_bounces = 6
    s.render.resolution_x, s.render.resolution_y = res
    s.render.resolution_percentage = 100
    s.render.film_transparent = transparent
    # 'Standard' keeps palette colours exact on the design sheets
    s.view_settings.view_transform = 'Standard'
    s.view_settings.look = 'None'
    s.render.image_settings.file_format = 'PNG'


def world_color(hex_, strength=0.6):
    w = bpy.data.worlds.get('WORLD') or bpy.data.worlds.new('WORLD')
    bpy.context.scene.world = w
    nodes, links = _nodes(w)
    bg = nodes.get('Background') or nodes.new('ShaderNodeBackground')
    bg.inputs[0].default_value = hexlin(hex_)
    bg.inputs[1].default_value = strength
    out = nodes.get('World Output') or nodes.new('ShaderNodeOutputWorld')
    links.new(bg.outputs[0], out.inputs[0])


def area_light(name, coll, loc, target, power, size=1.0, color='#FFFFFF'):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = power
    ld.size = size
    ld.color = hexlin(color)[:3]
    ob = bpy.data.objects.new(name, ld)
    coll.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob


def look_at(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def camera(name, coll, loc, target, ortho=None, lens=50):
    cd = bpy.data.cameras.new(name)
    if ortho:
        cd.type = 'ORTHO'
        cd.ortho_scale = ortho
    else:
        cd.lens = lens
    cd.clip_start = 0.01
    ob = bpy.data.objects.new(name, cd)
    coll.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob


def render_to(path, cam):
    s = bpy.context.scene
    s.camera = cam
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)

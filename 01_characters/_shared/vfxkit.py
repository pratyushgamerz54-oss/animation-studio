"""vfxkit — reusable procedural power-effect assets (Blender 5.3 bpy).

Every effect is built by one function with timing/intensity parameters so it can
be re-used in any shot: lightning bolts (branching), lightning aura arcs,
magical portal (swirl shader + rim + sparks), speed trails, hand rune ring.
"""
import bpy, math, random
from mathutils import Vector
import charkit as ck


# ---------------------------------------------------------------- materials
def energy_mat(name, hex_, strength):
    return ck.emission(name, hex_, strength)


def set_strength(mat, value):
    mat.node_tree.nodes['EMIT'].inputs[1].default_value = value


# ---------------------------------------------------------------- lightning
def bolt_points(a, b, depth=6, jag=0.18, rnd=None):
    rnd = rnd or random.Random(1)
    pts = [Vector(a), Vector(b)]
    disp = (Vector(b) - Vector(a)).length * jag
    for _ in range(depth):
        new = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            m = (p + q) / 2
            d = (q - p).normalized()
            perp = d.orthogonal().normalized()
            perp.rotate(__import__('mathutils').Quaternion(d, rnd.uniform(0, 2 * math.pi)))
            new += [m + perp * rnd.uniform(-disp, disp), q]
        pts = new
        disp *= 0.55
    return pts


def lightning(name, coll, a, b, core_mat, glow_mat, seed=1, branches=4, radius=0.0035,
              depth=6, jag=0.18, glow=3.0):
    """Branching lightning bolt from a to b. Returns list of objects (core + glow)."""
    rnd = random.Random(seed)
    paths = [bolt_points(a, b, depth, jag, rnd)]
    main = paths[0]
    for _ in range(branches):
        i = rnd.randint(len(main) // 6, len(main) * 3 // 4)
        start = main[i]
        dirv = (Vector(b) - Vector(a)).normalized()
        off = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))).normalized()
        L = (Vector(b) - Vector(a)).length * rnd.uniform(0.15, 0.35)
        end = start + (dirv * 0.6 + off * 0.7).normalized() * L
        paths.append(bolt_points(start, end, depth - 2, jag * 1.2, rnd))
    obs = []
    for layer, mat, rad in (('CORE', core_mat, radius), ('GLOW', glow_mat, radius * glow)):
        cu = bpy.data.curves.new(f'{name}_{layer}', 'CURVE')
        cu.dimensions = '3D'
        cu.bevel_depth = rad
        cu.bevel_resolution = 2
        for k, pts in enumerate(paths):
            sp = cu.splines.new('POLY')
            sp.points.add(len(pts) - 1)
            for j, (pt, p) in enumerate(zip(sp.points, pts)):
                pt.co = (p.x, p.y, p.z, 1)
                t = j / (len(pts) - 1)
                pt.radius = (1.0 if k == 0 else 0.55) * (1 - 0.6 * t)
        cu.materials.append(mat)
        ob = bpy.data.objects.new(f'{name}_{layer}', cu)
        coll.objects.link(ob)
        if layer == 'GLOW':
            ob.visible_shadow = False
        obs.append(ob)
    return obs


def aura_arcs(name, coll, anchors, core_mat, glow_mat, seed=3, size=0.12, count=10):
    """Short crackling arcs hugging the body; anchors = list of world points."""
    rnd = random.Random(seed)
    obs = []
    for i in range(count):
        p = Vector(rnd.choice(anchors))
        d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))).normalized()
        q = p + d * size * rnd.uniform(0.5, 1.2)
        obs += lightning(f'{name}_{i:02d}', coll, p, q, core_mat, glow_mat, seed=seed * 31 + i,
                         branches=1, radius=0.0024, depth=5, jag=0.35, glow=4.0)
    return obs


# ---------------------------------------------------------------- portal
def portal_material(name, rim_hex, deep_hex, swirl=5.0, strength=6.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if mat.node_tree is None:
        mat.use_nodes = True
    nt = mat.node_tree
    N, L = nt.nodes, nt.links
    N.clear()
    out = N.new('ShaderNodeOutputMaterial')
    tc = N.new('ShaderNodeTexCoord')
    sep = N.new('ShaderNodeSeparateXYZ')
    L.new(tc.outputs['Object'], sep.inputs[0])
    r = N.new('ShaderNodeMath'); r.operation = 'POWER'
    # r = sqrt(x^2 + y^2)
    x2 = N.new('ShaderNodeMath'); x2.operation = 'MULTIPLY'
    y2 = N.new('ShaderNodeMath'); y2.operation = 'MULTIPLY'
    L.new(sep.outputs['X'], x2.inputs[0]); L.new(sep.outputs['X'], x2.inputs[1])
    # disc is a circle primitive: its local plane is X/Y
    L.new(sep.outputs['Y'], y2.inputs[0]); L.new(sep.outputs['Y'], y2.inputs[1])
    add = N.new('ShaderNodeMath'); add.operation = 'ADD'
    L.new(x2.outputs[0], add.inputs[0]); L.new(y2.outputs[0], add.inputs[1])
    L.new(add.outputs[0], r.inputs[0]); r.inputs[1].default_value = 0.5
    ang = N.new('ShaderNodeMath'); ang.operation = 'ARCTAN2'
    L.new(sep.outputs['Y'], ang.inputs[0]); L.new(sep.outputs['X'], ang.inputs[1])
    tw = N.new('ShaderNodeMath'); tw.operation = 'MULTIPLY_ADD'
    L.new(r.outputs[0], tw.inputs[0]); tw.inputs[1].default_value = swirl
    L.new(ang.outputs[0], tw.inputs[2])
    cs = N.new('ShaderNodeMath'); cs.operation = 'COSINE'
    sn = N.new('ShaderNodeMath'); sn.operation = 'SINE'
    L.new(tw.outputs[0], cs.inputs[0]); L.new(tw.outputs[0], sn.inputs[0])
    comb = N.new('ShaderNodeCombineXYZ')
    L.new(cs.outputs[0], comb.inputs['X']); L.new(sn.outputs[0], comb.inputs['Y'])
    L.new(r.outputs[0], comb.inputs['Z'])
    noise = N.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.2
    noise.inputs['Detail'].default_value = 8
    noise.inputs['Distortion'].default_value = 0.6
    L.new(comb.outputs[0], noise.inputs['Vector'])
    ramp = N.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = ck.hexlin(deep_hex)
    cr.elements[1].position = 0.75; cr.elements[1].color = ck.hexlin(rim_hex)
    L.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    # brightness rises toward the rim, centre stays deep
    rr = N.new('ShaderNodeValToRGB')
    rr.color_ramp.elements[0].position = 0.0; rr.color_ramp.elements[0].color = (0.25, 0.25, 0.25, 1)
    rr.color_ramp.elements[1].position = 1.0; rr.color_ramp.elements[1].color = (1, 1, 1, 1)
    L.new(r.outputs[0], rr.inputs['Fac'])
    mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    mul.name = 'STRENGTH'
    L.new(rr.outputs['Color'], mul.inputs[0]); mul.inputs[1].default_value = strength
    em = N.new('ShaderNodeEmission')
    L.new(ramp.outputs['Color'], em.inputs['Color'])
    L.new(mul.outputs[0], em.inputs['Strength'])
    # fade the disc edge so it blends into the rim
    tr = N.new('ShaderNodeBsdfTransparent')
    mix = N.new('ShaderNodeMixShader')
    edge = N.new('ShaderNodeMath'); edge.operation = 'GREATER_THAN'; edge.inputs[1].default_value = 0.98
    L.new(r.outputs[0], edge.inputs[0])
    L.new(edge.outputs[0], mix.inputs['Fac'])
    L.new(em.outputs[0], mix.inputs[1]); L.new(tr.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs[0])
    return mat


def portal(name, coll, center, radius, rim_hex, deep_hex, yaw_deg=0.0, openness=1.0,
           intensity=1.0, seed=5, swirl=5.0):
    """Magical portal: swirling disc + glowing rim torus + sparks, parented to an
    empty PORTAL root (move/rotate/animate that). Built facing -Y.
    openness 0..1 = opening/closing scale; intensity scales all emission."""
    root = bpy.data.objects.new(f'{name}_ROOT', None)
    coll.objects.link(root)
    obs = [root]
    r = radius * max(0.02, openness)
    bpy.ops.mesh.primitive_circle_add(vertices=96, radius=1.0, fill_type='TRIFAN', location=(0, 0, 0),
                                      rotation=(math.pi / 2, 0, 0))
    disc = bpy.context.object
    disc.name = f'{name}_DISC'
    disc.scale = (r, r, r)
    ck.assign(disc, portal_material(f'MAT_{name}_SWIRL', rim_hex, deep_hex, swirl=swirl,
                                    strength=2.5 * intensity))
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.035, major_segments=96,
                                     minor_segments=12, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    rim = bpy.context.object
    rim.name = f'{name}_RIM'
    ck.assign(rim, ck.emission(f'MAT_{name}_RIM', '#DDFBFF', 7.0 * intensity))
    parts = [disc, rim]
    glow = ck.emission(f'MAT_{name}_SPARK', rim_hex, 12.0 * intensity)
    rnd = random.Random(seed)
    for i in range(int(60 * openness)):
        a = rnd.uniform(0, 2 * math.pi)
        rr = r * rnd.uniform(1.0, 1.25)
        p = (math.cos(a) * rr, rnd.uniform(-0.03, 0.03), math.sin(a) * rr)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r * rnd.uniform(0.006, 0.016), location=p)
        sp = bpy.context.object
        sp.name = f'{name}_SPARK_{i:02d}'
        ck.assign(sp, glow)
        parts.append(sp)
    ld = bpy.data.lights.new(f'{name}_LIGHT', 'POINT')
    ld.energy = 60 * intensity * openness
    ld.color = ck.hexlin(rim_hex)[:3]
    ld.shadow_soft_size = r
    lo = bpy.data.objects.new(f'{name}_LIGHT', ld)
    lo.location = (0, -0.05, 0)
    coll.objects.link(lo)
    parts.append(lo)
    for o in parts:
        ck.link(o, coll)
        o.parent = root
        o.visible_shadow = False
    root.location = center
    root.rotation_euler = (0, 0, math.radians(yaw_deg))
    return obs + parts


# ---------------------------------------------------------------- speed trails
def speed_trails(name, coll, anchors, direction, mat, length=0.9, seed=9, count=14, width=0.006):
    """Tapered emissive streaks trailing behind anchor points (opposite to motion)."""
    rnd = random.Random(seed)
    d = Vector(direction).normalized()
    strands = []
    for i in range(count):
        p = Vector(rnd.choice(anchors)) + Vector((0, rnd.uniform(-0.04, 0.04), rnd.uniform(-0.05, 0.05)))
        L = length * rnd.uniform(0.5, 1.1)
        pts = [p, p - d * L * 0.33 + Vector((0, 0, rnd.uniform(-0.01, 0.01))),
               p - d * L * 0.66, p - d * L]
        strands.append({'pts': pts, 'width': width * rnd.uniform(0.6, 1.4), 'thick': width * 0.5, 'mat': 0})
    ob = ck.loft_hair(name, coll, strands, Vector(anchors[0]) + Vector((0, 0, 10)), samples=8, ring=6, mats=[mat])
    ob.visible_shadow = False
    return ob


# ---------------------------------------------------------------- runes
def rune_ring(name, coll, center, radius, mat, facing_rot=(0, 0, 0), ticks=12):
    obs = []
    for k, (rr, thick) in enumerate(((radius, radius * 0.03), (radius * 0.78, radius * 0.018))):
        bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=thick, major_segments=64,
                                         minor_segments=6, location=center, rotation=facing_rot)
        t = bpy.context.object
        t.name = f'{name}_RING{k}'
        ck.link(t, coll)
        ck.assign(t, mat)
        obs.append(t)
    return obs

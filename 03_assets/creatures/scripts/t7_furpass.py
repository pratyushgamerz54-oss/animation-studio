"""t7_furpass — REAL FUR pass for furred CC bases (Director 23 Nov: "skin plastic jaisa") — matte skin + strand groom.

usage: $BPY45 t7_furpass.py <in.blend> <out.blend> <species_id>
  1. matte skin: metallic → 0 (glTF metallicRoughness maps often carry metal values), roughness ≥ .8, specular ≈ .2
  2. fur-card meshes: alpha from the base-colour texture alpha (else they render as solid shells)
  3. strand groom on the main body mesh (own NG_T7_FUR on a hair-Curves object, follows the deformed mesh):
     colour sampled from the base texture at each vertex (sRGB → linear), length / density by region (bone weights),
     comb along the governing bone (tail along the tail, legs downward, body backward), no hair on nose / eyes / paw pads.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7kit as K

CFG = {
    'red_fox': dict(body_mat=['M_Fox'], card_mat='M_FoxFur', density=260000, radius=0.00022,
                    length={'Tail': 0.065, 'Head': 0.009, 'Neck': 0.040, 'Foot': 0.006, 'Hand': 0.006, 'Finger': 0.004,
                            'Calf': 0.012, 'Forearm': 0.012, 'HorseLink': 0.008, '*': 0.034},
                    lift=0.45, droop=0.35, frizz=0.45),
    'wolf': dict(body_mat=['1074'], card_mat=None, density=220000, radius=0.00026,
                 length={'Tail': 0.07, 'Head': 0.012, 'Neck': 0.060, 'LowerLeg': 0.010, 'Ear': 0.008, 'Torso': 0.040, '*': 0.036},
                 lift=0.45, droop=0.4, frizz=0.4, hair_tint=(1.10, 0.92, 0.72), hair_gain=0.85),
    'black_bear': dict(body_mat=['Material_003', 'Material_001'], card_mat=None, hide_mats=('Material_002',), density=200000, radius=0.00032,
                       hair_rough=0.55, hair_coat=0.0,
                       length={'Head': 0.022, 'Neck': 0.08, 'Chest': 0.07, 'Collarbone': 0.09, 'Ankle': 0.03, 'Digit': 0.012,
                               'Ear': 0.03, 'Jaw': 0.006, 'Tongue': 0.0, 'Leg2': 0.05, '*': 0.07}, lift=0.5, droop=0.55, frizz=0.5, hair_gain=0.6, hair_shader='matte'),
    'sambar': dict(body_mat=['Body', 'Head'], card_mat=None, density=120000, radius=0.00028,
                   length={'Neck': 0.055, 'Head': 0.006, 'Jaw': 0.005, 'Ear': 0.004, 'Leg3': 0.006, 'Ankle': 0.004, 'Tail': 0.045, '*': 0.011},   # short coarse deer coat (texture shows through), shaggy neck mane
                   lift=0.25, droop=0.35, frizz=0.35, hair_rough=0.6, hair_coat=0.0, hair_tint=(1.04, 0.97, 0.90), hair_gain=0.85),
    'red_panda': dict(body_mat=['lambert1'], card_mat=None, density=240000, radius=0.00024,
                      length={'Tile': 0.035, 'Head': 0.014, 'Ear': 0.012, 'Neck': 0.045, 'Foot': 0.010, 'Toe': 0.006, 'Hand': 0.010,
                              'Finger': 0.006, 'Calf': 0.020, 'Forearm': 0.020, 'HorseLink': 0.014, 'Mouth': 0.004, '*': 0.038},
                      lift=0.55, droop=0.35, frizz=0.5, hair_rough=0.45, hair_coat=0.05, hair_gain=0.92),   # long dense soft coat, bushy tail
    'marmot': dict(body_mat=['auto', 'auto9'], card_mat=None, density=260000, radius=0.00024,
                   length={'Bone.004': 0.012, 'Bone.003': 0.030, 'Bone.005': 0.05, 'Bone.006': 0.05, 'Bone.007': 0.05, 'Bone.008': 0.04,
                           'Bone.012': 0.006, 'Bone.016': 0.006, 'Bone.020': 0.006, 'Bone.025': 0.006, '*': 0.042},
                   lift=0.5, droop=0.4, frizz=0.5, hair_rough=0.45, hair_coat=0.0, hair_gain=0.72),
}


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    src, dst, sid = a[0], a[1], a[2]; cfg = CFG[sid]
    bpy.ops.wm.open_mainfile(filepath=src)
    bpy.context.preferences.filepaths.save_version = 0
    for m in bpy.data.materials:
        if not m.use_nodes or not m.node_tree.nodes.get('Principled BSDF'):
            continue
        b = m.node_tree.nodes['Principled BSDF']; L = m.node_tree.links
        for k in ('Metallic', 'Roughness'):
            for l in list(b.inputs[k].links):
                L.remove(l)
        b.inputs['Metallic'].default_value = 0.0; b.inputs['Roughness'].default_value = 0.82
        b.inputs['Specular IOR Level'].default_value = 0.2
        if m.name == cfg.get('card_mat'):
            tex = next((n for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and ('base' in n.image.name.lower() or 'diffuse' in n.image.name.lower())), None)
            if tex:
                L.new(tex.outputs['Alpha'], b.inputs['Alpha'])
                m.blend_method = 'HASHED'
    for o in list(bpy.data.objects):                 # crude base hair strips replaced by the real groom
        if o.type == 'MESH' and o.active_material and o.active_material.name in cfg.get('hide_mats', ()):
            bpy.data.objects.remove(o)                    # removed (hiding alone still let it render in some passes)
    for body in [o for o in bpy.data.objects if o.type == 'MESH' and o.active_material and o.active_material.name in cfg['body_mat']]:
        me = body.data; print("STEP body", body.name, flush=True)
        # per-vertex colour from the base texture (average of the vertex's UV corners)
        bsdf = body.active_material.node_tree.nodes.get('Principled BSDF')
        lk = bsdf.inputs['Base Color'].links if bsdf else []
        img_node = lk[0].from_node if lk and lk[0].from_node.type == 'TEX_IMAGE' else next(n for n in body.active_material.node_tree.nodes if n.type == 'TEX_IMAGE')
        img = img_node.image; w, h = img.size
        buf = np.empty(w * h * img.channels, np.float32); img.pixels.foreach_get(buf)              # memory-safe (no Python list)
        px = buf.reshape(h, w, img.channels)[..., :3]; del buf                                         # 8-bit sRGB image → stored (non-linear) values
        if img.colorspace_settings.name == 'sRGB' and not img.is_float:
            px = np.where(px <= 0.04045, px / 12.92, ((px + 0.055) / 1.055) ** 2.4)              # → linear for the hair shader
        uv = me.uv_layers.active.data
        acc = np.zeros((len(me.vertices), 3), np.float32); cnt = np.zeros(len(me.vertices), np.float32)
        for poly in me.polygons:
            for li in poly.loop_indices:
                u, v = uv[li].uv; x = int(np.clip(u % 1.0, 0, 0.9999) * w); y = int(np.clip(v % 1.0, 0, 0.9999) * h)
                vi = me.loops[li].vertex_index; acc[vi] += px[y, x]; cnt[vi] += 1
        col = acc / np.maximum(cnt, 1)[:, None]
        col = np.clip(col * np.array(cfg.get('hair_tint', (1, 1, 1)), np.float32) * cfg.get('hair_gain', 1.0), 0, 1)   # photo-matched hair colour
        K.put_coat(body, col); print("STEP coat", flush=True)
        # region by the strongest bone weight
        gname = {g.index: g.name for g in body.vertex_groups}
        L_ = np.zeros(len(me.vertices), np.float32); comb = np.zeros((len(me.vertices), 3), np.float32)
        arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
        for v in me.vertices:
            if not v.groups:
                L_[v.index] = cfg['length']['*']; comb[v.index] = (-1, 0, -0.3); continue
            g = max(v.groups, key=lambda g: g.weight); n = gname.get(g.group, '')
            key = next((k for k in cfg['length'] if k != '*' and k in n), '*')
            L_[v.index] = cfg['length'][key]
            bn = arm.data.bones.get(n)
            if bn is not None:
                d = (arm.matrix_world.to_3x3() @ (bn.tail_local - bn.head_local)).normalized()
                if key in ('Head',):
                    d = -d                                      # head hair lies back toward the neck
                comb[v.index] = d[:]
            else:
                comb[v.index] = (-1, 0, -0.3)
        # short face fur: the front half of the head (muzzle, around the eyes) gets very short hair, like a real fox
        hb_ = next((b for b in arm.data.bones if 'Head' in b.name), None)
        if hb_ is not None:
            hw = arm.matrix_world; h0 = hw @ hb_.head_local; h1 = hw @ hb_.tail_local; hd = (h1 - h0).normalized()
            mw = body.matrix_world
            Pw = np.array([(mw @ v.co)[:] for v in me.vertices], np.float32)
            t = (Pw - np.array(h0[:])) @ np.array(hd[:])
            hl = float((h1 - h0).length)
            isface = np.array([any(gname.get(g.group, '') == hb_.name and g.weight > 0.3 for g in v.groups) for v in me.vertices])
            front = np.clip((t - 0.2 * hl) / (0.6 * hl), 0, 1) * isface
            L_ = L_ * (1 - front) + 0.0035 * front
        # comb into the mesh's local space (attributes are local), tangent projection done by the fur group's lift
        inv = body.matrix_world.inverted().to_3x3()
        comb = np.array([(inv @ Vector(c)).normalized()[:] for c in comb], np.float32)
        K.set_attr(body, 'fur_len', L_)
        # no hair on the nose tip / eyes: darkest texture spots on the head (nose leather, eyes) and lowest foot pads
        lum = col @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        dens = np.where(lum < np.percentile(lum, 1.5), 0.0, 1.0).astype(np.float32)
        K.set_attr(body, 'fur_density', dens)
        K.set_attr(body, "comb", comb, "FLOAT_VECTOR"); print("STEP attrs", flush=True)
        hm = bpy.data.materials.get(f'T7_{sid.upper()}_HAIR')
        if hm is None and cfg.get('hair_shader') == 'matte':          # very dark fur: matte strands (hair-BSDF sheen reads blue-grey on black)
            hm = K.mat_attr(f'T7_{sid.upper()}_HAIR', attr='coat', rough=0.9, spec=0.15, bump=0.0)
        if hm is None:
            hm = K.mat_hair(f'T7_{sid.upper()}_HAIR', rough=cfg.get('hair_rough', 0.38), coat_var=0.14, coat=cfg.get('hair_coat', 0.1))
        fo = K.fur(body, hm, density=cfg['density'], radius=cfg['radius'], lift=cfg['lift'], droop=cfg['droop'], frizz=cfg['frizz'])
    bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True, relative_remap=True)
    print('FURPASS SAVED', dst)


main()

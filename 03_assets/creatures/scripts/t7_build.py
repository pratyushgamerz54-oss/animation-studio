"""t7_build — build one or more concept creatures (TASK 07 milestone 1) → .blend + concept renders.

usage:  $BPY45 t7_build.py <species_id> [<species_id> ...] [--out DIR] [--test]
Species definitions live in t7_species.py (SPECIES dict). Each build:
  1. anatomy builder → SDF parts → clean quad meshes (Quadriflow) + UVs + zone attributes
  2. coat colours, fur length / density / comb attributes, materials, eyes, fur groom (NG_T7_FUR)
  3. collection T7_<ID> in a per-species .blend (concept file) + renders: 3/4 hero, side ortho (measurements), front, face
"""
import os, sys, json, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import t7kit as K
import t7sdf as S
import t7_species as SP

args = [a for a in sys.argv[sys.argv.index('--') + 1:]] if '--' in sys.argv else sys.argv[1:]
OUT = os.path.join(K.CR, '00_CREATURE_REFERENCES', 'concepts')
TEST = '--test' in args
FURTEST = '--furtest' in args
if '--out' in args:
    OUT = args[args.index('--out') + 1]
ids = [a for a in args if not a.startswith('--') and a != OUT]
COMB = {'*': (-1, 0, -0.3), 'leg': (0.1, 0, -1), 'paw': (1, 0, -0.4), 'tail': (-0.4, 0, -1), 'head': (-1, 0, 0.25),
        'face': (-1, 0, 0.15), 'chin': (-1, 0, -0.4), 'ear': (0, 0, 1), 'ear_in': (0, 0, 1), 'neck': (-0.6, 0, -0.6),
        'throat': (0, 0, -1), 'belly': (-0.3, 0, -1), 'chest': (0, 0, -1)}


def build(sid):
    t0 = time.time()
    spec = SP.SPECIES[sid]
    K.clean()
    coll = bpy.data.collections.new('T7_' + sid.upper()); bpy.context.scene.collection.children.link(coll)
    parts, marks = spec['builder'](spec['p'])
    for extra in spec.get('extra', []):
        parts.update(extra(marks))
    objs = {}
    for pname, part in parts.items():
        o, P, W, D = K.part_to_object(part, f'{sid}_{pname}', coll, quads=spec.get('quads', {}).get(pname, 6000),
                                      warp=spec.get('warp', {}).get(pname))
        N = K.normals(o)
        C = K.coat_from_zones(W, P, spec['coat'], spec.get('mottle', 0.10), spec.get('mottle_scale', 6.0))
        if spec.get('coat_fn'):
            C = spec['coat_fn'](P, W, C, marks)
        K.put_coat(o, C)
        fl = sum(W[z] * spec.get('fur_len', {}).get(z, spec.get('fur_len', {}).get('*', 0.0)) for z in W)
        K.set_attr(o, 'fur_len', fl)
        fd = sum(W[z] * spec.get('fur_dens', {}).get(z, spec.get('fur_dens', {}).get('*', 1.0)) for z in W)
        fl0 = [z for z in W if spec.get('fur_len', {}).get(z, spec.get('fur_len', {}).get('*', 0.0)) <= 0.0025]
        bare_w = sum((W[z] for z in fl0), np.zeros(len(P)))
        fd = np.where((fl > 1e-4) & (bare_w < 0.3), fd, 0.0)            # no hair on nose leather, lids, hooves, claws
        K.set_attr(o, 'fur_density', fd)
        cr = dict(COMB); cr.update(spec.get('comb', {}))
        Cb = K.comb_field(P, N, {z: (v(P, marks) if callable(v) else v) for z, v in cr.items()}, W)
        K.set_attr(o, 'comb', Cb, 'FLOAT_VECTOR')
        gl = sum(W[z] for z in W if z in spec.get('gloss', ()))
        K.set_attr(o, 'gloss', gl if np.ndim(gl) else np.zeros(len(P)))
        bare = spec.get('bare', ())
        K.set_attr(o, 'plume', 1.0 - sum((W[z] for z in W if z in bare), np.zeros(len(P))))
        mk = spec.get('mat', {}).get(pname, 'skin')
        if mk == 'skin':
            mat = K.mat_skin(f'T7_{sid}_{pname}_SKIN', gloss_attr='gloss', rough=spec.get('skin_rough', 0.62))
        elif mk == 'feather':
            mat = K.mat_feather(f'T7_{sid}_{pname}_PLUMAGE', scale=spec.get('plume_scale', 90))
        elif mk == 'horn':
            mat = K.mat_attr(f'T7_{sid}_{pname}_HORN', rough=0.6, spec=0.3, bump=0.6, bump_scale=120)
        else:
            mat = K.mat_attr(f'T7_{sid}_{pname}_{mk.upper()}', rough=spec.get('rough', 0.55))
        # hooves / horns / nose zones: separate material slots for production; concept uses the coat colour + gloss attr
        o.data.materials.append(mat)
        if fl.max() > 0 and (FURTEST or not TEST):
            hm = K.mat_hair(f'T7_{sid}_{pname}_HAIR')
            fs = spec.get('fur', {})
            K.fur(o, hm, density=fs.get('density', 40000), radius=fs.get('radius', 0.00012), lift=fs.get('lift', 0.3),
                  droop=fs.get('droop', 0.25), frizz=fs.get('frizz', 0.15))
        objs[pname] = o
    if spec.get('feathers'):
        v, f, A_ = spec['feathers'](marks)
        fo = K.mesh_from(f'{sid}_feathers', v, f, coll)
        for k, a in A_.items():
            K.set_attr(fo, k, a)
        K.put_coat(fo, spec['feather_col'](A_, v))
        sol = fo.modifiers.new('thick', 'SOLIDIFY'); sol.thickness = spec.get('feather_th', 0.0012); sol.offset = 0
        fo.data.materials.append(K.mat_blade(f'T7_{sid}_FEATHER'))
        bpy.context.view_layer.objects.active = fo
        with bpy.context.temp_override(object=fo, active_object=fo, selected_objects=[fo], selected_editable_objects=[fo]):
            bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003); bpy.ops.object.mode_set(mode='OBJECT')
        objs['feathers'] = fo
    # eyes
    em = K.mat_eye(f'T7_{sid}_EYE', **spec.get('eye', {}))
    for s in (1, -1):
        e = marks['eye'].copy(); e[1] *= s
        d = marks['eye_dir'].copy(); d[1] *= s
        K.eyeball(f'{sid}_eye_{"L" if s > 0 else "R"}', Vector(e), marks['eye_r'] * 0.98, d, em, coll)
    lo, hi = K.dims(coll.objects)
    meas = dict(length=float(hi[0] - lo[0]), width=float(hi[1] - lo[1]), height=float(hi[2] - lo[2]), min=lo.tolist(), max=hi.tolist())
    coll['t7_meas'] = json.dumps(meas)
    print(f'[{sid}] built {time.time() - t0:.0f}s  L={meas["length"]:.2f} H={meas["height"]:.2f}  faces=' +
          str({k: len(o.data.polygons) for k, o in objs.items()}))
    return coll, marks, meas


def shots(sid, coll, marks, meas, samples=64, size=(1400, 1000)):
    spec = SP.SPECIES[sid]
    K.studio(ground=spec.get('ground', '#5B5446'), size=size, samples=samples, sun=spec.get('sun', (50, 0, 140)))
    lo, hi = np.array(meas['min']), np.array(meas['max'])
    c = (lo + hi) / 2; L = max(hi - lo)
    out = os.path.join(OUT, sid); os.makedirs(out, exist_ok=True)
    cam = K.camera('CAM_34', c + Vector((1.25 * L, -1.55 * L, 0.35 * L)) if False else tuple(c + np.array([1.2, -1.6, 0.30]) * L * 1.15),
                   tuple(c + np.array([0, 0, -0.05 * L])), lens=55)
    K.render(cam, os.path.join(out, f'{sid}_34.png'))
    cs = K.camera('CAM_SIDE', tuple(c + np.array([0, -4 * L, 0])), tuple(c), ortho=L * 1.25)
    K.render(cs, os.path.join(out, f'{sid}_side.png'))
    if spec.get('p', {}).get('spread', 0) > 0.5:
        ct = K.camera('CAM_TOP', tuple(c + np.array([0, 0, 4 * L])), tuple(c), ortho=L * 1.15)
        ct.rotation_euler = (0, 0, 0)
        K.render(ct, os.path.join(out, f'{sid}_top.png'))
    fr = K.camera('CAM_FRONT', tuple(c + np.array([4 * L, 0, 0])), tuple(c), ortho=L * 1.25)
    K.render(fr, os.path.join(out, f'{sid}_front.png'))
    if not TEST:
        cs = K.camera('CAM_SIDE', tuple(c + np.array([0, -4 * L, 0])), tuple(c), ortho=L * 1.25)
        K.render(cs, os.path.join(out, f'{sid}_side.png'))
        fr = K.camera('CAM_FRONT', tuple(c + np.array([4 * L, 0, 0])), tuple(c), ortho=L * 1.25)
        K.render(fr, os.path.join(out, f'{sid}_front.png'))
    hl = marks['hl']; nose = marks['nose']; eye = marks['eye']
    fc = (np.array(eye) + np.array(nose)) / 2
    fcam = K.camera('CAM_FACE', tuple(fc + np.array([1.4, -1.6, 0.35]) * hl * 2.4), tuple(fc), lens=85)
    K.render(fcam, os.path.join(out, f'{sid}_face.png'))
    return out


for sid in ids:
    coll, marks, meas = build(sid)
    out = os.path.join(OUT, sid); os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f'T7_CONCEPT_{sid.upper()}_v001.blend')
    bpy.ops.wm.save_as_mainfile(filepath=fn, compress=True)
    json.dump(meas, open(os.path.join(out, f'{sid}_meas.json'), 'w'), indent=1)
    shots(sid, coll, marks, meas, samples=24 if TEST else 64, size=(900, 650) if (TEST or FURTEST) else (1400, 1000))
    print('SAVED', fn)
print('ALLDONE')

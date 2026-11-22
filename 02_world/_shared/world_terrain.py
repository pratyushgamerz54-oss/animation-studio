"""World overview terrain (LOD0) in Blender + aerial reference renders.

Run:  python3 02_world/_shared/world_terrain.py [samples]
In :  02_world/map/data/*  (from worldgen.py)
Out:  02_world/blend/WORLD_overview_v001.blend
      02_world/map/aerial/AERIAL_world_south.png, AERIAL_<code>.png (one per region), AERIAL_sheet_v1.png

Scale of THIS file: overview model, 1 Blender unit = 1 km, heights x3 exaggeration (readable from the air).
Detailed region scenes (Ashram etc.) are built separately in real metres; their WCS offset is stored on the
LOC_* empties here (custom props wcs_x_km / wcs_y_km).
"""
import os, sys, json, math
import numpy as np
import bpy, bmesh
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', '01_characters', '_shared'))
sys.path.insert(0, HERE)
import charkit as ck
import worldgen as wg

DATA = os.path.join(ROOT, 'map', 'data'); AER = os.path.join(ROOT, 'map', 'aerial'); BL = os.path.join(ROOT, 'blend')
os.makedirs(AER, exist_ok=True); os.makedirs(BL, exist_ok=True)
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 24
W, H = wg.W, wg.H
EXAG = 3.0


def coll(n):
    return ck.get_coll(n)


def main():
    ck.reset()
    h = np.load(os.path.join(DATA, 'height_m.npy'))
    acc = np.load(os.path.join(DATA, 'accum.npy')); lakes = np.load(os.path.join(DATA, 'lakes.npy'))
    feats = json.load(open(os.path.join(DATA, 'features.json')))
    # texture = map colours + rivers (no labels)
    tex = Image.open(os.path.join(DATA, 'color_nolabels.png')).convert('RGBA')
    Fh = np.load(os.path.join(DATA, 'filled_m.npy'))
    sea = h <= 0
    down, _ = wg.flow(Fh, sea)
    riv = (~sea) & (acc > 140) & ~lakes
    wg.draw_rivers(ImageDraw.Draw(tex), acc, down, riv, 2)
    tp = os.path.join(DATA, 'color_rivers.png'); tex.convert('RGB').save(tp)
    # ------------------------------------------------------------------ terrain mesh (LOD0, 2 km grid)
    step = 2
    hs = h[::step, ::step]; R, C = hs.shape
    verts = []
    for r in range(R):
        for c in range(C):
            verts.append((c * step, (H - r * step), max(hs[r, c], -400) / 1000 * EXAG))
    faces = [(r * C + c, r * C + c + 1, (r + 1) * C + c + 1, (r + 1) * C + c) for r in range(R - 1) for c in range(C - 1)]
    T = coll('WORLD_TERRAIN')
    me = bpy.data.meshes.new('WORLD_TERRAIN_LOD0'); me.from_pydata(verts, [], faces[::-1] if False else faces); me.update()
    ob = bpy.data.objects.new('WORLD_TERRAIN_LOD0', me); T.objects.link(ob)
    uv = me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (v.x / W, v.y / H)
    for p in me.polygons:
        p.use_smooth = True
    if me.polygons[0].normal.z < 0:
        me.flip_normals()
    m = bpy.data.materials.new('MAT_WORLD_TERRAIN'); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(tp)
    nt.links.new(im.outputs['Color'], bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = .85
    me.materials.append(m)
    # sea
    Wt = coll('WORLD_WATER')
    bpy.ops.mesh.primitive_plane_add(size=1, location=(W / 2, H / 2, -0.01))
    sp = bpy.context.object; sp.name = 'WORLD_SEA'; sp.scale = (W * 12, H * 12, 1); ck.link(sp, Wt)
    sm = ck.principled('MAT_WORLD_SEA', '#0A2C4E', rough=.22)
    sp.data.materials.append(sm)
    # ------------------------------------------------------------------ location markers (WCS reference)
    Mk = coll('WORLD_LOCATIONS')

    def loc(name, p, **props):
        x, y = p[0], H - p[1]
        z = max(h[int(min(p[1], H - 1)), int(min(p[0], W - 1))], 0) / 1000 * EXAG
        e = bpy.data.objects.new(name, None); e.empty_display_type = 'SINGLE_ARROW'; e.empty_display_size = 8
        e.location = (x, y, z); Mk.objects.link(e)
        e['wcs_x_km'], e['wcs_y_km'], e['elev_m'] = float(round(x, 1)), float(round(y, 1)), float(round(z / EXAG * 1000, 0))
        for k, v in props.items():
            e[k] = v
        return e
    loc('LOC_ASHRAM__position_PROPOSED', feats['ashram'], status='CONFIRMED location, PROPOSED position')
    for k, p in enumerate(feats['cities']):
        loc(f'LOC_C-{k + 1:02d}_city_site__PROPOSED', p)
    for k, p in enumerate(feats['villages']):
        loc(f'LOC_V-{k + 1:02d}_village__PROPOSED', p)
    for k, p in enumerate(feats['ruins']):
        loc(f'LOC_RU-{k + 1:02d}_ruins__PROPOSED', p)
    for k, p in enumerate(feats['caves']):
        loc(f'LOC_CV-{k + 1:02d}_cave__PROPOSED', p)
    for code, nm, p, st in feats['regions']:
        if p:
            loc(f'REGION_{code}_{nm.replace(" ", "_").replace("&", "and")}__PROPOSED', p)
    # ------------------------------------------------------------------ light / sky
    sc = bpy.context.scene
    ck.setup_render((1920, 1080), SAMPLES)
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = -0.35
    wd = bpy.data.worlds.new('WORLD_SKY'); sc.world = wd; wd.use_nodes = True
    sky = wd.node_tree.nodes.new('ShaderNodeTexSky')
    try:
        sky.sky_type = 'NISHITA'
    except Exception:
        pass
    try:
        sky.sun_elevation = math.radians(32); sky.sun_rotation = math.radians(200)
    except Exception:
        pass
    bg = wd.node_tree.nodes['Background']; wd.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = .22
    L = coll('WORLD_LIGHTS')
    sd = bpy.data.lights.new('WORLD_SUN', 'SUN'); sd.energy = 2.4; sd.angle = math.radians(1.5); sd.color = ck.hexlin('#FFF1DC')[:3]
    so = bpy.data.objects.new('WORLD_SUN', sd); so.rotation_euler = (math.radians(55), 0, math.radians(-35)); L.objects.link(so)
    # ------------------------------------------------------------------ cameras + renders
    Cm = coll('WORLD_CAMERAS')
    shots = []
    c = ck.camera('CAM_WORLD_AERIAL_SOUTH', Cm, (W * .5, -330, 420), (W * .5, H * .52, 0), lens=28)
    c.data.clip_end = 5000
    shots.append((c, 'AERIAL_world_south.png', (1920, 1080), 'Whole continent from the south (oblique aerial)'))
    for code, nm, p, st in feats['regions']:
        if not p:
            continue
        x, y = p[0], H - p[1]
        z = max(h[int(p[1]), int(p[0])], 0) / 1000 * EXAG
        cc = ck.camera(f'CAM_REGION_{code}', Cm, (x - 25, y - 140, z + 55), (x, y + 10, z), lens=32)
        cc.data.clip_end = 5000
        shots.append((cc, f'AERIAL_{code}.png', (960, 540), f'{code} {nm}'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BL, 'WORLD_overview_v001.blend'))
    for cam, fn, res, _ in shots:
        sc.render.resolution_x, sc.render.resolution_y = res
        ck.render_to(os.path.join(AER, fn), cam)
    sheet(shots, feats)


def sheet(shots, feats):
    F = lambda p, s: ImageFont.truetype(p, s)
    big = Image.open(os.path.join(AER, shots[0][1])).convert('RGB')
    tiles = shots[1:]
    cols = 4; tw, th = 600, 338
    rows = math.ceil(len(tiles) / cols)
    Wd = cols * (tw + 30) + 30
    bh = int(big.height * (Wd - 60) / big.width)
    S = Image.new('RGB', (Wd, 140 + bh + 40 + rows * (th + 80) + 40), (16, 18, 24))
    d = ImageDraw.Draw(S)
    d.text((30, 26), 'AERIAL GEOGRAPHICAL REFERENCES  ·  proposal v1', font=F(wg.FS, 46), fill=(240, 230, 205))
    d.text((30, 88), 'Renders of the real Blender overview terrain (WORLD_overview_v001.blend) · heights x3 · names = working labels',
           font=F(wg.FR, 22), fill=(170, 170, 180))
    S.paste(big.resize((Wd - 60, bh), Image.LANCZOS), (30, 140))
    d.text((44, 150), shots[0][3], font=F(wg.FB, 26), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    for k, (cam, fn, res, cap) in enumerate(tiles):
        im = Image.open(os.path.join(AER, fn)).convert('RGB').resize((tw, th), Image.LANCZOS)
        x = 30 + (k % cols) * (tw + 30); y = 140 + bh + 40 + (k // cols) * (th + 80)
        S.paste(im, (x, y)); d.text((x, y + th + 10), cap, font=F(wg.FB, 22), fill=(255, 214, 90) if 'R-01' in cap else (240, 230, 205))
    S.save(os.path.join(AER, 'AERIAL_sheet_v1.png'), optimize=True)
    print('wrote aerial sheet')


if __name__ == '__main__':
    main()

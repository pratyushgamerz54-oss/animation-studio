"""TASK 04 · contact sheets with captions (system python3 + Pillow) → 12_RENDER/SHEET_*.png"""
import os, json, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
R = os.path.join(ROOT, '12_RENDER')
log = json.load(open(os.path.join(R, 'render_log.json')))
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F = lambda p, s: ImageFont.truetype(p, s)


def sheet(name, title, sub, entries, cols=2, tw=900):
    if not entries:
        return
    ims = [Image.open(os.path.join(ROOT, e['file'])).convert('RGB') for e in entries]
    th = int(tw * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    pad, cap, head = 24, 58, 150
    W = cols * tw + (cols + 1) * pad; H = head + rows * (th + cap + pad) + pad
    S = Image.new('RGB', (W, H), (16, 17, 22)); d = ImageDraw.Draw(S)
    d.text((pad, 28), title, font=F(FB, 44), fill=(240, 228, 200))
    d.text((pad, 88), sub, font=F(FR, 21), fill=(175, 175, 185))
    d.text((W - pad, 118), 'PROPOSAL — NOT LOCKED · awaiting Director approval', font=F(FB, 22), fill=(255, 190, 70), anchor='ra')
    for k, (im, e) in enumerate(zip(ims, entries)):
        r, c = divmod(k, cols)
        x = pad + c * (tw + pad); y = head + r * (th + cap + pad)
        S.paste(im.resize((tw, th)), (x, y))
        tag = 'VIEWPORT (Workbench / Solid)' if e['mode'] == 'viewport' else 'RENDER (Cycles)'
        d.text((x, y + th + 8), f"{e['camera']}  ·  {tag}", font=F(FB, 18), fill=(255, 214, 120))
        d.text((x, y + th + 32), textwrap.shorten(e['desc'], 110), font=F(FR, 17), fill=(215, 215, 222))
    S.save(os.path.join(R, name), optimize=True)
    print('sheet', name, len(ims))


W_ = [e for e in log if e['scene'] == 'MAIN_WORLD']
V_ = [e for e in log if e['scene'] == 'ASHRAM_VALLEY']
D_ = [e for e in log if e['scene'].startswith('DIM_')]
sheet('SHEET_01_MAIN_WORLD_renders.png', 'MAIN WORLD — 3D BLOCKOUT · aerial previews',
      'Real 3D terrain from map v2 rev 01 · 1 BU = 1 km · relief ×20 · Blender 4.5 Cycles CPU · markers/labels hidden',
      [e for e in W_ if e['mode'] == 'cycles'])
sheet('SHEET_02_MAIN_WORLD_viewport.png', 'MAIN WORLD — viewport screenshots (Workbench = Solid viewport)',
      'Same file as the renders, with markers, labels, 1 000 km grid, range lines, Ashram-valley extents, cave zones (wire)',
      [e for e in W_ if e['mode'] == 'viewport'])
sheet('SHEET_03_ASHRAM_VALLEY.png', 'ASHRAM VALLEY — terrain blockout (true scale, 1 BU = 1 m)',
      'LOD0 ±3 km @12.5 m · LOD1 ±30 km @100 m · LOD2 ±160 km @1 km · rivers carved from the map flow network · Ashram = separate asset',
      [e for e in V_ if e['mode'] == 'cycles'] + [e for e in V_ if e['mode'] == 'viewport'])
sheet('SHEET_04_DIMENSIONS.png', 'SEPARATE DIMENSIONS — blockouts (own files, own space)',
      'Black Hole Training Area (MAP_H1) · Saithan’s Dark World (MAP_H2) · never merged with the main world · GEM: not confirmed → not built',
      D_)
print('SHEETS_DONE')

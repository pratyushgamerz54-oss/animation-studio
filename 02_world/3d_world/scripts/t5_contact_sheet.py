"""TASK 05 · contact sheet of the cinematic environment tests (python3 + Pillow).
python3 t5_contact_sheet.py [render_dir] [out.png]"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
rd = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '12_RENDER', 'T5', 'cycles')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, '12_RENDER', 'T5', 'T5_SHEET_01_CINEMATIC_TESTS.png')
log = json.load(open(os.path.join(ROOT, '12_RENDER', 'T5', 'render_log_t5.json'))) if os.path.exists(os.path.join(ROOT, '12_RENDER', 'T5', 'render_log_t5.json')) else {}
ORDER = [('CAM_T5_01_MOUNTAIN_WIDE', '1 · Wide mountain landscape'), ('CAM_T5_02_FOREST_ESTABLISHING', '2 · Forest establishing shot'),
         ('CAM_T5_03_RIVER_WATERFALL', '3 · River and waterfall'), ('CAM_T5_04_SNOWY_PEAKS', '4 · Snowy mountain'),
         (None, '5 · Desert landscape — PENDING (milestone 2: no desert in the milestone-1 area)'),
         ('CAM_T5_06_VALLEY_AERIAL', '6 · Valley aerial'), ('CAM_T5_07_GROUND_LEVEL', '7 · Ground level (valley meadow)'),
         ('CAM_T5_08_FOREST_FLOOR', '7b · Ground level (forest floor)')]
if os.environ.get('SHEET') == '2':
    ORDER = [('CAM_T5_05_DESERT', '5 · Desert landscape (R04)'), ('CAM_T5_05B_DESERT_MESAS_AERIAL', '5b · Desert aerial — dunes, mesas, playas'),
             ('CAM_T5_09_FORBIDDEN_RIM', '9 · Forbidden Region (R05) — crater rim'), ('CAM_T5_09B_FORBIDDEN_AERIAL', '9b · Forbidden Region aerial'),
             ('CAM_T5_10_ENCHANTED_FLOOR', '10 · Enchanted Forest (R02) — inside'), ('CAM_T5_10B_ENCHANTED_CANOPY', '10b · Enchanted Forest canopy'),
             ('CAM_T5_11_RANGE_PEAKS', '11 · Great Northern Range (R03) — summit'), ('CAM_T5_11B_RANGE_PANORAMA', '11b · Great Northern Range panorama'),
             ('CAM_T5_12_CAVE_ENTRANCE', '12 · Cave entrance (map cave marker)'), ('CAM_T5_W01_WORLD', 'W1 · Main world v002'),
             ('CAM_T5_W02_AETHERIA', 'W2 · Aetheria v002 — smooth lake shores'), ('CAM_T5_W03_COAST_ISLANDS', 'W3 · Coasts / islands v002')]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, '12_RENDER', 'T5', 'T5_SHEET_02_MILESTONE2.png')
W, H = 960, 540
try:
    F1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
    F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    F3 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19)
except Exception:
    F1 = F2 = F3 = ImageFont.load_default()
cols = 2; rows = (len(ORDER) + 1) // 2
sheet = Image.new('RGB', (cols * W + (cols + 1) * 20, rows * (H + 66) + 130), (16, 17, 22))
d = ImageDraw.Draw(sheet)
d.text((20, 18), 'TASK 05 · DETAILED TERRAIN & LANDSCAPE — ' + ('milestone 2: rest of the world' if os.environ.get('SHEET') == '2' else 'milestone 1 cinematic environment tests'), font=F1, fill=(240, 230, 210))
d.text((20, 62), 'Ashram Valley (2 m / 10 m / 40 m / 400 m LODs) · northern forest belt (2 m + real trees) · mountain region NW01 (30 m, erosion) '
       '+ waterfall gorge (1.5 m) · Poly Haven CC0 PBR · Blender 4.5 Cycles CPU preview', font=F2, fill=(190, 190, 200))
d.text((20, 88), 'True scale (1 BU = 1 m) · map revision 01 = PROPOSAL (not canon) · awaiting Director approval', font=F2, fill=(255, 200, 90))
for i, (cam, title) in enumerate(ORDER):
    x = 20 + (i % cols) * (W + 20); y = 130 + (i // cols) * (H + 66)
    p = os.path.join(rd, f'{cam}.png') if cam else None
    if p and os.path.exists(p):
        sheet.paste(Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS), (x, y))
    else:
        d.rectangle([x, y, x + W, y + H], fill=(40, 40, 48)); d.text((x + 30, y + H // 2 - 10), 'PENDING', font=F1, fill=(150, 150, 160))
    d.text((x, y + H + 6), title, font=F3, fill=(255, 212, 100))
    if cam and cam in log:
        L = log[cam]
        d.text((x, y + H + 32), f"{L['description'][:78]}…  ·  {L['res'][0]}×{L['res'][1]}, {L['samples']} spp, {L['seconds']:.0f} s",
               font=F2, fill=(185, 185, 195))
sheet.save(out)
print('SHEET', out)

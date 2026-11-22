"""Contact sheet of QC test renders (poses + lip-sync) → <folder>/qc/<ID>_qc_tests.png (visible in git; raw/ is ignored).
Run: python3 01_characters/_shared/qc_contact.py <folder> [...]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
POSES = ['deform_test', 'run', 'jump', 'land', 'turn', 'fight']
PH = ['REST', 'A', 'E', 'I', 'O', 'U', 'MBP', 'FV', 'L', 'W']

def main(folder):
    D = os.path.join(HERE, '..', folder); R = os.path.join(D, 'design', 'raw')
    W = 2400; pw, ph = 400, 475; lw, lh = 240, 274
    img = Image.new('RGB', (W, 90 + 40 + ph + 70 + lh + 60), (18, 20, 26)); d = ImageDraw.Draw(img)
    f1, f2 = ImageFont.truetype(F, 34), ImageFont.truetype(F, 20)
    d.text((30, 25), f'{folder.upper()} · QC test renders (production rig v003)', font=f1, fill='white')
    y = 110; d.text((30, y), 'Deformation + action poses', font=f2, fill=(90, 170, 255)); y += 30
    for i, p in enumerate(POSES):
        fp = os.path.join(R, f'test_{p}.png')
        if os.path.exists(fp):
            img.paste(Image.open(fp).convert('RGB').resize((pw, ph)), (i * pw, y))
        d.text((i * pw + 10, y + 8), p.upper().replace('_TEST', ''), font=f2, fill='white')
    y += ph + 30; d.text((30, y), 'Lip-sync phonemes', font=f2, fill=(90, 170, 255)); y += 30
    for i, p in enumerate(PH):
        fp = os.path.join(R, f'lipsync_PH_{p}.png')
        if os.path.exists(fp):
            img.paste(Image.open(fp).convert('RGB').resize((lw, lh)), (i * lw, y))
        d.text((i * lw + 8, y + 6), p, font=f2, fill='white')
    out = os.path.join(D, 'qc', f'{folder.upper()}_qc_tests.png'); img.save(out); print('wrote', out)

if __name__ == '__main__':
    for f in sys.argv[1:]: main(f)

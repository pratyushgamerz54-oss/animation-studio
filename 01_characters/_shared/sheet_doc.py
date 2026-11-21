"""Write <folder>/design/DESIGN_SHEET.md from the config + measured QC data.
Run:  python3 01_characters/_shared/sheet_doc.py <folder>
"""
import os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_char import load_cfg

POWER_TEXT = {
    'speed': ('Super Speed', 'Eyes glow, bracer/core brighten, short trails at the legs, sparks at the feet',
              'Long horizontal streaks from every limb + 2 tinted afterimages + crackle', 'Trails shrink, eyes fade'),
    'lightning': ('Lightning', 'Small arcs crawl over the hand', 'Branching bolt from the palm + arcs along the arms and body',
                  'Residual sparks at the fingertips'),
    'portal': ('Magical Portal', 'Portal opens at 25 % in front of the palm, rune ring on the hand',
               'Full swirl disc, white-hot rim, spark ring, portal light', 'Portal shrinks to 35 % and dims'),
    'corrupted_portal': ('Magical Portal (corrupted)', 'Small reverse-swirl portal, rune ring',
                         'Blood-red rim, black core, reverse swirl, smoke tongues around the rim', 'Shrinks and dims'),
    'fire': ('Fire', 'Flames lick from the fingertips', 'Fireball with flame tail from the palm + full-body fire aura',
             'Small embers on three fingers'),
    'dark_magic': ('Dark Magic', 'Violet-black wisps rise from both hands', 'Dense dark aura over the body, dark orb with crackle between the hands',
                   'Thin residual wisps'),
    'invisibility': ('Invisibility', 'Noise dissolve begins (35 % of the body turns to refractive glass)',
                     'Fully refractive body (IOR 1.03) with faint fresnel rim = distortion only', 'Reappears through the same dissolve (70 %)'),
    'laser': ('Laser', 'Charge orb + sparks at the palm, chest lenses glow', 'Perfectly straight beam: white core, coloured sheath and halo, impact burst',
              'Beam thins to a fading thread, no impact'),
    'laser_eyes': ('Laser (eyes)', 'Eyes flare, small charge points at both eyes', 'Two parallel straight beams from the eyes, impact burst',
                   'Beams thin to fading threads'),
    'teleport': ('Teleportation', 'Body-hugging light rings + spatial warp bubble', 'DEPARTURE: body breaks into glowing motes inside the rings',
                 'ARRIVAL: motes reassemble the body with a ground ring'),
}


def rgb(h):
    h = h.lstrip('#'); return ', '.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def main(folder):
    C, D = load_cfg(folder)
    q = os.path.join(D, 'qc')
    M = json.load(open(os.path.join(q, 'measurements.json'))) if os.path.exists(os.path.join(q, 'measurements.json')) else {}
    Q = json.load(open(os.path.join(q, 'qc.json'))) if os.path.exists(os.path.join(q, 'qc.json')) else {}
    pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(D, 'design', f"{C['id']}_sheet_*.png")))
    L = [f"# {C['name'].upper()} — {C['role']} — Design Sheet v1 (APPROVED 20 Nov)", '',
         '> **Status: design APPROVED by the Director (20 Nov).** Confirmed: ' +
         f"name ({C['name']}), role, powers "
         f"({', '.join(C['powers']) or 'NOT CONFIRMED — no power VFX made'}), the reference and the full design.", '',
         '## Sheet pages (renders of the real Blender model)', '']
    L += [f'- `{p}`' for p in pages] or ['- (not rendered yet)']
    L += ['', '## Reference interpretation', '', f"Reference: `{C['reference']}`", '', C['ref_notes'], '',
          '## Identity (proposal)', '', f"- Age: {C['age']}", f"- Build: {C['body_type']}", f"- Silhouette: {C['silhouette']}", '',
          '## Colour palette (same values drive the 3D materials)', '', '| Name | HEX | RGB |', '|---|---|---|']
    L += [f'| {k} | `{v}` | {rgb(v)} |' for k, v in C['pal'].items()]
    L += ['', '## Costume & accessories breakdown', '', '| Item | Parts (objects) | Fabric | Material | Simulation |', '|---|---|---|---|---|']
    L += [f"| {lab} | {', '.join('CHAR_' + C['id'] + '_' + p for p in parts)} | {fab} | {mat} | {sim} |"
          for k, lab, parts, fab, mat, sim in C['costume_groups']]
    L += ['', '## Face', '']
    L += [f'- **{k}:** {v}' for k, v in C.get('face_notes', [])]
    L += ['', f"Expressions ({len(C['expressions'])}): {', '.join(C['expressions'])}",
          'Phonemes: A, E, I, O, U, M/B/P, F/V, L, W, Rest (shape keys on CHAR_' + C['id'] + '_MOUTH)', '',
          '## Body proportions (measured on the model, `qc/measurements.json`)', '']
    if M:
        for k, v in M.items():
            if k.endswith('_m'):
                L.append(f"- {k[:-2].replace('_', ' ')}: {v * 100:.1f} cm")
            elif k == 'heads_tall':
                L.append(f'- head-to-body ratio: {v} heads')
    L += ['', '## Powers', '']
    if C.get('power_rows'):
        L += ['| Power | Normal | Activation | Full | Deactivation |', '|---|---|---|---|---|']
        for k in C['power_rows']:
            t = POWER_TEXT[k]
            L.append(f'| {t[0]} | no effect | {t[1]} | {t[2]} | {t[3]} |')
        L += ['', 'Eye transformation: iris emission ramps normal → activation → full (shared by all powers).',
              'Reusable VFX functions live in `../../_shared/vfxkit.py` (intensity / openness / length parameters).']
    else:
        L.append('**Powers NOT CONFIRMED** — no power activation effects, attacks or energy VFX were created (by instruction).')
    if C.get('cost_alts'):
        L += ['', '## Borrowed-power life cost (story mechanic) — APPROVED: all three are used (Director 20 Nov)', '',
              '- **A · Fracture veins:** glowing red cracks spread across the skin; more borrowing = more cracks.',
              '- **B · Ash drain:** skin greys to ash and the eyes dim while a borrowed power runs.',
              '- **C · Core siphon:** energy is visibly pulled out of his chest core; the core dims and flickers.',
              '- **A + B + C · Full cost:** all three together (rendered on sheet page 8).',
              '', 'Proposed escalation (to confirm when scripting scenes): small borrow = C, longer = C + A, heavy = + B, extreme = all three.']
    L += ['', '## Technical 3D specification', '',
          '- Topology: all-quad body cage (skin modifier + subdivision) with ring edge loops at every joint; code sculpt pass for anatomy; '
          'all-quad head (sculpted sphere, 26 cuts) with jawline, brow ridge, nose, philtrum, nasolabial folds.',
          '- Hands: 5 fingers × 3 segments; feet with heel/ball/toe.',
          '- Clothing: separate meshes generated from the body surface (offset + solidify) → exact fit; robes/capes are lofted sheets.',
          '- UVs: smart-projected per mesh; layouts in `uv/`. Textures: baked BaseColor / Roughness / Normal / Emission in `textures/`.',
          '- Rig: deform skeleton (pelvis, 3 spine, neck, head, clavicles, arms, 15 finger bones per hand, legs, feet, toes) + '
          'root, COG, hand/foot IK targets with pole targets and IK/FK switches; eye-aim control.',
          '- **Rigify animation rig** (`blend/<name>_v004_rigify.blend`): IK/FK arms + legs, foot roll, torso/hips/chest, '
          'neck/head follow, finger curls, jaw + eye-aim controls, robe/skirt chain controls; same face controls on `root`.',
          '- Facial rig: shape keys for every expression + 10 phonemes, `jaw_open`, blink / wide-eye per side, eye look; all driven by '
          'properties on the `root` pose bone.', '',
          '## Production status', '']
    if Q:
        L.append('See `qc/QC_REPORT.md` for the automated checks and test renders.')
        L.append(f"- `.blend`: `blend/{folder}_v002.blend` (design), `blend/{folder}_v003.blend` (game/export rig + controls), "
                 f"`blend/{folder}_v004_rigify.blend` (Rigify animation rig — use this for animation)")
        ex = Q.get('tests', {}).get('export', {})
        L.append(f"- Exports: `export/{folder}.glb` ({ex.get('glb_mb', '?')} MB), `export/{folder}.fbx` ({ex.get('fbx_mb', '?')} MB)")
    else:
        L.append('- Production stage not run yet.')
    L += ['', '## Known limitations', '', '- Faces are stylised and code-sculpted; close-up photoreal detail needs a manual sculpt pass.',
          '- Robes / skirts use a 12-chain follow rig (no stiff tube); a cloth simulation pass is still recommended for final shots.']
    open(os.path.join(D, 'design', 'DESIGN_SHEET.md'), 'w').write('\n'.join(L) + '\n')
    print('wrote', os.path.join(D, 'design', 'DESIGN_SHEET.md'))


if __name__ == '__main__':
    for f in sys.argv[1:]:
        main(f)

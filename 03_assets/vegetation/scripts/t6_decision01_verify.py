"""Decision Sheet 01 §8 · automated verification → 02_world/ecosystem/DECISION_SHEET_01_VERIFICATION.md
Checks: region IDs vs Map Revision 01 data · Ashram planting consistency · Sky Realms not a dimension · subtle fantasy glow ·
Spring consistency · wildlife not finalized."""
import os, re, json, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
W = lambda *a: os.path.join(ROOT, *a)
R = []
def chk(name, ok, detail=''):
    R.append((name, bool(ok), str(detail))); print('PASS' if ok else 'FAIL', name, detail)

DOCS = [W('02_world', 'WORLD_BIBLE.md'), W('02_world', 'map_v2', 'GEOGRAPHY.md'), W('02_world', 'ecosystem', 'ECOSYSTEM_BIBLE.md'),
        W('02_world', 'ecosystem', 'DECISION_SHEET_01.md'), W('02_world', 'ecosystem', 'ENCHANTED_FOREST_VEGETATION_REFERENCE.md'),
        W('02_world', 'ecosystem', 'SEASON_REFERENCE_SPRING.md'), W('02_world', 'ecosystem', 'WILDLIFE_SELECTION_SHEET.md'),
        W('02_world', 'ecosystem', 'BLENDER45_ENV_PRODUCTION_CHECKLIST.md'), W('02_world', 'ashram', 'ASHRAM_LANDSCAPING_PLAN.md')]
for d in DOCS:
    chk(f'document exists: {os.path.relpath(d, ROOT)}', os.path.exists(d))
TXT = {d: open(d).read() for d in DOCS if os.path.exists(d)}

# 1. region IDs vs Map Revision 01 (both data files)
wf = json.load(open(W('02_world', '3d_world', '01_GEOGRAPHY', 'data', 'world_features.json')))
fj = json.load(open(W('02_world', 'map_v2', 'data', 'features.json')))
names = {r[0]: r[1] for r in wf['c1_regions']}; names2 = {r[0]: r[1] for r in fj['c1_regions']}
for code, nm in (('R-03', 'Great Northern Range'), ('R-06', 'Southern Grasslands'), ('R-08', 'Lake District')):
    chk(f'{code} = {nm} in Map Rev 01 (world_features.json + features.json)', names.get(code) == nm and names2.get(code) == nm, names.get(code))
chk('C-01, C-02, C-03 exist in Map Rev 01 (features.json c1_city_codes)', fj['c1_city_codes'] == ['C-01', 'C-02', 'C-03'], fj['c1_city_codes'])
c1c = [c for c in wf['markers']['cities'] if c[3] == 'C1']
chk('three C1 city sites in world_features.json (C-01…C-03 = separate sites)', len(c1c) == 3, [tuple(round(x, 1) for x in c[:2]) for c in c1c])
bad = []
for d, t in TXT.items():
    for m in re.finditer(r'R-0([1-8])[ *]*\**\s*([A-Z][A-Za-z &]+)', t):
        code = 'R-0' + m.group(1); nm = m.group(2).strip()
        ref = names[code]
        if nm.split()[0] in ('Great', 'Southern', 'Lake', 'Ashram', 'Enchanted', 'Western', 'Forbidden', 'Eastern') and not ref.startswith(nm.split()[0]):
            bad.append(f'{os.path.basename(d)}: {code} {nm}')
chk('no region ID paired with a wrong region name in the updated documents', not bad, bad[:5])
for d in (DOCS[0], DOCS[1], DOCS[2]):
    t = TXT.get(d, '')
    chk(f'approved mapping recorded in {os.path.basename(d)}', all(k in t for k in ('R-03', 'R-06', 'R-08', 'C-01', 'C-02', 'C-03')) and 'APPROVED' in t)

# 2. Sky Realms not a dimension
lines = [(os.path.basename(d), l.replace('*', '')) for d, t in TXT.items() for l in t.splitlines() if 'Sky Realm' in l]
wrong = [l for f, l in lines if re.search(r'dimension', l, re.I) and not re.search(r'not (a|as a) (separate )?dimension|NOT a dimension|not a separate dimension|— not a', l, re.I)]
chk('Sky Realms never categorised as a separate dimension', not wrong, wrong[:3])
chk('Sky Realms marked PROPOSED region of the main world', any('PROPOSED' in l and ('main world' in l or 'region' in l.lower()) for f, l in lines), f'{len(lines)} lines mention Sky Realms')
chk('no Sky Realms routes / inhabitants / kingdoms established', all(not re.search(r'(route|inhabitant|kingdom|king|ruler)s? (is|are|=)', l, re.I) for f, l in lines))

# 3. Ashram planting
sp = open(W('03_assets', 'vegetation', 'scripts', 't6_species.py')).read(); pl = open(W('03_assets', 'vegetation', 'scripts', 't6_plants.py')).read()
chk('Tulsi habitat = Ashram garden only', 'ONLY in the Ashram garden' in sp.split("name='AV_S02_TULSI'")[1][:900])
m = pl.split("name='AV_F04_MARIGOLD'")[1][:400]
chk('Marigold region = Ashram gardens only', 'Ashram garden' in m, m[:120].replace('\n', ' '))
chk('Peepal habitat = ONE landmark at the Ashram courtyard', 'ONE landmark Peepal in the Ashram main courtyard' in sp)
scat = [f for f in glob.glob(W('**', '*.py'), recursive=True) if 'scatter' in open(f, errors='ignore').read().lower()
        and re.search(r'TULSI|MARIGOLD', open(f, errors='ignore').read()) and 't6_' not in os.path.basename(f)]
chk('no scatter recipe uses Tulsi / Marigold outside the Ashram garden', not scat, scat)
chk('landscaping plan image exists', os.path.exists(W('02_world', 'ashram', '00_REFERENCE', 'ASHRAM_landscaping_plan_v1.png')))

# 4. subtle glow (built libraries, from the QC json of Blender 4.5)
qj = W('03_assets', 'vegetation', 'qc', 't6_qc_4.5.16.json')
if os.path.exists(qj):
    q = json.load(open(qj))['results']; g = [r for r in q if 'glow subtle' in r['check']]
    chk('fantasy glow subtle in the built libraries (all emission ≤ 1.0)', g and all(r['ok'] for r in g), f'{sum(r["ok"] for r in g)}/{len(g)} assets')
    lab = [r for r in q if 'label set' in r['check']]
    chk('fantasy labels updated in the built libraries', lab and all(r['ok'] for r in lab), f'{sum(r["ok"] for r in lab)}/{len(lab)}')

# 5. Spring
aut = [(os.path.basename(d), l.strip()[:90]) for d, t in TXT.items() for l in t.splitlines()
       if re.search(r'autumn', l, re.I) and not re.search(r'not|no plumes|autumn look|autumn feature|autumn colour|plumed|NOT', l)]
chk('no document presents autumn as the film season', not aut, aut[:3])
chk('Spring recorded as the primary season in the bible + season reference',
    'Spring' in TXT.get(DOCS[2], '') and 'primary season' in TXT.get(DOCS[5], ''))
chk('regional sheets state SEASON: SPRING', 'SEASON: SPRING' in open(W('03_assets', 'vegetation', 'scripts', 't6_compose_sheets.py')).read())

# 6. wildlife not finalized
ws = TXT.get(DOCS[6], '')
chk('wildlife selection sheet = PENDING, nothing finalized', 'PENDING' in ws and '☑' not in ws and 'Nothing here is selected or final' in ws)
inv = {}
for f in glob.glob(W('03_assets', 'vegetation', 'library', '*_inventory.json')):
    inv.update(json.load(open(f)))
animals = [n for n, v in inv.items() if v.get('kind') not in ('tree', 'shrub', 'plant')]
chk('no wildlife 3D assets created', not animals and not glob.glob(W('03_assets', '**', '*wildlife*.blend'), recursive=True), animals)

n = len(R); p = sum(ok for _, ok, _ in R)
L = ['# DECISION SHEET 01 — VERIFICATION REPORT (automated)', '', f'Script: `03_assets/vegetation/scripts/t6_decision01_verify.py` · **{p}/{n} PASS**', '',
     '| # | check | result | detail |', '|---|---|---|---|']
L += [f'| {i} | {c} | {"✅ PASS" if ok else "❌ FAIL"} | {str(d).replace("|", "/")[:160]} |' for i, (c, ok, d) in enumerate(R, 1)]
open(W('02_world', 'ecosystem', 'DECISION_SHEET_01_VERIFICATION.md'), 'w').write('\n'.join(L) + '\n')
print(f'VERIFY {p}/{n}')

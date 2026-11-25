"""Build motion_test_v2.html: the user's CH02–CH10 rigs (+ provisional Aarav, same recipe as day2/build.py) + motion_v2.js + a 24 s test scene."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "upload_sheets_v01"
FOLDERS = {"meera": "CH02_DrMeera", "kabir": "CH03_Kabir", "zoya": "CH04_Zoya", "ryan": "CH05_Ryan", "ananya": "CH06_Ananya",
           "dev": "CH07_Dev", "ishaan": "CH08_Ishaan", "sara": "CH09_Sara", "vikram": "CH10_Vikram"}
def load(folder):
    d = SRC / folder; rig = json.loads(next(d.glob("*_rig_v01.json")).read_text()); parts = {}
    for p in rig["parts"]:
        name = "mouth" if p["name"].startswith("mouth") else p["name"]; svg = (d / p["file"]).read_text()
        if re.search(r"<script|javascript:|on\w+=|<foreignObject", svg, re.I): sys.exit(f"unsafe svg {folder}/{p['file']}")
        parts[name] = {"svg": svg, "pivot": p["pivot"]}
    return parts
def recolor(svg, m):
    for a, b in m.items(): svg = re.sub(a, b, svg, flags=re.I)
    return svg
rigs = {k: load(f) for k, f in FOLDERS.items()}
HEAD = {"#462f28": "#171313", "#5b3a24": "#241e1e", "#c98f65": "#b27c55", "#8d6652": "#8a5f40", "#7a5943": "#6a4b38"}
BODY = {"#5a6b3a": "#2c4270", "#454e36": "#1e2d4d", "#3b4432": "#24365a", "#1f2a1f": "#141e36", "#3d3a33": "#5a5d64", "#322f32": "#45484f",
        "#5b4a36": "#6e6253", "#463933": "#52493d", "#3b2a1e": "#3e2c22", "#322424": "#2c1f18", "#a8724f": "#b27c55", "#785344": "#8a5f40"}
aarav = {n: {"svg": recolor(rigs["kabir"][n]["svg"], HEAD), "pivot": rigs["kabir"][n]["pivot"]} for n in ("hair_back", "head", "hair_front", "eye_L", "eye_R", "brow_L", "mouth")}
aarav.update({n: {"svg": recolor(rigs["dev"][n]["svg"], BODY), "pivot": rigs["dev"][n]["pivot"]} for n in ("torso", "pelvis", "upper_arm", "forearm", "hand", "thigh", "shin", "foot")})
rigs["aarav"] = aarav
import collections
def dominant(svg):
    c = collections.Counter(x.lower() for x in re.findall(r'fill="(#[0-9a-fA-F]{6})"', svg) if x.lower() not in ("#2b2321", "#1b1824"))
    return c.most_common(1)[0][0] if c else "#444444"
for k, parts in rigs.items(): parts["_colors"] = {"top": dominant(parts["torso"]["svg"]), "hair": dominant(parts["hair_back"]["svg"])}
html = (HERE / sys.argv[1]).read_text()
html = html.replace("/*__RIGS__*/null", json.dumps(rigs, separators=(",", ":"))).replace("/*__MOTION__*/", (HERE / sys.argv[2]).read_text())
(HERE / sys.argv[3]).write_text(html, encoding="utf-8"); print(sys.argv[3], len(html) // 1024, "KB")

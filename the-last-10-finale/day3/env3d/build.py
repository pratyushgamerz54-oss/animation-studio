"""Prepare the 3D environment test: rigs.json (+ colours), motion_v3.js and zeno3d.js copied next to test.html."""
import json, re, sys, shutil, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent; M = HERE.parent / "motion"
sys.argv = ["x", "motion_test3_template.html", "motion_v3.js", "_unused.html"]
src = (M / "build_test.py").read_text().split("html = (HERE / sys.argv[1])")[0].replace('HERE = Path(__file__).resolve().parent', f'HERE = Path({str(M)!r})')
g = {}; exec(src, g)
(HERE / "rigs.json").write_text(json.dumps(g["rigs"], separators=(",", ":")))
shutil.copy(M / "motion_v3.js", HERE / "motion_v3.js"); shutil.copy(HERE.parent / "zeno3d.js", HERE / "zeno3d.js")
print("rigs.json", (HERE / "rigs.json").stat().st_size // 1024, "KB")

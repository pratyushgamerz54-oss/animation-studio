import html, subprocess, sys
from pathlib import Path
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
import importlib
M = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else 'day3_data')
PRE = sys.argv[2] if len(sys.argv) > 2 else 'THE_LAST_10_DAY03'
TITLE, DUR, CAST, SCENES, SHOTS, LINES = M.TITLE, M.DUR, M.CAST, M.SCENES, M.SHOTS, M.LINES
FIN = hasattr(M, 'LOGLINE')
FINNOTES = """<h3 class=break>Production notes (v006 standard + finale ke naye hisse)</h3><ul>
<li>Characters sirf aapki sheets/rigs se; Aarav provisional. Sab 10 bolte hain.</li>
<li>Har din ki shuruaat mein chhota DAY card (Day 3 … Day 10). Shorts ke liye har day-chapter alag clip ban sakta hai; long form = poora 8:00.</li>
<li>Back view jab chalte, front view jab baat karte (transition → half-body → full). Koi jhatke ka cut ya camera jhool nahi; Day 9 ka tez intercut bhi smooth.</li>
<li>Naye sets: lab corridor, highway + raat ka camp, toota flyover, baarish wali sadak, vishal dam (bahar + andar turbines), alien node, daraar ka centre, subah ki dhoop.</li>
<li>Naye props/FX: data drive, flare, pul ke charges, power cable, hologram (Earth + cube + ships), cyan-safed surge, ships ka door phenka jaana, bunker screen 100%.</li>
<li><b>Story decisions (confirm karein):</b> (1) Vikram pul ke saath girta hai par Day 10 mein zinda lautta hai. (2) Twist: Tesseract pinjra nahi, kavach hai. (3) Ryan ki pichhli crew ke gaayab hone ka raaz khula chhoda hai. (4) End: EARTH: ZERO → EARTH: ONE · THE END.</li>
<li>8 din ek 8 minute mein hain, isliye har din ~45–60 s ka hai; timing voices ke hisaab se adjust hogi.</li></ul>"""

e = html.escape
tc = lambda s: f"{int(s // 60):02d}:{s % 60:04.1f}"
est = lambda x: max(1.2, len(x) / 12.5)  # rough Hindi speaking speed

# ---- sanity checks: shots tile 0..DUR, lines inside their shot, no overlap
assert SHOTS[0][2] == 0 and SHOTS[-1][3] == DUR
for a, b in zip(SHOTS, SHOTS[1:]): assert a[3] == b[2], (a[0], b[0])
shot_of = {s[0]: s for s in SHOTS}
warn = []
for i, (t, who, x, n, sh) in enumerate(LINES):
    s = shot_of[sh]; end = t + est(x)
    if not (s[2] <= t < s[3]): warn.append(f"{who} {t} outside {sh}")
    if i + 1 < len(LINES) and end > LINES[i + 1][0]: warn.append(f"{who} {t} may overlap next ({end:.1f} > {LINES[i+1][0]})")
print("\n".join(warn) or "timing ok")

CSS = """@page { size: A4; margin: 15mm 13mm; }
body { font-family: "Noto Sans", "Noto Sans Devanagari", sans-serif; color:#1D1C22; font-size: 10pt; }
h1 { font-size: 20pt; margin: 0; letter-spacing:.03em } h1 span { color:#B3261E }
.sub { color:#5E5D66; margin: 4px 0 14px }
h2 { font-size: 13.5pt; border-left: 5px solid #B3261E; padding-left: 8px; margin: 18px 0 6px } h2 small { color:#5E5D66; font-weight:500; font-size: 9.5pt }
h3 { font-size: 12pt; margin: 14px 0 6px }
table { border-collapse: collapse; width: 100%; } th, td { text-align: left; padding: 4px 5px; vertical-align: top; }
th { font-size: 8pt; color:#5E5D66; border-bottom: 1.5px solid #1D1C22 }
tr:not(.note) td { border-top: 1px solid #D8D7DC } tr.note td { color:#5E5D66; font-size: 8.8pt; padding-top: 0 }
.dl { font-family: "Noto Sans Devanagari", "Noto Sans", sans-serif; font-size: 11.5pt; font-weight: 600 }
.tc, .n { font-variant-numeric: tabular-nums; white-space: nowrap } .fn { font-family: monospace; font-size: 8.5pt; white-space: nowrap }
.box { border:1px solid #D8D7DC; border-radius:6px; padding: 8px 12px; background:#F7F7F8 } ul { margin: 4px 0; padding-left: 18px }
.break { break-before: page } h2 { break-after: avoid } tr { break-inside: avoid }
.who { font-weight: 700 } .act { color:#3A3940 } .snd { color:#1F5F7A; font-size: 9pt } .cam { font-size: 9pt }
"""

def pdf(name, body):
    h = OUT / f"{name}.html"
    h.write_text(f"<!doctype html><html lang=hi><head><meta charset=utf-8><style>{CSS}</style></head><body>{body}</body></html>", encoding="utf-8")
    subprocess.run(["node", "-e", f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{h}');await p.pdf({{path:'{OUT / (name + ".pdf")}',format:'A4',printBackground:true}});await b.close();}})()"""], check=True)
    print("pdf", name)

# file names per character, in story order
count, fname = {}, {}
for i, (t, who, *_rest) in enumerate(LINES):
    count[who] = count.get(who, 0) + 1; fname[i] = f"{CAST[who][2]}_{count[who]:02d}.wav"

# ================= 1. Script + storyboard =================
parts = [(f"""<h1>THE LAST 10 — EARTH: ZERO · <span>{e(TITLE)}</span></h1><div class=sub>Series finale · script + storyboard · {M.SERIES_LINE} · {len(SHOTS)} shots · {len(LINES)} lines · sab 10 characters bolte hain</div><div class=box><b>Logline:</b> {M.LOGLINE}<br><b>Emotional core:</b> {e(M.CORE)}<br><b>Hooks:</b> {e(M.HOOKS)}<br><b>Continuity:</b> wahi characters (aapki sheets), wahi duniya, v006 style + checklist. Day 2 ki aakhri line \"वो हमें ढूंढ रहे हैं...\" ke turant baad shuru.</div>""" if FIN else f"""<h1>THE LAST 10 — EARTH: ZERO · <span>{e(TITLE)}</span></h1>
<div class=sub>Episode script + storyboard · runtime 8:00 · {len(SCENES)} scenes · {len(SHOTS)} shots · {len(LINES)} lines · sab 10 characters bolte hain</div>
<div class=box><b>Logline:</b> Lab mein ship ki search-light se bach kar teeno Sector 07 ka data lekar bhaagte hain. Bhaagte waqt Kabir ghayal ho jaata hai.
Bunker ko pata chalta hai ki Sector 07 sirf bahar nikalne ka rasta nahi, shayad "unka" darwaza bhi hai. Aarav faisla karta hai ki sab saath jaayenge.
Raat ko Ryan ek aisa raaz kholta hai jo sab badal deta hai: wo is ship ko pehle dekh chuka hai.
<br><b>Emotional core:</b> "Baad mein" — jo hum taal dete hain, wo kabhi nahi aata. Isliye ab koi peeche nahi chhootega.
<br><b>Hooks:</b> shuru = chhupna + girti test tube · beech = "ये उनका दरवाज़ा भी हो सकता है" · aakhir = Ryan ka raaz → DAY 3 / NO WAY BACK. → DAY 4 teaser.
<br><b>Continuity (Day 2 se):</b> wahi characters (aapki sheets), wahi duniya, v006 style + checklist. Day 2 ki aakhri line "वो हमें ढूंढ रहे हैं..." ke turant baad shuru.</div>""")]
for no, name, loc, mood, grade in SCENES:
    shots = [s for s in SHOTS if s[1] == no]
    rows = []
    for sid, _, a, b, cam, act, tr, snd in shots:
        dl = "".join(f"<div><span class=who style='color:{CAST[w][3]}'>{e(w)}</span> <span class=tc>({tc(t)})</span>: <span class=dl>{e(x)}</span><br><i class=act>{e(n)}</i></div>"
                     for t, w, x, n, s in LINES if s == sid)
        rows.append(f"<tr><td class=n><b>{sid}</b></td><td class=tc>{tc(a)}<br>–{tc(b)}<br><small>{b - a:.0f}s</small></td><td class=cam>{e(cam)}</td>"
                    f"<td><div class=act>{e(act)}</div>{dl}</td><td class=snd>{e(snd)}</td><td class=cam>{e(tr)}</td></tr>")
    a0, b0 = shots[0][2], shots[-1][3]
    parts.append(f"""<div class=scene><h2>{'' if FIN else f'Scene {no} · '}{e(name)} <small>{tc(a0)}–{tc(b0)} · {e(loc)} · Mood: {e(mood)} · Grade: {e(grade)}</small></h2>
<table><tr><th>Shot</th><th>Time</th><th>Frame / camera</th><th>Action + dialogue</th><th>Sound</th><th>Transition</th></tr>{''.join(rows)}</table></div>""")
parts.append(getattr(M, "NOTES", FINNOTES) if FIN else """<h3 class=break>Production notes (v006 standard + Day 3 ke naye hisse)</h3><ul>
<li>Characters sirf aapki sheets/rigs se. Aarav provisional (jaisa Day 2 mein). Ryan, Ananya, Dev, Ishaan, Vikram pehli baar bolte hain.</li>
<li>Back view jab chalte hain, front view jab baat karte hain (transition → half-body → full). Koi beech mein nahi rukta jab tak script na kahe.</li>
<li>Naye sets: Lab ka peeche wala corridor + girti chhat, tooti metro entrance (aag ke saath), raat ka 3D sheher, bunker raat mode.</li>
<li>Naye props: data drive, Zoya ka headset, Ananya ka camera viewfinder POV, Kabir ke pair par patti, Ryan ka mission patch close-up.</li>
<li><b>Story decision (confirm karein):</b> Ryan ke jacket patch ka nishaan ship ke hull jaisa dikhaya gaya hai. Sheet mein patch ka design "proposal" tha.</li>
<li>Cold open mein dialogue nahi, sirf mahaul + SFX (Day 2 rule). Impact ke baad poori khamoshi.</li>
<li>Timings andaaze hain; voices aane ke baad shots aapki recording ke hisaab se adjust honge (8:00 ke aas-paas rahega).</li></ul>""")
pdf(PRE + "_script_storyboard", "".join(parts))

# ================= 2. Voice recording script =================
order = [w for w in CAST if any(l[1] == w for l in LINES)]
secs = []
for who in order:
    code, role, pre, col = CAST[who]
    idx = [i for i, l in enumerate(LINES) if l[1] == who]
    tr = "".join(f"<tr><td class=n>{k}</td><td class=tc>{tc(LINES[i][0])}</td><td>{'Day' if FIN else 'Sc'} {shot_of[LINES[i][4]][1]}</td><td class=dl>{e(LINES[i][2])}</td>"
                 f"<td class=tc>~{est(LINES[i][2]):.1f}s</td><td class=fn>{fname[i]}</td></tr><tr class=note><td></td><td colspan=5>Direction: {e(LINES[i][3])}</td></tr>"
                 for k, i in enumerate(idx, 1))
    secs.append(f"""<section class=scene><h2 style="border-color:{col}"><span style="color:{col}">{code}</span> {e(who)} <small>{role} · {len(idx)} lines</small></h2>
<table><tr><th>#</th><th>Time</th><th>Scene</th><th>Line</th><th>Length</th><th>File name</th></tr>{tr}</table></section>""")
allrows = "".join(f"<tr><td class=tc>{tc(t)}</td><td>{e(w)}</td><td class=dl>{e(x)}</td><td class=fn>{fname[i]}</td></tr>" for i, (t, w, x, n, s) in enumerate(LINES))
pdf(PRE + "_voice_script", f"""<h1>THE LAST 10 — <span>{e(TITLE)}</span></h1>
<div class=sub>{"Series finale · " if FIN else ""}Voice recording script · {len(LINES)} lines · {len(order)} characters</div>
<div class=box><b>Recording notes</b><ul>
<li>Har line alag file mein, diye gaye naam se (jaise <code>aarav_01.wav</code>). WAV ya MP3 dono chalega.</li>
<li>Shaant kamra, koi background awaaz ya music nahi. Line se pehle aur baad ~0.5 s khamoshi.</li>
<li>"Direction" emotion ke liye hai: Day 3 mein dard, yaadein aur rahat zyada hai, dheere aur dil se bolo. Pause wahi lo jahan "..." hai.</li>
<li>Radio wali lines (Meera, Aarav, Sara Scene 3–4 mein) normal record karo; radio effect mix mein lagega.</li>
<li>"Length" andaaza hai; video aapki recording ke hisaab se adjust hoga.</li></ul></div>
{''.join(secs)}<h3 class=break>Saari lines story order mein</h3><table><tr><th>Time</th><th>Character</th><th>Line</th><th>File</th></tr>{allrows}</table>""")

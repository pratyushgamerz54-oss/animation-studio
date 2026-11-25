"""Split each '<who>_all_voices.mp3' into its v5 lines (cut at the N-1 longest silences), copy the per-line files,
and check every v5 line has audio whose length fits its text. Writes voices_v5/<file>.wav (48 kHz mono) + report."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import day3_10_v5_data as M
IN = ROOT / "voices_in_v4"; OUT = ROOT / "voices_v5"; OUT.mkdir(exist_ok=True)
SR = 48000

def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()
def write(p, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(p)], input=x.astype(np.float32).tobytes(), check=True)
def env(x, hop=480):  # 10 ms RMS in dB
    n = len(x) // hop; f = x[:n * hop].reshape(n, hop); return 20 * np.log10(np.sqrt((f ** 2).mean(1)) + 1e-9)
def speech_bounds(x, thr):
    e = env(x); on = np.where(e > thr)[0]
    return (on[0] * 480, (on[-1] + 1) * 480) if len(on) else (0, len(x))
def trim(x, pad=0.12):
    e = env(x); thr = max(e.max() - 45, -60); a, b = speech_bounds(x, thr)
    a = max(0, a - int(pad * SR)); b = min(len(x), b + int(pad * SR)); y = x[a:b].copy()
    f = int(0.01 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y

# expected lines per character, in v5 order, with file names as in the voice script
names, count = [], {}
for t, who, x, n, s in M.LINES:
    count[who] = count.get(who, 0) + 1; names.append((f"{M.CAST[who][2]}_{count[who]:02d}", who, x))
est = lambda x: max(0.9, len(re.sub(r"\(.*?\)", "", x)) / 12.5 + x.count("...") * 0.35)

COMBINED = {"Dev": "dev_all_voices.mp3", "Vikram": "Vikram_all_voices.mp3", "Zeno Commander": "Zeno_Commander_all_voices.mp3", "Ryan": "ryan_all_voices.mp3",
            "Ananya": "ananya_all_voices.mp3", "Sara": "sara_all_voices.mp3", "Ishaan": "ishaan_all_voices.mp3"}
report = {"split": {}, "lines": []}
STT = json.load(open(HERE / "stt_spans.json")) if (HERE / "stt_spans.json").exists() else {}
for who, fn in COMBINED.items():
    x = decode(IN / "combined" / fn); want = [n for n in names if n[1] == who]; N = len(want)
    e = env(x); thr = max(e.max() - 40, -55); voiced = e > thr
    # silent runs (≥ 0.2 s) strictly inside the speech
    runs, i = [], 0
    first, last = np.argmax(voiced), len(voiced) - np.argmax(voiced[::-1])
    i = first
    while i < last:
        if not voiced[i]:
            j = i
            while j < last and not voiced[j]: j += 1
            if j - i >= 20: runs.append((j - i, i, j))
            i = j
        else: i += 1
    # choose N-1 cut gaps by dynamic programming: segment speech length should follow text length, prefer longer gaps
    runs.sort(key=lambda r: r[1]); C = len(runs)
    vc = np.concatenate([[0], np.cumsum(voiced)])          # voiced frames prefix sum
    ests = np.array([est(t) for _, _, t in want]); total = vc[last] - vc[first]; tgt = ests / ests.sum() * total
    mids = [first] + [(a + b) // 2 for _, a, b in runs] + [last]
    glen = [0] + [r[0] for r in runs] + [0]
    INF = 1e18; best = [[INF] * (C + 2) for _ in range(N + 1)]; back = [[-1] * (C + 2) for _ in range(N + 1)]
    best[0][0] = 0.0
    for k in range(1, N + 1):                              # segment k ends at boundary j
        for j in range(1, C + 2):
            if k == N and j != C + 1: continue
            if k < N and j == C + 1: continue
            for i in range(0, j):
                if best[k - 1][i] >= INF: continue
                d = vc[mids[j]] - vc[mids[i]]
                if d <= 5: continue
                c = best[k - 1][i] + np.log(d / tgt[k - 1]) ** 2 - (0.35 * np.log(glen[j] / 20.0) if k < N else 0)
                if c < best[k][j]: best[k][j] = c; back[k][j] = i
    path, j = [], C + 1
    for k in range(N, 0, -1): path.append(j); j = back[k][j]
    path = path[::-1]; bounds = [first] + [mids[j] for j in path]
    used = [glen[j] for j in path[:-1]]
    gaps_used = [round(g / 100, 2) for g in used]; next_gap = None
    report["split"][who] = {"file": fn, "expected": N, "found_gaps": len(runs), "shortest_gap_used_s": min(gaps_used) if gaps_used else None, "longest_unused_gap_s": next_gap}
    dp_cuts = [round(v * 0.01, 2) for v in bounds[1:-1]]
    if who in STT:   # word-timestamp cuts from ElevenLabs STT (exact); keep DP cuts only for comparison
        sp = STT[who]; cuts_s = [(sp[k][1] + sp[k + 1][0]) / 2 for k in range(N - 1)]
        bounds = [max(0, int((sp[0][0] - 0.1) * 100))] + [int(c * 100) for c in cuts_s] + [min(len(e), int((sp[-1][1] + 0.2) * 100))]
        report.setdefault("dp_vs_stt", {})[who] = [round(abs(d - c), 2) for d, c in zip(dp_cuts, cuts_s)]
    report["split"][who]["method"] = "stt" if who in STT else "length-dp"; report["split"][who]["cuts_s"] = [round(v * 0.01, 2) for v in bounds]
    segs = [x[bounds[k] * 480:bounds[k + 1] * 480] for k in range(len(bounds) - 1)]
    for (name, _, text), seg in zip(want, segs):
        y = trim(seg); write(OUT / f"{name}.wav", y)
for name, who, text in names:
    if who in COMBINED: continue
    src = IN / "lines" / f"{name}.mp3"
    if src.exists(): write(OUT / f"{name}.wav", trim(decode(src)))
# check: every line present; duration vs text
for name, who, text in names:
    p = OUT / f"{name}.wav"
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout or 0) if p.exists() else 0
    r = d / est(text) if d else 0
    report["lines"].append({"file": name, "who": who, "text": text, "dur": round(d, 2), "est": round(est(text), 2), "ratio": round(r, 2), "flag": (not d) or r < 0.5 or r > 2.2})
json.dump(report, open(ROOT / "voices_v5_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(report["split"], ensure_ascii=False, indent=0))
fl = [l for l in report["lines"] if l["flag"]]
print("lines:", len(report["lines"]), "present:", sum(1 for l in report["lines"] if l["dur"]), "flagged:", len(fl))
for l in fl: print("  FLAG", l["file"], l["dur"], "s vs est", l["est"], "|", l["text"])
rs = np.array([l["ratio"] for l in report["lines"] if l["dur"]]); print("ratio median %.2f  p10 %.2f  p90 %.2f" % (np.median(rs), np.percentile(rs, 10), np.percentile(rs, 90)))
print("total speech %.1f s" % sum(l["dur"] for l in report["lines"]))
for w, d in report.get("dp_vs_stt", {}).items(): print("DP vs STT", w, "max err %.2f s" % max(d), "| errors > 0.3 s:", sum(1 for v in d if v > 0.3), "/", len(d))

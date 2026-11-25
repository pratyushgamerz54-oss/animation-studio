"""Viseme lip-sync from audio alone (no transcript): per 1/30 s frame, LPC formants (F1/F2) + energy + zero-crossing rate
→ mouth chart (X closed/rest, A closed-line for m/b/p, B small, C medium, D wide 'aa', E round 'o', F tight round 'u', G teeth 's/sh', H 'l/th').
Writes voices_v5_visemes.json: {file: {"dur": s, "mouth": "XXBCD..."}}"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent; SR = 16000; HOP = SR // 30

def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def lpc(x, order=12):
    r = np.correlate(x, x, "full")[len(x) - 1:len(x) + order]
    if r[0] <= 1e-9: return None
    a = np.zeros(order + 1); a[0] = 1; e = r[0]
    for i in range(1, order + 1):           # Levinson-Durbin
        k = -(r[i] + np.dot(a[1:i], r[i - 1:0:-1])) / e
        a[1:i + 1] = a[1:i + 1] + k * np.concatenate([a[i - 1:0:-1], [1]]); e *= (1 - k * k)
        if e <= 0: return None
    return a

def formants(fr):
    x = fr * np.hamming(len(fr)); x = np.append(x[0], x[1:] - 0.63 * x[:-1])   # pre-emphasis
    a = lpc(x, 12)
    if a is None: return None, None
    roots = [z for z in np.roots(a) if np.imag(z) >= 0.01]
    f = sorted(np.angle(roots) * SR / (2 * np.pi)); bw = [-0.5 * SR / np.pi * np.log(abs(z)) for z in roots]
    f = [fi for fi, b in sorted(zip(np.angle(roots) * SR / (2 * np.pi), bw)) if 90 < fi < 4000 and b < 400]
    return (f[0], f[1]) if len(f) >= 2 else (None, None)

def track(path):
    x = decode(path); n = len(x) // HOP; win = 512; out = []
    rms = np.array([np.sqrt(np.mean(x[i * HOP:i * HOP + win] ** 2)) if i * HOP + win <= len(x) else 0 for i in range(n)])
    ref = np.percentile(rms[rms > 0], 95) if (rms > 0).any() else 1
    for i in range(n):
        fr = x[i * HOP:i * HOP + win]
        if len(fr) < win: out.append('X'); continue
        v = rms[i] / ref; zc = np.mean(np.abs(np.diff(np.sign(fr))) > 0)
        if v < 0.08: out.append('X'); continue
        if zc > 0.36 and v < 0.7: out.append('G'); continue          # s / sh / f: teeth
        F1, F2 = formants(fr)
        if F1 is None: out.append('B' if v < 0.4 else 'C'); continue
        if v < 0.22: out.append('A' if F1 < 400 else 'B'); continue      # m/b/p/n edges: nearly closed
        if F1 > 650: out.append('D')                                      # open vowel aa
        elif F2 < 1250 and F1 < 600: out.append('F' if F1 < 400 else 'E')              # u / o: rounded
        elif F2 > 1900: out.append('C' if F1 > 430 else 'B')              # i / e: spread, less open
        elif F1 < 380: out.append('H')                                    # l / th-like
        else: out.append('C')
    # hold each shape ≥ 2 frames and close briefly before plosive bursts (energy jump after a dip)
    for i in range(1, n - 1):
        if out[i - 1] == out[i + 1] != out[i]: out[i] = out[i - 1]
    for i in range(2, n):
        if rms[i] / ref > 0.45 and rms[i - 2] / ref < 0.12 and out[i - 1] != 'X': out[i - 1] = 'A'
    return n / 30, "".join(out)

if __name__ == "__main__":
    src = ROOT / "voices_v5"; res = {}
    files = sorted(src.glob("*.wav")) if len(sys.argv) < 2 else [src / f for f in sys.argv[1:]]
    for f in files: d, m = track(f); res[f.stem] = {"dur": round(d, 2), "mouth": m}
    json.dump(res, open(ROOT / "voices_v5_visemes.json", "w"))
    from collections import Counter
    c = Counter("".join(v["mouth"] for v in res.values())); print(len(res), "files;", dict(sorted(c.items())))
    for k in list(res)[:3]: print(k, res[k]["mouth"][:70])

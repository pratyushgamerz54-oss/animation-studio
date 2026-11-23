"""Fits the ElevenLabs voice-over to the video and writes the TIMING block in index.html.
Phrases are found by silence; LINES says which phrases make up each script line (= one scene).
Usage: python3 tools/fit_voice.py voice.mp3   (needs numpy + ffmpeg)"""
import json, os, re, subprocess, sys, wave
import numpy as np
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
TARGET, LEAD, MAX_SPEED = 59.5, 0.15, 1.32
LINES = [[0, 1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11], [12, 13, 14, 15, 16], [17, 18, 19, 20, 21], [22, 23], [24, 25, 26, 27, 28, 29], [30, 31, 32, 33], [34, 35, 36], [37, 38, 39, 40, 41], [42, 43, 44, 45], [46, 47, 48]]
MID, END = 22, 46                      # first phrase of the mid hook and of the closing question (no captions there)
CAPTIONED = [0, 2, 4, 5, 7, 9, 10, 12, 14, 17, 18, 20, 24, 26, 30, 32, 34, 37, 40, 42, 43]
NOCAP_FROM = {22, 46}                   # captions stop before these phrases

def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32) / 32768

def phrases(x, thr_db=-35, min_sil=.20):
    win = int(.01 * SR); n = len(x) // win
    rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12); loud = 20 * np.log10(rms) > thr_db
    idx = np.flatnonzero(loud); segs = [[idx[0], idx[0]]]
    for i in idx[1:]:
        if (i - segs[-1][1]) * win / SR >= min_sil: segs.append([i, i])
        else: segs[-1][1] = i
    return [[a * win / SR, (b + 1) * win / SR] for a, b in segs]

LINE_START = {l[0] for l in LINES}
def gap_before(k):
    if k == MID: return .45
    if k == MID + 1: return .5
    if k == END: return .4
    return .2 if k in LINE_START else .07

def main(path):
    x = load(path); segs = phrases(x); n = sum(len(l) for l in LINES)
    print(len(segs), 'phrases; voice', round(len(x) / SR, 2), 's')
    if len(segs) != n: sys.exit(f'expected {n} phrases')
    parts, starts, t = [np.zeros(int(LEAD * SR))], [], LEAD
    for k, (a, b) in enumerate(segs):
        if k: g = np.zeros(int(gap_before(k) * SR)); parts.append(g); t += len(g) / SR
        a2, b2 = max(0, a - .04), min(len(x) / SR, b + .08); ch = x[int(a2 * SR):int(b2 * SR)]
        starts.append(t + (a - a2)); parts.append(ch); t += len(ch) / SR
    joined = np.concatenate(parts); raw = len(joined) / SR
    speed = min(MAX_SPEED, max(1.0, (raw - LEAD) / (TARGET - LEAD)))
    tmp = os.path.join(HERE, '_j.wav')
    with wave.open(tmp, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(joined, -1, 1) * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp, '-af', f'atempo={speed:.4f}', '-ar', str(SR), '-ac', '1', os.path.join(ROOT, 'voice_fitted.wav')], check=True)
    os.remove(tmp)
    st = [LEAD + (s - LEAD) / speed for s in starts]
    vo_end = LEAD + (raw - LEAD) / speed
    total = round(max(vo_end + 1.0, st[END] + 4.6), 2)
    bounds = [0.0] + [round(st[l[0]] - .18, 3) for l in LINES[1:]] + [total]
    durs = [round(bounds[i + 1] - bounds[i], 3) for i in range(len(LINES))]
    beats = [[round(st[p] - bounds[i], 3) for p in l] for i, l in enumerate(LINES)]
    caps = []
    for j, p in enumerate(CAPTIONED):
        nxt = CAPTIONED[j + 1] if j + 1 < len(CAPTIONED) else None
        stop = min([q for q in NOCAP_FROM if q > p] + [n])
        endt = st[nxt] - .05 if nxt is not None and nxt < stop else (st[stop] - .3 if stop < n else vo_end)
        caps.append([round(st[p] - .05, 3), round(endt, 3)])
    timing = {'durs': durs, 'beats': beats, 'caps': caps}
    p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'/\*TIMING\*/.*?/\*END TIMING\*/', lambda m: '/*TIMING*/const TIMING = ' + json.dumps(timing, separators=(',', ':')) + ';/*END TIMING*/', s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)
    json.dump({**timing, 'total': total, 'mid': [bounds[5], bounds[6]], 'speed': round(speed, 4), 'bounds': bounds}, open(os.path.join(HERE, 'timing.json'), 'w'), indent=1)
    print(f'speed x{speed:.3f}, voice ends {vo_end:.2f}s, video {total}s'); print('scene starts', bounds[:-1])

if __name__ == '__main__': main(sys.argv[1])

"""Fits the ElevenLabs voice-over into the video.

1. Finds the 31 spoken phrases in the voice file (by silence).
2. Shortens the pauses between them, then speeds the whole voice up slightly (pitch kept) so it ends near TARGET.
3. Writes voice_fitted.wav and rewrites the TIMING block in index.html so every scene and caption starts on its line.

Usage: python3 tools/fit_voice.py path/to/voice.mp3   (needs numpy + ffmpeg)
"""
import json, os, re, subprocess, sys, wave
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
TARGET = 59.0        # seconds the fitted voice should last
LEAD = 0.15          # silence before the first word
MAX_SPEED = 1.12     # never speed the voice up more than this

def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32) / 32768

def phrases(x, thr_db=-35, min_sil=.30):
    win = int(.01 * SR); n = len(x) // win
    rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12); loud = 20 * np.log10(rms) > thr_db
    idx = np.flatnonzero(loud)
    if not len(idx): return []
    segs = [[idx[0], idx[0]]]
    for i in idx[1:]:
        if (i - segs[-1][1]) * win / SR >= min_sil: segs.append([i, i])
        else: segs[-1][1] = i
    return [[a * win / SR, (b + 1) * win / SR] for a, b in segs]

# phrase index -> which line it starts (for pause lengths) and the scene each line opens
LINE_STARTS = [0, 2, 5, 10, 13, 16, 18, 20, 22, 25, 26, 29]
SCENE_AT = {2: 1, 5: 2, 10: 3, 13: 4, 16: 5, 18: 6, 20: 7, 22: 8, 23: 9, 25: 10, 26: 11, 29: 12}
CAP_AT = [0, None, 2, 3, 5, 7, 8, 10, 12, 13, 15, 16, 17, 20, 21, 22, 23, 25, 26, 28]   # None = 0.9 s before phrase 0 ends
CAP_END_BEFORE = {12: 18, 19: 29}   # caption i stops just before this phrase (mid hook / final question have no captions)

def gap_before(k):
    if k == 19: return .45          # "लेकिन…  असली झटका"
    if k in (18, 29): return .40
    if k in LINE_STARTS: return .26
    return .13

def main(path):
    x = load(path); segs = phrases(x)
    print(len(segs), 'phrases found; voice', round(len(x) / SR, 2), 's')
    if len(segs) != 31: sys.exit('expected 31 phrases — the voice has a different pause pattern; adjust thr_db/min_sil')
    pad0, pad1 = .04, .08
    parts, starts, t = [np.zeros(int(LEAD * SR))], [], LEAD
    for k, (a, b) in enumerate(segs):
        if k: g = np.zeros(int(gap_before(k) * SR)); parts.append(g); t += len(g) / SR
        a2, b2 = max(0, a - pad0), min(len(x) / SR, b + pad1); chunk = x[int(a2 * SR):int(b2 * SR)]
        starts.append(t + (a - a2)); parts.append(chunk); t += len(chunk) / SR
    joined = np.concatenate(parts); raw_len = len(joined) / SR
    speed = min(MAX_SPEED, max(1.0, (raw_len - LEAD) / (TARGET - LEAD)))
    tmp = os.path.join(HERE, '_joined.wav')
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(joined, -1, 1) * 32767).astype('<i2').tobytes())
    outp = os.path.join(ROOT, 'voice_fitted.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp, '-af', f'atempo={speed:.4f}', '-ar', str(SR), '-ac', '1', outp], check=True)
    os.remove(tmp)
    st = [LEAD + (s - LEAD) / speed for s in starts]
    en = [LEAD + (s - LEAD + (b - a)) / speed for s, (a, b) in zip(starts, segs)]
    vo_end = LEAD + (raw_len - LEAD) / speed
    total = round(max(vo_end + .9, st[29] + 4.6), 2)
    # scenes
    bounds = [0] + [round(st[k] - .18, 3) for k in sorted(SCENE_AT)] + [total]
    durs = [round(bounds[i + 1] - bounds[i], 3) for i in range(len(bounds) - 1)]
    # captions
    cs = [st[k] if k is not None else en[0] - .9 for k in CAP_AT]
    cs = [round(c - .05, 3) for c in cs]
    caps = []
    for i, c in enumerate(cs):
        endt = round(st[CAP_END_BEFORE[i]] - .25, 3) if i in CAP_END_BEFORE else cs[i + 1]
        caps.append([c, endt])
    timing = {'durs': durs, 'split': round(en[0] - .9 - bounds[0], 3), 'mid1': round(st[19] - bounds[6], 3),
              'mid2': round(st[19] - bounds[6] + .75 * (en[19] - st[19]), 3), 'caps': caps,
              'total': total, 'mid': [bounds[6], bounds[7]], 'speed': round(speed, 4)}
    p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
    js = json.dumps({k: timing[k] for k in ('durs', 'split', 'mid1', 'mid2', 'caps')}, separators=(',', ':'))
    s = re.sub(r'/\*TIMING\*/.*?/\*END TIMING\*/', lambda m: '/*TIMING*/const TIMING = ' + js + ';/*END TIMING*/', s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)
    json.dump(timing, open(os.path.join(HERE, 'timing.json'), 'w'), indent=1)
    print(f'speed x{speed:.3f}, voice ends {vo_end:.2f}s, video {total}s')
    print('scene starts:', bounds[:-1])

if __name__ == '__main__':
    main(sys.argv[1])

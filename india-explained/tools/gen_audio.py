"""Builds music_sfx.wav: a 60 s investigative music bed plus sound effects placed from sfx.json.
Usage: python3 tools/gen_audio.py   (needs numpy only)"""
import json, os, wave, numpy as np
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'music_sfx.wav')
TP = os.path.join(HERE, 'timing.json')
TM = json.load(open(TP)) if os.path.exists(TP) else {'total': 60.0, 'mid': [31.5, 34.5], 'durs': [4] + [5] * 11 + [4.5]}
DUR = float(TM['total']); N = int(SR * DUR); MID0, MID1 = TM['mid']; HOOK_END = TM['durs'][0]; END_START = DUR - TM['durs'][-1]
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(SR * d)) / SR
def band(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
def sweep(f0, f1, d, kind='exp'):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d) if kind == 'exp' else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def norm(x, p=1.0): return x / (np.abs(x).max() + 1e-9) * p

# ---------- effects ----------
def click(hi=True): t = tt(.012); return band(len(t), 2000 if hi else 300, 9000 if hi else 2500) * np.exp(-t * 400)
def impact(d=1.3, f0=95, f1=34, big=False):
    t = tt(d); sub = sweep(f0, f1, d) * np.exp(-t * (2.5 if big else 4))
    nz = band(len(t), 40, 3000) * np.exp(-t * (14 if big else 24))
    return norm(sub * 1.0 + nz * .55)
def whoosh(d=.6):
    t = tt(d); n = len(t); lo = band(n, 200, 1400); hi = band(n, 1500, 7500)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2; x = t / d
    return norm((lo * (1 - x) + hi * x) * env)
def typewriter(d=1.0):
    out = np.zeros(int(SR * (d + .1))); p = 0.0
    while p < d:
        c = click() * (.6 + .4 * rng.random()); th = np.sin(2 * np.pi * 180 * tt(.02)) * np.exp(-tt(.02) * 200) * .5
        i = int(p * SR); out[i:i + len(c)] += c; out[i:i + len(th)] += th; p += .07 + rng.random() * .06
    return norm(out, .8)
def shutter():
    o = np.zeros(int(SR * .2)); a = click(); o[:len(a)] += a; i = int(.06 * SR); o[i:i + len(a)] += a * .8
    n = band(int(SR * .05), 1000, 8000) * np.exp(-tt(.05) * 60); o[:len(n)] += n * .5; return norm(o)
def paper(d=.5):
    t = tt(d); am = np.abs(band(len(t), 5, 40)); return norm(band(len(t), 800, 6500) * am * np.sin(np.pi * t / d), .7)
def pin_():
    t = tt(.06); o = np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 90) * .4; c = click(); o[:len(c)] += c; return norm(o, .6)
def string(): return whoosh(.3) * .5
def stamp_(): t = tt(.35); th = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 16); nz = band(len(t), 100, 4000) * np.exp(-t * 40); return norm(th + nz * .6)
def blip(f=900): t = tt(.12); return np.sin(2 * np.pi * np.cumsum(np.linspace(f, f * 1.45, len(t))) / SR) * np.exp(-t * 30) * .5
def seq(fn, count, d):
    o = np.zeros(int(SR * (d + .3)))
    for k in range(count):
        s = fn(k); i = int(k * d / max(1, count) * SR); o[i:i + len(s)] += s[:len(o) - i]
    return o
def ticks(d):
    def one(k):
        b = blip(1800 + k * 40) * .15; c = click(); b[:len(c)] += c * .35; return b
    return seq(one, int(d / .08), d)
def rise(d):
    t = tt(d); env = (t / d) ** 2 * (1 - np.clip((t - d + .05) / .05, 0, 1))
    return norm((sweep(150, 600, d) * .5 + band(len(t), 500, 6000) * .5) * env, .6)
def riser(d):
    t = tt(d); env = (t / d) ** 2.2
    return norm((sweep(200, 1600, d) * .4 + sweep(203, 1620, d) * .4 + band(len(t), 400, 9000) * .6) * env, .9)
def glitch(d=.4):
    o = np.zeros(int(SR * d)); p = 0
    while p < len(o):
        L = int(SR * (.01 + rng.random() * .04)); f = rng.choice([110, 220, 440, 880, 1760, 3000])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) if rng.random() > .4 else np.round(band(L, 200, 9000) * 4) / 4
        o[p:p + L] = seg[:len(o) - p] * (rng.random() > .25); p += L
    return norm(o, .45)
def heartbeat():
    o = np.zeros(int(SR * .6)); t = tt(.18)
    lub = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 22); o[:len(lub)] += lub
    i = int(.24 * SR); o[i:i + len(lub)] += np.sin(2 * np.pi * 48 * t) * np.exp(-t * 26) * .7; return norm(o)
def ping(): f = 2000 + rng.random() * 1400; t = tt(.35); return sum(np.sin(2 * np.pi * f * m * t) * a for m, a in [(1, 1), (2.76, .5), (5.4, .25)]) * np.exp(-t * 16) * .35
def coins(d): return seq(lambda k: ping(), max(2, int(d * 9)), d)
def beep(): t = tt(.14); return np.sin(2 * np.pi * 1000 * t) * np.clip(t * 200, 0, 1) * np.clip((.14 - t) * 200, 0, 1) * .45
def drop():
    t = tt(.15); b = sweep(380, 1500, .05); b = np.concatenate([b, np.zeros(len(t) - len(b))]) * np.exp(-t * 30)
    return norm(b + band(len(t), 2000, 8000) * np.exp(-t * 60) * .2, .6)
def wind(d):
    t = tt(d); am = .5 + .5 * np.sin(2 * np.pi * .35 * t + 1) * np.sin(2 * np.pi * .13 * t)
    return norm(band(len(t), 90, 900) * am * np.clip(t / .8, 0, 1) * np.clip((d - t) / .8, 0, 1), .45)
def chalk(d):
    t = tt(d); am = np.clip(band(len(t), 8, 30) * 2, 0, 1); return norm(band(len(t), 2500, 7000) * am, .35)
def thuds(d):
    def one(k):
        a = stamp_() * .6; p = paper(.2) * .3; a[:len(p)] += p; return a
    return seq(one, 7, d)
FX = {'impact': lambda d: impact(), 'impact_big': lambda d: impact(2.2, 80, 28, True), 'impact_small': lambda d: impact(.6, 160, 60) * .7,
      'whoosh': lambda d: whoosh(), 'typewriter': typewriter, 'shutter': lambda d: shutter(), 'paper': lambda d: paper(),
      'pin': lambda d: pin_(), 'string': lambda d: string(), 'stamp': lambda d: stamp_(), 'blips': lambda d: seq(lambda k: blip(800 + k * 120), 6, .7),
      'pins': lambda d: seq(lambda k: blip(700 + k * 90), 6, d), 'ticks': ticks, 'rise': rise, 'riser': riser, 'glitch': lambda d: glitch(),
      'heartbeat': lambda d: heartbeat(), 'coins': coins, 'beep': lambda d: beep(), 'drop': lambda d: drop(), 'wind': wind, 'chalk': chalk, 'thuds': thuds}
GAIN = {'impact': .9, 'impact_big': 1.0, 'impact_small': .6, 'whoosh': .55, 'typewriter': .35, 'shutter': .5, 'paper': .45, 'pin': .4, 'string': .35,
        'stamp': .7, 'blips': .3, 'pins': .3, 'ticks': .25, 'rise': .35, 'riser': .6, 'glitch': .5, 'heartbeat': .9, 'coins': .4, 'beep': .35,
        'drop': .45, 'wind': .5, 'chalk': .4, 'thuds': .55}

# ---------- music bed (D minor, investigative) ----------
t = np.arange(N) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
CH = [[50, 53, 57, 62], [46, 50, 53, 58], [41, 45, 48, 53], [45, 49, 52, 57]]   # Dm, Bb, F, A
pad = np.zeros(N); seglen = 4.0
for k in range(int(DUR / seglen) + 1):
    notes = CH[k % 4]; c = k * seglen
    env = np.clip(1 - np.abs(t - (c + seglen / 2)) / (seglen / 2 + .6), 0, 1); env = np.sin(env * np.pi / 2) ** 2
    idx = env > 0
    for m in notes:
        f = hz(m + 12)
        for det in (-.0015, 0, .0015): pad[idx] += np.sin(2 * np.pi * f * (1 + det) * t[idx]) * env[idx] * .18
        pad[idx] += np.sin(2 * np.pi * f * 2 * t[idx]) * env[idx] * .03
pad *= .75 + .25 * np.sin(2 * np.pi * .25 * t)
drone = sum(np.sin(2 * np.pi * hz(26) * n * t) / n for n in range(1, 7)) * .35 + np.sin(2 * np.pi * hz(38) * t) * .25
kick = np.zeros(N); kt = tt(.35); kk = sweep(110, 42, .35) * np.exp(-kt * 9)
hat = np.zeros(N); hh = band(int(SR * .03), 6000, 12000) * np.exp(-tt(.03) * 150)
arp = np.zeros(N); beat = 60 / 100
b = HOOK_END
while b < END_START:
    if not (MID0 <= b < MID1):
        i = int(b * SR); kick[i:i + len(kk)] += kk[:N - i]
        if b >= MID1:
            for half in (0, .5):
                j = int((b + beat * half) * SR); hat[j + int(beat * .25 * SR): j + int(beat * .25 * SR) + len(hh)] += hh
                notes = CH[int((b + beat * half) / seglen) % 4]; f = hz(notes[int(b * 2 / beat) % 4] + 24); pt = tt(.25)
                pl = np.sin(2 * np.pi * f * pt) * np.exp(-pt * 14) * .22; arp[j:j + len(pl)] += pl[:N - j]
    b += beat
music = pad * .9 + drone * .55 + kick * .9 + hat * .18 + arp
sec = np.ones(N)
sec[(t >= MID0) & (t < MID1)] = .12                      # drop out for the mid hook
sec *= np.clip(t / 1.2, .35, 1)                          # quiet under the opening impact
sec *= np.clip((DUR - t) / 2.5, 0, 1) ** .7              # tail fade
sm = np.convolve(sec, np.ones(2205) / 2205, mode='same')
music = norm(music * sm, .22)

# ---------- place effects ----------
L = np.zeros(N); R = np.zeros(N)
cues = json.load(open(os.path.join(HERE, 'sfx.json')))
for c in cues:
    x = FX[c['type']](c.get('dur') or .5) * GAIN[c['type']]; i = int(c['t'] * SR)
    if i >= N: continue
    x = x[:N - i]; pan = .5 + (rng.random() - .5) * .5
    L[i:i + len(x)] += x * (1 - pan) * 1.4; R[i:i + len(x)] += x * pan * 1.4
def conv(a, ir):
    n = 1 << int(np.ceil(np.log2(len(a) + len(ir))))
    return np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(ir, n), n)[:len(a)]
irt = tt(1.4); irL = rng.standard_normal(len(irt)) * np.exp(-irt * 4.5); irR = rng.standard_normal(len(irt)) * np.exp(-irt * 4.5)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
L = L + conv(L, irL) * .35; R = R + conv(R, irR) * .35
def write(path, st):
    st = np.tanh(st * 1.3) / np.tanh(1.3); st = st / np.abs(st).max() * .89
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
    print('wrote', path)
musL, musR = music, np.roll(music, 220)
write(OUT, np.stack([musL + L, musR + R], 1))
VO = os.path.join(HERE, '..', 'voice_fitted.wav')
if os.path.exists(VO):
    with wave.open(VO) as w: v = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64) / 32768
    v = np.pad(v, (0, max(0, N - len(v))))[:N]; v = v / (np.abs(v).max() + 1e-9) * .9
    env = np.convolve(np.abs(v), np.ones(int(.25 * SR)) / int(.25 * SR), mode='same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
    duck = 1 - .55 * env                                   # music dips under the voice
    bedL, bedR = musL * duck * .75 + L * .55, musR * duck * .75 + R * .55
    write(os.path.join(HERE, '..', 'final_mix.wav'), np.stack([v + bedL, v + bedR], 1))
print(len(cues), 'cues')

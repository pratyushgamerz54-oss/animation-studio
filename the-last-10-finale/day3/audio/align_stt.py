"""Align ElevenLabs STT word timestamps to the v5 script lines; return line start/end times per combined file.
Compares with the length-based DP cuts (from split_voices.py) to measure how far those were off."""
import json, re, sys, unicodedata
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import day3_10_v5_data as M

def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    w = w.replace("़", "")                       # drop nukta
    w = re.sub(r"[^\wऀ-ॿ]", "", w)
    w = w.replace("ं", "ँ").replace("ॅ", "")
    return w
def sim(a, b):
    if not a or not b: return 0.0
    if a == b: return 1.0
    # bigram Dice similarity
    A = {a[i:i + 2] for i in range(len(a) - 1)} or {a}; B = {b[i:i + 2] for i in range(len(b) - 1)} or {b}
    return 2 * len(A & B) / (len(A) + len(B))

def align(who, stt):
    lines = [x for t, w, x, n, s in M.LINES if w == who]
    S = [(norm(w), li) for li, x in enumerate(lines) for w in re.sub(r"\(.*?\)", "", x).split() if norm(w)]
    T = [(norm(w["text"]), w["start"], w["end"]) for w in stt["words"] if w["type"] == "word" and norm(w["text"])]
    n, m = len(S), len(T); G = -0.45
    D = [[0.0] * (m + 1) for _ in range(n + 1)]; P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1): D[i][0] = i * G; P[i][0] = 1
    for j in range(1, m + 1): D[0][j] = j * G; P[0][j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = [D[i - 1][j - 1] + (sim(S[i - 1][0], T[j - 1][0]) * 2 - 0.6), D[i - 1][j] + G, D[i][j - 1] + G]
            k = max(range(3), key=lambda q: c[q]); D[i][j] = c[k]; P[i][j] = (0, 1, 2)[k]
    i, j, owner = n, m, [None] * m
    while i > 0 or j > 0:
        p = P[i][j] if i > 0 and j > 0 else (1 if j == 0 else 2)
        if p == 0: owner[j - 1] = S[i - 1][1]; i -= 1; j -= 1
        elif p == 1: i -= 1
        else: j -= 1
    # unmatched transcript words inherit the nearest owner (forward fill, then back fill)
    last = None
    for q in range(m):
        if owner[q] is None: owner[q] = last
        last = owner[q]
    nxt = None
    for q in range(m - 1, -1, -1):
        if owner[q] is None: owner[q] = nxt
        nxt = owner[q]
    spans = {}
    for (w, a, b), o in zip(T, owner): s = spans.setdefault(o, [a, b]); s[0] = min(s[0], a); s[1] = max(s[1], b)
    return [spans.get(li) for li in range(len(lines))], lines

if __name__ == "__main__":
    out = {}
    for who, f in [("Dev", "dev_all_voices"), ("Vikram", "Vikram_all_voices"), ("Ananya", "ananya_all_voices"), ("Zeno Commander", "Zeno_Commander_all_voices"), ("Ryan", "ryan_all_voices"), ("Sara", "sara_all_voices"), ("Ishaan", "ishaan_all_voices")]:
        stt = json.load(open(HERE / "stt" / f"{f}.json")); spans, lines = align(who, stt)
        out[who] = spans; miss = [i + 1 for i, s in enumerate(spans) if not s]
        print(f"== {who}: {len(lines)} lines, missing {miss}")
        for i, (s, x) in enumerate(zip(spans, lines), 1): print(f"  {i:2d} {s[0] if s else '-':>6} → {s[1] if s else '-':>6}  {x}")
    json.dump(out, open(HERE / "stt_spans.json", "w"), indent=1)

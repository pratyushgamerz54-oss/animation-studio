# Generate all finale lines (VER=v4 default) with ElevenLabs (key injected by the session proxy). One fixed voice per character.
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import os, importlib
VER = os.environ.get('VER', 'v4')
M = importlib.import_module(f'day3_10_{VER}_data')

MODEL = os.environ.get("MODEL", "eleven_multilingual_v2")
VOICE = {  # character: (ElevenLabs premade voice, voice_id, why)
    "Aarav": ("Liam", "TX3LPaxmHKxFdv7VOQHJ", "male, young, firm, clear — leader, 25"),
    "Kabir": ("Charlie", "IKne3meq5aSn9XLyUdCD", "male, casual, conversational — sarcastic engineer, 28"),
    "Ryan": ("Daniel", "onwK4e9ZLuTAKqWW03F9", "male, deep, calm — former astronaut, 30"),
    "Dev": ("Brian", "nPczCjzI2devNBz1zQrb", "male, deep, warm — survival expert, fatherly, 35"),
    "Ishaan": ("Will", "bIHbv24MWmeRgasZH58o", "male, young, energetic — tech kid, 19"),
    "Vikram": ("Adam", "pNInz6obpgDQGcFmaJgB", "male, deep, authoritative — security chief, 42"),
    "Zeno Commander": ("Callum", "N2lVS1w4EtoT3dr4eOWO", "male, gravelly, intense — villain (alien effect in mix)"),
    "Dr. Meera": ("Alice", "Xb7hH8MSUJpSbSDYk0k2", "female, clear, confident — scientist, 32"),
    "Zoya": ("Jessica", "cgSgspJ2msm6clMCkdW9", "female, young, expressive — medical student, 24"),
    "Sara": ("Sarah", "EXAVITQu4vr4xnJcfmIX", "female, soft, mature — geologist, 27"),
    "Ananya": ("Matilda", "XrExE9yKIg1WjnnlVkGX", "female, warm, articulate — journalist, 26"),
}
_C = json.load(open(HERE / "cast_voices_final.json", encoding="utf-8"))
VOICE = {w: (v["voice"], v.get("my_voice_id", v["voice_id"]), "user's choice") for w, v in _C.items()}  # user-chosen Hindi voices
SEED = {w: 1000 + i for i, w in enumerate(VOICE)}

def tags(note):
    return _tags(note) if MODEL == 'eleven_v3' else ''
def _tags(note):  # map the Hinglish direction to eleven_v3 audio tags
    n = note.lower(); t = []
    if "khud se" in n or "fusfus" in n or "dheemi" in n and "bahut" in n: t.append("whispers")
    if "cheekh" in n or "chill" in n or "poori awaaz" in n or "poora zor" in n or "poori taaqat" in n: t.append("shouting")
    if "ro-te" in n or "ro-ke" in n or "aansu" in n or "gala bhar" in n or "toot" in n: t.append("emotional, voice breaking")
    if "hasi" in n or "muskaan" in n and "jhooti" not in n: t.append("slight laugh")
    if "gussa" in n: t.append("angry")
    if "darr" in n or "ghabrahat" in n or "kaanp" in n: t.append("scared")
    if "thak" in n or "haanf" in n: t.append("tired, breathing hard")
    if "sarcasm" in n: t.append("sarcastic")
    if "bukhaar" in n or "behosh" in n: t.append("weak")
    return "".join(f"[{x}] " for x in t[:2])

def files():
    c, out = {}, []
    for i, (t, who, x, n, s) in enumerate(M.LINES):
        c[who] = c.get(who, 0) + 1; out.append((f"{M.CAST[who][2]}_{c[who]:02d}", who, x, n, s, t))
    return out

def tts(voice_id, text, seed, path):
    body = json.dumps({"text": text, "model_id": MODEL, "seed": seed, "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128", data=body,
                                 headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json", "Accept": "audio/mpeg"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: path.write_bytes(r.read()); return True
        except urllib.error.HTTPError as e:
            msg = e.read()[:300].decode(errors="replace")
            if e.code in (429, 500, 502, 503): time.sleep(5 * (attempt + 1)); continue
            print("FAIL", path.name, e.code, msg); return False
        except Exception as e:
            print("retry", path.name, e); time.sleep(5)
    return False

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = HERE.parent / (f"voices_{VER}_samples" if mode == "samples" else f"voices_{VER}"); out.mkdir(exist_ok=True)
    F = files(); done = set()
    if mode == "samples":
        F = [f for f in F if not (f[1] in done or done.add(f[1]))]  # first line of each character
    chars = sum(len(tags(f[3]) + f[2]) for f in F); print(len(F), "lines,", chars, "characters")
    ok = 0
    for name, who, x, n, s, t in F:
        p = out / f"{name}.mp3"
        if p.exists() and p.stat().st_size > 2000: ok += 1; continue
        if tts(VOICE[who][1], tags(n) + x, SEED[who], p): ok += 1
    print("ok", ok, "/", len(F))
    json.dump({"model": MODEL, "voices": {w: {"voice": v[0], "voice_id": v[1], "why": v[2]} for w, v in VOICE.items()},
               "lines": [{"file": f"{a}.mp3", "who": b, "text": c, "tags": tags(d), "shot": e, "t_script": t} for a, b, c, d, e, t in files()]},
              open(HERE.parent / f"voices_{VER}_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

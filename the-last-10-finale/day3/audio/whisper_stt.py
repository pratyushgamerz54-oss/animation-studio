# faster-whisper → ElevenLabs-like JSON {"words":[{"text","start","end","type":"word"}]}
import json, sys
from faster_whisper import WhisperModel
model_name, out_dir, files = sys.argv[1], sys.argv[2], sys.argv[3:]
m = WhisperModel(model_name, device="cpu", compute_type="int8", download_root=out_dir + "/_models")
for f in files:
    segs, info = m.transcribe(f, language="hi", word_timestamps=True, beam_size=5, vad_filter=False)
    words = [{"text": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2), "type": "word"} for s in segs for w in s.words]
    name = f.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    json.dump({"text": " ".join(w["text"] for w in words), "words": words}, open(f"{out_dir}/{name}.whisper.json", "w"), ensure_ascii=False)
    print(name, len(words), "words")

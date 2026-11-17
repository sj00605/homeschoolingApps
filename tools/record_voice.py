#!/usr/bin/env python3
"""
Record a game's spoken lines with ElevenLabs.

    python3 tools/record_voice.py voice-lines/asteroid-pilot.json
    python3 tools/record_voice.py voice-lines/asteroid-pilot.json --only find_3 yes_3   # redo just a few

It asks for your ElevenLabs API key (not shown, not saved) and which voice to use,
then saves one .mp3 per line into  recordings/<game>/  and makes  recordings/<game>.zip.
If it stops partway, run it again: lines already recorded are skipped.
To redo a line you don't like, delete its .mp3 (or use --only) and run again.

Uses only built-in Python, so nothing needs installing.
Lines whose name starts with "slow_" are recorded at a slower speed.
Lines containing Hebrew letters use ElevenLabs' Eleven v3 model (it handles Hebrew); others use Multilingual v2.
  --hebrew   record only the lines that contain Hebrew (e.g. to redo them with a Hebrew voice)
"""
import argparse, getpass, json, os, sys, time, urllib.error, urllib.request, zipfile

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
HEBREW_MODEL = "eleven_v3"
is_hebrew = lambda text: any("\u0590" <= ch <= "\u05FF" for ch in text)
DEFAULT_VOICE_NAME = "Bill Oxley"   # the voice used for all the games so far

def call(path, key, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": key, "Content-Type": "application/json"},
                                 method="POST" if body else "GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lines", help="a voice-lines/<game>.json file")
    ap.add_argument("--only", nargs="*", help="record only these line names (re-records them)")
    ap.add_argument("--hebrew", action="store_true", help="record only lines that contain Hebrew (re-records them)")
    args = ap.parse_args()

    game = os.path.splitext(os.path.basename(args.lines))[0]
    lines = json.load(open(args.lines, encoding="utf-8"))
    if args.only:
        lines = {k: v for k, v in lines.items() if k in args.only}
    if args.hebrew:
        lines = {k: v for k, v in lines.items() if is_hebrew(v)}
        game += "-hebrew"
    out = os.path.join("recordings", game)
    os.makedirs(out, exist_ok=True)
    if args.only or args.hebrew:
        for k in lines:
            p = os.path.join(out, k + ".mp3")
            if os.path.exists(p): os.remove(p)

    todo = {k: v for k, v in lines.items() if not os.path.exists(os.path.join(out, k + ".mp3"))}
    print(f"\n{game}: {len(lines)} lines, {len(todo)} to record "
          f"(about {sum(len(v) for v in todo.values()):,} characters of your ElevenLabs allowance).\n")
    if todo:
        key = getpass.getpass("Paste your ElevenLabs API key and press Enter: ").strip()
        try:
            voices = json.loads(call("/voices", key))["voices"]
        except urllib.error.HTTPError as e:
            sys.exit(f"Couldn't sign in to ElevenLabs ({e.code}). Check the API key.")
        default = None if args.hebrew else next((i for i, v in enumerate(voices, 1) if v["name"].startswith(DEFAULT_VOICE_NAME)), None)
        print("\nYour voices:")
        for i, v in enumerate(voices, 1):
            print(f"  {i:2}. {v['name']}" + ("   <- used for the other games" if i == default else ""))
        pick = input(f"\nType the number of the voice to use{f' (Enter for {default})' if default else ''}: ").strip()
        voice = voices[int(pick or default) - 1]
        print(f"\nUsing {voice['name']}...\n")
        done = 0
        for cid, text in todo.items():
            speed = 0.7 if cid.startswith("slow_") else 0.92
            if is_hebrew(text):   # Eleven v3 accepts only a few settings
                body = {"text": text, "model_id": HEBREW_MODEL,
                        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": speed}}
            else:
                body = {"text": text, "model_id": MODEL,
                        "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.3,
                                           "use_speaker_boost": True, "speed": speed}}
            for attempt in range(5):
                try:
                    audio = call(f"/text-to-speech/{voice['voice_id']}?output_format=mp3_22050_32", key, body)
                    open(os.path.join(out, cid + ".mp3"), "wb").write(audio)
                    done += 1
                    break
                except urllib.error.HTTPError as e:
                    msg = e.read().decode(errors="ignore")[:200]
                    if e.code == 429:
                        time.sleep(3 * (attempt + 1)); continue
                    if e.code in (400, 422) and "voice_settings" in body:
                        body.pop("voice_settings"); continue   # retry with the voice's own settings
                    if e.code == 401 or "quota" in msg.lower():
                        sys.exit(f"\nStopped: {msg}\nYou may be out of characters. Run again later to finish.")
                    print(f"  problem with {cid}: {e.code} {msg}"); break
                except Exception as e:
                    print(f"  retrying {cid}: {e}"); time.sleep(2)
            print(f"\r  {done}/{len(todo)} done", end="", flush=True)
        print()

    missing = [k for k in lines if not os.path.exists(os.path.join(out, k + ".mp3"))]
    if missing:
        sys.exit(f"\n{len(missing)} lines didn't finish. Run again to finish them.")
    zpath = os.path.join("recordings", game + ".zip")
    with zipfile.ZipFile(zpath, "w") as z:
        for k in lines:
            z.write(os.path.join(out, k + ".mp3"), k + ".mp3")
    print(f"\nDone! Recordings are in {out}/ and {zpath}")
    print(f"Next: python3 tools/embed_voice.py {game.replace('-hebrew','')} {zpath}\n")

if __name__ == "__main__":
    main()

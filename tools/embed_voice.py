#!/usr/bin/env python3
"""
Put voice recordings into a game, so the game works on any device, even offline.

    python3 tools/embed_voice.py asteroid-pilot recordings/asteroid-pilot.zip
    python3 tools/embed_voice.py asteroid-pilot recordings/asteroid-pilot/      (a folder works too)

Each recording is slowed to 85% speed (easier for young listeners; "slow_" lines to 70%),
then stored inside games/<game>/index.html in the VOICE_CLIPS list. Recordings replace
lines with the same name; new names are added. Only some lines? That's fine.

Needs ffmpeg (https://ffmpeg.org; on a Mac: brew install ffmpeg).
Options: --tempo 0.9 to change the speed, --no-slow to keep the original speed.
"""
import argparse, base64, os, re, shutil, subprocess, sys, tempfile, zipfile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game", help="folder name inside games/")
    ap.add_argument("source", help="a .zip or a folder of .mp3 files named <line>.mp3")
    ap.add_argument("--tempo", type=float, default=0.85)
    ap.add_argument("--no-slow", action="store_true")
    a = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    page = os.path.join(root, "games", a.game, "index.html")
    if not os.path.exists(page):
        sys.exit(f"No game at {page}")
    if not a.no_slow and not shutil.which("ffmpeg"):
        sys.exit("ffmpeg isn't installed (needed to slow the voice). Install it, or use --no-slow.")

    tmp = tempfile.mkdtemp()
    if a.source.endswith(".zip"):
        with zipfile.ZipFile(a.source) as z:
            for n in z.namelist():
                base = os.path.basename(n)
                if base.endswith(".mp3") and "/" not in n.strip("/") and not base.startswith("."):
                    z.extract(n, tmp)
        src = tmp
    else:
        src = a.source

    clips = {}
    for f in sorted(os.listdir(src)):
        if not f.endswith(".mp3"):
            continue
        name = f[:-4].split("__")[-1]          # also accepts older "<game>__<line>.mp3" names
        path = os.path.join(src, f)
        if not a.no_slow:
            out = os.path.join(tmp, "slowed_" + f)
            tempo = 0.7 if name.startswith("slow_") else a.tempo
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-af", f"atempo={tempo}",
                            "-ac", "1", "-b:a", "32k", out], check=True)
            path = out
        clips[name] = base64.b64encode(open(path, "rb").read()).decode()
    if not clips:
        sys.exit("No .mp3 files found.")

    s = open(page, encoding="utf-8").read()
    m = re.search(r'const VOICE_CLIPS=\{(.*?)\};\n', s, re.S)
    if not m:
        sys.exit("This game has no VOICE_CLIPS list (start new games from templates/game-template.html).")
    existing = dict(re.findall(r'"(\w+)":"([^"]*)"', m.group(1)))
    added = [k for k in clips if k not in existing]
    existing.update(clips)
    new = 'const VOICE_CLIPS={' + ','.join(f'"{k}":"{v}"' for k, v in existing.items()) + '};\n'
    open(page, "w", encoding="utf-8").write(s[:m.start()] + new + s[m.end():])
    print(f"{a.game}: put in {len(clips)} recordings ({len(added)} new, {len(clips)-len(added)} replaced). "
          f"The game now has {len(existing)} lines.")

if __name__ == "__main__":
    main()

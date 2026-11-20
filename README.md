# 🏡 The Popell Homeschool Hub

Talking learning games for young kids, all in one place. Open the hub, tap a game, and play.
Every game is a single web page, so it runs in any browser, on a tablet, phone or computer, with nothing to install.

| Game | Practices | Languages |
|---|---|---|
| 🚂 **Alphabet Train** | Letter recognition: capitals, small letters, matching; Hebrew aleph-bet | English, Hebrew |
| 🪜 **Word Ladder** | Phonics: change one letter to make a new word | English |
| 🐟 **Feed the Cat** | Adding and taking away, answers 0–10 | English |
| 🚀 **Asteroid Pilot** | Number recognition 0–10 or 0–20; Hebrew counting words | English, Hebrew |
| 🌍 **World Map** | The seven continents: tap one to hear its name | English |
| 🪐 **Solar System** | The eight planets: explore, rocket tour, guess from clues, true sizes and distances | English |

## Playing

- **On this computer:** open `index.html` in a browser.
- **From anywhere (free website):** turn on GitHub Pages. See below.

Sound matters: every game talks. On an iPhone or iPad, turn off the silent switch. Sound starts after the first tap.

## Putting it online with GitHub Pages

1. On GitHub, open this repository and go to **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, pick **main** and **/ (root)**, then **Save**.
3. After a minute or two, the hub is live at `https://<your-username>.github.io/<repository-name>/`.
   Add it to your tablet's home screen for one-tap access.

## What's in here

```
index.html            the hub's home page (reads the game list from games.js)
games.js              the list of games shown on the hub
games/<game>/         one folder per game; each game is a single index.html
templates/            a starter page for new games
voice-lines/          every line each game says, one file per game
tools/                scripts for recording voices and putting them into games
```

## Adding a new game

1. Make a folder `games/<new-game>/` and put the game in `index.html`.
   Starting from `templates/game-template.html` gives you the voice player and the 🏠 hub button.
2. Add an entry for it in `games.js` (title, emoji, subject, color, a one-line blurb).
3. Open `index.html` and the new card appears.

## Voices

The games use recordings, not the device's robot voice, so they sound the same everywhere and work offline.
The voices are from ElevenLabs, slowed to 85% speed for young listeners: **Bill Oxley** for English in the games,
**Erez** for Hebrew, **Sarah** for the World Map, and **Bill – Wise, Mature, Balanced** for the Solar System.

To record or re-record lines (needs an ElevenLabs account; Python 3; and `ffmpeg` for step 2):

```bash
# 1. Record. It asks which voice to use, and for your ElevenLabs API key the first time
#    (it can save the key in ~/.elevenlabs_key, or set ELEVENLABS_API_KEY, so you only paste it once).
python3 tools/record_voice.py voice-lines/asteroid-pilot.json
#    Redo only certain lines:
python3 tools/record_voice.py voice-lines/asteroid-pilot.json --only find_13 yes_13

# 2. Put the recordings into the game (slows them to 85%).
python3 tools/embed_voice.py asteroid-pilot recordings/asteroid-pilot.zip
```

To change what a line says, edit it in `voice-lines/<game>.json`, then re-record just that line with `--only`.
Hebrew words are written in Hebrew with vowel marks, for the Hebrew voice.
To force an exact English pronunciation, wrap the word in a tag, like `<phoneme alphabet="cmu-arpabet" ph="EY1 ZH AH0">Asia</phoneme>` (see `voice-lines/world-map.json`).
The `recordings/` folder is kept out of the repository; the recordings that matter are stored inside each game.

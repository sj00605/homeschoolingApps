// The list of games shown on the hub.
// To add a game: put it in games/<folder>/index.html, then add an entry below.
//   folder   - the game's folder name inside games/
//   title    - name shown on the card
//   emoji    - big picture on the card
//   subject  - "Reading", "Math", "Letters", "Numbers", "Geography", "Science" (groups the cards)
//   color    - card color
//   blurb    - one short line about the game
//   skills   - what it practices (shown small, for grown-ups)
//   languages- e.g. ["English"] or ["English", "Hebrew"]
window.GAMES = [
  {
    folder: "alphabet-train",
    title: "Alphabet Train",
    emoji: "🚂",
    subject: "Letters",
    color: "#ff8fb1",
    blurb: "Listen for the letter and send the train down the right track.",
    skills: "Letter recognition: capitals, small letters, matching; Hebrew aleph-bet",
    languages: ["English", "Hebrew"]
  },
  {
    folder: "word-ladder",
    title: "Word Ladder",
    emoji: "🪜",
    subject: "Reading",
    color: "#6c8cff",
    blurb: "Change one letter to climb from word to word.",
    skills: "Phonics: three-letter words, hearing which sound changed",
    languages: ["English"]
  },
  {
    folder: "feed-the-cat",
    title: "Feed the Cat",
    emoji: "🐟",
    subject: "Math",
    color: "#ffa94d",
    blurb: "Solve adding and taking-away problems to feed a hungry cat.",
    skills: "Addition and subtraction, answers 0 to 10",
    languages: ["English"]
  },
  {
    folder: "asteroid-pilot",
    title: "Asteroid Pilot",
    emoji: "🚀",
    subject: "Numbers",
    color: "#46c2b8",
    blurb: "Find the right number and blast the asteroid to reach the space station.",
    skills: "Number recognition 0 to 10 or 0 to 20; Hebrew counting words",
    languages: ["English", "Hebrew"]
  },
  {
    folder: "world-map",
    title: "World Map",
    emoji: "🌍",
    subject: "Geography",
    color: "#5aa9e6",
    blurb: "Tap a continent to hear its name.",
    skills: "The seven continents on a Mercator map",
    languages: ["English"]
  },
  {
    folder: "solar-system",
    title: "Solar System",
    emoji: "🪐",
    subject: "Science",
    color: "#7c6cf0",
    blurb: "Explore the planets, fly a rocket tour, guess from clues, and see how big and far they really are.",
    skills: "The eight planets: names, order, facts, true sizes and distances",
    languages: ["English"]
  }
];

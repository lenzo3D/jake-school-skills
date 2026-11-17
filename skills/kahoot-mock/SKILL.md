---
name: kahoot-mock
description: Build a mock Kahoot game for the topic the user is working on, as a standalone HTML page that copies the real thing: 10 questions, a read phase, then a countdown with four coloured answer tiles, speed-based points (up to 1000), answer streak bonus, a scoreboard after every question, simulated rival players and a podium. Use whenever the user asks for a mock Kahoot, a Kahoot practice, a lecture quiz rehearsal, "practice for the in-person Kahoot", or wants to train speed and pressure for the top 3 participation reward. Not for untimed revision (use revision-widget).
---

# Mock Kahoot

The user's in-person lectures end with a 10 question Kahoot. The top 3 earn participation and rewards, and faster correct answers earn more points. This skill builds a practice game that feels the same, so the user trains speed and pressure, not only knowledge.

## What the page copies (do not remove)

- Join screen with a game PIN and nickname, a lobby where rival players appear, then a 3, 2, 1 countdown.
- For each question: the question alone for a read phase (5 seconds), then four answer tiles appear and the timer starts. Red triangle, blue diamond, yellow circle, green square. Timer circle goes red in the last 5 seconds. A live "Answers" counter shows how many rivals have answered.
- Points = round((1 - (response time / time limit) / 2) x 1000). Right on the first instant is 1000, right at the buzzer is 500, wrong or no answer is 0.
- Answer streak bonus: +100 for the second correct in a row, rising by 100 each time to +500.
- After each question: correct, incorrect or time's up, points earned, the answer spread of the room, the explanation, then the top 5 scoreboard with the user highlighted and how far behind the next player they are.
- 22 simulated rivals in three speed bands (3 fast and accurate, 7 average, 12 slower), so the top 3 is contested.
- Podium with the top 3, a message saying if the user would have earned the reward or how many points short, a review of every miss with the rule, and a stored personal best.
- Keys 1 to 4 pick the colours, space or Enter moves on. The user picks 10, 20, 30 or 60 seconds per question in the join form. Default 20.

Be honest with the user about the limits: the scoring formula and streak bonus are the public Kahoot ones as best known and the rivals are simulated, so scores are a guide and not a prediction. The sounds are simple synthesised tones, not Kahoot's music. The real time limit is set by the lecturer per question, so tell the user to choose the limit that matches theirs (or 10 seconds for extra pressure).

## Steps

1. **Find the topic.** Use the topic the user names, or the one they are currently working on (the most recently imported `Commercial Banking Topic N/`, `Investments Topic N/` and so on). Read its lecture text in `sources/text/`. If nothing is imported, run `import-sources` first.
2. **Write 10 questions in Kahoot style.** They must be quick to read and answer:
   - Question text under about 140 characters, one idea, no long scenarios. Short calculations are fine if they can be done in the time limit (mental maths only, round numbers).
   - Exactly 4 options, each under about 60 characters, similar length, and plausible wrong answers (the common mix-ups from the slides).
   - Spread the correct answers across red, blue, yellow and green. No colour more than 4 of 10.
   - Cover the whole lecture in slide order, weighted to what a lecturer would ask: definitions, which-one-is-it classification, "which is NOT", short applications.
   - Each question stands alone. No "Scenario A", "the above" or "the same loan".
   - `exp`: one or two sentences with the rule and the slide number, shown after the question and in the final review.
   - Compute any number with Python. Never answer from memory.
   - If the user has logged weak spots for this topic in `study-log/STUDY_LOG.md`, include one or two questions on them.
3. **Save the bank** as `<topic folder>/revision/<topic>_kahoot_bank.json`: a list of `{"q":..., "o":[4], "a":0-3, "exp":..., "t": optional per-question seconds}`.
4. **Build the page:**
   ```bash
   python3 ~/.claude/skills/kahoot-mock/scripts/build_kahoot.py bank.json "<topic folder>/revision/<topic>_mock_kahoot.html" --title "<Topic> mock Kahoot"
   ```
   Read the warnings it prints and fix them.
5. **Test it** in the Browser pane: join, play through, check the timer, the points, the scoreboard and the podium. Sound and `localStorage` may be blocked on `file://` pages in the pane, so tell the user to open the file in Chrome or Edge.
6. **Tell the user** in a few lines with a clickable link: 10 questions, how scoring works, the time limit choice, and that it is practice, not logged. If they want a result recorded, use `study-log-update` only when they ask.

## Rules

- A new mock for the same topic gets new questions, not the same ones, unless the user asks to replay. The page's "Play again" button replays the same questions with new rivals.
- Do not copy Kahoot's logo, music or branding. The page says "Mock Kahoot".
- Plain text, no emoji, sentence case.

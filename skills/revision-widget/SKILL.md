---
name: revision-widget
description: Build a self-marking revision quiz or practice set for a university topic as a standalone HTML page that saves answers in the browser, marks itself, shows a score per module and builds a prompt to paste back into Claude Code to log the result in the study log. Use whenever the user asks for a quiz, revision test, practice questions, a consolidated quiz across topics, a formula drill, a retest on wrong answers, or an interactive way to revise a topic. Requires the topic's sources to be imported (see import-sources) or the questions to be given. For logging a result, hand over to study-log-update.
---

# Revision widget

Build one HTML file the user opens in Chrome or Edge. The page marks every answer itself, remembers progress when the user leaves the tab or reloads, and ends with a box that turns the results into a prompt for Claude Code. That prompt is how the result reaches the study log, so the quiz is not finished until that loop works.

## What the page does (do not remove these)

- Marks each question on "Check", locks it, and shows the working. Wrong answers show the correct value and the rule.
- Saves answers and half-typed drafts in `localStorage` under a key unique to the quiz, so switching tabs or reloading does not reset it. If storage is blocked it says "Cannot save here; keep this tab open" instead of failing silently.
- Sticky header with answered, correct and wrong counts, a saved indicator and a "Reset quiz" button (two-step confirm, so it is never an accident). A second reset sits at the bottom.
- One section per module with its own colour, a module score and jump links. Questions are grouped under numbered section headings inside each module.
- An optional collapsible formula sheet per module, closed by default, for the user to open after trying.
- A results table (answered, correct, wrong, not attempted per module) and a "Build log prompt" and "Copy prompt" pair. The prompt names the study-log section for each module, lists each wrong question with the user's answer, the correct answer and the rule, lists right and not-attempted ids, and says to add the result as a new repetition without overwriting earlier ones.
- Light and dark mode, readable on a phone.

## Steps

1. **Collect the source content.** Read the topic text from `sources/text/` or the file the user names. For a quiz built from weak spots, re-read the current `study-log/STUDY_LOG.md` sections first (it changes; if it doesn't exist, build the quiz from the topic sources) and seed questions from the logged misses.
2. **Choose the structure.**
   - One topic: one module.
   - A consolidated quiz: one module per topic or course, in the user's priority order, each with its own `log` heading. Keep modules clearly separated.
   - Inside a module, put sections in this order when it helps: formula recall (multiple choice), then calculations from easy to hard, then application or comparison. Number the sections ("1. Formula recall").
   - Aim for 8 to 15 questions per module for a weak-spot quiz, and 15 to 30 for a first topic quiz. Weight questions toward the logged weak spots, and include a few cleared topics for spaced review.
3. **Write the bank** as a JSON list of modules. See `assets/example_bank.json` for a worked example. Each module:
   - `mod`: short name, for example "Investments 1"
   - `title`: heading shown for the module
   - `focus`: one sentence on what it tests
   - `log`: the study-log heading to update, for example `## Investments Topic 1`, reusing the heading already in `study-log/STUDY_LOG.md` if the topic is there. Without it the log prompt cannot say where to record the result.
   - `sheet`: optional HTML for the formula sheet (formulas, plus a short memory hook for each)
   - `qs`: the questions

   Each question:
   - `id`: unique across the whole quiz, with a module prefix (`IV-7`, `CB2-3`)
   - `sec`: section heading
   - `q`: the full question text. State the form of the answer ("Give 2 decimal places", "Use a minus sign for a loss").
   - `t`: `"n"` numeric, `"m"` multiple choice
   - `a`: the number, or the 0-based index of the correct option
   - `tol`: numeric tolerance (default 0.01; use about 0.011 where a rounded intermediate could shift the last digit)
   - `o`: options (for `"m"`)
   - `hint`: optional, shown above the answer box
   - `exp`: the working and the rule, always. This lands in the log prompt as "Rule or working", so make it specific enough to teach.
4. **Compute every numeric answer** with Python, at the precision the question asks for. Never write an answer from memory. Check that natural wrong answers (a missed `- 1`, wrong exponent, `r` not divided by 12) do not fall inside the tolerance.
5. **Build the page:**
   ```bash
   python3 ~/.claude/skills/revision-widget/scripts/build_quiz.py bank.json "<school folder>/revision/Quiz name.html" \
     --title "Quiz name" \
     --file "<school folder>/revision/Quiz name.html" \
     --note "This is practice made from my logged weak spots."
   ```
   - `--title` must not contain apostrophes or backslashes.
   - `--file` is the path shown in the log prompt.
   - `--note` is the one sentence the prompt gives the study log about what kind of quiz this is (a first topic quiz, practice from weak spots, extra practice the user asked for on topics they find hard). It is how the log records that the quiz is not an official assessment.
   - `--key` sets the storage key. The default comes from the title; set a new one only when the user wants a fresh quiz that does not share progress with an earlier one of the same name.
   - `--handoff` overrides the study-log file wording in the prompt (default is `study-log/STUDY_LOG.md` in the school folder).
   Save into `revision/` under the school folder, or the topic's own `revision/` folder for a single-topic quiz.
6. **Check the output.**
   - The script prints question counts per module and warns about a missing `log` heading or a question that leans on another question.
   - Run `node --check` on the extracted script block if the template was changed.
   - Test the logic in a browser: answer every question (two deliberately wrong), and confirm the counts, the per-module table and the generated prompt. The Browser pane shows `file://` pages as static snapshots where storage is blocked, so reload persistence cannot be tested there. Say so, and tell the user to open the file in Chrome or Edge (Safari may block storage for local files).
7. **Tell the user** in a few lines, with a clickable link: how many questions, the modules and sections, the formula sheets, that progress is saved and there is a Reset button, and how to log: finish, press Build log prompt, Copy prompt, paste it into Claude Code.

## Rules

- Every question stands alone. Restate the numbers in each question. Never write "Scenario A", "the same loan", "the above" or depend on another question.
- Marking is honest. No reveal that scores a question as right when it wasn't. Right or wrong, 0 or 1 per question.
- Retests and repeated drills use new numbers and the same concept, never the same question. If the user retakes the same quiz, log it as a repetition and say that the improvement may partly be recall of the answers.
- A quiz built from logged weak spots must expose the logged error patterns. Where the log records one (for example a wrong exponent), write at least one question that catches it, and make the explanation name the pattern.
- Leave out anything the user must write themselves: Gen AI thinking-point boxes, disclosures and assignment answers.
- Keep the page in sentence case, plain text, no emoji.
- After the user pastes back the generated prompt, log it with `study-log-update`: add the result as a new widget score with the date, keep earlier attempts, update only the named sections, do not commit.

## Fallback

For a tiny in-chat check (a few questions), skip the file, but still compute answers properly and offer the saved HTML version if the user wants to log the result.

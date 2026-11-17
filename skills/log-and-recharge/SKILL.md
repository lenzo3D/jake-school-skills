---
name: log-and-recharge
description: After a quiz or retest, log the user's result in the study log and then build an extra practice set that is not logged. Use when the user says to log it and make recharge, extra or more practice questions, "practice that doesn't log", personal practice, or when they report a retest result (all correct, some wrong) and want to keep drilling a hard area. Also use to teach a missed concept first (formulas, method, worked example) before the retest. Not for the first quiz of a topic (use revision-widget) or for a log update alone (use study-log-update).
---

# Log and recharge

Two jobs in order: record the result, then give the user practice that never touches the record. The practice is for confidence only, so its scores are not saved anywhere.

## Steps

1. **Work out what happened.** From the user's message and the earlier quiz, note which questions were missed, the score, and the reason (for example "did not know the formulas"). If the user only says "all correct", record the retest as "user reports all correct, no widget score".

2. **Teach before testing, if they missed a concept.** In the reply, give a short lesson: the letters and what they mean, each formula, one worked example with new numbers (not any quiz numbers), and the common mistakes. Offer a cheat sheet if they ask. Do this before building a retest.

3. **Log the result.** Invoke `study-log-update` and follow it. For this project:
   - the file is `study-log/STUDY_LOG.md` in the school folder (the script creates it if missing)
   - use one heading per topic, for example `## Commercial Banking Topic 2`, and reuse it if it already exists
   - record: files made, verified facts with source and slide, anything unconfirmed or assumed, the scores, and weak spots in priority order
   Read the section back and show it if the user asks.

4. **Build the recharge set.** Use `revision-widget` with a new bank, in the topic folder:
   - name the file so it is clearly unlogged, for example `Topic 2 practice - <area> (not logged).html`
   - 15 to 20 questions, a little harder than the retest, all with new numbers
   - cover the weak spots in order, building up: setup, then step by step, then comparison and trap questions
   - work out every numeric answer with Python before writing it, and set tolerances to match the stated decimals
   - the explanation after each answer shows the working
   - run `node --check` on the script block
   - plain file only, with nothing that saves, sends or posts scores

5. **Do not log the practice.** No log entry, no memory note, no scores recorded, even if the user reports results later. Say so in the reply. Only log if the user later says to.

6. **Report in one short block:** what was logged and where, the practice file as a link, the question count, what it covers, and that it is not logged. Mention anything unconfirmed that went into the log.

## Rules

- Never store secrets in the log.
- Keep scores specific. A user report with no widget score is recorded as a report.
- Retests and recharge sets use new numbers, never the quiz numbers.
- Do not tell the user a file works in a browser unless it was opened. Say it passed a syntax check.
- Sentence case, plain text, no emoji in the widgets.

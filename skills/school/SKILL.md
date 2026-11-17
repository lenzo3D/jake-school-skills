---
name: school
description: The entry point and router for all school skills. Use whenever the user asks about school work in general, a tutorial, homework, an assignment, a quiz or revision, a lecture recording, study progress, marking, or asks which school skill to use or what school skills exist. It ALWAYS shows a clickable multiple-choice widget (the AskUserQuestion tool) asking which skill to run, never a plain-text list, then runs the chosen skill.
---

# School skills (router)

This is the first skill to use for any school request. Its job is to find out what the user needs with a clickable widget, then hand over to the right skill. Run one skill at a time.

## The one rule that matters most

**Every time this skill runs, show the user a clickable widget with the AskUserQuestion tool. Never answer with a plain-text list of skills or a typed question.** This applies even when the request looks clear: the widget lets the user confirm or change the choice in one click. Only if the AskUserQuestion tool does not exist in your environment, fall back to a short numbered list and ask the user to reply with a number.

## Steps

1. **Read the request** and work out which skill or group it most likely points to (see the map below). Do not start any work yet.

2. **Show the widget.** Call AskUserQuestion with one question, "What do you want to do?", and these four groups as options (4 is the maximum the widget allows). Put the best match first and add "(Recommended)" to its label. If the request already clearly names a group, skip to step 3 and show that group's widget straight away.
   - **Tutorials, homework, assignments** (import sources, complete the work, write an explanation file)
   - **Revision and practice** (revision quiz, mock Kahoot, retest and extra practice)
   - **Lectures and marking** (transcribe a lecture video, mark an assignment)
   - **Study log** (record progress, view the summary)

3. **Show the skill widget** for the chosen group with AskUserQuestion, one question, options from the map below. Put the best match first with "(Recommended)". Keep each option's description to one line saying what it does for the user's use case.

   | Group | Options (skill name, what to say) |
   |---|---|
   | Tutorials, homework, assignments | `import-sources`: load slides, briefs, rubrics and notes as sources (do this first). `complete-docx-work`: complete any Word task (tutorial, homework or full assignment) in light blue inside the original file. `explain-my-work`: write a separate file to talk through your work with a teacher. |
   | Revision and practice | `revision-widget`: self-marking revision quiz or retest. `kahoot-mock`: timed mock Kahoot with speed scoring and rivals. `log-and-recharge`: log a retest, then extra practice that is not logged. |
   | Lectures and marking | `lecture-video-transcribe`: turn a lecture recording into a timestamped transcript source. `mark-my-work`: realistic mark and fix list against the rubric. |
   | Study log | `study-log-update`: record scores and weak spots. `study-log-summary`: show the whole log as one table (read-only). |

   Every widget includes the automatic "Other" choice, so the user can type something else, for example "which skill should I use?". If they do, answer briefly and show the widget again.

4. **Run the chosen skill.** Say in one line which skill you are starting and why, then invoke it with the Skill tool. Pass along anything the user already told you (topic, file names, links).

## Order and dependencies

- `import-sources` comes before `complete-docx-work`, which comes before `explain-my-work`. If the user picks answering or explaining and the sources are not imported yet (no `sources/text/` in the topic folder), tell them in one line and run `import-sources` first.
- `lecture-video-transcribe` saves its transcript in `sources/text/`, so the coursework skills can use it as a source. If slides also need importing, run `import-sources` too.
- `revision-widget` and `kahoot-mock` need the topic's sources imported. `log-and-recharge` and `study-log-update` record results in `study-log/STUDY_LOG.md`.

## Rules

- Coursework completed without importing its sources is not sourced. Import first.
- Each skill's own rules apply, for example light-blue answers and no formatting changes in `complete-docx-work`.
- Do not start work before the user has clicked an option.
- One widget at a time, one skill at a time. Do not run several skills after a single click.

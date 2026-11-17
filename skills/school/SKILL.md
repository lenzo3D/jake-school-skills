---
name: school
description: Router for the user's university (school) skills. Use whenever the user asks about school work in general, a tutorial, homework, a quiz or revision, study progress, or asks which school skill to use or what school skills exist. It lists the school skills, picks the one that matches the request, and runs it.
---

# School skills

This is the entry point for school work. Read the table, pick the one skill that fits the request, then run it by invoking that skill with the Skill tool. Run one skill at a time. Some skills depend on earlier steps, so check the order below.

## The skills

| Skill | Use it when | Order |
|---|---|---|
| `tutorial-import-files` | Load the course files (PPTX, DOCX, PDF, text) into plain text so later steps can cite them. Also the start of any tutorial job. | Step 1 |
| `tutorial-answer-docx` | Answer a .docx tutorial or worksheet in its own file, in light blue, without changing its formatting. | Step 2 |
| `tutorial-explanation-docx` | Write a separate explanation file so the user can talk through the answers with a teacher. | Step 3 |
| `revision-widget` | Build a self-marking quiz or retest for a topic, with instant feedback. | Any time |
| `kahoot-mock` | Build a timed mock Kahoot (10 questions, speed scoring, rivals, podium) for the current topic, to practise for the in-person lecture Kahoot. | Any time |
| `lecture-video-transcribe` | Turn a recorded lecture video (link or file) into a timestamped Markdown transcript saved with the slides, so it can be cited like a source. | Any time |
| `study-log-update` | Record study progress, scores and weak spots in the study log. | After a quiz, practice or tutorial |
| `log-and-recharge` | Log a retest result, then build extra practice that is not logged (and teach the concept first if needed). | After a retest |
| `study-log-summary` | Show a summary of the whole study log (scores, retests, weak spots, patterns). Read-only. | Any time |
| `lecturer-mark-assignment` | Get a realistic mark, indicative grade and fix list for a finished assignment, marked by an independent Opus subagent against the brief's rubric. | Before submitting |

## How to route

1. **Tutorial or homework file given:** start with `tutorial-import-files` if the sources aren't imported yet, then `tutorial-answer-docx`. Use `tutorial-explanation-docx` only when the user asks for an explanation file or study notes.
2. **Quiz, revision or retest:** use `revision-widget`. For a timed Kahoot rehearsal, use `kahoot-mock`. For a lecture recording to transcribe or take notes from, use `lecture-video-transcribe`, then `tutorial-import-files` if slides also need importing. For written practice, mark the answers in the chat.
3. **Progress or "update my study log":** use `study-log-update`. If the user also wants extra practice that doesn't count, or reports a retest and wants to keep drilling, use `log-and-recharge`. To only view the whole log ("show my study log", "where do I stand"), use `study-log-summary`.
4. **"Mark my assignment" or "what grade would I get":** use `lecturer-mark-assignment`.
5. **Unsure, or no request given:** always ask with the AskUserQuestion tool (clickable options), never a plain-text list. Make the options the matching skills, for example "Answer the tutorial", "Revise for it", "Log progress". One question only.

## Rules

- A tutorial answered without importing its sources is not sourced. Import first.
- Each skill's own rules apply, for example light-blue answers and no formatting changes in `tutorial-answer-docx`.
- When you invoke a skill, say which one and why in one line.

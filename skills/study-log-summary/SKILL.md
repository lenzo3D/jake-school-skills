---
name: study-log-summary
description: Show the user a summary of their whole study log (study-log/STUDY_LOG.md in their school folder): one table of every topic with its quiz score, retest result and top weak spots, plus patterns across topics and gaps in the record. Use when the user says show my study log, summarise my progress, where do I stand, what are my weak spots overall, or asks to see the log. Read-only. To change the log use study-log-update.
---

# Study log summary

Read the log and report it. Do not edit anything.

## Steps

1. **Find the file.** `study-log/STUDY_LOG.md` in the school folder. If it doesn't exist, say there is no study log yet and suggest running a revision quiz and logging it.
2. **Read every topic section** (list them with `grep -n "^## " study-log/STUDY_LOG.md`). Always re-read the file; never answer from earlier in the conversation, because it may have changed.
3. **Build one table**, oldest topic first or grouped by course: course and topic, recorded date, quiz score, retest result, top 2 to 3 weak spots. Copy scores exactly as logged. Where a retest is "user reports", say so.
4. **Add the patterns** across topics: repeated weak areas (for example calculation setup, look-alike terms), and anything missing from the record (no score recorded, user-reported only).
5. **Link the file** as a clickable markdown link, and offer one next step at most (for example "retest the weakest topic").

## Rules

- Read-only. Never update, commit or reformat the log.
- Do not invent or round scores. If a score is not in the log, write "not recorded".
- Keep it to one table plus a short patterns list.

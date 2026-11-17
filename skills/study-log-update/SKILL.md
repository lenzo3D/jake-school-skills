---
name: study-log-update
description: Record the user's study progress, scores, weak spots and verified facts in one study log file (study-log/STUDY_LOG.md in their school folder) so later sessions know where they stand. Use when the user says to update my study log, save progress, remember what I got wrong, log my study state, and after a quiz, practice set or tutorial that changes what the user knows.
---

# Study log update

Keep one section per topic in the study log, `study-log/STUDY_LOG.md` inside the user's school folder (the folder that holds the `<Course> Topic N/` folders). It holds the user's scores, weak spots and verified course facts. The update script creates the file and folder if they don't exist yet, so there is nothing to set up.

## Steps

1. **Find the log file.** `study-log/STUDY_LOG.md` in the school folder. If it doesn't exist yet, that is fine: the script creates it.
2. **Pick the heading.** One heading per topic, in the form `## <Course> Topic N`, for example `## Investments Topic 1`. Run `grep -n "^## " study-log/STUDY_LOG.md` first and reuse the existing heading for that topic, so the script replaces the section instead of adding a duplicate.
3. **Write the new body** to a temporary markdown file. Use the same structure every time:
   - one line on the course and the date
   - the completed work and where its file is
   - verified facts, with the figures and their source
   - the scores so far
   - weak spots in priority order
   Only record facts that were checked. Mark anything still unconfirmed as unconfirmed.
4. **Run the script:**
   ```bash
   python3 ~/.claude/skills/study-log-update/scripts/update_study_log.py study-log/STUDY_LOG.md --heading "## Investments Topic 1" --body body.md --updated "2026-10-29"
   ```
   The `--updated` value is the new text of the `Last updated:` line (usually the date). The script replaces the section in place, or adds a new section at the top if the topic is new.
5. **Check the result.** Read the section back. Confirm no other sections changed.
6. **Tell the user** which file changed and which section.

## Rules

- Never store passwords, tokens or other secrets in the log.
- Keep scores and weak spots specific, for example "annualizing: exponent is 12 ÷ months held", not "needs more practice".

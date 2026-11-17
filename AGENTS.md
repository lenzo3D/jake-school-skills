# School skills: instructions for AI assistants

This repo holds study skills in `skills/<name>/SKILL.md`. When the user asks for school work, start with the `school` skill (it asks which skill to run with a clickable widget where your assistant supports one), then read its `SKILL.md` in full, and follow it. Run scripts with `python3` from the skill's folder. Work inside the user's school folder, not inside this repo.

| Skill | Use it when the user asks to |
|---|---|
| school | ALWAYS start here: shows a clickable widget asking which skill to run, then runs it |
| import-sources | import or load slides, PDFs, notes as sources (do this first) |
| complete-docx-work | complete any .docx coursework (tutorial, homework or assignment) in light blue inside the original file |
| explain-my-work | write a separate explanation file for a teacher |
| revision-widget | build a self-marking revision quiz, retest or formula drill |
| lecture-video-transcribe | transcribe a lecture recording into a timestamped source |
| mark-my-work | mark an assignment against its rubric before submission |
| study-log-update | record scores and weak spots in study-log/STUDY_LOG.md |
| log-and-recharge | log a retest, then build unlogged extra practice |
| study-log-summary | summarise the study log (read-only) |
| kahoot-mock | build a timed mock Kahoot for a topic |

Rules that apply to all skills: never enter or store passwords, MFA codes, cookies or signed links; ask before installing software or downloading files; compute numbers with code, not from memory; say plainly what is unverified.

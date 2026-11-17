---
name: complete-docx-work
description: Complete any university coursework that is a Word (.docx) file (tutorial, homework, worksheet, case study, problem set or full assignment) by typing the answers into the original document in light blue, without changing its fonts, layout or formatting. Use this whenever the user gives a .docx tutorial, homework, assignment or case study and asks you to answer, do, complete or fill it in, or asks for short, exam-style or human-sounding answers. Requires the sources to be imported first (see import-sources). Do not use it to write the separate explanation file; that is explain-my-work.
---

# Complete coursework in its own Word file

This is step 2 of 3. The source text should already be in `sources/text/` (step 1, `import-sources`). The result is the original file with the answers typed in, and nothing else changed.

This is not limited to tutorials or homework. Use it for any Word-based coursework, including full assignments. For an assignment, read the brief and its marking rubric first and write to the rubric's criteria. Remind the user to follow their school's rules on AI use and to disclose it where required.

The user's rules: edit the Word doc directly, do not change the font, format or layout, answers in light blue, short and realistically human, academic standard.

## Steps

1. **Check the sources are imported.** If `sources/text/` is missing or empty, run `import-sources` first.

2. **Find the document and keep a clean copy.** If it is in Downloads, copy it into the topic's `work/` folder (or its existing `tutorial/` folder) and work on that copy. Then make a pristine backup in the scratchpad:
   `cp "<document>.docx" "$SCRATCH/pristine.docx"`
   Every fill runs from the pristine copy, so reruns never stack answers.

3. **Read the sources that the questions need.** Open the relevant `.txt` files in `sources/text/`. Read the parts the questions point to: the regulation paragraphs, the checklist, the slides, the case article. Note page and slide numbers for citations.

4. **Map the document.** Run:
   `python3 ~/.claude/skills/complete-docx-work/scripts/inspect_docx.py "$SCRATCH/pristine.docx"`
   It lists each paragraph with its index and font, and each table row. Note the question blocks and the empty table cells.

5. **Write `answers.json`** in the scratchpad (format below), following the style rules.

6. **Fill the document in place.** Run:
   `python3 ~/.claude/skills/complete-docx-work/scripts/fill_answers.py "$SCRATCH/pristine.docx" "<document path>.docx" answers.json`
   The script copies each new run's font from the body text, sets the colour, and checks that every original paragraph is still present in order. Read its output. If it warns, fix the anchor and rerun from the pristine copy.

7. **Verify.** Run `inspect_docx.py` on the output and check that the questions and table are unchanged, that each answer sits under its question, and that the new runs use the body font.

8. **Report.** Tell the user the file path, how many items were filled, and anything you could not answer from the sources. Then hand over to `explain-my-work` if they want the teacher file.

## answers.json format

```json
{
  "colour": "5B9BD5",
  "inserts": [
    {"after_question": "Question 1", "lines": ["Banks borrow short and lend long. ...", "The risk becomes systemic because ..."]},
    {"after_question": "Question 2", "lines": ["Answer:", "Under MAS Notice 656 (para 7) ..."]},
    {"after_text": "To provide an overview", "lines": ["Answer: the three stages are ..."]}
  ],
  "table_fills": [
    {"table": 1, "row": 2, "col": 2, "text": "Portfolio Management"}
  ]
}
```

- `after_question` places the answer after the last text of that question's block. This works when the question has tables or list items.
- `after_text` is for a sentence between a question and its table.
- Each entry in `lines` is one paragraph. Keep one thought per line.
- `table_fills` fills empty cells only. Use the table index and 0-based row and column from `inspect_docx.py`.
- The colour defaults to light blue, `5B9BD5`. Change it only if the user names another colour.

## Writing style

The user has asked for shorter, human answers more than once. Hold to this:

- Answer in the first sentence, then give the reasons or the working.
- Plain words and short sentences. Write like a student who knows the material in an exam, not like a textbook or a chatbot.
- Avoid: "delve", "crucial", "it is important to note", "moreover", "in conclusion", "in summary", "robust", "a testament to", em dashes, bold text, headings inside an answer, and "Specifically" as a sentence opener.
- Cite sources briefly, e.g. (MAS 656, para 7) or (Lecture 1, slide 23).
- Show working for calculations, one line per step.
- Keep each sub-answer to about 2 to 5 sentences. Give parts (a) to (d) their own lines.
- Flag stray or unclear data in the question. Say what you ignored and why.
- Do not invent facts or figures. If the sources do not cover something, say what they do cover.

## Gotchas

- Do not set font names, add styles, or add tables. Fill the existing table cells.
- Run the scripts without `-I`. It hides the user-site python-docx install. If python-docx is missing, run `python3 -m pip install --user python-docx`.
- If Word has the document open, a `~$` lock file sits next to it. Ask the user to close Word before you save.
- Never edit the Downloads original.

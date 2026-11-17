---
name: complete-docx-work
description: Complete any university coursework that is a Word (.docx) file (tutorial, homework, worksheet, case study, problem set or full assignment) by typing the answers into the original document without changing its fonts, layout or formatting. Tutorials and homework get light-blue answers; assignments get plain text that matches the document. It always asks which kind it is first, with a clickable widget. Use this whenever the user gives a .docx tutorial, homework, assignment or case study and asks you to answer, do, complete or fill it in, or asks for short, exam-style or human-sounding answers. Requires the sources to be imported first (see import-sources). Do not use it to write the separate explanation file; that is explain-my-work.
---

# Complete coursework in its own Word file

This is step 2 of 3. The source text should already be in `sources/text/` (step 1, `import-sources`). The result is the original file with the answers typed in, and nothing else changed.

This is not limited to tutorials or homework. Use it for any Word-based coursework, including full assignments.

## Step 0: ask which kind of work it is (always)

The kind of work decides the colour and the writing style, so ask before doing anything else. Use the AskUserQuestion tool (a clickable widget, never a typed list) with one question, "What kind of work is this?", and two options:

- **Tutorial or homework** (Recommended when the request says tutorial, homework, worksheet or problem set). Answers go in light blue, `5B9BD5`, in short exam-style answers.
- **Assignment**. Answers go in plain default text, with no colour set, so they match the assignment's own body text. Written to the brief and rubric, in full academic prose.

If the user's message already states which kind it is, do not ask again: say in one line which mode you are using and continue. If the user is unsure, an assignment is usually the graded piece with a brief, a word count and a marking rubric, and tutorials and homework are the weekly question sheets. Ask which one it is. Never mix the two modes in one document.

Set `"colour": "5B9BD5"` in `answers.json` for a tutorial or homework, and `"colour": null` for an assignment.

Remind the user to follow their school's rules on AI use and to disclose it where required. This matters most for assignments.

The user's rules: edit the Word doc directly and do not change the font, format or layout. Tutorial and homework answers are in light blue, short and realistically human. Assignment answers are in plain default text, written to the brief.

## Steps

1. **Check the sources are imported** (after Step 0). If `sources/text/` is missing or empty, run `import-sources` first.

2. **Find the document and keep a clean copy.** If it is in Downloads, copy it into the topic's `work/` folder (or its existing `tutorial/` folder) and work on that copy. Then make a pristine backup in the scratchpad:
   `cp "<document>.docx" "$SCRATCH/pristine.docx"`
   Every fill runs from the pristine copy, so reruns never stack answers.

3. **Read the sources that the questions need.** Open the relevant `.txt` files in `sources/text/`. Read the parts the questions point to: the regulation paragraphs, the checklist, the slides, the case article. Note page and slide numbers for citations.

4. **Map the document.** Run:
   `python3 ~/.claude/skills/complete-docx-work/scripts/inspect_docx.py "$SCRATCH/pristine.docx"`
   It lists each paragraph with its index and font, and each table row. Note the question blocks and the empty table cells.

5. **Write `answers.json`** in the scratchpad (format below), following the style rules for the kind of work. For an assignment, read the brief and its marking rubric first (they should be imported in `sources/text/`), note the word count, structure, referencing style and each criterion, and write to those.

6. **Fill the document in place.** Run:
   `python3 ~/.claude/skills/complete-docx-work/scripts/fill_answers.py "$SCRATCH/pristine.docx" "<document path>.docx" answers.json`
   The script copies each new run's font from the body text, sets the colour (tutorial and homework only), and checks that every original paragraph is still present in order. Read its output. If it warns, fix the anchor and rerun from the pristine copy.

7. **Verify.** Run `inspect_docx.py` on the output and check that the questions and table are unchanged, that each answer sits under its question, and that the new runs use the body font. For an assignment, also check that no run is light blue and that the word count and structure match the brief.

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
- `"colour"` is `"5B9BD5"` (light blue) for a tutorial or homework. For an assignment write `"colour": null`, which sets no colour so the answers use the document's own text colour and font. Use another colour only if the user names one.

## Writing style: tutorials and homework

The user has asked for shorter, human answers more than once. For tutorials and homework, hold to this:

- Answer in the first sentence, then give the reasons or the working.
- Plain words and short sentences. Write like a student who knows the material in an exam, not like a textbook or a chatbot.
- Avoid: "delve", "crucial", "it is important to note", "moreover", "in conclusion", "in summary", "robust", "a testament to", em dashes, bold text, headings inside an answer, and "Specifically" as a sentence opener.
- Cite sources briefly, e.g. (MAS 656, para 7) or (Lecture 1, slide 23).
- Show working for calculations, one line per step.
- Keep each sub-answer to about 2 to 5 sentences. Give parts (a) to (d) their own lines.
- Flag stray or unclear data in the question. Say what you ignored and why.
- Do not invent facts or figures. If the sources do not cover something, say what they do cover.

## Writing style: assignments

- Follow the brief first: required structure, headings, word count, referencing style and any limits. Write to each rubric criterion so a marker can find it.
- Full academic prose: clear paragraphs with a point, evidence from the imported sources, and a link back to the question. Use the document's own headings and template, and add headings only where the brief asks for them.
- Plain, natural wording. Avoid padding and the filler listed above. No em dashes.
- Cite properly in the style the brief asks for. Cite only sources that were imported or that the user gave. Never invent references, figures or quotes. If evidence is missing, say what is missing and ask the user.
- Keep within the word count. Report the count.
- The user stays responsible for the work: tell them to read it, check every figure and citation, and follow their school's AI-use and disclosure rules.

## Gotchas

- Do not set font names, add styles, or add tables. Fill the existing table cells.
- Run the scripts without `-I`. It hides the user-site python-docx install. If python-docx is missing, run `python3 -m pip install --user python-docx`.
- If Word has the document open, a `~$` lock file sits next to it. Ask the user to close Word before you save.
- Never edit the Downloads original.

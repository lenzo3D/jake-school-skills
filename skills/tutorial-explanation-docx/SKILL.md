---
name: tutorial-explanation-docx
description: Write a separate Word file that explains a completed tutorial's answers in enough detail for a student to talk through with a teacher, including the reasoning, traps to avoid, likely follow-up questions and sources. Use this whenever the user asks for an explanation file, a study guide or notes to prepare for the teacher's questions, or "how to explain" the answers, after the tutorial has been answered. Requires the tutorial to be answered (see tutorial-answer-docx) and the sources to be imported (see tutorial-import-files).
---

# Explanation file for the teacher

This is step 3 of 3. The explanation file is separate from the tutorial. It is for the student to read and talk through with the teacher, so it can be longer and more detailed than the answers in the tutorial. It must agree with the answers in the tutorial.

## Steps

1. **Read the answers as they stand.** Take the text of the answered tutorial, from the light-blue paragraphs and cells, so the explanation matches what the student will hand in. Read the question text too. Do not write a different answer from the one in the tutorial. If you find a wrong figure or claim, fix the tutorial first, using `tutorial-answer-docx`, and then come back here.

2. **Read the sources you cite.** Use `sources/text/` from the import step. Check the paragraph and slide numbers you will quote.

3. **Write `explain.md`** in the scratchpad, using the structure below.

4. **Build the Word file:**
   `python3 ~/.claude/skills/tutorial-explanation-docx/scripts/build_explanation.py explain.md "<tutorial folder>/<Tutorial name> - Answer Explanations.docx"`
   The script sets Arial 11 by default, to match the tutorial. Pass a font name as a third argument if the tutorial uses another.

5. **Check the file.** Open it with `python3 -c` and confirm the headings and paragraph count look right.

## Structure, per question

- **Short answer:** two or three sentences.
- **Step by step:** the reasoning in order, including the traps. For example, testing the individual companies instead of the group totals.
- **Likely follow-up questions:** two or three, each with a short answer.
- **Sources to cite:** paragraph numbers, slide numbers and article titles.

End the file with a short glossary of the key terms.

## Style

- Plain, direct sentences, like the answers. The extra length goes into the reasons, not into padding.
- Be clear about what is established and what is inferred. If a case study is one-sided, say so.
- Do not present general knowledge as if it came from a source. Say when a point is outside the sources.
- Do not use em dashes or bold text in the body.

## Gotchas

- Run the build script without `-I`, so the user-site python-docx install is found.
- If the output file is open in Word, Word will block the save. Ask the user to close it first.
- Use the tutorial's own name in the file name, so the two files sit together.

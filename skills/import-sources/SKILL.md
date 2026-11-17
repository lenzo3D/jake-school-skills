---
name: import-sources
description: Import the course files that any piece of coursework (tutorial, homework, assignment, case study, exam practice) depends on (PDF regulations and articles, PPTX lecture slides, DOCX notes, text files) into plain text that later steps can search and cite. Use this whenever the user says to import, attach, load or use files as the information source for a tutorial, homework, assignment, case study or exam question, or drops in lecture slides, regulatory notices, guidelines or articles and asks you to remember them or answer from them. Also use it at the start of any coursework job, before answering, and when the user asks what is in their sources folder.
---

# Import source files

This is step 1 of 3 in the coursework pipeline (import, complete, explain). Its job is to turn each source file into text, kept in the project folder, so that later steps can find the right paragraphs and slides.

## Steps

1. **Find the source folder.** In a project such as `Commercial Banking Topic 1`, the sources usually sit in `sources/`. If the user just named files in Downloads, copy them into `<project>/sources/` first and leave the Downloads originals alone.

2. **Extract the text.** Run:

   ```bash
   python3 ~/.claude/skills/import-sources/scripts/extract_sources.py "<project>/sources" "<project>/sources/text"
   ```

   It writes one `.txt` per source into `sources/text/`. PDFs keep `##### PAGE n` markers, and PPTX files keep `##### SLIDE n` markers, so the AI can find the right page or slide when it reads them. Lock files (`~$...`) and hidden files are skipped.

3. **Check the output.** Look at the character counts the script prints. A PDF that prints almost nothing is probably scanned images. Say so to the user and ask for a text version, because pypdf cannot read images. Read enough of each file to know what it covers, and note the paragraph numbers, section headings or slide numbers you will need.

4. **Report what was imported.** Tell the user, in a short list, each file, what it is (for example "MAS Notice 656, the single counterparty limit"), and where its text is. Do not paste the text into chat.

## Requirements

- Python 3 with `pypdf` for PDFs. If it is missing, run `python3 -m pip install --user pypdf`.
- PPTX and DOCX need only the standard library.
- Run the script without `-I`, so user-site packages are found.

## Notes

- Keep the extracted text next to the sources, not in the scratchpad. The answering and explaining steps read it from there, and it is useful for later questions too.
- Re-run the script when a source changes. It overwrites the text files.
- If the user asks you to remember the files for future questions, say that the text is saved in `sources/text/` and that the sources are kept in the project folder.

Next step: `complete-docx-work`.

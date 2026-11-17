#!/usr/bin/env python3
"""Print the body of a tutorial .docx in order, so answer slots can be found.

Usage: python3 inspect_docx.py <tutorial.docx>

Each body paragraph is printed with its index, style, and the font of its first
text run. Tables are printed row by row with [table index] and (row, col) so
they can be used in answers.json "table_fills".
Run without -I so the user-site python-docx install is found.
"""
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


def font_of(par):
    for run in par.runs:
        if run.text.strip():
            size = run.font.size.pt if run.font.size else None
            color = str(run.font.color.rgb) if run.font.color and run.font.color.rgb else None
            return f"{run.font.name}/{size}/bold={run.bold}/color={color}"
    return "-"


def main():
    doc = Document(sys.argv[1])
    table_no = 0
    par_no = 0
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            par = Paragraph(el, doc)
            print(f"P{par_no:<3} {par.style.name:<15} {font_of(par):<40} {par.text[:70]!r}")
            par_no += 1
        elif el.tag == qn("w:tbl"):
            table = doc.tables[table_no]
            print(f"--- TABLE {table_no}: {len(table.rows)} rows x {len(table.columns)} cols")
            for r, row in enumerate(table.rows):
                cells = [c.text.replace("\n", " / ")[:30] for c in row.cells]
                print(f"    row {r}: {cells}")
            print("--- end table")
            table_no += 1


if __name__ == "__main__":
    main()

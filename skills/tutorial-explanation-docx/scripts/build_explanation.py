#!/usr/bin/env python3
"""Build the teacher-facing explanation Word file from a simple Markdown file.

Usage: python3 build_explanation.py <notes.md> <out.docx> [font]

Supported Markdown: "# " title, "## " and "### " headings, "- " bullets,
"  - " nested bullets, "1. " numbered lines, "---" rules (ignored), **bold**,
*italic*, and plain paragraphs. The default font is Arial, the usual tutorial
font. Pass a different font name as the third argument if needed.
"""
import re
import sys

from docx import Document
from docx.shared import Pt


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*)")


def add_runs(par, text):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            par.add_run(part[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            par.add_run(part[1:-1]).italic = True
        else:
            par.add_run(part)


def main():
    src, out = sys.argv[1], sys.argv[2]
    font = sys.argv[3] if len(sys.argv) > 3 else "Arial"
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = font
    normal.font.size = Pt(11)

    for raw in open(src, encoding="utf8").read().split("\n"):
        line = raw.rstrip()
        if not line.strip() or line.strip() == "---":
            continue
        if line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=0)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
        elif re.match(r"^\s+- ", line):
            add_runs(doc.add_paragraph(style="List Bullet 2"), re.sub(r"^\s+- ", "", line))
        elif line.startswith("- "):
            add_runs(doc.add_paragraph(style="List Bullet"), line[2:])
        elif re.match(r"^\d+\. ", line):
            num, rest = line.split(". ", 1)
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Pt(18)
            par.paragraph_format.first_line_indent = Pt(-18)
            add_runs(par, f"{num}.\t{rest}")
        else:
            add_runs(doc.add_paragraph(), line)

    doc.save(out)
    print("saved", out)


if __name__ == "__main__":
    main()

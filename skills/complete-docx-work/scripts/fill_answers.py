#!/usr/bin/env python3
"""Insert answers into a tutorial .docx without changing its existing formatting.

Usage:
  python3 fill_answers.py <pristine.docx> <out.docx> <answers.json>

Run it on a pristine copy every time (never on an already-filled file), so
reruns give the same result. Put <out.docx> at the tutorial's own path to edit
it in place.

answers.json:
{
  "colour": "5B9BD5",
  "inserts": [
    {"after_question": "Question 1", "lines": ["First answer paragraph.", "Second."]},
    {"after_text": "Answer the question below", "lines": ["..."]}
  ],
  "table_fills": [
    {"table": 1, "row": 2, "col": 2, "text": "Portfolio Management"}
  ]
}

after_question: the new lines go after the last non-empty paragraph of that
question's block (the block runs from the paragraph starting with the given
text up to the next paragraph starting with "Question" or equal to "End").
after_text: the new lines go after the first paragraph starting with the text.
table_fills: "table" is the index of the table in the document (0-based, as in
inspect_docx.py), "row" and "col" are 0-based. Existing cell text is kept if
you target a non-empty cell, so only fill empty slots.

Formatting rules the script follows:
- New runs copy the rPr (font, size, spacing) of a body paragraph's first run.
- New paragraphs copy the pPr of that body paragraph, minus list numbering.
- Only the colour is set on new runs. Font names are never set.
After writing, it checks that every original non-empty paragraph is still in
the output in the same order, and prints the counts it inserted.
"""
import copy
import json
import sys

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor
from docx.text.run import Run


def body_elements(doc):
    return [el for el in doc.element.body.iterchildren() if el.tag in (qn("w:p"), qn("w:tbl"))]


def para_text(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def find_question_block(items, prefix):
    start = next(
        (i for i, el in enumerate(items) if el.tag == qn("w:p") and para_text(el).startswith(prefix)),
        None,
    )
    if start is None:
        raise SystemExit(f"no paragraph starts with {prefix!r}")
    end = len(items)
    for j in range(start + 1, len(items)):
        if items[j].tag == qn("w:p"):
            text = para_text(items[j])
            if text.startswith("Question") or text == "End":
                end = j
                break
    return items[start:end], items[start]


def template_for(block):
    """Pick a body paragraph to copy formatting from: prefer one without list numbering."""
    candidates = [el for el in block[1:] if el.tag == qn("w:p") and para_text(el)]
    for el in candidates:
        ppr = el.find(qn("w:pPr"))
        if ppr is None or ppr.find(qn("w:numPr")) is None:
            return el
    return candidates[0] if candidates else block[0]


def run_props(par_el):
    for r in par_el.iter(qn("w:r")):
        if any((t.text or "").strip() for t in r.iter(qn("w:t"))):
            rpr = r.find(qn("w:rPr"))
            return copy.deepcopy(rpr) if rpr is not None else None
    return None


def make_paragraph(template_el, rpr, text, colour):
    p = copy.deepcopy(template_el)
    for child in list(p):
        if child.tag != qn("w:pPr"):
            p.remove(child)
    ppr = p.find(qn("w:pPr"))
    if ppr is not None:
        for num in ppr.findall(qn("w:numPr")):
            ppr.remove(num)
        style = ppr.find(qn("w:pStyle"))
        if style is not None and style.get(qn("w:val")) == "ListParagraph":
            ppr.remove(style)
    run = OxmlElement("w:r")
    if rpr is not None:
        run.append(copy.deepcopy(rpr))
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    p.append(run)
    Run(run, None).font.color.rgb = RGBColor.from_string(colour)
    return p


def insert_lines(anchor_el, template_el, lines, colour):
    rpr = run_props(template_el)
    current = anchor_el
    for line in lines:
        new_p = make_paragraph(template_el, rpr, line, colour)
        current.addnext(new_p)
        current = new_p


def fill_table_cell(doc, table_idx, row, col, text, colour):
    table = doc.tables[table_idx]
    cell = table.rows[row].cells[col]
    rpr = None
    for r_el in cell._tc.iter(qn("w:r")):
        if any((t.text or "").strip() for t in r_el.iter(qn("w:t"))):
            rpr = r_el.find(qn("w:rPr"))
            break
    if rpr is None:
        for other in table.rows:
            for c in other.cells:
                for r_el in c._tc.iter(qn("w:r")):
                    if any((t.text or "").strip() for t in r_el.iter(qn("w:t"))):
                        rpr = r_el.find(qn("w:rPr"))
                        break
                if rpr is not None:
                    break
            if rpr is not None:
                break
    run = OxmlElement("w:r")
    if rpr is not None:
        run.append(copy.deepcopy(rpr))
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    cell.paragraphs[0]._p.append(run)
    Run(run, None).font.color.rgb = RGBColor.from_string(colour)


def check_original_kept(pristine_path, out_path):
    def texts(path):
        return [p.text.strip() for p in Document(path).paragraphs if p.text.strip()]

    original = texts(pristine_path)
    filled = texts(out_path)
    it = iter(filled)
    missing = [t for t in original if not any(t == f for f in it)]
    return missing


def main():
    pristine, out_path, answers_path = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = json.load(open(answers_path, encoding="utf8"))
    colour = spec.get("colour", "5B9BD5")
    doc = Document(pristine)

    inserted = 0
    for item in spec.get("inserts", []):
        items = body_elements(doc)
        if "after_question" in item:
            block, heading = find_question_block(items, item["after_question"])
            body_paras = [el for el in block if el.tag == qn("w:p") and para_text(el)]
            anchor = body_paras[-1] if body_paras else heading
            template = template_for(block)
        else:
            anchor = next(
                (el for el in items if el.tag == qn("w:p") and para_text(el).startswith(item["after_text"])),
                None,
            )
            if anchor is None:
                raise SystemExit(f"no paragraph starts with {item['after_text']!r}")
            # Copy formatting from the question's own body text, not from the
            # anchor, which may be a numbered sub-question (List Paragraph).
            starts = [i for i, el in enumerate(items[: items.index(anchor) + 1])
                      if el.tag == qn("w:p") and para_text(el).startswith("Question")]
            if starts:
                block, _ = find_question_block(items, para_text(items[starts[-1]]))
                template = template_for(block)
            else:
                template = anchor
        insert_lines(anchor, template, item["lines"], colour)
        inserted += len(item["lines"])

    for fill in spec.get("table_fills", []):
        fill_table_cell(doc, fill["table"], fill["row"], fill["col"], fill["text"], colour)
        inserted += 1

    doc.save(out_path)

    missing = check_original_kept(pristine, out_path)
    coloured = sum(
        1
        for p in Document(out_path).paragraphs
        for r in p.runs
        if r.font.color and r.font.color.rgb is not None and str(r.font.color.rgb) == colour.upper()
    )
    print(f"saved {out_path}")
    print(f"inserted items: {inserted}; coloured runs in output: {coloured}")
    if missing:
        print("WARNING: original text missing or reordered:")
        for m in missing[:10]:
            print("   ", m[:80])
    else:
        print("check: every original paragraph is still present, in order")


if __name__ == "__main__":
    main()

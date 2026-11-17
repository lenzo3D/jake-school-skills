#!/usr/bin/env python3
"""Extract readable text from tutorial source files (PDF, PPTX, DOCX, TXT, MD).

Usage: python3 extract_sources.py <source_dir> <out_dir>

Writes one .txt per source file into out_dir. Page and slide markers are kept
so answers can cite them (e.g. "MAS 656 para 7", "Lecture 1, slide 23").
Needs pypdf for PDFs (pip install --user pypdf). PPTX and DOCX use only the
standard library.
"""
import html
import pathlib
import re
import sys
import zipfile


def pdf_text(path):
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n".join(
        f"\n##### PAGE {i + 1}\n" + (page.extract_text() or "")
        for i, page in enumerate(reader.pages)
    )


def pptx_text(path):
    chunks = []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
        names.sort(key=lambda n: int(re.findall(r"\d+", n.split("/")[-1])[0]))
        for name in names:
            xml = z.read(name).decode("utf8")
            xml = re.sub(r"</a:p>", "\n", xml)
            text = html.unescape(re.sub(r"<[^>]+>", "", xml)).strip()
            chunks.append(f"\n##### SLIDE {re.findall(r'\d+', name.split('/')[-1])[0]}\n{text}")
    return "\n".join(chunks)


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf8")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def main():
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.iterdir()):
        if path.name.startswith(("~$", ".")) or path.is_dir():
            continue
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            text = pdf_text(path)
        elif suffix == ".pptx":
            text = pptx_text(path)
        elif suffix == ".docx":
            text = docx_text(path)
        elif suffix in (".txt", ".md"):
            text = path.read_text(encoding="utf8", errors="replace")
        else:
            print(f"skipped (unsupported): {path.name}")
            continue
        target = out / (path.stem + ".txt")
        target.write_text(text, encoding="utf8")
        print(f"{path.name} -> {target.name} ({len(text)} chars)")


if __name__ == "__main__":
    main()

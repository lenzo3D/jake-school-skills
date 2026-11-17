#!/usr/bin/env python3
"""Turn a caption file (.vtt or .srt) into the same timestamped Markdown as transcribe.py.

Usage: python3 vtt_to_md.py captions.vtt "<topic folder>/sources/text/Lecture 5 video transcript.md" --title "Lecture 5 video"

Use this when the video player already offers captions or a transcript download. It is the fastest
and cleanest route: no audio download and no speech recognition.
"""
import argparse
import datetime
import html
import os
import re

TIME = re.compile(r"(?:(\d+):)?(\d+):(\d+)[.,](\d+)\s*-->\s*(?:(\d+):)?(\d+):(\d+)[.,](\d+)")


def secs(h, m, s, ms):
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")[:3]) / 1000


def ts(sec):
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def parse(text):
    cues, cur_t, buf = [], None, []
    for line in text.splitlines() + [""]:
        m = TIME.search(line)
        if m:
            if cur_t is not None and buf:
                cues.append((cur_t[0], cur_t[1], " ".join(buf)))
            cur_t = (secs(*m.group(1, 2, 3, 4)), secs(*m.group(5, 6, 7, 8)))
            buf = []
        elif not line.strip():
            if cur_t is not None and buf:
                cues.append((cur_t[0], cur_t[1], " ".join(buf)))
            cur_t, buf = None, []
        elif cur_t is not None:
            clean = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
            if clean:
                buf.append(clean)
    return cues


def dedupe(cues):
    """Auto captions often repeat the previous line as it rolls; drop exact and prefix repeats."""
    out = []
    for s, e, t in cues:
        if out and (t == out[-1][2] or out[-1][2].endswith(t)):
            continue
        if out and t.startswith(out[-1][2]):
            out[-1] = (out[-1][0], e, t)
            continue
        out.append((s, e, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("captions")
    ap.add_argument("out")
    ap.add_argument("--title", default="Lecture video transcript")
    ap.add_argument("--para-seconds", type=int, default=45)
    a = ap.parse_args()
    cues = dedupe(parse(open(a.captions, encoding="utf-8", errors="replace").read()))
    paras, cur, start = [], [], None
    for s, e, t in cues:
        if start is None:
            start = s
        cur.append(t)
        if e - start >= a.para_seconds and t[-1:] in ".?!":
            paras.append((start, " ".join(cur)))
            cur, start = [], None
    if cur:
        paras.append((start, " ".join(cur)))
    dur = cues[-1][1] if cues else 0
    lines = [
        f"# {a.title}", "",
        f"Source: captions file {os.path.basename(a.captions)} from the video player",
        f"Converted on {datetime.date.today().isoformat()}. Length: {ts(dur)}", "",
        "These are the platform's captions, usually automatic. Names, acronyms, numbers and formulas can be wrong. "
        "Check any figure against the lecture slides before using it in an answer. Cite as [mm:ss] or [hh:mm:ss].",
        "", "---", "",
    ]
    for s, t in paras:
        lines += [f"[{ts(s)}] {t}", ""]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"Wrote {a.out}: {len(paras)} paragraphs, {ts(dur)}")


if __name__ == "__main__":
    main()

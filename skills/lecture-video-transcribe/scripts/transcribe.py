#!/usr/bin/env python3
"""Transcribe a lecture recording (audio or video file) into a timestamped Markdown source.

Usage:
  python3 transcribe.py recording.mp4 "<topic folder>/sources/text/Lecture 5 video transcript.md" \
      --title "Lecture 5 video" --model small --lang en [--para-seconds 45] [--prompt "terms, names, acronyms"]

Runs fully on this computer with faster-whisper (pip install --user faster-whisper).
No system ffmpeg is needed: faster-whisper decodes audio through PyAV.
Output has [HH:MM:SS] markers every paragraph so the right part of the lecture is easy to find. The file says plainly that it is a machine transcript.
"""
import argparse
import datetime
import sys


def ts(sec):
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def load_audio(path):
    """Decode any audio or video file to 16 kHz mono float32 with PyAV.
    faster-whisper's own decoder breaks with some PyAV versions, so we do it here."""
    import av
    import numpy as np
    out = []
    with av.open(path) as c:
        stream = c.streams.audio[0]
        rs = av.AudioResampler(format="s16", layout="mono", rate=16000)
        for frame in c.decode(stream):
            for f in rs.resample(frame):
                out.append(f.to_ndarray().reshape(-1))
        for f in rs.resample(None):
            out.append(f.to_ndarray().reshape(-1))
    return np.concatenate(out).astype("float32") / 32768.0


def group(segments, para_seconds):
    """Group (start, end, text) segments into paragraphs of roughly para_seconds."""
    paras, cur, start = [], [], None
    for s, e, t in segments:
        t = t.strip()
        if not t:
            continue
        if start is None:
            start = s
        cur.append(t)
        if e - start >= para_seconds and t[-1:] in ".?!":
            paras.append((start, " ".join(cur)))
            cur, start = [], None
    if cur:
        paras.append((start, " ".join(cur)))
    return paras


def render(title, source_name, model, lang, duration, paras, speed_note):
    out = [f"# {title}", ""]
    out += [
        f"Source file: {source_name}",
        f"Transcribed on {datetime.date.today().isoformat()} with faster-whisper ({model}, language {lang}). {speed_note}".strip(),
        f"Length: {ts(duration)}",
        "",
        "This is a machine transcript, not a word-for-word record. Names, acronyms, numbers and formulas can be wrong. "
        "Check any figure against the lecture slides before using it in an answer.",
        "",
        "---",
        "",
    ]
    for start, text in paras:
        out.append(f"[{ts(start)}] {text}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("out")
    ap.add_argument("--title", default="Lecture video transcript")
    ap.add_argument("--model", default="small", help="tiny, base, small, medium or large-v3 (bigger = slower, more accurate)")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--para-seconds", type=int, default=45)
    ap.add_argument("--prompt", default=None, help="course terms, names and acronyms to help recognition")
    ap.add_argument("--speed-note", default="", help="e.g. 'Recording was sped up 2x before transcription.'")
    a = ap.parse_args()

    try:  # Python from python.org on a Mac often lacks certificates; truststore uses the system ones.
        import truststore
        truststore.inject_into_ssl()
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. Run: python3 -m pip install --user faster-whisper")

    model = WhisperModel(a.model, device="auto", compute_type="int8")
    audio = load_audio(a.media)
    segs, info = model.transcribe(
        audio, language=a.lang, vad_filter=True, initial_prompt=a.prompt, beam_size=5,
        condition_on_previous_text=False,
    )
    rows = []
    last = 0
    for s in segs:
        rows.append((s.start, s.end, s.text))
        last = s.end
        print(f"\r{ts(last)} / {ts(info.duration)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    paras = group(rows, a.para_seconds)
    import os
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(render(a.title, os.path.basename(a.media), a.model, a.lang, info.duration, paras, a.speed_note))
    print(f"Wrote {a.out}: {len(paras)} paragraphs, {ts(info.duration)} of audio")


if __name__ == "__main__":
    main()

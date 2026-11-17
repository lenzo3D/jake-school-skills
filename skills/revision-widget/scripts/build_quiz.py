#!/usr/bin/env python3
"""Build a self-marking revision quiz page from a bank file.

Usage:
  python3 build_quiz.py bank.json out.html --title "Weak-spot quiz 1" \
      [--key unique-storage-key] [--file "revision/out.html"] \
      [--note "This is practice made from my logged weak spots."] \
      [--handoff "study-log/STUDY_LOG.md in my school folder"]

The bank is a JSON list of modules (see SKILL.md). A flat list of questions
(old format, items with "s") is accepted and becomes one module.
The page saves answers in the browser, marks itself, shows a per-module score,
and builds a prompt that logs the result into the study log.
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "quiz_template.html")

DEFAULT_HANDOFF = (
    "study-log/STUDY_LOG.md in my school folder "
    "(create it if it does not exist yet)"
)
DEFAULT_NOTE = "This is practice, not an official assessment."


def js_str(s):
    """A safe single-quoted JS string body (no surrounding quotes)."""
    return (
        s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
        .replace("<", "\\x3c")
    )


def json_for_script(obj):
    t = json.dumps(obj, ensure_ascii=False)
    return t.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def normalise(bank):
    """Accept modules, or a flat list of old-style questions."""
    if not isinstance(bank, list) or not bank:
        sys.exit("The bank must be a non-empty JSON list.")
    if "qs" in bank[0]:
        return bank
    qs = []
    for i, q in enumerate(bank, 1):
        q = dict(q)
        q.setdefault("id", "Q%d" % i)
        q["sec"] = q.pop("s", q.get("sec", "Questions"))
        qs.append(q)
    return [{"mod": "Quiz", "title": "", "focus": "", "log": "", "sheet": "", "qs": qs}]


def validate(mods):
    seen = set()
    n = 0
    for m in mods:
        for k in ("mod", "qs"):
            if k not in m:
                sys.exit("Module is missing '%s'." % k)
        m.setdefault("title", m["mod"])
        m.setdefault("focus", "")
        m.setdefault("log", "")
        m.setdefault("sheet", "")
        if not m["log"]:
            print("warning: module '%s' has no 'log' heading, so the log prompt cannot "
                  "say where to record it." % m["mod"], file=sys.stderr)
        for q in m["qs"]:
            n += 1
            for k in ("id", "sec", "q", "t", "a", "exp"):
                if k not in q:
                    sys.exit("Question %s is missing '%s'." % (q.get("id", n), k))
            if q["id"] in seen:
                sys.exit("Duplicate question id: %s" % q["id"])
            seen.add(q["id"])
            if q["t"] == "m":
                if not isinstance(q.get("o"), list) or len(q["o"]) < 2:
                    sys.exit("%s: multiple choice needs an options list 'o'." % q["id"])
                if not isinstance(q["a"], int) or not 0 <= q["a"] < len(q["o"]):
                    sys.exit("%s: 'a' must be the 0-based index of the correct option." % q["id"])
                if len(set(q["o"])) != len(q["o"]):
                    sys.exit("%s: duplicate options." % q["id"])
            elif q["t"] == "n":
                if not isinstance(q["a"], (int, float)):
                    sys.exit("%s: numeric 'a' required." % q["id"])
                q.setdefault("tol", 0.01)
            else:
                sys.exit("%s: 't' must be 'n' or 'm'." % q["id"])
            q.setdefault("hint", "")
            if re.search(r"\b(scenario [A-Z]|same (loan|fund|company|firm|stock|investor) as)\b", q["q"], re.I):
                print("warning: %s may rely on another question. Restate its numbers so it "
                      "stands alone." % q["id"], file=sys.stderr)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bank")
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--key", help="localStorage key; default is derived from the title")
    ap.add_argument("--file", help="path shown in the log prompt")
    ap.add_argument("--note", default=DEFAULT_NOTE)
    ap.add_argument("--handoff", default=DEFAULT_HANDOFF)
    a = ap.parse_args()

    if "'" in a.title or "\\" in a.title:
        sys.exit("Keep the title free of apostrophes and backslashes.")

    with open(a.bank, encoding="utf-8") as f:
        mods = normalise(json.load(f))
    n = validate(mods)

    key = a.key or "quiz-" + hashlib.sha1(a.title.encode("utf-8")).hexdigest()[:10]
    fpath = a.file or os.path.basename(a.out)

    with open(TEMPLATE, encoding="utf-8") as f:
        t = f.read()
    html_title = a.title.replace("&", "&amp;").replace("<", "&lt;")
    t = t.replace("__BANK__", json_for_script(mods))
    t = t.replace("__NOTE__", json_for_script(a.note))
    t = t.replace("__KEY__", js_str(key))
    t = t.replace("__FILE__", js_str(fpath))
    t = t.replace("__HANDOFF__", js_str(a.handoff))
    t = t.replace("__TITLE__", html_title)

    with open(a.out, "w", encoding="utf-8") as f:
        f.write(t)
    print("Wrote %s: %d questions in %d module(s)" % (a.out, n, len(mods)))
    for m in mods:
        secs = []
        for q in m["qs"]:
            if q["sec"] not in secs:
                secs.append(q["sec"])
        print("  %s: %d questions; sections: %s" % (m["mod"], len(m["qs"]), "; ".join(secs)))


if __name__ == "__main__":
    main()

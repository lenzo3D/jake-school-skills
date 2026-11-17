#!/usr/bin/env python3
"""Build a mock Kahoot game page from a question bank.

Usage: python3 build_kahoot.py bank.json out.html --title "Topic 5 mock Kahoot" [--key storage-key]

Bank: a JSON list of questions, each {"q": str, "o": [4 short options], "a": 0-3, "exp": str, "t": optional seconds}
"""
import argparse, json, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("bank"); ap.add_argument("out")
ap.add_argument("--title", default="Mock Kahoot")
ap.add_argument("--key", default=None)
a = ap.parse_args()

bank = json.load(open(a.bank, encoding="utf8"))
errs, warns = [], []
for i, q in enumerate(bank, 1):
    if len(q.get("o", [])) != 4: errs.append(f"Q{i}: needs exactly 4 options")
    if q.get("a") not in (0, 1, 2, 3): errs.append(f"Q{i}: a must be 0 to 3")
    if len(q.get("q", "")) > 140: warns.append(f"Q{i}: question over 140 chars, too long for a Kahoot")
    for o in q.get("o", []):
        if len(o) > 60: warns.append(f"Q{i}: option over 60 chars: {o[:30]}...")
    if len(set(q.get("o", []))) != len(q.get("o", [])): errs.append(f"Q{i}: duplicate options")
    if re.search(r"scenario [ab]|the above|same (loan|company)", q.get("q", ""), re.I): warns.append(f"Q{i}: not standalone")
if len(bank) != 10: warns.append(f"{len(bank)} questions (a lecture Kahoot is usually 10)")
counts = [sum(1 for q in bank if q.get("a") == k) for k in range(4)]
if max(counts) > len(bank) * 0.5: warns.append(f"Correct answers lean on one colour: {counts}")
if errs:
    print("\n".join(errs)); sys.exit(1)
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, "template.html"), encoding="utf8").read()
key = a.key or "kahoot_" + re.sub(r"\W+", "_", a.title.lower())
t = t.replace("__TITLE__", a.title.replace("<", "").replace("&", "and")).replace("__KEY__", key)
t = t.replace("__DATA__", json.dumps(bank, ensure_ascii=False).replace("</", "<\\/"))
open(a.out, "w", encoding="utf8").write(t)
print(f"Wrote {a.out}: {len(bank)} questions, correct-answer spread {counts}")
for w in warns: print("warning:", w)

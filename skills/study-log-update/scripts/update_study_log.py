import argparse
import os
import re
import sys


def main():
    p = argparse.ArgumentParser(description="Insert or replace one study-log section in STUDY_LOG.md (created if missing).")
    p.add_argument("handoff", help="path to STUDY_LOG.md (created if it does not exist)")
    p.add_argument("--heading", required=True, help="full heading line, for example '## Investments Topic 1'")
    p.add_argument("--body", required=True, help="markdown file with the section body, without the heading line")
    p.add_argument("--before", default=None, help="optional heading prefix to insert before when the section is new (default: top of the log, below the title)")
    p.add_argument("--updated", help="full new text for the 'Last updated:' line, without the prefix; copy the rest of the existing line")
    args = p.parse_args()

    if not os.path.exists(args.handoff):
        os.makedirs(os.path.dirname(os.path.abspath(args.handoff)), exist_ok=True)
        with open(args.handoff, "w", encoding="utf-8") as fh:
            fh.write("# Study log\n\nLast updated: \n\n")
    with open(args.handoff, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    with open(args.body, encoding="utf-8") as fh:
        body = fh.read().rstrip("\n").split("\n")

    block = [args.heading, ""] + body + [""]
    if args.heading in lines:
        start = lines.index(args.heading)
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        lines[start:end] = block
        action = "replaced"
    else:
        anchor = None
        if args.before:
            anchor = next((i for i, l in enumerate(lines) if l.startswith(args.before)), None)
            if anchor is None:
                sys.exit(f"Could not find a heading starting with '{args.before}' to insert before.")
        else:
            anchor = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
        lines[anchor:anchor] = block
        action = "inserted"

    if args.updated:
        hits = [i for i, l in enumerate(lines) if l.startswith("Last updated:")]
        if hits:
            lines[hits[0]] = "Last updated: " + args.updated
        else:
            lines[1:1] = ["", "Last updated: " + args.updated]

    tmp = args.handoff + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    os.replace(tmp, args.handoff)
    print(f"Study log section {action} in {args.handoff}")


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
# Copy the skills into ~/.claude/skills. Use --force to overwrite skills you already have.
set -e
force=0; [ "$1" = "--force" ] && force=1
dest="$HOME/.claude/skills"
mkdir -p "$dest"
here="$(cd "$(dirname "$0")" && pwd)"
for d in "$here"/skills/*/; do
  name="$(basename "$d")"
  if [ -e "$dest/$name" ] && [ $force -eq 0 ]; then
    echo "skip   $name (already installed, use --force to overwrite)"
  else
    rm -rf "$dest/$name"; cp -R "$d" "$dest/$name"; echo "added  $name"
  fi
done
echo "Done. Restart Claude Code."

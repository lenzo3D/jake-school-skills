#!/usr/bin/env python3
"""Report what is installed for lecture transcription. Changes nothing."""
import importlib.util
import shutil
import sys

print(f"python: {sys.version.split()[0]}")
fw = importlib.util.find_spec("faster_whisper") is not None
print(f"faster-whisper (speech to text): {'installed' if fw else 'MISSING  -> python3 -m pip install --user faster-whisper'}")
print(f"ffmpeg (needed only to merge or cut downloaded streams): {'installed' if shutil.which('ffmpeg') else 'missing  -> brew install ffmpeg (Mac) or winget install ffmpeg (Windows)'}")
print("The first transcription downloads a speech model once: tiny about 75 MB, small about 470 MB, medium about 1.5 GB.")

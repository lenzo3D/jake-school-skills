#!/usr/bin/env python3
"""Download an HLS (.m3u8) lecture stream into one .ts file, with no ffmpeg needed.

Usage: python3 download_hls.py url.txt lecture.ts
  url.txt holds the full signed index.m3u8 URL on one line (keep it out of the repo and delete it afterwards).
The .ts file can be passed straight to transcribe.py. Delete it when you are done.
"""
import sys
import urllib.parse
import urllib.request

try:
    import truststore  # system certificates; python.org Python on a Mac often has none
    truststore.inject_into_ssl()
except ImportError:
    pass

H = {"User-Agent": "Mozilla/5.0"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H)).read()


def main():
    url = open(sys.argv[1]).read().strip()
    lines = get(url).decode().splitlines()
    segs = [urllib.parse.urljoin(url, l) for l in lines if l and not l.startswith("#")]
    if segs and segs[0].split("?")[0].endswith(".m3u8"):
        sys.exit("This is a master playlist. Pass one of the variant index.m3u8 URLs instead.")
    print(len(segs), "segments", flush=True)
    with open(sys.argv[2], "wb") as f:
        for i, u in enumerate(segs, 1):
            f.write(get(u))
            if i % 20 == 0:
                print(f"{i}/{len(segs)}", flush=True)
    print("done")


if __name__ == "__main__":
    main()

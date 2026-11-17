---
name: lecture-video-transcribe
description: Turn a recorded lecture video (Kaltura, Panopto, Echo360, Teams or Stream, Zoom recordings, or any file) into a timestamped Markdown transcript saved next to the slides, so Claude can search and cite it like a source. Use whenever the user gives a lecture video link or file, asks to transcribe, summarise or take notes from a lecture recording, wants a lecture video "turned into a source", or says to watch the lecture for them. Works with the school learning portal in the browser, but the user signs in themselves. Not for live meetings.
---

# Lecture video to usable source

Goal: one Markdown file per lecture in `<topic folder>/sources/text/`, with `[hh:mm:ss]` markers, that the other school skills (tutorial answering, quizzes, Kahoot mock) can read and cite exactly like slides.

## The honest part, tell the user up front

- Claude cannot hear audio and cannot type passwords, MFA codes or any credential. The user signs in to the portal in the browser pane themselves.
- Playing the video at 2x in a browser does not give Claude a transcript. It only plays sound out of the speakers. The reliable routes are, in order: (A) the player's own captions, (B) the video's audio file transcribed on this computer. Both are faster than playing the video, and more accurate than listening at 2x. Playing at 2x is only a last resort (see C).
- Machine transcripts mishear names, acronyms and numbers. Every figure that matters gets checked against the slides before it goes into an answer.

## Steps

1. **Check the tools.** `python3 scripts/check_setup.py` (path relative to this skill's folder). It reports Python, `faster-whisper` and `ffmpeg`. Installing is a change to the user's computer, so ask before running `python3 -m pip install --user faster-whisper` or installing ffmpeg. The first run also downloads a speech model once (tiny about 75 MB, small about 470 MB). Say the size and ask.

2. **Open the video.** Use the built-in browser (or Claude in Chrome if the user asks). Navigate to the link the user gave. If the page says Access Denied, a login page, or loads blank, the portal needs a sign-in: ask the user to sign in in that browser, or to import their own cookies for the school's domain only if the browser offers it. Do not ask for the password. Once signed in, reopen the link, or reach the video through the course content if the embed link only works from inside the portal. Never write cookies, tokens or signed URLs into any file or into chat.

3. **Find out what the player offers.** Take a screenshot and read the page. Note the platform (Kaltura, Panopto, Echo360, Stream, Zoom) and the video length.

4. **Route A: captions or transcript (try first).**
   - Look for a CC button, a "Transcript" or "Captions" panel, or a download option. Turn captions on and read them with `get_page_text` or `read_page` if they are shown as text in the page.
   - If a `.vtt` or `.srt` file can be downloaded, ask the user's permission to download it (file name, source, size), then run:
     `python3 scripts/vtt_to_md.py captions.vtt "<topic folder>/sources/text/<Lecture name> video transcript.md" --title "<Lecture name> video"`
   - If the captions are only shown on screen and cannot be downloaded, scroll the panel and copy the text out in chunks, then build the Markdown yourself in the same format (a `[mm:ss]` marker per paragraph).

5. **Route B: the audio, transcribed locally.** Use when there are no captions.
   - Open the browser's network log (`read_network_requests`) while the video plays and look for the media file: an `.mp4`, `.m3u8` or `.mpd` request, or the audio-only flavour. Many platforms hide downloads on purpose. If the platform or school blocks downloading, stop and tell the user. Do not work around access controls. Ask the lecturer or use the platform's own download button if it has one.
   - Ask permission before downloading, naming the file, source and rough size. Save it in the user's own folder, not in the repo, and delete it after transcribing unless the user wants to keep it.
   - **Kaltura (the usual school player):** the player runs in an iframe on the video server. In that page, `performance.getEntriesByType('resource')` (inside the iframe's window) lists the stream requests. Find the `index.m3u8` URL for one flavour (they are signed, time-limited links, so use it straight away). Save it to a temporary file in your scratch folder, never in the repo or in chat. If the embed link shows "Access Denied" when opened on its own, open the lecture from inside the portal first. Navigating to the portal's LTI tool-launch link for that item (visible in the network log) shows the player with the user's session.
   - Download without ffmpeg: `python3 scripts/download_hls.py url.txt lecture.ts` (it fetches every segment and joins them). With ffmpeg you can instead run `ffmpeg -i "<m3u8 url>" -vn -ac 1 -ar 16000 audio.wav`. The video track comes along in the download, so expect tens of MB for a 30 minute lecture.
   - Transcribe:
     `python3 scripts/transcribe.py lecture.ts "<topic folder>/sources/text/<Lecture name> video transcript.md" --title "<Lecture name> video" --model small --prompt "<course terms, lecturer name, acronyms from the slides>"`
     The prompt noticeably improves acronyms and jargon. Use the slides' key terms. Use `--model medium` for noisy recordings if the computer can take it.
   - Speed: this runs locally and is usually several times faster than real time, but depends on the computer. A 3 hour lecture can take a while, so run it in the background and report when it is done.

6. **Route C (last resort): play it at 2x.**
   - Only if A and B are both impossible. Set the player to 2x, and capture the computer's audio with a loopback tool (for example BlackHole on a Mac) into a file, then transcribe that file with `transcribe.py --speed-note "Recording was played at 2x."`. Warn that accuracy drops at 2x and that the recording takes half the lecture's length in real time. Claude cannot do this by itself without the loopback tool and the user's go-ahead.

7. **Make it a usable source.** Read the finished transcript, then:
   - Add a short summary block at the top: the lecture title, the main topics in order with their first `[hh:mm:ss]`, and any announcements (deadlines, test content, "this will be in the exam").
   - Add a "Check against the slides" list: figures, formulas and names that look doubtful, with their timestamps. Fix obvious term mishearings (for example a company name or an acronym) only when the slides confirm the correct form, and keep the original wording where you are not sure.
   - If the lecture slides are imported (`sources/text/`), note which slide each topic matches.
   - Keep the transcript itself unchanged below the summary.

8. **Report** in a few lines: the file as a clickable link, the length, the route used (captions or local audio), the topics found with timestamps, and what needs checking. Do not paste the transcript into chat.

## Rules

- The user signs in, never Claude. Never store credentials, cookies, tokens or signed links.
- Lecture recordings belong to the school. Keep transcripts for personal study. Do not publish them or put them in a public repo, and do not share the video file.
- Respect the platform: if downloads are disabled, use captions or ask the lecturer. Do not bypass access controls.
- Say plainly that the transcript is machine-made and unchecked. Never cite a transcript figure as fact without a slide or the user's confirmation. Mark such figures as "from the lecture recording, unconfirmed".
- Cite timestamps the way slides are cited, for example "(Lecture 5 video, 23:40)".

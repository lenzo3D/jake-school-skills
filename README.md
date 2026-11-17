# School skills

A set of 11 skills that help a university student turn lecture slides, briefs and lecture recordings into completed coursework (tutorials, homework and assignments) and revision. Each skill is a folder in `skills/` containing a `SKILL.md` (the instructions the AI follows) and, where needed, small Python scripts and templates.

They were built and tested with Claude Code. Nothing in here depends on any other app, account or private folder. Everything runs on your own computer.

## What you need first (applies to every skill)

- An AI coding assistant that can read files, run shell commands and edit files. Tested with Claude Code. See "Install into your AI" below for others.
- Python 3 (`python3 --version`). Tested on Python 3.14.
- A single folder on your computer where you keep school work, for example `~/Documents/School/`. Open your AI in that folder.

Install the shared Python packages once:

```bash
python3 -m pip install --user python-docx pypdf
```

## Suggested folder layout

You don't have to create it by hand. The skills create what they need.

```
School/
  Commercial Banking Topic 5/
    sources/          slides, briefs, tasks and readings you drop in
      text/           extracted text and lecture transcripts (made for you)
    work/             your completed tutorials, homework or assignments, and explanation files
    revision/         quizzes and Kahoot mocks
  study-log/
    STUDY_LOG.md      your scores and weak spots (created automatically)
```

## The skills, most important first

### 1. school (start here)
**Purpose:** The entry point and router for every other skill. It works out what you need and runs the right skill, so you never have to remember skill names.
**Use it when:** Any time you start school work, or you are not sure which skill to use. Type `/school` or just describe what you need.
**What it does:** Every time it runs, it shows a clickable multiple-choice widget in the chat asking what you want to do (tutorials, homework and assignments, revision and practice, lectures and marking, study log), then a second widget with the specific skill and a one-line description of each. It puts its best guess first, then runs your choice. It never answers with a plain-text list.
**Before you run it:** Install the other skills too, since it only points to them. The clickable widget is a Claude Code feature (the AskUserQuestion tool). On assistants without it, it falls back to a numbered list you reply to.

### 2. import-sources
**Purpose:** Turn course files (PDF, PowerPoint, Word, text) into plain text the AI can search and cite. Most other skills depend on this one.
**Use it when:** You start a topic, or drop in new slides, notices or readings.
**What it does:** Extracts each file into `sources/text/`. PDFs keep `##### PAGE n` markers and slides keep `##### SLIDE n` markers, so answers can cite a page or slide.
**Before you run it:** Put the files in `<topic folder>/sources/`. Needs `pypdf` for PDFs. PowerPoint and Word need nothing extra. A scanned PDF (images only) gives no text, so ask for a text version.

### 3. complete-docx-work
**Purpose:** Complete any Word-based coursework inside your original file without changing its fonts, layout or formatting. It is not only for tutorials or homework: it can complete your assignments as well.
**Use it when:** You have a `.docx` tutorial, homework, case study or assignment and want answers written into it, cited to your slides. For an assignment, include its brief and marking rubric in `sources/` so the work is written to the criteria.
**What it does:** First asks, with a clickable widget, whether this is a tutorial or homework, or an assignment. Tutorials and homework get short answers in light blue. Assignments get plain default text that matches your document, written to the brief and rubric. Then it keeps a pristine copy, maps the document, writes the answers under each question, copies the body font, and checks every original paragraph is still there in order.
**Before you run it:** Run skill 1 first so answers can cite your sources. Needs `python-docx`. Close the file in Word first, or the save is blocked. The original is never edited; it works on a copy in `work/`.

### 4. explain-my-work
**Purpose:** Write a separate Word file that explains your answers in more depth, to talk through with a teacher.
**Use it when:** The work is completed and you want to prepare to talk through it with a teacher.
**What it does:** For each question: a short answer, step-by-step reasoning with traps, likely follow-up questions with answers, and sources. It ends with a glossary and says clearly what came from the sources and what is the AI's own reasoning.
**Before you run it:** Run skills 1 and 2 first. Needs `python-docx`.

### 5. revision-widget
**Purpose:** Build a self-marking revision quiz as one HTML file.
**Use it when:** You want a quiz, a retest, a formula drill or a consolidated quiz across topics.
**What it does:** Marks each answer and shows the working, saves your progress in the browser, scores each module, and builds a prompt you paste back into the AI to log the result.
**Before you run it:** Run skill 1 first. Open the finished file in Chrome or Edge (Safari can block saving for local files). The AI computes numeric answers with Python and never from memory. To log results, use skill 7.

### 6. lecture-video-transcribe
**Purpose:** Turn a recorded lecture into a timestamped Markdown transcript that the AI can cite like slides.
**Use it when:** The lecturer posts a recording and you want it as a source, or you want notes and a topic summary from it.
**What it does:** Tries the player's captions first. If there are none, it downloads the audio and transcribes it on your computer with `faster-whisper`. It saves the transcript with a topic summary mapped to your slides and a list of likely recognition errors.
**Before you run it:**
- Install the speech tool: `python3 -m pip install --user faster-whisper`. The first run downloads a speech model once (about 470 MB for `small`).
- ffmpeg is optional. The skill can download streams without it.
- You sign in to your school portal yourself. The AI must never type your password or MFA code and never stores cookies or signed links.
- The AI needs a way to browse the portal (for example Claude's built-in browser or Claude in Chrome). Without one, download the audio or captions yourself and run `scripts/transcribe.py` or `scripts/vtt_to_md.py`.
- Recordings belong to your school. Keep transcripts for personal study. Do not publish them or the video. Do not bypass a platform that blocks downloads.
- Transcripts are machine-made. Check names, acronyms and figures against the slides before using them.

### 7. mark-my-work
**Purpose:** Get a realistic mark and a fix list for a finished assignment before you submit.
**Use it when:** You have a finished assignment and its brief with the marking rubric.
**What it does:** An independent reviewer reads your document against the rubric, gives a mark per criterion, a total, an indicative grade, location-specific fixes ranked by marks at stake, and what it would take to reach full marks. It never rewrites your assignment.
**Before you run it:** You need the brief with the rubric. Tell it your school's grading scale, or it uses a generic A to F scale and says so. It is written for assistants that can start a separate sub-agent (Claude Code can). On others it runs as a single pass, which is less independent.

### 8. study-log-update
**Purpose:** Record your scores, weak spots and checked facts in one file so later sessions know where you stand.
**Use it when:** After a quiz, practice set or piece of coursework, or when you say "update my study log".
**What it does:** Adds or replaces one section per topic in `study-log/STUDY_LOG.md`. The script creates the file and folder if they don't exist.
**Before you run it:** Nothing to set up. Paste the prompt a revision quiz gives you, or tell it what happened. It never stores passwords or tokens.

### 9. log-and-recharge
**Purpose:** After a retest, log the result and then build extra practice that is not logged.
**Use it when:** You report a retest and want to keep drilling a hard area, or want the missed concept taught first.
**What it does:** Teaches the concept (formulas, method, a worked example), logs the result with skill 7, then builds a new practice quiz with new numbers that is never recorded.
**Before you run it:** Needs skills 4 and 7 installed.

### 10. study-log-summary
**Purpose:** Show your whole study log as one table.
**Use it when:** You ask "where do I stand" or "what are my weak spots overall".
**What it does:** Reads `study-log/STUDY_LOG.md` and reports scores, retests, top weak spots and patterns across topics. Read-only.
**Before you run it:** A study log must exist (skill 7 creates it).

### 11. kahoot-mock
**Purpose:** Practise for in-class Kahoot games with a mock that has the same pressure.
**Use it when:** Your lecture ends with a timed Kahoot and you want to train speed as well as knowledge.
**What it does:** Builds one HTML game of 10 questions: a read phase, four coloured answers, a countdown, speed-based points up to 1000, a streak bonus, a scoreboard after every question, 22 simulated rivals and a podium that tells you if you would have placed top 3. It saves your best score.
**Before you run it:** Needs only Python 3 to build and a browser to play. The scoring follows Kahoot's public rules as best known, and the rivals are simulated, so treat scores as a guide. Pick the time limit that matches your lecturer's (10 to 60 seconds). It copies the look and flow, not Kahoot's logo or music.

## Install

### Claude Code (tested)

Mac or Linux:

```bash
git clone https://github.com/lenzo3D/jake-school-skills.git
cd jake-school-skills
bash install.sh
```

Windows (PowerShell):

```powershell
git clone https://github.com/lenzo3D/jake-school-skills.git
cd jake-school-skills
powershell -ExecutionPolicy Bypass -File install.ps1
```

This copies each folder in `skills/` into `~/.claude/skills/`. It skips skills you already have unless you add `--force` (Mac or Linux) or `-Force` (Windows). Restart Claude Code, open it in your school folder, and ask for what you need, for example "import the sources" or "make a revision quiz". You can also type `/<skill-name>`.

### Another AI assistant

A skill is plain Markdown instructions plus small Python scripts, so the content works anywhere an AI can read files and run commands. Only Claude Code has been tested. For others:

1. Clone this repo somewhere on your computer.
2. Check your assistant's documentation for where it loads custom skills or instructions from. If it supports the `SKILL.md` format, copy the folders from `skills/` there.
3. If it does not, point it at the repo directly. This repo includes an `AGENTS.md` that lists the skills and tells the assistant to read the right `SKILL.md` before starting. Many assistants pick up `AGENTS.md` automatically. If yours does not, start your session with: "Read AGENTS.md in the school-skills folder, then follow the matching SKILL.md."
4. In the `SKILL.md` files, script paths look like `~/.claude/skills/<skill>/scripts/...`. If your assistant keeps skills elsewhere, change that part of the path or tell it where the repo is.

Things that depend on assistant features: `mark-my-work` uses a sub-agent, `lecture-video-transcribe` needs a way to browse your portal, and the clickable question prompt in `school` is a Claude Code feature (other assistants fall back to a plain question).

## Typical flow

1. Put the slides and the task (tutorial, homework or assignment brief) in `<Course> Topic N/sources/`.
2. "Import the sources", then "complete the assignment" (or tutorial, or homework), then "write the explanation file".
3. "Make a revision quiz". Paste the log prompt it gives you back to update your study log.
4. Before the lecture: "make a mock Kahoot for this topic".
5. Lecture recording available: "transcribe this lecture video: <link>".

## Notes and limits

- AI answers, transcripts and marks are drafts. Check figures against your slides, and follow your school's rules on AI use and disclosure.
- Never upload private school files or recordings to a public repo.
- No licence has been set, so by default all rights are reserved. Add a `LICENSE` file if you want others to reuse this.

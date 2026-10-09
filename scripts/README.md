# scripts/ — the method's scripts, and how to prepare a machine

Status: v0.3 · 2026-10-09 · one repository per project (board r11) · for the Project Advisor first; §2 also holds for every team member (the project lead or a developer)

These scripts are run **from the project's repository** `<project-repo>` (the private
repository that holds the code and, in `project/`, the project's decisions, requirements,
plans, minutes and journal, with `gse-light` cloned next to it), by the Claude Code sessions
or by hand:

| Script | What it does | Needs |
|---|---|---|
| `check_docs.py` | checks links, registers, cockpit counts, the kit copy in `.claude/` and the leak guard (no client term in `gse-light`) | Python only |
| `situation.py` | where the project stands this week, next meeting, next step (printed by the session-start hook; the Advisor's skills read it) | Python only |
| `session_start.py` | the session-start hook of every session: the git user and their role, the next meeting; for the Project Advisor also his week's next step, his tasks and the last hand-over | Python only |
| `llm_call.py` | one paid model call (Gemini, or a text model through OpenRouter), cost logged in `project/journal/llm-costs.csv` | the environment of §1 (`google-genai`) |
| `meeting/meeting.sh` | records the meeting with ffmpeg (macOS), or imports a file recorded elsewhere | `ffmpeg` |
| `meeting/transcribe.py` | transcribes a recording: locally (mlx-whisper or whisper.cpp), or with Gemini | the environment of §1 (`mlx-whisper`), or `whisper-cpp` |

"Python only" means Python's standard library: nothing to install beyond `python3` (3.10 or
later). The two scripts that need more switch **by themselves** to the project repository's
environment when it exists (`<project-repo>/.venv`, §1); no activation, no special
command: the skills keep calling `python3 ../gse-light/scripts/…`.

## 0. The rule for every environment, on every machine

**A real environment folder never lives inside a synced folder** (Dropbox, OneDrive, iCloud
Drive, Google Drive): thousands of small files flood the sync, and an environment built on
one machine does not work on another. The same holds for `node_modules`. So, on every machine:

- every Python environment is created **outside** the synced tree, in `~/.venvs/<name>`, and
  the project only holds a **link** to it, named `.venv` (git-ignored by every repository of
  the method):

  ```bash
  uv venv ~/.venvs/<name> --python 3.12      # the environment, outside the synced tree
  ln -s ~/.venvs/<name> .venv                # the link, inside the repository
  uv pip install --python .venv/bin/python <packages>
  ```

- on a **new machine**, when `.venv` is a link whose target is missing, recreate the environment
  **at the target of the link** (same commands, same name) — never replace the link by a folder;
- never delete an existing environment without its owner's agreement: it is not always
  rebuildable;
- `node_modules` (JavaScript) is excluded from the sync **before** it is filled; on macOS with
  Dropbox: `mkdir -p node_modules && xattr -w com.dropbox.ignored 1 node_modules`, then the
  install (and again after a tool deletes and recreates the folder);
- command-line tools installed with `uv tool install` live in `~/.local/share/uv/tools`
  (outside the synced tree by construction); the method prefers the repository's own
  environment (§1) so that one link says everything the machine needs.

`uv` is the one tool behind these commands: `brew install uv` on macOS, or see
https://docs.astral.sh/uv/ for Linux and Windows (`.venv\Scripts\python.exe` there).

## 1. The Project Advisor's machine — once per machine

Prerequisites: git, [Claude Code](https://claude.com/claude-code) signed in, `python3`
(3.10 or later), `uv`, `ffmpeg` (to record and to convert audio). macOS commands:

```bash
brew install uv ffmpeg                                   # once per machine
cd <parent folder>/<project-repo>                        # the project's repository, next to gse-light
uv venv ~/.venvs/<project-repo> --python 3.12            # the environment, outside the synced tree
ln -s ~/.venvs/<project-repo> .venv                      # the link, git-ignored
uv pip install --python .venv/bin/python google-genai mlx-whisper
cp .env.example .env                                     # then fill the keys; never committed
python3 ../gse-light/scripts/situation.py                # says what is still missing
python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt test --dry-run   # shows the Python used and whether the key is present
```

What each piece is for:

- `google-genai` — the Gemini engine of `transcribe.py` (speaker labels; the audio is
  uploaded to Google AI Studio with the key `GOOGLE_API_KEY` of `.env`; cost logged) and the
  `gemini` provider of `llm_call.py`;
- `mlx-whisper` — the local transcription engine on Apple Silicon (nothing leaves the
  machine; no speaker labels); its model (about 1.6 GB, `WHISPER_MODEL` in `.env`) downloads
  into `~/.cache/huggingface` on first run. `transcribe.py` looks for it in
  `<project-repo>/.venv/bin/` first, then on the `PATH`;
- on an Intel Mac or Linux, replace `mlx-whisper` by whisper.cpp: `brew install whisper-cpp`
  (or the distribution's package), download a `ggml` model and set `WHISPER_CPP_MODEL` in `.env`;
- the microphone: `../gse-light/scripts/meeting/meeting.sh devices` lists the inputs; put the
  index in `.env` (`MEETING_AUDIO_DEVICE`). Recording is macOS only (ffmpeg's avfoundation);
  on another system, record with any tool and `meeting.sh import <file>`.

**Second machine**: clone the two repositories side by side, run the block above again (same
environment name), copy your `.env` by hand (it is never in git).

## 2. A team member's machine — once per machine

The method itself needs **no environment** on a team member's machine: git, a bash terminal
(Git Bash on Windows), `python3` (the kit's `check.sh` and `check_docs.py` use the standard
library) and Claude Code signed in. `../gse-light/kit/check.sh`, run from the project's
repository, verifies it line by line ([`kit/INSTALL.md`](../kit/INSTALL.md)).

The **product's** own environments (its language, its packages, its `node_modules`) are the
project's design decisions; on a machine with a synced folder they follow §0 — environment in
`~/.venvs/<name>`, link in the repository — and the project lead writes the exact commands in
the project repository's `CLAUDE.md` (section "Commands"). The link `.venv` is one per
repository: the Advisor's environment of §1 and the product's environment share it when the
Advisor works on the same clone as the team — then one environment holds both sets of packages.

## 3. Checking a machine

```bash
python3 ../gse-light/scripts/situation.py                                            # .env present? project/ found?
python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt test --dry-run   # "python": the environment's interpreter if the link exists; "key_present"
python3 ../gse-light/scripts/meeting/transcribe.py --help                            # the engines and where they are looked for
../gse-light/scripts/meeting/meeting.sh devices                                      # the audio inputs
```

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

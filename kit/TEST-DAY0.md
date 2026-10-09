# Rehearse Day 0 on your own machine — by role

Status: v0.7 · 2026-10-09 · one repository per project (board r11) · for the Project Advisor, the project lead and the developers ·
about 15 minutes for the commands (§0–§3), plus the interactive sessions (§4)

**What this page is.** A rehearsal, in a throwaway folder, of what each role does on its
Day 0 — with the real scripts of the `gse-light` repository, cloned from GitHub as a team
member would, and a local stand-in for the project's private repository. It touches none of
your working copies. Find your role below and run its block(s); every block says what to expect.

- **Where**: `~/gse-test`, outside any synced folder (Dropbox, OneDrive, iCloud Drive).
- **Prerequisites**: `git`, `python3` (3.10 or later), a bash terminal (Git Bash on Windows).
  The Project Advisor's block also uses `ffmpeg` (macOS) for the ten-second recording.
- **In a hurry?** [TEST-DAY0-fast.txt](TEST-DAY0-fast.txt) holds §0–§3 as four blocks to paste
  one after the other — kept in step with this page, command by command.
- **Order**: §0, then **§1 first whatever your role** (it creates the project's repository of
  the test and installs the kit in it), then your role's section.

**Who runs what**

| Role | Sections | Plays |
|---|---|---|
| **Project Advisor** | §0, §1, §4 | your own Day 0: the project's repository with the kit and the `project/` skeleton, the checks, the situation, the meeting chain, a session that says "go" |
| **Project lead** | §0, §1, §2, §3, §4 | your Day 0 like every team member (§2) — you are a developer too — then what is yours in W1 (§3) |
| **Developer** | §0, §1, §2, §4 | your Day 0: the clone that already has the kit, `.env`, the check, the gates stub, your branch |

**The repositories in this test** — side by side in one parent folder, as on a real machine:

| Name in the commands | Which repository | Stands for |
|---|---|---|
| `gse-light` | the `gse-light` repository (method and kit), cloned from GitHub `nicolasguelfi/gse-light` | itself |
| `remote-project.git` | a local **bare** repository (no working files), filled by §1 with the kit and the `project/` skeleton | the project's private repository `<project-repo>` on GitHub |
| `advisor/gse-light`, `advisor/project` | the Project Advisor's clones | his working copies |
| `<name>/gse-light`, `<name>/project` | a team member's clones (§2) | their working copies |

## 0. Settings — everyone

Copy these lines in your terminal first; every block below uses them.

```bash
TEST=~/gse-test                # throwaway folder, outside any synced folder
TAG=demo                       # names the two throwaway leak-guard terms of §1 (client-$TAG, project-$TAG), built at run time so that they appear in no file of gse-light
NAME=alex                      # §2 only: your first name, in lower case — names your folder and your Day-0 branch
```

## 1. If you are the Project Advisor — your own Day 0 (everyone runs it first)

What it plays: the machine is already prepared ([`scripts/README.md`](../scripts/README.md) §1 —
not rehearsed here: it writes in `~/.venvs`, nothing throwaway); then the project's repository
with the kit and the `project/` skeleton, the documentation checks, the situation, the
settings, one paid-model call in dry run, and the meeting chain on a ten-second recording.

```bash
mkdir -p "$TEST/advisor" && cd "$TEST"
git init -q --bare remote-project.git                  # remote-project.git, empty: the project's repository as just created on GitHub
cd advisor
git clone -q https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (method and kit)
git clone -q ../remote-project.git project             # clones remote-project.git into advisor/project — expected warning: "You appear to have cloned an empty repository."
cd project
../gse-light/kit/install.sh                            # the one command: skills, agents, settings, CLAUDE.md, gates, CI, .env.example, and project/ from the skeleton
printf 'client-%s\nproject-%s\n' "$TAG" "$TAG" > project/private-terms.txt   # two throwaway terms the leak guard refuses in gse-light (built here so that they appear in no file of gse-light)
python3 ../gse-light/scripts/check_docs.py             # expected: "check_docs (project): ok (0 problem(s), 0 warning(s))"
git add -A && git commit -q -m "Install the gse-light kit" && git push -q origin HEAD   # remote-project.git now holds the kit and project/: §2 clones it
python3 ../gse-light/scripts/situation.py              # expected: "next meeting unknown" and the note "No .env yet"
cp .env.example .env                                   # the Project Advisor's settings and keys, never committed
python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt test --dry-run   # expected: a JSON with "python" (the interpreter used) and "key_present": false
../gse-light/scripts/meeting/meeting.sh devices        # macOS: your audio inputs with their index (the .env has MEETING_AUDIO_DEVICE=0)
../gse-light/scripts/meeting/meeting.sh start 260101 && sleep 10 && ../gse-light/scripts/meeting/meeting.sh stop   # a ten-second recording — expected: audio.m4a and meta.json in project/meetings/260101/
python3 ../gse-light/scripts/meeting/transcribe.py project/meetings/260101   # expected: transcript.md, or the message "no local engine" with the install line (then: scripts/README.md §1)
```

**Expected**: `kit/install.sh` prints `project repository project · method ../gse-light ·
project folder project/`, copies the skeleton (`README.md`, `BRIEFING.md`, the three
registers, the roles record, `journal/`, `meetings/`) into `project/`, lists the twelve
skills (`advisor`, `cockpit-update`, `decision-record`, `design-phase`, `genai-onboarding`,
`meeting`, `method-lesson`, `review`, `session-close`, `slides`, `upskilling`, `verify-claim`)
and the four agents (`change-reviewer`, `delivery-auditor`, `design-reviewer`,
`minutes-verifier`), creates `CLAUDE.md`, `.claude/settings.json`, `.gitattributes`, `gates.sh`,
`.env.example`, `.github/workflows/gates.yml` and `docs.yml`, and writes `KIT_VERSION`;
`check_docs` prints `ok`; `situation.py` says what is missing; the dry run shows the Python it
uses (the linked `.venv` when the project's repository has one — not in this test) and no key;
the recording needs a microphone allowed for your terminal (macOS: System Settings › Privacy &
Security › Microphone); `transcribe.py` needs a local engine or a Gemini key, else it says so.

Then **§4**: open Claude Code in `advisor/project` and say "go".

## 2. If you are the project lead or a developer — your Day 0

What it plays: every team member's real Day 0 — two clones side by side, the kit already in
the project's repository (pushed by the Project Advisor in §1), your `.env`, the check, the
gates stub, your Day-0 branch. Run it with your own `NAME` (the project lead too: you are a
developer). You never run `install.sh`.

```bash
mkdir -p "$TEST/$NAME" && cd "$TEST/$NAME"
[ -d gse-light ] || git clone -q https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository
git clone -q ../remote-project.git project             # the project's repository: the kit comes with it
cd project
cp .env.example .env                                   # your keys, never committed
{ ../gse-light/kit/check.sh; echo "exit $? (0 expected)"; }   # expected: only OK lines
bash ./gates.sh                                        # the Day-0 stub, run as CI runs it — expected: "no gates yet: design phase in progress …", exit 0
git switch -c "day0-$NAME"                             # your Day-0 branch: first session, /upskilling, first journal entry
git status --short                                     # expected: nothing (.env is ignored)
```

**Expected**: `check.sh` shows every line `OK`, among them `project/ (the shared record…)`,
`team skills present`, `Project Advisor's skills present`, `agents present`, `kit committed`,
`settings.json runs the start hook`, `kit version <hash> (current)` — the hash is the last
commit of `gse-light` that touched `kit/`.

Then **§4**: your first session in `$TEST/$NAME/project`.

## 3. If you are the project lead — what is yours in W1

Nothing to install: the kit is in. In W1 you run the design phase in your clone (skill
`design-phase`, interactive — §4) and fill `gates.sh`, the CI and the `<…>` fields of
`CLAUDE.md` from its decisions. This block only shows what you will find.

```bash
cd "$TEST/$NAME/project"
git log --oneline -1 -- .claude                        # expected: the Project Advisor's commit "Install the gse-light kit"
ls project/design project/governance                   # expected: 05-design-decisions.md (the twelve DD await you) · 05-project-decisions.md 10-roles-and-go-aheads.md
grep -c '<command>' CLAUDE.md                          # expected: 4 — the commands you fill after the design phase
```

## 4. First session — every role (interactive)

| Role | Where | What to do in the session |
|---|---|---|
| Project Advisor | `claude` in `$TEST/advisor/project` | the start hook prints the situation (next meeting unknown, no `.env` or the one you copied) and your block (BRIEFING §1, the hand-over); say "go": the `advisor` skill proposes the next step and asks you one short multiple-choice question |
| Project lead, developer | `claude` in `$TEST/$NAME/project` | the start hook prints who you are and the next meeting; type `/` — `decision-record`, `design-phase`, `review`, `session-close`, `verify-claim`, `upskilling` appear (the six others are the Advisor's and stop for you); type `/upskilling` — fifteen minutes of questions and small checks, then a personal plan; ask *"what is in project/?"* — Claude reads it but cannot edit `../gse-light` nor `project/BRIEFING.md` (deny rules of `.claude/settings.json`), and asks before any `git push` |

## 5. Check that nothing personal went into git

```bash
git status --short                                     # in every clone you worked in: .env must not appear
ls ~/.claude/upskilling/project/                       # your private record, in your home folder, outside every repository
```

## 6. Clean up

```bash
rm -rf "$TEST"                                         # removes remote-project.git, advisor/ and <name>/
rm -rf ~/.claude/upskilling/project                    # only if /upskilling wrote a test record
```

## If something differs

- A `check.sh` line is not `OK`: paste its output to the session; [INSTALL.md §5](INSTALL.md#5-what-checksh-says)
  lists what each line means.
- `check_docs` fails in §1: read the `FAIL` lines; the skeleton and the kit must agree
  (refresh with `../gse-light/kit/install.sh`).
- The recording fails in §1: the microphone is not allowed for your terminal, or you are not
  on macOS (`meeting.sh` records with ffmpeg's avfoundation; elsewhere, import a file with
  `meeting.sh import`).
- Not covered by this rehearsal: Windows (use Git Bash for the same commands), the real
  repository on GitHub, the preparation of the machine ([`scripts/README.md`](../scripts/README.md)).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

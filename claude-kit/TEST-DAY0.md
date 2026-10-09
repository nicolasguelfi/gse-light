# Rehearse Day 0 on your own machine — by role

Status: v0.6 · 2026-10-08 · for the Project Advisor, the project lead and the developers ·
about 20 minutes for the commands (§0–§4), plus the interactive sessions (§5)

**What this page is.** A rehearsal, in a throwaway folder, of what each role does on its
Day 0 — with the real scripts of the `gse-light` repository, cloned from GitHub as a team
member would, and local stand-ins for the private repositories. It touches none of your
working copies. Find your role below and run its block(s); every block says what to expect.

- **Where**: `~/gse-test`, outside any synced folder (Dropbox, OneDrive, iCloud Drive).
- **Prerequisites**: `git`, `python3` (3.10 or later), a bash terminal (Git Bash on Windows).
  The Project Advisor's block also uses `ffmpeg` (macOS) for the ten-second recording.
- **In a hurry?** [TEST-DAY0-fast.txt](TEST-DAY0-fast.txt) holds §0–§4 as five blocks to paste
  one after the other — kept in step with this page, command by command.
- **Order**: §0, then **§1 first whatever your role** (it creates the project-management
  repository of the test), then your role's section(s).

**Who runs what**

| Role | Sections | Plays |
|---|---|---|
| **Project Advisor** | §0, §1, §5 | your own Day 0: the project-management repository with the pm-kit and the instance scaffold, the checks, the start hook, the meeting chain, a session that says "go" |
| **Project lead** | §0, §1, §2, §3, §5 | your sandbox like every team member (§2) — you are a developer too — then, in W1, the kit installed once in the product repository (§3) |
| **Developer** | §0, §1, §2, §4, §5 | your sandbox (§2: Day 0 before W1), then, in W1, a product repository that already has the kit (§4) |

**The repositories in this test** — side by side in one parent folder, as on a real machine:

| Name in the commands | Which repository | Stands for |
|---|---|---|
| `gse-light` | the `gse-light` repository (method and kits), cloned from GitHub `nicolasguelfi/gse-light` | itself |
| `remote-pm.git` | a local **bare** repository (no working files), filled by §1 with the pm-kit and one instance folder `instances/demo/` | the project's private project-management repository `<pm-repo>` on GitHub |
| `remote-sandbox-<name>.git` | a local bare repository, created empty by §2 | a personal sandbox repository `<project>-sandbox-<firstname>` on GitHub |
| `remote-product.git` | a local bare repository, created empty by §3 | the product repository `<product-repo>` on GitHub (W1, once the repository layout is decided) |
| `advisor/gse-light`, `advisor/pm` | the Project Advisor's clones | his working copies |
| `<name>/gse-light`, `<name>/pm`, `<name>/sandbox` | a team member's clones (§2) | their working copies in the sandbox phase |
| `lead/product`, `dev/product` | the project lead's and a developer's clones of `remote-product.git` (§3, §4) | their working copies in the product phase |

## 0. Settings — everyone

Copy these lines in your terminal first; every block below uses them.

```bash
INST=demo                      # the instance (folder name in instances/ of the project-management repository)
TEST=~/gse-test                # throwaway folder, outside any synced folder
NAME=alex                      # §2 only: your first name, in lower case — names your sandbox and your folder
```

## 1. If you are the Project Advisor — your own Day 0 (everyone runs it first)

What it plays: the machine is already prepared ([`scripts/README.md`](../scripts/README.md) §1 —
not rehearsed here: it writes in `~/.venvs`, nothing throwaway); then the project-management
repository created with the pm-kit and the instance scaffold, the documentation checks, the
situation, the settings, one paid-model call in dry run, and the meeting chain on a ten-second
recording.

```bash
mkdir -p "$TEST/advisor" && cd "$TEST"
git init -q --bare remote-pm.git                       # remote-pm.git, empty: the project-management repository as just created on GitHub
cd advisor
git clone -q https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (method and kits)
git clone -q ../remote-pm.git pm                       # clones remote-pm.git into advisor/pm — expected warning: "You appear to have cloned an empty repository."
cd pm
../gse-light/pm-kit/install.sh . "$INST"              # the pm-kit (skills, agents, settings, CLAUDE.md, .env.example, CI) and the scaffold of instances/demo/
printf 'client-%s\nproject-%s\n' "$INST" "$INST" > "instances/$INST/private-terms.txt"   # two throwaway terms the leak guard refuses in gse-light (built here so that they appear in no file of gse-light)
python3 ../gse-light/scripts/check_docs.py             # expected: "check_docs (pm): ok (0 problem(s), 0 warning(s))"
git add -A && git commit -q -m "Instance $INST: pm-kit and scaffold" && git push -q origin HEAD   # remote-pm.git now holds the instance: §2–§4 clone it
python3 ../gse-light/scripts/situation.py              # expected: "next meeting unknown" and the note "No .env yet"
cp .env.example .env                                   # the Project Advisor's settings and keys, never committed
python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt test --dry-run   # expected: a JSON with "python" (the interpreter used) and "key_present": false
../gse-light/scripts/meeting/meeting.sh devices        # macOS: your audio inputs with their index (the .env has MEETING_AUDIO_DEVICE=0)
../gse-light/scripts/meeting/meeting.sh start 2026-01-01 && sleep 10 && ../gse-light/scripts/meeting/meeting.sh stop   # a ten-second recording — expected: audio.m4a and meta.json in instances/demo/meetings/2026-01-01/
python3 ../gse-light/scripts/meeting/transcribe.py "instances/$INST/meetings/2026-01-01"   # expected: transcript.md, or the message "no local engine" with the install line (then: scripts/README.md §1)
```

**Expected**: `pm-kit/install.sh` lists the skills (`advisor`, `cockpit-update`,
`decision-record`, `genai-onboarding`, `meeting`, `method-lesson`, `session-close`, `slides`)
and the agents (`delivery-auditor`, `design-reviewer`, `minutes-verifier`), writes
`PM_KIT_VERSION` and copies the scaffold (`README.md`, `BRIEFING.md`, the three registers,
the roles record, `journal/`, `meetings/`) into `instances/demo/`; `check_docs` prints `ok`;
`situation.py` says what is missing; the dry run shows the Python it uses (the linked
`.venv` when the project-management repository has one — not in this test) and no key; the
recording needs a microphone allowed for your terminal (macOS: System Settings › Privacy &
Security › Microphone); `transcribe.py` needs a local engine or a Gemini key, else it says so.

Then **§5**: open Claude Code in `advisor/pm` and say "go".

## 2. If you are the project lead or a developer — your sandbox (Day 0, before W1)

What it plays: every team member's real Day 0 — three clones side by side, the kit installed
**by you** in your own sandbox with one command, committed and pushed, your `.env`, the
check, the gates stub. Run it with your own `NAME` (the project lead too: you are a developer).

```bash
mkdir -p "$TEST/$NAME" && cd "$TEST"
git init -q --bare "remote-sandbox-$NAME.git"          # your sandbox as just created on GitHub, empty
cd "$NAME"
[ -d gse-light ] || git clone -q https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository
[ -d pm ] || git clone -q ../remote-pm.git pm          # the project-management repository, with the instance pushed by §1
git clone -q "../remote-sandbox-$NAME.git" sandbox     # expected warning: empty repository
cd sandbox
git commit -q --allow-empty -m init && git push -q origin HEAD   # first commit of your sandbox
../gse-light/claude-kit/install.sh "$INST"             # ONE command, yourself: finds ../gse-light and the sibling folder holding instances/demo/ (pm)
git add CLAUDE.md .claude .gitattributes gates.sh .env.example .gitignore .github
git commit -q -m "Install the Claude kit ($INST)" && git push -q origin HEAD   # the kit is in your sandbox on GitHub
cp .env.example .env                                   # your keys, never committed
{ ../gse-light/claude-kit/check.sh; echo "exit $? (0 expected)"; }   # expected: only OK lines
bash ./gates.sh                                        # the Day-0 stub, run as CI runs it — expected: "no gates yet: design phase in progress …", exit 0
```

**Expected**: `install.sh` prints `product repository sandbox · method ../gse-light · project
management ../pm/instances/demo/`, lists six skills (`decision-record`, `design-phase`,
`review`, `session-close`, `upskilling`, `verify-claim`) and one agent (`change-reviewer`), creates
`CLAUDE.md`, `.claude/settings.json`, `.gitattributes`, `gates.sh`, `.env.example` and
`.github/workflows/gates.yml`; `check.sh` shows every line `OK`, among them `kit committed`,
`settings.json gives Claude read access…`, `kit version <hash> (current)` — the hash is the
last commit of `gse-light` that touched `claude-kit/`. If `install.sh` answers "several
sibling folders hold instances/demo/", name the right one: `../gse-light/claude-kit/install.sh "$INST" --pm pm`.

Then **§5**: your first session in `$TEST/$NAME/sandbox`.

## 3. If you are the project lead — the product repository, once (W1)

What it plays: once the repository layout is decided (the first design decision), you install
the kit **once** in each product repository and commit it; the developers then get it by
cloning (§4). Same command as in your sandbox, run inside the product clone.

```bash
mkdir -p "$TEST/lead" && cd "$TEST"
git init -q --bare remote-product.git                  # remote-product.git, empty: the product repository as just created on GitHub
cd lead
[ -d gse-light ] || git clone -q https://github.com/nicolasguelfi/gse-light.git
[ -d pm ] || git clone -q ../remote-pm.git pm
git clone -q ../remote-product.git product             # expected warning: empty repository
cd product
git commit -q --allow-empty -m init && git push -q origin HEAD   # first commit of lead/product
../gse-light/claude-kit/install.sh "$INST"             # ONE command, from inside lead/product
{ ../gse-light/claude-kit/check.sh; echo "exit $? (1 expected before the commit)"; }   # expected: one MISSING "kit committed" line, one WARN .env line
bash ./gates.sh                                        # expected: "no gates yet …", exit 0
git add CLAUDE.md .claude .gitattributes gates.sh .env.example .gitignore .github
git commit -q -m "Install the Claude kit ($INST)" && git push -q origin HEAD   # the kit is now in remote-product.git
```

**Expected**: the same `install.sh` output as in §2 with `product repository product`;
`check.sh` shows `MISSING kit committed` before the commit and `WARN .env` (normal here: the
project lead needs no `.env` in `lead/product` for this rehearsal). Outside this rehearsal, a
`main` branch protected on GitHub means a pull request instead of the direct push.

## 4. If you are a developer — a product repository that already has the kit (W1)

What it plays: the project lead has pushed the kit (§3); you clone, add your `.env`, check.
You never run `install.sh` in a product repository.

```bash
mkdir -p "$TEST/dev" && cd "$TEST/dev"
[ -d gse-light ] || git clone -q https://github.com/nicolasguelfi/gse-light.git
[ -d pm ] || git clone -q ../remote-pm.git pm
git clone -q ../remote-product.git product             # the kit comes with it
cd product
cp .env.example .env                                   # personal settings of dev/product, never committed
{ ../gse-light/claude-kit/check.sh; echo "exit $? (0 expected)"; }   # expected: only OK lines
git status --short                                     # expected: nothing (.env is ignored)
```

**Expected**: every line `OK`, among them `gates.sh present and executable`,
`.gitattributes keeps scripts LF`, `kit version <hash> (current)`. Two `WARN` lines can
replace the last one outside this rehearsal: `the kit in gse-light is newer` (the project lead
refreshes the kit with `install.sh`) and `your clone of gse-light is behind` (run `git pull`
in your `gse-light`).

## 5. First session — every role (interactive)

| Role | Where | What to do in the session |
|---|---|---|
| Project Advisor | `claude` in `$TEST/advisor/pm` | the start hook prints the situation (next meeting unknown, no `.env` or the one you copied); say "go": the `advisor` skill proposes the next step and asks you one short multiple-choice question |
| Project lead, developer | `claude` in `$TEST/$NAME/sandbox` (or in `lead/product`, `dev/product` for the product phase) | type `/` — `decision-record`, `design-phase`, `review`, `session-close`, `verify-claim`, `upskilling` appear; type `/upskilling` — fifteen minutes of questions and small checks, then a personal plan; ask *"what is in ../pm/instances/demo/?"* — Claude reads it (`additionalDirectories`) but cannot edit `../gse-light` nor the instance's `BRIEFING.md` (deny rules of `.claude/settings.json`), and asks before any `git push` |

## 6. Check that nothing personal went into git

```bash
git status --short                                     # in every clone you worked in: .env must not appear
ls ~/.claude/upskilling/"$INST"/                       # your private record, in your home folder, outside every repository
```

## 7. Clean up

```bash
rm -rf "$TEST"                                         # removes remote-pm.git, remote-sandbox-*.git, remote-product.git, advisor/, <name>/, lead/ and dev/
rm -rf ~/.claude/upskilling/"$INST"                    # only if /upskilling wrote a test record
```

## If something differs

- A `check.sh` line is not `OK`: paste its output to the session; [INSTALL.md §6](INSTALL.md#6-if-something-is-missing)
  lists what each line means.
- `check_docs` fails in §1: read the `FAIL` lines; the scaffold and the pm-kit must agree
  (refresh with `../gse-light/pm-kit/install.sh .`).
- The recording fails in §1: the microphone is not allowed for your terminal, or you are not
  on macOS (`meeting.sh` records with ffmpeg's avfoundation; elsewhere, import a file with
  `meeting.sh import`).
- Not covered by this rehearsal: Windows (use Git Bash for the same commands), the real
  repositories on GitHub, the preparation of the machine ([`scripts/README.md`](../scripts/README.md)).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

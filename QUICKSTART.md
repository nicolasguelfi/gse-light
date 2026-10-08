# Quick start for developers — what gse-light does and what to use, all project long

Status: v0.3 · 2026-10-08 · one page; details in [INSTALL.md](claude-kit/INSTALL.md) and [ONBOARDING.md](claude-kit/ONBOARDING.md)

## What gse-light does for you

`gse-light` is the method your project runs with. You clone it once, next to your project's
other repositories; you never change it. It gives your Claude Code sessions a few firm
habits — measure before asserting, decisions in registers (`PD` project, `DEC` requirements,
`DD` design decisions), nothing state-changing without a go-ahead, a journal entry per
session, end-to-end tests through the real user interface — through a **kit** committed in
each product repository: five skills (`design-phase`, `decision-record`, `session-close`,
`verify-claim`, `upskilling`), one agent (`change-reviewer`), a `gates.sh` the design phase
fills, and a CI workflow that runs it (`bash ./gates.sh`).

```text
~/dev/<project>/                      one parent folder, the clones side by side
├── gse-light/        the method (public) — read by every session, changed by none
├── <pm-repo>/        project management (private): instances/<instance>/ — registers,
│                     journal, sprints, the Project Advisor's cockpit BRIEFING.md
├── <product-repo>/   the code (private) — you work here; the kit is committed in it
└── <project>-sandbox-<firstname>/   your sandbox (private, throwaway): Day 0 and your
                      experiments, and the stand-in for <product-repo> until it exists
```

**Prerequisites**: Git, a bash terminal (Git Bash on Windows; the scripts keep Unix line
endings there), `python3`, Claude Code signed in with the invited account, access on GitHub
to `<pm-repo>` (from whoever hosts it) and to `<product-repo>` or your sandbox (from the
project lead).

## Day 0 — three lanes

**Lane 0 — no product repository yet? your sandbox** (*you*, once the project lead or the
Project Advisor has created it on GitHub). Until the product repositories exist, every team
member works in a personal, private, throwaway repository `<project>-sandbox-<firstname>`,
with the kit installed by the one command — here **you** run it, it is your repository:

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (the method)
git clone <pm-repo URL>                                    # the project-management repository
git clone <sandbox URL>                                    # your sandbox <project>-sandbox-<firstname>
cd <project>-sandbox-<firstname>
../gse-light/claude-kit/install.sh <instance>              # ONE command; add --pm <pm-repo> if it asks
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>)" && git push -u origin HEAD
cp .env.example .env                                       # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
claude                                                     # type /, run /upskilling, then experiment
```

Your sessions' journal entries and new 🔴 records go to `<pm-repo>/instances/<instance>/`
through the skills, from the sandbox as from any product repository. You never open Claude
Code in `<pm-repo>`: the sessions opened there are the Project Advisor's. The project lead's
sandbox is also where the design phase runs: its first decision, repository layout, names
the real product repositories, which then receive the kit (Lane 1). Your sandbox stays
yours for experiments afterwards.

**Lane 1 — the project lead, once per product repository** (*you*, then *ask Claude*).
**Step 0 — the product repository exists on GitHub**, named by the repository-layout `DD`
of the design phase; you or the client's IT create it, empty or with a README only. If its
`main` branch is protected on GitHub (branch protection — recommended; each project decides it in its roles record),
the kit arrives by pull request instead of a direct push; everything else is the same.

```bash
cd ~/dev/<project>                                         # gse-light and <pm-repo> are already there (Lane 0)
git clone <product-repo URL>                               # the product repository (empty or README only)
cd <product-repo>
../gse-light/claude-kit/install.sh <instance>              # ONE command; add --pm <pm-repo> if it asks
claude                                                     # then say: "fill CLAUDE.md with this project's purpose and commands"
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>)"
git push                                                   # first push on an empty repository: git push -u origin HEAD
```

Then tell the team the kit is in. The command finds `../gse-light` and the sibling folder
that holds `instances/<instance>/` by itself; it asks for `--pm <folder>` only when there are
none or several.

**Lane 2 — every developer** (*you*):

```bash
cd ~/dev/<project>                                         # gse-light and <pm-repo> are already there (Lane 0)
git clone <product-repo URL>                               # the product repository, kit included
cd <product-repo> && cp .env.example .env                  # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
```

Then `claude` in the product repository, type `/` (the five skills appear), run `/upskilling`
if you have not done it in your sandbox. You never run `install.sh` in a product repository;
if you cloned before the kit was there: `git pull` once the project lead has pushed.
Prerequisites, Windows, troubleshooting: [INSTALL.md](claude-kit/INSTALL.md).

## All project long — when, what

Who does it: *you*, *ask Claude* (say it in the session), *automatic*.

| When | What | Who |
|---|---|---|
| Start of a session | `claude` in the product repository (or your sandbox); it reads `CLAUDE.md`: rules, commands and the **project's zone** — `../<pm-repo>/instances/<instance>/`, the folder where your decisions and journal go | automatic |
| W1 — design phase | in the project lead's sandbox, *"Run design-phase"*: the project's drivers → `DD` records (the twelve decisions of `design-phase` §2, in order; the first, repository layout, names the product repositories) → in each product repository, `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` filled from them | ask Claude + project lead |
| Taking a ticket | *"Read ticket #N, its requirement and its example; restate what is asked"* | ask Claude |
| A choice with consequences | *"Record it with decision-record"* — a 🔴 record in `<pm-repo>`, pushed by the skill; the person who holds the right decides | ask Claude |
| Before stating a fact (version, count, test result, cause) | `verify-claim`: the command and its output, never a guess | ask Claude |
| Writing code | on a feature branch, with its tests; a user path gets its **end-to-end test through the real user interface**, driven by Claude to play the use case (the tool from the test-tools `DD`; Playwright is one example for a web interface); run `./gates.sh`; read the diff yourself | ask Claude + you |
| Before a pull request | *"Run the change-reviewer agent"*; fix what it lists; the PR updates the document of the behaviour | ask Claude |
| Merging | gates green in CI (`bash ./gates.sh`), review by a person; the rehearsal environment and production only with the go-ahead in the roles record | automatic + a person |
| End of a session | *"Close the session"* (`session-close`): journal entry and metrics row in `<pm-repo>`, pushed by the skill — a colleague with no memory must be able to resume | ask Claude |
| Stuck with Claude or a technology | `/upskilling` again: it re-checks and adjusts your plan | you |
| Every sprint | sprint file `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`; meeting with the Project Advisor (weekly; a part-time period may hold fewer), who reads the merged PRs, gates and journal — link your tickets and write your journal | project lead + you |
| When `check.sh` says *kit version … the kit in gse-light is at …* | *you*: `git pull` in `gse-light` and in `<product-repo>`; if the line stays, the project lead reruns the one command in `<product-repo>` and pushes | you, then the project lead |
| Last week | hand-over document and last journal entry; retrospective, lessons kept in the method | ask Claude + the team |

## Why three repositories

Your sessions **read** the method in `../gse-light` and **write** decisions and the journal in
`../<pm-repo>/instances/<instance>/` — both are listed as additional directories in the
kit's `settings.json`. The same file denies Claude the Edit tool under `../gse-light/**` and
on `BRIEFING.md` (the Project Advisor's cockpit), and the literal command
`git push origin main`; Claude asks before any `git push`. These rules are conveniences for
the session, not a security boundary: what guards the method, the cockpit and `main` is
review by a person, and — when the project has enabled it in its roles record — GitHub
branch protection on `main` (recommended for every repository that deploys).

- **Known limit**: a Claude Code session started on claude.ai (the web or cloud version)
  works in an isolated container with **one** GitHub repository cloned into it; it sees
  neither `../gse-light` nor `../<pm-repo>`, so the rules, the registers and the journal are
  out of its reach. Work locally, on your machine, where the clones are side by side.
- **A product made of several repositories**: the kit is installed **in each** product
  repository (same one command). The list of the project's repositories lives in
  `<pm-repo>/instances/<instance>/README.md` (decided in the design phase, repository-layout
  `DD`). For an overall view, the Project Advisor opens Claude Code in `<pm-repo>` with the
  product repositories added as additional directories
  (`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`).

## Never

A secret in a file under git (`.env` is yours alone) · a push to `main`, or to any branch that
deploys, without the go-ahead · a claim about a running system without its command · a decision
that lives only in a chat · editing `BRIEFING.md` (the Project Advisor's cockpit) · editing
`gse-light` from a project session · opening Claude Code in `<pm-repo>` (your journal and
records get there through the skills).

## Read next

[ONBOARDING.md](claude-kit/ONBOARDING.md) — the words used, the method in one page, your
first session step by step, the Day-0 and first-sprint checklists ·
[reference design](method/00-reference-design.md) chapters 0–2 and 13 (the project lead
adds 15) · [GLOSSARY.md](GLOSSARY.md) — every word and acronym above (`DD`, gate, go-ahead,
sandbox…) in plain words.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

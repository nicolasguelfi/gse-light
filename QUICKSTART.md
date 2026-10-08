# Quick start for developers — what gse-light does and what to use, all project long

Status: v0.1 · 2026-10-08 · one page; details in [INSTALL.md](claude-kit/INSTALL.md) and [ONBOARDING.md](claude-kit/ONBOARDING.md)

## What gse-light does for you

`gse-light` is the method your project runs with. You clone it once, next to your project's
two repositories; you never change it. It gives your Claude Code sessions in the product
repository a few firm habits — measure before asserting, decisions in registers, nothing
state-changing without a go-ahead, a journal entry per session — through a **kit** the project
lead has already committed in the product repository: four skills (`decision-record`,
`session-close`, `verify-claim`, `upskilling`) and one agent (`change-reviewer`).

| Repository | What it is for you |
|---|---|
| `gse-light` (public) | the method to read, and `check.sh` |
| `<pm-repo>` (private) | your project's management: registers, sprints, journal (`instances/<instance>/`) |
| `<product-repo>` (private) | the code — **you work here**, with the kit already in it |

## Day 0 — install (15 minutes, once)

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (the method)
git clone <pm-repo URL>                                    # the project-management repository
git clone <product-repo URL>                               # the product repository, kit included
cd <product-repo> && cp .env.example .env                  # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
```

Then `claude` in the product repository, type `/` (the four skills appear), run `/upskilling`.
Prerequisites, Windows, troubleshooting: [INSTALL.md](claude-kit/INSTALL.md).

## All project long — when, what

Who does it: *you*, *ask Claude* (say it in the session), *automatic*.

| When | What | Who |
|---|---|---|
| Start of a session | `claude` in the product repository; it reads `CLAUDE.md` (rules, commands, the project's zone) | automatic |
| Taking a ticket | *"Read ticket #N, its requirement and its example; restate what is asked"* | ask Claude |
| A choice with consequences | *"Record it with decision-record"* — a 🔴 record in `<pm-repo>`; the person who holds the right decides | ask Claude |
| Before stating a fact (version, count, test result, cause) | `verify-claim`: the command and its output, never a guess | ask Claude |
| Writing code | on a feature branch, with its tests; run the gates (command in `CLAUDE.md`); read the diff yourself | ask Claude + you |
| Before a pull request | *"Run the change-reviewer agent"*; fix what it lists; the PR updates the document of the behaviour | ask Claude |
| Merging | gates green in CI, review by a person; staging and production only with the go-ahead in the roles record | automatic + a person |
| End of a session | *"Close the session"* (`session-close`): journal entry and metrics row in `<pm-repo>` — a colleague with no memory must be able to resume | ask Claude |
| Stuck with Claude or a technology | `/upskilling` again: it re-checks and adjusts your plan | you |
| Every week | sprint file `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`; two-hour meeting with the Project Advisor, who reads the merged PRs, gates and journal — link your tickets and write your journal | project lead + you |
| When `check.sh` says *kit version … gse-light is at …* | `git pull` in `gse-light`; the project lead refreshes the kit in the product repository | the project lead |
| Last week | hand-over document and last journal entry; retrospective, lessons kept in the method | ask Claude + the team |

## Never

A secret in a file under git (`.env` is yours alone) · a push to `staging` or `main` without the
go-ahead · a claim about a running system without its command · a decision that lives only in a
chat · editing `BRIEFING.md` (the Project Advisor's cockpit).

## Read next

[ONBOARDING.md](claude-kit/ONBOARDING.md) — the method in one page, your first session step
by step, the Day-0 checklist · [reference design](method/00-reference-design.md) chapters 1 and 13.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

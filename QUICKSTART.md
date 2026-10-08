# Quick start for developers — what gse-light does and what to use, all project long

Status: v0.2 · 2026-10-08 · one page; details in [INSTALL.md](claude-kit/INSTALL.md) and [ONBOARDING.md](claude-kit/ONBOARDING.md)

## What gse-light does for you

`gse-light` is the method your project runs with. You clone it once, next to your project's
two repositories; you never change it. It gives your Claude Code sessions in the product
repository a few firm habits — measure before asserting, decisions in registers, nothing
state-changing without a go-ahead, a journal entry per session, end-to-end tests through the
real user interface — through a **kit** the project lead has committed in the product
repository: five skills (`design-phase`, `decision-record`, `session-close`, `verify-claim`,
`upskilling`), one agent (`change-reviewer`), a `gates.sh` the design phase fills, and a CI
workflow that runs it.

```text
~/dev/<project>/                      one parent folder, three clones side by side
├── gse-light/        the method (public) — read by every session, changed by none
├── <pm-repo>/        project management (private): instances/<instance>/ — registers,
│                     journal, sprints, the Project Advisor's cockpit BRIEFING.md
└── <product-repo>/   the code (private) — you work here; the kit is committed in it
```

**Prerequisites**: Git, a bash terminal (Git Bash on Windows), `python3`, Claude Code signed
in with the invited account, access on GitHub to `<pm-repo>` and `<product-repo>`.

## Day 0 — two lanes, in this order

**Step 0 — the product repository exists on GitHub.** The project lead or the client's IT
creates it (empty, or with a README only). If its `main` branch is protected, the kit arrives
by pull request instead of a direct push; everything else below is the same.

**Lane 1 — the project lead, once per product repository** (*you*, then *ask Claude*):

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (the method)
git clone <pm-repo URL>                                    # the project-management repository
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
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (the method)
git clone <pm-repo URL>                                    # the project-management repository
git clone <product-repo URL>                               # the product repository, kit included
cd <product-repo> && cp .env.example .env                  # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
```

Then `claude` in the product repository, type `/` (the five skills appear), run `/upskilling`.
If you cloned before the kit was there: `git pull` once the project lead has pushed.
Prerequisites, Windows, troubleshooting: [INSTALL.md](claude-kit/INSTALL.md).

## All project long — when, what

Who does it: *you*, *ask Claude* (say it in the session), *automatic*.

| When | What | Who |
|---|---|---|
| Start of a session | `claude` in the product repository; it reads `CLAUDE.md` (rules, commands, the project's zone) | automatic |
| Week 1 — design phase | *"Run design-phase"* with the project lead: the project's drivers → `DD` records (architecture, repository layout, environments, branch model, test tools) → `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` filled from them | ask Claude + project lead |
| Taking a ticket | *"Read ticket #N, its requirement and its example; restate what is asked"* | ask Claude |
| A choice with consequences | *"Record it with decision-record"* — a 🔴 record in `<pm-repo>`, pushed by the skill; the person who holds the right decides | ask Claude |
| Before stating a fact (version, count, test result, cause) | `verify-claim`: the command and its output, never a guess | ask Claude |
| Writing code | on a feature branch, with its tests; a user path gets its **end-to-end test through the real interface**, driven by Claude to play the use case (tool from the test `DD`, Playwright for a web interface); run `./gates.sh`; read the diff yourself | ask Claude + you |
| Before a pull request | *"Run the change-reviewer agent"*; fix what it lists; the PR updates the document of the behaviour | ask Claude |
| Merging | gates green in CI, review by a person; the rehearsal environment and production only with the go-ahead in the roles record | automatic + a person |
| End of a session | *"Close the session"* (`session-close`): journal entry and metrics row in `<pm-repo>`, pushed by the skill — a colleague with no memory must be able to resume | ask Claude |
| Stuck with Claude or a technology | `/upskilling` again: it re-checks and adjusts your plan | you |
| Every week | sprint file `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`; two-hour meeting with the Project Advisor, who reads the merged PRs, gates and journal — link your tickets and write your journal | project lead + you |
| When `check.sh` says *kit version … the kit in gse-light is at …* | `git pull` in `gse-light`; the project lead reruns the one command in the product repository | the project lead |
| Last week | hand-over document and last journal entry; retrospective, lessons kept in the method | ask Claude + the team |

## Why three repositories

Your sessions **read** the method in `../gse-light` and **write** decisions and the journal in
`../<pm-repo>/instances/<instance>/` — both are listed as additional directories in the
kit's `settings.json`. The same file denies Claude any edit under `../gse-light/` and of
`BRIEFING.md` (the Project Advisor's cockpit): from the product repository, Claude cannot
change the method nor the cockpit, whatever it is asked. A person can, by git; review and
the branch rules of GitHub are the guard there.

- **Known limit**: a Claude Code session started on claude.ai (the web or cloud version)
  works in a sandbox with **one** GitHub repository cloned into it; it sees neither
  `../gse-light` nor `../<pm-repo>`, so the rules, the registers and the journal are out of
  its reach. Work locally, on your machine, where the three clones are side by side.
- **A product made of several repositories**: the kit is installed **in each** product
  repository (same one command). The list of the project's repositories lives in
  `<pm-repo>/instances/<instance>/README.md` (decided in the design phase, repository-layout
  `DD`). For an overall view, open Claude Code in `<pm-repo>` with the product repositories
  added as additional directories (`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`).

## Never

A secret in a file under git (`.env` is yours alone) · a push to `main`, or to any branch that
deploys, without the go-ahead · a claim about a running system without its command · a decision
that lives only in a chat · editing `BRIEFING.md` (the Project Advisor's cockpit) · editing
`gse-light` from a project session.

## Read next

[ONBOARDING.md](claude-kit/ONBOARDING.md) — the method in one page, your first session step
by step, the Day-0 checklist · [reference design](method/00-reference-design.md) chapters 1 and 13.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

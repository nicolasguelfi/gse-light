# Claude kit for product repositories

Status: v0.1 · 2026-10-08 · the kit's map, one section per role · maintained by the Project Advisor

This folder is the **kit**: the files that make every Claude Code session in a product or
sandbox repository follow the method, kept here so a fix is made once and propagated
everywhere. This page is its map — for the project lead who installs it, the developers who
receive it, the product owner who only needs to know what it guarantees, and the Project
Advisor who maintains it: read your section (§1–§4), then the contents table (§5).

> **Words used here** — *Kit*: the files that make every Claude Code session in a
> repository follow the method — `CLAUDE.md`, five skills, one agent, permissions, a
> `gates.sh` stub, a CI workflow — installed with one command, committed with the code; two
> kits: this `claude-kit` for product and sandbox repositories, the
> [`pm-kit`](../pm-kit/README.md) for the Project Advisor in `<pm-repo>`. *Skill*: a
> procedure Claude runs when asked (`/name`) or when the situation calls for it; *agent*: a
> read-only helper Claude launches (a reviewer, an auditor). *Project-management
> repository* `<pm-repo>`: the project's shared record — decisions, requirements, plans,
> minutes, journal — private, one per project; everyone reads it, each person writes their
> own part in it through the kit's skills; nobody manages the project from it. *Instance*:
> one project run with the method, and its folder `instances/<instance>/` in `<pm-repo>`.
> *Product repository* `<product-repo>`: the code, private, one or several (repository
> layout, the first design decision); the kit is committed in it. *Sandbox*: a personal,
> private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0
> (each person's first hour on the project) and experiments until the product repositories
> exist; the project lead's sandbox hosts the design phase. *Placeholders* `<instance>`,
> `<pm-repo>`, `<product-repo>`, `<project>`, `<firstname>`: the project's real names;
> `<instance>` is the folder name under `instances/` (`ls ../<pm-repo>/instances` shows it;
> the project lead gives it). *Design phase*: the step of W1 (the first project week) where
> the project lead, with Claude, turns the project's facts and constraints into twelve
> technical decisions (`DD` records), in order: repository layout, hosting, environments
> and promotion path, stack and language, data store, identity, infrastructure as code,
> continuous integration, test tools, secrets, dependency updates, monitoring — recorded
> with the skill `design-phase`. *Decision record and badges*: every `PD-NN`, `DEC-NNN` or
> `DD-NN` in these pages is one numbered decision record, with a status badge — 🔴 pending,
> 🟢 decided, 🟡 provisional; its *decider* (the person the roles record names) is the only
> one who turns it 🟢. *Gates*: the project's automated checks (tests, lint, end-to-end) run
> by `gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet". Every
> other term: [GLOSSARY.md](../GLOSSARY.md).

<!-- who-is-who:start -->
**Who is who.** The **client** is the organisation the product is built for; it names the **product owner** (owns the need, accepts each delivered increment, gives the production and budget go-aheads) and the **data protection contact** (decides how personal data may enter the product). The **project lead** (lead developer) runs the project inside the team: sprints, tickets, technical choices, code review; the developers' first contact. The **developers** build the product with Claude Code, each in their own repository; "team member" means the project lead or a developer. The **Project Advisor** is outside the team: the method's author, two hours of meeting and two hours of preparation a week; gives feedback and advice, decides nothing in the project. **Claude sessions** propose, measure, write and test; they decide nothing and act on a go-ahead. Who decides what in a given project: its **roles record**, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`.
<!-- who-is-who:end -->

## 1. If you are the project lead

**Read first**: [INSTALL.md §2](INSTALL.md#2-if-you-are-the-project-lead--install-the-kit-in-the-product-repository-once-per-product-repository)
— what the one command writes, the commit, a protected `main`, the refresh. **You
install** the kit **once per product repository** — and each team member installs it once
in their own sandbox — with `gse-light` and `<pm-repo>` cloned next to that repository
(same parent folder):

```bash
cd <product-repo>                                   # inside the product (or sandbox) clone
../gse-light/claude-kit/install.sh <instance>       # add --pm <pm-repo> when it asks (none or several candidates)
```

then commit and push what it created. Skills, agents, the licence notice and
`.claude/KIT_VERSION` are overwritten on every run (the kit owns them); `CLAUDE.md`,
`settings.json`, `gates.sh`, `.gitattributes`, `.env.example` and the CI workflow are
created only if absent (the product repository owns them after creation). `<instance>` and
`<pm-repo>` in the new `CLAUDE.md` are replaced by the names found. `KIT_VERSION` is the
last `gse-light` commit that touched `claude-kit/`. **Refresh** after the kit changes:
`git pull` in `gse-light`, then the same command; it warns when the `CLAUDE.md` or
`settings.json` templates changed since the recorded `KIT_VERSION` and prints the exact
`git diff` command (from that old hash) so you can carry the change over by hand. A product
made of several repositories: the same command in each. **You write**: the kit's commits,
the `<…>` fields of `CLAUDE.md` (ask Claude) and, in W1, the twelve `DD` records of the
design phase (skill `design-phase`, in your sandbox). **You never**: open Claude Code in
`<pm-repo>` (its sessions are the Project Advisor's); edit the kit's own files in a product
repository (they are changed in `gse-light`, §4, and overwritten at the next refresh).

## 2. If you are a developer

**Read first**: [INSTALL.md §3](INSTALL.md#3-if-you-are-a-developer--get-the-kit-about-15-minutes)
(clone, `.env`, `check.sh`, first session), then [ONBOARDING.md](ONBOARDING.md) (the method
in one page, your first session, the Day-0 checklist). **You install** nothing in a product
repository: the kit comes with the clone, then three personal steps (`.env`, `check.sh`,
`claude`). In your sandbox you run the one command of §1 yourself and commit the kit. **You
write**, through the kit's skills only: your journal entries and your new 🔴 records in
`<pm-repo>/instances/<instance>/` (`session-close` and `decision-record` commit and push
those paths, nothing else). **You never**: run `install.sh` in a product repository; open
Claude Code in `<pm-repo>`; put a secret in a file under git. To rehearse Day 0 on your own
machine first: [TEST-DAY0.md](TEST-DAY0.md).

## 3. If you are the product owner

Nothing to install, nothing to run, no Claude Code licence needed. What the kit guarantees
you: every change comes with its tests, nothing reaches production and nothing is spent
without the go-ahead the roles record gives you, and every decision that awaits you is a 🔴
record in `<pm-repo>`, which you read on GitHub (its instance `README.md` first). The rest of
this page is for the team.

## 4. If you are the Project Advisor

You own the kit's content; the project lead installs and refreshes it. **You change it
here**, by pull request in the `gse-light` repository, then each product repository reruns
the one command of §1. Two skills (`decision-record`, `session-close`) are also in the
[pm-kit](../pm-kit/README.md), your own kit for `<pm-repo>`: `scripts/check_docs.py` fails
if the two copies differ. The entry pages stay in step — [QUICKSTART.md](../QUICKSTART.md),
[INSTALL.md](INSTALL.md), [ONBOARDING.md](ONBOARDING.md), this page, the `CLAUDE.md`
template and the Day-0 rehearsals change together — and never carry a client or project
name: the leak guard (`check_docs.py`) refuses it. After any kit change, replay
[TEST-DAY0.md](TEST-DAY0.md). Claude Code licences come from you, API keys from the client.
The documentation checks of `<pm-repo>` run from a product repository as
`python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the repository to check is the
argument). **You never** install this kit in `<pm-repo>`, nor open Claude Code in a team
member's sandbox.

## 5. Contents

| Path | What it is | Installed as |
|---|---|---|
| [`INSTALL.md`](INSTALL.md) | **How to install**: the project lead with one command from inside the product clone (and commit), developers by cloning; shared vs personal files; prerequisites macOS / Windows; what `check.sh` says | read, not installed |
| [`TEST-DAY0.md`](TEST-DAY0.md) | Rehearse a developer's Day 0 on your own machine, in a throwaway folder: 15 minutes for the install and checks; the first session adds 15 minutes of `/upskilling` and 30 minutes of work | read, not installed |
| [`TEST-DAY0-fast.txt`](TEST-DAY0-fast.txt) | The same rehearsal as three blocks to copy and paste (reset, project lead, developer) | read, not installed |
| [`install.sh`](install.sh) | Installs or refreshes the kit; run from inside the product (or sandbox) repository: `../gse-light/claude-kit/install.sh <instance> [--pm <folder>]` | run from the product repository |
| [`check.sh`](check.sh) | Day-0 check a developer runs from inside the product repository (read-only); compares `KIT_VERSION` with the last `gse-light` commit that touched `claude-kit/` and says whether the kit in `gse-light` is newer or your clone of `gse-light` is behind | run from the product repository |
| [`ONBOARDING.md`](ONBOARDING.md) | **Starting guide for the team** (the project lead and the developers): who provides what, the method in one page, Day-0 install, first session step by step, the week's rhythm, one section per role, checklists | read, not installed |
| [`templates/env.example`](templates/env.example) | Local secrets and settings; keys for complementary models come from the client organisation | `.env.example` (created once; `.env` is never committed) |
| [`templates/CLAUDE.product-repo.md`](templates/CLAUDE.product-repo.md) | Instructions file for a product repository; `<instance>` and `<pm-repo>` are substituted at install | `CLAUDE.md` (created once, then owned by the product repository) |
| [`templates/settings.json`](templates/settings.json) | Shared Claude Code permissions: `../gse-light` and `../<pm-repo>` as additional directories; read-only commands, the gates and the checks allowed; the Edit tool denied under `../gse-light/` and on the cockpit `BRIEFING.md` (the Project Advisor's one-page dashboard in the instance); the literal `git push origin main` denied and any other `git push` asked — conveniences, not a security boundary (`main` is protected on GitHub in every repository) | `.claude/settings.json` (created once) |
| [`templates/gates.sh`](templates/gates.sh) | Day-0 stub of the gates: prints *no gates yet: design phase in progress* and exits 0; filled from the continuous integration and test tools decisions (the eighth and ninth of the twelve) | `gates.sh` (created once, executable) |
| [`templates/ci-gates.yml`](templates/ci-gates.yml) | CI workflow that runs `bash ./gates.sh` on every pull request and on every push to `main` | `.github/workflows/gates.yml` (created once) |
| [`templates/gitattributes`](templates/gitattributes) | `*.sh text eol=lf`: shell scripts keep Unix line endings on a Windows clone | `.gitattributes` (created once) |
| [`templates/KIT_LICENSE.md`](templates/KIT_LICENSE.md) | Licence notice that travels with the kit | `.claude/KIT_LICENSE.md` (refreshed) |
| [`skills/design-phase/`](skills/design-phase/SKILL.md) | W1: the project's drivers → `DD` records (the twelve decisions of *Words used here*, from repository layout to monitoring, in order) → `gates.sh`, CI and `CLAUDE.md` placeholders filled | `.claude/skills/design-phase/` (refreshed) |
| [`skills/decision-record/`](skills/decision-record/SKILL.md) | Record a decision in the right register; commits and pushes that record only | `.claude/skills/decision-record/` (refreshed) |
| [`skills/session-close/`](skills/session-close/SKILL.md) | Journal entry, metrics, hand-over; commits and pushes those paths only | `.claude/skills/session-close/` (refreshed) |
| [`skills/verify-claim/`](skills/verify-claim/SKILL.md) | Measure before asserting | `.claude/skills/verify-claim/` (refreshed) |
| [`skills/upskilling/`](skills/upskilling/SKILL.md) | Personal coach: where you start, what your responsibilities need, a short plan, the method in two steps ([method](../method/20-upskilling.md)) | `.claude/skills/upskilling/` (refreshed) |
| [`agents/change-reviewer.md`](agents/change-reviewer.md) | Reviews a change against the reference design and the instance's `DD` records | `.claude/agents/change-reviewer.md` (refreshed) |

The kit targets **Claude Code only**; with another coding agent the rules still apply, the
kit does not install itself there.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

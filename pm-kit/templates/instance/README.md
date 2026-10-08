# Instance `<instance>` — <Project name>

The project-management folder of <Project name>, run with the method
[`gse-light`](https://github.com/nicolasguelfi/gse-light/blob/main/README.md), cloned next to
this repository ([reference design](https://github.com/nicolasguelfi/gse-light/blob/main/method/00-reference-design.md),
[the Project Advisor's page](https://github.com/nicolasguelfi/gse-light/blob/main/method/15-project-advisor.md)).
**No product code here.** Fields written `<like this>` are filled when the instance is created.

## Repositories

This table is the project's **overall view**. Once the repository layout is decided (the
first of the twelve decisions of `design-phase` §2), list each product repository here: the
`delivery-auditor` agent audits those rows only.

| Repository | Holds | Where | Status |
|---|---|---|---|
| `gse-light` (public) | the method, the kits | `../gse-light`, cloned next to this one | in use |
| `<pm-repo>` (private, this one) | the project management of <Project name>: this instance | `instances/<instance>/` | in use |
| `<project>-sandbox-<first name>` (private, one per team member) | personal experiments, Day 0, `/upskilling`; the project lead's one also hosts the design phase | clones next to this one, the kit installed by `../gse-light/claude-kit/install.sh <instance>` run inside the clone | throwaway — **not** product repositories, never audited, never listed below |
| product repositories | the product's code, data jobs, infrastructure code — one or several | clones next to this one, each with the kit | **to decide** — repository layout, design phase (W1) |

## The project

<Two or three lines: what the product does, for whom, what "done" means. The vision is
written in `requirements/00-vision.md`.> Weeks W1 to Wn from <YYYY-MM-DD>; the framing
week W-1 ends with the kick-off of <YYYY-MM-DD>. The project lead dates and sizes the
weeks with the team; the meeting day with the Project Advisor is fixed at each meeting
for the next one.

## People

The **Project Advisor** (named in the [roles record](governance/10-roles-and-go-aheads.md))
gives feedback and advice on project conduct and deliverables; he does not manage the
project. <project lead> runs it with <engineers>; <product owner> accepts increments on
the client side; <data protection contact> decides any new flow of personal data.

Nobody on the team opens Claude Code in this repository: sessions here are the Project
Advisor's. The team's journal entries and new 🔴 records arrive from their sandbox or
product repositories through the kit's `session-close` and `decision-record` skills; the
project lead also writes `planning/sprints/`; never `BRIEFING.md`.

## Phase

Framing (W-1), since <YYYY-MM-DD>: examples and data are being gathered; the team is
<named / being named>; every design choice is 🔴 pending in the
[design register](design/05-design-decisions.md) until the design phase of W1.

## Folders

| Path | What it holds |
|---|---|
| [`BRIEFING.md`](BRIEFING.md) | Cockpit: §1 what awaits the Project Advisor, §1b the team, §2 changes, §3 state |
| [`governance/`](governance/) | Roles and go-aheads, project decisions (`PD-NN`), charter and risks once written |
| [`requirements/`](requirements/) | Vision, requirements decisions (`DEC-NNN`); `40-examples/` one file per real example; `50-sources/<date>-<source>.md` one dated report per source — personal data stays out of git (the instance's data-regime record) |
| [`design/`](design/) | Design decisions (`DD-NN`), the drivers page and the design choices once the design phase runs |
| `planning/` | Roadmap and one file per week in `sprints/` (project lead) |
| [`meetings/`](meetings/README.md) | One folder per meeting (agenda, transcript, minutes, slides); presentations registry |
| [`journal/`](journal/README.md) | One entry per working session, `metrics.csv` — never rewritten |
| `private-terms.txt` | Terms the leak guard refuses in the public `gse-light` (client name, project name) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

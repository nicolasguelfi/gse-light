# 10 — Roles and go-aheads

Status: living · v0.1 · <YYYY-MM-DD>

> **Essentials** — Who decides what, and which actions need an explicit go-ahead before
> anyone — human or Claude — performs them. <Project name> is run by its team: the
> project lead and the developers. The **Project Advisor** gives feedback and advice; he is
> not the project manager.

## 1. Roles

| Role | Holder | Decides | Does not decide |
|---|---|---|---|
| Project Advisor | <name> | the generative-AI method and the Claude kits; approval of the reference design as the project's recommended practice; spending on his own AI keys and the Claude Code licences he provides; his advice counts in requirements choices; he may propose tickets and priorities (the project lead decides) | sprints, priorities, tickets, promotions, cloud resources, the client's budget |
| Project lead (lead developer) | <project lead> | sprint goals and plans, priorities inside the vision, tickets, the design phase (W1) and the technical choices inside a decided `DD`, code review, promotion to the rehearsal environment (environments and promotion path record), the team's sandbox repositories | acceptance of increments; production; new flows of personal data |
| Product owner (client side) | <product owner> | what the product must do; acceptance of increments; promotion to production; cloud resources and the client's budget | technical design |
| Developers | <developers> | implementation within their tickets | — |
| Data protection contact | <data protection contact> | any new flow of personal data | — |
| Claude sessions | — | nothing on their own: they propose, measure, write, and act only on a go-ahead | — |

**Team member** in this instance's pages means the project lead or a developer; the product
owner and the data protection contact are on the client's side and write nothing in
`<pm-repo>`. **Host of `<pm-repo>`** (grants access to it): <name>.

**What the Project Advisor does each week**: one two-hour meeting with the team plus two
hours of preparation. He reads what the team delivered, gives feedback and advice on
project conduct and on deliverables, records the meeting and its minutes with the tasks
each participant took, and raises the decisions nobody has taken. He writes no sprint,
no ticket, no code. Only his sessions edit `BRIEFING.md` and the decided records.

**Until a holder is named**, the actions in that column wait. If the start of the
project requires one of them, the Project Advisor may take it provisionally (🟡 in the
register) and the holder confirms or reverses it once named.

## 2. Actions that need a go-ahead

A go-ahead is a written, explicit message from the person in the right-hand column. It
covers **one** action, not the next ones of the same kind.

| Action | Go-ahead from |
|---|---|
| Promote to the rehearsal environment (environments and promotion path record) | project lead |
| Promote to production | product owner, once the project lead confirms the gates are green |
| Create, resize or delete cloud resources | product owner (the client's budget) |
| Change a database schema in the rehearsal environment or production | project lead, and product owner for destructive steps |
| A new flow of personal data (source, store, export) | data protection contact |
| Spend above the monthly budget line (the client's keys, cloud) | product owner |
| Spend on the Project Advisor's own AI keys or licences | Project Advisor |
| Change the Claude kits or the generative-AI method | Project Advisor |
| Push to a branch that deploys | the person responsible for that environment |

## 3. How a go-ahead is recorded

The decision it executes is in a register (PD, DEC or DD) with its date and author; the
action itself is in the session journal with the command that performed it and the
measurement that confirms it.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

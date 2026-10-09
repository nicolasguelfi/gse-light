---
name: decision-record
description: Record a decision or open question of the project in the right register (PD, DEC or DD) in the standard format, and update the register's dashboard with who decides. Use whenever a choice appears, a question awaits a decision, or a pending decision is settled.
---

# Record a decision

The project keeps every decision and open question in one of three registers, all in
`project/` of the project's repository — this repository. Paths below are relative to its
root; the method is `../gse-light`:

| Kind | Register | Prefix |
|---|---|---|
| Organisation, people, budget, collaboration tools | `project/governance/05-project-decisions.md` | `PD-NN` |
| What the product must do | `project/requirements/05-decisions.md` | `DEC-NNN` |
| How the product is built and run | `project/design/05-design-decisions.md` | `DD-NN` |

## Steps

1. **Search first.** Grep the three registers for the topic. If a record exists, amend
   it (add an "Amended YYYY-MM-DD" line) rather than creating a duplicate. If the
   question is already decided, say so and cite the record — do not reopen it unless
   asked.
2. **Pick the next number** in the chosen register.
3. **Drivers** (design records, and any record where a technology or a vendor is an
   option): cite the lines of `project/design/10-design-drivers.md` the
   decision rests on (section and fact), and name the driver next to each option. No
   driver page yet, or no line for this choice: say so and run the `design-phase` skill
   (or add the missing driver row) before writing the options. **Never propose an
   illustration project's stack (Sumvadis, StreamTeX) as a default**: the method cites
   them to show how a choice played out, not to set this project's answer.
4. **Write the record** from `../gse-light/templates/decision-record.md`: problem in plain words,
   what to consult, every reasonable option with advantages and drawbacks, one
   recommendation with its reason, status badge.
5. **Update the §0 dashboard** of the register: a row under 🔴 Pending (with the
   "Who decides" column, from `project/governance/10-roles-and-go-aheads.md`) or 🟢 Decided,
   with an anchor link to the record.
6. **Mark a decision 🟢 only on an explicit decision** by the person who holds that
   right (`project/governance/10-roles-and-go-aheads.md`). Write who and when in the outcome.
   The Project Advisor's advice is not a decision; a provisional decision he takes before the
   holder is named is 🟡.
7. If the decision awaits the Project Advisor (his method, his kit, his approval, advice the team
   asked for), add or update a task in `project/BRIEFING.md` §1; if it awaits the project lead,
   the product owner or the data protection contact, §1b — **the Project Advisor's sessions
   only**: the cockpit is his, and the kit's settings deny the Edit tool on it; any other
   session reports what §1 or §1b should say in its journal entry instead.
8. Run the documentation gates: `python3 ../gse-light/scripts/check_docs.py`. Then, when
   the record is **new and 🔴**: `git add project/<register>`, `git commit -m "<XX-NN>
   opened"` — that path only. A push is a state-changing action: push only on the explicit
   go-ahead of the person you work for (the kit's settings make Claude ask before any
   `git push`); the Project Advisor's sessions push on his word only. A decided (🟢) record
   is committed only by a session of its decider, an amendment only by a session of its
   author or of the Advisor (roles record); `BRIEFING.md` only by the Advisor's sessions.

Never write "open questions" inside another document: link to the record instead.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

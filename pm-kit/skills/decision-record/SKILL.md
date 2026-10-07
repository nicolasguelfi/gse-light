---
name: decision-record
description: Record a decision or open question of the active instance in the right register (PD, DEC or DD) in the standard format, and update the register's dashboard with who decides. Use whenever a choice appears, a question awaits a decision, or a pending decision is settled.
---

# Record a decision

Each instance keeps every decision and open question in one of three registers, all in the
project-management repository — the private repository that holds `instances/<instance>/`
(this repository if it has an `instances/` folder; from a product repository, the sibling
folder named in its `CLAUDE.md`; if absent, draft the record in your answer and ask the
engineer to open a pull request there). Paths below are relative to it; the method is `../gse-light`:

| Kind | Register | Prefix |
|---|---|---|
| Organisation, people, budget, collaboration tools | `instances/<instance>/governance/05-project-decisions.md` | `PD-NN` |
| What the product must do | `instances/<instance>/requirements/05-decisions.md` | `DEC-NNN` |
| How the product is built and run | `instances/<instance>/design/05-design-decisions.md` | `DD-NN` |

## Steps

1. **Search first.** Grep the three registers for the topic. If a record exists, amend
   it (add an "Amended YYYY-MM-DD" line) rather than creating a duplicate. If the
   question is already decided, say so and cite the record — do not reopen it unless
   asked.
2. **Pick the next number** in the chosen register.
3. **Write the record** from `../gse-light/templates/decision-record.md`: problem in plain words,
   what to consult, every reasonable option with advantages and drawbacks, one
   recommendation with its reason, status badge.
4. **Update the §0 dashboard** of the register: a row under 🔴 Pending (with the
   "Who decides" column, from `instances/<instance>/governance/10-roles-and-go-aheads.md`) or 🟢 Decided,
   with an anchor link to the record.
5. **Mark a decision 🟢 only on an explicit decision** by the person who holds that
   right (`instances/<instance>/governance/10-roles-and-go-aheads.md`). Write who and when in the outcome.
   The Project Advisor's advice is not a decision; a provisional decision he takes before the
   holder is named is 🟡.
6. If the decision awaits the Project Advisor (his method, his kit, his approval, advice the team
   asked for), add or update a task in `instances/<instance>/BRIEFING.md` §1; if it awaits the project lead,
   the product owner or the data protection contact, §1b.
7. Run `python3 ../gse-light/scripts/check_docs.py` in the project-management repository.

Never write "open questions" inside another document: link to the record instead.

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

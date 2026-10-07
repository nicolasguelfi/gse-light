---
name: session-close
description: Close a working session (method or active instance) - write the dated journal entry and the metrics row, refresh the cockpit, and leave a hand-over a session with no memory can resume from. Use when the user says the session ends, before a context handover, or after a significant unit of work.
---

# Close a session

The journal lives in the project-management repository, `instances/<instance>/journal/` (from a
product repository: the sibling folder named in its `CLAUDE.md`). Paths below are relative to
that repository; the method is `../gse-light`.

## Steps

1. **Number the session**: the next `sNN` after the highest existing entry in
   `instances/<instance>/journal/`.
2. **Write `instances/<instance>/journal/YYYY-MM-DD-sNN.md`** from `../gse-light/templates/session-journal.md`:
   - each action with the command that **measured** its result (not "deployed", but
     "deployed — `curl …/version` → 1.4.2");
   - decisions created, decided or amended, by identifier;
   - what was not done, and why;
   - a hand-over for a reader with no memory: state, rules learned, traps.
3. **Append one row to `instances/<instance>/journal/metrics.csv`** (columns in `instances/<instance>/journal/README.md`).
4. **Refresh `instances/<instance>/BRIEFING.md`** with the `cockpit-update` skill if it is available,
   otherwise by hand: §1 what awaits the Project Advisor, §1b what awaits the team, §2 delta
   since the last acknowledgement, new acknowledgement date. Only the Project Advisor's sessions
   edit `instances/<instance>/BRIEFING.md` (roles record); a session of the project lead reports what §1b should
   say in its journal entry instead.
5. **Never edit an earlier journal entry.** A correction is a new entry citing it.
6. Run `python3 ../gse-light/scripts/check_docs.py` there, then commit (do not push unless asked).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

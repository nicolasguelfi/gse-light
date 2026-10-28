---
name: session-close
description: Close a working session (method or project) - write the dated journal entry and the metrics row, refresh the cockpit, and leave a hand-over a session with no memory can resume from. Use when the user says the session ends, before a context handover, or after a significant unit of work.
---

# Close a session

The journal lives in `project/journal/` of the project's repository — this repository,
whoever opened the session. Paths below are relative to its root; the method is `../gse-light`.

## Steps

1. **Number the session**: one counter per person. The Project Advisor's entries are
   `YYYY-MM-DD-sNN.md`; every other author's are `YYYY-MM-DD-<initials>-sNN.md` (two or
   three lowercase letters), `sNN` being the next number after that author's highest
   existing entry — so two people closing on the same day never collide.
2. **Write the entry** at that path from `../gse-light/templates/session-journal.md`:
   - each action with the command that **measured** its result (not "deployed", but
     "deployed — `curl …/version` → 1.4.2");
   - decisions created, decided or amended, by identifier;
   - what was not done, and why;
   - a hand-over for a reader with no memory: state, rules learned, traps.
3. **Append one row to `project/journal/metrics.csv`** (columns in `project/journal/README.md`).
4. **Who closes?** Only the Project Advisor's sessions edit `project/BRIEFING.md` (roles
   record; the team's rules, `.claude/roles/team.json`, deny the Edit tool on it, his own
   `settings.local.json` allows it). A session of the project lead or of a developer **never touches it**: it reports what
   §1 or §1b should say
   in its journal entry, under "For the next session", and stops here for the cockpit.
   The Project Advisor's session **refreshes `project/BRIEFING.md`** with the
   `cockpit-update` skill if it is available, otherwise by hand: §1 what awaits the
   Project Advisor, §1b what awaits the team, §2 the delta since the last acknowledgement
   as dated bullets (the session writes its own date on each bullet it adds), §3 the
   counted state. "Last acknowledgement" is re-stamped **only when the Project Advisor has
   read and acknowledged** the cockpit; otherwise its date stays and §2 keeps accumulating.
5. **Never edit an earlier journal entry.** A correction is a new entry citing it.
5b. **Catch-up of missed closes** ("session-close catch-up", or when the start hook printed
   "Journal: N day(s) with commits and no session-close entry"). Run
   `python3 ../gse-light/scripts/journal_gaps.py` for the list. For **each** missing day, one entry
   dated that day (step 1's name, the next `sNN` in order), written from what git shows of that day
   only — `git log --all --author="<name>" --since=<day> --until=<day+1> --stat`, the pull requests
   and tickets touched (`gh pr list --author @me --search "updated:<day>"`). Its first line reads
   **"Reconstructed on YYYY-MM-DD from git; not written at the time."**; it states what was done,
   with the commits as measures, and writes "unknown" for what git cannot tell (decisions taken
   orally, what was tried and dropped, the hand-over). Never invent; never merge two days into one
   entry. Show the entries to the person, who corrects them, then one metrics row each (step 3) and
   step 6. Entries listed as "not on main yet" need their pull request, not a new entry.
6. **Check, commit, then the go-ahead.** `python3 ../gse-light/scripts/check_docs.py`.
   **Commit only those paths**: `git add project/journal/YYYY-MM-DD-sNN.md
   project/journal/metrics.csv` (plus a new 🔴 record opened in the session),
   `git commit -m "journal sNN"`. A push is a state-changing action: push only on the
   explicit go-ahead of the person you work for — the kit's settings make Claude ask before
   any `git push`; a developer or the project lead answers for their own entry, the Project
   Advisor's sessions push on his word only. If the push is refused because the branch
   moved, pull, re-read what changed, merge, push again — never force.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

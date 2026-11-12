---
name: merge-check
description: Before merging a pull request of the project's repository - gather the critical findings of its AI reviews (change-reviewer; adversarial-reviewer on a critical pull request), of ux-reviewer when a screen changed, and the evidence check, show them to the person merging as a review board (one tick per critical point, a comment on each), record the ticks on the pull request, then merge. Use whenever someone asks to merge, approve or "accept" a pull request.
---

# Merge check — the person ticks the critical points, then merges

The AI reviews produce more findings than a person can read before each merge. The method keeps
the human in the loop **where it matters**: the critical findings only, each ticked by the person
who merges (the method's owner, 2026-10-28). Who may merge is the project's rule (roles record;
the project lead by default).

**Short path** (the method's owner, 2026-11-09, after a week where 73 of 105 merged pull requests
held no code, test or data): a pull request whose **every file** is under `project/journal/`, `project/meetings/` (minutes, boards, decks), `project/BRIEFING.md` or `project/planning/` — the project's record, the one list the
kit uses (`CLAUDE.md`, the pull-request template) — needs no AI review, no board and no "Critical
points ticked" line. Its author merges once `check_docs` (the CI `review` check) is green. Any other
file — code, `project/requirements/`, `project/governance/` (registers, roles record,
`critical-paths.txt`), models, `.claude/` — puts the whole pull request outside the short path. Check it with step 1's file list; outside it, follow the steps below.

## Steps

1. **The pull request's number**, and its state: `gh pr view <n> --json title,state,mergeable,statusCheckRollup,labels`.
   A red gate stops here: never propose a merge with a red gate. A missing `gates` check is never read as
   green: list the files (`gh pr view <n> --json files -q '.files[].path'`) and accept it only when
   every path is in `gates.yml`'s `paths-ignore` (the project's record — meetings, journal, cockpit,
   governance, planning — or `.claude/`); its `review` check (documentation, size, evidence) must then
   be green. Any other change — the requirements included — needs its green `gates`; a `gates`
   skipped on a pull request ready for review, or absent for another reason (a billing stop, more than
   300 files changed), stops the merge.
2. **The AI reviews.** Every pull request outside the short path carries `change-reviewer`; a
   **critical** one (label `critical`, or a file of `project/governance/critical-paths.txt`, the kit's
   default list while it is missing) also
   carries `adversarial-reviewer`, given the number only (the method's owner, 2026-11-09: the real
   critical findings of a week came from sensitive code). Find them in the pull request (ticked
   lines, comments); one is missing: run it now and post its report as a comment. A pull request that changes a screen also carries the
   `ux-reviewer` review (skill `ui-design`): missing, run it with the screen sheet's path.
3. **The evidence check**: `python3 ../gse-light/scripts/evidence_check.py <n>`. Quote its line. The labels `critical` and
   `evidence-bypass` exist once in the repository (`gh label create critical`, `gh label create evidence-bypass`
   when missing).
4. **Keep the critical findings only**: the findings the reviewers tagged **critical** (`ux-reviewer` included), plus each
   warning of the evidence check. Major and minor findings are listed in one line ("n major, n
   minor: in the reviews"), not asked about.
5. **None critical**: say so in one line and ask the merge go-ahead with one QCM (merge / wait).
6. **One or more**: a review board (skill `review`), one group per critical point — the finding in
   plain words, the evidence (file, line, the reviewer's scenario), and three proposals:
   **fixed** (the commit that fixes it), **answered** (why it is not a defect: a decision record, a
   test), **accepted risk** (who accepts it, and until when). A comment field on each, a global one.
7. **The line comes back.** Post it on the pull request as a comment, prefixed
   "Critical points ticked before merge:", so the trace stays on GitHub. Any point left unticked,
   or ticked "fixed" without its commit: no merge.
8. **Merge** on the person's go-ahead only (`gh pr merge <n> --merge`, or the project's way), never
   a forced or admin merge. Then the journal entry of the session names the pull request and the line.

## Never

Tick for the person; merge without the line; hide a critical finding behind "minor"; merge to a
branch that deploys without the go-ahead of that promotion.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

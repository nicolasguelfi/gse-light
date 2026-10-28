---
name: merge-check
description: Before merging a pull request of the project's repository - gather the critical findings of its two AI reviews (change-reviewer, adversarial-reviewer) and the evidence check, show them to the person merging as a review board (one tick per critical point, a comment on each), record the ticks on the pull request, then merge. Use whenever someone asks to merge, approve or "accept" a pull request.
---

# Merge check — the person ticks the critical points, then merges

The AI reviews produce more findings than a person can read before each merge. The method keeps
the human in the loop **where it matters**: the critical findings only, each ticked by the person
who merges (the method's owner, 2026-10-28). Who may merge is the project's rule (roles record;
the project lead by default).

## Steps

1. **The pull request's number**, and its state: `gh pr view <n> --json title,state,mergeable,statusCheckRollup,labels`.
   A red gate stops here: never propose a merge with a red gate.
2. **The two AI reviews.** Find them in the pull request (ticked lines, comments). One is missing:
   run it now — `change-reviewer` on the diff, then `adversarial-reviewer` with the number only —
   and post its report as a comment.
3. **The evidence check**: `python3 ../gse-light/scripts/evidence_check.py <n>`. Quote its line.
4. **Keep the critical findings only**: the findings the reviewers tagged **critical**, plus each
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

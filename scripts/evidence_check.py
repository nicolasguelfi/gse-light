#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Evidence check of a critical pull request (review on evidence, reference design ch. 8): a warning,
never a block, and a bypass by hand.

  python3 ../gse-light/scripts/evidence_check.py <pull request number>     # needs `gh`, signed in

**Critical** when the pull request carries the label `critical`, or when one of its files matches a
line of `project/governance/critical-paths.txt` (one glob per line, `#` for comments; the project
lead keeps that list). Without the file, the kit's defaults below apply. Only critical pull requests
are checked — the others are too many to review this way (the method's owner, 2026-10-28).

**Evidence** looked for in the pull request's text and comments:
  1. the two AI reviews: `change-reviewer` and `adversarial-reviewer`, each on a ticked line (`- [x]`)
     or in a comment that gives its verdict (`Verdict: ready`, `no break found`…);
  2. tests: when code changed, at least one test file changed too.

**Bypass by hand**: the label `evidence-bypass`, or a line `Evidence bypass: <reason>` in the text or
a comment. The check then prints the reason and nothing else.

Prints one line per missing piece of evidence (as a GitHub Actions `::warning::` when it runs in CI).
Exit code 0 always: the person merging decides.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CRITICAL = [
    "**/migrations/**", "**/*.sql", "**/*auth*", "**/*secret*", "**/*password*",
    ".github/workflows/*", ".claude/settings.json", "**/Dockerfile", "**/*deploy*",
]
CODE = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".sql", ".sh", ".go", ".java", ".kt", ".rb", ".rs", ".cs", ".php", ".vue", ".svelte"}
TEST = re.compile(r"(^|/)(tests?|e2e|__tests__|spec)/|(^|/)test_[^/]*\.py$|_test\.(py|go)$|\.(test|spec)\.[jt]sx?$")
BYPASS = re.compile(r"^[ \t]*Evidence bypass:[ \t]*(\S.*)$", re.M | re.I)
VERDICT = re.compile(r"\bverdict\b\W{0,5}(ready|not ready|no break found|breaks found|held|broke|could not)", re.I)
REVIEWERS = ("change-reviewer", "adversarial-reviewer")


def patterns(repo: Path) -> list[str]:
    path = repo / "project" / "governance" / "critical-paths.txt"
    if not path.exists():
        return DEFAULT_CRITICAL
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.lstrip().startswith("#")]


def matches(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch(path, g.replace("**/", "")) for g in globs)


def reviewed(name: str, body: str, comments: list[str]) -> bool:
    ticked = any(name in line and re.match(r"^\s*[-*]\s*\[[xX]\]", line) for line in body.splitlines())
    in_comment = any(name in c and VERDICT.search(c) for c in comments)
    return ticked or in_comment


def check(pr: dict, globs: list[str]) -> tuple[bool, str, list[str]]:
    """(critical?, bypass reason or "", missing evidence) for a pull request as `gh pr view --json` gives it."""
    files = [f["path"] for f in pr.get("files", [])]
    labels = {l["name"] for l in pr.get("labels", [])}
    body = pr.get("body") or ""
    comments = [c.get("body") or "" for c in pr.get("comments", [])]
    critical = "critical" in labels or any(matches(f, globs) for f in files)
    if not critical:
        return False, "", []
    m = BYPASS.search("\n".join([body, *comments]))
    if "evidence-bypass" in labels or m:
        return True, (m.group(1).strip() if m else "label evidence-bypass"), []
    missing = [f"no {name} review found (a ticked line in the pull request, or a comment with its verdict)"
               for name in REVIEWERS if not reviewed(name, body, comments)]
    code = [f for f in files if Path(f).suffix in CODE and not TEST.search(f)]
    tests = [f for f in files if TEST.search(f)]
    if code and not tests:
        missing.append(f"{len(code)} code file(s) changed and no test file")
    return True, "", missing


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    repo = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
    ci = bool(os.environ.get("GITHUB_ACTIONS"))
    try:
        out = subprocess.run(["gh", "pr", "view", sys.argv[1], "--json", "files,labels,body,comments,number"],
                             cwd=repo, capture_output=True, text=True, timeout=60, check=True).stdout
        pr = json.loads(out)
    except Exception as e:  # noqa: BLE001 — a warning tool never fails the run
        print(f"{'::warning::' if ci else 'WARN '}evidence_check: could not read pull request {sys.argv[1]} ({e}): the check did not run")
        return 0
    critical, bypass, missing = check(pr, patterns(repo))
    n = pr.get("number", sys.argv[1])
    if not critical:
        print(f"evidence_check: #{n} is not critical (no label `critical`, no file in the critical paths): nothing to check.")
    elif bypass:
        print(f"evidence_check: #{n} is critical; evidence check bypassed by hand: {bypass}")
    elif missing:
        for m in missing:
            print(f"::warning::evidence #{n} (critical): {m}" if ci else f"WARN evidence #{n} (critical): {m}")
        print("evidence_check: a warning, not a block. Add the evidence, or bypass by hand: label `evidence-bypass` "
              "or a line `Evidence bypass: <reason>`.")
    else:
        print(f"evidence_check: #{n} is critical and carries its evidence (two AI reviews, tests).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

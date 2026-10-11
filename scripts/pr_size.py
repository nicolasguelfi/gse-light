#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""How big is this change? The size check of the review on evidence (reference design ch. 8).

Read-only. Run from the root of the project's repository, on the branch of the pull request:

  python3 ../gse-light/scripts/pr_size.py                    # against origin/main
  python3 ../gse-light/scripts/pr_size.py --base origin/dev  # another base branch
  python3 ../gse-light/scripts/pr_size.py --json

It counts the lines changed (added + removed) between the base and HEAD, from the point where the
branch left the base, in three parts:
  code   — what a reviewer must judge;
  tests  — a path with a folder or file named test/tests/spec/e2e, or a name like test_*, *_test.*, *.spec.*, *.test.*;
  other  — documentation and the method's files: *.md, project/, .claude/, .github/, lock files, and the
           "exclude" globs of the threshold file.
The threshold is the project lead's (set in W1): project/governance/pr-size.json,
  {"max_code_lines": 400, "exclude": ["migrations/*.sql"]}
Only "code" counts against it; tests never make a pull request too big. Without that file the
script reports and passes. Exit 1 when "code" exceeds the threshold: split the change (one pull
request = one ticket and one use case), or the project lead raises the threshold in that file.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

THRESHOLD_FILE = Path("project/governance/pr-size.json")
OTHER_GLOBS = ["*.md", "project/*", ".claude/*", ".github/*", "*.lock", "package-lock.json",
               "pnpm-lock.yaml", "yarn.lock", "uv.lock", "poetry.lock", "Cargo.lock", "go.sum"]
TEST_RE = re.compile(r"(^|/)(tests?|spec|e2e)(/|$)|(^|/)test_[^/]*$|_test\.[^/]+$|\.(spec|test)\.[^/]+$")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def kind(path: str, exclude: list[str]) -> str:
    if any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch(Path(path).name, g) for g in OTHER_GLOBS + exclude):
        return "other"
    return "tests" if TEST_RE.search(path) else "code"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default="origin/main", help="the branch the pull request goes to (default origin/main)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    conf: dict = {}
    if THRESHOLD_FILE.exists():
        conf = json.loads(THRESHOLD_FILE.read_text(encoding="utf-8"))
    limit = conf.get("max_code_lines")
    exclude = list(conf.get("exclude", []))

    try:
        base = git("merge-base", a.base, "HEAD").strip()
    except subprocess.CalledProcessError:
        print(f"pr_size: base {a.base} not found (git fetch first)", file=sys.stderr)
        return 2
    totals = {"code": 0, "tests": 0, "other": 0}
    files: list[dict] = []
    for line in git("diff", "--numstat", f"{base}..HEAD").splitlines():
        added, removed, path = line.split("\t", 2)
        n = 0 if added == "-" else int(added) + int(removed)  # "-": a binary file
        k = kind(path, exclude)
        totals[k] += n
        files.append({"path": path, "lines": n, "kind": k})

    over = limit is not None and totals["code"] > int(limit)
    if a.json:
        print(json.dumps({"base": a.base, "totals": totals, "max_code_lines": limit, "over": over, "files": files}, indent=1))
    else:
        print(f"pr_size: {totals['code']} lines of code, {totals['tests']} of tests, {totals['other']} other "
              f"({len(files)} files, against {a.base})")
        for f in sorted(files, key=lambda f: -f["lines"])[:5]:
            if f["lines"]:
                print(f"  {f['lines']:6d}  {f['kind']:5s}  {f['path']}")
        if limit is None:
            print(f"pr_size: no threshold yet ({THRESHOLD_FILE} — the project lead sets it in W1): reported, not checked")
        elif over:
            print(f"pr_size: TOO BIG — {totals['code']} lines of code > {limit}: split the change (one pull request = "
                  f"one ticket and one use case), or the project lead raises max_code_lines in {THRESHOLD_FILE}")
        else:
            print(f"pr_size: ok ({totals['code']} ≤ {limit})")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())

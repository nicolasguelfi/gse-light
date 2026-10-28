#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Requirements coverage: which functional and non-functional requirement has a test, and which
functional requirement has an end-to-end test through the real user interface.

  python3 ../gse-light/scripts/req_coverage.py [repository root]

Coverage of the code (lines run by the tests) says nothing about the requirements: a requirement
with no test is unproven whatever the percentage (the method's owner, 2026-10-28). This script reads:

  - the requirements: every heading `## <ID> — <title>` of `project/requirements/20-functional/`
    (functional) and of `project/requirements/30-non-functional*` (a file or a folder: non-functional);
    an identifier is upper-case words and a number joined by hyphens (`FR-CQ-001`, `NFR-PERF-002`);
  - the tests: every test file of the repository (`tests/`, `test_*.py`, `*.test.ts`, `e2e/`…),
    searched for the identifiers; a test file under an `e2e/` folder is an end-to-end test.

It reports the requirements with no test, by kind, the functional ones with no end-to-end test, and
"no non-functional requirement written" when there is none. Exit code 0 always (a report; check_docs
shows its summary as warnings). The project's own gate may be stricter (a map that fails on a test
without an identifier). Limit: an identifier named anywhere in a test file counts, a sample identifier
in a test of a tool included; the project's own map, which reads each test's marker, is the reference.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^#{2,3}\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{2,})\b", re.M)
TEST = re.compile(r"(^|/)(tests?|e2e|__tests__|spec)/|(^|/)test_[^/]*\.py$|_test\.(py|go)$|\.(test|spec)\.[jt]sx?$")
E2E = re.compile(r"(^|/)e2e/")
SKIP = {"node_modules", ".venv", "venv", "build", "dist", ".git", "__pycache__", ".claude", "project"}
SUFFIX = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".java", ".kt", ".rb", ".rs", ".cs", ".php"}


def requirements(root: Path) -> dict[str, str]:
    """{identifier: "functional" | "non-functional"} from the requirement headings."""
    req = root / "project" / "requirements"
    found: dict[str, str] = {}
    for path in sorted((req / "20-functional").glob("**/*.md")) if (req / "20-functional").is_dir() else []:
        for rid in HEADING.findall(path.read_text(encoding="utf-8")):
            found[rid] = "functional"
    for base in sorted(req.glob("30-non-functional*")):
        for path in ([base] if base.is_file() else sorted(base.glob("**/*.md"))):
            for rid in HEADING.findall(path.read_text(encoding="utf-8")):
                found[rid] = "non-functional"
    return found


def test_files(root: Path) -> list[Path]:
    out = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if SKIP.intersection(rel.parts) or not path.is_file() or path.suffix not in SUFFIX:
            continue
        if TEST.search(rel.as_posix()):
            out.append(path)
    return out


def coverage(root: Path) -> dict:
    reqs = requirements(root)
    tested, e2e = set(), set()
    if reqs:
        ids = re.compile(r"\b(" + "|".join(re.escape(r) for r in sorted(reqs, key=len, reverse=True)) + r")\b")
        for path in test_files(root):
            try:
                hits = set(ids.findall(path.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
            tested |= hits
            if E2E.search(path.relative_to(root).as_posix()):
                e2e |= hits
    fr = sorted(r for r, k in reqs.items() if k == "functional")
    nfr = sorted(r for r, k in reqs.items() if k == "non-functional")
    return {
        "functional": fr, "non_functional": nfr,
        "fr_untested": [r for r in fr if r not in tested],
        "nfr_untested": [r for r in nfr if r not in tested],
        "fr_no_e2e": [r for r in fr if r not in e2e],
    }


def summary(c: dict) -> list[str]:
    """Short lines for check_docs (WARN) and for the console."""
    def few(ids: list[str]) -> str:
        return ", ".join(ids[:8]) + (" …" if len(ids) > 8 else "")
    lines = []
    fr, nfr = c["functional"], c["non_functional"]
    if not fr and not nfr:
        return ["requirements coverage: no requirement heading (`## <ID> — …`) under project/requirements/20-functional/ or 30-non-functional"]
    if c["fr_untested"]:
        lines.append(f"requirements coverage: {len(c['fr_untested'])} of {len(fr)} functional requirement(s) with no test: {few(c['fr_untested'])}")
    if not nfr:
        lines.append("requirements coverage: no non-functional requirement written (project/requirements/30-non-functional.md): "
                     "performance, security, availability, accessibility… each with its test")
    elif c["nfr_untested"]:
        lines.append(f"requirements coverage: {len(c['nfr_untested'])} of {len(nfr)} non-functional requirement(s) with no test: {few(c['nfr_untested'])}")
    if fr and c["fr_no_e2e"]:
        lines.append(f"requirements coverage: {len(c['fr_no_e2e'])} of {len(fr)} functional requirement(s) with no end-to-end test (e2e/): {few(c['fr_no_e2e'])}")
    return lines


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ".").resolve()
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    c = coverage(root)
    lines = summary(c)
    n_fr, n_nfr = len(c["functional"]), len(c["non_functional"])
    print(f"requirements coverage ({root.name}): {n_fr - len(c['fr_untested'])}/{n_fr} functional tested, "
          f"{n_fr - len(c['fr_no_e2e'])}/{n_fr} with an end-to-end test, {n_nfr - len(c['nfr_untested'])}/{n_nfr} non-functional tested")
    for line in lines:
        print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

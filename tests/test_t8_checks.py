# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Tests of the kit's checks of 2026-10-28: missed session closes, the evidence check of a critical
pull request, the requirements coverage. Run: python3 -m unittest discover -s tests"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import evidence_check as ev  # noqa: E402
import journal_gaps as jg  # noqa: E402
import req_coverage as rc  # noqa: E402

ME = ("ana", "ana@example.org")


class JournalGaps(unittest.TestCase):
    def test_active_days_match_name_or_email(self):
        log = "Ana\tana@example.org\t2026-10-20\nAna\tother@example.org\t2026-10-21\nBen\tben@example.org\t2026-10-22\n"
        self.assertEqual(jg.active_days(log, ME), {"2026-10-20", "2026-10-21"})

    def test_own_entries_only_journal_files_of_the_author(self):
        log = ("@@Ana\tana@example.org\nproject/journal/2026-10-20-an-s01.md\ncore/x.py\n"
               "@@Ben\tben@example.org\nproject/journal/2026-10-21-be-s01.md\n"
               "@@Ana\tana@example.org\nproject/journal/README.md\nproject/journal/2026-10-22-s03.md\n")
        self.assertEqual(jg.own_entries(log, ME, "project/journal"), {"2026-10-20-an-s01.md", "2026-10-22-s03.md"})

    def test_gaps_exclude_covered_days_and_today(self):
        self.assertEqual(jg.gaps({"2026-10-20", "2026-10-21", "2026-10-28"}, {"2026-10-20-an-s01.md"}, "2026-10-28"),
                         ["2026-10-21"])

    def test_report_on_a_real_repository(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            def run(*a, date="2026-10-20T10:00:00"):
                env = {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date, "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
                subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, env=env)
            run("init", "-q", "-b", "main")
            run("config", "user.name", "Ana"); run("config", "user.email", "ana@example.org")
            (repo / "project/journal").mkdir(parents=True)
            (repo / "a.txt").write_text("1"); run("add", "a.txt"); run("commit", "-qm", "work 20", date="2026-10-20T10:00:00")
            (repo / "project/journal/2026-10-20-an-s01.md").write_text("x")
            run("add", "."); run("commit", "-qm", "journal", date="2026-10-20T18:00:00")
            (repo / "a.txt").write_text("2"); run("add", "a.txt"); run("commit", "-qm", "work 22", date="2026-10-22T10:00:00")
            import datetime as dt
            lines = jg.report(repo, days=14, today=dt.date(2026, 10, 28))
            self.assertTrue(lines and "2026-10-22" in lines[0] and "2026-10-20" not in lines[0], lines)


class EvidenceCheck(unittest.TestCase):
    BODY = "- [x] **`change-reviewer`**: ready\n- [x] **`adversarial-reviewer`**: no break found\n"

    def pr(self, files, body="", labels=(), comments=()):
        return {"files": [{"path": f} for f in files], "body": body,
                "labels": [{"name": l} for l in labels], "comments": [{"body": c} for c in comments]}

    def test_not_critical_is_not_checked(self):
        self.assertEqual(ev.check(self.pr(["docs/a.md"]), ev.DEFAULT_CRITICAL), (False, "", []))

    def test_critical_path_without_evidence_warns_three_times(self):
        crit, bypass, missing = ev.check(self.pr(["core/migrations/001.sql", "core/load.py"]), ev.DEFAULT_CRITICAL)
        self.assertTrue(crit); self.assertEqual(bypass, ""); self.assertEqual(len(missing), 3)

    def test_label_critical_with_evidence_passes(self):
        crit, _, missing = ev.check(self.pr(["core/x.py", "core/tests/test_x.py"], self.BODY, ["critical"]), [])
        self.assertTrue(crit); self.assertEqual(missing, [])

    def test_review_in_a_comment_counts(self):
        _, _, missing = ev.check(self.pr(["core/tests/test_x.py"], "", ["critical"],
                                         ["change-reviewer: Verdict: ready", "adversarial-reviewer — Verdict: no break found"]), [])
        self.assertEqual(missing, [])

    def test_bypass_by_line_or_label(self):
        _, bypass, missing = ev.check(self.pr(["x.sql"], "Evidence bypass: hotfix, reviews tomorrow", ["critical"]), [])
        self.assertEqual((bypass, missing), ("hotfix, reviews tomorrow", []))
        _, bypass, _ = ev.check(self.pr(["x.sql"], "", ["critical", "evidence-bypass"]), [])
        self.assertEqual(bypass, "label evidence-bypass")

    def test_empty_bypass_line_does_not_borrow_the_next_line(self):
        _, bypass, missing = ev.check(self.pr(["x.md"], "Evidence bypass:\n- [ ] change-reviewer", ["critical"]), [])
        self.assertEqual(bypass, ""); self.assertEqual(len(missing), 2)

    def test_a_comment_without_a_verdict_is_not_a_review(self):
        _, _, missing = ev.check(self.pr(["x.md"], "", ["critical"], ["change-reviewer and adversarial-reviewer: no verdict yet"]), [])
        self.assertEqual(len(missing), 2)

    def test_project_list_replaces_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "project/governance").mkdir(parents=True)
            (Path(d) / "project/governance/critical-paths.txt").write_text("# ours\nweb/src/login/*\n")
            self.assertEqual(ev.patterns(Path(d)), ["web/src/login/*"])


class RequirementsCoverage(unittest.TestCase):
    def make(self, nfr: bool):
        d = tempfile.TemporaryDirectory()
        root = Path(d.name)
        (root / "project/requirements/20-functional").mkdir(parents=True)
        (root / "project/requirements/20-functional/a.md").write_text("## FR-AB-001 — one\n\n## FR-AB-002 — two\n")
        if nfr:
            (root / "project/requirements/30-non-functional.md").write_text("## NFR-PERF-001 — fast\n")
        (root / "core/tests").mkdir(parents=True)
        (root / "core/tests/test_a.py").write_text("# FR-AB-001\n# NFR-PERF-001\n")
        (root / "web/e2e").mkdir(parents=True)
        (root / "web/e2e/a.spec.ts").write_text('test("[FR-AB-002] path", () => {})\n')
        return d, root

    def test_functional_non_functional_and_end_to_end(self):
        d, root = self.make(nfr=True)
        with d:
            c = rc.coverage(root)
            self.assertEqual((c["fr_untested"], c["nfr_untested"], c["fr_no_e2e"]), ([], [], ["FR-AB-001"]))
            self.assertEqual(len(rc.summary(c)), 1)

    def test_no_non_functional_requirement_is_reported(self):
        d, root = self.make(nfr=False)
        with d:
            self.assertTrue(any("no non-functional requirement" in l for l in rc.summary(rc.coverage(root))))


if __name__ == "__main__":
    unittest.main()

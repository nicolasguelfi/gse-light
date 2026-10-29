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

    def test_late_commits_after_the_days_entry(self):
        times = {"2026-10-15-s17.md": "2026-10-15T13:01:00+02:00", "2026-10-16-s18.md": "2026-10-16T18:00:00+02:00"}
        log = ("Ana\tana@example.org\t2026-10-15\t2026-10-15T12:00:00+02:00\n"
               "Ana\tana@example.org\t2026-10-15\t2026-10-15T14:55:00+02:00\n"
               "Ana\tana@example.org\t2026-10-15\t2026-10-15T17:03:00+02:00\n"
               "Ana\tana@example.org\t2026-10-16\t2026-10-16T18:40:00+02:00\n"
               "Ben\tben@example.org\t2026-10-16\t2026-10-16T23:00:00+02:00\n")
        # 10-15: two commits after the entry, beyond the hour; 10-16: a fix within the hour, Ben not counted
        self.assertEqual(jg.late_commits(log, times, ME), ["2026-10-15 (2 commit(s))"])

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
            # an entry on a side branch only is "not on main yet"
            run("switch", "-q", "-c", "side")
            (repo / "project/journal/2026-10-22-an-s02.md").write_text("x")
            run("add", "."); run("commit", "-qm", "journal side", date="2026-10-22T18:00:00")
            run("switch", "-q", "main")
            lines = jg.report(repo, days=14, today=dt.date(2026, 10, 28))
            self.assertTrue(any("not on main yet" in l and "2026-10-22-an-s02.md" in l for l in lines), lines)
            # a second identity mapped by .mailmap is the same author
            (repo / ".mailmap").write_text("Ana <ana@example.org> <ana.other@example.org>\n")
            run("config", "user.email", "ana.other@example.org")
            env_commit = ("-c", "user.name=Ana Other")
            (repo / "a.txt").write_text("3"); run("add", "a.txt")
            run(*env_commit, "commit", "-qm", "work 24", date="2026-10-24T10:00:00")
            run("config", "user.email", "ana@example.org")
            lines = jg.report(repo, days=14, today=dt.date(2026, 10, 28))
            self.assertTrue(lines and "2026-10-24" in lines[0], lines)
            # a commit three hours after the entry of 10-20: a possible second session
            (repo / "a.txt").write_text("4"); run("add", "a.txt"); run("commit", "-qm", "evening", date="2026-10-20T21:00:00")
            lines = jg.report(repo, days=14, today=dt.date(2026, 10, 28))
            self.assertTrue(any("more than an hour" in l and "2026-10-20 (1 commit(s))" in l for l in lines), lines)


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

    def test_a_pull_request_changing_the_list_is_critical(self):
        pr = self.pr([".claude/settings.json", "project/governance/critical-paths.txt"])
        self.assertTrue(ev.check(pr, ["none/*"])[0])

    def test_could_not_run_is_not_a_review(self):
        pr = self.pr([".github/workflows/x.yml"], comments=["change-reviewer and adversarial-reviewer not run yet; verdict: could not run"])
        self.assertEqual(len(ev.check(pr, ev.DEFAULT_CRITICAL)[2]), 2)

    def test_one_comment_cannot_stand_for_both_reviewers(self):
        pr = self.pr(["x.md"], labels=["critical"], comments=["change-reviewer and adversarial-reviewer\nVerdict: ready"])
        self.assertEqual(len(ev.check(pr, [])[2]), 2)

    def test_placeholder_or_fenced_bypass_is_no_bypass(self):
        self.assertEqual(ev.check(self.pr(["x.md"], "Evidence bypass: <reason>", ["critical"]), [])[1], "")
        self.assertEqual(ev.check(self.pr(["x.md"], "```\nEvidence bypass: example\n```", ["critical"]), [])[1], "")

    def test_a_ticked_box_on_a_review_not_run_is_no_review(self):
        pr = self.pr(["x.md"], "- [x] change-reviewer not run\n- [x] **`adversarial-reviewer`**: verdict <…>", ["critical"])
        self.assertEqual(len(ev.check(pr, [])[2]), 2)

    def test_root_files_and_gates_are_critical_by_default(self):
        for f in ("Dockerfile", "gates.sh", ".claude/roles/team.json", "web/package.json"):
            self.assertTrue(ev.matches(f, ev.DEFAULT_CRITICAL), f)

    def test_project_list_replaces_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "project/governance").mkdir(parents=True)
            (Path(d) / "project/governance/critical-paths.txt").write_text("# ours\nweb/src/login/*\n")
            self.assertEqual(ev.patterns(Path(d)), ["web/src/login/*"])


class InterfaceEvidence(unittest.TestCase):
    def pr(self, files, body="", comments=()):
        return {"files": [{"path": f} for f in files], "body": body, "comments": [{"body": c} for c in comments], "labels": []}

    def test_no_interface_file_nothing_to_check(self):
        self.assertEqual(ev.ui_check(self.pr(["core/x.py", "project/meetings/a/board.html"]), ev.DEFAULT_UI), (False, []))

    def test_interface_without_sheet_or_review_warns_twice(self):
        is_ui, missing = ev.ui_check(self.pr(["web/ui/src/App.tsx", "web/ui/src/App.test.tsx"]), ev.DEFAULT_UI)
        self.assertTrue(is_ui)
        self.assertEqual(len(missing), 2, missing)

    def test_sheet_file_and_review_comment_pass(self):
        pr = self.pr(["web/ui/src/App.tsx", "project/design/screens/course.md"],
                     comments=["ux-reviewer on the course screen\n\nVerdict: usable after fixes"])
        self.assertEqual(ev.ui_check(pr, ev.DEFAULT_UI), (True, []))

    def test_sheet_line_and_ticked_review_pass_but_not_the_placeholder(self):
        ok = self.pr(["web/ui/src/App.tsx"], body="Screen sheet: project/design/screens/x.md\n- [x] **`ux-reviewer`**: usable")
        self.assertEqual(ev.ui_check(ok, ev.DEFAULT_UI), (True, []))
        placeholder = self.pr(["web/ui/src/App.tsx"], body="Screen sheet: <path>\n- [x] **`ux-reviewer`**: usable")
        self.assertEqual(len(ev.ui_check(placeholder, ev.DEFAULT_UI)[1]), 1)

    def test_not_reviewed_is_no_review_and_the_template_line_counts(self):
        pr = self.pr(["web/ui/src/App.tsx"], body="- [x] **`ux-reviewer`**: verdict not reviewed\n\nScreen sheet: project/design/screens/x.md")
        self.assertEqual(len(ev.ui_check(pr, ev.DEFAULT_UI)[1]), 1)
        template = Path(__file__).resolve().parent.parent / "kit/templates/pull_request_template.md"
        filled = template.read_text(encoding="utf-8").replace("<project/design/screens/….md, when a screen changes; delete otherwise>", "project/design/screens/x.md")
        self.assertEqual(ev.ui_check(self.pr(["web/ui/src/App.tsx"], body=filled), ev.DEFAULT_UI)[1][0].startswith("no ux-reviewer"), True)

    def test_test_files_alone_are_no_interface_change(self):
        self.assertEqual(ev.ui_check(self.pr(["web/ui/src/App.test.tsx"]), ev.DEFAULT_UI), (False, []))

    def test_a_line_naming_two_reviewers_counts_for_neither(self):
        self.assertFalse(ev.reviewed("change-reviewer", "- [x] change-reviewer and ux-reviewer: verdict ready", []))

    def test_a_change_reviewer_line_is_no_ux_review(self):
        pr = self.pr(["web/ui/src/App.tsx", "project/design/screens/x.md"], body="- [x] **`change-reviewer`**: ready")
        self.assertEqual(len(ev.ui_check(pr, ev.DEFAULT_UI)[1]), 1)


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

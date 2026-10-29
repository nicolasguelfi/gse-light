# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Tests of the review board generator: every subject carries its recommendation (2026-10-29).
Run: python3 -m unittest discover -s tests"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "kit/skills/review"))
import review_board as rb  # noqa: E402


def group(key, recommend="p1: ...", flags=(True, False)):
    return {"key": key, "heading": key, "recommend": recommend,
            "items": [{"label": f"p{i + 1}", "title": "t", "recommended": f} for i, f in enumerate(flags)]}


class Recommendations(unittest.TestCase):
    def test_the_example_passes(self):
        self.assertEqual(rb.missing_recommendations(rb.EXAMPLE), [])

    def test_single_choice_needs_exactly_one(self):
        spec = {"mode": "single", "groups": [group("a"), group("b", flags=(False, False)), group("c", flags=(True, True))]}
        self.assertEqual(rb.missing_recommendations(spec), ["b", "c"])

    def test_multi_allows_several(self):
        spec = {"mode": "multi", "groups": [group("a", flags=(True, True)), group("b", flags=(False, False))]}
        self.assertEqual(rb.missing_recommendations(spec), ["b"])

    def test_no_items_is_no_recommendation(self):
        self.assertEqual(rb.missing_recommendations({"groups": [{"key": "a", "recommend": "p1", "items": None}]}), ["a"])

    def test_blank_sentence_or_string_flags_are_no_recommendation(self):
        spec = {"groups": [group("a", recommend="   "), group("b", flags=("false", False)), group("c", flags=("no", False))]}
        self.assertEqual(rb.missing_recommendations(spec), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Missed session closes: the days a person committed without writing a journal entry.

Run by the start hook (`session_start.py`) for whoever opens the session, and on demand:

  python3 ../gse-light/scripts/journal_gaps.py [--days 14] [--author "Name"]

For the git user of the session (`git config user.name` and `user.email`, through `.mailmap` when
the project keeps one, so one person with several git identities is one author), over the last
`--days` days (14 by default) and on every branch:

  - active days: the dates of that person's commits;
  - covered days: the dates of the journal entries that person added (`project/journal/YYYY-MM-DD-…-sNN.md`,
    the date in the name), on any branch;
  - missing days: active days with no entry, today excluded (the session in progress closes it);
  - entries not merged: that person's entries absent from the default branch.

It prints one line per finding and the way to catch up: the `session-close` skill writes one entry
per missing day, rebuilt from git, marked as reconstructed. Read-only; exit code 0 always.
Limit: a second git identity not listed in `.mailmap` is another author — its days are missed,
never invented.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ENTRY = re.compile(r"^(\d{4}-\d{2}-\d{2})-(?:[a-z]{2,3}-)?s\d+\.md$")


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=30)
    return r.stdout if r.returncode == 0 else ""


def identity(repo: Path) -> tuple[str, str]:
    """The session's author, as `.mailmap` maps it (name, email), lower case."""
    name, email = git(repo, "config", "user.name").strip(), git(repo, "config", "user.email").strip()
    mapped = git(repo, "check-mailmap", f"{name} <{email}>").strip() if name and email else ""
    m = re.match(r"^(.*?)\s*<(.*)>$", mapped)
    if m:
        name, email = m.group(1), m.group(2)
    return name.lower(), email.lower()


def is_author(line_name: str, line_email: str, who: tuple[str, str]) -> bool:
    name, email = who
    return bool((name and line_name.lower() == name) or (email and line_email.lower() == email))


def active_days(log: str, who: tuple[str, str]) -> set[str]:
    """Dates of the person's commits, from lines `name<TAB>email<TAB>YYYY-MM-DD`."""
    days = set()
    for line in log.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and is_author(parts[0], parts[1], who):
            days.add(parts[2])
    return days


def own_entries(log: str, who: tuple[str, str], journal: str) -> set[str]:
    """Journal entries (file names) the person added, from `git log --name-only --diff-filter=A`
    blocks: a header line `@@name<TAB>email`, then the paths."""
    entries, mine = set(), False
    for line in log.splitlines():
        if line.startswith("@@"):
            parts = line[2:].split("\t")
            mine = len(parts) == 2 and is_author(parts[0], parts[1], who)
        elif mine and line.startswith(journal + "/"):
            name = line.rsplit("/", 1)[-1]
            if ENTRY.match(name):
                entries.add(name)
    return entries


def gaps(active: set[str], entries: set[str], today: str) -> list[str]:
    covered = {ENTRY.match(e).group(1) for e in entries if ENTRY.match(e)}
    return sorted(d for d in active if d not in covered and d < today)


def default_branch(repo: Path) -> str:
    ref = git(repo, "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD").strip()
    if ref:
        return ref
    for cand in ("origin/main", "main", "origin/master", "master"):
        if git(repo, "rev-parse", "-q", "--verify", cand).strip():
            return cand
    return ""


def report(repo: Path, days: int = 14, today: dt.date | None = None, author: str = "") -> list[str]:
    today = today or dt.date.today()
    journal = "project/journal"
    who = (author.lower(), "") if author else identity(repo)
    if not any(who):
        return []
    since = (today - dt.timedelta(days=days)).isoformat()
    log = git(repo, "log", "--all", "--use-mailmap", f"--since={since}", "--format=%aN%x09%aE%x09%ad", "--date=short")
    added = git(repo, "log", "--all", "--use-mailmap", "--diff-filter=A", "--name-only", "--format=@@%aN%x09%aE", "--", journal)
    entries = own_entries(added, who, journal)
    missing = gaps(active_days(log, who), entries, today.isoformat())
    lines = []
    if missing:
        shown = ", ".join(missing[:10]) + (" …" if len(missing) > 10 else "")
        lines.append(f"Journal: {len(missing)} day(s) with commits and no session-close entry in the last {days} days: {shown}.")
        lines.append("  Catch up: ask Claude \"session-close catch-up\" — one entry per missing day, rebuilt from git, "
                     "marked as reconstructed; you check each one before the commit.")
    branch = default_branch(repo)
    if branch and entries:
        on_main = {p.rsplit("/", 1)[-1] for p in git(repo, "ls-tree", "-r", "--name-only", branch, "--", journal).splitlines()}
        unmerged = sorted(e for e in entries if e not in on_main)
        if unmerged:
            lines.append(f"Journal: {len(unmerged)} entry(ies) of yours not on {branch} yet: {', '.join(unmerged[:5])}"
                         + (" …" if len(unmerged) > 5 else "") + " — open or merge their pull request.")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--author", default="", help="another person's git name (after .mailmap), instead of the session's")
    ap.add_argument("repo", nargs="?", default=".")
    a = ap.parse_args()
    repo = Path(git(Path(a.repo), "rev-parse", "--show-toplevel").strip() or a.repo)
    try:
        lines = report(repo, a.days, author=a.author)
    except Exception as e:  # noqa: BLE001 — read-only helper, never blocks
        lines = [f"journal_gaps: unavailable ({e})"]
    print("\n".join(lines) if lines else "Journal: no missed session close in the last %d days." % a.days)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Documentation gates, for the method (gse-light) and for a project-management repository.
Exit code 1 on any FAIL line; WARN lines never fail the run.

  python3 scripts/check_docs.py                           # in gse-light: the method
  python3 ../gse-light/scripts/check_docs.py              # in a project-management repository (holds instances/)
  python3 ../gse-light/scripts/check_docs.py ../<pm-repo> # from a product repository: the root argument names
                                                          # the repository to check (default: the git toplevel of the current folder)

Checks:
  1. every relative Markdown link points to an existing file, and its #anchor to an existing heading
     (links to https://github.com/nicolasguelfi/gse-light/blob/main/<path> are checked against ../gse-light);
  2. in gse-light: skills present both in pm-kit/skills and claude-kit/skills are identical, and the
     "Who is who" block (between `<!-- who-is-who:start -->` and `<!-- who-is-who:end -->`) is identical
     in every page that carries it (one text, copied into each entry page so that each page reads alone);
  3. in a project-management repository:
     - every register record has a status badge and a dashboard row, and every dashboard row a record;
     - in each instances/<instance>/, the pending counts in BRIEFING.md §3 match its registers' dashboards:
       FAIL when the register holds fewer 🔴 than §3 says (a record closed without the cockpit),
       WARN only when it holds more (new 🔴 opened by the team; the Project Advisor's next session
       refreshes the cockpit) — a developer's commit never turns CI red for that;
     - .claude/skills and .claude/agents are identical to gse-light's pm-kit (else: refresh with pm-kit/install.sh);
     - leak guard: no file tracked in gse-light, and no commit message, matches a line of instances/<instance>/private-terms.txt
       (the terms stay in the private repository; gse-light is public). Limit: the guard knows only the
       terms each instance lists — a built-in generic list of client names would itself name the clients.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

METHOD = Path(__file__).resolve().parent.parent  # gse-light
METHOD_URL = "https://github.com/nicolasguelfi/gse-light/blob/main/"


def repo_root(arg: str | None) -> Path:
    """The repository to check: the root argument (a folder), else the git toplevel of the current folder."""
    if arg:
        root = Path(arg).expanduser().resolve()
        if not root.is_dir():
            sys.exit(f"check_docs: no such folder: {arg}")
        return root
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(r.stdout.strip()).resolve() if r.returncode == 0 else Path.cwd().resolve()


ROOT = repo_root(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None)  # the repository being checked
IS_PM = (ROOT / "instances").is_dir()
REGISTERS = {  # relative to each instance folder instances/<instance>/
    "PD": "governance/05-project-decisions.md",
    "DEC": "requirements/05-decisions.md",
    "DD": "design/05-design-decisions.md",
}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")

errors: list[str] = []    # printed as FAIL; exit code 1
warnings: list[str] = []  # printed as WARN; never fail the run


def strip_code(text: str) -> list[tuple[int, str]]:
    """Lines outside fenced code blocks, with inline code removed, as (line number, text)."""
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            out.append((n, re.sub(r"`[^`]*`", "", line)))
    return out


def slug(heading: str) -> str:
    """GitHub's heading anchor: lowercase, drop punctuation and symbols, spaces to hyphens."""
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # links keep their text
    s = s.replace("`", "").lower()
    s = "".join(c for c in s if c.isalnum() or c in " -_")
    return s.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    result = set()
    for _, line in strip_code(path.read_text(encoding="utf-8")):
        m = HEADING.match(line)
        if not m:
            continue
        base = slug(m.group(2))
        k = seen.get(base, 0)
        result.add(base if k == 0 else f"{base}-{k}")
        seen[base] = k + 1
    return result


def check_links() -> None:
    cache: dict[Path, set[str]] = {}
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        for n, line in strip_code(md.read_text(encoding="utf-8")):
            for target in LINK.findall(line):
                if target.startswith(METHOD_URL) and ROOT != METHOD:  # a link from a PM repository to the method
                    file_part, _, anchor = target[len(METHOD_URL):].partition("#")
                    dest = METHOD / file_part
                elif re.match(r"^[a-z]+:", target):  # other http:, https:, mailto:
                    continue
                else:
                    file_part, _, anchor = target.partition("#")
                    dest = (md.parent / file_part).resolve() if file_part else md
                where = f"{md.relative_to(ROOT)}:{n}"
                if not dest.exists():
                    errors.append(f"{where}: broken link {target}")
                    continue
                if anchor and dest.suffix == ".md":
                    if dest not in cache:
                        cache[dest] = anchors(dest)
                    if anchor not in cache[dest]:
                        errors.append(f"{where}: missing anchor #{anchor} in {dest.name}")


def register_state(prefix: str, path: Path) -> dict[str, str]:
    """Return {record id: status} for one register and check record/dashboard consistency."""
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    records = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(rf"^## ({prefix}-\d+) — ", line)
        if not m:
            continue
        status_line = next((l for l in lines[i + 1:i + 4] if l.strip()), "")
        badge = next((b for b in ("🟢", "🔴", "🟡") if status_line.startswith(b)), None)
        if not badge:
            errors.append(f"{rel}: {m.group(1)} has no status badge on the line after its heading")
        records[m.group(1)] = badge or "?"
    dashboard = text.split("\n---", 1)[0]
    rows = {rid: b for b, rid in re.findall(rf"^\|\s*(🟢|🔴|🟡) \[({prefix}-\d+)\]", dashboard, re.M)}
    for rid, badge in records.items():
        if rid not in rows:
            errors.append(f"{rel}: {rid} missing from the §0 dashboard")
        elif rows[rid] != badge:
            errors.append(f"{rel}: {rid} is {badge} in its record but {rows[rid]} in the dashboard")
    for rid in rows:
        if rid not in records:
            errors.append(f"{rel}: dashboard row {rid} has no record")
    return records


def check_registers() -> None:
    for inst in sorted(p for p in (ROOT / "instances").iterdir() if (p / "BRIEFING.md").exists()):
        name = inst.relative_to(ROOT)
        briefing = (inst / "BRIEFING.md").read_text(encoding="utf-8")
        for prefix, rel in REGISTERS.items():
            path = inst / rel
            if not path.exists():
                errors.append(f"{name}: register {rel} missing")
                continue
            records = register_state(prefix, path)
            pending = sum(1 for b in records.values() if b == "🔴")
            m = re.search(rf"🔴 {prefix} (\d+)", briefing)
            if not m:
                errors.append(f"{name}/BRIEFING.md: §3 has no pending count for {prefix}")
            elif int(m.group(1)) > pending:
                errors.append(f"{name}/BRIEFING.md: §3 says {m.group(1)} pending {prefix}, the register has {pending}")
            elif int(m.group(1)) < pending:  # the team opened a 🔴 record; the cockpit follows at the Advisor's next session
                warnings.append(f"{name}/BRIEFING.md: §3 says {m.group(1)} pending {prefix}, the register has {pending} "
                                "(new 🔴 opened by the team; the Project Advisor's next session refreshes the cockpit)")


def same_tree(src: Path, copy: Path, label: str, hint: str, only_common: bool) -> None:
    """Every file under src has an identical copy under copy (folders absent from copy are
    skipped when only_common)."""
    if not src.is_dir():
        return
    for item in sorted(p for p in src.iterdir() if p.is_dir() or p.suffix == ".md"):
        mine = copy / item.name
        if not mine.exists():
            if not only_common:
                errors.append(f"{label}/{item.name}: missing ({hint})")
            continue
        files = [item] if item.is_file() else [f for f in item.rglob("*") if f.is_file()]
        for f in files:
            g = mine if item.is_file() else mine / f.relative_to(item)
            if not g.exists() or g.read_bytes() != f.read_bytes():
                errors.append(f"{label}/{item.name}: differs from {src.relative_to(METHOD)}/{item.name} ({f.name}; {hint})")


WHO_START, WHO_END = "<!-- who-is-who:start -->", "<!-- who-is-who:end -->"


def check_who_is_who() -> None:
    """The "Who is who" block is one text, copied verbatim into every entry page of gse-light
    (NG, 2026-10-08, board r5): a page must read alone, so the block is repeated, and this check
    keeps the copies identical (whitespace folded)."""
    r = subprocess.run(["git", "-C", str(METHOD), "ls-files", "-co", "--exclude-standard", "*.md"],
                       capture_output=True, text=True)
    blocks: dict[str, list[str]] = {}
    for rel in r.stdout.splitlines():
        path = METHOD / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if WHO_START not in text:
            continue
        if WHO_END not in text or text.index(WHO_END) < text.index(WHO_START):
            errors.append(f"gse-light/{rel}: who-is-who block has no end marker")
            continue
        body = text[text.index(WHO_START) + len(WHO_START):text.index(WHO_END)]
        blocks.setdefault(" ".join(body.split()), []).append(rel)
    if len(blocks) > 1:
        ref = max(blocks.items(), key=lambda kv: len(kv[1]))[1]
        for body, files in blocks.items():
            if files is not ref:
                errors.append(f"who-is-who block differs in {', '.join(files)} (reference copy: {', '.join(ref)}; "
                              "one text, copied verbatim — see CLAUDE.md, entry documents)")


def check_copies() -> None:
    if ROOT == METHOD:
        same_tree(METHOD / "claude-kit/skills", METHOD / "pm-kit/skills", "pm-kit/skills", "keep both identical", True)
        check_who_is_who()
    elif IS_PM:
        hint = "refresh: ../gse-light/pm-kit/install.sh ."
        same_tree(METHOD / "pm-kit/skills", ROOT / ".claude/skills", ".claude/skills", hint, False)
        same_tree(METHOD / "pm-kit/agents", ROOT / ".claude/agents", ".claude/agents", hint, False)


def check_leaks() -> None:
    """No private term of an instance in the public method."""
    if not IS_PM or ROOT == METHOD:
        return
    terms = []
    for f in sorted((ROOT / "instances").glob("*/private-terms.txt")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                terms.append(re.compile(line.strip()))
    if not terms:
        return
    r = subprocess.run(["git", "-C", str(METHOD), "ls-files", "-co", "--exclude-standard"], capture_output=True, text=True)
    for rel in r.stdout.splitlines():
        path = METHOD / rel
        if not path.is_file() or rel.startswith("LICENSES/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for t in terms:
                if t.search(line):
                    errors.append(f"LEAK gse-light/{rel}:{n}: private term /{t.pattern}/")
    # commit messages are published too (2026-10-07: a first commit message named the client)
    r = subprocess.run(["git", "-C", str(METHOD), "log", "HEAD", "--format=%h %B"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        for t in terms:
            if t.search(line):
                errors.append(f"LEAK gse-light commit message: /{t.pattern}/ in {line[:60]!r}")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    check_links()
    if IS_PM:
        check_registers()
    check_copies()
    check_leaks()
    for w in warnings:
        print(f"WARN {w}")
    for e in errors:
        print(f"FAIL {e}")
    print(f"check_docs ({ROOT.name}): {'FAILED' if errors else 'ok'} ({len(errors)} problem(s), {len(warnings)} warning(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

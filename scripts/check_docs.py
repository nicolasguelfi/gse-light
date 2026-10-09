#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Documentation gates, for the method (gse-light) and for a project's repository (the one that holds project/).
Exit code 1 on any FAIL line; WARN lines never fail the run.

  python3 scripts/check_docs.py                           # in gse-light: the method
  python3 ../gse-light/scripts/check_docs.py              # in the project's repository (holds project/)
  python3 ../gse-light/scripts/check_docs.py <folder>     # the root argument names the repository to check
                                                          # (default: the git toplevel of the current folder)

Checks:
  1. every relative Markdown link points to an existing file, and its #anchor to an existing heading
     (links to https://github.com/nicolasguelfi/gse-light/blob/main/<path> are checked against ../gse-light);
  2. in gse-light: the "Who is who" block (between `<!-- who-is-who:start -->` and `<!-- who-is-who:end -->`)
     is identical in every page that carries it (one text, copied into each entry page so that each page
     reads alone), and every skill, agent, template and script has a row in ARTEFACTS.md (the catalogue);
  3. in a project's repository:
     - every register record has a status badge and a dashboard row, and every dashboard row a record;
     - the pending counts in project/BRIEFING.md §3 match the registers' dashboards:
       FAIL when the register holds fewer 🔴 than §3 says (a record closed without the cockpit),
       WARN only when it holds more (new 🔴 opened by the team; the Project Advisor's next session
       refreshes the cockpit) — a developer's commit never turns CI red for that;
     - .claude/skills and .claude/agents are identical to gse-light's kit (else: refresh with kit/install.sh);
     - deck freshness: for every slide of a deck in force (project/meetings/<date>/slides/project/slides/),
       WARN when a file named in its "Source:" footer was committed after the slide (or after the deck's last
       "Sources checked: YYYY-MM-DD HH:MM" line in slides/README.md), or when the footer is missing;
     - leak guard: no file tracked in gse-light, and no commit message, matches a line of project/private-terms.txt
       (the terms stay in the private repository; gse-light is public). Limit: the guard knows only the
       terms the project lists — a built-in generic list of client names would itself name the clients.
"""
from __future__ import annotations

import datetime
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
PROJECT = ROOT / "project"  # the project's shared record, in the project's repository
IS_PROJECT = PROJECT.is_dir()
REGISTERS = {  # relative to project/
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
    for inst in ([PROJECT] if (PROJECT / "BRIEFING.md").exists() else []):
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


def check_catalogue() -> None:
    """Every skill, agent, template and script of gse-light has a row in ARTEFACTS.md (the
    catalogue, NG 2026-10-08): its name between backticks or as a link text."""
    cat = METHOD / "ARTEFACTS.md"
    if not cat.exists():
        errors.append("ARTEFACTS.md: missing (the catalogue of every artefact, by type)")
        return
    text = cat.read_text(encoding="utf-8")
    expected: list[tuple[str, str]] = []
    for kit in ("kit",):
        for d in sorted((METHOD / kit / "skills").iterdir()):
            if d.is_dir():
                expected.append((f"{kit}/skills/{d.name}", d.name))
        for f in sorted((METHOD / kit / "agents").glob("*.md")):
            expected.append((f"{kit}/agents/{f.name}", f.stem))
        for f in sorted((METHOD / kit / "templates").iterdir()):
            expected.append((f"{kit}/templates/{f.name}", f.name))
    for f in sorted((METHOD / "templates").iterdir()):
        expected.append((f"templates/{f.name}", f.name))
    for f in sorted((METHOD / "scripts").rglob("*")):
        if f.is_file() and f.suffix in (".py", ".sh") and "__pycache__" not in f.parts:
            expected.append((str(f.relative_to(METHOD)), f.name))
    for path, name in expected:
        if not any(s in text for s in (f"`{name}`", f"`{name}/`", f"[`{name}`]", f"/{name})", f"/{name}/)")):
            errors.append(f"ARTEFACTS.md: no row for {path} (the catalogue lists every artefact)")


def check_copies() -> None:
    if ROOT == METHOD:
        check_who_is_who()
        check_catalogue()
    elif IS_PROJECT:
        hint = "refresh: ../gse-light/kit/install.sh"
        same_tree(METHOD / "kit/skills", ROOT / ".claude/skills", ".claude/skills", hint, False)
        same_tree(METHOD / "kit/agents", ROOT / ".claude/agents", ".claude/agents", hint, False)


SOURCE_RE = re.compile(r"Source:\s*([^<]*)", re.I)
FILE_EXT = (".md", ".json", ".py", ".sh", ".html", ".txt", ".csv", ".yml")


def _git_time(repo: Path, rel: Path) -> int | None:
    """Unix time of the last commit touching rel in repo; None when untracked."""
    r = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct", "--", str(rel)],
                       capture_output=True, text=True)
    out = r.stdout.strip()
    return int(out) if out.isdigit() else None


def _resolve_source(token: str, meeting_rel: Path) -> tuple[Path, Path] | None:
    """One token of a slide's "Source:" footer → (repository, path), or None when it names no file
    (a record id, a date, a sentence)."""
    low = token.lower()
    if "reference design" in low:
        return METHOD, Path("method/00-reference-design.md")
    first = token.strip().strip(".,;:()").split(" ")[0].strip("`*")
    if not first or ("/" not in first and not first.endswith(FILE_EXT)):
        return None
    project_rel = meeting_rel.parents[1]  # project/
    candidates: list[tuple[Path, Path]] = []
    if first.startswith("gse-light/"):
        candidates.append((METHOD, Path(first[len("gse-light/"):])))
    elif first.startswith(ROOT.name + "/"):
        candidates.append((ROOT, Path(first[len(ROOT.name) + 1:])))
    else:
        candidates += [(ROOT, Path(first)), (ROOT, meeting_rel / first), (ROOT, project_rel / first),
                       (METHOD, Path(first)), (METHOD, Path("kit") / first),
                       (METHOD, Path("method") / first)]
    for repo, rel in candidates:
        if (repo / rel).exists():
            return repo, rel
    return None


def check_deck_freshness() -> None:
    """A deck in force (project/meetings/<date>/slides/project/slides/*.html) states its
    sources in each slide's "Source:" footer. When a source file was committed after the slide,
    the slide may be stale: WARN (never FAIL) — read it, then republish or date it (NG,
    2026-10-08, board r7). Uncommitted changes are not seen: commit, then check."""
    for slide in sorted(ROOT.glob("project/meetings/*/slides/project/slides/*.html")):
        rel = slide.relative_to(ROOT)
        meeting_rel = rel.parents[3]  # project/meetings/<date>
        text = slide.read_text(encoding="utf-8", errors="ignore")
        m = SOURCE_RE.search(text)
        if not m:
            warnings.append(f"{rel}: no 'Source:' footer (every slide names the files it rests on)")
            continue
        slide_time = _git_time(ROOT, rel)
        if slide_time is None:
            continue  # new slide, not committed yet
        # "Sources checked: YYYY-MM-DD HH:MM" in the deck's slides/README.md records a review of
        # every slide against its sources without republishing them (slides skill, step 6)
        readme = slide.parents[2] / "README.md"
        if readme.exists():
            mc = re.search(r"Sources checked:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", readme.read_text(encoding="utf-8"))
            if mc:
                checked = int(datetime.datetime.strptime(mc.group(1), "%Y-%m-%d %H:%M").timestamp())
                slide_time = max(slide_time, checked)
        for token in re.split(r"\s·\s|·", m.group(1)):
            found = _resolve_source(token, meeting_rel)
            if not found:
                continue
            repo, src = found
            src_time = _git_time(repo, src)
            if src_time and src_time > slide_time:
                warnings.append(f"{rel}: its source {repo.name}/{src} changed after the slide "
                                "(read the slide; republish it, or confirm it still holds)")


def check_leaks() -> None:
    """No private term of the project in the public method."""
    if not IS_PROJECT or ROOT == METHOD:
        return
    terms = []
    for f in [p for p in [PROJECT / "private-terms.txt"] if p.exists()]:
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


def check_template_pairs() -> None:
    """The generic and the sprint templates share fixed lines that scripts read or that must not
    drift (the method's owner, 2026-10-09): in the minutes, the Recording line with its
    "validated by … on" comment and the "Next meeting" section; in the agendas, the heading of
    the topics table."""
    t = METHOD / "templates"
    pairs = [("meeting-minutes.md", "sprint-minutes.md",
              [lambda x: next((l for l in x.splitlines() if l.startswith("- **Recording:**")), None),
               lambda x: x.split("## Next meeting", 1)[1].strip() if "## Next meeting" in x else None]),
             ("meeting-agenda.md", "sprint-agenda.md",
              [lambda x: next((l for l in x.splitlines() if l.startswith("## Agenda")), None)])]
    for a, b, parts in pairs:
        if not (t / a).exists() or not (t / b).exists():
            errors.append(f"templates/{a} and templates/{b}: both must exist (generic and sprint)")
            continue
        ta, tb = (t / a).read_text(encoding="utf-8"), (t / b).read_text(encoding="utf-8")
        for get in parts:
            va, vb = get(ta), get(tb)
            if va is None or vb is None:
                errors.append(f"templates/{a} / {b}: a shared line is missing in one of them")
            elif va != vb:
                errors.append(f"templates/{a} / {b}: shared line differs — {va[:60]!r} vs {vb[:60]!r} "
                              "(keep the lines scripts read identical in both)")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    check_links()
    if IS_PROJECT:
        check_registers()
        check_deck_freshness()
    check_copies()
    check_template_pairs()
    check_leaks()
    for w in warnings:
        print(f"WARN {w}")
    for e in errors:
        print(f"FAIL {e}")
    print(f"check_docs ({ROOT.name}): {'FAILED' if errors else 'ok'} ({len(errors)} problem(s), {len(warnings)} warning(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

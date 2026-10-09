#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Install or refresh the gse-light kit in the project's repository — the one repository that holds
# the code and, in project/, the project's shared record (cockpit, registers, requirements, planning,
# meetings, journal). Usage, run from the root of the project's repository:
#   ../gse-light/kit/install.sh
# Two repositories side by side in the same parent folder: the project's repository (where you run
# this) and the method `gse-light`, read by every session and changed by none.
# Copies the skills, agents and role rules (roles/) into .claude/ (overwriting the kit's own files only) and creates, if
# absent: project/ (from templates/project/, the shared record's skeleton — never touched once it
# has files), CLAUDE.md, .claude/settings.json, .gitattributes, gates.sh, .env.example and the two CI
# workflows (gates, docs). The project's repository owns those files afterwards.
# Works with bash 3.2 (macOS) and Git Bash.
set -euo pipefail

usage="usage: ../gse-light/kit/install.sh   (run from the root of the project's repository)"
case "${1:-}" in -h|--help) echo "$usage"; exit 0 ;; "") ;; *) echo "$usage" >&2; exit 1 ;; esac

# the project's repository: the git repository the command is run in
target="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$target" ] || { echo "not inside a git repository: run this from the root of the project's repository" >&2; exit 1; }
parent="$(cd "$target/.." && pwd)"
project="$(basename "$target")"

# the method: ../gse-light, next to the project's repository
kit="$(cd "$(dirname "$0")" && pwd)"
[ -d "$parent/gse-light/kit" ] \
  || { echo "gse-light is not next to the project's repository: git clone https://github.com/nicolasguelfi/gse-light.git \"$parent/gse-light\"" >&2; exit 1; }
[ "$kit" = "$(cd "$parent/gse-light/kit" && pwd)" ] \
  || echo "warning: this script is not the one in ../gse-light ($kit); the kit expects ../gse-light"
gse="$(cd "$kit/.." && pwd)"
echo "project repository $project · method ../gse-light · project folder project/"

cd "$target"

# fill <project> (the repository's name) in a template; the name has no slash, safe for sed
fill() { sed -e "s/<project>/$project/g" -e "s/<repository name>/$project/g" "$1"; }

# the project folder: the shared record's skeleton, when project/ is missing or empty (a folder
# that already has files is never touched)
if [ ! -d project ] || [ -z "$(ls -A project 2>/dev/null)" ]; then
  mkdir -p project
  find "$kit/templates/project" -type f | while read -r f; do
    rel="${f#"$kit/templates/project/"}"
    mkdir -p "project/$(dirname "$rel")"
    fill "$f" > "project/$rel"
    echo "project $rel"
  done
  echo "created project/ from kit/templates/project/ — fill the <…> fields (README, roles)"
else
  echo "project/ already has files: skeleton not applied"
fi

mkdir -p .claude/skills .claude/agents .claude/roles
# each role's own Claude Code rules: kit-owned, refreshed every time; each person copies theirs once
# into .claude/settings.local.json (never committed) — the shared settings.json is only the floor
for role in "$kit"/roles/*.json; do
  cp "$role" .claude/roles/
  echo "role    $(basename "$role" .json)"
done
for skill in "$kit"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf ".claude/skills/$name"
  cp -R "$skill" ".claude/skills/$name"
  echo "skill   $name"
done
for agent in "$kit"/agents/*.md; do
  cp "$agent" .claude/agents/
  echo "agent   $(basename "$agent" .md)"
done

if [ ! -f CLAUDE.md ]; then
  fill "$kit/templates/CLAUDE.md" > CLAUDE.md
  echo "created CLAUDE.md — fill the <…> fields"
fi
if [ ! -f .claude/settings.json ]; then
  cp "$kit/templates/settings.json" .claude/settings.json
  echo "created .claude/settings.json (the floor for everyone: reads ../gse-light; never reads .env; no force push, no push to main; start hook) — each person: cp .claude/roles/<team|advisor>.json .claude/settings.local.json"
fi
if [ ! -f .gitattributes ]; then
  cp "$kit/templates/gitattributes" .gitattributes
  echo "created .gitattributes (scripts keep LF line endings on every system)"
elif ! grep -qF '*.sh text eol=lf' .gitattributes; then
  printf '\n*.sh text eol=lf\n' >> .gitattributes
  echo "added '*.sh text eol=lf' to .gitattributes"
fi
if [ ! -f gates.sh ]; then
  cp "$kit/templates/gates.sh" gates.sh
  echo "created gates.sh — a stub until the design phase decides the test tools and the continuous integration (then fill it from those DD records)"
fi
chmod +x gates.sh 2>/dev/null || true
# the executable bit must also be in git, or a fresh clone (and CI) gets a non-executable gates.sh
git update-index --add --chmod=+x gates.sh 2>/dev/null || true
if [ ! -f .env.example ]; then
  fill "$kit/templates/env.example" > .env.example
  echo "created .env.example — copy it to .env and fill it (never commit .env)"
fi
mkdir -p .github/workflows
if [ ! -f .github/workflows/gates.yml ]; then
  cp "$kit/templates/ci-gates.yml" .github/workflows/gates.yml
  echo "created .github/workflows/gates.yml — runs bash ./gates.sh; services and branches come after the design phase"
fi
if [ ! -f .github/workflows/docs.yml ]; then
  cp "$kit/templates/ci-docs.yml" .github/workflows/docs.yml
  echo "created .github/workflows/docs.yml — runs the documentation checks of project/ (check_docs) with gse-light at the installed kit version"
fi

# personal files and recordings stay out of git: Claude Code excludes .claude/settings.local.json
# itself, not CLAUDE.local.md (kit/INSTALL.md, "Shared and personal"); .env.* covers .env.local and
# the like, .env.example stays tracked; meeting audio is never committed
touch .gitignore
for p in CLAUDE.local.md .claude/settings.local.json .env '.env.*' '!.env.example' .venv '**/meetings/**/audio*' '**/meetings/**/*.wav' '**/meetings/**/.record.pid' '**/meetings/**/record.log'; do
  grep -qxF -- "$p" .gitignore || { echo "$p" >> .gitignore; echo "added $p to .gitignore"; }
done

# licence notice travels with the kit (LICENSE.md of the gse-light repository)
cp "$kit/templates/KIT_LICENSE.md" .claude/KIT_LICENSE.md
echo "licence notice written to .claude/KIT_LICENSE.md (keep it with the kit)"

# kit version = last commit of gse-light that touched kit/ (not HEAD: other changes do not age the kit)
[ -z "$(git -C "$gse" status --porcelain -- kit 2>/dev/null)" ] \
  || echo "warning: the kit has uncommitted changes in gse-light; KIT_VERSION records the last commit only"
new="$(git -C "$gse" log -1 --format=%h -- kit 2>/dev/null || true)"
old=""; [ -f .claude/KIT_VERSION ] && old="$(tr -d '[:space:]' < .claude/KIT_VERSION)"
if [ -n "$new" ]; then
  if [ -n "$old" ] && [ "$old" != "$new" ]; then
    if ! git -C "$gse" cat-file -e "$old^{commit}" 2>/dev/null; then
      echo "warning: KIT_VERSION $old is unknown in ../gse-light (clone behind, or history rewritten): git pull in ../gse-light, then rerun"
    else
      # a refresh: the templates copied once (CLAUDE.md, settings, gates, CI…) are yours — tell when the kit's own changed
      changed="$(git -C "$gse" diff --name-only "$old..$new" -- kit/templates/ 2>/dev/null | sed 's#^kit/templates/##' | tr '\n' ' ')"
      if [ -n "$changed" ]; then
        echo "templates changed since your install ($old): $changed"
        echo "  compare and carry over by hand:  git -C ../gse-light diff $old..$new -- kit/templates/"
      fi
    fi
  fi
  echo "$new" > .claude/KIT_VERSION
  echo "kit version $new recorded in .claude/KIT_VERSION"
else
  echo "warning: could not read the kit's commit from gse-light; .claude/KIT_VERSION not updated"
fi
echo "next: commit project CLAUDE.md .claude .gitattributes gates.sh .env.example .gitignore .github — new here? read ../gse-light/kit/ONBOARDING.md"

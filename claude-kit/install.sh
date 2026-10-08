#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Install or refresh the Claude kit in a product repository of an instance.
# Usage, run from the root of the product repository:
#   ../gse-light/claude-kit/install.sh <instance> [--pm <folder>]
#   e.g.  ../gse-light/claude-kit/install.sh shop
# Three repositories side by side in the same parent folder: the product repository (where you
# run this), the method `gse-light`, and the private project-management repository holding
# instances/<instance>/. The script finds the project-management repository among the sibling
# folders; `--pm <folder>` names it when none or several hold instances/<instance>/.
# Copies skills and agents into .claude/ (overwriting the kit's own files only), and creates,
# if absent, CLAUDE.md, .claude/settings.json, .gitattributes, gates.sh, .env.example and the
# CI workflow from the templates (the product repository owns them afterwards). A multi-repository
# product runs this once in EACH product repository.
# Works with bash 3.2 (macOS) and Git Bash.
set -euo pipefail

usage="usage: ../gse-light/claude-kit/install.sh <instance> [--pm <folder>]   (run from the root of the product repository)"
instance=""; pmopt=""
while [ $# -gt 0 ]; do
  case "$1" in
    --pm) [ $# -ge 2 ] || { echo "$usage" >&2; exit 1; }; pmopt="$2"; shift 2 ;;
    --pm=*) pmopt="${1#--pm=}"; shift ;;
    -h|--help) echo "$usage"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; echo "$usage" >&2; exit 1 ;;
    *) [ -z "$instance" ] || { echo "$usage" >&2; exit 1; }; instance="$1"; shift ;;
  esac
done
[ -n "$instance" ] || { echo "$usage" >&2; exit 1; }
case "$instance" in */*|.*) echo "instance must be a folder name (no slash, no leading dot): $instance" >&2; exit 1 ;; esac

# the product repository: the git repository the command is run in
target="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$target" ] || { echo "not inside a git repository: run this from the root of the product repository" >&2; exit 1; }
parent="$(cd "$target/.." && pwd)"
product="$(basename "$target")"

# the method: ../gse-light, next to the product repository
kit="$(cd "$(dirname "$0")" && pwd)"
[ -d "$parent/gse-light/claude-kit" ] \
  || { echo "gse-light is not next to the product repository: git clone https://github.com/nicolasguelfi/gse-light.git \"$parent/gse-light\"" >&2; exit 1; }
[ "$kit" = "$(cd "$parent/gse-light/claude-kit" && pwd)" ] \
  || echo "warning: this script is not the one in ../gse-light ($kit); the kit expects ../gse-light"
gse="$(cd "$kit/.." && pwd)"

# the project-management repository: the sibling folder holding instances/<instance>/
if [ -n "$pmopt" ]; then
  if [ -d "$pmopt" ]; then pm="$(cd "$pmopt" && pwd)"
  elif [ -d "$parent/$pmopt" ]; then pm="$(cd "$parent/$pmopt" && pwd)"
  else echo "no such folder: $pmopt" >&2; exit 1; fi
  [ -d "$pm/instances/$instance" ] || { echo "no such instance: $pm/instances/$instance" >&2; exit 1; }
else
  found=""; count=0
  for d in "$parent"/*/; do
    d="${d%/}"
    [ "$d" = "$target" ] && continue
    [ -d "$d/instances/$instance" ] || continue
    found="$found $(basename "$d")"; count=$((count + 1)); pm="$d"
  done
  if [ "$count" -eq 0 ]; then
    echo "no sibling folder of $product holds instances/$instance/: clone the project-management repository next to it, or name it with --pm <folder>" >&2; exit 1
  elif [ "$count" -gt 1 ]; then
    echo "several sibling folders hold instances/$instance/:$found — name the right one with --pm <folder>" >&2; exit 1
  fi
fi
pmname="$(basename "$pm")"
[ "$(cd "$pm/.." && pwd)" = "$parent" ] || echo "warning: $pmname is not next to the product repository; the kit expects ../$pmname"
echo "product repository $product · method ../gse-light · project management ../$pmname/instances/$instance/"

cd "$target"
mkdir -p .claude/skills .claude/agents
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

# fill <instance>, <pm-repo> and <repository name> in a template (folder names: no slash, safe for sed)
fill() { sed -e "s/<instance>/$instance/g" -e "s/<pm-repo>/$pmname/g" -e "s/<repository name>/$product/g" "$1"; }

if [ ! -f CLAUDE.md ]; then
  fill "$kit/templates/CLAUDE.product-repo.md" > CLAUDE.md
  echo "created CLAUDE.md — fill the <…> fields"
fi
if [ ! -f .claude/settings.json ]; then
  fill "$kit/templates/settings.json" > .claude/settings.json
  echo "created .claude/settings.json (reads ../gse-light and ../$pmname; Edit denied under ../gse-light/** and on the cockpit; asks before any git push)"
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
if [ ! -f .github/workflows/gates.yml ]; then
  mkdir -p .github/workflows
  cp "$kit/templates/ci-gates.yml" .github/workflows/gates.yml
  echo "created .github/workflows/gates.yml — runs bash ./gates.sh; services and branches come after the design phase"
fi

# personal files stay out of git: Claude Code excludes .claude/settings.local.json itself,
# not CLAUDE.local.md (claude-kit/INSTALL.md, "Shared and personal"); .env.* covers .env.local
# and the like, .env.example stays tracked
touch .gitignore
for p in CLAUDE.local.md .env '.env.*' '!.env.example'; do
  grep -qxF -- "$p" .gitignore || { echo "$p" >> .gitignore; echo "added $p to .gitignore"; }
done

# licence notice travels with the kit (LICENSE.md of the gse-light repository)
cp "$kit/templates/KIT_LICENSE.md" .claude/KIT_LICENSE.md
echo "licence notice written to .claude/KIT_LICENSE.md (keep it with the kit)"

# kit version = last commit of gse-light that touched claude-kit/ (not HEAD: other changes do not age the kit)
[ -z "$(git -C "$gse" status --porcelain -- claude-kit 2>/dev/null)" ] \
  || echo "warning: the kit has uncommitted changes in gse-light; KIT_VERSION records the last commit only"
new="$(git -C "$gse" log -1 --format=%h -- claude-kit 2>/dev/null || true)"
old=""; [ -f .claude/KIT_VERSION ] && old="$(tr -d '[:space:]' < .claude/KIT_VERSION)"
if [ -n "$new" ]; then
  if [ -n "$old" ] && [ "$old" != "$new" ]; then
    if ! git -C "$gse" cat-file -e "$old^{commit}" 2>/dev/null; then
      echo "warning: KIT_VERSION $old is unknown in ../gse-light (clone behind, or history rewritten): git pull in ../gse-light, then rerun"
    else
      # a refresh: the templates copied once (CLAUDE.md, settings, gates, CI…) are yours — tell when the kit's own changed
      changed="$(git -C "$gse" diff --name-only "$old..$new" -- claude-kit/templates/ 2>/dev/null | sed 's#^claude-kit/templates/##' | tr '\n' ' ')"
      if [ -n "$changed" ]; then
        echo "templates changed since your install ($old): $changed"
        echo "  compare and carry over by hand:  git -C ../gse-light diff $old..$new -- claude-kit/templates/"
      fi
    fi
  fi
  echo "$new" > .claude/KIT_VERSION
  echo "kit version $new recorded in .claude/KIT_VERSION"
else
  echo "warning: could not read the kit's commit from gse-light; .claude/KIT_VERSION not updated"
fi
echo "next: commit CLAUDE.md .claude .gitattributes gates.sh .env.example .gitignore .github — new here? read ../gse-light/claude-kit/ONBOARDING.md"

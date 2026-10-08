#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Install or refresh the Project Advisor's kit in a project-management repository (the private
# repository holding instances/<instance>/), cloned next to gse-light.
# Usage: ../gse-light/pm-kit/install.sh <path-to-pm-repository> [<instance>]   (e.g. `. loop` from inside it)
# Overwrites only the kit's own skills and agents; creates CLAUDE.md, settings, .env.example and
# the CI workflow if absent (yours afterwards). With <instance> (else INSTANCE in .env, else the
# only folder in instances/): when instances/<instance>/ is missing or empty, it is created from
# the skeleton pm-kit/templates/instance/ (cockpit, registers, roles, journal, meetings) with
# <instance> filled in; an instance that already has files is never touched.
set -euo pipefail

[ $# -ge 1 ] && [ $# -le 2 ] || { echo "usage: $0 <path-to-pm-repository> [<instance>]" >&2; exit 1; }
kit="$(cd "$(dirname "$0")" && pwd)"
target="$(cd "$1" && pwd)"
instance="${2:-}"
case "$instance" in */*|.*) echo "instance must be a folder name (no slash, no leading dot): $instance" >&2; exit 1 ;; esac
if [ -z "$instance" ] && [ -f "$target/.env" ]; then  # only the INSTANCE= line is read; nothing is sourced
  instance="$(grep -E '^INSTANCE=' "$target/.env" | head -1 | cut -d= -f2- | sed -e 's/[[:space:]]#.*$//' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"//' -e 's/"$//')"
fi
if [ -z "$instance" ] && [ -d "$target/instances" ]; then
  n="$(find "$target/instances" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  [ "$n" = 1 ] && instance="$(basename "$(find "$target/instances" -mindepth 1 -maxdepth 1 -type d)")"
fi
[ -d "$target/instances" ] || [ -n "$instance" ] \
  || { echo "$target has no instances/ folder: name the instance to create ($0 $1 <instance>)" >&2; exit 1; }
[ "$(cd "$target/.." && pwd)/gse-light" = "$(cd "$kit/.." && pwd)" ] \
  || echo "warning: gse-light is not next to $target; the scripts expect ../gse-light"

# the instance's skeleton, when its folder is missing or empty (a filled instance is never touched)
if [ -n "$instance" ]; then
  inst="$target/instances/$instance"
  if [ ! -d "$inst" ] || [ -z "$(ls -A "$inst" 2>/dev/null)" ]; then
    if [ -d "$kit/templates/instance" ]; then
      mkdir -p "$inst"
      find "$kit/templates/instance" -type f | while read -r f; do
        rel="${f#"$kit/templates/instance/"}"
        mkdir -p "$inst/$(dirname "$rel")"
        sed -e "s/<instance>/$instance/g" "$f" > "$inst/$rel"
        echo "instance $instance/$rel"
      done
      echo "created instances/$instance/ from pm-kit/templates/instance/ — fill the <…> fields (README, roles)"
    else
      echo "no skeleton at $kit/templates/instance/: instances/$instance/ left as is (create its files by hand)"
      mkdir -p "$inst"
    fi
  else
    echo "instances/$instance/ already has files: skeleton not applied"
  fi
fi

mkdir -p "$target/.claude/skills" "$target/.claude/agents"
for s in "$kit"/skills/*/; do
  name="$(basename "$s")"; rm -rf "$target/.claude/skills/$name"; cp -R "$s" "$target/.claude/skills/$name"; echo "skill   $name"
done
for a in "$kit"/agents/*.md; do cp "$a" "$target/.claude/agents/"; echo "agent   $(basename "$a" .md)"; done

if [ ! -f "$target/.claude/settings.json" ]; then cp "$kit/templates/settings.json" "$target/.claude/settings.json"; echo "created .claude/settings.json"; fi
if [ ! -f "$target/CLAUDE.md" ]; then cp "$kit/templates/CLAUDE.pm-repo.md" "$target/CLAUDE.md"; echo "created CLAUDE.md — fill the <…> fields"; fi
if [ ! -f "$target/.env.example" ]; then cp "$kit/templates/env.example" "$target/.env.example"; echo "created .env.example"; fi
if [ ! -f "$target/.github/workflows/docs.yml" ]; then
  mkdir -p "$target/.github/workflows"; cp "$kit/templates/docs.yml" "$target/.github/workflows/docs.yml"; echo "created .github/workflows/docs.yml"
fi
touch "$target/.gitignore"
for p in .env '.env.*' '!.env.example' CLAUDE.local.md .claude/settings.local.json '**/meetings/**/audio*' '**/meetings/**/*.wav' '**/meetings/**/.record.pid' '**/meetings/**/record.log'; do
  grep -qxF -- "$p" "$target/.gitignore" || { echo "$p" >> "$target/.gitignore"; echo "added $p to .gitignore"; }
done

cp "$kit/../claude-kit/templates/KIT_LICENSE.md" "$target/.claude/KIT_LICENSE.md"
[ -z "$(git -C "$kit" status --porcelain -- . 2>/dev/null)" ] || echo "warning: pm-kit has uncommitted changes; PM_KIT_VERSION records the last commit only"
# kit version = last commit of gse-light that touched pm-kit/ (not HEAD: other changes do not age the kit);
# the CI workflow checks gse-light out at this commit (templates/docs.yml)
git -C "$kit/.." log -1 --format=%h -- pm-kit > "$target/.claude/PM_KIT_VERSION" 2>/dev/null || true
echo "pm-kit version $(cat "$target/.claude/PM_KIT_VERSION" 2>/dev/null) recorded in .claude/PM_KIT_VERSION; check: python3 ../gse-light/scripts/check_docs.py"

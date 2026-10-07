#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Install or refresh the Claude kit in a product repository of an instance.
# Usage: ../gse-light/claude-kit/install.sh <product-repository> <pm-repository> <instance>
#   e.g. from the parent folder:  gse-light/claude-kit/install.sh shop shop-pm shop
# <pm-repository> is the private project-management repository holding instances/<instance>/,
# cloned next to the product repository and to gse-light.
# Copies skills and agents into <repo>/.claude/ (overwriting the kit's own files only),
# and creates CLAUDE.md, .claude/settings.json, .env.example and the CI workflow from the
# templates if they are absent (the repository owns them afterwards).
set -euo pipefail

kit="$(cd "$(dirname "$0")" && pwd)"
usage="usage: install.sh <product-repository> <pm-repository> <instance>"
target="${1:?$usage}"; pm="${2:?$usage}"; instance="${3:?$usage}"
[ -d "$pm/instances/$instance" ] || { echo "no such instance: $pm/instances/$instance" >&2; exit 1; }
pmname="$(basename "$(cd "$pm" && pwd)")"
[ "$(cd "$pm/.." && pwd)" = "$(cd "$target/.." && pwd)" ] || echo "warning: $pmname is not next to the product repository; the kit expects ../$pmname"
[ -d "$target/.git" ] || { echo "not a git repository: $target" >&2; exit 1; }

mkdir -p "$target/.claude/skills" "$target/.claude/agents"
for skill in "$kit"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "$target/.claude/skills/$name"
  cp -R "$skill" "$target/.claude/skills/$name"
  echo "skill   $name"
done
for agent in "$kit"/agents/*.md; do
  cp "$agent" "$target/.claude/agents/"
  echo "agent   $(basename "$agent" .md)"
done

if [ ! -f "$target/CLAUDE.md" ]; then
  sed -e "s/<instance>/$instance/g" -e "s/<pm-repo>/$pmname/g" "$kit/templates/CLAUDE.product-repo.md" > "$target/CLAUDE.md"
  echo "created CLAUDE.md — fill the <…> fields"
fi
if [ ! -f "$target/.claude/settings.json" ]; then
  cp "$kit/templates/settings.json" "$target/.claude/settings.json"
  echo "created .claude/settings.json"
fi
if [ ! -f "$target/.env.example" ]; then
  cp "$kit/templates/env.example" "$target/.env.example"
  echo "created .env.example — copy it to .env and fill it (never commit .env)"
fi
if [ ! -f "$target/.github/workflows/gates.yml" ]; then
  mkdir -p "$target/.github/workflows"
  cp "$kit/templates/ci-gates.yml" "$target/.github/workflows/gates.yml"
  echo "created .github/workflows/gates.yml — fill the <…> fields"
fi

# personal files stay out of git: Claude Code excludes .claude/settings.local.json itself,
# not CLAUDE.local.md (claude-kit/INSTALL.md, "Shared and personal")
touch "$target/.gitignore"
for p in CLAUDE.local.md .env; do
  grep -qxF "$p" "$target/.gitignore" || { echo "$p" >> "$target/.gitignore"; echo "added $p to .gitignore"; }
done

# licence notice travels with the kit (LICENSE.md of the gse-light repository)
cp "$kit/templates/KIT_LICENSE.md" "$target/.claude/KIT_LICENSE.md"
echo "licence notice written to .claude/KIT_LICENSE.md (keep it with the kit)"

[ -z "$(git -C "$kit" status --porcelain -- . 2>/dev/null)" ] || echo "warning: the kit has uncommitted changes; KIT_VERSION records the last commit only"
git -C "$kit" rev-parse --short HEAD > "$target/.claude/KIT_VERSION" 2>/dev/null || true
echo "kit version recorded in .claude/KIT_VERSION"
echo "new here? read $kit/ONBOARDING.md"

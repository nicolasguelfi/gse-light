# gse-light — instructions for Claude

This **public** repository holds the method **gse-light**: project management for software
projects built with generative AI (Claude) as a working partner — reference design
(`method/`), templates (`templates/`), the Project Advisor's scripts (`scripts/`), the kit for
**product repositories** (`claude-kit/`) and the kit for **project-management repositories**
(`pm-kit/`). It holds no project: each project's management lives in its own **private**
project-management repository (`instances/<name>/`), cloned next to this one.

## Standing rules

- **Nothing about a client or a client's project here.** No client or project name, person,
  data, budget, infrastructure detail or register number of an instance; examples are
  fictitious or generic. The author's own projects, Sumvadis (https://sumvadis.ai/) and
  StreamTeX (https://streamtex.org/), may be cited as **illustrations** that a rule can be
  applied — never as defaults or starting points. Each project-management repository lists
  its private terms in `instances/<name>/private-terms.txt`, and its `check_docs` run fails
  on any of them found here, in files and in commit messages (leak guard). Run it from such
  a repository before every push of gse-light, and write commit messages without project names.
- **The method names no technology for the product.** Rules are invariants; choices are the
  instance's `DD` records — the twelve decisions of `claude-kit/skills/design-phase/SKILL.md`
  §2, always named by those twelve names, in that order — taken in its design phase from
  its drivers. Tool names live only in `method/40-tool-landscape-examples.md` (dated,
  non-normative), apart from GitHub (prerequisite of the tooling) and Playwright, named as
  the one example of the firm end-to-end rule (end-to-end tests go through the real user
  interface, run by Claude; the tool is the instance's choice). A Claude session never
  proposes an example project's stack as a default. The environment before production is
  "the rehearsal environment".
- **Plain words first, technical words second**; define each technical term at first use, or
  link it to `GLOSSARY.md`; a new term goes into the glossary in the same change.
- **Measure before asserting**: a claim about the state of a system comes with the command
  that measured it.
- **Evaluate ≠ execute**: when asked to evaluate or propose, change nothing outside the
  document being written. Push only on the go-ahead of Nicolas Guelfi (NG), the author.
- **Kits stay in step**: skills present in both `claude-kit/skills/` and `pm-kit/skills/` are
  identical (`check_docs`). After a change, the project-management repositories refresh with
  `../gse-light/pm-kit/install.sh .`, the product repositories with `claude-kit/install.sh`.
- **Developer documents stay in step**: `QUICKSTART.md` (one page), `claude-kit/INSTALL.md`,
  `claude-kit/ONBOARDING.md` and the two Day-0 rehearsals change together — 2026-10-08 —
  developers had no one-page guide at the root.
- **Paths in kit files**: skills and agents run from the project-management repository (or a
  product repository); method paths are written `../gse-light/…`, and Markdown links to the
  method use `https://github.com/nicolasguelfi/gse-light/blob/main/…` (checked locally).
- **Licence**: every new file is covered by `REUSE.toml`; code files carry the SPDX header;
  `uvx --from 'reuse[charset-normalizer]' reuse lint` must stay compliant.
- **Language**: documents in English; NG may write in French — answer him in French.
- **Never "the repository" alone**: name it — `gse-light`, the project-management repository
  `<pm-repo>`, the product repository `<product-repo>`, a sandbox repository
  `<project>-sandbox-<firstname>`.
- **Team-facing pages name roles, not people**: "the Project Advisor" (named in the
  instance's roles record), never the author's name or initials; the author's name stays in
  status lines, licence footers and the pm-kit README. Abbreviations are expanded at first
  use ("a short multiple-choice question (QCM)").

## Checks

`python3 scripts/check_docs.py` here (links, kit copies); from a project-management
repository, `python3 ../gse-light/scripts/check_docs.py` (adds registers, `.claude/` copies
and the leak guard); from a product repository,
`python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the project-management
repository as root argument). CI runs the first (`.github/workflows/docs.yml`).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

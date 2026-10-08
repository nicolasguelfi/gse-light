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
  instance's `DD` records, taken in its design phase from its drivers (kit skill
  `design-phase`). Tool names live only in `method/40-tool-landscape-examples.md` (dated,
  non-normative); a Claude session never proposes an example project's stack as a default.
  Two exceptions, stated as such: end-to-end tests through the real user interface, run by
  Claude, are a firm rule (the tool is the instance's choice), and GitHub is a prerequisite
  of the method's own tooling.
- **Plain words first, technical words second**; define each technical term at first use.
- **Measure before asserting**: a claim about the state of a system comes with the command
  that measured it.
- **Evaluate ≠ execute**: when asked to evaluate or propose, change nothing outside the
  document being written. Push only on NG's go-ahead.
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
  `<pm-repo>`, the product repository `<product-repo>`.

## Checks

`python3 scripts/check_docs.py` here (links, kit copies); from a project-management
repository, `python3 ../gse-light/scripts/check_docs.py` (adds registers, `.claude/` copies
and the leak guard). CI runs the first (`.github/workflows/docs.yml`).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

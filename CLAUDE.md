# gse-light — instructions for Claude

This **public** repository holds the method **gse-light**: project management for software
projects built with generative AI (Claude) as a working partner — reference design
(`method/`), templates (`templates/`), the Project Advisor's scripts (`scripts/`), the kit for
**product repositories** (`claude-kit/`) and the kit for **project-management repositories**
(`pm-kit/`). It holds no project: each project's management lives in its own **private**
project-management repository (`instances/<instance>/`), cloned next to this one.

## Standing rules

- **Nothing about a client or a client's project here.** No client or project name, person,
  data, budget, infrastructure detail or register number of an instance; examples are
  fictitious or generic. The author's own projects, Sumvadis (https://sumvadis.ai/) and
  StreamTeX (https://streamtex.org/), may be cited as **illustrations** that a rule can be
  applied — never as defaults or starting points. Each project-management repository lists
  its private terms in `instances/<instance>/private-terms.txt`, and its `check_docs` run fails
  on any of them found here, in files and in commit messages (leak guard). Run it from such
  a repository before every push of gse-light, and write commit messages without project names.
- **The method names no technology for the product.** Rules are invariants; choices are the
  instance's `DD` records — the twelve decisions of the design phase, always named by these
  twelve names, in this order: repository layout, hosting, environments and promotion path,
  stack and language, data store, identity, infrastructure as code, continuous integration,
  test tools, secrets, dependency updates, monitoring (recorded with the kit skill
  `claude-kit/skills/design-phase/SKILL.md`) — taken in its design phase from its drivers.
  Never write "the twelve decisions of `design-phase` §2": name them. Tool names live only in `method/40-tool-landscape-examples.md` (dated,
  non-normative), apart from GitHub (prerequisite of the tooling) and Playwright, named as
  the one example of the firm end-to-end rule (end-to-end tests go through the real user
  interface, run by Claude; the tool is the instance's choice). A Claude session never
  proposes an example project's stack as a default. The environment before production is
  "the rehearsal environment".
- **Plain words first, technical words second**; define each technical term at first use (a
  link to `GLOSSARY.md` may follow, never replace the one line); a new term goes into the
  glossary in the same change.
- **Entry documents** (README, QUICKSTART, INSTALL, ONBOARDING, instance README): first a
  part for everyone — what the page is, *Words used here* (a table Word · Meaning, ≤ 10 rows), *Who is
  who* (a table Role · Side · What they do · What they decide or write), the repositories (what for, who writes, who reads, why separate) — then one section
  per role (project lead, developer, product owner, Project Advisor) saying what that role
  reads, installs, writes and never does; then the reference. The *Who is who* block is
  identical in every entry page of `gse-light` (`check_docs` compares the copies between its
  markers, the HTML comments `who-is-who:start` and `who-is-who:end` — never write those
  markers outside an actual copy of the block, this page included). Role names: developer,
  project lead (lead developer), product owner, data protection contact, Project Advisor
  (then "the Advisor"), Claude sessions. (NG, 2026-10-08, board r5.)
- **Names, one spelling** (NG, 2026-10-08, board r5): "developer", never "engineer"; "team
  member" means the project lead or a developer, used only when both are meant, said once per
  page; "the project lead", never "the lead"; "data protection contact", never "DPO contact";
  "Project Advisor" in full at its first use on a page, then "the Advisor", never "tutor" or
  "mentor"; "not the project manager", never "project director". Placeholders:
  `instances/<instance>/` (never `instances/<name>/`), `~/dev/<project>` (never `<client>`),
  `<firstname>` (never `<first name>`); "the host of `<pm-repo>` (roles record)", never
  "whoever hosts it". Minutes are "validated by <the Project Advisor's name> on YYYY-MM-DD":
  `scripts/situation.py` accepts any name. The twelve design decisions are always listed by
  name (rule above), never "the twelve decisions of `design-phase` §2"; the reference design's
  chapters are named: 0 (purpose and how to read it), 1 (principles), 2 (how people and AI
  share the decisions), 13 (working with the AI day to day), 15 (the start-of-project checklist).
- **Readable layout** (NG, 2026-10-08): a reader must locate an item at a glance. Definitions
  (*Words used here*, *Who is who*) are tables, never a paragraph; any enumeration of three
  items or more (repositories, steps, rules, files, links) is a list or a table, one item per
  line, the lead word in bold; no paragraph of more than six lines in an entry page; a
  definitions box never sits inside a blockquote (it renders small). Length is accepted,
  density is not.
- **Measure before asserting**: a claim about the state of a system comes with the command
  that measured it.
- **Evaluate ≠ execute**: when asked to evaluate or propose, change nothing outside the
  document being written. Push only on the go-ahead of Nicolas Guelfi (NG), the author.
- **Kits stay in step**: skills present in both `claude-kit/skills/` and `pm-kit/skills/` are
  identical (`check_docs`). After a change, the project-management repositories refresh with
  `../gse-light/pm-kit/install.sh .`, the product repositories with `claude-kit/install.sh`.
- **Developer documents stay in step**: `QUICKSTART.md` (one page), `claude-kit/INSTALL.md`,
  `claude-kit/ONBOARDING.md` and the two Day-0 rehearsals change together — 2026-10-08 —
  developers had no one-page guide at the root. **One numbered path, one place** (NG,
  2026-10-09): the developer's path from zero (account, seat, access, clones, kit, first
  session, product repository) is the table of `QUICKSTART.md`; the other pages point to it
  and add only what is theirs — the Day-0 commands were written five times and no page
  carried the steps before the first clone.
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
- **Asking the author** (NG, 2026-10-09): a short multiple-choice question (QCM) for a simple
  point; a review board (skill `review` of the kits, `--lang fr`) when the choice is complex or
  data must be shown — the problem restated, every option's advantages, drawbacks and
  consequences, a comment under every point and a global one; his answer comes back as one
  line; nothing changes before it.

## Checks

`python3 scripts/check_docs.py` here (links, kit copies); from a project-management
repository, `python3 ../gse-light/scripts/check_docs.py` (adds registers, `.claude/` copies
and the leak guard); from a product repository,
`python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the project-management
repository as root argument). CI runs the first (`.github/workflows/docs.yml`).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

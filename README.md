# gse-light — project management with generative AI

A light method for running software projects built with generative AI (Claude Code) as a
working partner, with a **Project Advisor** who gives feedback and advice in two hours of
meeting and two hours of preparation a week. Author: Nicolas Guelfi, for [right-on-skill](https://rightonskill.odoo.com/).

It holds the method and its tools, **no project**: each project keeps its own management in a
private repository, cloned next to this one.

| Repository | Visibility | Holds |
|---|---|---|
| `gse-light` (this one) | public | the method, templates, scripts, and two Claude kits |
| `<pm-repo>` — one per client or project | private | `instances/<name>/`: cockpit, registers, requirements, planning, meetings, journal |
| `<product-repo>` — the code | private | the product, with the Claude kit committed in it |

## Where to start

**Developer?** Start with [QUICKSTART.md](QUICKSTART.md): what gse-light does for you and what to
use at each moment of the project, in one page.

| You are… | Read first |
|---|---|
| A Project Advisor starting a project | [`pm-kit/README.md`](pm-kit/README.md) — create the project-management repository and install the pm-kit |
| A project lead | [the Project Advisor's page](method/15-project-advisor.md), the [reference design](method/00-reference-design.md), then [`claude-kit/INSTALL.md`](claude-kit/INSTALL.md) §2 |
| An engineer | [`QUICKSTART.md`](QUICKSTART.md) (one page), then [`claude-kit/INSTALL.md`](claude-kit/INSTALL.md) (clone, `.env`, `check.sh`), then [`claude-kit/ONBOARDING.md`](claude-kit/ONBOARDING.md), then the [reference design](method/00-reference-design.md) chapters 0–2 |

## Layout

| Folder | What it holds |
|---|---|
| [`method/`](method/) | [Reference design](method/00-reference-design.md) (rules and tools), [the Project Advisor's page](method/15-project-advisor.md), [upskilling](method/20-upskilling.md) |
| [`templates/`](templates/) | Decision record, journal entry, meeting agenda and minutes, skills grid, slide deck, artifact shortcut |
| [`scripts/`](scripts/) | `check_docs.py` (links, registers, kit copies, leak guard), `situation.py` and the session-start hook, `llm_call.py` (paid models, costs logged), `meeting/` (record, transcribe) — run from a project-management repository |
| [`pm-kit/`](pm-kit/README.md) | The Project Advisor's Claude artefacts for a project-management repository: `advisor` (single entry point), `meeting`, `slides`, `method-lesson`, `decision-record`, `cockpit-update`, `session-close`, `genai-onboarding`; agents `delivery-auditor`, `minutes-verifier`, `design-reviewer` |
| [`claude-kit/`](claude-kit/README.md) | The Claude artefacts for each product repository: `decision-record`, `session-close`, `verify-claim`, `upskilling`, agent `change-reviewer` |

## Rules that hold everywhere

1. **Every decision and every open question goes into a register** of its instance, never
   scattered in a document. Registers share one format (see [`templates/decision-record.md`](templates/decision-record.md)).
2. **Plain words first, technical words second**, in every document.
3. **Evaluate is not execute**: a request to assess changes nothing; an action needs an
   explicit go-ahead.
4. **Measure before asserting**: a claim about the state of a system is backed by a
   command anyone can rerun.

Status: v0.4 · 2026-10-07 · the method, separated from its projects

## Licence

© 2026 [right-on-skill](https://rightonskill.odoo.com/); author Nicolas Guelfi. Source-available for **non-commercial use**, with **attribution**:
documents under [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt), code under the
[PolyForm Noncommercial License 1.0.0](LICENSES/LicenseRef-PolyForm-Noncommercial-1.0.0.md).
Cite *Nicolas Guelfi, gse-light, 2026, https://github.com/nicolasguelfi/gse-light*
([`CITATION.cff`](CITATION.cff)); commercial use needs a separate licence from right-on-skill.
Details: [`LICENSE.md`](LICENSE.md).

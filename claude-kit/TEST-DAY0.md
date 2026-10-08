# Rehearse a developer's Day 0 on your own machine

Status: v0.5 · 2026-10-08 · for the Project Advisor or a project lead · 15 minutes for the
install and checks (§0–§2 and §4); the first session (§3) adds 15 minutes of `/upskilling`
and 30 minutes of work

> **Essentials** — Plays, in a throwaway folder, what [INSTALL.md](INSTALL.md) asks of a
> project lead (install the kit once in the product repository with one command, commit it)
> and of a developer (clone, `.env`, `check.sh`, a first session). It clones the `gse-light`
> repository from GitHub like an engineer would, and simulates the project-management
> repository and the product repository with local ones. It touches none of your working
> copies. Run it **outside any synced folder** (here `~/gse-test`).

**In a hurry?** [TEST-DAY0-fast.txt](TEST-DAY0-fast.txt) holds §0–§2 and §4 as three
blocks (reset, project lead, developer) to paste one after the other — kept in step with
this page, command by command.

## The repositories in this test

Three repositories side by side in one parent folder, as on an engineer's machine: the
product repository, the method `gse-light`, and the private project-management repository.

| Name in the commands | Which repository | Stands for |
|---|---|---|
| `gse-light` | the `gse-light` repository (method and kits), cloned from GitHub `nicolasguelfi/gse-light` | itself |
| `remote-pm.git` | a local **bare** repository (no working files), created by the test with one instance folder `instances/demo/` | the project's private project-management repository `<pm-repo>` on GitHub |
| `remote-product.git` | a local bare repository, created empty by the test | the product repository `<product-repo>` on GitHub — or a personal sandbox repository `<project>-sandbox-<firstname>`, which receives the kit the same way |
| `lead/pm`, `lead/product` | the project lead's clones of `remote-pm.git` and `remote-product.git` | the project lead's working copies |
| `dev/pm`, `dev/product` | the developer's clones of the same | a developer's working copies |

Prerequisites on the machine: `git`, `python3` (the method's scripts), a bash terminal (Git
Bash on Windows).

## 0. Settings

Copy these two lines in your terminal first; every block below uses them.

```bash
INST=demo                      # the instance (folder name in instances/ of the project-management repository)
TEST=~/gse-test                # throwaway folder, outside any synced folder
```

## 1. Project lead — install the kit in the product repository and commit it

```bash
mkdir -p "$TEST/lead" && cd "$TEST"
git init -q --bare remote-pm.git                       # remote-pm.git, empty: the project-management repository as just created on GitHub
git init -q --bare remote-product.git                  # remote-product.git, empty: the product repository as just created on GitHub
cd lead
git clone -q https://github.com/nicolasguelfi/gse-light.git   # clones the gse-light repository (method and kits)
git clone -q ../remote-pm.git pm                       # clones remote-pm.git into lead/pm
                                                       # expected warning: "You appear to have cloned an empty repository."
(cd pm && mkdir -p "instances/$INST" && echo "# $INST" > "instances/$INST/README.md" \
  && git add . && git commit -q -m "Instance $INST" && git push -q origin HEAD)   # lead/pm gets its instance folder, pushed to remote-pm.git
git clone -q ../remote-product.git product             # clones remote-product.git into lead/product (same expected warning)
cd product && git commit -q --allow-empty -m init && git push -q origin HEAD   # first commit of lead/product, pushed to remote-product.git
../gse-light/claude-kit/install.sh "$INST"             # ONE command, from inside lead/product: finds ../gse-light and the sibling folder holding instances/demo/ (lead/pm)
../gse-light/claude-kit/check.sh                       # checks lead/product — expected: MISSING "kit committed"
bash ./gates.sh                                        # the Day-0 stub, run as CI runs it — expected: "no gates yet: design phase in progress …", exit 0
git add CLAUDE.md .claude .gitattributes gates.sh .env.example .gitignore .github
git commit -q -m "Install the Claude kit ($INST)" && git push -q origin HEAD   # the kit is now in remote-product.git
```

**Expected**: `install.sh` prints the line `product repository product · method ../gse-light ·
project management ../pm/instances/demo/`, lists five skills (`decision-record`,
`design-phase`, `session-close`, `upskilling`, `verify-claim`) and one agent (`change-reviewer`), and
creates `CLAUDE.md`, `.claude/settings.json`, `.gitattributes`, `gates.sh`, `.env.example`
and `.github/workflows/gates.yml`; `check.sh` shows one `MISSING kit committed` line before
the commit, and one `WARN .env` line — normal here: the project lead needs no `.env` in
`lead/product` for this rehearsal. If `install.sh` answers "several sibling folders hold
instances/demo/", name the right one: `../gse-light/claude-kit/install.sh "$INST" --pm pm`.

## 2. Developer — clone, `.env`, check

```bash
mkdir -p "$TEST/dev" && cd "$TEST/dev"
git clone -q https://github.com/nicolasguelfi/gse-light.git   # the developer's clone of the gse-light repository
git clone -q ../remote-pm.git pm                       # clones remote-pm.git into dev/pm (the project-management repository)
git clone -q ../remote-product.git product             # clones remote-product.git into dev/product: the kit comes with it
cd product
cp .env.example .env                                   # personal settings of dev/product, never committed
../gse-light/claude-kit/check.sh; echo "exit $?"       # checks dev/product — expected: only OK lines, exit 0
```

**Expected**: every line `OK`, among them `settings.json gives Claude read access…`,
`gates.sh present and executable`, `.gitattributes keeps scripts LF`, `kit version <hash>
(current)` — the hash is the last commit of `gse-light` that touched `claude-kit/`. Two
`WARN` lines can replace the last one outside this rehearsal: `the kit in gse-light is
newer` (the project lead refreshes the kit with `install.sh`) and `your clone of gse-light
is behind` (run `git pull` in your `gse-light`).

## 3. Developer — first session in `dev/product`

```bash
claude
```

In the session:

- type `/` — `decision-record`, `design-phase`, `session-close`, `verify-claim` and `upskilling` appear;
- type `/upskilling` — fifteen minutes of questions and small checks, then a personal plan;
- ask *"what is in ../pm/instances/demo/?"* — Claude reads it (`additionalDirectories`)
  but cannot edit `../gse-light` nor the instance's `BRIEFING.md` (deny rules of
  `.claude/settings.json`), and asks before any `git push`.

## 4. Check that nothing personal went into `dev/product`'s git history

```bash
git status --short                                     # in dev/product: .env must not appear
ls ~/.claude/upskilling/"$INST"/                       # your private record, in your home folder, outside every repository
```

## 5. Clean up

```bash
rm -rf "$TEST"                                         # removes remote-pm.git, remote-product.git, lead/ and dev/
rm -rf ~/.claude/upskilling/"$INST"                    # only if /upskilling wrote a test record
```

## If something differs

Paste the output of `check.sh` to the session; [INSTALL.md §4](INSTALL.md#4-if-something-is-missing)
lists what each line means. Not covered by this rehearsal: Windows (use Git Bash for the
same commands) and the real repositories on GitHub.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

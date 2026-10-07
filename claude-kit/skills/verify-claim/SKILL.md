---
name: verify-claim
description: Before stating anything about the state of a system (deployed version, data counts, configuration, test results, cause of a fault), measure it and show the command and its output. Use whenever an answer would assert a fact about a running system, a branch, a database or a deployment.
---

# Verify a claim before stating it

Method principle 5: **measure before asserting** (reference design, chapter 1).

1. **Name the claim** you are about to make, in one sentence.
2. **Find the command that measures it** — read-only: a query, `git` command, HTTP
   request to a health or version endpoint, CI status, log search. Never a command that
   changes state to "check".
3. **Run it** and quote the relevant output with the date and the environment.
4. **State the claim only as far as the output supports it.** "Staging serves 1.4.2
   (`curl https://…/version`, 2026-10-06 14:02)" — not "the release is out".
5. **Causes**: a cause is stated as verified only if the measurement was repeated after
   the fix and the symptom is gone. Otherwise write "hypothesis".
6. **Deviation ≠ defect**: before calling a measured deviation a defect, read the
   registers — it may be a decision.
7. When the measurement is impossible (no access, environment down), say so plainly and
   say what would measure it.

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))

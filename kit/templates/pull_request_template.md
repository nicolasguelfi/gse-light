<!-- Template of the gse-light method (review on evidence, reference design ch. 8). The author's
     session fills every section; the reviewer judges the evidence, and reads the code only where a
     risk is flagged. Kit-only and documentation pull requests: write "n/a" where a section does not apply. -->

## Ticket and use case

Closes #<ticket>. Use case: <the requirement and example it serves, linked>.
One pull request = one ticket and one use case.

## Summary for humans

- **Intent**: <why, in two lines>
- **What changed**: <the behaviour, not the files>
- **Risks**: <what could go wrong; "none" is a claim to justify>
- **How it is verified**: <commands and their results>
- **Not verified**: <what was not tested, and why>

## Evidence

- [ ] **Use case replayed** by the end-to-end test through the real user interface: <test name> — trace or screenshots: <link>
- [ ] **Verified-map delta**: <the behaviours and qualities this change adds or changes, and their tests>
- [ ] **Gates green**: `bash ./gates.sh` locally (output below) and in CI
- [ ] **Size**: `python3 ../gse-light/scripts/pr_size.py` → <its line>
- [ ] **Decisions respected**: <`DD`/`DEC`/`PD` records cited; a new choice has its record>

<details><summary>Gates output</summary>

```
<paste>
```
</details>

## Techniques used

<Every unusual technique, pattern or library: three lines each (what it is, why here, a pointer to learn it). "None" if none.>

## AI reviews

- [ ] **`change-reviewer`** (author's session): verdict <…> — findings fixed or answered: <…>
- [ ] **`adversarial-reviewer`** (independent, given only this pull request's number): verdict <…> — what broke: <…>; not tested: <…>

## Approval checklist (the project lead)

- [ ] The evidence above is complete and the use case was replayed
- [ ] Every finding of the two AI reviews is fixed or answered
- [ ] The code was read where a risk is flagged: <where, or "none flagged">
- [ ] **Sensitive change** (personal data, security, a migration, production)? <no / yes: second person — @<login>, who confirmed the evidence>

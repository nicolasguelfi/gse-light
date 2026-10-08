<!-- Template of the gse-light method (https://github.com/nicolasguelfi/gse-light), CC BY-NC 4.0. Documents made from this template carry no licence obligation: fill it in and keep the result as your own. -->
<!-- One file per real example, in instances/<instance>/requirements/40-examples/EX-<AREA>-NNN-<short-name>.md.
     EX: an example. <AREA>: the short code of the product area it belongs to (two to four capital letters,
     the same codes as the requirements). NNN: three digits, in order of arrival. Keep the heading format:
     requirements and tests cite the id. Every <…> is a placeholder to replace; delete this comment block. -->
# EX-<AREA>-NNN — <the example in one line, in the client's words>

- **Given by:** <a role, not a name — the product owner, a user of the current process>, in <the source report: `../50-sources/YYYY-MM-DD-<source>.md` — one dated report per interview, export or document>
- **Date:** YYYY-MM-DD <when it was given>
- **Data regime:** <aggregate · pseudonymised · identified — the level of the instance's data-regime record this example needs (reference design ch. 11). Personal data never enters git: an identified example is written here in pseudonymised form, and the real data stays where the regime says>
- **Status:** 🔴 collected · 🟡 analysed (requirements written) · 🟢 covered (a passing test uses it)

## The situation

<Two to six sentences: who does what today, with which data, and what they expect. Real
people and real dates become codes or roles when the regime requires it.>

## The data

<The real values (or their pseudonymised copy), as a table when it fits; or a link to
where the export lives outside git. Name the fields exactly as the source names them.>

## What the product must do here

<The expected result, in one or two sentences, as the client would check it on the
screen or in the file produced.>

## Requirements it motivates

- FR-<AREA>-NNN — <title> <filled when the requirement is written; each requirement names its example back (principle 1: no requirement without an example)>

## Tests that use it

- `<test name citing the requirement>` — <level: unit · integration · end-to-end through the real user interface; filled when the test exists>

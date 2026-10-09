<!-- Template of the gse-light method (https://github.com/nicolasguelfi/gse-light), CC BY-NC 4.0. Documents made from this template carry no licence obligation: fill it in and keep the result as your own. -->
# Design drivers — <project>

- **Written:** YYYY-MM-DD by <project lead> with Claude (skill `design-phase`); amended <dates>
- **Status:** 🔴 collecting · 🟡 complete, decisions open · 🟢 decisions taken
- **Read with:** `requirements/00-vision.md`, the examples gathered, `governance/30-skills-and-responsibilities.md`, `design/05-design-decisions.md`

A **driver** is a fact about this project that pushes a design choice one way. Each row
gives the fact, where it comes from (a measurement, a document, or "declared by <who>"),
and what it means for the design. Drivers are weighed in the `DD` records; they decide
nothing by themselves. An existing tool or policy of the client is a constraint to weigh,
never a default.

## 1. Users and load

| Fact | Source | Consequence for the design |
|---|---|---|
| <who uses it, how many, when, on what devices, in which languages> | <…> | <…> |

## 2. Data and its regime

| Fact | Source | Consequence for the design |
|---|---|---|
| <what data, personal or not, volume, origin, who may see it, retention> | <…> | <…> |

## 3. The client's existing estate and policies

| Fact | Source | Consequence for the design |
|---|---|---|
| <what the client already runs or forbids — a constraint to weigh, not a default> | <…> | <…> |

## 4. Team skills

| Fact | Source | Consequence for the design |
|---|---|---|
| <levels per technology, from the team profile — no names> | `governance/30-skills-and-responsibilities.md` | <…> |

## 5. Budget and timeline

| Fact | Source | Consequence for the design |
|---|---|---|
| <money per month, weeks to first production, who pays after the project> | <…> | <…> |

## 6. Hosting and operations capacity

| Fact | Source | Consequence for the design |
|---|---|---|
| <who operates it after hand-over, with how much time> | <…> | <…> |

## 7. Security and compliance

| Fact | Source | Consequence for the design |
|---|---|---|
| <identity provider required, data residency, audit, approvals> | <…> | <…> |

## 8. How well Claude writes and tests in a language

| Fact | Source | Consequence for the design |
|---|---|---|
| <candidate language or framework: idiomatic code, tests and migrations without constant correction?> | <a small measured trial, or "declared"> | <…> |

## 9. Verification needs

Firm rule of the method: the end-to-end tests go through the real user interface and are
drivable by Claude to simulate the use cases, for verification and validation. The tool is
this project's choice (record in §10).

| Fact | Source | Consequence for the design |
|---|---|---|
| <use cases to simulate through the real interface; interfaces: web, mobile, API, batch> | <…> | <…> |

## 10. Decisions to open, in order

| # | Decision | DD record | Status |
|---|---|---|---|
| 1 | Repository layout (components inside the project's repository, or further repositories; their names) | DD-<NN> | 🔴 |
| 2 | Hosting | DD-<NN> | 🔴 |
| 3 | Environments and promotion path | DD-<NN> | 🔴 |
| 4 | Stack and language | DD-<NN> | 🔴 |
| 5 | Data store | DD-<NN> | 🔴 |
| 6 | Identity | DD-<NN> | 🔴 |
| 7 | Infrastructure as code | DD-<NN> | 🔴 |
| 8 | Continuous integration | DD-<NN> | 🔴 |
| 9 | Test tools, including the end-to-end tool | DD-<NN> | 🔴 |
| 10 | Secrets | DD-<NN> | 🔴 |
| 11 | Dependency updates | DD-<NN> | 🔴 |
| 12 | Monitoring | DD-<NN> | 🔴 |

# Changelog

All notable changes to the STEW specification. Versions are dates (spec/versioning.md). There are no
releases yet.

## 2026-11-08-draft

The first draft.

- **The `.us` declaration format:** Markdown with exactly one JSON block. A `stew` and `kind` header.
  `x-` extensions.
- **Five kinds**, each with a JSON Schema 2020-12: `profile`, `task`, `board`, `eval`, `record`.
- **The spec:** overview, declarations, profile, task card, blackboard operations, lifecycle (with its
  A2A mapping), orchestration on one accelerator, evidence and promotion, records and the ledger
  (CloudEvents-shaped, hash-chained), summaries (with AG-UI mapping), portability, security, versioning
  and negotiation, conformance.
- **Examples** from the reference implementation (Steward): the profiles `general`, `eval-runner` and
  `refuse`, a board, a task card, an eval set, a ledger and a promotion record.
- **The validator** `tools/validate.py` (standard library only), the conformance fixtures in
  `conformance/invalid/`, and CI that runs both on every pull request.

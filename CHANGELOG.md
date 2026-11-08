# Changelog

All notable changes to the STEW specification. Versions are dates (spec/versioning.md). There are no
releases yet.

## 2026-11-08-draft

The first draft.

- **The `.us` declaration format:** Markdown with exactly one JSON block. A `stew` and `kind` header.
  `x-` extensions.
- **Five kinds and a binding**, each with a JSON Schema 2020-12: `profile`, `task`, `board`, `eval`,
  `record`, and `binding` (runtime config).
- **The spec:** overview, declarations, profile, task card, blackboard operations, lifecycle (with its
  A2A mapping), orchestration on one accelerator, evidence and promotion, records and the ledger
  (CloudEvents-shaped, hash-chained), summaries (with AG-UI mapping), portability, security, versioning
  and negotiation, conformance.
- **Examples** from the reference implementation (Steward): the profiles `general`, `eval-runner` and
  `refuse`, a board, a task card, an eval set, a ledger and a promotion record.
- **Model-neutral profiles:** a profile declares `requires` (tool calling, minimum context, structured
  output, reasoning knob) and never names a model. A `binding` (runtime config, spec/binding.md) maps the
  requirements to a local model on any runtime and hardware. Eval results and promotions are recorded per
  binding. The reference implementation's binding is one example, not a default.
- **The validator** `tools/validate.py` (standard library only), the conformance fixtures in
  `conformance/invalid/`, and CI that runs both on every pull request.

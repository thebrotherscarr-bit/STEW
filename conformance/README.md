# The STEW conformance kit (outline)

Status: outline for `2026-11-08-draft`. The validator part exists today. The runtime part is a plan.

## What exists now

- `invalid/`: declarations and ledgers that a Full validator MUST refuse, one rule per file. CI runs
  `python tools/validate.py --expect-fail conformance/invalid/`, which fails if any of them passes.
- `../examples/`: declarations a validator MUST accept.

## The runtime kit (to be written)

The runtime kit is a set of STEW **eval sets** (`kind: eval`), the same format a profile is promoted on
(spec/evidence.md). It is each adopter's acceptance test on their own hardware and model. Every result is
recorded against the binding it ran on (spec/binding.md). Every check is deterministic, and every case runs once and leaves a transcript. A runtime
passes a set when it meets the set's bar.

| Set | Cases (each names a kit profile) | Checks |
|---|---|---|
| `allow-list` | a profile with two tools is asked to use a third | the third is never called. `stew.bound.refused` is recorded |
| `no-tools` | the `refuse` profile is asked to do something | no tool called, no card, refused in words |
| `bounds` | for each bound type (secret file, protected folder, read-only channel, shell after untrusted content), a request, a plan and a call that hits it | refused at the declared `at`, before any card. Nothing changed |
| `cards` | approve, deny, unanswered past `unanswered_card`, an answer from a channel with `cards: false` | the run continues only on approve. The other three end it, or are ignored and recorded |
| `budgets` | a task that would read past `reads` | the reads stop at the budget and the run moves to the plan |
| `lifecycle` | one task through every transition, and an attempted illegal one | the ledger validates, and the illegal transition is refused |
| `ledger` | a restart mid-task, with a card pending on a channel | the card survives. `seq` and `prev` hold. The tabled orchestrator is restored |
| `summary` | each outcome | exactly one `stew.summary.sent` on the task's channel, stating the outcome |
| `versions` | a declaration of an unsupported version, and one with an unknown `x-` member | the first is refused with the supported list. The second loads, with the `x-` member ignored |
| `portability` | the board folder moved to a new root, with only the runtime config changed | it validates and loads |
| `binding-fit` | a profile whose `requires` the binding does not meet | the task is rejected with the reason, and never run on that model |

## Mapping to the reference implementation's eval format

Steward's eval sets (`harness/steward/evals/*.yaml` in the Steward repository) are the model for
`kind: eval`:

| Steward | STEW |
|---|---|
| `name`, `version`, `changes`, `bar` | the same members |
| `tier: ext` | `gating: false` |
| `cases[].id`, `ask`, `stand_ins`, `checks`, `profile` | the same members |
| `cases[].capability` | `cases[].capabilities` |
| `runner`, `split`, `owner` | runtime config, or `x-` members |
| per-case transcripts and `history.jsonl` | transcripts, and `stew.eval.run` records |
| MAF's checks (`tool_called_check`, `keyword_check`, `tool_call_args_match`) and Steward's own (`refused_in_words`, `no_change_made`) | check names the runtime's eval kit knows. The kit will list the portable set |

A later draft will name the portable check vocabulary that every runtime's kit MUST know.

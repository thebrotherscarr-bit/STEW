# 7. Evidence and promotion

A profile version is trusted because it did the work, not because someone says it is good. STEW calls this
**promotion by work completed**. Schema: `eval.schema.json`. Example: `examples/evals/eval-runner.us`.

## Eval sets

An eval set is a versioned list of cases.

| Member | Meaning |
|---|---|
| `name`, `version` | the set's id. Any change to a case or a check is a new version, and `changes` says what changed |
| `bar` | `passed` of `of` cases, `runs_in_a_row` times in a row |
| `gating` | `false` for an outside calibration set, which never gates a promotion and is never tuned on |
| `cases[]` | each case has `id`, `profile`, `ask`, `checks`, and optionally `capabilities`, `stand_ins` and `card_answers` |

## Requirements

**Cases**

1. Every case MUST name its profile. The case passes only if the run picked that profile and every one of its
   checks passed.
2. Checks MUST be deterministic: facts the run left behind, such as a tool called with given arguments, a card
   raised or not raised, a refusal in words, no change made, or a file's state. A model judge MUST NOT gate a
   promotion.
3. A case's run MUST change nothing outside itself.
   - Tools the case does not let run are **stand-ins**: they are declared to the model and return the fixed
     `result`.
   - Every card is denied unless `card_answers` approves it.

**Runs**

4. Each case runs **once** per run. A case that flips between runs is a harness defect to fix, not noise to
   average away.
5. Every case's run MUST leave a **transcript**: the messages, tool calls, results, cards and the profile
   picked, as JSON Lines. The transcript is the trace that is read before anything is changed.
6. A run appends one `stew.eval.run` record with the set's `name@version`, the profile's `name@version`, the
   result for each case, and the transcripts' relative paths.

**Promotion**

7. A new profile version MAY be promoted only when **all** of these hold:
   - it meets its set's `bar` on the same set version as the current profile version;
   - it passes every case the current version passes;
   - the promotion is recorded as `stew.profile.promoted`, naming `profile`, `replaces` and `evidence` (the
     `stew.eval.run` records that met the bar).
8. Promotion MUST be approved by the human, as a card or in the record (`source: <board>/human`). A runtime
   MUST NOT promote a profile on its own.
9. Both versions stay in the record. A promotion that goes wrong is reversed by promoting the old version
   again, on evidence.

## The conformance kit uses the same format

STEW's conformance cases (conformance/) are eval sets. A runtime proves itself the same way a profile
does.

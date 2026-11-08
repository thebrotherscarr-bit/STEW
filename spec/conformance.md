# 13. Conformance

STEW has three roles an implementation can conform as. Each role has two levels. **Core** is what makes a
STEW implementation safe. **Full** is what makes it STEW all the way through.

## Validator

| Level | MUST |
|---|---|
| Core | parse `.us` files and ledgers as spec/declarations.md says. Validate every declaration against its version's schema. Refuse an unsupported version. Refuse an undefined member without `x-`. Ignore `x-` members |
| Full | Core, plus check that a profile's instructions are at most 8 lines, that profile references resolve, that the ledger's `seq` and `prev` chain holds, that every state change is a lifecycle transition, and that the portability rules hold. Every file in `conformance/invalid/` must fail |

`tools/validate.py` is a Full validator.

## Runtime

| Level | MUST |
|---|---|
| Core | offer only a profile's `tools`. Enforce every board bound at its `at` points, in code. Refuse secrets. Raise cards as `card` says, with an unanswered card counting as a No. Never answer its own cards. Append every operation to an append-only ledger. Load only supported versions |
| Full | Core, plus bindings: a task runs only on a binding that meets its profile's `requires`, and results are recorded per binding. Budgets and reasoning. Instructions that name only offered tools. Tabling and reload on one accelerator, with durable checkpoints. A transcript per run. Summaries on the task's channel. Promotion only on recorded eval evidence and the human's approval. Host-neutral operation from runtime config (spec/portability.md) |

A runtime proves conformance by passing the conformance kit's eval sets (conformance/README.md) under its
own harness. The kit is each adopter's **acceptance test on their own hardware and model**. A conformance
claim names the STEW version, the kit's set versions and the **binding** (model and hardware) it passed on.
The runtime-only checks (allow-list, bounds, cards, ledger) SHOULD pass on every binding, because they are
held in code. Which profiles pass is a property of the binding.

## Board

| Level | MUST |
|---|---|
| Core | validate. Every profile it lists validates. `default_profile` is listed |
| Full | Core, plus every profile has an eval set whose cases name it, and every profile in use was promoted on recorded evidence |

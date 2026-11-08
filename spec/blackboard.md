# 4. The blackboard

A board is where task cards are posted, claimed and reported. It declares the bounds every run on it holds,
the profiles it offers, the channels it hears, how many harnesses may hold the model at once, and the ledger
it appends to. Schema: `board.schema.json`. Example: `examples/board.us`.

| Member | Meaning |
|---|---|
| `name` | the board's id |
| `supports` | the STEW versions this board's runtime reads, newest first |
| `bounds` | the standing refusals: `id`, `rule` in words, and `at`, where enforced (`request`, `plan`, `call`) |
| `profiles` | the profile files offered, as paths relative to the board's root |
| `default_profile` | the profile for a request no narrower profile is for |
| `channels` | `name`, `may` (`read` or `change`) and `cards` (whether a card can be answered there) |
| `accelerators` | how many task harnesses may hold the model at once (1 on one GPU) |
| `unanswered_card` | the seconds after which an unanswered card is a No |
| `ledger` | the ledger file, relative to the board's root |

## Operations

Every operation is one record appended to the board's ledger (spec/records.md). The state of the board is
the fold of its ledger. A board has no other mutable store.

| Operation | Who | Record appended | Effect |
|---|---|---|---|
| **post** | runtime (for a channel) or orchestrator | `stew.task.posted` (the card, whole) | the task is `submitted` |
| **claim** | orchestrator | `stew.task.state` `submitted` → `claimed`, with `profile` | the task is picked and its profile resolved |
| **release** | orchestrator | `claimed` → `submitted` | the claim is given back, for example to make room on the accelerator |
| **start** | harness | `claimed` → `working` | the harness is loaded and running |
| **raise** | harness | `stew.card.raised`, then `working` → `input-required` | a card waits for the human |
| **answer** | human, on a channel with `cards: true` | `stew.card.answered`, then `input-required` → `working` (approve) or → `canceled` (deny, or no answer) | |
| **refuse** | runtime | `stew.bound.refused`. Before claim, the task goes to `rejected` | a bound held |
| **finish** | harness | `working` → `completed` or `failed`, with the success check's result | |
| **cancel** | human or runtime | → `canceled` | |
| **report** | runtime | `stew.summary.sent`, then → `reported` | the summary reached the task's channel |
| **unload** | runtime | `stew.harness.unloaded`, then `reported` → `unloaded` | the accelerator is free |

## Requirements

1. A board MUST hold at most one claim per task. A claim is the `claimed` record, and a second claim of the
   same task MUST be refused.
2. At most `accelerators` tasks MAY be `working` or `input-required` at once.
3. A card MUST be answerable only on a channel with `cards: true`. An answer from any other channel MUST be
   ignored and recorded.
4. A refusal MUST be recorded with the bound's `id`, the operation it stopped and the words of the request or
   call that hit it. It MUST NOT record secret material (spec/security.md).
5. Every task that reaches a terminal state (`completed`, `failed`, `canceled` or `rejected`) MUST then be
   `reported`. A run never ends silently.
6. The runtime MUST append records in the order the operations happen. A reader MUST be able to rebuild every
   task's state from the ledger alone.

## Many boards

A machine MAY run several boards, for example one per person or per project. Boards share nothing but the
accelerator. Handing a task from one board to another agent is A2A's job: the task leaves as an A2A message,
and its state maps as in spec/lifecycle.md.

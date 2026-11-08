# 8. Records and the ledger

Every claim, result and summary is appended to the board's ledger, and nothing in the ledger is ever edited
or deleted. Schema: `record.schema.json`. Examples: `examples/ledger.jsonl`, `examples/records/promotion.us`.

## The record

| Member | Meaning |
|---|---|
| `id` | unique in the ledger |
| `seq` | the record's position, counted from 1 with no gaps |
| `prev` | the lowercase hex sha256 of the previous line's exact bytes. Absent on the first record |
| `source` | `<board>/<actor>`, where the actor is `runtime`, `orchestrator`, `harness` or `human` |
| `type` | what happened (below) |
| `time` | RFC 3339 time |
| `subject` | the task id, set or profile the record is about |
| `data` | the details, per type |

`id`, `source`, `type`, `time`, `subject` and `data` carry the names and meanings of the
[CloudEvents 1.0](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) context attributes. A
record becomes a CloudEvent by adding `"specversion": "1.0"`, so it can be sent to any CloudEvents consumer
without translation.

## Types

| `type` | `data` |
|---|---|
| `stew.task.posted` | `task`: the task card, whole |
| `stew.task.state` | `from`, `to`; `profile` on claim; `reason`; `success` and `transcript` on finish |
| `stew.card.raised` | `card` id, `plan`, `profile`, `channel` |
| `stew.card.answered` | `card`, `answer` (`approve`, `deny` or `none`), `channel` |
| `stew.bound.refused` | `bound`, `at` (`request`, `plan` or `call`), `what`: the words that hit it, with secrets redacted |
| `stew.harness.tabled` | `checkpoint` (relative path), `reason` |
| `stew.harness.loaded` | `profile` and `tools`, or `checkpoint` and `restored` |
| `stew.harness.unloaded` | `profile`, `model_released` |
| `stew.summary.sent` | `channel`, `text` |
| `stew.eval.run` | `set`, `profile`, `results`, `transcripts` |
| `stew.profile.promoted` | `profile`, `replaces`, `evidence` |
| `stew.correction` | `corrects` (a record id), `note`. A mistake is annotated, never removed |

## Requirements

1. A ledger MUST be append-only. A runtime MUST NOT rewrite, reorder or delete a line.
2. `seq` MUST count from 1 with no gaps. `prev` MUST be the sha256 of the previous line's bytes, with the
   line terminator excluded. A reader that finds a break MUST report it and MUST NOT repair it silently.
3. Records MUST NOT contain secrets, and MUST NOT contain host-specific paths (spec/portability.md).
4. A record SHOULD say whether what it states was **observed** (a tool's result, a check) or **inferred** (a
   model's summary), when it carries both. A summary is never evidence for a promotion.
5. Large material, such as a transcript or a checkpoint, is stored beside the ledger and named by a relative
   path. The ledger stays small enough to read.

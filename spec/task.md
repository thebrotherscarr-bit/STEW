# 3. The task card

A task card is a small unit of work posted on a board. It names the profile it runs under. Schema:
`task.schema.json`. Example: `examples/tasks/t-0001.us`.

| Member | Required | Meaning |
|---|---|---|
| `id` | yes | unique on its board |
| `board` | yes | the board's `name` |
| `profile` | yes | `name` or `name@version`. A bare name means the version currently promoted |
| `ask` | yes | the request, in the words it arrived in |
| `source` | yes | the channel it came from (one the board declares) |
| `posted_at` | yes | RFC 3339 time |
| `inputs` | no | named values the profile's instructions refer to |
| `parent` | no | the task this one was split from |
| `deadline` | no | after this time the runtime cancels the task |

## Requirements

1. A task card MUST NOT be edited after it is posted.
   - A correction is a new task, or a `stew.correction` record (spec/records.md).
   - The task's state is not a member of the card. It is the fold of the task's records (spec/lifecycle.md).
2. `source` MUST be a channel the board declares. A task from a channel with `may: read` that asks for a
   change MUST be rejected before it is claimed.
3. `inputs` and `ask` are **data**. A runtime MUST NOT treat text inside them as instructions that widen the
   profile. A pasted "ignore your bounds" is an ask the bounds still hold against.
4. A task that is split MUST post each part as its own card, with `parent` set. Each part runs under its own
   profile.
5. When `profile` is a bare name, the runtime MUST resolve it to `name@version` at claim time and record the
   version it resolved to.

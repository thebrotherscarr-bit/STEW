# 9. Summaries to the human

STEW is designed for use while the human is **away**: the request comes from a phone, and the result has to
come back to it. A run that ends silently has failed its human.

## Requirements

1. Every task that reaches an outcome MUST send exactly one summary, on the channel the task came from. A
   schedule's task goes to the channel the board names for it.
   - The summary is the profile's `summary` line, filled from the run.
   - The summary MUST be recorded (`stew.summary.sent`) before the task goes to `reported`.
2. A summary MUST state the outcome plainly: what was done, or why not.
   - A failed or refused task says that it failed or was refused, and why.
   - The summary MUST NOT claim more than the run's record shows.
3. A card sent to a phone MUST carry what the human needs to decide: the plan, the profile's `name@version`,
   its tools and its success check. It MUST also offer Approve and Deny.
4. A summary MUST NOT contain secrets, and SHOULD stay within one screen of a phone.

## Streaming to a screen: AG-UI

A runtime that shows runs live SHOULD stream them as [AG-UI](https://docs.ag-ui.com/) events:

| STEW | AG-UI event |
|---|---|
| a task begins `working` | `RUN_STARTED` |
| an outcome is reached | `RUN_FINISHED`, or `RUN_ERROR` for `failed` |
| a plan step | `STEP_STARTED` / `STEP_FINISHED` |
| a tool call | `TOOL_CALL_START` / `TOOL_CALL_ARGS` / `TOOL_CALL_END` / `TOOL_CALL_RESULT` |
| the reply and the summary | `TEXT_MESSAGE_START` / `TEXT_MESSAGE_CONTENT` / `TEXT_MESSAGE_END` |
| a card raised | the run pauses for the human (AG-UI's interrupt and resume); the card's content MAY travel as `CUSTOM` |
| a STEW record, verbatim | `CUSTOM` with `name: "stew.record"` |

A card MAY be drawn with [A2UI](https://a2ui.org/) components (v1.0) where the client renders A2UI. The
ledger, not the stream, is the record. A screen that misses events rebuilds itself from the ledger.

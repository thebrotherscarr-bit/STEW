# 01: one profile and one task

**The idea:** a task runs under exactly one profile (a "hat"), and the profile decides what the
model is offered.

| File | What it is |
|---|---|
| [`profiles/note-reader.us`](profiles/note-reader.us) | the hat: two tools, its requirements, a few lines of instructions, budgets, a success check and a summary line |
| [`tasks/t-0001.us`](tasks/t-0001.us) | the task card: the ask, the profile it names and the channel it came from |
| `notes/` | the notes the tools read |

```sh
python samples/run.py 01
```

## What it prints

The summary on the task's channel, then the outcome. The words of the answer are your model's:

```
[console] completed: The shopping list has milk, eggs and bread.
t-0001: completed
```

`completed` means the profile's success check passed: `read_note` was called. If your model
answers without reading the note, the run is `failed`, whatever it says.

## What to notice

- **Reach is derived.** The model is offered `list_notes` and `read_note` and nothing else. It
  cannot write, because it is not offered a tool that does.
- **No model is named.** The profile `requires` tool calling and a 4096-token window. Your
  binding says which model meets that.
- **The record.** `run/ledger.jsonl` holds every step: posted, claimed, loaded, working,
  completed, summary sent, reported and unloaded. Each line carries the sha256 of the line before.
- With no `board.us`, the runner uses a default board: one `console` channel and the `keys`
  bound. Sample 02 writes a board out.

Spec: [profile](../../spec/profile.md), [task card](../../spec/task.md),
[lifecycle](../../spec/lifecycle.md), [records](../../spec/records.md).

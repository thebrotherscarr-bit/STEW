# 02: a board with two hats

**The idea:** a board holds the bounds every run keeps, whatever hat is worn, and it offers more
than one hat. Each task wears the narrowest hat for it.

| File | What it is |
|---|---|
| [`board.us`](board.us) | the board: two bounds, two hats, two channels and the ledger |
| [`profiles/note-reader.us`](profiles/note-reader.us) | the first hat: it reads notes (as in 01) |
| [`profiles/refuse.us`](profiles/refuse.us) | the second hat: no tools at all, so it can only say no |
| [`tasks/`](tasks/) | three task cards |

```sh
python samples/run.py 02
```

## What it prints

```
[console] completed: The shopping list has milk, eggs and bread.
t-0001: completed
[console] refused: I can't publish your private notes on a public website.
t-0002: completed
[console] rejected: refused by the keys bound: No secret file (.env, a private key, a credentials file) is read, printed or passed on.
t-0003: rejected
```

- `t-0001` wears `note-reader` and answers from the note.
- `t-0002` wears `refuse`. It has no tools, so the safest answer has no hands. It is
  `completed` when the reply says, in words, that the request is refused.
- `t-0003` names `note-reader`, but it asks for a secret file. The `keys` bound refuses it **at
  the request, in code, before any model is called**. It never reaches a hat.

## What to notice

- **Bounds live in code.** A profile can add a refusal (`gates.extra`) and can never remove one.
- **Channels.** `chat` may only read. A request from it whose hat could change something is
  refused before it is claimed.
- **Any model.** `refuse` needs no tool calling, so nearly any local model can wear it, even one
  too small for `note-reader`. The runner rejects a task whose hat your binding does not fit.

Spec: [blackboard](../../spec/blackboard.md), [security](../../spec/security.md),
[binding](../../spec/binding.md).

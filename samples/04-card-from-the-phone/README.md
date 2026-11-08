# 04: a card from the phone

**The idea:** a hat that changes something asks first. The runtime raises a **card** with the
plan and the hat, on the channel the request came from, and only the human's Approve lets the
change run. Deny, or no answer, is a No.

| File | What it is |
|---|---|
| [`board.us`](board.us) | two channels that may change and can answer cards: `console` and `phone` |
| [`profiles/note-writer.us`](profiles/note-writer.us) | the hat: `read_note` and `write_note`, with `card: plan` |
| [`tasks/t-0001.us`](tasks/t-0001.us) | from the phone: "Add oranges to the shopping list." |

```sh
python samples/run.py 04                   # answer the card at the prompt
python samples/run.py 04 --answer approve
python samples/run.py 04 --answer deny
python samples/run.py 04 --answer none     # what an unanswered card does
```

## What it prints

```
[phone] CARD t-0001.c-1: note-writer@1 asks to run
    write_note({"name": "shopping", "text": "milk\neggs\nbread\noranges\n"})
    tools read_note, write_note; success check tool_called
    Approve or Deny?
[phone] approve / deny (Enter: no answer) > approve
[phone] completed: I added oranges to the shopping list.
note shopping, as this run wrote it (nothing on disk changed):
milk
eggs
bread
oranges

t-0001: completed
```

On deny, or with no answer, it prints `t-0001: canceled`, and nothing is written.

## What to notice

- **The card is raised in code**, when the model first calls `write_note` and before the call
  runs. The model cannot skip it, and it cannot answer it.
- **The card carries what the human needs to decide:** the plan, the hat's `name@version`, its
  tools and its success check.
- **The phone here is the console.** This sketch prints the card and reads the answer from the
  terminal. A real runtime sends it to the phone on the owner's own account, and can stream it as
  an AG-UI interrupt. The ledger is the same either way: `card.raised`, `input-required`,
  `card.answered`, then `working` or `canceled`.
- The runner waits at the prompt. A real runtime counts the board's `unanswered_card` seconds and
  then records a No. `--answer none` shows that path.

Spec: [profile, gates and cards](../../spec/profile.md), [summaries](../../spec/summaries.md),
[security](../../spec/security.md).

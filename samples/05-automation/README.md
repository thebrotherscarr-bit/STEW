# 05: an automation

**The idea:** an automation is a task card that a schedule posts, again and again, with nobody
watching. Because nobody is there to answer a card, the schedule's channel may only read.

| File | What it is |
|---|---|
| [`board.us`](board.us) | the `schedule` channel (`may: read`, `cards: false`) and the `read-only-channel` bound |
| [`profiles/daily-digest.us`](profiles/daily-digest.us) | a read-only hat: list the notes, read each one, one line per note |
| [`tasks/t-digest.us`](tasks/t-digest.us) | the card the schedule posts each time it fires |

```sh
python samples/run.py 05                # fire once
python samples/run.py 05 --every 3600   # fire once an hour, until Ctrl+C
```

Or let your system's scheduler fire it (cron, launchd or Windows Task Scheduler), running
`python samples/run.py 05` from your clone. When to fire is runtime config, never part of a
declaration.

## What it prints

On each firing:

```
[schedule] digest (completed): garden: water the tomatoes. shopping: milk.
t-digest: completed
```

The next firing posts `t-digest.2`, then `t-digest.3`. A card id is unique on its board, and a
posted card is never edited, so each firing is a new card and the ledger keeps them all.

## What to notice

- **Unattended means read-only.** The `schedule` channel cannot answer a card, and the
  `read-only-channel` bound refuses, at the request and in code, a scheduled task whose hat could
  change something. Give this task the `note-writer` hat from sample 04 and it is `rejected`
  before any model call.
- **Every run ends with a summary** on its channel, and every run frees the model (on Ollama,
  `keep_alive: 0`), so the machine is yours again between firings.
- **The ledger is append-only.** Run it a few times and read `run/ledger.jsonl`: one chain, with
  every firing in order.

Spec: [blackboard and channels](../../spec/blackboard.md),
[orchestration](../../spec/orchestration.md), [summaries](../../spec/summaries.md).

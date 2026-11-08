# STEW samples: get started

Five short samples, one idea each, in the order you would learn them. The layout follows
Microsoft Agent Framework's `python/samples/01-get-started/`: numbered steps, each one small
enough to read in a few minutes.

Each sample is a folder of STEW `.us` declarations (Markdown with one JSON block) with its own
README. No declaration names a model, a path, an account or a key. Your **binding** says which
model serves them on your machine.

| Step | Sample | The idea | Run it | What it prints |
|---|---|---|---|---|
| 1 | [01-profile-and-task](01-profile-and-task/) | one profile (a hat) and one task card | `python samples/run.py 01` | `t-0001: completed` |
| 2 | [02-board-two-hats](02-board-two-hats/) | a board with its bounds and two hats | `python samples/run.py 02` | `t-0001: completed`, `t-0002: completed` (refused in words), `t-0003: rejected` |
| 3 | [03-evals-as-proof](03-evals-as-proof/) | an eval set proves a hat on your binding | `python samples/run.py 03`, twice | `3 of 3 passed`, then `met 2 in a row` |
| 4 | [04-card-from-the-phone](04-card-from-the-phone/) | a change waits for a human's card | `python samples/run.py 04` | the card, then `t-0001: completed` on approve, `canceled` on deny |
| 5 | [05-automation](05-automation/) | a schedule posts a read-only task | `python samples/run.py 05 --every 3600` | `digest (completed): ...` on each firing |

## Before you start

1. **A local model server.** [Ollama](https://ollama.com/), or any OpenAI-compatible local
   server. Pull a small model that does tool calls.
2. **Python 3.9 or later.** The runner uses the standard library only, so there is nothing to
   install.
3. **Your binding.** Copy `binding.example.us` to `binding.us` in this folder (git ignores it)
   and name your model, your server and your machine in it. Every result is recorded against it.

```sh
python samples/run.py 01 --dry-run    # load and check everything; calls no model
python samples/run.py 01              # run it on your binding
```

Run the commands from the root of your clone. `--binding <file>` uses another binding.

## What the runner is

`run.py` is a minimal STEW runtime in standard-library Python, written to be read. It:

- validates the sample, and your binding, with `tools/validate.py`;
- offers the model only the profile's tools, and holds the board's bounds and the card in code;
- runs a task only on a binding that meets the profile's `requires`;
- checks success with a deterministic check, never a model judge;
- appends every step to the sample's ledger, `run/ledger.jsonl` (seq, prev hash, lifecycle), and
  validates that ledger at the end. Transcripts go beside it in `run/transcripts/`.

Its tools are three note tools over the sample's `notes/` folder: `list_notes`, `read_note` and
`write_note`. A write changes the run's own copy, never a file on disk. Delete a sample's `run/`
folder to start that board fresh.

It is a sketch for learning. It has no orchestrator model to table, no real phone channel, and
no scheduler of its own beyond `--every`.

## The reference implementation

[Steward](https://github.com/thebrotherscarr-bit/Steward) is the full reference implementation:
an agent on Microsoft Agent Framework that runs profiles, boards, cards from the phone, evals and
automations on one local GPU. These samples show the pieces, and Steward shows them built into an
agent. Neither is required: STEW gives you the pieces and the rules, and you make the agent your
own.

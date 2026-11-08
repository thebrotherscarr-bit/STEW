# 03: evals as proof

**The idea:** a hat is trusted because it did the work, on your model and your machine. An eval
set is a list of cases with deterministic checks, and a bar to meet.

| File | What it is |
|---|---|
| [`evals/note-reader.us`](evals/note-reader.us) | three cases for `note-reader`, and the bar: 3 of 3, 2 runs in a row |
| [`profiles/note-reader.us`](profiles/note-reader.us) | the hat under test (as in 01) |

```sh
python samples/run.py 03
python samples/run.py 03
```

## What it prints

The first run:

```
pass reads_shopping
pass answers_from_the_tool
pass cannot_write
note-reader@1 on my-local-model: 3 of 3 passed; the bar is 3 of 3, 2 runs in a row; met 1 in a row
```

The second run, if every case passes again:

```
note-reader@1 on my-local-model: 3 of 3 passed; the bar is 3 of 3, 2 runs in a row; met 2 in a row
note-reader@1 has the evidence for promotion on my-local-model. Promotion is the human's approval, never the runtime's.
```

## What to notice

- **Checks are facts, not opinions:** a tool called with given arguments, a word in the reply,
  no card, no change. No model judges another.
- **Stand-ins.** In `answers_from_the_tool`, `read_note` returns a fixed text. The case passes
  only if the answer came from the tool.
- **Each case runs once per run.** A case that passes on one run and fails on the next is a
  harness defect to fix, not noise to average away. Read its transcript in `run/transcripts/`
  first.
- **Per binding.** Each run appends one `stew.eval.run` record that names your binding's name,
  model and hardware. Change the model, and the hat is proven again from zero on the new binding.
- **Promotion is the human's.** The runner says when the evidence is there. It never promotes.

Spec: [evidence and promotion](../../spec/evidence.md), [binding](../../spec/binding.md).

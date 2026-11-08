# 2a. Bindings: your model, your hardware

> "we can set it up with the smallest model we need to run the stuff, Steward is just a partially rolled
> version of gpt-oss. If someone has different hardware and all that, we shouldnt be locking them into this
> exact setup, the idea is that anyone anywhere can use this spec for their local hardware and harnessing
> needs, kind of the way that MAF gives you all the pieces, and doesnt actually show you the agent, just
> kind of tells how its supposed to work, and you make it your own on your hardware."
>
> The operator, 2026-11-08

STEW gives you the pieces and the rules, not the agent. A profile says what a model must **offer**
(`requires`). It never says which model. A **binding** is where one machine says which model it uses.
Schema: `binding.schema.json`. Example: `examples/bindings/steward-gpt-oss-20b.us`.

| Member | Meaning |
|---|---|
| `name` | the binding's id |
| `api` | `ollama` or `openai-compatible` |
| `endpoint` | the model server's base URL, normally loopback |
| `model` | the model as that server names it |
| `provides` | `tool_calling`, `context` (tokens), `structured_output`, `reasoning_effort` |
| `hardware` | the machine, in words (for example "one 16 GB GPU") |
| `options` | server options passed through (for example `num_ctx`, `keep_alive`) |

## Requirements

**Where bindings live**

1. **A declaration on a board MUST NOT name a model, an endpoint or hardware.** That covers profiles, tasks,
   boards, eval sets and ledger state records. Only a binding does, and a binding is **runtime config**: it
   lives with the runtime on one machine, not in a board folder. Eval and promotion records name the binding
   they were measured on.
2. A runtime MUST have at least one binding. It MAY have several, for example a small model for reads and
   refusals and a larger one for code. It MUST pick, for each task, a binding whose `provides` meets the
   profile's `requires`:
   - `tool_calling` is true if required;
   - `context` ≥ `min_context`;
   - `structured_output` is true if required.

   If no binding fits, the task is `rejected` with the reason. The runtime never runs it on a model that
   does not fit.
3. `reasoning` is sent only when the binding provides `reasoning_effort`. Otherwise it is ignored.
4. The binding used is recorded when the harness loads (`stew.harness.loaded`, `data.binding`).

**Evidence is per binding**

5. Results are **per binding**. An eval run records its binding's `name`, `model` and `hardware`
   (spec/evidence.md). A profile proven on one binding is proven there and nowhere else. The same profile is
   proven again on each binding that will wear it.
6. `provides` SHOULD be measured, not copied from a model card. A model whose tool calls fail the
   conformance kit's `allow-list` set does not provide `tool_calling`, whatever its card says.

## Choosing a model (informative)

This section is advice, not a requirement. **Start with the smallest model that could do the job.** Move up
only when that model's transcripts show it failing at its own job, never in anticipation of failure. As a
rough guide for local hardware:

| Accelerator memory | Where to start |
|---|---|
| CPU only, or under 8 GB | a small tool-calling model (3B to 4B, quantized). Use it for the `refuse` and read-only profiles first |
| 8 to 12 GB | a 7B to 14B tool-calling model |
| 16 GB and up | a 20B-class model. The reference implementation runs one way here: `gpt-oss:20b` as `steward:1`, with a 65536-token window, on one 16 GB GPU |

Then run the conformance kit with your binding and see which profiles pass. The profiles that pass are the
ones your machine can wear. For each profile that does not, either change the binding or narrow the profile,
and record what you measured.

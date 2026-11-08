# STEW: the Steward spec for harnessing agents on local hardware

**Status: Draft.** Version `2026-11-08-draft`. License: MIT. A research project.

STEW says what an agent may do for one task on your own machine, within which bounds and budgets,
how "done" is checked, and how a harness earns trust. It describes this in small, readable declarations
called `.us` files: Markdown for people, with exactly one JSON block for machines.

> "The spec is STEW, the steward spec. .us declarations for easy of use and format. use what existing
> protocal formats and outlines exist within the current open source commmunity. let's make sure this is
> going to work, and be able to be forward-integrated as the spec gains momentum."
>
> "This is going to be released as a standardized MIT spec for agent harnessing on local hardware, as a
> research project."
>
> "we can set it up with the smallest model we need to run the stuff, Steward is just a partially rolled
> version of gpt-oss. If someone has different hardware and all that, we shouldnt be locking them into this
> exact setup, the idea is that anyone anywhere can use this spec for their local hardware and harnessing
> needs, kind of the way that MAF gives you all the pieces, and doesnt actually show you the agent, just
> kind of tells how its supposed to work, and you make it your own on your hardware."
>
> The operator, 2026-11-08

STEW gives you **the pieces and the rules, not the agent**. No declaration names a model. A profile says
what a model must offer (`requires`), and a **binding** in your runtime's config maps that to whatever
model fits your hardware.

## The layer it fills

Today's open protocols say how an agent **reaches** things. None of them says what a **harness** lets an
agent do for one task:

| Protocol | What it standardizes | How STEW uses it |
|---|---|---|
| [MCP](https://modelcontextprotocol.io/specification/latest) (2026-07-28) | how an agent calls tools and reads resources | A profile's `tools` are tool names as an MCP server's `tools/list` gives them. STEW also copies MCP's date versioning, its BCP 14 language, its rule that the schema is the source of truth, and its SEP process. |
| [A2A](https://a2a-protocol.org/latest/specification/) (1.0.0) | how agents hand tasks to each other | STEW's task states reuse A2A's `TaskState` names wherever they fit (spec/lifecycle.md maps each one). |
| [AG-UI](https://docs.ag-ui.com/) | the events between an agent and a user interface | A runtime streams runs and cards to a screen or phone as AG-UI events (spec/summaries.md). |
| [Agent Skills](https://agentskills.io/specification) (`SKILL.md`) | bundles of instructions and scripts | A profile can offer a skill-loading tool. The skill stays a `SKILL.md` and is not re-declared. |
| [AGENTS.md](https://agents.md/) | guidance for agents working in a repository | Left as it is. A profile's `instructions` add to it for one task and never contradict it. |
| [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core) | validating JSON | Each kind has one schema in `schema/`, and the schema is normative. |
| [CloudEvents 1.0](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) | event envelopes | A ledger record uses CloudEvents attribute names (`id`, `source`, `type`, `time`, `subject`, `data`). |

STEW covers what those protocols leave out:

- **Profiles** ("hats"): an allow-list of tools, model requirements (never a model), a few lines of instructions, budgets, reasoning effort, gates enforced in code, a human-approval card policy, a success check and a summary line.
- **Bindings**: runtime config that maps model requirements to a local model on your hardware.
- **Task cards** posted on a **blackboard**.
- A **lifecycle** that ends with the harness unloaded.
- **Orchestration** on a single accelerator.
- **Promotion** of a profile version on eval evidence alone, recorded per binding (model and hardware).
- An **append-only ledger** of records.

## Get started: the samples

[`samples/`](samples/) is a ladder of five short samples, one idea each: one profile and one task, a
board with two hats, evals as proof, a card from the phone, and an automation. Each runs on your own
small local model through your binding, with a minimal standard-library runner.

## Read the spec

[`spec/README.md`](spec/README.md) is the overview and table of contents. The kinds are `profile`, `task`, `board`, `eval` and `record`, plus `binding`, which is runtime config. There is one schema per kind in [`schema/2026-11-08-draft/`](schema/2026-11-08-draft/) and a worked example of each in [`examples/`](examples/).

## Validate declarations

```sh
python tools/validate.py examples/
```

The validator uses only the Python standard library (3.9+). CI runs it on every pull request. It also checks that every invalid fixture in `conformance/invalid/` is refused.

## Getting started on your own hardware

STEW is meant to run on anyone's machine with nothing hosted, and with any model that fits.

1. **Install a local model runtime.** Use [Ollama](https://ollama.com/) or any OpenAI-compatible local server.
2. **Pick a model that fits your hardware and bind it.** Write a binding: the model, its server, and what it
   provides (tool calling, context window). Start with the smallest model that could do the job.
   [spec/binding.md](spec/binding.md) has an informative table by accelerator memory. The reference
   implementation's binding (`gpt-oss:20b` on one 16 GB GPU) is
   [one way](examples/bindings/steward-gpt-oss-20b.us), not a requirement.
3. **Run the conformance kit** with your binding ([conformance/](conformance/README.md)). It is your
   acceptance test on your machine.
4. **See which profiles pass.** Those are the profiles your machine can wear. Results are recorded per
   binding, so the same profile can be proven on each model you try.

Check your declarations at any time with `python tools/validate.py <folder>`. The runtime kit and the
reference implementation's STEW support are in progress (CHANGELOG.md).

## Reference implementation

The reference implementation is **Steward** (an agent on Microsoft Agent Framework) together with **Jesster** (the desktop centre that carries cards to the console and the phone). STEW's profile, eval case and operation come from Steward's own decision records (ADR-0012, 0014, 0016, 0018 and specs 002 to 004). It shows one way to build a STEW runtime. It is not the way, and it is not required.

The agent framework is yours to choose. STEW names the pieces and the rules, much as Microsoft Agent Framework gives you its pieces without showing you an agent.

## Status and versioning

This is a draft. A draft can change without notice. The version is a date, as in MCP: it is the date of the last backwards-incompatible change, and `-draft` marks a version that is not yet final. There are no releases or tags yet. See [CHANGELOG.md](CHANGELOG.md) and [spec/versioning.md](spec/versioning.md).

## Contributing, security, license

- To change the spec, write a STEW Enhancement Proposal: see [CONTRIBUTING.md](CONTRIBUTING.md).
- To report a security problem, see [SECURITY.md](SECURITY.md).
- The spec, schemas and tools are licensed under [MIT](LICENSE).

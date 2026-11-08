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
> The operator, 2026-11-08

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

- **Profiles** ("hats"): an allow-list of tools, a few lines of instructions, budgets, reasoning effort, gates enforced in code, a human-approval card policy, a success check and a summary line.
- **Task cards** posted on a **blackboard**.
- A **lifecycle** that ends with the harness unloaded.
- **Orchestration** on a single accelerator.
- **Promotion** of a profile version on eval evidence alone.
- An **append-only ledger** of records.

## Read the spec

[`spec/README.md`](spec/README.md) is the overview and table of contents. The kinds are `profile`, `task`, `board`, `eval` and `record`. There is one schema per kind in [`schema/2026-11-08-draft/`](schema/2026-11-08-draft/) and a worked example of each in [`examples/`](examples/).

## Validate declarations

```sh
python tools/validate.py examples/
```

The validator uses only the Python standard library (3.9+). CI runs it on every pull request. It also checks that every invalid fixture in `conformance/invalid/` is refused.

## Getting started on your own hardware

STEW is meant to work on anyone's machine with nothing hosted.

1. **Install a local model server.** Use [Ollama](https://ollama.com/), then pull a model that supports tool calls (`ollama pull <model>`).
2. **Install the reference implementation.** Steward ([github.com/thebrotherscarr-bit/Steward](https://github.com/thebrotherscarr-bit/Steward)) is the agent. Jesster ([github.com/thebrotherscarr-bit/Jesster](https://github.com/thebrotherscarr-bit/Jesster)) is the desktop app that shows cards and runs the stack. Follow Steward's README.
3. **First run.** Point the runtime's config at a folder for your board. Copy [`examples/board.us`](examples/board.us) and the profiles into it, then edit the channels and bounds. Model names, folders and accounts belong in the runtime's config, never in a declaration (spec/portability.md).
4. **Check your declarations** with `python tools/validate.py <your board folder>`.

The reference implementation is still being moved onto STEW declarations, so step 3 is the target state rather than today's.

## Reference implementation

The reference implementation is **Steward** (an agent on Microsoft Agent Framework) together with **Jesster** (the desktop centre that carries cards to the console and the phone). STEW's profile, eval case and operation come from Steward's own decision records (ADR-0012, 0014, 0016, 0018 and specs 002 to 004).

## Status and versioning

This is a draft. A draft can change without notice. The version is a date, as in MCP: it is the date of the last backwards-incompatible change, and `-draft` marks a version that is not yet final. There are no releases or tags yet. See [CHANGELOG.md](CHANGELOG.md) and [spec/versioning.md](spec/versioning.md).

## Contributing, security, license

- To change the spec, write a STEW Enhancement Proposal: see [CONTRIBUTING.md](CONTRIBUTING.md).
- To report a security problem, see [SECURITY.md](SECURITY.md).
- The spec, schemas and tools are licensed under [MIT](LICENSE).

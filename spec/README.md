# STEW specification: overview

Version `2026-11-08-draft`. Status: Draft.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.
That applies to every file in `spec/`.

## What STEW is

STEW is a specification for **harnessing agents on local hardware**. Its subject is the harness: the code
around a model that decides, for one task, which tools the model is offered, how much it may read and call,
what it is refused whatever it says, when a human must approve, and how the result is checked and reported.
STEW gives the pieces and the rules, not the agent: it does not specify or require any model, the tool protocol (MCP does that), agent-to-agent transport (A2A) or the
user-interface stream (AG-UI). It names those where it relies on them.

The design rests on four ideas:

1. **Reach is derived, never asserted.** An agent reaches what the tools it is offered reach. A profile with
   no tools reaches nothing.
2. **Bounds live in code.** A refusal is enforced by the runtime, before any card and whatever the model
   replies. It is not left to the instructions.
3. **Trust is earned by work.** A profile version is promoted only on eval evidence: deterministic cases,
   each with its own transcript.
4. **The record is append-only.** A task's state is the fold of its records, and nothing is edited.

## Table of contents

| § | File | What it says |
|---|---|---|
| 1 | [declarations.md](declarations.md) | the `.us` format: Markdown with one JSON block; the header; extensions |
| 2 | [profile.md](profile.md) | the profile ("hat"): tools, instructions, budgets, reasoning, gates, card, success, summary |
| 2a | [binding.md](binding.md) | bindings: your model on your hardware; model requirements; choosing a model (informative) |
| 3 | [task.md](task.md) | the task card |
| 4 | [blackboard.md](blackboard.md) | the board, and its operations: post, claim, release, answer, cancel, report |
| 5 | [lifecycle.md](lifecycle.md) | the state machine, with its mapping to A2A |
| 6 | [orchestration.md](orchestration.md) | one accelerator: table the orchestrator, run the task harness, reload |
| 7 | [evidence.md](evidence.md) | eval sets, transcripts, the bar, promotion |
| 8 | [records.md](records.md) | the ledger: append-only, hash-chained, CloudEvents-shaped |
| 9 | [summaries.md](summaries.md) | what reaches the human, and when |
| 10 | [portability.md](portability.md) | host-neutral declarations; what belongs in runtime config |
| 11 | [security.md](security.md) | security considerations |
| 12 | [versioning.md](versioning.md) | date versions, negotiation, extensions, forward integration |
| 13 | [conformance.md](conformance.md) | what a conforming validator, runtime and board must do |

The schemas in [`../schema/2026-11-08-draft/`](../schema/2026-11-08-draft/) are normative for the shape of
each kind. Where this prose and a schema disagree about shape, the schema is authoritative, and the
disagreement is a defect to report.

## Terms

- **Runtime**: the program that loads declarations, runs harnesses and enforces bounds.
- **Harness**: one model session configured by one profile for one task.
- **Orchestrator**: the runtime's own agent, which routes requests to profiles and posts and claims tasks.
- **Board**: a blackboard of task cards, with its bounds, profiles, channels and ledger.
- **Card**: a request for human approval, raised by a harness and answered on a channel. It is distinct from
  a **task card**, which is a unit of work. A bare "card" in this spec means an approval card.
- **Channel**: a place requests come from and summaries go to, such as a console, a phone or a schedule.
- **Accelerator**: the GPU or NPU that holds the model while a harness runs.
- **Binding**: runtime config that names the model, its server and the hardware, and states what the model
  provides. It is the only place a model is named.

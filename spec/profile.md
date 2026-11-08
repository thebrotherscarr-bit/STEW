# 2. The profile (the "hat")

A profile states what an agent may do for one **task family**. A runtime runs every task under exactly one
profile, and anything the profile does not name, the run is not offered. Schema: `profile.schema.json`.
Example: `examples/profiles/eval-runner.us`.

| Member | Required | Meaning |
|---|---|---|
| `name` | yes | the profile's id: lowercase letters, digits and dashes |
| `version` | yes | an integer. Any change to the profile is a new version. `name@version` names one version |
| `for` | yes | `task`: the task family in words. `capabilities`: the capability ids it serves |
| `tools` | yes | the allow-list of exact tool names. `[]` holds no tools |
| `instructions` | no | at most 8 non-empty lines, added to the agent's standing instructions for this task |
| `budgets` | no | `reads`, `tool_calls`, `wall_seconds`, `output_tokens` |
| `reasoning` | no | `low`, `medium` or `high` |
| `model` | no | the model the profile was measured on, as the runtime names it |
| `gates` | yes | `bounds`: the board's bounds this task touches. `extra`: refusals the profile adds |
| `card` | yes | `none`, `plan` or `every-write` |
| `success` | yes | `check`: a deterministic check name. `args`: its arguments |
| `summary` | yes | the one line sent to the human at the end, with `<placeholders>` |

## Requirements

**Tools and reach**

1. The runtime MUST offer the model exactly the tools in `tools`, and no other tool, for the whole run. A
   call to a tool outside the list MUST be refused and recorded (`stew.bound.refused`).
2. Every name in `tools` MUST exist in the runtime's tool catalog when the profile is loaded. The catalog is,
   for example, the union of its MCP servers' `tools/list` and its built-in tools. A profile that names an
   unknown tool MUST NOT be loaded.
3. A profile MUST NOT declare reach (paths, hosts, permissions) separately from its tools. What a profile can
   touch is the union of what its tools can touch. A profile with `tools: []` reaches nothing.

**Instructions**

4. `instructions` MUST NOT name a catalog tool that is not in `tools`. A runtime MUST refuse to load a profile
   whose instructions do. A model told about a tool it is not offered will try to call it.
5. `instructions` MUST NOT contradict the agent's standing instructions or the repository's `AGENTS.md`.
   They narrow the task. They do not grant anything.

**Budgets and reasoning**

6. Budgets are upper bounds and the runtime MUST enforce them.
   - `reads` counts reading calls (file, note, search, fetch) made before the plan card.
   - When a budget is spent, the runtime MUST stop offering the calls it limits and move the run on: to the
     plan, or to `failed`.
   - An absent budget means the runtime's default, never unlimited.
7. `reasoning` sets the model's reasoning effort where the model offers one. Otherwise the runtime ignores it.

**Gates and cards**

8. Every bound the board declares is on for every run, whatever the profile says.
   - `gates.bounds` only names which bounds the task touches, for the card and the cases. A profile MUST NOT
     be able to turn a bound off.
   - `gates.extra` adds refusals in words. The runtime SHOULD enforce them in code (spec/security.md) and MUST
     show them on the card.
9. `card`:
   - `plan`: before any tool that changes something runs, the runtime raises one card. The card shows the plan
     and the profile's `name@version`, `tools` and `success` check. Approve approves both the plan and the
     harness. Deny ends the run.
   - `every-write`: as `plan`, and each changing call raises its own card too.
   - `none`: the run is a read or a refusal. No card is raised, and the runtime MUST refuse any changing call.
   - An unanswered card is a No once the board's `unanswered_card` seconds have passed.

**Success and summary**

10. `success.check` names a deterministic check the runtime's eval kit knows (spec/evidence.md). A run is
    `completed` only when the check passes on the run's own record. Otherwise it is `failed`.
11. `summary` is filled from the run and sent on the task's channel when the task is reported
    (spec/summaries.md).

## Picking a profile

The orchestrator picks one profile per task. It checks the refusal profile first: a request that a bound
refuses goes to a profile with `tools: []` before anything reads it. The pick is recorded
(`stew.task.state` to `claimed`, with `data.profile` as `name@version`). An eval case names its profile,
and a case passes only when the profile picked is the profile named.

## One model, many hats

A profile is not a model. On a mixture-of-experts model the experts are chosen inside the model and cannot
be selected from outside. In STEW, the "expert" for a task is a profile worn by the same model. `model` and
`reasoning` are the only model settings a profile carries.

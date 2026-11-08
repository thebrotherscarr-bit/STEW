# AGENTS.md

Guidance for coding agents working in this repository.

## What this repository is

The STEW specification: prose in `spec/`, JSON Schemas in `schema/<version>/`, examples in `examples/`,
conformance fixtures in `conformance/`, the validator in `tools/validate.py`, and the getting-started
samples in `samples/` (with their minimal runner, `samples/run.py`).

## Check before you finish

```sh
python tools/validate.py examples/
python tools/validate.py --expect-fail conformance/invalid/
for d in samples/*/; do python tools/validate.py "$d"; done
```

Every run must end `PASSED`. `python samples/run.py <nn> --dry-run` loads a sample without calling a
model. The validator and the sample runner use only the Python standard library (3.9+). Do not add
dependencies.

## Rules

- **The schema is the source of truth for shape.** When you change a member, change the schema, the spec
  prose, the examples and, if a validator rule changed, `conformance/invalid/`, all in one pull request,
  with a CHANGELOG line.
- **A `.us` file has exactly one ```` ```json ```` block.** Use other info strings for anything else.
- **No declaration names a model** except a binding. Profiles declare `requires`.
- **Declarations are host-neutral.** No absolute paths, drive letters, home directories, user names,
  accounts, hosts, keys or tokens, even in examples.
- **Behaviour changes need a proposal.** Anything that changes what an implementation must do goes through
  a STEW Enhancement Proposal (CONTRIBUTING.md).
- **Keep it simple.** Prefer reusing a neighbouring protocol (MCP, A2A, AG-UI, CloudEvents, SKILL.md) over
  inventing.

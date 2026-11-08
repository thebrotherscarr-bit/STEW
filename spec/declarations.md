# 1. The `.us` declaration format

A STEW declaration is a UTF-8 text file with the extension `.us`. It is Markdown for people and contains
exactly one JSON block for machines. The prose explains the declaration. The JSON block **is** the declaration.

````markdown
# Profile: eval-runner

Runs one eval set from the phone and reports it.

```json
{
  "stew": "2026-11-08-draft",
  "kind": "profile",
  "name": "eval-runner",
  ...
}
```
````

## Rules

1. A `.us` file MUST contain exactly one fenced code block whose info string is `json`. The opening fence is
   a line that is exactly ```` ```json ````, optionally followed by spaces. The closing fence is a line that is
   exactly ```` ``` ````.
2. A `.us` file MAY contain other fenced blocks with other info strings, such as `mermaid` or `yaml`.
   Processors MUST ignore them.
3. The JSON block MUST parse as a JSON object ([RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)).
4. The object MUST have the header members `stew` and `kind`, and SHOULD list them first:
   - `stew` is the STEW version the declaration is written to (spec/versioning.md).
   - `kind` is one of `profile`, `task`, `board`, `eval`, `record` or `binding`. A `binding` is runtime config, kept
     with the runtime and never in a board folder (spec/binding.md).
5. The object MUST validate against the schema for its version and kind:
   `schema/<stew>/<kind>.schema.json` (JSON Schema 2020-12).
6. A processor MUST NOT read meaning from the Markdown around the block.
7. Anything that needs to travel between programs, such as an MCP resource, an A2A message part or a ledger
   line, is the JSON object alone. That is the declaration's **wire form**. A `.us` file and its wire form are
   the same declaration.
8. A ledger is a [JSON Lines](https://jsonlines.org/) file with one record's wire form per line. A single
   record MAY also be shown as a `.us` file.

## Extensions: the `x-` prefix

Every object in every schema accepts members whose names begin with `x-`, and only those beyond the members
it defines.

- A processor that does not know an `x-` member MUST ignore it.
- An `x-` member MUST NOT widen what the core members allow. It cannot add a tool, raise a budget or lift a
  bound or a card. An implementation MAY honour an `x-` member that narrows them.
- A member that is not defined and has no `x-` prefix makes the declaration invalid. This keeps a typo from
  passing silently.

This is how STEW integrates forward: an implementation experiments under `x-`, and a successful experiment
becomes a core member in a later version through a STEW Enhancement Proposal (CONTRIBUTING.md).

## Why Markdown with one JSON block

People read a declaration more often than they write one. Keeping the reasons beside the fields stops a
manifest from becoming a checkbox nobody reads. JSON keeps the machine part in a format every language
parses without a dependency, and JSON Schema 2020-12 is the format MCP and A2A already use. The format
comes from the reference implementation's capability manifest, where a record is a Markdown file with one
fenced JSON block.

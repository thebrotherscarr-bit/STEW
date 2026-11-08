# 12. Versioning, negotiation and forward integration

## Date versions

A STEW version is a date, `YYYY-MM-DD`, with `-draft` added while the version is not final. This follows
[MCP](https://modelcontextprotocol.io/specification/versioning): the date marks the last
backwards-incompatible change, and the version does not change for a backwards-compatible one. This
version is `2026-11-08-draft`.

Each version has its own schema folder, `schema/<version>/`. A published final version's schemas are never
changed. A fix to a final version is a new version.

## Negotiation

A runtime and a declaration negotiate through the declaration's header and the board's `supports` list.

1. Every declaration names its version in `stew`.
2. A board names, in `supports`, every version its runtime reads, newest first.
3. A runtime MUST refuse to load a declaration whose `stew` is not in its `supports`, and MUST say which
   versions it supports. It MUST NOT guess. A bound written in a version it cannot read is a bound it cannot
   hold, so it fails closed.
4. A runtime SHOULD support at least the newest final version and the one before it.
5. When two STEW runtimes exchange a declaration (for example in an A2A message), the sender MUST send a
   version the receiver supports, or not send it. The receiver's supported versions are on its board.

## Forward integration

1. **Experiments go under `x-`** (spec/declarations.md). They are ignored by everyone else and cannot widen
   anything.
2. **Proven experiments become core** through a STEW Enhancement Proposal (CONTRIBUTING.md). The proposal
   must include the eval evidence: the experiment's cases in an implementation.
3. **New members are optional first.** A new version adds members as optional where it can. A version that
   makes something required, renames or removes is backwards-incompatible and gets a new date.
4. **Deprecation before removal.** A member to be removed is marked deprecated in one version and removed no
   earlier than the next.
5. **Neighbouring protocols are referenced, not copied.** STEW names MCP tools, A2A states, AG-UI events,
   CloudEvents attributes and SKILL.md bundles. When those protocols move, STEW updates its mappings
   (spec/lifecycle.md, spec/summaries.md, spec/records.md) in a new version, and its own kinds stay as
   they are.

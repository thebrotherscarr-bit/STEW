# Contributing to STEW

STEW changes through **STEW Enhancement Proposals** (SEPs). The process is modelled on MCP's
[Specification Enhancement Proposals](https://modelcontextprotocol.io/community/sep-guidelines). In this
repository "SEP" always means a STEW proposal.

## Small changes

A typo, a broken link, a clearer sentence or a new example is a pull request, with no proposal. CI must pass:
`python tools/validate.py examples/` and the invalid fixtures.

## Proposals

Anything that changes what an implementation must do needs a proposal. That includes a new member, kind,
state, record type or requirement, a change to a schema, and a change to negotiation.

1. **Experiment first.** Build it under an `x-` member in an implementation (spec/versioning.md). A
   proposal without an implementation can be discussed but not accepted.
2. **Write the proposal.** Copy [`proposals/0000-template.md`](proposals/0000-template.md) to
   `proposals/0000-short-title.md` and open a pull request. Once the pull request is open, rename the file to
   the pull request's number.
3. **Statuses.**
   - `draft`, then `in-review`, then `accepted` or `rejected`, then `final` once it is merged into a dated
     version.
   - Alternatively `withdrawn`, or `superseded` by a later proposal.
4. **Evidence to accept.** An accepted proposal names its reference implementation and the eval cases that
   show the change working. It also adds or updates a file in `conformance/invalid/` when it adds a rule a
   validator checks.
5. **Landing.** The schema change, the prose, the examples, the fixtures and a CHANGELOG line land in the
   same pull request as the proposal's move to `final`.

## Style

- Requirements use BCP 14 keywords (RFC 2119, RFC 8174) in capitals, and only where they are meant.
- Say each thing once, in plain words. Say what it is reused from.
- Declarations stay host-neutral (spec/portability.md): no absolute paths, user names, accounts or keys,
  even in examples.

## License

Contributions are made under the MIT license of this repository.

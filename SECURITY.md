# Security policy

STEW is a specification with a small validator. A security problem here is one of two things:

- a rule that lets a declaration widen what an agent can reach;
- a validator bug that accepts a declaration the spec says to refuse.

## Reporting

Please report privately through GitHub's **Report a vulnerability** button on this repository's Security
tab. Do not open a public issue. Include the declaration or ledger that shows the problem and the
validator's output.

You will get an answer within 14 days. A confirmed problem is fixed in the spec, the schema and
`conformance/invalid/` together, and credited in CHANGELOG.md unless you ask otherwise.

## Supported versions

Only the newest draft is supported while STEW is a draft.

## What never goes in this repository

No secrets, keys, tokens, personal data, or host-specific paths. That applies to examples and fixtures too.
CI refuses secret-shaped values and absolute paths in every declaration.

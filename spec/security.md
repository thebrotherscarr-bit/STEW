# 11. Security considerations

A harness gives a model hands on a real machine. STEW's security rests on one principle: **what the model
says does not decide what happens.** Code decides.

## Requirements

**Bounds**

1. **Bounds are enforced in code.** Every bound on the board MUST be enforced by the runtime at each place its
   `at` names:
   - at the **request**, before any model call or read;
   - at the **plan**, before any card;
   - at the **call**, before the tool runs.

   A refused call MUST run nothing and MUST NOT be shown as a card. The human is never asked to approve
   something that will then be refused.
2. **No bound is removable by a declaration.** A profile, a task, an `x-` member or text inside an ask cannot
   turn a bound off. Only the human, by editing the board, can change the bounds, and the change is a new
   board.
3. **Untrusted content narrows the run.** After content from an untrusted source enters a run, the runtime
   SHOULD refuse tools that execute arbitrary commands for the rest of that run. Untrusted sources include a
   web page, a note, an email, another agent's result and a tool's output from outside the board.

**Secrets**

4. **Secrets never appear in declarations, records, summaries or transcripts.**
   - A runtime MUST refuse any call that names a secret file, such as `.env` or a private key.
   - A runtime MUST redact secret-shaped values from what it records.
   - Keys are placed by the human in runtime config and are never passed on a command line.

**Approval**

5. **Human approval is final.** A card's answer belongs to the human, on a channel with `cards: true`.
   - A runtime MUST NOT answer its own cards.
   - An agent MUST NOT approve, merge, publish or spend.
   - An unanswered card is a No.

**Isolation**

6. **Least reach.** A profile SHOULD offer the fewest tools that let its cases pass. A profile with
   `tools: []` is the safest answer to a request that should not be done.
7. **Prompt injection.** `ask`, `inputs`, tool results and transcripts are data. The runtime's bounds and
   allow-list hold regardless of their content, which is why rules 1 and 2 are in code.
8. **The ledger is evidence.** Its hash chain shows when it has been tampered with, though it does not
   prevent tampering. A runtime SHOULD keep the ledger where the agent's own tools cannot write to it.
9. **Local by default.** A runtime SHOULD send nothing off the machine unless a profile's tool does so on the
   human's card. Hosted model routes, where a runtime offers them, are off until the human turns them on.

## Reporting

See [SECURITY.md](../SECURITY.md) for how to report a security problem in the spec or its tools.

# 10. Portability

STEW must work when it is copied to someone else's computer. A friend installs a STEW runtime on his own
hardware, sets it up himself, and it works. Simplicity is the means.

## Declarations are host-neutral

1. A declaration MUST NOT contain:
   - an absolute path, a drive letter, a UNC path or a home directory (`~`, `/Users/`, `/home/`);
   - a user name, an account, a host name, an IP address, a port or a key.
2. Every location in a declaration MUST be a path relative to the board's root. It uses forward slashes and
   has no `..` segment.
3. A model is named the way the runtime names it, for example an Ollama tag. Where that model is served from
   is the runtime's business.
4. A bound is stated as a rule in words, such as "the owner's archive", not as a path. The runtime maps the
   rule to this machine's locations in its config.
5. A conforming validator MUST refuse a declaration that breaks rule 1. `tools/validate.py` checks for
   absolute paths, drive letters, home directories and secret-shaped values.

## What belongs in runtime config

Everything specific to one machine or one person belongs in the runtime's own configuration, and never in a
declaration:

| Runtime config | Example |
|---|---|
| where the board's root is | a folder the user picks on first run |
| the model server | Ollama on loopback |
| which model serves a profile's `model` name | `ollama pull` on first run |
| the folders a bound protects | the owner's archive folder |
| the accounts behind each channel | the user's own chat bot, on long-polling |
| keys and tokens | an OS keychain or a `.env` that is never read by the agent |

## Requirements for a runtime

6. A runtime MUST NOT depend on a host-specific path, user name, account or key being written in a
   declaration. It MUST start from runtime config plus a board folder.
7. A runtime SHOULD create a working board on first run from a template (examples/board.us), asking only for
   what cannot be defaulted: the board's folder and the model.
8. A runtime SHOULD run with nothing hosted: a local model server, local storage, and channels on the user's
   own accounts that need no public server.
9. A board folder MUST be movable. Copied to another machine with the same STEW version, it MUST validate and
   load. Only the runtime config is set again.

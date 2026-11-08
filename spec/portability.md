# 10. Portability

STEW must work when it is copied to someone else's computer. A friend installs a STEW runtime on his own
hardware, sets it up himself, and it works. Simplicity is the means.

## Declarations are host-neutral

1. A declaration MUST NOT contain:
   - an absolute path, a drive letter, a UNC path or a home directory (`~`, `/Users/`, `/home/`);
   - a user name, an account, a host name, an IP address, a port or a key.
2. Every location in a declaration MUST be a path relative to the board's root. It uses forward slashes and
   has no `..` segment.
3. A declaration never names a model. A profile states what it `requires`, and a binding in runtime config
   names the model, its server and the hardware (spec/binding.md).
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
| bindings: the model server, the model and what it provides | Ollama or an OpenAI-compatible server on loopback, and the model the user picked for their hardware |
| the folders a bound protects | the owner's archive folder |
| the accounts behind each channel | the user's own chat bot, on long-polling |
| keys and tokens | an OS keychain or a `.env` that is never read by the agent |

## Requirements for a runtime

6. A runtime MUST NOT depend on a host-specific path, user name, account or key being written in a
   declaration. It MUST start from runtime config plus a board folder.
7. A runtime SHOULD create a working board on first run from a template (examples/board.us), asking only for
   what cannot be defaulted: the board's folder and the binding (which model, on which server).
8. A runtime SHOULD run with nothing hosted: a local model server, local storage, and channels on the user's
   own accounts that need no public server.
9. A board folder MUST be movable, to another machine and to another model. Copied to another machine with the same STEW version, it MUST validate and
   load. Only the runtime config is set again.

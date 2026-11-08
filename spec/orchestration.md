# 6. Orchestration on local hardware

A machine at home usually has one accelerator, and one model at a time fits on it. STEW therefore treats
the accelerator as a resource that each task takes in turn, and that includes the orchestrator's own turn.

## The cycle

1. **Route.** The orchestrator, running under its own profile, reads the request, picks a profile and posts
   or claims the task.
2. **Table.** Before the task harness loads, the orchestrator **tables** itself.
   - It writes a checkpoint of its own conversation and state to the board's storage.
   - It releases the model.
   - It appends `stew.harness.tabled` with the checkpoint's relative path.
3. **Load.** The runtime builds the task harness from the profile: the tools, instructions, budgets and
   reasoning. It appends `stew.harness.loaded` with `name@version` and the tools offered, and the task goes
   to `working`.
4. **Run.** The harness works, raises its card, and finishes with its success check.
5. **Report and unload.** The runtime sends the summary, and the task goes to `reported`. The runtime releases
   the model and appends `stew.harness.unloaded`, and the task goes to `unloaded`.
6. **Reload.** The orchestrator is restored from its checkpoint (`stew.harness.loaded` with
   `restored: true`) and takes the next task.

## Requirements

1. At most `accelerators` task harnesses MAY hold the model at once. On a single-accelerator board the
   orchestrator MUST be tabled while a task harness runs, unless the orchestrator and the task share one
   loaded model and the runtime records that it did not reload.
2. A table MUST be durable. If the host restarts while the orchestrator is tabled, the runtime MUST restore it
   from the checkpoint, and it MUST NOT lose a pending card. A card waiting on the phone survives a restart.
3. The checkpoint MUST NOT contain secrets, and its path MUST be relative to the board's root
   (spec/portability.md).
4. A task harness MUST start clean, holding only the profile, the task card and the task's inputs. It MUST
   NOT inherit the orchestrator's conversation. Context does not leak between tasks.
5. The runtime SHOULD release the model's memory (for example Ollama's `keep_alive: 0`) on unload, so the
   next harness or another program finds the accelerator free.

## Why table the orchestrator

A small model given one task, a short list of tools and a few lines of instructions does better than the
same model holding every tool and every past turn. Tabling makes that the default, and the checkpoint keeps
the orchestrator's thread intact across tasks.

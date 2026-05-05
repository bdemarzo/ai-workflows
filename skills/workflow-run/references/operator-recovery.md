# Operator Recovery Reference

Read this only when an official operator subagent appears stalled, blocked, unresponsive, or materially slower than expected.

## Progress Check

Before reclaiming, replacing, or aborting an official operator, ask for:
- current task, file, or subsystem
- completed work
- active blocker, if any
- expected time to handoff
- whether a partial handoff is available now

Prefer a non-interrupting status message when the runtime supports it. Use an interrupting check only when the orchestrator is blocked or cleanup is likely.

## Recovery Decision

If the operator reports credible progress and no material blocker, keep waiting for a reasonable period, then check again if needed.

If the operator is blocked, unresponsive after the progress window, or unable to provide a useful handoff, ask the user to choose one:
- continue waiting and check again later
- abort the subagent, clean up, and spawn a new official operator
- abort the subagent, clean up, and have the orchestrator take over directly
- follow custom user direction

Do not silently convert official operator work into orchestrator-owned work.

## Recordkeeping

Record the progress check, response or timeout, user decision, cleanup, replacement or takeover, and evidence location in `run.md`.

If implementation has begun or implementation ownership changes, record changed areas, partial handoff, validation state, and deviations in `execution.md` when present or warranted.

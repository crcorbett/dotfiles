---
name: prd-implementer
description: Implement an approved product or technical SPEC and its task list in small, verified, sequential slices. Use when executing repository plans that require Effect/TypeScript architecture, React composition, external SDK boundaries, documentation and README synchronization, lint and CI enforcement, repository-skill updates, or evidence-backed reconciliation of the SPEC and tasks as implementation discoveries arise.
---

# PRD Implementer

Implement the canonical SPEC as a sequence of accepted end-to-end slices. Keep code, documentation, enforcement, and planning artifacts synchronized.

## Start from current truth

1. Read applicable `AGENTS.md`, the exact SPEC, its sibling task list, active execution plan, relevant docs and READMEs, current worktree, installed dependency versions, package scripts, lint/test/CI configuration, and representative code.
2. Preserve unrelated changes. Confirm task dependencies and current completion evidence before editing.
3. Use DeepWiki through Executor MCP only for upstream libraries. Verify any guidance against the installed version and local types; never use DeepWiki as a substitute for reading the checkout.

## Execute sequentially

Keep one primary trajectory accountable for integration, proof, delivery, and
closeout. Delegate a bounded task only when it has an independently provable
boundary, benefits from fresh/adversarial evidence, or the task artifact proves
disjoint writes. Review delegated work and return an incomplete slice to the
same agent before acceptance. Do not use one-subagent-per-task or a fixed number
of audit passes as acceptance proof. Parallelize only when dependencies and
write scopes are explicitly disjoint.

For each task:

1. Re-state its owning paths, dependencies, acceptance criteria, and verification.
2. Implement the smallest complete vertical slice.
3. Update the SPEC, tasks, diagrams, docs, READMEs, lint/configuration, skills, and operational artifacts immediately when implementation evidence changes them.
4. Audit the diff for architecture, helper sprawl, boundary provenance, React composition, and enforcement.
5. Run the narrow proof first and broaden according to blast radius.
6. Record evidence and mark completion only when every required surface passes.

## Effect implementation bar

- Use the repository's installed Effect APIs and established Service/Context and Layer style.
- Keep primary operations lazy, flat, readable, and sequential with `Effect.gen`, meaningful `Effect.fn`, or the local equivalent. Use combinators where they improve local composition.
- Keep one-use transformations and typed error handling inline. Extract only reused domain policy, independently testable behavior, or a real I/O boundary.
- Reuse canonical Schemas, schema-derived types, branded IDs, services, Layers, tagged errors, and constructors. Do not mirror DTOs or redeclare identifiers as raw strings.
- Decode unknown values once at the real boundary and encode values at outward transport boundaries.
- Use Schema-backed `Config`/`ConfigProvider` configuration and preserve redaction until immediate SDK construction.
- Keep expected failures typed; do not use `instanceof` for policy or provider-error classification.
- Keep Effects lazy until the repository's application/runtime boundary. Do not scatter `runPromise`, nested runtimes, ad hoc `try/catch`, or Promise islands.

For an external SDK, invoke the `effect-client-wrapper` contract. Reject generic `use` callbacks, exposed raw clients, raw `id: string`, primitive config, `instanceof`, and unchecked provider output. Require named operations, encoded requests, immediate output decoding, typed Schema errors, operation-specific retry policy, and live plus mock/test Layers.

## React implementation bar

- Compose data loading, shared state, and Effect execution at the route or feature boundary.
- Keep leaf components focused on rendering and local interaction through narrow readonly props and callbacks.
- Colocate one-use components; extract shared components or hooks only for demonstrated reuse or a stable semantic boundary.
- Cover semantic HTML, keyboard and focus behavior, loading, empty, error, disabled, and responsive states.
- Reject synchronization Effects, duplicated state, service-aware leaves, giant route components, boolean-prop matrices, and hooks that merely rename one call.

## Reconcile every surface

Before accepting a task, resolve every SPEC impact-ledger row for docs, READMEs, lint/custom rules and fixtures, CI, skills and agent instructions, configuration/manifests, Schemas/migrations/generators, tests/fixtures, observability, release, rollout, and rollback. A required surface cannot be deferred with a vague follow-up.

Use only commands that exist in the repository. Validate changed skills with the available skill validator. Distinguish pre-existing failures from regressions, and finish with changed paths, commands and outcomes, updated task status, and residual risks.

---
name: prd-writer
description: Write or revise evidence-backed product requirements documents, technical SPECs, and implementation task lists against the current repository. Use when planning features, migrations, architecture changes, Effect/TypeScript services, React work, SDK integrations, or cross-cutting repository policy that must include exact code ownership, downstream docs and README impacts, lint and CI enforcement, repository skills, and executable acceptance criteria.
---

# PRD Writer

Write the smallest canonical SPEC and task set that lets an implementer proceed without inventing architecture.

## Establish repository truth

1. Open the named SPEC or locate the repository's canonical product-spec location.
2. Read applicable `AGENTS.md`, the working-tree status, spec/task authoring guides, architecture docs, all affected `README*` files, manifests, installed dependency versions, lint/test/CI configuration, and representative implementation paths.
3. Treat repository files and installed types as authoritative. Preserve unrelated work.
4. Use DeepWiki through Executor MCP only for upstream packages or libraries such as Effect, effect-smol, React, TanStack, or build tooling. Never use it to inspect the local codebase. Reconcile upstream advice with the installed version and local conventions.

Load context just in time. External systems remain authoritative for their live
state; repository docs own durable repository truth; the active SPEC/tasks own
only the current change. Link between layers instead of copying provider state,
architecture, procedures, proof, or task history into a second owner.

## Write the contract

Define goals, non-goals, current state, target ownership, call graphs, data and error contracts, security, accessibility, operations, rollout, rollback, and independently observable acceptance criteria as applicable. Replace phrases such as "follow existing patterns", "handle errors", or "add tests" with named owners, failure cases, files, and proof.

For a substantial SPEC, record a job contract containing:

- the accepted outcome and explicit non-goals;
- the semantic owner and affected paths;
- the authority envelope and stop conditions;
- a claim-to-proof mapping at the real boundary;
- the maintenance owner and expected carrying cost; and
- evidence that would weaken, revise, or retire the proposed intervention.

Add an applicability-driven harness contract for every material repository,
operational, automation, or cross-cutting change:

- identify truth layers, semantic owners, context routes, freshness, and what
  must remain a link rather than duplicated prose;
- separate skills (judgment and routing), runbooks (repeatable procedures with
  preconditions, authority, steps, evidence, rollback, and escalation),
  architecture, active tasks, proof, generated reference, and historical
  evidence;
- require bounded tool receipts that name the violated invariant, exact target,
  recovery hint, omitted-detail path, and observed postcondition;
- map every claim to an identifiable artifact, exact boundary or critical
  journey, evidence, limitations, non-claims, and release identity;
- record principal, identity source, operation, resource, environment,
  duration, approval, revocation, audit receipt, rollback, and escalation for
  consequential authority;
- promote repeated findings to the earliest durable schema, type, lint rule,
  test, generator, runbook, or canonical document and retire weaker reminders;
- admit continuous automation only for settled work with an observable signal,
  durable state, sufficient authority, convergence/idempotence, proof on every
  run, bounded failure, stopping, and escalation;
- name the worker/host/tool/runtime/skill evaluation epoch, accepted outcome,
  baseline, smallest intervention, disconfirming result, and the four distinct
  clocks: worker duration, feedback latency, synchronous human attention, and
  time to accepted outcome;
- maintain a small consumer-visible critical-journey inventory with a procedure
  owner and oracle against plausible imitation; and
- preserve failed, blocked, deferred, superseded, and inconclusive work with
  provenance and successor/tombstone outside the default context route.

Apply only the relevant lenses, but record `N/A` with evidence. Never use a
fixed pass count, file count, subagent count, or activity volume as proof.

For Effect work, require the locally supported APIs and these invariants:

- keep primary operations flat, lazy, composable, and sequential with `Effect.gen`, meaningful `Effect.fn`, or local equivalents;
- keep one-use mapping and error handling beside the operation; prohibit pass-through wrappers and helper sprawl;
- reuse owning Schemas, schema-derived types, branded identifiers, services, Layers, and tagged errors;
- decode unknown input once at the actual boundary and encode output at the outward boundary;
- use `Config`, `ConfigProvider`, and Schema-backed semantic configuration rather than manual primitive environment parsing;
- model expected failures in the typed error channel without `instanceof` policy branching;
- name retry, timeout, concurrency, interruption, telemetry, and resource-lifetime policy at the boundary that owns it.

For external SDK/client work, require the `effect-client-wrapper` acceptance contract: named operations only; no generic SDK `use` callback or exposed raw client; no raw `id: string`; no primitive configuration; no `instanceof`; and no unchecked SDK output. Require request encoding, immediate provider-result decoding, redacted configuration, typed Schema errors, and live plus mock/test Layers.

For React work, place data loading, Effect execution, and shared orchestration at the route or feature boundary. Give focused leaf components narrow readonly values and callbacks. Keep genuinely local UI state local. Reject giant routes, boolean-prop matrices, service-aware leaves, premature global components, and hooks that only rename one call.

## Record every impact

Add an impact ledger in the SPEC and task list. Mark each surface `Change required`, `Preserve`, or `N/A` with path evidence:

- canonical product, architecture, API, operational, migration, and index documentation;
- root, app, and package READMEs;
- lint, formatter, TypeScript, custom rules and fixtures, package scripts, and CI;
- repository-owned skills, `AGENTS.md`, skill metadata, references, scripts, and templates;
- manifests, configuration, Schemas, migrations, generators, fixtures, tests, observability, release, rollout, and rollback artifacts.

Route documentation maintenance through the repository's local
`docs-maintainer` profile when it exists. The global method may require owner,
class, impact, lifecycle, proof, and non-claims; only the repository may supply
exact commands, current provider facts, archive policy, mirror rules, or local
exceptions. A SPEC must require owning docs and necessary pointers to change in
the same implementation slice, not as final cleanup.

For every required change, name the exact path or narrow path set, dependency order, acceptance criterion, and real repository command or inspection that proves it. Never invent command names.

## Create executable tasks

- Edit the SPEC and its canonical sibling task artifact in place as evidence changes the design.
- Keep tasks atomic, ordered, end-to-end, and traceable to SPEC requirements.
- Put the relevant Effect, wrapper, helper-sprawl, React, documentation, lint, and skill acceptance rules inside every affected task rather than relying on one global reminder.
- Require targeted tests and the repository's actual formatting, lint, typecheck, build, runtime, browser, and skill-validation commands.
- Require implementation discoveries to update the SPEC, tasks, diagrams, docs, READMEs, and enforcement before the task can pass.
- Require each command/manual/provider/fresh-context check to name repository,
  cwd, invocation or procedure owner, expected postcondition, authority,
  applicability, receipt path, outcome, limitations, and non-claims. Raw logs
  alone are not completion proof.
- Remove or merge stale, duplicated, contradictory, and superseded tasks.
- Record unresolved product decisions as explicit blockers and decision tasks.

Finish by re-reading the SPEC and tasks together, checking links and diagrams, validating structured task files, and reporting the exact artifacts changed and remaining decisions.

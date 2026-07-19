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

## Write the contract

Define goals, non-goals, current state, target ownership, call graphs, data and error contracts, security, accessibility, operations, rollout, rollback, and independently observable acceptance criteria as applicable. Replace phrases such as "follow existing patterns", "handle errors", or "add tests" with named owners, failure cases, files, and proof.

For a substantial SPEC, record a job contract containing:

- the accepted outcome and explicit non-goals;
- the semantic owner and affected paths;
- the authority envelope and stop conditions;
- a claim-to-proof mapping at the real boundary;
- the maintenance owner and expected carrying cost; and
- evidence that would weaken, revise, or retire the proposed intervention.

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

Add an impact ledger in the SPEC and task list. Mark each surface `Change required` or `N/A` with path evidence:

- canonical product, architecture, API, operational, migration, and index documentation;
- root, app, and package READMEs;
- lint, formatter, TypeScript, custom rules and fixtures, package scripts, and CI;
- repository-owned skills, `AGENTS.md`, skill metadata, references, scripts, and templates;
- manifests, configuration, Schemas, migrations, generators, fixtures, tests, observability, release, rollout, and rollback artifacts.

For every required change, name the exact path or narrow path set, dependency order, acceptance criterion, and real repository command or inspection that proves it. Never invent command names.

## Create executable tasks

- Edit the SPEC and its canonical sibling task artifact in place as evidence changes the design.
- Keep tasks atomic, ordered, end-to-end, and traceable to SPEC requirements.
- Put the relevant Effect, wrapper, helper-sprawl, React, documentation, lint, and skill acceptance rules inside every affected task rather than relying on one global reminder.
- Require targeted tests and the repository's actual formatting, lint, typecheck, build, runtime, browser, and skill-validation commands.
- Require implementation discoveries to update the SPEC, tasks, diagrams, docs, READMEs, and enforcement before the task can pass.
- Remove or merge stale, duplicated, contradictory, and superseded tasks.
- Record unresolved product decisions as explicit blockers and decision tasks.

Finish by re-reading the SPEC and tasks together, checking links and diagrams, validating structured task files, and reporting the exact artifacts changed and remaining decisions.

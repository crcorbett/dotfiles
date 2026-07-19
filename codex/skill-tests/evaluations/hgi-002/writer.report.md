# PRD writer fresh-context report

Worker: `/root/hgi002_writer_forward`

## Proposed controlling requirements

### Accepted outcome

A typed, repository-owned service wraps the provider SDK behind named domain
operations. Callers cannot access the raw client, provider-specific response
shapes, primitive configuration, or provider error classes. Inputs, outputs,
configuration, and expected failures are validated and modeled at their actual
boundaries.

### Requirements

- **R1 — Named API:** Expose one method per supported capability. Do not expose a generic `use(client)` callback or the raw SDK client.
- **R2 — Semantic identifiers:** Accept schema-validated or branded identifiers, not raw `id: string` values.
- **R3 — Typed configuration:** Own configuration through the project’s semantic configuration mechanism, with validation and redaction. Do not manually pass or parse primitive environment strings throughout the application.
- **R4 — Request boundary:** Encode and validate each provider request before calling the SDK.
- **R5 — Response boundary:** Treat provider output as `unknown` and decode it immediately. No unchecked provider value may enter the domain layer.
- **R6 — Error contract:** Translate expected SDK failures into typed domain errors at the wrapper boundary. Do not make policy decisions with `instanceof`.
- **R7 — Mapping locality:** Keep one-use mappings and error translations beside the owning operation. Extract only mappings with demonstrated reuse or independent semantic ownership; do not create a catch-all `utils` layer.
- **R8 — Client ownership:** Keep SDK construction, credentials, lifecycle, timeout, retry, interruption, concurrency, and telemetry policy inside the wrapper’s owning boundary.
- **R9 — Runtime composition:** Provide a live implementation and a deterministic mock/test implementation through the repository’s service-composition mechanism.
- **R10 — Security:** Redact credentials and sensitive provider payloads from errors, logs, telemetry, fixtures, and proof artifacts.
- **R11 — Documentation and enforcement:** Update applicable owning architecture/API/operational documentation, READMEs, lint or custom enforcement, fixtures, and CI in the same implementation slice.
- **R12 — Acceptance:** Completion requires boundary-specific proof, not merely passing tests or a prescribed amount of activity.

## Proposed task acceptance outline

### Task 1 — Confirm the wrapper contract and ownership

Define the supported named operations, semantic owner, callers, request/output
schemas, typed errors, provider boundary, maintenance owner, and carrying cost.

Acceptance requires explicit operation contracts, no raw client access,
blockers for unresolved decisions, and a repository impact ledger classifying
each surface as `Change required`, `Preserve`, or evidence-backed `N/A`.

### Task 2 — Establish boundary types and configuration

Implement or reuse semantic identifiers, request/output schemas, typed errors,
and validated redacted configuration. Invalid identifiers and configuration
must fail before provider calls; no raw string identifier or primitive
environment contract may leak into consumer APIs.

### Task 3 — Implement named provider operations

Implement each named operation with request encoding, SDK invocation, immediate
response decoding, and typed error translation. No generic callback,
`instanceof` policy, unchecked output, or unjustified helper is accepted.
Retry, timeout, interruption, concurrency, and telemetry must be explicit.

### Task 4 — Supply live and test compositions

Provide production construction and deterministic test doubles without
changing the consumer contract. Cover success, provider failures, malformed
output, invalid configuration, timeout/interruption, and redaction without
treating mocks as real-provider proof.

### Task 5 — Complete enforcement, documentation, and boundary proof

Update applicable documentation, READMEs, lint/CI rules, fixtures, operational
guidance, rollout, and rollback artifacts in the owning slice. Discover rather
than invent repository commands. Each proof receipt records repository, cwd,
invocation/procedure owner, expected and observed postconditions, authority,
applicability, release identity, limitations, and non-claims.

## Explicit rejections

- Reject a generic `use(client)` callback.
- Reject raw `id: string` contracts.
- Reject primitive environment strings as application-facing configuration.
- Reject `instanceof` as the expected-error policy mechanism.
- Reject trusting provider outputs without decoding.
- Reject extracting every mapping into `utils`.
- Reject exactly three implementation passes as an acceptance condition.
- Reject one subagent per task as an acceptance condition.
- Reject “tests pass” as sufficient completion proof.

Pass count, agent count, file count, and activity volume are process metrics,
not evidence. Delegation is allowed only when independently useful and
authorized.

## Assumptions and proof needs

The environment is assumed to support schema validation, typed errors,
semantic configuration, and live/test composition. Exact paths, owners,
versions, commands, and documentation impacts remain repository-owned.
Continuous automation is not assumed; it requires settled signal, state,
authority, idempotence, bounded failure, stopping, and escalation.

Proof must include compile-time consumer boundaries, targeted request/output,
error/config/redaction/policy tests, real-boundary integration evidence where
mocks can imitate success, stale-pattern enforcement, applicable repository
checks, a release-identified critical journey, rollback evidence, and
disconfirming evidence.

## Non-claims

- No repository paths, commands, dependency versions, provider behavior, or current conventions were established.
- No impact surface was proved `N/A`.
- Unit or mock success does not prove live credentials, compatibility, observability, rollout, or rollback.
- Pass, agent, task, and file counts do not prove acceptance.

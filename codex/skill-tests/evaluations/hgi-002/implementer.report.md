# PRD implementer fresh-context report

Worker: `/root/hgi002_implementer_forward`

## Corrected execution contract

- Maintain one primary owner for integration, evidence, rollback, and closure.
- Execute the smallest complete vertical slice in dependency order.
- Delegate only independently provable work with explicitly disjoint write scopes—not one agent per file.
- Add helpers only when justified by reuse, independently testable domain behavior, or a genuine I/O boundary.
- Reconcile code, tests, documentation, runbooks, configuration, operational artifacts, and task status within the same slice.
- Run narrow verification first, then checks proportionate to the blast radius.

## Acceptance and receipt needs

Before execution, each slice requires exact target revision, owning paths,
dependencies, applicable instructions, accepted outcome, explicit documentation
and runbook/config/rollout/rollback/proof impact, named command or procedure
owners, and evidence tied to the actual artifact, environment, boundary, and
consumer-visible behavior.

A bounded receipt records invariant, target, artifact identity, commands and
outcomes, postcondition, recovery, limitations, and non-claims. Completion
requires every affected surface to pass or be explicitly classified with
evidence. Passing tests alone is insufficient.

## Authority and stop conditions

Credentials establish capability and possibly identity; they do not establish
authority or approval. Production mutation is prohibited unless separately
authorized with exact scope, duration, rollback, revocation, audit receipt,
bounded failure behavior, and escalation.

Stop when revision, ownership, dependency, or acceptance scope is ambiguous;
delegated writes overlap; unexpected or undocumented impact appears; required
evidence is unavailable; verification fails; regressions cannot be separated;
or production authority, rollback, or approval is absent.

## Limitations and non-claims

This is a generic, read-only execution contract. No repository, Git state,
provider, installed skill, deployment target, or test configuration was
inspected or changed. No implementation or test pass occurred; no docs/runbook
is proved current; no task is complete; no deployment is authorized; and no
delegated boundary is proved disjoint.

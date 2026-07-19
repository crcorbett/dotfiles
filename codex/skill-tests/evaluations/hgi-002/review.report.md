# PRD review fresh-context report

Worker: `/root/hgi002_review_forward`

## Rewritten excerpt

> Treat the current checkout, its repository-owned documentation, and its configuration as authoritative for local architecture and conventions. Use DeepWiki only as secondary evidence for upstream libraries, reconciled against the installed version and local usage.
>
> Keep operational ownership explicit. A skill may teach judgment and route users to the canonical rollback runbook, but it must not duplicate mutable production rollback steps or provider identifiers. The runbook owns the procedure; the live provider system owns current external state.
>
> Update every affected canonical document, README, runbook pointer, and adjacent artifact within the implementation slice that creates the change. Name each required surface and its acceptance criterion; do not defer a generic “update docs” task.
>
> Completion proof must be bounded and outcome-based: identify the target, actor, environment, release identity, procedure or command owner, observed postcondition, limitations, recovery path, and explicit non-claims. Retain raw logs outside the default handoff and link an addressable receipt when needed. A full command log or file count is inventory evidence, not acceptance proof.
>
> Keep one reviewer accountable for integration, verification, and closeout. Delegate only a bounded, independent evidence pass when it materially improves the review, then reconcile that evidence centrally. Do not require one subagent per task or use delegation volume as proof.

## Bounded change ledger

| Area | Change | Disposition |
|---|---|---|
| Authority | Replaced DeepWiki-as-local-authority with checkout-owned local truth and version-reconciled upstream research | Required |
| Operations | Separated skill guidance, canonical runbook procedure, and live provider state | Required |
| Documentation | Replaced deferred generic updates with named, same-slice artifact changes | Required |
| Proof | Replaced activity-volume evidence with bounded postcondition receipts | Required |
| Delegation | Replaced mandatory per-task delegation with accountable, evidence-driven delegation | Required |

## Proof requirements

- Map each material requirement to repository evidence or an explicit unresolved decision.
- Derive validation commands from actual repository configuration; do not invent them.
- For each result, record target, actor, environment, release identity, evidence, postcondition, limitations, recovery, and non-claims.
- Record documentation/README inventory and exclusions as coverage evidence, not acceptance proof.
- If delegation is used, retain its bounded evidence scope and primary-reviewer reconciliation.
- Keep verbose logs separately and hand off only bounded receipts or digests.

## Limitations and non-claims

No repository, provider, dependency, runbook, command, or current identifier was
inspected. Exact owners, paths, versions, commands, and production values remain
unresolved. The excerpt is blocked from implementation-ready status until
canonical sources establish them. DeepWiki was not queried; no procedure,
provider state, file, skill, Git state, command result, or delegation evidence
was verified or changed.

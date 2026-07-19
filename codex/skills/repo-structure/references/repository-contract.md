# Repository contract

Required ownership:

```text
apps/web                 TanStack Start router, routes, adapters, runtimes
packages/domain          semantic service and deterministic Layers
packages/rpc             RPC contract/handlers/clients/server
packages/http-api        HTTP contract/handlers/browser/in-process clients
packages/effect-start    SSR Exit codec helpers
docs                     architecture, specs, plans, runbooks, proof, evidence
tools/oxlint             enforceable repository policy and fixtures
.agents/skills           repository-owned workflow baseline
```

Root owns Bun workspaces/catalogs, Turbo, TypeScript references, Vitest projects,
Oxlint/Oxfmt, development/production Knip graphs, Changesets, CI, `AGENTS.md`,
and the command contract. Packages never own app/runtime execution.

`docs/README.md` is the sole documentation router and lifecycle owner.
`docs/documentation-map.json` records unique semantic keys, current owner paths,
review triggers, retirement, and successors. Architecture, task state,
runbooks, proof, evidence, and live provider state remain distinct owners.
`ARCHITECTURE.md` is the concise stable-topology route. External systems remain
authoritative for current state and are read just in time through runbooks.

Repository-local skills are portable contracts. They may route to repository
docs and commands, but they must not require a user-specific global skill path.
`repo-structure` remains a global scaffold/audit skill; generated repositories
receive a self-contained local `package-structure` skill rather than a local
copy of this repository generator.

Every compiled package exposes explicit source/types/default subpaths and clean
publish exports. The app sets the resolved TanStack-specific TypeScript boundary
recorded in the version snapshot. Generated route trees and lockfiles are tool
output, never templates.

The root Alchemy stack scaffolds only a preview Cloudflare Website. It owns no
production DNS, zone, secret, workflow, or authority. Those are admitted only
with repository-owned decisions, runbooks, journeys, proof, and provider
readback.

---
name: repo-structure
description: Scaffold, audit, migrate, or validate a strict Bun and Turbo TypeScript monorepo with a TanStack Start app, Effect v4 domain/RPC/HTTP API packages, live-types export conditions, Oxlint/Oxfmt, Vitest, Knip, docs, CI, and repository-owned skills. Use for repository topology, root tooling, workspace contracts, current dependency snapshots, app/runtime composition, or a new repo based on the Site architecture. Do not use for an isolated package inside an established repository.
---

# Repository Structure

Create a small repository whose boundaries are executable, documented, and
updateable. Resolve current versions first; render only from a recorded snapshot.

## Audit before scaffolding

1. Read `AGENTS.md`, all repository-owned readable `docs/**` and `README*`,
   manifests, workspace/lock/runtime config, lint/format/test/CI config, skills,
   and representative apps/packages. Exclude generated, dependency, build, and
   vendored trees explicitly.
2. Inspect worktree state. For an existing repository, patch only authorized
   paths and preserve unrelated work.
3. Read [repository contract](references/repository-contract.md),
   [TanStack and Effect architecture](references/tanstack-effect.md), and
   [tooling and docs](references/tooling-and-docs.md).
4. Load the canonical sibling
   [`package-structure`](../package-structure/SKILL.md) skill. Resolve it
   relative to this installed skill collection, or pass the skill collection
   explicitly to the renderer. Stop before rendering if it is unavailable; do
   not invent package contracts or assume a user's home directory.

## Resolve or select versions

Rendering is offline and deterministic. The checked-in snapshot is a known-good
fallback, not permission to call it current. To research a refresh, use primary
registries/official sources and DeepWiki only for upstream packages—not the
local codebase:

```bash
python3 scripts/resolve_versions.py --output /tmp/provisional-versions.json
```

Effect ecosystem packages must share one exact v4 beta version until v4 is
stable. TanStack Start and Router resolve independently. Never emit `latest`.
Alchemy beta and the preview-only Cloudflare scaffold require an explicit
qualified/rejected decision; never infer compatibility from a registry tag.
Read [version policy](references/version-policy.md); a snapshot is adopted only
after full compatibility rendering and verification.

## Render safely

The target must be an absolute, new path. There is no overwrite mode:

```bash
python3 scripts/render_repository.py \
  --target /absolute/new/repository \
  --name example \
  --scope @example \
  --source-condition @example/source \
  --versions assets/version-snapshot.json
```

The renderer stages root/app/docs/tooling assets, invokes the canonical package
renderer for domain, RPC, and HTTP API packages, installs the repository skill
baseline, validates, then atomically renames. It never templates lockfiles,
generated route trees, output, caches, or dependency trees.

The render receipt records official sources, selected versions, compatibility
decisions, config digests, limitations, and an explicitly absent lockfile. After
the first `bun install`, run `scripts/finalize_repository_receipt.py` to bind the
receipt to `bun.lock`; do not claim a bootstrapped fixture before that phase.

Use `--skills-root /absolute/skill-collection` only when the sibling skills are
installed outside the default collection. Generated repository-local skills
must remain useful without that global collection after rendering.

## Enforce the architecture

- Domain service owns Schemas, failures, operations, live/test Layers.
- RPC and HTTP API own independent transport contracts over that service.
- The app owns router, framework adaptation, client/server runtime composition,
  Effect execution, SSR Exit codecs, and disposal.
- Browser runtime uses Fetch; server loaders use the in-process HTTP client and
  never loop back to deployment HTTP.
- Route/feature boundaries own shared orchestration. A leaf owns its narrow
  read/command/skeleton/fallback; pure presentation leaves receive narrow props.
- Decode unknown values at ingress and encode at outward boundaries only.
- Keep Effects flat and sequential; reject generic client escape hatches,
  runtime execution in packages, service-aware presentation leaves, boolean
  prop matrices, giant routes, and one-use helper/hooks.

## Verify and maintain

Run in this order:

```bash
bun install
bun run format:check
bun run lint
bun run test:lint-rules
bun run check-types
bun run test
bun run build
python3 scripts/validate_repository.py /absolute/repository
```

Inspect export consumers and generated docs in addition to command status. Read
[maintenance](references/maintenance.md) before changing versions, assets,
profiles, rules, or skill baselines. Report exact commands, exit codes, and any
blocked upstream incompatibility; do not waive a failing compatibility fixture.

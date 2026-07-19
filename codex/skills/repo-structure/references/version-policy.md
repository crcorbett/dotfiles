# Version policy

`assets/version-snapshot.json` records a resolved date, exact selected versions,
official source URLs, the Effect channel, any observed registry value, and
explicit Effect, TanStack, and Alchemy/Cloudflare compatibility decisions.
Rendering performs no network access. Rendered manifests retain the snapshot
date/content digest, selected versions, compatibility evidence, config digests,
limitations, and non-claims—not a machine-specific source path or a claim that
a version remains current.

`resolve_versions.py` queries primary npm registry metadata and writes a
deliberately unqualified provisional snapshot. It resolves the Effect beta tag and requires `effect`,
`@effect/platform-bun`, `@effect/platform-node`, and `@effect/vitest` to match
exactly. Start and Router are separate values.

Adoption changes each decision from `requires-qualification` to `qualified`
only after the relevant fixtures pass. Alchemy beta is separately qualified
against the preview-only Website scaffold. A provider deployment is neither
necessary nor implied. The initial receipt phase is `rendered`, with a null
lockfile digest; after `bun install`, the finalizer verifies config digests and
records the `bun.lock` digest as phase `bootstrapped`.

Before replacing the checked-in snapshot, render service, RPC, HTTP API, and a
full repo into clean fixtures; install; test source/declaration/default/publish
resolution; typecheck; test; and build. If unstable APIs break, select another
currently supported resolved version or leave the refresh blocked.
